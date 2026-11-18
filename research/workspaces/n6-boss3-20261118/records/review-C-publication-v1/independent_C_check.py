"""Non-author C review. Reconstruct columns directly from one-customer payoffs.

This checker does not import either author generator while building or verifying
the systems. Bit zero denotes E, bits one through four denote the four F sets;
its client-column order deliberately differs from the author product ordering.
The optional final comparison imports only the frozen canonical replay module,
after all independent exact dual checks have succeeded, and never calls main.
"""
from fractions import Fraction as R
from itertools import product, permutations, combinations_with_replacement
from functools import lru_cache
from pathlib import Path
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[5]
OUT = Path(__file__).resolve().parent
EVIDENCE = ROOT / 'tools/evidence/six-five-extra-C-prefix'
FREEZE = ROOT / 'research/runs/n6-boss3-20261118/studio/freezes/boss3-C-publication-v1/3c2d3dbeb69959f860939853073407a870db5775df38f012de8ff155bb55a60e.json'
FPAIRS = [(i, j) for i in range(4) for j in range(4) if i != j]
PERMS = list(permutations(range(4)))
CUSTOMERS = [(block, mask) for block in range(7) for mask in range(32)
             if block != 6 or mask != 0]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def transform(pattern, pi):
    return tuple(FPAIRS.index((pi[FPAIRS[p][0]], pi[FPAIRS[p][1]]))
                 for p in pattern)


def orbit_key(pattern):
    return min(tuple(sorted(transform(pattern, pi))) for pi in PERMS)


@lru_cache(None)
def local_column(branch, pair_index, block, mask):
    # A single actual client, in the same original catalog and same four-prefix.
    flags = tuple((mask >> i) & 1 for i in range(5))
    members = tuple(int(block == i) for i in range(6)) + flags
    before_tail = 2 * flags[0] + int(block == 5) + int(block == branch)
    a, y = FPAIRS[pair_index]
    ma, my = flags[1 + a], flags[1 + y]
    final_load = before_tail + ma + my
    ua = R(ma, final_load) if ma else R(0)
    uy = R(my, final_load) if my else R(0)
    force = R(1, final_load) if block == branch else R(0)
    result = [force, -ua, -uy]
    for q in members:
        result.append(R(q, before_tail + ma + 1) - uy)
    for t in members:
        result.append(R(t, before_tail + 2) - ua)
    for k in range(5):
        if k == branch:
            continue
        other_new = block < 5 and block not in (branch, k)
        result.append(-ua - R(2, 3) * flags[0] * int(block == k)
                      - R(2, 9) * flags[0] * int(other_new))
    for t in flags[1:]:
        for q in flags[1:]:
            result.append(R(t, before_tail + 1)
                          + R(q, before_tail + t + 1) - ua)
    assert len(result) == 45
    return tuple(result)


def column(pattern, block, mask):
    flags = [(mask >> i) & 1 for i in range(5)]
    answer = flags + [flags[0] * int(block == j) for j in range(4)]
    for j, p in enumerate(pattern):
        answer.extend(local_column(j, p, block, mask))
    assert len(answer) == 189
    return answer


def rhs():
    branch = [R(0), -R(7, 12), -R(7, 12)] + [R(0)] * 22 + [-R(1)] * 4 + [R(1)] * 16
    return [R(1)] * 5 + [R(1, 2)] * 4 + branch * 4


def run():
    freeze = json.loads(FREEZE.read_text())
    read_refs = []
    for ref in freeze['content_refs']:
        actual = sha(ROOT / ref['path'])
        assert actual == ref['sha256'], ref
        read_refs.append(dict(ref))
    bundle = json.loads((EVIDENCE / 'C-all-orbit-rational-certificates.json').read_text())
    mapping = json.loads((EVIDENCE / 'C-1365-to-69-orbit-map.json').read_text())
    replay = json.loads((EVIDENCE / 'C-all-orbit-exact-replay.json').read_text())
    scan = json.loads((EVIDENCE / 'C-all-orbit-float-scan.json').read_text())
    assert not bundle['failures'] and not scan['failures']
    assert mapping['pairs'] == [list(p) for p in FPAIRS]
    modes = list(combinations_with_replacement(range(12), 4))
    representatives = sorted({orbit_key(mode) for mode in modes})
    assert len(modes) == 1365 and len(representatives) == 69
    assert mapping['representatives'] == [list(p) for p in representatives]
    assert len(mapping['mapping']) == 1365
    for mode, item in zip(modes, mapping['mapping']):
        key = orbit_key(mode)
        assert item['mode'] == list(mode)
        assert item['representative'] == representatives.index(key)
        pi, order = item['extra_permutation'], item['anchor_order']
        assert sorted(pi) == sorted(order) == list(range(4))
        renamed = transform(mode, pi)
        assert tuple(renamed[i] for i in order) == key
        # Verify the map's specified tie-breaking, not only existence.
        choices = []
        for p in PERMS:
            ren = transform(mode, p)
            ordering = tuple(sorted(range(4), key=lambda j: (ren[j], j)))
            choices.append((tuple(ren[j] for j in ordering), p, ordering))
        assert (key, tuple(pi), tuple(order)) == min(choices)
    # All 12^4 original ordered assignments have one of those sorted modes.
    multiplicities = {p: 0 for p in modes}
    for ordered in product(range(12), repeat=4):
        multiplicities[tuple(sorted(ordered))] += 1
    assert sum(multiplicities.values()) == 20736 and min(multiplicities.values()) > 0
    assert len(CUSTOMERS) == 223
    assert len(bundle['certificates']) == 69
    b = rhs()
    results = []
    independent_columns = {}
    for expected, cert in zip(representatives, bundle['certificates']):
        assert cert['mode'] == list(expected)
        indices = [int(i) for i, v in cert['inequality_dual']]
        assert len(indices) == len(set(indices)) and all(0 <= i < 189 for i in indices)
        lam = {int(i): R(v) for i, v in cert['inequality_dual']}
        assert all(v <= 0 for v in lam.values())
        eq = [R(v) for v in cert['equality_dual']]
        assert len(eq) == 6
        bound = sum((lam[i] * b[i] for i in lam), R(0)) + sum(eq)
        assert bound == R(cert['bound']) and bound >= R(1, 2)
        columns = [column(expected, block, mask) for block, mask in CUSTOMERS]
        gcol = [R(0)] * 189
        for j in range(4):
            gcol[9 + 45 * j] = -R(1)
        columns.append(gcol)
        independent_columns[expected] = columns
        reduced = []
        for c, vector in enumerate(columns):
            val = R(int(c == 223)) - sum((v * vector[i] for i, v in lam.items()), R(0))
            if c < 223 and CUSTOMERS[c][0] < 6:
                val -= eq[CUSTOMERS[c][0]]
            assert val >= 0, (expected, c, val)
            reduced.append(val)
        results.append({'mode': list(expected), 'bound': str(bound),
                        'minimum_reduced_cost': str(min(reduced)),
                        'zero_reduced_cost_columns': reduced.count(R(0)),
                        'nonzero_dual_rows': len(lam)})
    assert results == replay['summaries']
    # Actual frozen canonical-path replay in read-only import mode.
    spec = importlib.util.spec_from_file_location('frozen_C_replay', EVIDENCE / 'verify_C_all_orbits.py')
    author = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(author)
    author_replay = author.verify()
    assert author_replay == replay
    compared = 0
    our_index = {key: i for i, key in enumerate(CUSTOMERS)}
    for mode in representatives:
        A, ab, ae, _ = author.build(mode)
        assert ab == b
        for c, (block, flags) in enumerate(author.TYPES):
            mask = sum(int(v) << i for i, v in enumerate(flags))
            ours = independent_columns[mode][our_index[(block, mask)]]
            assert [r[c] for r in A] == ours
            assert [r[c] for r in ae] == [R(int(block == k)) for k in range(6)]
            compared += 189
        assert [r[223] for r in A] == independent_columns[mode][-1]
        assert all(r[223] == 0 for r in ae)
        compared += 189
    # Read and sanity check every diagnostic numeric record; not proof inputs.
    assert len(scan['float_results']) == 69
    for mode, record, exact in zip(representatives, scan['float_results'], results):
        assert record['mode'] == list(mode) and record['status'] == 0
        assert record['gamma'] >= .5 and abs(record['gamma'] - float(R(exact['bound']))) < 1e-7
    diagnostic_text = (EVIDENCE / 'C-all-orbit-discovery-summary.json').read_text()
    decoder = json.JSONDecoder()
    diagnostics = []
    while diagnostic_text.strip():
        obj, used = decoder.raw_decode(diagnostic_text.lstrip())
        diagnostics.append(obj)
        diagnostic_text = diagnostic_text.lstrip()[used:]
    assert len(diagnostics) == 3 and diagnostics[0]['failures'] == 0
    assert diagnostics[1]['certificates'] == 69 and diagnostics[1]['failures'] == []
    assert diagnostics[2]['minimum_dual_bound'] == '1001/1896'
    report = {'status': 'PASS', 'independent_model': 'columnwise one-client exact payoffs; no author imports before all dual checks passed',
              'ordered_assignments': 20736, 'multisets': 1365, 'orbits': 69,
              'client_types': 223, 'columns': 224, 'inequalities': 189, 'equalities': 6,
              'exact_dual_columns_verified': 69 * 224,
              'author_matrix_coefficients_compared': compared,
              'canonical_readonly_replay_matches_frozen': True,
              'minimum_bound': str(min(R(r['bound']) for r in results)),
              'freeze_content_refs_checked': len(read_refs), 'summaries': results}
    (OUT / 'independent-results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'summaries'}, indent=2))


if __name__ == '__main__':
    run()

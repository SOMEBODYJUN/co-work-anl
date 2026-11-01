"""Finite exact helper contracts, with no discover/main/LP invocation.

Compare the original hypergeometric evaluator to explicit index tuples, then
compare all 1905 coefficients to a raw-index construction on one frozen point.
The three fixed multiplier pairs are probes, not a continuous-family dual.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
from collections import defaultdict, Counter
from functools import lru_cache
from hashlib import sha256
import importlib.util
import json
import platform
import sys
import time

BETA = {1: F(1), 2: F(3, 2), 3: F(5, 3), 4: F(1499, 750)}
QUERIES = ('opt_subset', 'opt_include_i', 'opt_exclude_i', 'opt_include_ij')
MULTIPLIERS = ((F(), F()), (F(1, 3), F(2, 5)), (F(7, 5), F(3, 2)))


def ratio(numerator, denominator):
    if denominator == 0:
        assert numerator == 0
        return F()
    return F(numerator, denominator)


@lru_cache(None)
def compare_tuples(bits, ii, jj, r, b, t, query):
    slots = tuple(range(6))
    if query == 'opt_subset':
        tuples = tuple(combinations(slots, r))
    elif query == 'opt_include_i':
        tuples = tuple((ii,) + rest for rest in combinations(tuple(k for k in slots if k != ii), r - 1))
    elif query == 'opt_exclude_i':
        tuples = tuple(combinations(tuple(k for k in slots if k != ii), r))
    elif r == 1:
        tuples = ((ii,),)
    else:
        tuples = tuple((ii, jj) + rest for rest in combinations(tuple(k for k in slots if k not in (ii, jj)), r - 2))
    assert tuples and all(len(z) == r for z in tuples)
    return sum((ratio(sum(bits[k] for k in z), b + t + sum(bits[k] for k in z)) for z in tuples), F()) / len(tuples)


@lru_cache(None)
def envelope(b, ell, t, rc, r, alpha, gamma):
    values = [ratio(t - gamma * BETA[r] * z, b + t + z) + alpha * F(z, ell + 1) for z in range(r + 1)]
    return gamma * rc + min(values)


def main():
    if len(sys.argv) != 4:
        raise SystemExit('usage: helper-audit.py source.py point.json new-output.json')
    source, point_path, output = map(lambda x: Path(x).resolve(), sys.argv[1:])
    assert not output.exists()
    source_bytes = source.read_bytes()
    point_bytes = point_path.read_bytes()
    assert sha256(source_bytes).hexdigest() == '9f812b0381186aa8546a038416b6335424673cbf1f895e8da40f7b6f4baadfdc'
    assert sha256(point_bytes).hexdigest() == 'abac45f78980d02f2bd056758a96653aa0bc0d8b87571820a5742397dc490246'
    spec = importlib.util.spec_from_file_location('frozen_tail_reply_subset_contract_only', source)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    point = json.loads(point_bytes)
    cols = point['columns']
    weights = [F(c['weight']) for c in cols]
    assert len(cols) == 1905
    started = time.monotonic()
    local_keys = set()
    tuple_checks = 0
    for bits in product((0, 1), repeat=6):
        for ii, jj in ((0, 0), (0, 1)):
            for r in range(1, 5):
                for b, t, q in product(range(6 - r), (0, 1), QUERIES):
                    got = old.comp_rc(q, sum(bits), b, t, r, (0,) * 6, (bits[ii], 0, 0), (bits[jj], 0, 0), int(ii == jj))
                    expected = compare_tuples(bits, ii, jj, r, b, t, q)
                    assert got == expected
                    tuple_checks += 1
                    local_keys.add((sum(bits), bits[ii], bits[jj], int(ii == jj), r, b, t, q))
    fallback = 0
    # These helpers exist in the source but are not in its four discovery queries.
    a = (0, 1, 0, 1, 1, 0)
    wi, wj = (0, 1, 0), (1, 0, 1)
    for r, b, t in product(range(1, 5), range(5), (0, 1)):
        for q, bit in [('self', t)] + [(f'actual{k}', a[k]) for k in range(6)] + [(f'wi{k}', wi[k]) for k in range(3)] + [(f'wj{k}', wj[k]) for k in range(3)]:
            assert old.comp_rc(q, 1, b, t, r, a, wi, wj, 0) == ratio(r * bit, b + t + r * bit)
            fallback += 1
    histograms = []
    active = None
    for j, col in enumerate(cols):
        if col['kind'] == 'hist':
            words = tuple(word for word, count in zip(product((0, 1), repeat=3), col['hist']) for _ in range(count))
            assert len(words) == 6 and sum(w[0] for w in words) == col['d']
            active = {'hi': j, 'col': col, 'words': words, 'groups': {}}
            histograms.append(active)
        elif col['kind'] == 'joint-reply':
            f, diag, wi, wj = col['group']
            key = (f, diag, tuple(wi), tuple(wj))
            active['groups'].setdefault(key, {})[tuple(col['state'])] = j
    row_records = []
    original_states_calls = original_rows_calls = coefficient_comparisons = 0
    for i, member, orb, query in product(range(1, 5), (0, 1), ((0, 0), (1, 0), (1, 1)), QUERIES):
        r = 5 - i
        cut = {'i': i, 'member': member, 'orb': list(orb), 'q': query}
        st = defaultdict(F)
        ui = u6 = F()
        rows = [[F()] * len(cols) for _ in MULTIPLIERS]
        for hist in histograms:
            hi, col, words = hist['hi'], hist['col'], hist['words']
            a = tuple(map(int, col['actual_bits']))
            b, ell, total = sum(a[:i]), sum(a[:5]), sum(a)
            own, final = ratio(a[i], total), ratio(a[5], total)
            hm = weights[hi]
            ui += hm * own
            u6 += hm * final
            for rr, (alpha, gamma) in zip(rows, MULTIPLIERS):
                rr[hi] = own + r * alpha * final
            # Enumerate original labelled indices, never histogram multiplicities.
            index_pairs = [(x, y) for x, y in product(range(6), repeat=2) if (x == y) == bool(orb[1])]
            denominator = len(index_pairs)
            assert denominator == (6 if orb[1] else 30)
            bits = tuple(w[0] for w in words)
            for x, y in index_pairs:
                group = (orb[0], orb[1], words[x], words[y])
                stored = hist['groups'][group]
                on = sum((weights[j] for state, j in stored.items() if state[member]), F())
                assert 0 <= on <= hm
                rcs = [compare_tuples(bits, x, y, r, b, t, query) for t in (0, 1)]
                for t, mass in ((0, hm - on), (1, on)):
                    st[b, ell, t, rcs[t]] += mass / denominator
                for rr, (alpha, gamma) in zip(rows, MULTIPLIERS):
                    values = [envelope(b, ell, t, rcs[t], r, alpha, gamma) for t in (0, 1)]
                    rr[hi] -= values[0] / denominator
                    for state, j in stored.items():
                        if state[member]:
                            rr[j] += (values[0] - values[1]) / denominator
        st = {k: v for k, v in st.items() if v}
        got_st, got_ui, got_u6 = old.states(point, cut)
        original_states_calls += 1
        assert (got_st, got_ui, got_u6) == (st, ui, u6)
        assert sum(st.values()) == sum(weights[h['hi']] for h in histograms) == 1
        for expected, (alpha, gamma) in zip(rows, MULTIPLIERS):
            chosen = {**cut, 'alpha': str(alpha), 'gamma': str(gamma)}
            got = old.coefficient_rows(cols, chosen)
            original_rows_calls += 1
            assert got == expected
            coefficient_comparisons += len(cols)
            value = sum((c * w for c, w in zip(got, weights)), F())
            direct = ui + r * alpha * u6 - sum((w * envelope(*k, r, alpha, gamma) for k, w in st.items()), F())
            assert value == direct
            assert all(c == 0 for c, col in zip(got, cols) if col['kind'] in ('K', 'overlap'))
            row_records.append({**chosen, 'slack': str(value), 'nonzero_coefficients': sum(c != 0 for c in got)})
    assert original_states_calls == 96 and original_rows_calls == 288
    assert source.read_bytes() == source_bytes and point_path.read_bytes() == point_bytes
    report = {
        'status': 'PASS_FINITE_EXACT_ORIGINAL_HELPER_CONTRACTS',
        'scope': 'Original helpers versus explicit labelled tuples and full coefficient arrays; 96 structures at three fixed nonnegative multiplier pairs only. No main, discover, optimization, original 5075 verification or continuous-family nonseparation certificate.',
        'python': platform.python_version(), 'elapsed_seconds': time.monotonic() - started,
        'source_sha256': sha256(source_bytes).hexdigest(), 'point_sha256': sha256(point_bytes).hexdigest(),
        'audit_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'explicit_tuple_comparison_checks': tuple_checks, 'distinct_hypergeometric_input_states': len(local_keys),
        'fallback_repeated_query_checks': fallback, 'original_states_calls': original_states_calls,
        'original_coefficient_rows_calls': original_rows_calls, 'exact_coefficient_equalities': coefficient_comparisons,
        'state_mass_one_in_all_96_structures': True, 'input_and_source_bytes_unchanged': True,
        'multiplier_probes': [[str(a), str(g)] for a, g in MULTIPLIERS],
        'sampled_slack_signs': dict(Counter('negative' if F(z['slack']) < 0 else 'zero' if F(z['slack']) == 0 else 'positive' for z in row_records)),
        'main_calls': 0, 'discover_calls': 0, 'linprog_calls': 0,
        'sampled_rows': row_records,
    }
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'sampled_rows'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

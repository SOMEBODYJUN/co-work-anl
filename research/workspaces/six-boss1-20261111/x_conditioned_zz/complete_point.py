"""Exact fixed-core completion once Main supplies a NEW rational point.

No solver, support search, rational recovery, or input mutation is performed.
The default command opens no point.  --self-check uses an explicitly synthetic
vector only.  A real invocation requires both an exact file and its supplied
SHA256; all outputs are confined to a fresh subdirectory of this owned folder.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json
import re

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
MATRIX = WORK/'common_x_joint_lp/final/exact_matrix.json.gz'
MATRIX_SHA = '1b4a4e544e5b9eeea1fa64b3849a9d4cc532b997a5ad972ce33df81c224551e7'


def digest(path): return sha256(path.read_bytes()).hexdigest()


def read(path):
    with gzip.open(path, 'rt', encoding='utf-8') if path.suffix == '.gz' else path.open() as f:
        return json.load(f)


def write(out, name, value):
    path = out/name
    assert HERE in path.resolve().parents and not path.exists()
    data = json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()
    if path.suffix == '.gz':
        with path.open('wb') as stream:
            with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as gz:
                gz.write(data)
    else:
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


@lru_cache(maxsize=None)
def rat(value): return F(value)


def dot(row, values):
    return sum((rat(a)*values[j] for j, a in row if values[j]), F())


def encode(row): return [[j, str(a)] for j, a in sorted(row.items()) if a]


def load_contract(require_freeze=True):
    assert digest(MATRIX) == MATRIX_SHA
    manifest = read(HERE/'build_manifest.json')
    assert manifest['matrix_sha256'] == MATRIX_SHA
    for item in manifest['products']:
        assert digest(HERE/item['path']) == item['sha256']
    audit = read(HERE/'independent_audit.json')
    assert audit['status'] == 'PASS_INDEPENDENT_SYMBOLIC_INTERFACE'
    assert audit['build_manifest_sha256'] == digest(HERE/'build_manifest.json')
    assert audit['verifier_sha256'] == digest(HERE/'verify_interface.py')
    if require_freeze:
        freeze = read(HERE/'freeze_manifest.json')
        assert freeze['status'] == 'FROZEN_WAITING_FOR_NEW_EXACT_POINT'
        assert freeze['matrix_sha256'] == MATRIX_SHA
        for item in freeze['files']:
            assert digest(HERE/item['path']) == item['sha256']
    matrix = read(MATRIX)
    interface = read(HERE/'column_interface.json')
    layer = read(HERE/'conditioned_upper_rows.json')
    sign = read(HERE/'old_aux_sign_audit.json')
    assert (len(matrix['rows']), len(matrix['columns'])) == (23676, 21021)
    assert interface['core_columns'] == list(range(4849))+list(range(15593, 21021))
    assert interface['real_overlap_core_columns'] == list(range(20601, 21021))
    assert len(interface['blocks']) == 2790 and len(layer['rows']) == 5580
    return matrix, interface, layer, sign


def canonicalize(values, interface):
    """Change exactly the old 2790 p slots; never alter a core or a max slot."""
    result = list(values)
    choices = []
    for block in interface['blocks']:
        p = block['p_column']
        endpoints = [dot(record['row'], values) for record in block['endpoints']]
        smallest = min(endpoints)
        q, v = endpoints[:2]
        r, z = values[block['r_column']], values[block['z_column']]
        assert smallest == min(r, z)+min(q-r, v-z)
        active = [k for k, value in enumerate(endpoints) if value == smallest]
        result[p] = smallest
        choices.append(dict(p_column=p, previous_value=str(values[p]),
                            canonical_value=str(smallest), endpoint_values=list(map(str, endpoints)),
                            selected_endpoint=active[0], tied_endpoints=active,
                            old_two_endpoint_canonical=values[p] == min(q, v)))
    changed = {j for j, (a, b) in enumerate(zip(values, result)) if a != b}
    assert changed <= set(interface['changed_canonical_rule_columns'])
    assert all(values[j] == result[j] for j in interface['core_columns'])
    assert all(values[j] == result[j] for j in interface['unchanged_max_columns'])
    assert all(values[j] == result[j] for j in interface['real_overlap_core_columns'])
    return result, choices


def selfcheck():
    matrix, interface, layer, sign = load_contract(require_freeze=False)
    # These values are deliberately synthetic and are NOT a feasible LP point.
    values = [F((j % 13)+1, 37) for j in range(21021)]
    for j in interface['real_overlap_core_columns']:
        values[j] = F((j % 3)+1, 4)*dot(matrix['columns'][j]['query_marginal'], values)
    for block in interface['blocks']:
        values[block['p_column']] = min(dot(e['row'], values) for e in block['endpoints'][:2])
    after, choices = canonicalize(values, interface)
    assert all(after[j] >= 0 for j in interface['changed_canonical_rule_columns'])
    assert all(dot(rec['row'], after) >= 0 for rec in layer['rows'])
    assert all(dot(matrix['rows'][i], after) >= 0 for b in interface['blocks'] for i in b['old_upper_rows'])
    assert all(after[b['p_column']] <= values[b['p_column']] for b in interface['blocks'])
    assert any(after[b['p_column']] < values[b['p_column']] for b in interface['blocks'])
    # Probe the exact elimination identity for EVERY genuine budget, without
    # interpreting any synthetic budget sign as a feasible-point exclusion.
    by_p = {b['p_column']: b for b in interface['blocks']}
    choice_by_p = {r['p_column']: r for r in choices}
    identities = 0
    for i in range(19511, 19550):
        projected = defaultdict(F)
        for j, a in matrix['rows'][i]: projected[j] += F(a)
        for p, a in matrix['rows'][i]:
            if p not in by_p: continue
            a = F(a); assert a > 0
            b = by_p[p]; k = choice_by_p[p]['selected_endpoint']
            for j, v in b['endpoints'][k]['row']: projected[j] += a*F(v)
            projected[p] -= a
        assert not any(a and 12803 <= j < 15593 for j, a in projected.items())
        assert dot(encode(projected), values) == dot(matrix['rows'][i], after)
        identities += 1
    report = dict(status='PASS_SYNTHETIC_CORE_PRESERVATION_AND_ELIMINATION_PROBES',
                  matrix_sha256=MATRIX_SHA, exact_point_files_opened=0, optimizer_calls=0,
                  synthetic_vector_is_not_claimed_feasible=True,
                  old_p_slots_exercised=2790, real_y_values_preserved=420,
                  all_core_values_preserved=10277, old_max_values_preserved=7954,
                  new_upper_rows_checked=5580, old_upper_rows_checked=5580,
                  true_budget_elimination_identities_checked=identities,
                  script_sha256=digest(Path(__file__)))
    target = HERE/'completion_selfcheck.json'
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(report))


def complete(point_path, expected_sha, tag):
    matrix, interface, layer, sign = load_contract()
    point_path = point_path.resolve()
    assert WORK.resolve() in point_path.parents and point_path.is_file()
    assert re.fullmatch(r'[0-9a-f]{64}', expected_sha)
    assert digest(point_path) == expected_sha
    assert re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]*', tag)
    out = HERE/('point_'+tag)
    assert not out.exists(), 'Refuse to overwrite a frozen point diagnostic.'
    point = read(point_path)
    assert len(point['columns']) == 21021
    assert [{k: v for k, v in c.items() if k != 'weight'} for c in point['columns']] == matrix['columns']
    if 'matrix_sha256' in point:
        assert point['matrix_sha256'] == MATRIX_SHA
    raw = [c['weight'] for c in point['columns']]
    assert all(isinstance(v, (str, int)) and not isinstance(v, bool) for v in raw)
    assert all(re.fullmatch(r'-?[0-9]+(?:/[1-9][0-9]*)?', str(v)) for v in raw)
    original = [F(v) for v in raw]
    out.mkdir()
    normalization = [[j, a] for j, a in enumerate(matrix['normalization']) if F(a)]
    objective = [[j, a] for j, a in enumerate(matrix['objective']) if F(a)]
    before_slacks = [dot(row, original) for row in matrix['rows']]
    before_O, before_W = dot(normalization, original), dot(objective, original)
    invalid = dict(negative_columns=[j for j, a in enumerate(original) if a < 0],
                   negative_rows=[i for i, a in enumerate(before_slacks) if a < 0],
                   normalization=str(before_O), required_normalization='1')
    metadata = dict(matrix_sha256=MATRIX_SHA, point_sha256=expected_sha,
                    point_path=str(point_path.relative_to(WORK)), optimizer_calls=0,
                    extension_sha256=digest(HERE/'conditioned_upper_rows.json'),
                    contract_sha256=digest(HERE/'freeze_manifest.json'))
    write(out, 'input_validation.json', dict(**metadata, **invalid,
          minimum_old_slack=str(min(before_slacks)), minimum_column=str(min(original)),
          objective=str(before_W)))
    if invalid['negative_columns'] or invalid['negative_rows'] or before_O != 1:
        write(out, 'result.json', dict(**metadata, status='INPUT_NOT_A_VALID_FROZEN_MATRIX_POINT',
              core_exclusion_claimed=False, reason='Input validation failed before any auxiliary replacement.'))
        print(json.dumps(dict(status='INPUT_NOT_A_VALID_FROZEN_MATRIX_POINT', output=str(out))))
        return
    if 'O' in point: assert F(point['O']) == before_O
    if 'W' in point: assert F(point['W']) == before_W
    completed, choices = canonicalize(original, interface)
    assert min(completed) >= 0
    after_slacks = [dot(row, completed) for row in matrix['rows']]
    new_slacks = [dot(rec['row'], completed) for rec in layer['rows']]
    assert min(new_slacks) >= 0
    assert dot(normalization, completed) == before_O == 1
    assert dot(objective, completed) == before_W
    changed = [j for j in range(21021) if original[j] != completed[j]]
    negative = [i for i, value in enumerate(after_slacks) if value < 0]
    # The complete sign audit implies these are the only possible failures.
    assert all(19511 <= i < 19550 for i in negative)
    maxima_were_canonical = all(
        original[rec['column']] == max(F(), -dot(
            [[j, a] for j, a in matrix['rows'][rec['threshold_row']] if j != rec['column']], original))
        for rec in sign['max_column_summary'])
    write(out, 'row_slacks.json.gz', dict(**metadata,
          old_before=list(map(str, before_slacks)), old_after=list(map(str, after_slacks)),
          new_after=list(map(str, new_slacks))))
    write(out, 'auxiliary_choices.json', dict(**metadata, endpoint_order=interface['canonical_endpoint_order'],
          choices=choices, real_420_y_never_canonicalized=True))
    completed_point = dict(**metadata,
        scope='Exact virtual same-X ZZ envelope candidate on fixed core; no full common law or SPE claim.',
        status='EXACT_FEASIBLE_COMPLETION' if not negative else 'MAXIMAL_ENVELOPE_CANDIDATE_INFEASIBLE',
        O='1', W=str(before_W), verified_old_rows=23676, checked_new_rows=5580,
        negative_old_row_count=len(negative), minimum_old_slack=str(min(after_slacks)),
        minimum_new_slack=str(min(new_slacks)), changed_columns=changed,
        columns=[dict(**c, weight=str(v)) for c, v in zip(matrix['columns'], completed)])
    write(out, 'completed_point.json.gz' if not negative else 'maximal_candidate.json.gz', completed_point)
    report = dict(**metadata,
        status='EXACT_FIXED_CORE_CONDITIONED_ZZ_COMPLETION' if not negative else 'FIXED_CORE_EXCLUDED_BY_TRUE_ZZ_BUDGET',
        core_values_preserved=10277, real_y_values_preserved=420, max_values_preserved=7954,
        all_16_histograms_retained=True, all_21021_columns_retained=True,
        changed_p_count=len(changed), old_maxima_were_canonical=maxima_were_canonical,
        old_all_p_were_two_endpoint_canonical=all(r['old_two_endpoint_canonical'] for r in choices),
        old_rows_recomputed=23676, new_rows_recomputed=5580,
        normalization='1', W=str(before_W), negative_true_budget_count=len(negative),
        minimum_old_slack=str(min(after_slacks)), minimum_new_slack=str(min(new_slacks)),
        budget_slacks=[dict(row_index=i, name=matrix['row_names'][i],
                            old_slack=str(before_slacks[i]), completed_slack=str(after_slacks[i]))
                       for i in range(19511, 19550)],
        original_new_upper_violations_are_not_used_as_core_exclusion=True)
    if negative:
        i = min(negative, key=lambda k: (after_slacks[k], k))
        by_p = {b['p_column']: b for b in interface['blocks']}
        by_choice = {r['p_column']: r for r in choices}
        projected = defaultdict(F)
        for j, a in matrix['rows'][i]: projected[j] += F(a)
        bound_multipliers = []
        for p, coefficient in matrix['rows'][i]:
            if p not in by_p: continue
            coefficient = F(coefficient); assert coefficient > 0
            block, choice = by_p[p], by_choice[p]
            k = choice['selected_endpoint']
            if k < 2:
                source, bound_index = 'old', block['old_upper_rows'][k]
                bound = matrix['rows'][bound_index]
            else:
                source, bound_index = 'new', block['new_candidate_rows'][k-2]
                bound = layer['rows'][bound_index]['row']
            assert dot(bound, completed) == 0
            for j, a in bound: projected[j] += coefficient*F(a)
            bound_multipliers.append(dict(p_column=p, coefficient=str(coefficient),
                endpoint=block['endpoints'][k]['name'], endpoint_value=choice['canonical_value'],
                bound_source=source, bound_index=bound_index, bound_row=bound))
        projected = {j: a for j, a in projected.items() if a}
        assert set(projected) <= set(interface['core_columns'])
        exact_negative = dot(encode(projected), original)
        assert exact_negative == after_slacks[i] < 0
        certificate = dict(**metadata,
            status='EXACT_FIXED_CORE_EXCLUSION_CERTIFICATE', budget_row_index=i,
            budget_name=matrix['row_names'][i], budget_row=matrix['rows'][i],
            budget_multiplier='1', bound_multipliers=bound_multipliers,
            projected_core_row=encode(projected), projected_value=str(exact_negative),
            fixed_core_values=[[j, str(original[j])] for j in sorted(projected)],
            identity='budget + sum(nonnegative_coefficient * selected_upper_row) = projected_core_row',
            contradiction='All constituent inequalities require projected_core_row >= 0, but its fixed-core value is strictly negative.',
            excludes_any_2790_p_choice_for_this_core=True,
            does_not_exclude_other_cores_or_prove_the_original_six_player_claim=True)
        write(out, 'core_exclusion_certificate.json', certificate)
        report['most_negative_true_budget'] = dict(row_index=i, name=matrix['row_names'][i],
                                                  value=str(exact_negative))
    write(out, 'result.json', report)
    output_files = sorted(path for path in out.iterdir() if path.is_file())
    write(out, 'output_manifest.json', dict(**metadata,
          files=[dict(path=p.name, sha256=digest(p), bytes=p.stat().st_size) for p in output_files],
          completion_script_sha256=digest(Path(__file__))))
    assert digest(MATRIX) == MATRIX_SHA and digest(point_path) == expected_sha
    print(json.dumps(dict(status=report['status'], negative_true_budgets=len(negative), output=str(out))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-check', action='store_true', help='Synthetic semantic probes; opens no exact point.')
    parser.add_argument('--point', type=Path, help='New exact point explicitly returned by Main.')
    parser.add_argument('--point-sha256', help='Expected SHA256 explicitly supplied with that new point.')
    parser.add_argument('--tag', help='Fresh output suffix; files stay in this owned directory.')
    args = parser.parse_args()
    if args.self_check:
        assert args.point is None and args.point_sha256 is None and args.tag is None
        selfcheck()
    elif args.point is not None:
        assert args.point_sha256 is not None and args.tag is not None
        complete(args.point, args.point_sha256, args.tag)
    else:
        parser.print_help()

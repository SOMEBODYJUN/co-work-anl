#!/usr/bin/env python3
"""Generate only the authorized 536 homogeneous rows; no LP or fixed point."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import defaultdict
import hashlib
import json

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[3]
WS = OUT.parent

def dump(name, data):
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    guard = json.loads((OUT / 'source_manifest.json').read_text())
    for key in ('source_sha256', 'prior_frozen_artifact_sha256'):
        for p, h in guard[key].items():
            assert sha(REPO / p) == h, p
    domain = json.loads((OUT / 'parameter_polytopes.json').read_text())
    base = json.loads((WS / 'visible_maximum_joint_v2/exact_input.json').read_text())
    bits = list(product((0, 1), repeat=9))
    atoms = []
    for index, b in enumerate(bits):
        atom = {'index': index, 'old_index': index // 2, 'a': list(b[:6]), 'x': b[6], 'o': b[7], 'c': b[8]}
        assert atom == base['atom_columns'][index]
        atoms.append(atom)
    assert base['K_column'] == 512 and base['bit_order'] == ['a1','a2','a3','a4','a5','a6','x','o','c']
    columns = {'schema': 'all_source_joint_reweighted_513_coordinate_contract_v1', 'bit_order': base['bit_order'], 'atom_columns': atoms, 'K_column': 512, 'variables': 513, 'nonnegative_columns': list(range(513)), 'C_size_equality': {'name': 'C_maximum_size', 'a': {str(k): str(b[8]) for k, b in enumerate(bits)} | {'512': '-1'}, 'rhs': '0'}, 'normalization_used_in_new_rows': False, 'source_coordinate_input_sha256': sha(WS / 'visible_maximum_joint_v2/exact_input.json')}
    dump('coordinate_contract.json', columns)
    rows, groups = [], defaultdict(list)
    roles = [f'A{j}' for j in range(1, 7)] + ['X', 'C']
    for source in domain['sources']:
        i = source['source']
        n, ci = 6-i, F(7-i, 2)
        for vertex in source['vertices']:
            theta, s = list(map(F, vertex['theta'])), F(vertex['s'])
            a = F(25) + sum(theta) - s
            assert str(a) == vertex['a']
            for role in roles:
                role_index = int(role[1:])-1 if role.startswith('A') else {'X': 6, 'C': 8}[role]
                coefficients = {}
                for index, b in enumerate(bits):
                    p, t, o = sum(b[:i-1]), b[role_index], b[7]
                    actual_load = sum(b[:6])
                    ui = F(b[i-1], actual_load) if actual_load else F(0)
                    D = p + n + 1
                    value = a*ui - ci*t - F(24*t, D) + s*F(t, min(D, 5)) - F(o, 6*(p+1+n*t))
                    value -= sum(w*F(o, 6*(p+(j-i)*t+7-j)) for j, w in zip(range(i+1, 6), theta))
                    coefficients[str(index)] = str(value)
                coefficients['512'] = str(ci)
                name = f'ALL_SOURCE_JOINT_REWEIGHTED_SAFE_I{i}_{vertex["id"].split("_")[1]}_T{role}'
                row = {'name': name, 'family': 'ALL_SOURCE_JOINT_REWEIGHTED_TRUE_INTERNAL_SAFE', 'source': i, 'T': role, 'query_menu': 'Omean_from_six_legal_labels', 'vertex_id': vertex['id'], 'theta_by_true_source': {str(j): str(w) for j, w in zip(range(i+1,6), theta)}, 's': str(s), 'source_IC_weight': str(a), 'middle_cap_weight': '1/2', 'terminal_cap_weight': '1', 'terminal_BR_average_weight': '1', 'K_weight': str(ci), 'uses_C_size_equality': False, 'a': coefficients, 'rhs': '0', 'numerical_divisor': '25'}
                rows.append(row)
                groups[tuple(coefficients[str(k)] for k in range(513))].append(name)
    assert len(rows) == 536
    exact = {'schema': 'all_source_joint_reweighted_536x513_v1', 'status': 'GENERATED_NO_SOLVE_NO_POINT', 'inequality_convention': 'a dot z >= rhs', 'variables': 513, 'raw_row_count': len(rows), 'bit_order': columns['bit_order'], 'K_column': 512, 'T_roles': roles, 'vertex_counts': {str(x['source']): len(x['vertices']) for x in domain['sources']}, 'raw_scale': 'terminal BR-average weight 1', 'numerical_positive_divisor': '25', 'rows': rows, 'raw_row_policy': 'Keep all vertex/role rows, including identical or redundant rows. All 513 coefficient fields retained, including zeros.', 'parameter_domain_sha256': sha(OUT / 'parameter_polytopes.json'), 'coordinate_contract_sha256': sha(OUT / 'coordinate_contract.json'), 'optimizer_calls': 0, 'fixed_point_bound': False}
    dump('exact_family.json', exact)
    dump('row_catalogue.json', [{k:v for k,v in row.items() if k != 'a'} for row in rows])
    dump('raw_duplicate_report.json', {'raw_rows': 536, 'coefficient_distinct_rows': len(groups), 'identical_groups': [v for v in groups.values() if len(v)>1], 'no_rows_deleted': True})
    dump('family_build_output.json', {'status': 'PASS', 'raw_rows': 536, 'variables': 513, 'coefficient_count': 536*513, 'coefficient_distinct_rows': len(groups), 'source_row_counts': {str(i): sum(r['source']==i for r in rows) for i in range(1,5)}, 'exact_family_sha256': sha(OUT / 'exact_family.json'), 'optimizer_calls': 0, 'input_or_point_bound': False, 'project_code_imported_or_executed': False})
    print(json.dumps({'status': 'PASS', 'rows': 536, 'columns': 513, 'coefficients': 536*513, 'coefficient_distinct_rows': len(groups), 'exact_family_sha256': sha(OUT / 'exact_family.json')}))

if __name__ == '__main__':
    main()

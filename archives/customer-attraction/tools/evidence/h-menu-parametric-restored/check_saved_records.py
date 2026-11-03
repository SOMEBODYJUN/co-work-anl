"""Read every frozen JSON field and check saved-record arithmetic/domain consistency.

This does not import/execute any source program, solve BI, evaluate utilities,
replay IC, verify true-menu completeness, or reconstruct a new SPE certificate.
"""
import ast
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'H-one-and-pooled-author-eight-primary/original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round7_general/signed'


def load(name):
    return json.loads((SOURCE / name).read_text())


def leaves(value, counts):
    if isinstance(value, dict):
        counts['dicts'] += 1
        for key, item in value.items():
            counts['keys'] += 1
            assert isinstance(key, str)
            leaves(item, counts)
    elif isinstance(value, list):
        counts['lists'] += 1
        for item in value:
            leaves(item, counts)
    else:
        assert value is None or isinstance(value, (str, int, bool))
        counts[type(value).__name__] += 1


def keys(record, expected):
    assert set(record) == set(expected.split())


def line(row):
    keys(row, 'slope intercept')
    return F(row['slope']), F(row['intercept'])


def evaluate(row, t):
    a, b = line(row)
    return a * t + b


def root_rows(rows, t):
    assert [row['A'] for row in rows] == list(range(6))
    for row in rows:
        keys(row, 'A theta H_A witness_B witness_terminal d_line v_line grandchild_outcomes')
        terminal = row['witness_terminal']
        assert len(terminal) == 4 and all(0 <= a < 6 for a in terminal)
        assert terminal[:2] == [row['A'], row['witness_B']]
        assert F(row['theta']) == (t + 1) / 2
        assert F(row['H_A']) == F(1, 2)
        assert evaluate(row['d_line'], t) - evaluate(row['v_line'], t) + F(row['theta']) == F(1, 2)
        assert row['grandchild_outcomes'] > 0


def attack_record(record):
    keys(record, 'unit_clients players topics ordered_tree_states examined_prefixes minimum_H_at_1 negative_prefixes all_prefixes scope')
    p, m = len(record['topics']), record['players']
    assert record['ordered_tree_states'] == sum(p ** j for j in range(m + 1))
    assert record['examined_prefixes'] == sum(p ** j for j in range(m - 1))
    prefixes = [tuple(r['prefix']) for r in record['all_prefixes']]
    assert prefixes == [h for j in range(m - 1) for h in product(range(p), repeat=j)]
    rows_seen = 0
    for prefix in record['all_prefixes']:
        keys(prefix, 'prefix remaining H_at_1 all_current_action_rows')
        h = prefix['prefix']
        assert prefix['remaining'] == m - len(h)
        rows = prefix['all_current_action_rows']
        assert [r['A'] for r in rows] == list(range(p))
        for row in rows:
            keys(row, 'A theta minimum argmin_B witness_terminal d v complete_grandchild_outcomes')
            z = row['witness_terminal']
            assert len(z) == m and all(0 <= a < p for a in z)
            assert z[:len(h) + 2] == h + [row['A'], row['argmin_B']]
            assert F(row['d']) - F(row['v']) + F(row['theta']) == F(row['minimum'])
            assert row['complete_grandchild_outcomes'] > 0
        assert F(prefix['H_at_1']) == max(F(r['minimum']) for r in rows)
        rows_seen += len(rows)
    assert record['minimum_H_at_1'] == min(record['all_prefixes'], key=lambda r: F(r['H_at_1']))
    assert record['negative_prefixes'] == [r for r in record['all_prefixes'] if F(r['H_at_1']) < 0]
    return {'clients':record['unit_clients'], 'players':m, 'topics':p,
            'prefixes':len(prefixes), 'current_action_rows':rows_seen,
            'root_H':record['all_prefixes'][0]['H_at_1'],
            'minimum_H':record['minimum_H_at_1']['H_at_1'],
            'minimum_prefix':record['minimum_H_at_1']['prefix'],
            'H_values_by_depth':{str(j):dict(sorted(Counter(r['H_at_1'] for r in record['all_prefixes'] if len(r['prefix']) == j).items())) for j in range(m-1)}}


def main():
    all_json = {name:load(name) for name in [
        'H_one_parametric_attack.json', 'H_one_parametric_regression.json',
        'attack_H_at_one.json', 'attack_H_at_one_multilevel.json',
        'audit_pooled_successor_transfer.json']}
    consumed = {}
    for name, obj in all_json.items():
        counts = Counter()
        leaves(obj, counts)
        consumed[name] = {'structure_counts':dict(counts), 'file_sha256':sha256((SOURCE/name).read_bytes()).hexdigest()}

    grid = all_json['H_one_parametric_attack.json']
    keys(grid, 'status exact_candidate normalization original_payoff_lines positive_payoff_order_grid open_cells critical_points BI_runs states_per_run decision_states_per_run all_forced_entries_per_run including_own_at_every_history all_open_cells all_critical_points comparison_table negative_rational_parameters exact_constant_one_half_all_open_cells_and_critical_points zero_boundary_right_limit tail_slope scope')
    utility_lines = [(F(1,p),F(1,q)) for p,q in product(range(1,5),repeat=2)]
    assert [line(x) for x in grid['original_payoff_lines']] == utility_lines
    cross = sorted({(d-b)/(a-c) for (a,b),(c,d) in combinations(utility_lines,2) if a != c and (d-b)/(a-c)>0})
    assert list(map(F,grid['positive_payoff_order_grid'])) == cross
    assert (grid['open_cells'],grid['critical_points'],grid['BI_runs']) == (24,23,47)
    assert (grid['states_per_run'],grid['decision_states_per_run'],grid['all_forced_entries_per_run']) == (1555,259,1554)
    assert grid['including_own_at_every_history'] is True
    menus = Counter()
    gc_counts = Counter()
    for index, cell in enumerate(grid['all_open_cells']):
        keys(cell, 'left right sample theta_line H_concave_affine_menu H_left_one_sided H_right_one_sided tail_minimum_slope nonnegative_certificate exact_constant_one_half_certificate all_forced_root_rows_at_sample')
        left = F(cell['left']); right = None if cell['right'] is None else F(cell['right'])
        assert left == ([F(0)]+cross)[index]
        assert right == (cross[index] if index<len(cross) else None)
        sample = F(cell['sample'])
        assert left < sample and (right is None or sample < right)
        assert line(cell['theta_line']) == (F(1,2),F(1,2))
        menu = [line(l) for l in cell['H_concave_affine_menu']]
        menus[str(menu)] += 1
        assert (F(0),F(1,2)) in menu
        assert min(a*left+b for a,b in menu) == F(cell['H_left_one_sided']) == F(1,2)
        if right is None:
            assert cell['H_right_one_sided'] is None
            assert min(a for a,b in menu) == F(cell['tail_minimum_slope']) == 0
        else:
            assert min(a*right+b for a,b in menu) == F(cell['H_right_one_sided']) == F(1,2)
            assert cell['tail_minimum_slope'] is None
        assert cell['nonnegative_certificate'] and cell['exact_constant_one_half_certificate']
        root_rows(cell['all_forced_root_rows_at_sample'], sample)
        gc_counts.update(r['grandchild_outcomes'] for r in cell['all_forced_root_rows_at_sample'])
    for index, point in enumerate(grid['all_critical_points']):
        keys(point, 't H_at_actual_ties all_forced_root_rows')
        assert F(point['t']) == cross[index]
        assert F(point['H_at_actual_ties']) == F(1,2)
        root_rows(point['all_forced_root_rows'],cross[index])
        row = grid['comparison_table'][index]
        keys(row,'t H_from_left H_at_actual_ties H_from_right')
        assert row == {'t':point['t'], 'H_from_left':grid['all_open_cells'][index]['H_right_one_sided'], 'H_at_actual_ties':point['H_at_actual_ties'], 'H_from_right':grid['all_open_cells'][index+1]['H_left_one_sided']}
        gc_counts.update(r['grandchild_outcomes'] for r in point['all_forced_root_rows'])
    assert grid['negative_rational_parameters'] == []
    assert grid['exact_constant_one_half_all_open_cells_and_critical_points']
    assert F(grid['zero_boundary_right_limit']) == F(1,2) and F(grid['tail_slope']) == 0

    regress = all_json['H_one_parametric_regression.json']
    keys(regress,'status candidate cases scope')
    assert [(r['a'],r['b']) for r in regress['cases']] == [(1,9),(1,2),(1,1),(2,1),(3,1),(9,1),(3,2)]
    for case in regress['cases']:
        keys(case,'a b unit_clients all_terminal_unit_expansion_checks H_root_exact theta_exact all_forced_root_rows_normalized ordered_states decision_states all_forced_BI_entries')
        a,b = case['a'],case['b']
        assert case['unit_clients'] == 3*a+2*b
        assert case['all_terminal_unit_expansion_checks'] == 1296
        assert (case['ordered_states'],case['decision_states'],case['all_forced_BI_entries']) == (1555,259,1554)
        assert F(case['H_root_exact']) == F(b,2) and F(case['theta_exact']) == F(a+b,2)
        root_rows(case['all_forced_root_rows_normalized'],F(a,b))

    attacks = all_json['attack_H_at_one.json']
    keys(attacks,'old34 old23 old31 read_product_a3_b1_m4')
    attack_summaries = {name:attack_record(record) for name,record in attacks.items()}
    side = all_json['attack_H_at_one_multilevel.json']
    attack_record(side)
    assert side == attacks['read_product_a3_b1_m4']

    audit = all_json['audit_pooled_successor_transfer.json']
    keys(audit,'status purpose parameters unit_clients themes all_ordered_decision_histories all_forced_IC_comparisons_including_own own_comparisons minimum_IC_gap ordered_two_action_prefixes_in_exact_BI terminal_last_BR_evaluations all_forced_first_caps M_root_exact separate_barM_cap strict_M_saving policy target scope')
    assert audit['parameters'] == {'a':2,'b':1,'q':2}
    assert audit['unit_clients'] == 16 and audit['themes'] == 36
    assert audit['all_ordered_decision_histories'] == audit['own_comparisons'] == 1+36+36**2 == 1333
    assert audit['all_forced_IC_comparisons_including_own'] == 36*1333 == 47988
    assert audit['ordered_two_action_prefixes_in_exact_BI'] == 36**2
    assert audit['terminal_last_BR_evaluations'] == 36**3
    assert F(audit['minimum_IC_gap']) == 0
    policy = {}
    for item in audit['policy']:
        keys(item,'history action')
        h = tuple(item['history'])
        assert h not in policy and len(h)<3 and all(0<=a<36 for a in h)
        assert 0<=item['action']<36
        policy[h] = item['action']
    assert set(policy) == {h for j in range(3) for h in product(range(36),repeat=j)}
    themes = list(product(range(3),range(3),range(2),range(2)))
    assert [r['forced_first'] for r in audit['all_forced_first_caps']] == list(range(36))
    for cap in audit['all_forced_first_caps']:
        keys(cap,'forced_first forced_theme ell next_threshold constructed_terminal constructed_profits')
        first = cap['forced_first']; second = policy[(first,)]
        assert cap['forced_theme'] == list(themes[first])
        assert cap['constructed_terminal'] == [first,second,policy[(first,second)]]
        assert list(map(F,cap['constructed_profits'])) == [F(4),F(5),F(5)]
        assert F(cap['ell']) == 4 and F(cap['next_threshold']) == 5
    assert (F(audit['M_root_exact']),F(audit['separate_barM_cap']),F(audit['strict_M_saving'])) == (4,5,1)
    target = audit['target']
    keys(target,'ordered_topics profits W OPT B true_g old_repair_cost new_repair_cost strict_repair_saving B_plus_new_C')
    assert target['ordered_topics'] == [0,0,19] and list(map(F,target['profits'])) == [3,3,6]
    assert (target['W'],target['OPT'],target['B']) == (12,16,8)
    assert 2*target['W']-target['OPT'] == target['B']
    g = list(map(F,target['true_g']))
    assert g == [1,2]
    assert F(target['new_repair_cost']) == 2*sum(g)+max(g) == 8
    assert F(target['old_repair_cost'])-F(target['new_repair_cost']) == F(target['strict_repair_saving']) == 2
    assert target['B']+F(target['new_repair_cost']) == F(target['B_plus_new_C']) == 16

    syntax = {}
    for name in ['H_one_parametric_attack.py','attack_H_at_one.py','audit_pooled_successor_transfer.py']:
        tree = ast.parse((SOURCE/name).read_text(), filename=name)
        syntax[name] = {'syntax':'parsed', 'imports':[n.module if isinstance(n,ast.ImportFrom) else ','.join(x.name for x in n.names) for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom))]}
    report = {'status':'PASS: saved-data consistency only',
              'full_json_consumption':consumed, 'source_AST_only':syntax,
              'grid':{'cells':24,'critical_points':23,'root_rows':47*6,'menu_variants':dict(menus),'saved_grandchild_counts_histogram':dict(gc_counts)},
              'regression':{'cases':7,'root_rows':42,'saved_terminal_checks':7*1296},
              'attack_records':attack_summaries,
              'multilevel_semantic_duplicate':True,
              'pooled':{'policy_rows':len(policy),'cap_rows':36,'saved_comparisons_with_own':47988,'own':1333,'nonown':46655},
              'execution_scope':{'original_main':0,'original_import':0,'original_function_calls':0,'BI':0,'utility_evaluations':0,'IC_replay':0,'LP_or_random_search':0},
              'limits':'No true-menu completeness or historical execution event is certified by these saved-record arithmetic/domain checks.'}
    (HERE/'saved-record-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()

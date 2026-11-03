"""Bind the frozen tables to the delivered proof; no discovery or solver import."""
from ast import literal_eval
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parent
tree = base.parents[4]
page = tree / 'archives/customer-attraction/state/反例/有限四层DR势的完整槽聚合亏损--反例.md'
manifest = json.loads((base / 'source-manifest.json').read_text())
for row in manifest:
    data = (tree / row['local_path']).read_bytes()
    assert len(data) == row['size']
    assert hashlib.sha256(data).hexdigest() == row['sha256']
raw = json.loads((base / 'original/fullslots/dr_counterexample_exact.json').read_text())
floating = json.loads((base / 'original/fullslots/probe_general_dr_float.json').read_text())
P = {tuple(map(int, k.split(','))): F(v) for k, v in raw['potential'].items()}
sig = {tuple(map(int, k.split(','))) if k else (): a for k, a in raw['strategy'].items()}

def ct(z):
    return tuple(z.count(a) for a in range(4))

def val(z):
    return P[ct(z)]

def add(q, a):
    return tuple(v + int(i == a) for i, v in enumerate(q))

def end(h):
    while len(h) < 3:
        h += (sig[h],)
    return h

def u(z, j):
    return val(z) - val(z[:j] + z[j+1:])

def U(z):
    return sum((u(z, j) for j in range(len(z))), F())

def G(z):
    return sum((val(z + (a,)) - val(z) for a in range(4)), F()) / 4

expected_counts = {ct(z) for n in range(5) for z in product(range(4), repeat=n)}
expected_histories = {z for n in range(3) for z in product(range(4), repeat=n)}
assert set(P) == expected_counts and len(P) == 70 and P[(0, 0, 0, 0)] == 0
assert set(sig) == expected_histories and len(sig) == 21
assert all(type(a) is int and 0 <= a < 4 for a in sig.values())
assert raw['strategy'] == floating['strategy']
scale_error = max(abs(raw['potential'][k] - 10 * v) for k, v in floating['potential'].items())
assert raw['potential'].keys() == floating['potential'].keys() and scale_error < 1e-10

text = page.read_text()
potential_part = text.split('## 全部势值', 1)[1].split('## 单调与全部多重集 DR', 1)[0]
potential_rows = []
for line in potential_part.splitlines():
    cells = [s.strip() for s in line.strip().strip('|').split('|')]
    if line.startswith('|') and len(cells) == 2 and cells[1].isdigit():
        z = () if cells[0] == '∅' else tuple(map(int, cells[0]))
        assert val(z) == int(cells[1])
        potential_rows.append(ct(z))
assert len(potential_rows) == 70 and set(potential_rows) == set(P)

dr_part = text.split('全部 150 个余项如下', 1)[1].split('下表是全部大小三背景', 1)[0]
dr_rows = 0
for line in dr_part.splitlines():
    cells = [s.strip() for s in line.strip().strip('|').split('|')]
    if line.startswith('|') and len(cells) == 11 and cells[1].isdigit():
        z = () if cells[0] == '∅' else tuple(map(int, cells[0]))
        q = ct(z)
        expected = [P[add(q, a)] + P[add(q, b)] - P[q] - P[add(add(q, a), b)]
                    for a in range(4) for b in range(a, 4)]
        assert expected == list(map(F, cells[1:])) and min(expected) >= 0
        dr_rows += 1
assert dr_rows == 15

marginal_part = text.split('下表是全部大小三背景', 1)[1].split('## 完整有序历史策略', 1)[0]
marginal_rows = 0
for line in marginal_part.splitlines():
    cells = [s.strip() for s in line.strip().strip('|').split('|')]
    if line.startswith('|') and len(cells) == 5 and cells[1].isdigit():
        z = tuple(map(int, cells[0]))
        expected = [val(z + (a,)) - val(z) for a in range(4)]
        assert expected == list(map(F, cells[1:])) and min(expected) >= 0
        marginal_rows += 1
assert marginal_rows == 20

ic_part = text.split('## 完整有序历史策略', 1)[1].split('## 全槽菜单与严格违反', 1)[0]
ic_rows = 0
for line in ic_part.splitlines():
    cells = [s.strip() for s in line.strip().strip('|').split('|')]
    if line.startswith('|') and len(cells) == 6 and cells[1].isdigit():
        h = () if cells[0] == '∅' else literal_eval(cells[0])
        assert sig[h] == int(cells[1])
        pay = [u(end(h + (a,)), len(h)) for a in range(4)]
        assert pay == list(map(F, cells[2:])) and pay[sig[h]] == max(pay)
        ic_rows += 1
assert ic_rows == 21

z = end(())
menu_part = text.split('## 全槽菜单与严格违反', 1)[1].split('全部12列查询', 1)[0]
menu_rows = []
for line in menu_part.splitlines():
    cells = [s.strip() for s in line.strip().strip('|').split('|')]
    if line.startswith('|') and len(cells) == 4 and cells[0].isdigit():
        a = int(cells[0]); leaf = literal_eval(cells[1]); ds = literal_eval(cells[2])
        i = len(menu_rows) // 4
        assert leaf == end(z[:i] + (a,))
        assert ds == tuple(val(leaf + (t,)) - val(leaf) for t in range(4))
        assert F(cells[3]) == G(leaf) == F(11, 4)
        menu_rows.append(leaf)
assert len(menu_rows) == 12 and z == (0, 1, 2) and U(z) == 8

euler_rows = []
for q in sorted((q for q in P if sum(q) == 3)):
    leaf = tuple(a for a in range(4) for _ in range(q[a]))
    lhs = 4 * G(leaf) - sum((G(leaf[:i] + leaf[i+1:]) for i in range(3)), F())
    rhs = sum((U(leaf + (a,)) - U(leaf) for a in range(4)), F()) / 4
    assert lhs == rhs
    euler_rows.append({'counts': q, 'mean_total_marginal_increment': str(rhs)})
assert U((3, 3, 3)) == 18 and U((3, 3, 3, 3)) == 0
frozen_parent = json.loads((base / 'original/parent/audit_fullslot_dr_parent.json').read_text())
replayed_parent = json.loads((base / 'replay/round2/parent/audit_fullslot_dr_parent.json').read_text())
assert frozen_parent == replayed_parent
author = json.loads((base / 'original/fullslots/dr_counterexample_audit.json').read_text())
assert author['actual'] == list(z) and author['sum_min_query'] == '33/4' and author['gap'] == '1/4'
for i, row in enumerate(author['menus']):
    assert row['forced_leaf'] == [list(t) for t in menu_rows[4*i:4*i+4]]
    assert row['query_values'] == ['11/4'] * 4 and row['minimum'] == '11/4'

report = {'source_files': len(manifest), 'source_bytes': sum(r['size'] for r in manifest),
          'all_source_sha256_match': True, 'complete_potential_domain': 70,
          'complete_ordered_strategy_domain': 21, 'document_potential_rows': len(potential_rows),
          'document_DR_rows': dr_rows, 'document_marginal_rows': marginal_rows,
          'document_IC_rows': ic_rows, 'document_menu_rows': len(menu_rows),
          'float_times_ten_max_error': scale_error, 'float_and_exact_strategy_equal': True,
          'parent_report_matches_replay': True, 'actual': z, 'total_marginal_utility': str(U(z)),
          'sum_min_query': '33/4', 'gap': '1/4', 'Euler_uniform_rows': euler_rows,
          'non_CAG_fixed_three': {'theme0_value_inferred': '9', 'required_payoff_lower_bound': '3', 'actual_payoff': '2'},
          'nonmonotone_total_marginal': {'U_333': '18', 'U_3333': '0'},
          'solver_calls': 0, 'discovery_imports': 0}
(base / 'binding-review.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'Euler_uniform_rows'}, ensure_ascii=False))

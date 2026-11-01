"""Independent definition-level audit of the 56 split rows, not the full graph.

The original build/CLI is never called. Only the source's scalar values(r,z)
expression is compiled in a supplied local environment for comparison.
"""
import ast
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
from types import SimpleNamespace
import argparse

PAT = tuple(product((0, 1), repeat=3))
RN = ('source', 'terminal_own_B', 'terminal_own_C', 'terminal_own_T',
      'terminal_opt_average', *(f'terminal_actual_{i+1}' for i in range(6)),
      'terminal_B_average', 'terminal_C_average', 'reverse_terminal', 'price', 'capacity')
ZN = ('source', 'pair', 'price', 'capacity', *(f'actual{i}' for i in range(6)), 'ownR', 'reverseR')
SPLIT = [(stage, diagonal, name) for stage, names in (('R', RN), ('Z', ZN))
         for diagonal in (0, 1) for name in names]
SI = {value: i for i, value in enumerate(SPLIT)}


@lru_cache(None)
def own(member, others):
    return F(member, member + others) if member else F(0)


def literal(a, words, i, j, r, z):
    """True-history utilities and the strong-PAIR expression, per customer."""
    p, pa, ell = sum(a[:3]), sum(a[:4]), sum(a[:5])
    t, b, c = words[i]
    y = words[j][2]
    ui = own(b, p+t+c)
    vi = own(c, p+t+b)
    ur = own(r, p+t+y)
    u5, u6 = own(a[4], sum(a)-a[4]), own(a[5], sum(a)-a[5])
    terminal = [ur-own(q, p+t+y) for q in (b, c, t)]
    terminal += [ur-sum(own(row[0], p+t+y) for row in words)/6]
    terminal += [ur-own(q, p+t+y) for q in a]
    terminal += [ur-sum(own(row[k], p+t+y) for row in words)/6 for k in (1, 2)]
    rr = [ui-own(y, p+t+r), *terminal,
          vi-own(r, p+t+b), u6-own(r, ell), -F(r)]
    f = lambda q: own(q, pa)
    g = lambda q, s: F(int(q and s), (pa+1)*(pa+2))
    h = u5+u6+g(a[4], a[4])
    uz = own(z, pa+r)
    zz = [u5-own(r, pa+z), h-f(r)-f(z)+g(r, z),
          u6-own(z, ell), -F(z)]
    zz += [uz-own(q, pa+r) for q in a]
    zz += [uz-own(r, pa+r), ur-own(z, p+t+y)]
    diagonal = int(i == j)
    return {**{SI['R', diagonal, name]: val for name, val in zip(RN, rr)},
            **{SI['Z', diagonal, name]: val for name, val in zip(ZN, zz)}}


def original_scalar(source, a, words, i, j):
    """Reuse only the untouched source inner function, not graph construction."""
    t, b, c = words[i]
    p = sum(a[:3]); y = words[j][2]
    env = {'F': F, 'nr': SimpleNamespace(share=lambda n,d:F(n,d) if n else F(), NAMES=RN),
           'nest': SimpleNamespace(BASIC=ZN), 'SI': SI, 'a': a, 'p': p,
           'pa': sum(a[:4]), 'ell': sum(a[:5]), 'whole': sum(a),
           't': t, 'b': b, 'cc': c, 'y': y, 'diag': int(i == j),
           'den': p+t+y+1, 'c': {'d': sum(row[0] for row in words)},
           'nb': sum(row[1] for row in words), 'nc': sum(row[2] for row in words)}
    exec(source, env)
    return env['values']


def main():
    if not __debug__:
        raise RuntimeError('Run with assertions enabled')
    ap = argparse.ArgumentParser()
    ap.add_argument('--runtime', type=Path)
    ap.add_argument('--output', type=Path, default=Path(__file__).resolve().parent/'independent-report.json')
    args = ap.parse_args()
    own_dir = Path(__file__).resolve().parent
    old_route = 'research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/six_astra'
    if args.runtime:
        old_dir = args.runtime/old_route
        here = args.runtime/'research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
        source_path, point_path = here/'split_basic_graph.py', here/'split_basic_exact.json'
    else:
        old_dir = own_dir.parent/'combined-branch-master-program/dependencies'/old_route
        source_path, point_path = own_dir/'original/split_basic_graph.py', own_dir/'related/split_basic_exact.json'
    expected_inputs = [
        (source_path, '649ea591b5c15c076246d72f4b13920caeade77d1b87c59530ac492f3e50b1dc'),
        (point_path, 'b12c4aa6b3cd106f3fb8e8a56be7469988456c0cb6e02b1741db8c09d587b34a'),
        (old_dir/'attractive_nested_exact.json', 'cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1'),
        (old_dir/'new_reply_budget.py', '5be0586e5b013a8bd7dacc197874b6b4549d700a383bbd12726fe2b8f0245773'),
        (old_dir/'actual_fifth_nested.py', '1b65c9fe43b955c3c4c1f34b70ba2b3966d61a7452cbde62963f375c559b2528'),
    ]
    input_records=[]
    for path, expected in expected_inputs:
        data=path.read_bytes();digest=hashlib.sha256(data).hexdigest()
        assert digest==expected,path
        input_records.append({'name':path.name,'bytes':len(data),'sha256':digest})
    raw = source_path.read_bytes()
    tree = ast.parse(raw)
    node = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == 'values')
    scalar = compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), '<frozen-values-expression>', 'exec')
    # Match the source names, so zip truncation or reordered inherited labels
    # cannot silently pass the scalar comparison.
    for filename, variable, expected in [('new_reply_budget.py', 'NAMES', RN), ('actual_fifth_nested.py', 'BASIC', ZN)]:
        source_tree = ast.parse((old_dir/filename).read_text())
        assignment = next(n for n in source_tree.body if isinstance(n, ast.Assign)
                          and any(isinstance(t, ast.Name) and t.id == variable for t in n.targets))
        env = {}
        exec(compile(ast.Module(body=[assignment], type_ignores=[]), '<frozen-labels>', 'exec'), env)
        assert tuple(env[variable]) == expected
    # The unselected indices enter only through three linear menu averages.
    # All-zero plus each coordinate basis fill spans those affine terms.
    fills = ((0,0,0), (1,0,0), (0,1,0), (0,0,1))
    local_cases, local_coefficients = 0, 0
    for a in product((0,1), repeat=6):
        for diagonal in (0,1):
            for wi in PAT:
                for wj in ((wi,) if diagonal else PAT):
                    for fill in fills:
                        words = (wi,)+(fill,)*5 if diagonal else (wi,wj)+(fill,)*4
                        i,j = (0,0) if diagonal else (0,1)
                        authored = original_scalar(scalar, a, words, i, j)
                        for r,z in product((0,1),repeat=2):
                            actual, expected = authored(r,z), literal(a,words,i,j,r,z)
                            assert actual == expected,(a,words,i,j,r,z)
                            assert len(actual) == 28
                            local_cases += 1; local_coefficients += len(actual)
    old = json.loads((old_dir/'attractive_nested_exact.json').read_bytes())
    point = json.loads(point_path.read_bytes())
    strip = lambda cs:[{k:v for k,v in c.items() if k!='weight'} for c in cs]
    assert len(old['columns']) == len(point['columns']) == 1905
    assert strip(old['columns']) == strip(point['columns'])
    columns = point['columns']; hist = {}; current = None
    for index,column in enumerate(columns):
        assert F(column['weight']) >= 0
        if column['kind'] == 'hist':
            current=index;hist[index]={'column':column,'groups':{}}
        elif column['kind'] == 'joint-reply':
            f,diag,wi,wj=column['group'];key=(f,diag,tuple(wi),tuple(wj))
            states=hist[current]['groups'].setdefault(key,{})
            assert tuple(column['state']) not in states
            states[tuple(column['state'])]=index
        else: assert column['kind'] in ('K','overlap')
    assert len(hist)==16
    rows=[[F()]*1905 for _ in SPLIT]
    authored_rows=[[F()]*1905 for _ in SPLIT]
    for hi,data in hist.items():
        c=data['column'];a=tuple(map(int,c['actual_bits']))
        words=tuple(w for w,n in zip(PAT,c['hist']) for _ in range(n))
        assert len(words)==6 and sum(w[0] for w in words)==c['d']
        for group,states in data['groups'].items():
            assert set(states)=={(0,1),(1,0),(1,1)}
            assert sum(F(columns[j]['weight']) for j in states.values())<=F(c['weight'])
        for i,j in product(range(6),repeat=2):
            group=(1,int(i==j),words[i],words[j]);states=data['groups'][group]
            authored=original_scalar(scalar,a,words,i,j)
            for target,fn in ((rows,lambda r,z:literal(a,words,i,j,r,z)),(authored_rows,authored)):
                zero=fn(0,0)
                for row,v in zero.items():target[row][hi]+=v
                for state,col in states.items():
                    for row,v in fn(*state).items():target[row][col]+=v-zero[row]
    for stage in ('R','Z'):
        for diagonal,count in ((0,30),(1,6)):
            rows[SI[stage,diagonal,'capacity']][0]=F(count)
            authored_rows[SI[stage,diagonal,'capacity']][0]=F(count)
    assert rows==authored_rows
    assert all(rows[i][j]==0 for i in range(56) for j,c in enumerate(columns) if c['kind']=='overlap')
    slacks=[sum(c*F(v['weight']) for c,v in zip(row,columns)) for row in rows]
    assert len(slacks)==56 and min(slacks)>=0
    norm=sum(F(c['weight']) for c in columns if c['kind']=='hist' and c['d']>0)
    welfare=sum(F(c['weight']) for c in columns if c['kind']=='hist' and '1' in c['actual_bits'])
    assert norm==1 and welfare==F(point['W'])<F(1,2)
    report={'scope':'new exact audit of the 56 split rows; no full-graph build, original CLI or LP solve',
            'source_sha256':hashlib.sha256(raw).hexdigest(),'inputs':input_records,
            'local_scalar_cases':local_cases,'local_scalar_coefficients_compared':local_coefficients,
            'affine_menu_basis_fills':list(fills),'split_rows':56,'columns':1905,
            'matrix_coefficients_compared':56*1905,'histograms':16,
            'reply_groups':sum(len(d['groups']) for d in hist.values()),
            'column_kinds':dict(Counter(c['kind'] for c in columns)),
            'old_and_split_column_descriptors_equal':True,
            'joint_00_masses_nonnegative':True,'split_point_O':str(norm),'split_point_W':str(welfare),
            'split_slacks':[{'stage':s,'diagonal':d,'name':n,'value':str(v)} for (s,d,n),v in zip(SPLIT,slacks)],
            'minimum_split_slack':str(min(slacks)),
            'limits':'All 56 added rows checked at the frozen split point; its other 3889 rows not revalidated here. Shared combined --verify executes original split.build including old-row sum assertions. No complete SPE or exact optimum certification.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('local_scalar_cases','local_scalar_coefficients_compared','matrix_coefficients_compared','minimum_split_slack','split_point_W')},indent=2))


if __name__=='__main__':main()

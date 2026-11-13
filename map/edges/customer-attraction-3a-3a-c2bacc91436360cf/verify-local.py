"""Read-only mathematical replay; writes only this task's replay.json.

Uses exact scaled integers for R-373d and reuses the already read Fraction
fixed-cone verifier function without executing its artifact-writing main.
No optimizer, git operation or queue operation is invoked.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations_with_replacement, combinations
from functools import lru_cache
import ast, hashlib, json
import numpy as np

ROOT = Path.cwd()
OUT = ROOT / 'map/edges/customer-attraction-3a-3a-c2bacc91436360cf'
E = ROOT / 'archives/customer-attraction/tools/evidence'
reports = {}

# Exact input equality, not an assertion that parsing is mathematical reading.
cert = E / 'five-player-indexed/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
dep = E / 'R-373d-credible2-20261031/dependencies/evidence/certificates/customer_attraction/five_player_indexed_bound.json'
assert cert.read_bytes() == dep.read_bytes()
d = json.loads(cert.read_text())
md = (ROOT / 'archives/customer-attraction/state/障碍/五人索引偏离模板--障碍.md').read_text()
table = [line.split('|')[1:-1] for line in md.splitlines() if line.startswith('| ') and line.split('|')[1].strip().isdigit()]
assert len(table) == len(d['primal']['atoms']) == 64
for row, atom in zip(table, d['primal']['atoms']):
    ix,bits,ab,ae,second,menus,mass = [x.strip() for x in row]
    assert int(ix) == d['primal']['atoms'].index(atom)
    assert bits.strip('`') == ''.join(map(str,atom['bits']))
    assert int(mass) == atom['mass_numerator']
    assert json.loads(menus.strip('`')) == atom['menus_lh']
    for view, actual in [(ab,atom['AB_hist']),(ae,atom['AE_hist']),(second,atom['second_hist'])]:
        vec = [0]*len(actual)
        for item in view.strip('`').split(','):
            k,v = map(int,item.split(':')); vec[k] = v
        assert vec == actual
reports['indexed_table'] = {'all_64_atoms_equal_full_MD_table': True,
    'dependency_certificate_same_bytes': True, 'atoms':64,'rows':len(d['primal']['rows'])}

# R-373d rounded p=15,m=5 input. All shares have denominator dividing 60.
saved = json.loads((E / 'R-373d-credible2-20261031/source/materialized_seed37381021_scale1000000.json').read_text())
types = dict(saved['types']); p,m=15,5
assert sum(types.values())*60 < 2**63
B = np.array([[(mask>>a)&1 for a in range(p)] for mask in types],dtype=np.int64)
weights = np.array(list(types.values()),dtype=np.int64)
qs = tuple(tuple(h.count(a) for a in range(p)) for h in combinations_with_replacement(range(p),m))
idx = {q:i for i,q in enumerate(qs)}; Q=np.array(qs,dtype=np.int64)
denoms=Q@B.T; shares=np.zeros_like(denoms);nz=denoms>0
assert all(60 % int(v) == 0 for v in np.unique(denoms[nz]))
shares[nz]=60//denoms[nz]; pay=(shares*weights)@B; W=(denoms>0)@weights
R={q:frozenset((i,)) for i,q in enumerate(qs)}; depths=[]
def inc(k,a): return k[:a]+(k[a]+1,)+k[a+1:]
for dep in range(m-1,-1,-1):
    states=tuple(tuple(h.count(a) for a in range(p)) for h in combinations_with_replacement(range(p),dep))
    for k in states:
        children=[R[inc(k,a)] for a in range(p)]
        floor=max(min(int(pay[q,a]) for q in options) for a,options in enumerate(children))
        R[k]=frozenset(q for a,options in enumerate(children) for q in options if pay[q,a]>=floor)
    depths.append({'depth':dep,'states':len(states),'max_outcomes':max(map(lambda k:len(R[k]),states))})
root=R[(0,)*p]; assert len(root)==1
q=next(iter(root)); welfare=int(W[q]); ABCDE=(1,)*5+(0,)*10
opt=max(sum(w for mask,w in types.items() if mask & sum(1<<a for a in port)) for port in combinations(range(p),m))
assert list(qs[q])==saved['root_worst_counts'] and welfare==saved['welfare']==1810296
assert opt==saved['optimum']==2061696 and int(W[idx[ABCDE]])==saved['actual_ABCDE_welfare']==1000000
assert (idx[ABCDE] in root)==saved['actual_ABCDE_is_SPE_outcome']==False
assert F(opt,welfare)==F(85904,75429)
reports['rounded_instance']={'unique_root_counts':qs[q],'W':welfare,'OPT':opt,
    'ratio':str(F(opt,welfare)),'ABCDE_in_root':False,'depths':depths,'arithmetic':'int64, proved safe by total weight*60 bound'}

# All three scan records have the complete constant-zero strategy.
reports['constant_zero_candidates']=[]
for name in ('weak_scan_best.json','strong_scan_best.json','strong_all_scan_best.json'):
    d=json.loads((E/'R-373d-credible2-20261031/source'/name).read_text());p,m=d['p'],d['m']
    acts=d['strategy']['actions'];hs=[h for dep in range(m) for h in product(range(p),repeat=dep)]
    assert [tuple(x['history']) for x in acts]==hs and all(x['action']==0 for x in acts)
    types={i+1:w for i,w in enumerate(d['weights']) if w}; size=[sum(w for mask,w in types.items() if mask & 1<<a) for a in range(p)]
    assert size[0]==m and size[1:]==[1]*(p-1)
    def utility(z,i): return sum((F(w,sum(bool(mask & 1<<a) for a in z)) for mask,w in types.items() if mask & 1<<z[i]),F(0))
    least=None
    for h in hs:
        actual=h+(0,)*(m-len(h)); u=utility(actual,len(h))
        for a in range(p):
            alt=h+(a,)+(0,)*(m-len(h)-1); slack=u-utility(alt,len(h));assert slack>=0
            least=slack if least is None else min(least,slack)
    welfare=size[0];opt=max(sum(w for mask,w in types.items() if mask & sum(1<<a for a in port)) for port in combinations(range(p),min(m,p)))
    assert welfare==d['welfare'] and opt==d['optimum']
    reports['constant_zero_candidates'].append({'file':name,'histories':len(hs),'all_actions_zero':True,'theme_sizes':size,'W':welfare,'OPT':opt,'minimum_slack':str(least)})

# Existing fixed-cone verifier: only definitions and read statements before main.
fp=E/'full-tree-milp-candidate-audits-primary/independent_exact_review.py'
tree=ast.parse(fp.read_text());prefix=[]
for node in tree.body:
    if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='results' for t in node.targets):break
    prefix.append(node)
ns={'__file__':str(fp)};exec(compile(ast.Module(body=prefix,type_ignores=[]),str(fp),'exec'),ns)
records=[];j=0
for group in json.loads((E/'full-tree-milp-candidate-audits-primary/replay-audit/exact_candidate_audit.json').read_text()):
    for record in group['records']:
        item,*_=ns['verify'](record,group['source'],ns['duals'][j]);j+=1
        records.append({k:v for k,v in item.items() if k!='all_node_comparisons'})
assert j==14
reports['fixed_cone_reused_fraction_verifier']={'new_optimizer_calls':0,'records':ns['enc'](records),
    'nodes':sum(x['nodes'] for x in records),'comparisons':sum(x['including_self_comparisons'] for x in records),
    'implementation':str(fp.relative_to(ROOT)),'source_sha256':hashlib.sha256(fp.read_bytes()).hexdigest()}

out=OUT/'replay.json';out.write_text(json.dumps(reports,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'pass','rounded_unique_root':reports['rounded_instance'],
 'constant_zero_candidates':reports['constant_zero_candidates'],
 'fixed_cone_points':j,'fixed_cone_nodes':reports['fixed_cone_reused_fraction_verifier']['nodes'],
 'fixed_cone_comparisons':reports['fixed_cone_reused_fraction_verifier']['comparisons'],
 'indexed_64_table_equality':reports['indexed_table']},ensure_ascii=False))

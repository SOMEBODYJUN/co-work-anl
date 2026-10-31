"""Standalone unit-customer SPE checks and exact observed-dual replay.

No original helper, canonical solver, numpy/scipy or optimizer is imported.
Fourteen gap points and two terminal comparison points are checked on every
ordered history. The saved 14 gap duals are rebuilt against Fraction-lex IC
rows; the old terminal optimum claims are not relabeled new dual checks.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache,reduce
from itertools import product,combinations
from math import gcd,lcm
import hashlib,json

E=Path(__file__).resolve().parent
RAW=E/'original/research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss'
gap=json.loads((RAW/'exact_candidate_audit.json').read_text())
terminal=json.loads((RAW/'terminal_exact_audit.json').read_text())
duals=json.loads((E/'replay-audit/replayed-exact-duals.json').read_text())['records']
def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))

def verify(record,origin,dual=None):
    inst=record['instance'];m=inst['players'];p=len(inst['topics'])
    units=[];types=[0]*((1<<p)-1)
    for c in inst['customers']:
        n=c['multiplicity'];assert isinstance(n,int) and n>=0
        likes=frozenset(c['topics']);assert likes and all(a in range(p) for a in likes)
        units.extend([likes]*n);types[sum(1<<a for a in likes)-1]+=n
    actions={tuple(z['history']):z['action'] for z in record['strategy']['actions']}
    hs=[h for d in range(m) for h in product(range(p),repeat=d)]
    assert len(actions)==len(record['strategy']['actions']) and set(actions)==set(hs)
    assert all(a in range(p) for a in actions.values())
    @lru_cache(None)
    def continuation(h):
        return h if len(h)==m else continuation(h+(actions[h],))
    @lru_cache(None)
    def pay(z,i):
        return sum((F(1,sum(b in likes for b in z)) for likes in units if z[i] in likes),F(0))
    def coefficient(z,a):
        return tuple(F(1,sum(bool(mask & (1<<b)) for b in z)) if mask & (1<<a) else F(0) for mask in range(1,1<<p))
    def cover(support):return tuple(F(any(mask & (1<<a) for a in support)) for mask in range(1,1<<p))
    rows=set();details=[];checks=nonself=0;minimum=None
    for h in hs:
        i=len(h);a=actions[h];z=continuation(h);u=pay(z,i);co=coefficient(z,a)
        alternatives=[]
        for b in range(p):
            zz=continuation(h+(b,));value=pay(zz,i);slack=u-value;assert slack>=0,(origin,h,b,slack)
            checks+=1;nonself+=b!=a;minimum=slack if minimum is None else min(minimum,slack)
            alternatives.append({'action':b,'terminal':zz,'payoff':value,'slack':slack})
            if b!=a:
                diff=tuple(x-y for x,y in zip(co,coefficient(zz,b)))
                if any(diff):rows.add(diff)
        details.append({'history':h,'chosen':a,'terminal':z,'chosen_payoff':u,'alternatives':alternatives})
    root=continuation(());q=tuple(root.count(a) for a in range(p));player=record['normalized_player']
    assert root==tuple(record['actual_path']) and q==tuple(record['strategy']['terminal_counts'])
    U=tuple(pay(root,i) for i in range(m));W=sum(any(a in likes for a in root) for likes in units)
    OPT=max(sum(any(a in likes for a in t) for likes in units) for t in combinations(range(p),min(m,p)))
    assert sum(U)==W and W==record['W'] and OPT==record['OPT'] and U[player]==F(record['utility'])
    gap_slack=m*U[player]-(OPT-W);assert gap_slack==F(record['gap_bridge_slack'])
    ordered_rows=tuple(sorted(rows));norm=coefficient(root,root[player]);welfare=cover(set(root))
    objective=tuple(a-b for a,b in zip(cover(record['portfolio']),welfare)) if dual else None
    dual_result=None
    if dual is not None:
        assert dual['input']==origin and dual['portfolio']==record['portfolio']
        assert len(ordered_rows)==dual['rows_count']
        rowsha=hashlib.sha256(json.dumps(enc(ordered_rows),separators=(',',':')).encode()).hexdigest()
        assert rowsha==dual['rows_fraction_lex_order_sha256']
        assert norm==tuple(map(F,dual['norm'])) and objective==tuple(map(F,dual['objective']))
        v=tuple(map(F,dual['normalized_primal']));beta=F(dual['beta']);mu=[F(0)]*len(ordered_rows)
        for j,value in dual['dual_support']:
            assert mu[j]==0;mu[j]=F(value)
        assert all(vv>=0 for vv in v) and dot(norm,v)==1 and all(dot(row,v)>=0 for row in ordered_rows)
        assert all(vv>=0 for vv in mu)
        residual=tuple(beta*norm[j]-sum(a*row[j] for a,row in zip(mu,ordered_rows))-objective[j] for j in range(len(norm)))
        assert all(vv>=0 for vv in residual) and residual==tuple(map(F,dual['dual_coordinate_residuals']))
        value=dot(objective,v);assert value==beta==F(record['exact_normalized_objective'])==F(record['fixed_cone_exact_dual'])
        D=lcm(*(vv.denominator for vv in v));ints=[int(vv*D) for vv in v];g=reduce(gcd,ints);ints=[a//g for a in ints]
        assert ints==types
        dual_result={'exact_optimum':beta,'dual_support':dual['dual_support'],'IC_rows':len(ordered_rows),
                     'all_type_coordinates':len(norm),'minimum_coordinate_residual':min(residual),
                     'rows_fraction_lex_order_sha256':rowsha,'new_optimizer_calls':0}
    return {'source':origin,'portfolio':record['portfolio'],'m':m,'p':p,'normalized_player':player,
       'customers':len(units),'positive_type_masks':[(j+1,n) for j,n in enumerate(types) if n],
       'distinct_coverages':len({tuple(j for j,likes in enumerate(units) if a in likes) for a in range(p)}),
       'root_path':root,'root_counts':q,'utilities':U,'W':W,'OPT':OPT,'GAP_slack':gap_slack,
       'half_slack':2*W-OPT,'nodes':len(hs),'including_self_comparisons':checks,'nonself_comparisons':nonself,
       'minimum_IC_margin':minimum,'independent_exact_dual_replay':dual_result,'all_node_comparisons':details},units,actions,pay

results=[];index=0
for report in gap:
    for r in report['records']:
        data,*_=verify(r,report['source'],duals[index]);index+=1;results.append(data)
assert index==14
terminal_results=[]
for report in terminal:
    for r in report['records']:
        data,units,actions,pay=verify(r,report['source'])
        if not terminal_results:
            p=data['p'];m=data['m']
            @lru_cache(None)
            def outcomes(h):
                if len(h)==m:return frozenset([h])
                children=[outcomes(h+(a,)) for a in range(p)];i=len(h)
                floor=max(min(pay(z,i) for z in option) for option in children)
                return frozenset(z for option in children for z in option if pay(z,i)>=floor)
            roots=outcomes(());assert len(roots)==26 and tuple(data['root_path']) in roots
            data.update(all_ordered_SPE_root_paths=sorted(roots),root_path_count=26,
              C1_slack=2*data['utilities'][0]-data['utilities'][-1],
              C2_slack=2*data['W']-(m+1)*data['utilities'][-1],
              terminal_fixed_cone_optimum_is_historical_not_new_replayed_dual=True)
        terminal_results.append(data)
assert terminal_results[0]['C1_slack']==F(-1,2) and terminal_results[0]['C2_slack']==0
newmip=json.loads((E/'replay-milp/new_m3p4i0.json').read_text())
oldmip=json.loads((RAW/'milp_m3p4i0.json').read_text())
assert len(newmip['results'])==len(oldmip['results'])==2
for new,old in zip(newmip['results'],oldmip['results']):
    assert new['actions']==old['actions'] and new['types']==old['types']
out={'status':'pass','new_independent_script_runs':1,'timing_recorded':False,'optimizer_calls':0,
 'imports_original_or_canonical':False,'gap_exact_points':results,'terminal_comparison_points':terminal_results,
 'gap_distinct_dual_certificates_replayed':14,'gap_points_nodes':sum(x['nodes'] for x in results),
 'gap_points_including_self_comparisons':sum(x['including_self_comparisons'] for x in results),
 'gap_points_nonself_comparisons':sum(x['nonself_comparisons'] for x in results),
 'terminal_points_nodes':sum(x['nodes'] for x in terminal_results),
 'terminal_points_including_self_comparisons':sum(x['including_self_comparisons'] for x in terminal_results),
 'terminal_points_nonself_comparisons':sum(x['nonself_comparisons'] for x in terminal_results),
 'new_m3p4_MILP_actions_and_types_equal_frozen_reference':True,
 'old_terminal_review_not_rerun':True,'terminal_dual_bounds_not_new_certified':True}
(E/'independent-exact-review.json').write_text(json.dumps(enc(out),ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['gap_exact_points','terminal_comparison_points']},ensure_ascii=False))
for row in results:print(json.dumps(enc({k:v for k,v in row.items() if k not in ['all_node_comparisons','independent_exact_dual_replay']}),ensure_ascii=False))

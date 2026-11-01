"""Exact standalone replay of only the two NEW terminal dual certificates.

No original helper/package, numerical library, or optimizer is imported.
The 15 coordinates and IC rows are reconstructed from the primary graphs.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache,reduce
from itertools import product,combinations
from math import gcd,lcm
import hashlib,json
E=Path(__file__).resolve().parent
raw=json.loads((E/'original/research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/next_boss/terminal_exact_audit.json').read_text())
new=json.loads((E/'replay-terminal-duals/terminal_exact_audit.json').read_text())
duals=json.loads((E/'replay-terminal-duals/observed-exact-duals.json').read_text())['records']
def enc(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):enc(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [enc(x) for x in v]
    return v
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
result=[]
for i,(report,replayed,d) in enumerate(zip(raw,new,duals)):
    rec=report['records'][0];assert replayed['records']==report['records']
    inst=rec['instance'];m=inst['players'];p=len(inst['topics']);assert (m,p)==(3,4)
    ac=rec['strategy']['actions'];actions={tuple(z['history']):z['action'] for z in ac}
    hs=[h for k in range(m) for h in product(range(p),repeat=k)]
    assert len(ac)==len(actions)==len(hs) and set(actions)==set(hs)
    assert all(isinstance(a,int) and a in range(p) for a in actions.values())
    @lru_cache(None)
    def cont(h):return h if len(h)==m else cont(h+(actions[h],))
    def coefficient(z,a):
        return tuple(F(1,sum(bool(B&(1<<b)) for b in z)) if B&(1<<a) else F(0) for B in range(1,1<<p))
    types=[0]*((1<<p)-1);unitlikes=[]
    for c in inst['customers']:
        n=c['multiplicity'];assert isinstance(n,int) and n>=0
        B=sum(1<<a for a in c['topics']);assert B>0
        types[B-1]+=n;unitlikes.extend([frozenset(c['topics'])]*n)
    origins={};checks=[]
    for h in hs:
        z=cont(h);co=coefficient(z,actions[h]);alternatives=[]
        for b in range(p):
            zz=cont(h+(b,));v=coefficient(zz,b)
            g=tuple(x-y for x,y in zip(co,v));margin=dot(g,types);assert margin>=0
            if any(g):origins.setdefault(g,[]).append({'history':h,'chosen':actions[h],'deviation':b,
                'chosen_terminal':z,'deviation_terminal':zz})
            alternatives.append({'action':b,'terminal':zz,'slack':margin})
        checks.append({'history':h,'chosen':actions[h],'terminal':z,'alternatives':alternatives})
    rows=tuple(sorted(origins));assert len(rows)==d['rows_count']
    sha=hashlib.sha256(json.dumps(enc(rows),separators=(',',':')).encode()).hexdigest()
    assert sha==d['rows_fraction_lex_order_sha256']
    root=cont(());j=rec['normalized_player'];norm=coefficient(root,root[j]);objective=coefficient(root,root[-1])
    assert norm==tuple(map(F,d['norm'])) and objective==tuple(map(F,d['objective']))
    x=tuple(map(F,d['normalized_primal']));beta=F(d['beta']);mu=[F(0)]*len(rows)
    for k,value in d['dual_support']:
        assert mu[k]==0;mu[k]=F(value)
    assert all(t>=0 for t in x) and dot(norm,x)==1 and all(dot(g,x)>=0 for g in rows)
    assert all(t>=0 for t in mu)
    residual=tuple(beta*norm[k]-sum(t*g[k] for t,g in zip(mu,rows))-objective[k] for k in range(len(norm)))
    assert residual==tuple(map(F,d['dual_coordinate_residuals'])) and min(residual)>=0
    assert dot(objective,x)==beta==F(rec['exact_normalized_objective'])==F(rec['fixed_cone_exact_dual'])
    D=lcm(*(t.denominator for t in x));ints=[int(t*D) for t in x];gcdval=reduce(gcd,ints);ints=[t//gcdval for t in ints]
    assert ints==types
    U=tuple(dot(coefficient(root,root[k]),types) for k in range(m))
    W=sum(any(a in B for a in root) for B in unitlikes)
    OPT=max(sum(any(a in B for a in J) for B in unitlikes) for J in combinations(range(p),min(m,p)))
    assert root==tuple(rec['actual_path']) and U[j]==F(rec['utility']) and W==rec['W'] and OPT==rec['OPT']
    distinct=len({tuple(k for k,B in enumerate(unitlikes) if a in B) for a in range(p)})
    result.append({'input_record':i,'input_pointer':f'/{i}/records/0','m':m,'p':p,'j_zero_based':j,
      'root':root,'unit_types_mask_multiplicity':[(k+1,t) for k,t in enumerate(types) if t],
      'customers':len(unitlikes),'distinct_topic_coverages':distinct,'utilities':U,'W':W,'OPT':OPT,
      'C1_slack':2*U[j]-U[-1],'C2_slack':2*W-(m+1)*U[-1],'half_slack':2*W-OPT,
      'normalized_primal':x,'primitive_scale_from_x':F(D,gcdval),'beta':beta,'norm':norm,'terminal_objective':objective,
      'node_count':len(hs),'including_self_comparisons':len(hs)*p,'nonself_comparisons':len(hs)*(p-1),
      'unique_nonzero_IC_rows':len(rows),'rows_fraction_lex_order_sha256':sha,
      'all_fraction_lex_IC_rows':rows,'all_ordered_node_checks':checks,
      'complete_dual_support':[{'zero_based_row':k,'multiplier':mu[k],'coefficients':rows[k],
         'one_origin':origins[rows[k]][0],'all_origins':origins[rows[k]]} for k in range(len(rows)) if mu[k]],
      'all_15_coordinate_residuals':residual,'all_coefficients_nonnegative':True,
      'original_and_new_audit_records_identical':True,'optimizer_calls':0})
assert len(raw)==len(new)==len(duals)==len(result)==2
out={'status':'pass','new_standalone_entry_runs':1,'timing_recorded':False,'optimizer_calls':0,
 'imports_original_or_canonical':False,'fixed_cone_terminal_certificates':2,'nodes':42,
 'including_self_comparisons':168,'nonself_comparisons':126,'type_coordinates_each':15,'records':result}
(E/'exact-terminal-duals-review.json').write_text(json.dumps(enc(out),ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='records'}))
for r in result:
    print(json.dumps(enc({k:v for k,v in r.items() if k not in ['all_fraction_lex_IC_rows','all_ordered_node_checks','norm','terminal_objective','normalized_primal']})))

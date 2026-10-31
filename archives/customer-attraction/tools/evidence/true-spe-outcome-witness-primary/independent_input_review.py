"""Standard-library reconstruction of saved fixed-cone proofs and comparison inputs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from functools import lru_cache
import json,hashlib
H=Path(__file__).resolve().parent
B=H/'original/research/workspaces/customer-attraction/R-3d6f7a072d5e489eb5a0bdc4d32bb769/true_spe_search'
def read(p):return json.loads(p.read_text())
def main():
    cert=read(B/'fractional_weak_m4_certificate.json');proofs=read(B/'m4_new_budget_fixed_cone.json');acts={tuple(r['history']):r['action']for r in cert['actions']};assert set(acts)=={h for d in range(4)for h in product(range(4),repeat=d)}
    @lru_cache(None)
    def finish(h):return tuple(h.count(a)for a in range(4))if len(h)==4 else finish(h+(acts[h],))
    def payoff(q,a):return tuple(F(1,sum(q[b]for b in range(4)if mask>>b&1))if mask>>a&1 else F(0)for mask in range(1,16))
    def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
    root=finish(());assert root==tuple(cert['terminal_counts'])==(1,3,0,0)
    c=tuple(F(any(q and(mask>>a&1)for a,q in enumerate(root)))for mask in range(1,16))
    rows=set()
    for h,a in acts.items():
        base=payoff(finish(h),a)
        for b in range(4):
            row=tuple(x-y for x,y in zip(base,payoff(finish(h+(b,)),b)))
            if any(row):rows.add(row)
    rows=sorted(rows);checked=[]
    for rec in proofs['records']:
        a=rec['query'];pr=rec['result'];clones=tuple(map(F,pr['integer_clones']));W=dot(c,clones)
        objective=[]
        for mask in range(1,16):
            load=sum(root[b]for b in range(4)if mask>>b&1)
            g=F(4,4+3*load)if mask>>a&1 else F(0);R=F(3*load,4+3*load)
            objective.append(4*g+R)
        assert tuple(objective)==tuple(map(F,rec['objective']))
        assert all(dot(row,clones)>=0 for row in rows)
        beta=F(pr['exact_dual_bound']);mu=[F(0)]*len(rows)
        for i,v in pr['dual_support']:assert mu[i]==0;mu[i]=F(v)
        residual=[beta*c[j]-sum(v*r[j]for v,r in zip(mu,rows))-objective[j]for j in range(15)]
        assert beta>=0 and min(mu)>=0 and min(residual)>=0
        value=dot(objective,clones)/W;assert value==beta==F(pr['value'])
        checked.append(dict(query=a,value=str(value),W=str(W),nonzero_clones=[[i+1,str(w)]for i,w in enumerate(clones)if w],dual_support=pr['dual_support'],min_dual_coordinate_residual=str(min(residual)),exact_policy_nonself_comparisons=85*3))
    old=read(H/'original/research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/strategy_duality/markov_obstruction_report.json');r=old['legal_types'];f=old['F_boolean']
    def us(s,a):return f[sum(1<<b for b in s)]-f[sum(1<<b for b in s if b!=a)]
    def W(s):return sum(w for mask,w in enumerate(r,1)if any(mask>>a&1 for a in s))
    menus=[]
    for pair in combinations(range(5),2):
        cand=[a for a in range(5)if a not in pair];v={a:us(set(pair)|{a},a)for a in cand};menus.append(dict(pair=''.join(map(str,pair)),actions=[a for a in cand if v[a]==max(v.values())]))
    tables=[dict(triple=''.join(map(str,s)),W=W(s),full_SPE=''.join(map(str,s))in old['all_full_SPE_root_sets'],Markov_SPE=''.join(map(str,s))in old['all_count_Markov_SPE_root_sets'])for s in combinations(range(5),3)]
    assert all(x>0 for x in r)and sum(r)==24831 and W((0,2,3))==22428
    assert min(x['W']for x in tables if x['full_SPE'])==22428 and min(x['W']for x in tables if x['Markov_SPE'])==22429
    assert F(13*3+33)-F(708669,123025)-66==F(29481,123025)>0
    report=dict(status='pass',solver_calls=0,original_main_executions=0,fixed_m4_complete_policy_histories=85,fixed_m4_nonzero_distinct_IC_rows=len(rows),fixed_m4_exact_proofs=checked,Markov_comparison_pair_menus=menus,Markov_comparison_triple_welfare=tables,budget_identity='R=W-G; m*g+R<=2W iff m*g<=W+G',old13_exact_budget_excess='29481/123025',scope='Independent exact coefficient/input reconstruction. Does not repeat 648-map exhaustion or MILP searches, which are separately recorded original executions.')
    (H/'independent-input-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

"""Pressure only: incumbent-reserve aggregate on saved complete SPEs."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations,product
import json
ROOT=Path(__file__).resolve().parents[6]
HERE=Path(__file__).resolve().parent

def check(name,sets,m,policy):
    def leaf(h):
        while len(h)<m:h=h+(policy[h],)
        return h
    def pay(i,z):
        return sum((F(1,sum(x in sets[t] for t in z)) for x in sets[z[i]]),F())
    def cov(z):return set().union(*(sets[t] for t in z)) if z else set()
    nodes=[]
    for k in range(m):
        for h in product(range(len(sets)),repeat=k):
            z=leaf(h);v=[pay(k,leaf(h+(t,))) for t in range(len(sets))]
            assert pay(k,z)==max(v),(name,h)
            p=cov(h);r=m-k
            opt=max(len(p|cov(t)) for size in range(min(r,len(sets))+1) for t in combinations(range(len(sets)),size))
            w=len(cov(z));past=sum((pay(i,z) for i in range(k)),F())
            gap=F(opt)-2*w+past
            nodes.append((gap,h,opt,w,str(past)))
    worst=max(nodes)
    return {'name':name,'players':m,'nodes':len(nodes),'max_F_minus_2W_plus_U_past':str(worst[0]),'worst_history':worst[1],'F':worst[2],'W':worst[3],'U_past':worst[4],'violations':sum(g>0 for g,*_ in nodes)}

def expand(types,n):
    sets=[set() for _ in range(n)]
    for j,(mask,w) in enumerate(types):
        for a in range(n):
            if mask>>a&1:sets[a].update((j,k) for k in range(w))
    return sets

def main():
    out=[]
    for name in ['individual_security_failure','root_tax_failure']:
        ex=json.loads((ROOT/f'examples/customer_attraction/{name}.json').read_text())
        cert=json.loads((ROOT/f'evidence/certificates/customer_attraction/{name}.json').read_text())
        sets=expand([(sum(1<<a for a in c['topics']),c.get('multiplicity',1)) for c in ex['customers']],len(ex['topics']))
        pol={tuple(row['history']):row['action'] for row in cert['strategy']['actions']}
        out.append(check(name,sets,ex['players'],pol))
    p=ROOT/'research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round3_general'
    o=json.loads((p/'equilibrium/fractional_global_raw.json').read_text())
    sets=expand([(int(m),w) for m,w in o['customer_mask_multiplicities'].items()],len(o['topics']))
    out.append(check('fractional_global817',sets,o['players'],{tuple(a['history']):a['action'] for a in o['policy']}))
    o=json.loads((p/'exchange/copy2_counterexample_audit.json').read_text())
    out.append(check('copy2_35',[set(t) for t in o['expanded_topics']],o['players'],{tuple(a['history']):a['action'] for a in o['strategy']}))
    (HERE/'incumbent_reserve_saved_pressure.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

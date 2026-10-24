"""Exact falsification search for the explicit all-ordered-tuple SM candidate.
Uses all pure SPE continuation outcomes, never a fixed anonymous selector.
"""
import json, sys
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
sys.path.insert(0,str(Path(__file__).resolve().parents[7]))
from customer_attraction import Instance, ExactSPESolver


def check(instance):
    p=instance.topic_count; m=instance.players
    solver=ExactSPESolver(instance); roots=solver.outcomes()
    opt=instance.optimal_welfare()
    @lru_cache(None)
    def L(k,a):
        child=k[:a]+(k[a]+1,)+k[a+1:]
        return min(instance.topic_payoff(a,q) for q in solver.outcomes(child))
    cover=[sum(c.multiplicity for c in instance.customers if any((mask>>a)&1 for a in c.topics)) for mask in range(1<<p)]
    best=None; bestopt=None
    # All actual paths for a fixed terminal count are accounted for by DP.
    for q in sorted(roots):
        W=instance.welfare(q); payoff=instance.topic_payoffs(q)
        states={((0,)*p,0):(Fraction(0),(),())}
        for i in range(m):
            nex={}
            for (k,mask),(cost,path,comp) in states.items():
                admissible=[]
                for a in range(p):
                    if k[a]>=q[a]:continue
                    child=k[:a]+(k[a]+1,)+k[a+1:]
                    if q in solver.outcomes(child) and payoff[a]>=solver.threshold(k):admissible.append((a,child))
                for t in range(p):
                    c=cost+L(k,t); newmask=mask|(1<<t)
                    for a,child in admissible:
                        key=(child,newmask)
                        if key not in nex or c<nex[key][0]:nex[key]=(c,path+(a,),comp+(t,))
            states=nex
        for (k,mask),(cost,path,comp) in states.items():
            item=(cost+W-cover[mask],q,path,comp,cost,W,cover[mask])
            if best is None or item[0]<best[0]:best=item
            if cover[mask]==opt and (bestopt is None or item[0]<bestopt[0]):bestopt=item
    return best,bestopt,solver.stats

if __name__=='__main__':
    out=[]
    for path in sorted(Path('examples/customer_attraction').glob('*.json')):
        try:
            data=json.loads(path.read_text()); inst=Instance.from_dict(data)
            if inst.topic_count>8 or inst.players>6:continue
            best,bestopt,stats=check(inst)
            row={'file':str(path),'p':inst.topic_count,'m':inst.players,'best':list(map(str,best)),'bestopt':list(map(str,bestopt)),'stats':str(stats)}
            out.append(row); print(json.dumps(row),flush=True)
            if bestopt[0]<0:break
        except Exception as e:print(str(path),repr(e),flush=True)
    Path(__file__).with_name('existing_results.json').write_text(json.dumps(out,indent=2)+'\n')

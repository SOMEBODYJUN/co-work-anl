"""Attack the peer's five-player helper sum(u1:u3)+Gamma2 >= 3u5.

Gamma2 is explicitly defined here as maximum harmonic two-slot potential at the
actual prefix minus actual terminal potential. A counterexample only refutes
this helper; finite nonfailure proves nothing. Main HALF(5) remains open.
"""
from pathlib import Path
from itertools import combinations_with_replacement
from fractions import Fraction as F
import sys,json,random
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,ExactSPESolver,verify_certificate
HERE=Path(__file__).resolve().parent

def attack(themes):
    inst=Instance.from_topic_sets(themes,5);sol=ExactSPESolver(inst);cache={};bestphi={}
    N=set().union(*themes)
    def data(count):
        count=tuple(count)
        if count not in cache:
            loads=[sum(count[j] for j,t in enumerate(themes) if x in t) for x in N]
            phi=sum(sum(60//v for v in range(1,c+1)) for c in loads)
            u=inst.topic_payoffs(count);v=[int(60*x) for x in u]
            assert all(F(x,60)==y for x,y in zip(v,u))
            cache[count]=(phi,v)
        return cache[count]
    minimum=None;arg=None;checked=0
    for path in sol.ordered_outcomes():
        counts=inst.counts(path,terminal=True);pref=inst.counts(path[:3]);phi,uv=data(counts)
        if pref not in bestphi:
            values=[]
            for a,b in combinations_with_replacement(range(len(themes)),2):
                z=list(pref);z[a]+=1;z[b]+=1;values.append(data(z)[0])
            bestphi[pref]=max(values)
        gamma=bestphi[pref]-phi;us=[uv[t] for t in path]
        gap=sum(us[:3])+gamma-3*us[4];checked+=1
        if minimum is None or gap<minimum:minimum=gap;arg=path
        if gap<0:
            cert=sol.certificate(on_path=path);ver=verify_certificate(inst,cert);ver.assert_valid()
            return {'status':'helper-counterexample','themes':[sorted(t) for t in themes],'path':list(path),'payoffs':[str(F(v,60)) for v in us],'Gamma2':str(F(gamma,60)),'gap':str(F(gap,60)),'W':inst.welfare(counts),'OPT5':inst.optimal_welfare(),'full_checked_histories':ver.checked_histories,'full_checked_deviations':ver.checked_deviations,'certificate':cert.to_dict()}
    return {'status':'no-helper-counterexample','checked_paths':checked,'minimum_gap':str(F(minimum or 0,60)),'minimum_path':arg}

def run():
    rng=random.Random(51625);results=[]
    for trial in range(80):
        n=5+trial%4;k=4+trial%2
        masks=rng.sample(range(1<<n),k);themes=tuple(frozenset(x for x in range(n) if mask>>x&1) for mask in masks)
        res=attack(themes)
        if res['status']=='helper-counterexample':
            res.update({'trial':trial,'scope':__doc__});HERE.joinpath('attack_two_tail_gamma.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({k:v for k,v in res.items() if k!='certificate'}),flush=True);return
        results.append(res)
    result={'status':'no-helper-counterexample-in-selected-inputs','scope':__doc__,'seed':51625,'cases':len(results),'checked_paths':sum(r['checked_paths'] for r in results),'smallest_gap':str(min(F(r['minimum_gap']) for r in results))}
    HERE.joinpath('attack_two_tail_gamma.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
if __name__=='__main__':run()

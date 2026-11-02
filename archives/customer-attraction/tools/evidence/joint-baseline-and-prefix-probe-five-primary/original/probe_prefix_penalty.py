"""Exploratory test of a stronger existential-prefix payment, not a theorem."""
from fractions import Fraction as F
from pathlib import Path
import importlib.util, json, random, time

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
SOURCE=REPO/'research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py'
spec=importlib.util.spec_from_file_location('prior_background_oracle',SOURCE)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)


def best_charge(m,k,weights,prefix,opt):
    types=[];ts={F(0),F(4)}
    for mask,w in weights.items():
        d=sum(opt[a] for a in range(len(opt)) if mask>>a&1)
        if not d:continue
        b=sum(prefix[a] for a in range(len(opt)) if mask>>a&1)
        types.append((w,b,d))
        ts.add(F(4*m*(b+1),d*(k-1)+m*(b+1)))
    def score(t):
        return sum(w*(1-F(2*(k-2)*d,m*(b+k))-min(t*d/(m*(b+1)),(t*d/m+4-t)/(b+k)))
                   for w,b,d in types)
    return min((score(t),t) for t in ts)


def actual_path(sol, terminal_idx):
    path=[];c=[0]*sol.q
    while len(path)<sol.r:
        floor=sol.thresholds[tuple(c)]
        found=False
        for a in range(sol.q):
            new=c.copy();new[a]+=1
            if sol.solve(tuple(new))>>terminal_idx&1 and sol.pays[terminal_idx][a]>=floor:
                path.append(a);c=new;found=True;break
        assert found
    return path


def main():
    rng=random.Random(902103);started=time.time();m=5;q=6
    best=None
    for trial in range(400):
        weights={mask:rng.randint(1,30) for mask in rng.sample(range(1,1<<q),rng.randint(q,3*q))}
        sol=module.BackgroundSolver(q,m,[0]*q,weights)
        welfare_min,actual=sol.minimum();idx=sol.tidx[actual]
        path=actual_path(sol,idx)
        optimum=max(sol.profits)
        opts=[z for z,v in zip(sol.terminals,sol.profits) if v==optimum]
        prefix=[0]*q;early=F(0);all_margins=[]
        for depth in range(m-1):
            k=m-depth
            candidate=min((best_charge(m,k,weights,prefix,opt)+(opt,)) for opt in opts)
            all_margins.append({'k':k,'best_margin':str(candidate[0]-2*early),
                                'best_t':str(candidate[1]),'optimal_counts':candidate[2]})
            a=path[depth];prefix[a]+=1;early+=F(sol.pays[idx][a],sol.scale)
        margin=min(F(z['best_margin']) for z in all_margins)
        if best is None or margin>best[0]:
            obj={'status':'exploratory oracle path; full strategy not yet frozen',
                 'trial':trial,'seed':902103,'m':m,'q':q,'weights':weights,
                 'actual_path':path,'actual_counts':actual,'welfare':str(welfare_min),
                 'optimum':str(optimum),'number_of_optimal_count_profiles':len(opts),
                 'minimum_prefix_payment_margin':str(margin),'margins':all_margins}
            best=(margin,obj)
            (ROOT/'prefix_penalty_probe.json').write_text(json.dumps(obj,indent=2)+'\n')
            print(trial,'margin',margin,'welfare',welfare_min,'opt',optimum,'seconds',round(time.time()-started,2),flush=True)
        if margin>0:
            break
    best[1]['completed_trials']=trial+1
    best[1]['scope']='one lexicographic realizable path of one least-welfare SPE terminal per instance; all optimal count profiles and all k>=2 prefixes'
    best[1]['all_SPE_paths_tested']=False
    best[1]['no_positive_margin_found']=best[0]<=0
    (ROOT/'prefix_penalty_probe.json').write_text(json.dumps(best[1],indent=2)+'\n')
    print(json.dumps(best[1],indent=2))

if __name__=='__main__':main()

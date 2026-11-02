"""Exact diagnostic of r-tail extension of collision-free Q/B family."""
import sys,json
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,ExactSPESolver,verify_certificate

def make(k,r,t,a,b,d):
    x=[{('x',i,j) for j in range(t)} for i in range(k)]
    aa=[{('a',i,j) for j in range(a)} for i in range(k)]
    bb=[{('b',i,j) for j in range(b)} for i in range(r)]
    dd=[{('d',i,j) for j in range(d)} for i in range(r)]
    names=[];cov=[]
    def add(n,c): names.append(n);cov.append(c)
    for i in range(k):
        add('A'+str(i),x[i]|aa[i]);add('C'+str(i),x[i])
        for j in range(r):add('B'+str(i)+'_'+str(j),x[i]|bb[j])
    for j in range(r):add('D'+str(j),bb[j]|dd[j])
    return Instance.from_topic_sets(cov,k+r,tuple(names))

def trial(k,r,t,a,b,d,cert=False):
    ins=make(k,r,t,a,b,d);sol=ExactSPESolver(ins)
    path=tuple(ins.topics.index('C'+str(i)) for i in range(k))+tuple(ins.topics.index('D'+str(j)) for j in range(r))
    target=ins.counts(path,terminal=True)
    outcomes=sol.outcomes();exists=target in outcomes
    result={'params':dict(k=k,r=r,t=t,a=a,b=b,d=d),'instance':ins.to_dict(),'path':list(path),'target_counts':list(target),'target_count_reachable':exists,'path_reachable':False,'target_welfare':ins.welfare(target),'opt':ins.optimal_welfare(),'min_spe_welfare':sol.minimum_welfare(),'worst_ratio':str(sol.inefficiency_ratio()),'count_states':len(sol._outcomes),'root_outcomes':len(outcomes)}
    try:
        c=sol.certificate(on_path=path);v=verify_certificate(ins,c);v.assert_valid();result['path_reachable']=True;result['verification']=str(v)
        if cert:result['certificate']=c.to_dict()
    except ValueError as e:result['path_error']=str(e)
    # Locate first path-prefix failing actual intended continuation comparison.
    for i in range(len(path)):
        pref=ins.counts(path[:i]);child=ins.counts(path[:i+1]);threshold=sol.threshold(pref)
        viable=target in sol.outcomes(child) and ins.topic_payoff(path[i],target)>=threshold
        if not viable:
            result['first_local_failure']={'depth':i,'prefix':list(path[:i]),'action':ins.topics[path[i]],'target_in_child':target in sol.outcomes(child),'actual_payoff':str(ins.topic_payoff(path[i],target)),'threshold':str(threshold)};break
    return result

if __name__=='__main__':
    out=Path(sys.argv[1]);rows=[]
    for tup in [(1,1,2,1,1,1),(2,1,2,1,1,1),(1,2,3,2,2,1),(2,2,3,2,2,1),(2,2,3,2,4,1),(2,2,3,2,3,1)]:
        row=trial(*tup);rows.append(row);print({k:v for k,v in row.items() if k not in ('instance','target_counts','verification')},flush=True)
    out.write_text(json.dumps(rows,indent=2))

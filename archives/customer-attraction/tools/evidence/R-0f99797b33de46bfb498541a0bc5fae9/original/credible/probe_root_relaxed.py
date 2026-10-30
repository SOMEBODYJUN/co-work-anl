"""Finite exact set-valued BI diagnosis of root-relaxed half and insurer spread."""
from pathlib import Path
import json,random,sys
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver
HERE=Path(__file__).resolve().parent

def audit_case(m,p,masses):
    I=Instance(tuple(map(str,range(p))),tuple(CustomerType(frozenset(a for a in range(p) if mask>>a&1),r) for mask,r in enumerate(masses,1) if r),m)
    S=ExactSPESolver(I);O=I.optimal_welfare();C=I.customer_count
    best=None;spread_best=None
    for a in range(p):
        pref=tuple(int(i==a) for i in range(p));qs=S.outcomes(pref)
        lo=min(qs,key=lambda q:(I.welfare(q),q));w=I.welfare(lo)
        if best is None or F(O,w)>best[0]:best=(F(O,w),a,lo,w)
        high=max(qs,key=lambda q:I.topic_payoff(a,q));low=min(qs,key=lambda q:I.topic_payoff(a,q))
        spread=I.topic_payoff(a,high)-I.topic_payoff(a,low)
        z=F((m+1)*spread,C) if C else F(0)
        if spread_best is None or z>spread_best[0]:spread_best=(z,a,high,low,spread)
    return I,S,best,spread_best

def forced_certificate(I,S,a,target):
    actions={():a}
    def expand(h,k,q):
        if len(h)==I.players:return
        floor=S.threshold(k)
        aa=next(j for j in range(I.topic_count) if q in S.outcomes(tuple(k[i]+int(i==j) for i in range(I.topic_count))) and I.topic_payoff(j,q)>=floor)
        actions[h]=aa
        for b in range(I.topic_count):
            child=tuple(k[i]+int(i==b) for i in range(I.topic_count))
            dest=q if b==aa else min(S.outcomes(child),key=lambda q:(I.topic_payoff(b,q),q))
            expand(h+(b,),child,dest)
    for b in range(I.topic_count):
        k=tuple(int(i==b) for i in range(I.topic_count))
        q=target if b==a else min(S.outcomes(k))
        expand((b,),k,q)
    def end(h):
        while len(h)<I.players:h=h+(actions[h],)
        return h
    def u(h,b):return I.topic_payoff(b,I.counts(end(h),terminal=True))
    slacks=[]
    for h,x in actions.items():
        if h:
            for b in range(I.topic_count):slacks.append(u(h,x)-u(h+(b,),b))
    assert min(slacks)>=0
    z=end(());u0=u((),a);ds=[u((b,),b) for b in range(I.topic_count)]
    return {'schema':'full-policy-positive-depth-SPE-v1','instance':I.to_dict(),
            'actions':[{'history':list(h),'action':x} for h,x in sorted(actions.items())],
            'path':list(z),'utilities':list(map(str,I.player_payoffs(z))),
            'root_deviation_payoffs':list(map(str,ds)),'delta':str(max(ds)-u0),
            'W':I.welfare(I.counts(z)),'OPT':I.optimal_welfare(),
            'nonroot_comparisons':len(slacks),'min_nonroot_slack':str(min(slacks))}

def main():
    rng=random.Random(231033);report={'scope':'Finite exact BI diagnostic; no universal theorem from no witness.','seed':231033,'batches':[]}
    any_fail=False
    for m,p,n in [(3,5,80),(4,5,120),(5,6,80),(6,6,40)]:
        best=(F(0),None);sp=(F(0),None)
        for j in range(n):
            # Mix sparse and full incidence, including the empty theme as label 0 in half the cases.
            masses=[rng.randrange(0,8) if rng.random()<(0.28 if j%3 else 0.75) and (j%2 or not(mask&1)) else 0 for mask in range(1,1<<p)]
            if not any(masses):masses[0]=1
            I,S,b,z=audit_case(m,p,masses)
            if b[0]>best[0]:best=(b[0],dict(case=j,a=b[1],q=b[2],W=b[3],OPT=I.optimal_welfare(),masses=masses))
            if z[0]>sp[0]:sp=(z[0],dict(case=j,a=z[1],high=z[2],low=z[3],spread=str(z[4]),customers=I.customer_count,masses=masses))
            if b[0]>2:
                cert=forced_certificate(I,S,b[1],b[2]);fn=f'root_relaxed_half_failure_m{m}p{p}.json';(HERE/fn).write_text(json.dumps(cert,indent=2)+'\n');any_fail=True
                print('FAILURE',fn,cert['W'],cert['OPT'],cert['delta'],flush=True)
                break
        batch={'m':m,'p':p,'tested':j+1,'best_root_relaxed_ratio':str(best[0]),'best_root_relaxed':best[1],
                'best_scaled_insurer_spread':str(sp[0]),'best_spread':sp[1]}
        report['batches'].append(batch)
        (HERE/'root_relaxed_probe.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({k:v for k,v in batch.items() if k not in ('best_root_relaxed','best_spread')}),flush=True)
        if any_fail:break
if __name__=='__main__':main()

from fractions import Fraction as F
from itertools import product
from math import isqrt
import json,sys,platform,hashlib

def instance(r):
    k=r*(r+1)
    machines=[('H',i) for i in range(r)]+[('Q',i) for i in range(1,r)]+[('Z',0)]
    macro=[('b',s) for s in range(r)]
    tiny=[('t',i,u) for i in range(r) for u in range(k)]
    options={j:[(a,F(1)) for a in machines if a[0]!='Z'] for j in macro}
    options.update({j:[(('H',j[1]),F(1,k)),(('Z',0),F(1,k))] for j in tiny})
    x={}
    for j in macro:
        for a,p in options[j]:x[a,j]=F(1,r*r) if a[0]=='H' else F(1,r)
    for j in tiny:x[('H',j[1]),j]=F(r-1,r);x[('Z',0),j]=F(1,r)
    sigma={j:('H',j[1]) for j in macro}
    sigma.update({j: ('Z',0) if j[2]%r==0 else ('H',j[1]) for j in tiny})
    return k,machines,macro,tiny,options,x,sigma

def actual_load(options,machines,schedule):
    loads={a:F(0) for a in machines}
    for j,a in schedule.items():
        choices=dict(options[j]);assert a in choices
        loads[a]+=choices[a]
    return loads

def check_x_components(r):
    k,machines,macro,tiny,options,x,sigma=instance(r)
    seen={key:F(0) for key in x};count=0
    for h in range(r):
        destinations=[('H',h)]+[('Q',i) for i in range(1,r)]
        for rot in range(r):
            sched={j:destinations[(j[1]+rot)%r] for j in macro}
            sched.update({j:('Z',0) if j[1]==h else ('H',j[1]) for j in tiny})
            assert max(actual_load(options,machines,sched).values())==1
            for j,a in sched.items():seen[a,j]+=F(1,r*r)
            count+=1
    assert seen==x
    for j in macro+tiny:assert sum(v for (a,jj),v in x.items() if jj==j)==1
    return count

def check_slots(r):
    k,machines,macro,tiny,options,x,sigma=instance(r)
    # Build all intervals by explicit sorting. This does not use closed-form interval endpoints.
    intervals={};totals={}
    for a in machines:
        eligible=[j for j in macro+tiny if x.get((a,j),0)>0]
        eligible.sort(key=lambda j:(-dict(options[j])[a],j))
        prefix=F(0)
        for j in eligible:
            end=prefix+x[a,j];intervals[a,j]=(prefix,end);prefix=end
        totals[a]=prefix
    injection={};slots=set()
    for j in macro+tiny:
        a=sigma[j]
        if j[0]=='b':s=0
        elif a[0]=='Z':s=j[1]*(r+1)+j[2]//r
        else:
            aa,bb=divmod(j[2],r);assert bb>0;s=aa*(r-1)+bb
        lo,hi=intervals[a,j]
        assert min(hi,s+1)>max(lo,s), (r,a,j,s,lo,hi)
        assert (a,s) not in slots
        slots.add((a,s));injection[j]=(a,s)
    assert len(injection)==len(macro+tiny)
    loads=actual_load(options,machines,sigma)
    assert max(loads.values())==F(2*r-1,r)
    return len(injection)

def frozen_count_oracle(r):
    # Enumerate actual integral numbers of moved tiny jobs in every group, without objective formula shortcuts.
    k,machines,macro,tiny,options,x,sigma=instance(r)
    best=None;arg=None;checked=0
    for ds in product(range(k+1),repeat=r):
        # Each count vector stands for actual schedules; within a group all jobs have identical endpoints/times.
        loads=[F(1)+F(k-d,k) for d in ds]+[F(sum(ds),k)]
        c=max(loads)
        if best is None or c<best:best,arg=c,ds
        checked+=1
    assert best==F(2*r,r+1),(r,best,arg)
    return {'r':r,'count_vectors':checked,'best':str(best),'one_best':arg}

def all_actual_small(r):
    k,machines,macro,tiny,options,x,sigma=instance(r)
    jobs=macro+tiny;best=None;bestfreeze=None;checked=0;alpha_counts={};by_budget=[None]*r
    destinations=[[a for a,p in options[j]] for j in jobs]
    for dest in product(*destinations):
        sch=dict(zip(jobs,dest));loads=actual_load(options,machines,sch);c=max(loads.values())
        if best is None or c<best:best=c
        changed=sum(sch[j]!=sigma[j] for j in macro)
        for d in range(changed,r):
            if by_budget[d] is None or c<by_budget[d]:by_budget[d]=c
        if all(sch[j]==sigma[j] for j in macro):
            if bestfreeze is None or c<bestfreeze:bestfreeze=c
        if c<2:
            s=sum(sch[j][0]=='H' for j in macro)
            assert s<=c/(2-c)
            alpha_counts.setdefault(str(c),set()).add(s)
        checked+=1
    assert best==1 and bestfreeze==F(2*r,r+1)
    for d,bv in enumerate(by_budget):
        ss=r-d;pred=F((2*ss*k+ss)//(ss+1),k)
        assert bv==pred,(r,d,bv,pred)
    return {'r':r,'actual_assignments':checked,'OPT':str(best),'frozen_OPT':str(bestfreeze),'best_by_macro_change_budget':[str(z) for z in by_budget],'macro_home_count_ranges':{a:[min(ss),max(ss)] for a,ss in alpha_counts.items()}}

def threshold_check(delta):
    target=(delta.denominator+delta.numerator-1)//delta.numerator
    r=max(1,(isqrt(1+4*target)-1)//2)
    while r*(r+1)<target:r+=1
    assert F(1,r*(r+1))<=delta<1
    if r>1:assert F(1,(r-1)*r)>delta
    return {'delta':str(delta),'minimal_r':str(r),'tiny':str(F(1,r*(r+1)))}

def frontier_count_oracle(r):
    k=r*(r+1);best=[None]*(r+1);checked=0
    for ds in product(range(k+1),repeat=r):
        zz=sum(ds)
        for ss in range(1,r+1):
            load=max([zz]+[(k if i<ss else 0)+k-ds[i] for i in range(r)])
            if best[ss] is None or load<best[ss]:best[ss]=load
        checked+=1
    for ss in range(1,r+1):assert best[ss]==(2*ss*k+ss)//(ss+1)
    thresholds=[]
    for M in range(k,2*k):
        need=min(r-ss for ss in range(1,r+1) if best[ss]<=M)
        pred=max(0,r-M//(2*k-M))
        assert need==pred,(r,M,need,pred)
        # Two distinct rational alpha values in this integer grid cell.
        for aa in [F(M,k),F(3*M+1,3*k)]:
            assert aa>=1 and aa<2
            mm=(aa*k).numerator//(aa*k).denominator
            assert mm==M and max(0,r-mm//(2*k-mm))==need
        thresholds.append(need)
    return {'r':r,'count_vectors':checked,'best_by_H_macro_count':[best[ss] for ss in range(1,r+1)],'scaled_unit_denominator':k,'all_integer_thresholds_checked':len(thresholds)}

def main():
    components=[{'r':r,'components':check_x_components(r)} for r in range(1,8)]
    slots=[{'r':r,'jobs':check_slots(r)} for r in range(1,21)]
    counts=[frozen_count_oracle(r) for r in range(1,5)]
    assignments=[all_actual_small(r) for r in (1,2)]
    frontiers=[frontier_count_oracle(r) for r in range(1,5)]
    thresholds=[threshold_check(d) for d in [F(1,2),F(1,1000),F(1,10**100+3),F(999,1000)]]
    out={'status':'passed','independence':'No import, read, or call of tiny_reopening generator or solver; independent initial reconstruction hash b853b3d77a7ea559ab7b94e1b1fbb4054e0cd2069cd60647c2029472edb7f753 predates frozen proof review.','exact_arithmetic':'Fraction and integer','python':platform.python_version(),'source_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),'components':components,'slot_injections':slots,'frozen_count_enumerations':counts,'actual_assignment_enumerations':assignments,'sharp_frontier_enumerations':frontiers,'threshold_edges':thresholds}
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()

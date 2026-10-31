from fractions import Fraction as F
from itertools import product
import hashlib,json,sys
from pathlib import Path

def instance(r):
    k=r*(r+1)
    H=list(range(r)); Q=list(range(r,2*r-1)); Z=2*r-1
    jobs=[('b',s) for s in range(r)]+[('t',i,t) for i in range(r) for t in range(k)]
    times={}
    for j in jobs:
        if j[0]=='b': times[j]={i:F(1) for i in H+Q}
        else: times[j]={j[1]:F(1,k),Z:F(1,k)}
    return k,H,Q,Z,jobs,times

def loads(r,sigma):
    k,H,Q,Z,jobs,p=instance(r)
    assert set(sigma)==set(jobs)
    out=[F(0)]*(2*r)
    for j,i in sigma.items():
        assert i in p[j]
        out[i]+=p[j][i]
    return out

def interval_slot_support(r,x):
    k,H,Q,Z,jobs,p=instance(r)
    edges={j:set() for j in jobs}
    for i in range(2*r):
        # Same tiny order on H_i and Z; at Z the groups stay contiguous.
        row=sorted((j for j in jobs if x.get((i,j),0)>0),key=lambda j:(-p[j][i],j))
        start=F(0)
        for j in row:
            end=start+x[i,j]
            for slot in range(start.numerator//start.denominator, -(-end.numerator//end.denominator)):
                if max(start,F(slot))<min(end,F(slot+1)):
                    edges[j].add((i,slot))
            start=end
    return edges

def main():
    results=[]
    for r in range(1,9):
        k,H,Q,Z,jobs,p=instance(r)
        # Independent explicit optimum schedules: h chooses H; rotation allocates labels.
        components=[]
        for h in H:
            places=[h]+Q
            for rot in range(r):
                sig={('b',b):places[(b+rot)%r] for b in range(r)}
                for j in jobs:
                    if j[0]=='t': sig[j]=Z if j[1]==h else j[1]
                assert max(loads(r,sig))==1
                components.append(sig)
        x={}
        for sig in components:
            for j,i in sig.items(): x[i,j]=x.get((i,j),F(0))+F(1,r*r)
        for b in range(r):
            for i in H: assert x[i,('b',b)]==F(1,r*r)
            for i in Q: assert x[i,('b',b)]==F(1,r)
        for j in jobs:
            assert sum(x.get((i,j),0) for i in range(2*r))==1
            if j[0]=='t':
                assert x.get((j[1],j),F(0))==F(r-1,r)
                assert x[Z,j]==F(1,r)
        # Explicit bad ST matching, with all macro jobs at distinct H machines.
        support=interval_slot_support(r,x)
        matching={('b',i):(i,0) for i in H}
        if r==1:
            for t in range(k): matching[('t',0,t)]=(Z,t)
        else:
            for i in H:
                for a in range(r+1):
                    matching[('t',i,a*r)]=(Z,i*(r+1)+a)
                    for b in range(1,r):
                        matching[('t',i,a*r+b)]=(i,a*(r-1)+b)
        assert set(matching)==set(jobs)
        assert len(set(matching.values()))==len(jobs)
        assert all(slot in support[j] for j,slot in matching.items())
        bad={j:s[0] for j,s in matching.items()}
        badloads=loads(r,bad)
        assert max(badloads)==F(2*r-1,r)
        # Freeze macros and hit the globally optimal tiny-reoptimization bound exactly.
        frozen={('b',i):i for i in H}
        for j in jobs:
            if j[0]=='t': frozen[j]=Z if j[2]<2*r else j[1]
        frozenloads=loads(r,frozen)
        exact=F(2*r,r+1)
        assert max(frozenloads)==exact
        assert all(frozenloads[i]==exact for i in H+[Z])
        # Exact independent quotient oracle; tiny labels are exchangeable only here.
        enum=None
        if r<=3:
            enum=min(max([F(2)-F(q,k) for q in qs]+[F(sum(qs),k)])
                     for qs in product(range(k+1),repeat=r))
            assert enum==exact
        frontier=[]
        for d in range(r):
            s=r-d
            units=-(-(2*s*k)//(s+1))
            frontier.append(str(F(units,k)))
        # Raw all-assignment oracle, independent of quotient/symmetry reductions.
        raw=None
        if r<=2:
            allopts={}
            tiny=[j for j in jobs if j[0]=='t']
            best_by_budget=[None]*r
            for bplaces in product(H+Q,repeat=r):
                edits=sum(i!=bplaces[i] for i in H)
                for choices in product((0,1),repeat=len(tiny)):
                    sig={('b',b):bplaces[b] for b in H}
                    for j,z in zip(tiny,choices): sig[j]=Z if z else j[1]
                    c=max(loads(r,sig))
                    for d in range(edits,r):
                        if best_by_budget[d] is None or c<best_by_budget[d]: best_by_budget[d]=c
                    if r==1 or c<2:
                        active=sum(i in H for i in bplaces)
                        if c<2: assert active<=c/(2-c)
            assert best_by_budget==[F(v) for v in frontier]
            raw={'assignments':len(H+Q)**r*2**len(tiny),
                 'best_by_macro_edit_budget':[str(v) for v in best_by_budget]}
        # Verify the exact frontier by a separate integer-capacity oracle for all s.
        if r<=4:
            for s in range(1,r+1):
                enum_s=min(max([F(1)]+[F(2)-F(q,k) for q in qs]+[F(sum(qs),k)])
                           for qs in product(range(k+1),repeat=s))
                assert enum_s==F(frontier[r-s])
        # Independently attain each claimed frontier with a concrete assignment.
        for d in range(r):
            s=r-d
            M=-(-(2*s*k)//(s+1))
            sig={('b',b):(b if b<s else Q[b-s]) for b in H}
            q=2*k-M
            for j in jobs:
                if j[0]=='t': sig[j]=Z if j[1]<s and j[2]<q else j[1]
            assert sum(sig[('b',b)]!=b for b in H)==d
            assert max(loads(r,sig))==F(M,k)
        results.append({'r':r,'k':k,'machines':2*r,'jobs':len(jobs),'components':len(components),
                        'bad_st_makespan':str(max(badloads)), 'frozen_tiny_opt':str(exact),
                        'tiny_quotient_enum':str(enum) if enum is not None else None,
                        'macro_edit_frontier':frontier,'raw_oracle':raw})
    out={'python':sys.version,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'arithmetic':'Fraction only','construction_checks':results,
         'scope':'Exact finite support and full convex-average checks r=1,...,8. Quotient complete tiny assignment enumeration r<=3; conditional-s count enumeration r<=4; raw all-assignment enumeration r<=2. General proof remains separate.'}
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':main()

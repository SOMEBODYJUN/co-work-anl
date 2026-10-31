"""闭环容量释放的独立整数穷举：不导入规范构造或槽核心。"""
from collections import deque
from fractions import Fraction as F
from itertools import product
import json

def instance(k,d):
    scale=4*k*k
    a=4*k*(k-1); tiny=4*(k-1)
    rows=[]; chains=[]; machine=1
    # index 0 denotes special tiny; k denotes macro.
    lengths=[d]*k+[d+k-1]
    root_times=[tiny+1]+[tiny]*(k-1)+[a]
    tails=[2]+[4]*(k-1)+[4]
    for q,length in enumerate(lengths):
        homes=list(range(machine,machine+length));machine+=length
        root_job=len(rows); rows.append([(0,root_times[q]),(homes[0],scale)])
        chain_jobs=[]
        for l,h in enumerate(homes):
            chain_jobs.append(len(rows))
            rows.append([(h,a),(homes[l+1],scale)] if l+1<length else [(h,a),(0,tails[q])])
        chains.append((root_job,chain_jobs,homes))
    # true optimum schedules represented by endpoint bits.
    s0=[0]*len(rows);s1=[0]*len(rows);bad=[0]*len(rows)
    for q,(g,es,hs) in enumerate(chains):
        for j in [g]+es:
            s0[j]=int(q<k);s1[j]=int(q==k);bad[j]=int(q==0)
    return rows,chains,machine,scale,tuple(s0),tuple(s1),tuple(bad)

def loads(rows,bits,m):
    out=[0]*m
    for j,e in enumerate(bits):
        h,p=rows[j][e];out[h]+=p
    return out

def slots(rows,s0,s1,k,m,tie_priority=None):
    masses={}
    for j in range(len(rows)):
        for bit,weight in [(s0[j],1),(s1[j],k-1)]:
            h,p=rows[j][bit];masses[h,j]=masses.get((h,j),0)+weight
    neighbors={j:[] for j in range(len(rows))};slotset=[]
    for h in range(m):
        at=0
        # All tie orders are immaterial to the formula, but ascending j is used here.
        ids=sorted([j for j in range(len(rows)) if masses.get((h,j),0)],key=lambda j:(-dict(rows[j])[h],(tie_priority or {}).get(j,j)))
        for j in ids:
            end=at+masses[h,j]
            for slot in range(at//k,(end+k-1)//k):
                if max(at,k*slot)<min(end,k*(slot+1)):
                    key=(h,slot);neighbors[j].append(key)
                    if key not in slotset:slotset.append(key)
            at=end
    return neighbors,slotset,masses

def slot_realizes(rows,bits,adj):
    owner={}
    # Independent alternating-path matching restricted to actual target machines.
    for j in range(len(rows)):
        todo=deque([j]);parent={j:None};found=None
        while todo and found is None:
            job=todo.popleft();h,_=rows[job][bits[job]]
            for slot in adj[job]:
                if slot[0]!=h:continue
                if slot not in owner:found=(job,slot);break
                old=owner[slot]
                if old not in parent:parent[old]=(job,slot);todo.append(old)
        if found is None:return False
        job,slot=found
        while True:
            owner[slot]=job
            if parent[job] is None:break
            job,slot=parent[job]
    return True

def audit(k,d):
    rows,chains,m,scale,s0,s1,bad=instance(k,d)
    n=len(rows);B=2-F(3,k)+F(3,2*k*k)
    actualB=max(loads(rows,bad,m));assert F(actualB,scale)==B
    assert max(loads(rows,s0,m))==max(loads(rows,s1,m))==scale
    adj,slotset,masses=slots(rows,s0,s1,k,m)
    assert len(slotset)==n and slot_realizes(rows,bad,adj)
    fracload=[sum((dict(rows[j])[h]*F(masses.get((h,j),0),k) for j in range(n) if h in dict(rows[j])),F(0)) for h in range(m)]
    assert all(v<=scale for v in fracload)
    best=None;least_changes=n+1;least_machines=m+1
    minslot=None;minslot_states=[];allowed=slotstates=0
    for bits in product((0,1),repeat=n):
        ls=loads(rows,bits,m);peak=max(ls)
        if best is None or peak<best:best=peak
        if bits!=bad and peak<=actualB:
            allowed+=1
            changed=[j for j in range(n) if bits[j]!=bad[j]]
            touched={rows[j][e][0] for j in changed for e in (bits[j],bad[j])}
            least_changes=min(least_changes,len(changed));least_machines=min(least_machines,len(touched))
        # One-slot nonroot machines are necessary before matching.
        counts=[0]*m
        for j,e in enumerate(bits):counts[rows[j][e][0]]+=1
        if any(counts[h]!=1 for h in range(1,m)) or counts[0]!=k+1:continue
        if not slot_realizes(rows,bits,adj):continue
        slotstates+=1;cost=sum(ls)
        if minslot is None or cost<minslot:minslot=cost;minslot_states=[bits]
        elif cost==minslot:minslot_states.append(bits)
    assert best==scale and least_changes==least_machines==d+1
    assert minslot_states==[bad]
    return dict(k=k,d=d,m=m,n=n,assignments=2**n,at_most_bad_distinct=allowed,slot_assignments=slotstates,
                optimum=str(F(best,scale)),bad=str(B),minimum_changed_jobs=least_changes,minimum_touched_machines=least_machines,
                unique_minimum_cost_assignment=True)

def tie_audit(k,d=1):
    from itertools import permutations
    rows,chains,m,scale,s0,s1,bad=instance(k,d)
    # The only ties at root are k-1 ordinary root tinies and k non-special tails.
    tiny=[chains[q][0] for q in range(1,k)]
    tail=[chains[q][1][-1] for q in range(1,k+1)]
    checked=0
    for u in permutations(tiny):
        for v in permutations(tail):
            priority={j:i for i,j in enumerate(u+v)}
            adj,_,_=slots(rows,s0,s1,k,m,priority)
            assert slot_realizes(rows,bad,adj)
            best=None; winners=[]
            for activation in product((0,1),repeat=k+1):
                bits=[0]*len(rows)
                for q,(g,es,_) in enumerate(chains):
                    for j in [g]+es:bits[j]=activation[q]
                bits=tuple(bits)
                if not slot_realizes(rows,bits,adj):continue
                cost=sum(loads(rows,bits,m))
                if best is None or cost<best:best=cost;winners=[bits]
                elif cost==best:winners.append(bits)
            assert winners==[bad]
            checked+=1
    return {"k":k,"d":d,"all_equal_size_root_tie_orders":checked,
            "scope":"all complete-cycle states in each tie graph; full arbitrary states audited separately"}

if __name__=='__main__':
    results=[audit(k,d) for k,d in [(3,1),(3,2),(4,1),(4,2),(5,1)]]
    print(json.dumps({'arithmetic':'exact integer scaled times and Fraction x','results':results,
                      'tie_checks':[tie_audit(3),tie_audit(4)]},indent=2))

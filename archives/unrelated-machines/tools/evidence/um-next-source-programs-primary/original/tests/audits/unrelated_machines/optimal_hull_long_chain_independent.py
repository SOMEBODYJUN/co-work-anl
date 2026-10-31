#!/usr/bin/env python3
"""长链修复的独立带标签全分配与实际槽图审计；不导入规范构造。"""
from fractions import Fraction as F
from itertools import product
import json,platform,hashlib
from pathlib import Path

def construct(k,d):
    D=d+2*k-1; scale=2*k; a=F(scale-1,scale); delta=F(1,k)
    nodes=1;chains=[]
    for length in [D]+[d]*k:
        homes=list(range(nodes,nodes+length));nodes+=length
        sink=nodes;nodes+=1;chains.append((homes,sink))
    jobs=[]
    for r,(homes,sink) in enumerate(chains): jobs.append((0,homes[0],scale if r==0 else 2,scale))
    own=[]
    for r,(homes,sink) in enumerate(chains):
        ids=[]
        for h,nxt in zip(homes,homes[1:]+[sink]):
            ids.append(len(jobs));jobs.append((h,nxt,scale-1,scale))
        own.append(ids)
    bad=[0]*len(jobs);bad[1]=1
    for j in own[1]:bad[j]=1
    S0=[0]*len(jobs);S1=[0]*len(jobs)
    for r in range(1,k+1):
        S0[r]=1
        for j in own[r]:S0[j]=1
    S1[0]=1
    for j in own[0]:S1[j]=1
    return D,scale,a,delta,nodes,chains,jobs,own,tuple(bad),tuple(S0),tuple(S1)
def load(jobs,bits,nodes):
    ans=[0]*nodes
    for (u,v,x,y),b in zip(jobs,bits):ans[v if b else u]+=y if b else x
    return ans

def row_slots(row):
    out={};at=F(0)
    for j,p,x in sorted(row,key=lambda t:(-t[1],t[0])):
        end=at+x;out[j]=[s for s in range((end.numerator+end.denominator-1)//end.denominator) if min(end,s+1)>max(at,s)];at=end
    return out,(at.numerator+at.denominator-1)//at.denominator

def cover_machine(root_jobs,edges):
    slots={}
    def aug(j,seen):
        for s in edges[j]:
            if s in seen:continue
            seen.add(s)
            if s not in slots or aug(slots[s],seen):slots[s]=j;return True
        return False
    return all(aug(j,set()) for j in root_jobs)

def audit(k,d):
    D,scale,a,delta,nodes,chains,jobs,own,bad,S0,S1=construct(k,d)
    old=load(jobs,bad,nodes);oldsort=tuple(sorted(old,reverse=True));C=2*scale-2
    assert max(old)==C and max(load(jobs,S0,nodes))==scale and max(load(jobs,S1,nodes))==scale
    rows=[[] for _ in range(nodes)]
    for j,(u,v,x,y) in enumerate(jobs):
        p=delta*S0[j]+(1-delta)*S1[j]
        if p<1:rows[u].append((j,F(x,scale),1-p))
        if p>0:rows[v].append((j,F(y,scale),p))
    graphs=[];slotcounts=[]
    for row in rows:
        e,c=row_slots(row);graphs.append(e);slotcounts.append(c)
        assert sum(p*x for _,p,x in row)<=1
    assert slotcounts[0]==k and all(c==1 for c in slotcounts[1:])
    assert graphs[0][0]==[0] and graphs[0][1]==[0]
    rootfeas={mask:cover_machine([j for j in range(k+1) if not (mask>>j)&1],graphs[0]) for mask in range(1<<(k+1))}
    opt=None;minjobs=None;minmachines=None;mincost=None;minmatch=[];lex_count=0;slot_cover_count=0
    for mask in range(1<<len(jobs)):
        bits=tuple((mask>>j)&1 for j in range(len(jobs)))
        L=load(jobs,bits,nodes);makespan=max(L)
        if opt is None or makespan<opt:opt=makespan
        if tuple(sorted(L,reverse=True))<oldsort:
            lex_count+=1
            changed=[j for j,z in enumerate(bits) if z!=bad[j]]
            machines={i for j in changed for i in jobs[j][:2]}
            minjobs=len(changed) if minjobs is None else min(minjobs,len(changed))
            minmachines=len(machines) if minmachines is None else min(minmachines,len(machines))
        # Test actual ST output assignment space; all nonroot machines have exactly one slot.
        counts=[0]*nodes
        for (u,v,x,y),b in zip(jobs,bits):counts[v if b else u]+=1
        if any(c>1 for c in counts[1:]) or not rootfeas[mask&((1<<(k+1))-1)]:continue
        # Independently test actual interval edges by bipartite augmenting matching on EVERY machine.
        machinejobs=[[] for _ in range(nodes)]
        for j,((u,v,x,y),b) in enumerate(zip(jobs,bits)):machinejobs[v if b else u].append(j)
        assert all(cover_machine(machinejobs[i],graphs[i]) for i in range(nodes))
        slot_cover_count+=1
        cost=sum(L)
        if mincost is None or cost<mincost:mincost=cost;minmatch=[bits]
        elif cost==mincost:minmatch.append(bits)
    assert opt==scale
    assert minjobs==d+1 and minmachines==d+2
    assert minmatch==[bad]
    ct=1-delta+d*(1-a);cb=D*(1-a)
    assert cb-ct==F(1,2*k)
    # Strict lex target attained by activating one extra inactive tiny chain.
    target=list(bad);target[2]=1
    for j in own[2]:target[j]=1
    targetload=load(jobs,target,nodes)
    assert max(targetload)==C-2
    return {'k':k,'d':d,'D':D,'a':str(a),'machines':nodes,'jobs':len(jobs),'enumerated_assignments':1<<len(jobs),'OPT':str(F(opt,scale)),'bad_ratio':str(F(C,scale)),'lex_improving_assignments':lex_count,'min_lex_jobs':minjobs,'min_lex_machines':minmachines,'root_first_tiny_forced_or_macro_out':True,'mincost_slot_assignment_unique':True,'slot_covering_machine_assignments':slot_cover_count,'mincost_slot_machine_assignments':len(minmatch),'instance_sha256':hashlib.sha256(json.dumps({'k':k,'d':d,'scale':scale,'jobs':jobs},sort_keys=True).encode()).hexdigest(),'tiny_activation_cost':str(ct),'macro_activation_cost':str(cb),'cost_difference':str(cb-ct),'root_slot_edges':graphs[0]}

runs=[audit(3,1),audit(3,2),audit(4,1)]
print(json.dumps({'status':'PASS','python':platform.python_version(),'arithmetic':'integer loads scaled by 2k; exact Fraction fractional points/slot intervals','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'total_enumerated_assignments':sum(r['enumerated_assignments'] for r in runs),'runs':runs},indent=2))

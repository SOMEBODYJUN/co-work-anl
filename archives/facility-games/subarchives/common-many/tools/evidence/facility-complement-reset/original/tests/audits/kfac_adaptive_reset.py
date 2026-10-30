#!/usr/bin/env python3
"""Independent exact finite audit of adaptive reset fixtures; no polynomial scheduler implementation."""
from fractions import Fraction as F
from itertools import product
import json

def greedy(clients,k,ns):
    q=[0]*ns; W=[0]*ns; a=[-1]*len(clients); trace=[]; opened={}
    for step in range(k):
        scores=[(W[s],q[s]+1) if q[s] else (sum(w for i,(w,A) in enumerate(clients) if a[i]<0 and s in A),1) for s in range(ns)]
        s=0
        for t in range(1,ns):
            if scores[t][0]*scores[s][1]>scores[s][0]*scores[t][1]: s=t
        if not q[s]:
            opened[s]=step
            for i,(w,A) in enumerate(clients):
                if a[i]<0 and s in A: a[i]=s;W[s]+=w
        q[s]+=1; trace.append((s,*scores[s]))
    return q,W,a,trace,opened


BASE=[(110,(0,)),(110,(0,)),(110,(0,)),(114,(0,)),(140,(1,)),(100,(1,)),(80,(1,)),(100,(2,)),(50,(0,1)),(60,(1,2)),(5,(0,2))]

def lpt(C,pool,n):
 bins=[[] for _ in range(n)];W=[0]*n
 for i in sorted(pool,key=lambda i:(-C[i][0],i)):
  j=min(range(n),key=lambda j:(W[j],j));bins[j].append(i);W[j]+=C[i][0]
 return bins,W

def loads(C,bins):return [sum(C[i][0] for i in b) for b in bins]
def ne_moves(C,layout,bins):
 W=loads(C,bins)
 return [(i,s,t) for s,bin in enumerate(bins) for i in bin for t in range(len(layout)) if t!=s and layout[t] in C[i][1] and W[s]-C[i][0]>W[t]]
def served_check(C,layout,bins):
 ass=[i for b in bins for i in b]
 assert len(ass)==len(set(ass))
 assert set(ass)=={i for i,(w,A) in enumerate(C) if any(s in A for s in layout)}
 assert all(layout[s] in C[i][1] for s,b in enumerate(bins) for i in b)
def audit(augmented=False):
 C=list(BASE);ns=3
 if augmented:
  C[8]=(50,(0,1,3));C[9]=(60,(1,2,3));C.append((37,(3,)));ns=4
 q,W0,a,tr,opened=greedy(C,8,ns)
 assert q==[4,3,1]+([0] if augmented else [])
 assert [x[0] for x in tr]==[0,1,0,1,0,1,0,2]
 assert [F(x[1],x[2]) for x in tr]==list(map(F,[499,380,F(499,2),190,F(499,3),F(380,3),F(499,4),100]))
 gamma=F(tr[-1][1],tr[-1][2])
 pools=[[i for i,s in enumerate(a) if s==t] for t in range(ns)]
 ell=[min((w for w,A in C if A==(t,)),default=0) if sum(A==(t,) for w,A in C)>=q[t] else 0 for t in range(ns)]
 normal={};deleted={}
 layout=[0]*4+[1]*3+[2]
 for s in range(3):
  normal[s],lw=lpt(C,pools[s],q[s]);assert min(lw)>=gamma
  if q[s]>1:
   deleted[s],dw=lpt(C,pools[s],q[s]-1)
   assert max(dw)<=2*max(gamma,ell[s])
 bins=[b[:] for s in range(3) for b in normal[s]]
 # There is a concrete two-improvement NE from the LPT first allocation.
 for target_i in [10,8]:
  candidates=[m for m in ne_moves(C,layout,bins) if m[0]==target_i]
  assert candidates
  i,s,t=min(candidates,key=lambda m:(m[2],m[1]));bins[s].remove(i);bins[t].append(i)
 served_check(C,layout,bins);assert not ne_moves(C,layout,bins)
 onW=loads(C,bins);assert sorted(onW[:4])==[110,110,110,114] and sorted(onW[4:7])==[140,140,150] and onW[7]==105
 assert min(onW)>=gamma
 rows=[]
 for f,u in enumerate(layout):
  for r in range(ns):
   if r==u:continue
   cap=2*max(gamma,ell[u]) if q[u]>=2 else 2*gamma
   nl=layout[:];nl[f]=r;bs=[[] for _ in layout]
   for s in range(3):
    fs=[g for g,t in enumerate(layout) if t==s and g!=f]
    if not fs:
     for i in pools[s]:
      opts=[g for g,t in enumerate(nl) if t in C[i][1]]
      if opts:bs[f].append(i)
     continue
    pk=deleted[s] if s==u else normal[s]
    for g,p in zip(fs,pk):bs[g]=p[:]
   previously_served={i for pool in pools for i in pool}
   for i,(w,A) in enumerate(C):
    if i not in previously_served and r in A:bs[f].append(i)
   served_check(C,nl,bs)
   before=loads(C,bs);assert max(before)<=cap
   new_weight=sum(C[i][0] for i in bs[f]);seen=set();steps=0
   while (moves:=ne_moves(C,nl,bs)):
    key=tuple(tuple(sorted(b)) for b in bs);assert key not in seen;seen.add(key)
    i,s,t=min(moves,key=lambda m:(m[0],m[2],m[1]))
    old=loads(C,bs);bs[s].remove(i);bs[t].append(i);new=loads(C,bs)
    assert sum(x*x for x in new)<sum(x*x for x in old)
    assert max(new)<=cap;steps+=1
   served_check(C,nl,bs);assert not ne_moves(C,nl,bs)
   after=loads(C,bs);assert after[f]<=2*onW[f]
   rows.append(dict(f=f,source=u,target=r,a=onW[f],cap=str(cap),deviator=after[f],new_weight=new_weight,steps=steps))
 assert len(rows)==8*(ns-1)
 return dict(augmented=augmented,q=q,gamma=str(gamma),forced_floors=ell,initial_pool_totals=W0,normal_loads={s:loads(C,normal[s]) for s in normal},deletion_loads={s:loads(C,deleted[s]) for s in deleted},on_path_loads=onW,all_labeled_deviations=rows)
if __name__=='__main__':
    base,extra=audit(),audit(True)
    print(json.dumps({'status':'exact finite audit passed','base_deviations':len(base['all_labeled_deviations']),'augmented_deviations':len(extra['all_labeled_deviations']),'gamma':base['gamma'],'base_on_path_loads':base['on_path_loads']},indent=2))

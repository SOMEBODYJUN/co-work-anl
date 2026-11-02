exec(open('/workspace/scratch/6f91cee763bb/enum_spe.py').read().split("if __name__=='__main__':")[0])
from itertools import permutations,product,combinations

def bestcost(tree,S,N,m,T):
 actual=actual_path_tree(tree); C=set().union(*T); C0=set().union(*actual); R=C-C0; G=len(C0-C); u=pay(actual,N)
 nodes=[];t=tree;pref=[]
 for i in range(m):
  nodes.append((i,pref.copy(),t)); A,ch=t;pref.append(A);t=ch[A][1]
 # state profile cache
 profcache={}
 def prof(i,a):
  k=(i,a)
  if k not in profcache: profcache[k]=terminal_forced(nodes[i][2],a)
  return profcache[k]
 @lru_cache(None)
 def V(i,a,x):
  p=prof(i,a); D=pay(p,N)[i]
  F=[j for j in range(i+1,m) if x in p[j]]
  c=1+len(F)
  val=Fraction(u[i],D) / c if D else Fraction(10**9)
  if F:
   val += Fraction(len(F),c)*min(V(j,p[j],x) for j in F)
  return val
 # each x choose owner theme j and role s; evaluate permutations role->theme
 best=None;bestarg=None
 for perm in permutations(range(m)): # role s gets T[perm[s]]
  total=Fraction(0); owners={}
  for x in R:
   choices=[(V(s,T[j],x),s,j) for s,j in enumerate(perm) if x in T[j]]
   if not choices: raise Exception('no')
   vv,s,j=min(choices)
   total+=vv;owners[x]=(s,j,vv)
  if best is None or total<best:best,bestarg=total,(perm,owners)
 return best,G,len(R),u,actual,C,bestarg

if __name__=='__main__':
 from itertools import chain
 for n in (2,3):
  N=tuple(range(n)); allsubs=[frozenset(x for x in N if mask>>x&1) for mask in range(1<<n)]
  for k in (4,):
   for S in combinations(allsubs,k):
    if not any(S):continue
    m=3;E=gen(N,S,m)
    if len(E)>20000:continue
    best=-1;Ts=[]
    for T in product(S,repeat=m):
      o=len(set().union(*T))
      if o>best:best=o;Ts=[T]
      elif o==best:Ts.append(T)
    worst=None
    for p,t in E:
      for T in Ts:
       q=bestcost(t,S,N,m,T)
       # candidate cost <= W+G? 
       W=sum(q[3]); cost=q[0];G=q[1]
       if worst is None or cost-W-G>worst[0]:worst=(cost-W-G,q,T,t,q)
    if worst and worst[0]>0:
      print('VIOL cand',n,S,'E',len(E),'delta',worst[0],'q',worst[4]);raise SystemExit
   print('done',n,k)
 print('none')

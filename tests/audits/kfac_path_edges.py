from fractions import Fraction as F
S=('H','M','N','L')
w=list(map(F,(184,140,89,41,14,10,6)))
opt=tuple(map(set,({'H'},{'M'},{'N'},{'L'},{'H','M'},{'M','N'},{'N','L'})))
a=[None]*7
q=dict.fromkeys(S,0)
def totals():return {s:sum((w[i] for i in range(7) if a[i]==s),F(0)) for s in S}
trace=[]
for j in range(10):
 W=totals();score={s:W[s]/(q[s]+1) if q[s] else sum((w[i] for i in range(7) if a[i] is None and s in opt[i]),F(0)) for s in S}
 t=max(S,key=lambda s:score[s]); assert sum(score[s]==score[t] for s in S)==1
 trace.append((t,score[t]));
 if not q[t]:
  for i in range(7):
   if a[i] is None and t in opt[i]:a[i]=t
 q[t]+=1
assert trace==list(zip(('H','M','H','N','M','H','M','H','N','L'),map(F,(198,150,99,95,75,66,50,'99/2','95/2',41))))
assert q==dict(zip(S,(4,3,2,1)));assert totals()==dict(zip(S,(198,150,95,41)))
for i,src,dst in ((6,'N','L'),(5,'M','N')):
 W=totals(); assert a[i]==src;assert (W[src]-w[i])/q[src]>W[dst]/q[dst];a[i]=dst
 W=totals();assert all(q[s]*41<=W[s]<=(q[s]+1)*41 for s in S)
W=totals();assert W==dict(zip(S,(198,140,99,47)))
assert all((W[a[i]]-w[i])/q[a[i]]<=W[s]/q[s] for i in range(7) for s in opt[i] if s!=a[i])
assert F(89,2)>41
print('PASS: exact strict greedy trace, two strict path moves, full box, all customer NE inequalities, initial RANGE failure')

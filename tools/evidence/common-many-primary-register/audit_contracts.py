from fractions import Fraction as F
from itertools import product
import json

def eq_instance(q,c,d,menus):
 h=[min(a) for a in menus]; H=[h.count(t) for t in range(len(q))]; b=[c[t]-d*H[t] for t in range(len(q))]
 rows=[]
 for a in product(*menus):
  N=[a.count(t) for t in range(len(q))]; X=[b[t]+d*N[t] for t in range(len(q))]
  psi=sum((b[t]*N[t]+d*N[t]*(N[t]-1)/2)/q[t] for t in range(len(q)))
  ne=all((X[a[i]]-d)/q[a[i]]<=X[v]/q[v] for i in range(len(a)) for v in menus[i])
  lower=all(x>=0 for x in X); box=lower and all(x<=1 for x in X)
  home=all((X[a[i]]-d)/q[a[i]]<=(1-d)/q[h[i]] for i in range(len(a)))
  rows.append(dict(a=a,X=list(map(str,X)),psi=str(psi),ne=ne,lower=lower,box=box,H=home))
 pmin=min(F(r['psi']) for r in rows); cpmin=min(F(r['psi']) for r in rows if r['lower'])
 mins=[r for r in rows if F(r['psi'])==pmin]; cmins=[r for r in rows if r['lower'] and F(r['psi'])==cpmin]
 assert [r['a'] for r in mins]==[r['a'] for r in cmins]
 assert all(r['box'] and r['H'] and r['ne'] for r in mins)
 return rows,mins
old_rows,oldmins=eq_instance((3,2,1),(F(27,41),F(8,41),F(0)),F(10,41),((0,1),(1,2)))
assert [r['a'] for r in oldmins]==[(1,2)]
adversary,advmins=eq_instance((3,2,1,1),(F(1,10),F(1,10),F(1,25),F(0)),F(1,2),((0,1),(1,2)))
assert [r['a'] for r in advmins]==[(0,1)]
assert adversary[-1]['ne'] and not adversary[-1]['box'] and adversary[-1]['H']
q=(1,1,2,1,3); clients=((200,(0,)),(128,(0,2)),(231,(2,1)),(240,(2,)),(68,(0,3)),(330,(3,)),(60,(2,4)),(740,(4,)),(200,(1,)))
rows=[]
for a in product(*(m for w,m in clients)):
 W=[sum(w for (w,m),t in zip(clients,a) if t==s) for s in range(5)]
 sq=[sum(w*w for (w,m),t in zip(clients,a) if t==s) for s in range(5)]
 P=sum(F(W[s]*W[s]-sq[s],2*q[s]) for s in range(5))
 ne=all(F(W[a[i]]-w,q[a[i]])<=F(W[v],q[v]) for i,(w,m) in enumerate(clients) for v in m)
 rows.append(dict(a=a,W=W,P=str(P),NE=ne))
nes=[r for r in rows if r['NE']]; pmin=min(F(r['P']) for r in rows); mins=[r for r in rows if F(r['P'])==pmin]
assert len(rows)==16 and len(nes)==2 and len(mins)==1
assert mins[0]['W']==[268,431,428,330,740] and pmin==86200
assert F(430,214)==F(215,107)>2
q2=(3,2,1,1); c=(F(44,45),F(44,45),F(2,45),F(0)); ws=(F(4,5),F(44,45)); menus=((0,1),(1,2)); homes=(0,1)
ph=[]
for a in product(*menus):
 X=[c[t]+sum(ws[i] for i in range(2) if a[i]==t)-sum(ws[i] for i in range(2) if homes[i]==t) for t in range(4)]
 phi=sum((X[t]*X[t]-sum(ws[i]*ws[i] for i in range(2) if a[i]==t))/(2*q2[t]) for t in range(4))
 ph.append(dict(a=a,X=list(map(str,X)),Phi=str(phi)))
assert [F(r['Phi']) for r in ph]==list(map(lambda x:F(x,6075),(326,590,2414,302)))
assert -F(88,2025)+F(32,675)==F(8,2025)>0
print(json.dumps({'status':'passed','scope':'four exact finite mathematical cross-checks; not a rerun of canonical flow or scheduling software','old_equal_weight_four_states':old_rows,'old_equal_weight_optimizer':oldmins,'local_NE_adversary_four_states':adversary,'fixed_layout_potential_all_16_assignments':rows,'fixed_layout_potential_NEs':nes,'fixed_layout_potential_unique_minimum':mins,'two_weight_four_states':ph,'new_original_program_runs':0},indent=2))

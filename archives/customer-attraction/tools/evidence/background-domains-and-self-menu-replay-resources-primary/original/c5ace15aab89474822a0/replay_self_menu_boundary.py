"""Independent unit-customer replay of existing empty-background SELF failure.
No canonical solver imported. Checks every ordered history and the exact
response-covariance identity. This recovers an old result, not a new game.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[5]
S=ROOT/'research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json'
p=json.loads(S.read_text());I=p['instance'];m=I['players'];k=len(I['topics'])
clients=[frozenset(x['topics'])for x in I['customers']for _ in range(x['multiplicity'])]
actions={tuple(x['history']):x['action']for x in p['certificate']['actions']}
q=list(map(F,p['query_probability']))
def end(h):
 while len(h)<m:h+=(actions[h],)
 return h
def payoff(z,i):return sum((F(1,sum(a in X for a in z))for X in clients if z[i]in X),F(0))
def cover(z):return sum(any(a in X for a in z)for X in clients)
n=c=0
for d in range(m):
 for h in product(range(k),repeat=d):
  n+=1;v=payoff(end(h),d)
  for a in range(k):
   if a==actions[h]:continue
   c+=1;assert v>=payoff(end(h+(a,)),d)
root=[end((a,))for a in range(k)]
D=sum((q[a]*payoff(root[a],0)for a in range(k)),F(0))
C=sum((q[t]*q[a]*sum((F(1,1+sum(b in X for b in root[a]))for X in clients if t in X),F(0))for t in range(k)for a in range(k)),F(0))
cov=F(0);refund=F(0)
for X in clients:
 px=sum(q[a]for a in X)
 f=[F(1,1+sum(a in X for a in z[1:]))for z in root]
 cov+=sum((q[a]*int(a in X)*f[a]for a in range(k)),F(0))-px*sum((q[a]*f[a]for a in range(k)),F(0))
 refund+=px*sum((q[a]*int(a in X)*f[a]/(2+sum(b in X for b in root[a][1:]))for a in range(k)),F(0))
assert D==F(29,30) and C==F(41,40) and D-C==F(-7,120)
assert cov+refund==D-C
Z=end(());u=payoff(Z,0);assert u==F(29,3)
out={'scope':'Existing root b=0 SELF-MENU refutation recovered; not Mfull or HALF refutation.','source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'customers':len(clients),'m':m,'topics':k,'ordered_histories':n,'nonself_IC':c,'all_IC_passed':True,'actual':Z,'payoffs':[str(payoff(Z,i))for i in range(m)],'W':cover(Z),'OPT':max(cover(z)for z in product(range(k),repeat=m)),'p':[str(v)for v in q],'D':str(D),'C':str(C),'response_covariance':str(cov),'self_refund':str(refund),'D_minus_C':str(D-C),'root_IC_slack':str(u-D),'u_minus_C':str(u-C)}
(P/'self_menu_boundary_replay.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))

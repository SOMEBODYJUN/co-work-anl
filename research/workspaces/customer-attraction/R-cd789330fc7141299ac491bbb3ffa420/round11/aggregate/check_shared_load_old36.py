"""One named auxiliary diagnostic: C<=0 at a shared-load optimizer.
Uses only old36 complete SPE; not a welfare counterexample or general proof.
"""
import json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[6]
a=json.loads((ROOT/'examples/customer_attraction/aggregate_theta_failure.json').read_text())
s=json.loads((ROOT/'evidence/certificates/customer_attraction/aggregate_theta_failure.json').read_text())
policy={tuple(row['history']):row['action'] for row in s['strategy']['actions']}
m=a['players'];k=len(a['topics']);types=a['customers']
inc=np.array([[int(j in c['topics']) for c in types] for j in range(k)])
w=np.array([c['multiplicity'] for c in types])
def leaf(h):
 h=list(h)
 while len(h)<m:h.append(policy[tuple(h)])
 return tuple(h)
z=leaf(())
cols=np.array([[sum(inc[t] for j,t in enumerate(leaf(z[:i]+(b,))) if j!=i) for b in range(k)] for i in range(m)])
p=np.array([0,0,.5,0,0,.5]);rho=p@inc
objective=lambda q:np.sum(w*rho/(1+np.einsum('ij,ijx->x',q.reshape(m,k),cols)/m))
def jac(q):
 L=np.einsum('ij,ijx->x',q.reshape(m,k),cols)/m
 return (-np.einsum('ijx,x->ij',cols,w*rho/(1+L)**2)/m).ravel()
res=minimize(objective,np.full(m*k,1/k),jac=jac,bounds=[(0,1)]*(m*k),constraints=[{'type':'eq','fun':lambda q:q.reshape(m,k).sum(axis=1)-1,'jac':lambda q:np.kron(np.eye(m),np.ones((1,k)))}],method='SLSQP',options={'ftol':1e-13,'maxiter':1000})
q=[[F(float(x)).limit_denominator(10000) for x in row] for row in res.x.reshape(m,k)]
print('float minimum',res.fun,'q',q,'success',res.success)
# Candidate rationalization is only accepted if exact simplex and KKT pass.
assert all(sum(qi)==1 and min(qi)>=0 for qi in q)
colsf=[[[F(int(x)) for x in col] for col in row] for row in cols]
pp=[F(str(x)) for x in p];rr=[sum(pp[j]*int(inc[j,x]) for j in range(k)) for x in range(len(types))]
L=[sum(q[i][j]*colsf[i][j][x] for i in range(m) for j in range(k))/m for x in range(len(types))]
t=[1/(1+l) for l in L]
values=[[sum(F(int(w[x]))*rr[x]*t[x]**2*colsf[i][b][x] for x in range(len(types))) for b in range(k)] for i in range(m)]
print('kkt residual',max(float(max(values[i])-values[i][b]) for i in range(m) for b in range(k) if q[i][b]))
C=sum(pp[j]*sum(F(int(w[x]))*int(inc[j,x])*t[x]**2*(colsf[i][j][x]-L[x]) for x in range(len(types))) for i in range(m) for j in range(k))
D=sum(pp[j]*sum(F(int(w[x]))*int(inc[j,x])*t[x]**2*(colsf[i][j][x]-L[x])**2/(1+colsf[i][j][x]) for x in range(len(types))) for i in range(m) for j in range(k))
W=F(34);val=sum(F(int(w[x]))*rr[x]*t[x] for x in range(len(types)))
assert W-m*val==D-C
out={'scope':'old36 only, feasible rational columns; floating optimum is not certified; exact balance and C sign only','p':[str(x) for x in pp],'q':[[str(x) for x in row] for row in q],'F_shared':str(val),'W_minus_mF':str(W-m*val),'C':str(C),'D':str(D),'IC_sum':'0','strong_C_nonpositive':C<=0}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

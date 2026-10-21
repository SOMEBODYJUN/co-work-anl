"""Finite column proof exploration; all 6-label binary memberships are retained."""
import itertools
import numpy as np
from scipy.optimize import linprog
from fractions import Fraction as F
bits=list(itertools.product((0,1),repeat=6))
names=[]
cols=[]
def U(x,y):return F(x,1+y) if x else F(0)
def column(z):
 a,b,t,s,q,r=z
 acts=[a,b,t,s,q,r]
 u1,u2=U(a,b),U(b,a)
 vals=[]
 labels=[]
 for label,x in zip('ABTSQR',acts):
  vals.append(u2-U(x,a));labels.append('actual_B>='+label)
 for label,x in zip('ABTSQR',acts):
  vals.append(U(q,t)-U(x,t));labels.append('reply_Q>='+label)
 for label,x in zip('ABTSQR',acts):
  vals.append(U(r,s)-U(x,s));labels.append('reply_R>='+label)
 vals += [u1-U(t,q),u1-U(s,r),2*u1-q,2*u1-r]
 labels += ['root_T','root_S','root_Q_floor','root_R_floor']
 return labels,vals
names=column(bits[0])[0]
arr=np.array([[float(v) for v in column(z)[1]] for z in bits]).T
W=np.array([int(z[0]+z[1]>0) for z in bits])
O=np.array([int(not(z[0]+z[1]) and z[2]+z[3]>0) for z in bits])
lp=linprog(W,A_ub=-arr,b_ub=np.zeros(len(names)),A_eq=[O],b_eq=[1],bounds=(0,None),method='highs')
print(lp.message,'minimum',lp.fun)
print('dual',[(n,F(float(-v)).limit_denominator(10000)) for n,v in zip(names,lp.ineqlin.marginals) if abs(v)>1e-8])
print('support',[(z,F(float(v)).limit_denominator(10000)) for z,v in zip(bits,lp.x) if v>1e-8])

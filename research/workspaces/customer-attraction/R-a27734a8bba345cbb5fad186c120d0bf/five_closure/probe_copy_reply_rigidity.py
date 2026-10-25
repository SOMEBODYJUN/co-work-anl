"""Numerical discovery of root rigidity with an actual off-path copy reply.
This is a source of candidates, never an exact universal certificate.
"""
import numpy as np,json
from itertools import product,combinations_with_replacement
from scipy.optimize import linprog
from pathlib import Path
m=5
# Topic indices T Q B2 B3 B4 B5 C; C=last reply after penultimate chooses B5.
bits=np.array(list(product((0,1),repeat=7)),dtype=int);N=len(bits);p=bits[:,0];q=bits[:,1]
acts=bits[:,[0,2,3,4,5]];load=acts.sum(axis=1)
def share(a,den):return np.divide(a,den,out=np.zeros(N,dtype=float),where=den!=0)
prof=[share(acts[:,j],load) for j in range(m)];A=[];names=[]
def add(name,v,uc=0):A.append(np.r_[v,uc]);names.append(name)
add('root-real-IC',-prof[0],1)
for j in range(7):add(f'size-{j}',-bits[:,j],5)
for stage in range(1,5):
 prefix=acts[:,:stage].sum(axis=1)
 for j in range(7):add(f'floor-s{stage}-q{j}',prof[stage]-bits[:,j]/(prefix+5-stage))
prefix=acts[:,:3].sum(axis=1);forced=bits[:,5];reply=bits[:,6];newload=prefix+forced+reply
add('penultimate-real-copy-B5',prof[3]-share(forced,newload))
for j in range(7):add(f'copy-reply-BR-{j}',share(reply,newload)-bits[:,j]/(prefix+forced+1))
# Actual last BR vs C is already floor-s4-q6 (no future at s4).
# Full genuine last-two H envelopes at both terminal histories.
for lab,bg,first,last in [('actual',prefix,bits[:,4],bits[:,5]),('copy',prefix,bits[:,5],bits[:,6])]:
 den=bg+first+last;H=share(first+last,den)+first/((bg+1)*(bg+2))
 for j,k in combinations_with_replacement(range(7),2):
  x=bits[:,j];y=bits[:,k]
  add(f'{lab}-pair-{j}-{k}',H-(x+y)/(bg+1)+x*y/((bg+1)*(bg+2)))
A=np.array(A);eq=np.r_[-p,5];objective=np.r_[q/(1+4*p),-1]
res=linprog(-objective,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=[eq],b_eq=[1],bounds=(0,None),method='highs')
print(res.success,-res.fun if res.success else res.message)
if res.success:
 active=[{'name':n,'weight':float(-v)} for n,v in zip(names,res.ineqlin.marginals) if abs(v)>1e-7];print(active)
 out={'scope':'Floating exploratory optimum; not an exact bound','slope':float(-res.fun),'active_rows':active,'equality_dual':float(res.eqlin.marginals[0]),'positive_primal':[(int(i),list(map(int,bits[i])) if i<N else 'u',float(v)) for i,v in enumerate(res.x) if v>1e-8]}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')

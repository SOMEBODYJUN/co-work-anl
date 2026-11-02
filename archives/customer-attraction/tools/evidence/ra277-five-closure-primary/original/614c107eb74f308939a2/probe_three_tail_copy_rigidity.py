"""Exploratory root rigidity: third-player true deviation with genuine two-tail.
No floating result is a theorem. Exact certificate required separately.
"""
import numpy as np,json
from itertools import product,combinations_with_replacement
from scipy.optimize import linprog
from pathlib import Path
# T,Q,B2,B3,B4,B5,C,D,E. Original root-T leaf and two true deviations to B5.
labels=['T','Q','B2','B3','B4','B5','C','D','E'];P=len(labels)
bits=np.array(list(product((0,1),repeat=P)),dtype=int);N=len(bits);t=bits[:,0];q=bits[:,1]
paths={'original':[0,2,3,4,5],'copy4':[0,2,3,5,6],'copy3':[0,2,5,7,8]}
rows=[];names=[];profs={}
def sh(x,d):return np.divide(x,d,out=np.zeros(N,dtype=float),where=d!=0)
def add(name,v,uc=0):rows.append(np.r_[v,uc]);names.append(name)
for lab,inds in paths.items():
 acts=bits[:,inds];load=acts.sum(axis=1);profs[lab]=[sh(acts[:,j],load) for j in range(5)]
add('root-real-IC',-profs['original'][0],1)
for j in range(P):add(f'size-{labels[j]}',-bits[:,j],5)
add('IC-original4-copy5',profs['original'][3]-profs['copy4'][3])
add('IC-original3-copy5',profs['original'][2]-profs['copy3'][2])
for lab,stages in [('original',range(1,5)),('copy4',[4]),('copy3',[3,4])]:
 inds=paths[lab];acts=bits[:,inds]
 for stage in stages:
  pref=acts[:,:stage].sum(axis=1)
  for j in range(P):add(f'{lab}:floor:{stage}:{labels[j]}',profs[lab][stage]-bits[:,j]/(pref+5-stage))
 if lab!='copy4':
  pref=acts[:,:3].sum(axis=1);H=profs[lab][3]+profs[lab][4]+acts[:,3]/((pref+1)*(pref+2))
  for j,k in combinations_with_replacement(range(P),2):
   x=bits[:,j];y=bits[:,k];add(f'{lab}:pair:{labels[j]}:{labels[k]}',H-(x+y)/(pref+1)+x*y/((pref+1)*(pref+2)))
A=np.array(rows);eq=np.r_[-t,5];obj=np.r_[q/(1+4*t),-1]
res=linprog(-obj,A_ub=-A,b_ub=np.zeros(len(A)),A_eq=[eq],b_eq=[1],bounds=(0,None),method='highs')
print(res.success,-res.fun if res.success else res.message)
if res.success:
 active=[{'name':n,'weight':float(-v)} for n,v in zip(names,res.ineqlin.marginals) if abs(v)>1e-7];print(active)
 out={'scope':'Floating exploratory root branching necessary-condition optimum; no theorem or counterexample','slope':float(-res.fun),'active_rows':active,'equality_dual':float(res.eqlin.marginals[0]),'positive_primal':[(int(i),list(map(int,bits[i])) if i<N else 'u',float(v)) for i,v in enumerate(res.x) if v>1e-8]}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')

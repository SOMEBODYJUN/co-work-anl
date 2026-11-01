exec(open('test_mixed_singleton_lp3.py').read().split("for target_name")[0])
for target_name in ['OPT6']:
 cols=[];R=[];tar=[]
 for I in range(1,1<<S):
  for E in range(1<<5):
   J,co=rows(I,E)
   if I.bit_count()==1 and I not in (1,1<<6) and E==0: continue
   if any(((E>>t)&1) and not ((I>>route[t])&1) for t in range(5)): continue
   cols.append((I,E,J));R.append(co);tar.append((F(1) if I==(1<<6) else F(int(bool(J))-1,2)))
 import numpy as np
 A_mat=np.array([[float(x) for x in row] for row in R]);b=np.array([float(x) for x in tar]);m=A_mat.shape[1]
 # constraints A lam + eps <= b; maximize eps
 Aub=np.zeros((len(b),m+1));Aub[:,:m]=A_mat;Aub[:,-1]=1
 c=np.zeros(m+1); c[-1]=-1
 res=linprog(c,A_ub=Aub,b_ub=b,bounds=[(0,None)]*m+[(-100,None)],method='highs')
 print(res.status,res.message,'eps',res.x[-1])
 vals=b-A_mat@res.x[:m]
 print('min',vals.min(),'arg',cols[vals.argmin()])
 print('active',[(i,x) for i,x in enumerate(res.x[:m]) if x>1e-7])

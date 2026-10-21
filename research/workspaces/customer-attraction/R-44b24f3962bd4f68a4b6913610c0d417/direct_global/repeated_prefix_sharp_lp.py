exec(open(__file__.replace('repeated_prefix_sharp_lp','repeated_prefix_lp')).read().split('for m in range(2,21)')[0].split('def calc(m):')[0])
for m in range(3,21):
 rows=[];obj=[];cells=[]
 for a,b,d,ell in product(range(2),range(2),range(m+1),range(m+1)):
  p=(m-2)*a; den=(p+1)*(p+2)
  for h in range(max(0,d+ell-m),min(d,ell)+1):
   uA=F(a,m-1+b) if a else F(0);uB=F(b,1+(m-1)*a) if b else F(0)
   rows.append([m*uA-F(d,p+1)+F(h,den),m*uB-F(d,p+a+1),m*uB-F(ell,p+a+1),F(d*ell-m*h,den),m*uA-F(ell,p+2),uA-F(b,p+2),m*uB-a,-int(a+b>0)])
   obj.append(-int(d>0));cells.append((a,b,d,ell,h))
 arr=np.array(rows,dtype=float)
 res=linprog([0]*7+[1],A_ub=arr,b_ub=np.array(obj,dtype=float),bounds=(0,None),method='highs')
 print(m,res.fun,res.x.tolist() if res.success else res.message)

from fractions import Fraction as F
from scipy.optimize import linprog
import itertools

def build(pmin=0):
 names=['G']+[f'safe_{i}_{j}' for i in range(5) for j in range(6)]+[f'safe_{i}_opt' for i in range(5)]+[f'last_{j}' for j in range(6)]+['last_opt']
 rows=[]; rhs=[]; metas=[]
 for bits in itertools.product([0,1],repeat=6):
  *es,a,b=bits;p=sum(es); c=sum(bits);w=int(c>0)
  if a and p<pmin:continue
  u=[F(e,c) if c else F(0) for e in bits]; alpha,beta=u[-2:]
  for d,l in itertools.product(range(7),repeat=2):
   G=6*alpha+beta/2-F(d,p+1)-F(l,12*(p+a+1))+F(d*l,6*(p+1)*(p+2))
   row=[G]
   for i in range(5):
    den=sum(bits[:i])+6-i
    for j in range(6):row.append(u[i]-F(bits[j],den))
   for i in range(5):row.append(6*u[i]-F(d,sum(bits[:i])+6-i))
   for j in range(6):row.append(beta-F(bits[j],sum(bits[:5])+1))
   row.append(6*beta-F(d,sum(bits[:5])+1))
   rows.append(list(map(float,row)));rhs.append(2*w-int(d>0));metas.append((bits,d,l,row))
 return names,rows,rhs,metas
if __name__=='__main__':
 for pmin in [0,1,2]:
  names,rows,rhs,metas=build(pmin)
  r=linprog([0]*len(names),A_ub=rows,b_ub=rhs,bounds=[(0,None)]*len(names),method='highs')
  print('pmin',pmin,r.success)
  if r.success:
   vals=[F(float(z)).limit_denominator(100000) for z in r.x]; print([(n,str(x)) for n,x in zip(names,vals) if x]);print('residual',min(F(v)-sum(x*y for x,y in zip(vals,m[-1])) for v,m in zip(rhs,metas)))

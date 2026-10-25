"""Joint last-reply identity attack on a frozen indexed point.

No outcome is called SPE merely from this LP. The 5 T-membership marginals
are coupled on each old atom, and every selected reply is an actual last BR
against the fixed ten topics and all five T's. Enumeration uses all set
partitions of the five problematic deviation branches, up to T relabeling.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools, json
import numpy as np
from scipy.optimize import linprog
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
HERE=Path(__file__).resolve().parent

def partitions(n):
 def rec(prefix):
  if len(prefix)==n:
   yield tuple(prefix);return
  for x in range(max(prefix,default=-1)+2):
   yield from rec(prefix+[x])
 yield from rec([])

def run():
 data=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
 atoms=data['atoms'];N=len(atoms);den=int(data['denominator']);r=[F(a['mass_numerator'],den) for a in atoms]
 bits=[[int(v) for v in a['bits']] for a in atoms];d=[sum(a['AB_hist'][4:]) for a in atoms]
 onload=[sum(b[:5]) for b in bits]
 u=[sum(rr*F(b[j],ll) for rr,b,ll in zip(r,bits,onload) if b[j]) for j in range(5)]
 bad=(4,6,7,8,9);variables=5*N+1;rows=[];rhs=[];names=[]
 def row():return [F(0)]*variables
 def add(a,b,name):rows.append(a);rhs.append(b);names.append(name)
 # Universal lower bounds on a T deviation at each of the five on-path nodes.
 for j in range(5):
  for i in range(5):
   z=row()
   for k,(rr,b) in enumerate(zip(r,bits)):z[5*k+j]=rr/F(sum(b[:i])+5-i)
   add(z,u[i],f'path_floor_{i}_T{j}')
 eq=[];beq=[]
 for k,dd in enumerate(d):
  z=row()
  for j in range(5):z[5*k+j]=F(1)
  eq.append(z);beq.append(F(dd))
 base_rows=len(rows)
 branch_data=[]
 for dev in bad:
  load=[sum(b[i] for i in (0,1,2,dev)) for b in bits]
  last=[sum(rr*F(b[j],ll+1) for rr,b,ll in zip(r,bits,load)) for j in range(10)]
  fixedmax=max(last)
  g=[rr/F(ll+1) for rr,ll in zip(r,load)]
  base=sum(rr*F(b[dev],ll) for rr,b,ll in zip(r,bits,load) if b[dev])
  loss=[-rr*F(b[dev],ll*(ll+1)) if b[dev] else F(0) for rr,b,ll in zip(r,bits,load)]
  branch_data.append((g,fixedmax,base,loss))
 results=[];best=None
 for partition in partitions(len(bad)):
  rows=rows[:base_rows];rhs=rhs[:base_rows];names=names[:base_rows]
  for dev,j,(g,fixedmax,base,loss) in zip(bad,partition,branch_data):
   z=row()
   for k,v in enumerate(g):z[5*k+j]=-v
   add(z,-fixedmax,f'last_BR_fixed_{dev}_T{j}')
   for ell in range(5):
    if ell==j:continue
    z=row()
    for k,v in enumerate(g):z[5*k+ell]=v;z[5*k+j]=-v
    add(z,F(0),f'last_BR_T{ell}_{dev}_T{j}')
   z=row()
   for k,v in enumerate(loss):z[5*k+j]=v
   z[-1]=F(-1)
   add(z,u[3]-base,f'penultimate_IC_{dev}_T{j}')
  c=np.zeros(variables);c[-1]=1
  A=np.array(rows,dtype=float);b=np.array(rhs,dtype=float);E=np.array(eq,dtype=float);f=np.array(beq,dtype=float)
  result=linprog(c,A_ub=A,b_ub=b,A_eq=E,b_eq=f,bounds=[(0,1)]*(variables-1)+[(-2,2)],method='highs')
  entry={'partition':partition,'status':result.message}
  if result.success:
   entry['minimum_common_IC_violation']=float(result.fun)
   if best is None or result.fun<best[0]:best=(result.fun,partition,result,rows[:],rhs[:],names[:],eq,beq)
  results.append(entry)
 if best:
  value,partition,result,rows,rhs,names,eq,beq=best
  print('best',value,partition,flush=True)
  (HERE/'best_alignment_proposal.json').write_text(json.dumps({'partition':partition,'delta':float(value),'x':result.x.tolist(),'dual_ub':result.ineqlin.marginals.tolist(),'dual_eq':result.eqlin.marginals.tolist(),'dual_lower':result.lower.marginals.tolist(),'dual_upper':result.upper.marginals.tolist()},indent=2)+'\n')
 report={'scope':'Exact 64 old atoms and masses, five T marginals with fixed per-atom optimum multiplicity, on-path guaranteed floors, genuine one-player BRs after five fixed deviations at ABC; fractional proposals only until exact rational verification.','partitions':len(results),'branches':bad,'minimum_proposal':None if best is None else best[0],'results':results}
 (HERE/'joint_alignment_proposal.json').write_text(json.dumps(report,indent=2)+'\n')
 return best
if __name__=='__main__':run()

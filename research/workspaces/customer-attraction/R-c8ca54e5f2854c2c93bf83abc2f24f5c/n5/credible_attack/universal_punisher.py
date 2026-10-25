from max_topic_security import *

def extra(last):
 atoms,r,bits,u,G,rows,rhs,names,own=build(last)
 idx=names.index('T0_has_largest_residual');rows.pop(idx);rhs.pop(idx);names.pop(idx)
 def add(a,b,name):rows.append(a);rhs.append(b);names.append(name)
 add(own,u[3],'T0_penultimate_IC')
 for dev in (4,6,7,8,9):
  load=[sum(b[j] for j in (0,1,2,dev)) for b in bits]
  g=[rr/F(ll+1) for rr,ll in zip(r,load)]
  fixedmax=max(sum(rr*F(b[j],ll+1) for rr,b,ll in zip(r,bits,load)) for j in range(10))
  add([-v for v in g],-fixedmax,f'fixeddev_{dev}_replyT0_BR_fixed')
  add([-F(5,4)*v for v in g],-sum(g)/4,f'fixeddev_{dev}_replyT0_BR_other_T')
  base=sum(rr*F(b[dev],ll) for rr,b,ll in zip(r,bits,load) if b[dev])
  loss=[-rr*F(b[dev],ll*(ll+1)) if b[dev] else F(0) for rr,b,ll in zip(r,bits,load)]
  add(loss,u[3]-base,f'fixeddev_{dev}_penultimate_IC')
 return atoms,r,bits,u,G,rows,rhs,names,own

def main():
 report=[]
 for last in range(11):
  atoms,r,bits,u,G,rows,rhs,names,own=extra(last)
  # Add a common nonnegative violation only to the 6 penultimate IC rows;
  # all BR and path-floor constraints remain hard.
  viol=[True for name in names]
  AA=np.array([rr+[F(-1) if v else F(0)] for rr,v in zip(rows,viol)],dtype=float)
  res=linprog([0]*len(atoms)+[1],A_ub=AA,b_ub=np.array(rhs,dtype=float),bounds=[(0,1)]*len(atoms)+[(0,None)],method='highs')
  row={'last_reply':last,'status':res.message}
  if res.success:row.update({'minimum_common_violation':float(res.fun),'x':res.x.tolist(),'dual':res.ineqlin.marginals.tolist(),'lower':res.lower.marginals.tolist(),'upper':res.upper.marginals.tolist(),'names':names})
  print({k:v for k,v in row.items() if k not in ('x','dual','lower','upper','names')},flush=True);report.append(row)
 (HERE/'universal_punisher_proposal.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()

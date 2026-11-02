"""Independent Fraction check of the 113/21 true-penultimate strengthening."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def share(v,c):return F(v,c) if v else F(0)
def rho(t,q,a,b,c):
 load=t+a+b+c
 r=share(t,load);v4=share(b,load);v5=share(c,load)
 return -F(113,21)*t-F(q,1+4*t)+F(311,21)*r+F(a,2)+F(31,42)*b+F(37,42)*c-F(5,21)*(v4-F(c,t+a+2))-v5+F(q,t+a+b+1)

def main():
 vals=[]
 for t,q,b2,b3,b4,b5 in product((0,1),repeat=6):
  rr=rho(t,q,b2+b3,b4,b5)
  assert rr>=0,(t,q,b2,b3,b4,b5,rr)
  vals.append({'bits':[t,q,b2,b3,b4,b5],'rho':str(rr)})
 table=[]
 for t in (0,1):
  for a in range(3):
   # minimal q is 1 when t=0, 0 when t=1; other q only raises rho.
   q=1-t;scaled=[1260*rho(t,q,a,b,c) for b,c in product((0,1),repeat=2)]
   assert all(x.denominator==1 for x in scaled)
   table.append({'T':t,'B2_plus_B3':a,'worst_Q':q,'1260rho_B4B5_00_01_10_11':[int(v) for v in scaled]})
 out={'claim':'For five players, f_(4T)(Q)<=u+(113/21)(5u-|T|).','scope':'Exact 64-membership coefficient proof audit, requiring root IC, all catalog root-size caps, genuine penultimate worst-denominator comparison with B5, and final BR with Q.','dual':{'root_IC':'311/21','K_B2':'1/2','K_B3':'1/2','K_B4':'31/42','K_B5':'37/42','penultimate_compare_B5':'5/21','last_compare_Q':'1'},'minimum_rho':str(min(F(v['rho']) for v in vals)),'compressed_full_nonnegative_table':table,'all_64_residuals':vals}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='all_64_residuals'},indent=2))
if __name__=='__main__':main()

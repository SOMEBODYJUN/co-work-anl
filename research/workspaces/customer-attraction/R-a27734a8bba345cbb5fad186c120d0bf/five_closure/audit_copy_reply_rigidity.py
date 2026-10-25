"""Exact verification of genuine-copy-reply root rigidity, slope 16/3.
No optimizer is imported. All 128 memberships are evaluated directly.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,math

def share(x,den):return F(x,den) if x else F(0)
def rho(t,q,a,b,c,d):
 p=t+a;ell=p+b+c;copyell=p+c+d
 r=share(t,ell);v4=share(b,ell);v5=share(c,ell)
 L=v4-share(c,copyell)
 ZQ=v5-F(q,p+b+1)
 ZC=v5-F(d,p+b+1)
 CQ=share(d,copyell)-F(q,p+c+1)
 return -F(16,3)*t-F(q,1+4*t)+F(44,3)*r+F(a,2)+F(11,15)*b+F(13,15)*c-F(4,15)*L-F(14,15)*ZQ-F(2,15)*ZC-F(1,15)*CQ

def main():
 vals=[]
 for t,q,b2,b3,b4,b5,C in product((0,1),repeat=7):
  rr=rho(t,q,b2+b3,b4,b5,C)
  assert rr>=0,(t,q,b2,b3,b4,b5,C,rr)
  vals.append({'bits':[t,q,b2,b3,b4,b5,C],'rho':str(rr)})
 D=1
 for v in vals:D=math.lcm(D,F(v['rho']).denominator)
 table=[]
 for t,a,d in product((0,1),range(3),(0,1)):
  scaled=[D*rho(t,1-t,a,b,c,d) for b,c in product((0,1),repeat=2)]
  assert all(v.denominator==1 for v in scaled)
  table.append({'T':t,'B2_plus_B3':a,'copy_reply_C':d,'worst_Q':1-t,'scaled_rho_B4B5_00_01_10_11':[int(v) for v in scaled]})
 out={'claim':'f_(4T)(Q)<=(44/3)u+(13/5)M-(16/3)|T|, with common catalog maximum M.','scope':'Exact 128-type identity from root IC, common topic size caps, real penultimate deviation to original B5 with actual reply C, original last BR versus Q,C, and copied-history last BR versus Q.','dual':{'root_IC':'44/3','K_B2':'1/2','K_B3':'1/2','K_B4':'11/15','K_B5':'13/15','real_penultimate_copy_B5':'4/15','original_last_compare_Q':'14/15','original_last_compare_C':'2/15','copy_history_last_compare_Q':'1/15'},'minimum_rho':str(min(F(v['rho']) for v in vals)),'table_scale':D,'compressed_complete_nonnegative_table':table,'all_128_residuals':vals}
 Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='all_128_residuals'},indent=2))
if __name__=='__main__':main()

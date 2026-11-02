"""Fraction scalar checks only; the accompanying analytic proof carries all m.

No SPE tree is rebuilt: the universal exclusion uses one genuine final-node BR.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def check(m):
 k=m-1;C=k*(k+1);h=k+2;P=k+3
 v=F(C,k+1)+P;delta=F(m,4*(m+1))
 assert v==2*m+1
 assert F(2*C,k+1)<=v
 alpha=F(C,2*k*(k+1))-F(P,4*h)
 assert alpha==delta>0
 for z in range(k+1):
  assert F(1,k-z+1)-F(1,k+1)>=F(z,k*(k+1))
 for r in range(k+1):assert F(r,r+1)<=F(r,2)
 # q0=B^k; q1=B^(k-1) plus a single X leaf.
 f0=F(C,k+1)+P
 f1=F(C,2)*(F(1,k+1)+F(1,k))+P-F(P,4*h)
 assert f0==v and f1-f0==delta
 # Genuine terminal deviation after a root B, respectively a root X leaf.
 stay_Broot=F(2*C,k+1);dev_Broot=F(C,k+1)+P
 stay_leafroot=F(C,k+1)+F(C,k);dev_leafroot=F(C,k)+P
 assert dev_Broot-stay_Broot==dev_leafroot-stay_leafroot==3
 # A fresh, never-copied leaf has this uniform lower bound in any m-player prefix.
 fresh_lower=P+F(C,m)
 assert fresh_lower==v
 O=m*P+2*C
 assert O==3*m*m
 ratio=F(O,m*v)
 assert ratio==F(3*m,2*m+1)<F(3,2)
 return {'m':m,'C':C,'h':h,'P':P,'v':str(v),'strict_tail_slack':str(delta),'nonworst_one_leaf_slack':str(f1-f0),'both_last_BR_improvements':'3','fresh_floor':str(fresh_lower),'OPT_m':O,'ratio_upper':str(ratio)}

if __name__=='__main__':
 report={'scope':'scalar Fraction regression; no SPE-tree sweep','cases':[check(m) for m in range(2,13)]}
 Path(__file__).with_name('strict_tail_scalar_audit.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'cases':len(report['cases']),'m_range':[2,12],'status':'pass'},indent=2))

"""New exact arithmetic for the 7943B independent review's distinct certificate.
No old m20 rbar=25/27 proof, old SPE tree, old53/100 check or original CLI rerun.
The all-history SPE and all-m quantifiers are proved in the accompanying text.
"""
from fractions import Fraction as F
from pathlib import Path
import json

def g(n,p):return sum(((1-p)**i for i in range(n)),F())/n

def main():
 out=Path(__file__).with_name('new-independent-coverage-certificate.json')
 assert not out.exists(),'successful new check must not be rerun'
 m,J=20,100;lo=F(92579,100000);hi=F(4629,5000)
 def D(b):return 2*(m-1)*g(m,b)-2*g(m,1-b)-g(m,(1-b)/J)
 dlo,dhi=D(lo),D(hi)
 assert dlo>F(1,20000) and dhi<-F(1,25000)
 LB=38*(1-(1-lo)**20)+2*(1-hi**20)+100*(1-(1-(1-hi)/100)**20)
 assert LB>F(8209,200)
 margin=F(39,40)*F(8209,200)-40
 assert margin==F(151,8000)>0
 # Distinct coverage proof constants; no Taylor common constant or old scalar cut rerun.
 universal_excess=F(1191,800)-F(9,20)-F(1,100)
 assert universal_excess==F(823,800)>F(82,81)
 data={'status':'passed','new_math_entries':{'attempts':1,'successes':1,'failures':0},'original_CLI_entries':0,'solver_calls':0,'float_operations':0,'m20_J100':{'root_lower':str(lo),'root_upper':str(hi),'D_lower':str(dlo),'D_upper':str(dhi),'D_lower_minus_1_over_20000':str(dlo-F(1,20000)),'minus_1_over_25000_minus_D_upper':str(-F(1,25000)-dhi),'coverage_lower_bound':str(LB),'coverage_lower_minus_8209_over_200':str(LB-F(8209,200)),'strict_weak_margin_lower':str(margin)},'universal_distinct_coverage_constants':{'private_lower':str(F(1191,800)),'core_upper':str(F(9,20)),'B_upper':str(F(1,100)),'excess_lower':str(universal_excess),'excess_lower_minus_82_over_81':str(universal_excess-F(82,81))},'old_successes_rerun':[],'scope':'Only the 7943B source distinct rational root bracket and coverage arithmetic. No solver/root finding/full SPE enumeration, no old m20 short certificate or m53/100 rerun. General m>=41 and all ordered histories depend on analytic proof.'}
 out.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':'passed','root_bracket':[str(lo),str(hi)],'weak_margin_lower':str(margin),'all_m_coverage_excess':str(universal_excess),'old_reruns':0}))

if __name__=='__main__':main()

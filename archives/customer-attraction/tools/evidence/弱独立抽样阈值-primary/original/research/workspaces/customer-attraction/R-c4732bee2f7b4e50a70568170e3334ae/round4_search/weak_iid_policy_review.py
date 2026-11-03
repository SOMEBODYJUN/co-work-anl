"""Independent exact full ordered-history audit of weak-iid policy family.
Finite certificate checks supplement a separate all-history analytic proof.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,sys
from math import factorial
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction import CustomerType,Instance,StrategyCertificate,verify_certificate
from customer_attraction_strategy_lp import serializable

def instance(m,K):
 return Instance(tuple(['C','B']+[f'P{j}' for j in range(1,K+1)]),tuple([CustomerType(frozenset([0]+list(range(2,K+2))),2),CustomerType(frozenset([1]),2*(m-1))]+[CustomerType(frozenset([j]),1) for j in range(2,K+2)]),m)

def policy(h,m,K):
 if not h:return 0
 if len(h)<m-1:return 1
 non=[a for a in h if a!=1]
 if not non:return 2
 if len(non)==1 and non[0]!=0:return 2 if non[0]!=2 else 3
 return 1

def g(m,z):return (1-(1-z)**m)/(m*z) if z else F(1)

def main():
 rows=[]
 for m,K in [(2,2),(3,2),(3,3),(4,4),(5,5),(6,4)]:
  I=instance(m,K);p=K+2
  acts={h:policy(h,m,K) for d in range(m) for h in product(range(p),repeat=d)}
  cert=StrategyCertificate(acts,(1,m-1)+(0,)*K)
  check=verify_certificate(I,cert);check.assert_valid()
  # Also directly verify every decision-node / deviation payoff, without the
  # canonical certificate verifier or set-valued equilibrium solver.
  def terminal(h):
   while len(h)<m:h=h+(acts[h],)
   return I.counts(h,terminal=True)
  comparisons=0
  for h,a in acts.items():
   ua=I.topic_payoffs(terminal(h))[a]
   for b in range(p):
    if b==a:continue
    assert ua>=I.topic_payoffs(terminal(h+(b,)))[b]
    comparisons+=1
  rows.append({'m':m,'K':K,'ordered_decision_histories':len(acts),'direct_comparisons':comparisons,'W':I.welfare(cert.terminal_counts),'OPT':I.optimal_welfare(),'all_histories_verified':True})
 m=K=100;t=F(1969,2000);c=F(2011,1000)
 alphaB=2*(m-1)*g(m,t);alphaP=2*g(m,1-t)+g(m,(1-t)/K)
 assert alphaB>c and alphaP>c and c>F(400,199)
 exp_lower=sum((F(3,2)**j/F(factorial(j)) for j in range(6)),F(0))
 assert exp_lower==F(5711,1280) and exp_lower>F(40,9)
 for mm in range(3,101):
  cc=F(4*mm,2*mm-1)
  Bbound=F(2*(mm-1),mm)*(1+F(3,2*mm)+F(9,4*mm*mm))
  Pbound=F(61,30)-F(3,4*mm)
  assert Bbound-cc==F(4*mm*mm-21*mm+9,2*mm**3*(2*mm-1))
  assert Pbound-cc==F(4*mm*mm-212*mm+45,60*mm*(2*mm-1))
  if mm>=5:assert Bbound>cc
  if mm>=53:assert Pbound>cc
 report={'scope':'independent exact checks; analytic review covers all m>=2,K>=2; no half-coverage counterexample','infinite_certificate':{'parameter_range':'m=K>=53','exp_partial_sum_exact':str(exp_lower),'exp_partial_sum_exceeds_40_over_9':True,'B_gap_numerator_at_m5':4,'petal_gap_numerator_at_m53':45,'gap_formulas_checked_exactly_m3_through100':True},'finite_full_history_checks':rows,'iid_test':{'m':m,'K':K,'t':str(t),'alpha_B_float':float(alphaB),'alpha_P_float':float(alphaP),'threshold':str(c),'alpha_B_exceeds_threshold_exact':alphaB>c,'alpha_P_exceeds_threshold_exact':alphaP>c,'threshold_exceeds_400_over_199_exact':c>F(400,199),'strict_weak_bridge_gap_lower_bound':str(F(199,2)*c-200)},'m1_excluded':'root C payoff2 but petal deviation yields3; B has zero clients and policy is not an SPE','K1_excluded':'requires another distinct petal after a lone petal prefix'}
 Path(__file__).with_suffix('.json').write_text(json.dumps(serializable(report),indent=2)+'\n');print(json.dumps(serializable(report),indent=2))
if __name__=='__main__':main()

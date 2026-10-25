"""Exact pointwise audit of the unconditional reply-of-reply row.
This audits the coefficient identity, not the existence of any SPE.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def u(v,load):return F(v,load) if v else F(0)
def P(bg,a,b):return sum(F(1,j) for j in range(bg+1,bg+a+b+1))
def audit(k):
 checked=0;minH=None
 for bg in range(4):
  for a,b,c,*comparison in product((0,1),repeat=3+k):
   O=bool(a or any(comparison)) if k==4 else bool(any(comparison))
   RA=F(a,bg+1);RB=F(b,bg+1);RC=F(c,bg+1)
   ua=u(a,bg+a+b);ub=u(b,bg+a+b);qb=u(b,bg+b+c)
   IA=-ua;IB=-qb;L=P(bg,b,c)-P(bg,a,b)
   total=sum(u(t,bg+a+t) for t in comparison)
   K=k*ub-total
   H=total-F(int(O and not a),bg+1)
   assert H>=0
   desired= -F(int(O or a),bg+1)+RB+(k-1)*RC-(k-1)*RA
   exact=IA+(k-1)*IB+(k-1)*L+K+H
   assert desired==exact,(k,bg,a,b,c,comparison,desired,exact)
   checked+=1;minH=H if minH is None else min(H,minH)
 return {'comparator_rows':k,'customer_patterns_checked':checked,'minimum_coverage_gap':str(minH),'coefficient_identity_exact':True}

def main():
 report={'scope':'pointwise coefficient audit of FF (four other comparators) and FF5 (five arbitrary comparators), background load 0..3; algebraic proofs in feedback_cycle.md cover all finite instances','FF':audit(4),'FF5':audit(5)}
 Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()

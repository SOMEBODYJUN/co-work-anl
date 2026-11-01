"""Exact finite algebra regression; the four-case derivation in the note is the proof."""
from fractions import Fraction as F
from itertools import product

def u(h,r,s,xa,xb,whose):
 return F(xa if whose=='a' else xb,h+r*xa+s*xb) if (xa if whose=='a' else xb) else F(0)
checks=0
for h,r,s,xa,xb in product(range(16),range(1,12),range(1,12),range(2),range(2)):
 if r<s:continue
 lhs=r*s*u(h,r,s,xa,xb,'a')+r*(r-s)*u(h,s,r,xa,xb,'b')
 rhs=s*s*u(h,s,r,xa,xb,'a')+(r-s)*F(xb,h+1)
 if xa and not xb:err=F((r-s)*h*s,(h+r)*(h+s))
 elif xb and not xa:err=F((r-s)*h*(r-1),(h+r)*(h+1))
 elif xa and xb:err=F((r-s)*h*(r+s-1),(h+r+s)*(h+1))
 else:err=F(0)
 assert lhs==rhs+err and err>=0
 if r==2 and s==1:
  assert err==F(h,h+1)-F(h,h+1+xa+xb)
 checks+=1
for h,r,s,xa,xc,xb in product(range(16),range(1,10),range(1,10),range(2),range(2),range(2)):
 if r<s:continue
 def error(x):
  if x and not xb:return F((r-s)*h*s,(h+r)*(h+s))
  if xb and not x:return F((r-s)*h*(r-1),(h+r)*(h+1))
  if x and xb:return F((r-s)*h*(r+s-1),(h+r+s)*(h+1))
  return F(0)
 filtered=F(s*(r-s)*h*(xa-xc),(h+r)*(h+s+r*xb))
 assert error(xa)-error(xc)==filtered
 checks+=1
for h,xb in product(range(1000),range(2)):
 charge=F(h,(h+2)*(h+1+2*xb))
 assert charge<=F(1,6)
 checks+=1
print({'status':'pass','exact_finite_algebra_checks':checks,'scope':'Regression only; general identities proved by four membership cases in note'})

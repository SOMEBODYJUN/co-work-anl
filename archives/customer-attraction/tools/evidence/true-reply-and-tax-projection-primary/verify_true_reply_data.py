#!/usr/bin/env python3
"""Independent exact data/certificate check for DG mathematical source.
No original audit_reply_cap import/run and no optimizer or projection LP.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json,hashlib
E=Path(__file__).resolve().parent;C=E/'comparison'
def load(p):return json.loads((C/p).read_text())
def audit(name):
 inp=load('examples/customer_attraction/'+name+'.json');cert=load('evidence/certificates/customer_attraction/'+name+'.json');clients=[frozenset(r['topics']) for r in inp['customers'] for _ in range(r['multiplicity'])];sigma={tuple(r['history']):r['action'] for r in cert['strategy']['actions']};k=len(inp['topics']);m=inp['players'];assert k==6 and m==3
 expected={h for n in range(m) for h in product(range(k),repeat=n)};assert set(sigma)==expected
 def terminal(h):
  while len(h)<m:h=h+(sigma[h],)
  return h
 def pay(z,i):return sum((F(1,sum(a in x for a in z)) for x in clients if z[i] in x),F(0))
 comparisons=nonself=0;slacks=[]
 for h in sorted(expected,key=lambda h:(len(h),h)):
  z=terminal(h);i=len(h)
  for a in range(k):
   slack=pay(z,i)-pay(terminal(h+(a,)),i);assert slack>=0;slacks.append(slack);comparisons+=1;nonself+=a!=sigma[h]
 caps=[];b1=[];b2=[]
 for before in range(k):
  h=(before,);z=terminal(h);A,B=z[1:];u=pay(z,1);v=pay(z,2)
  def f(T):return sum((F(1,1+(before in x)) for x in clients if T in x),F(0))
  def g(T,S):return sum((F(1,(1+(before in x))*(2+(before in x))) for x in clients if T in x and S in x),F(0))
  cap=max(map(f,range(k)))
  for T,S in combinations_with_replacement(range(k),2):
   slack=u+cap-f(T)-f(S)+g(T,S);assert slack>=0;caps.append(slack)
  for T in range(k):
   slack=2*u+v+g(A,T)-2*f(T);assert slack>=0;b2.append(slack)
   for S in range(k):
    slack=3*u+2*v+2*g(A,T)-3*f(T)-f(S)+g(T,S);assert slack>=0;b1.append(slack)
 H=[F(0)]
 for n in range(1,4):H.append(H[-1]+F(1,n))
 potential=[];maxima=[]
 for n in range(1,4):
  vals=[dict(topics=list(q),value=sum((H[sum(a in x for a in q)] for x in clients),F(0))) for q in combinations_with_replacement(range(k),n)];best=max(r['value'] for r in vals);maxima.append(best);potential.append(dict(slots=n,all_multisets=[dict(topics=r['topics'],value=str(r['value'])) for r in vals],maximum=str(best)))
 actual=terminal(());W=sum(pay(actual,i) for i in range(m));opt=max(sum(any(a in x for a in q) for x in clients) for q in combinations_with_replacement(range(k),m))
 assert comparisons==258 and nonself==215 and len(caps)==126 and len(b1)==216 and len(b2)==36
 if name=='individual_security_failure':assert len(clients)==34 and W==32 and opt==34 and maxima[1:]==[F(39),F(149,3)] and pay(actual,0)==F(29,3)
 else:assert len(clients)==36 and W==34 and opt==36 and maxima[1:]==[F(75,2),F(99,2)] and pay(actual,0)==10
 return dict(name=name,customers=len(clients),topics=k,players=m,complete_policy=[dict(history=list(h),action=sigma[h]) for h in sorted(expected,key=lambda h:(len(h),h))],histories=len(expected),comparisons=comparisons,nonself=nonself,IC_minimum=str(min(slacks)),actual=list(actual),payoffs=[str(pay(actual,i)) for i in range(m)],W=str(W),OPT=opt,cap_rows=len(caps),cap_minimum=str(min(caps)),beta1_rows=len(b1),beta1_minimum=str(min(b1)),beta2_rows=len(b2),beta2_minimum=str(min(b2)),potentials=potential,current_increment=str(maxima[2]-maxima[1]),root_minus_current_increment=str(pay(actual,0)-(maxima[2]-maxima[1])),W_minus_m_current_increment=str(W-m*(maxima[2]-maxima[1])))
def atom_checks():
 count=0;betas=[F(0),F(1,2),F(1),F(3,2),F(2),F(7)]
 for b in [0,1,2,10,10**40]:
  w=F(1,b+1);d=F(1,(b+1)*(b+2));assert 0<d<=w/2
  for A,T,S,Q in product(range(2),repeat=4):
   f=lambda X:w*X;g=lambda X,Y:d*X*Y;u=F(1,7);v=F(2,11)
   G1=u-f(T)+g(T,Q);G2=f(Q)-g(T,Q)-f(S)+g(T,S);G3=v-f(Q)+g(A,Q)
   for beta in betas:
    rem=F(max(1,beta),2)*f(Q)+min(1,beta)*g(A,T)-g(A,Q)-beta*g(T,Q);assert rem>=0
    if beta<=1:
     target=(2*beta+1)*u+2*v+2*beta*g(A,T)-(2*beta+1)*f(T)-f(S)+g(T,S);assert target==(2*beta+1)*G1+G2+2*G3+2*rem
    elif beta<=2:
     target=(beta+2)*u+2*v+2*g(A,T)-(beta+2)*f(T)-(2-beta)*(f(S)-g(T,S));assert target==(beta+2)*G1+(2-beta)*G2+2*G3+2*rem
    count+=1
 return dict(backgrounds=[0,1,2,10,str(10**40)],membership_fields=['A','T','S','Q'],beta_values=list(map(str,betas)),atom_cases=count,scope='algebraic identity and nonnegative overlap remainder; arbitrary u,v used only to test cancellation, not claimed SPE atoms')
def main():
 games=[audit(n) for n in ['individual_security_failure','aggregate_theta_failure']];atoms=atom_checks();assert atoms['atom_cases']==480
 # Six-group m4, independently from explicit membership sizes.
 groups=[({0,1},108),({2,3},108),({0,2},24),({1,3},24),({0,1,2},32),({3},4)]
 f=lambda T:sum((F(n,1+2*(0 in B)) for B,n in groups if T in B),F(0));g=lambda T,S:sum((F(n,(1+2*(0 in B))*(2+2*(0 in B))) for B,n in groups if T in B and S in B),F(0));u=F(68);v=F(124);Fmax=max(map(f,range(4)))
 assert Fmax==f(3) and f(3)==136
 gap=f(2)-g(2,3)-u;beta1=3*u+2*v+2*g(1,3)-3*f(3)-f(2)+g(3,2);beta2=2*u+v+g(1,3)-2*f(3);assert gap==F(14,3) and beta1==-F(14,3) and beta2==0
 data=dict(status='PASS',scope=__doc__,games=games,atom_checks=atoms,six_group_m4=dict(topics=['C','P','L','D'],F=str(Fmax),cap_violation=str(gap),beta1_slack=str(beta1),beta2_slack=str(beta2)),original_program_runs=0,projection_LP_runs=0,helper_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 Path('result.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');print('PASS: two full SPE fixtures each 258 IC, 126 RC, 216 beta1, 36 beta2; 480 atoms; harmonic maxima; m4 projection exclusion. No original audit/LP run.')
if __name__=='__main__':main()

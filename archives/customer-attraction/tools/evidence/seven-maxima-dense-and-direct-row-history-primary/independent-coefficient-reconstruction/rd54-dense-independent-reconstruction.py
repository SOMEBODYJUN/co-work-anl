"""Informed exact algebra replay from fully read MD rows, never import source checker.
Only finite literal coefficient columns; no LP/SPE enumeration/game construction.
"""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib
B=[F(1,21),F(2,37),F(1,16),F(2,27),F(1,11),F(7,72)]
LM=[F(207,355),F(417,710),F(253,426),F(133,213),F(0),F(0)]
def bc(x):return x.bit_count()
def residual(I,E):
 J=E|((1<<5) if I&1 else 0); q=bc(J);u=[F(bool(J&(1<<t)),q) if q else F(0) for t in range(6)]
 M=[u[t]-B[t] for t in range(6)]
 L=[u[5]-F(bool(I&(1<<j)),bc(J&31)+1) for j in range(7)]
 p=bc(J&15);d=bool(J&16)
 def tax(j,k):
  m=int(bool(I&(1<<j)))+int(bool(I&(1<<k)))
  return u[4]+u[5]+F(d,(p+1)*(p+2))-(F(m,p+m) if m else 0)
 rows=sum(LM[t]*M[t] for t in range(6))+F(8,71)*sum(L[1:])+F(7,71)*sum(tax(0,j) for j in range(1,7))
 return F(bool(J))-F(1,2)-rows,J

def scan(incs):
 vals=[(residual(I,E)[0],I,E,residual(I,E)[1])for I in incs for E in range(32)]
 m=min(x[0]for x in vals)
 return dict(columns=len(vals),minimum=str(m),minimizers=[dict(I=I,E=E,J=J)for r,I,E,J in vals if r==m],negative_columns=sum(r<0 for r,I,E,J in vals))
dense=scan([I for I in range(1,128)if bc(I)>=2]);other=scan([64]);final=scan([1]);assert dense['columns']==3840 and dense['minimum']=='15591089/238321440'and dense['negative_columns']==0;assert other['minimum']=='-34758511/238321440';assert str(residual(1,0)[0])=='-7905391/238321440'
out=dict(kind='informed-independent-exact-literal-column-algebra-only',primary_MD_id='dc50804a7271758b53f7',source_checker_imports=0,source_checker_runs=0,LP_runs=0,SPE_strategy_audits=0,new_game_instances=0,dense=dense,private_at_index6=other,private_at_final_index0=final,point_final_private_I1_E0_J32_residual=str(residual(1,0)[0]),early_mixed_private_envelope='1/12 at all six positions; first four B_t<=1/12',sum_early_lambda_B=str(sum(LM[t]*B[t]for t in range(4))),scope='same displayed weaker first-four M/L/T rows; singleton residuals refute literal W-U/2 certificate extension, not extension truth or half')
p=Path(__file__);out['implementation_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();print(json.dumps(out,ensure_ascii=False,indent=2))

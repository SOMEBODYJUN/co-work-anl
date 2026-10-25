from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
T3=list(product((0,1),repeat=3));T4=list(product((0,1),repeat=4))
def opt_rows(a):
 b=list(map(int,a['bits']));d=sum(a['AB_hist'][4:]);r={}
 # Replace one matched optimal theme T_i by Q_i, or a fixed theme Q.
 for i,q in enumerate(b):r[f'fixed:{i}']=int(d==1)*(1-q)-5*int(d==0)*q
 for name,h,ty in [('AB',a['AB_hist'],T3),('AE',a['AE_hist'],T3),('S',a['second_hist'],T4)]:
  for j in range(1,len(ty[0])):
   r[f'{name}:matched:{j}']=sum(n*(int(d==1)*t[0]*(1-t[j])-int(d==0)*t[j]) for n,t in zip(h,ty))
   # independently remove any T_i and insert any Q_j.
   q=sum(n*t[j] for n,t in zip(h,ty));r[f'{name}:all:{j}']=int(d==1)*(5-q)-5*int(d==0)*q
 for i,(ell,hh) in enumerate(a['menus_lh']):
  r[f'L{i}:matched']=int(d==1)*(1-hh)-int(d==0)*ell
  r[f'L{i}:all']=int(d==1)*(5-ell)-5*int(d==0)*ell
 return r
if __name__=='__main__':
 outs=[]
 for p in [ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json',ROOT/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible/enhanced_2396_exact_obstruction.json']:
  c=json.loads(p.read_text());aa=c['primal']['atoms'] if 'primal' in c else c['atom_masses'];ss={}
  for a in aa:
   m=F(a['mass']) if 'mass' in a else F(a['mass_numerator'],c['primal']['denominator'])
   for n,v in opt_rows(a).items():ss[n]=ss.get(n,F(0))+m*v
  outs.append({'source':str(p.relative_to(ROOT)),'slacks':{n:str(v) for n,v in ss.items()},'violated':{n:str(v) for n,v in ss.items() if v<0}})
 print(json.dumps(outs,indent=2))

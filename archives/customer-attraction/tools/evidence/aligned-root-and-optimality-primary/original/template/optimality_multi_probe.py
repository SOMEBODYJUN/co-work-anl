from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
T3=list(product((0,1),repeat=3));T4=list(product((0,1),repeat=4))
def binom(n,k):return comb(n,k) if 0<=k<=n else 0
def opt_multi(a):
 d=sum(a['AB_hist'][4:]);out={};menus=[]
 for name,h,ty in [('AB',a['AB_hist'],T3),('AE',a['AE_hist'],T3),('S',a['second_hist'],T4)]:
  for j in range(1,len(ty[0])):menus.append((f'{name}:{j}',sum(n*int(t[0]==0 and t[j]==0) for n,t in zip(h,ty)),sum(n*t[0]*t[j] for n,t in zip(h,ty))))
 if 'root_hist' in a:
  ty=list(product((0,1),repeat=5));h=a['root_hist']
  for j in range(1,5):menus.append((f'root:{j}',sum(n*int(t[0]==0 and t[j]==0) for n,t in zip(h,ty)),sum(n*t[0]*t[j] for n,t in zip(h,ty))))
 for i,(ell,hh) in enumerate(a['menus_lh']):menus.append((f'L{i}',5-d-ell+hh,hh))
 for i,q in enumerate(map(int,a['bits'])):menus.append((f'fixed:{i}',(5-d)*(1-q),d*q))
 for name,n00,n11 in menus:
  for k in range(1,6):out[f'{name}:k{k}']=(binom(n00,k-d) if n11==0 else 0)-int(d==0)*binom(5,k)
 return out
if __name__=='__main__':
 outs=[]
 for p in [ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json',ROOT/'research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_credible/enhanced_2396_exact_obstruction.json']:
  c=json.loads(p.read_text());aa=c['primal']['atoms'] if 'primal' in c else c['atom_masses'];ss={}
  for a in aa:
   m=F(a['mass']) if 'mass' in a else F(a['mass_numerator'],c['primal']['denominator'])
   for n,v in opt_multi(a).items():ss[n]=ss.get(n,F(0))+m*v
  outs.append({'source':str(p.relative_to(ROOT)),'slacks':{n:str(v) for n,v in ss.items()},'violated':{n:str(v) for n,v in ss.items() if v<0}})
 out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(outs,indent=2)+'\n')
 for x in outs:print(x['source'],x['violated'])

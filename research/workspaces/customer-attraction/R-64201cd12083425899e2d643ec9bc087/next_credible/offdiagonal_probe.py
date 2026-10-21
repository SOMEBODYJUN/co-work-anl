"""Exact missing distinct-index necessary rows at the 437-row obstruction.
Does not claim a full SPE or a universal welfare bound.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[5]
cert=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
types=list(product((0,1),repeat=3));quads=list(product((0,1),repeat=4));labels='ABCDEUVWXY'
paths={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'}
def q(n,d):return F(n,d) if n else F(0)
def rows(a):
 b=dict(zip(labels,map(int,a['bits'])));out={}
 for f,pn in enumerate(paths):
  p=sum(b[k] for k in paths[pn][:3]);ell,h=a['menus_lh'][f]
  d=sum(n*t for n,(t,x,y) in zip(a['AB_hist'],types))
  own=q(ell,p+1)-q(h,(p+1)*(p+2))-q(d,p+2)
  allr=q(5*ell-5*d,p+1)+q(d*d-5*h,(p+1)*(p+2))
  out[pn+':old-last:off-T']=allr-own
 for tag,key,prefix,ts in [('AB','AB_hist','AB',types),('AE','AE_hist','AE',types),('Sbranch','second_hist','A',quads)]:
  p=sum(b[k] for k in prefix);hist=a[key];m=len(ts[0])-1
  loads=[p+sum(t) for t in ts]
  d=sum(n*t[0] for n,t in zip(hist,ts))
  def sm(fn):return sum((n*fn(t) for n,t in zip(hist,ts)),F())
  for pos in range(1,m+1):
   # pos=1 is earliest follower. The last-node denominator is exact;
   # for other nodes it is the valid worst-follower denominator.
   den=lambda t: p+sum(t[:pos])+m-pos+1
   u=sm(lambda t:q(t[pos],p+sum(t)))
   menu_names=['T','X','Y'] if m==2 else ['T','U','V','W']
   for action in range(m+1):
    count=sum(n*t[action] for n,t in zip(hist,ts))
    off=4*u-count*sm(lambda t:q(1,den(t)))+sm(lambda t:q(t[action],den(t)))
    out[f'{tag}:node-{pos}:off-{menu_names[action]}']=off
 return out
def main():
 slacks={}
 for a in cert['atoms']:
  mass=F(a['mass_numerator'],cert['denominator'])
  for n,v in rows(a).items():slacks[n]=slacks.get(n,F())+mass*v
 report={'scope':'additional universally necessary distinct-index floors or exact last BR; evaluated only at frozen 437-row LP point','row_count':len(slacks),'negative':{k:str(v) for k,v in slacks.items() if v<0},'all':{k:str(v) for k,v in slacks.items()}}
 print(json.dumps(report,indent=2))
 Path(__file__).with_name('offdiagonal_probe.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()

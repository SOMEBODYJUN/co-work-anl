"""Necessary cross-family menu comparisons on the unchanged indexed coordinates."""
from offdiagonal_probe import types,quads,labels,paths,q,cert,F

def rows(a):
 b=dict(zip(labels,map(int,a['bits'])));out={};menus={}
 for i,(ell,h) in enumerate(a['menus_lh']):menus['L'+str(i)]=ell
 for tag,key,ts in [('AB','AB_hist',types),('AE','AE_hist',types),('Sbranch','second_hist',quads)]:
  for pos,mn in enumerate('XY' if tag!='Sbranch' else 'UVW',1):menus[tag+':'+mn]=sum(n*t[pos] for n,t in zip(a[key],ts))
 for tag,key,prefix,ts in [('AB','AB_hist','AB',types),('AE','AE_hist','AE',types),('Sbranch','second_hist','A',quads)]:
  p=sum(b[k] for k in prefix);hist=a[key];m=len(ts[0])-1
  def sm(fn):return sum((n*fn(t) for n,t in zip(hist,ts)),F())
  for pos in range(1,m+1):
   den=lambda t:p+sum(t[:pos])+m-pos+1
   u=sm(lambda t:q(t[pos],p+sum(t)));di=sm(lambda t:q(1,den(t)))
   for mn,count in menus.items():out[f'{tag}:node-{pos}:crossmenu-{mn}']=5*u-count*di
 return out

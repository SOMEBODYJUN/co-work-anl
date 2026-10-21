"""Existing valid last-two tax compared to all retained cross-menu pairs."""
from offdiagonal_probe import types,quads,labels,paths,q,F
from itertools import combinations_with_replacement

def rows(a):
 b=dict(zip(labels,map(int,a['bits'])));out={};menus={l:(1,b[l]) for l in labels}
 menus['T']=(5,sum(n*t[0] for n,t in zip(a['AB_hist'],types)))
 for i,(ell,h) in enumerate(a['menus_lh']):menus['L'+str(i)]=(5,ell)
 for tag,key,ts in [('AB','AB_hist',types),('AE','AE_hist',types),('Sbranch','second_hist',quads)]:
  for pos,mn in enumerate('XY' if tag!='Sbranch' else 'UVW',1):menus[tag+':'+mn]=(5,sum(n*t[pos] for n,t in zip(a[key],ts)))
 groups=[]
 for pn,path in paths.items():
  p=sum(b[k] for k in path[:3]);H=q(b[path[3]]+b[path[4]],sum(b[k] for k in path))+q(b[path[3]],(p+1)*(p+2))
  groups.append((pn,H,q(1,p+1),q(1,p+2)))
 for tag,key,prefix,ts in [('AB','AB_hist','AB',types),('AE','AE_hist','AE',types),('Sbranch','second_hist','A',quads)]:
  p0=sum(b[k] for k in prefix);hist=a[key];m=len(ts[0])-1
  def sm(fn):return sum((n*fn(t) for n,t in zip(hist,ts)),F())
  bg=lambda t:p0+sum(t[:-2]);H=sm(lambda t:q(t[-2]+t[-1],p0+sum(t))+q(t[-2],(bg(t)+1)*(bg(t)+2)))
  groups.append((tag,H,sm(lambda t:q(1,bg(t)+1)),sm(lambda t:q(1,bg(t)+2))))
 for tag,H,D1,D2 in groups:
  for ma,mb in combinations_with_replacement(menus,2):
   s,x=menus[ma];t,y=menus[mb]
   out[f'{tag}:newtax:{ma}|{mb}']=s*t*H-(x*(t-y)+(s-x)*y)*D1-2*x*y*D2
 return out

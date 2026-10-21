"""Aligned and distinct comparison-index tax sums, without new coordinates."""
from offdiagonal_probe import types,quads,labels,paths,q,F
from itertools import combinations_with_replacement

def rows(a):
 b=dict(zip(labels,map(int,a['bits'])));out={};pairs=[]
 T=sum(n*t[0] for n,t in zip(a['AB_hist'],types))
 for i,(ell,h) in enumerate(a['menus_lh']):pairs.append(('T','L'+str(i),T,ell,h))
 for tag,key,ts in [('AB','AB_hist',types),('AE','AE_hist',types),('Sbranch','second_hist',quads)]:
  names=['T']+[tag+':'+v for v in ('XY' if tag!='Sbranch' else 'UVW')]
  for i,j in combinations_with_replacement(range(len(names)),2):
   x=sum(n*t[i] for n,t in zip(a[key],ts));y=sum(n*t[j] for n,t in zip(a[key],ts));dot=sum(n*t[i]*t[j] for n,t in zip(a[key],ts));pairs.append((names[i],names[j],x,y,dot))
 groups=[]
 for pn,path in paths.items():
  p=sum(b[k] for k in path[:3]);H=q(b[path[3]]+b[path[4]],sum(b[k] for k in path))+q(b[path[3]],(p+1)*(p+2));groups.append((pn,H,q(1,p+1),q(1,p+2)))
 for tag,key,prefix,ts in [('AB','AB_hist','AB',types),('AE','AE_hist','AE',types),('Sbranch','second_hist','A',quads)]:
  p0=sum(b[k] for k in prefix);hist=a[key]
  def sm(fn):return sum((n*fn(t) for n,t in zip(hist,ts)),F())
  bg=lambda t:p0+sum(t[:-2]);H=sm(lambda t:q(t[-2]+t[-1],p0+sum(t))+q(t[-2],(bg(t)+1)*(bg(t)+2)));groups.append((tag,H,sm(lambda t:q(1,bg(t)+1)),sm(lambda t:q(1,bg(t)+2))))
 for tag,H,D1,D2 in groups:
  for ma,mb,x,y,dot in pairs:
   out[f'{tag}:align-tax:{ma}|{mb}']=5*H-(x+y)*D1+2*dot*(D1-D2)
   out[f'{tag}:off-tax:{ma}|{mb}']=20*H-4*(x+y)*D1+2*(x*y-dot)*(D1-D2)
 return out

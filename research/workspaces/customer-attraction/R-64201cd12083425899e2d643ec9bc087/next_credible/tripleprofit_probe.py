"""Necessary real remaining-three 5/3 profit comparisons of aligned menu triples.
No new customer coordinates. Every row sums fixed whole-theme comparisons.
"""
from offdiagonal_probe import types,quads,labels,paths,q,F
from itertools import combinations_with_replacement

def rows(a):
 b=dict(zip(labels,map(int,a['bits'])));out={};S=a['second_hist'];d=sum(n*t[0] for n,t in zip(S,quads));pA=b['A']
 tail=lambda path: q(sum(b[k] for k in path[2:]),sum(b[k] for k in path))
 actual=tail(paths['actual']);second=tail(paths['second']);batch=sum((n*q(sum(t[1:]),pA+sum(t)) for n,t in zip(S,quads)),F())
 for source,key,ts,names in [('AB','AB_hist',types,'TXY'),('AE','AE_hist',types,'TXY'),('Sbranch','second_hist',quads,'TUVW')]:
  hist=a[key]
  for positions in combinations_with_replacement(range(len(names)),3):
   title=source+':'+''.join(names[i] for i in positions)
   def load(t):return sum(t[i] for i in positions)
   for group,p,R in [('AB',b['A']+b['B'],actual),('AE',b['A']+b['E'],second)]:
    cmp=sum((n*q(load(t),p+load(t)) for n,t in zip(hist,ts)),F())
    out[f'{group}:three-profit:{title}']=F(25,3)*R-cmp
   allcmp=sum((n*(d*q(load(t),pA+1+load(t))+(5-d)*q(load(t),pA+load(t))) for n,t in zip(hist,ts)),F())
   owncmp=sum((n*q(load(t),pA+t[0]+load(t)) for n,t in zip(hist,ts)),F())
   out[f'Sbranch:three-profit-all:{title}']=F(25,3)*batch-allcmp
   out[f'Sbranch:three-profit-align:{title}']=F(5,3)*batch-owncmp
   out[f'Sbranch:three-profit-off:{title}']=F(20,3)*batch-allcmp+owncmp
 return out

"""Independent exact audits; no optimizer or peer algebra helpers imported."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
import json
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[5]
# Crossed-reply identity: exact coefficients of 1/(p+1),1/(p+2),
# 1/(p+3), hence all symbolic backgrounds p>=0 at once. Adjacent tax
# denominators use 1/[(p+k)(p+k+1)]=1/(p+k)-1/(p+k+1).
def E(k,n=1):return tuple(Q(n) if j==k else Q(0) for j in (1,2,3))
def add(*xs):return tuple(map(sum,zip(*xs)))
def neg(x):return tuple(-z for z in x)
def u(a,others):return E(1+sum(others),a)
def phi(a,b):return add(E(1,int(a+b>=1)),E(2,int(a+b>=2)))
zero=(Q(0),)*3;checks=0
for t,r,s,v,w,k in product((0,1),repeat=6):
 L1=add(u(r,[t,s]),neg(u(v,[t,k])))
 L2=add(u(k,[t,v]),neg(u(w,[t,v])))
 L3=add(u(s,[t,r]),neg(u(k,[t,r])))
 lhs=add(u(t,[r,s]),neg(u(t,[v,w])))
 assert add(lhs,neg(L1),neg(L2),neg(u(s,[t])),u(k,[t]),neg(phi(v,w)),phi(r,s))==zero
 tax=Q(r*(1-s));rem=Q(r*(1-k))
 taxform=add(E(t+1,tax),E(t+2,-tax))
 remform=add(E(t+1,rem),E(t+2,-rem))
 assert add(lhs,taxform,neg(L1),neg(L2),neg(L3),neg(remform),neg(phi(v,w)),phi(r,s))==zero
 assert tax>=0 and rem>=0
 checks+=1
# D7 separation: rebuild seven genuine rows from customer incidence and path
# backgrounds, independent of separate_second_D.seven and third_D_completion.
source=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
peer=json.loads((BASE.parent/'branch_geometry'/'separate_second_D.json').read_text())
names=('F2D','last:E','last:sumopt','AE4:R','AE4:S','second3:T','second4:T')
weights=[Q(peer['nonnegative_weights'][name]) for name in names]
assert all(x>=0 for x in weights)
def ratio(n,d):return Q(n,d) if n else Q(0)
tri=list(product((0,1),repeat=3));quad=list(product((0,1),repeat=4))
maxima=[];legal=0
for atom in source['atoms']:
 a,b,c,d,e,*_=map(int,atom['bits']); oldload=a+b+c+d+e
 opt_counts=[sum(cnt*pattern[0] for cnt,pattern in zip(atom[key],tri if key!='second_hist' else quad)) for key in ('AB_hist','AE_hist','second_hist')]
 assert len(set(opt_counts))==1
 opt=opt_counts[0]
 ae_first=Q(0);ae_den=Q(0);sec_first=Q(0);sec_second=Q(0);sec_den1=Q(0);sec_den2=Q(0)
 for cnt,(ot,rr,ss) in zip(atom['AE_hist'],tri):
  ae_first+=cnt*ratio(rr,a+e+ot+rr+ss)
  ae_den+=cnt*Q(1,a+e+ot+2)
 for cnt,(ot,hh,ii,jj) in zip(atom['second_hist'],quad):
  load=a+ot+hh+ii+jj
  sec_first+=cnt*ratio(hh,load);sec_second+=cnt*ratio(ii,load)
  sec_den1+=cnt*Q(1,a+ot+3);sec_den2+=cnt*Q(1,a+ot+hh+2)
 values=[]
 for rr,ss,tt in product((0,1),repeat=3):
  newload=a+d+rr+ss+tt
  rows=(ratio(b,oldload)-ratio(d,newload),
        ratio(tt,newload)-ratio(e,a+d+rr+ss+1),
        5*ratio(tt,newload)-ratio(opt,a+d+rr+ss+1),
        ae_first-rr*ae_den,ae_first-ss*ae_den,
        sec_first-tt*sec_den1,sec_second-tt*sec_den2)
  values.append(sum(w*x for w,x in zip(weights,rows)));legal+=1
 maxima.append(max(values))
assert maxima==[Q(z) for z in peer['maximums']]
gap=sum(Q(int(atom['mass_numerator']),int(source['denominator']))*mx for atom,mx in zip(source['atoms'],maxima))
assert gap==Q(peer['exact_projected_slack'])<0
report={'status':'passed','crossed_reply_symbolic_background_cases':checks,'crossed_reply_scope':'general nonnegative integer old background, all history-dependent replies/ties; proves only taxed decorrelation','D7_atoms':len(maxima),'D7_split_types':legal,'D7_exact_projected_slack':str(gap),'D7_scope':'historical fixed-primal extension excluded; no full five-player bound or SPE counterexample'}
(BASE/'peer_relations_independent_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))

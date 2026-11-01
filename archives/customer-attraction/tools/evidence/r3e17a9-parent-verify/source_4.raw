"""Exact replay. Old 1143 rows reuse frozen old generator; new 88 rows literal.
Does not import either new discovery implementation.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from collections import defaultdict
import sys,json,hashlib
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
PREV=ROOT/'research/workspaces/customer-attraction/R-a8ee6fdb155c47da95540775b4a6a2db/closure'
sys.path.insert(0,str(PREV));import joint_atoms as old
PAT=tuple(product(range(2),repeat=3))
NAMES=['source','oldpair-newpair']+[('oldC',q) for q in ('D','E')]
NAMES += [('newE',q) for q in ('T','B','C','D','E','opt','oldB','oldC')+tuple('a'+str(i) for i in range(6))]
NAMES += [('pair',tuple(qs)) for qs in combinations_with_replacement(('T','B','C')+tuple('a'+str(i) for i in range(6)),2)]
NAMES += [('pair','opt'),('pair','Topt'),('pair','Bopt'),('pair','Copt')]
NAMES += [('price',q,i) for q in ('D','E') for i in range(6)]+[('capacity',q) for q in ('D','E')]
NAMES += [('actualpair',qs) for qs in (('D','E'),('B','D'),('B','E'),('C','D'),('C','E'),('T','D'),('T','E'))]
def share(n,d):return F(n,d) if n else F()
def H(b,X,Y):return F(X+Y,b+1)-F(X*Y,(b+1)*(b+2))
def pair_budget(b,X,Y):return share(X+Y,b+X+Y)+F(X,(b+1)*(b+2))
def literal(a,h,word,de):
 t,b,c=word;D,E=de;p=sum(a[:3]);whole=sum(a);words=[w for w,n in zip(PAT,h) for _ in range(n)]
 mem={'T':t,'B':b,'C':c,'D':D,'E':E}|{'a'+str(i):v for i,v in enumerate(a)}
 uc=share(c,p+t+b+c);ue=share(E,p+b+D+E);newbudget=pair_budget(p+b,D,E);actualbudget=pair_budget(sum(a[:4]),a[4],a[5]);out=[]
 for name in NAMES:
  if name=='source':val=share(a[3],whole)-share(b,p+b+D+E)
  elif name=='oldpair-newpair':val=pair_budget(p+t,b,c)-H(p+t,D,E)
  elif name[0]=='oldC':val=uc-F(mem[name[1]],p+t+b+1)
  elif name[0]=='newE':
   q=name[1]
   if q in ('opt','oldB','oldC'):
    pos=('opt','oldB','oldC').index(q);val=sum(ue-F(w[pos],p+b+D+1) for w in words)/6
   else:val=ue-F(mem[q],p+b+D+1)
  elif name[0]=='pair':
   q=name[1]
   if q=='opt':cost=sum(H(p+b,words[i][0],words[j][0]) for i in range(6) for j in range(i+1,6))/15
   elif isinstance(q,str):cost=sum(H(p+b,mem[q[0]],w[0]) for w in words)/6
   else:cost=H(p+b,*(mem[z] for z in q))
   val=newbudget-cost
  elif name[0]=='price':_,q,i=name;val=share(a[i],whole)-F(mem[q],sum(a[:i])+6-i)
  elif name[0]=='capacity':val=-F(mem[name[1]])
  elif name[0]=='actualpair':val=actualbudget-H(sum(a[:4]),*(mem[z] for z in name[1]))
  out.append(val)
 return out

def main():
 target=HERE/'promotion_joint_atoms_exact.json';data=json.loads(target.read_text());names,kcol,locs=old.model();K=F(data['K'])
 assert len(names)==1143 and len(NAMES)==88
 oldslack=[K*v for v in kcol];mass=defaultdict(F);W=O=F()
 for atom in data['RZ_atoms']:
  hi=atom['hist_index'];n=F(atom['weight']);assert n>=0;loc=locs[hi];r,z=atom['R'],atom['Z'];assert all(v in (0,1) for v in r+z)
  vals=old.atom(loc,r,z,True);oldslack=[s+n*v for s,v in zip(oldslack,vals)];mass[hi]+=n;W+=n*loc['obj'];O+=n*loc['norm']
 assert O==1 and W==F(data['W']) and W<F(1,2) and min(oldslack)>=0
 states=defaultdict(dict)
 for q in data['promotion_states']:
  key=q['hist_index'],q['word_index'];de=tuple(q['DE']);n=F(q['weight']);assert n>=0 and de in ((0,1),(1,0),(1,1)) and de not in states[key];states[key][de]=n
 slacks=[6*K if isinstance(n,tuple) and n[0]=='capacity' else F() for n in NAMES];boundslack=[];cases=0
 for hi,loc in enumerate(locs):
  a=tuple(map(int,loc['hist']['actual_bits']));h=loc['hist']['hist']
  assert data['histograms'][hi]==loc['hist']
  for wi,(word,mult) in enumerate(zip(PAT,h)):
   if not mult:assert not states[hi,wi];continue
   vals=states[hi,wi];zero=mass[hi]-sum(vals.values());assert zero>=0;boundslack.append(zero)
   for de,n in [((0,0),zero),*vals.items()]:
    vs=literal(a,h,word,de);slacks=[s+mult*n*v for s,v in zip(slacks,vs)];cases+=1
 assert min(slacks)>=0,(NAMES[slacks.index(min(slacks))],min(slacks))
 report={'status':'exact feasible necessary point verified; no game/SPE or half theorem','scope':'old 1143 rows reuse frozen generator; new 88 rows independently expanded from labeled query/pair definitions; state mass bounds independently checked','old_rows':len(names),'new_rows':len(NAMES),'state_mass_bounds':len(boundslack),'total_rows':len(names)+len(NAMES)+len(boundslack),'literal_new_state_cases':cases,'W':str(W),'strict_half_gap':str(1-2*W),'minimum_slack':str(min(oldslack+slacks+boundslack)),'RZ_atoms':len(data['RZ_atoms']),'positive_promotion_states':len(data['promotion_states']),'input_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
 assert report['total_rows']==data['rows']
 (HERE/'promotion_joint_atoms_verify.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()

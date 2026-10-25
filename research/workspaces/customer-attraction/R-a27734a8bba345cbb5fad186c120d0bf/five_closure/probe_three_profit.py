from fractions import Fraction as F
from itertools import combinations_with_replacement, product
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
NAMES=list('ABCDEUV WXY'.replace(' ',''))
def frac(x):return F(x)
def profit(p,k):return F(k,p+k) if k else F(0)
def expected(p, probs):
 return sum((profit(p,sum(v))*prod((q if bit else 1-q) for bit,q in zip(v,probs)) for v in product((0,1),repeat=3)),F(0))
def prod(xs):
 z=F(1)
 for x in xs:z*=x
 return z
def atom_data(a):
 bits=list(map(int,a['bits']));B=[tuple(map(int,f'{i:03b}')) for i in range(8)];S=[tuple(map(int,f'{i:04b}')) for i in range(16)]
 AB=list(zip(a['AB_hist'],B));AE=list(zip(a['AE_hist'],B));SB=list(zip(a['second_hist'],S))
 probs={n:F(b) for n,b in zip(NAMES,bits)}
 probs['T']=sum((F(n)*v[0]/5 for n,v in AB),F(0))
 for lab,hh,cols in [('AB',AB,'RS'),('AE',AE,'RS'),('SB',SB,'HIJ')]:
  for k,c in enumerate(cols,1):probs[lab+'.'+c]=sum((F(n)*v[k]/5 for n,v in hh),F(0))
 for k,(l,h) in enumerate(a['menus_lh']):probs['L'+str(k)]=F(l,5)
 aa,b,c,d,e,u,v,w,x,y=bits
 sources={'AB':[(F(1),aa+b,profit(aa+b,c+d+e))], 'AE':[(F(1),aa+e,profit(aa+e,u+v+w))], 'SB':[(F(n,5),aa+t,profit(aa+t,h+i+j)) for n,(t,h,i,j) in SB if n]}
 return F(a['exact_mass']),probs,sources

def main(path):
 d=json.load(open(path));dat=[atom_data(a) for a in d['atoms']];names=list(dat[0][1]);triples=list(combinations_with_replacement(names,3)); out=[]
 for src in ['AB','AE','SB']:
  vals=[]
  for qs in triples:
   slack=sum((mass*sum((weight*(F(5,3)*V-expected(p,[probs[q] for q in qs])) for weight,p,V in sources[src]),F(0)) for mass,probs,sources in dat),F(0))
   vals.append((slack,qs))
  vals.sort();out.append({'source':src,'minimum':str(vals[0][0]),'minimum_float':float(vals[0][0]),'queries':vals[0][1],'negative_rows':sum(v<0 for v,q in vals)})
 return {'source':str(path),'scope':'Three-remaining 5/3 profit theorem, independent Cartesian triple query distributions; exact marginal evaluation only','rows_per_source':len(triples),'results':out}
if __name__=='__main__':
 print(json.dumps(main(Path(sys.argv[1])),indent=2))

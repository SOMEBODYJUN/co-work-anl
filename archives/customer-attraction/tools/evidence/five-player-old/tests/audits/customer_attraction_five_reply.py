"""Pure Fraction replay of CA-FIVE-REPLY-UPPER.
No LP, SPE solver, or floating discovery output is read. The theorem also
requires the manuscript's ordered-node legality argument.
"""
import argparse
from fractions import Fraction as Q
from itertools import product
from math import lcm
from pathlib import Path
import hashlib,json
LABELS=tuple('ABCDEUVWXY')
PATHS={'actual':tuple('ABCDE'),'second':tuple('AEUVW'),'third':tuple('ABEXY')}
ROOT=Path(__file__).resolve().parents[2]
CERT=ROOT / 'evidence/certificates/customer_attraction/five_player_reply_bound.json'
EXPECTED_MINIMA=(0, 0, 0, 33787799191020600, 35644333391981100, 26312270041902900, 0, 39570994049198600, 18352830214258200, 1062579276463200, 0, 20085137676333200, 9885320187038200, 15597170349671800, 870090456771950, 29256266152440950, 41060538182699400, 7735274982211200, 8995605516109920, 21324995575968120, 18880925703148120, 16837028249306720, 6240740486985270, 28528711039627970, 6081507332903600, 0, 0, 15686380873567330, 0, 8499737116717530, 1301205546691780, 22158447840456840)
def frac(n,d):return Q(n,d) if n else Q(0)
def coefficient(bits,d,ell,name):
 b=dict(zip(LABELS,bits));opt=int(d>0)
 def profit(path,i):return frac(b[path[i]],sum(b[t] for t in path))
 terms=name.split(':')
 if terms[0]=='F':
  pos={'second':1,'third':2}[terms[1]]
  return profit(PATHS['actual'],pos)-profit(PATHS[terms[1]],pos)
 key=terms[0];path=PATHS[key]
 if terms[1]=='reply':
  p=sum(b[t] for t in path[:3]);L=ell[tuple(PATHS).index(key)]
  if terms[2]=='S+V':return 25*profit(path,3)-frac(5*d,p+1)+frac(d*L,(p+1)*(p+2))
  if terms[2]=='Z':return 5*profit(path,4)-frac(L,p+b[path[3]]+1)
  raise AssertionError(name)
 pos=int(terms[1])-1;p=sum(b[t] for t in path[:pos]);k=5-pos
 if terms[2]=='K':return profit(path,pos)-frac(b[terms[3]],p+k)
 if terms[2]=='O':return 5*k*profit(path,pos)+frac(p,p+k)-opt
 if terms[2].startswith('sum-L-'):
  group=terms[2][6:];L=ell[tuple(PATHS).index(group)]
  return 5*profit(path,pos)-frac(L,p+k)
 raise AssertionError(name)
def check():
 data=json.loads(CERT.read_text());assert data['claim']=='CA-FIVE-REPLY-UPPER'
 assert data['labels']==list(LABELS)
 assert data['paths']=={k:list(v) for k,v in PATHS.items()}
 bound=Q(data['bound']);weights={n:Q(v) for n,v in data['multipliers'].items()}
 assert bound>2 and bound<Q(211,100)
 assert all(v>=0 for v in weights.values())
 multiplier_den=lcm(*[v.denominator for v in weights.values()],bound.denominator)
 scale=120*multiplier_den;table=[];checks=zero=0
 for actual in product((0,1),repeat=5):
  minimum=None
  for aux in product((0,1),repeat=5):
   for d in range(6):
    for ell in product((0,5),repeat=3):
     r=bound*int(any(actual))-int(d>0)-sum((w*coefficient(actual+aux,d,ell,n) for n,w in weights.items()),Q(0))
     assert r>=0,(actual,aux,d,ell,r)
     rr=scale*r;assert rr.denominator==1
     minimum=int(rr) if minimum is None else min(minimum,int(rr));zero+=r==0;checks+=1
  table.append(minimum)
 assert tuple(table)==EXPECTED_MINIMA
 report={'claim':'CA-FIVE-REPLY-UPPER','exact_bound':str(bound),'corner_checks':checks,'zero_corner_residuals':zero,'common_multiplier_denominator':multiplier_den,'residual_table_scale':scale,'minimum_scaled_residual_by_actual_ABCDE':table,'weights_nonnegative':True,'all_corner_residuals_nonnegative':True,'certificate_sha256':hashlib.sha256(CERT.read_bytes()).hexdigest(),'scope':'Universal algebra certificate, contingent on legally defined true SPE paths and reply menus; this is neither a game instance nor a half-coverage result.'}
 return report
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--output',type=Path)
 args=parser.parse_args()
 report=check()
 rendered=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
 if args.output:
  args.output.parent.mkdir(parents=True,exist_ok=True)
  with args.output.open('x',encoding='utf-8') as handle:handle.write(rendered)
 print(rendered,end='')
if __name__=='__main__':main()

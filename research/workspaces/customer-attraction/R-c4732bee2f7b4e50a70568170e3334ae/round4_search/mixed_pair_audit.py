"""Lift-independent common-catalog pair comparisons across every recorded menu.
Original three two-player nodes and the aggregate of each indexed family.
All query-pair sums are Cartesian, so joint cross-family lifts are unnecessary.
"""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json,hashlib,argparse
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
ACTOR=Path(__file__).resolve().parents[1]
PARTS=tuple(product((0,1),repeat=3));PART4=tuple(product((0,1),repeat=4))

def query_menus(atom):
 bits=dict(zip('ABCDEUVWXY',map(int,atom['bits'])))
 out={a:(1,b) for a,b in bits.items()}
 for fam,field,arity,labels in [('AB','AB_hist',3,('T','AB.R','AB.S')),('AE','AE_hist',3,('T','AE.R','AE.S')),('SB','second_hist',4,('T','SB.H','SB.I','SB.J'))]:
  states=tuple(product((0,1),repeat=arity));hist=atom[field]
  for pos,label in enumerate(labels):
   value=(5,sum(n*st[pos] for n,st in zip(hist,states)))
   if label in out:assert out[label]==value
   out[label]=value
 for r,(ell,h) in zip(('actual.L','second.L','third.L'),atom['menus_lh']):out[r]=(5,ell)
 return bits,out

def local_H(p,first,last):
 return (F(first+last,p+first+last) if first+last else F(0))+F(first,(p+1)*(p+2))

def branches(atom):
 bits,_=query_menus(atom);out={}
 for fam,pref,first,last in [('actual','ABC','D','E'),('second','AEU','V','W'),('third','ABE','X','Y')]:
  p=sum(bits[b] for b in pref);out[fam]=(local_H(p,bits[first],bits[last]),F(1,p+1),F(1,(p+1)*(p+2)))
 for fam,field,arity,pref in [('AB','AB_hist',3,'AB'),('AE','AE_hist',3,'AE'),('SB','second_hist',4,'A')]:
  h=f=d=F(0);prefix=sum(bits[b] for b in pref)
  for st,n in zip(product((0,1),repeat=arity),atom[field]):
   p=prefix+sum(st[:-2]);h+=n*local_H(p,*st[-2:]);f+=F(n,p+1);d+=F(n,(p+1)*(p+2))
  out[fam]=(h,f,d)
 return out

def rows(atom):
 bits,menus=query_menus(atom);out={}
 for branch,(H,inv,inv2) in branches(atom).items():
  for a,b in combinations_with_replacement(menus,2):
   na,M=menus[a];nb,N=menus[b]
   out[f'{branch}:mixed-pair:{a}:{b}']=na*nb*H-(nb*M+na*N)*inv+M*N*inv2
 # Split whether one query index equals its own two-player branch index.
 # The other query remains a Cartesian menu sum (or one fixed topic).
 for fam,field,arity,pref,labels in [('AB','AB_hist',3,'AB',('T','AB.R','AB.S')),('AE','AE_hist',3,'AE',('T','AE.R','AE.S')),('SB','second_hist',4,'A',('T','SB.H','SB.I','SB.J'))]:
  states=tuple(product((0,1),repeat=arity));hist=atom[field];prefix=sum(bits[b] for b in pref)
  for pos,label in enumerate(labels):
   _,B=menus[label]
   for other,(n,N) in menus.items():
    diagonal=off=F(0)
    for st,ct in zip(states,hist):
     p=prefix+sum(st[:-2]);H=local_H(p,*st[-2:]);b=st[pos]
     diagonal+=ct*(n*H-F(n*b+N,p+1)+F(b*N,(p+1)*(p+2)))
     off+=ct*(4*n*H-F(n*(B-b)+4*N,p+1)+F((B-b)*N,(p+1)*(p+2)))
    out[f'{fam}:mixed-index:{label}:{other}:diagonal']=diagonal
    out[f'{fam}:mixed-index:{label}:{other}:offdiagonal']=off
 # Direct one-step comparisons at actual indexed optimizing nodes.
 for fam,field,arity,pref in [('AB','AB_hist',3,'AB'),('AE','AE_hist',3,'AE'),('SB','second_hist',4,'A')]:
  states=tuple(product((0,1),repeat=arity));hist=atom[field];prefix=sum(bits[b] for b in pref)
  for remaining in range(1,arity):
   pos=arity-remaining
   U=F(0);inv=F(0)
   for st,ct in zip(states,hist):
    background=prefix+sum(st[:pos]);total=prefix+sum(st)
    U+=F(ct*st[pos],total) if st[pos] else F(0)
    inv+=F(ct,background+remaining)
   for label,(n,N) in menus.items():out[f'{fam}:direct:{pos}:all-{label}']=n*U-N*inv
 for fam,pref,menu in [('actual','ABC',0),('second','AEU',1),('third','ABE',2)]:
  p=sum(bits[b] for b in pref);ell,h=atom['menus_lh'][menu];j=menus['T'][1]
  U=F(ell-h,p+1)+F(h,p+2);inv=F(5-j,p+1)+F(j,p+2)
  for label,(n,N) in menus.items():out[f'{fam}:indexed-terminal:all-{label}']=n*U-N*inv
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,default=ACTOR/'round4_pricing/exact_primal_overlap1.json');ap.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));a=ap.parse_args()
 src=json.loads(a.source.read_text());totals={}
 for atom in src['atoms']:
  mass=F(atom['exact_mass'])
  for name,v in rows(atom).items():totals[name]=totals.get(name,F(0))+mass*v
 neg={k:v for k,v in totals.items() if v<0}
 ordered=sorted(neg,key=lambda k:neg[k]);report={'scope':'Necessary true-SPE Cartesian pair-query sums across all recorded menus; lift-independent, no sufficiency claim','source':str(a.source.resolve().relative_to(ROOT)),'source_sha256':hashlib.sha256(a.source.read_bytes()).hexdigest(),'row_count':len(totals),'negative_count':len(neg),'negative_rows':{k:str(neg[k]) for k in ordered},'all_rows':{k:str(v) for k,v in totals.items()}}
 a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({**{k:v for k,v in report.items() if k not in ('all_rows','negative_rows')},'most_negative':[{'row':k,'value':str(neg[k]),'float':float(neg[k])} for k in ordered[:20]]},indent=2))
if __name__=='__main__':main()

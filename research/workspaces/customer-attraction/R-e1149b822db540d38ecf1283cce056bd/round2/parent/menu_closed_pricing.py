"""Common-K/COPY-M closure over all old menus; floating discovery only."""
from fractions import Fraction as F
import hashlib,json,sys,time
import numpy as np
from scipy.optimize import linprog
import cross_family_pricing as cf
HERE=cf.HERE;ROOT=cf.ROOT;old=cf.old
AC,BC,CC=F(44,3),F(13,5),F(16,3)
MENUS=[(t,c) for t in cf.TAGS for c in cf.QUERIES[t]]+[(f'L{i}','L') for i in range(3)]
KINDS=[('cap',0)]+[(k,j) for k in ('source-fixed','fixed-target') for j in range(10)]+[('source-opt',0),('opt-target',0)]
SPECS=[(tag,c,k,j) for tag,c in MENUS for k,j in KINDS]
GNAMES=[t+':GM:'+str(i) for i,(t,_,_,_) in enumerate(SPECS)]
SPEC=dict(zip(GNAMES,SPECS))
def formula(bits,d,s):
 tag,c,kind,j=s;b=list(map(int,bits));r=cf.q(b[0],sum(b[:5]));v=b[j]
 if kind=='cap':return F(),F(-1),F(5)
 if kind=='source-fixed':return 5*AC*r-5*v,-CC+F(4,5)*v,5*BC
 if kind=='fixed-target':return 5*AC*r-5*CC*v,F(-1)+F(4,5)*v,5*BC
 if kind=='source-opt':return 25*AC*r-5*d,-5*CC+F(4,5)*d,25*BC
 if kind=='opt-target':return 25*AC*r-5*CC*d,F(-5)+F(4,5)*d,25*BC
 raise AssertionError(kind)
def count(atom,tag,c):
 if tag.startswith('L'):return int(atom['menus_lh'][int(tag[1:])][0])
 k=4 if tag=='Sbranch' else 3;j=cf.QUERIES[tag].index(c)+1
 hist=atom['second_hist' if k==4 else tag+'_hist']
 return sum(int(n)*((i>>(k-1-j))&1) for i,n in enumerate(hist))
def rows(atom):
 d=sum(atom['AB_hist'][4:]);out={}
 for n,s in SPEC.items():
  const,co,kco=formula(atom['bits'],d,s);out[n]=const+co*count(atom,s[0],s[1])
 return out

class Universe(cf.Universe):
 def __init__(self):
  super().__init__();self.names+=GNAMES
  arr=np.zeros((1024,6,len(GNAMES)),dtype=np.int64)
  ec=np.zeros((1024,6,3,len(GNAMES)),dtype=np.int64)
  for bi,bits in enumerate(self.bits):
   for d in range(6):
    vals=[formula(bits,d,s) for s in SPECS];arr[bi,d]=old.sc([z[0] for z in vals])
    for j,(tag,c,kind,v) in enumerate(SPECS):
     if tag.startswith('L'):ec[bi,d,int(tag[1:]),j]=int(old.sc(vals[j][1]))
  self.oldnames+=GNAMES;self.oldids=[self.names.index(n) for n in self.oldnames]
  self.base=np.concatenate((self.base,arr),axis=-1)
  self.ec=np.concatenate((self.ec,ec),axis=-1)
  self.hc=np.concatenate((self.hc,np.zeros_like(ec)),axis=-1)
  for n,s in SPEC.items():cf.shared.KCO[n]=formula((0,)*10,0,s)[2]
  print(json.dumps({'menu_closed_rows':len(GNAMES),'total_rows':len(self.names)}),flush=True)
 def atom_rows(self,atom):
  rr=super().atom_rows(atom);rr.update(rows(atom));return rr
 def family_score(self,bits,tag,weights,integer=False):
  own=[(n,v) for n,v in weights if ':GM:' in n]
  rest=[(n,v) for n,v in weights if ':GM:' not in n]
  key,const,vec,E,H=super().family_score(bits,tag,rest,integer)
  coeff={c:[0,0] for c in cf.QUERIES[tag]}
  for n,v in own:
   s=SPEC[n];assert s[0]==tag;c=s[1]
   c0=int(old.sc(formula(bits,0,s)[1]))
   c1=int(old.sc(formula(bits,1,s)[1]))-c0
   coeff[c][0]+=v*c0;coeff[c][1]+=v*c1
  vec=list(vec);k=4 if tag=='Sbranch' else 3
  for c,(v0,v1) in coeff.items():
   if v0:vec.append((v0,self.count[k][c]))
   if v1:vec.append((v1,self.count[k][c]*self.d[k]))
  return (k,key,tuple((c,*v) for c,v in coeff.items())),const,vec,E,H

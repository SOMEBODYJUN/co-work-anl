"""Finite-grid legal priced cuts: forced R/Z, Q from its six old index bits."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
import json,sys
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'work.py').exists())
sys.path.insert(0,str(ROOT))
from customer_attraction.priced_hidden_reply import projected_by_count
PAT=tuple(product((0,1),repeat=3));GS=((0,0),(1,0),(1,1))
@lru_cache(None)
def psi(i,p,ell,t,q,mode,aa,mu):
 k=6-i;alpha=(aa,)*(k-1) if mode=='all' else (F(),)*(k-2)+(aa,)
 return projected_by_count(p,ell,t,q,alpha,(F(),)*(k-1),mu)
def groups(hist):
 out={}
 for f,diag in GS:
  for wi,wj in product(PAT,repeat=2):
   ni=hist[PAT.index(wi)];nj=hist[PAT.index(wj)]
   n=ni if diag and wi==wj else (0 if diag else ni*nj-(ni if wi==wj else 0))
   if n:out[(f,diag,wi,wj)]=n
 return out

def row(cols,cut):
 i,member,f,diag,qi,mode,aa,mu=cut;aa=F(aa);mu=F(mu);out=[F()]*len(cols);hi=None;na=(5-i)*aa if mode=='all' else aa
 for j,c in enumerate(cols):
  if c['kind']=='hist':
   hi=c;a=tuple(map(int,c['actual_bits']));whole=sum(a);p=sum(a[:i]);ell=sum(a[:5]);ct=6 if diag else 30
   own=F(a[i],whole) if a[i] else F();last=F(a[5],whole) if a[5] else F();v=ct*(own+na*last)
   for (ff,dd,wi,wj),n in groups(c['hist']).items():
    if (ff,dd)==(f,diag):v-=n*psi(i,p,ell,0,(wi+wj)[qi],mode,aa,mu)
   out[j]=v
  elif c['kind']=='joint-reply':
   ff,dd,wi,wj=c['group']
   if (ff,dd)!=(f,diag) or not c['state'][member]:continue
   ni=hi['hist'][PAT.index(tuple(wi))];nj=hi['hist'][PAT.index(tuple(wj))];n=ni if diag else ni*nj-(ni if wi==wj else 0)
   a=tuple(map(int,hi['actual_bits']));p=sum(a[:i]);ell=sum(a[:5]);q=(tuple(wi)+tuple(wj))[qi]
   out[j]=-n*(psi(i,p,ell,1,q,mode,aa,mu)-psi(i,p,ell,0,q,mode,aa,mu))
 return out

def discover(path,outpath):
 point=json.loads(Path(path).read_text());hs=[];h=None
 for c in point['columns']:
  if c['kind']=='hist':
   h={'a':tuple(map(int,c['actual_bits'])),'mass':F(c['weight']),'groups':groups(c['hist']),'tmass':{}};hs.append(h)
  elif c['kind']=='joint-reply':
   f,d,wi,wj=c['group'];g=(f,d,tuple(wi),tuple(wj));ys=h['tmass'].setdefault(g,[F(),F()]);w=F(c['weight'])
   for m in range(2):ys[m]+=w*c['state'][m]
 data={};us=[F()]*6
 for h in hs:
  a=h['a'];whole=sum(a)
  for i in range(6):us[i]+=h['mass']*(F(a[i],whole) if a[i] else F())
 for member,fdiag,qi in product(range(2),GS,range(6)):
  byhist=[]
  for h in hs:
   nq=[F(),F()];mt=[F(),F()]
   for g,n in h['groups'].items():
    f,d,wi,wj=g
    if (f,d)!=fdiag:continue
    q=(wi+wj)[qi];nq[q]+=h['mass']*n;mt[q]+=n*h['tmass'].get(g,[F(),F()])[member]
   byhist.append((h['a'],((nq[0]-mt[0],mt[0]),(nq[1]-mt[1],mt[1]))))
  data[member,*fdiag,qi]=byhist
 candidates=[];checked=0
 for i,member,fdiag,qi,mode,aa,mu in product(range(5),range(2),GS,range(6),('all','last'),(F(),F(1,8),F(1,4),F(1,2),F(1),F(2)),(F(),F(1,2),F(1),F(2),F(4))):
  if aa==0 and mode=='last':continue
  f,d=fdiag;na=(5-i)*aa if mode=='all' else aa;v=(6 if d else 30)*(us[i]+na*us[5])
  for a,masses in data[member,f,d,qi]:
   p=sum(a[:i]);ell=sum(a[:5])
   for q,t in product(range(2),repeat=2):v-=masses[q][t]*psi(i,p,ell,t,q,mode,aa,mu)
  checked+=1
  if v<0:candidates.append((v,(i,member,f,d,qi,mode,str(aa),str(mu))))
 candidates.sort();selected=[];seen=set()
 for v,cut in candidates:
  if cut[:6] in seen:continue
  seen.add(cut[:6]);selected.append({'cut':cut,'slack':str(v)})
  if len(selected)>=64:break
 ys=[F(c['weight']) for c in point['columns']]
 for c in selected:assert sum(x*y for x,y in zip(row(point['columns'],c['cut']),ys))==F(c['slack'])
 result={'scope':'finite rational-grid separation only; necessary graph, not SPE','input':str(path),'W':point['W'],'candidates_checked':checked,'negative_candidates':len(candidates),'selected':selected}
 Path(outpath).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='selected'},indent=2));print('selected',len(selected),'worst',selected[0] if selected else None)
if __name__=='__main__':discover(sys.argv[1],sys.argv[2])

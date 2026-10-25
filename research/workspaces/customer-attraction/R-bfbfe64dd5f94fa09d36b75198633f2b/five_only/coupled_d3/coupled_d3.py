"""Discovery: couple genuine optimal-root menus to ABD(FG) branch; no game claim."""
import sys,json,time
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
D=HERE.parent
sys.path.insert(0,str(D))
import combined_root_penultimate as m
old=m.old;ap=m.ap;copies=m.copies
LABELS,ROOTS,PATHS,STATES,TAILS,FIRST=m.LABELS,m.ROOTS,m.PATHS,m.STATES,m.TAILS,m.FIRST
S='D3'

def cross_rows(bits,hist,cb,exact=True):
 Q=old.EX['q'] if exact else old.VE['q']; b=dict(zip(LABELS,bits));path=[b['A'],b['B'],b['D'],*cb];tot=sum(path);p=sum(path[:3]);u=[Q(x,tot) for x in path];H=u[3]+u[4]+Q(cb[0],(p+1)*(p+2))
 def sm(fn):return sum((n*fn(*map(int,t)) for n,t in zip(hist,ap.TYPES)),F(0) if exact else 0)
 count={n:sm(lambda *tt:tt[j]) for j,n in enumerate(ap.RPOS)}
 share={i:sm(lambda *tt:Q(tt[i],sum(tt))) for i in range(1,5)}
 den={i:sm(lambda *tt:Q(1,sum(tt[:i])+5-i)) for i in range(1,5)}
 rootH=share[3]+share[4]+sm(lambda *tt:Q(tt[3],(sum(tt[:3])+1)*(sum(tt[:3])+2)))
 D1=sm(lambda *tt:Q(1,sum(tt[:3])+1));D2=sm(lambda *tt:Q(1,sum(tt[:3])+2))
 out={}
 for i in (3,4):
  pr=sum(path[:i]);k=5-i
  for n,c in count.items():out[f'Cross:copy:{i}:{n}']=5*u[i]-Q(c,pr+k)
 for i in range(1,5):
  for j,lab in enumerate('fg'):out[f'Cross:root:{i}:{lab}']=share[i]-cb[j]*den[i]
 for n,c in count.items():
  for j,lab in enumerate('fg'):
   v=cb[j];out[f'Cross:copytax:{n}:{lab}']=5*H-Q(c+5*v-2*c*v,p+1)-Q(2*c*v,p+2)
 pairs=[('f',cb[0]),('g',cb[1])]+[(l,b[l]) for l in LABELS]
 for (ln,x),(rn,y) in combinations_with_replacement(pairs,2):out[f'Cross:roottax:{ln}:{rn}']=rootH-(x+y-2*x*y)*D1-2*x*y*D2
 return out

class Universe(m.Universe):
 def __init__(self):
  super().__init__();self.root_engine.local['CrossH']=self.root_engine.rh@old.sc([old.q(int(t[3]+t[4]),int(sum(t)))+old.q(int(t[3]),(int(sum(t[:3]))+1)*(int(sum(t[:3]))+2)) for t in ap.TYPES]);self.root_engine.local['CrossD1']=self.root_engine.rh@old.sc([old.q(1,int(sum(t[:3]))+1) for t in ap.TYPES]);self.root_engine.local['CrossD2']=self.root_engine.rh@old.sc([old.q(1,int(sum(t[:3]))+2) for t in ap.TYPES]);self.xnames=list(cross_rows([0]*10,[5]+[0]*31,(0,0)));self.names+=self.xnames;self.xids=[self.names.index(n) for n in self.xnames];print(json.dumps({'cross_rows':len(self.xnames),'total':len(self.names)}),flush=True)
 def atom_rows(self,a,exact=True):
  rr=super().atom_rows(a,exact);rr.update(cross_rows(tuple(map(int,a['bits'])),a['root_hist'],a['copies'][S],exact));return rr
 def price(self,lam,beta,batch=80):
  weights=[(n,float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
  fam={t:[] for t in ('AB','AE','Sbranch')}
  for n,v in weights:
   tag=n.split(':')[0]
   if tag in fam:fam[tag].append((n,v))
   elif ':sum-S' in n:fam['Sbranch'].append((n,v))
  ow=np.asarray(lam)[self.oldids];fixed=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
  fixed+=(self.AP@np.asarray(lam)[self.apids])[:,None];fixed+=self.ST@np.asarray(lam)[self.satids]
  Cvals={};Cidx={};jointS=None
  for src in ROOTS:
   ww=np.asarray(lam)[self.cids[src]];ids=np.flatnonzero(np.abs(ww)>1e-11)
   score=np.tensordot(self.CT[src][...,ids],ww[ids],axes=([-1],[0])) if len(ids) else np.zeros((1024,6,len(STATES[src])))
   satq=np.asarray([sum(float(C*120)*lam[self.names.index(f'Saturation{gi}:copy:{src}:{j}')] for gi,(B,C) in enumerate(m.PAIRS)) for j in range(TAILS[src])])
   if np.any(satq):score-=(np.asarray(STATES[src])@satq)[None,None,:]
   CE=np.zeros((1024,len(STATES[src]),3))
   for i in range(FIRST[src],5):
    for fi,pn in enumerate(PATHS):CE[:,:,fi]-=lam[self.query_indices[src,i,pn]]*self.QD[src,i]
   joint=score[:,:,:,None]+np.einsum('bsf,dqf->bdsq',CE,self.MenuL,optimize=True)
   if src==S:jointS=joint;continue
   Cidx[src]=np.argmax(joint,axis=2);Cvals[src]=np.max(joint,axis=2)
  rw=[(n,v) for n,v in weights if n in self.root_name_set];xw=[(n,v) for n,v in weights if n in self.xnames]
  cache={};rcache={};best=[];minimum=1e100
  for bi,bits in enumerate(self.bits):
   fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[];bm=dict(zip(LABELS,bits))
   for fi,(pn,z) in enumerate(PATHS.items()):
    pp=sum(bm[x] for x in z[:3]);ww=float(np.sum(np.asarray(lam)[self.menu_weight_indices[pn]]))
    E[:,fi]-=sum(float(C*120)*lam[self.names.index(f'Saturation{gi}:L:'+pn)] for gi,(B,C) in enumerate(m.PAIRS))
    E[:,fi]+=ww*int(old.sc(old.q(1,pp+1)));H[:,fi]-=ww*int(old.sc(old.q(1,(pp+1)*(pp+2))))
   for tag in fam:
    key,const,vec,me,mh=self.family_score(bits,tag,fam[tag]);k=key[0]
    if key not in cache:
     score=np.zeros(len(self.hist[k]))
     for v,a in vec:score+=v*a
     vals=[];idx=[]
     for ids in self.ids[k]:
      arg=ids[int(np.argmax(score[ids]))];vals.append(score[arg]);idx.append(int(arg))
     cache[key]=(np.asarray(vals),idx)
    vals,idx=cache[key];fs.append(vals+const);choices.append(idx);E+=me.T;H+=mh.T
   rk,rc,co,me,mh=self.root_engine.root_score(bits,rw)
   for menu in ap.RPOS[1:]:co['count:'+menu]-=sum(float(C*120)*lam[self.names.index(f'Saturation{gi}:rootmenu:'+menu)] for gi,(B,C) in enumerate(m.PAIRS))
   E+=me.T;H+=mh.T
   rootvals=[];rootidx=[]
   for si,cb in enumerate(STATES[S]):
    p=sum(bm[x] for x in 'ABD');path=[bm['A'],bm['B'],bm['D'],*cb];tot=sum(path);u=[old.q(x,tot) for x in path];Ht=u[3]+u[4]+old.q(cb[0],(p+1)*(p+2));constant=0.;cnew=co.copy()
    for name,v in xw:
     sp=name.split(':')[1:]
     if sp[0]=='copy':
      i=int(sp[1]);menu=sp[2];constant+=v*120*5*float(u[i]);cnew['count:'+menu]-=v*120*float(old.q(1,sum(path[:i])+5-i))
     elif sp[0]=='root':
      i=int(sp[1]);cnew[f'Root:{i+1}:K:A']+=v;cnew['den:'+str(i)]-=v*cb['fg'.index(sp[2])]
     elif sp[0]=='copytax':
      menu=sp[1];x=cb['fg'.index(sp[2])];constant+=v*120*float(5*Ht-old.q(5*x,p+1));cnew['count:'+menu]-=v*120*float(old.q(1-2*x,p+1)+old.q(2*x,p+2))
     else:
      vals={**bm,'f':cb[0],'g':cb[1]};x,y=vals[sp[1]],vals[sp[2]];cnew['CrossH']+=v;cnew['CrossD1']-=v*(x+y-2*x*y);cnew['CrossD2']-=v*2*x*y
    rk=tuple(sorted((n,v) for n,v in cnew.items() if v))
    if rk not in rcache:rcache[rk]=self.root_engine.root_price(cnew)
    rv,ri=rcache[rk];rootvals.append(rv+rc+constant);rootidx.append(ri)
   rootvals=np.asarray(rootvals)
   for d in range(6):
    scores=self.MenuL[d]@E[d]+self.MenuH[d]@H[d]
    for src in ROOTS:
     if src!=S:scores+=Cvals[src][bi,d]
    jointnew=jointS[bi,d]+rootvals[:,d,None]
    argS=np.argmax(jointnew,axis=0);scores+=np.max(jointnew,axis=0)
    menu_index=int(np.argmax(scores));si=int(argS[menu_index]);lhs=[(int(self.MenuL[d,menu_index,f]),int(self.MenuH[d,menu_index,f])) for f in range(3)]
    rho=120*(beta*int(any(bits[:5]))-int(d>0))-fixed[bi,d]-float(scores[menu_index])-sum(v[d] for v in fs);minimum=min(minimum,rho)
    if rho < -1e-7:
     cp={s:STATES[s][Cidx[s][bi,d,menu_index]] for s in ROOTS if s!=S};cp[S]=STATES[S][si]
     a={'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][choices[0][d]]),'AE_hist':list(self.hist[3][choices[1][d]]),'second_hist':list(self.hist[4][choices[2][d]]),'menus_lh':lhs,'copies':cp,'root_hist':self.root_engine.rh[rootidx[si][d]].tolist()};best.append((rho,a))
  best.sort(key=lambda x:x[0])
  for rho,a in best[:min(batch,8)]:
   rr=self.atom_rows(a);direct=120*(beta*int(any(map(int,a['bits'][:5])))-int(any(a['AB_hist'][4:])))-120*sum(float(v)*float(rr[n]) for n,v in zip(self.names,lam));assert abs(direct-rho)<1e-5,(direct,rho)
  return minimum,best[:batch],len(cache)+len(rcache)

def run(maxiter=15):
 U=Universe();target=HERE/'search.json';warm=json.loads((target if target.exists() else D/'envelope_half_search.json').read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
 def add(a):
  k=m.key(a)
  if k in keys:return 0
  rr=U.atom_rows(a,False);cols.append(np.fromiter((float(rr[n]) for n in U.names),dtype=float,count=len(U.names)));atoms.append(a);keys.add(k);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
 for a in warm['atoms']:add(a)
 for a in atoms[::max(1,len(atoms)//8)]:
  ex=U.atom_rows(a);ff=U.atom_rows(a,False);assert max(abs(float(ex[n])-float(ff[n])) for n in U.names)<1e-7
 print(json.dumps({'initial_columns':len(atoms),'fast_exact_crosschecks':'passed'}),flush=True);history=[]
 for it in range(maxiter):
  t=time.time();mat=np.asarray(cols).T;scale=np.maximum(1.,np.max(np.abs(mat),axis=1));out=linprog(np.ones(len(U.names)),A_ub=(mat/scale[:,None]).T,b_ub=2*np.asarray(ws)-np.asarray(os),bounds=(0,None),method='highs')
  if not out.success:
   print(json.dumps({'status':'restricted-certificate-infeasible','message':out.message}),flush=True);target.write_text(json.dumps({'status':'restricted-certificate-infeasible','atoms':atoms,'history':history,'message':out.message})+'\n');break
  lam=out.x/scale;minimum,new,contexts=U.price(lam,2.,batch=400);n=sum(add(a) for _,a in new);rec={'iteration':it,'columns':len(atoms),'minimum_scaled_residual':minimum,'new_columns':n,'contexts':contexts,'seconds':time.time()-t};history.append(rec);print(json.dumps(rec),flush=True);target.write_text(json.dumps({'scope':'Floating necessary-row discovery only; not a game or proof.','status':'fixed-beta-two-search','atoms':atoms,'history':history,'dual_multipliers_float':{name:float(v) for name,v in zip(U.names,lam) if v>1e-10}})+'\n')
  if n==0:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 15)

"""Full-universe CG with ten AB-source cross-final single-menu envelopes.

Condition on the AB histogram's t-by-penultimate-bit counts. This leaves
AE and second histograms independent, so no fixed support is imposed.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,time
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent;OLD=HERE.parent/'round4_pricing'
sys.path.insert(0,str(OLD))
from full_pricing import atom_key,sc,LABELS
from cross_pair_pricing import CrossUniverse
from exact_primal import verify_atom
sys.path.insert(0,str(HERE.parent/'round4_coupling'))
from joint_transport import joint_row

class TerminalUniverse(CrossUniverse):
    def __init__(self):
        super().__init__();self.single=[];self.qcost={};self.condids={}
        for target in ('AE','Sbranch'):
            for pos in range(1,4 if target=='Sbranch' else 3):
                for kind in ('D','O'):self.single.append((f'crossfinal:AB:{target}:{pos}{kind}',target,pos,kind))
        self.names += [z[0] for z in self.single]
        self.xcount={t:self.H[3]@(self.ty[3][:,0].__eq__(t)*self.ty[3][:,1]) for t in (0,1)}
        for d in range(6):
            for h0 in range(6-d):
                for h1 in range(d+1):
                    self.condids[d,h0,h1]=np.where((self.d[3]==d)&(self.xcount[0]==h0)&(self.xcount[1]==h1))[0]
        for k in (3,4):
            H=self.H[k];ty=self.ty[k]
            for p,d,h0,h1 in product(range(3),range(6),range(6),range(6)):
                if h0>5-d or h1>d:continue
                D=sum(F(n-h,p+t+1)+F(h,p+t+2) for t,n,h in ((0,5-d,h0),(1,d,h1)))
                for pos in range(1,k):
                    counts={t:H@(ty[:,0].__eq__(t)*ty[:,pos]) for t in (0,1)}
                    K=counts[0]+counts[1];top=np.zeros(len(H),dtype=np.int64);bottom=top.copy()
                    for t,n,h in ((0,5-d,h0),(1,d,h1)):
                        a0=int(sc(F(1,p+t+1)));a1=int(sc(F(1,p+t+2)));c=counts[t]
                        top+=a0*np.minimum(c,n-h)+a1*np.maximum(0,c-n+h)
                        bottom+=a1*np.minimum(c,h)+a0*np.maximum(0,c-h)
                    self.qcost[k,p,d,h0,h1,pos,'D']=-bottom
                    self.qcost[k,p,d,h0,h1,pos,'O']=top-int(sc(D))*K
        print(json.dumps({'terminal_cross_rows':len(self.single),'rows':len(self.names)}),flush=True)
    def atom_rows(self,atom):
        rr=super().atom_rows(atom)
        for n,target,pos,kind in self.single:rr[n]=joint_row(atom,'AB','second' if target=='Sbranch' else target,((pos,kind,F(1)),))
        return rr
    def price(self,lam,beta,batch=80,integer=False,objective_scale=1):
        # All score arrays below are integer-scaled by120 when exact pricing.
        dtype=object if integer=='object' else np.int64 if integer else float
        self.crossweights=[(*row,int(w) if integer else float(w)) for row,w in zip(self.cross,lam[557:717]) if abs(w)>1e-11];self.extra_cache={}
        sw=[(*row,int(w) if integer else float(w)) for row,w in zip(self.single,lam[717:]) if abs(w)>1e-11]
        weights=[(n,int(v) if integer else float(v)) for n,v in zip(self.names[:717],lam[:717]) if abs(v)>1e-11]
        fam={t:[] for t in ('AB','AE','Sbranch')}
        for n,v in weights:
            tag=n.split(':')[0]
            if tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam,dtype=dtype)[self.oldids];base=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        cache={};best=[];minimum=None
        for bi,bits in enumerate(self.bits):
            vectors={};keys={};consts={};E=EC[bi].copy();H=HC[bi].copy();p=bits[0]+bits[1]
            for tag in fam:
                key,const,vec,me,mh=self.family_score(bits,tag,fam[tag],integer=integer);k=key[0];keys[tag]=key;consts[tag]=const;E+=me.T;H+=mh.T
                if key not in cache:
                    score=np.zeros(len(self.hist[k]),dtype=dtype)
                    for v,a in vec:score+=v*(a.astype(object) if integer=='object' else a)
                    cache[key]=score
                vectors[tag]=cache[key]
            ownw=sum(w*({'D':1,'O':4,'OO':8}[kind]) for _,target,pos,kind,w in sw)
            AB=vectors['AB']+ownw*(self.M[3,p]['zy'].astype(object) if integer=='object' else self.M[3,p]['zy'])
            for d in range(6):
                fbest=None;fidx=None
                for h0 in range(6-d):
                    for h1 in range(d+1):
                        abids=self.condids[d,h0,h1];iab=int(abids[np.argmax(AB[abids])]);val=AB[iab]+consts['AB'];idx=[iab]
                        for tag,k in (('AE',3),('Sbranch',4)):
                            ck=('cond',keys[tag],p,d,h0,h1)
                            if ck not in cache:
                                score=vectors[tag].copy()
                                for _,target,pos,kind,w in sw:
                                    if target==tag:
                                        a=self.qcost[k,p,d,h0,h1,pos,kind];score+=w*(a.astype(object) if integer=='object' else a)
                                ids=self.ids[k][d];arg=int(ids[np.argmax(score[ids])]);cache[ck]=(score[arg],arg)
                            v,arg=cache[ck];val+=v+consts[tag];idx.append(arg)
                        if fbest is None or val>fbest:fbest=val;fidx=idx
                menus=0;lhs=[]
                for f in range(3):
                    corners=[(0,0),(d,d),(5-d,0),(5,d)];lh=max(corners,key=lambda z:z[0]*E[d,f]+z[1]*H[d,f]);lhs.append(lh);menus+=lh[0]*E[d,f]+lh[1]*H[d,f]
                residual=120*(beta*int(any(bits[:5]))-objective_scale*int(d>0))-base[bi,d]-menus-fbest
                minimum=residual if minimum is None else min(minimum,residual)
                if residual<(0 if integer else -1e-7):best.append((residual,{'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][fidx[0]]),'AE_hist':list(self.hist[3][fidx[1]]),'second_hist':list(self.hist[4][fidx[2]]),'menus_lh':lhs}))
        best.sort(key=lambda z:z[0])
        for residual,atom in best[:batch]:
            rr=self.atom_rows(atom);rho=120*(beta*int(any(map(int,atom['bits'][:5])))-objective_scale*int(any(atom['AB_hist'][4:])))
            rho-=120*sum((int(v)*rr[n] if integer else float(v)*float(rr[n])) for n,v in zip(self.names,lam));assert abs(rho-residual)<F(1,10**6),(rho,residual)
        return minimum,best[:batch],len(cache)

def run(maxiter=100):
    U=TerminalUniverse();src=json.loads((OLD/'cg_cross_pair_final.json').read_text());atoms=[];keys=set();cols=[];w=[];o=[]
    def add(a):
        key=atom_key(a)
        if key in keys:return False
        rr=U.atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key);w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])));return True
    checkpoint=HERE/'cg_terminal_cross.json'
    if checkpoint.exists():src=json.loads(checkpoint.read_text())
    for a in src['atoms']:add(a)
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.asarray(cols).T;out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert out.success,out.message
        beta=-out.fun;lam=-out.ineqlin.marginals;minimum,new,contexts=U.price(lam,beta);count=sum(add(a) for _,a in new);rec={'iteration':it,'columns':len(atoms),'beta':beta,'pricing_minimum_scaled':float(minimum),'new_columns':count,'score_contexts':contexts,'seconds':time.time()-t0};history.append(rec);print(json.dumps(rec),flush=True)
        checkpoint.write_text(json.dumps({'scope':'727-row necessary-condition template; no SPE or true OPT claim','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history},indent=2)+'\n')
        if count==0:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 100)

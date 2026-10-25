"""Original indexed rows plus exact maximal-root envelope projections.

All-state discovery, fixed beta two. Floating status never asserts HALF(5).
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time,hashlib,numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import actual_root_copies as cp
old=cp.old;ROOT=cp.ROOT;LABELS=cp.LABELS;PATHS=cp.PATHS
PAIRS=[(F(80),F(71,5)),(F(89090,1753),F(29147,3506)),(F(50200,1753),F(4851,1753)),(F(678285,23888),F(64639,23888))]
FM={'AB':('AB_hist','XY'),'AE':('AE_hist','XY'),'Sbranch':('second_hist','UVW')}

def satrows(a,exact=True):
    b=list(map(int,a['bits']));r=old.q(b[0],sum(b[:5]));d=sum(a['AB_hist'][4:]);o=int(d>0);rr={}
    for gi,(B,C) in enumerate(PAIRS):
        p=f'Sat{gi}:'
        rr.update({p+'C:'+m:B*r-C*x-o for m,x in zip(LABELS,b)})
        rr[p+'opt']=5*B*r-C*d-5*o
        for fi,pn in enumerate(PATHS):rr[p+'L:'+pn]=5*B*r-C*a['menus_lh'][fi][0]-5*o
        for tag,(hn,ms) in FM.items():
            k=1+len(ms)
            for j,m in enumerate(ms,1):
                count=sum(n*((idx>>(k-1-j))&1) for idx,n in enumerate(a[hn]))
                rr[f'{tag}:Sat:{gi}:{m}']=5*B*r-C*count-5*o
    return rr

class Universe(old.Universe):
    def __init__(self):
        super().__init__(1)
        h3=[5]+[0]*7;h4=[5]+[0]*15
        a={'bits':'0000000000','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(0,0)]*3}
        self.sn=list(satrows(a));self.names+=self.sn
        self.fixedsn=[n for n in self.sn if n.startswith('Sat')];self.sid=[self.names.index(n) for n in self.fixedsn]
        self.ST=np.zeros((1024,6,len(self.fixedsn)))
        for bi,b in enumerate(self.bits):
            r=old.q(b[0],sum(b[:5]))
            for d in range(6):
                for ni,n in enumerate(self.fixedsn):
                    g,kind,*detail=n.split(':');B,C=PAIRS[int(g[3:])]
                    if kind=='C':v=B*r-C*b[LABELS.index(detail[0])]-int(d>0)
                    elif kind=='opt':v=5*B*r-C*d-5*int(d>0)
                    else:v=5*B*r-5*int(d>0)
                    self.ST[bi,d,ni]=120*float(v)
        print(json.dumps({'core_rows':len(self.names),'new_envelope_rows':len(self.sn)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(satrows(a));return rr
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,v) for n,v in weights if ':Sat:' in n];rest=[(n,v) for n,v in weights if ':Sat:' not in n]
        key,const,vec,E,H=super().family_score(bits,tag,rest,integer)
        b=dict(zip(LABELS,bits));r=old.q(b['A'],sum(b[m] for m in 'ABCDE'));k=key[0]
        for n,v in own:
            _,_,gi,m=n.split(':');B,C=PAIRS[int(gi)]
            const+=v*float(5*B*r*120)
            vec.append((-v*float(C*120),self.count[k][m]))
            vec.append((-v*600,(self.d[k]>0).astype(int)))
        return key+(tuple(own),),const,vec,E,H
    def price(self,lam,beta,batch=50,integer=False,objective_scale=1):
        weights=[(n,int(v) if integer else float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
        fam={t:[] for t in ('AB','AE','Sbranch')}
        for n,v in weights:
            tag=n.split(':')[0]
            if tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam,dtype=object if integer=='object' else np.int64 if integer else float)[self.oldids]
        base=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        base+=self.ST@np.asarray(lam)[self.sid]
        cache={};best=[];minimum=1e100
        for bi,bits in enumerate(self.bits):
            fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[]
            for tag in fam:
                key,const,vec,me,mh=self.family_score(bits,tag,fam[tag],integer=integer);k=key[0]
                if key not in cache:
                    score=np.zeros(len(self.hist[k]),dtype=object if integer=='object' else np.int64 if integer else float)
                    for v,a in vec:score+=v*(a.astype(object) if integer=='object' else a)
                    vals=[];idx=[]
                    for ids in self.ids[k]:
                        arg=ids[int(np.argmax(score[ids]))];vals.append(score[arg]);idx.append(int(arg))
                    cache[key]=(np.asarray(vals),idx)
                vals,idx=cache[key];fs.append(vals+const);choices.append(idx);E+=me.T;H+=mh.T
            for fi,pn in enumerate(PATHS):
                E[:,fi]-=sum(float(C*120)*lam[self.names.index(f'Sat{gi}:L:'+pn)] for gi,(B,C) in enumerate(PAIRS))
            for d in range(6):
                corners=[(0,0),(d,d),(5-d,0),(5,d)];lhs=[];menus=0
                for f in range(3):
                    lh=max(corners,key=lambda lh:lh[0]*E[d,f]+lh[1]*H[d,f]);lhs.append(lh);menus+=lh[0]*E[d,f]+lh[1]*H[d,f]
                residual=120*(beta*int(any(bits[:5]))-objective_scale*int(d>0))-base[bi,d]-menus-sum(a[d] for a in fs)
                minimum=min(minimum,residual)
                if residual < (0 if integer else -1e-7):
                    atom={'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][choices[0][d]]),'AE_hist':list(self.hist[3][choices[1][d]]),'second_hist':list(self.hist[4][choices[2][d]]),'menus_lh':lhs}
                    best.append((residual,atom))
        best.sort(key=lambda z:z[0])
        for residual,atom in best[:batch]:
            direct=self.atom_rows(atom)
            rho=120*(beta*int(any(map(int,atom['bits'][:5])))-objective_scale*int(any(atom['AB_hist'][4:])))
            rho-=120*sum((int(v)*direct[n] if integer else float(v)*float(direct[n])) for n,v in zip(self.names,lam))
            assert abs(rho-residual)<(F(1,10**6)),(rho,residual,atom)
        return minimum,best[:batch],len(cache)

def run(maxiter=35):
    U=Universe();target=HERE/'core_envelope_search.json';atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        k=old.atom_key(a)
        if k in keys:return 0
        a={n:a[n] for n in ('bits','AB_hist','AE_hist','second_hist','menus_lh')};rr=U.atom_rows(a)
        atoms.append(a);keys.add(k);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    warm=json.loads((HERE/'penultimate_branch_half_search.json').read_text())
    keep=list(range(0,len(warm['atoms']),max(1,len(warm['atoms'])//500)))+list(range(max(0,len(warm['atoms'])-100),len(warm['atoms'])))
    for i in sorted(set(keep)):add(warm['atoms'][i])
    source={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(old.__file__),HERE/'maxroot_envelope.json']}
    history=[]
    for it in range(maxiter):
        t=time.time();mat=np.asarray(cols).T;scale=np.maximum(1.,np.max(np.abs(mat),axis=1))
        out=linprog(np.ones(len(U.names)),A_ub=(mat/scale[:,None]).T,b_ub=2*np.asarray(ws)-np.asarray(os),bounds=(0,None),method='highs')
        if not out.success:
            result={'status':'restricted-certificate-infeasible','scope':'Floating row-system certificate search only, not a SPE counterexample or exact template theorem','message':out.message,'sources':source,'atoms':atoms,'history':history}
            target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','message']}),flush=True);return
        lam=out.x/scale;minimum,new,contexts=U.price(lam,2,batch=400);n=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'minimum_scaled_residual':minimum,'new_columns':n,'contexts':contexts,'seconds':time.time()-t};history.append(rec);print(json.dumps(rec),flush=True)
        result={'status':'fixed-beta-two-search','scope':'Floating complete-state coefficient search only; no universal welfare bound until exact rational audit','sources':source,'atoms':atoms,'history':history,'multipliers_float':{n:float(x) for n,x in zip(U.names,lam) if x>1e-10}}
        target.write_text(json.dumps(result,indent=2)+'\n')
        if n==0:return
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 35)

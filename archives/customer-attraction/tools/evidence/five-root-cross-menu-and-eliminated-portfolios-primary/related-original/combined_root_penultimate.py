"""Combine genuine optimal-root replies with actual-root and early-D branches.

Fixed beta two, discovery only. Independent histogram domains are a relaxation
of the same original complete SPE. No floating LP status is a game theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,time,hashlib,math,numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import actual_root_copies as copies
import ap_binary_pricing as ap
from weighted_root_saturation_check import PAIRS as WEIGHTED_PAIRS
PAIRS=WEIGHTED_PAIRS+[(F(89090,1753),F(29147,3506)),(F(50200,1753),F(4851,1753)),(F(678285,23888),F(64639,23888))]
old=copies.old;ROOT=copies.ROOT;ROOTS=copies.ROOTS;PATHS=copies.PATHS
LABELS=copies.LABELS;STATES=copies.STATES;TAILS=copies.TAILS;FIRST=copies.FIRST

def saturation_rows(a,exact=True):
    Q=old.EX['q'] if exact else old.VE['q']
    b=list(map(int,a['bits']));r=Q(b[0],sum(b[:5]));d=sum(a['AB_hist'][4:]);o=int(d>0)
    rr={}
    for gi,(B,C) in enumerate(PAIRS):
        tag=f'Saturation{gi}:'
        rr.update({tag+'C:'+lab:B*r-C*v-o for lab,v in zip(LABELS,b)})
        rr[tag+'opt']=5*B*r-C*d-5*o
        for fi,pn in enumerate(PATHS):rr[tag+'L:'+pn]=5*B*r-C*a['menus_lh'][fi][0]-5*o
        for src in ROOTS:
            for j,x in enumerate(a['copies'][src]):rr[tag+f'copy:{src}:{j}']=B*r-C*x-o
        for tag,hn,menus in [('AB','AB_hist','XY'),('AE','AE_hist','XY'),('Sbranch','second_hist','UVW')]:
            k=1+len(menus)
            for j,m in enumerate(menus,1):
                cc=sum(n*((idx>>(k-1-j))&1) for idx,n in enumerate(a[hn]))
                rr[f'{tag}:Sat:{gi}:{m}']=5*B*r-C*cc-5*o
        for j,m in enumerate(ap.RPOS[1:],1):
            cc=sum(n*int(t[j]) for n,t in zip(a['root_hist'],ap.TYPES))
            rr[f'Saturation{gi}:rootmenu:'+m]=5*B*r-C*cc-5*o
    return rr

class Universe(copies.Universe):
    def __init__(self):
        super().__init__()
        self.root_engine=ap.Universe()
        self.root_names=[n for n in self.root_engine.names if n not in self.names]
        self.root_name_set=set(self.root_names)
        self.names+=self.root_names
        fake={'bits':'0000000000','AB_hist':[5,0,0,0,0,0,0,0],'menus_lh':[(0,0)]*3,'copies':{s:[0]*TAILS[s] for s in ROOTS},'root_hist':[5]+[0]*31,'AE_hist':[5]+[0]*7,'second_hist':[5]+[0]*15}
        self.satnames=[n for n in saturation_rows(fake) if n.startswith("Saturation")];self.satfamily=[n for n in saturation_rows(fake) if ":Sat:" in n];self.satids=list(range(len(self.names),len(self.names)+len(self.satnames)))
        self.names+=self.satnames+self.satfamily
        st=np.zeros((1024,6,len(self.satnames)),dtype=float)
        for bi,bits in enumerate(self.bits):
            r=old.q(bits[0],sum(bits[:5]))
            for d in range(6):
                for ni,n in enumerate(self.satnames):
                    group,kind,*detail=n.split(':');B,C=PAIRS[int(group[len('Saturation'):])]
                    if kind=='C':v=B*r-C*bits[LABELS.index(detail[0])]-int(d>0)
                    elif kind=='opt':v=5*B*r-C*d-5*int(d>0)
                    elif kind=='copy':v=B*r-int(d>0)
                    else:v=5*B*r-5*int(d>0)
                    st[bi,d,ni]=120*float(v)
        self.ST=st
        print(json.dumps({'combined_rows':len(self.names),'new_optimal_root_rows':len(self.root_names)}),flush=True)
    def atom_rows(self,a,exact=True):
        rr=super().atom_rows(a,exact)
        bits=tuple(map(int,a['bits']));rh=a['root_hist']
        rr.update(ap.base.root_rows(bits,rh,a['menus_lh'],exact))
        rr.update(ap.aligned.aligned_rows(rh,exact,bits))
        rr.update(ap.root_ap_rows(rh,bits,True) if exact else self.fast_ap_rows(rh,bits))
        rr.update(saturation_rows(a,exact))
        return rr
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
    @staticmethod
    def hist_rank(hist):
        rem=5;rank=0
        for i,h in enumerate(hist[:-1]):
            n=32-i
            for v in range(h):rank+=math.comb(rem-v+n-2,n-2)
            rem-=h
        assert rem==hist[-1]
        return rank
    def fast_ap_rows(self,hist,bits):
        rid=self.hist_rank(hist);b=dict(zip(LABELS,bits));out={}
        for i in (1,2,3):
            aa=ap.alpha2(5-i)
            v=self.root_engine.local[f'APshare:{i}'][rid]/120
            worst=self.root_engine.local[f'APworst:{i}'][rid]/120
            instant=self.root_engine.local[f'APinstant:{i}'][rid]/120
            for c in LABELS:
                for d in LABELS:
                    cv,dv=b[c],b[d]
                    out[f'Root:AProot:{i}:{c}:{d}']=aa*v-((aa-2)*cv+2*cv*dv)*worst-2*dv*(1-cv)*instant
            for c in ap.RPOS:
                for d in ap.RPOS:
                    n=f'Root:APown:{i}:{c}:{d}';out[n]=self.root_engine.local[n][rid]/120
        return out
    def price(self,lam,beta,batch=80):
        weights=[(n,float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
        fam={t:[] for t in ('AB','AE','Sbranch')}
        for n,v in weights:
            tag=n.split(':')[0]
            if tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam)[self.oldids];fixed=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        fixed+=(self.AP@np.asarray(lam)[self.apids])[:,None]
        fixed+=self.ST@np.asarray(lam)[self.satids]
        Cvals={};Cidx={}
        for src in ROOTS:
            ww=np.asarray(lam)[self.cids[src]];ids=np.flatnonzero(np.abs(ww)>1e-11)
            score=np.tensordot(self.CT[src][...,ids],ww[ids],axes=([-1],[0])) if len(ids) else np.zeros((1024,6,len(STATES[src])))
            satq=np.asarray([sum(float(C*120)*lam[self.names.index(f'Saturation{gi}:copy:{src}:{j}')] for gi,(B,C) in enumerate(PAIRS)) for j in range(TAILS[src])])
            if np.any(satq):score-=(np.asarray(STATES[src])@satq)[None,None,:]
            CE=np.zeros((1024,len(STATES[src]),3))
            for i in range(FIRST[src],5):
                for fi,pn in enumerate(PATHS):
                    CE[:,:,fi]-=lam[self.query_indices[src,i,pn]]*self.QD[src,i]
            if np.any(CE):
                joint=score[:,:,:,None]+np.einsum('bsf,dqf->bdsq',CE,self.MenuL,optimize=True)
                Cidx[src]=np.argmax(joint,axis=2);Cvals[src]=np.max(joint,axis=2)
            else:
                Cidx[src]=np.repeat(np.argmax(score,axis=2)[:,:,None],64,axis=2)
                Cvals[src]=np.repeat(np.max(score,axis=2)[:,:,None],64,axis=2)
        rw=[(n,v) for n,v in weights if n in self.root_name_set]
        cache={};rcache={};best=[];minimum=1e100
        for bi,bits in enumerate(self.bits):
            fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[]
            bm=dict(zip(LABELS,bits))
            for fi,(pn,z) in enumerate(PATHS.items()):
                pp=sum(bm[x] for x in z[:3]);ww=float(np.sum(np.asarray(lam)[self.menu_weight_indices[pn]]))
                E[:,fi]-=sum(float(C*120)*lam[self.names.index(f"Saturation{gi}:L:"+pn)] for gi,(B,C) in enumerate(PAIRS))
                E[:,fi]+=ww*int(old.sc(old.q(1,pp+1)))
                H[:,fi]-=ww*int(old.sc(old.q(1,(pp+1)*(pp+2))))
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
            for m in ap.RPOS[1:]:co['count:'+m]-=sum(float(C*120)*lam[self.names.index(f'Saturation{gi}:rootmenu:'+m)] for gi,(B,C) in enumerate(PAIRS))
            rk=tuple(sorted((n,v) for n,v in co.items() if v))
            if rk not in rcache:rcache[rk]=self.root_engine.root_price(co)
            rv,ri=rcache[rk];fs.append(rv+rc);E+=me.T;H+=mh.T
            for d in range(6):
                scores=self.MenuL[d]@E[d]+self.MenuH[d]@H[d]
                for src in ROOTS:scores=scores+Cvals[src][bi,d]
                menu_index=int(np.argmax(scores))
                lhs=[(int(self.MenuL[d,menu_index,f]),int(self.MenuH[d,menu_index,f])) for f in range(3)]
                rho=120*(beta*int(any(bits[:5]))-int(d>0))-fixed[bi,d]-float(scores[menu_index])-sum(v[d] for v in fs)
                minimum=min(minimum,rho)
                if rho < -1e-7:
                    a={'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][choices[0][d]]),'AE_hist':list(self.hist[3][choices[1][d]]),'second_hist':list(self.hist[4][choices[2][d]]),'menus_lh':lhs,'copies':{s:STATES[s][Cidx[s][bi,d,menu_index]] for s in ROOTS}}
                    a['root_hist']=self.root_engine.rh[ri[d]].tolist()
                    best.append((rho,a))
        best.sort(key=lambda x:x[0])
        for rho,a in best[:min(batch,8)]:
            rr=self.atom_rows(a)
            direct=120*(beta*int(any(map(int,a['bits'][:5])))-int(any(a['AB_hist'][4:])))
            direct-=120*sum(float(v)*float(rr[n]) for n,v in zip(self.names,lam))
            assert abs(direct-rho)<1e-6,(direct,rho)
        return minimum,best[:batch],len(cache)+len(rcache)

def key(a):return copies.key(a)+(tuple(a['root_hist']),)
def run(maxiter=50):
    U=Universe();target=HERE/'full_envelope_half_search.json'
    source=HERE/'envelope_half_search.json'
    warm=json.loads((target if target.exists() else source).read_text())
    atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        if key(a) in keys:return 0
        rr=U.atom_rows(a,False);cols.append([float(rr[n]) for n in U.names])
        atoms.append(a);keys.add(key(a));ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
        return 1
    keep=list(range(0,len(warm['atoms']),max(1,len(warm['atoms'])//220)))+list(range(max(0,len(warm['atoms'])-100),len(warm['atoms'])))
    for i in sorted(set(keep)):
        a=warm['atoms'][i]
        if 'root_hist' in a:add(a);continue
        d=sum(a['AB_hist'][4:])
        for mask in (0,15):
            hh=[0]*32;hh[mask]=5-d;hh[16+mask]=d
            add({**a,'root_hist':hh})
    h3=[0]*8;h3[3]=4;h3[7]=1;h4=[0]*16;h4[7]=4;h4[15]=1;rh=[0]*32;rh[15]=4;rh[31]=1
    big={'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'root_hist':rh,'menus_lh':[(5,1)]*3,'copies':{s:(1,)*TAILS[s] for s in ROOTS}}
    h3=[0]*8;h3[0]=4;h3[4]=1;h4=[0]*16;h4[0]=4;h4[8]=1;rh=[0]*32;rh[0]=4;rh[16]=1
    omit={'bits':'0000000000','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'root_hist':rh,'menus_lh':[(0,0)]*3,'copies':{s:(0,)*TAILS[s] for s in ROOTS}}
    rb=U.atom_rows(big);ro=U.atom_rows(omit)
    assert all(rb[n]+F(4,5)*ro[n]>=0 for n in U.names),[(n,rb[n]+F(4,5)*ro[n]) for n in U.names if rb[n]+F(4,5)*ro[n]<0][:5]
    add(big);add(omit)
    for a in atoms[::max(1,len(atoms)//10)]+atoms[-2:]:
        x=U.atom_rows(a);y=U.atom_rows(a,False)
        assert max(abs(float(x[n])-float(y[n])) for n in U.names)<1e-8
    for rid in [0,1,15,200,len(U.root_engine.rh)-1]:assert U.hist_rank(U.root_engine.rh[rid])==rid
    print(json.dumps({'initial_columns':len(atoms),'exact_fast_rows':'passed'}),flush=True)
    provenance={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(copies.__file__),Path(ap.__file__),HERE/'_aligned_rows_safe.py',Path(ap.aligned.__file__),Path(ap.base.__file__),Path(old.__file__),ROOT/'research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/root_saturation.md',HERE/'weighted_root_saturation.md',HERE/'weighted_root_saturation_check.py',HERE/'maxroot_envelope.py',HERE/'maxroot_envelope.json',HERE/'audit_maxroot_envelope.py']}
    history=[]
    for it in range(maxiter):
        t=time.time();mat=np.asarray(cols).T;scale=np.maximum(1.,np.max(np.abs(mat),axis=1))
        out=linprog(np.ones(len(U.names)),A_ub=(mat/scale[:,None]).T,b_ub=2*np.asarray(ws)-np.asarray(os),bounds=(0,None),method='highs')
        if not out.success:
            report={'scope':'Floating restricted necessary-row certificate search only; not a SPE counterexample or a proof of template impossibility','status':'restricted-certificate-infeasible','message':out.message,'sources':provenance,'atoms':atoms,'history':history}
            target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['atoms','history']}),flush=True);return
        lam=out.x/scale;minimum,new,contexts=U.price(lam,2.,batch=400);n=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'beta':2.,'minimum_scaled_residual':minimum,'new_columns':n,'contexts':contexts,'seconds':time.time()-t};history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Floating all-type coefficient discovery, not a universal bound or SPE instance','status':'fixed-beta-two-search','sources':provenance,'atoms':atoms,'history':history,'dual_multipliers_float':{name:float(v) for name,v in zip(U.names,lam) if v>1e-10}}
        target.write_text(json.dumps(report,indent=2)+'\n')
        if n==0:return
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 50)

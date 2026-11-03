"""HALF(5): genuine root copies and early deviations to penultimate D.

All-state column generation, no finite catalog scan. Discovery only until
rational multipliers and exact complete coefficient pricing are verified.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import sys,json,time,hashlib,numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
BASE=ROOT/'research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing'
sys.path.insert(0,str(BASE))
import full_pricing as old
sys.path.insert(0,str(HERE))
from ap_binary_pricing import fixed_rows
LABELS,PATHS,START=old.LABELS,old.PATHS,old.START
SPECS={**{s:('',s) for s in 'BCDE'},'D2':('A','D'),'D3':('AB','D')}
ROOTS=tuple(SPECS);TAILS={s:4-len(pre) for s,(pre,_) in SPECS.items()}
STATES={s:list(product((0,1),repeat=TAILS[s])) for s in ROOTS}
NEWLABELS={s:'fghi'[:TAILS[s]] for s in ROOTS}
FIRST={s:1+len(pre) for s,(pre,_) in SPECS.items()}

def copy_rows(bits,dd,cb,source,exact=True,lhs=None):
    Q=old.EX['q'] if exact else old.VE['q']
    b=dict(zip(LABELS,bits));pre,forced=SPECS[source];start=FIRST[source]
    assert len(cb)==TAILS[source]
    path=tuple(b[x] for x in pre)+(b[forced],*cb);p=path[0];total=sum(path)
    u=[Q(x,total) for x in path];act=PATHS['actual'];actload=sum(b[x] for x in act)
    out={'forced-IC':Q(b[act[start-1]],actload)-u[start-1]}
    labels={**b,**dict(zip('fghi',cb))}
    for i in range(start,5):
        pref=sum(path[:i]);k=5-i
        for lab,x in labels.items():out[f'{i}:K:{lab}']=u[i]-Q(x,pref+k)
        out[f'{i}:opt']=5*u[i]-Q(dd,pref+k)
    # Every old genuine node can query each new reply theme.
    for pn,z in PATHS.items():
        for i in range(START[pn],5):
            pref=sum(b[x] for x in z[:i]);v=Q(b[z[i]],sum(b[x] for x in z))
            for lab,x in zip('fghi',cb):out[f'old:{pn}:{i}:{lab}']=v-Q(x,pref+5-i)
    pref=sum(path[:3]);H=u[3]+u[4]+Q(path[3],(pref+1)*(pref+2))
    o=int(dd>0) if exact else np.asarray(dd>0,dtype=int)
    out['r2:O']=F(5,2)*H+Q(pref,pref+1)-o if exact else 2.5*H+Q(pref,pref+1)-o
    out['r2:opt']=10*H-Q(dd*(5-dd),pref+1)-Q(dd*(dd-1),pref+2)
    for l,m in combinations_with_replacement(labels,2):
        x,y=labels[l],labels[m]
        out[f'r2:pair:{l}:{m}']=H-Q(x+y-2*x*y,pref+1)-Q(2*x*y,pref+2)
    def g3(bg,d):return Q(d*(5-d)*(4-d),2*(bg+1))+Q(d*(d-1)*(5-d),bg+2)+Q(d*(d-1)*(d-2),2*(bg+3))
    def g4(bg,d):return Q(d*(d-1),bg+d-1)+Q((5-d)*d,bg+d)
    V3=sum(u[2:]);V4=sum(u[1:]);Vin=p-u[0]
    for name,d in [('opt',dd),*[(n,sum(b[x] for x in z)) for n,z in PATHS.items()]]:
        if start<=2:out['r3:'+name]=50*V3-3*g3(path[0]+path[1],d)
        if start<=1:
            out['r4:'+name]=7495*V4-750*g4(p,d)
            out['r4binary:'+name]=29985*V4-4985*Vin-3000*g4(p,d)
    # Cross-history money: the old genuine last menus can query each new
    # reply, and the old genuine two-tail nodes can query all mixed pairs.
    for fi,(pn,z) in enumerate(PATHS.items()):
        pp=sum(b[x] for x in z[:3]);DP=(pp+1)*(pp+2)
        HH=Q(b[z[3]]+b[z[4]],sum(b[x] for x in z))+Q(b[z[3]],DP)
        ell,match=(lhs[fi] if lhs is not None else (0,0))
        for lab,x in zip('fghi',cb):
            out[f'lastmenu:{pn}:{lab}']=Q(ell-5*x,pp+1)+Q(dd*x-match,DP)
            for oldlabel,y in b.items():
                out[f'oldpair:{pn}:{lab}:{oldlabel}']=HH-Q(x+y-2*x*y,pp+1)-Q(2*x*y,pp+2)
        for li,mi in combinations_with_replacement(range(len(cb)),2):
            x,y=cb[li],cb[mi]
            out[f'oldpairnew:{pn}:{li}:{mi}']=HH-Q(x+y-2*x*y,pp+1)-Q(2*x*y,pp+2)
    # Converse direction: each new genuine node queries every old L menu.
    for ii in range(start,5):
        prefnew=sum(path[:ii]);knew=5-ii
        for fi,pn in enumerate(PATHS):
            ell=lhs[fi][0] if lhs is not None else 0
            out[f'queryL:{ii}:{pn}']=5*u[ii]-Q(ell,prefnew+knew)
    return out

class Universe(old.Universe):
    def __init__(self):
        super().__init__(1)
        self.apnames=list(fixed_rows([0]*10));self.names+=self.apnames
        self.AP=np.array([[int(old.sc(v)) for v in fixed_rows(b).values()] for b in self.bits],dtype=np.int64)
        bb=np.array(self.bits,dtype=np.int8);bits=[bb[:,i,None,None] for i in range(10)]
        ds=np.arange(6)[None,:,None]
        self.CT={};self.cnames={};self.cids={}
        for src in ROOTS:
            cc=np.array(STATES[src],dtype=np.int8);cb=[cc[None,None,:,i] for i in range(TAILS[src])]
            rr=copy_rows(bits,ds,cb,src,False);self.cnames[src]=list(rr)
            self.CT[src]=np.stack([old.sc(np.broadcast_to(v,(1024,6,len(STATES[src])))) for v in rr.values()],axis=-1).astype(np.int32)
            self.cids[src]=list(range(len(self.names),len(self.names)+len(rr)))
            self.names += [f'Copy{src}:{n}' for n in self.cnames[src]]
        self.apids=[self.names.index(n) for n in self.apnames]
        self.menu_weight_indices={pn:[self.names.index(f'Copy{src}:lastmenu:{pn}:{lab}') for src in ROOTS for lab in NEWLABELS[src]] for pn in PATHS}
        self.query_indices={(src,i,pn):self.names.index(f'Copy{src}:queryL:{i}:{pn}') for src in ROOTS for i in range(FIRST[src],5) for pn in PATHS}
        self.QD={}
        for src in ROOTS:
            pre,forced=SPECS[src];fixed=pre+forced
            pp=sum(bb[:,LABELS.index(x),None] for x in fixed)
            cc=np.array(STATES[src],dtype=np.int8)
            for i in range(FIRST[src],5):
                den=pp+cc[None,:,:i-FIRST[src]].sum(axis=2)+(5-i)
                self.QD[src,i]=old.sc(old.VE['q'](1,den))
        self.MenuL=[];self.MenuH=[]
        for d in range(6):
            corners=[(0,0),(d,d),(5-d,0),(5,d)]
            menus=list(product(corners,repeat=3))
            self.MenuL.append([[z[0] for z in mm] for mm in menus]);self.MenuH.append([[z[1] for z in mm] for mm in menus])
        self.MenuL=np.asarray(self.MenuL);self.MenuH=np.asarray(self.MenuH)
        print(json.dumps({'continuation_rows':{s:len(v) for s,v in self.cnames.items()},'total_rows':len(self.names),'shared_menu_vertices':64}),flush=True)
    def atom_rows(self,a,exact=True):
        bits=tuple(map(int,a['bits']));d=sum(a['AB_hist'][4:])
        if exact:rr=super().atom_rows(a)
        else:
            rr=old.VE['evaluate'](bits,[a['AB_hist'],a['AE_hist'],a['second_hist']],a['menus_lh'],True)
            rr.update(old.terminal_rows(a));rr.update(old.pair_rows(a,overlap=1))
        rr.update(fixed_rows(bits,exact))
        for src in ROOTS:rr.update({f'Copy{src}:{n}':v for n,v in copy_rows(bits,d,a['copies'][src],src,exact,a['menus_lh']).items()})
        return rr
    def price(self,lam,beta,batch=80):
        weights=[(n,float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
        fam={t:[] for t in ('AB','AE','Sbranch')}
        for n,v in weights:
            tag=n.split(':')[0]
            if tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam)[self.oldids];fixed=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        fixed+=(self.AP@np.asarray(lam)[self.apids])[:,None]
        Cvals={};Cidx={}
        for src in ROOTS:
            ww=np.asarray(lam)[self.cids[src]];ids=np.flatnonzero(np.abs(ww)>1e-11)
            score=np.tensordot(self.CT[src][...,ids],ww[ids],axes=([-1],[0])) if len(ids) else np.zeros((1024,6,len(STATES[src])))
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
        cache={};best=[];minimum=1e100
        for bi,bits in enumerate(self.bits):
            fs=[];E=EC[bi].copy();H=HC[bi].copy();choices=[]
            bm=dict(zip(LABELS,bits))
            for fi,(pn,z) in enumerate(PATHS.items()):
                pp=sum(bm[x] for x in z[:3]);ww=float(np.sum(np.asarray(lam)[self.menu_weight_indices[pn]]))
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
            for d in range(6):
                scores=self.MenuL[d]@E[d]+self.MenuH[d]@H[d]
                for src in ROOTS:scores=scores+Cvals[src][bi,d]
                menu_index=int(np.argmax(scores))
                lhs=[(int(self.MenuL[d,menu_index,f]),int(self.MenuH[d,menu_index,f])) for f in range(3)]
                rho=120*(beta*int(any(bits[:5]))-int(d>0))-fixed[bi,d]-float(scores[menu_index])-sum(v[d] for v in fs)
                minimum=min(minimum,rho)
                if rho < -1e-7:
                    a={'bits':''.join(map(str,bits)),'AB_hist':list(self.hist[3][choices[0][d]]),'AE_hist':list(self.hist[3][choices[1][d]]),'second_hist':list(self.hist[4][choices[2][d]]),'menus_lh':lhs,'copies':{s:STATES[s][Cidx[s][bi,d,menu_index]] for s in ROOTS}}
                    best.append((rho,a))
        best.sort(key=lambda x:x[0])
        for rho,a in best[:batch]:
            rr=self.atom_rows(a)
            direct=120*(beta*int(any(map(int,a['bits'][:5])))-int(any(a['AB_hist'][4:])))
            direct-=120*sum(float(v)*float(rr[n]) for n,v in zip(self.names,lam))
            assert abs(direct-rho)<1e-6,(direct,rho)
        return minimum,best[:batch],len(cache)

def key(a):return old.atom_key(a)+tuple(tuple(a['copies'][s]) for s in ROOTS)

def run(maxiter=60):
    U=Universe();target=HERE/'penultimate_branch_half_search.json'
    source=HERE/'bidirectional_menu_half_search.json';warm=json.loads((target if target.exists() else source).read_text())
    atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        if key(a) in keys:return 0
        rr=U.atom_rows(a,False);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key(a))
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    if 'primal_float' in warm:
        keep=[i for i,v in enumerate(warm['primal_float']) if v>1e-9]
    else:
        keep=list(range(0,len(warm['atoms']),max(1,len(warm['atoms'])//1000)))
    keep+=list(range(max(0,len(warm['atoms'])-200),len(warm['atoms'])))
    for i in sorted(set(keep)):
        a=warm['atoms'][i]
        if 'copies' in a and all(s in a['copies'] for s in ROOTS):add(a);continue
        for bit in (0,1):
            add({**a,'copies':{s:a.get('copies',{}).get(s,(bit,)*TAILS[s]) for s in ROOTS}})
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,d)]*3,'copies':{s:(1,)*TAILS[s] for s in ROOTS}})
    # Genuine all-big five-player SPE gives W=5, OPT=9. Its two full
    # customer states seed ratio 9/5 rather than a degenerate ratio-one start.
    h3=[0]*8;h3[3]=4;h3[7]=1;h4=[0]*16;h4[7]=4;h4[15]=1
    big={'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,1)]*3,'copies':{ss:(1,)*TAILS[ss] for ss in ROOTS}}
    h3o=[0]*8;h3o[0]=4;h3o[4]=1;h4o=[0]*16;h4o[0]=4;h4o[8]=1
    omitted={'bits':'0000000000','AB_hist':h3o,'AE_hist':h3o,'second_hist':h4o,'menus_lh':[(0,0)]*3,'copies':{ss:(0,)*TAILS[ss] for ss in ROOTS}}
    rb=U.atom_rows(big);ro=U.atom_rows(omitted)
    assert all(rb[n]+F(4,5)*ro[n]>=0 for n in U.names)
    add(big);add(omitted)
    for a in atoms[::max(1,len(atoms)//8)]+atoms[-2:]:
        x=U.atom_rows(a);y=U.atom_rows(a,False)
        assert max(abs(float(x[n])-float(y[n])) for n in U.names)<1e-9
    print(json.dumps({'initial_columns':len(atoms),'exact_fast_rows':'passed'}),flush=True)
    provenance={str(pp.relative_to(ROOT)):hashlib.sha256(pp.read_bytes()).hexdigest() for pp in [Path(__file__),Path(old.__file__),HERE/'ap_binary_pricing.py',ROOT/'tests/audits/customer_attraction_five_indexed.py']}
    history=[]
    for it in range(maxiter):
        t=time.time();mat=np.asarray(cols).T
        scale=np.maximum(1.,np.max(np.abs(mat),axis=1))
        rhs=2*np.asarray(ws,float)-np.asarray(os,float)
        out=linprog(np.ones(len(U.names)),A_ub=(mat/scale[:,None]).T,b_ub=rhs,bounds=(0,None),method='highs')
        if not out.success:
            report={'scope':'Fixed beta=2 certificate search on this row system only; infeasibility is not a game counterexample','status':'restricted-certificate-infeasible','sources':provenance,'message':out.message,'atoms':atoms,'history':history}
            target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['atoms','history']}),flush=True);return U,out,atoms
        beta=2.;lam=out.x/scale;minimum,new,contexts=U.price(lam,beta,batch=400);n=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'beta':beta,'minimum_scaled_residual':minimum,'new_columns':n,'contexts':contexts,'seconds':time.time()-t};history.append(rec);print(json.dumps(rec),flush=True)
        result={'scope':'Floating necessary-condition discovery only, not a universal bound or SPE instance','target':'HALF(5)','sources':provenance,'row_names':U.names,'atoms':atoms,'warm_column_flags':[1]*len(atoms),'status':'fixed-beta-two-search','dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history}
        target.write_text(json.dumps(result,indent=2)+'\n')
        if n==0:break
    return U,out,atoms
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 60)

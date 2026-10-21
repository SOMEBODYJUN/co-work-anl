"""Full histogram column generation; exact certificate recovery is separate.

All new output stays here. This program never claims an SPE counterexample.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product, combinations_with_replacement
from collections import defaultdict
import ast, json, sys, time
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ACTOR=HERE.parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').exists())
sys.path[:0]=[str(ACTOR/'round3_closure'),str(ACTOR/'continuation_completion')]
from partition_pair_closure import rows as pair_rows
from offdiagonal_closure import rows as terminal_rows

LABELS='ABCDEUVWXY';PATHS={'actual':'ABCDE','second':'AEUVW','third':'ABEXY'};START={'actual':0,'second':2,'third':3};SCALE=120

def load_eval(vector=False):
    fn=ROOT/'tests/audits/customer_attraction_five_indexed.py'
    s=fn.read_text().split('\nfrom pathlib import Path')[0]
    if vector:s=s.replace('opt=int(d>0)','opt=np.asarray(d>0,dtype=int)')
    ns={'np':np};exec(compile(s,str(fn),'exec'),ns)
    if vector:
        ns['F']=lambda x=0,y=1:x/y
        def q(n,v):
            n,v=np.broadcast_arrays(n,v)
            return np.divide(n,v,out=np.zeros(n.shape,dtype=float),where=n!=0)
        ns['q']=q
    return ns
EX=load_eval();VE=load_eval(True)

def compositions(n,k):
    if k==1:yield(n,);return
    for j in range(n+1):
        for h in compositions(n-j,k-1):yield(j,)+h

def sc(x):
    z=np.asarray(x,dtype=float)*120
    assert np.max(np.abs(z-np.rint(z)))<1e-7
    return np.rint(z).astype(np.int64)

def q(n,d):return F(n,d) if n else F(0)

class Universe:
    def __init__(self,overlap=1):
        t0=time.time();self.overlap=overlap
        self.hist={3:list(compositions(5,8)),4:list(compositions(5,16))}
        self.H={k:np.asarray(v,dtype=np.int64) for k,v in self.hist.items()}
        self.ty={k:np.asarray(list(product((0,1),repeat=k)),dtype=np.int64) for k in (3,4)}
        self.d={k:self.H[k]@self.ty[k][:,0] for k in (3,4)}
        self.ids={k:[np.where(self.d[k]==d)[0] for d in range(6)] for k in (3,4)}
        self.count={k:{m:self.H[k]@self.ty[k][:,i] for i,m in enumerate('XY' if k==3 else 'UVW',1)} for k in (3,4)}
        self.M={}
        for k in (3,4):
            hh=self.H[k];tt=self.ty[k]
            for p in range(3 if k==3 else 2):
                # The existing independent audit's vectorizable equations give
                # every local family row. Fixed-topic constants are removed.
                bits=[0]*10;bits[0]=int(p>0)
                if p==2:bits[1]=1
                if k==3:
                    raw=VE['third_rows'](bits,hh.T,[(0,0)]*3,'AB')
                    out={n[3:]:sc(v) for n,v in raw.items() if n.startswith('AB:')}
                    # F3 contains a fixed-path constant 5*share(path,2).
                    out['F3']=-(hh@sc([q(t[0],p+sum(t)) for t in tt]))
                    localnames=['zt','zx','zy','dx','dy','D1','D2','H','taxp','ctlast','cxlast','cyfourth']
                    def vals(t):
                        a,x,y=map(int,t);load=p+a+x+y
                        return [q(a,load),q(x,load),q(y,load),q(1,p+a+2),q(1,p+a+x+1),q(1,p+a+1),q(1,p+a+2),q(x+y,load)+q(x,(p+a+1)*(p+a+2)),q(p+a,p+a+1),q(a,p+a+x+1),q(x,p+a+x+1),q(y,p+a+2)]
                else:
                    raw=VE['second_rows'](bits,hh.T)
                    out={n[8:]:sc(v) for n,v in raw.items() if n.startswith('Sbranch:')}
                    out['F2']=-(hh@sc([q(t[0],p+sum(t)) for t in tt]))
                    localnames=['zt','zu','zv','zw','du','dv','dw','H','D1','D2','taxp','ctlast','culast','cvlast','cufourth','cwforth','cfv','cfw']
                    def vals(t):
                        a,u,v,w=map(int,t);load=p+a+u+v+w
                        return [q(a,load),q(u,load),q(v,load),q(w,load),q(1,p+a+3),q(1,p+a+u+2),q(1,p+a+u+v+1),q(v+w,load)+q(v,(p+a+u+1)*(p+a+u+2)),q(1,p+a+u+1),q(1,p+a+u+2),q(p+a+u,p+a+u+1),q(a,p+a+u+v+1),q(u,p+a+u+v+1),q(v,p+a+u+v+1),q(u,p+a+u+2),q(w,p+a+u+2),q(v,p+a+3),q(w,p+a+3)]
                arr=np.asarray([sc(vals(t)) for t in tt])
                out.update({n:hh@arr[:,j] for j,n in enumerate(localnames)})
                prefix=p+tt[:,:-2].sum(1);D1=hh@sc([q(1,int(v)+1) for v in prefix]);DG=hh@sc([q(1,(int(v)+1)*(int(v)+2)) for v in prefix]);H=out['H']
                for u,v in combinations_with_replacement(range(k),2):
                    B=hh@tt[:,u];C=hh@tt[:,v];K=hh@(tt[:,u]*tt[:,v])
                    bu=hh@sc([q(int(t[u]),int(z)+1) for t,z in zip(tt,prefix)]);cv=hh@sc([q(int(t[v]),int(z)+1) for t,z in zip(tt,prefix)])
                    bg=hh@sc([q(int(t[u]),(int(z)+1)*(int(z)+2)) for t,z in zip(tt,prefix)]);cg=hh@sc([q(int(t[v]),(int(z)+1)*(int(z)+2)) for t,z in zip(tt,prefix)]);bcg=hh@sc([q(int(t[u]*t[v]),(int(z)+1)*(int(z)+2)) for t,z in zip(tt,prefix)])
                    for name,value in {
                        'all_equal':H-bu-cv+overlap*bcg,
                        'query_equal':4*H-(B+C)*D1+bu+cv+overlap*(K*DG-bcg),
                        'first_branch':4*H-4*bu-C*D1+cv+overlap*(C*bg-bcg),
                        'second_branch':4*H-B*D1+bu-4*cv+overlap*(B*cg-bcg),
                        'all_distinct':12*H-3*((B+C)*D1-bu-cv)+overlap*((B*C-K)*DG-B*cg-C*bg+2*bcg)
                    }.items():out[f'pair:{u}{v}:{name}']=value
                lastden=hh@sc([q(1,int(p+sum(t[:-1]))+1) for t in tt]);lastshare=out['zy' if k==3 else 'zw']
                for pos in range(k):
                    B=hh@tt[:,pos];own=hh@sc([q(int(t[pos]),int(p+sum(t[:-1]))+1) for t in tt])
                    out[f'5:offdiag:{pos}']=4*lastshare-B*lastden+own
                self.M[k,p]=out
        src=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
        self.oldnames=list(EX['old_rows']((0,)*10,0,[(0,0)]*3))
        self.names=src['rows']+list(terminal_rows(src['atoms'][0]))+list(pair_rows(src['atoms'][0],overlap=overlap))
        self.oldids=[self.names.index(n) for n in self.oldnames]
        self.bits=list(product((0,1),repeat=10))
        self.base=np.zeros((1024,6,len(self.oldnames)),dtype=np.int64)
        self.ec=np.zeros((1024,6,3,len(self.oldnames)),dtype=np.int64);self.hc=self.ec.copy()
        ds=np.arange(6)
        for bi,bits in enumerate(self.bits):
            zero=VE['old_rows'](bits,ds,[(0,0)]*3)
            for j,n in enumerate(self.oldnames):self.base[bi,:,j]=sc(zero[n])
            for f in range(3):
                el=[(0,0)]*3;el[f]=(1,0);er=VE['old_rows'](bits,ds,el)
                hl=[(0,0)]*3;hl[f]=(0,1);hr=VE['old_rows'](bits,ds,hl)
                for j,n in enumerate(self.oldnames):self.ec[bi,:,f,j]=sc(er[n]-zero[n]);self.hc[bi,:,f,j]=sc(hr[n]-zero[n])
        print(json.dumps({'initialized_seconds':time.time()-t0,'rows':len(self.names),'histograms':{k:len(v) for k,v in self.hist.items()}}),flush=True)

    def atom_rows(self,atom):
        bits=tuple(map(int,atom['bits']))
        out=EX['evaluate'](bits,[atom['AB_hist'],atom['AE_hist'],atom['second_hist']],atom['menus_lh'],True)
        out.update(terminal_rows(atom));out.update(pair_rows(atom,overlap=self.overlap))
        return out

    def family_score(self,bits,tag,weights,integer=False):
        b=dict(zip(LABELS,bits));k=4 if tag=='Sbranch' else 3;p=b['A']+(b['B'] if tag=='AB' else b['E'] if tag=='AE' else 0)
        M=self.M[k,p];cnt=self.count[k];ds=self.d[k];co=defaultdict(int if integer else float);const=0
        menuE=np.zeros((3,6),dtype=object if integer=='object' else np.int64 if integer else float);menuH=menuE.copy()
        def share(path,i):return q(b[path[i]],sum(b[t] for t in path))
        for n,v in weights:
            sp=n.split(':')
            if n.startswith(tag+':'):sp=sp[1:]
            if sp[0] in ('F2','F3'):
                path=PATHS['actual' if tag!='AE' else 'second'];i=1 if k==4 else 2
                const+=v*int(sc(5*share(path,i)));co['zt']-=v
            elif sp[0] in ('3','4','5'):
                i=int(sp[0]);sh={3:'zu',4:'zv',5:'zw'}[i] if k==4 else {4:'zx',5:'zy'}[i];den={3:'du',4:'dv',5:'dw'}[i] if k==4 else {4:'dx',5:'dy'}[i]
                if sp[1]=='K':co[sh]+=v;co[den]-=v*b[sp[2]]
                else:co[':'.join(sp)]+=v
            elif sp[0] in ('r2','pair'):co[':'.join(sp)]+=v
            else:
                pn=sp[0];path=PATHS[pn]
                if sp[1]=='reply':
                    menu=sp[2].removeprefix('all-');pp=sum(b[t] for t in path[:3]);Dp=(pp+1)*(pp+2);f=list(PATHS).index(pn)
                    menuE[f,:]+=v*int(sc(q(5,pp+1)));menuH[f,:]-=v*int(sc(q(5,Dp)))
                    co['allreply-'+menu+'-'+str(pp)]+=v
                elif sp[1]=='r2':
                    pp=sum(b[t] for t in path[:3]);Dp=(pp+1)*(pp+2);hold=share(path,3)+share(path,4)+q(b[path[3]],Dp)
                    const+=v*int(sc(25*hold));co['oldtax-'+sp[2].removeprefix('menu-')+'-'+str(pp)]+=v
                else:
                    i=int(sp[1])-1;prefix=sum(b[t] for t in path[:i]);menu=sp[2].removeprefix('sum-').removeprefix('S')
                    const+=v*int(sc(5*share(path,i)));co['count-'+menu]-=v*int(sc(q(1,prefix+5-i)))
        vectors=[]
        for feature,v in co.items():
            if not v:continue
            if feature.startswith('count-'):a=120*cnt[feature[6:]] # coefficients in co already scaled: correct below
            elif feature.startswith('allreply-'):
                _,menu,pn=feature.split('-');pp=int(pn);Dp=(pp+1)*(pp+2);c=cnt[menu]
                a=-int(sc(q(5,pp+1)))*c+int(sc(q(1,Dp)))*ds*c
            elif feature.startswith('oldtax-'):
                _,mn,pn=feature.split('-');pp=int(pn);x=cnt[mn[0]];y=cnt[mn[1]]
                a=-int(sc(q(1,pp+1)))*(x*(5-y)+(5-x)*y)-int(sc(q(2,pp+2)))*x*y
            else:a=M[feature]
            if feature.startswith('count-'):a=cnt[feature[6:]]
            vectors.append((v,a))
        key=(k,p,tuple(sorted((f,v) for f,v in co.items() if v)))
        return key,const,vectors,menuE,menuH

    def price(self,lam,beta,batch=50,integer=False,objective_scale=1):
        weights=[(n,int(v) if integer else float(v)) for n,v in zip(self.names,lam) if abs(v)>1e-11]
        fam={t:[] for t in ('AB','AE','Sbranch')}
        for n,v in weights:
            tag=n.split(':')[0]
            if tag in fam:fam[tag].append((n,v))
            elif ':sum-S' in n:fam['Sbranch'].append((n,v))
        ow=np.asarray(lam,dtype=object if integer=='object' else np.int64 if integer else float)[self.oldids]
        base=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
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


def atom_key(a):return (a['bits'],tuple(a['AB_hist']),tuple(a['AE_hist']),tuple(a['second_hist']),tuple(tuple(v) for v in a['menus_lh']))

def run(overlap=1,maxiter=100):
    U=Universe(overlap);src=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
    atoms=[];keys=set();cols=[];ws=[];os=[]
    def add(a):
        key=atom_key(a)
        if key in keys:return False
        rr=U.atom_rows(a);col=[float(rr[n]) for n in U.names]
        atoms.append({k:a[k] for k in ('bits','AB_hist','AE_hist','second_hist','menus_lh')});keys.add(key);cols.append(col)
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
        return True
    for a in src['atoms']:add(a)
    # Feasible anchor: five identical universal topics plus five identical
    # comparison topics and constant identical continuations.
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,d)]*3})
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.asarray(cols).T
        out=linprog(-np.asarray(os,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
        if not out.success:raise RuntimeError(out.message)
        beta=float(-out.fun);lam=-out.ineqlin.marginals
        minimum,new,ncache=U.price(lam,beta,batch=80)
        count=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'beta':beta,'pricing_minimum_scaled':minimum,'new_columns':count,'score_contexts':ncache,'seconds':time.time()-t0}
        history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Full histogram necessary-condition relaxation; no SPE or actual OPT claim','overlap':overlap,'row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history}
        (HERE/f'cg_overlap{overlap}.json').write_text(json.dumps(report,indent=2)+'\n')
        if count==0:break
    return U,out,atoms

if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 1,int(sys.argv[2]) if len(sys.argv)>2 else 100)

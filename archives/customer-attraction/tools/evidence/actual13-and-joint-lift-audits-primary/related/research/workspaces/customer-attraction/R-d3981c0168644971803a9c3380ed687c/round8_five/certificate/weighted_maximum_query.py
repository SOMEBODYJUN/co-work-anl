"""Shared weighted-maximum query at the maximum branch's third player.

H maximizes sum_H 1/(p+3) at the exact original history (M,z2).
Its single extra membership bit is shared by all old indexed menu queries.
This is a new selected legal theme, not a multiplier change to fixed AP.
"""
from pathlib import Path
from fractions import Fraction as F
import json, hashlib, sys
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix
import max_indexed_coupling as cm

HERE=Path(__file__).resolve().parent
FIXED=list(cm.mp.LABELS)+[f'z{j}' for j in range(5)]+['opt']
NODES=cm.mp.NODES+[(pn,4) for pn in cm.mp.PATHS]


def rows(a,mb,h):
    b=dict(zip(cm.mp.LABELS,map(int,a['bits'])));d=sum(a['AB_hist'][4:])
    p=sum(mb[:2]);k=3;u=cm.lm.q(mb[2],sum(mb));K=cm.lm.q(h,p+k)
    out={'wmax:legal-size':F(mb[0]-h),'wmax:current-floor':u-K}
    def fixed(t):
        if t=='opt':return d,5
        if t.startswith('z'):return mb[int(t[1:])],1
        return b[t],1
    for t in FIXED:
        q,n=fixed(t)
        out[f'wmax:cap:{t}']=n*K-cm.lm.q(q,p+k)
        # Exact weighted-maximum BNS, (k-1)(5-1)=8.
        out[f'wmax:BNS:{t}']=8*n*u-7*n*K-cm.lm.q(h*q,p+k)-cm.lm.q((1-h)*q,p+1)
    load=sum(b[t] for t in 'ABCDE');root=cm.lm.q(b['A'],load)
    out['wmax:global-root-BNS']=80*root-15*mb[0]-(5-4*mb[0])*h
    for pn,i in NODES:
        path=cm.mp.PATHS[pn];oldp=sum(b[t] for t in path[:i]);oldu=cm.lm.q(b[path[i]],sum(b[t] for t in path))
        out[f'wmax:oldK:{pn}:{i}']=oldu-cm.lm.q(h,oldp+5-i)
    for i in range(1,5):
        out[f'wmax:maxK:{i}']=cm.lm.q(mb[i],sum(mb))-cm.lm.q(h,sum(mb[:i])+5-i)
    for tag,menus in cm.mp.MENUS.items():
        cc=cm.counts(a,tag)
        for t in menus:
            q=cc[t]
            out[f'{tag}:wmax:cap:{t}']=5*K-cm.lm.q(q,p+k)
            out[f'{tag}:wmax:BNS:{t}']=40*u-35*K-cm.lm.q(h*q,p+k)-cm.lm.q((1-h)*q,p+1)
    return out


class Universe(cm.Universe):
    """The complete 64-state maximum-path/H block and three old families."""
    def __init__(self):
        super().__init__()
        dummy={'bits':'0'*10,'AB_hist':[5]+[0]*7,'AE_hist':[5]+[0]*7,'second_hist':[5]+[0]*15}
        self.wnames=list(rows(dummy,(0,)*5,0));self.names+=self.wnames
        self.active_H=None
        print(json.dumps({'shared_weighted_maximum_rows':len(self.wnames),'total_rows':len(self.names)}),flush=True)

    def atom_rows(self,a):
        rr=super().atom_rows(a)
        if 'H_bit' not in a:
            assert self.active_H is not None
            a['H_bit']=self.active_H
        rr.update(rows(a,tuple(map(int,a['max_bits'])),a['H_bit']))
        return rr

    def block_weighted(self,name):
        h=self.active_H;b=self.B;mb=self.SMB;d=self.dd
        p=mb[:,:2].sum(1)[None,None,:]
        total=mb.sum(1);u=np.divide(mb[:,2],total,out=np.zeros(32),where=total>0)[None,None,:]
        K=h/(p+3);sp=name.split(':')
        def old(pn,i):
            path=cm.mp.PATHS[pn];load=b[:,[cm.mp.LABELS.index(t) for t in path]].sum(1)
            profit=np.divide(b[:,cm.mp.LABELS.index(path[i])],load,out=np.zeros(1024),where=load>0)[:,None,None]
            pref=b[:,[cm.mp.LABELS.index(t) for t in path[:i]]].sum(1)[:,None,None]
            return profit,pref
        if sp[1]=='legal-size':return mb[:,0][None,None,:]-h
        if sp[1]=='current-floor':return u-K
        if sp[1] in ('cap','BNS'):
            t=sp[2]
            if t=='opt':q=d;n=5
            elif t.startswith('z'):q=mb[:,int(t[1:])][None,None,:];n=1
            else:q=b[:,cm.mp.LABELS.index(t)][:,None,None];n=1
            if sp[1]=='cap':return n*K-q/(p+3)
            return 8*n*u-7*n*K-h*q/(p+3)-(1-h)*q/(p+1)
        if sp[1]=='global-root-BNS':
            root=old('actual',0)[0];m=mb[:,0][None,None,:]
            return 80*root-15*m-(5-4*m)*h
        if sp[1]=='oldK':
            i=int(sp[3]);profit,pref=old(sp[2],i)
            return profit-h/(pref+5-i)
        if sp[1]=='maxK':
            i=int(sp[2]);profit=np.divide(mb[:,i],total,out=np.zeros(32),where=total>0)[None,None,:]
            return profit-h/(mb[:,:i].sum(1)[None,None,:]+5-i)
        raise ValueError(name)

    def maximum_scores(self,lam):
        score=super().maximum_scores(lam)
        assert self.active_H in (0,1)
        for name,w in zip(self.wnames,lam[-len(self.wnames):]):
            if not name.startswith('wmax:') or abs(w)<1e-11:continue
            score+=120*w*self.block_weighted(name)
        return score

    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,v) for n,v in weights if ':wmax:' in n]
        rest=[(n,v) for n,v in weights if ':wmax:' not in n]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        mb=cm.lm.STATES[self.active_max];h=self.active_H;p=sum(mb[:2]);K=cm.lm.q(h,p+3);u=cm.lm.q(mb[2],sum(mb));co={}
        for n,w in own:
            _,_,kind,menu=n.split(':')
            if kind=='cap':c=5*K;v=-cm.lm.q(1,p+3)
            else:c=40*u-35*K;v=-cm.lm.q(h,p+3)-cm.lm.q(1-h,p+1)
            const+=w*float(120*c);co[menu]=co.get(menu,0)+w*float(120*v)
        for menu,w in co.items():vec.append((w,self.countarr[tag][menu]))
        return (key[0],key,tuple(sorted(co.items()))),const,vec,me,mh

    def price(self,lam,beta,batch=60,**kw):
        minimum=None;chosen=[];contexts=0
        for h in (0,1):
            self.active_H=h
            value,cols,count=super().price(lam,beta,batch=batch,**kw)
            minimum=value if minimum is None else min(minimum,value)
            chosen.extend(cols);contexts+=count
        self.active_H=None
        chosen.sort(key=lambda z:z[0]);return minimum,chosen[:batch],contexts


def run(maxiter=8):
    import time
    U=Universe();target=HERE/'weighted_discovery.json'
    source=target if target.exists() else HERE/'coupled_discovery.json'
    src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ww=[];oo=[]
    def add(a):
        key=cm.mp.atom_key(a)+(a['max_bits'],a['H_bit'])
        if key in keys:return 0
        rr=U.atom_rows(a);assert set(rr)==set(U.names)
        atoms.append(a);cols.append([float(rr[n]) for n in U.names]);keys.add(key)
        ww.append(int(any(map(int,a['bits'][:5]))));oo.append(int(any(a['AB_hist'][4:])))
        return 1
    for a,v in zip(src['atoms'],src['primal_float']):
        if v>1e-9:
            for h in (0,1):add(dict(a,H_bit=h))
    history=[]
    for it in range(maxiter):
        start=time.time();mat=np.asarray(cols).T
        lp=linprog(-np.array(oo,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ww],b_eq=[1.],bounds=(0,None),method='highs')
        assert lp.success,lp.message
        beta=-lp.fun;lam=-lp.ineqlin.marginals
        print(json.dumps({'iteration':it,'restricted_beta':beta,'columns':len(atoms),'pricing':'started'}),flush=True)
        if beta>2+1e-7:minimum=None;new=[];contexts=None
        else:minimum,new,contexts=U.price(lam,beta,batch=90)
        count=sum(add(a) for _,a in new)
        rec={'iteration':it,'restricted_beta':beta,'columns':len(atoms),'new_columns':count,'minimum_scaled_residual':minimum,'pricing_contexts':contexts,'seconds':time.time()-start};history.append(rec)
        print(json.dumps(rec),flush=True)
        report={'scope':'Floating shared weighted-maximum plus indexed-menu necessary rows. Not full-universe exact bound, actual OPT, or complete SPE.',
                'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,
                'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},
                'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        target.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or count==0:break


def lift(source):
    source=source.resolve();src=json.loads(source.read_text())
    if 'primal_float' in src:
        support=[(a,F(str(v))) for a,v in zip(src['atoms'],src['primal_float']) if v>1e-9]
    else:support=[(a,F(a['exact_mass'])) for a in src['atoms']]
    names=list(rows(support[0][0],tuple(map(int,support[0][0]['max_bits'])),0))
    mat=np.array([[float(rows(a,tuple(map(int,a['max_bits'])),h)[n]) for a,m in support for h in (0,1)] for n in names])
    eq=np.zeros((len(support),2*len(support)))
    for j in range(len(support)):eq[j,2*j:2*j+2]=1
    rhs=np.array([float(m) for a,m in support])
    lp=linprog(np.zeros(2*len(support)),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=eq,b_eq=rhs,bounds=(0,None),method='highs')
    report={'scope':'Conditional lifting of a fixed necessary-row primal to a shared weighted maximum at the original max-third node. No universal bound or game claim.',
            'source':str(source.relative_to(cm.ROOT)),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'source_atoms':len(support),'new_rows':len(names),'floating_lift_feasible':bool(lp.success),
            'message':lp.message,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    if lp.success:
        report['minimum_new_slack_float']=float(min(mat@lp.x))
        report['lift']=[{'source_atom':j,'H_bit':h,'mass_float':float(lp.x[2*j+h])} for j in range(len(support)) for h in (0,1) if lp.x[2*j+h]>1e-10]
    else:
        aux=linprog(np.r_[np.zeros(2*len(support)),1.],A_ub=np.column_stack([-mat,-np.ones(len(names))]),b_ub=np.zeros(len(names)),
                    A_eq=np.column_stack([eq,np.zeros(len(support))]),b_eq=rhs,bounds=(0,None),method='highs')
        if aux.success:
            report['minimum_uniform_violation_float']=float(aux.fun)
            report['diagnostic_row_multipliers_float']={n:float(-v) for n,v in zip(names,aux.ineqlin.marginals) if -v>1e-10}
            report['diagnostic_atom_bounds_float']=aux.eqlin.marginals.tolist()
    out=HERE/('weighted_lift_'+source.stem+'.json');out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('lift','diagnostic_row_multipliers_float','diagnostic_atom_bounds_float')},indent=2))
    return report


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='run':run(int(sys.argv[2]) if len(sys.argv)>2 else 8)
    else:
        source=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'coupled_discovery.json'
        lift(source)

"""Maximum-root third-node weighted-maximum hinges at all exact breakpoints.

Inherits all coupled indexed histograms. The shared maximizing legal theme
is eliminated analytically, retaining the optimal-count hinge exactly.
This is discovery of necessary-row payments, never a full-SPE counterexample.
"""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,time
import numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent
CERT=HERE.parent/'certificate'
sys.path.insert(0,str(CERT))
import max_indexed_coupling as cm

def breakpoints(k=3):
    L=(k-1)*4
    return sorted({F(0),F(L-1)}|{F(L-1)-F((k-1)*d,5*(p+1)) for p in range(6-k) for d in range(6) if F(L-1)-F((k-1)*d,5*(p+1))>=0})

SPECS=[(f'{tag}:MaxHinge:3:{menu}:{t}',tag,menu,t) for tag,menus in cm.mp.MENUS.items() for menu in menus for t in breakpoints()]
SPEC={s[0]:s for s in SPECS}

def scalar(p,k,u,d,c,t):
    L=(k-1)*4
    return 5*L*u-F(t*c,p+k)-F(d,p+1)+max(F(0),F((k-1)*d-5*(L-1-t)*(p+1),(p+1)*(p+k)))

def hinge_rows(a):
    mb=tuple(map(int,a['max_bits']));p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb));d=sum(a['AB_hist'][4:])
    cc={tag:cm.counts(a,tag) for tag in cm.mp.MENUS}
    return {n:scalar(p,3,u,d,cc[tag][menu],t) for n,tag,menu,t in SPECS}

class Universe(cm.Universe):
    def __init__(self):
        super().__init__();self.names += [s[0] for s in SPECS]
        print(json.dumps({'max_third_hinge_rows':len(SPECS),'breakpoints':list(map(str,breakpoints())),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(hinge_rows(a));return rr
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert not integer,'Use exact scalar audit; denominator includes rational breakpoints.'
        mb=cm.lm.STATES[self.active_max];p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb));k=3;L=8;dd=self.countarr[tag]['opt']
        for n,w in own:
            _,_,menu,t=SPEC[n];cc=self.countarr[tag][menu]
            val=5*L*float(u)-float(t)/(p+k)*cc-dd/(p+1)+np.maximum(0.,(k-1)*dd-5*float(L-1-t)*(p+1))/((p+1)*(p+k))
            vec.append((120*w,val))
        return (key[0],key,self.active_max,tuple(own)),const,vec,me,mh

def run(maxiter=3):
    U=Universe();target=HERE/'hinge_breakpoint_discovery.json'
    source=target if target.exists() else CERT/'coupled_discovery.json'
    src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key in keys:return 0
        rr=U.atom_rows(a);assert set(rr)==set(U.names)
        atoms.append(a);cols.append([float(rr[n]) for n in U.names]);keys.add(key)
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
        return 1
    for a,m in zip(src['atoms'],src['primal_float']):
        if m>1e-9:add(a)
    for d in (0,5):
        h3=[0]*8;h3[3 if d==0 else 7]=5;h4=[0]*16;h4[7 if d==0 else 15]=5
        add({'bits':'1111111111','AB_hist':h3,'AE_hist':h3,'second_hist':h4,'menus_lh':[(5,d)]*3,'max_bits':'11111'})
    history=[]
    for it in range(maxiter):
        begin=time.time();mat=np.asarray(cols).T
        lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
        assert lp.success,lp.message;beta=-lp.fun;lam=-lp.ineqlin.marginals
        print(json.dumps({'iteration':it,'restricted_beta':beta,'columns':len(atoms),'pricing':'started' if beta<=2+1e-7 else 'not_needed_for_restricted_obstruction'}),flush=True)
        if beta>2+1e-7:minimum=None;new=[];contexts=None
        else:minimum,new,contexts=U.price(lam,beta,batch=50)
        count=sum(add(a) for _,a in new)
        rec={'iteration':it,'restricted_beta':beta,'columns':len(atoms),'new_columns':count,'minimum_scaled_residual':minimum,'pricing_contexts':contexts,'seconds':time.time()-begin};history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(w) for n,w in zip(U.names,lam) if w>1e-10},'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        target.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or not count:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 3)

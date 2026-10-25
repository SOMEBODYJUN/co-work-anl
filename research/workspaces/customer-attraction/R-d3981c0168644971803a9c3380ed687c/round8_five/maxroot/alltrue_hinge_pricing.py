"""All fixed genuine old nodes plus the real maximum-root tail: hinge attack.

Each history selects its own weighted maximum before analytic elimination;
no equality between distinct ordered-history maxima is imposed.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import numpy as np
from scipy.optimize import linprog
import allmax_hinge_pricing as am
hp=am.hp;cm=am.cm;HERE=Path(__file__).resolve().parent
SPECS=[(f'{tag}:OldHinge:{pn}:{pos}:{menu}:{t}',tag,pn,pos,menu,t) for pn,pos in cm.mp.NODES for tag,menus in cm.mp.MENUS.items() for menu in menus for t in hp.breakpoints(5-pos)]
SPEC={s[0]:s for s in SPECS}
def rows(a):
    bits=tuple(map(int,a['bits']));d=sum(a['AB_hist'][4:]);cc={tag:cm.counts(a,tag) for tag in cm.mp.MENUS}
    out={}
    for n,tag,pn,pos,menu,t in SPECS:
        p,k,u=cm.mp.source(bits,(pn,pos));out[n]=hp.scalar(p,k,u,d,cc[tag][menu],t)
    return out
class Universe(am.Universe):
    def __init__(self):
        super().__init__();self.names += [s[0] for s in SPECS]
        print(json.dumps({'old_true_hinge_rows':len(SPECS),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert not integer
        dd=self.countarr[tag]['opt']
        for n,w in own:
            _,_,pn,pos,menu,t=SPEC[n];p,k,u=cm.mp.source(bits,(pn,pos));L=(k-1)*4;cc=self.countarr[tag][menu]
            val=5*L*float(u)-float(t)/(p+k)*cc-dd/(p+1)+np.maximum(0.,(k-1)*dd-5*float(L-1-t)*(p+1))/((p+1)*(p+k))
            vec.append((120*w,val))
        return (key[0],key,tuple(bits),tuple(own)),const,vec,me,mh
def run():
    U=Universe();src=json.loads(HERE.joinpath('allmax_hinge_discovery.json').read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    for a,m in zip(src['atoms'],src['primal_float']):
        if m<1e-9:continue
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key in keys:continue
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);keys.add(key);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
    assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('alltrue_hinge_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

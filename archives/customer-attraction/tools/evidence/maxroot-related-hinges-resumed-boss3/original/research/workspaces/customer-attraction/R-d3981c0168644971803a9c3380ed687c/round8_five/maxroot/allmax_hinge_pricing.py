"""Extend exact weighted-maximum hinge breakpoints to all true max-tail nodes.

Independent derived rows, same fixed original maximum-root branch.
Floating necessary-row attack only, never a general bound or SPE witness.
"""
from pathlib import Path
import sys,json,hashlib,time
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import hinge_breakpoint_pricing as hp
cm=hp.cm;HERE=Path(__file__).resolve().parent
SPECS=[(f'{tag}:OtherMaxHinge:{pos}:{menu}:{t}',tag,pos,menu,t) for pos in (1,3) for tag,menus in cm.mp.MENUS.items() for menu in menus for t in hp.breakpoints(5-pos)]
SPEC={s[0]:s for s in SPECS}
def rows(a):
    mb=tuple(map(int,a['max_bits']));d=sum(a['AB_hist'][4:]);cc={tag:cm.counts(a,tag) for tag in cm.mp.MENUS}
    return {n:hp.scalar(sum(mb[:pos]),5-pos,cm.lm.q(mb[pos],sum(mb)),d,cc[tag][menu],t) for n,tag,pos,menu,t in SPECS}
class Universe(hp.Universe):
    def __init__(self):
        super().__init__();self.names += [s[0] for s in SPECS]
        print(json.dumps({'other_max_hinge_rows':len(SPECS),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert not integer
        mb=cm.lm.STATES[self.active_max];dd=self.countarr[tag]['opt']
        for n,w in own:
            _,_,pos,menu,t=SPEC[n];p=sum(mb[:pos]);k=5-pos;L=(k-1)*4;u=cm.lm.q(mb[pos],sum(mb));cc=self.countarr[tag][menu]
            val=5*L*float(u)-float(t)/(p+k)*cc-dd/(p+1)+np.maximum(0.,(k-1)*dd-5*float(L-1-t)*(p+1))/((p+1)*(p+k))
            vec.append((120*w,val))
        return (key[0],key,self.active_max,tuple(own)),const,vec,me,mh
def run():
    U=Universe();source=HERE/'hinge_breakpoint_discovery.json';src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    for a,m in zip(src['atoms'],src['primal_float']):
        if m<1e-9:continue
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key in keys:continue
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);keys.add(key);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
    assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('allmax_hinge_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

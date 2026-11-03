"""Both arbitrary five-topic menus of the true-H projection are retained.

The seven-row theorem permits d to be any legal five-menu, not only an
optimal tuple. Same-family substitutions preserve full histogram pricing.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import numpy as np
from scipy.optimize import linprog
import trueH_payment_pricing as th
cm=th.cm;HERE=Path(__file__).resolve().parent
SPECS=[]
for node in ('max','actual','second','indexed'):
    for tag,menus in cm.mp.MENUS.items():
        if node=='indexed' and tag!='Sbranch':continue
        for dc in ('opt',)+menus:
            for jc in ('opt',)+menus:
                if dc=='opt' and jc in menus:continue
                SPECS.append((f'{tag}:TrueHTwoMenus:{node}:{dc}:{jc}',tag,node,dc,jc))
SPEC={s[0]:s for s in SPECS}
def row_value(a,tag,node,dc,jc):
    bits=tuple(map(int,a['bits']));mb=tuple(map(int,a['max_bits']));M=mb[0];cc=cm.counts(a,tag);cc['opt']=sum(a['AB_hist'][4:]);d=cc[dc];j=cc[jc]
    if node=='indexed':
        bg=bits[cm.mp.LABELS.index('A')]
        return sum((n*(17040*cm.lm.q(typ[1],bg+sum(typ))+1085*M-F(2679*j,bg+typ[0]+3)-th.FT[bg+typ[0]][d]) for n,typ in zip(a['second_hist'],cm.mp.TYPES[4])),F(0))
    if node=='max':p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb))
    else:p,k,u=cm.mp.source(bits,(node,2));assert k==3
    return 17040*u+1085*M-F(2679*j,p+3)-th.FT[p][d]
def rows(a):return {n:row_value(a,tag,node,dc,jc) for n,tag,node,dc,jc in SPECS}
class Universe(th.Universe):
    def __init__(self):
        super().__init__();self.names += [s[0] for s in SPECS];self.twomenu_cache={}
        print(json.dumps({'trueH_bidirectional_rows':len(SPECS),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def two_menu_array(self,bits,tag,node,dc,jc):
        mb=cm.lm.STATES[self.active_max];M=mb[0];dd=self.countarr[tag][dc];cc=self.countarr[tag][jc]
        if node!='indexed':
            if node=='max':p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb))
            else:p,k,u=cm.mp.source(bits,(node,2));assert k==3
            return 17040*float(u)+1085*M-2679*cc/(p+3)-np.array([float(x) for x in th.FT[p]])[dd]
        bg=bits[cm.mp.LABELS.index('A')];key=(tag,bg,M,dc,jc)
        if key in self.twomenu_cache:return self.twomenu_cache[key]
        ans=np.zeros(len(self.H[4]))
        for ti,typ in enumerate(cm.mp.TYPES[4]):
            p=bg+typ[0];u=cm.lm.q(typ[1],bg+sum(typ));ans+=self.H[4][:,ti]*(17040*float(u)+1085*M-2679*cc/(p+3)-np.array([float(x) for x in th.FT[p]])[dd])
        self.twomenu_cache[key]=ans;return ans
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert not integer
        for n,w in own:
            _,_,node,dc,jc=SPEC[n];vec.append((120*w,self.two_menu_array(bits,tag,node,dc,jc)))
        return (key[0],key,tuple(bits),self.active_max,tuple(own)),const,vec,me,mh
def run():
    U=Universe();src=json.loads(HERE.joinpath('trueH_payment_fullpricing.json').read_text());atoms=[];cols=[];ws=[];os=[]
    for a in src['atoms']:
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('trueH_bidirectional_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

"""Add the independently checked true-H/two-successor projection to payment.

Source derivation and 144-state certificate belong to sibling certificate/
trueH_seven_rows.md. Each current profit comes from its own true history.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import numpy as np
from scipy.optimize import linprog
import indexed_hinge_pricing as ip
hp=ip.hp;cm=ip.cm;HERE=Path(__file__).resolve().parent
FT=((F(0),F(960),F(1220),F(1480),F(1740),F(2000)),(F(0),F(1665,4),F(2745,4),F(3785,4),F(4825,4),F(5865,4)),(F(0),F(320),F(524),F(728),F(932),F(1136)))
SPECS=[(f'{tag}:TrueHProjection:{node}:{menu}',tag,node,menu) for node in ('max','actual','second') for tag,menus in cm.mp.MENUS.items() for menu in menus]+[(f'Sbranch:TrueHIndexed:{menu}','Sbranch','indexed',menu) for menu in cm.mp.MENUS['Sbranch']]
SPEC={s[0]:s for s in SPECS}
def row_value(a,tag,node,menu):
    bits=tuple(map(int,a['bits']));mb=tuple(map(int,a['max_bits']));M=mb[0];d=sum(a['AB_hist'][4:]);c=cm.counts(a,tag)[menu]
    if node=='indexed':
        bg=bits[cm.mp.LABELS.index('A')]
        return sum((n*(17040*cm.lm.q(typ[1],bg+sum(typ))+1085*M-F(2679*c,bg+typ[0]+3)-FT[bg+typ[0]][d]) for n,typ in zip(a['second_hist'],cm.mp.TYPES[4])),F(0))
    if node=='max':p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb))
    else:p,k,u=cm.mp.source(bits,(node,2));assert k==3
    return 17040*u+1085*M-F(2679*c,p+3)-FT[p][d]
def rows(a):return {n:row_value(a,tag,node,menu) for n,tag,node,menu in SPECS}
class Universe(ip.Universe):
    def __init__(self):
        super().__init__();self.names += [s[0] for s in SPECS];self.projection_cache={}
        print(json.dumps({'trueH_two_successor_rows':len(SPECS),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def coefficient_array(self,*args,**kwargs):return super().coefficient_array(*args,**kwargs)
    def project_array(self,bits,tag,node,menu):
        mb=cm.lm.STATES[self.active_max];M=mb[0];dd=self.countarr[tag]['opt'];cc=self.countarr[tag][menu]
        if node!='indexed':
            if node=='max':p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb))
            else:p,k,u=cm.mp.source(bits,(node,2));assert k==3
            f=np.array([float(x) for x in FT[p]])[dd]
            return 17040*float(u)+1085*M-2679*cc/(p+3)-f
        bg=bits[cm.mp.LABELS.index('A')];cachekey=(tag,bg,M,menu)
        if cachekey in self.projection_cache:return self.projection_cache[cachekey]
        ans=np.zeros(len(self.H[4]))
        for ti,typ in enumerate(cm.mp.TYPES[4]):
            p=bg+typ[0];u=cm.lm.q(typ[1],bg+sum(typ));ff=np.array([float(x) for x in FT[p]])[dd]
            ans+=self.H[4][:,ti]*(17040*float(u)+1085*M-2679*cc/(p+3)-ff)
        self.projection_cache[cachekey]=ans;return ans
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert not integer
        for n,w in own:
            _,_,node,menu=SPEC[n];vec.append((120*w,self.project_array(bits,tag,node,menu)))
        return (key[0],key,tuple(bits),self.active_max,tuple(own)),const,vec,me,mh
def run():
    U=Universe();src=json.loads(HERE.joinpath('indexed_hinge_fullpricing.json').read_text());atoms=[];cols=[];ws=[];os=[]
    for a in src['atoms']:
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('trueH_payment_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

"""Weighted-max queries inside matched indexed deviation continuations.

Unlike a query at one fixed old history, each indexed branch retains its
own exact background and true successor utility. Only same-family menus
are combined, so full histogram separation remains valid.
"""
from pathlib import Path
import json,hashlib
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
import alltrue_hinge_pricing as at
hp=at.hp;cm=at.cm;HERE=Path(__file__).resolve().parent
NODES={'AB':(1,),'AE':(1,),'Sbranch':(1,2)}
SPECS=[(f'{tag}:IndexedHinge:{pos}:{menu}:{t}',tag,pos,menu,t) for tag,positions in NODES.items() for pos in positions for menu in cm.mp.MENUS[tag] for t in hp.breakpoints((4 if tag=='Sbranch' else 3)-pos)]
SPEC={s[0]:s for s in SPECS}
def context(bits,tag):
    b=dict(zip(cm.mp.LABELS,map(int,bits)))
    return b['A'] if tag=='Sbranch' else b['A']+b['B' if tag=='AB' else 'E']
def row_value(bits,tag,pos,menu,t,hist):
    types=cm.mp.TYPES[4 if tag=='Sbranch' else 3];bg=context(bits,tag);d=sum(n*typ[0] for n,typ in zip(hist,types));menuindex=cm.mp.MENUS[tag].index(menu)+1;c=sum(n*typ[menuindex] for n,typ in zip(hist,types));k=len(types[0])-pos
    return sum((n*hp.scalar(bg+sum(typ[:pos]),k,cm.lm.q(typ[pos],bg+sum(typ)),d,c,t) for n,typ in zip(hist,types)),F(0))
def rows(a):
    return {n:row_value(a['bits'],tag,pos,menu,t,a[cm.mp.FIELDS[tag]]) for n,tag,pos,menu,t in SPECS}
class Universe(at.Universe):
    def __init__(self):
        super().__init__();self.names += [s[0] for s in SPECS];self.hinge_array_cache={}
        print(json.dumps({'matched_indexed_hinge_rows':len(SPECS),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def coefficient_array(self,bits,tag,pos,menu,t):
        bg=context(bits,tag);cachekey=(tag,bg,pos,menu,t)
        if cachekey in self.hinge_array_cache:return self.hinge_array_cache[cachekey]
        types=cm.mp.TYPES[4 if tag=='Sbranch' else 3];H=self.H[len(types[0])];d=self.countarr[tag]['opt'];c=self.countarr[tag][menu];k=len(types[0])-pos;L=4*(k-1);ans=np.zeros(len(H))
        for ti,typ in enumerate(types):
            p=bg+sum(typ[:pos]);u=cm.lm.q(typ[pos],bg+sum(typ))
            val=5*L*float(u)-float(t)/(p+k)*c-d/(p+1)+np.maximum(0.,(k-1)*d-5*float(L-1-t)*(p+1))/((p+1)*(p+k))
            ans+=H[:,ti]*val
        self.hinge_array_cache[cachekey]=ans;return ans
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert not integer
        for n,w in own:
            _,_,pos,menu,t=SPEC[n];vec.append((120*w,self.coefficient_array(bits,tag,pos,menu,t)))
        return (key[0],key,context(bits,tag),tuple(own)),const,vec,me,mh
def run():
    U=Universe();src=json.loads(HERE.joinpath('alltrue_hinge_discovery.json').read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    for a,m in zip(src['atoms'],src['primal_float']):
        if m<1e-9:continue
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key in keys:continue
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);keys.add(key);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('indexed_hinge_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

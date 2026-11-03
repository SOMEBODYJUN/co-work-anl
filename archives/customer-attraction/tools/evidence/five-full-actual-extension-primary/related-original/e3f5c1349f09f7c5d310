"""Complete source-indexed true-H J queries with its own T/U/V repeats.

Its own W repeat is already present. These are omitted instances of the
same certified projection, not a new mechanism or new welfare theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import numpy as np
from scipy.optimize import linprog
import trueH_fixed_closure_pricing as fc
th=fc.th;cm=fc.cm;HERE=Path(__file__).resolve().parent
SPECS=[(f'Sbranch:TrueHOwnIndex:{i}',i) for i in range(3)];SPEC=dict(SPECS)
def rows(a):
    bg=int(a['bits'][cm.mp.LABELS.index('A')]);M=int(a['max_bits'][0]);d=sum(a['AB_hist'][4:])
    return {n:sum((v*(17040*cm.lm.q(t[1],bg+sum(t))+1085*M-F(13395*t[i],bg+t[0]+3)-th.FT[bg+t[0]][d]) for v,t in zip(a['second_hist'],cm.mp.TYPES[4])),F(0)) for n,i in SPECS}
class Universe(fc.Universe):
    def __init__(self):
        super().__init__();self.names += [n for n,i in SPECS];self.own_index_cache={}
        print(json.dumps({'own_index_repeat_query_rows':3,'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in SPEC];rest=[(n,w) for n,w in weights if n not in SPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert tag=='Sbranch' and not integer
        mb=cm.lm.STATES[self.active_max];M=mb[0];bg=bits[cm.mp.LABELS.index('A')];dd=self.countarr[tag]['opt']
        for n,w in own:
            i=SPEC[n];ck=(bg,M,i)
            if ck not in self.own_index_cache:
                ans=np.zeros(len(self.H[4]))
                for ti,t in enumerate(cm.mp.TYPES[4]):
                    p=bg+t[0];u=cm.lm.q(t[1],bg+sum(t));ans+=self.H[4][:,ti]*(17040*float(u)+1085*M-13395*t[i]/(p+3)-np.array([float(x) for x in th.FT[p]])[dd])
                self.own_index_cache[ck]=ans
            vec.append((120*w,self.own_index_cache[ck]))
        return (key[0],key,bg,M,tuple(own)),const,vec,me,mh
def run():
    U=Universe();src=json.loads(HERE.joinpath('trueH_fixed_closure_fullpricing.json').read_text());atoms=[];cols=[];ws=[];os=[]
    for a in src['atoms']:
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('trueH_own_index_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

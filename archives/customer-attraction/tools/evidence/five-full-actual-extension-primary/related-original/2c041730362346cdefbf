"""One true actual-third HQR projection added to the 6750-row payment.

The projection is max over all eight same-strategy HQR membership states.
Conditioned on h, all histogram-dependent terms are independent of q,r;
their four states are maximized in the fixed block, then h is priced twice.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
import numpy as np
from scipy.optimize import linprog
import trueH_own_index_pricing as oi
cm=oi.cm;HERE=Path(__file__).resolve().parent
import actual13_projection as proj
WEIGHT_SOURCE=HERE.parent/'certificate/actual13_projection.json'
WEIGHTS={n:int(v) for n,v in json.loads(WEIGHT_SOURCE.read_text())['nonnegative_integer_row_weights'].items()}
NAME='Actual13TrueHQRProjection'

def family_delta(p,h,x,d,tag,ab=0,ae=0,su=0,sv=0,sw=0):
    a=F(1,p+h+1);b=F(1,p+h+2);diff=a-b
    if tag=='AB':return WEIGHTS['AB:trueH:tax:mY:opt']*ab*(-5*a+2*d*diff)
    if tag=='AE':return -F(WEIGHTS['AE:trueH:weighted-cap:mY']*ae,p+3)
    return (WEIGHTS['Sbranch:trueH:tax:mU:X']*su*(-a+2*x*diff)
            +WEIGHTS['Sbranch:trueH:tax:mU:mV']*(-5*(su+sv)*a+2*su*sv*diff)
            +WEIGHTS['Sbranch:trueH:tax:mU:mW']*(-5*(su+sw)*a+2*su*sw*diff)
            +WEIGHTS['Sbranch:trueH:tax:mV:opt']*sv*(-5*a+2*d*diff))

class Universe(oi.Universe):
    def __init__(self):
        super().__init__();self.names.append(NAME);self.proj_h=None;self.proj_weight=0.;self.constant_tables={};self.constant_cache={}
        print(json.dumps({'actual13_projection_rows':1,'total_rows':len(self.names),'projection_pricing_modes':2,'hidden_qr_states_per_mode':4}),flush=True)
    def pricing_modes(self):return (0,1)
    def set_pricing_mode(self,h):self.proj_h=h
    def atom_rows(self,a):
        rr=super().atom_rows(a);c=proj.context(a)
        if self.proj_h is None:rr[NAME]=proj.coefficient(a,WEIGHTS)
        else:rr[NAME]=max(proj.conditioned(c,(self.proj_h,q,r),WEIGHTS) for q,r in product((0,1),repeat=2))
        return rr
    def constant_block(self,h):
        if h in self.constant_tables:return self.constant_tables[h]
        table=np.zeros((1024,6,2,2))
        for bi,bits in enumerate(self.bits):
            bb=dict(zip(cm.mp.LABELS,bits));p=bb['A']+bb['B'];u=cm.lm.q(bb['C'],sum(bb[t] for t in 'ABCDE'));x=bb['X'];y=bb['Y']
            for d in range(6):
                for m,z in product((0,1),repeat=2):
                    key=(h,p,u,x,y,d,m,z)
                    if key not in self.constant_cache:
                        c={'p':p,'u':u,'m':m,'x':x,'y':y,'z':z,'d':d,'ab':0,'ae':0,'su':0,'sv':0,'sw':0}
                        self.constant_cache[key]=max(proj.conditioned(c,(h,q,r),WEIGHTS) for q,r in product((0,1),repeat=2))
                    table[bi,d,m,z]=float(self.constant_cache[key])
        self.constant_tables[h]=table;return table
    def maximum_scores(self,lam):
        score=super().maximum_scores(lam);self.proj_weight=float(lam[self.names.index(NAME)])
        if abs(self.proj_weight)>1e-11:
            assert self.proj_h in (0,1)
            table=self.constant_block(self.proj_h);m=self.SMB[:,0].astype(int);z=self.SMB[:,4].astype(int)
            score+=120*self.proj_weight*table[:,:,m,z]
        return score
    def family_score(self,bits,tag,weights,integer=False):
        key,const,vec,me,mh=super().family_score(bits,tag,weights,integer=integer)
        if abs(self.proj_weight)<1e-11:return key,const,vec,me,mh
        assert not integer and self.proj_h in (0,1)
        bb=dict(zip(cm.mp.LABELS,bits));p=bb['A']+bb['B'];x=bb['X'];h=self.proj_h;d=self.countarr[tag]['opt'];arr=self.countarr[tag];a=1./(p+h+1);diff=a-1./(p+h+2)
        if tag=='AB':v=WEIGHTS['AB:trueH:tax:mY:opt']*arr['mY']*(-5*a+2*d*diff)
        elif tag=='AE':v=-WEIGHTS['AE:trueH:weighted-cap:mY']*arr['mY']/(p+3)
        else:
            su,sv,sw=arr['mU'],arr['mV'],arr['mW']
            v=(WEIGHTS['Sbranch:trueH:tax:mU:X']*su*(-a+2*x*diff)
               +WEIGHTS['Sbranch:trueH:tax:mU:mV']*(-5*(su+sv)*a+2*su*sv*diff)
               +WEIGHTS['Sbranch:trueH:tax:mU:mW']*(-5*(su+sw)*a+2*su*sw*diff)
               +WEIGHTS['Sbranch:trueH:tax:mV:opt']*sv*(-5*a+2*d*diff))
        vec.append((120*self.proj_weight,v));return (key[0],key,p,x,h,self.proj_weight),const,vec,me,mh

def audit_decomposition():
    checks=0
    for p,h,x,d in product(range(3),range(2),range(2),range(6)):
        base={'p':p,'u':F(0),'m':0,'x':x,'y':0,'z':0,'d':d,'ab':0,'ae':0,'su':0,'sv':0,'sw':0}
        for q,r in product((0,1),repeat=2):
            state=(h,q,r);zeros=proj.raw_blocks(base,state)
            for tag,index in [('AB',1),('AE',2),('Sbranch',3)]:
                domain=[(v,0,0) for v in range(6)] if tag!='Sbranch' else product(range(6),repeat=3)
                for a,b,c in domain:
                    cc=dict(base)
                    if tag=='AB':cc['ab']=a;kw={'ab':a}
                    elif tag=='AE':cc['ae']=a;kw={'ae':a}
                    else:cc.update(su=a,sv=b,sw=c);kw={'su':a,'sv':b,'sw':c}
                    block=proj.raw_blocks(cc,state)[index]
                    delta=sum(WEIGHTS[n]*(v-zeros[index][n]) for n,v in block.items())
                    assert delta==family_delta(p,h,x,d,tag,**kw);checks+=1
    report={'status':'passed','checks':checks,'meaning':'At fixed h every family delta is independent of q,r; exact max4 constant plus three independent family deltas equals conditional max4 raw.'}
    HERE.joinpath('actual13_decomposition_audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)

def run():
    audit_decomposition();U=Universe();src=json.loads(HERE.joinpath('trueH_own_index_discovery.json').read_text());atoms=[];cols=[];ws=[];os=[]
    for a in src['atoms']:
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('actual13_payment_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

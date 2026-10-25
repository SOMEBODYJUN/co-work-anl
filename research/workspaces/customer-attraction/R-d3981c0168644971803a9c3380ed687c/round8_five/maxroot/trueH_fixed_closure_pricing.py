"""Complete the known true-H projection's J queries over all 15 fixed labels.

This closes a previously omitted legal-query class. It does not claim a
new mechanism, independent-H compatibility obstruction, or welfare bound.
"""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import numpy as np
from scipy.optimize import linprog
import trueH_source_last_pricing as sl
th=sl.th;cm=sl.cm;HERE=Path(__file__).resolve().parent
LABELS=list(cm.mp.LABELS)+[f'z{i}' for i in range(5)]
FIXED=[(f'PFixed:{node}:{label}',node,label) for node in ('max','actual','second') for label in LABELS]
INDEXED=[(f'Sbranch:PFixedIndexed:{label}',label) for label in LABELS]
SPEC={n:(node,label) for n,node,label in FIXED};ISPEC=dict(INDEXED)
def query(bits,mb,label):return mb[int(label[1:])] if label.startswith('z') else bits[cm.mp.LABELS.index(label)]
def rows(a):
    bits=tuple(map(int,a['bits']));mb=tuple(map(int,a['max_bits']));M=mb[0];d=sum(a['AB_hist'][4:]);out={}
    for n,node,label in FIXED:
        if node=='max':p=sum(mb[:2]);u=cm.lm.q(mb[2],sum(mb))
        else:p,k,u=cm.mp.source(bits,(node,2));assert k==3
        out[n]=17040*u+1085*M-F(13395*query(bits,mb,label),p+3)-th.FT[p][d]
    bg=bits[cm.mp.LABELS.index('A')]
    for n,label in INDEXED:
        q=query(bits,mb,label)
        out[n]=sum((v*(17040*cm.lm.q(t[1],bg+sum(t))+1085*M-F(13395*q,bg+t[0]+3)-th.FT[bg+t[0]][d]) for v,t in zip(a['second_hist'],cm.mp.TYPES[4])),F(0))
    return out
class Universe(sl.Universe):
    def __init__(self):
        super().__init__();self.names += [n for n,node,label in FIXED]+[n for n,label in INDEXED];self.fixed_query_cache={}
        print(json.dumps({'all_fixed_trueH_query_rows':len(FIXED)+len(INDEXED),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(rows(a));return rr
    def fixed_block(self,node,label):
        b=self.B;mb=self.SMB;M=mb[:,0][None,None,:];d=self.dd.astype(int)
        if node=='max':p=mb[:,:2].sum(1)[None,None,:].astype(int);total=mb.sum(1);u=np.divide(mb[:,2],total,out=np.zeros(32),where=total>0)[None,None,:]
        else:
            path=cm.mp.PATHS[node];ids=[cm.mp.LABELS.index(t) for t in path];total=b[:,ids].sum(1);p=b[:,ids[:2]].sum(1)[:,None,None].astype(int);u=np.divide(b[:,ids[2]],total,out=np.zeros(1024),where=total>0)[:,None,None]
        q=mb[:,int(label[1:])][None,None,:] if label.startswith('z') else b[:,cm.mp.LABELS.index(label)][:,None,None]
        return 17040*u+1085*M-13395*q/(p+3)-np.array([[float(x) for x in row] for row in th.FT])[p,d]
    def maximum_scores(self,lam):
        score=super().maximum_scores(lam)
        for n,w in zip(self.names,lam):
            if n in SPEC and abs(w)>1e-11:
                node,label=SPEC[n];score+=120*w*self.fixed_block(node,label)
        return score
    def family_score(self,bits,tag,weights,integer=False):
        own=[(n,w) for n,w in weights if n in ISPEC];rest=[(n,w) for n,w in weights if n not in ISPEC]
        key,const,vec,me,mh=super().family_score(bits,tag,rest,integer=integer)
        if not own:return key,const,vec,me,mh
        assert tag=='Sbranch' and not integer
        mb=cm.lm.STATES[self.active_max];M=mb[0];bg=bits[cm.mp.LABELS.index('A')];dd=self.countarr[tag]['opt']
        for n,w in own:
            label=ISPEC[n];q=query(bits,mb,label);ck=(bg,M,q)
            if ck not in self.fixed_query_cache:
                ans=np.zeros(len(self.H[4]))
                for ti,t in enumerate(cm.mp.TYPES[4]):
                    p=bg+t[0];u=cm.lm.q(t[1],bg+sum(t));ans+=self.H[4][:,ti]*(17040*float(u)+1085*M-13395*q/(p+3)-np.array([float(x) for x in th.FT[p]])[dd])
                self.fixed_query_cache[ck]=ans
            vec.append((120*w,self.fixed_query_cache[ck]))
        return (key[0],key,tuple(bits),self.active_max,tuple(own)),const,vec,me,mh
def run():
    U=Universe();src=json.loads(HERE.joinpath('trueH_source_last_discovery.json').read_text());atoms=[];cols=[];ws=[];os=[]
    for a in src['atoms']:
        rr=U.atom_rows(a);assert set(rr)==set(U.names);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
    mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist(),'dual_beta_float':float(-lp.fun),'minimum_slack_float':float(min(mat@lp.x)),'dual_multipliers_float':{n:float(-w) for n,w in zip(U.names,lp.ineqlin.marginals) if w< -1e-10},'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    HERE.joinpath('trueH_fixed_closure_discovery.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('row_names','atoms','primal_float','dual_multipliers_float')},indent=2))
if __name__=='__main__':run()

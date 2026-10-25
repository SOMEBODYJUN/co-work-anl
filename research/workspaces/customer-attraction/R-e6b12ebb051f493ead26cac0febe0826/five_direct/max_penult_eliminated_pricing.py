"""Add the eliminated genuine max-branch penultimate portfolio row.

Float full-domain discovery; exact certification is a separate task.
The row comes from 10*S+Z+2*V, with all reply membership counts eliminated
by 0<=ell<=5. No new history selectors or customer bounds are imposed.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys,json,time,hashlib
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'AGENTS.md').exists())
OLD=ROOT/'research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round13/certificate'
sys.path.insert(0,str(OLD))
import max_menu_tuple_pricing as mt
import max_menu_joint_pricing as mj
import menu_ap_pricing as mp

NAME='max:penult:optimal_portfolio_eliminated'
PARAMETERS=sorted({F(d*(p+a+1),(p+1)*(p+2)) for p in range(4) for a in (0,1) for d in range(6)})


def newrow(a,t=F(1,2)):
    mb=list(map(int,a['max_bits']));p=sum(mb[:3]);tot=sum(mb)
    d=sum(a['AB_hist'][4:])
    v4=F(mb[3],tot) if mb[3] else F(0)
    v5=F(mb[4],tot) if mb[4] else F(0)
    return 5*v4+t*v5-F(d,p+1)+max(F(0),F(d,(p+1)*(p+2))-t/F(p+mb[3]+1))


class Universe(mt.Universe):
    def __init__(self,family=False):
        super().__init__()
        self.params={NAME:F(1,2)} if not family else {NAME+':'+str(t):t for t in PARAMETERS}
        self.maxnames+=list(self.params);self.names+=list(self.params)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update({name:newrow(a,t) for name,t in self.params.items()});return rr
    def block_coeff(self,name):
        if name not in self.params:return super().block_coeff(name)
        t=float(self.params[name])
        mb=self.SMB;d=self.dd
        p=mb[:,:3].sum(1)[None,None,:]
        tot=mb.sum(1)
        v4=np.divide(mb[:,3],tot,out=np.zeros(32),where=tot>0)[None,None,:]
        v5=np.divide(mb[:,4],tot,out=np.zeros(32),where=tot>0)[None,None,:]
        lastterm=np.maximum(0,d/((p+1)*(p+2))-t/(p+mb[:,3][None,None,:]+1))
        return 5*v4+t*v5-d/(p+1)+lastterm


def main():
    family='--family' in sys.argv
    U=Universe(family);src=json.loads((OLD/'exact_max_menu_tuple_primal.json').read_text())
    atoms=[];cols=[];keys=set();ws=[];os=[];oldcache={}
    def add(a):
        key=mp.atom_key(a)+(a['max_bits'],)
        if key in keys:return 0
        oldkey=mp.atom_key(a)
        if oldkey not in oldcache:oldcache[oldkey]=mp.Universe.atom_rows(U,a)
        mb=tuple(map(int,a['max_bits']))
        rr={**oldcache[oldkey],**mj.new_rows(a,mb),**mt.tuple_rows(a,mb),**{name:newrow(a,t) for name,t in U.params.items()}}
        cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key)
        ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])))
        return 1
    for a in src['atoms']:
        for mb in product((0,1),repeat=5):
            b=dict(a,max_bits=''.join(map(str,mb)));b.pop('exact_mass',None);add(b)
    outpath=HERE/('max_penult_family_discovery.json' if family else 'max_penult_eliminated_discovery.json');history=[]
    for it in range(12):
        start=time.time();mat=np.asarray(cols).T
        lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs')
        assert lp.success,lp.message
        beta=-lp.fun;lam=-lp.ineqlin.marginals
        if beta>2+1e-7:minimum=None;new=[];contexts=None
        else:minimum,new,contexts=U.price(lam,beta,batch=80)
        oldcount=len(atoms);count=sum(add(a) for _,a in new)
        rec={'iteration':it,'columns':len(atoms),'restricted_beta':beta,'minimum_scaled_residual':minimum,'new_columns':count,'pricing_contexts':contexts,'seconds':time.time()-start}
        history.append(rec);print(json.dumps(rec),flush=True)
        report={'scope':'Floating max-branch eliminated true penultimate portfolio row, joined with old necessary rows. Not a welfare theorem or SPE.','row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_lambda_float':lam.tolist(),'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
        outpath.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or count==0:break


if __name__=='__main__':main()

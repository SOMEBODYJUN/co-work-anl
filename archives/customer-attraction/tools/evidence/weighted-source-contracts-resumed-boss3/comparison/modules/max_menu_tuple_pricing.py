"""Max 3/4-tail comparisons with all multisets from Q and max five labels.

Q ranges over the old ten fixed legal themes. The 875 distinct comparisons
retain the complete 32-state block. Float discovery, not a theorem.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import sys,json
import numpy as np
import max_menu_joint_pricing as mj
import menu_ap_pricing as mp
import lift_maximum_branch as lm
def specs():
    ans=[]
    for rem in (3,4):
        for qs in combinations_with_replacement(range(5),rem):ans.append((f'MaxTuple:{rem}:own:{"".join(map(str,qs))}',rem,None,0,qs))
        for q in mp.LABELS:
            for n in range(1,rem+1):
                for qs in combinations_with_replacement(range(5),rem-n):ans.append((f'MaxTuple:{rem}:{q}:{n}:{"".join(map(str,qs))}',rem,q,n,qs))
    return ans
SPECS=specs();SPEC={s[0]:s for s in SPECS}
def tuple_rows(a,mb):
    b=dict(zip(mp.LABELS,map(int,a['bits'])));out={};total=sum(mb)
    for name,rem,q,n,qs in SPECS:
        p=sum(mb[:5-rem]);e=(n*b[q] if q else 0)+sum(mb[i] for i in qs);beta=F(5,3) if rem==3 else F(1499,750)
        val=beta*lm.q(sum(mb[5-rem:]),total)-lm.q(e,p+e)
        if rem==4:val-=mj.RHOMIN[mb[0],tuple(mb[1:])]
        out[name]=val
    return out
class Universe(mj.Universe):
    def __init__(self):
        super().__init__();self.tuplenames=[s[0] for s in SPECS];self.names+=self.tuplenames;self.maxnames+=self.tuplenames
        print(json.dumps({'local_six_label_tuple_rows':len(SPECS),'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,a):
        rr=super().atom_rows(a);rr.update(tuple_rows(a,tuple(map(int,a['max_bits']))));return rr
    def block_coeff(self,name):
        if name not in SPEC:return super().block_coeff(name)
        _,rem,q,n,qs=SPEC[name];mb=self.SMB;p=mb[:,:5-rem].sum(1)[None,None,:];total=mb.sum(1);v=np.divide(mb[:,5-rem:].sum(1),total,out=np.zeros(32),where=total>0)[None,None,:]
        e=mb[:,list(qs)].sum(1)[None,None,:]
        if q:e=e+n*self.B[:,mp.LABELS.index(q)][:,None,None]
        den=p+e;comp=np.divide(e,den,out=np.zeros(np.broadcast_shapes(e.shape,den.shape)),where=e>0);val=(5/3 if rem==3 else 1499/750)*v-comp
        if rem==4:val=val-np.array([float(mj.RHOMIN[s[0],tuple(s[1:])]) for s in mj.STATES])[None,None,:]
        return val
if __name__=='__main__':mj.run(int(sys.argv[1]) if len(sys.argv)>1 else 8,Universe,'max_menu_tuple_discovery.json','max_menu_joint_discovery.json')

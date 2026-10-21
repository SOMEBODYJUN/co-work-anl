"""A genuinely shared matching cut, priced over the full type universe."""
from terminal_cross_pricing import *

class JointTerminalUniverse(TerminalUniverse):
    def __init__(self):
        super().__init__();self.single.append(('jointfinal:AB:Sbranch:2O+3O','Sbranch',23,'OO'));self.names += [self.single[-1][0]]
        H=self.H[4];ty=self.ty[4];K=H@ty[:,2];L=H@ty[:,3]
        counts={t:(H@(ty[:,0].__eq__(t)*(ty[:,2]+ty[:,3]-ty[:,2]*ty[:,3])),H@(ty[:,0].__eq__(t)*ty[:,2]*ty[:,3])) for t in (0,1)}
        for p,d,h0,h1 in product(range(3),range(6),range(6),range(6)):
            if h0>5-d or h1>d:continue
            D=sum(F(n-h,p+t+1)+F(h,p+t+2) for t,n,h in ((0,5-d,h0),(1,d,h1)))
            cost=-int(sc(D))*(K+L)
            for t,n,h in ((0,5-d,h0),(1,d,h1)):
                a0=int(sc(F(1,p+t+1)));a1=int(sc(F(1,p+t+2)))
                for c in counts[t]:cost+=a0*np.minimum(c,n-h)+a1*np.maximum(0,c-n+h)
            self.qcost[4,p,d,h0,h1,23,'OO']=cost
        print(json.dumps({'genuine_joint_terminal_rows':1,'total_rows':len(self.names)}),flush=True)
    def atom_rows(self,atom):
        rr=CrossUniverse.atom_rows(self,atom)
        for n,target,pos,kind in self.single:
            comp=((2,'O',F(1)),(3,'O',F(1))) if kind=='OO' else ((pos,kind,F(1)),)
            rr[n]=joint_row(atom,'AB','second' if target=='Sbranch' else target,comp)
        return rr

def run(maxiter=100):
    U=JointTerminalUniverse();src=json.loads((HERE/'cg_terminal_cross_final.json').read_text());atoms=[];keys=set();cols=[];w=[];o=[]
    def add(a):
        key=atom_key(a)
        if key in keys:return False
        rr=U.atom_rows(a);cols.append([float(rr[n]) for n in U.names]);atoms.append(a);keys.add(key);w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])));return True
    checkpoint=HERE/'cg_joint_terminal.json'
    if checkpoint.exists():src=json.loads(checkpoint.read_text())
    for a in src['atoms']:add(a)
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.asarray(cols).T;out=linprog(-np.asarray(o,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[w],b_eq=[1.],bounds=(0,None),method='highs');assert out.success,out.message
        beta=-out.fun;lam=-out.ineqlin.marginals;minimum,new,contexts=U.price(lam,beta);count=sum(add(a) for _,a in new);rec={'iteration':it,'columns':len(atoms),'beta':beta,'pricing_minimum_scaled':float(minimum),'new_columns':count,'score_contexts':contexts,'seconds':time.time()-t0};history.append(rec);print(json.dumps(rec),flush=True)
        checkpoint.write_text(json.dumps({'scope':'728-row necessary-condition template with genuine shared matching cut; no SPE or true OPT claim','row_names':U.names,'atoms':atoms,'primal_float':out.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},'history':history},indent=2)+'\n')
        if count==0:break
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 100)

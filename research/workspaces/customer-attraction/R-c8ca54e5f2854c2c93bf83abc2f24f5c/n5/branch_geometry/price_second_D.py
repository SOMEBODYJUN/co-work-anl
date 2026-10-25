"""Full-domain floating column generation: historical 557 rows plus 7 genuine D2 rows.

No positive theorem is inferred from numerical convergence. An exact dual audit
would be required if a <=2 candidate were found.
"""
import importlib.util
import itertools
import json
import sys
import time
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
from separate_second_D import seven, NAMES, SOURCE

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
PEER=ROOT/"research/workspaces/customer-attraction/R-c4732bee2f7b4e50a70568170e3334ae/round4_pricing/full_pricing.py"
spec=importlib.util.spec_from_file_location("baseline_full_pricing",PEER)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)


class Extended(base.Universe):
    def __init__(self):
        super().__init__(1)
        self.base_names=list(self.names)
        self.names+=list("D2:"+n for n in NAMES)

    def atom_rows(self,atom):
        out=super().atom_rows(atom)
        out.update(zip(self.names[-7:],seven(atom,*atom["D2_bits"])))
        return out

    def price(self,lam,beta,batch=80):
        old=lam[:-7];new=lam[-7:]
        alpha,bbeta,gamma,delta,epsilon,zeta,eta=new
        weights=[(n,float(v)) for n,v in zip(self.base_names,old) if abs(v)>1e-11]
        fam={t:[] for t in ("AB","AE","Sbranch")}
        for n,v in weights:
            tag=n.split(":")[0]
            if tag in fam:fam[tag].append((n,v))
            elif ":sum-S" in n:fam["Sbranch"].append((n,v))
        ow=np.asarray(old)[self.oldids]
        fixedbase=self.base@ow;EC=self.ec@ow;HC=self.hc@ow
        cache={};best=[];minimum=1e100

        def family_result(bits,tag,extra):
            key,const,vec,me,mh=self.family_score(bits,tag,fam[tag])
            key2=(key,tuple(extra))
            k,p=key[:2]
            if key2 not in cache:
                score=np.zeros(len(self.hist[k]))
                for value,array in vec:score+=value*array
                for feature,value in extra:
                    if value:score+=value*self.M[k,p][feature]
                vals=[];idx=[]
                for ids in self.ids[k]:
                    arg=ids[int(np.argmax(score[ids]))];vals.append(score[arg]);idx.append(int(arg))
                cache[key2]=(np.asarray(vals),idx)
            vals,idx=cache[key2]
            return vals+const,idx,me,mh

        for bi,bits in enumerate(self.bits):
            a,b,c,d,e,*_=bits
            rootpart=120*alpha*float(base.q(b,sum(bits[:5])))
            ab,abidx,me,mh=family_result(bits,"AB",())
            E=EC[bi].copy()+me.T;H=HC[bi].copy()+mh.T
            # Old menu contributions do not depend on the new D2 memberships.
            ae_options={}
            for r,s in itertools.product((0,1),repeat=2):
                ae_options[r,s]=family_result(bits,"AE",(("zx",delta+epsilon),("dx",-delta*r-epsilon*s)))
            second_options={t:family_result(bits,"Sbranch",(("zu",zeta),("zv",eta),("du",-zeta*t),("dv",-eta*t))) for t in (0,1)}
            E+=ae_options[0,0][2].T+second_options[0][2].T
            H+=ae_options[0,0][3].T+second_options[0][3].T
            for j in range(6):
                corners=[(0,0),(j,j),(5-j,0),(5,j)];lhs=[];menus=0
                for f in range(3):
                    lh=max(corners,key=lambda lh:lh[0]*E[j,f]+lh[1]*H[j,f]);lhs.append(lh)
                    menus+=lh[0]*E[j,f]+lh[1]*H[j,f]
                for r,s,t in itertools.product((0,1),repeat=3):
                    ae,aeidx,_,_=ae_options[r,s];sec,secidx,_,_=second_options[t]
                    num=-alpha*d+(bbeta+5*gamma)*t
                    newshare=num/(a+d+r+s+t) if num else 0.
                    newfixed=120*(newshare-(bbeta*e+gamma*j)/(a+d+r+s+1))
                    residual=120*(beta*int(any(bits[:5]))-int(j>0))-fixedbase[bi,j]-menus-ab[j]-ae[j]-sec[j]-rootpart-newfixed
                    minimum=min(minimum,residual)
                    if residual < -1e-7:
                        atom={"bits":"".join(map(str,bits)),"AB_hist":list(self.hist[3][abidx[j]]),
                              "AE_hist":list(self.hist[3][aeidx[j]]),"second_hist":list(self.hist[4][secidx[j]]),
                              "menus_lh":lhs,"D2_bits":[r,s,t]}
                        best.append((residual,atom))
        best.sort(key=lambda z:z[0])
        for residual,atom in best[:batch]:
            direct=self.atom_rows(atom)
            rho=120*(beta*int(any(map(int,atom["bits"][:5])))-int(any(atom["AB_hist"][4:])))
            rho-=120*sum(float(v)*float(direct[n]) for n,v in zip(self.names,lam))
            assert abs(rho-residual)<1e-5,(rho,residual,atom)
        return minimum,best[:batch],len(cache)


def key(a):return base.atom_key(a)+(tuple(a["D2_bits"]),)


def main(maxiter=35):
    U=Extended();pr=json.loads(SOURCE.read_text())["primal"]
    atoms=[];keys=set();cols=[];ws=[];os=[]
    def add(a):
        kk=key(a)
        if kk in keys:return False
        rr=U.atom_rows(a)
        atoms.append(a);keys.add(kk);cols.append([float(rr[n]) for n in U.names])
        ws.append(int(any(map(int,a["bits"][:5]))));os.append(int(any(a["AB_hist"][4:])))
        return True
    sources=[pr["atoms"]]
    peer=PEER.parent/"exact_optimum_primal_overlap1.json"
    if peer.exists():sources.append(json.loads(peer.read_text())["atoms"])
    for source in sources:
        for a in source:
            old={k:a[k] for k in ("bits","AB_hist","AE_hist","second_hist","menus_lh")}
            for rst in itertools.product((0,1),repeat=3):add(dict(old,D2_bits=list(rst)))
    for j in (0,5):
        h3=[0]*8;h3[3 if j==0 else 7]=5;h4=[0]*16;h4[7 if j==0 else 15]=5
        add({"bits":"1111111111","AB_hist":h3,"AE_hist":h3,"second_hist":h4,"menus_lh":[(5,j)]*3,"D2_bits":[1,1,1]})
    history=[]
    for it in range(maxiter):
        t0=time.time();mat=np.asarray(cols).T
        out=linprog(-np.asarray(os,dtype=float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method="highs")
        if not out.success:raise RuntimeError(out.message)
        beta=-float(out.fun);lam=-out.ineqlin.marginals
        minimum,new,ncache=U.price(lam,beta,batch=100)
        count=sum(add(atom) for _,atom in new)
        rec={"iteration":it,"columns":len(atoms),"beta":beta,"pricing_minimum_scaled":float(minimum),"new_columns":count,"contexts":ncache,"seconds":time.time()-t0}
        history.append(rec);print(json.dumps(rec),flush=True)
        report={"scope":"Full 564-row floating necessary-condition relaxation; no theorem or SPE claim", "row_names":U.names,"atoms":atoms,"primal_float":out.x.tolist()+[0.]*count,"dual_beta_float":beta,"dual_multipliers_float":{n:float(v) for n,v in zip(U.names,lam) if v>1e-10},"history":history}
        (HERE/"cg_second_D.json").write_text(json.dumps(report,indent=2)+"\n")
        if count==0:break


if __name__=="__main__":main(int(sys.argv[1]) if len(sys.argv)>1 else 35)

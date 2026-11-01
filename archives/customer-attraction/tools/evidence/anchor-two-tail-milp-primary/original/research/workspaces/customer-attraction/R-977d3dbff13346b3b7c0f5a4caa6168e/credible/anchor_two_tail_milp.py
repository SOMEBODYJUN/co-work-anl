"""Inverse full-SPE MILP for the last fresh group of the two-tail scaffold.

Discovery only. Prefix C0 is fixed; three players remain; desired continuation
C1,D0,D1. All 111 decision histories and every deviation are represented.
No policy cone is frozen. A candidate needs exact full-history validation.
"""
from pathlib import Path
import argparse,json,sys,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
from anchor_general_cones import AnchorSearch

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seconds',type=float,default=120)
    ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();start=time.time()
    s=AnchorSearch(2,2);p=s.p;n=len(s.supports);actual=4;d0=8;d1=9
    # Correct bounds derived from current payoff 1 and universal 1/3
    # denominator guarantee: |Y0|,|Y1| <=2; |D0|,|D1|<=3; a<=2.
    # Hence each actual theme has size <=3 and all continuation payoffs <=3.
    lb=[];ub=[];integ=[];obj=[]
    def var(lo=0,hi=3,binary=False,cost=0):
        j=len(lb);lb.append(lo);ub.append(hi);integ.append(int(binary));obj.append(cost);return j
    w=[var(1,1),var(0,2,cost=-1)]+[var(0,3) for _ in range(n-2)]
    first=[[var() for b in range(p)] for a in range(p)]
    second=[[var() for b in range(p)] for a in range(p)]
    last=[[var() for b in range(p)] for a in range(p)]
    rootpay=[var(0,1) for a in range(p)];vsecond=[var() for a in range(p)]
    choose2=[[var(0,1,True) for b in range(p)] for a in range(p)]
    choose3=[[[var(0,1,True) for c in range(p)] for b in range(p)] for a in range(p)]
    rr=[];cc=[];vv=[];lower=[];upper=[]
    def row(d,lo=-np.inf,hi=np.inf):
        r=len(lower)
        for j,v in d.items():
            if v:rr.append(r);cc.append(j);vv.append(float(v))
        lower.append(lo);upper.append(hi)
    # Anchor membership columns are ordered by nonempty 4-bit core masks.
    for bit,bound in [(0,2),(1,2),(2,3),(3,3)]:
        row({w[mask+1]:1 for mask in range(1,16) if mask>>bit&1},hi=bound)
    def coeff(a,b,c,who):
        q=[0]*p;q[0]=1;q[a]+=1;q[b]+=1;q[c]+=1
        # AnchorSearch was built with 4 players, so q is a legal terminal.
        return s.pay[s.leaf_index[tuple(q)],who]/s.scale
    def conditional_equal(value,co,z):
        terms={value:1,z:3}
        for j,x in zip(w,co):terms[j]=terms.get(j,0)-x
        row(terms,hi=3)
        terms={value:1,z:-3}
        for j,x in zip(w,co):terms[j]=terms.get(j,0)-x
        row(terms,lo=-3)
    for a in range(p):
        row({choose2[a][b]:1 for b in range(p)},1,1)
        for b in range(p):
            z2=choose2[a][b]
            row({vsecond[a]:1,second[a][b]:-1},lo=0)
            row({vsecond[a]:1,second[a][b]:-1,z2:3},hi=3)
            row({rootpay[a]:1,first[a][b]:-1,z2:3},hi=3)
            row({rootpay[a]:1,first[a][b]:-1,z2:-3},lo=-3)
            row({choose3[a][b][c]:1 for c in range(p)},1,1)
            for c in range(p):
                z3=choose3[a][b][c]
                conditional_equal(first[a][b],coeff(a,b,c,a),z3)
                conditional_equal(second[a][b],coeff(a,b,c,b),z3)
                co=coeff(a,b,c,c);conditional_equal(last[a][b],co,z3)
                terms={last[a][b]:1}
                for j,x in zip(w,co):terms[j]=terms.get(j,0)-x
                row(terms,lo=0)
    lb[choose2[actual][d0]]=ub[choose2[actual][d0]]=1
    lb[choose3[actual][d0][d1]]=ub[choose3[actual][d0][d1]]=1
    matrix=coo_matrix((vv,(rr,cc)),shape=(len(lower),len(lb))).tocsc()
    result=milp(np.array(obj),integrality=np.array(integ),bounds=Bounds(lb,ub),
                constraints=LinearConstraint(matrix,lower,upper),options={'time_limit':args.seconds,'mip_rel_gap':1e-7})
    data={'status':int(result.status),'message':str(result.message),'variables':len(lb),'rows':len(lower),'seconds':time.time()-start,
          'mathematical_status':'MILP discovery only; no exact feasibility or universal dual certificate claimed'}
    if result.x is not None:
        data.update(a=float(result.x[w[1]]),weights=[float(result.x[j]) for j in w],
                    choose2=[int(np.argmax([result.x[z] for z in row])) for row in choose2],
                    choose3=[[int(np.argmax([result.x[z] for z in row])) for row in block] for block in choose3])
    for name in ['mip_gap','mip_node_count','mip_dual_bound']:
        if hasattr(result,name):data[name]=getattr(result,name)
    args.output.write_text(json.dumps(data,indent=2));print(json.dumps({k:v for k,v in data.items() if k not in ['weights','choose2','choose3']}),flush=True)

if __name__=='__main__':main()

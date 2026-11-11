"""Main's unified sparse exact dual, all free weights; no optimizer or game point."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent

def remainder(r, typ, p):
    n,k,x,*tail = typ
    ys,t,q = tail[:-2],tail[-2],tail[-1]
    j,D = sum(ys),n+r-1
    alpha,safe,maximum,delta = p[0],p[1:r],p[r:2*r-1],p[-1]
    C = alpha + sum(safe)
    return (alpha*F(x,n+j+t) +
            sum((s*F(y,D) for s,y in zip(safe,ys+[t])),F()) -
            (C-1)*F(x,D) - q*(F(x,D)+F(1-x,n)) -
            sum((a*F(x-y,n+k) for a,y in zip(maximum,ys+[t])),F()) -
            delta*F(t-q,n+x+j))

def main():
    result=[]
    for r in (4,5,6):
        m,N=r-2,7-r
        ca=F(r*(-r*r+14*r-21),2*(r-1))
        cg,ch=F(r*(6*r-11),r-1),F(30*m,r-1)
        cb,cd=F(r,m),F(r*(r-1),m)
        rho=F(30*m,N*(r-1))-F(r*(6*r-11),(r-1)**2)
        Cstar=F(r**3+10*r*r-31*r+22,2*(r-1))
        assert min(ca,cg,ch,cb,cd,rho)>0
        types=[(n,k,*b) for n in range(1,N+1) for k in range(m+1)
               for b in product(range(2),repeat=r+1)]
        support=[('A',(1,0,0,*([0]*m),0,1),ca),
                 ('G',(1,m,0,*([0]*m),1,0),cg),
                 ('H',(N,0,1,*([1]*m),0,0),ch)]
        for j in range(m):
            e=[int(i==j) for i in range(m)]
            support += [(f'B{j+1}',(1,0,1,*(1-v for v in e),1,0),cb),
                        (f'D{j+1}',(1,m,0,*e,0,1),cd)]
        assert len({t for _,t,_ in support})==2*m+3
        zero=[F() for _ in range(2*r)]
        basis=[zero]+[[F(int(i==j)) for i in range(2*r)] for j in range(2*r)]
        checks=[]
        for p in basis:
            lhs=sum(p[:r])-Cstar
            rhs=sum((w*remainder(r,t,p) for _,t,w in support),F())+rho*p[-2]
            assert lhs==rhs
            for name,t,w in support:
                alpha,st,at,delta=p[0],p[r-1],p[-2],p[-1]
                if name=='A': closed=delta-1
                elif name=='G': closed=st/r+at/(r-1)-delta
                elif name=='H': closed=alpha/30-st/6+F(1,6)-at/N
                else:
                    j=int(name[1:])-1
                    s,a=p[1+j],p[r+j]
                    closed=(alpha/F(r*(r-1))-s/r-a+F(1,r)-delta/(r-1)
                            if name.startswith('B') else s/r+a/(r-1)+delta/2-1)
                assert remainder(r,t,p)==closed
            checks.append(str(lhs))
        a=F(-r*r+11*r-12,2*r*m)
        s=F(r,2)-F(r,r-1)*a
        primal=[F(5*(r-1))]+[s]*m+[F(r)]+[a]*m+[F(),F(1)]
        assert sum(primal[:r])==Cstar and min(primal)>=0
        vals=[remainder(r,t,primal) for t in types]
        assert min(vals)>=0
        assert all(remainder(r,t,primal)==0 for _,t,_ in support)
        assert s/r+a/(r-1)==F(1,2)
        assert s+r*a==F(primal[0]-1,r-1)
        det=F(1,r)*r-F(1,r-1)
        assert det==F(r-2,r-1)>0
        result.append({'r':r,'variables':2*r,'types':len(types),'C':str(Cstar),
            'support':[{'name':name,'type':t,'row_index':types.index(t),'weight':str(w)}
                       for name,t,w in support],
            'positive_reduced_cost_for_terminal_MAX':str(rho),
            'affine_basis_checks':len(checks),'unique_primal':list(map(str,primal)),
            'zero_types':sum(v==0 for v in vals),'min_positive_remainder':str(min(v for v in vals if v>0)),
            'uniqueness_determinant':str(det)})
    out={'status':'PASS_UNIFORM_DUAL_AND_UNIQUE_OPTIMA','optimizer_calls':0,
         'game_point_reads':0,'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'source_proof_sha256':sha256((HERE/'main_prefix_safety_maxx_family.md').read_bytes()).hexdigest(),
         'results':result,'scope':'Specified nonnegative pointwise SAFE/MAX cones only; no SPE sharpness.'}
    target=HERE/'main_prefix_cone_uniform_dual.json'
    assert not target.exists()
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='results'},ensure_ascii=False))

if __name__=='__main__':
    main()


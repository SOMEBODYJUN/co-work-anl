"""Independent exact preliminary audit; not a production EPTAS or its universal proof.
Original algebraic core preserved; command-line output replaces temporary paths.
"""
from fractions import Fraction as F
from itertools import product
from random import Random
import json
from pathlib import Path
import argparse
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from tests.audits.near_band_completion_independent import near_select
C={'instances':0,'layouts':0,'full_cells_examined':0,'far_patterns_examined':0,'near_patterns_examined':0,'conditional_cost_comparisons':0,'facility_deviations':0}

def local(clients,s,t):
    a=sum(w for w,A in clients if s in A and t not in A)
    b=sum(w for w,A in clients if t in A and s not in A)
    ww=[w for w,A in clients if s in A and t in A]
    return F(a),F(b),ww

def onecell(a,b,ww,st,lo,hi):
    m=st.count(0);D=a-b+sum(w*x for w,x in zip(ww,st))
    for w,x in zip(ww,st):
        if x!=1:lo=max(lo,-w)
        if x!=-1:hi=min(hi,w)
    if m==1:
        if D:return None
    else:
        d=D/(1-m);lo=max(lo,d);hi=min(hi,d)
    if lo>hi:return None
    def probabilities(d, st=st, ww=ww):
        return [F(1) if x==1 else F(0) if x==-1 else (1+d/w)/2 for w,x in zip(ww,st)]
    return (lo,hi,probabilities)

def check(a,b,ww,pp):
    X=a+sum(w*p for w,p in zip(ww,pp));Y=b+sum(w*(1-p) for w,p in zip(ww,pp))
    for i,(w,p) in enumerate(zip(ww,pp)):
        c1=a+w+sum(v*pp[j] for j,v in enumerate(ww) if j!=i)
        c2=b+w+sum(v*(1-pp[j]) for j,v in enumerate(ww) if j!=i)
        assert 0<=p<=1 and (p==0 or c1<=c2) and (p==1 or c2<=c1)
        C['conditional_cost_comparisons']+=2
    return X,Y

def allcells(a,b,ww):
    W=a+b+sum(ww);out=[]
    for st in product((-1,0,1),repeat=len(ww)):
        C['full_cells_examined']+=1
        cell=onecell(a,b,ww,st,-W,W)
        if cell:
            for d in set(cell[:2]):assert check(a,b,ww,cell[2](d))[0]-check(a,b,ww,cell[2](d))[1]==d
            out.append(cell)
    assert out
    return out

def smallmenu(a,b,ww,eta):
    W=a+b+sum(ww);H=eta*W;heavy=[i for i,w in enumerate(ww) if w>H];out=[]
    if W==0:return [(F(0),F(0),lambda d:[])]
    for pat in product((-1,0,1),repeat=len(heavy)):
        C['near_patterns_examined']+=1
        pp=near_select(a,b,ww,H,heavy,pat)
        if pp is not None:
            X,Y=check(a,b,ww,pp);d=X-Y
            out.append((d,d,lambda delta, pp=pp:list(pp)))
        for sig in (-1,1):
            C['far_patterns_examined']+=1
            st=[-sig]*len(ww)
            for i,x in zip(heavy,pat):st[i]=x
            lo,hi=(H,W) if sig==1 else (-W,-H)
            cell=onecell(a,b,ww,tuple(st),lo,hi)
            if cell:
                for d in set(cell[:2]):check(a,b,ww,cell[2](d))
                out.append(cell)
    assert out
    return out

def ratio(num,den):
    if den:return num/den
    return F(0) if num==0 else None

def solve(S,clients,menus):
    loads={(s,t):sum(w for w,A in clients if s in A or t in A) for s,t in product(S,repeat=2)}
    mins={}
    for s,t in product(S,repeat=2):
        W=loads[(s,t)];cells=menus[(s,t)]
        c1=min(cells,key=lambda c:c[0]);c2=max(cells,key=lambda c:c[1])
        mins[(s,t)]=((W+c1[0])/2,(W-c2[1])/2,c1,c2)
    D1={t:max(mins[(r,t)][0] for r in S) for t in S}
    D2={s:max(mins[(s,r)][1] for r in S) for s in S}
    best=None;result=None
    for s,t in product(S,repeat=2):
        W=loads[(s,t)];u=D1[t];v=D2[s]
        target=W*(u-v)/(u+v) if u+v else F(0)
        for cell in menus[(s,t)]:
            d=max(cell[0],min(cell[1],target));x=(W+d)/2;y=(W-d)/2
            r1,r2=ratio(u,x),ratio(v,y)
            if r1 is None or r2 is None:continue
            score=max(F(1),r1,r2)
            if best is None or score<best:best=score;result=(s,t,d,cell)
    return best,result,mins,D1,D2

def actual(S,clients,menus,result,mins):
    s,t,d,cell=result;table={}
    for r,z in product(S,repeat=2):
        if (r,z)==(s,t):c=cell;delta=d
        elif z==t and r!=s:c=mins[(r,z)][2];delta=c[0]
        elif r==s and z!=t:c=mins[(r,z)][3];delta=c[1]
        else:c=menus[(r,z)][0];delta=c[0]
        a,b,ww=local(clients,r,z);table[(r,z)]=check(a,b,ww,c[2](delta))
    x,y=table[(s,t)];score=F(1)
    for r in S:
        if r!=s:
            rr=ratio(table[(r,t)][0],x);assert rr is not None
            score=max(score,rr);C['facility_deviations']+=1
        if r!=t:
            rr=ratio(table[(s,r)][1],y);assert rr is not None
            score=max(score,rr);C['facility_deviations']+=1
    return score

rng=Random(20261009003);graphs=[];S=tuple(range(4))
for _ in range(180):
    k=rng.randrange(0,7);clients=[]
    for i in range(k):
        w=F(rng.randrange(1,40),rng.choice([1,2,3,20,2**30]))
        A=tuple(s for s in S if rng.random()<.6)
        clients.append((w,A))
    graphs.append(clients)
# The no-FPTAS core/guards, all coverage equal, no coverage, one positive atom,
# and tiny payoff denominators.
for src in [(1,1),(1,2),(1,2,4)]:
    n=2*max(len(src),2);T=sum(src);aa=list(src)+[0]*(n-len(src))
    ws=[1+F(n*x-T,16*n*n*T) for x in aa]
    M=F(5*n,2);q=F(13,20*n);R=F(143*n*n+13,40*n)
    cs=[(M,S)]+[(w,(0,1)) for w in ws]+[(q,(2,0)),(n-q,(0,)),(F(n),(1,)),(R-M-q,(2,)),(F(n,5),(3,))]
    graphs.append(cs)
graphs += [[(F(10),S)],[(F(10),()),(F(1,2**40),())],[(F(2), (0,1)),(F(1,2**50),(2,3))]]
rows=[]
for clients in graphs:
    full={};menu={};eta=rng.choice([F(1,8),F(1,4),F(1,2)])
    for s,t in product(S,repeat=2):
        a,b,ww=local(clients,s,t);full[(s,t)]=allcells(a,b,ww);menu[(s,t)]=smallmenu(a,b,ww,eta)
        C['layouts']+=1
    opt,_,m,D1,D2=solve(S,clients,full)
    val,result,mhat,U1,U2=solve(S,clients,menu)
    c=(1+eta)/(1-eta)
    for key in m:
        for j in (0,1):assert m[key][j]<=mhat[key][j]<=c*m[key][j],(key,m[key][:2],mhat[key][:2],eta)
    for s in S:
        assert D1[s]<=U1[s]<=c*D1[s] and D2[s]<=U2[s]<=c*D2[s]
    act=actual(S,clients,menu,result,mhat)
    assert act<=val<=c*c*opt,(clients,eta,opt,val,act)
    assert opt<=2
    rows.append({'eta':str(eta),'optimal_alpha':str(opt),'menu_bound':str(val),'actual_alpha':str(act)})
    C['instances']+=1
report={'counts':C,'seed':20261009003,'results':rows,'status':'all assertions passed; finite audit only'}
parser=argparse.ArgumentParser()
parser.add_argument("--output",type=Path)
args=parser.parse_args()
if args.output:
    if args.output.exists():
        raise FileExistsError("frozen evidence must not be overwritten")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({'counts':C,'status':report['status']},indent=2))

"""Second independently reconstructed exact audit; no canonical solver or constructor imports.
Finite checks only. Run from any working directory; frozen report defaults to stdout.
"""
from fractions import Fraction as F
from itertools import product
import json

from pathlib import Path
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("--output",type=Path)
args=parser.parse_args()
S=('B','C','A','D')
COUNTS={'sources':0,'support_cells_examined':0,'accepted_cells':0,'conditional_cost_comparisons':0,'yes':0,'no':0,'yes_certificate_deviations':0}

def setup(src):
    t=len(src); n=2*max(t,2); T=sum(src); aa=list(src)+[0]*(n-t)
    w=[F(1)+F(n*a-T,16*n*n*T) for a in aa]
    M=F(5*n,2); V=F(11*n,2); tau=F(1,2*n)
    q=F(13,20*n); R=F(143*n*n+13,40*n); d=F(27*n,10)
    clients=[('big',M,tuple(S))]+[(f'v{i}',v,('B','C')) for i,v in enumerate(w)]
    clients += [('cross',q,('A','B')),('Bprivate',n-q,('B',)),('Cprivate',F(n),('C',)),('Aprivate',R-M-q,('A',)),('Dprivate',F(n,5),('D',))]
    assert len(clients)==n+6 and all(v>0 for _,v,_ in clients)
    rb=sum(v for _,v,a in clients if 'B' in a); rc=sum(v for _,v,a in clients if 'C' in a)
    ra=sum(v for _,v,a in clients if 'A' in a); rd=sum(v for _,v,a in clients if 'D' in a)
    assert (rb,rc,ra,rd)==(F(9*n,2),F(9*n,2),R,d)
    assert sum(w)==n and sum(abs(v-1) for v in w)<=F(1,8*n)
    assert R-q==F(13,10)*(V-tau)/2 and 2*R-q==F(13,10)*V
    assert F(9*n,2)>R>d>M and R-q>d>F(9*n,4) and R>2*n
    return n,T,w,M,V,tau,q,R,d,clients

def locals_data(clients,s,t):
    common=[(name,v) for name,v,a in clients if s in a and t in a]
    a=sum(v for _,v,r in clients if s in r and t not in r)
    b=sum(v for _,v,r in clients if t in r and s not in r)
    return F(a),F(b),common

def check_ne(a,b,common,pp):
    X=a+sum(v*p for (_,v),p in zip(common,pp));Y=b+sum(v*(1-p) for (_,v),p in zip(common,pp))
    for i,((name,v),p) in enumerate(zip(common,pp)):
        c1=a+v+sum(u*pp[j] for j,(_,u) in enumerate(common) if j!=i)
        c2=b+v+sum(u*(1-pp[j]) for j,(_,u) in enumerate(common) if j!=i)
        assert c1==X+(1-p)*v and c2==Y+p*v
        assert (p==0 or c1<=c2) and (p==1 or c2<=c1), (name,v,p,c1,c2)
        COUNTS['conditional_cost_comparisons']+=2
    return X,Y

def cells(clients,s,t):
    a,b,common=locals_data(clients,s,t); vv=[v for _,v in common]
    out=[]
    # State -1 = pure second, 0 = nominal mixed, 1 = pure first.
    for st in product((-1,0,1),repeat=len(vv)):
        COUNTS['support_cells_examined']+=1
        m=st.count(0); z=sum(v*x for v,x in zip(vv,st) if x)
        if m==1:
            if a-b+z:continue
            lo=max([-v for v,x in zip(vv,st) if x<=0] or [-sum(vv)-a-b])
            hi=min([v for v,x in zip(vv,st) if x>=0] or [sum(vv)+a+b])
            if lo>hi:continue
        else:
            lo=hi=(a-b+z)/(1-m)
            if any((x==1 and lo>v) or (x==-1 and lo<-v) or (x==0 and not -v<=lo<=v) for v,x in zip(vv,st)):continue
        pp=lambda delta, st=st, vv=vv: [F(1) if x==1 else F(0) if x==-1 else (1+delta/v)/2 for v,x in zip(vv,st)]
        for delta in {lo,hi}:
            x,y=check_ne(a,b,common,pp(delta))
            assert x-y==delta
        COUNTS['accepted_cells']+=1
        out.append((lo,hi,st,pp))
    assert out
    return a,b,common,out

def partition(src):
    T=sum(src)
    for st in product((0,1),repeat=len(src)):
        if 2*sum(a*x for a,x in zip(src,st))==T:
            return [i for i,x in enumerate(st) if x]
    return None

def proof_bounds(n,R,q,d):
    bounds=[F(27,20),(R-q)/d,F(2*n)/(R-F(5*n,2)),(R-q)/F(9*n,4),R/F(9*n,4),2*d/R,F(40,27)]
    assert all(v>F(131,100) for v in bounds)
    return bounds

def actual_certificate(clients,pmap,path=('B','C')):
    loads={}
    for s,t in product(S,repeat=2):
        a,b,common=locals_data(clients,s,t)
        pp=[pmap[(s,t)][name] for name,_ in common]
        loads[(s,t)]=check_ne(a,b,common,pp)
    s,t=path; x,y=loads[(s,t)]; ratios=[F(1)]
    for r in S:
        if r!=s:ratios.append(loads[(r,t)][0]/x);COUNTS['yes_certificate_deviations']+=1
        if r!=t:ratios.append(loads[(s,r)][1]/y);COUNTS['yes_certificate_deviations']+=1
    return max(ratios)

cases=[(1,),(2,),(1,1),(1,2),(1,3),(2,2),(2,3),(3,5),(1,1,2),(1,2,4),(2,3,5),(1,1,1),(2,2,3),(1,1,1,1),(1,2,3,6),(1,2,4,8),(7,7,13,1),(1,10**12+1),(10**12+1,10**12+1)]
rows=[]
for src in cases:
    n,T,w,M,V,tau,q,R,d,clients=setup(src);yes=partition(src)
    isyes=yes is not None;COUNTS['sources']+=1;COUNTS['yes' if isyes else 'no']+=1
    Q=80*n*n*T;ints=[v*Q for _,v,_ in clients]
    expected=[200*n**3*T]+[80*n*n*T+5*n*a-5*T for a in list(src)+[0]*(n-len(src))]+[52*n*T,80*n**3*T-52*n*T,80*n**3*T,86*n**3*T-26*n*T,16*n**3*T]
    assert ints==expected and all(v.denominator==1 and v>0 for v in ints)
    intclients=[(name,v*Q,aa) for name,v,aa in clients]
    ppmap={}; price={('B','A'):(F(2*n),R-q),('C','A'):(F(2*n),R),('B','D'):(F(2*n),d),('C','D'):(F(2*n),d),('A','D'):(R-M,d)}
    for (s,t),want in price.items():
        a,b,common,allcells=cells(clients,s,t)
        pset=set()
        for lo,hi,_,pp in allcells:
            assert lo==hi
            p=tuple(pp(lo));pset.add(p)
            assert check_ne(a,b,common,p)==want
        assert len(pset)==1
        p=next(iter(pset));ppmap[(s,t)]={name:x for (name,_),x in zip(common,p)}
        ppmap[(t,s)]={name:1-x for (name,_),x in zip(common,p)}
    a,b,common,core=cells(clients,'B','C')
    best=None;one_mixed=0
    for lo,hi,st,pp in core:
        one_mixed+=st.count(0)==1
        delta=max(lo,min(hi,tau));p=pp(delta);x,y=check_ne(a,b,common,p)
        amin=max(F(1),R/x,(R-q)/y)
        best=amin if best is None else min(best,amin)
        if not isyes:
            assert st.count(0)!=1
            assert abs(delta-tau)>=F(3,8*n)
            assert amin>=F(13,10)+F(1,44*n*n)
        ai,bi,ci=locals_data(intclients,'B','C');ix,iy=check_ne(ai,bi,ci,p)
        assert (ix,iy)==(Q*x,Q*y)
    proof_bounds(n,R,q,d)
    if isyes:
        assert best==F(13,10)
        chosen=set(yes);chosen.update(range(len(src),len(src)+n//2-len(yes)))
        assert len(chosen)==n//2 and sum(w[i] for i in chosen)==F(n,2)
        probs={'big':F(1,2)+F(1,10*n*n)}
        probs.update({f'v{i}':F(i in chosen) for i in range(n)})
        ppmap[('B','C')]=probs;ppmap[('C','B')]={name:1-p for name,p in probs.items()}
        for s in S:
            _,_,cc=locals_data(clients,s,s)
            ppmap[(s,s)]={name:F(1,2) for name,_ in cc}
        assert actual_certificate(clients,ppmap)==F(13,10)
        assert actual_certificate(intclients,ppmap)==F(13,10)
    else:
        assert best>=F(13,10)+F(1,100*n*n)
    rows.append({'source':src,'n':n,'yes':isyes,'core_cells':len(core),'core_guard_lower_bound':str(best),'one_nominal_mixed_cells':one_mixed})
report={'counts':COUNTS,'cases':rows,'status':'all assertions passed; finite audit only'}
if args.output:
    if args.output.exists():
        raise FileExistsError("frozen evidence must not be overwritten")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))

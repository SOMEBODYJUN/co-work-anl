#!/usr/bin/env python3
"""New exact finite reconstruction of separate interfaces in the current paper.

Menu C is supplied by exhaustive local support enumeration, NOT a recovered
implementation of the manuscript's polynomial chord constructor. Global
finite menu checks do not close the pending arbitrary-cycle proof review.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
stats=Counter()


def sgn(x):return (x>0)-(x<0)


def affine_q_sign(a,b):
    """Sign(a+b*q), q>0 and q*q+q=1, using only rational arithmetic."""
    a,b=F(a),F(b)
    if not b:return sgn(a)
    z=-a/b
    z_minus_q=-1 if z<0 else sgn(z*z+z-1)
    return -sgn(b)*z_minus_q


def pair_ends(v,c,i,j):
    b=c[i]+c[j]
    lo=max(-v[i],b-v[j]);hi=min(v[i],b+v[j])
    return ((lo,b-lo),(hi,b-hi))


def exchange(v,t):
    v=list(map(F,v));t=F(t);assert abs(t)<=sum(v)
    c=[-x for x in v];remaining=t+sum(v)
    for i,x in enumerate(v):
        step=min(2*x,remaining);c[i]+=step;remaining-=step
    moves=0;changes=0;seen=set()
    while True:
        assert sum(c)==t and all(abs(x)<=w for x,w in zip(c,v))
        piv=[i for i,x in enumerate(c) if abs(x)<v[i]];assert len(piv)<=1
        assert tuple(c) not in seen;seen.add(tuple(c))
        if not piv:break
        j=piv[0];z=v[j];d=c[j];move=None
        for i in range(len(v)):
            if i==j:continue
            ends=pair_ends(v,c,j,i);other=next((p for p in ends if p!=(c[j],c[i])),None)
            if other and sum(x*x for x in other)>c[j]*c[j]+c[i]*c[i]:move=(i,other);break
        if move is None:break
        i,(cj,ci)=move;s=sgn(c[i]);old=c[j]*c[j]+c[i]*c[i];c[j],c[i]=cj,ci
        assert c[j]*c[j]+c[i]*c[i]>old
        newpiv=[h for h,x in enumerate(c) if abs(x)<v[h]]
        if newpiv and newpiv[0]!=j:
            assert newpiv[0]==i and v[i]<z
            assert c[j]*c[j]+c[i]*c[i]-old==2*(z-s*d)*(z-v[i]);changes+=1
        elif newpiv:
            assert abs(c[j])>abs(d)
        moves+=1;assert moves<=(len(v)+1)**3
    for i,j in combinations(range(len(v)),2):
        assert all(x*x+y*y<=c[i]*c[i]+c[j]*c[j] for x,y in pair_ends(v,c,i,j))
    piv=[i for i,x in enumerate(c) if abs(x)<v[i]]
    if piv:
        j=piv[0];d=c[j];z=v[j]
        for i,x in enumerate(c):
            if i==j:continue
            assert d<=v[i] if x>0 else d>=-v[i]
            if d>0:
                assert v[i]>=z if x>0 else (v[i]>=z or v[i]<=d)
            if d<0:
                assert v[i]>=z if x<0 else (v[i]>=z or v[i]<=-d)
    return tuple(c),moves,changes


box_cases=0;max_moves=0;pivot_changes=0
for m in range(5):
    for v in product((1,2,3),repeat=m):
        total=sum(v)
        for twice_t in range(-2*total,2*total+1):
            c,moves,changes=exchange(v,F(twice_t,2));box_cases+=1;max_moves=max(max_moves,moves);pivot_changes+=changes
v=tuple(map(F,(14,13,19)));local=tuple(map(F,(14,-5,-19)));better=tuple(map(F,(-14,-13,17)))
assert sum(local)==sum(better)==-10
assert all(x*x+y*y<=local[i]**2+local[j]**2 for i,j in combinations(range(3),2) for x,y in pair_ends(v,local,i,j))
assert sum(x*x for x in local)==582<654==sum(x*x for x in better)


def load(A,B,w,p):
    return F(A)+sum(x*y for x,y in zip(w,p)),F(B)+sum(x*(1-y) for x,y in zip(w,p))


def ne(A,B,w,p):
    L,R=load(A,B,w,p);gap=L-R
    return all(gap<=x if y==1 else gap>=-x if y==0 else gap==x*(2*y-1) for x,y in zip(w,p))


def pure_repair(A,B,w,p,guarded=False):
    p=list(p);L,R=load(A,B,w,p);oldlo=min(L,R);oldhi=max(L,R);lower=0 if L<R else 1
    if guarded and L!=R:
        assert all(x>=oldhi-oldlo for x,y in zip(w,p) if y==(1 if lower==0 else 0))
    moved=[];seen=set()
    while True:
        assert tuple(p) not in seen;seen.add(tuple(p));L,R=load(A,B,w,p)
        eligible=[i for i,(x,y) in enumerate(zip(w,p)) if y==1 and L>R+x or y==0 and R>L+x]
        if not eligible:break
        i=min(eligible,key=lambda i:(-w[i],i));before=abs(L-R);p[i]=1-p[i];L2,R2=load(A,B,w,p)
        assert abs(L2-R2)<before and min(L2,R2)>min(L,R) and max(L2,R2)<max(L,R)
        assert i not in moved;moved.append(i);assert len(moved)<=len(w)
        if guarded and ((lower==0 and L2>R2) or (lower==1 and R2>L2)):break
    assert ne(A,B,w,p)
    if guarded and oldlo<oldhi:
        L,R=load(A,B,w,p);assert min(L,R)>=oldlo and (L if lower==0 else R)<oldhi
    return tuple(p),len(moved)


def local_chord_hyp(A,B,w):
    U=F(A)+sum(w);V=F(B)+sum(w)
    if U<V:return local_chord_hyp(B,A,w)
    return U>0 and affine_q_sign(2*V-U,-U)>0 and affine_q_sign(-sum(w),V)>0 and all(affine_q_sign(U-x,-U)>=0 for x in w)


def quota(A,B,w,p):
    U=F(A)+sum(w);V=F(B)+sum(w);L,R=load(A,B,w,p)
    return affine_q_sign(L,-V)>=0 and affine_q_sign(R,-U)>=0


def supports(A,B,w):
    """One representative per discrete status; single-mixer continuum uses gap 0."""
    delta=F(A)-F(B)
    for status in product((-1,0,1),repeat=len(w)):
        mixed=[i for i,s in enumerate(status) if s==0];pure=sum((w[i]*s for i,s in enumerate(status)),F(0));r=len(mixed)
        if r==1:
            if delta+pure:continue
            gap=F(0)
        else:gap=-(delta+pure)/(r-1)
        p=tuple(F(1) if s==1 else F(0) if s==-1 else (1+gap/w[i])/2 for i,s in enumerate(status))
        if all(0<=x<=1 for x in p) and ne(A,B,w,p):yield status,p


def menu(A,B,w):
    A,B=F(A),F(B);w=tuple(map(F,w));k=len(w);result=[]
    seeds=[(1,)*k,(0,)*k]
    for h in range(k):seeds += [tuple(int(i==h) for i in range(k)),tuple(int(i!=h) for i in range(k))]
    for p in seeds:
        if ne(A,B,w,p):result.append(('P',p));continue
        L,R=load(A,B,w,p);g=abs(L-R);lower=1 if L<R else 0
        if all(x>=g for x,y in zip(w,p) if y==lower):
            q,steps=pure_repair(A,B,w,p,True);result.append(('P',q));stats['guarded_repairs']+=1;stats['guarded_moves']+=steps
    if A==B:result.append(('E',(F(1,2),)*k))
    for h,j in combinations(range(k),2):
        for reflect in ((False,True) if A==B else (A>B,)):
            a,b=(B,A) if reflect else (A,B);D=b-a+sum(w)-w[h]-w[j]
            if D<=min(w[h],w[j]):
                p=[F(0)]*k;p[h]=(1+D/w[h])/2;p[j]=(1+D/w[j])/2
                if reflect:p=[1-x for x in p]
                result.append(('T',tuple(p)))
    if local_chord_hyp(A,B,w):
        p=next((p for st,p in supports(A,B,w) if quota(A,B,w,p)),None)
        assert p is not None;result.append(('C_support_enumeration',p));stats['finite_C_calls']+=1
    assert any(tag=='P' for tag,p in result)
    assert all(ne(A,B,w,p) for tag,p in result)
    return result


local_pairs=0;repair_seeds=0;max_pure_moves=0
for k in range(5):
    for w in product((F(1),F(2),F(3)),repeat=k):
        for A,B in product((0,2,5),repeat=2):
            result=menu(A,B,w);local_pairs+=1
            for p in product((0,1),repeat=k):
                terminal,steps=pure_repair(A,B,w,p);repair_seeds+=1;max_pure_moves=max(max_pure_moves,steps)

# The manuscript's three-mixer fixture, with all smaller supports explicitly checked.
w=(F(20),)*3;ps=list(supports(40,39,w));good=[(st,p) for st,p in ps if quota(40,39,w,p)]
assert good and all(sum(s==0 for s in st)==3 for st,p in good)
assert (F(39,80),)*3 in [p for st,p in good]
assert load(40,39,w,(F(39,80),)*3)==(F(277,4),F(279,4))

# Full finite catalogs: menus fixed pairwise before computing full-catalog d.
catalog_records=[];cycle_checks=0
def catalog(weights,coverage):
    global cycle_checks
    n=len(weights);N=len(coverage);Fpair={}
    for s in range(N):
        for t in range(s,N):
            common=sorted(coverage[s]&coverage[t]);w=tuple(F(weights[i]) for i in common)
            A=sum(weights[i] for i in coverage[s]-coverage[t]);B=sum(weights[i] for i in coverage[t]-coverage[s])
            entries=[{'family':tag,'common':common,'p':p,'loads':load(A,B,w,p)} for tag,p in menu(A,B,w)]
            Fpair[s,t]=entries
            if s!=t:Fpair[t,s]=[{'family':e['family'],'common':common,'p':tuple(1-x for x in e['p']),'loads':tuple(reversed(e['loads']))} for e in entries]
    u={(s,t):min(e['loads'][0] for e in Fpair[s,t]) for s in range(N) for t in range(N)}
    d=[max(u[s,t] for s in range(N)) for t in range(N)];b=[min(s for s in range(N) if u[s,t]==d[t]) for t in range(N)]
    def witness(vertices):
        return next(((s,t,e) for s in vertices for t in vertices for e in Fpair[s,t]
                     if affine_q_sign(e['loads'][0],-d[t])>=0 and affine_q_sign(e['loads'][1],-d[s])>=0),None)
    chosen=witness(range(N));assert chosen
    cycles=set()
    for start in range(N):
        seen=[];x=start
        while x not in seen:seen.append(x);x=b[x]
        cyc=seen[seen.index(x):];key=tuple(sorted(cyc))
        if key not in cycles:assert witness(cyc);cycles.add(key);cycle_checks+=1
    s,t,e=chosen;continuations={(s,t):e}
    for r in range(N):
        if r!=s:
            dest=(r,t);assert dest not in continuations
            z=min(Fpair[dest],key=lambda x:x['loads'][0]);continuations[dest]=z
            assert affine_q_sign(e['loads'][0],-z['loads'][0])>=0
        if r!=t:
            dest=(s,r);assert dest not in continuations
            z=min(Fpair[dest],key=lambda x:x['loads'][1]);continuations[dest]=z
            assert affine_q_sign(e['loads'][1],-z['loads'][1])>=0
    for dest,entries in Fpair.items():
        if dest not in continuations:continuations[dest]=next(x for x in entries if x['family']=='P')
    assert len(continuations)==N*N
    catalog_records.append({'weights':list(map(str,weights)),'coverage':[sorted(c) for c in coverage],
                            'd':list(map(str,d)),'b':b,'chosen':[s,t],'onpath_loads':list(map(str,e['loads'])),
                            'complete_ordered_layouts':N*N,'cycle_count':len(cycles)})
for weights in product((1,3),repeat=2):
    for masks in product(range(8),repeat=2):catalog(weights,tuple(frozenset(i for i,b in enumerate(masks) if b&(1<<s)) for s in range(3)))
for masks in product(range(4),repeat=3):catalog((1,2,3),tuple(frozenset(i for i,b in enumerate(masks) if b&(1<<s)) for s in range(2)))

report={'scope':'New independent finite checks. Local C uses exponential support enumeration, not the claimed polynomial constructor. No general phi/menu-cover review PASS is inferred.',
        'box_slice':{'cases':box_cases,'max_observed_moves':max_moves,'pivot_changes':pivot_changes,
                     'nonglobal_local_max':{'weights':['14','13','19'],'target':'-10','local':['14','-5','-19'],'local_F':'582','better':['-14','-13','17'],'better_F':'654'}},
        'local_menus':{'pairs':local_pairs,'all_pure_repair_seeds':repair_seeds,'max_observed_pure_moves':max_pure_moves,**dict(stats)},
        'three_mixer_example':{'private':['40','39'],'weights':['20']*3,'p':['39/80']*3,'loads':['277/4','279/4'],
                               'enumerated_NE_statuses':len(ps),'quota_statuses':len(good),'all_quota_statuses_require_three_designated_mixers':True},
        'colocation_equal_half':{'one_common_weight':'1','loads':['1/2','1/2'],'strong_qR_quota_met':False,
                                 'actual_single_catalog_d':'1/2','q_times_d_quota_met':True},
        'finite_catalogs':{'count':len(catalog_records),'ordered_layouts':sum(x['complete_ordered_layouts'] for x in catalog_records),
                           'cycles_checked':cycle_checks,'records':catalog_records},
        'not_claimed':['Full current arbitrary-cycle targeted proof review complete','Original polynomial C program reproduced',
                       'Finite tests prove universal phi existence or complexity','All-NE minima equal finite-menu minima','A box-slice local endpoint maximum is globally maximal']}
(OUT/'math-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('finite_catalogs',)},ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report['finite_catalogs'].items() if k!='records'},ensure_ascii=False))

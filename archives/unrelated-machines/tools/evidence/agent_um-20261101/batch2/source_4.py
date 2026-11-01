#!/usr/bin/env python3
"""Tiny exact LP audits, not a polynomial solver or a scheduling algorithm.

Enumerates vertices independently for primal and dual. No repository imports.
Default output is fresh stdout JSON; no frozen files are overwritten by code.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import platform


def dot(a,b):
    return sum((x*y for x,y in zip(a,b)),F(0))


def solve_square(a,b):
    n=len(b)
    aug=[[F(v) for v in row]+[F(rhs)] for row,rhs in zip(a,b)]
    for col in range(n):
        pivot=next((r for r in range(col,n) if aug[r][col]),None)
        if pivot is None:
            return None
        aug[col],aug[pivot]=aug[pivot],aug[col]
        z=aug[col][col]
        aug[col]=[v/z for v in aug[col]]
        for row in range(n):
            if row==col or not aug[row][col]:
                continue
            z=aug[row][col]
            aug[row]=[x-z*y for x,y in zip(aug[row],aug[col])]
    return tuple(row[-1] for row in aug)


def vertex_opt(a,b,obj,minimize=False):
    n=len(obj)
    if n==0:
        assert all(v>=0 for v in b)
        return F(0),(),1
    rows=[list(row) for row in a]
    rhs=list(b)
    for j in range(n):
        row=[F(0)]*n
        row[j]=-1
        rows.append(row)
        rhs.append(F(0))
    best=None
    arg=None
    vertices=set()
    for ids in combinations(range(len(rows)),n):
        z=solve_square([rows[k] for k in ids],[rhs[k] for k in ids])
        if z is None or any(dot(row,z)>r for row,r in zip(rows,rhs)):
            continue
        vertices.add(z)
        val=dot(obj,z)
        if best is None or (val<best if minimize else val>best):
            best,arg=val,z
    assert best is not None
    return best,arg,len(vertices)


def normalize(p):
    assert p and all(len(row)==len(p[0]) for row in p)
    out=[]
    for row in p:
        nr=[]
        for v in row:
            if isinstance(v,(float,bool)):
                raise ValueError('Exact rational input only')
            nr.append(None if v is None else F(v))
        out.append(nr)
    assert all(v is None or v>=0 for row in out for v in row)
    return out


def dual_feasible(p,mu,alpha):
    return (all(v>=0 for v in mu+alpha) and
            all(alpha[j]+p[i][j]*mu[i]>=1
                for i in range(len(p)) for j in range(len(p[0]))
                if p[i][j] is not None))


def capacity_value(p,c):
    p=normalize(p)
    m,n=len(p),len(p[0])
    c=tuple(map(F,c))
    assert len(c)==m and all(v>=0 for v in c)
    edges=[(i,j) for i in range(m) for j in range(n) if p[i][j] is not None]
    a=[]
    for i in range(m):
        a.append([p[ii][j] if ii==i else F(0) for ii,j in edges])
    for j in range(n):
        a.append([F(jj==j) for i,jj in edges])
    value,x,pverts=vertex_opt(a,list(c)+[F(1)]*n,[F(1)]*len(edges))
    da=[]
    for i,j in edges:
        row=[F(0)]*(m+n)
        row[i]=-p[i][j]
        row[m+j]=-1
        da.append(row)
    dual_value,z,dverts=vertex_opt(da,[-F(1)]*len(edges),list(c)+[F(1)]*n,True)
    mu,alpha=z[:m],z[m:]
    assert value==dual_value
    assert value==sum(x,F(0))
    assert dual_feasible(p,mu,alpha)
    assert all(dot(row,x)<=r for row,r in zip(a,list(c)+[F(1)]*n))
    assert all(v>=0 for v in x)
    return {'value':value,'edges':edges,'x':x,'mu':mu,'alpha':alpha,
            'primal_vertices':pverts,'dual_vertices':dverts}


def lattice_case(name,p,c,d):
    p=normalize(p)
    c,d=tuple(map(F,c)),tuple(map(F,d))
    lo=tuple(min(a,b) for a,b in zip(c,d))
    hi=tuple(max(a,b) for a,b in zip(c,d))
    cache={}
    def get(v):
        if v not in cache:
            cache[v]=capacity_value(p,v)
        return cache[v]
    vc,vd,vlo,vhi=map(get,(c,d,lo,hi))
    assert vc['value']+vd['value']>=vlo['value']+vhi['value']
    mu,nu=vc['mu'],vd['mu']
    alpha,beta=vc['alpha'],vd['alpha']
    mumin=tuple(min(a,b) for a,b in zip(mu,nu))
    mumax=tuple(max(a,b) for a,b in zip(mu,nu))
    amin=tuple(min(a,b) for a,b in zip(alpha,beta))
    amax=tuple(max(a,b) for a,b in zip(alpha,beta))
    assert dual_feasible(p,mumin,amax) and dual_feasible(p,mumax,amin)
    hi_cost=dot(hi,mumin)+sum(amax,F(0))
    lo_cost=dot(lo,mumax)+sum(amin,F(0))
    assert hi_cost>=vhi['value'] and lo_cost>=vlo['value']
    assert hi_cost+lo_cost<=vc['value']+vd['value']
    for ci,di,mi,ni in zip(c,d,mu,nu):
        assert max(ci,di)*min(mi,ni)+min(ci,di)*max(mi,ni)<=ci*mi+di*ni
    return {'name':name,'p':p,'c':c,'d':d,
            'values':{'c':vc['value'],'d':vd['value'],'meet':vlo['value'],'join':vhi['value']},
            'lattice_slack':vc['value']+vd['value']-vlo['value']-vhi['value'],
            'primal_dual_certificates':[{'capacity':k,**v} for k,v in cache.items()],
            'mixed_dual_costs':{'meet':lo_cost,'join':hi_cost}}


def stringify(v):
    if isinstance(v,F):
        return str(v)
    if isinstance(v,dict):
        return {k:stringify(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):
        return [stringify(x) for x in v]
    return v


def audit():
    sanity=solve_square([[1,1],[1,-1]],[F(1),F(0)])
    assert sanity==(F(1,2),F(1,2)) and all(isinstance(v,F) for v in sanity)
    cases=[
        ('empty_tasks',[[],[]],(0,0),('1/3','2/5')),
        ('no_light_endpoint',[[None],[None]],(1,0),(0,1)),
        ('strict_machine_overlap',[['1/2'],['3/5']],('1/2',0),(0,'3/5')),
        ('arbitrary_endpoint_times',[['1/3','2/5'],['1/2','1/4']],('1/5','1/10'),('1/10','1/5')),
        ('incomplete_eligibility',[['1/3',None,'2/5'],['1/2','1/4',None]],('1/5','1/3'),('2/5','1/10')),
        ('zero_time_zero_capacity',[[0,'1/3'],['1/2',None]],(0,0),('1/3','1/4')),
        ('large_denominator',[['1/1000003']],(0,),('1/1000003',)),
    ]
    lattice=[lattice_case(*case) for case in cases]
    assert lattice[2]['lattice_slack']>0
    assert lattice[5]['values']['c']==1 # zero capacity retains a free zero-time job
    assert lattice[6]['values']['join']==1
    p=[['1/2','1/3'],['2/3',None]]
    c=tuple(map(F,('2/3','2/3')))
    a=tuple(map(F,('1/3','1/2')))
    occ=[]
    for mask in range(4):
        cap=tuple(c[i]-a[i]*bool(mask>>i&1) for i in range(2))
        res=capacity_value(p,cap)
        occ.append({'mask':mask,'capacity':cap,'F':res['value'],'D':2-res['value']})
    for s in range(4):
        for t in range(4):
            assert occ[s]['F']+occ[t]['F']>=occ[s|t]['F']+occ[s&t]['F']
            assert occ[s]['D']+occ[t]['D']<=occ[s|t]['D']+occ[s&t]['D']
            if s&t==s:
                assert occ[s]['F']>=occ[t]['F'] and occ[s]['D']<=occ[t]['D']
    # Exact formula checks, not expanded LP instances.
    throughput=[]
    for n in (1,3,10**6):
        ratio=F(n,n+1)
        assert 1-ratio==F(1,n+1)
        throughput.append({'served_jobs':n,'total_jobs':n+1,'ratio':ratio,'unserved':1})
    for eta in (F(1,10),F(1,10**9)):
        result=capacity_value([['1']],(1-eta,))
        assert result['value']==1-eta<1
    # Joint-identity negative control: actual original matrix, not a price LP.
    original=[[F(1),F(1,2)],[F(1,2),F(1)]]
    schedules=[]
    for sigma in product(range(2),repeat=2):
        loads=[F(0),F(0)]
        for j,i in enumerate(sigma):
            loads[i]+=original[i][j]
        schedules.append({'sigma':sigma,'loads':loads,'makespan':max(loads)})
    optimum=min(z['makespan'] for z in schedules)
    assert optimum==F(1,2)
    big=[(0,0),(1,1)]
    light=[[None,F(1,2)],[F(1,2),None]]
    joint=[]
    for mask in range(4):
        h=[big[z] for z in range(2) if mask>>z&1]
        assert len({i for i,j in h})==len(h)==len({j for i,j in h})
        selected={j for i,j in h}
        remaining=[j for j in range(2) if j not in selected]
        cap=tuple(F(1)-sum((original[i][j] for ii,j in h if ii==i),F(0)) for i in range(2))
        residual=[[row[j] for j in remaining] for row in light]
        res=capacity_value(residual,cap)
        val=F(len(h))+res['value']
        joint.append({'mask':mask,'H':h,'remaining':remaining,'capacity':cap,
                      'F':res['value'],'V':val,'D':2-val,'residual_certificate':res})
    assert [z['F'] for z in joint]==[F(2),F(0),F(0),F(0)]
    assert [z['V'] for z in joint]==[F(2),F(1),F(1),F(2)]
    assert joint[1]['V']+joint[2]['V']<joint[0]['V']+joint[3]['V']
    assert joint[1]['D']+joint[2]['D']>joint[0]['D']+joint[3]['D']
    return stringify({'status':'passed','python':platform.python_version(),
            'arithmetic':'fractions.Fraction, exact vertex enumeration and Gaussian elimination',
            'scope':'Seven tiny lattice cases; four occupancy subsets; two near-complete one-job LPs; one 2x2 joint-identity negative control, four original schedules and four exact residual LPs; no random or large scheduling enumeration',
            'joint_identity_control':{'P':original,'T':F(1),'original_optimum':optimum,'all_schedules':schedules,'hybrid_H_values':joint},
            'lattice_cases':lattice,'occupancy_cases':occ,'throughput_formula_checks':throughput,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})


if __name__=='__main__':
    print(json.dumps(audit(),ensure_ascii=False,indent=2))

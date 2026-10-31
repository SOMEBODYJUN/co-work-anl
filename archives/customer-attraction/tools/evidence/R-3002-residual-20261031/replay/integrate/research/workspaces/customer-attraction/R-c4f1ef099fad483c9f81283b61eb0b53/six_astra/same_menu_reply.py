"""True same-menu last replies after every penultimate deviation.
No equilibrium-sufficiency claim: this is an expanded necessary system.
"""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import sys,json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
OLD=ROOT/'research/workspaces/customer-attraction/R-07e871289a6b4c1fb07244c97eb4aac8'
sys.path[:0]=[str(OLD/'general_from_half5'),str(OLD/'three_certificate_comparison')]
from six_copy_refine import decode,solve_exact_system,verify
from nested_horizon_refine import system
M=6
TYPES=[(a,d) for a in product((0,1),repeat=M) for d in range(M+1)]

def share(a,i):return F(a[i],sum(a)) if a[i] else F(0)
def atomprob(d,t):return F(d if t else M-d,M)
def one_variable(a,d,j,t):
    b=sum(a[:-2]);ell=sum(a[:-1]);ti=a[j] if j<M else t
    return {'b':b,'ell':ell,'ti':ti,'prob':F(1) if j<M else atomprob(d,t),
            'price':F(1,ell+1),'follower':F(1,b+ti+1),
            'discount':F(ti,(b+ti)*(b+ti+1)) if ti else F(0)}

def structure(cross):
    specs=[]
    for j in range(M+1):
        specs += [('leader',j),('price',j),('cap',j)]
        specs += [('queryA',j,q) for q in range(M)]
        specs += [('queryO',j)] if j<M else [('queryOwn',j),('queryOther',j)]
        if cross:specs += [('queryR',j,q) for q in range(M+1) if q!=j]
    return specs

def variable_coef(spec,a,d,reply,t):
    kind,j,*qs=spec;v=one_variable(a,d,reply,t)
    b=v['b']
    if kind=='leader':return -v['discount'] if reply==j else F(0)
    if kind=='price':return v['price'] if reply==j else F(0)
    if kind=='cap':return F(int(reply==j))
    c=-v['follower'] if reply==j else F(0)
    if kind=='queryR' and reply==qs[0]:
        if j<M:c+=F(1,b+a[j]+1)
        else:c+=(1-atomprob(d,1))*F(1,b+1)+atomprob(d,1)*F(1,b+2)
    return c

def rhs_coef(spec,a,d):
    kind,j,*qs=spec;b=sum(a[:-2]);u5=share(a,4);u6=share(a,5)
    if kind=='leader':
        base=F(a[j],b+a[j]) if j<M and a[j] else F(0)
        if j==M:base=atomprob(d,1)*F(1,b+1)
        return u5-base
    if kind=='price':return u6
    if kind=='cap':return F(0)
    if kind=='queryR':return F(0)
    if j<M:
        den=b+a[j]+1
        q=F(a[qs[0]]) if kind=='queryA' else F(d,M)
        return -q/den
    val=F(0)
    for t in (0,1):
        q=F(a[qs[0]]) if kind=='queryA' else F(t) if kind=='queryOwn' else F(d-t,M-1)
        val-=atomprob(d,t)*q/F(b+t+1)
    return val

def make_cut(specs,lambdas,cross):
    assert len(specs)==len(lambdas) and min(lambdas)>=0
    norm=sum(v for s,v in zip(specs,lambdas) if s[0]=='leader')
    assert norm>0
    lambdas=[v/norm for v in lambdas]
    coeff=[]
    for a,d in TYPES:
        rhs=sum(v*rhs_coef(s,a,d) for s,v in zip(specs,lambdas))
        credit=F(0)
        for reply in range(M+1):
            for t in ((None,) if reply<M else (0,1)):
                prob=one_variable(a,d,reply,t)['prob']
                c=sum(v*variable_coef(s,a,d,reply,t) for s,v in zip(specs,lambdas))
                credit+=prob*min(F(0),c)
        coeff.append(rhs-credit)
    coeff.append(sum(v for s,v in zip(specs,lambdas) if s[0]=='cap'))
    weights=[{'spec':list(s),'weight':str(v)} for s,v in zip(specs,lambdas) if v]
    return coeff,weights

def separate(n,cross=True):
    specs=structure(cross)
    active=[(i,a,d,n[i]) for i,(a,d) in enumerate(TYPES) if n[i]]
    variables=[(i,a,d,j,t,mass*one_variable(a,d,j,t)['prob']) for i,a,d,mass in active for j in range(M+1) for t in ((None,) if j<M else (0,1)) if one_variable(a,d,j,t)['prob']]
    mat=[[float(variable_coef(s,a,d,j,t)) for i,a,d,j,t,mass in variables]+[-float(s[0]=='leader')] for s in specs]
    rhs=[sum(rhs_coef(s,a,d)*mass for i,a,d,mass in active)+(n[-1] if s[0]=='cap' else F(0)) for s in specs]
    sol=linprog([0.]*len(variables)+[1.],A_ub=mat,b_ub=list(map(float,rhs)),bounds=[(0,float(v[-1])) for v in variables]+[(None,None)],method='highs')
    assert sol.success,sol.message
    lam=[F(float(-v)).limit_denominator(1000000) for v in sol.ineqlin.marginals]
    row,weights=make_cut(specs,lam,cross)
    slack=sum(v*x for v,x in zip(row,n))
    return {'cross':cross,'gap_float':sol.fun,'exact_cut_slack':str(slack),'weights':weights},row

def from_weights(weights):
    specs=[tuple(v['spec']) for v in weights];lam=[F(v['weight']) for v in weights]
    return make_cut(specs,lam,True)[0]

def load_old():
    old=json.loads((OLD/'general_from_half5/six_copy_free_results.json').read_text())['final']
    new=json.loads((OLD/'three_certificate_comparison/nested_horizon_refine.json').read_text())['certificate']
    return {'old_387_closed':old,'nested_587':new}

if __name__=='__main__':
    out={}
    for name,record in load_old().items():
        n=decode(record,TYPES);out[name]=[]
        for cross in (False,True):
            res,row=separate(n,cross);out[name].append(res)
            print(name,cross,res['gap_float'],res['exact_cut_slack'],len(res['weights']),flush=True)
    Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')

def feasible_reply_witness(n,cross=True):
    """Recover and exactly verify a feasible expanded response assignment.
    This is a relaxation witness, never an SPE strategy.
    """
    from six_stress import exact_solve
    specs=structure(cross)
    active=[(i,a,d,n[i]) for i,(a,d) in enumerate(TYPES) if n[i]]
    variables=[(i,a,d,j,t,mass*one_variable(a,d,j,t)['prob']) for i,a,d,mass in active for j in range(M+1) for t in ((None,) if j<M else (0,1)) if one_variable(a,d,j,t)['prob']]
    mat=[[variable_coef(s,a,d,j,t) for i,a,d,j,t,mass in variables] for s in specs]
    rhs=[sum(rhs_coef(s,a,d)*mass for i,a,d,mass in active)+(n[-1] if s[0]=='cap' else F(0)) for s in specs]
    sol=linprog([0.]*len(variables),A_ub=np.asarray(mat,float),b_ub=list(map(float,rhs)),bounds=[(0,float(v[-1])) for v in variables],method='highs')
    assert sol.success,sol.message
    support=[i for i,x in enumerate(sol.x) if x>1e-8]
    eqs=[[row[j] for j in support]+[bound] for row,bound in zip(mat,rhs) if abs(sum(float(c)*x for c,x in zip(row,sol.x))-float(bound))<1e-8]
    eqs += [[F(int(k==j)) for k in support]+[variables[j][-1]] for j in support if abs(sol.x[j]-float(variables[j][-1]))<1e-8]
    exact=exact_solve(eqs,len(support))
    z=[F(0)]*len(variables)
    for j,x in zip(support,exact):z[j]=x
    assert all(0<=x<=v[-1] for x,v in zip(z,variables))
    slacks=[bound-sum(c*x for c,x in zip(row,z)) for row,bound in zip(mat,rhs)]
    assert min(slacks)>=0
    return {'scope':'exact fractional necessary-response witness, not SPE','cross':cross,'min_primitive_slack':str(min(slacks)),'variables':[{'actual_bits':''.join(map(str,a)),'d':d,'reply':j,'t':t,'mass':str(mass),'reply_mass':str(x)} for (i,a,d,j,t,mass),x in zip(variables,z)]}

def verify_feasible_reply_witness(n,witness):
    specs=structure(witness['cross']);got={}
    for v in witness['variables']:
        a=tuple(map(int,v['actual_bits']));d=v['d'];j=v['reply'];t=v['t'];x=F(v['reply_mass']);mass=F(v['mass'])
        assert (a,d,j,t) not in got
        index=TYPES.index((a,d));assert mass==n[index]*one_variable(a,d,j,t)['prob']
        assert 0<=x<=mass;got[a,d,j,t]=x
    variables=[(a,d,j,t) for i,(a,d) in enumerate(TYPES) if n[i] for j in range(M+1) for t in ((None,) if j<M else (0,1)) if one_variable(a,d,j,t)['prob']]
    assert set(got)==set(variables)
    for s in specs:
        lhs=sum(variable_coef(s,a,d,j,t)*got[a,d,j,t] for a,d,j,t in variables)
        rhs=sum(rhs_coef(s,a,d)*mass for (a,d),mass in zip(TYPES,n[:-1]))+(n[-1] if s[0]=='cap' else 0)
        assert lhs<=rhs,(s,lhs,rhs)

#!/usr/bin/env python3
"""全局assignment矩的有理PSD、平坦提取和宏微共同分配证书。

No SDP solver and no floating point. Moments in examples come from explicit
rational distributions. The extractor only receives those truncated moments.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import platform


def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def transpose(a): return list(map(list,zip(*a)))
def mm(a,b): return [[dot(row,col) for col in transpose(b)] for row in a]
def mv(a,v): return [dot(row,v) for row in a]
def ident(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def sub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def zero(a): return all(x==0 for row in a for x in row)
def norm(v,g): return dot(v,mv(g,v))


def invert(a):
    n=len(a)
    rows=[row.copy()+ident(n)[k] for k,row in enumerate(a)]
    for k in range(n):
        pivot=next(j for j in range(k,n) if rows[j][k])
        rows[k],rows[pivot]=rows[pivot],rows[k]
        div=rows[k][k];rows[k]=[x/div for x in rows[k]]
        for j in range(n):
            if j!=k and rows[j][k]:
                factor=rows[j][k]
                rows[j]=[x-factor*y for x,y in zip(rows[j],rows[k])]
    return [row[n:] for row in rows]


def psd_exact(matrix):
    """Symmetric rational Schur elimination; zero pivots are handled exactly."""
    a=[list(map(F,row)) for row in matrix]
    n=len(a)
    assert all(len(row)==n for row in a)
    assert a==transpose(a)
    remaining=list(range(n));basis=[];pivots=[]
    while remaining:
        if any(a[i][i]<0 for i in remaining):
            raise ValueError('negative exact Schur diagonal')
        positive=next((i for i in remaining if a[i][i]>0),None)
        if positive is None:
            if any(a[i][j] for i in remaining for j in remaining):
                raise ValueError('zero-diagonal nonzero Schur block')
            break
        pivot=a[positive][positive]
        basis.append(positive);pivots.append(pivot)
        tail=[i for i in remaining if i!=positive]
        for i in tail:
            for j in tail:
                a[i][j]-=a[i][positive]*a[positive][j]/pivot
        remaining=tail
    return {'rank':len(basis),'basis':basis,'positive_pivots':pivots}


def monomials(variables,degree):
    out=[]
    for k in range(degree+1):
        for indices in combinations(range(len(variables)),k):
            if len({variables[e][1] for e in indices})==k:
                out.append(frozenset(indices))
    return out


def build_moments(jobs,atoms,r):
    variables=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
    all_monomials=monomials(variables,2*r)
    def atom_value(s,assignment):
        return all(assignment[variables[e][1]]==variables[e][0] for e in s)
    y={s:sum((w for w,assignment in atoms if atom_value(s,assignment)),F(0)) for s in all_monomials}
    return variables,y


def moment_value(variables,y,s):
    s=frozenset(s)
    if len({variables[e][1] for e in s})!=len(s):return F(0)
    return y[s]


def validate(jobs,T,r,variables,y):
    T=F(T);get=lambda s:moment_value(variables,y,s)
    assert get(())==1
    assert all(0 <= value <= 1 for value in y.values())
    conservation_checks=0
    for s in monomials(variables,2*r-1):
        for j in range(len(jobs)):
            assert sum((get(s|{e}) for e,(_,job) in enumerate(variables) if job==j),F(0))==get(s)
            conservation_checks+=1
    low=monomials(variables,r-1);high=monomials(variables,r)
    low_matrix=[[get(s|t) for t in low] for s in low]
    high_matrix=[[get(s|t) for t in high] for s in high]
    low_check=psd_exact(low_matrix);high_check=psd_exact(high_matrix)
    localizers=[]
    machines=sorted({i for job in jobs for i in job})
    for i in machines:
        edges=[(e,jobs[j][i]) for e,(v,j) in enumerate(variables) if v==i]
        coefficients=[('load',T,edges)]
        for threshold in sorted({p for _,p in edges if p>0}):
            count=min(len(jobs),int(T//threshold))
            coefficients.append(('prefix_'+str(threshold),F(count),[(e,F(1)) for e,p in edges if p>=threshold]))
        for name,bound,terms in coefficients:
            matrix=[[bound*get(s|t)-sum((p*get(s|t|{e}) for e,p in terms),F(0)) for t in low] for s in low]
            checked=psd_exact(matrix)
            localizers.append({'machine':i,'constraint':name,'rank':checked['rank'],
                               'positive_pivots':list(map(str,checked['positive_pivots']))})
    return {'low_rank':low_check['rank'],'high_rank':high_check['rank'],
            'low_rows':len(low),'high_rows':len(high),
            'assignment_conservation_checks':conservation_checks,
            'moment_psd_positive_pivots':list(map(str,high_check['positive_pivots'])),
            'localizers':localizers},low,high,low_matrix,low_check


def compressed_operator_audit(jobs,T,variables,y):
    checked,low,high,low_matrix,low_check=validate(jobs,T,2,variables,y)
    basis=[low[k] for k in low_check['basis']]
    get=lambda s:moment_value(variables,y,s)
    g=[[get(s|t) for t in basis] for s in basis]
    inv=invert(g);rank=len(g)
    h=[];operators=[];defects=[]
    for e in range(len(variables)):
        he=[[get(s|t|{e}) for t in basis] for s in basis]
        ae=mm(inv,he)
        psd_exact(he);psd_exact(sub(g,he))
        de=sub(ae,mm(ae,ae))
        psd_exact(mm(g,de))
        h.append(he);operators.append(ae);defects.append(de)
    v0=mv(inv,[get(s) for s in basis])
    for job in range(len(jobs)):
        total=[[sum((operators[e][u][v] for e,(_,j) in enumerate(variables) if j==job),F(0)) for v in range(rank)] for u in range(rank)]
        assert total==ident(rank)
    for ae,de in zip(operators,defects):
        assert all(x==0 for x in mv(de,v0))
    gram=[]
    for e in range(len(variables)):
        block_rows=[[] for _ in basis]
        for f in range(len(variables)):
            jef=[[get(s|t|{e,f}) for t in basis] for s in basis]
            cross=sub(jef,mm(mm(h[e],inv),h[f]))
            for k,row in enumerate(cross):block_rows[k].extend(row)
            cef=mm(inv,jef)
            b_e_star_b_f=sub(cef,mm(operators[e],operators[f]))
            b_f_star_b_e=sub(cef,mm(operators[f],operators[e]))
            commutator=sub(mm(operators[e],operators[f]),mm(operators[f],operators[e]))
            assert commutator==sub(b_f_star_b_e,b_e_star_b_f)
            assert all(x==0 for x in mv(commutator,v0))
        gram.extend(block_rows)
    joint_check=psd_exact(gram)
    assert joint_check['rank']==checked['high_rank']-checked['low_rank']
    trace_defect=sum((de[k][k] for de in defects for k in range(rank)),F(0))
    assert trace_defect>=0
    assert (trace_defect==0)==(checked['high_rank']==checked['low_rank'])
    saturated=0
    for i in {i for job in jobs for i in job}:
        terms=[(e,jobs[j][i]) for e,(v,j) in enumerate(variables) if v==i]
        slack=[[F(T)*ident(rank)[u][v]-sum((p*operators[e][u][v] for e,p in terms),F(0)) for v in range(rank)] for u in range(rank)]
        psd_exact(mm(g,slack))
        mean=sum((p*get({e}) for e,p in terms),F(0))
        if mean==T:
            assert zero(slack)
            saturated+=1
    return {'V1_dimension':rank,'joint_defect_gram_rows':len(gram),
            'joint_defect_gram_rank':joint_check['rank'],'trace_defect_Delta':str(trace_defect),
            'pair_commutator_identities_checked':len(variables)**2,
            'initial_state_commutators_zero':True,'initial_state_defects_zero':True,
            'saturated_full_operator_identities':saturated}


def flat_extract(jobs,T,r,variables,y):
    checked,low,high,low_matrix,low_check=validate(jobs,T,r,variables,y)
    if checked['low_rank']!=checked['high_rank']:
        return None,checked
    basis=[low[k] for k in low_check['basis']]
    get=lambda s:moment_value(variables,y,s)
    g=[[get(s|t) for t in basis] for s in basis]
    inv=invert(g);rank=len(g)
    operators=[]
    for e in range(len(variables)):
        h=[[get(s|t|{e}) for t in basis] for s in basis]
        a=mm(inv,h)
        assert zero(sub(mm(a,a),a))
        assert mm(g,a)==h and h==transpose(h)
        operators.append(a)
    for a in operators:
        for b in operators:
            assert mm(a,b)==mm(b,a)
    for j in range(len(jobs)):
        total=[[sum((operators[e][u][v] for e,(_,job) in enumerate(variables) if job==j),F(0)) for v in range(rank)] for u in range(rank)]
        assert total==ident(rank)
    v0=mv(inv,[get(s) for s in basis])
    branches=[(v0,())]
    max_branches=1
    for a in operators:
        next_branches=[]
        for vector,bits in branches:
            one=mv(a,vector)
            nil=[u-v for u,v in zip(vector,one)]
            for bit,part in ((0,nil),(1,one)):
                weight=norm(part,g)
                assert weight>=0
                if weight:
                    next_branches.append((part,bits+(bit,)))
        branches=next_branches
        max_branches=max(max_branches,len(branches))
        assert len(branches)<=rank
    atoms=[]
    for vector,bits in branches:
        assignment=[]
        for j in range(len(jobs)):
            machines=[i for e,(i,job) in enumerate(variables) if job==j and bits[e]]
            assert len(machines)==1
            assignment.append(machines[0])
        weight=norm(vector,g)
        load={i:sum((jobs[j][i] for j,v in enumerate(assignment) if v==i),F(0)) for i in {i for job in jobs for i in job}}
        assert max(load.values(),default=F(0))<=T
        atoms.append((weight,tuple(assignment)))
    assert sum((w for w,_ in atoms),F(0))==1
    for s,value in y.items():
        recovered=sum((w for w,assignment in atoms if all(assignment[variables[e][1]]==variables[e][0] for e in s)),F(0))
        assert recovered==value
    checked.update({'flat':True,'extracted_atoms':len(atoms),'max_live_branches':max_branches,
                    'rational_multiplication_operator_checks':len(variables)**2+len(variables)})
    return atoms,checked


def run():
    # One macro chooses between homes; its choice jointly moves two microjobs.
    jobs=[{0:F(1),1:F(1)}]
    for home,sink in ((0,2),(1,3)):
        jobs.extend([{home:F(1,2),sink:F(1,4)} for _ in range(2)])
    original=[(F(1,2),(0,2,2,1,1)),(F(1,2),(1,0,0,3,3))]
    variables,y=build_moments(jobs,original,2)
    recovered,flat=flat_extract(jobs,F(1),2,variables,y)
    assert recovered is not None
    flat_operators=compressed_operator_audit(jobs,F(1),variables,y)
    saturated_checks=0
    for i in (0,1):
        for s in monomials(variables,2):
            value=sum((jobs[j][i]*moment_value(variables,y,s|{e}) for e,(v,j) in enumerate(variables) if v==i),F(0))
            assert value==moment_value(variables,y,s)
            saturated_checks+=1
    # A valid common global moment can be non-flat; flatness is not automatic.
    independent_jobs=[{0:F(1),1:F(1)} for _ in range(4)]
    independent_atoms=[(F(1,16),assignment) for assignment in product((0,1),repeat=4)]
    iv,iy=build_moments(independent_jobs,independent_atoms,2)
    no_extraction,nonflat=flat_extract(independent_jobs,F(4),2,iv,iy)
    assert no_extraction is None and (nonflat['low_rank'],nonflat['high_rank'])==(5,11)
    nonflat_operators=compressed_operator_audit(independent_jobs,F(4),iv,iy)
    # Caratheodory preserves first moments, not the entire given M1.
    compressed_atoms=[(F(1,2),(0,0,0,0)),(F(1,2),(1,1,1,1))]
    cv,cy=build_moments(independent_jobs,compressed_atoms,2)
    compressed,compressed_check=flat_extract(independent_jobs,F(4),2,cv,cy)
    assert compressed is not None
    assert all(iy[frozenset({e})]==cy[frozenset({e})] for e in range(len(iv)))
    assert any(iy[s]!=cy[s] for s in monomials(iv,2))
    balanced_atoms=[(F(1,6),assignment) for assignment in product((0,1),repeat=4) if sum(assignment)==2]
    bv,by=build_moments(independent_jobs,balanced_atoms,2)
    balanced_operators=compressed_operator_audit(independent_jobs,F(2),bv,by)
    balanced_checks=validate(independent_jobs,F(2),2,bv,by)[0]
    assert balanced_operators['saturated_full_operator_identities']==2
    assert balanced_operators['trace_defect_Delta']=='4'
    # Reuse the team's cyclic Latin-4 lower-order example. This is a
    # global PSD first/second matrix for triple indicators, NOT a supplied
    # degree-four assignment SDP witness or a scheduling gap-two certificate.
    triples=[(x,z,(x+z)%4) for x in range(4) for z in range(4)]
    mu=[F(1,4)]*16
    q=[[F(1,4) if a==b else F(1,8) if all(x!=z for x,z in zip(triples[a],triples[b])) else F(0)
        for b in range(16)] for a in range(16)]
    covariance=[[q[a][b]-mu[a]*mu[b] for b in range(16)] for a in range(16)]
    latin_matrix=[[F(1)]+mu]+[[mu[a]]+q[a] for a in range(16)]
    latin_psd=psd_exact(latin_matrix)
    cov_psd=psd_exact([[16*x for x in row] for row in covariance])
    assert (latin_psd['rank'],cov_psd['rank'])==(7,6)
    perfect=[chosen for chosen in combinations(range(16),4)
             if all(len({triples[a][d] for a in chosen})==4 for d in range(3))]
    assert not perfect
    assert all(sum(row,F(0))==1 for row in q)
    return {'status':'all exact rational checks passed','arithmetic':'Fraction only; exact Schur PSD elimination; no SDP solver/no numerical eigenvalues',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'python_version':platform.python_version(),
            'flat_macro_micro':{'jobs':[{str(i):str(p) for i,p in job.items()} for job in jobs],
                                'T':'1','level_r':2,'variables':variables,'moment_entries':len(y),
                                'checks':flat,'compressed_operator_checks':flat_operators,'saturated_load_null_checks':saturated_checks,
                                'extracted_distribution':[{'weight':str(w),'assignment':a} for w,a in recovered],
                                'moments':[{'edges':[variables[e] for e in sorted(s)],'value':str(v)} for s,v in y.items()]},
            'nonflat_valid_global_distribution':{'jobs':4,'machines':2,'T':'4','level_r':2,'checks':nonflat,'compressed_operator_checks':nonflat_operators,
                'same_first_moments_compressed_lift':{'checks':compressed_check,'atoms':[{'weight':str(w),'assignment':a} for w,a in compressed]}},
            'balanced_optimal_uniform_distribution':{'jobs':4,'machines':2,'T':'2','support_atoms':6,'checks':balanced_checks,'compressed_operator_checks':balanced_operators,
                'general_same_state_confidence_bound':'1/2 + 1/(2 sqrt(n-1)) for even n'},
            'cyclic_latin4_global_second_moments':{'triples':triples,'mu':'1/4','Q_diagonal':'1/4',
                'Q_disjoint':'1/8','Q_other':'0','moment_rank':latin_psd['rank'],
                'covariance_rank':cov_psd['rank'],'16_covariance_positive_pivots':list(map(str,cov_psd['positive_pivots'])),
                'four_triple_subsets_checked':1820,'perfect_3dm_exists':False,
                'scope':'Lower-order triple indicators only; not a full degree-four assignment/localizer scheduling witness.'},
            'limits':'Examples validate rational certificates and extraction, not a general constant-level SDP solver, flatness guarantee, integrality-gap bound or makespan approximation.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=run();args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('flat_macro_micro','nonflat_valid_global_distribution')},ensure_ascii=False,indent=2))
    print(json.dumps({'flat_ranks':(result['flat_macro_micro']['checks']['low_rank'],result['flat_macro_micro']['checks']['high_rank']),
                      'nonflat_ranks':(result['nonflat_valid_global_distribution']['checks']['low_rank'],result['nonflat_valid_global_distribution']['checks']['high_rank']),
                      'atoms':result['flat_macro_micro']['extracted_distribution']},indent=2))

#!/usr/bin/env python3
"""近平坦共同矩的独立greedy-HS证书提取审计。

Core selection is independently implemented here. The local helper supplies
only Fraction linear algebra and full exact moment validation/building.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
import argparse
import hashlib
import json
import platform
import global_assignment_flat_moment_audit as h


def trace(a):return sum((a[k][k] for k in range(len(a))),F(0))
def scale(a,c):return [[c*x for x in row] for row in a]
def plus(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def adjoint(a,g,ginv):return h.mm(h.mm(ginv,h.transpose(a)),g)
def hs2(a,g,ginv):return trace(h.mm(adjoint(a,g,ginv),a))


def operators(jobs,T,variables,y):
    validated,low,_,_,low_psd=h.validate(jobs,T,2,variables,y)
    basis=[low[k] for k in low_psd['basis']]
    get=lambda s:h.moment_value(variables,y,s)
    g=[[get(s|t) for t in basis] for s in basis]
    inv=h.invert(g);effects=[];defects=[];delta_e=[]
    for e in range(len(variables)):
        he=[[get(s|t|{e}) for t in basis] for s in basis]
        ae=h.mm(inv,he)
        h.psd_exact(he);h.psd_exact(h.sub(g,he))
        de=h.sub(ae,h.mm(ae,ae))
        h.psd_exact(h.mm(g,de))
        effects.append(ae);defects.append(de);delta_e.append(trace(de))
    rank=len(g)
    for j in range(len(jobs)):
        total=[[sum((effects[e][u][v] for e,(_,job) in enumerate(variables) if job==j),F(0))
                for v in range(rank)] for u in range(rank)]
        assert total==h.ident(rank)
    return g,inv,effects,defects,delta_e,validated


def greedy_hs(jobs,T,eta,variables,y):
    n=len(jobs);d=len(variables)
    if n==0:return {'assignment':(),'loads':{},'certificate_passed':True,'empty_jobs':True}
    assert all(F(0)<=p<=T for job in jobs for p in job.values()), 'pruned domain required'
    g,inv,effects,defects,de,validated=operators(jobs,T,variables,y)
    rank=len(g);delta=sum(de,F(0))
    threshold=min(F(1,64*n*d*rank),F(eta,16))
    passed=delta<=threshold
    k=h.ident(rank);history=[];prefix=[]
    for j in range(n):
        best=None
        for e,(machine,job) in enumerate(variables):
            if job!=j:continue
            candidate=h.mm(effects[e],k)
            score=hs2(candidate,g,inv)
            assert score>=0
            if best is None or score>best[0]:best=(score,e,candidate)
        score,e,k=best
        assert score>0
        history.append(e)
        if passed:
            assert score>=(1-2*n*delta)**2
        prefix.append({'job':j,'chosen_edge':variables[e],'HS_squared':str(score)})
    kh=adjoint(k,g,inv);denom=hs2(k,g,inv)
    rho=scale(h.mm(k,kh),1/denom)
    assert trace(rho)==1
    assignment=tuple(variables[e][0] for e in history)
    machines=sorted({i for job in jobs for i in job})
    loads={i:sum((jobs[j][i] for j,w in enumerate(assignment) if i==w),F(0)) for i in machines}
    selected_losses=[]
    for e in history:
        expectation=trace(h.mm(rho,effects[e]))
        assert 0<=expectation<=1
        loss=1-expectation
        if passed:assert loss<=3*de[e]
        if de[e]==0:assert loss==0
        selected_losses.append({'edge':variables[e],'delta_e':str(de[e]),'loss':str(loss)})
    for i in machines:
        si=[[sum((jobs[j][i]*effects[e][u][v] for e,(machine,j) in enumerate(variables) if machine==i),F(0))
             for v in range(rank)] for u in range(rank)]
        h.psd_exact(h.mm(g,h.sub(scale(h.ident(rank),T),si)))
        if passed:
            local_error=3*sum((jobs[j][i]*de[e] for j,e in enumerate(history) if assignment[j]==i),F(0))
            assert loads[i]<=T+local_error<=(1+3*delta)*T<=(1+eta)*T
    return {'assignment':assignment,'loads':{str(i):str(v) for i,v in loads.items()},
            'makespan':max(loads.values(),default=F(0)),
            'certificate_passed':passed,'delta':delta,'threshold':threshold,
            'rank_M1':rank,'rank_M2':validated['high_rank'],'denominator_HS_squared':denom,
            'prefix':prefix,'selected_losses':selected_losses}


def real_load(jobs,assignment):
    return {i:sum((jobs[j][i] for j,w in enumerate(assignment) if i==w),F(0)) for i in {i for job in jobs for i in job}}


def independent_vectors(vectors):
    basis=[];pivots=[];selected=[]
    for index,vector in enumerate(vectors):
        row=list(map(F,vector))
        for pivot,old in zip(pivots,basis):
            factor=row[pivot]
            row=[x-factor*y for x,y in zip(row,old)]
        if any(row):
            pivot=next(k for k,x in enumerate(row) if x)
            div=row[pivot];row=[x/div for x in row]
            pivots.append(pivot);basis.append(row);selected.append(index)
    return selected


def macro_micro_cases():
    jobs=[{0:F(1),1:F(1)}]
    for home,sink in ((0,2),(1,3)):
        jobs.extend([{home:F(1,2),sink:F(1,4)} for _ in range(2)])
    all_schedules=[a for a in product(*(tuple(sorted(job)) for job in jobs)) if max(real_load(jobs,a).values())<=1]
    variables=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
    vectors=[[1]+[int(a[j]==i) for i,j in variables] for a in all_schedules]
    base=independent_vectors(vectors)
    rare=[k for k in range(len(all_schedules)) if k not in base]
    assert len(all_schedules)==8 and len(base)==6 and len(rare)==2
    for bits in (30,80):
        q=F(1,2**bits)
        atoms=[((1-q)/len(base) if k in base else q/len(rare),a) for k,a in enumerate(all_schedules)]
        yield 'macro_micro_nonflat_q_2minus'+str(bits),jobs,F(1),F(1,10),atoms,{'base_atoms':len(base),'rare_atoms':len(rare),'rare_weight':str(q)}
    # Saturated optimal balanced distribution, outside small-defect certificate.
    jobs=[{0:F(1),1:F(1)} for _ in range(4)]
    atoms=[(F(1,6),a) for a in product((0,1),repeat=4) if sum(a)==2]
    yield 'balanced_optimal_large_defect',jobs,F(2),F(1,10),atoms,{}


def general_cases():
    rng=Random(20261016)
    retained=0;attempts=0
    while retained<18:
        attempts+=1
        machines=3;n=4
        jobs=[]
        for _ in range(n):
            choices=sorted(rng.sample(range(machines),2))
            jobs.append({i:F(rng.randrange(1,5),4) for i in choices})
        feasible=[a for a in product(*(tuple(sorted(job)) for job in jobs)) if max(real_load(jobs,a).values())<=1]
        if len(feasible)<6:continue
        variables=[(i,j) for j,job in enumerate(jobs) for i in sorted(job)]
        features=[[1]+[int(a[j]==i) for i,j in variables] for a in feasible]
        affine_rank=len(independent_vectors(features))
        if len(feasible)<=affine_rank:continue
        weights=[rng.randrange(1,9) for _ in feasible];normalizer=sum(weights)
        atoms=[(F(w,normalizer),a) for w,a in zip(weights,feasible)]
        yield f'general_true_T_{retained}',jobs,F(1),F(1,10),atoms,{'generating_attempt':attempts,'feasible_schedules':len(feasible),'support_affine_rank':affine_rank}
        retained+=1


def run():
    rows=[];small=nonflat_small=large=large_overshoot=0
    worst=F(0);worst_name=None
    for name,jobs,T,eta,atoms,extra in list(macro_micro_cases())+list(general_cases()):
        variables,y=h.build_moments(jobs,atoms,2)
        result=greedy_hs(jobs,T,eta,variables,y)
        ratio=result['makespan']/T
        if result['certificate_passed']:
            small+=1;nonflat_small+=result['rank_M2']>result['rank_M1']
        else:
            large+=1;large_overshoot+=ratio>1
        if ratio>worst:worst=ratio;worst_name=name
        rows.append({'name':name,'jobs':[{str(i):str(p) for i,p in job.items()} for job in jobs],
                     'T':str(T),'eta':str(eta),'support_atoms':[{'weight':str(w),'assignment':a} for w,a in atoms],
                     **extra,**{k:(str(v) if isinstance(v,F) else v) for k,v in result.items()}})
    assert F(37,32)/F(31,32)**2==F(1184,961)<3
    assert F(67,64)<F(3,2)
    edge_cases=[]
    for name,jobs,atoms in (
            ('empty_jobs',[],[(F(1),())]),
            ('T0_zero_private',[{0:F(0),1:F(0)},{2:F(0)}],[(F(1,2),(0,2)),(F(1,2),(1,2))]),
            ('T0_zero_effect',[{0:F(0),1:F(0)}],[(F(1),(0,))])):
        variables,y=h.build_moments(jobs,atoms,2)
        got=greedy_hs(jobs,F(0),F(1,10),variables,y)
        assert got['certificate_passed']
        edge_cases.append({'name':name,'assignment':got['assignment'],'loads':got['loads']})
    return {'status':'all exact certificate-conditional assertions passed',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'helper_source':str(Path(h.__file__)),'helper_sha256':hashlib.sha256(Path(h.__file__).read_bytes()).hexdigest(),
            'python_version':platform.python_version(),'arithmetic':'Fraction; exact Schur PSD and G-HS; no roots/eigenvalues/SDP solver',
            'algorithm':'one greedy maximum-G-HS product per job; independent implementation',
            'threshold':'delta <= min(1/(64 n d R), eta/16)',
            'proof_constant_checks':{'h_lower':'961/1024','loss_numerator_upper':'37/32','loss_coefficient_upper':'1184/961 < 3','at_T_generator_ratio_upper':'67/64 < 3/2'},
            'edge_cases':edge_cases,'total_cases':len(rows),'certificate_pass_cases':small,'genuinely_nonflat_certificate_pass_cases':nonflat_small,
            'ordinary_large_defect_cases':large,'ordinary_large_defect_outputs_above_T':large_overshoot,
            'maximum_observed_makespan_ratio':str(worst),'maximum_ratio_instance':worst_name,
            'scope':'Small-defect conditional extractor only; large-defect runs are finite attacks, not a general guarantee or a counterexample to arbitrary SDP initialization.',
            'instances':rows}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=run();args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='instances'},ensure_ascii=False,indent=2))
    print(json.dumps([{'name':r['name'],'delta':r['delta'],'threshold':r['threshold'],'rank_M1':r['rank_M1'],'rank_M2':r['rank_M2'],
                      'certificate_passed':r['certificate_passed'],'makespan':r['makespan']} for r in result['instances'][:3]],indent=2))

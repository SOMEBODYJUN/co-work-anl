"""Exact recovery from the one saved phase-I basis; no optimization calls."""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'


def sha(p):return sha256(p.read_bytes()).hexdigest()


def save(n,x):(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')


def sparse(r):return [[j,str(v)] for j,v in sorted(r.items()) if v]


def reduce_equations(equations,variables,approx):
    """Sparse rational elimination with all exact inconsistencies fatal."""
    basis={};log=[]
    for source,row,rhs in equations:
        rr={j:v for j,v in row.items() if v};bb=rhs
        while rr:
            p=min(rr)
            if p not in basis:
                factor=rr[p];rr={j:v/factor for j,v in rr.items()};bb/=factor
                basis[p]=(rr,bb);log.append({'source':source,'independent':True,'pivot':p});break
            er,eb=basis[p];factor=rr[p]
            for j,v in er.items():
                rr[j]=rr.get(j,F())-factor*v
                if not rr[j]:del rr[j]
            bb-=factor*eb
        else:
            assert bb==0,('inconsistent exact equation',source,str(bb))
            log.append({'source':source,'independent':False})
    free=[j for j in variables if j not in basis]
    result={j:F(approx[j]).limit_denominator(10**12) for j in free}
    for p in sorted(basis,reverse=True):
        row,rhs=basis[p]
        result[p]=rhs-sum(v*result[j] for j,v in row.items() if j!=p)
    return result,log,free,len(basis)


def main():
    lift=json.loads((HERE/'symbolic_lift.json').read_bytes())
    num=json.loads((HERE/'phase_I_discovery.json').read_bytes())
    assert num['success'] and num['linprog_calls']==1
    assert num['point_sha256']==sha(POINT)==lift['point_sha256']
    assert num['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json')
    w=[F(c['weight']) for c in json.loads(POINT.read_bytes())['columns'][:4849]]
    rows=[{j:F(v) for j,v in r['row']} for r in lift['rows']]
    oldpart=[{j:v for j,v in r.items() if j<4849} for r in rows]
    B=[{j-4849:v for j,v in r.items() if j>=4849} for r in rows]
    rhs=[sum(v*w[j] for j,v in r.items()) for r in oldpart]
    assert [str(v) for v in rhs]==num['fixed_old_row_values']
    n=len(lift['new_columns']);m=len(rows)
    common={'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json'),
            'discovery_sha256':sha(HERE/'phase_I_discovery.json'),'recovery_source_sha256':sha(Path(__file__)),
            'scope':'Only the stated four-state E successor necessary lift at the new 20910 point; no common implementation or SPE claim.',
            'optimization_calls_during_recovery':0}
    if num['phase_I']<=1e-10:
        assert num['phase_I']==0
        equations=[]
        for j,t in enumerate(num['x'][:-1]):
            if abs(t)<1e-10:equations.append(({'nonnegative_x':j},{j:F(1)},F()))
        # Local upper bounds first make exact elimination much smaller.
        active=[i for i,s in enumerate(num['row_slack']) if abs(s)<1e-9]
        active.sort(key=lambda i:(lift['rows'][i]['name'][0]!='E-at-most-old-state',i))
        for i in active:equations.append(({'row':i,'name':lift['rows'][i]['name']},B[i],-rhs[i]))
        result,log,free,rank=reduce_equations(equations,list(range(n)),dict(enumerate(num['x'][:-1])))
        x=[result[j] for j in range(n)];assert min(x)>=0
        values=w+x
        slacks=[sum(v*values[j] for j,v in r.items()) for r in rows]
        bad=[(i,str(s)) for i,s in enumerate(slacks) if s<0]
        assert not bad,bad
        certificate={**common,'kind':'primal','phase_I':'0','rank':rank,'free_variables':free,
                     'new_values':[str(v) for v in x],'row_slacks':[str(v) for v in slacks],
                     'minimum_slack':str(min(slacks)),'positive_new_values':sum(v>0 for v in x),
                     'max_numeric_displacement':max(abs(float(v)-num['x'][j]) for j,v in enumerate(x)),
                     'equations':log}
        save('exact_certificate.json',certificate)
        print(json.dumps({k:certificate[k] for k in ('kind','phase_I','rank','free_variables','minimum_slack','positive_new_values','max_numeric_displacement')},ensure_ascii=False))
    else:
        supp=[i for i,v in enumerate(num['lambda']) if v>1e-10]
        variables=list(range(len(supp)));rmap={i:j for j,i in enumerate(supp)}
        equations=[({'normalization':'sum lambda = 1'},{j:F(1) for j in variables},F(1))]
        colvecs=defaultdict(dict)
        for i in supp:
            for j,v in B[i].items():colvecs[j][rmap[i]]=v
        for j in range(n):
            reduced=-sum(float(v)*num['lambda'][supp[k]] for k,v in colvecs[j].items())
            if abs(reduced)<1e-9 and colvecs[j]:
                equations.append(({'annihilate_new_column':j},colvecs[j],F()))
        recovered,log,free,rank=reduce_equations(equations,variables,{j:num['lambda'][i] for j,i in enumerate(supp)})
        lam=[F()]*m
        for j,i in enumerate(supp):lam[i]=recovered[j]
        assert min(lam)>=0 and sum(lam,F())==1
        mu=[-sum(lam[i]*B[i].get(j,F()) for i in supp) for j in range(n)]
        assert min(mu)>=0,[(j,str(v)) for j,v in enumerate(mu) if v<0]
        out=defaultdict(F)
        for i in supp:
            for j,v in oldpart[i].items():out[j]+=lam[i]*v
        out={j:v for j,v in out.items() if v}
        value=sum(v*w[j] for j,v in out.items());assert value<0
        certificate={**common,'kind':'Farkas','phase_I_exact_dual_value':str(-value),
                     'phase_I_float':num['phase_I'],'lambda':[str(v) for v in lam],
                     'nonnegative_x_multipliers':[str(v) for v in mu],
                     'old_necessary_row':sparse(out),'old_point_value':str(value),'old_point_value_float':float(value),
                     'rank':rank,'free_variables':free,'equations':log,
                     'positive_lambda_count':sum(v>0 for v in lam),
                     'positive_nonnegative_x_count':sum(v>0 for v in mu),
                     'positive_lambda':[{'index':i,'name':lift['rows'][i]['name'],'multiplier':str(lam[i])} for i in supp if lam[i]],
                     'all_new_columns_eliminated':True}
        save('exact_certificate.json',certificate)
        # A small standalone row is ready for Main's original-column matrix.
        save('necessary_negative_row.json',{'scope':common['scope'],
                                           'point_sha256':sha(POINT),'original_columns':4849,
                                           'row':sparse(out),'inequality':'row dot original_point >= 0',
                                           'value':str(value),'value_float':float(value),
                                           'certificate_sha256':sha(HERE/'exact_certificate.json')})
        print(json.dumps({k:certificate[k] for k in ('kind','phase_I_exact_dual_value','old_point_value','old_point_value_float','rank','free_variables','positive_lambda_count','positive_nonnegative_x_count')},ensure_ascii=False))


if __name__=='__main__':main()

"""Recover exact primal or Farkas data from the unique saved phase I.

No optimizer is imported.  Primal recovery first replaces every virtual min
by its numerical active branch, recovering only the 776 true E variables;
the final min values are then recomputed exactly, and every full row checked.
"""
from collections import defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import argparse
import gzip
import json
import time
import traceback

HERE=Path(__file__).resolve().parent
POINT=HERE.parent/'full624_augmented_lp/recovery/augmented_lp_exact.json'

def sha(p):return sha256(p.read_bytes()).hexdigest()
def save(name,data):(HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def sparse(v):return [[j,str(c)] for j,c in sorted(v.items()) if c]
def decode(v):return {j:Q(c) for j,c in v}
def dot(a,x):return sum((c*x[j] for j,c in a.items()),Q())

def eliminate(equations,n,approx):
    basis={};log=[]
    for source,row,rhs in equations:
        v={j:c for j,c in row.items() if c};b=rhs
        while v:
            p=min(v)
            if p not in basis:
                c=v[p];v={j:t/c for j,t in v.items()};b/=c
                basis[p]=(v,b);log.append({'source':source,'pivot':p,'independent':True});break
            rr,bb=basis[p];c=v[p]
            for j,t in rr.items():
                v[j]=v.get(j,Q())-c*t
                if not v[j]:del v[j]
            b-=c*bb
        else:
            assert b==0,('inconsistent active equation',source,str(b))
            log.append({'source':source,'independent':False})
    free=[j for j in range(n) if j not in basis]
    x={j:Q(str(approx[j])).limit_denominator(10**12) for j in free}
    for p in sorted(basis,reverse=True):
        row,b=basis[p];x[p]=b-sum((c*x[j] for j,c in row.items() if j!=p),Q())
    return [x[j] for j in range(n)],len(basis),free,log

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--discovery',type=Path,default=HERE/'actions_output/phase_I_discovery.json');args=ap.parse_args()
    start=time.perf_counter();num=json.loads(args.discovery.read_bytes())
    lift=json.loads(gzip.decompress((HERE/'symbolic_lift.json.gz').read_bytes()))
    assert num['linprog_calls']==1 and num['success'] and num['method']=='highs-ds'
    assert num['point_sha256']==lift['point_sha256']==sha(POINT)
    assert num['symbolic_lift_sha256']==sha(HERE/'symbolic_lift.json.gz')
    assert num['shape']==[len(lift['rows']),len(lift['new_columns'])+1]
    w=[Q(c['weight']) for c in json.loads(POINT.read_bytes())['columns'][:4849]]
    rows=[decode(r['row']) for r in lift['rows']]
    old=[{j:c for j,c in r.items() if j<4849} for r in rows]
    new=[{j-4849:c for j,c in r.items() if j>=4849} for r in rows]
    fixed=[dot(r,w) for r in old]
    assert list(map(str,fixed))==num['fixed_old_row_values']
    n=len(lift['new_columns']);m=len(rows)
    common={'scope':'Exact certificate for the complete single-query envelope necessary lift; no common coupling/SPE conclusion.',
            'point_sha256':sha(POINT),'symbolic_lift_sha256':sha(HERE/'symbolic_lift.json.gz'),
            'discovery_sha256':sha(args.discovery),'recovery_source_sha256':sha(Path(__file__)),
            'optimization_calls_during_recovery':0,'all_new_columns':n,'all_rows':m}
    try:
        if num['phase_I']<=1e-10:
            assert num['phase_I']==0,'A positive numerical delta is not an exact feasible result.'
            approximation=num['x'][:776];allfloat=[float(v) for v in w]+approximation
            choices=[];branches=[];projected=[]
            for c in lift['new_columns'][776:]:
                a=decode(c['a']);b=decode(c['b'])
                choose=a if sum(float(v)*allfloat[j] for j,v in a.items())<=sum(float(v)*allfloat[j] for j,v in b.items()) else b
                choices.append(choose)
                other=b if choose is a else a
                branch=defaultdict(Q,other)
                for j,v in choose.items():branch[j]-=v
                branches.append(dict(branch))
            for i,r in enumerate(rows[:1056]):
                pp=defaultdict(Q)
                for j,v in r.items():
                    if j<5625:pp[j]+=v
                    else:
                        for k,c in choices[j-5625].items():pp[k]+=v*c
                projected.append(({'row':i,'name':lift['rows'][i]['name']},{j:v for j,v in pp.items() if v}))
            equations=[]
            for j,x in enumerate(approximation):
                if abs(x)<1e-10:equations.append(({'zero_E':j},{j:Q(1)},Q()))
            # Original box constraints have exact state semantics and take priority.
            ordered=sorted(projected,key=lambda p:p[0]['name'][0]!='E-at-most-old-state')
            for src,r in ordered+[(dict(min_branch=j),r) for j,r in enumerate(branches)]:
                b=dot({j:v for j,v in r.items() if j<4849},w)
                B={j-4849:v for j,v in r.items() if j>=4849 and v}
                residual=float(b)+sum(float(v)*approximation[j] for j,v in B.items())
                if B and abs(residual)<1e-9:equations.append((src,B,-b))
            E,rank,free,log=eliminate(equations,776,approximation)
            assert min(E)>=0
            values=w+E;minvalues=[]
            for c in lift['new_columns'][776:]:minvalues.append(min(dot(decode(c['a']),values),dot(decode(c['b']),values)))
            x=E+minvalues;assert len(x)==n and min(x)>=0
            values=w+x;slacks=[dot(r,values) for r in rows]
            bad=[{'index':i,'name':lift['rows'][i]['name'],'slack':str(s)} for i,s in enumerate(slacks) if s<0]
            assert not bad,('exact primal has negative rows',bad[:20])
            cert={**common,'kind':'primal','phase_I':'0','E_rank':rank,'E_free_variables':free,
                  'E_values':[str(v) for v in E],'canonical_min_values':[str(v) for v in minvalues],
                  'new_values':[str(v) for v in x],'row_slacks':[str(v) for v in slacks],
                  'minimum_slack':str(min(slacks)),'positive_E_values':sum(v>0 for v in E),
                  'canonical_mins_recomputed':True,'max_E_displacement':max(abs(float(v)-approximation[j]) for j,v in enumerate(E)),
                  'equations':log}
            save('exact_certificate.json',cert)
            print(json.dumps({k:cert[k] for k in ('kind','phase_I','E_rank','E_free_variables','minimum_slack','positive_E_values','max_E_displacement')}))
        else:
            support=[i for i,v in enumerate(num['lambda']) if v>1e-12]
            pos={i:j for j,i in enumerate(support)};col=defaultdict(dict)
            for i in support:
                for j,v in new[i].items():col[j][pos[i]]=v
            equations=[({'normalization':'sum lambda=1'},{j:Q(1) for j in range(len(support))},Q(1))]
            for j,rr in sorted(col.items(),key=lambda item:(len(item[1]),item[0])):
                residual=-sum(float(v)*num['lambda'][support[k]] for k,v in rr.items())
                if abs(residual)<1e-9:equations.append(({'zero_reduced_cost_new_column':j},rr,Q()))
            recovered,rank,free,log=eliminate(equations,len(support),[num['lambda'][i] for i in support])
            lam=[Q()]*m
            for i,v in zip(support,recovered):lam[i]=v
            assert min(lam)>=0 and sum(lam,Q())==1
            mu=[Q()]*n;out=defaultdict(Q)
            for i in support:
                for j,v in new[i].items():mu[j]-=lam[i]*v
                for j,v in old[i].items():out[j]+=lam[i]*v
            assert min(mu)>=0,('negative exact reduced costs',[(j,str(v)) for j,v in enumerate(mu) if v<0][:20])
            out={j:v for j,v in out.items() if v};value=dot(out,w);assert value<0
            cert={**common,'kind':'Farkas','lambda':[str(v) for v in lam],
                  'nonnegative_new_multipliers':[str(v) for v in mu],
                  'old_necessary_row':sparse(out),'old_point_value':str(value),'old_point_value_float':float(value),
                  'phase_I_float':num['phase_I'],'exact_dual_value':str(-value),'rank':rank,'free_variables':free,
                  'equations':log,'positive_lambda_count':sum(v>0 for v in lam),
                  'positive_nonnegative_new_count':sum(v>0 for v in mu),
                  'positive_lambda':[{'index':i,'name':lift['rows'][i]['name'],'multiplier':str(lam[i])} for i in support if lam[i]],
                  'all_11034_new_columns_eliminated':True}
            save('exact_certificate.json',cert)
            save('necessary_negative_row.json',{'scope':common['scope'],'original_columns':4849,
                                                'point_sha256':sha(POINT),'row':sparse(out),
                                                'value':str(value),'value_float':float(value),
                                                'certificate_sha256':sha(HERE/'exact_certificate.json')})
            print(json.dumps({k:cert[k] for k in ('kind','phase_I_float','exact_dual_value','old_point_value_float','rank','free_variables','positive_lambda_count','positive_nonnegative_new_count')}))
        save('recovery_summary.json',{'kind':cert['kind'],'certificate_sha256':sha(HERE/'exact_certificate.json'),
                                     'elapsed_seconds':time.perf_counter()-start,'optimization_calls':0,'success':True})
    except BaseException as exc:
        save('exact_recovery_failure.json',{**common,'success':False,'exception_type':type(exc).__name__,
                                            'exception':str(exc),'traceback':traceback.format_exc(),
                                            'elapsed_seconds':time.perf_counter()-start})
        raise

if __name__=='__main__':main()

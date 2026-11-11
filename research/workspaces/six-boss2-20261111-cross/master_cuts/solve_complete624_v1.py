#!/usr/bin/env python3
"""Separate solve/recovery adapter for the reviewed 12666 x 12631 lift.

The matrix remains in joint_requery.  All original 7639 columns, including the
2790 ZZ auxiliaries and every zero-mass structural domain, remain in the LP.
Floating discovery selects a face; every final number is checked as Fraction.
"""
from __future__ import annotations
from array import array
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, math, platform, resource, sys, time
from merge_master import exact_linear_system, canonical_sha

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
ROOT = HERE.parents[3]
STEM = 'complete624_actual4_R00_solve_v1'
MATRIX = RUN / 'joint_requery/complete624_actual4_R00_v1_matrix.json.gz'
MATRIX_SHA = '556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a'
MAP = RUN / 'joint_requery/complete624_actual4_R00_v1_mapping.json'
MAP_SHA = '24a601ebc1e2f7dc5e175bca453a5ab05433e046dfc7c2a782e830849817d109'
REVIEW = RUN / 'main_verify_complete624_v1.json'


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def path(kind): return HERE / f'{STEM}_{kind}'
def write(kind, obj):
    p = path(kind + '.json')
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    return p
def log(stage, **kw): print(json.dumps({'stage':stage, **kw},ensure_ascii=False),flush=True)


@lru_cache(None)
def frac(s): return F(s)


def load():
    assert sha(MATRIX) == MATRIX_SHA and sha(MAP) == MAP_SHA
    review = json.loads(REVIEW.read_text())
    assert review['status'] == 'PASS' and review['matrix_sha256'] == MATRIX_SHA
    with gzip.open(MATRIX, 'rt') as stream: data = json.load(stream)
    assert data['row_count'] == 12666 and data['column_count'] == 12631
    assert data['base_row_count'] == 11418 and data['base_column_count'] == 7639
    rows = [{j:frac(v) for j,v in r['nonzero']} for r in data['rows']]
    return data, rows, list(map(frac,data['objective'])), list(map(frac,data['normalization']))


def solve():
    import numpy as np
    import scipy
    from scipy.sparse import csr_matrix
    from scipy.optimize import linprog
    assert not path('exact.json').exists() and not path('float.npz').exists()
    started=time.time(); data,rows,obj,norm=load()
    rr=array('i');cc=array('i');vv=array('d');sc=[]
    for i,row in enumerate(rows):
        scale=max((abs(float(v)) for v in row.values()),default=1.0);sc.append(scale)
        for j,v in row.items(): rr.append(i);cc.append(j);vv.append(-float(v)/scale)
    matrix=csr_matrix((np.frombuffer(vv,dtype=np.float64),
                       (np.frombuffer(rr,dtype=np.int32),np.frombuffer(cc,dtype=np.int32))),
                      shape=(len(rows),len(obj)))
    log('float-start',rows=len(rows),columns=len(obj),nonzeros=int(matrix.nnz),load_seconds=time.time()-started)
    sol=linprog(list(map(float,obj)),A_ub=matrix,b_ub=np.zeros(len(rows)),
                A_eq=csr_matrix([list(map(float,norm))]),b_eq=[1],bounds=(0,None),
                method='highs',options={'primal_feasibility_tolerance':1e-9,
                 'dual_feasibility_tolerance':1e-9,'time_limit':180})
    out={'scope':data['scope'],'float_only':True,'success':bool(sol.success),
         'status':int(sol.status),'message':sol.message,
         'W_float':None if sol.fun is None else float(sol.fun),'rows':len(rows),'columns':len(obj),
         'matrix_path':str(MATRIX.relative_to(ROOT)),'matrix_sha256':MATRIX_SHA,
         'seconds':time.time()-started,'numpy':np.__version__,'scipy':scipy.__version__,
         'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    if sol.success:
        np.savez(path('float.npz'),x=sol.x,scaled_slacks=sol.ineqlin.residual,
                 inequality_marginals=sol.ineqlin.marginals,lower_marginals=sol.lower.marginals,
                 scales=np.array(sc))
        out.update(iterations=int(sol.nit),positive_columns_1e_10=int(sum(sol.x>1e-10)),
            original_positive_columns=int(sum(sol.x[:4849]>1e-10)),
            ZZ_positive_columns=int(sum(sol.x[4849:7639]>1e-10)),
            macro_positive_columns=int(sum(sol.x[7639:]>1e-10)),
            minimum_scaled_slack_float=float(min(sol.ineqlin.residual)))
    write('float',out);log('float-finished',**out);assert sol.success


def reconstruct():
    import numpy as np
    assert not path('exact.json').exists()
    started=time.time();data,rows,obj,norm=load();fl=np.load(path('float.npz'))
    fx,sl=fl['x'],fl['scaled_slacks']; positive={int(j) for j in np.flatnonzero(fx>1e-10)}
    dependent={};definitions=[]
    zz=json.loads((HERE/'complete_zz_5799_v1_mapping.json').read_text())
    for a in zz['auxiliaries']:
        j=a['column_index']
        if j not in positive:continue
        for rk,ck in [('upper_q_row','source_R_columns'),('upper_v_row','query_Z_columns')]:
            if abs(sl[a[rk]])<1e-10:
                dependent[j]={c:F(1) for c in a[ck] if c in positive}
                assert dependent[j]
                definitions.append({'column':j,'kind':'ZZ_upper','row':a[rk],
                    'expression':[[k,str(v)] for k,v in dependent[j].items()]})
                break
    mapping=json.loads(MAP.read_text())
    for group in mapping['groups']:
        for state in group['states']:
            pos=[j for j in state['hidden_columns'] if j in positive]
            if not pos:continue
            j=max(pos,key=lambda k:fx[k])
            expression={k:F(v) for k,v in state['old_marginal_affine'] if k in positive}
            expression.update({k:F(-1) for k in pos if k!=j})
            dependent[j]=expression
            definitions.append({'column':j,'kind':'macro_margin','row':state['equality_plus_row'],
                'expression':[[k,str(v)] for k,v in expression.items()]})
    core=sorted(positive-set(dependent));index={j:i for i,j in enumerate(core)}
    assert all(k in index for expression in dependent.values() for k in expression)
    def project(row):
        result=defaultdict(F)
        for j,v in row.items():
            if j in dependent:
                for k,a in dependent[j].items():result[index[k]]+=v*a
            elif j in index:result[index[j]]+=v
        return tuple(result.get(i,F()) for i in range(len(core)))
    eq=[];rhs=[];origins=[];seen=set()
    for i,row in enumerate(rows):
        if abs(sl[i])>1e-8:continue
        small=project(row)
        if not any(small) or small in seen:continue
        seen.add(small);eq.append(list(small));rhs.append(F());origins.append(i)
    eq.append([norm[j] for j in core]);rhs.append(F(1));origins.append('O=1')
    log('exact-primal-start',positive=len(positive),eliminated=len(dependent),
        core_variables=len(core),candidate_equations=len(eq))
    values,chosen=exact_linear_system(eq,rhs);full=[F()]*len(obj)
    for j,v in zip(core,values):full[j]=v
    for j,expression in dependent.items():full[j]=sum(a*full[k] for k,a in expression.items())
    slacks=[sum(v*full[j] for j,v in row.items() if full[j]) for row in rows]
    if min(full)<0 or min(slacks)<0:
        write('primal_diagnostic',{'negative_columns':[[j,str(v)] for j,v in enumerate(full) if v<0],
            'negative_rows':[[i,str(v)] for i,v in enumerate(slacks) if v<0],
            'support_threshold':1e-10,'active_threshold':1e-8})
    assert min(full)>=0 and min(slacks)>=0 and sum(n*v for n,v in zip(norm,full))==1
    W=sum(c*v for c,v in zip(obj,full))
    point={'scope':data['scope'],'exact_feasible':True,'exact_optimum_claim':False,
        'matrix_path':str(MATRIX.relative_to(ROOT)),'matrix_sha256':MATRIX_SHA,
        'O':'1','W':str(W),'W_float_for_display':float(W),'K':str(full[0]),
        'strict_half_gap_O_minus_2W':str(1-2*W),'verified_rows':len(rows),
        'minimum_slack':str(min(slacks)),'minimum_column_weight':str(min(full)),
        'positive_columns':sum(v>0 for v in full),'original_positive_columns':sum(v>0 for v in full[:4849]),
        'ZZ_positive_columns':sum(v>0 for v in full[4849:7639]),
        'macro_positive_columns':sum(v>0 for v in full[7639:]),
        'columns':[dict(c,weight=str(v)) for c,v in zip(data['columns'],full)]}
    pp=write('exact',point)
    write('basis',{'core_columns':core,'dependent_columns':definitions,
        'chosen_equation_rows':[origins[i] for i in chosen],'candidate_equations':len(eq),
        'core_variables':len(core),'seconds':time.time()-started})
    write('slacks',{'point_sha256':sha(pp),'rows':[
        {'index':i,'name':r['name'],'slack':str(v)} for i,(r,v) in enumerate(zip(data['rows'],slacks))]})
    log('exact-primal-passed',W=str(W),display=float(W),positive_columns=point['positive_columns'],
        minimum_slack=str(min(slacks)),seconds=time.time()-started)


def dual():
    import numpy as np
    from scipy.linalg import qr
    from sympy import ZZ
    from sympy.polys.matrices import DomainMatrix
    assert not path('dual.json').exists()
    started=time.time();data,rows,obj,norm=load()
    pp=path('exact.json');point=json.loads(pp.read_text());W=F(point['W'])
    previous=HERE/'complete_zz_5799_v1_dual.json';old=json.loads(previous.read_text())
    if W==F(old['dual_value']):
        records=old['row_multipliers'];method='Exact zero extension of previous complete-ZZ dual.'
        extra={'source_dual_path':str(previous.relative_to(ROOT)),'source_dual_sha256':sha(previous)}
    else:
        fl=np.load(path('float.npz'))
        support=[int(i) for i in np.flatnonzero(-fl['inequality_marginals']/fl['scales']>1e-10)]
        active=[j for j,c in enumerate(point['columns']) if F(c['weight'])>0 or abs(fl['lower_marginals'][j])<1e-12]
        eq=[];rhs=[];origins=[];seen=set()
        for j in active:
            r=tuple(rows[i].get(j,F()) for i in support);b=obj[j]-W*norm[j]
            if not any(r):assert b==0;continue
            if (r,b) in seen:continue
            seen.add((r,b));eq.append(r);rhs.append(b);origins.append(j)
        n=len(support);arr=np.array([[float(v) for v in r] for r in eq])
        scales=np.max(abs(arr),axis=1);scales[scales==0]=1
        _,r,piv=qr((arr/scales[:,None]).T,mode='economic',pivoting=True)
        diag=abs(np.diag(r));rank=int(sum(diag>1e-10*max(diag[0],1)));assert rank==n,(rank,n)
        chosen=list(map(int,piv[:n]));L=[math.lcm(*(v.denominator for v in rows[i].values())) for i in support]
        D=math.lcm(*(b.denominator for b in rhs));ae={};be={}
        for k,q in enumerate(chosen):
            for i,v in enumerate(eq[q]):
                if v:ae[k,i]=ZZ((v*L[i]).numerator)
            if rhs[q]:be[k,0]=ZZ((rhs[q]*D).numerator)
        log('exact-dual-start',support=n,candidate_equations=len(eq),rhs_denominator_digits=len(str(D)))
        a=DomainMatrix.from_dok(ae,(n,n),ZZ);b=DomainMatrix.from_dok(be,(n,1),ZZ)
        numer,denom=a.solve_den(b,method='rref')
        values=[F(int(v[0]),int(denom))*F(l,D) for v,l in zip(numer.to_list(),L)]
        if min(values)<0:write('dual_negative_diagnostic',{'weights':[[i,str(v)] for i,v in zip(support,values)],'negative':[[i,str(v)] for i,v in zip(support,values) if v<0]})
        assert min(values)>=0
        records=[{'row_index':i,'row_name':data['rows'][i]['name'],'weight':str(v)} for i,v in zip(support,values) if v]
        method='Exact per-row integer-scaled dual system, with full-column verification.'
        extra={'selected_column_equations':[origins[i] for i in chosen]}
    x=[F(c['weight']) for c in point['columns']]
    residual=[c-W*n for c,n in zip(obj,norm)]
    for record in records:
        i=record['row_index'];v=F(record['weight']);assert v>0
        assert record['row_name']==data['rows'][i]['name']
        for j,a in rows[i].items():residual[j]-=v*a
        assert v*sum(a*x[j] for j,a in rows[i].items() if x[j])==0
    if min(residual)<0:write('dual_residual_diagnostic',{'negative_columns':[[j,str(v)] for j,v in enumerate(residual) if v<0]})
    assert min(residual)>=0 and sum(v*r for v,r in zip(x,residual))==0
    out={'status':'passed','scope':data['scope'],'primal_value':str(W),'dual_value':str(W),
        'normalization_multiplier':str(W),'matrix_sha256':MATRIX_SHA,'point_sha256':sha(pp),
        'minimum_dual_residual':str(min(residual)),'positive_multipliers':len(records),
        'row_multipliers':records,'residuals':list(map(str,residual)),'reconstruction':method,
        'seconds':time.time()-started,**extra}
    write('dual',out);log('exact-dual-passed',W=str(W),positive_multipliers=len(records),seconds=time.time()-started)


def verify():
    started=time.time();data,rows,obj,norm=load()
    pp,dp=path('exact.json'),path('dual.json');point=json.loads(pp.read_text());dual=json.loads(dp.read_text())
    assert dual['matrix_sha256']==MATRIX_SHA and dual['point_sha256']==sha(pp)
    assert [{k:v for k,v in c.items() if k!='weight'} for c in point['columns']]==data['columns']
    for i,r in enumerate(data['rows']):assert r['index']==i and canonical_sha(r['nonzero'])==r['sparse_sha256']
    x=[F(c['weight']) for c in point['columns']];assert min(x)>=0
    assert sum(n*v for n,v in zip(norm,x))==1
    W=sum(c*v for c,v in zip(obj,x));assert W==F(point['W'])==F(dual['dual_value'])==F(dual['normalization_multiplier'])
    slacks=[sum(v*x[j] for j,v in row.items() if x[j]) for row in rows];assert min(slacks)>=0
    residual=[c-W*n for c,n in zip(obj,norm)];used=set()
    for r in dual['row_multipliers']:
        i=r['row_index'];v=F(r['weight']);assert i not in used and v>0;used.add(i)
        assert r['row_name']==data['rows'][i]['name'] and v*slacks[i]==0
        for j,a in rows[i].items():residual[j]-=v*a
    assert min(residual)>=0 and list(map(str,residual))==dual['residuals']
    assert sum(v*r for v,r in zip(x,residual))==0
    zz=json.loads((HERE/'complete_zz_5799_v1_mapping.json').read_text());canonical=list(x)
    for a in zz['auxiliaries']:
        canonical[a['column_index']]=min(sum(x[j] for j in a['source_R_columns']),sum(x[j] for j in a['query_Z_columns']))
    zz_slacks=[sum(v*canonical[j] for j,v in rows[c['row_index']].items()) for c in zz['classes']]
    assert min(zz_slacks)>=0
    projection={'scope':'Original 4849-column projection of the exact complete624/ZZ point; it is a necessary-system point, not an SPE.',
        'exact_feasible':True,'exact_optimum_claim':False,'O':'1','W':str(W),'K':str(x[0]),
        'parent_full_point_sha256':sha(pp),'parent_full_matrix_sha256':MATRIX_SHA,
        'verified_old_rows':5799,'additional_verified_ZZ_min_bounds':39,
        'positive_columns':sum(v>0 for v in x[:4849]),'minimum_slack':str(min(slacks[:5799])),
        'columns':point['columns'][:4849]}
    proj=write('original4849_exact',projection)
    h=[dict(c,column_index=j) for j,c in enumerate(projection['columns']) if c['kind']=='hist']
    u=[sum(F(c['weight'])*F(int(c['actual_bits'][i]),sum(map(int,c['actual_bits']))) for c in h if c['actual_bits'][i]=='1') for i in range(6)]
    write('visible',{'source':str(proj.relative_to(ROOT)),'point_sha256':sha(proj),'full_point_sha256':sha(pp),
        'O':'1','W':str(W),'K':str(x[0]),'actual_utilities':list(map(str,u)),'histograms':h})
    old=json.loads((HERE/'complete_zz_5799_v1_exact.json').read_text())
    out={'status':'PASS','scope':data['scope'],'rows':len(rows),'columns':len(x),
        'exact_optimum':str(W),'previous_complete_ZZ_W':old['W'],'W_change':str(W-F(old['W'])),
        'strict_half_gap':str(1-2*W),'minimum_primal_slack':str(min(slacks)),
        'minimum_column_weight':str(min(x)),'minimum_dual_residual':str(min(residual)),
        'positive_columns':sum(v>0 for v in x),'positive_multipliers':len(used),
        'positive_new_dual_rows':[r for r in dual['row_multipliers'] if r['row_index']>=11418],
        'all_39_ZZ_min_bounds_nonnegative':True,'minimum_ZZ_min_bound':str(min(zz_slacks)),
        'matrix_path':str(MATRIX.relative_to(ROOT)),'matrix_sha256':MATRIX_SHA,
        'point_sha256':sha(pp),'dual_sha256':sha(dp),'original4849_projection_sha256':sha(proj),
        'optimizer_calls':0,'math_float_operations':0,'seconds':time.time()-started}
    write('verification',out);log('full-exact-certificate-passed',**{k:v for k,v in out.items() if k!='positive_new_dual_rows'})


def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=('solve','reconstruct','dual','verify'));args=ap.parse_args()
    started=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    try:globals()[args.mode]();success=True
    finally:write('execution_'+args.mode,{'command':[sys.executable,'-B',str(Path(__file__).resolve()),args.mode],
        'cwd':str(ROOT),'started_utc':stamp,'elapsed_seconds':time.time()-started,'success':success,
        'python':platform.python_version(),'script_sha256':sha(__file__),'matrix_path':str(MATRIX.relative_to(ROOT)),
        'matrix_sha256':MATRIX_SHA,'mapping_sha256':MAP_SHA,'main_review_sha256':sha(REVIEW),
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})


if __name__=='__main__':main()

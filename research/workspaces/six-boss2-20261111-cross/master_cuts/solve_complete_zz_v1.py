#!/usr/bin/env python3
"""Solve/certify the reviewed 7639-column ZZ extension in separate stages.

Primal recovery eliminates positive auxiliary variables tied to an upper row,
so the exact square solve uses original positive columns and at most the few
remaining free auxiliaries. Final validation always checks the full matrix.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse,datetime,hashlib,json,platform,sys,time
import extend_master as engine
from merge_master import exact_linear_system,canonical_sha
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
STEM='complete_zz_5799_v1'
MATRIX_SHA='8b076497ef826b60c797edcb8dc719f2f7ad678a01a34ecf66d2e757af525a20'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def load():
    engine.STEM=STEM
    data,rows,obj,norm=engine.load()
    assert sha(HERE/(STEM+'_matrix.json.gz'))==MATRIX_SHA
    assert len(rows)==11418 and len(obj)==7639
    return data,rows,obj,norm

def check_review():
    p=HERE.parent/'main_verify_complete_zz_v1.json'
    review=json.loads(p.read_text());assert review['status']=='PASS'
    # The independently reviewed matrix identity appears in the report. Retain
    # the exact report hash without guessing a provider-specific field name.
    assert MATRIX_SHA in p.read_text()
    return {'path':str(p.relative_to(REPO)),'sha256':sha(p)}

def solve():
    import numpy as np
    assert not (HERE/(STEM+'_exact.json')).exists()
    load();engine.solve()
    fl=np.load(HERE/(STEM+'_float.npz'))
    positive=np.flatnonzero(fl['x']>1e-10)
    dual=np.flatnonzero(-fl['inequality_marginals']/fl['scales']>1e-10)
    engine.write('discovery_sizes',{'original_positive_columns':int(sum(positive<4849)),
        'auxiliary_positive_columns':int(sum(positive>=4849)),
        'positive_float_dual_rows':len(dual),'new_upper_dual_rows':int(sum((dual>=5799)&(dual<11379))),
        'new_budget_dual_rows':int(sum(dual>=11379)),
        'scope':'Floating discovery only; no exact feasibility or optimality assertion.'})

def reconstruct():
    import numpy as np
    started=time.time();data,rows,obj,norm=load()
    output=HERE/(STEM+'_exact.json');assert not output.exists()
    fl=np.load(HERE/(STEM+'_float.npz'));fx=fl['x'];sl=fl['scaled_slacks']
    mapping=json.loads((HERE/(STEM+'_mapping.json')).read_text())
    positive={int(j) for j in np.flatnonzero(fx>1e-10)}
    dependent={};free_aux=[];definitions=[]
    for a in mapping['auxiliaries']:
        j=a['column_index']
        if j not in positive:continue
        choices=[]
        for row_key,col_key in [('upper_q_row','source_R_columns'),('upper_v_row','query_Z_columns')]:
            if abs(sl[a[row_key]])<1e-10:choices.append((a[row_key],a[col_key]))
        if choices:
            origin,columns=choices[0]
            dependent[j]={c:F(1) for c in columns if c in positive}
            assert dependent[j]
            definitions.append({'auxiliary':j,'chosen_upper_row':origin,'expression_columns':columns})
        else:free_aux.append(j)
    core=sorted(j for j in positive if j<4849)+free_aux
    core_index={j:i for i,j in enumerate(core)}
    assert len(core)==len(positive)-len(dependent)
    def project(row):
        result=defaultdict(F)
        for j,v in row.items():
            if j in dependent:
                for k,c in dependent[j].items():result[core_index[k]]+=v*c
            elif j in core_index:result[core_index[j]]+=v
        return tuple(result.get(i,F()) for i in range(len(core)))
    equations=[];rhs=[];origins=[];seen=set()
    for i,row in enumerate(rows):
        if abs(sl[i])>1e-8:continue
        projected=project(row)
        if not any(projected) or projected in seen:continue
        seen.add(projected);equations.append(list(projected));rhs.append(F());origins.append(i)
    equations.append([norm[j] for j in core]);rhs.append(F(1));origins.append('O=1')
    engine.log('structured-primal-recovery',original_positive=sum(j<4849 for j in core),
        free_auxiliary_positive=len(free_aux),eliminated_auxiliaries=len(dependent),
        core_variables=len(core),candidate_equations=len(equations))
    values,chosen=exact_linear_system(equations,rhs)
    full=[F()]*len(obj)
    for j,value in zip(core,values):full[j]=value
    for j,expression in dependent.items():full[j]=sum(value*full[k] for k,value in expression.items())
    assert min(full)>=0 and sum(n*v for n,v in zip(norm,full))==1
    slacks=[sum(v*full[j] for j,v in row.items() if full[j]) for row in rows]
    assert min(slacks)>=0,(slacks.index(min(slacks)),min(slacks))
    W=sum(c*v for c,v in zip(obj,full))
    point={'scope':'Exact feasible point for the reviewed complete finite ZZ upper-bound extension. Auxiliary columns are not true intersections; no SPE or universal half assertion.',
        'exact_feasible':True,'exact_optimum_claim':False,'O':'1','W':str(W),'W_float_for_display':float(W),
        'K':str(full[0]),'strict_half_gap_O_minus_2W':str(1-2*W),
        'verified_rows':len(rows),'minimum_slack':str(min(slacks)),
        'minimum_column_weight':str(min(full)),'positive_columns':sum(v>0 for v in full),
        'original_positive_columns':sum(v>0 for v in full[:4849]),
        'auxiliary_positive_columns':sum(v>0 for v in full[4849:]),
        'columns':[dict(c,weight=str(v)) for c,v in zip(data['columns'],full)]}
    engine.write('exact',point)
    engine.write('basis',{'core_columns':core,'dependent_auxiliaries':definitions,
        'chosen_equation_rows':[origins[i] for i in chosen],
        'candidate_equations':len(equations),'core_variables':len(core),'seconds':time.time()-started})
    engine.write('slacks',{'point_sha256':sha(output),'rows':[{'index':i,'name':r['name'],'slack':str(v)} for i,(r,v) in enumerate(zip(data['rows'],slacks))]})
    engine.log('exact-expanded-primal',W=str(W),display=float(W),positive_columns=point['positive_columns'],
               original_positive_columns=point['original_positive_columns'],minimum_slack=str(min(slacks)),seconds=time.time()-started)

def dual():
    data,rows,obj,norm=load()
    pp=HERE/(STEM+'_exact.json');point=json.loads(pp.read_text());W=F(point['W'])
    old_path=HERE/'dynamic_5799_dual.json';old=json.loads(old_path.read_text())
    if W==F(old['dual_value']):
        # An exact feasible point at the previous lower bound closes the larger
        # LP. Zero-extension is a proof, without recovering a gratuitously
        # different floating dual basis.
        residual=[c-W*n for c,n in zip(obj,norm)]
        x=[F(c['weight']) for c in point['columns']]
        for record in old['row_multipliers']:
            i=record['row_index'];weight=F(record['weight'])
            assert i<5799 and weight>0 and record['row_name']==data['rows'][i]['name']
            for j,v in rows[i].items():residual[j]-=weight*v
            assert weight*sum(v*x[j] for j,v in rows[i].items())==0
        assert min(residual)>=0 and sum(v*r for v,r in zip(x,residual))==0
        out={'scope':'Exact zero-extension of the 5799 lower-bound certificate to the reviewed full ZZ matrix; equal-value full primal verified.',
             'status':'passed','primal_value':str(W),'dual_value':str(W),
             'normalization_multiplier':str(W),'minimum_dual_residual':str(min(residual)),
             'positive_multipliers':len(old['row_multipliers']),
             'matrix_sha256':MATRIX_SHA,'point_sha256':sha(pp),
             'row_multipliers':old['row_multipliers'],'residuals':list(map(str,residual)),
             'reconstruction':'Old exact row multipliers, with zero coefficients on every new upper/budget row and zero residuals on the new columns.',
             'source_dual_path':str(old_path.relative_to(REPO)),'source_dual_sha256':sha(old_path)}
        engine.write('dual',out);engine.log('exact-dual-zero-extension',value=str(W),multipliers=len(old['row_multipliers']))
    else:
        import scaled_dual
        scaled_dual.run({'stem':STEM},1e-10,None)

def verify():
    started=time.time();data,rows,obj,norm=load()
    pp=HERE/(STEM+'_exact.json');dp=HERE/(STEM+'_dual.json')
    point=json.loads(pp.read_text());dual=json.loads(dp.read_text())
    assert dual['matrix_sha256']==MATRIX_SHA and dual['point_sha256']==sha(pp)
    assert [engine.desc(c) for c in point['columns']]==data['columns']
    for i,row in enumerate(data['rows']):assert row['index']==i and canonical_sha(row['nonzero'])==row['sparse_sha256']
    x=[F(c['weight']) for c in point['columns']]
    assert min(x)>=0 and sum(n*v for n,v in zip(norm,x))==1
    W=sum(c*v for c,v in zip(obj,x))
    assert W==F(point['W'])==F(dual['dual_value'])==F(dual['normalization_multiplier'])
    slacks=[sum(v*x[j] for j,v in row.items() if x[j]) for row in rows];assert min(slacks)>=0
    residual=[c-W*n for c,n in zip(obj,norm)];used=set();new_dual=[]
    for record in dual['row_multipliers']:
        i=record['row_index'];weight=F(record['weight'])
        assert weight>0 and i not in used and record['row_name']==data['rows'][i]['name'];used.add(i)
        assert weight*slacks[i]==0
        for j,v in rows[i].items():residual[j]-=weight*v
        if i>=5799:new_dual.append(record)
    assert min(residual)>=0 and list(map(str,residual))==dual['residuals']
    assert sum(v*r for v,r in zip(x,residual))==0
    mapping=json.loads((HERE/(STEM+'_mapping.json')).read_text())
    canonical=list(x)
    for a in mapping['auxiliaries']:
        canonical[a['column_index']]=min(sum(x[j] for j in a['source_R_columns']),sum(x[j] for j in a['query_Z_columns']))
    min_values=[sum(v*canonical[j] for j,v in rows[c['row_index']].items()) for c in mapping['classes']]
    assert min(min_values)>=0
    # Freeze a separate exact 4849-column projection for existing separators.
    projection={k:v for k,v in point.items() if k not in ('columns','verified_rows','positive_columns','scope','minimum_slack','auxiliary_positive_columns')}
    projection.update({'scope':'Original 4849-column projection of an exact feasible full 11418x7639 point; all 5799 old rows and all 39 exact ZZ min upper bounds verified. No auxiliary column is a customer or a true intersection.',
        'verified_rows':5799,'additional_verified_ZZ_min_bounds':39,
        'parent_full_point_sha256':sha(pp),'parent_full_matrix_sha256':MATRIX_SHA,
        'parent_auxiliary_positive_columns':point['auxiliary_positive_columns'],
        'positive_columns':sum(v>0 for v in x[:4849]),'minimum_slack':str(min(slacks[:5799])),
        'columns':point['columns'][:4849]})
    projection_path=HERE/(STEM+'_original4849_exact.json')
    serialized=json.dumps(projection,ensure_ascii=False,indent=2)+'\n'
    if projection_path.exists():assert projection_path.read_text()==serialized
    else:projection_path.write_text(serialized)
    h=[dict(c,column_index=j) for j,c in enumerate(projection['columns']) if c['kind']=='hist']
    u=[sum(F(c['weight'])*F(int(c['actual_bits'][i]),sum(map(int,c['actual_bits']))) for c in h if c['actual_bits'][i]=='1') for i in range(6)]
    engine.write('visible',{'source':str(projection_path.relative_to(REPO)),'point_sha256':sha(projection_path),
        'full_point_sha256':sha(pp),'O':'1','W':str(W),'K':str(x[0]),
        'actual_utilities':list(map(str,u)),'histograms':h})
    old=json.loads((HERE/'dynamic_5799_exact.json').read_text())
    report={'status':'PASS','scope':'Exact primal/dual proof for the complete finite ZZ upper extension; original-column projection separately frozen for further separation.',
        'rows':len(rows),'columns':len(x),'exact_optimum':str(W),'previous_5799_W':old['W'],
        'W_change':str(W-F(old['W'])),'strict_half_gap':str(1-2*W),
        'positive_columns':sum(v>0 for v in x),'original_positive_columns':sum(v>0 for v in x[:4849]),
        'positive_dual_multipliers':len(used),'positive_new_dual_rows':new_dual,
        'minimum_primal_slack':str(min(slacks)),'minimum_dual_residual':str(min(residual)),
        'all_39_min_bounds_nonnegative':True,'minimum_ZZ_min_bound':str(min(min_values)),
        'ZZ_min_values':[{'class':c['class'],'slack':str(v)} for c,v in zip(mapping['classes'],min_values)],
        'matrix_sha256':MATRIX_SHA,'point_sha256':sha(pp),'dual_sha256':sha(dp),
        'original4849_projection_sha256':sha(projection_path),'seconds':time.time()-started,
        'optimizer_calls':0,'math_float_operations':0}
    engine.write('verification',report)
    engine.log('exact-extension-certified',**{k:v for k,v in report.items() if k not in ('positive_new_dual_rows','ZZ_min_values')})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('mode',choices=('solve','reconstruct','dual','verify'));args=ap.parse_args()
    engine.STEM=STEM;review=check_review();started=time.time();success=False
    stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:globals()[args.mode]();success=True
    finally:engine.write('execution_'+args.mode,{'command':[sys.executable,'-B',str(Path(__file__).resolve()),args.mode],
        'cwd':str(REPO),'script_sha256':sha(Path(__file__)),'review':review,
        'python':platform.python_version(),'started_utc':stamp,'elapsed_seconds':time.time()-started,'success':success})

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Append independently reviewed dynamic cuts without overwriting 5716 assets.

All Fraction rows are checked against their stated exact source point before
optimization. The output is another fixed-support necessary LP, never an SPE.
"""
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, math, os, platform, sys, time, traceback
from merge_master import HERE, REPO, canonical_sha, sha, desc, exact_linear_system
STEM='dynamic_5727'
RUN=HERE.parent


def write(name,value):
    path=HERE/(STEM+'_'+name+'.json');path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');return path

def read(name):return json.loads((HERE/(STEM+'_'+name+'.json')).read_text())
def log(stage,**kw):print(json.dumps({'stage':stage,**kw},ensure_ascii=False),flush=True)
def full_hash(sparse,ncols):
    v=['0']*ncols
    for j,x in sparse:v[j]=str(F(x))
    return hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest()

def prepare():
    start=time.time()
    with gzip.open(HERE/'master_5716_exact.json.gz','rt',encoding='utf-8') as f:base=json.load(f)
    point_path=HERE/'merged_5716_exact.json';point=json.loads(point_path.read_text());pointsha=sha(point_path)
    assert base['row_count']==5716 and base['column_count']==4849
    assert [desc(c) for c in point['columns']]==base['columns']
    x=[F(c['weight']) for c in point['columns']]
    sources=[RUN/'coverage_bridge/new5716_joint_discounted.json',RUN/'joint_requery/selected_cuts_5716.json']
    additions=[];input_manifest=[]
    for family,path in zip(('discounted','pair'),sources):
        pack=json.loads(path.read_text());source_sha=pack.get('input_sha256',pack.get('source_sha256'));assert source_sha==pointsha
        input_manifest.append({'family':family,'path':str(path.relative_to(REPO)),'sha256':sha(path),'point_sha256':source_sha})
        cuts=([r for r in pack['results'] if F(r.get('exact_slack','0'))<0] if family=='discounted' else pack['cuts'])
        for local_index,cut in enumerate(cuts,1):
            sparse=cut['row_nonzero'] if family=='discounted' else cut['sparse_row']
            assert all(isinstance(j,int) and 0<=j<4849 and F(v) for j,v in sparse)
            assert len({j for j,v in sparse})==len(sparse)
            sparse=sorted([[j,str(F(v))] for j,v in sparse])
            assert full_hash(sparse,4849)==cut['row_sha256']
            slack=sum(F(v)*x[j] for j,v in sparse);assert slack==F(cut['exact_slack'])<0
            parameters={k:v for k,v in cut.items() if k not in ('row_nonzero','sparse_row','visible')}
            additions.append({'index':5716+len(additions),'name':f'dynamic-{family}-{local_index}','sparse_sha256':canonical_sha(sparse),'full_vector_sha256':cut['row_sha256'],'nonzero':sparse,'source_pack':str(path.relative_to(REPO)),'source_pack_sha256':sha(path),'source_parameters':parameters,'at_5716_slack':str(slack)})
    assert len(additions)==11 and len({r['sparse_sha256'] for r in additions})==11
    assert not {r['sparse_sha256'] for r in additions}&{r['sparse_sha256'] for r in base['rows']}
    matrix=dict(base);matrix['scope']='Fixed sixteen histograms: certified 5716-row master plus six same-source discounted Bellman rows and five shared-two-branch PAIR rows; necessary LP only, no SPE or universal half inference.'
    matrix['base_row_count']=5716;matrix['added_row_count']=11;matrix['rows']=base['rows']+additions;matrix['row_count']=5727
    with gzip.open(HERE/(STEM+'_matrix.json.gz'),'wt',encoding='utf-8') as f:json.dump(matrix,f,ensure_ascii=False,separators=(',',':'))
    identity={'scope':matrix['scope'],'rows':5727,'columns':4849,'input_point_sha256':pointsha,'base_matrix_sha256':sha(HERE/'master_5716_exact.json.gz'),'input_packs':input_manifest,'new_rows':[{'index':r['index'],'name':r['name'],'full_vector_sha256':r['full_vector_sha256'],'sparse_sha256':r['sparse_sha256'],'at_5716_slack':r['at_5716_slack']} for r in additions],'matrix_sha256':sha(HERE/(STEM+'_matrix.json.gz')),'descriptor_sha256':canonical_sha(matrix['columns']),'row_vector_list_sha256':canonical_sha([r['sparse_sha256'] for r in matrix['rows']]),'seconds':time.time()-start}
    write('identity',identity);log('prepared',rows=5727,columns=4849,nonzeros=sum(len(r['nonzero']) for r in matrix['rows']),seconds=time.time()-start)

def load():
    with gzip.open(HERE/(STEM+'_matrix.json.gz'),'rt',encoding='utf-8') as f:data=json.load(f)
    return data,[{j:F(v) for j,v in r['nonzero']} for r in data['rows']],[F(v) for v in data['objective']],[F(v) for v in data['normalization']]

def solve():
    start=time.time();import numpy as np
    from scipy.sparse import csr_matrix
    from scipy.optimize import linprog
    data,rows,obj,norm=load();rr=[];cc=[];vv=[];sc=[]
    for i,row in enumerate(rows):
        scale=max((abs(v) for v in row.values()),default=F(1));sc.append(float(scale))
        for j,v in row.items():rr.append(i);cc.append(j);vv.append(-float(v/scale))
    m=csr_matrix((vv,(rr,cc)),shape=(len(rows),len(obj)))
    sol=linprog(list(map(float,obj)),A_ub=m,b_ub=np.zeros(len(rows)),A_eq=csr_matrix([list(map(float,norm))]),b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'time_limit':180})
    out={'scope':data['scope'],'success':bool(sol.success),'message':sol.message,'status':int(sol.status),'W_float':None if sol.fun is None else float(sol.fun),'rows':len(rows),'columns':len(obj),'float_only':True,'seconds':time.time()-start}
    if sol.success:
        np.savez(HERE/(STEM+'_float.npz'),x=sol.x,scaled_slacks=sol.ineqlin.residual,inequality_marginals=sol.ineqlin.marginals,lower_marginals=sol.lower.marginals,scales=np.array(sc))
        out.update({'iterations':int(sol.nit),'positive_columns_1e_10':int(sum(sol.x>1e-10)),'minimum_scaled_slack_float':float(min(sol.ineqlin.residual))})
    write('float',out);log('float-solved',**out);assert sol.success

def reconstruct():
    start=time.time();import numpy as np
    data,rows,obj,norm=load();fl=np.load(HERE/(STEM+'_float.npz'));x=fl['x'];ss=fl['scaled_slacks'];keep=[int(j) for j in np.flatnonzero(x>1e-10)]
    eq=[];rhs=[];origins=[];seen=set()
    for i,row in enumerate(rows):
        if abs(ss[i])>1e-8:continue
        small=tuple(row.get(j,F()) for j in keep)
        if not any(small) or small in seen:continue
        seen.add(small);eq.append(list(small));rhs.append(F());origins.append(i)
    eq.append([norm[j] for j in keep]);rhs.append(F(1));origins.append('O=1')
    log('reconstructing',support=len(keep),candidate_equations=len(eq))
    vals,chosen=exact_linear_system(eq,rhs);full=[F()]*len(obj)
    for j,v in zip(keep,vals):full[j]=v
    assert min(full)>=0 and sum(v*w for v,w in zip(norm,full))==1
    slacks=[sum(v*full[j] for j,v in row.items()) for row in rows];assert min(slacks)>=0,(slacks.index(min(slacks)),min(slacks))
    W=sum(v*w for v,w in zip(obj,full));cols=[dict(c,weight=str(v)) for c,v in zip(data['columns'],full)]
    point={'scope':data['scope'],'exact_feasible':True,'exact_optimum_claim':False,'O':'1','W':str(W),'W_float_for_display':float(W),'K':str(full[0]),'strict_half_gap_O_minus_2W':str(1-2*W),'verified_rows':len(rows),'minimum_slack':str(min(slacks)),'minimum_column_weight':str(min(full)),'positive_columns':sum(v>0 for v in full),'columns':cols}
    outpath=write('exact',point)
    write('basis',{'positive_column_indices':keep,'chosen_equation_rows':[origins[i] for i in chosen],'candidate_equations':len(eq),'seconds':time.time()-start})
    write('slacks',{'point_sha256':sha(outpath),'rows':[{'index':i,'name':r['name'],'slack':str(s)} for i,(r,s) in enumerate(zip(data['rows'],slacks))]})
    h=[dict(c,column_index=j) for j,c in enumerate(cols) if c['kind']=='hist'];u=[sum(F(c['weight'])*F(int(c['actual_bits'][i]),sum(map(int,c['actual_bits']))) for c in h if c['actual_bits'][i]=='1') for i in range(6)]
    write('visible',{'source':str(outpath.relative_to(REPO)),'point_sha256':sha(outpath),'O':'1','W':str(W),'K':str(full[0]),'actual_utilities':list(map(str,u)),'histograms':h})
    log('exact-primal',**{k:v for k,v in point.items() if k!='columns'},seconds=time.time()-start)

def dual():
    start=time.time();import numpy as np
    data,rows,obj,norm=load();fl=np.load(HERE/(STEM+'_float.npz'));point=read('exact');W=F(point['W'])
    support=[int(i) for i in np.flatnonzero(-fl['inequality_marginals']/fl['scales']>1e-10)]
    activecols=[int(j) for j in np.flatnonzero(abs(fl['lower_marginals'])<1e-8)]
    eq=[];rhs=[];origins=[];seen=set()
    for j in activecols:
        r=tuple(rows[i].get(j,F()) for i in support);b=obj[j]-W*norm[j]
        if not any(r):assert b==0;continue
        if (r,b) in seen:continue
        seen.add((r,b));eq.append(list(r));rhs.append(b);origins.append(j)
    log('dual-reconstructing',support=len(support),candidate_equations=len(eq))
    vals,chosen=exact_linear_system(eq,rhs);assert min(vals)>=0
    residual=[obj[j]-W*norm[j] for j in range(len(obj))]
    for i,v in zip(support,vals):
        for j,c in rows[i].items():residual[j]-=v*c
    assert min(residual)>=0,(residual.index(min(residual)),min(residual))
    pointpath=HERE/(STEM+'_exact.json');matrixpath=HERE/(STEM+'_matrix.json.gz')
    out={'scope':data['scope'],'status':'passed','primal_value':str(W),'dual_value':str(W),'normalization_multiplier':str(W),'minimum_multiplier':str(min(vals)),'minimum_dual_residual':str(min(residual)),'positive_multipliers':sum(v>0 for v in vals),'matrix_sha256':sha(matrixpath),'point_sha256':sha(pointpath),'row_multipliers':[{'row_index':i,'row_name':data['rows'][i]['name'],'weight':str(v)} for i,v in zip(support,vals) if v],'residuals':list(map(str,residual)),'selected_column_equations':[origins[i] for i in chosen],'seconds':time.time()-start}
    write('dual',out);log('exact-dual',**{k:v for k,v in out.items() if k not in ('row_multipliers','residuals','selected_column_equations')})

def verify():
    start=time.time();data,rows,obj,norm=load();point=read('exact');dual=read('dual');identity=read('identity');old=json.loads((HERE/'merged_5716_exact.json').read_text())
    assert sha(HERE/(STEM+'_matrix.json.gz'))==identity['matrix_sha256']==dual['matrix_sha256']
    assert sha(HERE/(STEM+'_exact.json'))==dual['point_sha256']
    assert [desc(c) for c in point['columns']]==data['columns']==[desc(c) for c in old['columns']]
    assert canonical_sha(data['columns'])==identity['descriptor_sha256']
    for i,r in enumerate(data['rows']):assert r['index']==i and canonical_sha(r['nonzero'])==r['sparse_sha256']
    assert canonical_sha([r['sparse_sha256'] for r in data['rows']])==identity['row_vector_list_sha256']
    x=[F(c['weight']) for c in point['columns']];ox=[F(c['weight']) for c in old['columns']]
    assert min(x)>=0 and sum(a*b for a,b in zip(norm,x))==1
    W=sum(a*b for a,b in zip(obj,x));assert W==F(point['W'])==F(dual['dual_value'])==F(dual['normalization_multiplier'])
    slacks=[sum(v*x[j] for j,v in row.items() if x[j]) for row in rows];assert min(slacks)>=0
    residual=[c-W*n for c,n in zip(obj,norm)];used=set();added_weights=[]
    for r in dual['row_multipliers']:
        i=r['row_index'];v=F(r['weight']);assert v>=0 and i not in used;used.add(i);assert r['row_name']==data['rows'][i]['name']
        for j,c in rows[i].items():residual[j]-=v*c
        assert v*slacks[i]==0
        if i>=5716:added_weights.append(r)
    assert min(residual)>=0 and list(map(str,residual))==dual['residuals']
    assert sum(r*v for r,v in zip(residual,x))==0
    newrows=[{'index':i,'name':data['rows'][i]['name'],'at_5716_slack':str(sum(v*ox[j] for j,v in rows[i].items())),'at_5727_slack':str(slacks[i]),'parameters':data['rows'][i]['source_parameters']} for i in range(5716,5727)]
    kinds=defaultdict(lambda:{'columns':0,'changed':0,'old_positive':0,'new_positive':0})
    for c,v,w in zip(data['columns'],x,ox):
        k=kinds[c['kind']];k['columns']+=1;k['changed']+=v!=w;k['old_positive']+=w>0;k['new_positive']+=v>0
    report={'status':'passed','scope':data['scope'],'exact_optimum':str(W),'old_W':old['W'],'W_change':str(W-F(old['W'])),'strict_half_gap':str(1-2*W),'rows':len(rows),'columns':len(x),'minimum_primal_slack':str(min(slacks)),'minimum_dual_residual':str(min(residual)),'positive_multipliers':len(used),'new_rows_positive_dual_weights':added_weights,'new_rows':newrows,'column_changes_by_kind':dict(kinds),'point_sha256':sha(HERE/(STEM+'_exact.json')),'matrix_sha256':sha(HERE/(STEM+'_matrix.json.gz')),'dual_sha256':sha(HERE/(STEM+'_dual.json')),'seconds':time.time()-start,'math_float_operations':0,'optimizer_calls':0}
    write('verification',report);log('certificate-verified',**{k:v for k,v in report.items() if k not in ('new_rows','column_changes_by_kind','new_rows_positive_dual_weights')})

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('prepare','solve','reconstruct','dual','verify','all'));args=parser.parse_args();start=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    actions={'prepare':prepare,'solve':solve,'reconstruct':reconstruct,'dual':dual,'verify':verify}
    try:
        for name,action in actions.items():
            if args.mode in (name,'all'):action()
        success=True
    finally:
        write('execution_'+args.mode,{'command':[sys.executable,'-B',str(Path(__file__).resolve()),args.mode],'cwd':os.getcwd(),'script_sha256':sha(__file__),'python':platform.python_version(),'started_utc':stamp,'elapsed_seconds':time.time()-start,'success':success})
if __name__=='__main__':main()

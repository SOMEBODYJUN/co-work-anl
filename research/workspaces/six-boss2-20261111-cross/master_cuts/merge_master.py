#!/usr/bin/env python3
"""Merge exactly the 24 frozen rational cuts into the certified 5692-row master.

All writes stay under this script's directory. Frozen sources are read-only.
Every output point is a necessary-system point, never a complete-history SPE.
"""
from __future__ import annotations
import argparse, gzip, hashlib, importlib.util, json, math, os, platform, subprocess, sys, time
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
EV = REPO / 'archives/customer-attraction/tools/evidence'
BPK = EV / 'b-family-menu-prices-boss3'
CPK = EV / 'requery-capacity-cut-packs-boss3'
BASE = Path('research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1')
RUNTIME = REPO.parent / 'boss2-master-runtime'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def canonical_sha(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def save(name, value):
    target = HERE / name
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    return target


def announce(stage, **values):
    print(json.dumps({'stage':stage, **values}, ensure_ascii=False), flush=True)


def desc(column):
    # Frozen overlap descriptors contain nested tuples before JSON serialization.
    return json.loads(json.dumps({k:v for k,v in column.items() if k != 'weight'}))


def materialize():
    began = time.time()
    base_pkg = EV / 'combined-branch-master-program'
    if not RUNTIME.exists():
        subprocess.run([sys.executable, '-B', str(base_pkg/'materialize_runtime.py'), str(RUNTIME)], check=True)
    manifest = json.loads((base_pkg/'source-manifest.json').read_text())['frozen_sources']
    original_records = []
    for rec in manifest:
        original = REPO / rec['stored_path']
        data = original.read_bytes()
        assert len(data) == rec['size'] and sha(original) == rec['sha256']
        destination = RUNTIME / rec['path']
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        original_records.append({'role':'base', 'source':str(original.relative_to(REPO)), 'runtime_path':rec['path'], 'sha256':rec['sha256']})
    # The archived outer materializer expects a nonexistent `stored_path` key.
    # Its actual nine-source manifest uses repository-relative `local_original`.
    overlays = json.loads((BPK/'source-manifest.json').read_text())
    for rec in overlays:
        source_path = rec.get('local_original', rec.get('local_replay'))
        target_path = rec.get('path', str(BASE/'research_2'/rec.get('basename', '')))
        assert source_path and target_path
        original = REPO / source_path
        data = original.read_bytes()
        assert len(data) == rec['size'] and sha(original) == rec['sha256'], rec['id']
        destination = RUNTIME / target_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        original_records.append({'role':'overlay', 'source':source_path, 'runtime_path':target_path, 'sha256':rec['sha256']})
    final = {rec['runtime_path']:rec for rec in original_records}
    for path, rec in final.items():
        assert sha(RUNTIME/path) == rec['sha256']
    save('materialization.json', {'status':'passed', 'base_files':len(manifest), 'overlays':len(overlays), 'final_runtime_files':len(final), 'adapter':'local_original/local_replay are repository-relative; basename records route to research_2. Frozen outer materializer expects absent stored_path. Actual manifest has eight overlays, despite README nine.', 'input_records':original_records, 'seconds':time.time()-began})
    announce('materialized', base_files=len(manifest), overlays=len(overlays))


def audit():
    began=time.time()
    spec=importlib.util.spec_from_file_location('independent_cut_audit', CPK/'audit_cut_packs.py')
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    point_path=BPK/'original/research_2/all_menu_prices_exact.json'
    point=json.loads(point_path.read_text());common=point['columns'][:1905]
    assert len(point['columns'])==4849 and point['verified_rows']==5692
    pointweights=[F(c['weight']) for c in point['columns']]
    for rec in json.loads((CPK/'source-manifest.json').read_text()):
        assert sha(CPK/rec['evidence_path'])==rec['sha256']
    old_sparse=json.loads((CPK/'runs/all-sparse-row-coefficients.json').read_text())
    old_lookup={(r['pack'],r['field'],r['number']):r for r in old_sparse}
    packs=[('early_reply_requery_master_all_queries.json','selected','requery'),('capacity_master_price_cuts.json','selected','portfolio'),('coupled_pending_cuts.json','portfolio','portfolio'),('coupled_pending_cuts.json','requery','requery')]
    distinct={};records=[];inputs={str(point_path.relative_to(REPO)):sha(point_path)}
    for filename,field,kind in packs:
        path=mod.R3/filename;pack=json.loads(path.read_text());inputs[str(path.relative_to(REPO))]=sha(path)
        source=CPK/'original'/pack['source'];sourcepoint=json.loads(source.read_text());inputs[str(source.relative_to(REPO))]=sha(source)
        assert [desc(c) for c in sourcepoint['columns'][:1905]]==[desc(c) for c in common]
        sw=[F(c['weight']) for c in sourcepoint['columns'][:1905]]
        for number,item in enumerate(pack[field],1):
            row=mod.independent_row(common,kind,item['cut'])
            nonzero=[[j,str(x)] for j,x in enumerate(row) if x]
            saved=old_lookup[filename,field,number]
            assert saved['nonzero']==nonzero
            oldvalue=sum(x*y for x,y in zip(row,sw))
            assert oldvalue==F(item['slack'])<0
            key=canonical_sha(nonzero)
            label=f'{filename}:{field}:{number}'
            value=sum(x*y for x,y in zip(row,pointweights))
            record={'label':label,'kind':kind,'cut':item['cut'],'same_source_slack':str(oldvalue),'at_5692_slack':str(value),'sparse_sha256':key}
            records.append(record)
            if key not in distinct:
                distinct[key]={'name':'frozen-cut-'+str(len(distinct)+1),'sparse_sha256':key,'common_length':1905,'nonzero':nonzero,'records':[]}
            distinct[key]['records'].append(record)
    assert len(records)==27 and len(distinct)==24
    cols_desc=[desc(c) for c in point['columns']]
    result={'status':'passed','seconds':time.time()-began,'records':27,'distinct_rows':24,'input_sha256':inputs,'common_descriptor_sha256':canonical_sha(cols_desc[:1905]),'master_descriptor_sha256':canonical_sha(cols_desc),'old_master_W':point['W'],'old_master_K':point['columns'][0]['weight'],'old_master_new_cut_negative_count':sum(F(v['records'][0]['at_5692_slack'])<0 for v in distinct.values()),'old_master_new_cut_minimum':str(min(F(v['records'][0]['at_5692_slack']) for v in distinct.values())),'cuts':list(distinct.values())}
    save('cuts_24_exact.json',result)
    announce('independent-cut-reconstruction', **{k:v for k,v in result.items() if k not in ('cuts','input_sha256')})


def build():
    began=time.time()
    sys.path.insert(0,str(RUNTIME/BASE/'research_2'))
    import B_menu_prices_master as bm
    cols,names,rows,obj,norm=bm.build(all_families=True)
    assert (len(rows),len(cols))==(5692,4849)
    saved=json.loads((BPK/'original/research_2/all_menu_prices_exact.json').read_text())
    assert len(saved['columns'])==len(cols)
    mismatches=[{'index':i,'built':desc(c),'saved':desc(o)} for i,(c,o) in enumerate(zip(cols,saved['columns'])) if desc(c)!=desc(o)]
    save('descriptor_mismatches.json',mismatches)
    if mismatches: announce('descriptor-mismatches',count=len(mismatches),first=mismatches[:3])
    assert not mismatches
    announce('master-built', rows=len(rows), columns=len(cols), seconds=time.time()-began)
    exactcuts=json.loads((HERE/'cuts_24_exact.json').read_text())
    oldrowhash={}
    sparse=[]
    for i,row in enumerate(rows):
        nr=[[j,str(v)] for j,v in enumerate(row) if v]
        digest=canonical_sha(nr);oldrowhash.setdefault(digest,[]).append(i)
        sparse.append({'index':i,'name':names[i],'sparse_sha256':digest,'nonzero':nr})
    duplicates=[]
    for cut in exactcuts['cuts']:
        if cut['sparse_sha256'] in oldrowhash:
            duplicates.append({'cut':cut['name'],'old_indices':oldrowhash[cut['sparse_sha256']]})
        sparse.append({'index':len(sparse),'name':cut['name'],'sparse_sha256':cut['sparse_sha256'],'nonzero':cut['nonzero'],'record_labels':[r['label'] for r in cut['records']]})
    data={'scope':'Fixed sixteen histograms; 5692 certified inherited rows plus 24 distinct frozen rational vectors. Necessary system only; not complete-history SPE.','columns':[desc(c) for c in cols],'row_count':len(sparse),'column_count':len(cols),'base_row_count':5692,'added_row_count':24,'appended_rows_already_in_base':duplicates,'objective':[str(v) for v in obj],'normalization':[str(v) for v in norm],'rows':sparse}
    with gzip.open(HERE/'master_5716_exact.json.gz','wt',encoding='utf-8') as handle:
        json.dump(data,handle,ensure_ascii=False,separators=(',',':'))
    save('matrix_identity.json',{'rows':len(sparse),'columns':len(cols),'base_rows':5692,'added_rows':24,'descriptor_sha256':canonical_sha(data['columns']),'row_vector_list_sha256':canonical_sha([r['sparse_sha256'] for r in sparse]),'row_name_list_sha256':canonical_sha([r['name'] for r in sparse]),'matrix_file_sha256':sha(HERE/'master_5716_exact.json.gz'),'already_in_base':duplicates,'objective_sha256':canonical_sha(data['objective']),'normalization_sha256':canonical_sha(data['normalization']),'seconds':time.time()-began})
    announce('matrix-exported', rows=len(sparse),columns=len(cols),nonzeros=sum(len(r['nonzero']) for r in sparse),already_in_base=duplicates,seconds=time.time()-began)


def load_matrix():
    with gzip.open(HERE/'master_5716_exact.json.gz','rt',encoding='utf-8') as handle: data=json.load(handle)
    rows=[{j:F(v) for j,v in r['nonzero']} for r in data['rows']]
    return data,rows,[F(x) for x in data['objective']],[F(x) for x in data['normalization']]


def solve():
    began=time.time()
    import numpy as np
    import scipy
    from scipy.sparse import csr_matrix
    from scipy.optimize import linprog
    data,rows,obj,norm=load_matrix();nc=data['column_count']
    rr=[];cc=[];vv=[];scales=[]
    for i,row in enumerate(rows):
        scale=max((abs(v) for v in row.values()),default=F(1));scales.append(float(scale))
        for j,v in row.items():rr.append(i);cc.append(j);vv.append(-float(v)/float(scale))
    mat=csr_matrix((vv,(rr,cc)),shape=(len(rows),nc))
    sol=linprog(list(map(float,obj)),A_ub=mat,b_ub=np.zeros(len(rows)),A_eq=csr_matrix([list(map(float,norm))]),b_eq=[1],bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-9,'dual_feasibility_tolerance':1e-9,'time_limit':180})
    out={'scope':data['scope'],'success':bool(sol.success),'status':sol.message,'status_code':int(sol.status),'W_float':None if sol.fun is None else float(sol.fun),'rows':len(rows),'columns':nc,'seconds':time.time()-began,'scipy':scipy.__version__,'numpy':np.__version__,'float_only':True}
    if sol.success:
        np.savez(HERE/'solution_float.npz',x=sol.x,inequality_marginals=sol.ineqlin.marginals,equality_marginal=sol.eqlin.marginals,lower_marginals=sol.lower.marginals,scales=np.array(scales),scaled_slacks=sol.ineqlin.residual)
        out.update({'iterations':int(sol.nit),'positive_columns_1e_10':int(sum(sol.x>1e-10)),'minimum_scaled_slack_float':float(min(sol.ineqlin.residual)),'normalization_float':float(np.dot(np.array(list(map(float,norm))),sol.x))})
    save('solve_float.json',out);announce('float-solve',**out)


def exact_linear_system(equations, rhs):
    """Choose full-rank rows numerically, solve selected INTEGER equations exactly.

    Numerical rank selection is heuristic only. The returned rationals are
    subsequently verified against the complete original rational system.
    """
    import numpy as np
    from scipy.linalg import qr
    from sympy.polys.matrices import DomainMatrix
    from sympy import ZZ
    n=len(equations[0])
    arr=np.array([[float(v) for v in eq] for eq in equations])
    norms=np.max(abs(arr),axis=1);norms[norms==0]=1
    _,r,piv=qr((arr/norms[:,None]).T,mode='economic',pivoting=True)
    diag=np.abs(np.diag(r));rank=int(sum(diag>1e-10*max(diag[0],1)))
    assert rank==n,(rank,n,diag[-5:])
    selected=[int(i) for i in piv[:n]]
    entries={};bentries={}
    for i,k in enumerate(selected):
        den=math.lcm(*(v.denominator for v in equations[k]),rhs[k].denominator)
        for j,v in enumerate(equations[k]):
            if v:entries[i,j]=ZZ(int(v*den))
        if rhs[k]:bentries[i,0]=ZZ(int(rhs[k]*den))
    a=DomainMatrix.from_dok(entries,(n,n),ZZ)
    b=DomainMatrix.from_dok(bentries,(n,1),ZZ)
    numer,denom=a.solve_den(b,method='rref')
    out=[F(int(v[0]),int(denom)) for v in numer.to_list()]
    assert all(sum(v*x for v,x in zip(equations[k],out))==rhs[k] for k in selected)
    return out,selected


def reconstruct():
    began=time.time()
    import numpy as np
    data,rows,obj,norm=load_matrix();floating=np.load(HERE/'solution_float.npz');x=floating['x'];ss=floating['scaled_slacks']
    keep=[int(j) for j in np.flatnonzero(x>1e-10)]
    eqs=[];rhs=[];origins=[];seen=set()
    for i,row in enumerate(rows):
        if abs(ss[i])>1e-8:continue
        small=tuple(row.get(j,F()) for j in keep)
        if not any(small) or small in seen:continue
        seen.add(small);eqs.append(list(small));rhs.append(F());origins.append(i)
    eqs.append([norm[j] for j in keep]);rhs.append(F(1));origins.append('O=1')
    announce('rational-reconstruction-start',positive_support=len(keep),candidate_equations=len(eqs))
    vals,selected=exact_linear_system(eqs,rhs)
    full=[F()]*data['column_count']
    for j,v in zip(keep,vals):full[j]=v
    assert min(full)>=0
    assert sum(v*w for v,w in zip(norm,full))==1
    slacks=[sum(v*full[j] for j,v in row.items()) for row in rows]
    assert min(slacks)>=0,(slacks.index(min(slacks)),min(slacks))
    W=sum(v*w for v,w in zip(obj,full))
    cols=[dict(c,weight=str(w)) for c,w in zip(data['columns'],full)]
    report={'scope':data['scope'],'exact_feasible':True,'exact_optimum_claim':False,'O':'1','W':str(W),'W_float_for_display':float(W),'K':str(full[0]),'strict_half_gap_O_minus_2W':str(1-2*W),'verified_rows':len(rows),'minimum_slack':str(min(slacks)),'minimum_column_weight':str(min(full)),'minimum_strictly_positive_slack':str(min(v for v in slacks if v>0)),'positive_columns':sum(bool(v) for v in full),'columns':cols}
    save('merged_5716_exact.json',report)
    hist=[dict(c,column_index=j) for j,c in enumerate(cols) if c['kind']=='hist']
    pay=[sum(F(c['weight'])*F(int(c['actual_bits'][i]),sum(map(int,c['actual_bits']))) for c in hist if c['actual_bits'][i]=='1') for i in range(6)]
    save('visible_projection.json',{'source':'merged_5716_exact.json','point_sha256':sha(HERE/'merged_5716_exact.json'),'O':'1','W':str(W),'K':str(full[0]),'actual_utilities':list(map(str,pay)),'histograms':hist})
    save('primal_basis.json',{'support_column_indices':keep,'selected_equation_rows':[origins[i] for i in selected],'candidate_equations':len(eqs),'selected_equations':len(selected),'method':'Float QR selects equations; integer DomainMatrix solve_den with exact rational result; all 5716 original rational rows checked afterwards.','seconds':time.time()-began})
    save('exact_slacks.json',{'matrix_sha256':sha(HERE/'master_5716_exact.json.gz'),'point_sha256':sha(HERE/'merged_5716_exact.json'),'rows':[{'index':i,'name':r['name'],'slack':str(s)} for i,(r,s) in enumerate(zip(data['rows'],slacks))]})
    announce('exact-primal-certified',**{k:v for k,v in report.items() if k!='columns'},seconds=time.time()-began)


def verify():
    began=time.time();data,rows,obj,norm=load_matrix();point=json.loads((HERE/'merged_5716_exact.json').read_text());old=json.loads((BPK/'original/research_2/all_menu_prices_exact.json').read_text())
    assert [desc(c) for c in point['columns']]==data['columns']
    assert [desc(c) for c in old['columns']]==data['columns']
    x=[F(c['weight']) for c in point['columns']];ox=[F(c['weight']) for c in old['columns']]
    slacks=[sum(v*x[j] for j,v in row.items()) for row in rows];oldslacks=[sum(v*ox[j] for j,v in row.items()) for row in rows]
    W=sum(v*z for v,z in zip(obj,x));assert W==F(point['W']);assert min(x)>=0 and min(slacks)>=0 and sum(v*z for v,z in zip(norm,x))==1
    assert min(oldslacks[:5692])>=0
    counts=defaultdict(lambda:{'columns':0,'changed':0,'old_positive':0,'new_positive':0})
    for c,z,y in zip(data['columns'],x,ox):
        a=counts[c['kind']];a['columns']+=1;a['changed']+=z!=y;a['old_positive']+=y>0;a['new_positive']+=z>0
    newrows=[{'row':i,'name':data['rows'][i]['name'],'old_slack':str(oldslacks[i]),'new_slack':str(slacks[i]),'record_labels':data['rows'][i].get('record_labels',[])} for i in range(5692,len(rows))]
    result={'status':'passed','matrix_sha256':sha(HERE/'master_5716_exact.json.gz'),'point_sha256':sha(HERE/'merged_5716_exact.json'),'rows':len(rows),'columns':len(x),'old_matrix_minimum_slack':str(min(oldslacks[:5692])),'new_matrix_minimum_slack':str(min(slacks)),'old_W':old['W'],'new_W':str(W),'W_change':str(W-F(old['W'])),'new_strict_half_gap':str(1-2*W),'column_changes_by_kind':dict(counts),'new_rows':newrows,'seconds':time.time()-began}
    save('verification.json',result);announce('fresh-sparse-exact-verification',**{k:v for k,v in result.items() if k not in ('new_rows','column_changes_by_kind')})


def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('materialize','audit','build','solve','reconstruct','verify','all'));mode=parser.parse_args().mode
    actions={'materialize':materialize,'audit':audit,'build':build,'solve':solve,'reconstruct':reconstruct,'verify':verify}
    began=time.time();command=[sys.executable,'-B',str(Path(__file__).resolve()),mode]
    try:
        if mode=='all':
            for action in actions.values(): action()
        else:actions[mode]()
    finally:
        save('execution_'+mode+'.json',{'command':command,'cwd':os.getcwd(),'python':platform.python_version(),'script_sha256':sha(__file__),'elapsed_seconds':time.time()-began})

if __name__=='__main__':main()

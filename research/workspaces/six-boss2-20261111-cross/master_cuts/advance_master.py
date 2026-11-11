#!/usr/bin/env python3
"""Configured finite-master advancement; prior rounds remain byte-for-byte intact.

The configuration names a certified base matrix, its exact point, and frozen
cut packs. Reuses only the already checked numeric/reconstruction engine; the
final verification uses Fraction and the complete saved matrix.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, os, platform, sys, time
import extend_master as engine
from merge_master import HERE, REPO, canonical_sha, sha, desc
CONFIG=None

def config_path(name):
    p=Path(name);p=p if p.is_absolute() else REPO/p
    p=p.resolve();assert p.is_relative_to(REPO)
    return p

def base_path(key):
    p=(HERE/CONFIG[key]).resolve();assert p.is_relative_to(HERE)
    return p

def prepare():
    started=time.time();mp=base_path('base_matrix');pp=base_path('base_point')
    with gzip.open(mp,'rt',encoding='utf-8') as f:base=json.load(f)
    point=json.loads(pp.read_text());psha=sha(pp);x=[F(c['weight']) for c in point['columns']]
    ncols=base['column_count'];base_rows=base['row_count'];assert ncols==len(x)
    assert [desc(c) for c in point['columns']]==base['columns']
    known={r['sparse_sha256'] for r in base['rows']};added=[];inputs=[];duplicates=[]
    for bundle in CONFIG['packs']:
        path=config_path(bundle['path']);raw=path.read_bytes();pack=json.loads(raw);digest=hashlib.sha256(raw).hexdigest()
        if 'sha256' in bundle:assert digest==bundle['sha256']
        bound=pack.get('input_sha256',pack.get('source_sha256',pack.get('point_sha256')));assert bound==psha,(path,bound,psha)
        records=pack[bundle.get('list_key','cuts')]
        inputs.append({'family':bundle['family'],'path':str(path.relative_to(REPO)),'sha256':digest,'input_point_sha256':bound})
        for k,cut in enumerate(records,1):
            if F(cut.get('exact_slack','0'))>=0:continue
            sparse=cut.get('sparse_row',cut.get('row_nonzero'))
            assert sparse is not None and len(sparse)==len({j for j,v in sparse})
            sparse=sorted([[j,str(F(v))] for j,v in sparse if F(v)])
            assert all(isinstance(j,int) and 0<=j<ncols for j,v in sparse)
            fullsha=engine.full_hash(sparse,ncols);assert fullsha==cut['row_sha256']
            value=sum(F(v)*x[j] for j,v in sparse);assert value==F(cut['exact_slack'])<0
            h=canonical_sha(sparse);label=f"{bundle['family']}-{k}"
            if h in known:
                duplicates.append({'label':label,'sparse_sha256':h});continue
            known.add(h)
            metadata={key:v for key,v in cut.items() if key not in ('sparse_row','row_nonzero','visible')}
            added.append({'index':base_rows+len(added),'name':label,'sparse_sha256':h,'full_vector_sha256':fullsha,'nonzero':sparse,'source_pack':str(path.relative_to(REPO)),'source_pack_sha256':digest,'source_parameters':metadata,'at_base_slack':str(value)})
    expected=CONFIG.get('expected_rows');nrows=base_rows+len(added)
    if expected is not None:assert nrows==expected,(nrows,expected,duplicates)
    matrix=dict(base);matrix.update({'scope':CONFIG['scope'],'row_count':nrows,'base_row_count':base_rows,'added_row_count':len(added),'rows':base['rows']+added})
    matrixpath=HERE/(engine.STEM+'_matrix.json.gz')
    with gzip.open(matrixpath,'wt',encoding='utf-8') as f:json.dump(matrix,f,ensure_ascii=False,separators=(',',':'))
    ident={'scope':matrix['scope'],'rows':nrows,'columns':ncols,'base_rows':base_rows,'base_point':CONFIG['base_point'],'base_matrix':CONFIG['base_matrix'],'base_point_sha256':psha,'base_matrix_sha256':sha(mp),'input_packs':inputs,'duplicates_skipped':duplicates,'added_rows':[{'index':r['index'],'name':r['name'],'sparse_sha256':r['sparse_sha256'],'full_vector_sha256':r['full_vector_sha256'],'at_base_slack':r['at_base_slack']} for r in added],'matrix_sha256':sha(matrixpath),'descriptor_sha256':canonical_sha(matrix['columns']),'row_vector_list_sha256':canonical_sha([r['sparse_sha256'] for r in matrix['rows']]),'seconds':time.time()-started}
    engine.write('identity',ident);engine.log('configured-matrix-prepared',rows=nrows,columns=ncols,added_rows=len(added),nonzeros=sum(len(r['nonzero']) for r in matrix['rows']),seconds=time.time()-started)

def verify():
    start=time.time();data,rows,obj,norm=engine.load();point=engine.read('exact');dual=engine.read('dual');identity=engine.read('identity')
    oldpath=base_path('base_point');old=json.loads(oldpath.read_text());assert sha(oldpath)==identity['base_point_sha256']
    assert sha(HERE/(engine.STEM+'_matrix.json.gz'))==identity['matrix_sha256']==dual['matrix_sha256']
    assert sha(HERE/(engine.STEM+'_exact.json'))==dual['point_sha256']
    assert [desc(c) for c in point['columns']]==data['columns']==[desc(c) for c in old['columns']]
    assert canonical_sha(data['columns'])==identity['descriptor_sha256']
    hashes=[]
    for i,r in enumerate(data['rows']):
        assert r['index']==i;h=canonical_sha(r['nonzero']);assert h==r['sparse_sha256'];hashes.append(h)
    assert canonical_sha(hashes)==identity['row_vector_list_sha256']
    x=[F(c['weight']) for c in point['columns']];ox=[F(c['weight']) for c in old['columns']]
    assert min(x)>=0 and sum(a*b for a,b in zip(norm,x))==1
    W=sum(a*b for a,b in zip(obj,x));assert W==F(point['W'])==F(dual['dual_value'])==F(dual['normalization_multiplier'])
    slacks=[sum(v*x[j] for j,v in row.items() if x[j]) for row in rows];assert min(slacks)>=0
    residual=[c-W*n for c,n in zip(obj,norm)];used=set();new_weights=[]
    for record in dual['row_multipliers']:
        i=record['row_index'];v=F(record['weight']);assert 0<=i<len(rows) and v>=0 and i not in used;used.add(i)
        assert record['row_name']==data['rows'][i]['name']
        for j,c in rows[i].items():residual[j]-=v*c
        assert v*slacks[i]==0
        if i>=identity['base_rows']:new_weights.append(record)
    assert min(residual)>=0 and list(map(str,residual))==dual['residuals']
    assert sum(r*v for r,v in zip(residual,x))==0
    newrows=[{'index':i,'name':data['rows'][i]['name'],'base_slack':str(sum(v*ox[j] for j,v in rows[i].items())),'new_slack':str(slacks[i]),'source_parameters':data['rows'][i]['source_parameters']} for i in range(identity['base_rows'],len(rows))]
    report={'status':'passed','scope':data['scope'],'rows':len(rows),'columns':len(x),'base_rows':identity['base_rows'],'base_W':old['W'],'exact_optimum':str(W),'W_change':str(W-F(old['W'])),'strict_half_gap':str(1-2*W),'minimum_primal_slack':str(min(slacks)),'minimum_dual_residual':str(min(residual)),'positive_columns':sum(v>0 for v in x),'positive_dual_multipliers':len(used),'positive_new_row_multipliers':new_weights,'new_rows':newrows,'point_sha256':sha(HERE/(engine.STEM+'_exact.json')),'matrix_sha256':sha(HERE/(engine.STEM+'_matrix.json.gz')),'dual_sha256':sha(HERE/(engine.STEM+'_dual.json')),'seconds':time.time()-start,'math_float_operations':0,'optimizer_calls':0}
    engine.write('verification',report);engine.log('configured-certificate-verified',**{k:v for k,v in report.items() if k not in ('new_rows','positive_new_row_multipliers')})

def main():
    global CONFIG
    parser=argparse.ArgumentParser();parser.add_argument('config');parser.add_argument('mode',choices=('prepare','solve','reconstruct','dual','verify','all'));args=parser.parse_args()
    cp=Path(args.config).resolve();assert cp.is_relative_to(HERE);CONFIG=json.loads(cp.read_text());stem=CONFIG['stem'];assert stem and all(c.isalnum() or c=='_' for c in stem)
    engine.STEM=stem;start=time.time();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat();success=False
    actions={'prepare':prepare,'solve':engine.solve,'reconstruct':engine.reconstruct,'dual':engine.dual,'verify':verify}
    try:
        for mode,action in actions.items():
            if args.mode in (mode,'all'):action()
        success=True
    finally:
        engine.write('execution_'+args.mode,{'command':[sys.executable,'-B',str(Path(__file__).resolve()),str(cp),args.mode],'cwd':os.getcwd(),'started_utc':stamp,'elapsed_seconds':time.time()-start,'success':success,'python':platform.python_version(),'script_sha256':sha(__file__),'engine_sha256':sha(HERE/'extend_master.py'),'linear_helper_sha256':sha(HERE/'merge_master.py'),'config_sha256':sha(cp)})
if __name__=='__main__':main()

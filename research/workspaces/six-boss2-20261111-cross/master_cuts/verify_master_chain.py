#!/usr/bin/env python3
"""Check that the three certified matrices extend precisely the same mother rows."""
from pathlib import Path
import gzip,hashlib,json,os,platform,sys,time
HERE=Path(__file__).resolve().parent
FILES=('master_5716_exact.json.gz','dynamic_5727_matrix.json.gz','dynamic_5744_matrix.json.gz')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):
    with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)

def main():
    start=time.time();previous=None;records=[];all_new=[];old_hashes=None
    for filename in FILES:
        path=HERE/filename;data=read(path)
        if previous is None:
            assert data['row_count']==5716
            old_hashes={r['sparse_sha256'] for r in data['rows'][:5692]}
            all_new.extend(data['rows'][5692:])
            parent_rows=5692
        else:
            parent_rows=previous['row_count']
            assert data['columns']==previous['columns']
            assert data['objective']==previous['objective'] and data['normalization']==previous['normalization']
            assert data['rows'][:parent_rows]==previous['rows']
            all_new.extend(data['rows'][parent_rows:])
        records.append({'file':filename,'sha256':digest(path),'rows':data['row_count'],'columns':data['column_count'],'preserved_parent_rows':parent_rows,'new_rows':data['row_count']-parent_rows})
        previous=data
    assert len(all_new)==52 and len({r['sparse_sha256'] for r in all_new})==52
    assert not {r['sparse_sha256'] for r in all_new}&old_hashes
    output={'status':'passed','scope':'Identity-only chain check, no optimization and no new mathematical validity assumption.','same_4849_column_descriptors':True,'same_objective_and_normalization':True,'all_previous_rows_retained_exactly_in_order':True,'distinct_added_vectors_since_5692':52,'no_added_vector_identical_to_5692_row':True,'matrices':records,'execution':{'command':[sys.executable,'-B',str(Path(__file__).resolve())],'cwd':os.getcwd(),'python':platform.python_version(),'script_sha256':digest(Path(__file__)),'seconds':time.time()-start}}
    (HERE/'master_chain_identity.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(output,ensure_ascii=False))
if __name__=='__main__':main()

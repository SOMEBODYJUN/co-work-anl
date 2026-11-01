"""Build the frozen 5189-row superset once, then exactly verify two vectors.

The first 5180 rows are the --latest matrix by the frozen append order.
This is same-implementation reconstruction, not a second matrix derivation.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,sys,time,hashlib,importlib,ast,platform
HERE=Path(__file__).resolve().parent
BASE='research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5'
def normalized_metadata(c):return json.loads(json.dumps({k:v for k,v in c.items() if k!='weight'}))
def dot(row,positive):return sum((row[j]*w for j,w in positive if row[j]),F())
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: verify_both_points.py /absolute/prepared-runtime')
    runtime=Path(sys.argv[1]);assert runtime.is_absolute() and sys.flags.optimize==0
    script=runtime/BASE/'combined_branch_master.py';source=script.read_text()
    tree=ast.parse(source);node=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='build')
    branches=[ast.get_source_segment(source,x.test) for x in node.body if isinstance(x,ast.If)]
    assert branches==["'--latest' in sys.argv","'--new-local' in sys.argv or '--local-v2' in sys.argv"]
    local=json.loads((runtime/BASE/'joint_local_cuts.json').read_text())
    assert set(local)=={'scope','nested','requery'} and len(local['nested'])==5 and len(local['requery'])==4
    manifest=json.loads((HERE/'source-manifest.json').read_text())
    points={}
    for rec in manifest:
        raw=(HERE/rec['stored_path']).read_bytes()
        assert len(raw)==rec['size'] and hashlib.sha256(raw).hexdigest()==rec['sha256']
        assert (runtime/rec['path']).read_bytes()==raw
        points[Path(rec['path']).name]=json.loads(raw)
    build_start=time.time();sys.argv=[str(script),'--latest','--new-local'];sys.path.insert(0,str(script.parent))
    mod=importlib.import_module('combined_branch_master')
    cols,names,rows,obj,norm=mod.build();build_seconds=time.time()-build_start
    assert len(cols)==len(obj)==len(norm)==1905 and len(rows)==len(names)==5189
    assert all(len(row)==1905 for row in rows)
    assert all(n.startswith('actual4-force-new-reply-local:') for n in names[5180:5185])
    assert all(n.startswith('same-source-reply-requery:') for n in names[5185:])
    assert len(names[5108:5180])==72
    expected=[normalized_metadata(c) for c in cols];summaries={};vectors={}
    for filename,point in points.items():
        saved=point['columns'];ys=[F(c['weight']) for c in saved]
        assert len(saved)==1905 and [normalized_metadata(c) for c in saved]==expected
        assert min(ys)>=0 and sum(y>0 for y in ys)==point['positive_columns']
        kinds=Counter(c['kind'] for c in saved)
        assert kinds=={'K':1,'hist':16,'joint-reply':582,'overlap':1306}
        schemas={'K':('kind','weight'),'hist':('kind','actual_bits','d','hist','weight'),'joint-reply':('kind','hist_column_old','group','state','weight'),'overlap':('kind','hist_column','groups','weight')}
        for c in saved:assert tuple(c)==schemas[c['kind']]
        hids=[j for j,c in enumerate(saved) if c['kind']=='hist']
        assert all(len(saved[h]['hist'])==8 and sum(saved[h]['hist'])==6 and saved[h]['d']==1 for h in hids)
        positive=[(j,y) for j,y in enumerate(ys) if y]
        O=dot(norm,positive);W=dot(obj,positive)
        assert O==F(point['O'])==1 and W==F(point['W']) and O-2*W==F(point['strict_half_gap'])>0
        slacks=[dot(row,positive) for row in rows]
        included=5180 if filename=='combined_branch_latest_exact.json' else 5189
        assert included==point['verified_rows']
        assert min(slacks[:included])==F(point['minimum_slack'])==0
        assert all(s>=0 for s in slacks[:included])
        target='latest' if included==5180 else 'local'
        records=[{'row':j,'name':name,'slack':str(value),'included_in_saved_matrix':j<included} for j,(name,value) in enumerate(zip(names,slacks))]
        (HERE/'replay'/(target+'-all-superset-row-slacks.json')).write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
        summary={'input_filename':filename,'complete_input_header':{k:v for k,v in point.items() if k!='columns'},'all_1905_metadata_and_lengths_match_builder':True,'kind_counts':dict(kinds),'positive_by_kind':dict(Counter(c['kind'] for c,y in zip(saved,ys) if y>0)),'all_weights_nonnegative':True,'positive_columns':len(positive),'O':str(O),'W':str(W),'K':str(ys[0]),'strict_half_gap_O_minus_2W':str(O-2*W),'included_rows':included,'included_minimum_slack':str(min(slacks[:included])),'included_zero_rows':sum(v==0 for v in slacks[:included]),'latest_seventy_two':[records[j] for j in range(5108,5180)],'local_nine':[records[j] for j in range(5180,5189)],'local_nine_negative_count':sum(v<0 for v in slacks[5180:]),'nested_frozen_discovery_slacks_equal_current':[(str(slacks[5180+j])==c['slack']) for j,c in enumerate(local['nested'])]}
        summaries[filename]=summary;vectors[filename]=ys
    a,b=points['combined_branch_latest_exact.json'],points['combined_branch_local_exact.json']
    changes=[{'column':j,'kind':x['kind'],'latest_weight':x['weight'],'local_weight':y['weight']} for j,(x,y) in enumerate(zip(a['columns'],b['columns'])) if F(x['weight'])!=F(y['weight'])]
    comparison={'all_1905_metadata_equal':True,'W_difference_local_minus_latest':str(F(b['W'])-F(a['W'])),'K_equal':a['columns'][0]['weight']==b['columns'][0]['weight'],'hist_masses_equal':all(x['weight']==y['weight'] for x,y in zip(a['columns'],b['columns']) if x['kind']=='hist'),'changed_weight_count':len(changes),'changed_by_kind':dict(Counter(c['kind'] for c in changes)),'changed_columns':changes}
    report={'status':'one frozen build; two exact full included-matrix evaluations passed','builder_call_count':1,'original_CLI_called':False,'optimizer_called':False,'builder_script':str(script),'builder_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'argv_during_build':sys.argv,'python':platform.python_version(),'build_seconds':build_seconds,'total_seconds':time.time()-build_start,'superset_rows':5189,'columns':1905,'prefix_proof':{'build_if_order':branches,'latest_prefix':[0,5180],'new_local_last_nine':[5180,5189],'last_nine_kinds':{'nested':5,'requery':4},'flags_absent':['--local-v2']},'points':summaries,'comparison':comparison,'limits':'Same original coefficient builder only; no independent entire-matrix derivation, optimum, full-domain infeasibility, or SPE.'}
    (HERE/'replay/two-point-full-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('points','comparison')},ensure_ascii=False))
    for filename,s in summaries.items():print(filename,json.dumps({k:v for k,v in s.items() if k not in ('latest_seventy_two','local_nine','complete_input_header')},ensure_ascii=False))
    print(json.dumps({k:v for k,v in comparison.items() if k!='changed_columns'},ensure_ascii=False))
if __name__=='__main__':main()

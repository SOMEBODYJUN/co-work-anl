"""Publication checks only: never import or execute either original audit.

Run with explicit --stage and --repo. Checks original bytes, report identity,
transcription and references; these checks are not a new SPE computation.
"""
from pathlib import Path
from hashlib import sha256
from itertools import product
import argparse
import ast
import json
import re

EVREL='archives/customer-attraction/tools/evidence/source-reset-two-original-audits'
OBJ='archives/customer-attraction/state/程序/完整行接口与双副本可信菜单的原始精确审计--程序.md'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',type=Path,required=True)
    parser.add_argument('--repo',type=Path,required=True)
    args=parser.parse_args()
    stage,repo=args.stage.resolve(),args.repo.resolve()
    evidence=stage/EVREL
    def read(rel):
        return json.loads((evidence/rel).read_text())
    def digest(path):
        return sha256(path.read_bytes()).hexdigest()
    sources=read('source-manifest.json')
    dependencies=read('dependency-manifest.json')
    assert len(sources)==4 and sum(s['size'] for s in sources)==14990
    assert len(dependencies)==1 and dependencies[0]['size']==9623
    checked=[]
    for record in sources+dependencies:
        path=stage/record['preserved_path']
        assert path.stat().st_size==record['size']
        assert digest(path)==record['sha256']
        assert len(record['sources'])==2
        for s in record['sources']:
            assert re.fullmatch('[0-9a-f]{40}',s['commit'])
            assert s['path']==record['path']
        checked.append({'id':record['id'],'path':record['preserved_path'],'size':record['size'],'sha256':record['sha256']})
    by_name={Path(s['path']).name:stage/s['preserved_path'] for s in sources}
    for name in ['interface_audit.py','product_independent_audit.py']:
        ast.parse(by_name[name].read_text())
    interface=json.loads(by_name['interface_audit.json'].read_text())
    prod=json.loads(by_name['product_independent_audit.json'].read_text())
    units=read('semantic-units.json')
    assert set(interface)==set(units['interface_audit.json']['top_level_fields'])
    assert all(set(r)==set(units['interface_audit.json']['audit_record_fields']) for r in interface['audits'])
    assert set(prod)==set(units['product_independent_audit.json']['top_level_fields'])
    assert [r['t'] for r in interface['audits']]==[0,7]
    assert all(len(r['ic'])==6 for r in interface['audits'])
    assert len(prod['component_terminal_BR_rows'])==4
    assert len(prod['product_all_BR_rows'])==prod['product_terminal_BR_rows']==16
    assert prod['product_SPE_filtered_rows']==11

    actual_replay=read('current-replay/execution.json')
    assert len(actual_replay['events'])==2
    for event in actual_replay['events']:
        assert event['exit_code']==0 and event['optimization_disabled']
        assert '-I' in event['argv'] and '-B' in event['argv'] and '-O' not in event['argv']
        name=event['entry']
        assert event['original_script_sha256']==digest(by_name[name+'.py'])
        assert event['full_report_byte_equal_frozen']
        stdout=evidence/('current-replay/'+name+'-stdout.json')
        stderr=evidence/('current-replay/'+name+'-stderr.txt')
        assert digest(stdout)==event['stdout_sha256']
        assert stdout.stat().st_size==event['stdout_bytes']
        assert stderr.stat().st_size==event['stderr_bytes']==0
        full=stdout if event['stdout_is_full_report'] else evidence/'current-replay/product_independent_audit-generated.json'
        assert full.read_bytes()==by_name[name+'.json'].read_bytes()
        assert digest(full)==event['frozen_report_sha256']==event['generated_or_full_stdout_report_sha256']
    summary=read('current-replay/product_independent_audit-stdout.json')
    assert summary=={k:v for k,v in prod.items() if 'rows' not in k}
    assert set(prod)-set(summary)=={'component_terminal_BR_rows','product_terminal_BR_rows','product_SPE_filtered_rows','product_all_BR_rows'}

    cert=json.loads((stage/dependencies[0]['preserved_path']).read_text())
    assert set(cert)=={'instance','policy','forced_BB_path','forced_BB_payoffs'}
    labels=cert['instance']['topics']
    assert labels==[''.join(a) for a in product('ABC',repeat=2)]
    histories=[tuple(r['history']) for r in cert['policy']]
    expected={h for d in range(3) for h in product(labels,repeat=d)}
    assert len(histories)==len(set(histories))==91 and set(histories)==expected
    assert all(r['action'] in labels for r in cert['policy'])
    assert len(cert['instance']['customers'])==10
    assert all(r['multiplicity']==1 for r in cert['instance']['customers'])
    assert prod['certificate_sha256']==digest(stage/dependencies[0]['preserved_path'])
    assert cert['forced_BB_path']==['BB','BC','CA']
    assert cert['forced_BB_payoffs']==['5/2','3','9/2']
    assert prod['full_policy_histories']==91 and prod['full_policy_comparisons']==819
    assert 91*(len(labels)-1)==728
    structure=read('certificate-structure-and-scope.json')
    assert structure['raw_policy_list_records']==structure['unique_ordered_histories']==91

    body=(stage/OBJ).read_text()
    assert body.startswith('---\n') and body.count('\n---\n')==1
    assert '## scalar-interface\n' in body and '## product-credible-menu\n' in body
    fm=body.split('---',2)[1]
    for key in ['id','kind','type_tag','title','status','summary','source_refs']:
        assert re.search(r'^'+key+r':',fm,re.M)
    refs=re.findall(r'source:([0-9a-f]{40}):([^"\n]+)',fm)
    assert len(refs)==10
    for record in sources+dependencies:
        for source in record['sources']:
            assert (source['commit'],source['path']) in refs
    local_component=[]
    local_product=[]
    for line in body.splitlines():
        if not line.startswith('|'):
            continue
        cells=line.strip('|').split('|')
        if len(cells)==5 and cells[0] in 'ABC' and cells[1] in 'ABC':
            local_component.append(dict(zip(['second','last','d','v','last_u'],cells)))
        if len(cells)==6 and cells[0] in labels and cells[1] in labels:
            local_product.append(dict(zip(['second','last','d','v','last_u'],cells[:5])))
            assert cells[5]==('是' if cells[3] in ['3','7/2','4'] else '否')
    assert local_component==prod['component_terminal_BR_rows']
    assert local_product==prod['product_all_BR_rows']
    assert '|mapped_coordinate_coverage|1|2/9|' in body
    assert '|independent_coordinate_LP_min_cost|1|9/2|' in body
    checked_links=[]
    for rel in [OBJ,EVREL+'/README.md']:
        for target in re.findall(r'\]\(([^)]+)\)',(stage/rel).read_text()):
            if '://' in target or target.startswith('#'):
                continue
            relative=Path(rel).parent/target.split('#',1)[0]
            p=stage/relative
            generated_self_report=p.resolve()==(evidence/'publication-check.json').resolve()
            if not p.exists() and not generated_self_report:
                p=repo/relative
            assert p.exists() or generated_self_report,(rel,target)
            checked_links.append({'from':rel,'target':target})
    bindings=read('comparison-bindings.json')['paths']
    for binding in bindings:
        p=repo/binding['path']
        assert p.stat().st_size==binding['size'] and digest(p)==binding['sha256']
    receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-source-reset-four.json').read_text())
    assert {r['id'] for r in receipts}=={s['id'] for s in sources}
    required={'id','full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','disposition','targets'}
    for receipt in receipts:
        assert set(receipt)==required
        assert all(receipt[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all(receipt[k] for k in ['read_note','comparison_note','decision_note'])
        assert receipt['disposition']=='integrated' and receipt['targets']==[OBJ]
    parsed=[]
    for p in sorted(stage.rglob('*.json')):
        if p==evidence/'publication-check.json':
            continue
        json.loads(p.read_text())
        parsed.append(p.relative_to(stage).as_posix())
    result={
      'status':'PASS',
      'scope':'publication/transcription/byte/structure checks only; no original entry or solver executed by this checker',
      'primary_source_count':4,'primary_source_bytes':14990,
      'dependency_source_count':1,'dependency_source_bytes':9623,
      'checked_originals':checked,'original_python_files_ast_parsed':2,
      'prior_actual_original_entry_replays_bound':2,'original_entry_replays_executed_by_this_checker':0,
      'full_report_byte_equal_frozen_count':2,'product_stdout_is_complete_report':False,
      'report_top_level_fields_accounted':{'interface':4,'product':19},
      'interface_records':2,'interface_ic_records':12,'interface_proper_deviations_per_parameter':3,
      'raw_policy_records':91,'raw_policy_duplicates':0,'policy_depth_counts':[1,9,81],
      'product_including_self_comparisons':819,'product_proper_deviations':728,
      'body_component_rows_match_report':4,'body_product_rows_match_report':16,
      'body_product_credible_rows':11,'comparison_paths_sha256_matched':len(bindings),
      'complete_primary_receipts':4,'markdown_links_checked':len(checked_links),
      'parsed_json_paths':parsed,'limitations':'record consistency does not replace full-file reading, mathematical judgment, universal proof or parent publication gate'
    }
    (evidence/'publication-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert (evidence/'publication-check.json').is_file()
    print(json.dumps({k:result[k] for k in ['status','primary_source_count','primary_source_bytes','dependency_source_bytes','prior_actual_original_entry_replays_bound','original_entry_replays_executed_by_this_checker','body_product_rows_match_report','complete_primary_receipts']},ensure_ascii=False))


if __name__=='__main__':
    main()

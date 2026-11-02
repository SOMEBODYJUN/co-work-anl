"""Static publication checks; no original import/search/audit execution."""
from pathlib import Path
from hashlib import sha256
import argparse
import ast
import json
import re

E='archives/customer-attraction/tools/evidence/r879-independent-terminal-reviews-and-residual-probe'
R='archives/customer-attraction/state/审查/双末位银行停界的独立读序与假设边界--审查.md'
P='archives/customer-attraction/state/程序/实际遗漏并集预算的两人浮点回复菜单诊断--程序.md'


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--stage',type=Path,required=True)
    parser.add_argument('--repo',type=Path,required=True)
    parser.add_argument('--sibling-stage',type=Path,required=True)
    args=parser.parse_args()
    stage,repo,sibling=args.stage.resolve(),args.repo.resolve(),args.sibling_stage.resolve()
    ev=stage/E
    def read(p):return json.loads((ev/p).read_text())
    def digest(p):return sha256(p.read_bytes()).hexdigest()
    primary=read('source-manifest.json');related=read('related-source-manifest.json')
    assert len(primary)==4 and sum(s['size'] for s in primary)==9340
    assert len(related)==1 and related[0]['size']==10228
    for s in primary+related:
        p=stage/s['preserved_path']
        assert p.stat().st_size==s['size'] and digest(p)==s['sha256']
        assert len(s['sources'])==2
        assert all(re.fullmatch('[0-9a-f]{40}',x['commit']) and x['path']==s['path'] for x in s['sources'])
    code=next(stage/s['preserved_path'] for s in primary if s['id']=='93ec8bc28a20106a6d35')
    ast.parse(code.read_text())
    units=read('semantic-units.json')
    assert {s['id'] for s in primary}==set(units)-{'related_only'}
    assert all(units[s['id']]['size']==s['size'] and len(units[s['id']]['all_units'])>=6 for s in primary)
    bindings=read('comparison-bindings.json')['files']
    cross_stage={b['path'] for b in bindings if b['publication_state_when_read']=='sibling-staging-awaiting-parent-publication'}
    assert len(cross_stage)==2
    for b in bindings:
        p=Path(b['location_when_read'])/b['path']
        assert p.stat().st_size==b['bytes'] and digest(p)==b['sha256']
    checked_links=[]
    table_rows=0
    for rel in [R,P,E+'/README.md']:
        body=(stage/rel).read_text()
        if rel in [R,P]:
            assert body.startswith('---\n')
            fm=body.split('---',2)[1]
            for key in ['id','kind','type_tag','title','status','summary','source_refs']:
                assert re.search('^'+key+':',fm,re.M)
            refs=re.findall(r'source:([0-9a-f]{40}):([^"\n]+)',fm)
            assert len(refs)==(8 if rel==R else 4)
        current_columns=None
        for line in body.splitlines():
            if line.startswith('|'):
                columns=len(line.split('|'))-2
                if current_columns is None:current_columns=columns
                assert columns==current_columns,(rel,line)
                table_rows+=1
            else:current_columns=None
        for target in re.findall(r'\]\(([^)]+)\)',body):
            if '://' in target or target.startswith('#'):continue
            relative=Path(rel).parent/target.split('#',1)[0]
            p=(stage/relative).resolve()
            pending_self=p.resolve()==(ev/'publication-check.json').resolve()
            if not p.exists() and not pending_self:
                p=(repo/relative).resolve()
            if not p.exists() and not pending_self:
                p=(sibling/relative).resolve()
                assert p.resolve().relative_to(sibling).as_posix() in cross_stage,(rel,target)
            assert p.exists() or pending_self,(rel,target)
            checked_links.append([rel,target])
    mapping=read('old-point-relabeling-and-output-gap.json')
    permutation={int(a):b for a,b in mapping['old_to_new_labels'].items()}
    old_weights={1:4,2:3,4:3,10:2,12:2,18:2,20:2,25:2,32:5,56:2}
    def mask_relabel(mask):return sum(1<<permutation[i] for i in range(6) if mask&(1<<i))
    transformed=sorted([mask_relabel(mask),w] for mask,w in old_weights.items())
    assert transformed==mapping['new_masks_and_unit_multiplicities']
    new_reply=[None]*6
    for i,value in enumerate(mapping['old_reply']):new_reply[permutation[i]]=permutation[value]
    assert new_reply==mapping['new_compatible_reply']==[1,4,4,5,5,4]
    assert sum(w for _,w in transformed)==mapping['unit_clients']==27
    assert mapping['native_output_supplied_in_this_batch'] is False
    scope=read('execution-scope.json')
    assert all(scope[k]==0 for k in ['original_program_execution_count','original_program_import_count','new_LP_or_random_search_count','new_SPE_verification_or_terminal_formula_replay_count'])
    receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-r879-terminal-four.json').read_text())
    required={'id','full_file_reviewed','related_material_checked','unique_content_accounted_for','read_note','comparison_note','decision_note','disposition','targets'}
    assert {r['id'] for r in receipts}=={s['id'] for s in primary}
    for receipt in receipts:
        assert set(receipt)==required and receipt['disposition']=='integrated'
        assert all(receipt[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all(receipt[k] for k in ['read_note','comparison_note','decision_note'])
        assert receipt['targets']==units[receipt['id']]['targets']
        assert all((stage/t).is_file() for t in receipt['targets'])
    parsed=[]
    for p in sorted(stage.rglob('*.json')):
        if p==ev/'publication-check.json':continue
        json.loads(p.read_text());parsed.append(p.relative_to(stage).as_posix())
    result={
      'status':'PASS','scope':'static publication/byte/transcription checks; no original code imported or executed',
      'primary_source_count':4,'primary_source_bytes':9340,'related_source_count':1,'related_source_bytes':10228,
      'original_source_hashes_matched':5,'original_python_AST_only':1,
      'original_program_executions':0,'LP_random_or_SPE_replays':0,
      'semantic_unit_records_complete':4,'formal_objects':2,'formal_comparison_bindings':len(bindings),
      'sibling_referenced_objects_require_parent_publication':sorted(cross_stage),
      'markdown_links_checked':len(checked_links),'markdown_table_rows_checked':table_rows,
      'old_point_relabeling_metadata_consistent':True,'old_point_is_native_output':False,
      'complete_primary_receipts':4,'parsed_json_paths':parsed,
      'limitations':'does not prove new mathematics, recover missing stdout, replace human review or satisfy remote publication gate'
    }
    (ev/'publication-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert (ev/'publication-check.json').is_file()
    print(json.dumps({k:result[k] for k in ['status','primary_source_count','primary_source_bytes','original_program_executions','formal_objects','complete_primary_receipts']},ensure_ascii=False))


if __name__=='__main__':main()

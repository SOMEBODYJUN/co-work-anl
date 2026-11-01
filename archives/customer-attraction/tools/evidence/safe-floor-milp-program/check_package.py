#!/usr/bin/env python3
"""Static provenance/ledger integrity only: never execute or import a mathematical program."""
import ast
from collections import Counter
from fractions import Fraction
import hashlib,json,re
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/非可信保底菜单的混合整数松弛与九客户边界点--程序.md'
IDS=['a5598cc1012110ebe8cf','68f3fa9288cd960ab86f']


def read(p):return json.loads(p.read_text())


def verify(p,item):
 b=p.read_bytes()
 assert len(b)==item.get('bytes',item.get('size')),str(p)
 assert hashlib.sha256(b).hexdigest()==item['sha256'],str(p)


def main():
 own=read(HERE/'artifact-manifest.json')['files']
 for item in own:verify(ROOT/item['path'],item)
 sources=read(HERE/'source-manifest.json')['sources']
 assert sorted(x['id'] for x in sources if x['role']=='primary')==sorted(IDS)
 for item in sources:
  verify(ROOT/item['preserved_path'],item);assert item['full_file_reviewed'] is True
 compared=read(HERE/'comparison-manifest.json')['files']
 for item in compared:verify(ROOT/item['path'],item)
 json_files=sorted(x for x in HERE.rglob('*.json') if x.name!='self-check.json')
 for path in json_files:read(path)
 py_files=sorted(HERE.rglob('*.py'))
 for path in py_files:ast.parse(path.read_text(),filename=str(path))
 body=BODY.read_text();header=body.split('---',2)[1]
 for name in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search(r'^'+name+':',header,re.M),name
 links=[]
 for document in [BODY,HERE/'README.md',HERE/'run-history/README.md']:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',document.read_text()):
   target=target.strip('<>').split('#',1)[0]
   if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
   assert (document.parent/target).resolve().exists(),(str(document),target)
   links.append({'document':str(document.relative_to(ROOT)),'target':target})
 event=read(HERE/'execution.json')
 paths={'executed_script_snapshot':'run-history/audit_point_executed.py','raw_first_report':'run-history/raw-first-report.json','current_script':'audit_point.py','corrected_report':'exact-audit.json','original_input':'original/safe_floor_m3p6.json'}
 for key,name in paths.items():verify(HERE/name,event[key])
 for name,item in event['unchanged_arithmetic_outputs'].items():verify(HERE/name,item)
 assert event['observed_returncode']==0 and event['elapsed_seconds'] is None
 assert event['new_audit_executions']==1 and event['new_original_MILP_runs']==event['extra_math_after_correction']==0
 audit=read(HERE/'exact-audit.json');raw=read(HERE/'run-history/raw-first-report.json')
 old_explanation=raw['objective_upper_bound'];new_explanation=audit['objective_upper_bound']
 original_script=(HERE/'run-history/audit_point_executed.py').read_text();current_script=(HERE/'audit_point.py').read_text()
 assert original_script.count(old_explanation)==1
 assert original_script.replace(old_explanation,new_explanation)==current_script
 raw_compare=dict(raw);raw_compare.pop('objective_upper_bound')
 current_compare=dict(audit);current_compare.pop('objective_upper_bound');current_compare.pop('post_run_explanation_correction')
 assert raw_compare==current_compare
 assert audit['status']=='PASS'
 for key in ['original_imports','original_MILP_runs','solver_calls','canonical_SPE_calls']:assert audit[key]==0
 verify(HERE/'original/safe_floor_m3p6.json',audit['input'])
 assert audit['parameters']=={'topics':6,'players':3,'threshold':'1','mass_cap':18}
 assert audit['matrix']=={'rows':247,'columns':153,'continuous_weights':63,'binary_menu_variables':90,'row_family_counts':{'choose_one':6,'query_upper':90,'follower_lower':150,'mass_cap':1},'nonzero_coefficients':8073}
 ledger=read(HERE/'coefficient-rows.json');rows=ledger['rows']
 assert ledger['shape']==[247,153] and ledger['weight_masks']==list(range(1,64))
 assert len(ledger['menus'])==90 and len(rows)==247
 assert [x['row'] for x in rows]==list(range(247))
 assert Counter(x['kind'] for x in rows)==audit['matrix']['row_family_counts']
 assert sum(len(x['weight_coefficients'])+len(x['binary_coefficients']) for x in rows)==8073
 fraction_count=0
 for row in rows:
  for key in ['weight_coefficients','binary_coefficients']:
   for index,value in row[key]:
    assert str(Fraction(value))==value;fraction_count+=1
  for key in ['lower','upper']:
   value=row[key]
   if value is not None:assert str(Fraction(value))==value;fraction_count+=1
 assert rows[-1]['kind']=='mass_cap' and rows[-1]['upper']=='18'
 integer=audit['integer_repair'];displayed=audit['displayed_candidate']
 assert integer['objective']==integer['mass']=='9' and integer['negative_rows']==[]
 assert integer['minimum_variable_bound_slack']==integer['minimum_row_slack']=='0'
 assert integer['row_values'][-1]=={'row':246,'value':'9','minimum_bound_slack':'9'}
 for result in [integer,displayed]:
  assert result['row_count']==len(result['row_values'])==247
  assert [x['row'] for x in result['row_values']]==list(range(247))
  for row in result['row_values']:
   for key in ['value','minimum_bound_slack']:
    assert str(Fraction(row[key]))==row[key];fraction_count+=1
 assert [x['row'] for x in displayed['negative_rows']]==[45,72,141,207]
 assert [x['meta']['a'] for x in displayed['negative_rows']]==[0,1,3,5]
 assert displayed['minimum_row_slack']=='-1283/30000000000000000'
 assert displayed['reported_value_minus_displayed_objective']=='429/10000000000000000'
 point=read(HERE/'point-and-menus.json');p=point['point']
 assert p==integer['point'] and p['weights']=={'10':'3','20':'3','33':'3'}
 assert p['selected_binary_indices']==[14,24,42,50,69,75]
 assert len(p['integer_unit_customers'])==9
 old=read(HERE/'original/safe_floor_m3p6.json')
 assert p['selected_menus']==old['witness']
 assert len(point['menus'])==6 and [x['a'] for x in point['menus']]==list(range(6))
 for row in point['menus']:
  assert row['unit_role_payoffs']==['1','1','1'] and row['deviation_payoff']=='3' and row['strict_gain']=='2'
 assert len(point['support_coverage'])==audit['coverage']['supports_enumerated']==42
 assert len(audit['coverage']['optimal_supports'])==8 and audit['coverage']['OPT_3']==9
 assert audit['protected_floor_warning']=={'query_payoff':'1','follower_payoffs':['1','1'],'query_strictly_below_normalized_floor':False,'OPT_over_2m':'3/2','followers_meet_OPT_over_2m':False}
 scope=read(HERE/'execution-scope.json')
 assert scope['new_original_MILP_runs']==scope['new_canonical_DP_or_SPE_runs']==0
 assert scope['new_independent_definition_audit_runs']==1 and scope['constraint_rows']==247
 targets=0
 for source_id in IDS:
  receipt=read(ROOT/f'cleanup/workspaces/Boss7/receipts-round19/{source_id}.json')
  assert receipt['id']==source_id and receipt['disposition']=='integrated'
  for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert receipt[key] is True
  for target in receipt['targets']:assert (ROOT/target).exists(),target
  targets+=len(receipt['targets'])
 result={'status':'PASS','scope':'Static fingerprints, saved coefficient/value schemas, source syntax, exact prose-only correction, receipt and links. No original MILP, independent audit rerun, payoff or SPE computation.',
         'own_fingerprints':len(own),'source_bindings':len(sources),'comparison_bindings':len(compared),'JSON_files':len(json_files),'Python_AST_files':len(py_files),
         'local_links':len(links),'receipt_count':2,'receipt_targets_with_duplicates':targets,'coefficient_rows':247,'columns':153,'nonzero_coefficients':8073,
         'saved_point_evaluations':2,'saved_row_values':494,'canonical_fraction_strings':fraction_count,
         'arithmetic_before_after_identical':True,'executed_script_change_only_explanation':True,
         'new_mathematical_runs':0,'links':links}
 (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False))


if __name__=='__main__':main()

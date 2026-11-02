#!/usr/bin/env python3
"""Static bytes/report/links QA; never executes original or fixed scientific checks."""
from pathlib import Path
from fractions import Fraction as F
import argparse,ast,hashlib,json,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaves(o,path=''):
 if isinstance(o,dict):return [z for k,v in o.items() for z in leaves(v,path+'/'+k)]
 if isinstance(o,list):return [z for k,v in enumerate(o) for z in leaves(v,path+'/'+str(k))]
 return [{'pointer':path,'value':o}]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();stage=a.stage.resolve();repo=a.repo.resolve();ev=stage/'archives/customer-attraction/tools/evidence/r92-relay-stationary'
 sources=json.loads((ev/'source-manifest.json').read_text())['primary_sources'];assert len(sources)==9 and sum(s['size'] for s in sources)==25777
 byid={s['id']:s for s in sources}
 for s in sources:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and sha(p)==s['sha256']
 rel=json.loads((ev/'related-source-manifest.json').read_text())['sources'];assert len(rel)==2
 for s in rel:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and sha(p)==s['sha256']
 ledger=json.loads((ev/'lossless-report-reading.json').read_text());all_leaves=[]
 for i in ['03af380226e5ba437d88','a6e6412f08cd56667290','80fd349243c9ff02560d']:
  obj=json.loads((stage/byid[i]['preserved_path']).read_text());assert ledger['reports'][i]==obj
  rawleaves=leaves(obj,'/'+i);assert len(rawleaves)==ledger['primitive_leaf_counts'][i];all_leaves+=rawleaves
 assert all_leaves==ledger['all_primitive_leaves'] and len(all_leaves)==109
 author=ledger['reports']['a6e6412f08cd56667290'];assert set(author)=={'status','grid_cases','samples'};assert author['grid_cases']==59*6==354 and len(author['samples'])==15
 for r in author['samples']:
  n=r['r']-1;aa=r['a'];t=r['t'];b=r['b'];assert F(r['loss'])==F(aa*t*(r['r']-aa-t),n*(aa+t)*(b+r['r']-aa)*(b+t))
 parent=ledger['reports']['80fd349243c9ff02560d'];assert parent['seed']==9221
 assert parent['checks']=={'pair_checks':4*sum(n*n for n in range(1,41)),'mixture_checks':40*4*5,'partial_checks':40*4*5,'derivative_checks':4*sum(n*(n-1)//2 for n in range(1,41)),'sharp_multiplicative':40*4}
 point=ledger['reports']['03af380226e5ba437d88'];assert point['weights']=={'3':1,'12':1} and len(point['terminal_actions'])==16
 assert F(str(point['objective']))==F(str(point['fixed_selector_objective']))==F(-1,8) and F(point['stationary_defect'])==F(-1,4)
 fixed=json.loads((ev/'fixed-audit-stdout.json').read_text());event=json.loads((ev/'fixed-audit-execution.json').read_text())
 assert event['exit_code']==0 and event['new_fixed_stdlib_audit_invocations']==1 and event['original_program_invocations']==0
 assert sha(ev/'fixed-audit-stdout.json')==event['stdout_sha256'] and sha(ev/'fixed-audit-stderr.txt')==event['stderr_sha256']
 assert sha(ev/'audit-fixed-two-client-menu.py')==event['audit_code_sha256']
 assert fixed['point_sha256']==byid['03af380226e5ba437d88']['sha256'] and fixed['author_code_sha256']==byid['934d46caba106707f803']['sha256']
 assert fixed['full_ordered_decision_histories']==21 and len(fixed['full_strategy_and_IC_rows'])==21
 assert fixed['comparisons_including_self']==84 and fixed['proper_comparisons']==63 and fixed['proper_strict']==21 and fixed['proper_ties']==42
 bridge=json.loads((ev/'static-value-identification.json').read_text());assert bridge['fixed_stdout_sha256']==event['stdout_sha256'];assert bridge['mixed_static_safety_value_v3']=='1/2' and bridge['pure_threshold_theta3']=='1/2'
 assert min(F(r['uniform_query_expectation']) for r in bridge['all_profile_expectations'])==F(1,2)
 assert bridge['all_pure_query_values_against_upper_certificate']==['1/2']*4
 comparison=json.loads((ev/'comparison-bindings-preprimary.json').read_text())['files'];assert len(comparison)==6
 for c in comparison:
  p=repo/c['path'];assert p.stat().st_size==c['bytes'] and sha(p)==c['sha256']
 receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-r92-relay-stationary-nine.json').read_text());assert {r['id'] for r in receipts}==set(byid)
 for r in receipts:
  for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert r[k] is True
  for k in ['read_note','comparison_note','decision_note','disposition','targets']:assert r[k]
  assert all((stage/t).is_file() for t in r['targets'])
 formal=[];ids=[];links=0
 for p in (stage/'archives/customer-attraction/state').rglob('*.md'):
  s=p.read_text();assert s.startswith('---\n');front=s.split('---',2)[1]
  for k in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+k+':',front,re.M)
  ids.append(re.search(r'^id:\s*"?(.*?)"?$',front,re.M).group(1));formal.append(str(p.relative_to(stage)))
  for c in re.findall(r'source:([a-f0-9]+):',front):assert len(c)==40
  for target in re.findall(r'\]\(([^)]+)\)',s):
   if re.match('[a-zA-Z]+:',target) or target.startswith('#'):continue
   q=(p.parent/target.split('#')[0]).resolve()
   if not q.exists():assert (repo/q.relative_to(stage)).exists(),str(q)
   links+=1
 assert len(formal)==3 and len(set(ids))==3
 for target in re.findall(r'\]\(([^)]+)\)',(ev/'README.md').read_text()):
  assert (ev/target).resolve().exists();links+=1
 out={'status':'passed','scope':'Static publication QA; no original program or fixed audit rerun. Only saved report arithmetic, bytes, AST-independent metadata, references and receipt completeness checked.','primary_sources':9,'primary_bytes':25777,'related_only_sources':2,'report_primitive_leaves':109,'author_parameter_grids':354,'parent_parameter_grids':160,'related_sibling_parameter_grids':377,'new_fixed_full_strategy_audit_runs':1,'new_original_entrypoint_runs':0,'fixed_IC_including_self':84,'fixed_proper_IC':63,'fixed_strict_proper':21,'fixed_tied_proper':42,'normalized_defect':'-1/8','integer_defect':'-1/4','pure_theta3_and_mixed_v3_equal_only_for_this_input':'1/2','formal_objects':sorted(formal),'comparison_bindings':6,'relative_links_checked':links,'complete_primary_receipts':9,'boundary_corrections':'General background actual remaining P differs from full coverage W; true mixed v distinguished from pure minmax theta. Once-run fixed raw output kept immutable and mixed identity supplemented analytically.'}
 a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()

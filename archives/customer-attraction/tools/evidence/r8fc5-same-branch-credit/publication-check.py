#!/usr/bin/env python3
"""Publication-only QA; do not import or execute the preserved original audit."""
from pathlib import Path
from fractions import Fraction as F
import argparse,ast,json,hashlib,re

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaves(o,path=''):
 if isinstance(o,dict):
  return [z for k,v in o.items() for z in leaves(v,path+'/'+k.replace('~','~0').replace('/','~1'))]
 if isinstance(o,list):return [z for k,v in enumerate(o) for z in leaves(v,path+'/'+str(k))]
 return [{'pointer':path,'value':o}]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 stage=a.stage.resolve();repo=a.repo.resolve();ev=stage/'archives/customer-attraction/tools/evidence/r8fc5-same-branch-credit'
 manifest=json.loads((ev/'source-manifest.json').read_text());sources=manifest['primary_sources'];assert len(sources)==5
 for s in sources:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and digest(p)==s['sha256']
 assert sum(s['size'] for s in sources)==52937
 byid={s['id']:s for s in sources};load=lambda i:json.loads((stage/byid[i]['preserved_path']).read_text())
 v1=load('eb7b67a32f8920ff75b0');v2=load('5a7bfb138c0bec9bc8ca')
 assert {k:v for k,v in v2.items() if k!='true_spe_full_depth_reentry'}==v1
 assert list(v1)==['status','scope','scalar','games','totals','unproved']
 assert v1['status']=='all_exact_checks_passed';assert len(v1['games'])==21
 expected=[]
 for i,o in [('eb7b67a32f8920ff75b0',v1),('5a7bfb138c0bec9bc8ca',v2)]:expected+=leaves(o,'/'+i)
 ledger=json.loads((ev/'lossless-report-reading.json').read_text());assert ledger['all_primitive_leaves']==expected
 assert ledger['primitive_leaf_counts']=={'eb7b67a32f8920ff75b0':350,'5a7bfb138c0bec9bc8ca':670}
 counts_rows=sum(17-d for c in range(1,14) for p in range(c+1) for aa in (0,1) for d in range(p+aa,17))
 counts_params=sum(1 for c in range(1,14) for p in range(c+1) for aa in (0,1) for d in range(p+aa,17))
 assert counts_rows==v1['scalar']['scalar_rows']==17771
 assert counts_params==v1['scalar']['fixed_parameter_envelopes']==2522
 assert v1['scalar']['sharp_d_values']==list(range(1,31))
 assert v1['scalar']['predelete_double_count']=={'old_pre':'4/5','root_gain':'3/10','old_refund':'3/10','old_post':'1/2','naive_total':'11/10','corrected_total':'4/5'}
 fields={'players','topics','unit_customers','decision_histories','true_deviation_comparisons','actual','welfare','real_branches','deletion_masks','customer_credit_checks','normalized_mixture_credit','normalized_mixture_cap'}
 for g in v1['games']:
  assert set(g)==fields
  m=g['players'];k=g['topics'];w=g['welfare'];hist=sum(k**j for j in range(m))
  assert g['decision_histories']==hist and g['true_deviation_comparisons']==k*hist
  assert len(g['actual'])==m and all(0<=x<k for x in g['actual'])
  assert 0<=w<=g['unit_customers']
  assert g['real_branches']==m*k and g['deletion_masks']==k*(2**m-1)
  assert g['customer_credit_checks']==w*g['deletion_masks']
  assert F(g['normalized_mixture_cap'])==F(m-1,m)*w
  assert 0<=F(g['normalized_mixture_credit'])<=F(g['normalized_mixture_cap'])
 for k,v in v1['totals'].items():assert sum(g[k] for g in v1['games'])==v
 assert v1['totals']=={'decision_histories':1231,'true_deviation_comparisons':4495,'real_branches':221,'deletion_masks':873,'customer_credit_checks':5830}
 assert sum(g['players'] for g in v1['games'])==73
 extra=v2['true_spe_full_depth_reentry'];assert len(extra)==64
 previous=F(0)
 for m,r in enumerate(extra,1):
  assert set(r)=={'players','true_decision_histories','true_deviation_comparisons','full_depth_credit','actual_welfare'}
  assert r['players']==r['true_decision_histories']==r['true_deviation_comparisons']==m
  assert r['actual_welfare']==1
  current=F(r['full_depth_credit'])
  assert current==previous+(F(1,m) if m>1 else 0)
  previous=current
 assert sum(r['true_decision_histories'] for r in extra)==2080
 assert extra[3]['full_depth_credit']=='13/12' and extra[5]['full_depth_credit']=='29/20'
 script=stage/byid['2f02cd9c62b5de3da049']['preserved_path'];tree=ast.parse(script.read_text())
 assert [n.name for n in tree.body if isinstance(n,ast.FunctionDef)]==['credit','envelope','scalar_audit','payoffs','build_spe','game_audit','reentry_audit','main']
 bindings=json.loads((ev/'comparison-bindings.json').read_text())['files']
 for b in bindings:
  p=repo/b['path'];assert p.stat().st_size==b['bytes'] and digest(p)==b['sha256']
 receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-r8fc5-global-credit-five.json').read_text());assert {r['id'] for r in receipts}==set(byid)
 for r in receipts:
  for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert r[key] is True
  for key in ['read_note','comparison_note','decision_note','disposition','targets']:assert r[key]
  assert all((stage/p).is_file() for p in r['targets'])
 formal=[];links=0;objectids=[]
 for p in (stage/'archives/customer-attraction/state').rglob('*.md'):
  text=p.read_text();assert text.startswith('---\n');front=text.split('---',2)[1]
  for key in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search(r'^'+key+':',front,re.M)
  objectids.append(re.search(r'^id:\s*"?(.*?)"?$',front,re.M).group(1))
  for ref in re.findall(r'source:([a-f0-9]+):([^"\n]+)',front):assert len(ref[0])==40
  formal.append(str(p.relative_to(stage)))
 for p in list((stage/'archives/customer-attraction/state').rglob('*.md'))+[ev/'README.md']:
  for match in re.finditer(r'\]\(([^)]+)\)',p.read_text()):
   url=match.group(1)
   if re.match(r'[a-zA-Z]+:',url) or url.startswith('#'):continue
   target=(p.parent/url.split('#')[0]).resolve()
   if target.exists():pass
   else:
    rel=target.relative_to(stage);assert (repo/rel).exists(),str(rel)
   links+=1
 assert len(formal)==3 and len(set(objectids))==3
 out={'status':'passed','scope':'Static publication/report-arithmetic QA only; original audit functions not imported or called. Recorded harmonic fractions checked by adjacent-row arithmetic, no new equilibrium or credit generation.','primary_sources':5,'primary_bytes':52937,'original_entrypoint_invocations':0,'new_full_SPE_runs':0,'new_scalar_credit_enumerations':0,'v1_v2_common_equal':True,'report_primitive_leaves':1020,'common_game_rows':21,'added_reentry_rows':64,'common_report_totals':v1['totals'],'proper_common_comparisons':3264,'reentry_histories_and_self_comparisons_each':2080,'reentry_proper_comparisons':0,'comparison_files_hashed':len(bindings),'complete_receipts':5,'formal_objects':sorted(formal),'relative_links_checked':links}
 a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()

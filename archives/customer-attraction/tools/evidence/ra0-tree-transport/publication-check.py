#!/usr/bin/env python3
"""Static publication/profile QA only; do not run any scientific entrypoint."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import argparse,json,hashlib,re,ast

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def leaves(o,path=''):
 if isinstance(o,dict):return [z for k,v in o.items() for z in leaves(v,path+'/'+k)]
 if isinstance(o,list):return [z for k,v in enumerate(o) for z in leaves(v,path+'/'+str(k))]
 return [{'pointer':path,'value':o}]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--stage',type=Path,required=True);ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();stage=a.stage.resolve();repo=a.repo.resolve();ev=stage/'archives/customer-attraction/tools/evidence/ra0-tree-transport'
 ss=json.loads((ev/'source-manifest.json').read_text())['primary_sources'];assert len(ss)==8 and sum(s['size'] for s in ss)==401887;byid={s['id']:s for s in ss}
 for s in ss:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and sha(p)==s['sha256']
  if p.suffix=='.py':ast.parse(p.read_text())
 reading=json.loads((ev/'lossless-report-reading.json').read_text());reports={};allleaves=[]
 for s in ss:
  if s['path'].endswith('.json'):
   o=json.loads((stage/s['preserved_path']).read_text());reports[s['id']]=o;assert reading['reports'][s['id']]==o;rows=leaves(o,'/'+s['id']);assert len(rows)==reading['primitive_leaf_counts'][s['id']];allleaves+=rows
 assert allleaves==reading['all_primitive_leaves'] and len(allleaves)==14892
 audit=reports['2585b5062b6d7463d1c1'];assert audit['arbitrary_background_scalar_checks']==6*sum(B*3**B for B in range(1,7))==36090
 assert len(audit['full_tree_audits'])==4 and sum(r['ordered_nodes'] for r in audit['full_tree_audits'])==634 and sum(r['kept_comparisons'] for r in audit['full_tree_audits'])==4326
 for r in audit['family_summaries']:
  assert sum(r['reward_sizes'])==r['W'] and r['OPT']==r['m']*r['L'];assert F(r['OPT_over_W'])==F(r['OPT'],r['W']);assert r['OPT_minus_2W']==r['OPT']-2*r['W']
 bench=reports['fa1e2c80c225c0c6cae4'];assert bench['players']==5 and bench['topics']==7 and bench['rounds']==31 and bench['J']==list(range(5))
 assert [r['step'] for r in bench['best']]==[0,22,30]
 first=bench['best'][0];assert first['exact'] is True;mapping={tuple(r['h']):r['a'] for r in first['actions']};assert len(mapping)==len(first['actions'])==2801
 assert set(mapping)=={h for d in range(5) for h in product(range(7),repeat=d)};assert mapping[(0,0,0,0)]==6 and mapping[(0,3,0)]==5
 for r in bench['best'][1:]:assert r['exact'] is False and not({'actions','masses','audit'}&set(r));F(r['value'])
 random=reports['6a55381be7189d1e9de8'];assert len(random['reports'])==1
 rr=random['reports'][0];rmap={tuple(r['history']):r['action'] for r in rr['actions']};assert len(rmap)==len(rr['actions'])==259 and set(rmap)=={h for d in range(4) for h in product(range(6),repeat=d)}
 assert all(r['value']=='1/4' and r['exact'] and 'weights' not in r for r in rr['reports'])
 weak=reports['fdcd3b8ed4ff19ffa7b9'];assert len(weak)==3 and all(r['reports']==weak[0]['reports'] and r['pi']==weak[0]['pi'] for r in weak)
 assert len(weak[0]['reports'])==6 and all(r['exact'] and 'weights' not in r for r in weak[0]['reports'])
 consumed=json.loads((ev/'consumed-policy-inputs.json').read_text());maps=[]
 for s in consumed['inputs']:
  p=stage/s['preserved_path'];assert p.stat().st_size==s['size'] and sha(p)==s['sha256'];o=json.loads(p.read_text());maps.append({tuple(r['history']):r['action'] for r in o['strategy']['actions']})
 assert len(maps)==3 and maps[0]==maps[1]==maps[2] and len(maps[0])==43
 for d in json.loads((ev/'dependency-reuse-manifest.json').read_text())['runtime_sources']:
  p=repo/d['reused_repo_path'];assert p.stat().st_size==d['size'] and sha(p)==d['sha256']
 for c in json.loads((ev/'comparison-bindings-preprimary.json').read_text())['files']:
  p=repo/c['path'];assert p.stat().st_size==c['bytes'] and sha(p)==c['sha256']
 event=json.loads((ev/'fixed-seven-client-execution.json').read_text());fixed=json.loads((ev/'fixed-seven-client-audit.json').read_text());assert event['exit_code']==0 and event['new_fixed_stdlib_audit_invocations']==1 and event['original_entrypoint_invocations']==0
 assert sha(ev/'audit-fixed-seven-client-restriction.py')==event['audit_source_sha256'];assert sha(ev/'fixed-seven-client-audit.json')==event['stdout_sha256'];assert sha(ev/'fixed-seven-client-stderr.txt')==event['stderr_sha256'];assert sha(ev/'fixed-seven-client-all-history-profiles.jsonl')==event['profiles_sha256']==fixed['profiles_sha256']
 profiles=[json.loads(line) for line in (ev/'fixed-seven-client-all-history-profiles.jsonl').read_text().splitlines()];assert len(profiles)==2801
 kept_self=kept_proper=neg=0;negby=[0]*7
 for r in profiles:
  h=tuple(r['history']);chosen=r['action'];assert chosen==mapping[h] and len(r['all_IC_slacks_integer'])==7
  for t,v in enumerate(r['all_IC_slacks_integer']):
   gap=F(v)
   if t<5:
    assert gap>=0;kept_self+=t==chosen;kept_proper+=t!=chosen
   if gap<0:neg+=1;negby[t]+=1
 assert kept_self==2050 and kept_proper==11955 and neg==2089 and negby==[0]*6+[2089]
 assert fixed['full_catalog_comparisons_including_self']==19607 and fixed['full_catalog_proper']==16806 and fixed['is_full_pure_SPE'] is False
 receipts=json.loads((stage/'cleanup/workspaces/Boss2/receipts-ra0-tree-transport-eight.json').read_text());assert {r['id'] for r in receipts}==set(byid)
 for r in receipts:
  for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert r[k] is True
  for k in ['read_note','comparison_note','decision_note','disposition','targets']:assert r[k]
  assert all((stage/t).is_file() for t in r['targets'])
 formal=[];ids=[];links=0
 for p in (stage/'archives/customer-attraction/state').rglob('*.md'):
  s=p.read_text();assert s.startswith('---\n');front=s.split('---',2)[1]
  for k in ['id','kind','type_tag','title','status','summary','source_refs']:assert re.search('^'+k+':',front,re.M)
  ids.append(re.search(r'^id:\s*"?(.*?)"?$',front,re.M).group(1));formal.append(str(p.relative_to(stage)))
  for commit in re.findall(r'source:([a-f0-9]+):',front):assert len(commit)==40
  for target in re.findall(r'\]\(([^)]+)\)',s):
   if re.match('[a-zA-Z]+:',target) or target.startswith('#'):continue
   q=(p.parent/target.split('#')[0]).resolve()
   if not q.exists():assert (repo/q.relative_to(stage)).exists(),str(q)
   links+=1
 assert len(formal)==len(set(ids))==3
 for target in re.findall(r'\]\(([^)]+)\)',(ev/'README.md').read_text()):assert (ev/target).resolve().exists();links+=1
 out={'status':'passed','scope':'Static bytes/wholeJSON/actions/recorded-profile arithmetic/old-dependency/links/receipts QA; no original or fixed scientific program rerun.','primary_count':8,'primary_bytes':401887,'original_JSON_count':4,'primitive_leaves':14892,'full_action_rows':3060,'related_policy_inputs':3,'unique_related_policy_rows':43,'benchmark_exact_records':1,'benchmark_false_records_without_complete_points':2,'native_fixed_weak_query_problems':6,'native_weak_record_occurrences':18,'new_fixed_stdlib_runs':1,'new_original_entrypoint_runs':0,'fixed_all_comparisons':19607,'fixed_proper':16806,'fixed_kept_J_self':2050,'fixed_kept_J_proper':11955,'fixed_omitted_profitable_only_label6':2089,'full_SPE_of_seven_client_point':False,'complete_primary_receipts':8,'formal_objects':sorted(formal),'links_checked':links}
 a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False))
if __name__=='__main__':main()

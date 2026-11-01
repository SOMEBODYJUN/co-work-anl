from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib,ast,re,itertools
S=Path(__file__).resolve().parent;B=S.parent;R=B/'co-work-anl-boss3';D=B/'independent_ranks_deliverables'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ss=json.loads((S/'source-manifest.json').read_text())
for x in ss:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for x in json.loads((S/'related-manifest.json').read_text()):
 p=S/x['saved_path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
for name in ['check_fixed_rank','check_rank_one','check_repeated_last']:
 event=json.loads((S/'replay'/name/'execution-record.json').read_text());raw=(S/'replay'/name/'stdout.txt').read_text();out=json.loads(raw)
 assert out==json.loads((S/'replay'/name/'parsed-output.json').read_text())
 assert event['exit_code']==0 and event['stderr_bytes']==0 and event['assertions_enabled'] and event['original_entry_calls']==1 and event['LP_calls']==0
 assert event['source_sha256']==sha(S/'original'/(name+'.py')) and (S/'replay'/name/'stderr.txt').read_text()==''
fixed=json.loads((S/'replay/check_fixed_rank/parsed-output.json').read_text());assert fixed['integer_lemma_cases']==180000
assert [(x['m'],x['cutoff'])for x in fixed['audits']]==[(9,1),(9,2),(5,3),(5,0)]
for x in fixed['audits']:
 m=x['m'];k=x['cutoff'];ranks=[(2*m-1)**j*comb(m,j+1)for j in range(min(k,m-1)+1)]
 assert ranks==x['by_rank'] and sum(ranks)==x['histories'] and x['rows']==2*m*x['histories'] and F(x['ratio'])==F(x['OPT'],x['W']) and F(x['minimum_slack'])==0
assert sum(x['histories']for x in fixed['audits'])==30073 and sum(x['rows']for x in fixed['audits'])==504874
one=json.loads((S/'replay/check_rank_one/parsed-output.json').read_text());assert one['retained_histories']==621 and one['all_action_rows']==11178 and one['genuine_alternative_rows']==10557
assert F(one['rank2_prescribed_payoff'])-F(one['rank2_deviating_payoff'])==F(one['rank2_row'])==F(-15,14)
repeat=json.loads((S/'replay/check_repeated_last/parsed-output.json').read_text());assert repeat['pointwise_cases']==sum((2*m+1)*(m+1)for m in range(1,101))==691950 and sum(range(1,101))==5050
u=json.loads((S/'uniform-input-schema-and-identity.json').read_text());assert len(u['inputs'])==4 and u['first_two_same_complete_action_map']and u['distinct_action_maps']==3
maps=[]
for x in u['inputs']:
 p=S/x['saved_path'];assert p.stat().st_size==x['size']and sha(p)==x['sha256']
 v=json.loads(p.read_text());actions={tuple(z['history']):z['action']for z in v['strategy']['actions']};k=x['k_from_all_actions_and_histories'];m=x['m_from_history_depth']
 assert set(actions)=={h for depth in range(m)for h in itertools.product(range(k),repeat=depth)}
 assert len(actions)==x['complete_ordered_histories'] and len(actions)*(k-1)==x['nonself_raw_IC_rows'];maps.append(actions)
assert maps[0]==maps[1]
finals=[(D/'uniform-program.md',Path('archives/customer-attraction/state/程序/均匀强组合攻击的输入与整数验收边界--程序.md')),(D/'independent-audits.md',Path('archives/customer-attraction/state/计算/固定离轨次数与重复末覆盖的独立原审计--计算.md'))]
ep=R/'archives/customer-attraction/tools/evidence/independent-ranks-four-boss3';links=0
for src,fr in finals:
 body=src.read_text();assert all(line.count('$')%2==0 for line in body.splitlines())and body.count('\\[')==body.count('\\]')
 for match in re.finditer(r'\]\(([^)]+)\)',body):
  href=match.group(1)
  if '://'in href or href.startswith('#'):continue
  p=(R/fr.parent/href.split('#')[0]).resolve()
  if p.is_relative_to(ep):p=S/p.relative_to(ep)
  elif p==R/finals[0][1]:p=finals[0][0]
  elif p==R/finals[1][1]:p=finals[1][0]
  assert p.exists(),str(p);links+=1
 for ref in re.findall(r'source:([^:]+):',body):assert ref=='68fad804ec5946cb296f77dc5b336308a66abf12',ref
receipts=json.loads((D/'receipts-20261101-independent-ranks-four.json').read_text());assert {x['id']for x in receipts}=={x['id']for x in ss}and all(x['disposition']=='integrated'for x in receipts)
assert not any(S.rglob('__pycache__'))
result={'status':'all staged hashes/all finite output fields/counts/input action schemas/receipt targets/links passed','primary_sources':4,'new_original_standard_library_entries':3,'new_uniform_entries':0,'new_uniform_imports':0,'new_LP_calls':0,'canonical_imports_in_three_originals':0,'fixed_rank_nodes':30073,'fixed_rank_including_self_rows':504874,'integer_parameter_cases':180000,'rank_one_nodes_also_in_fixed_rank':621,'rank_one_omitted_negative_slack':'-15/14','repeated_pointwise_cases':691950,'repeated_m_k_pairs':5050,'uniform_original_strategy_sources':4,'uniform_distinct_action_maps':3,'uniform_old_numerical_runs_not_replayed':True,'formal_links_checked':links,'math_delimiters_balanced':True,'all_stage_only':True}
(S/'package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))

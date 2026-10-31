from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
from collections import Counter
import json,hashlib,sys,time
c=Path(__file__).resolve().parent;b=c/'root-js-original-source';out=c/'root-js-report-field-check-001';assert not out.exists();out.mkdir();start=time.monotonic()
selection=b/'97048eafe4cc7c492a5d/residual_deficit_selection_probe.json';x=json.loads(selection.read_text());assert len(x['records'])==119
rows=[]
for index,r in enumerate(x['records']):
 m=len(r['last_path']);k=len(r['worst_counts'][0]);assert m>=2 and len(r['pair_path'])==m
 counts={tuple(v)for v in r['worst_counts']};assert len(counts)==len(r['worst_counts'])
 assert all(len(v)==k and sum(v)==m and all(isinstance(z,int)and z>=0 for z in v)for v in counts)
 for p in [r['last_path'],r['pair_path']]:assert all(0<=a<k for a in p)and tuple(p.count(a)for a in range(k))in counts
 last=F(r['last_best_cost']);pair=F(r['pair_best_cost']);ls=F(r['last_slack']);ps=F(r['pair_slack'])
 assert F(r['welfare'])-last==ls and F(r['welfare'])-pair==ps and pair<=last and ps>=ls
 assert 0<=r['welfare']<=r['opt']and r['worst_paths']>=len(counts)>0
 rows.append({'index':index,'name':r['name'],'players':m,'topics':k,'count_vectors':len(counts),'last_slack':str(ls),'pair_slack':str(ps),'reported_last_and_pair_best_cost_equal':last==pair})
k4p=b/'63a544cd810b3805e02e/residual_deficit_padding_k4.json';z=json.loads(k4p.read_text());inst=z['instance'];m=inst['players'];k=len(inst['topics']);types=inst['customers'];assert(m,k,sum(v['multiplicity']for v in types))==(7,10,764)
def welfare(counts):return sum(v['multiplicity']for v in types if any(counts[a]for a in v['topics']))
def utility(path):
 counts=Counter(path)
 return [sum((F(v['multiplicity'],sum(counts[a]for a in v['topics']))for v in types if t in v['topics']),F(0))for t in path]
support_checks=0;opt=0
for s in range(min(m,k)+1):
 for support in combinations(range(k),s):support_checks+=1;opt=max(opt,welfare([int(a in support)for a in range(k)]))
assert opt==z['opt']==764
assert len(z['worst_count_vectors'])==18 and all(sum(q)==m and welfare(q)==z['welfare']==744 for q in z['worst_count_vectors'])
path=z['last_min_path'];u=utility(path);last=(m-1)*u[-1];pen=(m-F(m+1,2*(m-1)))*u[-2];assert last==F(z['last_min_cost'])==720 and min(last,pen)==F(z['pair_min_cost'])==720 and pen==760
strictp=b/'0383e4422eeec5d072fe/residual_deficit_unique_tail_m4.json';strict=json.loads(strictp.read_text());assert strict['parameters']['trials']==500 and len(strict['progress'])==2 and all(r['best_float_gap_per_total_mass']<0 for r in strict['progress'])
report={'status':'exact-report-field-and-k4-input-check-passed','source_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in [selection,k4p,strictp]},'selection_records':119,'selection_known_examples':sum(not r['name'].startswith('random_')for r in rows),'selection_random_named':sum(r['name'].startswith('random_')for r in rows),'selection_player_histogram':dict(Counter(r['players']for r in rows)),'selection_zero_welfare_indices':[i for i,r in enumerate(x['records'])if r['welfare']==0],'selection_all_last_and_pair_slacks_nonnegative':all(F(r['last_slack'])>=0 and F(r['pair_slack'])>=0 for r in rows),'selection_all_best_costs_equal':all(r['reported_last_and_pair_best_cost_equal']for r in rows),'selection_records_checked':rows,'k4':{'providers':m,'topics':k,'clients':764,'coverage_supports_checked':support_checks,'opt':opt,'all18reported_worst_counts_have_coverage':744,'one_reported_path_payoffs':list(map(str,u)),'one_path_last_cost':str(last),'one_path_penultimate_cost':str(pen),'pair_min_from_that_path':str(min(last,pen)),'reported_outcome_count':z['outcome_count'],'reported_all_worst_paths':z['worst_paths']},'strict_report_progress':strict['progress'],'original_CLI_runs':0,'LP_calls':0,'BI_calls':0,'new_full_strategy_checks':0,'new_exact_report_checker_runs':1,'elapsed_seconds':time.monotonic()-start,'limitations':'No original solver reexecution; report shape/arithmetic and explicit k4 coverage/payoffs only. Does not verify reported all-SPE/path completeness, prove negativeLPupperbound, or certify500strictsuccessfulLPs.'}
(out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(out/'run-metadata.json').write_text(json.dumps({'command':[sys.executable,str(Path(__file__).resolve())],'cwd':str(Path.cwd()),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exit_code':0,'new_checker_runs':1,'original_CLI_runs':0},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items()if k not in ['selection_records_checked','strict_report_progress','source_hashes']},ensure_ascii=False),flush=True)

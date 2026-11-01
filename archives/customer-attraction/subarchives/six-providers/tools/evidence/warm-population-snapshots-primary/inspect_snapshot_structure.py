"""Static source extraction, lossless action decoding, and coverage arithmetic.
No original program import, solver/LP/MIP, SPE enumeration, or IC replay.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import json,hashlib,math
P=Path(__file__).resolve().parent
READ=json.loads((P/'complete-lossless-semantic-read.json').read_text())
summary=json.loads((P/'related/finite_search_summary.json').read_text())
canonical=[h for d in range(5) for h in product(range(7),repeat=d)]
records=[]
for entry in READ['records']:
 name=entry['file'];d=json.loads((P/'original'/name).read_text());c=d['exact_candidate'];a=c['strategy']['actions']
 assert len(a)==2801 and [tuple(x['history']) for x in a]==canonical
 assert all(set(x)=={'history','action'} and type(x['action']) is int and x['action'] in range(7) for x in a)
 assert d['universal_bound_proved'] is False and d['seed']==20261021
 assert set(c)=={'certified','value','integer_clones','exact_dual_bound','dual_optimal','dual_support','welfare','optimal_welfare','nodes','deviation_checks','strategy'}
 assert set(c['strategy'])=={'terminal_counts','actions'}
 assert c['certified'] is True and c['dual_optimal'] is True and c['nodes']==2801 and c['deviation_checks']==16806
 w=c['integer_clones'];assert len(w)==127 and all(type(x) is int and x>=0 for x in w)
 D={tuple(x['history']):x['action'] for x in a};path=();
 while len(path)<5:path+=D[path],
 root=[path.count(j) for j in range(7)];assert root==c['strategy']['terminal_counts']==d['milp']['root_counts']
 rootmask=sum(1<<j for j in set(path));W=sum(x for mask,x in enumerate(w,1) if mask&rootmask);N=sum(w)
 portfolio=d.get('parameters',{}).get('portfolio',[0,1,2,3,4]);pmask=sum(1<<j for j in portfolio)
 portfolio_coverage=sum(x for mask,x in enumerate(w,1) if mask&pmask)
 assert W==c['welfare'] and portfolio_coverage==N==c['optimal_welfare']
 assert F(N,W)==F(c['value'])==F(c['exact_dual_bound'])
 covered=[frozenset(mask for mask,x in enumerate(w,1) if x and mask>>j&1) for j in range(7)]
 classes=[]
 for j,S in enumerate(covered):
  group=next((g for g in classes if covered[g[0]]==S),None)
  if group is None:classes.append([j])
  else:group.append(j)
 assert all(covered)
 maximal=[all(not (S<T) for T in covered) for S in covered]
 supp=c['dual_support'];assert all(len(t)==2 and type(t[0]) is int and t[0]>=0 and F(t[1])>0 for t in supp)
 assert [t[0] for t in supp]==sorted({t[0] for t in supp})
 source_projection={**d,'exact_candidate':{k:v for k,v in c.items() if k not in ['strategy','integer_clones','dual_support']}}
 sr=[r for r in summary['records'] if r['original_local_filename']==name];assert len(sr)==1
 r={k:v for k,v in sr[0].items() if k not in ['original_local_filename','full_report_retained']};assert r==source_projection
 enc=entry['complete_lossless_source_tree']['exact_candidate']['strategy']['action_encoding']
 words=enc['action_words'];assert all(len(word)==7**depth for depth,word in enumerate(words))
 decoded=[{'history':list(h),'action':int(words[len(h)][sum(t*7**(len(h)-1-j) for j,t in enumerate(h))])} for h in canonical]
 assert decoded==a
 records.append({'file':name,'sha256':entry['sha256'],'complete_action_entries':len(a),'history_domain_and_original_order':'all 7-ary histories length 0..4, depth then lex; round-trip exact','root_path':path,'terminal_counts':root,'nonzero_mask_multiplicities':[[mask,x] for mask,x in enumerate(w,1) if x],'unit_customers':N,'actual_welfare':W,'portfolio':portfolio,'portfolio_covers_all_customers':True,'OPT_equal_N_by_cover_all_plus_trivial_upper_bound':True,'distinct_coverage_classes':classes,'all_seven_labels_have_maximal_nonempty_coverages':all(maximal),'action_alphabet':sorted(set(D.values())),'action_alphabets_by_depth':[sorted(set(x['action'] for x in a if len(x['history'])==depth)) for depth in range(5)],'fixed_cone_dual_support_items_preserved':len(supp),'dual_coefficient_inequalities_checked':False,'full_history_IC_checked':False,'projected_saved_report_equals_named_finite_summary_record':True,'half_margin':2*W-N})
out={'status':'PASS_LOSSLESS_STRUCTURE_SOURCE_COMPARISON_AND_STATIC_COVERAGE','scope':'all 8403 action records and source fields decoded losslessly; exact integer support, root leaf and one cover-all portfolio only; no solver, no IC replay, no G/dual-row reconstruction','records':records,'source_full_semantic_index':'complete-lossless-semantic-read.json','old_or_new_original_program_entries_executed':0,'SPE_enumeration_IC_LP_MIP_runs':0}
print(json.dumps(out,ensure_ascii=False,indent=2))

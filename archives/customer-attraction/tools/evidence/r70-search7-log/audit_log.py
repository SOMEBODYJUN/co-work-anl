"""Independent static audit of all 12 saved games; no SPE recursion or source import."""
from fractions import Fraction as F
import gzip, hashlib, itertools, json, math, re
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=Path('/workspace/scratch/c0ab78c47566/round17-r70-scan_36155.txt')
raw=SOURCE.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='ebe12aedf423068a7db88401b75113d69f43ae0ed2626d2efc264aa490581afb'
lines=raw.decode().splitlines();assert len(lines)==24
rx=re.compile(r'eval (\d+) ratio (\S+) W (\d+) OPT (\d+) margin (-?\d+) terminal((?: \d+){7})')
records=[];details=[]
terminal_multisets=list(itertools.combinations_with_replacement(range(7),6))
assert len(terminal_multisets)==924
for j in range(12):
    match=rx.fullmatch(lines[2*j]);assert match
    evaluation=int(match[1]);ratio_token=match[2];W=int(match[3]);OPT=int(match[4]);margin=int(match[5])
    counts=list(map(int,match[6].split()));assert len(counts)==7 and sum(counts)==6
    assert lines[2*j+1].startswith('weights ')
    pairs=[tuple(map(int,entry.split(':'))) for entry in lines[2*j+1].split()[1:]]
    assert [m for m,n in pairs]==sorted({m for m,n in pairs})
    assert all(1<=m<=127 and n>0 for m,n in pairs)
    mass=dict(pairs);private=[mass.get(1<<a,0) for a in range(7)]
    assert min(private)>0
    # Explicit unit customers, not original bit-array utility or DP helpers.
    customers=[frozenset(a for a in range(7) if m>>a&1) for m,n in pairs for _ in range(n)]
    topics=[{i for i,b in enumerate(customers) if a in b} for a in range(7)]
    assert len(set(map(frozenset,topics)))==7
    assert all(not topics[a]<=topics[b] for a in range(7) for b in range(7) if a!=b)
    leaves=[]
    for multiset in terminal_multisets:
        cover=set().union(*(topics[a] for a in multiset))
        leaves.append({'sorted_labels':list(multiset),'coverage':len(cover)})
    assert max(r['coverage'] for r in leaves)==OPT
    total=len(customers);assert OPT==total-min(private)
    omit_cover=[len(set().union(*(topics[a] for a in range(7) if a!=omit))) for omit in range(7)]
    assert omit_cover==[total-n for n in private]
    selected=[a for a,n in enumerate(counts) for _ in range(n)]
    covered=set().union(*(topics[a] for a in selected));assert len(covered)==W
    per_label={a:sum((F(1,sum(i in topics[b] for b in selected)) for i in topics[a]),F()) for a in set(selected)}
    assert sum(counts[a]*per_label[a] for a in per_label)==W
    assert 2*W-OPT==margin>0
    ratio=F(W,OPT);assert format(float(ratio),'.6g')==ratio_token
    token_error=F(ratio_token)-ratio
    if records:
        assert evaluation>records[-1]['evaluation']
        assert ratio<F(records[-1]['exact_ratio'])
        assert float(ratio)<float(F(records[-1]['exact_ratio']))-1e-12
    positive_types=[{'mask':m,'topics':[a for a in range(7) if m>>a&1],'unit_customers':n} for m,n in pairs]
    r={'record':j+1,'source_lines':[2*j+1,2*j+2],'evaluation':evaluation,
       'saved_ratio_token':ratio_token,'exact_ratio':str(ratio),'saved_token_minus_exact_ratio':str(token_error),
       'W':W,'OPT6':OPT,'half_margin_2W_minus_OPT':margin,'terminal_counts':counts,
       'unit_customers':total,'positive_type_count':len(mass),'zero_type_count':127-len(mass),
       'private_counts':private,'seven_omit_coverages':omit_cover,
       'optimal_omissions':[a for a,v in enumerate(omit_cover) if v==OPT],
       'all_seven_topics_distinct_and_maximal':True,
       'payoff_per_provider_by_selected_label':{str(a):str(v) for a,v in sorted(per_label.items())},
       'counts_are_not_ordered_path':True,'positive_types':positive_types,
       'static_coverage_states_checked':len(leaves),'root_SPE_minimum_recomputed':False}
    records.append(r);details.append({'record':j+1,'evaluation':evaluation,'all_924_static_coverages':leaves})
assert [r['evaluation'] for r in records]==[1,2,339,352,364,368,378,430,3584,3590,47750,47752]
last_change={m:dict((r['mask'],r['unit_customers']) for r in records[-1]['positive_types']).get(m,0)-dict((r['mask'],r['unit_customers']) for r in records[-2]['positive_types']).get(m,0) for m in range(1,128)}
last_change={str(m):n for m,n in last_change.items() if n}
assert last_change=={'48':2}
summary={'status':'PASS','kind':'one independent static-unit-customer audit of the complete historical log',
         'source_sha256':hashlib.sha256(raw).hexdigest(),'source_bytes':len(raw),'source_lines':len(lines),
         'original_source_imports':0,'original_binary_calls':0,'random_search_calls':0,'SPE_DP_calls':0,
         'complete_strategy_reconstructions':0,'new_game_inputs':12,
         'static_terminal_coverages_checked':12*924,'seven_omit_coverages_checked':12*7,
         'declared_terminal_payoffs_checked':12,'records':records,
         'last_two_input_difference_by_mask':last_change,
         'last_exact_ratio_improvement':str(F(records[-2]['exact_ratio'])-F(records[-1]['exact_ratio'])),
         'historical_missing':['argv','actual seed','requested budget','compiler flags','full root continuation sets','ordered paths','complete strategies','stderr completion','process exit status','elapsed time'],
         'limits':['The static checks do not independently certify root SPE reachability or lowest SPE welfare for any record.','A separate shared exact terminal-set/strategy audit handles the last record only.','The basename 36155 is not treated as a verified seed or evaluation budget.']}
details_raw=(json.dumps(details,separators=(',',':'))+'\n').encode()
with (HERE/'static-coverages.json.gz').open('wb') as out:
    with gzip.GzipFile(fileobj=out,mode='wb',mtime=0) as z:z.write(details_raw)
summary['static_detail_uncompressed_bytes']=len(details_raw)
summary['static_detail_uncompressed_sha256']=hashlib.sha256(details_raw).hexdigest()
summary['static_detail_gzip_sha256']=hashlib.sha256((HERE/'static-coverages.json.gz').read_bytes()).hexdigest()
with (HERE/'log-audit.json').open('x') as out:json.dump(summary,out,ensure_ascii=False,indent=2);out.write('\n')
print(json.dumps({'status':'PASS','records':12,'static_coverages':11088,'SPE_DP_calls':0,
                  'last_ratio':records[-1]['exact_ratio'],'last_margin':records[-1]['half_margin_2W_minus_OPT']}))

"""One exact set-DP and full ordered strategy audit; reuse peer static coverages."""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import platform
import time

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--log-audit',type=Path,required=True)
parser.add_argument('--coverages',type=Path,required=True)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args()
args.output_dir.mkdir(exist_ok=False)
clock=time.monotonic()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
log=json.loads(args.log_audit.read_text())
raw=gzip.decompress(args.coverages.read_bytes())
assert sha(args.coverages)==log['static_detail_gzip_sha256']
assert hashlib.sha256(raw).hexdigest()==log['static_detail_uncompressed_sha256']
record=log['records'][-1]
details=json.loads(raw)[-1]
assert record['evaluation']==details['evaluation']==47752
customers=[tuple(t['topics']) for t in record['positive_types'] for _ in range(t['unit_customers'])]
assert len(customers)==159
def count(actions):return tuple(actions.count(a) for a in range(7))
cover={count(x['sorted_labels']):x['coverage'] for x in details['all_924_static_coverages']}
all_terminals={count(list(t)) for t in itertools.combinations_with_replacement(range(7),6)}
assert set(cover)==all_terminals and len(cover)==924
assert record['OPT6']==158 and max(cover.values())==158

# Unit customers and only occupied actions. No original utility helper is imported.
pay={}
for q in sorted(all_terminals):
    row=[0]*7
    for likes in customers:
        load=sum(q[a] for a in likes)
        if load:
            assert 60%load==0
            for a in likes:
                if q[a]:row[a]+=60//load
    pay[q]=tuple(row)

def child(c,a):
    r=list(c);r[a]+=1
    return tuple(r)

@lru_cache(None)
def outcomes(c):
    if sum(c)==6:return frozenset([c])
    menus=[outcomes(child(c,a)) for a in range(7)]
    floors=[min(pay[q][a] for q in menus[a]) for a in range(7)]
    threshold=max(floors)
    result=frozenset(q for a in range(7) for q in menus[a] if pay[q][a]>=threshold)
    assert result
    return result

root=outcomes((0,)*7)
assert outcomes.cache_info().currsize==1716
target=tuple(record['terminal_counts'])
assert target in root
minimum=min(cover[q] for q in root)
assert minimum==record['W']==cover[target]==131
strategy={}
def fill(h,q):
    if len(h)==6:
        assert count(list(h))==q
        return
    c=count(list(h));menus=[outcomes(child(c,a)) for a in range(7)]
    floors=[min(pay[t][a] for t in menus[a]) for a in range(7)]
    chosen=min(a for a in range(7) if q in menus[a] and pay[q][a]>=max(floors))
    strategy[h]=chosen
    for a in range(7):
        continuation=q if a==chosen else min(menus[a],key=lambda t:(pay[t][a],t))
        fill(h+(a,),continuation)
fill((),target)
domain={h for depth in range(6) for h in itertools.product(range(7),repeat=depth)}
assert set(strategy)==domain and len(strategy)==19608
assert all(0<=a<7 for a in strategy.values())
@lru_cache(None)
def leaf(h):
    return h if len(h)==6 else leaf(h+(strategy[h],))
slacks=Counter();layers=[];full_rows=[]
for depth in range(6):
    layer=Counter()
    for h in itertools.product(range(7),repeat=depth):
        chosen=strategy[h];actual_q=count(list(leaf(h)))
        current=pay[actual_q][chosen]
        differences=[]
        for a in range(7):
            other=count(list(leaf(h+(a,))))
            difference=current-pay[other][a]
            assert difference>=0,(h,a,difference)
            slacks[difference]+=1;layer[difference]+=1;differences.append(difference)
        full_rows.append(dict(history=h,action=chosen,actual_terminal=actual_q,
                              scaled60_payoff=current,scaled60_slacks=differences))
    layers.append(dict(depth=depth,comparisons=sum(layer.values()),tight=layer[0],minimum_scaled60_slack=min(layer)))
assert sum(slacks.values())==137256
actual=leaf(())
assert count(list(actual))==target
assert sum(pay[target][a] for a in actual)==60*131

state_details=[]
for depth in range(7):
    for actions in itertools.combinations_with_replacement(range(7),depth):
        c=count(list(actions))
        state_details.append(dict(counts=c,outcomes=sorted(outcomes(c))))
full=dict(payoffs=[dict(counts=q,scaled60_payoffs=pay[q]) for q in sorted(pay)],
          all_1716_state_outcomes=state_details,all_19608_history_checks=full_rows)
full_raw=(json.dumps(full,separators=(',',':'))+'\n').encode()
with (args.output_dir/'exact-details.json.gz').open('wb') as f:
    with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as z:z.write(full_raw)
strategy_file=args.output_dir/'complete-strategy.json'
strategy_file.write_text(json.dumps(dict(players=6,topics=7,entries=[dict(history=h,action=strategy[h]) for h in sorted(strategy,key=lambda h:(len(h),h))]),indent=2)+'\n')
report=dict(status='PASS_EXACT_LAST_LOG_POINT',evaluation=47752,python=platform.python_version(),
            scope='One independent integer60 set DP and one exact full-ordered-history strategy verification for last log point only; static coverages reused from peer audit.',
            original_source_imports=0,original_binary_calls=0,new_original_helper_calls=0,new_DP_calls=1,new_full_strategy_audits=1,LP_calls=0,new_static_coverage_scans=0,
            inputs=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in [args.log_audit,args.coverages]],
            coverage_uncompressed_sha256=hashlib.sha256(raw).hexdigest(),unit_customers=159,positive_types=record['positive_types'],
            count_states=1716,terminal_counts=924,root_outcomes=len(root),
            root_outcome_counts=[dict(counts=q,welfare_from_shared_static_table=cover[q]) for q in sorted(root)],
            minimum_SPE_welfare=minimum,OPT6_from_shared_static_audit=158,exact_ratio=str(Fraction(minimum,158)),half_margin=104,
            target_count=target,actual_ordered_path=actual,actual_payoffs=[str(Fraction(pay[target][a],60)) for a in actual],
            strategy_nodes=len(strategy),all_history_comparisons=sum(slacks.values()),nonself_comparisons=117648,tight_including_self=slacks[0],minimum_exact_slack=str(Fraction(min(slacks),60)),
            exact_slack_histogram={str(Fraction(k,60)):v for k,v in sorted(slacks.items())},layers=layers,
            complete_strategy=dict(path=str(strategy_file),bytes=strategy_file.stat().st_size,sha256=sha(strategy_file)),
            details_gzip=dict(path=str(args.output_dir/'exact-details.json.gz'),bytes=(args.output_dir/'exact-details.json.gz').stat().st_size,sha256=sha(args.output_dir/'exact-details.json.gz')),
            details_uncompressed_sha256=hashlib.sha256(full_raw).hexdigest(),elapsed_seconds=time.monotonic()-clock,
            limits=['Only last historical input is re-solved; first eleven saved root-minimum claims are not newly audited here.','This is a new independent Python definition check, not an old ELF evaluate mode or recovered historical strategy.','No general six-player half statement or historical seed/finish evidence follows.'])
(args.output_dir/'point-audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','root_outcomes','minimum_SPE_welfare','OPT6_from_shared_static_audit','strategy_nodes','all_history_comparisons','tight_including_self','elapsed_seconds']}))

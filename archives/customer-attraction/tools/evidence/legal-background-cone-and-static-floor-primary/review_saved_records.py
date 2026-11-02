"""Inspect only frozen records. No imports or executions of original optimizers.

Cone arithmetic uses Fraction(str(parsed_float)), i.e. shortest-roundtrip decimal
rationalizations of saved numeric fields, without clipping or denominator limits.
Static utilities use exact integer weights and background/terminal counts.
This is not a free-threshold optimality, complete-SPE, or exhaustive-search audit.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations_with_replacement
from pathlib import Path
import json
import math
import time

ROOT = Path(__file__).resolve().parent

def canon(d):
    return json.dumps(d, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()

def digest(d):
    return sha256(canon(d)).hexdigest()

def fr(v):
    return F(str(v))

def masks(k):
    return [[int(bool(i & (1 << a))) for a in range(k)] for i in range(1, 1 << k)]

def fixed_utilities(w, prefix, terminal):
    M = masks(len(prefix))
    return [sum((F(wi * row[a], max(1, sum(row[j] * (prefix[j] + terminal[j])
         for j in range(len(prefix))))) for wi, row in zip(w, M)), F())
         for a in range(len(prefix))]

def leaf_summary(obj):
    c = Counter()
    def walk(v):
        c[type(v).__name__] += 1
        if isinstance(v, dict):
            for x in v.values(): walk(x)
        elif isinstance(v, list):
            for x in v: walk(x)
        elif isinstance(v, float):
            assert math.isfinite(v)
    walk(obj)
    return dict(c)

def sparse(values):
    return {str(i+1): v for i, v in enumerate(values) if v != 0}

def cone(s, where):
    r, k, p = s['r'], s['k'], s['prefix']
    M = masks(k)
    assert len(p) == k and all(isinstance(x, int) and x >= 0 for x in p)
    assert len(s['weights']) == 2**k-1
    assert len(s['query']) == len(s['fractional_q']) == k
    final = [tuple(seq.count(j) for j in range(k)) for seq in combinations_with_replacement(range(k), r)]
    t = s['terminal']; a = s['root_action']
    assert len(t) == k and sum(t) == r and t[a] > 0
    assert all(isinstance(x, int) and x >= 0 for x in t)
    pairs = []
    for q, target, action in s['policy']:
        assert len(q) == k and all(isinstance(v, int) and v >= 0 for v in q) and sum(q) < r
        assert 0 <= target < len(final) and 0 <= action < k
        assert all(x >= y for x, y in zip(final[target], q))
        assert final[target][action] > q[action]
        pairs.append((tuple(q), target))
    assert len(pairs) == len(set(pairs))
    assert all(len(row) == 2**k-1 for row in s['rows'])
    w = list(map(fr, s['weights']))
    rowvals = [sum((fr(c)*v for c,v in zip(row,w)), F()) for row in s['rows']]
    utilities = fixed_utilities(w, p, t)
    total_profit = sum((F(sum(row[j]*t[j] for j in range(k)),
        max(1, sum(row[j]*(p[j]+t[j]) for j in range(k)))) * wi for row,wi in zip(M,w)), F())
    return dict(where=where, saved_record_sha256=digest(s), weights_sha256=digest(s['weights']),
        status=s['status'], kind=s['kind'], r=r,k=k,prefix=p,root_action=a,terminal=t,
        support=sparse(s['weights']), trace=s['trace'], query=s['query'],fractional_q=s['fractional_q'],
        policy_states=len(pairs), policy_distinct_counts=len(set(q for q,_ in pairs)),
        policy_shape_and_target_extension_checked=True, policy_sha256=digest(s['policy']),
        row_count=len(rowvals),row_width=2**k-1,rows_sha256=digest(s['rows']),
        decimal_literal_row_min=str(min(rowvals)),decimal_literal_negative_rows=sum(v<0 for v in rowvals),
        negative_weight_coordinates=[dict(mask=i+1,value=v) for i,v in enumerate(s['weights']) if v<0],
        decimal_literal_remaining_profit=str(total_profit),decimal_literal_leader=str(utilities[a]),
        decimal_literal_query_sum_minus_one=str(sum(map(fr,s['query']),F())-1),
        decimal_literal_fractional_q_sum_minus_one=str(sum(map(fr,s['fractional_q']),F())-1),
        trace_entry_count=len(s['trace']),
        last_debt=s['trace'][-1]['debt'], saved_min_spe_margin=s['trace'][-1]['min_spe_margin'])

def static(s, where):
    r,k,p,w=s['r'],s['k'],s['prefix'],s['weights']
    assert len(w)==2**k-1 and all(isinstance(v,int) and v>=0 for v in w)
    assert len(p)==k and all(isinstance(v,int) and v>=0 for v in p)
    assert len(s['query_q'])==k and len(s['bads'])==k
    value=fr(s['value']); exact=[]; errors=[]
    for a,b in enumerate(s['bads']):
        assert b['action']==a
        t=b['terminal'];assert len(t)==k and sum(t)==r and t[a]==1
        assert all(isinstance(v,int) and v>=0 for v in t)
        u=fixed_utilities(w,p,t)
        assert len(b['utilities'])==k
        e=[abs(fr(x)-v) for x,v in zip(b['utilities'],u)]
        assert max(e)<=F(1,10**11)
        assert abs(fr(b['root'])-u[a])<=F(1,10**11)
        eligible=[u[j]-value for j in range(k) if j!=a and t[j]>0]
        assert all(v>=-F(1,10**8) for v in eligible)
        errors.extend(e)
        exact.append(dict(action=a,terminal=t,exact_utilities=list(map(str,u)),
            exact_root=str(u[a]), saved_utilities=b['utilities'],saved_root=b['root'],
            follower_gaps_to_decimal_saved_value=list(map(str,eligible))))
    exactscore=min(value-fr(x['exact_root']) for x in exact)
    assert abs(exactscore-fr(s['score']))<=F(1,10**11)
    assert abs(fr(s['relative'])-fr(s['score'])/sum(w))<=F(1,10**13)
    return dict(where=where,saved_record_sha256=digest(s),weights_sha256=digest(w),
        r=r,k=k,prefix=p,customer_count=sum(w),support=sparse(w),
        saved_value=s['value'],query_q=s['query_q'],saved_score=s['score'],saved_relative=s['relative'],
        decimal_literal_q_sum_minus_one=str(sum(map(fr,s['query_q']),F())-1),
        exact_root_score_against_decimal_saved_value=str(exactscore),
        max_utility_roundtrip_error=str(max(errors)),bads=exact)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    start=time.perf_counter();manifest=json.loads((ROOT/'source-manifest.json').read_text())
    files=[]
    for x in manifest:
        path=ROOT/'source-root'/x['path'];raw=path.read_bytes()
        assert len(raw)==x['size'] and sha256(raw).hexdigest()==x['sha256']
        if path.suffix!='.json':continue
        d=json.loads(raw);records=[('best',d['best'])]+[(f'bank[{i}]',v) for i,v in enumerate(d['bank'])]
        iscone='rows' in d['best']; review=cone if iscone else static
        summaries=[review(v,label) for label,v in records]
        files.append(dict(id=x['id'],path=x['path'],sha256=x['sha256'],size=x['size'],
            top={k:v for k,v in d.items() if k not in ('best','bank')},
            leaf_summary=leaf_summary(d),record_kind='cone' if iscone else 'static',
            records_including_best=len(records),distinct_saved_records=len({digest(v) for _,v in records}),
            distinct_weight_vectors=len({digest(v['weights']) for _,v in records}),records=summaries))
    totals=dict(json_files=len(files),cone_records=sum(f['records_including_best'] for f in files if f['record_kind']=='cone'),
        static_records=sum(f['records_including_best'] for f in files if f['record_kind']=='static'),
        cone_rows=sum(s['row_count'] for f in files if f['record_kind']=='cone' for s in f['records']),
        cone_policy_states=sum(s['policy_states'] for f in files if f['record_kind']=='cone' for s in f['records']),
        cone_trace_entries=sum(s['trace_entry_count'] for f in files if f['record_kind']=='cone' for s in f['records']),
        static_terminal_records=sum(len(s['bads']) for f in files if f['record_kind']=='static' for s in f['records']),
        static_utility_entries=sum(len(b['exact_utilities']) for f in files if f['record_kind']=='static' for s in f['records'] for b in s['bads']),
        cone_negative_weight_records=sum(bool(s['negative_weight_coordinates']) for f in files if f['record_kind']=='cone' for s in f['records']))
    report=dict(status='PASSED_FIXED_SAVED_RECORD_ARITHMETIC_AND_SCHEMA_ONLY',
        source_manifest_sha256=sha256((ROOT/'source-manifest.json').read_bytes()).hexdigest(),
        checker_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        arithmetic='Fraction(str(parsed_float)) for cone literals and saved thresholds; exact integers for static customer weights and counts; no clipping or small-denominator reconstruction',
        not_certified=['free threshold optimality','full policy transition graph','SPE incentives for all histories','minimum over unsaved static terminals','historical argv/helper versions','universal absence of counterexamples'],
        original_entry_executions=0,optimizer_or_spe_calls=0,totals=totals,files=files,
        elapsed_seconds=time.perf_counter()-start)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],totals=totals,elapsed_seconds=report['elapsed_seconds']),ensure_ascii=False))
if __name__=='__main__':main()

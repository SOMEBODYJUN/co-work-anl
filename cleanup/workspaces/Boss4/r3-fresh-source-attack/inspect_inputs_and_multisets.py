"""Supplement: classify the frozen scan, parse policies, verify m-slot costs.

No source main is imported or called. No SPE inequalities or LPs are solved.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement, product
from collections import Counter
import hashlib
import json
import time

STAGE=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-fresh-source-attack')
EV=STAGE/'archives/customer-attraction/tools/evidence/optimal-fresh-source-attack-primary'
ORIGINAL=EV/'original'
REPORT=ORIGINAL/'research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round11/geometry/audit_optimal_fresh_self_reserve.json'

def main():
    start=time.time()
    output=EV/'supplement/input-scan-and-multiset-check.json'
    assert not output.exists(),'Supplement already executed; do not rerun unnecessarily'
    cert_dir=ORIGINAL/'evidence/certificates/customer_attraction'
    example_dir=ORIGINAL/'examples/customer_attraction'
    certs=sorted(cert_dir.glob('*.json'))
    examples=sorted(example_dir.glob('*.json'))
    # Parse each preserved JSON fully, including the files the source skips.
    schemas=[]
    parsed={}
    for path in certs+examples:
        raw=path.read_bytes()
        data=json.loads(raw)
        parsed[path]=data
        schemas.append(dict(path=str(path.relative_to(ORIGINAL)),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),top_level_fields=list(data),fully_json_parsed=True))
    expected=json.loads(REPORT.read_text())['rows']
    by_name={Path(r['source_certificate']).name:r for r in expected}
    scan=[]
    checks=[]
    for cert in certs:
        example=example_dir/cert.name
        if not example.exists():
            scan.append(dict(name=cert.name,source_reads_json=False,outcome='missing-same-name-example'))
            continue
        data=parsed[cert]
        instance=parsed[example]
        strategy=data.get('strategy',data)
        counts=strategy.get('terminal_counts')
        if counts is None:
            scan.append(dict(name=cert.name,source_reads_json=True,outcome='terminal_counts-not-in-selected-strategy',certificate_fields=list(data),selected_fields=list(strategy)))
            continue
        m,p=instance['players'],len(instance['topics'])
        assert len(counts)==p and all(isinstance(v,int) and v>=0 for v in counts)
        if p>16 or sum(counts)!=m:
            scan.append(dict(name=cert.name,source_reads_json=True,outcome='solve-size-or-count-filter',m=m,p=p,count_sum=sum(counts)))
            continue
        action_rows=strategy['actions']
        policy={tuple(r['history']):r['action'] for r in action_rows}
        histories={h for depth in range(m) for h in product(range(p),repeat=depth)}
        assert set(policy)==histories and len(action_rows)==len(policy)
        assert all(a in range(p) for a in policy.values())
        actual=()
        while len(actual)<m:
            actual+=(policy[actual],)
        actual_counts=[actual.count(a) for a in range(p)]
        assert actual_counts==counts
        customers=instance['customers']
        assert all(isinstance(r.get('multiplicity',1),int) and r.get('multiplicity',1)>0 and all(a in range(p) for a in r['topics']) for r in customers)
        c=[sum(counts[a] for a in r['topics']) for r in customers]
        values=[r.get('multiplicity',1) for r in customers]
        W=sum(v for v,k in zip(values,c) if k)
        R=sum((F(v,1+k) for v,k in zip(values,c) if k),F(0))
        g=[sum((F(v,1+k) for r,v,k in zip(customers,values,c) if a in r['topics']),F(0)) for a in range(p)]
        best_cover=-1
        best_cost=None
        best_tuple=None
        enumerated=0
        for actions in combinations_with_replacement(range(p),m):
            enumerated+=1
            support=set(actions)
            cover=sum(v for r,v in zip(customers,values) if support.intersection(r['topics']))
            cost=sum((g[a] for a in actions),F(0))
            if cover>best_cover or (cover==best_cover and cost<best_cost):
                best_cover,best_cost,best_tuple=cover,cost,actions
        row=by_name[cert.name]
        assert W==row['W'] and R==F(row['reserve'])
        assert best_cover==row['OPT'] and best_cost==F(row['min_optimal_fresh_sum'])
        assert F(W)+R-best_cost==F(row['self_reserve_margin'])
        scan.append(dict(name=cert.name,source_reads_json=True,outcome='included-in-report',m=m,p=p))
        checks.append(dict(name=cert.name,m=m,p=p,customer_type_rows=len(customers),unit_customers=sum(values),complete_policy_actions=len(policy),actions_by_depth=dict(sorted(Counter(map(len,policy)).items())),actual=actual,declared_counts=counts,root_counts_match=True,policy_structure_complete=True,SPE_ICs_checked=False,m_slot_multisets_enumerated=enumerated,OPT=best_cover,min_K0=str(best_cost),min_tuple=best_tuple,W=W,R0=str(R),margin=str(F(W)+R-best_cost),matches_frozen_report=True))
    assert len(checks)==16 and len(scan)==29
    unused_examples=[p.name for p in examples if not (cert_dir/p.name).exists()]
    result=dict(kind='independent-finite-input-structure-and-m-slot-multiset-check',executions=1,original_source_mains_called=False,LPs_solved=False,SPE_ICs_checked=False,certificate_scan_count=len(certs),example_directory_count=len(examples),outcome_counts=dict(Counter(r['outcome'] for r in scan)),scan=scan,example_files_not_matched_by_any_scanned_certificate=unused_examples,fully_parsed_file_schemas=schemas,cases=checks,total_multisets=sum(r['m_slot_multisets_enumerated'] for r in checks),all_checks_passed=True,wall_seconds=time.time()-start)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['kind','certificate_scan_count','example_directory_count','outcome_counts','total_multisets','all_checks_passed','wall_seconds']},ensure_ascii=False))

if __name__=='__main__':
    main()

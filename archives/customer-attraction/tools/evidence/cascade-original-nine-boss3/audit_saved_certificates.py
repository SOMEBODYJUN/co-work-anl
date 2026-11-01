"""Read all frozen cascade records and check each distinct saved policy exactly.

Standard library only.  No discovery program, optimization library, canonical
certificate verifier, or backward-induction solver is imported or executed.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json
import platform
import time


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--evidence',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    started=time.time();tick=time.monotonic()
    manifest=json.loads((args.evidence/'source-manifest.json').read_text())
    sources={};digests={}
    for x in manifest:
        p=args.evidence/'original'/x['id']/Path(x['path']).name
        b=p.read_bytes();assert len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256']
        if p.suffix=='.json':sources[p.name]=json.loads(b);digests[p.name]=x['sha256']
    assert len(sources)==8
    all_nodes={};summaries=[];sha_cases={};history_review=[]
    for name,data in sources.items():
        if 'history' in data:
            params=data['parameters'];m=params['players'];p=params['topics'];history=data['history']
            assert data['universal_bound_proved'] is False
            previous_best=F(0);previous_elapsed=-1;iterations=[]
            for entry in history:
                iterations.append(entry['iteration']);assert sum(entry['root'])==m and len(entry['root'])==p
                assert all(type(n) is int and n>=0 for n in entry['root'])
                assert F(entry['source_ratio'])>=1 and F(entry['best'])>=previous_best
                if 'new_best' in entry:assert F(entry['new_best'])==F(entry['best'])
                assert entry['elapsed']>=previous_elapsed
                previous_best=F(entry['best']);previous_elapsed=entry['elapsed']
                if 'on_path' in entry and entry['on_path'] is not None:
                    path=entry['on_path'];assert len(path)==m and tuple(path.count(a) for a in range(p))==tuple(entry['root'])
            assert len(set(iterations))==len(iterations)
            history_review.append({'file':name,'sha256':digests[name],'parameters':params,
                'saved_record_count':len(history),'iterations':iterations,'last_elapsed':previous_elapsed,
                'last_best':str(previous_best),'new_best_entries':[e for e in history if 'new_best' in e],
                'all_records_read':True,'record_structure_check_not_replay_of_missing_seed_games':True,
                'parameter_keys':sorted(params),'row_key_sets':sorted({tuple(sorted(e)) for e in history})})
            continue
        if digests[name] in sha_cases:
            summaries.append({'file':name,'sha256':digests[name],'byte_identical_to':sha_cases[digests[name]],
                              'additional_policy_check_runs':0})
            continue
        sha_cases[digests[name]]=name
        inst=data['instance'];p=len(inst['topics']);m=inst['players']
        assert type(m) is int and m>0 and p>0 and len(set(inst['topics']))==p
        customers=[]
        for c in inst['customers']:
            topics=c['topics'];mass=c['multiplicity']
            assert type(mass) is int and mass>0
            assert len(set(topics))==len(topics) and all(type(a) is int and 0<=a<p for a in topics)
            customers.append((frozenset(topics),mass))
        record=data['certificate'];actions={}
        for item in record['actions']:
            h=tuple(item['history']);a=item['action']
            assert h not in actions and len(h)<m
            assert all(type(v) is int and 0<=v<p for v in h)
            assert type(a) is int and 0<=a<p
            actions[h]=a
        domain={h for d in range(m) for h in product(range(p),repeat=d)}
        assert set(actions)==domain
        @lru_cache(None)
        def finish(h):
            return h if len(h)==m else finish(h+(actions[h],))
        @lru_cache(None)
        def pay(counts,a):
            return sum((F(mass,sum(counts[b] for b in group)) for group,mass in customers if a in group),F(0))
        def counts(path):return tuple(path.count(a) for a in range(p))
        def welfare(q):return sum(mass for group,mass in customers if any(q[a] for a in group))
        def coverage(J):return sum(mass for group,mass in customers if group.intersection(J))
        node_rows=[];min_nonself=None;strict_nonself=0;nonself=0;groups=defaultdict(Counter)
        for h in sorted(actions,key=lambda h:(len(h),h)):
            a=actions[h];leaf=finish(h);v=pay(counts(leaf),a);deviation=[];slacks=[]
            for b in range(p):
                u=pay(counts(finish(h+(b,))),b);slack=v-u
                assert slack>=0,(name,h,a,b,str(slack))
                deviation.append(str(u));slacks.append(str(slack))
                if a!=b:
                    nonself+=1;strict_nonself+=slack>0
                    min_nonself=slack if min_nonself is None else min(min_nonself,slack)
            node_rows.append({'history':h,'chosen':a,'chosen_payoff':str(v),
                              'deviation_payoffs_by_label':deviation,'slacks_by_label':slacks})
            groups[counts(h)][a]+=1
        path=finish(());q=counts(path)
        assert q==tuple(record['terminal_counts'])==tuple(data['target'])
        W=welfare(q);assert W>0
        profits=[pay(q,a) for a in path];assert sum(profits,F(0))==W
        opts=[{'labels':J,'coverage':coverage(J)} for J in combinations(range(p),min(p,m))]
        OPT=max(x['coverage'] for x in opts);J=tuple(data['portfolio']);assert len(set(J))==len(J)<=m
        value=F(coverage(J),W);assert value==F(data['best_ratio_lower_bound'])
        supports=[frozenset(i for i,(group,mass) in enumerate(customers) if a in group) for a in range(p)]
        physical=set(supports);maxima=[s for s in physical if not any(s<t for t in physical)]
        if 'distinct_maximal_themes' in data:assert len(maxima)==data['distinct_maximal_themes']
        private=[sum(mass for group,mass in customers if group==frozenset([a])) for a in range(p)]
        if 'open' in name or 'private' in name:assert all(1000*n-W>=0 for n in private)
        alias_classes=[list(labels) for support,labels in sorted(
            ((s,tuple(a for a in range(p) if supports[a]==s)) for s in physical),key=lambda x:x[1])]
        summaries.append({'file':name,'sha256':digests[name],'players':m,'labels':p,
            'positive_customer_types':len(customers),'unit_customer_count':sum(mass for _,mass in customers),
            'complete_decision_histories':len(actions),'all_action_comparisons_including_self':len(actions)*p,
            'nonself_comparisons':nonself,'strict_nonself_comparisons':strict_nonself,
            'minimum_nonself_slack':str(min_nonself),'actual_path':path,'actual_counts':q,
            'actual_profits':list(map(str,profits)),'W':W,'OPT':OPT,'fixed_certificate_OPT_over_W':str(F(OPT,W)),
            'stored_comparison':J,'stored_comparison_coverage':coverage(J),'stored_comparison_over_W':str(value),
            'all_maximal_size_comparisons':opts,'distinct_physical_coverages':len(physical),
            'distinct_maximal_coverages':len(maxima),'coverage_alias_classes':alias_classes,
            'last_label_multiplicity':q[path[-1]],
            'last_physical_coverage_multiplicity':sum(supports[a]==supports[path[-1]] for a in path),
            'private_masses_by_label':private,'private_floor_1000_slacks':[1000*n-W for n in private],
            'count_state_groups':len(groups),'groups_with_different_prescribed_actions':sum(len(v)>1 for v in groups.values()),
            'full_count_groups':[{'counts':c,'actions_and_history_multiplicities':dict(v)} for c,v in sorted(groups.items())]})
        all_nodes[name]=node_rows
        print(json.dumps({k:summaries[-1][k] for k in ['file','unit_customer_count','complete_decision_histories','nonself_comparisons','actual_path','W','OPT','fixed_certificate_OPT_over_W','coverage_alias_classes','groups_with_different_prescribed_actions']},ensure_ascii=False),flush=True)
    base=sources['cascade_m5p7.json']['history'];pilot=sources['cascade_m5p7_pilot.json']['history']
    prefix_equal=all({k:v for k,v in a.items() if k!='elapsed'}=={k:v for k,v in b.items() if k!='elapsed'} for a,b in zip(base,pilot))
    assert prefix_equal and len(pilot)==4
    report={'source_files_read':len(manifest),'source_bytes':sum(x['size'] for x in manifest),
            'distinct_saved_policy_checks':len(sha_cases),'new_original_CLI_LP_MIP_random_BI_runs':0,
            'case_summaries':summaries,'history_reports':history_review,'history_entries_read':sum(x['saved_record_count'] for x in history_review),
            'pilot_matches_main_first_four_except_elapsed':prefix_equal,
            'historical_original_code_version_not_bound_by_schema_compatibility':True}
    dump(args.output/'certificate-review.json',report)
    dump(args.output/'all-node-comparisons.json',all_nodes)
    event={'started_unix':started,'elapsed_seconds':time.monotonic()-tick,'python':platform.python_version(),
           'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'assertions_enabled':__debug__,
           'new_checker_invocations':1,'distinct_saved_policy_checks':len(sha_cases),
           'original_imports_CLI_LP_MIP_random_BI':0,
           'output_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.output.iterdir()) if p.is_file()},
           'result':'all three distinct complete policies and all record structure checks passed'}
    dump(args.output/'event.json',event);print(json.dumps(event,ensure_ascii=False),flush=True)


if __name__=='__main__':main()

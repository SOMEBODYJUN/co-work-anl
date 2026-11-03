"""Independent exact recurrence/certificates for four saved Pareto inputs only.

No original imports, canonical solver, random sweep, floor LP, or background
random search. Other saved JSON data are consumed without mathematical reruns.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import hashlib
import json
import platform

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixed_case(record, orientation):
    source = record['instance']
    p, m = len(source['topics']), source['players']
    clients = [frozenset(item['topics']) for item in source['customers']
               for _ in range(item['multiplicity'])]
    topic_sets = [frozenset(i for i, interests in enumerate(clients) if a in interests) for a in range(p)]
    assert len(set(topic_sets)) == p and all(topic_sets)
    direction = 1 if orientation == 'minimize_all' else -1

    @lru_cache(None)
    def pay(q, a):
        if not q[a]:
            return F(0)
        return sum((F(1, sum(q[b] for b in interests)) for interests in clients if a in interests), F(0))

    def welfare(q):
        return sum(any(q[a] for a in interests) for interests in clients)

    def child(k, a):
        return tuple(value + int(i == a) for i, value in enumerate(k))

    def profile(k, q):
        return tuple(pay(q, a) for a in range(p) if k[a]) + (sum((q[a]-k[a])*pay(q,a) for a in range(p)),)

    pruned = []
    @lru_cache(None)
    def menu(k, mode):
        if sum(k) == m:
            return frozenset({k})
        kids = [menu(child(k, a), mode) for a in range(p)]
        threshold = max(min(pay(q, a) for q in kids[a]) for a in range(p))
        possible = frozenset(q for a in range(p) for q in kids[a] if pay(q, a) >= threshold)
        if mode == 'full' or not any(k):
            return possible
        vectors = {q: profile(k, q) for q in possible}
        kept = set()
        for q in sorted(possible):
            dominators = [r for r in sorted(possible)
                          if vectors[r] != vectors[q]
                          and all(direction*x <= direction*y for x,y in zip(vectors[r],vectors[q]))]
            if dominators:
                r = dominators[0]
                pruned.append({'prefix_counts': list(k), 'removed': list(q), 'dominating': list(r),
                    'removed_profile': list(map(str,vectors[q])), 'dominating_profile': list(map(str,vectors[r]))})
            else:
                kept.add(q)
        assert kept
        return frozenset(kept)

    root = (0,) * p
    full = menu(root, 'full')
    reduced = menu(root, 'pruned')
    assert sorted(full) == list(map(tuple, record['full_root_outcomes']))
    assert sorted(reduced) == list(map(tuple, record['compressed_root_outcomes']))
    assert reduced <= full
    full_min, reduced_min = min(map(welfare, full)), min(map(welfare, reduced))
    assert full_min == record['full_minimum_welfare'] < reduced_min == record['compressed_minimum_welfare']
    target = min(full, key=lambda q: (welfare(q), q))
    actions = {}

    def build(h, q):
        if len(h) == m:
            assert tuple(h.count(a) for a in range(p)) == q
            return
        k = tuple(h.count(a) for a in range(p))
        kids = [menu(child(k, a), 'full') for a in range(p)]
        threshold = max(min(pay(t, a) for t in kids[a]) for a in range(p))
        a = next(a for a in range(p) if q in kids[a] and pay(q,a) >= threshold)
        actions[h] = a
        for b in range(p):
            destination = q if b == a else min(kids[b], key=lambda t: (pay(t,b),t))
            assert b == a or pay(destination,b) <= pay(q,a)
            build(h+(b,), destination)

    build((), target)
    expected_histories = {h for depth in range(m) for h in product(range(p), repeat=depth)}
    assert set(actions) == expected_histories

    def finish(h):
        path = tuple(h)
        while len(path) < m:
            path += (actions[path],)
        return tuple(path.count(a) for a in range(p))

    checked = []
    for h in sorted(actions, key=lambda h:(len(h),h)):
        a = actions[h]
        terminal = finish(h)
        slacks = [pay(terminal,a)-pay(finish(h+(b,)),b) for b in range(p)]
        assert min(slacks) >= 0
        checked.append({'history':list(h),'action':a,'terminal_counts':list(terminal),
                        'slacks':list(map(str,slacks))})
    optimum = max(sum(any(a in interests for a in J) for interests in clients)
                  for J in combinations(range(p), min(p,m)))
    root_kids = [menu(child(root,a),'full') for a in range(p)]
    reduced_kids = [menu(child(root,a),'pruned') for a in range(p)]
    root_floors = [min(pay(q,a) for q in root_kids[a]) for a in range(p)]
    reduced_floors = [min(pay(q,a) for q in reduced_kids[a]) for a in range(p)]
    return {'orientation':orientation,'trial':record['trial'],'players':m,'topics':p,
        'unit_customers':len(clients),'five_or_four_distinct_nonempty_topic_subsets':True,
        'full_root_outcomes':[list(q) for q in sorted(full)],
        'compressed_root_outcomes':[list(q) for q in sorted(reduced)],
        'full_minimum_welfare':full_min,'compressed_minimum_welfare':reduced_min,'OPT':optimum,
        'root_full_action_floors':list(map(str,root_floors)),
        'root_pruned_action_floors':list(map(str,reduced_floors)),
        'pruning_events':pruned,'full_minimizer_counts':list(target),
        'full_SPE_histories':len(actions),'full_SPE_comparisons_including_self':len(actions)*p,
        'full_SPE_ordered_actions_and_slacks':checked,
        'computed_count_menus':menu.cache_info().currsize}


def main():
    for item in read(HERE/'source-manifest.json'):
        path=HERE/'original'/Path(item['path']).name
        assert path.stat().st_size==item['size'] and sha(path)==item['sha256']
    cases=[]
    frontier=[]
    for name in ['frontier_probe.json','frontier_probe_3_5.json','frontier_probe_4_5.json']:
        saved=read(HERE/'original'/name)
        assert set(saved)=={'status','seed','trials_requested','trials_checked','players','topics','counterexamples'}
        for label, record in saved['counterexamples'].items():
            assert set(record)=={'trial','instance','full_minimum_welfare','compressed_minimum_welfare','full_root_outcomes','compressed_root_outcomes'}
            case=fixed_case(record,label)
            case['source_report']=name
            cases.append(case)
        frontier.append({key:saved[key] for key in saved if key!='counterexamples'})
    floors=[]
    for name in ['floor_m3k5.json','floor_m5k7.json','floor_m7k6.json']:
        saved=read(HERE/'original'/name)
        assert set(saved)=={'claim','status','seed','topics','players','log','best_weights_float','best_violation_float'}
        assert len(saved['best_weights_float'])==(1<<saved['topics'])-1
        assert max(item['floor_violation_float'] for item in saved['log'])==saved['best_violation_float']<0
        for item in saved['log']:
            assert set(item)=={'iteration','source','floor_violation_float','rows','counts','topic','elapsed'}
            assert len(item['counts'])==saved['topics'] and sum(item['counts'])==saved['players'] and item['counts'][item['topic']]>0
        floors.append({'source_report':name,'players':saved['players'],'topics':saved['topics'],
            'all_saved_log_rows':saved['log'],'best_violation_float':saved['best_violation_float'],
            'best_log_iteration':max(saved['log'],key=lambda item:item['floor_violation_float'])['iteration'],
            'best_float_positive_mask_values':{str(i):value for i,value in enumerate(saved['best_weights_float'],1) if value>0},
            'float_weight_count':len(saved['best_weights_float']),
            'negative_zero_count':sum(value==0 and str(value).startswith('-') for value in saved['best_weights_float']),
            'exact_counterexample_saved':False,'LP_rerun':False})
    result={'scope':'four fixed Pareto instances, exact outcome recurrence and one full ordered SPE per input; floor saved-data consumption only',
        'python':platform.python_version(),'assertions_enabled':__debug__,'primary_sources':10,'primary_sha256_all_match':True,
        'frontier_original_finite_sweep_metadata':frontier,'fixed_pareto_cases':cases,'floor_report_consumption':floors,
        'new_full_ordered_SPE_histories':sum(c['full_SPE_histories'] for c in cases),
        'new_full_ordered_comparisons_including_self':sum(c['full_SPE_comparisons_including_self'] for c in cases),
        'original_main_runs':0,'random_search_trials':0,'optimizer_calls':0}
    (HERE/'four-pareto-cases-and-floor-consumption.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'fixed_pareto_inputs':4,'full_ordered_SPE_histories':result['new_full_ordered_SPE_histories'],
        'full_ordered_comparisons_including_self':result['new_full_ordered_comparisons_including_self'],
        'floor_saved_log_rows':sum(len(x['all_saved_log_rows']) for x in floors),
        'original_main_runs':0,'random_trials':0,'optimizer_calls':0}))


if __name__=='__main__':main()

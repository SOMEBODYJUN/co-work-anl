"""One new bounded CLI event, three helper inputs, literal complete-policy oracle.

The oracle enumerates every complete pure strategy on these tiny trees, not
the source's max-min recurrence. No old witness, model package, or LP is used.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import argparse, hashlib, io, json, platform, runpy, sys, time

def encode(x):
    if isinstance(x, F): return str(x)
    if isinstance(x, dict): return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [encode(v) for v in x]
    return x

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    source = Path(__file__).resolve().parent/'original/potential_probe.py'
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    assert before == 'b902078f2d0486182e904be371956c1bd82bd6b9f1261d50621b56666412e8f1'
    captures = []
    def trace(frame, event, value):
        if frame.f_code.co_filename == str(source) and frame.f_code.co_name == 'one' and event == 'return':
            captures.append((dict(frame.f_locals), value))
        return trace
    command = [str(source), '--m', '3', '--k', '2', '--trials', '1', '--seed', '670305']
    oldargv = sys.argv[:]
    stdout, stderr = io.StringIO(), io.StringIO()
    start = datetime.now(timezone.utc).isoformat()
    tick = time.perf_counter()
    try:
        sys.argv = command
        sys.settrace(trace)
        with redirect_stdout(stdout), redirect_stderr(stderr):
            namespace = runpy.run_path(str(source), run_name='__main__')
    finally:
        sys.settrace(None)
        sys.argv = oldargv
    elapsed = time.perf_counter()-tick
    assert len(captures) == 1 and stderr.getvalue() == ''
    parsed = json.loads(stdout.getvalue())
    assert parsed['trial'] == 0
    assert parsed['weights'] == captures[0][0]['weights']
    assert parsed['result'] == encode(captures[0][1])
    labels = ['original-main-one-trial-new-configuration']
    helper_inputs = [
        ('zero-customers-with-three-empty-labels', [0]*7, 2, 3),
        ('three-common-customers-two-duplicate-labels', [0, 0, 3], 3, 2),
        ('seven-customer-irregular-three-labels', [2, 0, 1, 0, 3, 1, 0], 2, 3),
    ]
    for label, weights, m, k in helper_inputs:
        sys.settrace(trace)
        try: namespace['one'](weights, m, k)
        finally: sys.settrace(None)
        labels.append(label)
    assert len(captures) == 4
    reports = []
    for label, (local, returned) in zip(labels, captures):
        weights, m, k, scale = [local[x] for x in ('weights', 'm', 'k', 'scale')]
        # Each list element is a different unit customer, even for equal likes.
        units = [frozenset(a for a in range(k) if mask & (1 << a))
                 for mask, w in enumerate(weights, 1) for _ in range(w)]
        leaves = list(product(range(k), repeat=m))
        nodes = [h for depth in range(m) for h in product(range(k), repeat=depth)]
        allhist = nodes + leaves
        def pay(p, i):
            return sum((F(1, sum(a in likes for a in p))
                        for likes in units if p[i] in likes), F(0))
        def potential(p):
            return sum((sum((F(1, j) for j in range(1, 1+sum(a in likes for a in p))), F(0))
                        for likes in units), F(0))
        def welfare(p): return sum(any(a in likes for a in p) for likes in units)
        def safe(p):
            return sum((F(1, sum(a in likes for a in p[:i])+m-i)
                        for i in range(m) for likes in units if p[i] in likes), F(0))
        utilities = {p: tuple(pay(p, i) for i in range(m)) for p in leaves}
        potentials = {p: potential(p) for p in leaves}
        assert all(tuple(F(v, scale) for v in local['payoff'][p]) == utilities[p] for p in leaves)
        assert all(F(local['phi'][p], scale) == potentials[p] for p in leaves)
        possible = {h: set() for h in allhist}
        policy_count = good = comparison_count = 0
        for choices in product(range(k), repeat=len(nodes)):
            policy_count += 1
            policy = dict(zip(nodes, choices))
            def follow(h):
                while len(h) < m: h = h+(policy[h],)
                return h
            valid = True
            for h in nodes:
                current = utilities[follow(h)][len(h)]
                for a in range(k):
                    comparison_count += 1
                    if current < utilities[follow(h+(a,))][len(h)]: valid = False
            if valid:
                good += 1
                for h in allhist: possible[h].add(follow(h))
        assert good > 0
        assert set(local['realizable']) == set(allhist)
        assert all(set(local['realizable'][h]) == possible[h] for h in allhist)
        pmax = max(potentials.values())
        root = sorted(possible[()])
        values = {p: potentials[p]+welfare(p)-safe(p)-pmax for p in root}
        best = min(root, key=lambda p: values[p])
        expected = ((values[best]*scale, best, welfare(best)*scale,
                     potentials[best]*scale, safe(best)*scale), pmax*scale, len(root), scale)
        assert returned == expected
        reports.append({
            'label': label, 'm': m, 'k': k, 'weights_in_low_bit_mask_order': weights,
            'unit_customers': len(units), 'scale': scale,
            'complete_policy_count': policy_count, 'complete_SPE_policy_count': good,
            'all_policy_node_action_comparisons': comparison_count,
            'payoff_cells': m*len(leaves), 'potential_cells': len(leaves),
            'all_prefix_sets_compared': len(allhist),
            'source_return': returned, 'minimum_unscaled_margin': values[best],
            'terminal_table': [dict(profile=p, utilities=utilities[p], phi=potentials[p],
                W=welfare(p), safe=safe(p), C=potentials[p]-safe(p),
                margin=potentials[p]+welfare(p)-safe(p)-pmax, root_SPE=p in possible[()]) for p in leaves],
            'all_prefix_outcome_sets': [dict(history=h, outcomes=sorted(possible[h])) for h in allhist],
        })
    after = hashlib.sha256(source.read_bytes()).hexdigest()
    assert before == after
    event = {'status': 'pass', 'new_event_not_historical_replay': True,
        'method': 'runpy unmodified main once; passive one-return observation; three explicit helper calls',
        'source': str(source), 'source_sha256_before': before, 'source_sha256_after': after,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'argv': command, 'started_utc': start, 'original_main_elapsed_seconds': elapsed,
        'original_main_returned_normally': True, 'separate_original_process': False,
        'python': platform.python_version(), 'assertions_enabled': __debug__,
        'original_main_calls': 1, 'original_one_calls': 4,
        'original_main_one_calls': 1, 'additional_helper_one_calls': 3,
        'LP_calls': 0, 'historical_or_mature_witness_reruns': 0,
        'stdout_bytes': len(stdout.getvalue().encode()), 'stderr_bytes': len(stderr.getvalue().encode())}
    report = {'status': 'pass', 'event': event,
        'scope': 'Four fixed new tiny inputs only; exhaustive complete policies for each. No general candidate proof.',
        'cases': reports,
        'totals': {key: sum(r[key] for r in reports) for key in [
            'complete_policy_count', 'complete_SPE_policy_count', 'all_policy_node_action_comparisons',
            'payoff_cells', 'potential_cells', 'all_prefix_sets_compared']}}
    (out/'stdout.txt').write_text(stdout.getvalue())
    (out/'stderr.txt').write_text(stderr.getvalue())
    (out/'execution.json').write_text(json.dumps(event, ensure_ascii=False, indent=2)+'\n')
    (out/'interface-audit.json').write_text(json.dumps(encode(report), ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(encode({'status': 'pass', 'totals': report['totals'],
        'cases': [{'label': r['label'], 'source_return': r['source_return']} for r in reports]})))

if __name__ == '__main__': main()

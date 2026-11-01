"""Small original-source replay plus independent two-player background oracle."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import contextlib
import hashlib
import importlib.util
import io
import json
import random
import sys

HERE = Path(__file__).resolve().parent
DEPENDENCIES = HERE.parents[1]/'R-51-uniform-portfolio-probes/replay'
sys.path.insert(0, str(DEPENDENCIES))
spec = importlib.util.spec_from_file_location('source_background_scan', HERE/'source.py')
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)


def direct_payoff(inst, c, a):
    return sum((F(ct.multiplicity, sum(c[b] for b in ct.topics))
                for ct in inst.customers if a in ct.topics), F())


def direct_outcomes(inst, background):
    """Exhaust all last-mover BR maps, then all first-mover BR actions."""
    k = inst.topic_count
    child_counts = {}
    best_replies = []
    for a in range(k):
        values = []
        for b in range(k):
            c = list(background)
            c[a] += 1
            c[b] += 1
            c = tuple(c)
            child_counts[a, b] = c
            values.append(direct_payoff(inst, c, b))
        best_replies.append(tuple(b for b in range(k) if values[b] == max(values)))
    outcomes = set()
    maps = 0
    for replies in product(*best_replies):
        maps += 1
        first_payoffs = [direct_payoff(inst, child_counts[a, replies[a]], a)
                         for a in range(k)]
        for a in range(k):
            if first_payoffs[a] == max(first_payoffs):
                outcomes.add(child_counts[a, replies[a]])
    return outcomes, maps


def record(inst, background):
    oracle, maps = direct_outcomes(inst, background)
    actual = set(source.ExactSPESolver(inst).outcomes(background))
    assert actual == oracle
    optimum = max(source.utility(inst, background, q) for q in source.comp(2,inst.topic_count))
    values = []
    for c in sorted(actual):
        q = tuple(c[a]-background[a] for a in range(inst.topic_count))
        u = source.utility(inst, background, q)
        alternative = sum((q[a]*direct_payoff(inst,c,a) for a in range(inst.topic_count) if q[a]),F())
        assert u == alternative
        assert sum(q) == 2
        values.append(dict(terminal=c, future_utility=str(u),
                           ratio=None if not u else str(optimum/u)))
    return dict(background=background, instance=inst.to_dict(),
                central_future_optimum=str(optimum), outcomes=values,
                complete_last_reply_maps=maps, independent_outcome_sets_equal=True)


if __name__ == '__main__':
    captured = io.StringIO()
    source.rng.seed(517392)
    with contextlib.redirect_stdout(captured):
        success = source.run(3,2,1,20)
    assert success
    (HERE/'smoke.stdout').write_text(captured.getvalue())
    examples = []
    rng = random.Random(1907)
    for trial in range(10):
        customers = tuple(source.CustomerType(frozenset(a for a in range(3) if mask>>a&1), w)
                          for mask in range(1,8) if (w := rng.randrange(4)))
        inst = source.Instance(('0','1','2'), customers,3)
        background = tuple(1 if a==trial%3 else 0 for a in range(3))
        examples.append(record(inst,background))
    zero = record(source.Instance(('0','1'),(),3),(1,0))
    assert zero['central_future_optimum'] == '0'
    out = dict(source_sha256=hashlib.sha256((HERE/'source.py').read_bytes()).hexdigest(),
               original_smoke=dict(parameters=[3,2,1,20],success=success,stdout=captured.getvalue()),
               direct_two_player_comparisons=examples,zero_customer_boundary=zero,
               full_default_five_runs_executed=False,
               conclusion='finite exact checks only; no universal inequality')
    (HERE/'replay.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(smoke=out['original_smoke'],oracle_inputs=len(examples),
                         zero_terminal_count=len(zero['outcomes']),all_equal=True),indent=2))

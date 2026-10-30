"""Attack a variable-player reduction, using exact complete count-policy enumeration.

Candidate (unproved): minimum complete-history pure-SPE welfare is attained by
some count-based pure SPE.  This is weaker than preserving a specified policy.
No floating point or generic tie breaking is used.  The canonical ordered-tree
solver supplies the comparison outcome set; count-policy enumeration is separate.
"""
import argparse
import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def counts_layer(p, total):
    if p == 1:
        return [(total,)]
    return [(i,) + t for i in range(total + 1)
            for t in counts_layer(p - 1, total - i)]


def incr(q, a):
    return q[:a] + (q[a] + 1,) + q[a + 1:]


def anonymous_outcomes(instance, cap=200000):
    p, m = instance.topic_count, instance.players
    layers = {t: counts_layer(p, t) for t in range(m + 1)}
    utilities = {q: instance.topic_payoffs(q) for q in layers[m]}
    outcomes = {q: q for q in layers[m]}
    policy = {}
    roots = set()
    witnesses = {}
    visited = 0

    def descend(depth):
        nonlocal visited
        if depth < 0:
            visited += 1
            if visited > cap:
                raise OverflowError('anonymous complete-policy cap reached')
            q = outcomes[(0,) * p]
            roots.add(q)
            witnesses.setdefault(q, dict(policy))
            return
        states = layers[depth]
        choices = []
        for q in states:
            childterm = [outcomes[incr(q, a)] for a in range(p)]
            values = [utilities[childterm[a]][a] for a in range(p)]
            best = max(values)
            # Equal terminal outcomes are equivalent to ancestors; retain one
            # prescribed action as a complete-policy witness.
            terms = {}
            for a in range(p):
                if values[a] == best:
                    terms.setdefault(childterm[a], a)
            choices.append(tuple(terms.items()))
        for selection in itertools.product(*choices):
            for q, (terminal, a) in zip(states, selection):
                outcomes[q] = terminal
                policy[q] = a
            descend(depth - 1)
        for q in states:
            outcomes.pop(q, None)
            policy.pop(q, None)

    descend(m - 1)
    return roots, witnesses, visited


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', type=int, default=28691031)
    parser.add_argument('--trials', type=int, default=2000)
    parser.add_argument('--p', type=int, default=3)
    parser.add_argument('--m', type=int, default=3)
    parser.add_argument('--cap', type=int, default=200000)
    parser.add_argument('--output')
    args = parser.parse_args()
    rng = random.Random(args.seed)
    summary = dict(candidate='worst full-history welfare attained by count-based SPE',
                   seed=args.seed, p=args.p, m=args.m, requested=args.trials,
                   completed=0, capped=0, total_anonymous_policies=0,
                   strict_outcome_set_gaps=0, found=None)
    for trial in range(args.trials):
        weights = [rng.randrange(7) for _ in range(2 ** args.p - 1)]
        instance = Instance(tuple(map(str, range(args.p))), tuple(
            CustomerType(frozenset(a for a in range(args.p) if mask & (1 << a)), w)
            for mask, w in enumerate(weights, 1) if w), args.m)
        solver = ExactSPESolver(instance)
        full = solver.outcomes()
        try:
            anon, witnesses, policies = anonymous_outcomes(instance, args.cap)
        except OverflowError:
            summary['capped'] += 1
            continue
        assert anon <= full
        summary['completed'] += 1
        summary['total_anonymous_policies'] += policies
        summary['strict_outcome_set_gaps'] += int(anon != full)
        wf = min(instance.welfare(q) for q in full)
        wa = min(instance.welfare(q) for q in anon)
        if wf < wa:
            bad = min(q for q in full if instance.welfare(q) == wf)
            cert = solver.certificate(bad)
            summary['found'] = dict(trial=trial, weights=weights,
                instance=instance.to_dict(), full_welfare=wf,
                anonymous_welfare=wa, full_outcomes=sorted(full),
                anonymous_outcomes=sorted(anon),
                full_certificate=cert.to_dict(),
                anonymous_policy_count=policies,
                anonymous_witnesses=[dict(terminal=q, actions=[
                    dict(counts=k, action=a) for k, a in sorted(pol.items())])
                    for q, pol in sorted(witnesses.items())])
            break
        if trial and trial % 100 == 0:
            print(json.dumps({k: v for k, v in summary.items() if k != 'found'}), flush=True)
    payload = json.dumps(summary, indent=2)
    if args.output:
        Path(args.output).write_text(payload + '\n')
    print(payload)


if __name__ == '__main__':
    main()

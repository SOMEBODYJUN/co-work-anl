"""Attack a sufficient last-player scalar inequality, not Q-CAG-HALF.

For a genuine on-path outcome let D=sum_{x outside last theme,c_x>0}1/(c_x+1).
The actual final BR implies OPT <= W+(m-1)u_last-D.  A possible stronger
bridge is (m-1)u_last <= W+D.  Enumerate all realizable ordered paths in each
sampled finite game, with exact fractions. A failure only refutes this bridge.
"""
import json
import random
from fractions import Fraction as F
from pathlib import Path
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver


def inspect(instance):
    solver = ExactSPESolver(instance)
    best = None
    for path in solver.ordered_outcomes():
        counts = instance.counts(path)
        payoff = instance.player_payoffs(path)
        W = instance.welfare(counts)
        D = sum((F(c.multiplicity, 1 + sum(counts[t] for t in c.topics))
                 for c in instance.customers
                 if path[-1] not in c.topics and any(counts[t] for t in c.topics)), F(0))
        gap = (instance.players - 1) * payoff[-1] - W - D
        if best is None or gap > best[0]:
            best = gap, path, payoff, D, W
    return solver, best


def main():
    rng = random.Random(20261021)
    completed = 0
    for m, p, trials in [(2, 3, 20), (3, 4, 60), (4, 5, 120), (5, 7, 200)]:
        for trial in range(trials):
            customers = tuple(CustomerType(frozenset(i for i in range(p) if mask >> i & 1), n)
                              for mask in range(1, 1 << p)
                              if (n := (rng.randrange(1, 11) if rng.random() < 0.2 else 0)))
            instance = Instance(tuple(map(str, range(p))), customers, m)
            solver, best = inspect(instance)
            completed += 1
            if best[0] > 0:
                gap, path, payoff, D, W = best
                cert = solver.certificate(on_path=path)
                result = dict(status="bridge_refuted", seed=20261021, games=completed,
                              m=m, p=p, trial=trial, gap=str(gap), path=path,
                              payoff=list(map(str, payoff)), D=str(D), W=W,
                              OPT=instance.optimal_welfare(), instance=instance.to_dict(),
                              certificate=cert.to_dict())
                out = Path(__file__).with_suffix(".json")
                out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
                print(json.dumps({k: result[k] for k in ["status", "games", "m", "p", "gap", "path", "payoff", "D", "W", "OPT"]}), flush=True)
                return
        print(json.dumps(dict(m=m, p=p, trials=trials, status="finite_no_bridge_violation")), flush=True)


if __name__ == "__main__":
    main()

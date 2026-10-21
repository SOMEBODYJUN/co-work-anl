"""Attack an auxiliary all-player floor using complete credible policy cones.

Not a general proof/search certificate. Float LP discovers examples only;
candidate is reconstructed using Fraction-valued canonical SPE solver.
"""
from pathlib import Path
import argparse
import importlib.util
import json
import sys
import time

import numpy as np
from scipy.optimize import linprog

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction').is_dir())
sys.path.insert(0, str(ROOT))
old = Path(__file__).resolve().parents[1]/'credible_search/iterative_search.py'
spec = importlib.util.spec_from_file_location('prior_search', old)
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate
from fractions import Fraction
from math import lcm


def exact_check(p, m, weights):
    rr = [Fraction(float(x)).limit_denominator(100000) for x in weights]
    scale = lcm(*(x.denominator for x in rr))
    cs = tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1), int(r*scale))
               for mask, r in enumerate(rr, 1) if r > 0)
    game = Instance(tuple(map(str, range(p))), cs, m)
    solver = ExactSPESolver(game)
    opt = game.optimal_welfare()
    for q in solver.outcomes():
        w = game.welfare(q)
        for a in range(p):
            if q[a] and m*game.topic_payoffs(q)[a] + w < opt:
                cert = solver.certificate(q)
                verify_certificate(game, cert).assert_valid()
                return {'instance':game.to_dict(), 'counts':q, 'topic':a,
                        'payoff':str(game.topic_payoffs(q)[a]), 'W':w, 'OPT':opt,
                        'floor_gap':str(m*game.topic_payoffs(q)[a]+w-opt),
                        'certificate':cert.to_dict()}
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topics', type=int, default=5)
    ap.add_argument('--players', type=int, default=4)
    ap.add_argument('--rounds', type=int, default=16)
    ap.add_argument('--seed', type=int, default=20261021)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    s = prior.Search(a.topics, a.players, a.seed)
    queue = list(prior.seeds(a.topics, a.players))
    best = -1e100
    log = []
    start = time.monotonic()
    report = {'claim':'every SPE player has m*u_i+W>=OPT_m',
              'status':'finite exploratory LP attack', 'seed':a.seed,
              'topics':a.topics,'players':a.players,'log':log}
    for it in range(a.rounds):
        label, r = queue[it] if it < len(queue) else s.rng.choice(queue)
        if it >= 3 and it % 3 == 2:
            r = r.copy()
            for _ in range(2):
                r[s.rng.randrange(len(r))] += .05*max(r.max(),1)
        _, target, j = s.solve(r)
        actions, A = s.policy(target, ['min','max','uniform','highW'][it%4])
        used = [b for b,c in enumerate(s.Q[target]) if c]
        local = None
        for b in used:
            for jj in list(dict.fromkeys([j]+s.rng.sample(range(len(s.Js)),min(2,len(s.Js))))):
                gain = s.v[jj] - s.w[target] - a.players*s.pay[target,b]
                out = linprog(-gain, A_ub=-A, b_ub=np.zeros(len(A)),
                              A_eq=s.w[[target]], b_eq=[1], bounds=(0,None), method='highs')
                if out.success and (local is None or out.fun < local[0].fun):
                    local = (out,b,jj)
        if local is None:
            continue
        out,b,jj = local
        queue.append((f'LP{it}',out.x))
        value = -out.fun
        row = {'iteration':it,'source':label,'floor_violation_float':value,
               'rows':len(A),'counts':s.Q[target],'topic':b,'elapsed':time.monotonic()-start}
        log.append(row)
        print(json.dumps(row),flush=True)
        if value > best:
            best = value
            report['best_weights_float'] = out.x.tolist()
            report['best_violation_float'] = value
        if value > 1e-7:
            candidate = exact_check(a.topics,a.players,out.x)
            if candidate:
                report['exact_counterexample'] = candidate
                report['status'] = 'auxiliary floor refuted by exact full SPE certificate'
                a.output.write_text(json.dumps(report,indent=2)+'\n')
                return
        a.output.write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()

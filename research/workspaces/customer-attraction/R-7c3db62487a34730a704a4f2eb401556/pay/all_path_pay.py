"""Exact existential-PAY attack over every SPE path and every optimal count.

This is a finite decision procedure, not a general PAY proof.  Count states
cache sets of possible continuations, never a single tie selector.  A surviving
path can be completed by the canonical all-history certificate reconstructor.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import importlib.util
import json
import sys
import time

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))
from customer_attraction import Instance, ExactSPESolver, verify_certificate

SOURCE = REPO / 'research/workspaces/customer-attraction/R-7e9f44beea424d469713364afe7dd180/background_induction/search_background.py'
spec = importlib.util.spec_from_file_location('pay_background_solver', SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def charge(m, k, types):
    """Exact weighted-quantile minimizer; see pay_quantile_and_path_cut.md.

    This is equal to minimizing over every breakpoint and both endpoints.
    types=(multiplicity,b,d); all comparison counts satisfy 0<=d<=m.
    """
    jumps = {}
    initial_slope = F(0)
    for w, b, d in types:
        if d:
            assert 1 <= d <= m and w >= 0
            D = d*(k-1)+m*(b+1)
            t = F(4*m*(b+1), D)
            initial_slope += F(w*d, m*(b+1))
            jumps[t] = jumps.get(t, F(0))+F(w*D, m*(b+1)*(b+k))
    if not jumps:
        return F(0), F(0)
    cumulative = F(0)
    for t in sorted(jumps):
        cumulative += jumps[t]
        if cumulative >= initial_slope:
            break
    else:
        raise AssertionError('nonpositive final slope must exist')
    def at(t):
        return sum(w*(1-F(2*(k-2)*d, m*(b+k))
                        -min(t*d/(m*(b+1)), (t*d/m+4-t)/(b+k)))
                   for w, b, d in types if d)
    return at(t), t


def inspect_instance(inst):
    started = time.time()
    q, m = inst.topic_count, inst.players
    if m < 2:
        return {'m': m, 'status': 'm=1 is outside the k>=2 PAY interface'}
    weights = {sum(1 << a for a in c.topics): c.multiplicity for c in inst.customers}
    # Merge compressed entries with equal membership rather than silently losing
    # duplicates. Instance accepts such entries.
    weights = {}
    for c in inst.customers:
        mask = sum(1 << a for a in c.topics)
        weights[mask] = weights.get(mask, 0) + c.multiplicity
    sol = mod.BackgroundSolver(q, m, [0]*q, weights)
    optimal = max(sol.profits)
    opts = [z for z, v in zip(sol.terminals, sol.profits) if v == optimal]

    @lru_cache(None)
    def min_charge(c):
        k = m-sum(c)
        return min((charge(m, k, [(w,
                    sum(c[a] for a in range(q) if mask >> a & 1),
                    sum(opt[a] for a in range(q) if mask >> a & 1))
                    for mask, w in weights.items()])+(opt,)) for opt in opts)

    best = None
    least_suffix2 = None
    terminals = sol.out
    targets = 0
    states = 0
    for idx, terminal in enumerate(sol.terminals):
        if not terminals >> idx & 1:
            continue
        targets += 1
        pay = sol.pays[idx]

        @lru_cache(None)
        def visit(c):
            nonlocal states, least_suffix2
            states += 1
            depth = sum(c)
            if depth == m-1:
                return (None, ())
            k = m-depth
            raw, t, opt = min_charge(c)
            early = sum(F(c[a]*pay[a], sol.scale) for a in range(q))
            here = raw-2*early
            if k == 2 and (least_suffix2 is None or here > least_suffix2[0]):
                least_suffix2 = (here, terminal, c, t, opt)
            out = None
            floor = sol.thresholds[c]
            for a in range(q):
                if c[a] >= terminal[a] or pay[a] < floor:
                    continue
                d = list(c)
                d[a] += 1
                d = tuple(d)
                if not sol.solve(d) >> idx & 1:
                    continue
                child = visit(d)
                if child is None:
                    continue
                margin = here if child[0] is None else min(here, child[0])
                candidate = (margin, (a,)+child[1])
                if out is None or candidate > out:
                    out = candidate
            return out

        candidate = visit((0,)*q)
        if candidate is not None and (best is None or candidate[0] > best[0]):
            best = candidate+(terminal,)

    assert best is not None
    margin, partial, terminal = best
    c = list(inst.counts(partial))
    final = next(a for a in range(q) if c[a] < terminal[a])
    path = partial+(final,)
    prefix = [0]*q
    early = F(0)
    pay = inst.player_payoffs(path)
    rows = []
    for depth in range(m-1):
        raw, t, opt = min_charge(tuple(prefix))
        rows.append({'k': m-depth, 'minimum_margin': str(raw-2*early),
                     'best_t': str(t), 'optimal_counts': opt})
        prefix[path[depth]] += 1
        early += pay[depth]
    answer = {'status': 'finite exhaustive SPE path decision', 'm': m, 'q': q,
              'optimal_welfare': str(optimal), 'optimal_counts': len(opts),
              'SPE_terminals': targets, 'terminal_state_pairs': states,
              'max_over_SPE_paths_min_over_prefix_opt_t': str(margin),
              'max_suffix2_margin': str(least_suffix2[0]),
              'best_actual_path': path, 'actual_payoffs': list(map(str, pay)),
              'actual_welfare': inst.welfare(terminal), 'path_margins': rows,
              'seconds': round(time.time()-started, 4)}
    if margin > 0:
        # Force only this one root path. Off-path choices remain unrestricted;
        # the canonical constructor independently fills all ordered histories.
        solver = ExactSPESolver(inst)
        cert = solver.certificate(terminal, on_path=path)
        verify_certificate(inst, cert).assert_valid()
        answer['instance'] = inst.to_dict()
        answer['certificate'] = cert.to_dict()
    return answer


if __name__ == '__main__':
    args = sys.argv[1:]
    for name in args:
        inst = Instance.from_dict(json.loads(Path(name).read_text()))
        print(json.dumps({'input': name, **inspect_instance(inst)}, ensure_ascii=False), flush=True)

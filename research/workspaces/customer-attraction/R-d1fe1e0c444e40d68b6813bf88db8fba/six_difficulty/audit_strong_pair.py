"""Independent ordered-history SPE and literal-index audit of parent rows.

Imports the proposed code only to compare its output. All game solving,
query-index sums, hidden-word enumeration and slack accounting are rebuilt.
No optimiser is called. Tests are implementation checks; the README supplies
the arbitrary-instance nonnegative identity.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import time


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "parent/strong_pair_projection.py"
FROZEN = HERE.parent / "parent/strong_pair_projection.json"


def q(n, d):
    return F(n, d) if n else F(0)


def independent_specs():
    return ([('price', name) for name in ('middle', 'B', 'C')]
            + [('cap', name) for name in ('middle', 'B', 'C')]
            + [('last', target) for target in (*range(6), 'avg')]
            + [('pair', i, j) for i in range(6) for j in range(i, 6)]
            + [('pair', i, 'avg') for i in range(6)]
            + [('pair', 'diag'), ('pair', 'off')])


@lru_cache(None)
def literal(a, d, source, t, hidden):
    """List all underlying legal queries rather than multiplying averages."""
    middle, b, c = hidden[:-2], hidden[-2], hidden[-1]
    p, ell = sum(a[:source]), sum(a[:-1])
    background = p + t + sum(middle)
    total = background + b + c
    source_share, last = q(t, total), q(c, total)
    H = q(b, total) + q(c, total) + F(b, (background + 1) * (background + 2))
    comp = (1,) * d + (0,) * (6 - d)
    pair_benefit = lambda x, y: (F(x, background + 1) + F(y, background + 1)
                                 - F(x * y, (background + 1) * (background + 2)))
    costs = [sum((F(x, ell + 1) for x in middle), F(0)), F(b, ell + 1), F(c, ell + 1),
             F(sum(middle)), F(b), F(c)]
    costs += [F(x, background + b + 1) - last for x in a]
    costs.append(sum(F(x, background + b + 1) - last for x in comp) / 6)
    costs += [pair_benefit(a[i], a[j]) - H for i in range(6) for j in range(i, 6)]
    costs += [sum(pair_benefit(a[i], comp[j]) - H for j in range(6)) / 6
              for i in range(6)]
    costs.append(sum(pair_benefit(x, x) - H for x in comp) / 6)
    costs.append(sum(pair_benefit(comp[i], comp[j]) - H
                     for i in range(6) for j in range(6) if i != j) / 30)
    return source_share, tuple(costs)


class OrderedSPE:
    def __init__(self, customers, catalogue, seed):
        self.N, self.catalogue = customers, tuple(catalogue)
        self.rng = random.Random(seed)
        self.actions, self.outcomes = {}, {}
        self.utilities = {}
        self.solve(())

    def payoff(self, history):
        # Only terminal utility values use counts. Strategy/tie decisions use
        # every ordered history and are never memoized by counts.
        counts = tuple(history.count(t) for t in range(len(self.catalogue)))
        if counts not in self.utilities:
            values = [F(0)] * len(self.catalogue)
            for x in range(self.N):
                likes = [(theme >> x) & 1 for theme in self.catalogue]
                load = sum(n * bit for n, bit in zip(counts, likes))
                if load:
                    for t, bit in enumerate(likes):
                        if bit:
                            values[t] += F(1, load)
            self.utilities[counts] = values
        return tuple(self.utilities[counts][t] for t in history)

    def solve(self, h):
        if len(h) == 6:
            self.outcomes[h] = h
            return h
        possible = [self.solve((*h, t)) for t in range(len(self.catalogue))]
        best = max(self.payoff(z)[len(h)] for z in possible)
        candidates = [t for t, z in enumerate(possible) if self.payoff(z)[len(h)] == best]
        chosen = self.rng.choice(candidates)
        self.actions[h] = chosen
        self.outcomes[h] = possible[chosen]
        return possible[chosen]

    def audit_ic(self):
        count = 0
        for h, chosen in self.actions.items():
            z = self.outcomes[h]
            assert z[:len(h) + 1] == (*h, chosen)
            u = self.payoff(z)[len(h)]
            for t in range(len(self.catalogue)):
                assert u >= self.payoff(self.outcomes[(*h, t)])[len(h)]
                count += 1
        return count


def main():
    started = time.monotonic()
    proposed_spec = spec_from_file_location("proposed_strong_pair", TARGET)
    proposed = module_from_spec(proposed_spec)
    proposed_spec.loader.exec_module(proposed)
    specs = independent_specs()
    assert specs == proposed.specs()
    cuts = json.loads(FROZEN.read_text())["cuts"]
    assert len(cuts) == 14
    for cut in cuts:
        assert len(cut['alpha']) == len(specs)
        assert 0 <= cut['source'] <= 3 and 0 <= cut['theme'] <= 5
        assert all(F(x) >= 0 for x in cut['alpha'])
    # Also cover all 24 source/theme pairs with a strictly positive multiplier
    # vector, rather than only the positions discovery happened to use.
    synthetic = [dict(source=i, theme=j, alpha=['1'] * len(specs))
                 for i in range(4) for j in range(6)]
    rng = random.Random(260626)
    game_inputs = [(0, [0]), (1, [1]), (1, [0, 1])]
    for n in (5, 7, 9):
        for _ in range(3):
            topics = {0}
            while len(topics) < 4:
                topics.add(rng.randrange(1 << n))
            game_inputs.append((n, sorted(topics)))
    node_ics = row_tests = option_comparisons = identity_checks = 0
    real_constraint_checks = 0
    records = []
    min_slack = None
    for game_index, (N, catalogue) in enumerate(game_inputs):
        game = OrderedSPE(N, catalogue, seed=101 + game_index)
        node_ics += game.audit_ic()
        actual = game.outcomes[()]
        u = game.payoff(actual)
        comparison = tuple(rng.randrange(len(catalogue)) for _ in range(6))
        memberships = [tuple((catalogue[t] >> x) & 1 for t in actual) for x in range(N)]
        ds = [sum((catalogue[t] >> x) & 1 for t in comparison) for x in range(N)]
        counts = Counter(zip(memberships, ds))
        types, masses = list(counts), list(counts.values())
        K = max(theme.bit_count() for theme in catalogue)
        n = [*map(F, masses), F(K)]
        for cut in [*cuts, *synthetic]:
            source, theme = cut['source'], cut['theme']
            alpha = tuple(map(F, cut['alpha']))
            follow = game.outcomes[(*actual[:source], actual[theme])]
            v = game.payoff(follow)[source]
            assert u[source] >= v
            budgets = []
            for sp in specs:
                multiplicity = (3 - source) if sp[1] == 'middle' else 1
                budgets.append(multiplicity * (u[-1] if sp[0] == 'price' else K)
                               if sp[0] in ('price', 'cap') else F(0))
            assert proposed.budgets(types, n, source) == budgets
            realcosts = [F(0)] * len(specs)
            minsum = localgap = F(0)
            independent_coeff = []
            pu = sum(alpha[j] * ((3 - source) if sp[1] == 'middle' else 1)
                     for j, sp in enumerate(specs) if sp[0] == 'price')
            for (a, d), mass in zip(types, masses):
                t = a[theme]
                # All literal follower words, including middle identities;
                # equal middle sums are compared to the proposed quotient.
                options = []
                quotient = {key: (value, cost) for key, value, cost in proposed.local(a, d, source, theme)}
                for hidden in product((0, 1), repeat=5 - source):
                    value, cost = literal(a, d, source, t, hidden)
                    assert quotient[sum(hidden[:-2]), hidden[-2], hidden[-1]] == (value, cost)
                    option_comparisons += 1
                    options.append(value + sum(x * y for x, y in zip(alpha, cost)))
                minimum = min(options)
                minsum += mass * minimum
                independent_coeff.append(q(a[source], sum(a)) + pu * q(a[-1], sum(a)) - minimum)
            pk = sum(alpha[j] * ((3 - source) if sp[1] == 'middle' else 1)
                     for j, sp in enumerate(specs) if sp[0] == 'cap')
            independent_coeff.append(pk)
            _, proposed_coeff = proposed.row(types, cut)
            assert proposed_coeff == independent_coeff
            row_tests += 1
            # Realized hidden words must be drawn from the same fixed SPE.
            for x, (a, d) in enumerate(zip(memberships, ds)):
                hidden = tuple((catalogue[t] >> x) & 1 for t in follow[source + 1:])
                value, cost = literal(a, d, source, a[theme], hidden)
                for j, c in enumerate(cost):
                    realcosts[j] += c
                realized = value + sum(x * y for x, y in zip(alpha, cost))
                minimum = min(literal(a, d, source, a[theme], h)[0]
                              + sum(x * y for x, y in zip(alpha, literal(a, d, source, a[theme], h)[1]))
                              for h in product((0, 1), repeat=5 - source))
                assert realized >= minimum
                localgap += realized - minimum
            slacks = [b - c for b, c in zip(budgets, realcosts)]
            assert min(slacks) >= 0
            real_constraint_checks += len(slacks)
            lhs = u[source] + pu * u[-1] + pk * K
            row_slack = lhs - minsum
            identity = u[source] - v + sum(x * y for x, y in zip(alpha, slacks)) + localgap
            assert row_slack == identity == sum(c * mass for c, mass in zip(proposed_coeff, n))
            assert row_slack >= 0
            min_slack = row_slack if min_slack is None else min(min_slack, row_slack)
            identity_checks += 1
        records.append(dict(N=N, catalogue=catalogue, ordered_nodes=len(game.actions),
                            actual=actual, repeated_comparison=comparison))
    report = dict(status="PASSED_INDEPENDENT_LITERAL_AND_COMPLETE_SPE_AUDIT",
                  target_sha256=hashlib.sha256(TARGET.read_bytes()).hexdigest(),
                  cuts_sha256=hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
                  multiplier_dimension=len(specs), frozen_cuts=len(cuts),
                  synthetic_all_position_cuts=len(synthetic), games=len(game_inputs),
                  full_ordered_node_action_ics=node_ics, row_comparisons=row_tests,
                  literal_hidden_word_comparisons=option_comparisons,
                  real_nonnegative_constraint_checks=real_constraint_checks,
                  full_nonnegative_identity_checks=identity_checks,
                  minimum_row_slack=str(min_slack),
                  seconds=round(time.monotonic() - started, 3), records=records,
                  scope="Row validity and implementation; not six-player half or full LP-certificate audit")
    (HERE / 'strong_pair_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}, indent=2))


if __name__ == '__main__':
    main()

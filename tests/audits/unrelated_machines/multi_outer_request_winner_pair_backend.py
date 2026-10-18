#!/usr/bin/env python3
"""Independent finite audit of a two-resource winner-moment CE backend.

Small instances only. Does not implement or certify a whole scheduling
algorithm or the proposed small-home-weight class.
"""
import itertools
import json
from fractions import Fraction as F


class Experiment:
    def __init__(self, alpha, coefficients, groups, weights, multipliers, request_rate):
        self.alpha, self.p = alpha, coefficients
        self.groups, self.weights = groups, weights
        self.k = max(groups)+1
        self.h, self.u = len(groups), len(coefficients[0][0])
        self.rules = multipliers
        self.rate = request_rate
        self.fixed_states, self.fixed_requests, self.fixed_rules = {}, {}, {}
        self.rank = {}
        for u in range(self.u):
            for r, lam in enumerate(self.rules):
                candidates = [(h, s) for h in range(self.h) for s in range(len(alpha[h]))
                              if self.p[h][s][u] > 0]
                candidates.sort(key=lambda hs: (-lam[groups[hs[0]]]*weights[hs[0]]*
                                                self.p[hs[0]][hs[1]][u], hs))
                self.rank[u, r] = {hs: j for j, hs in enumerate(candidates)}

    def state_options(self, h):
        if h in self.fixed_states:
            return [(self.fixed_states[h], F(1))]
        out = [(s, a) for s, a in enumerate(self.alpha[h]) if a]
        empty = 1-sum(self.alpha[h], F())
        if empty:
            out.append((None, empty))
        return out

    def rule_options(self, u):
        if u in self.fixed_rules:
            return [(self.fixed_rules[u], F(1))]
        return [(r, F(1, len(self.rules))) for r in range(len(self.rules))]

    def event_probability(self, events):
        # event=(resource, priority-rule, winning-helper, winning-state).
        result = F(1)
        for h in range(self.h):
            subtotal = F()
            for state, prior in self.state_options(h):
                requirements = {}
                possible = True
                for u, rule, winner, winning_state in events:
                    if h == winner:
                        if state != winning_state:
                            possible = False
                            break
                        requirements[u] = 1
                    elif state is not None and (h, state) in self.rank[u, rule]:
                        if self.rank[u, rule][h, state] < self.rank[u, rule][winner, winning_state]:
                            requirements[u] = 0
                if not possible:
                    continue
                probability = prior
                for u, required in requirements.items():
                    request = (F(self.fixed_requests[h, u]) if (h, u) in self.fixed_requests
                               else self.rate if state is not None else F())
                    probability *= request if required else 1-request
                subtotal += probability
            result *= subtotal
        return result

    def moments(self):
        means, seconds = [F() for _ in range(self.k)], [F() for _ in range(self.k)]
        for u in range(self.u):
            for r, probability_r in self.rule_options(u):
                for (h, s) in self.rank[u, r]:
                    value = self.weights[h]*self.p[h][s][u]
                    probability = probability_r*self.event_probability([(u, r, h, s)])
                    i = self.groups[h]
                    means[i] += value*probability
                    seconds[i] += value*value*probability
        for u, v in itertools.combinations(range(self.u), 2):
            for r, pr in self.rule_options(u):
                for t, pt in self.rule_options(v):
                    for (h, s) in self.rank[u, r]:
                        for (j, z) in self.rank[v, t]:
                            if self.groups[h] != self.groups[j]:
                                continue
                            probability = pr*pt*self.event_probability([(u, r, h, s), (v, t, j, z)])
                            value = self.weights[h]*self.p[h][s][u]*self.weights[j]*self.p[j][z][v]
                            seconds[self.groups[h]] += 2*value*probability
        return means, seconds

    def actual_values(self, states, requests, rules):
        values = [F() for _ in range(self.k)]
        for u, r in enumerate(rules):
            available = [(self.rank[u, r][h, s], h, s)
                         for h, s in enumerate(states) if s is not None and requests[h][u]
                         and (h, s) in self.rank[u, r]]
            if available:
                _, h, s = min(available)
                values[self.groups[h]] += self.weights[h]*self.p[h][s][u]
        return values

    def brute(self):
        options = []
        for h in range(self.h):
            possibilities = []
            for state, probability in self.state_options(h):
                for requests in itertools.product(range(2), repeat=self.u):
                    p = probability
                    for request in requests:
                        rate = self.rate if state is not None else F()
                        p *= rate if request else 1-rate
                    if p:
                        possibilities.append((state, requests, p))
            options.append(possibilities)
        means, seconds, mass, count = [F() for _ in range(self.k)], [F() for _ in range(self.k)], F(), 0
        for profile in itertools.product(*options):
            probability = F(1)
            for _, _, p in profile:
                probability *= p
            for rules in itertools.product(range(len(self.rules)), repeat=self.u):
                probability_r = probability/F(len(self.rules)**self.u)
                values = self.actual_values([x[0] for x in profile], [x[1] for x in profile], rules)
                for i in range(self.k):
                    means[i] += probability_r*values[i]
                    seconds[i] += probability_r*values[i]*values[i]
                mass += probability_r
                count += 1
        assert mass == 1
        return means, seconds, count

    def derandomize(self):
        mu, sec = self.moments()
        initial = sum((b-a*a for a, b in zip(mu, sec)), F())
        history = [initial]

        def potential():
            mean, second = self.moments()
            return sum((b-2*center*a+center*center
                        for a, b, center in zip(mean, second, mu)), F())

        def choose(mapping, key, choices):
            evaluations = []
            for value in choices:
                mapping[key] = value
                evaluations.append((potential(), value))
            best, selected = min(evaluations, key=lambda item: item[0])
            mapping[key] = selected
            assert best <= history[-1]
            history.append(best)

        for h in range(self.h):
            choose(self.fixed_states, h, [s for s, _ in self.state_options(h)])
        for h in range(self.h):
            for u in range(self.u):
                choices = [0, 1] if self.fixed_states[h] is not None else [0]
                choose(self.fixed_requests, (h, u), choices)
        for u in range(self.u):
            choose(self.fixed_rules, u, range(len(self.rules)))
        actual = self.actual_values([self.fixed_states[h] for h in range(self.h)],
                                    [[self.fixed_requests[h, u] for u in range(self.u)]
                                     for h in range(self.h)],
                                    [self.fixed_rules[u] for u in range(self.u)])
        assert history[-1] == sum(((a-b)**2 for a, b in zip(actual, mu)), F())
        means, seconds = self.moments()
        assert means == actual and seconds == [a*a for a in actual]
        return initial, history[-1], len(history)-1, actual


def run():
    coefficients = [[[F(3,4), F(1,4)], [F(1,4), F(3,4)]],
                    [[F(1,2), F(1,2)], [F(1), F()]],
                    [[F(1,3), F(2,3)], [F(2,3), F(1,3)]]]
    summaries = []
    for alpha, rate in [([[F(1,2), F(1,2)]]*3, F(1,3)),
                        ([[F(1,4), F(1,4)]]*3, F(1,2))]:
        experiment = Experiment(alpha, coefficients, [0,0,1], [F(1,2),F(1,2),F(1)],
                                [[F(1,3),F(2,3)], [F(2,3),F(1,3)]], rate)
        direct = experiment.moments()
        brute_mean, brute_second, count = experiment.brute()
        assert direct == (brute_mean, brute_second)
        initial, final, steps, values = experiment.derandomize()
        summaries.append({"brute_outcomes": count, "empty_probability": str(1-sum(alpha[0])),
                          "means": list(map(str, brute_mean)), "seconds": list(map(str, brute_second)),
                          "initial_potential": str(initial), "final_potential": str(final),
                          "CE_steps": steps, "final_values": list(map(str, values))})
    print(json.dumps({"scope": "independent finite exact two-resource moments and CE backend audit only",
                      "cases": summaries, "whole_scheduling_algorithm_checked": False,
                      "small_weight_class_instantiated": False}, indent=2))


if __name__ == "__main__":
    run()

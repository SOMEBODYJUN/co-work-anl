#!/usr/bin/env python3
"""Independent exact audit for state_review.md; Python standard library only.

The resource evaluator constructs strategies and recomputes resource loads. It
does not use the certificate surplus formulas to evaluate player costs. The
large amplifier tests check coefficients exactly rather than expanding their
enormous player sets. Run this file directly; its JSON output defaults beside it.
"""

from __future__ import annotations

import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rational(value):
    return str(F(value))


class BinaryRing:
    """Literal finite game with reusable strategy/load/cost evaluation."""

    def __init__(self, *, n, u, v, a, b, k, d, alpha, name=""):
        self.name = name
        self.n, self.u, self.v = tuple(n), tuple(u), tuple(v)
        self.a, self.b, self.k = tuple(a), tuple(b), tuple(k)
        self.d, self.alpha, self.m = d, F(alpha), len(n)
        require(self.m % 2 == 1, "ring must be odd")
        require(all(len(z) == self.m for z in (u, v, a, b, k)), "lengths")
        require(all(nn >= 1 and isinstance(nn, int) for nn in n), "counts")
        require(all(z > 0 for seq in (u, v, a, b) for z in seq), "positivity")
        require(all(0 <= kk <= d for kk in k), "degrees")
        require(self.alpha >= 1, "alpha domain")
        self.players = [("h", i, None) for i in range(self.m)] + [
            ("l", i, j) for i in range(self.m) for j in range(n[i])
        ]
        self.weights = [u[i] if role == "h" else v[i]
                        for role, i, _ in self.players]
        self.strategies = [
            [self.strategy(player, bit) for bit in (0, 1)]
            for player in self.players
        ]

    def strategy(self, player, bit):
        role, i, j = player
        if role == "h":
            prev = (i - 1) % self.m
            return [("A", i, None, bit)] + [
                ("B", prev, jj, bit) for jj in range(self.n[prev])
            ]
        return [("A", i, None, bit), ("B", i, j, 1 - bit)]

    def costs(self, bits):
        chosen = [strategies[bit]
                  for strategies, bit in zip(self.strategies, bits)]
        loads = {}
        for weight, resources in zip(self.weights, chosen):
            for resource in resources:
                loads[resource] = loads.get(resource, 0) + weight
        values = {}
        for resource, load in loads.items():
            kind, i, _, _ = resource
            values[resource] = (self.a[i] * load ** self.k[i]
                                if kind == "A" else self.b[i] * load ** self.d)
        return [sum(values[resource] for resource in resources)
                for resources in chosen]

    def deviation_records(self, bits):
        current = self.costs(bits)
        records = []
        for player_index, player in enumerate(self.players):
            switched = list(bits)
            switched[player_index] = 1 - switched[player_index]
            after = self.costs(switched)[player_index]
            surplus = current[player_index] - self.alpha * after
            records.append((player, current[player_index], after, surplus))
        return records

    def is_all_anti(self, bits):
        return all(bits[pos] != bits[i]
                   for pos, (role, i, _) in enumerate(self.players)
                   if role == "l")

    def normalized_terms(self):
        terms = []
        for i in range(self.m):
            nxt = (i + 1) % self.m
            x, t = F(self.v[i], self.u[i]), F(self.v[i], self.u[nxt])
            p = self.a[i] * self.u[i] ** self.k[i]
            q = self.b[i] * self.u[nxt] ** self.d
            N = (1 + x) ** self.k[i] - self.alpha * (self.n[i] * x) ** self.k[i]
            M = self.alpha * (1 + self.n[i] * x) ** self.k[i] - 1
            P = self.alpha * (1 + t) ** self.d - t ** self.d
            Q = (1 + t) ** self.d - self.alpha
            terms.append(dict(x=x, t=t, p=p, q=q, N=N, M=M, P=P, Q=Q))
        return terms


def original_literal_audit():
    """Reproduce the original four cases and all reported counts."""
    cases = [
        dict(name="mixed_three_hubs", n=(1, 2, 1), u=(2, 3, 5), v=(1, 2, 3),
             a=(1, 2, 4), b=(3, 1, 2), k=(1, 2, 3), d=3, alpha=F(3, 2)),
        dict(name="mixed_with_zero_main_degree", n=(2, 3, 1), u=(1, 4, 2),
             v=(3, 1, 2), a=(2, 3, 1), b=(1, 4, 3), k=(2, 0, 1), d=2, alpha=F(1)),
        dict(name="one_vertex_ring", n=(3,), u=(2,), v=(1,), a=(2,), b=(3,),
             k=(2,), d=2, alpha=F(2)),
        dict(name="degree_zero", n=(1, 1, 1), u=(2, 1, 3), v=(1, 2, 1),
             a=(1, 1, 1), b=(1, 1, 1), k=(0, 0, 0), d=0, alpha=F(1)),
    ]
    totals = dict(profiles=0, matching_light_comparisons=0,
                  worst_state_equalities=0, all_anti_hub_identities=0)
    results = []
    for parameters in cases:
        game = BinaryRing(**parameters)
        counts = {key: 0 for key in totals}
        for bits in product((0, 1), repeat=len(game.players)):
            counts["profiles"] += 1
            all_anti = game.is_all_anti(bits)
            for pos, (player, _, _, surplus) in enumerate(game.deviation_records(bits)):
                role, i, _ = player
                if role == "l" and bits[pos] == bits[i]:
                    nxt = (i + 1) % game.m
                    lower = game.a[i] * (
                        (game.u[i] + game.v[i]) ** game.k[i]
                        - game.alpha * (game.n[i] * game.v[i]) ** game.k[i]
                    ) - game.b[i] * (
                        game.alpha * (game.u[nxt] + game.v[i]) ** game.d
                        - game.v[i] ** game.d
                    )
                    require(surplus >= lower, (game.name, bits, pos, "light bound"))
                    r = sum(bits[zz] == bits[i]
                            for zz, (rr, ii, _) in enumerate(game.players)
                            if rr == "l" and ii == i)
                    if r == 1 and bits[nxt] == bits[i]:
                        require(surplus == lower, (game.name, bits, pos, "worst equality"))
                        counts["worst_state_equalities"] += 1
                    counts["matching_light_comparisons"] += 1
                if role == "h" and all_anti:
                    prev = (i - 1) % game.m
                    a_part = game.a[i] * (
                        game.u[i] ** game.k[i]
                        - game.alpha * (game.u[i] + game.n[i] * game.v[i]) ** game.k[i]
                    )
                    if bits[prev] == bits[i]:
                        b_part = game.n[prev] * game.b[prev] * (
                            (game.u[i] + game.v[prev]) ** game.d
                            - game.alpha * game.u[i] ** game.d
                        )
                    else:
                        b_part = game.n[prev] * game.b[prev] * (
                            game.u[i] ** game.d
                            - game.alpha * (game.u[i] + game.v[prev]) ** game.d
                        )
                    require(surplus == a_part + b_part,
                            (game.name, bits, pos, "hub identity"))
                    counts["all_anti_hub_identities"] += 1
        for key in totals:
            totals[key] += counts[key]
        serial_parameters = {key: (rational(value) if key == "alpha" else value)
                             for key, value in parameters.items()}
        results.append(dict(parameters=serial_parameters, checks=counts, passed=True))
    require(totals["profiles"] == 720, "original profile count")
    require(totals["matching_light_comparisons"] == 1912, "original light count")
    require(totals["all_anti_hub_identities"] == 74, "original hub count")
    return dict(passed=True, totals=totals, cases=results)


def amplifier_recipe_audit():
    """Reproduce the three exact, compressed large-game constructions."""
    results = []
    for d, t, alpha in [(2, F(1, 2), F(11, 10)),
                        (4, F(1, 2), F(4, 3)), (8, F(1, 4), F(2))]:
        y = (1 + t) ** d
        H = (y + t ** (d + 1)) / (1 + t * y)
        require(1 < alpha < H, "H trigger")
        P, Q = alpha * y - t ** d, y - alpha
        B = Q / P
        R = 5
        while not (t ** R < F(1, 4) / alpha and (B / t) ** R > 8 * alpha ** 2):
            R += 4
        m, x = (R + 1) // 2, t ** R
        reset_fraction = F(1, 2) / (alpha * x)
        n = reset_fraction.numerator // reset_fraction.denominator
        ns, ks, xs = [n] + [1] * (m - 1), [1] + [d] * (m - 1), [x] + [1 / t] * (m - 1)
        u = [F(1)] + [t ** (2 * (m - i)) for i in range(1, m)]
        v = [t ** R] + [t ** (2 * (m - i) - 1) for i in range(1, m)]
        require(all(v[i] / u[i] == xs[i] and v[i] / u[(i + 1) % m] == t
                    for i in range(m)), "weight closure")
        N = [(1 + xx) ** kk - alpha * (nn * xx) ** kk
             for xx, kk, nn in zip(xs, ks, ns)]
        M = [alpha * (1 + nn * xx) ** kk - 1
             for xx, kk, nn in zip(xs, ks, ns)]
        require(Q > 0 and all(z > 0 for z in N + M), "positive terms")
        K = [ns[i] * N[i] * Q / (P * M[(i + 1) % m]) for i in range(m)]
        G = F(1)
        for value in K:
            G *= value
        require(G > 1, "strict product")
        delta, halvings = F(2), 0
        while delta ** (m - 1) >= G:
            delta = 1 + (delta - 1) / 2
            halvings += 1
        main = [F(1)]
        for i in range(m - 1):
            main.append(K[i] * main[i] / delta)
        side = [(main[(i + 1) % m] * M[(i + 1) % m] / (ns[i] * Q)
                 + main[i] * N[i] / P) / 2 for i in range(m)]
        light_surpluses = [main[i] * N[i] - side[i] * P for i in range(m)]
        hub_surpluses = [ns[i] * side[i] * Q - main[(i + 1) % m] * M[(i + 1) % m]
                         for i in range(m)]
        require(all(z > 0 for z in light_surpluses + hub_surpluses), "coefficients")
        require(G == (n * (1 + x - alpha * n * x) / (alpha * (1 + n * x) - 1)) * B ** R,
                "reset product identity")
        compressed_game = [dict(n=ns[i], k=ks[i], u=rational(u[i]), v=rational(v[i]),
                               a=rational(main[i] / u[i] ** ks[i]),
                               b=rational(side[i] / u[(i + 1) % m] ** d))
                           for i in range(m)]
        results.append(dict(d=d, t=rational(t), alpha=rational(alpha), H=rational(H),
                            R=R, m=m, reset_count=n, delta=rational(delta), halvings=halvings,
                            product=rational(G), strict_coefficient_checks=2 * m,
                            compressed_game=compressed_game, passed=True))
    return dict(passed=True, cases=results,
                total_strict_coefficient_checks=sum(z["strict_coefficient_checks"] for z in results))


def unique_equal_edge_state(game, edge):
    """Reusable all-anti state with exactly one equal hub edge."""
    require(0 <= edge < game.m, "edge domain")
    hubs = [None] * game.m
    start = (edge + 1) % game.m
    hubs[start] = 0
    for offset in range(1, game.m):
        i = (start + offset) % game.m
        hubs[i] = 1 - hubs[(i - 1) % game.m]
    equal_edges = [i for i in range(game.m) if hubs[i] == hubs[(i + 1) % game.m]]
    require(equal_edges == [edge], "unique equal edge")
    return tuple(hubs + [1 - hubs[i] for i in range(game.m) for _ in range(game.n[i])])


def rotate(values, shift):
    result = [None] * len(values)
    for i, value in enumerate(values):
        result[(i + shift) % len(values)] = value
    return result


def make_witness_cases():
    """Cases with one failed edge, exact-boundary edges, alpha=1, and m=1."""
    configurations = []
    for m in (3, 5):
        base = [100 ** (m - 1 - i) for i in range(m)]
        for shift in range(m):
            configurations.append((f"one_failed_edge_m{m}_rotation{shift}",
                                   rotate(base, shift), F(3, 2), (m - 1 + shift) % m, False))
    for shift in range(3):
        configurations.append((f"exact_hub_boundary_rotation{shift}",
                               rotate([8, 1, 100], shift), F(3, 2), shift, True))
        configurations.append((f"alpha_one_rotation{shift}",
                               rotate([100, 10, 1], shift), F(1), (2 + shift) % 3, False))
    configurations.append(("one_vertex_failed_edge", [1], F(3, 2), 0, False))
    for name, main, alpha, edge, exact_boundary in configurations:
        m = len(main)
        side_ratio = (4 - alpha) / (2 * (4 * alpha - 1))
        game = BinaryRing(name=name, n=[1] * m, u=[1] * m, v=[1] * m,
                          a=main, b=[z * side_ratio for z in main],
                          k=[2] * m, d=2, alpha=alpha)
        yield game, edge, exact_boundary


def hub_failure_witness_audit():
    """Literal full-state tests of the conditional iff and reusable witnesses."""
    cases, total_profiles, total_deviations = [], 0, 0
    for game, edge, exact_boundary in make_witness_cases():
        terms = game.normalized_terms()
        light_margins = [z["p"] * z["N"] - z["q"] * z["P"] for z in terms]
        hub_margins = [game.n[i] * terms[i]["q"] * terms[i]["Q"]
                       - terms[(i + 1) % game.m]["p"] * terms[(i + 1) % game.m]["M"]
                       for i in range(game.m)]
        require(all(z > 0 for z in light_margins), "witness light forcing")
        require(hub_margins[edge] <= 0, "requested failed edge")
        if exact_boundary:
            require(hub_margins[edge] == 0, "exact boundary expected")
        else:
            require(hub_margins[edge] < 0, "strict failure expected")
        if game.name.startswith("one_failed_edge"):
            require(sum(z <= 0 for z in hub_margins) == 1, "single failed hub inequality")
        witness = unique_equal_edge_state(game, edge)
        witness_records = game.deviation_records(witness)
        require(all(record[3] <= 0 for record in witness_records), "literal witness PNE")
        profile_count = pne_count = 0
        for bits in product((0, 1), repeat=len(game.players)):
            records = game.deviation_records(bits)
            literal_pne = all(record[3] <= 0 for record in records)
            equal_edges = [i for i in range(game.m) if bits[i] == bits[(i + 1) % game.m]]
            predicted_pne = game.is_all_anti(bits) and all(hub_margins[i] <= 0 for i in equal_edges)
            require(literal_pne == predicted_pne,
                    (game.name, bits, "conditional characterization"))
            profile_count += 1
            pne_count += int(literal_pne)
            total_deviations += len(records)
        total_profiles += profile_count
        cases.append(dict(
            name=game.name, m=game.m, alpha=rational(game.alpha),
            main_coefficients=[rational(z) for z in game.a],
            side_coefficients=[rational(z) for z in game.b],
            counts=list(game.n), hub_weights=list(game.u), light_weights=list(game.v),
            main_degrees=list(game.k), side_degree=game.d,
            light_forcing_surpluses=[rational(z) for z in light_margins],
            hub_surpluses=[rational(z) for z in hub_margins],
            selected_failed_edge=edge, exact_boundary=exact_boundary,
            witness_bits=list(witness),
            witness_deviations=[dict(player=list(player), current=rational(current),
                                     deviation=rational(after), surplus=rational(surplus))
                                for player, current, after, surplus in witness_records],
            enumerated_profiles=profile_count, alpha_pne_count=pne_count, passed=True,
        ))
    return dict(passed=True, case_count=len(cases), enumerated_profiles=total_profiles,
                unilateral_deviation_checks=total_deviations, cases=cases)


def run_all():
    return dict(
        schema_version=1,
        audit="R1-ODD-RING-STATE-AUDIT-v1",
        arithmetic="Python fractions.Fraction; no floating-point comparisons",
        python_version=platform.python_version(),
        script_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
        literal_state_audit=original_literal_audit(),
        rational_amplifier_recipe_audit=amplifier_recipe_audit(),
        hub_failure_witness_audit=hub_failure_witness_audit(),
        passed=True,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("state_verification.json"))
    args = parser.parse_args()
    result = run_all()
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(dict(
        passed=True,
        output=str(args.output),
        original_literal_totals=result["literal_state_audit"]["totals"],
        amplifier_cases=len(result["rational_amplifier_recipe_audit"]["cases"]),
        amplifier_strict_checks=result["rational_amplifier_recipe_audit"]["total_strict_coefficient_checks"],
        witness_cases=result["hub_failure_witness_audit"]["case_count"],
        witness_profiles=result["hub_failure_witness_audit"]["enumerated_profiles"],
        witness_deviation_checks=result["hub_failure_witness_audit"]["unilateral_deviation_checks"],
    ), sort_keys=True))


if __name__ == "__main__":
    main()

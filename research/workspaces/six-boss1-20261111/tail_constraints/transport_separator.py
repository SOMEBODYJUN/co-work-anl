"""Exact conditional-transport cuts for new terminal <-> old R/Z queries.

The discovery LP fixes a saved necessary-system point.  It is not a game or
an SPE search.  Any reported cut is independently rebuilt with Fraction:
nonnegative whole-row IC weights, complete finite transportation dual
inequalities, exact row construction, and a strictly negative point value.

Only the model's real terminal queries are used.  The old menu identity M
is not reintroduced as a new constraint.  All paths are explicit arguments.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from typing import Any

STATES = ((0, 0), (0, 1), (1, 0), (1, 1))
ORBITS = ((0, 0), (1, 0), (1, 1))
ORBIT_SIZE = {(0, 0): 30, (1, 0): 30, (1, 1): 6}


def serial(value: Any) -> Any:
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


@dataclass
class Group:
    key: tuple
    orbit: tuple[int, int]
    omega: F
    rho: tuple[F, F, F, F]
    columns: dict[tuple[int, int], int]


@dataclass
class FamilyState:
    column: int
    mass: F
    terminal_denom: int
    terminal_payoff: F
    members: tuple[F, ...]


@dataclass
class Block:
    hist_column: int
    prefix4: int
    group: Group
    family_states: list[FamilyState]


class Point:
    def __init__(self, filename: Path):
        self.filename = filename
        self.raw = filename.read_bytes()
        self.report = json.loads(self.raw)
        self.columns = self.report["columns"]
        self.mass = [F(c["weight"]) for c in self.columns]
        assert all(x >= 0 for x in self.mass)
        self.hist = {j: c for j, c in enumerate(self.columns) if c["kind"] == "hist"}
        self.groups: dict[int, list[Group]] = {}
        self.family_states: dict[str, dict[int, list[FamilyState]]] = defaultdict(lambda: defaultdict(list))
        self.labels: dict[str, tuple[str, ...]] = {}

        old_to_current: dict[int, int] = {}
        joint: dict[tuple[int, tuple], dict[tuple[int, int], int]] = defaultdict(dict)
        current_hist = None
        for j, c in enumerate(self.columns):
            if c["kind"] == "hist":
                current_hist = j
            elif c["kind"] == "joint-reply":
                old = c["hist_column_old"]
                if old in old_to_current:
                    assert old_to_current[old] == current_hist
                else:
                    assert current_hist is not None
                    old_to_current[old] = current_hist
                f, diag, wi, wj = c["group"]
                key = (f, diag, tuple(wi), tuple(wj))
                state = tuple(c["state"])
                assert state not in joint[current_hist, key]
                joint[current_hist, key][state] = j

        for hi, h in self.hist.items():
            weights = {}
            for index, n in enumerate(h["hist"]):
                word = ((index >> 2) & 1, (index >> 1) & 1, index & 1)
                weights[word] = n
            groups = []
            orbit_totals = defaultdict(F)
            for (hj, key), indices in sorted(joint.items()):
                if hj != hi:
                    continue
                f, diag, wi, wj = key
                orbit = (f, diag)
                assert orbit in ORBITS
                assert set(indices) == set(STATES[1:])
                if diag:
                    assert wi == wj
                    count = weights[wi]
                elif wi == wj:
                    count = weights[wi] * (weights[wi] - 1)
                else:
                    count = weights[wi] * weights[wj]
                assert count > 0
                rho_nonzero = [self.mass[indices[state]] for state in STATES[1:]]
                rho = (self.mass[hi] - sum(rho_nonzero, F()), *rho_nonzero)
                assert all(v >= 0 for v in rho)
                omega = F(count, ORBIT_SIZE[orbit])
                groups.append(Group(key, orbit, omega, rho, indices))
                orbit_totals[orbit] += omega
            assert dict(orbit_totals) == {o: F(1) for o in ORBITS}
            self.groups[hi] = groups

        for j, c in enumerate(self.columns):
            kind = c["kind"]
            if kind not in ("actual-B-family-state", "maximum-root-family-state"):
                continue
            hi = c["hist_column"]
            a = tuple(map(int, self.hist[hi]["actual_bits"]))
            hidden = tuple(c["hidden"])
            if kind == "actual-B-family-state":
                source = c["source"]
                assert source in (2, 3, 4)
                family = f"B{source}"
                sequence = a[:source - 1] + (a[5],) + hidden
                labels = tuple(f"H{k+1}" for k in range(len(hidden))) + ("Y-average",)
                members = tuple(F(v) for v in hidden) + (F(c["ell"], 6),)
            else:
                family = "Mroot"
                sequence = (c["M"],) + hidden
                labels = ("M",) + tuple(f"H{k+1}" for k in range(5)) + ("Y-average",)
                members = tuple(F(v) for v in sequence) + (F(c["ell"], 6),)
            assert len(sequence) == 6 and c["ell"] in (0, 6)
            assert family not in self.labels or self.labels[family] == labels
            self.labels[family] = labels
            denom = sum(sequence[:-1]) + 1
            self.family_states[family][hi].append(
                FamilyState(j, self.mass[j], denom, F(sequence[-1], denom), members)
            )
        assert set(self.family_states) == {"B2", "B3", "B4", "Mroot"}
        for family, by_hist in self.family_states.items():
            assert set(by_hist) == set(self.hist)
            for hi, states in by_hist.items():
                assert sum((s.mass for s in states), F()) == self.mass[hi]

    def blocks(self, family: str) -> list[Block]:
        out = []
        for hi, h in self.hist.items():
            prefix4 = sum(map(int, h["actual_bits"][:4]))
            for group in self.groups[hi]:
                out.append(Block(hi, prefix4, group, self.family_states[family][hi]))
        return out


def row_specs(labels: tuple[str, ...]) -> list[tuple]:
    out = []
    for orbit in ORBITS:
        out.extend((("new-to-R", orbit), ("new-to-Z", orbit)))
        out.extend(("Z-to-new", orbit, j, label) for j, label in enumerate(labels))
    return out


def budgets(point: Point, family: str, specs: list[tuple]) -> list[F]:
    terminal = sum((state.mass * state.terminal_payoff
                    for states in point.family_states[family].values() for state in states), F())
    old_z = {o: F() for o in ORBITS}
    for hi, h in point.hist.items():
        prefix4 = sum(map(int, h["actual_bits"][:4]))
        for group in point.groups[hi]:
            old_z[group.orbit] += group.omega * sum(
                (mass * F(z, prefix4 + r + 1) for (r, z), mass in zip(STATES, group.rho)), F())
    return [terminal if spec[0] != "Z-to-new" else old_z[spec[1]] for spec in specs]


def primitive_cost(block: Block, rz: int, state: FamilyState, spec: tuple) -> F:
    if spec[1] != block.group.orbit:
        return F()
    r, z = STATES[rz]
    if spec[0] == "new-to-R":
        return block.group.omega * F(r, state.terminal_denom)
    if spec[0] == "new-to-Z":
        return block.group.omega * F(z, state.terminal_denom)
    assert spec[0] == "Z-to-new"
    return block.group.omega * state.members[spec[2]] / (block.prefix4 + r + 1)


def sorted_quote(q: F, states: list[FamilyState]) -> F:
    remaining = q
    value = F()
    for state in sorted(states, key=lambda x: -x.terminal_denom):
        take = min(remaining, state.mass)
        value += take / state.terminal_denom
        remaining -= take
    assert remaining == 0
    # Independent nested-level formula, exact for six-player quotes.
    layer_value = q / 6
    for k in range(1, 6):
        high_mass = sum((s.mass for s in states if s.terminal_denom > k), F())
        layer_value += max(F(), q - high_mass) / (k * (k + 1))
    assert value == layer_value
    return value


def single_row_lower_cost(point: Point, family: str, spec: tuple) -> F:
    """Independent Fraction sorting diagnostics, not the joint separation."""
    total = F()
    for block in point.blocks(family):
        if block.group.orbit != spec[1]:
            continue
        if spec[0] == "Z-to-new":
            r_mass = block.group.rho[2] + block.group.rho[3]
            y_mass = sum((s.mass * s.members[spec[2]] for s in block.family_states), F())
            p = block.prefix4
            value = y_mass / (p + 2) + max(F(), y_mass - r_mass) / ((p + 1) * (p + 2))
        else:
            coordinate = 0 if spec[0] == "new-to-R" else 1
            q = sum((mass * state[coordinate] for state, mass in zip(STATES, block.group.rho)), F())
            value = sorted_quote(q, block.family_states)
        total += block.group.omega * value
    return total


def paired_RZ_lower_cost(point: Point, family: str, orbit: tuple[int, int]) -> F:
    """Exact joint cost of the equal-weight new-to-R and new-to-Z rows."""
    total = F()
    for block in point.blocks(family):
        if block.group.orbit != orbit:
            continue
        union = sum(block.group.rho[1:], F())
        intersection = block.group.rho[3]
        total += block.group.omega * (sorted_quote(union, block.family_states)
                                      + sorted_quote(intersection, block.family_states))
    return total


def discover(point: Point, family: str, specs: list[tuple], rhs: list[F], tolerance: float) -> dict:
    """Fixed-point coupling feasibility; lambda is only a discovery output."""
    import numpy as np
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix

    blocks = point.blocks(family)
    variables = []
    block_vars = defaultdict(list)
    for bi, block in enumerate(blocks):
        for ri, rho in enumerate(block.group.rho):
            if not rho:
                continue
            for si, state in enumerate(block.family_states):
                if not state.mass:
                    continue
                index = len(variables)
                variables.append((bi, ri, si))
                block_vars[bi].append(index)
    n = len(variables)
    eq_rows, eq_cols, eq_data, eq_rhs = [], [], [], []
    for bi, indices in block_vars.items():
        block = blocks[bi]
        rs = [ri for ri, rho in enumerate(block.group.rho) if rho]
        ss = [si for si, state in enumerate(block.family_states) if state.mass]
        for ri in rs:
            er = len(eq_rhs)
            eq_rhs.append(float(block.group.rho[ri]))
            for vi in indices:
                if variables[vi][1] == ri:
                    eq_rows.append(er); eq_cols.append(vi); eq_data.append(1.)
        # The last state equation follows from all row equations.
        for si in ss[:-1]:
            er = len(eq_rhs)
            eq_rhs.append(float(block.family_states[si].mass))
            for vi in indices:
                if variables[vi][2] == si:
                    eq_rows.append(er); eq_cols.append(vi); eq_data.append(1.)
    ub_rows, ub_cols, ub_data = [], [], []
    for vi, (bi, ri, si) in enumerate(variables):
        block = blocks[bi]
        state = block.family_states[si]
        for k, spec in enumerate(specs):
            cost = primitive_cost(block, ri, state, spec)
            if cost:
                ub_rows.append(k); ub_cols.append(vi); ub_data.append(float(cost))
    for k in range(len(specs)):
        ub_rows.append(k); ub_cols.append(n); ub_data.append(1.)
    aeq = coo_matrix((eq_data, (eq_rows, eq_cols)), shape=(len(eq_rhs), n + 1)).tocsc()
    aub = coo_matrix((ub_data, (ub_rows, ub_cols)), shape=(len(specs), n + 1)).tocsc()
    objective = np.zeros(n + 1); objective[-1] = -1.
    sol = linprog(objective, A_ub=aub, b_ub=[float(v) for v in rhs],
                  A_eq=aeq, b_eq=eq_rhs,
                  bounds=[(0, None)] * n + [(None, None)], method="highs",
                  options={"primal_feasibility_tolerance": tolerance,
                           "dual_feasibility_tolerance": tolerance})
    result = {"success": bool(sol.success), "message": str(sol.message),
              "variables": n, "marginal_equations": len(eq_rhs), "query_rows": len(specs)}
    if sol.success:
        result["max_common_slack_float"] = float(sol.x[-1])
        result["dual_weights_float"] = [max(0., -float(v)) for v in sol.ineqlin.marginals]
    return result


def exact_transport(rho: tuple[F, ...], eta: list[F], costs: list[list[F]]) -> dict:
    """Successive shortest paths, then an exact complete-domain dual.

    Zero-mass rows/columns stay in the domain.  Their dual inequalities are
    checked too; a cut therefore remains valid when later points use them.
    """
    nr, nc = len(rho), len(eta)
    total = sum(rho, F())
    assert total == sum(eta, F()) and total > 0
    source, sink = nr + nc, nr + nc + 1
    node_count = sink + 1
    adjacency: list[list[list]] = [[] for _ in range(node_count)]

    def edge(u, v, cap, cost):
        ui, vi = len(adjacency[u]), len(adjacency[v])
        adjacency[u].append([v, vi, cap, cost])
        adjacency[v].append([u, ui, F(), -cost])
        return (u, ui)

    for ri, mass in enumerate(rho):
        edge(source, ri, mass, F())
    refs = [[None] * nc for _ in range(nr)]
    capacity = total + 1  # Every forward transportation edge stays residual.
    for ri in range(nr):
        for si in range(nc):
            refs[ri][si] = edge(ri, nr + si, capacity, costs[ri][si])
    for si, mass in enumerate(eta):
        edge(nr + si, sink, mass, F())

    sent = F()
    augmentations = 0
    while sent < total:
        dist = [None] * node_count
        pred = [None] * node_count
        dist[source] = F()
        for _ in range(node_count - 1):
            changed = False
            for u in range(node_count):
                if dist[u] is None:
                    continue
                for ei, (v, _, cap, cost) in enumerate(adjacency[u]):
                    if cap <= 0:
                        continue
                    candidate = dist[u] + cost
                    if dist[v] is None or candidate < dist[v]:
                        dist[v] = candidate; pred[v] = (u, ei); changed = True
            if not changed:
                break
        assert dist[sink] is not None
        amount = total - sent
        node = sink
        seen = set()
        while node != source:
            assert node not in seen and pred[node] is not None
            seen.add(node)
            u, ei = pred[node]
            amount = min(amount, adjacency[u][ei][2])
            node = u
        assert amount > 0
        node = sink
        while node != source:
            u, ei = pred[node]
            v, rev, _, _ = adjacency[u][ei]
            adjacency[u][ei][2] -= amount
            adjacency[v][rev][2] += amount
            node = u
        sent += amount
        augmentations += 1
        assert augmentations < 10000

    flow = [[F()] * nc for _ in range(nr)]
    for ri in range(nr):
        for si in range(nc):
            u, ei = refs[ri][si]
            flow[ri][si] = capacity - adjacency[u][ei][2]
    assert all(sum(flow[ri], F()) == rho[ri] for ri in range(nr))
    assert all(sum((flow[ri][si] for ri in range(nr)), F()) == eta[si] for si in range(nc))

    # All-source shortest distances on the complete transportation residual.
    edges = []
    for ri in range(nr):
        for si in range(nc):
            edges.append((ri, nr + si, costs[ri][si]))
            if flow[ri][si]:
                edges.append((nr + si, ri, -costs[ri][si]))
    dist = [F()] * (nr + nc)
    for iteration in range(nr + nc):
        changed = False
        for u, v, cost in edges:
            if dist[v] > dist[u] + cost:
                dist[v] = dist[u] + cost; changed = True
        if not changed:
            break
        assert iteration + 1 < nr + nc, "negative residual cycle"
    alpha = [-dist[ri] for ri in range(nr)]
    beta = [dist[nr + si] for si in range(nc)]
    # Saturate also the zero-mass coordinates.  The residual construction can
    # leave those potentials unnecessarily weak.  These two c-transforms only
    # increase a feasible dual, and complementary slackness keeps the value
    # unchanged on positive marginals.  Equal cost rows then receive equal
    # alpha even when one of their current masses is zero.
    alpha = [min(costs[ri][si] - beta[si] for si in range(nc)) for ri in range(nr)]
    beta = [min(costs[ri][si] - alpha[ri] for ri in range(nr)) for si in range(nc)]
    slacks = [costs[ri][si] - alpha[ri] - beta[si]
              for ri in range(nr) for si in range(nc)]
    assert min(slacks) >= 0
    primal = sum((flow[ri][si] * costs[ri][si]
                  for ri in range(nr) for si in range(nc)), F())
    dual = sum((a * m for a, m in zip(alpha, rho)), F()) + sum((b * m for b, m in zip(beta, eta)), F())
    assert primal == dual
    return {"minimum": primal, "alpha": alpha, "beta": beta,
            "flow": [(ri, si, flow[ri][si]) for ri in range(nr) for si in range(nc) if flow[ri][si]],
            "domain_pairs": nr * nc, "minimum_dual_slack": min(slacks),
            "augmentations": augmentations}


def exact_certificate(point: Point, family: str, specs: list[tuple], rhs: list[F], weights: list[F]) -> dict:
    assert len(weights) == len(specs) and all(w >= 0 for w in weights) and any(weights)
    row = defaultdict(F)
    terminal_weight = sum((w for w, spec in zip(weights, specs) if spec[0] != "Z-to-new"), F())
    for states in point.family_states[family].values():
        for state in states:
            row[state.column] += terminal_weight * state.terminal_payoff
    old_z_weights = {o: F() for o in ORBITS}
    for weight, spec in zip(weights, specs):
        if spec[0] == "Z-to-new":
            old_z_weights[spec[1]] += weight
    for hi, h in point.hist.items():
        prefix4 = sum(map(int, h["actual_bits"][:4]))
        for group in point.groups[hi]:
            for state, column in group.columns.items():
                r, z = state
                row[column] += old_z_weights[group.orbit] * group.omega * F(z, prefix4 + r + 1)

    exact_budget = sum((w * b for w, b in zip(weights, rhs)), F())
    total_minimum = F()
    witnesses = []
    pairs = 0
    for block in point.blocks(family):
        if not sum(block.group.rho, F()):
            continue
        active = [(weight, spec) for weight, spec in zip(weights, specs)
                  if weight and spec[1] == block.group.orbit]
        if not active:
            continue
        costs = [[sum((weight * primitive_cost(block, ri, state, spec)
                       for weight, spec in active), F())
                  for state in block.family_states] for ri in range(4)]
        transport = exact_transport(block.group.rho, [state.mass for state in block.family_states], costs)
        alpha, beta = transport["alpha"], transport["beta"]
        row[block.hist_column] -= alpha[0]
        for ri, state in enumerate(STATES[1:], 1):
            row[block.group.columns[state]] -= alpha[ri] - alpha[0]
        for state, coefficient in zip(block.family_states, beta):
            row[state.column] -= coefficient
        total_minimum += transport["minimum"]
        pairs += transport["domain_pairs"]
        witnesses.append({"hist_column": block.hist_column, "group": block.group.key,
                          "alpha": alpha,
                          "beta_by_column": [(state.column, value) for state, value in zip(block.family_states, beta)],
                          "minimum": transport["minimum"],
                          "positive_flow": [(STATES[ri], block.family_states[si].column, value)
                                            for ri, si, value in transport["flow"]],
                          "domain_pairs": transport["domain_pairs"],
                          "minimum_dual_slack": transport["minimum_dual_slack"]})
    sparse_row = sorted((j, value) for j, value in row.items() if value)
    row_value = sum((value * point.mass[j] for j, value in sparse_row), F())
    assert row_value == exact_budget - total_minimum
    return {"whole_row_weights": [(spec, weight) for spec, weight in zip(specs, weights) if weight],
            "exact_budget": exact_budget, "transport_minimum": total_minimum,
            "exact_slack": row_value, "strictly_separates": row_value < 0,
            "dual_domain_pairs_checked": pairs,
            "sparse_original_row": sparse_row, "transport_witnesses": witnesses}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("point", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--families", nargs="+", choices=("B2", "B3", "B4", "Mroot"),
                        default=("B2", "B3", "B4", "Mroot"))
    parser.add_argument("--tolerance", type=float, default=1e-9)
    parser.add_argument("--rational-denominator", type=int, default=10**6)
    parser.add_argument("--all-negative-singles", action="store_true",
                        help="Also certify every negative individual query projection, deduplicating the chosen joint cut.")
    args = parser.parse_args()
    point = Point(args.point)
    result = {"scope": "fixed saved point; exact terminal-query transport projection; not SPE or universal half",
              "input": str(args.point.resolve()), "input_sha256": hashlib.sha256(point.raw).hexdigest(),
              "column_count": len(point.columns), "W": point.report.get("W"), "families": []}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for family in args.families:
        specs = row_specs(point.labels[family])
        rhs = budgets(point, family, specs)
        singles = [(spec, budget - single_row_lower_cost(point, family, spec))
                   for spec, budget in zip(specs, rhs)]
        paired = [(orbit, 2 * rhs[0] - paired_RZ_lower_cost(point, family, orbit)) for orbit in ORBITS]
        item = {"family": family, "labels": point.labels[family],
                "single_row_slacks": singles, "paired_RZ_slacks": paired}
        discovery = discover(point, family, specs, rhs, args.tolerance)
        item["discovery"] = discovery
        if discovery.get("success") and discovery["max_common_slack_float"] < -10 * args.tolerance:
            weights = [F(str(v)).limit_denominator(args.rational_denominator)
                       if v > args.tolerance else F() for v in discovery["dual_weights_float"]]
            item["certificate"] = exact_certificate(point, family, specs, rhs, weights)
        if args.all_negative_singles:
            extra = []
            chosen = item.get("certificate", {}).get("whole_row_weights", [])
            for k, (spec, slack) in enumerate(singles):
                if slack >= 0:
                    continue
                if len(chosen) == 1 and chosen[0][0] == spec:
                    continue
                weights = [F()] * len(specs)
                weights[k] = F(1)
                cert = exact_certificate(point, family, specs, rhs, weights)
                assert cert["exact_slack"] == slack and cert["strictly_separates"]
                extra.append(cert)
            item["additional_single_certificates"] = extra
        result["families"].append(item)
        args.output.write_text(json.dumps(serial(result), ensure_ascii=False, indent=2) + "\n")
        summary = {"family": family,
                   "minimum_single_row_slack": str(min(slack for _, slack in singles)),
                   "negative_single_rows": sum(slack < 0 for _, slack in singles),
                   "paired_RZ_slacks": paired,
                   "discovery": {k: v for k, v in discovery.items() if k != "dual_weights_float"}}
        if "certificate" in item:
            summary["certificate"] = {k: v for k, v in item["certificate"].items()
                                      if k not in ("sparse_original_row", "transport_witnesses")}
        if "additional_single_certificates" in item:
            summary["additional_single_certificates"] = len(item["additional_single_certificates"])
        print(json.dumps(serial(summary), ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()

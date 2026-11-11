"""Finite exact epigraph extension for all 81 chosen single-query projections.

This adds no hypothesis and does not assert a joint transport completion.
The inequalities exactly encode the separate scalar minima.  Their sparse
Fraction coefficients can be appended to the current original-column LP.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from transport_separator import Point, ORBITS, STATES, serial


def metadata_sha(columns):
    stripped = [{k: v for k, v in column.items() if k != "weight"} for column in columns]
    raw = json.dumps(stripped, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def build(point: Point):
    base_n = len(point.columns)
    descriptors = []
    new_values = []
    rows = []
    family_counts = {}

    def add_variable(descriptor, canonical_value):
        index = base_n + len(descriptors)
        descriptors.append(descriptor)
        assert canonical_value >= 0
        new_values.append(canonical_value)
        return index

    def add_row(name, data, kind):
        coeff = sorted((j, value) for j, value in data.items() if value)
        rows.append({"name": name, "kind": kind, "coefficients": coeff})

    def add_member(data, group, member, weight):
        for state, col in group.columns.items():
            if state[member]:
                data[col] += weight

    def member_mass(group, member):
        return sum((mass * state[member] for state, mass in zip(STATES, group.rho)), F())

    for family in ("B2", "B3", "B4", "Mroot"):
        count_before = len(descriptors)
        rows_before = len(rows)
        tail_budgets = {(orbit, member): defaultdict(F) for orbit in ORBITS for member in (0, 1)}
        z_budgets = {(orbit, xi): defaultdict(F) for orbit in ORBITS
                     for xi in range(len(point.labels[family]))}

        # Each orbital terminal query pays the same one true new terminal.
        for states in point.family_states[family].values():
            for state in states:
                for budget in tail_budgets.values():
                    budget[state.column] += state.terminal_payoff

        tail_variable_count = 0
        reverse_variable_count = 0
        load_ranges = {}
        for hi, h in point.hist.items():
            states = point.family_states[family][hi]
            prefix4 = sum(map(int, h["actual_bits"][:4]))
            minload = min(state.terminal_denom - 1 for state in states)
            maxload = max(state.terminal_denom - 1 for state in states)
            load_ranges[hi] = (minload, maxload)
            high_masses = {k: sum((state.mass for state in states if state.terminal_denom > k), F())
                           for k in range(minload + 1, maxload + 1)}
            theme_masses = [sum((state.mass * state.members[xi] for state in states), F())
                            for xi in range(len(point.labels[family]))]
            for gi, group in enumerate(point.groups[hi]):
                # New terminal -> R or Z.  Outside the actual load range,
                # positive parts are identically zero or exactly q; absorb
                # the latter into the base coefficient 1/(maxload+1).
                for member in (0, 1):
                    q = member_mass(group, member)
                    budget = tail_budgets[group.orbit, member]
                    add_member(budget, group, member, -group.omega / (maxload + 1))
                    for k in range(minload + 1, maxload + 1):
                        variable = add_variable(
                            {"kind": "terminal-query-positive-part", "family": family,
                             "hist_column": hi, "group": group.key,
                             "member": "R" if member == 0 else "Z", "threshold": k},
                            max(F(), q - high_masses[k]))
                        threshold_row = defaultdict(F)
                        threshold_row[variable] = F(1)
                        add_member(threshold_row, group, member, -F(1))
                        for state in states:
                            if state.terminal_denom > k:
                                threshold_row[state.column] += 1
                        add_row(f"tail-threshold:{family}:{hi}:{gi}:{member}:{k}",
                                threshold_row, "tail-threshold")
                        budget[variable] -= group.omega / (k * (k + 1))
                        tail_variable_count += 1

                # Old Z -> any named new theme / the mean Y menu theme.
                r_mass = member_mass(group, 0)
                for xi, label in enumerate(point.labels[family]):
                    budget = z_budgets[group.orbit, xi]
                    for state, column in group.columns.items():
                        r, z = state
                        budget[column] += group.omega * F(z, prefix4 + r + 1)
                    for state in states:
                        budget[state.column] -= group.omega * state.members[xi] / (prefix4 + 2)
                    variable = add_variable(
                        {"kind": "reverse-Z-query-positive-part", "family": family,
                         "hist_column": hi, "group": group.key, "theme": label},
                        max(F(), theme_masses[xi] - r_mass))
                    threshold_row = defaultdict(F)
                    threshold_row[variable] = F(1)
                    add_member(threshold_row, group, 0, F(1))
                    for state in states:
                        threshold_row[state.column] -= state.members[xi]
                    add_row(f"Z-threshold:{family}:{hi}:{gi}:{label}", threshold_row, "Z-threshold")
                    budget[variable] -= group.omega / ((prefix4 + 1) * (prefix4 + 2))
                    reverse_variable_count += 1

        for (orbit, member), budget in tail_budgets.items():
            add_row(f"tail-budget:{family}:{orbit}:{'R' if member == 0 else 'Z'}", budget, "tail-budget")
        for (orbit, xi), budget in z_budgets.items():
            add_row(f"Z-budget:{family}:{orbit}:{point.labels[family][xi]}", budget, "Z-budget")
        family_counts[family] = {
            "old_groups": sum(len(groups) for groups in point.groups.values()),
            "tail_positive_parts": tail_variable_count,
            "reverse_Z_positive_parts": reverse_variable_count,
            "added_variables": len(descriptors) - count_before,
            "threshold_rows": tail_variable_count + reverse_variable_count,
            "tail_budget_rows": len(tail_budgets), "reverse_Z_budget_rows": len(z_budgets),
            "added_rows": len(rows) - rows_before, "load_ranges": load_ranges}

    full = point.mass + new_values
    values = []
    budget_values = []
    for row in rows:
        value = sum((coefficient * full[j] for j, coefficient in row["coefficients"]), F())
        values.append(value)
        if row["kind"].endswith("threshold"):
            assert value >= 0
        else:
            budget_values.append({"name": row["name"], "value": value})
    stats = {
        "base_columns": base_n, "hist_count": len(point.hist),
        "group_count": sum(len(groups) for groups in point.groups.values()),
        "added_columns": len(descriptors), "extended_columns": len(full),
        "added_rows": len(rows), "nonzero_coefficients": sum(len(row["coefficients"]) for row in rows),
        "threshold_rows": sum(row["kind"].endswith("threshold") for row in rows),
        "budget_rows": len(budget_values),
        "negative_canonical_budget_rows": sum(row["value"] < 0 for row in budget_values),
        "minimum_canonical_slack": min(values),
        "families": family_counts}
    assert len(budget_values) == 81
    if len(point.hist) == 16 and stats["group_count"] == 194:
        assert stats["added_columns"] == 7954
        assert stats["added_rows"] == 8035
        assert stats["threshold_rows"] == 7954
    return {
        "scope": "exact finite extension for 81 separate terminal-query minima; not joint transport or SPE",
        "input_point": str(point.filename.resolve()),
        "input_sha256": hashlib.sha256(point.raw).hexdigest(),
        "base_column_metadata_sha256": metadata_sha(point.columns),
        "convention": "every sparse row is dot(coefficients, extended nonnegative variables) >= 0",
        "stats": stats,
        "new_columns": descriptors,
        "rows": rows,
        "canonical_extension_at_input": {
            "new_weights": new_values,
            "budget_rows": budget_values,
            "warning": "all threshold rows hold; negative budgets correctly indicate that input has no epigraph completion"}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("point", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    point = Point(args.point)
    report = build(point)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(serial(report), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(serial(report["stats"]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

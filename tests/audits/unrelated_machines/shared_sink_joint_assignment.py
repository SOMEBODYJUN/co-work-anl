#!/usr/bin/env python3
"""共享汇点与宏任务共同匹配：精确有理算法及有限独立枚举审计。

Contract: machines 0,...,H-1 are homes and machine H is the sole sink.
Each tiny is (home, home_time, sink_time), with None denoting infinity;
at least one endpoint must be finite.  Each macro is an H-entry row, may
use homes only, and every finite time must be strictly greater than T/2.
No upper size bound is imposed on tiny jobs.  Times are nonnegative
Fraction-compatible rationals.  eta lies in (0,1].

solve_shared_sink returns a concrete assignment with every home <= T and
the sink <= (1+eta)T, or status REJECT_TARGET.  Every rejection implies
OPT > T for the stated class.  Success need not imply OPT <= T.  With
T=0, zero feasibility is decided exactly.  Invalid contracts raise
ValueError.  Runtime is polynomial in input bit length and numeric 1/eta;
the elementary covering DP uses O(q^4/eta) rational operations per home
option.  Matching uses exact integer-scaled costs and Hungarian updates.

Audit oracles below enumerate actual assignments and subsets, not the
DP recurrence.  They certify only the explicitly reported finite tests.
Default stdout is a fresh JSON report; no frozen evidence is overwritten.
"""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import json
import platform
import random


def _fraction(value):
    if isinstance(value, (float, bool)):
        raise ValueError("floats and booleans are not exact rational inputs")
    answer = F(value)
    if answer < 0:
        raise ValueError("negative time")
    return answer


def covering_fptas(items, requirement, eta):
    """Return (true cost, selected labels), or None if no cover exists.

    items are (nonnegative coverage, nonnegative cost, unique label).
    The returned cover has cost <= (1+eta) times the exact minimum,
    covers the original rational requirement exactly, and preserves zero
    optimum exactly.  It does not round the coverage constraint.
    """
    eta = _fraction(eta)
    if not 0 < eta <= 1:
        raise ValueError("eta must lie in (0,1]")
    if isinstance(requirement, (float, bool)):
        raise ValueError("supply an exact rational covering requirement")
    requirement = F(requirement)
    items = [(_fraction(a), _fraction(c), label) for a, c, label in items]
    if requirement <= 0:
        return F(0), ()
    free = [(a, c, label) for a, c, label in items if c == 0]
    free_labels = tuple(label for _, _, label in free)
    remaining = requirement - sum((a for a, _, _ in free), F(0))
    if remaining <= 0:
        return F(0), free_labels
    positive = [(a, c, label) for a, c, label in items if c > 0 and a > 0]
    if sum((a for a, _, _ in positive), F(0)) < remaining:
        return None
    q = len(positive)
    best = None
    for largest in sorted({c for _, c, _ in positive}):
        allowed = [(a, c, label) for a, c, label in positive if c <= largest]
        if sum((a for a, _, _ in allowed), F(0)) < remaining:
            continue
        delta = eta * largest / q
        scaled = [(a, int(c // delta), label) for a, c, label in allowed]
        bound = sum(w for _, w, _ in scaled)
        # Every cell is (maximal exact covered amount, subset bit mask).
        # A separate layer prevents reusing an item of rounded cost zero.
        dp = [None] * (bound + 1)
        dp[0] = (F(0), 0)
        for j, (amount, weight, _) in enumerate(scaled):
            nxt = dp[:]
            for used, old in enumerate(dp):
                if old is None or used + weight > bound:
                    continue
                amount_new = min(remaining, old[0] + amount)
                slot = used + weight
                if nxt[slot] is None or amount_new > nxt[slot][0]:
                    nxt[slot] = (amount_new, old[1] | (1 << j))
            dp = nxt
        for record in dp:
            if record is not None and record[0] >= remaining:
                chosen = [j for j in range(len(scaled)) if record[1] >> j & 1]
                cost = sum((allowed[j][1] for j in chosen), F(0))
                labels = free_labels + tuple(allowed[j][2] for j in chosen)
                if best is None or cost < best[0]:
                    best = cost, labels
                break
    assert best is not None
    return best


def minimum_assignment(costs):
    """Exact min-cost perfect matching; forbidden edges are None.

    All rational denominators are first cleared by their product, whose
    bit length is bounded by the sum of input denominator bit lengths.
    The Hungarian algorithm then uses integers only.  A forbidden edge
    gets a cost greater than every all-finite matching's possible cost.
    Return row -> column, or None if no finite perfect matching exists.
    """
    n = len(costs)
    if any(len(row) != n for row in costs):
        raise ValueError("assignment matrix must be square")
    if n == 0:
        return []
    finite = [_fraction(c) for row in costs for c in row if c is not None]
    denominator = 1
    for c in finite:
        denominator *= c.denominator
    integer = [[None if c is None else int(F(c) * denominator) for c in row]
               for row in costs]
    maximum = max((c for row in integer for c in row if c is not None), default=0)
    forbidden = n * maximum + 1
    matrix = [[forbidden if c is None else c for c in row] for row in integer]
    u, v, matched_row, way = [0] * (n + 1), [0] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    for row in range(1, n + 1):
        matched_row[0] = row
        column = 0
        slack = [None] * (n + 1)
        used = [False] * (n + 1)
        while True:
            used[column] = True
            active_row = matched_row[column]
            change = next_column = None
            for target in range(1, n + 1):
                if used[target]:
                    continue
                reduced = matrix[active_row - 1][target - 1] - u[active_row] - v[target]
                if slack[target] is None or reduced < slack[target]:
                    slack[target], way[target] = reduced, column
                if change is None or slack[target] < change:
                    change, next_column = slack[target], target
            assert change is not None
            for target in range(n + 1):
                if used[target]:
                    u[matched_row[target]] += change
                    v[target] -= change
                elif slack[target] is not None:
                    slack[target] -= change
            column = next_column
            if matched_row[column] == 0:
                break
        while column:
            previous = way[column]
            matched_row[column] = matched_row[previous]
            column = previous
    assignment = [None] * n
    for column in range(1, n + 1):
        assignment[matched_row[column] - 1] = column - 1
    if any(costs[row][assignment[row]] is None for row in range(n)):
        return None
    return assignment


def _normalize(home_count, macros, tinies, target, eta):
    if type(home_count) is not int or home_count < 0:
        raise ValueError("home_count must be a nonnegative integer")
    target, eta = _fraction(target), _fraction(eta)
    if not 0 < eta <= 1:
        raise ValueError("eta must lie in (0,1]")
    matrix = []
    for row in macros:
        if len(row) != home_count:
            raise ValueError("macro row has the wrong length")
        row = [None if p is None else _fraction(p) for p in row]
        if not any(p is not None for p in row):
            raise ValueError("macro has no available home")
        if any(p is not None and p <= target / 2 for p in row):
            raise ValueError("every finite macro time must be strictly greater than T/2")
        matrix.append(row)
    jobs = []
    for home, a, c in tinies:
        if type(home) is not int or not 0 <= home < home_count:
            raise ValueError("tiny has an invalid home")
        a = None if a is None else _fraction(a)
        c = None if c is None else _fraction(c)
        if a is None and c is None:
            raise ValueError("tiny has no available endpoint")
        jobs.append((home, a, c))
    return matrix, jobs, target, eta


def solve_shared_sink(home_count, macros, tinies, target, eta):
    """Return a certified actual schedule or a sound REJECT_TARGET.

    The assignment list gives macros first, then tinies, in input order.
    The sink machine has index home_count.  On success loads are exact
    Fractions.  Preprocessing does not silently delete or change domains.
    """
    macros, tinies, target, eta = _normalize(home_count, macros, tinies, target, eta)
    sink, macro_count = home_count, len(macros)

    def finish(assignment):
        loads = [F(0)] * (home_count + 1)
        for j, row in enumerate(macros):
            loads[assignment[j]] += row[assignment[j]]
        for j, (home, a, c) in enumerate(tinies, macro_count):
            machine = assignment[j]
            loads[machine] += a if machine == home else c
        assert all(load <= target for load in loads[:home_count])
        if loads[sink] > (1 + eta) * target:
            return {"status": "REJECT_TARGET", "reason": "approximate sink minimum exceeds augmented target"}
        return {"status": "SCHEDULE", "assignment": assignment, "loads": loads,
                "sink_load": loads[sink], "makespan": max(loads, default=F(0))}

    # Preserve an actual zero optimum even if the caller supplied T > 0.
    zero_assignment = []
    if not macros:
        for home, a, c in tinies:
            if a == 0:
                zero_assignment.append(home)
            elif c == 0:
                zero_assignment.append(sink)
            else:
                break
        else:
            return finish(zero_assignment)
    if target == 0:
        return {"status": "REJECT_TARGET", "reason": "some job has no zero endpoint"}
    if macro_count > home_count:
        return {"status": "REJECT_TARGET", "reason": "more macro jobs than homes"}

    mandatory_home = [F(0)] * home_count
    mandatory_sink = F(0)
    optional = [[] for _ in range(home_count)]
    tiny_default = []
    for label, (home, a, c) in enumerate(tinies):
        if c is None:
            mandatory_home[home] += a
            tiny_default.append(home)
        elif a is None:
            mandatory_sink += c
            tiny_default.append(sink)
        else:
            optional[home].append((a, c, label))
            tiny_default.append(home)
    if mandatory_sink > target:
        return {"status": "REJECT_TARGET", "reason": "mandatory sink load exceeds target"}

    def option(home, macro_time):
        if macro_time is None or mandatory_home[home] + macro_time > target:
            return None
        items = optional[home]
        requirement = mandatory_home[home] + macro_time + sum((a for a, _, _ in items), F(0)) - target
        return covering_fptas(items, requirement, eta)

    # One dummy per empty home is essential: empty homes also generate
    # sink load and cannot be omitted from the objective.
    witnesses = [[option(h, macros[j][h]) for h in range(home_count)]
                 for j in range(macro_count)]
    dummy_row = [option(h, F(0)) for h in range(home_count)]
    witnesses += [dummy_row[:] for _ in range(home_count - macro_count)]
    costs = [[None if witness is None else witness[0] for witness in row] for row in witnesses]
    matching = minimum_assignment(costs)
    if matching is None:
        return {"status": "REJECT_TARGET", "reason": "no home-feasible macro matching"}
    assignment = matching[:macro_count] + tiny_default
    for row, home in enumerate(matching):
        for label in witnesses[row][home][1]:
            assignment[macro_count + label] = sink
    return finish(assignment)


def enumerate_cover(items, requirement):
    best = None
    for bits in product((0, 1), repeat=len(items)):
        if sum((a for bit, (a, _, _) in zip(bits, items) if bit), F(0)) >= requirement:
            cost = sum((c for bit, (_, c, _) in zip(bits, items) if bit), F(0))
            if best is None or cost < best:
                best = cost
    return best


def enumerate_schedules(home_count, macros, tinies, target):
    """Independent actual-assignment oracle; no covering/matching calls."""
    choices = [[h for h, p in enumerate(row) if p is not None] for row in macros]
    choices += [[machine for machine, time in ((home, a), (home_count, c)) if time is not None]
                for home, a, c in tinies]
    optimum = sink_minimum = None
    checked = 0
    for assignment in product(*choices):
        checked += 1
        loads = [F(0)] * (home_count + 1)
        for j, row in enumerate(macros):
            loads[assignment[j]] += row[assignment[j]]
        for j, (home, a, c) in enumerate(tinies, len(macros)):
            machine = assignment[j]
            loads[machine] += a if machine == home else c
        value = max(loads, default=F(0))
        optimum = value if optimum is None else min(optimum, value)
        if all(load <= target for load in loads[:home_count]):
            sink_minimum = loads[-1] if sink_minimum is None else min(sink_minimum, loads[-1])
    return optimum, sink_minimum, checked


def _check_solution(home_count, macros, tinies, target, eta, result):
    optimum, sink_minimum, checked = enumerate_schedules(home_count, macros, tinies, target)
    if result["status"] == "REJECT_TARGET":
        assert optimum > target, ("unsound rejection", home_count, macros, tinies, result, optimum)
        return checked, optimum <= target, False
    assignment = result["assignment"]
    assert len(assignment) == len(macros) + len(tinies)
    loads = [F(0)] * (home_count + 1)
    for j, row in enumerate(macros):
        assert 0 <= assignment[j] < home_count and row[assignment[j]] is not None
        loads[assignment[j]] += row[assignment[j]]
    for j, (home, a, c) in enumerate(tinies, len(macros)):
        assert assignment[j] in (home, home_count)
        time = a if assignment[j] == home else c
        assert time is not None
        loads[assignment[j]] += time
    assert loads == result["loads"]
    assert all(value <= target for value in loads[:home_count])
    assert loads[-1] <= (1 + eta) * target
    assert sink_minimum is not None and loads[-1] <= (1 + eta) * sink_minimum
    if optimum == 0:
        assert result["makespan"] == 0
    return checked, optimum <= target, True


def audit(seed=2026101609):
    rng = random.Random(seed)
    eta_values = [F(1, 10), F(1, 3), F(1)]
    cover_count = matching_count = assignment_count = promised = successes = 0
    for _ in range(500):
        count = rng.randrange(9)
        items = [(F(rng.randrange(8), rng.randrange(1, 8)),
                  F(rng.randrange(8), rng.randrange(1, 8)), j) for j in range(count)]
        requirement = F(rng.randrange(15), rng.randrange(1, 8))
        eta = rng.choice(eta_values)
        exact = enumerate_cover(items, requirement)
        computed = covering_fptas(items, requirement, eta)
        assert (computed is None) == (exact is None)
        if computed is not None:
            assert len(computed[1]) == len(set(computed[1]))
            assert sum((items[j][0] for j in computed[1]), F(0)) >= requirement
            assert computed[0] == sum((items[j][1] for j in computed[1]), F(0))
            assert exact <= computed[0] <= (1 + eta) * exact
        cover_count += 1
    for _ in range(200):
        size = rng.randrange(7)
        costs = [[None if rng.randrange(4) == 0 else F(rng.randrange(9), rng.randrange(1, 11))
                  for _ in range(size)] for _ in range(size)]
        computed = minimum_assignment(costs)
        values = [sum((costs[row][perm[row]] for row in range(size)), F(0))
                  for perm in permutations(range(size))
                  if all(costs[row][perm[row]] is not None for row in range(size))]
        assert (computed is None) == (not values)
        if computed is not None:
            assert len(set(computed)) == size
            assert sum((costs[row][computed[row]] for row in range(size)), F(0)) == min(values)
        matching_count += 1
    small_times = [None, F(0), F(1, 11), F(1, 2), F(2, 3), F(1), F(3, 2)]
    for _ in range(600):
        homes = rng.randrange(1, 5)
        macro_count = rng.randrange(homes + 2)
        macros = []
        for _ in range(macro_count):
            row = [rng.choice([None, F(3, 5), F(2, 3), F(1), F(6, 5)]) for _ in range(homes)]
            if all(time is None for time in row):
                row[rng.randrange(homes)] = F(1)
            macros.append(row)
        tinies = []
        for _ in range(rng.randrange(7)):
            home = rng.randrange(homes)
            a, c = rng.choice(small_times), rng.choice(small_times)
            if a is None and c is None:
                a = F(0)
            tinies.append((home, a, c))
        eta = rng.choice(eta_values)
        result = solve_shared_sink(homes, macros, tinies, F(1), eta)
        checked, promise, success = _check_solution(homes, macros, tinies, F(1), eta, result)
        assignment_count += checked
        promised += promise
        successes += success
    huge = 2 ** 4096 + 1
    boundary_cases = [
        ("sink_only_empty", 0, [], [], F(0), F(1, 10)),
        ("empty_with_homes", 3, [], [], F(1), F(1, 10)),
        ("zero_endpoints", 2, [], [(0, F(0), F(7)), (1, F(8), F(0)), (0, None, F(0))], F(0), F(1, 10)),
        ("positive_zero_target", 1, [], [(0, F(1), F(1))], F(0), F(1, 10)),
        ("macro_zero_target", 1, [[F(1)]], [], F(0), F(1, 10)),
        ("home_only_tiny", 1, [], [(0, F(1), None)], F(1), F(1, 10)),
        ("sink_only_tiny", 1, [], [(0, None, F(1))], F(1), F(1, 10)),
        ("infeasible_mandatory_home", 1, [], [(0, F(2), None)], F(1), F(1, 10)),
        ("infeasible_mandatory_sink", 1, [], [(0, None, F(2))], F(1), F(1, 10)),
        ("macro_edge_above_target", 2, [[F(2), F(1)]], [(1, F(1), F(1))], F(1), F(1, 10)),
        ("large_tiny_requires_cover", 1, [[F(2, 3)]], [(0, F(1000), F(1))], F(1), F(1, 10)),
        ("huge_rational_denominator", 2, [[F(huge + 1, 2 * huge), F(1)]],
         [(0, F(huge - 1, 2 * huge), F(1, huge)), (1, None, F(1, huge))], F(1), F(1, 10)),
        ("zero_cost_cover", 1, [[F(1)]], [(0, F(1), F(0)), (0, F(0), F(9))], F(1), F(1, 10)),
        ("dummy_cost_is_essential", 2, [[F(1), F(1)]],
         [(0, F(3, 2), F(1)), (1, F(1, 2), F(1, 10))], F(1), F(1, 10)),
    ]
    boundary = []
    for name, homes, macros, tinies, target, eta in boundary_cases:
        result = solve_shared_sink(homes, macros, tinies, target, eta)
        checked, promise, success = _check_solution(homes, macros, tinies, target, eta, result)
        assignment_count += checked
        boundary.append({"name": name, "status": result["status"], "promise": promise,
                         "loads": [str(x) for x in result.get("loads", [])], "assignments_enumerated": checked})
    invalid_cases = [
        (1, [[F(1, 2)]], [], F(1), F(1, 10)),
        (1, [], [(0, None, None)], F(1), F(1, 10)),
        (1, [], [(1, F(0), F(0))], F(1), F(1, 10)),
        (1, [], [], F(1), F(0)),
        (True, [], [], F(1), F(1, 10)),
        (1, [], [(False, F(0), F(0))], F(1), F(1, 10)),
        (1, [], [(0, True, F(0))], F(1), F(1, 10)),
        (1, [], [], True, F(1, 10)),
        (1, [], [], F(1), True),
        (1, [], [], F(1), 0.1),
    ]
    for args in invalid_cases:
        try:
            solve_shared_sink(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid contract accepted")
    return {"status": "passed", "seed": seed, "python": platform.python_version(),
            "arithmetic": "Fraction throughout; integer Hungarian after exact denominator clearing",
            "source_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
            "cover_subset_oracle_cases": cover_count, "matching_permutation_oracle_cases": matching_count,
            "random_actual_schedule_cases": 600, "random_promised_cases": promised,
            "random_successes": successes, "actual_assignments_enumerated_including_boundaries": assignment_count,
            "invalid_contract_cases": len(invalid_cases), "boundary_cases": boundary,
            "scope": "Finite independent subset/permutation/actual-assignment checks; not a general proof or novelty certification."}


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))

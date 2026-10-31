"""Exact finite audit for the fixed-arity overload witness filter.

The triple capacity flow is fully implemented.  The general filter's exact
rational LP backend is not implemented: ``round_big_certificate`` receives,
validates and rounds an explicit feasible certificate for the big-only LP.
No floating point, relaxed load estimate or partial schedule is accepted.
"""

from collections import defaultdict, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import random


def rational(value):
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise ValueError("only exact integers/Fractions are accepted")
    return F(value)


def check_input(P, T):
    T = rational(T)
    if T < 0 or not isinstance(P, list) or not P:
        raise ValueError("nonnegative T and at least one explicit row required")
    n = len(P[0])
    if any(len(row) != n for row in P):
        raise ValueError("matrix is not rectangular")
    Q = []
    for row in P:
        qrow = []
        for p in row:
            qrow.append(None if p is None else rational(p))
            if qrow[-1] is not None and qrow[-1] < 0:
                raise ValueError("negative processing time")
        Q.append(qrow)
    if any(all(Q[i][j] is None for i in range(len(Q))) for j in range(n)):
        raise ValueError("every original job needs a finite endpoint")
    return Q, T, n


def positive_int(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("r must be a positive integer")
    return value


def slack(r):
    positive_int(r)
    if r == 1:
        return F(1)
    if r == 2:
        return F(1, 2)
    answer = F(1, 6)
    for k in range(4, r + 1):
        answer **= k - 1
    return answer


def ceil_fraction(q):
    return -(-q.numerator // q.denominator)


def loads(P, sigma):
    n = len(P[0])
    if len(sigma) != n:
        raise AssertionError("output does not contain all original jobs")
    L = [F(0) for _ in P]
    values = [[] for _ in P]
    for j, i in enumerate(sigma):
        if not isinstance(i, int) or not 0 <= i < len(P) or P[i][j] is None:
            raise AssertionError("output uses a non-original endpoint")
        L[i] += P[i][j]
        values[i].append(P[i][j])
    return L, values


def b_r(P, sigma, r):
    _, values = loads(P, sigma)
    return max((sum(sorted(row, reverse=True)[:r], F(0)) for row in values), default=F(0))


def exact_opt(P, top=None):
    n = len(P[0])
    domains = [[i for i in range(len(P)) if P[i][j] is not None] for j in range(n)]
    optimum = None
    attaining = None
    count = 0
    for sigma in product(*domains):
        count += 1
        value = max(loads(P, sigma)[0], default=F(0)) if top is None else b_r(P, sigma, top)
        if optimum is None or value < optimum:
            optimum, attaining = value, sigma
    return optimum, attaining, count


class IntegralFlow:
    def __init__(self):
        self.adj = defaultdict(list)
        self.cap = {}

    def add(self, u, v, capacity):
        if (u, v) in self.cap or (v, u) in self.cap:
            raise ValueError("parallel flow arcs are not used in this audit")
        self.adj[u].append(v)
        self.adj[v].append(u)
        self.cap[u, v] = capacity
        self.cap[v, u] = 0

    def run(self, source, sink):
        value = 0
        while True:
            prev = {source: None}
            queue = deque([source])
            while queue and sink not in prev:
                u = queue.popleft()
                for v in self.adj[u]:
                    if v not in prev and self.cap[u, v] > 0:
                        prev[v] = u
                        queue.append(v)
            if sink not in prev:
                return value
            bottleneck = None
            v = sink
            while prev[v] is not None:
                u = prev[v]
                bottleneck = self.cap[u, v] if bottleneck is None else min(bottleneck, self.cap[u, v])
                v = u
            v = sink
            while prev[v] is not None:
                u = prev[v]
                self.cap[u, v] -= bottleneck
                self.cap[v, u] += bottleneck
                v = u
            value += bottleneck


def triple_filter(P, T):
    P, T, n = check_input(P, T)
    if n == 0:
        return []
    if T == 0:
        sigma = []
        for j in range(n):
            zeros = [i for i in range(len(P)) if P[i][j] == 0]
            if not zeros:
                return None
            sigma.append(zeros[0])
        return sigma
    net = IntegralFlow()
    source, sink = ("source",), ("sink",)
    for j in range(n):
        net.add(source, ("job", j), 1)
    for i in range(len(P)):
        for s in (1, 2, 3):
            slot = ("machine", i, s)
            net.add(slot, sink, n if s == 3 else 1)
            for j in range(n):
                if P[i][j] is not None and s * P[i][j] <= T:
                    net.add(("job", j), slot, 1)
    if net.run(source, sink) != n:
        return None
    sigma = []
    for j in range(n):
        destinations = [v[1] for v in net.adj[("job", j)]
                        if v[0] == "machine" and net.cap[v, ("job", j)] == 1]
        assert len(destinations) == 1
        sigma.append(destinations[0])
    assert all(P[i][j] <= T for j, i in enumerate(sigma))
    assert b_r(P, sigma, 3) <= F(11, 6) * T
    return sigma


def sorted_slots(P, x):
    """Exact positive-overlap slots, with the full original job identities."""
    slots = []
    adjacency = [[] for _ in P[0]]
    envelopes = []
    for i, row in enumerate(P):
        jobs = sorted((j for j in range(len(row)) if x.get((i, j), 0) > 0),
                      key=lambda j: (-row[j], j))
        total = sum((x[i, j] for j in jobs), F(0))
        local = []
        for k in range(ceil_fraction(total)):
            local.append(len(slots))
            slots.append((i, k))
        position = F(0)
        maxima = [F(0) for _ in local]
        for j in jobs:
            end = position + x[i, j]
            for k, index in enumerate(local):
                overlap = min(end, F(k + 1)) - max(position, F(k))
                if overlap > 0:
                    adjacency[j].append(index)
                    maxima[k] = max(maxima[k], row[j])
            position = end
        envelopes.append(maxima)
    return slots, adjacency, envelopes


def match_slots(slots, adjacency):
    owner = {}

    def augment(j, seen):
        for s in adjacency[j]:
            if s in seen:
                continue
            seen.add(s)
            if s not in owner or augment(owner[s], seen):
                owner[s] = j
                return True
        return False

    for j in range(len(adjacency)):
        assert augment(j, set()), "Hall must hold for every validated certificate"
    sigma = [None] * len(adjacency)
    for s, j in owner.items():
        sigma[j] = slots[s][0]
    assert all(i is not None for i in sigma)
    return sigma


def round_big_certificate(P, T, r, rows, tiny):
    """Validate equations (8) exactly, then round their full x projection.

    rows[i] is [(positive rational weight, tuple of original big job IDs),...].
    tiny is {(original machine ID, original job ID): rational mass}.
    """
    P, T, n = check_input(P, T)
    positive_int(r)
    if r < 4 or T <= 0:
        raise ValueError("this certificate API covers r>=4,T>0")
    delta = slack(r - 1) / (2 * r)
    if len(rows) != len(P):
        raise ValueError("one explicit distribution per machine required")
    x = defaultdict(F)
    for i, distribution in enumerate(rows):
        normalization = F(0)
        for weight, C in distribution:
            weight = rational(weight)
            if weight <= 0 or len(set(C)) != len(C):
                raise ValueError("positive weights and distinct original jobs required")
            normalization += weight
            for j in C:
                if not isinstance(j, int) or not 0 <= j < n:
                    raise ValueError("configuration changes job identities")
                if P[i][j] is None or not delta * T < P[i][j] <= T:
                    raise ValueError("configuration contains non-big or unavailable edge")
                x[i, j] += weight
            if sum((P[i][j] for j in C), F(0)) > T:
                raise ValueError("configuration is not a real local schedule")
        if normalization != 1:
            raise ValueError("configuration distribution is not normalized")
    for (i, j), weight in tiny.items():
        weight = rational(weight)
        if not 0 <= i < len(P) or not 0 <= j < n or weight < 0:
            raise ValueError("invalid tiny endpoint or mass")
        if P[i][j] is None or not 0 <= P[i][j] <= delta * T:
            raise ValueError("tiny mass on a non-tiny or unavailable endpoint")
        x[i, j] += weight
    for j in range(n):
        if sum((x[i, j] for i in range(len(P))), F(0)) != 1:
            raise ValueError("original job is not covered exactly once")
    slots, adjacency, maxima = sorted_slots(P, x)
    sigma = match_slots(slots, adjacency)
    for i in range(len(P)):
        assert sum(maxima[i][:r], F(0)) <= (2 - slack(r)) * T
    assert b_r(P, sigma, r) <= (2 - slack(r)) * T
    assert all(P[i][j] <= T for j, i in enumerate(sigma))
    return sigma, maxima, x


def private_completion(sizes, configurations, r, extra_tiny=0):
    """Project a local CONFIG(1) into a full big-only certificate.

    Each center job has its own original time-1 private endpoint.  Jobs tiny
    at the center are deliberately sent to the center with mass 1, regardless
    of the supplied local distribution; this audits the missing-tiny branch.
    """
    delta = slack(r - 1) / (2 * r)
    sizes = list(sizes) + [delta] * extra_tiny
    n = len(sizes)
    P = [sizes] + [[F(1) if k == j else None for k in range(n)] for j in range(n)]
    center_rows = defaultdict(F)
    center_mass = defaultdict(F)
    for weight, C in configurations:
        assert sum((sizes[j] for j in C), F(0)) <= 1
        C = tuple(j for j in C if sizes[j] > delta)
        center_rows[C] += weight
        for j in C:
            center_mass[j] += weight
    rows = [[(w, C) for C, w in sorted(center_rows.items()) if w]]
    tiny = {}
    for j, size in enumerate(sizes):
        if size <= delta:
            tiny[0, j] = F(1)
            rows.append([(F(1), ())])
        else:
            mass = center_mass[j]
            private = []
            if 1 - mass:
                private.append((1 - mass, (j,)))
            if mass:
                private.append((mass, ()))
            rows.append(private)
    return P, rows, tiny


def all_row_distributions(values, max_jobs=4):
    """Finite exact local configurations and three-point distributions."""
    for n in range(1, max_jobs + 1):
        for sizes in product(values, repeat=n):
            configs = [C for k in range(n + 1) for C in combinations(range(n), k)
                       if sum((sizes[j] for j in C), F(0)) <= 1]
            # These finite distributions are test inputs, not vertex enumeration.
            chosen = configs[:2] + configs[-2:]
            for A in chosen:
                for B in chosen:
                    yield sizes, [(F(1, 3), A), (F(2, 3), B)]


def audit():
    report = {"arithmetic": "fractions.Fraction only", "seed": 20261019,
              "implemented": ["triple integer capacity flow", "given big-only certificate validation/rounding"],
              "not_implemented": ["general rational LP backend", "general makespan approximation"]}
    # Exact recurrence arithmetic, including large rational constants.
    for r in range(4, 9):
        D = 1 / slack(r - 1)
        assert D.denominator == 1 and D >= 6
        assert slack(r) == slack(r - 1) ** (r - 1)
        assert 1 / (D * (D + 1)) >= slack(r)
        delta = slack(r - 1) / (2 * r)
        for q in range(1, r):
            assert 2 - slack(q) + (r - q) * delta <= 2 - slack(r)
        assert r * delta <= 2 - slack(r)
    report["slacks"] = {str(r): str(slack(r)) for r in range(1, 6)}

    # Every actual schedule is enumerated on the small matrix family.
    values = [None, F(0), F(1, 3), F(1, 2), F(1)]
    matrices = schedules = successful_flows = failures = 0
    for n in range(1, 4):
        for entries in product(values, repeat=2 * n):
            P = [list(entries[:n]), list(entries[n:])]
            if any(P[0][j] is None and P[1][j] is None for j in range(n)):
                continue
            matrices += 1
            O, _, count = exact_opt(P)
            schedules += count
            for T in (F(0), F(1, 2), F(1)):
                sigma = triple_filter(P, T)
                if sigma is None:
                    failures += 1
                    assert O > T
                else:
                    successful_flows += 1
                    assert b_r(P, sigma, 3) <= F(11, 6) * T
    assert triple_filter([[]], F(0)) == []
    report["triple_full_matrix_oracle"] = {"machines": 2, "jobs": [1, 2, 3], "finite_palette": ["0", "1/3", "1/2", "1"],
        "unavailable": True, "targets": ["0", "1/2", "1"], "matrices": matrices, "actual_schedules": schedules,
        "successful_flows": successful_flows, "reliable_failures": failures}

    # Scope-sharpness of the *flow envelope*, on a full original matrix.
    sharp = [[F(1), F(1, 2), F(1, 3)], [F(1), None, None],
             [None, F(1), None], [None, None, F(1)]]
    O, _, count = exact_opt(sharp)
    assert O == 1 and b_r(sharp, [0, 0, 0], 3) == F(11, 6)
    report["triple_flow_envelope_attainment"] = {"actual_opt": str(O), "legal_bad_flow_sigma": [0, 0, 0],
        "B3": "11/6", "all_schedules_checked": count, "hardness_claim": False}

    # Universal row-prefix inequality on finite exact distributions.  This is
    # independent of the certificate projection and matching implementation.
    row_cases = 0
    for sizes, distribution in all_row_distributions([F(1, 7), F(1, 3), F(1, 2), F(1)], 4):
        x = defaultdict(F)
        for weight, C in distribution:
            for j in C:
                x[0, j] += weight
        _, _, maxima = sorted_slots([list(sizes)], x)
        for r in range(1, 8):
            assert sum(maxima[0][:r], F(0)) <= 2 - slack(r)
        row_cases += 1
    report["finite_local_row_distributions"] = row_cases

    rng = random.Random(20261019)
    full_certificates = 0
    q_classes = set()
    maximum_actual_total = F(0)
    for r in range(4, 8):
        for case in range(120):
            sizes = [F(1)] + [F(rng.randint(1, 6), rng.randint(7, 15)) for _ in range(rng.randint(3, 12))]
            available = list(range(len(sizes)))
            configurations = []
            weights = [rng.randint(1, 9) for _ in range(8)]
            W = sum(weights)
            for w in weights:
                rng.shuffle(available)
                C = []
                total = F(0)
                for j in available:
                    if total + sizes[j] <= 1 and rng.randint(0, 1):
                        C.append(j)
                        total += sizes[j]
                configurations.append((F(w, W), tuple(sorted(C))))
            P, rows, tiny = private_completion(sizes, configurations, r, extra_tiny=2 * r + case % 4)
            sigma, _, x = round_big_certificate(P, 1, r, rows, tiny)
            delta = slack(r - 1) / (2 * r)
            for i in range(len(P)):
                big_mass = sum((x[i, j] for j in range(len(P[0]))
                                if P[i][j] is not None and P[i][j] > delta), F(0))
                q = ceil_fraction(big_mass)
                q_classes.add((r, "zero" if q == 0 else "short" if q < r else "long"))
            maximum_actual_total = max(maximum_actual_total, max(loads(P, sigma)[0]))
            full_certificates += 1

        # A long-slot class with more positive-big jobs than the prefix arity.
        delta = slack(r - 1) / (2 * r)
        size = 2 * delta
        num = min(2 * r + 3, int(1 / size))
        sizes = [size] * num
        P, rows, tiny = private_completion(sizes, [(F(1), tuple(range(num)))], r, extra_tiny=r + 1)
        sigma, _, x = round_big_certificate(P, 1, r, rows, tiny)
        assert ceil_fraction(sum((x[0, j] for j in range(num)), F(0))) >= r
        q_classes.add((r, "long"))
        full_certificates += 1

    report["given_big_only_full_certificates"] = full_certificates
    report["big_slot_classes_covered"] = sorted([list(item) for item in q_classes])
    report["largest_actual_total_from_certificate_tests"] = str(maximum_actual_total)

    # Rejection tests prevent the certificate API from silently extending its
    # mathematical domain or accepting relaxed/partial outputs.
    rejected = 0
    P, rows, tiny = private_completion([F(1), F(1, 2)], [(F(1), (0,))], 4)
    mutations = [
        (P, rows[:-1], tiny),
        (P, [[(F(1, 2), ())]] + rows[1:], tiny),
        (P, [[(F(1), (0, 1))]] + rows[1:], tiny),
        (P, rows, {(0, 0): F(1)}),
    ]
    for badP, badrows, badtiny in mutations:
        try:
            round_big_certificate(badP, 1, 4, badrows, badtiny)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid certificate was accepted")
    for bad_r in (True, 0, F(4), 4.0):
        try:
            slack(bad_r)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("invalid arity was accepted")
    report["invalid_inputs_rejected"] = rejected

    # A fixed-r objective point does not justify the ordinary big-config LP.
    P = [[F(1, 4)] * 5]
    O, _, count = exact_opt(P)
    O4, _, _ = exact_opt(P, top=4)
    assert O == F(5, 4) and O4 == 1
    report["scope_counterexample"] = {"matrix": [["1/4"] * 5], "ordinary_opt": "5/4", "O4": "1",
        "reason_big_config_LP_at_T1_infeasible": "all five jobs have only the big endpoint; total expected work is 5/4>1",
        "actual_schedules_checked": count}

    # All bounded-size tuple constraints are exactly the B_r objective.
    tuple_tests = 0
    for k in range(5):
        for row in product([F(0), F(1, 3), F(2, 3), F(1)], repeat=k):
            for r in (1, 2, 3, 4):
                for threshold in (F(1), F(3, 2), F(11, 6)):
                    bad = any(sum(C, F(0)) > threshold for s in range(1, min(k, r) + 1) for C in combinations(row, s))
                    assert bad == (sum(sorted(row, reverse=True)[:r], F(0)) > threshold)
                    tuple_tests += 1
    report["tuple_CSP_equivalence_checks"] = tuple_tests
    report["status"] = "all exact finite audits passed; no universal proof is inferred from these tests"
    report["source_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    return report


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))

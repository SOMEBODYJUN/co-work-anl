"""Independent exact audit of the frozen shared R/Z income bridge.

Reads data only; does not import discovery or existing verification programs.
Reconstructs raw true-IC features, solves each of four two-state policies,
checks the displayed formulas and maps, and evaluates the exact 19662 point.
Only this directory receives output. No optimizer, Git, registry or RUN writes.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CROSS = REPO / "research/workspaces/six-boss2-20261111-cross"
DATA = CROSS / "coverage_bridge"
POINT = REPO / "research/workspaces/six-boss1-20261111/union_augmented_lp/augmented_lp_exact.json"
POINT_SHA = "b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3"
PACKAGE_SHA = "595e7386cfacc591f513fe477453e94d9e2271e4cb63ce3f5c57a8dc34fabd50"
BITS = tuple(product((0, 1), repeat=4))
WORDS = tuple(product((0, 1), repeat=3))
started = time.monotonic()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def clean(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [clean(v) for v in value]
    return value


def share(num, den):
    if not den:
        assert num == 0
        return Q(0)
    return Q(num, den)


package_path = DATA / "selected_prefix_tail_5752.json"
assert digest(package_path) == PACKAGE_SHA
package = json.loads(package_path.read_text())
PARAM = {}
for number, scale in ((2, 999), (13, 10000)):
    row = package["cuts"][number - 1]
    assert (row["source"], row["k"], Q(row["delta"])) == (4, 3, Q(1, 2))
    aa = {k.replace("@Bj", "@Cj"): scale * Q(v) for k, v in row["alpha"].items()}
    bb = {k: scale * Q(v) for k, v in row["beta"].items()}
    assert all(x >= 0 and x.denominator == 1 for x in (*aa.values(), *bb.values()))
    source = aa.get("sourceT", 0) + aa.get("sourceC", 0) + bb.get("source", 0)
    last = sum(v for k, v in aa.items() if k.startswith("price:"))
    last += bb.get("alpha_mid", 0) + bb.get("alpha_last", 0)
    assert [source, last, Q(0)] == [scale * Q(v) for v in row["budget"]]
    PARAM[number] = (aa, bb)


def prefix_raw(number, p, D, t, hidden, queries):
    """Directly sum the legal source, actual-price, last, and PAIR rows."""
    b, c, j, v = hidden
    z1, z2 = p + t + b + c, p + c + j + v
    members = {"t": Q(t), "b": Q(b), "c": Q(c), "j": Q(j), "v": Q(v)}
    total = Q(0)
    for name, weight in PARAM[number][0].items():
        if name == "sourceT":
            feature = share(t, z1)
        elif name == "sourceC":
            feature = share(c, z2)
        elif name.startswith("price:"):
            feature = members[name.split(":")[1]] / D
        else:
            main, *query = name.split("@")
            values = dict(members)
            if query:
                values["q"] = Q(queries[query[0]])
            family, which = main.split(":")
            if family == "last1":
                feature = values[which] / (p + t + b + 1) - share(c, z1)
            elif family == "last2":
                feature = values[which] / (p + c + j + 1) - share(v, z2)
            else:
                assert family in ("pair1", "pair2")
                x, y = (values[k] for k in which.split(","))
                background, first, last = (p + t, b, c) if family == "pair1" else (p + c, j, v)
                feature = (x + y) / (background + 1)
                feature -= (x * y + first) / ((background + 1) * (background + 2))
                feature -= share(first + last, background + first + last)
        total += weight * feature
    return total


QKEYS = ("Ti", "Tj", "Ci", "Cj", "A6", "other_T")


@lru_cache(None)
def affine_prefix(number, p, D, t, hidden):
    zeros = dict.fromkeys(QKEYS, Q(0))
    base = prefix_raw(number, p, D, t, hidden, zeros)
    coeffs = []
    for key in QKEYS:
        query = dict(zeros)
        query[key] = Q(1)
        coeffs.append(prefix_raw(number, p, D, t, hidden, query) - base)
    return base, tuple(coeffs)


def prefix(number, p, D, t, hidden, x, y, ci, cj, a6, n):
    base, coeffs = affine_prefix(number, p, D, t, hidden)
    query = (Q(x), Q(y), Q(ci), Q(cj), Q(a6), Q(n - x - y, 4))
    return base + sum((a * b for a, b in zip(coeffs, query)), Q(0))


def displayed_prefix(number, p, D, t, h, x, y, ci, cj, a6, n):
    b, c, j, v = h
    tau = Q(n - x - y, 4)
    if number == 2:
        q1, qp = 36 * x + 145 * ci + 36 * cj, 2 * a6 + 5 * x + 4 * cj + 13 * tau
        return (share(431 * t - 24 * b - 241 * c, p + t + b + c)
                + share(314 * c - j - 126 * v, p + c + j + v)
                + Q(2 * b + 64 * j + 63 * v, D)
                + Q(q1, p + t + b + 1) + (124 * b + tau) / (p + c + j + 1)
                + (qp + 24 * c) / (p + t + 1)
                - (qp * c + 24 * b) / ((p + t + 1) * (p + t + 2))
                + (tau + b) / (p + c + 1)
                - (tau * b + j) / ((p + c + 1) * (p + c + 2)))
    qq, uu = Q(103 * n + x + y, 4), Q(39 * n + x + y, 4)
    return (share(4325 * t - 2196 * c, p + t + b + c)
            + share(3187 * c - 59 * j - 1295 * v, p + c + j + v)
            + Q(630 * j + 624 * v, D)
            + Q(34 * j + 2162 * a6, p + t + b + 1)
            + (1081 * b + qq) / (p + c + j + 1)
            + (uu + 59 * v) / (p + c + 1)
            - (uu * v + 59 * j) / ((p + c + 1) * (p + c + 2)))


@lru_cache(None)
def tail(number, p, D, x, y, n):
    beta = PARAM[number][1]
    query = {"Ti": Q(x), "Tj": Q(y), "other_T": Q(n - x - y, 4)}
    a, m, ell = beta["source"], beta["alpha_mid"], beta["alpha_last"]
    total = sum(v for k, v in beta.items() if k.startswith("mu_"))
    qq = sum((v * query[k[3:]] for k, v in beta.items() if k.startswith("mu_")), Q(0))
    e = {}
    for t, c in product((0, 1), repeat=2):
        e[t, c] = min(share(a * t - total * c, p + t + s + c)
                      + (m * s + ell * c) / D + qq / (p + t + s + 1)
                      for s in (0, 1))
    closed = {(0, 0): min(qq / (p + 1), m / D + qq / (p + 2)),
              (0, 1): (qq - total) / (p + 1) + ell / D,
              (1, 0): a / (p + 2) + m / D + qq / (p + 3),
              (1, 1): (a - total + qq) / (p + 3) + (m + ell) / D}
    assert e == closed
    theta = Q(1, 2)
    candidates = [[], []]
    for c0, c1 in product((0, 1), repeat=2):
        # Solve V0=e0c0+theta*V_c0 and V1=e1c1+theta*V_c1.
        aa, bb = 1 - theta * (c0 == 0), -theta * (c0 == 1)
        cc, dd = -theta * (c1 == 0), 1 - theta * (c1 == 1)
        det = aa * dd - bb * cc
        candidates[0].append((dd * e[0, c0] - bb * e[1, c1]) / det)
        candidates[1].append((aa * e[1, c1] - cc * e[0, c0]) / det)
    values = tuple(min(v) for v in candidates)
    assert all(values[t] == min(e[t, c] + theta * values[c] for c in (0, 1)) for t in (0, 1))
    result = tuple((1 - theta) * v for v in values)
    displayed = (min(qq / (p + 1), m / D + qq / (p + 2),
                     (e[0, 1] + e[1, 1]) / 2, (2 * e[0, 1] + e[1, 0]) / 3),
                 min(e[1, 1], (e[1, 0] + qq / (p + 1)) / 2,
                     (e[1, 0] + m / D + qq / (p + 2)) / 2,
                     (2 * e[1, 0] + e[0, 1]) / 3))
    assert result == displayed
    return result


@lru_cache(None)
def L(number, p, D, t, x, y, ci, cj, a6, n):
    assert 0 <= n - x - y <= 4
    psi = tail(number, p, D, x, y, n)
    values = []
    for hidden in BITS:
        raw = prefix(number, p, D, t, hidden, x, y, ci, cj, a6, n)
        assert raw == displayed_prefix(number, p, D, t, hidden, x, y, ci, cj, a6, n)
        values.append(raw + psi[hidden[3]])
    return min(values)


def sum_values(sequence):
    return sum(sequence, Q(0))


def check_finite_tables():
    base = json.loads((DATA / "mainline_zero_capacity_v1.json").read_text())
    counts = {}
    for number, name in ((2, "cut2_complete_visible_table"), (13, "cut13_complete_visible_table")):
        count = 0
        for row in base[name]:
            p, D, a6, n = (row[k] for k in ("p", "d", "A6", "n"))
            if number == 2:
                x, y, ci, cj = (row[k] for k in ("x", "y", "Ci", "Bj"))
            else:
                r = row["r"]
                x, y, ci, cj = min(1, r), max(0, r - 1), 0, 0
            for t in (0, 1):
                assert L(number, p, D, t, x, y, ci, cj, a6, n) == Q(row["L"][t])
                count += 1
        counts[number] = count
    assert counts == {2: 3840, 13: 720}
    print("Raw-IC reconstruction: 3840 A values and 720 B values passed", flush=True)

    maxA, maxB, minR, minZ = Q(0), Q(0), None, None
    witnessesA, witnessesB = [], []
    types = 0
    for p in range(4):
        for a4, a5, a6, x, y, ci, cj in product((0, 1), repeat=7):
            for extra in range(5):
                n, D, P = x + y + extra, p + a4 + a5 + 1, p + a4
                av = tuple(L(2, p, D, t, x, y, ci, cj, a6, n) for t in (0, 1))
                bv = tuple(L(13, p, D, t, x, y, 0, 0, a6, n) for t in (0, 1))
                da, db = av[1] - av[0], bv[1] - bv[0]
                assert da > 0 and db > 0
                ra, rb = Q(n, 6 * (P + 1) * (P + 2)) / da, Q(1, P + 1) / db
                signature = (p, a4, a5, a6, x, y, ci, cj, n)
                if ra > maxA:
                    maxA, witnessesA = ra, [signature]
                elif ra == maxA:
                    witnessesA.append(signature)
                if rb > maxB:
                    maxB, witnessesB = rb, [signature]
                elif rb == maxB:
                    witnessesB.append(signature)
                mr = 49 * da - Q(17965 * n, 6 * (P + 1) * (P + 2))
                mz = 10 * db - Q(17965, P + 1)
                assert mr >= 0 and mz >= 0
                minR = mr if minR is None else min(minR, mr)
                minZ = mz if minZ is None else min(minZ, mz)
                full = min(49 * av[r] + 10 * bv[z] + Q(17965) * (Q(n, 6) - z) / (P + r + 1)
                           for r, z in product((0, 1), repeat=2))
                assert full == 49 * av[0] + 10 * bv[0] + Q(17965 * n, 6 * (P + 1))
                types += 1
    assert (types, maxA, maxB, minR, minZ) == (2560, Q(3, 1100), Q(2, 3593), Q(5, 6), Q(0))

    creditA, creditB, creditTotal = None, None, None
    credit_cases = 0
    for p in range(4):
        for D in range(p + 1, p + 4):
            for x, y, ci, cj in product((0, 1), repeat=4):
                for extra in range(5):
                    n = x + y + extra
                    da = L(2, p, D, 0, x, y, ci, cj, 1, n) - L(2, p, D, 0, x, y, ci, cj, 0, n)
                    db = L(13, p, D, 0, x, y, 0, 0, 1, n) - L(13, p, D, 0, x, y, 0, 0, 0, n)
                    assert da >= Q(2, p + 2) >= Q(1, D)
                    assert db >= Q(2162, D)
                    creditA = da * D if creditA is None else min(creditA, da * D)
                    creditB = db * D if creditB is None else min(creditB, db * D)
                    creditTotal = (49 * da + 10 * db) * D if creditTotal is None else min(creditTotal, (49 * da + 10 * db) * D)
                    credit_cases += 1
    assert (credit_cases, creditA, creditB, creditTotal) == (960, 1, 2162, 21669)

    map_reasons, map_gaps = Counter(), []
    for p in range(4):
        for D in range(p + 1, p + 4):
            for r in range(3):
                x, y = min(1, r), max(0, r - 1)
                for extra in range(5):
                    n = r + extra
                    for hidden in BITS:
                        b, c, j, v = hidden
                        if b == 0 or D >= p + 2:
                            mapped, reason = hidden, "same"
                        elif c == 1 or j == 0 or p >= 2:
                            mapped, reason = (0, c, j, v), "lower_b"
                        elif v:
                            mapped, reason = (0, 1, 1, 1), "exception_v1"
                        elif p == 1:
                            mapped, reason = (0, 1, 1, 0), "exception_p1_v0"
                        elif n:
                            mapped, reason = (0, 1, 1, 0), "exception_p0_positive_n"
                        else:
                            mapped, reason = (0, 0, 0, 0), "exception_zero_n"
                        assert mapped[3] == v
                        gap = prefix(13, p, D, 0, hidden, x, y, 0, 0, 1, n)
                        gap -= prefix(13, p, D, 0, mapped, x, y, 0, 0, 0, n) + Q(2162, D)
                        assert gap >= 0
                        map_reasons[reason] += 1
                        map_gaps.append(gap)
    assert len(map_gaps) == 2880 and min(map_gaps) == 0
    print("2560 four-state cases, 960 income differences, 2880 maps passed", flush=True)
    return dict(L_counts=counts, four_state_cases=types, alpha_per_lambda=maxA,
                beta_per_lambda=maxB, alpha_boundary_witnesses=witnessesA,
                beta_boundary_witnesses=witnessesB, fixed_min_R_margin=minR,
                fixed_min_Z_margin=minZ, income_credit_cases=credit_cases,
                income_credit_A=creditA, income_credit_B=creditB,
                income_credit_weighted=creditTotal, hidden_map_cases=len(map_gaps),
                hidden_map_reasons=dict(map_reasons), hidden_map_min_gap=min(map_gaps))


def parse_point():
    assert digest(POINT) == POINT_SHA
    point = json.loads(POINT.read_text())
    columns = point["columns"]
    hist, groups = {}, defaultdict(dict)
    current = None
    for i, col in enumerate(columns[:4849]):
        if col["kind"] == "hist":
            current = i
            bits = tuple(map(int, col["actual_bits"]))
            words = tuple(word for word, count in zip(WORDS, col["hist"]) for _ in range(count))
            assert len(words) == 6 and sum(w[0] for w in words) == col["d"]
            hist[i] = dict(bits=bits, words=words, mass=Q(col["weight"]), d=col["d"])
        elif col["kind"] == "joint-reply":
            f, diagonal, wi, wj = col["group"]
            key = (f, diagonal, tuple(wi), tuple(wj))
            groups[current].setdefault(key, {})[tuple(col["state"])] = Q(col["weight"])
    for i, block in groups.items():
        for key, states in block.items():
            assert set(states) == {(0, 1), (1, 0), (1, 1)}
            states[0, 0] = hist[i]["mass"] - sum_values(states.values())
            assert min(states.values()) >= 0
    incomes = [sum_values(h["mass"] * share(h["bits"][s], sum(h["bits"])) for h in hist.values()) for s in range(6)]
    welfare = sum_values(h["mass"] for h in hist.values() if any(h["bits"]))
    optimum = sum_values(h["mass"] for h in hist.values() if h["d"])
    assert welfare == sum(incomes) == Q(point["W"]) and optimum == Q(point["O"]) == 1
    assert sum_values(h["mass"] for h in hist.values()) == 1
    return point, columns, hist, groups, incomes


def evaluate_point():
    point, columns, hist, groups, incomes = parse_point()
    u4, u6 = incomes[3], incomes[5]
    costs = dict(A=Q(0), B=Q(0), Z_IC_cost=Q(0), A0=Q(0), B0=Q(0),
                 A00=Q(0), B00=Q(0), q_over_P1=Q(0), q_over_P2=Q(0), C_credit=Q(0))
    positive_states = 0
    per_hist = []
    for i, h in hist.items():
        a, words, mass, n = h["bits"], h["words"], h["mass"], h["d"]
        p, P, D = sum(a[:3]), sum(a[:4]), sum(a[:5]) + 1
        counts = Counter((words[i], words[j]) for i in range(6) for j in range(6) if i != j)
        assert sum(counts.values()) == 30
        sums = dict(A=Q(0), B=Q(0), Z_IC_cost=Q(0), A0=Q(0), B0=Q(0), A00=Q(0), B00=Q(0))
        for (wi, wj), count in counts.items():
            f = Q(count, 30)
            x, ci, y, cj = wi[0], wi[2], wj[0], wj[2]
            for r, z in product((0, 1), repeat=2):
                mm = groups[i][1, 0, wi, wj][r, z]
                if mm:
                    positive_states += 1
                sums["A"] += f * mm * L(2, p, D, r, x, y, ci, cj, a[5], n)
                sums["B"] += f * mm * L(13, p, D, z, x, y, 0, 0, a[5], n)
                sums["Z_IC_cost"] += f * mm * (Q(n, 6) - z) / (P + r + 1)
            sums["A0"] += f * mass * L(2, p, D, 0, x, y, ci, cj, a[5], n)
            sums["B0"] += f * mass * L(13, p, D, 0, x, y, 0, 0, a[5], n)
            sums["A00"] += f * mass * L(2, p, D, 0, x, y, ci, cj, 0, n)
            sums["B00"] += f * mass * L(13, p, D, 0, x, y, 0, 0, 0, n)
        for k, v in sums.items():
            costs[k] += v
        costs["q_over_P1"] += mass * Q(n, 6 * (P + 1))
        costs["q_over_P2"] += mass * Q(n, 6 * (P + 2))
        costs["C_credit"] += mass * Q(9065 * sum(w[2] for w in words), 6 * (p + 2))
        per_hist.append(dict(column=i, actual_bits="".join(map(str, a)), mass=mass, costs=sums))
    slack_A = 999 * u4 + 139 * u6 - costs["A"]
    slack_B = 10000 * u4 + 1358 * u6 - costs["B"]
    slack_Z = -costs["Z_IC_cost"]
    primitive = {"A_C_substituted": slack_A, "B": slack_B, "actual_Z_optimal_query": slack_Z}
    assert 0 < slack_Z < slack_B < slack_A
    # Rebuild full-column row vectors independently of the state-measure sums.
    sparse = {}
    for kind in ("A", "B", "Z_IC_cost"):
        vector = [Q(0)] * len(columns)
        budget4, budget6 = {"A": (999, 139), "B": (10000, 1358), "Z_IC_cost": (0, 0)}[kind]
        def cost_at(h, wi, wj, state):
            bits, n = h["bits"], h["d"]
            p, P, D = sum(bits[:3]), sum(bits[:4]), sum(bits[:5]) + 1
            r, z = state
            if kind == "Z_IC_cost":
                return (Q(n, 6) - z) / (P + r + 1)
            return L(2 if kind == "A" else 13, p, D, r if kind == "A" else z,
                     wi[0], wj[0], wi[2] if kind == "A" else 0,
                     wj[2] if kind == "A" else 0, bits[5], n)
        current = None
        counts = None
        for col_index, col in enumerate(columns[:4849]):
            if col["kind"] == "hist":
                current, h = col_index, hist[col_index]
                words, bits = h["words"], h["bits"]
                counts = Counter((words[i], words[j]) for i in range(6) for j in range(6) if i != j)
                vector[col_index] = budget4 * share(bits[3], sum(bits)) + budget6 * share(bits[5], sum(bits))
                vector[col_index] -= sum_values(Q(count, 30) * cost_at(h, wi, wj, (0, 0))
                                                for (wi, wj), count in counts.items())
            elif col["kind"] == "joint-reply" and col["group"][:2] == [1, 0]:
                _, _, wi, wj = col["group"]
                wi, wj = tuple(wi), tuple(wj)
                vector[col_index] = -Q(counts[wi, wj], 30) * (
                    cost_at(hist[current], wi, wj, tuple(col["state"])) - cost_at(hist[current], wi, wj, (0, 0)))
        slack = sum_values(value * Q(col["weight"]) for value, col in zip(vector, columns))
        assert slack == {"A": slack_A, "B": slack_B, "Z_IC_cost": slack_Z}[kind]
        sparse[kind] = dict(column_count=len(vector), exact_slack=slack,
                            row_nonzero=[(i, value) for i, value in enumerate(vector) if value],
                            row_sha256=sha256(json.dumps(list(map(str, vector)), separators=(",", ":")).encode()).hexdigest())
    (HERE / "primitive_rows.json").write_text(json.dumps(clean(dict(point_sha256=POINT_SHA, rows=sparse)), indent=2) + "\n")
    rows = []
    for label, aa, bb, lam in (("fixed_49_10", Q(49), Q(10), Q(17965)),
                              ("sharp_C00_extreme", Q(10779, 220), Q(10), Q(17965)),
                              ("A_axis", Q(1), Q(0), Q(0)),
                              ("B_axis", Q(0), Q(1), Q(0))):
        before = (999 * aa + 10000 * bb) * u4 + (139 * aa + 1358 * bb) * u6
        after = (999 * aa + 10000 * bb) * u4 + (138 * aa - 804 * bb) * u6
        raw = aa * slack_A + bb * slack_B + lam * slack_Z
        four = before - aa * costs["A0"] - bb * costs["B0"] - lam * costs["q_over_P1"]
        shifted = after - aa * costs["A00"] - bb * costs["B00"] - lam * costs["q_over_P1"]
        assert raw <= four <= shifted
        rows.append(dict(name=label, alpha=aa, beta=bb, lam=lam,
                         u4_coefficient=999 * aa + 10000 * bb,
                         u6_before=139 * aa + 1358 * bb, credit=aa + 2162 * bb,
                         u6_after=138 * aa - 804 * bb, raw_slack=raw,
                         C00_slack=four, strong_A6_slack=shifted,
                         raw_slack_float=float(raw), C00_slack_float=float(four),
                         strong_A6_slack_float=float(shifted)))
    fixed = rows[0]
    coverage_slack = 148951 * u4 - 1278 * u6 - Q(10857, 2) + Q(88871, 9) * Q(point["W"])
    assert coverage_slack >= fixed["strong_A6_slack"]
    return dict(point_sha256=POINT_SHA, W=point["W"], OPT=point["O"], incomes=incomes,
                primitive_slacks=primitive, primitive_slacks_float={k: float(v) for k, v in primitive.items()},
                all_three_primitive_slacks_nonnegative=all(v >= 0 for v in primitive.values()),
                all_three_primitive_slacks_positive=all(v > 0 for v in primitive.values()),
                normalized_full_three_weight_cone_lower_bound=slack_Z,
                full_column_revaluation=True,
                positive_visible_states=positive_states, costs=costs, rows=rows,
                coverage_slack=coverage_slack, coverage_slack_float=float(coverage_slack), per_hist=per_hist)


def coverage_and_count_check():
    shared = json.loads((DATA / "shared_rz_zero_capacity_v1.json").read_text())
    strong = json.loads((DATA / "strong_a6_transfer_v1.json").read_text())
    base = {}
    for row in shared["conditional_common_C_count_table"]:
        p, D, n, C = (row[k] for k in ("p", "D", "n", "Cnum"))
        values = []
        for overlap in range(max(0, C + n - 6), min(n, C) + 1):
            counts = (6 - n - C + overlap, C - overlap, n - overlap, overlap)
            words = tuple(word for word, count in zip(product((0, 1), repeat=2), counts) for _ in range(count))
            values.append(sum_values(49 * L(2, p, D, 0, words[i][0], words[j][0], words[i][1], words[j][1], 0, n)
                                     + 10 * L(13, p, D, 0, words[i][0], words[j][0], 0, 0, 0, n)
                                     for i in range(6) for j in range(6) if i != j) / 30)
        base[p, D, n, C] = min(values)
        assert min(values) == Q(row["base"])
    for (p, D, n, C), value in base.items():
        assert value >= base[p, D, n, 0] + Q(9065 * C, 6 * (p + 2))
    for row in strong["coverage_type_table"]:
        p, a4, a5, n = (row[k] for k in ("p", "A4", "A5", "n"))
        shift = 1 if row["mode"] == "joint" else 2
        value = base[p, p + a4 + a5 + 1, n, 0] + Q(17965 * n, 6 * (p + a4 + shift))
        assert value == Q(row["value"])
    taxes = {}
    for mode, shift in (("joint", 1), ("separate_same_weights", 2)):
        gain = min(base[0, 1, n, 0] + Q(17965 * n, 6 * shift) for n in range(1, 7))
        tax = max(gain * (n > 0) - base[p, p + a4 + a5 + 1, n, 0]
                  - Q(17965 * n, 6 * (p + a4 + shift))
                  for p in range(4) for a4, a5, a6 in product((0, 1), repeat=3)
                  for n in range(7) if p + a4 + a5 + a6 > 0)
        assert gain == Q(strong["coverage_contracts"][mode]["OPT_credit"])
        assert tax == Q(strong["coverage_contracts"][mode]["W_tax"])
        taxes[mode] = dict(OPT_credit=gain, W_tax=tax)
    return dict(common_C_counts=len(base), coverage_types=len(strong["coverage_type_table"]), taxes=taxes)


def main():
    finite = check_finite_tables()
    point = evaluate_point()
    print("Point primitive slacks:", point["primitive_slacks_float"], flush=True)
    coverage = coverage_and_count_check()
    inputs = [package_path, POINT, DATA / "formal_shared_rz_income_bridge_v1.md",
              DATA / "strong_a6_transfer_v1.md", DATA / "shared_rz_zero_capacity_v1.json",
              DATA / "strong_a6_transfer_v1.json"]
    report = dict(status="PASS", scope="Independent frozen-contract audit and exact fixed-three-weight-cone boundary; not whole free-weight source cone or full SPE.",
                  input_sha256={str(p.relative_to(REPO)): digest(p) for p in inputs},
                  finite=finite, point=point, coverage=coverage,
                  elapsed_seconds=time.monotonic() - started, verifier_sha256=digest(Path(__file__)))
    output = HERE / "audit_bridge.json"
    output.write_text(json.dumps(clean(report), ensure_ascii=False, indent=2) + "\n")
    print("PASS", output, "seconds", report["elapsed_seconds"], flush=True)
    for row in point["rows"]:
        print(row["name"], row["raw_slack_float"], row["C00_slack_float"], row["strong_A6_slack_float"], flush=True)


if __name__ == "__main__":
    main()

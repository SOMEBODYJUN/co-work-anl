"""Clean independent front reconstruction; no author front text imported.

Uses the independently written literal incidence and cost reconstruction from
independent_linear_degree_sweep.py. Finite checks support, but do not prove,
the front covering argument.
"""
from fractions import Fraction as F
import json
from independent_linear_degree_sweep import build_literal, cost, powers


def bits(x, n):
    return [int(j < x) if x < n else int(j >= x - n) for j in range(n)]


def state(n, own_class, other_phase):
    other = bits(other_phase, n)
    return [0 if c == own_class else other[j]
            for j in range(n) for c in range(2)]


def margins(n, k, orientation, degree, alpha, own_class, other_phase,
            heavy_weight=F(1), light_weight=None):
    if light_weight is None:
        light_weight = F(1, k)
    weights, actions = build_literal(n, k, orientation,
                                     heavy_weight, light_weight)
    s = state(n, own_class, other_phase)
    out = []
    for j in [0, n - 1]:
        u = 2 * j + own_class
        old = cost(u, s, weights, actions, degree)
        s[u] ^= 1
        new = cost(u, s, weights, actions, degree)
        s[u] ^= 1
        out.append(old - alpha * new)
    return out


def main():
    neighbour_cases = return_cases = exception_cases = clock_cases = 0
    for n in range(2, 9):
        for k in range(1, n):
            degree, alpha = 5, F(2)
            h = 2 ** degree - alpha
            x = sum((F(k + r, k) ** degree for r in range(1, k + 1)), F(0))
            y = sum((F(r, k) ** degree for r in range(1, k + 1)), F(0))
            ell = alpha * x - y
            for r in range(2 * n):
                heavy = margins(n, k, -1, degree, alpha, 0, r)
                light = margins(n, k, -1, degree, alpha, 1, r)
                if r == 0 or n + k <= r < 2 * n:
                    assert heavy[0] == h
                if k <= r < n:
                    assert heavy[1] == h
                assert min(light) >= -ell
                neighbour_cases += 1
        # Return test, epsilon chosen so N epsilon=1/p.
        degree, alpha = 5, F(2)
        epsilon = F(1, degree * n)
        c = F(degree + 1, degree) ** degree
        j = alpha * c - 1
        u = sum(((1 + r * epsilon) ** degree for r in range(1, n + 1)), F(0))
        v = sum(((r * epsilon) ** degree for r in range(1, n + 1)), F(0))
        z = u - alpha * v
        for t in range(n):
            # x_last-x_0 = T + parity*N.
            for parity in [0, 1]:
                r = (-t - parity * n) % (2 * n)
                heavy = margins(n, n, 1, degree, alpha, 0, r,
                                light_weight=epsilon)
                light = margins(n, n, 1, degree, alpha, 1, r,
                                light_weight=epsilon)
                assert min(heavy) >= -j
                selected = light[parity]  # even forward; odd backward
                assert selected >= z - 3 * (alpha + 1) * (t + 1)
                return_cases += 1
                phase = (r + parity) % (2 * n)
                b = bits(phase, n)
                e = [int(b[(-index) % n] == int(index == 0))
                     for index in range(n)]
                if parity == 0:
                    assert e.count(0) == t + 1
                else:
                    assert e.count(1) == t
                exception_cases += 1
    # Every nonfront is repaired by its earliest bit unlike its anchor.
    # Check actual sharing groups before/after in every anchored triple that
    # contains that mover, with positive arbitrary same-class weight.
    for n in range(3, 11):
        for mask in range(1 << n):
            b = [(mask >> i) & 1 for i in range(n)]
            flips = sum(b[i] != b[i - 1] for i in range(1, n))
            triples = [(0, j, k) for j in range(1, n) for k in range(j + 1, n)]
            triggered = [t for t in triples if b[t[0]] == b[t[2]] != b[t[1]]]
            assert bool(triggered) == (flips >= 2)
            if not triggered:
                continue
            mover = next(i for i in range(1, n) if b[i] != b[0])
            old_full = 0
            for t in triples:
                if mover not in t:
                    continue
                sides = [b[u] ^ phase for u, phase in zip(t, [0, 1, 0])]
                own = t.index(mover)
                old_full += int(len(set(sides)) == 1)
                sides[own] ^= 1
                assert len(set(sides)) > 1
            assert old_full >= 1
            clock_cases += 1
    # Large actual p endpoint parameters. No floating point is used.
    actual = []
    for p in list(range(20, 37)) + [40, 50]:
        alpha, q = F(p, 10), p ** 4
        m = 2
        while 2 ** (m - 1) < p ** 2:
            m += 1
        n = q ** (m - 1) // p
        scale = p * n
        u = F(powers(scale + n, p)[p] - powers(scale, p)[p], scale ** p)
        v = F(powers(n, p)[p], scale ** p)
        z = u - alpha * v
        tmax = (m - 1) * q
        loss = 3 * (alpha + 1) * (tmax + 1)
        assert m <= p and n >= p ** 7 and tmax < n
        assert loss <= F(9, 10) * p ** 2 * q <= z / p
        actual.append(p)
    # Independent exact endpoint check of the final clock inequality with D=p.
    p = 2 ** 20
    q = p ** 4
    m = 2
    while 2 ** (m - 1) < p ** 2:
        m += 1
    n = q ** (m - 1) // p
    lc = (n - 1) * (n - 2) // 2
    # eta0=(10*2^p-p)/40; alpha=p/10.
    hnum = 10 * 2 ** p - p
    bstar = m * q ** (m - 1) * 2 ** p
    assert 2 ** p * (8 * p ** 2 * bstar * lc) <= 5 * hnum * 3 ** p
    assert 184 ** 2 <= p
    return {"neighbour_phase_cases": neighbour_cases,
            "return_phase_cases": return_cases,
            "return_exception_count_cases": exception_cases,
            "nonfront_clock_repair_states": clock_cases,
            "actual_degree_cases": actual,
            "exact_clock_budget_at_degree_2_to_20": True,
            "passed": True}



def emit_report(result, inputs, dependencies=()):
    import argparse
    import hashlib
    from pathlib import Path
    import shlex
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        help="Write a new JSON result; refuse existing paths.")
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error("refusing to overwrite existing result: " + str(args.output))
    here = Path(__file__).resolve()
    repo = here.parents[4]
    proof = repo / "research/current/weighted_congestion/linear_degree_allstate_lower_bound.md"
    report = {
        "schema_version": 1,
        "command": shlex.join([sys.executable, *sys.argv]),
        "python_version": sys.version,
        "code_path": str(here.relative_to(repo)),
        "code_sha256": hashlib.sha256(here.read_bytes()).hexdigest(),
        "dependency_sha256": {name: hashlib.sha256((here.parent / name).read_bytes()).hexdigest()
                              for name in dependencies},
        "proof_path": str(proof.relative_to(repo)),
        "proof_sha256": hashlib.sha256(proof.read_bytes()).hexdigest(),
        "input_source": "explicit deterministic parameters in this source file",
        "actual_inputs": inputs,
        "precision": "exact Python integers and fractions.Fraction; no truncation or floating point",
        "seed": None,
        "randomness": "none",
        "evidence_scope": "only the listed finite cases and exact endpoint budget; not a substitute for the general proof",
        "results": result,
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output is not None:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    emit_report(main(), {
        "neighbour_endpoints": {"N": list(range(2, 9)), "K": "all integers 1..N-1",
                                "degree": 5, "alpha": "2", "weights": ["1", "1/K"],
                                "relative_phases": "all integers 0..2N-1"},
        "full_return": {"N": list(range(2, 9)), "K": "N", "degree": 5,
                        "alpha": "2", "weights": ["1", "1/(5N)"],
                        "T": "all integers 0..N-1", "parity": [0, 1]},
        "clock_repair": {"class_width": list(range(3, 11)), "states": "all binary strings",
                         "triples": "all (0,j,k), 1<=j<k<N", "mover": "earliest bit unlike anchor"},
        "actual_family_p": list(range(20, 37)) + [40, 50],
        "exact_clock_endpoint": {"p": 2**20, "D": 2**20, "eta0": "(2^p-p/10)/4",
                                 "L_c": "binom(N-1,2)", "Bstar": "m Q^(m-1) 2^p"},
    }, dependencies=("independent_linear_degree_sweep.py",))

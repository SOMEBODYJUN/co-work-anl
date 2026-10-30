"""Independent Fraction audit of the frozen healthy-sweep candidate.

Literal resource incidence is rebuilt without the repository lift code. Large
candidate parameters are checked using integer finite differences for sums of
powers, not the candidate's Riemann inequalities. Finite checks are not proofs.
"""
from fractions import Fraction as F
from math import comb
import json


def powers(n, degree):
    out = []
    for k in range(degree + 1):
        v = (n + 1) ** (k + 1) - 1
        v -= sum(comb(k + 1, j) * out[j] for j in range(k))
        assert v % (k + 1) == 0
        out.append(v // (k + 1))
    return out


def build_literal(n, k, orientation, w0=F(5, 3), w1=F(2, 7)):
    # Player order is clone index first, then heavy/light class.
    weights = [w0 if u % 2 == 0 else w1 for u in range(2 * n)]
    actions = [[set(), set()] for _ in weights]
    for j in range(n):
        h = 2 * j
        actions[h][0].add(2 * j)
        actions[h][1].add(2 * j + 1)
        for t in range(k):
            u = 2 * ((j + t) % n) + 1
            side = int(u > h) ^ int(orientation == -1)
            actions[u][0].add(2 * j + side)
            actions[u][1].add(2 * j + 1 - side)
    return weights, actions


def cost(u, state, weights, actions, degree):
    loads = [F(0) for _ in range(len(weights))]
    for v, action in enumerate(state):
        for e in actions[v][action]:
            loads[e] += weights[v]
    return sum((loads[e] ** degree for e in actions[u][state[u]]), F(0))


def literal_audit():
    sweeps = states_checked = 0
    for n in range(1, 7):
        for k in range(1, n + 1):
            for orientation in [-1, 1]:
                weights, actions = build_literal(n, k, orientation)
                assert all(a[0].isdisjoint(a[1]) for a in actions)
                assert all(all(a) for a in actions)
                wh, wl = weights[:2]
                for degree in [0, 1, 2, 5]:
                    old = [wh ** degree,
                           sum(((wh + r * wl) ** degree for r in range(1, k + 1)), F(0))]
                    new = [(wh + k * wl) ** degree,
                           sum(((r * wl) ** degree for r in range(1, k + 1)), F(0))]
                    if orientation == -1:
                        old, new = new, old
                    state = [0] * (2 * n)
                    first = []
                    for half in range(2):
                        observed = []
                        for u in range(2 * n):
                            before = cost(u, state, weights, actions, degree)
                            state[u] ^= 1
                            after = cost(u, state, weights, actions, degree)
                            assert before == old[u % 2]
                            assert after == new[u % 2]
                            observed.append((before, after))
                        if half == 0:
                            first = observed
                        else:
                            assert observed == first
                    assert state == [0] * (2 * n)
                    sweeps += 1
                # Exhaustive all-state cap, separately from sweep identities.
                if n <= 4:
                    for mask in range(1 << (2 * n)):
                        state = [(mask >> u) & 1 for u in range(2 * n)]
                        for u in range(2 * n):
                            bound = (1 if u % 2 == 0 else k) * (wh + k * wl) ** 3
                            assert cost(u, state, weights, actions, 3) <= bound
                        states_checked += 1
    return {"literal_parameter_cases": sweeps,
            "exhaustive_states_checked": states_checked}


def family_audit(p):
    alpha = F(p, 10)
    qden = p ** 4
    m = 2
    while 2 ** (m - 1) < p ** 2:
        m += 1
    scale = qden ** (m - 1)
    n = scale // p
    assert scale % p == 0 and n >= qden
    x = F(powers(2 * qden, p)[p] - powers(qden, p)[p], qden ** p)
    y = F(powers(qden, p)[p], qden ** p)
    u = F(powers(scale + n, p)[p] - powers(scale, p)[p], scale ** p)
    v = F(powers(n, p)[p], scale ** p)
    h = 2 ** p - alpha
    ell = alpha * x - y
    c = F(p + 1, p) ** p
    j = alpha * c - 1
    z = u - alpha * v
    amplitudes = [(2 * ell / h) ** a for a in range(m - 1)]
    ret = h / (2 * j)
    margins = [h - ret * j]
    margins += [amplitudes[a] * h - amplitudes[a - 1] * ell
                for a in range(1, m - 1)]
    margins += [ret * z - amplitudes[-1] * ell]
    assert all(value > 0 for value in [h, ell, j, z])
    assert F(4, qden) <= h / ell <= F(40, qden)
    assert z / j > F(3 * scale, p * p)
    assert min(margins) == h / 2
    assert margins[-1] > h / 2
    assert all(value > h / 2 for value in margins[1:])
    cap = m * scale * 2 ** p
    class_caps = [2 ** p + ret * c]
    class_caps += [(qden * amplitudes[a - 1] + amplitudes[a]) * 2 ** p
                   for a in range(1, m - 1)]
    class_caps += [qden * amplitudes[-1] * 2 ** p + n * ret * c]
    assert max(class_caps) <= cap
    assert cap / min(margins) <= F(20, 9) * m * scale
    return {"p": p, "m": m, "minimum_margin_is_H_over_2": True,
            "global_state_caps_pass": True}


def main():
    for n in range(8):
        for degree in range(10):
            assert powers(n, degree)[degree] == sum(r ** degree for r in range(1, n + 1))
    result = literal_audit()
    result["family_cases"] = [family_audit(p) for p in list(range(20, 37)) + [40, 50]]
    return result



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
        "literal": {"N": list(range(1, 7)), "K": "all integers 1..N",
                    "orientations": [-1, 1], "degrees": [0, 1, 2, 5],
                    "weights": ["5/3", "2/7"], "rounds": 2},
        "all_state_cap": {"N": list(range(1, 5)), "K": "all integers 1..N",
                          "orientations": [-1, 1], "degree": 3,
                          "states": "all 2^(2N) action states"},
        "power_sum_self_check": {"n": list(range(8)), "degrees": list(range(10))},
        "actual_family_p": list(range(20, 37)) + [40, 50],
    })

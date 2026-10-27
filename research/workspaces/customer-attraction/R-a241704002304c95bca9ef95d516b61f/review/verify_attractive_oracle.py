"""Independent integer audits of mincut and invariant-orbit compression.

No author's oracle, graph package, or CAG row generator is imported.
The mathematical proof is separate; these checks audit factors and signs.
"""
from collections import deque
from itertools import product
from pathlib import Path
import json
import random

HERE = Path(__file__).resolve().parent


def value(bits, v0, v1, J):
    return sum(v1[i] if r else v0[i] for i, r in enumerate(bits)) + sum(
        J[i][j]*bits[i]*bits[j] for i in range(len(bits)) for j in range(i+1, len(bits))
    )


def brute(v0, v1, J):
    return max(value(bits, v0, v1, J) for bits in product((0, 1), repeat=len(v0)))


def mincut_max(v0, v1, J):
    n = len(v0)
    source, sink = n, n+1
    residual = [[0]*(n+2) for _ in range(n+2)]
    # Work with 2*objective, keeping every capacity an exact integer.
    d = [2*(v1[i]-v0[i])+sum(J[i]) for i in range(n)]
    for i in range(n):
        residual[source][i] = max(d[i], 0)
        residual[i][sink] = max(-d[i], 0)
        for j in range(n):
            if i != j:
                residual[i][j] = J[i][j]
    flow = 0
    while True:
        parent = [-1]*(n+2)
        parent[source] = source
        todo = deque([source])
        while todo and parent[sink] < 0:
            i = todo.popleft()
            for j, cap in enumerate(residual[i]):
                if cap > 0 and parent[j] < 0:
                    parent[j] = i
                    todo.append(j)
        if parent[sink] < 0:
            break
        delta, j = None, sink
        while j != source:
            i = parent[j]
            delta = residual[i][j] if delta is None else min(delta, residual[i][j])
            j = i
        flow += delta
        j = sink
        while j != source:
            i = parent[j]
            residual[i][j] -= delta
            residual[j][i] += delta
            j = i
    twice = 2*sum(v0)+sum(max(x, 0) for x in d)-flow
    assert twice % 2 == 0
    return twice//2


def compress(blocks, v0, v1, J):
    k = len(blocks)
    c0 = [sum(v0[i] for i in block) for block in blocks]
    c1 = [sum(v1[i] for i in block)+sum(J[i][j] for ii, i in enumerate(block) for j in block[ii+1:]) for block in blocks]
    CJ = [[0]*k for _ in range(k)]
    for g in range(k):
        for h in range(g+1, k):
            CJ[g][h] = CJ[h][g] = sum(J[i][j] for i in blocks[g] for j in blocks[h])
    return c0, c1, CJ


def main():
    rng = random.Random(241061)
    cases = 0
    for n in range(1, 9):
        for _ in range(32):
            k = rng.randint(1, min(n, 4))
            colors = list(range(k)) + [rng.randrange(k) for _ in range(n-k)]
            rng.shuffle(colors)
            blocks = [[i for i, c in enumerate(colors) if c == h] for h in range(k)]
            unary0 = [rng.randint(-7, 7) for _ in blocks]
            unary1 = [rng.randint(-7, 7) for _ in blocks]
            v0, v1 = [unary0[c] for c in colors], [unary1[c] for c in colors]
            W = [[0]*k for _ in range(k)]
            for g in range(k):
                for h in range(g, k):
                    W[g][h] = W[h][g] = rng.randint(0, 9)
            J = [[0 if i == j else W[colors[i]][colors[j]] for j in range(n)] for i in range(n)]
            expected = brute(v0, v1, J)
            assert mincut_max(v0, v1, J) == expected
            c0, c1, CJ = compress(blocks, v0, v1, J)
            assert brute(c0, c1, CJ) == expected
            assert mincut_max(c0, c1, CJ) == expected
            cases += 1
    # Exact local elimination before the r-graph: direct all 32^2 choices
    # versus independent per-vertex 16-state optimization and the binary cut.
    local_cases = 0
    for _ in range(16):
        tables = [[rng.randint(-5, 7) for _ in range(32)] for _ in range(2)]
        J = [[0, rng.randint(0, 8)], [0, 0]]
        J[1][0] = J[0][1]
        expected = max(tables[0][i]+tables[1][j]+J[0][1]*(i//16)*(j//16) for i, j in product(range(32), repeat=2))
        v0 = [max(t[:16]) for t in tables]
        v1 = [max(t[16:]) for t in tables]
        assert mincut_max(v0, v1, J) == expected
        local_cases += 1
    # Sign condition is essential: two symmetric vertices, repulsive edge.
    Jbad = [[0, -2], [-2, 0]]
    full = brute([0, 0], [1, 1], Jbad)
    invariant = max(value((b, b), [0, 0], [1, 1], Jbad) for b in (0, 1))
    assert full == 1 and invariant == 0
    report = {
        "scope": "independent implementation audit of exact mincut, local elimination and invariant-orbit reduction; not a six-player theorem",
        "seed": 241061,
        "integer_mincut_and_orbit_cases": cases,
        "local_32_state_elimination_cases": local_cases,
        "negative_edge_control": {"full_max": full, "orbit_constant_max": invariant},
        "status": "all exact checks passed",
    }
    (HERE / "attractive_oracle_audit.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()

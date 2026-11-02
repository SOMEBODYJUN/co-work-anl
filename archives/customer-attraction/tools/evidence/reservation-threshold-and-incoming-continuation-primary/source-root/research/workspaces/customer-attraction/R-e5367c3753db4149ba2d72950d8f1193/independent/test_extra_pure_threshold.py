"""Attack only the all-input candidate u_1 >= theta_(m+1)(0).

Fix the full-history strategy of the existing individual-security example and
vary all 63 unit-customer type multiplicities. A MILP chooses a profitable
extra query for each three-provider background. A positive gap would refute
the candidate, not Q-CAG-HALF. No conclusion follows from solver failure.
"""

import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

ROOT = Path(__file__).resolve().parents[5]
n = 6
m = 3
types = list(range(1, 1 << n))
data = json.loads((ROOT / "evidence/certificates/customer_attraction/individual_security_failure.json").read_text())
sigma = {tuple(row["history"]): row["action"] for row in data["strategy"]["actions"]}


def leaf(h):
    while len(h) < m:
        h = (*h, sigma[h])
    return h


def coeff(z, i):
    return np.array([
        ((1 / sum(bool(mask & (1 << a)) for a in z))
         if mask & (1 << z[i]) else 0)
        for mask in types
    ])


rows = []
lbs = []
ubs = []
backgrounds = list(itertools.combinations_with_replacement(range(n), m))
nw = len(types)
nd = nw
nb = len(backgrounds) * n
nv = nw + 1 + nb


def append(row, lo=-np.inf, hi=np.inf):
    rows.append(row)
    lbs.append(lo)
    ubs.append(hi)


root_coeff = coeff(leaf(()), 0)
for length in range(m):
    for h in itertools.product(range(n), repeat=length):
        actual = coeff(leaf(h), length)
        for a in range(n):
            row = np.zeros(nv)
            row[:nw] = actual - coeff(leaf((*h, a)), length)
            append(row, lo=0)

row = np.zeros(nv)
row[:nw] = 1
append(row, lo=1, hi=1)
for j, B in enumerate(backgrounds):
    choices = np.zeros(nv)
    for a in range(n):
        q = np.array([
            ((1 / (1 + sum(bool(mask & (1 << b)) for b in B)))
             if mask & (1 << a) else 0)
            for mask in types
        ])
        row = np.zeros(nv)
        row[:nw] = q - root_coeff
        row[nd] = -1
        row[nw + 1 + j * n + a] = -2
        append(row, lo=-2)
        choices[nw + 1 + j * n + a] = 1
    append(choices, lo=1)

A = lil_matrix((len(rows), nv))
for i, row in enumerate(rows):
    A[i] = row
objective = np.zeros(nv)
objective[nd] = -1
integrality = np.zeros(nv)
integrality[nw + 1:] = 1
lower = np.zeros(nv)
upper = np.ones(nv)
lower[nd] = -1
result = milp(objective, integrality=integrality,
              bounds=Bounds(lower, upper),
              constraints=LinearConstraint(A.tocsr(), lbs, ubs),
              options={"time_limit": 90, "mip_rel_gap": 1e-8})
output = {"status": int(result.status), "message": result.message}
if result.x is not None:
    output["gap"] = float(result.x[nd])
    output["weights"] = {str(mask): float(w) for mask, w in zip(types, result.x[:nw]) if w > 1e-8}
    output["queries"] = [int(np.argmax(result.x[nw + 1 + j * n:nw + 1 + (j + 1) * n])) for j in range(len(backgrounds))]
out = Path(__file__).with_suffix(".json")
out.write_text(json.dumps(output, indent=2) + "\n")
print(json.dumps(output, indent=2))

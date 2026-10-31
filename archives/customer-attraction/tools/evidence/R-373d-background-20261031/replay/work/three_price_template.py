"""Search a specific three-remaining-player price certificate template.

The LP uses all 3-player-sharp rows with symmetric query multipliers and
eliminates h exactly by setting the V multiplier to S/n. A failed LP is only
a template obstruction. No floating result is a theorem.
"""
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def value_row(n, bg, a, b, c, q, r, d, ell, enriched=False):
    den = bg + a + b + c
    al, be, ga = [(z / den if z else 0) for z in (a, b, c)]
    other = bg + c + q + r
    cp = c / other if c else 0
    rp = r / other if r else 0
    # Variables: x=K_Q,y=K_R,p=Psum,z=Zsum,s=Ssum,f=F,j=Jsum.
    row = [3 * al - 3 * q / (bg + 3),
           3 * al - 3 * r / (bg + 3),
           n * ga - d / (bg + a + b + 1),
           n * ga - ell / (bg + a + b + 1),
           n * be - d / (bg + a + 1)
           + d * ell / (n * (bg + a + 1) * (bg + a + 2)),
           al - cp,
           n * rp - d / (bg + c + q + 1)]
    if enriched:
        row += [n*al-d/(bg+3), n*al-ell/(bg+3),
                al-b/(bg+3), al-c/(bg+3)]
    target = n * al + int(den > 0) - int(d > 0)
    return row, target


def solve(n, bgmax=30, enriched=False):
    A, B, labels = [], [], []
    for bg in range(bgmax + 1):
        for a, b, c, q, r in itertools.product(range(2), repeat=5):
            for d in set([0, 1, n]):
                for ell in [0, n]:
                    row, target = value_row(n, bg, a, b, c, q, r, d, ell, enriched)
                    A.append(row); B.append(target)
                    labels.append([bg, a, b, c, q, r, d, ell])
    res = linprog(np.ones(11 if enriched else 7), A_ub=np.array(A), b_ub=np.array(B),
                  bounds=(0, None), method="highs")
    out = {"n": n, "bgmax": bgmax, "enriched": enriched, "status": int(res.status),
           "message": res.message}
    if res.success:
        out["multipliers"] = res.x.tolist()
        out["minimum_slack"] = float(min(np.array(B)-np.array(A)@res.x))
    print(json.dumps(out), flush=True)
    return out


if __name__ == "__main__":
    results = [solve(n) for n in [1, 2, 3, 4, 5, 10, 20, 100]]
    Path(__file__).with_name("three_price_template_report.json").write_text(
        json.dumps(results, indent=2)+"\n")

"""Integer coefficient audit, independently rebuilt from six legal slacks.

Multiplies the residual by 48(b+1)(b+2)(b+3). All 15 Boolean membership
patterns are checked; nonnegative coefficients prove all real b>=0.
"""
from itertools import product
from pathlib import Path
import json

POLY = {1: (6, 5, 1), 2: (3, 4, 1), 3: (2, 3, 1)}


def main():
    minima = [None, None, None]
    root_table = {}
    count = 0
    for bits in product((0, 1), repeat=15):
        a, b, c = bits[:3]
        t, ell, q, r = bits[3:6], bits[6:9], bits[9:12], bits[12:15]
        out = [0, 0, 0]

        def add(mult, numerator, denom_shift):
            if numerator:
                for i in range(3):
                    out[i] += mult*numerator*POLY[denom_shift][i]

        def utility(mult, x, y, z):
            add(mult, x, 1+y+z)

        s, d = a+b+c, sum(t)
        add(112, s, s)
        add(-144, d, d)
        for j in range(3):
            utility(48, t[j], q[j], r[j])
            utility(48, t[j], a, ell[j])
            utility(48, t[j], a, b)
            # Subtract 3/4 E_LC.
            utility(-36, ell[j], a, t[j]); utility(36, c, a, t[j])
            # Subtract 1/8 E_RC.
            utility(-6, r[j], t[j], q[j]); utility(6, c, t[j], q[j])
            # Subtract 17/48 E_CT.
            utility(-17, c, a, b); utility(17, t[j], a, b)
            # Subtract E_CL.
            utility(-48, c, a, b); utility(48, ell[j], a, b)
            # Subtract 7/48 E_CQ.
            utility(-7, c, a, b); utility(7, q[j], a, b)
            # Subtract 1/12 E_LR.
            for k in range(3):
                utility(-4, ell[j], a, t[j]); utility(4, r[k], a, t[j])
        assert all(v >= 0 for v in out), (bits, out)
        expected_b2_scaled = 112*(a+b)+22*c+17*d+7*sum(q)+6*sum(r)
        assert out[2] == expected_b2_scaled
        key = ''.join(map(str, (a,b,c)))+':'+str(d)
        root_table[key] = out[0] if key not in root_table else min(root_table[key], out[0])
        minima = [v if old is None else min(old,v) for old,v in zip(minima,out)]
        count += 1
    report = {"membership_patterns": count, "coefficient_scale": 48,
              "minimum_scaled_coefficients": minima, "root_table_scale": 288,
              "root_minima_scaled": root_table,
              "status": "independent integer coefficient reconstruction passed",
              "scope": "Universal three-remaining-player transfer using six true last-mover slacks; no arbitrary-player proof."}
    Path(__file__).with_name('three_transfer_independent_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

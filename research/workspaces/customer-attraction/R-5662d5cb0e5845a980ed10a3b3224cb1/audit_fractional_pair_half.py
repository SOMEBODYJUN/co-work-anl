"""Independent reconstruction of research_6's nine-row tau=21/5 certificate.

No author-code imports, solver or floating arithmetic. Each literal customer
keeps all six actual membership bits and its comparison-set membership.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

TAU = F(21, 5)
FLOOR_WEIGHTS = tuple(map(F, (
    '2784735/10526656', '240968825/852659136',
    '65773795/213164784', '820179895/4547515392',
    '14864915/252639744', '9728723/24060928',
)))
SAFE4_WEIGHT = F(99135297, 120304640)
SAFE5_WEIGHT = F(9429757, 30076160)
PAIR_WEIGHT = F(8821071, 12030464)


def reconstruct():
    assert all(w >= 0 for w in (
        *FLOOR_WEIGHTS, SAFE4_WEIGHT, SAFE5_WEIGHT, PAIR_WEIGHT))
    # Rebuild strongPAIR from its three original true-IC slacks, not from
    # an imported projected row. q is the genuine last response to T.
    strong_pair_identities = 0
    share = lambda k, den: F(k, den) if k else F(0)
    for p in range(5):
        dd = (p+1)*(p+2)
        for a, b, t, q, s in product((0, 1), repeat=5):
            u1, u2 = share(a, p+a+b), share(b, p+a+b)
            original_ic = (
                u1-share(t, p+t+q)
                +share(q, p+t+q)-share(s, p+t+s)
                +u2-share(q, p+a+q))
            strong = u1+u2+F(a, dd)-F(t+s, p+1)+F(t*s, dd)
            assert strong == original_ic+F(a*(1-q), dd)
            strong_pair_identities += 1
    rows = []
    for e in product((0, 1), repeat=6):
        c = sum(e)
        u = tuple(F(k, c) if c else F(0) for k in e)
        p = sum(e[:4])
        for o in (0, 1):
            # Actual source i, remaining players including source = 6-i.
            floors = tuple(TAU*u[i] - F(o, sum(e[:i]) + 6-i)
                           for i in range(6))
            # Actual players 4,5 query actual final theme B, using all
            # remaining providers in the safe denominator.
            safe4 = u[3] - F(e[5], sum(e[:3])+3)
            safe5 = u[4] - F(e[5], p+2)
            # Average strongPAIR over two independent queries from one
            # fractional-cover distribution, discard non-C terms.
            demand = 2/(TAU*(p+1)) - 1/(TAU*TAU*(p+1)*(p+2))
            pair = u[4]+u[5] + F(e[4], (p+1)*(p+2)) - o*demand
            weighted = sum(w*s for w, s in zip(FLOOR_WEIGHTS, floors))
            weighted += SAFE4_WEIGHT*safe4 + SAFE5_WEIGHT*safe5
            weighted += PAIR_WEIGHT*pair
            target = 2*int(c > 0)-o
            residual = target-weighted
            assert residual >= 0, (e, o, residual)
            rows.append({'actual_bits': list(e), 'in_comparison_set': o,
                         'residual': str(residual)})
    # Analytic monotonicity: d/dq [2q/(p+1)-q^2/D]
    # is positive for all 0<=q<=1 and integer p>=0.
    for p in range(5):
        assert F(2, p+1) - F(2, (p+1)*(p+2)) > 0
    return {
        'scope': 'Complete coefficient domain, not finite game sampling; '
                 'nine genuine nonnegative global SPE slacks.',
        'tau': str(TAU), 'literal_types': len(rows),
        'minimum_residual': str(min(F(r['residual']) for r in rows)),
        'zero_types': sum(F(r['residual']) == 0 for r in rows),
        'minimum_positive_residual': str(min(
            F(r['residual']) for r in rows if F(r['residual']) > 0)),
        'raw_three_IC_strongPAIR_identities': strong_pair_identities,
        'all_weights_nonnegative': True,
        'author_code_imported': False,
        'main_target': 'OPEN; comparison fractional-cover condition is essential',
        'types': rows,
    }


if __name__ == '__main__':
    result = reconstruct()
    out = Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'types'},
                     ensure_ascii=False))

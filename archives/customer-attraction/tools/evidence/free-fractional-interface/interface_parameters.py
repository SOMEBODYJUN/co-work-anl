"""Exact parameters behind the original finite audit; no optimizer or SPE search.

Exposes the audit's static background and the obstruction to treating it as
a legal history, plus exact tangent/price constants omitted from its stdout.
"""
from fractions import Fraction as Q
import json


def main():
    weights = {2: 1, 5: 2, 6: 2}
    r = 3
    background = {mask: mask % 3 for mask in weights}
    p = (Q(1, 2), Q(1, 3), Q(1, 6))
    q0 = (Q(1, 4), Q(1, 2), Q(1, 4))

    def alpha(mask, q):
        return sum(q[a] for a in range(3) if mask >> a & 1)

    den = {mask: background[mask]+1+(r-1)*alpha(mask, q0) for mask in weights}
    value = sum(Q(w)*alpha(mask, p)/den[mask] for mask, w in weights.items())
    H = tuple(sum(Q(w)*alpha(mask, p)/den[mask]**2
                  for mask, w in weights.items() if mask >> a & 1) for a in range(3))
    lower = value+(r-1)*(sum(q0[a]*H[a] for a in range(3))-max(H))
    assert value == Q(49, 60) and H == (Q(1, 12), Q(217, 1200), Q(73, 300))
    assert lower == Q(809, 1200)

    # Legal history counts would have h1=2 from type2 and h1+h2=0 from
    # type6.  Thus h2=-2; no nonnegative history counts can give this b.
    forced_h1 = background[2]
    forced_h2 = background[6]-forced_h1
    assert forced_h1 == 2 and forced_h2 == -2

    price_q = (Q(1, 5), Q(3, 10), Q(1, 2))
    price_den = {mask: 1+(r-1)*alpha(mask, price_q) for mask in weights}
    price_values = tuple(sum(Q(w)/price_den[mask] for mask, w in weights.items()
                             if mask >> a & 1) for a in range(3))
    mass = sum(Q(w)*(price_den[mask]-1)/price_den[mask] for mask, w in weights.items())
    assert price_values == (Q(5, 6), Q(145, 104), Q(125, 78))
    assert mass == Q(865, 312) == (r-1)*sum(price_q[a]*price_values[a] for a in range(3))

    def cap_values(q):
        return tuple(sum(Q(w)/(1+alpha(mask, q)) for mask, w in weights.items()
                         if mask >> a & 1) for a in range(3))

    restricted_midpoint = cap_values((Q(1, 2), Q(1, 2), Q(0)))
    free = cap_values((Q(0), Q(0), Q(1)))
    assert restricted_midpoint == (Q(4, 3), Q(2), Q(8, 3))
    assert free == (Q(1), Q(2), Q(2))
    report = dict(
        weights=weights,
        tangent=dict(r=r, competitor_mass=r-1, background=background,
                     p=p, q0=q0, denominators=den, K=value, H=H, lower_bound=lower,
                     legal_history=False, forced_h1=forced_h1, forced_h2=forced_h2,
                     scope='Arbitrary nonnegative static-background algebra; not an original-model legal prefix or SPE.'),
        price=dict(background=0, competitor_mass=r-1, q=price_q,
                   denominators=price_den, queries=price_values,
                   deletion_mass=mass, upper=(r-1)*max(price_values)),
        support_example=dict(players=2, restricted_midpoint_queries=restricted_midpoint,
                             restricted_optimum=Q(8, 3), free_queries=free,
                             free_optimum=Q(2), welfare=5,
                             scope='Optimum lower bounds use the analytic formulas in the formal counterexample, not a finite grid minimum.'))
    print(json.dumps(report, default=str, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

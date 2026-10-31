#!/usr/bin/env python3
"""Audit frozen BGW v1 Algorithm 7 on a symmetric infeasible MixPC instance.

P and C have two identical rows and two columns, with P_ij=1,
C_ij=1/100.  Hence t=x1+x2, local_j=100*exp(1.01*t), x_j(0)=1/2.
An ineligible inner round is followed only by identical no-op rounds in
that phase; skipping these is exact for this instance. Decimal arithmetic
is numerical supporting evidence, not an exact rational certificate.
"""
from decimal import Decimal, ROUND_CEILING, localcontext
import json


def run(epsilon: str, precision: int = 80) -> dict:
    with localcontext() as ctx:
        ctx.prec = precision
        e = Decimal(epsilon)
        one = Decimal(1)
        L = 4 * Decimal(2).ln() / e
        log_step = (one + e).ln()
        phases = int((10 * L / log_step).to_integral_value(rounding=ROUND_CEILING))
        # A fixed polynomial budget of the same safe-update-bound order.
        R = int((100 * L / e * (200 * L).ln()).to_integral_value(rounding=ROUND_CEILING))
        multiplier = one + e / (10 * L)
        log100 = Decimal(100).ln()
        t = one
        updates = 0
        exhausted = False
        deleted_covering = False
        for phase in range(phases):
            log_tau = phase * log_step
            k = 0
            while k < R:
                if t / 100 >= L:
                    deleted_covering = True
                    break
                # log(local_j/tau) <= log(1+e); both variables update together.
                if log100 + Decimal('1.01') * t > log_tau + log_step:
                    break
                t *= multiplier
                k += 1
                updates += 1
            exhausted = exhausted or (k == R)
            if deleted_covering:
                break
        assert not deleted_covering
        assert not exhausted
        assert t > 9 * L
        return {
            'internal_epsilon': epsilon,
            'precision': precision,
            'm': 2,
            'n': 2,
            'P_entry': '1',
            'C_entry': '1/100',
            'L': str(+L),
            'inner_round_budget': R,
            'phases': phases,
            'simultaneous_updates': updates,
            'packing_load': str(+t),
            'packing_load_over_L': str(+(t / L)),
            'covering_load_over_L': str(+(t / (100 * L))),
            'all_covering_rows_reject': t / 100 < L,
            'budget_exhausted': exhausted,
        }


if __name__ == '__main__':
    print(json.dumps({
        'status': 'finite-decimal-replay-not-formal-certificate',
        'source_algorithm': 'BGW arXiv:2607.10075v1 Algorithm 7 (no unstated packing guard)',
        'cases': [run(e) for e in ('0.1', '0.05', '0.02')],
    }, indent=2))

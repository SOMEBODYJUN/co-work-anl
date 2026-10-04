"""Exact arithmetic audit for the mixed-multiplicity interface boundary.

This does not solve the mixed-q selector.  It checks (i) the equal-q
reduction to restricted identical-link NE and (ii) a positive integer witness
that the restricted-related-link inequality is different when q differs.
"""
from fractions import Fraction


def rq_source_residual(q_source, w_source, source_total):
    return Fraction(source_total - w_source, q_source)


def rq_target_load(q_target, target_total):
    return Fraction(target_total, q_target)


def related_current_latency(speed, total):
    return Fraction(total, speed)


def related_target_latency(speed, total, weight):
    return Fraction(total + weight, speed)


def main():
    # Equal multiplicity: (W_t-w_i)/q <= W_v/q iff W_t-w_i <= W_v.
    q = 3
    assert rq_source_residual(q, 5, 17) <= rq_target_load(q, 13)
    assert 17 - 5 <= 13

    # Mixed multiplicity witness from the current research note.
    q_t, q_v, w_i, W_t, W_v = 1, 2, 2, 5, 6
    assert rq_source_residual(q_t, w_i, W_t) == rq_target_load(q_v, W_v) == 3
    assert related_current_latency(q_t, W_t) > related_target_latency(q_v, W_v, w_i)
    print("equal-q reduction and mixed-q mismatch verified exactly")


if __name__ == "__main__":
    main()

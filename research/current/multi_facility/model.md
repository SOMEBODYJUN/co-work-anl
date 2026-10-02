# MF-MODEL: arbitrary many labeled facilities, common catalog

Version 1, 2026-10-02. This is an explicit extension of the two-facility model,
not a silent change to `research/current/model.md`.

There are finitely many clients I, positive real weights w_i, a finite nonempty
physical site catalog S, and k >= 2 labeled facilities. Every facility has
exactly the same catalog S. A site s covers an arbitrary subset C_s of I. A
layout is the labeled tuple s in S^k; repetitions are permitted. A client i may
choose exactly one facility in A_i(s)={f:i in C_{s_f}}. If this set is empty the
client is unserved; otherwise service is compulsory. Different clients randomize
independently. For probabilities p_if, the conditional cost of using f is

    c_if = w_i + sum_{j != i} w_j p_jf.

The expected facility revenue is L_f=sum_i w_i p_if. An exact client Nash
equilibrium requires positive probability only on accessible facilities with
minimum conditional cost. There is no distance term, capacity, entrance fee,
client-specific delay or correlated randomization.

A complete continuation sigma chooses an exact client equilibrium for EVERY
labeled layout in S^k. The sought alpha-SPE is a layout s and such a sigma with

    L_f(sigma(s[f <- r])) <= alpha L_f(sigma(s))

for every f and every r in S other than s_f. A zero on-path load requires all its
selected deviation loads to be zero. No facility optimality is imposed at the
off-path first-stage layouts themselves; client optimality is imposed there.

For algorithmic descriptions, clients and their site incidence are explicit,
weights are positive binary rationals, and the k output facility coordinates are
explicit. Bounds polynomial in k are NOT bounds in log(k) for a succinct encoding.
The theorem `SC-K-2-E` is an existence theorem for real weights. The accompanying
exhaustive implementation makes no polynomial-time claim.

## Finite default continuation

For any fixed layout, choose any feasible pure client assignment and repeatedly
perform a strict client improvement. If i moves from f to g, the change in
one-half the sum of squared loads is

    w_i (L_g + w_i - L_f) < 0.

There are finitely many pure assignments. Thus the process ends at an exact pure
NE. Fixing least-index initial choices and least-index strict best replies makes
this a deterministic rule at every layout. Termination is not a polynomial
iteration bound.

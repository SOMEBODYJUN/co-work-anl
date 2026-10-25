# Why common catalog price caps alone cannot improve a deviation floor

2026-10-25. Exact general-m CAG-MODEL. This is a short analytic elimination
of one proposed compression, not a new welfare inequality. HALF(5) remains
OPEN. No numerical scan or new optimizer was needed.

Fix any actual path in a complete pure SPE. Let u_j be actual player j's
final payoff, p_j(x) its actual earlier-player load, r_j=m-j+1, and

    a_j(x)=1/[p_j(x)+r_j].

For every legal topic T, the standard true deviation floor gives the
common catalog cap

    sum_{x in T} a_j(x) <= u_j                         for all j.   (K)

Consider position i and a forced legal topic T. Its r_i-1 true successor
actions each satisfy all caps (K), so their aggregate future customer
loads k_x satisfy their aggregate caps. For any lambda_j>=0 define

    phi_i(x;lambda) = min_{k=0,...,r_i-1}
      {1/[p_i(x)+1+k]+k sum_j lambda_j a_j(x)}.

Lagrangian elimination of those successor loads indeed yields the valid row

    u_i+(r_i-1)sum_j lambda_j u_j
      >= sum_{x in T} phi_i(x;lambda).                       (C)

However **every row (C) is already implied by (K)**. In the displayed minimum
choose k=r_i-1, obtaining

    phi_i(x;lambda)
      <= a_i(x)+(r_i-1)sum_j lambda_j a_j(x).

Sum over T and use (K) at i and at every j. This is exactly (C), with
nonnegative multipliers 1 and (r_i-1)lambda_j. Thus optimizing over all
prices lambda, or retaining all actual-node caps simultaneously, adds no
information to the original floor system.

The primal reason is equally exact: the hypothetical successor tuple
(T,...,T) is always feasible for every common catalog cap, since T itself
is legal. It realizes the lowest possible current payoff
sum_T 1/(p_i+r_i). A strict improvement must use successor **incentives** or
another condition that can forbid this all-copy tuple. Adding further
necessary properties of individual legal topics alone cannot exclude it.

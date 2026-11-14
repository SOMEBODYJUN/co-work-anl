# Support — degree-two lift, sharp three-player point, and quotient boundary

## Core semantics

The fixed object has complete ordered policy tables for `(m,p)=(3,5),(4,6),(5,6)` and keeps every ordered history. The local rows are the finite intersection-cylinder inequalities; the global degree-2 lift uses one common nonnegative customer-type vector for all singleton/pair moments. It does not bind cubic moments, and the fixed-point LP objective is not a global strategy or customer-cone optimum.

## Exact point disposition

- `m3p5`: `x_{1}=1/3`, `x_{0,2}=1`, `x_{3}=1/3`; scale by 3 to five unit customers. All 124 nonself IC rows pass exactly, the policy uses only aliases 0/2, and the full-history strategy is a genuine SPE with `(W,OPT_3)=(3,5)`.
- `m4p6`: `t=(9/10)t*+(1/10)1`, fixed maximum coverage `19/10`; `Q(t)=0` and `P(t)=-1/10` for leaves 1,3,4.
- `m5p6`: `t=(24/25)t*+(1/25)1`, fixed maximum coverage `49/25`; `Q(t)=0` and `P(t)=-1/25` for leaves 0,1,3.

The cubic Boolean function
`P(z)=z_A-Σ_i z_Az_i+Σ_{i<j}z_iz_j-z_iz_jz_k`
is nonnegative on every customer type. Therefore the two latter tables cannot be moments of any common nonnegative customer population, even though their local rows, complete-policy IC rows and degree-2 lift rows pass.

## Migration boundaries

The duplicate-coverage quotient preserves the set of achievable ordered physical coverage paths, payoffs, welfare and `OPT` only after allowing a new complete strategy on quotient histories. It does not preserve a given alias-labelled policy table or fixed-label LP. The m3 point therefore transfers as a physical equality witness, while the fixed m4/m5 matrices remain label-level certificates.

The sharp theorem is universal for root three-player complete pure SPEs and has the same `(3,1,1)` equality family. The saved m3 point is a concrete alias-preserving realization of that family; it does not extend the theorem to four or five players.

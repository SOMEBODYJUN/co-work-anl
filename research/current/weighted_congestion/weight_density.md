# Resource-local weight density and approximate pure equilibria

Date: 2026-10-14 UTC. Research actor: R2. This account was reconstructed
from the exact model and the resource externality calculation, then independently
attacked internally. It is a structural upper bound, not a solution of WC-TARGET.

## Exact identities

### WC-R2-DENSITY-MOMENT v1

- **Objects/domain:** a finite multiset of positive real numbers
  `z_1,...,z_n`, real `R>1`, integer `K>=1`, real `0<p<1`.
- **Quantifiers/assumption:** every interval `[x,Rx)`, for every real `x>0`,
  contains at most `K` members, counting multiplicities.
- **Definitions:** `S=sum z_i`,
  `A_R(p)=(1-R^(-1))^p/(1-R^(-p))`.
- **Exact statement/conclusion:**

      sum z_i^p <= A_R(p) K^(1-p) S^p.

  For fixed `R,p,K`, this constant is the supremum over all such finite
  multisets. A nonempty finite multiset need not attain that supremum.
- **Scope/dependencies:** a real-variable moment inequality; it does not assume
  any game, rational input, or external theorem.
- **Evidence:** the finite telescoping proof below and an exact-arithmetic audit.
- **Objections:** half-open intervals and repeated values are essential to the
  sorting argument; both are handled explicitly. No unresolved fatal objection
  after the internal attack; no external review or global priority certification.
- **Status:** complete general proof, independently internally checked,
  unrefereed. This is a Canonical Record of the stated inequality, not a paper fact.

### WC-R2-WEIGHT-DENSITY v1

- **Objects/domain:** every finite weighted atomic congestion game in
  [MODEL](../../weighted_congestion_frontier/MODEL.md), integer `d>=1`;
  all weights may be arbitrary positive reals. Empty strategies, identically
  zero costs, and arbitrary finite multi-resource strategies are allowed.
- **Definitions:** `U_e={i: e belongs to at least one strategy of i}` and

      K_R = max_e sup_{x>0} |{i in U_e : x <= w_i < R x}|.

  For any `R>1`, `0<p<1`, set

      B = A_R(p) K_R^(1-p) d^p,
      alpha = 1+B,
      Psi(s) = sum_i w_i^p C_i(s).

- **Exact statement/quantifiers:** for every such game, every `R>1` and
  `0<p<1`, every unilateral local minimum of `Psi` is an `alpha`-PNE.
  Every unilateral move with `C_i(s)>alpha C_i(t_i,s_-i)` strictly decreases
  `Psi`; hence every sequence of these moves terminates in the finite state
  space. In particular an `alpha`-PNE exists. When `K_R=0`, nobody can use any
  resource, all costs are zero, and an exact PNE exists.
- **Scope:** a resource-local spectrum assumption, with no bound on the total
  number of players or on the number of resources in a strategy. There is no
  polynomial-time bound or general-real-arithmetic implementation claim.
- **Dependencies:** WC-R2-DENSITY-MOMENT v1, finite minimization, the elementary
  polynomial increment inequality proved below. No imported existence theorem
  is used in this proof.
- **Evidence:** the general proof, independent internal reconstruction/attack,
  literal rational game audits with rational power weights.
- **Objections:** `K_R` counts potential users, not merely current users; a
  minimum must protect all possible deviations. Counting distinct weights
  instead of players is invalid. Equal weights of arbitrarily high multiplicity
  make `K_R` unbounded. No general-class `o(d)` result follows.
- **Status:** complete general proof, independently internally checked,
  unrefereed. Priority outside the checked literature remains unverified.

Related files for both claims: the branch claim ledger, internal
[review](../../weighted_congestion_frontier/assets/R2/weight_density/review.md),
`tests/audits/weighted_congestion_density.py`,
`evidence/runs/2026-10-14/weighted_congestion_density.json`, and the original
derivation record `history/source/notes/weighted_congestion/density_externality.md`.

## 1. The moment inequality, using only finite sums

Sort the multiset in nonincreasing order. Put `q=1/R`. Whenever `j+K<=n`,

    z_(j+K) <= q z_j.                                      (1)

Indeed, if the inequality were strict in the other direction, the `K+1`
entries from `j` through `j+K` would all lie in `[z_(j+K),R z_(j+K))`.
Equality in (1) is allowed because the upper endpoint of this interval is
excluded. Split the sorted list into its `K` residue classes of indices.
Each nonempty class is a chain `a_1,...,a_m` with `a_(j+1)<=q a_j`.

For a single chain let `T_j=sum_(l=j)^m a_l` and `T_(m+1)=0`. The geometric
tail bound gives `T_j<=a_j/(1-q)`, so `t_j=a_j/T_j>=1-q`.
For `0<t<=1`, define

    H_p(t)= t^p / [1-(1-t)^p].

This is decreasing: for `0<t<1`, its derivative has the sign of
`1-(1-t)^(p-1)`, which is negative. Continuity covers `t=1`.
Consequently

    a_j^p
      = H_p(t_j) [T_j^p-T_(j+1)^p]
      <= A_R(p) [T_j^p-T_(j+1)^p].                         (2)

Summing (2) telescopes to `sum_j a_j^p<=A_R(p) T_1^p`.
If the totals of the `K` chains are `S_l>=0`, elementary concavity gives
`sum_l S_l^p<=K^(1-p)(sum_l S_l)^p`. This proves the claim, including
empty chains. The all-empty multiset has both sides zero.

For sharpness take `K` copies of every number `1,q,...,q^(m-1)`.
Every half-open `R` window contains at most one level and hence at most `K`
entries. The ratio of the left side to `S^p` is

    K^(1-p) A_R(p) (1-q^(pm))/(1-q^m)^p,

which tends to `K^(1-p) A_R(p)` as `m` tends to infinity. Sharpness here is
only sharpness of this moment inequality, not of the equilibrium factor.

## 2. A polynomial increment at its actual total load

For a resource newly acquired by player `i`, write `w=w_i` and let
`X=sum_(j currently on e) w_j` before the move. Its new load is `Y=X+w`.
For a monomial of degree `k<=d`,

    Y^k-X^k <= min(1, k w/Y) Y^k
             <= min(1, d w/Y) Y^k.                       (3)

For `k>=1`, this follows from `1-(1-u)^k<=ku`, `0<=u<=1`;
the degree-zero increment is zero. Multiply by each nonnegative coefficient
and sum to obtain

    0 <= c_e(Y)-c_e(X) <= min(1,d w/Y)c_e(Y).              (4)

This statement holds without division by `c_e(Y)`, so zero polynomials
cause no exceptional case.

Put `r_j=w_j/w` for the incumbents and `S=sum r_j=X/w`.
Their additional contribution to `Psi`, divided only by the positive `w^p`,
is bounded by

    min(1,d/(1+S)) (sum_j r_j^p) c_e(Y)
      <= A_R(p) K_R^(1-p)
         min(1,d/(1+S)) S^p c_e(Y)
      <= B c_e(Y).                                       (5)

The moment lemma applies to this subset of the potential users after
rescaling all weights by `w`. For the last inequality, if `S<=d` then
`S^p<=d^p`; if `S>=d` then
`d S^p/(1+S)<=d S^(p-1)<=d^p`. For `S=0` the externality is zero.

The new contribution of player `i` itself is `w^p c_e(Y)`.
Thus the total potential increase on this resource is at most
`(1+B)w^p c_e(Y)`.

## 3. An arbitrary multi-resource unilateral move

Let `D=s_i\t_i` be the removed resources, `A=t_i\s_i` the acquired resources,
and `H=s_i intersect t_i` the retained resources. Retained loads and costs
are unchanged. On removed resources, all incumbents' costs weakly decrease,
and the mover's contribution disappears. Therefore

    Psi(t_i,s_-i)-Psi(s)
      <= w_i^p [(1+B) sum_(e in A)c_e(new load)
                         -sum_(e in D)c_e(old load)].     (6)

Writing the retained-resource cost as `C_H>=0`, the bracket in (6) equals

    alpha C_i(t_i,s_-i)-C_i(s) -(alpha-1) C_H
      <= alpha C_i(t_i,s_-i)-C_i(s).                       (7)

If the deviation violates `alpha`-PNE, the right side is strictly negative.
This proves strict decrease, termination, and the local-minimum conclusion.
The proof covers an empty old or new strategy. In particular, a move to
zero cost from positive cost strictly decreases the potential; no `0/0`
ratio is used. Finiteness alone ensures that a global minimum exists even
for arbitrary real weights and coefficients.

For `d=0`, every resource cost is independent of other players; choosing
each player's cheapest strategy separately gives an exact PNE. This
separate endpoint is not obtained by assigning a meaningless logarithmic
power or a division by zero to the formulas above.

## 4. Consequences and the precise research frontier

For `d>=3`, choose `R=d` and `p=ln(2)/ln(d)`. Then `d^p=2`, so

    alpha = 1+4(1-1/d)^p K_d^(1-p) <= 1+4K_d.             (8)

This strengthens the preliminary geometric-band bound
`1+K_d(4+2/(1-2/d))`. The original expression is retained in the source
record, with its narrower preliminary status; it is not silently rewritten
as the same exact claim.

If on each resource the sorted potential-user weights obey
`w_(j+1)>=R0 w_j` for a fixed `R0>1` (one player at each level), then
`K_d<=ceil(ln(d)/ln(R0))`. Formula (8) gives `O(log d)`-PNE for every
such game. In particular it covers resource-local dyadic or stronger
geometric separation, uniformly in the number of players and arbitrary
multi-resource strategies. Multiplicities bounded by `K0` multiply this
count by at most `K0`.

More generally one may select `R,p` after reading the game's weights and
take the best stated factor. This is a mathematical finite minimization
guarantee, not a promise to efficiently compute a local minimum. For
`K_R` equal to a large equal-weight cohort, the density factor can be large;
the known universal `d` guarantee remains a separate literature baseline.

**Consequence for lower-bound design:** a polynomial replacement of the
binary/superincreasing step-function constructions, while keeping their
resource-local weight separation, has an `O(log d)` pure equilibrium
regardless of how its nonnegative polynomial coefficients are reassigned.
This is an existence constraint, stronger than merely showing that a
particular platform-preserving replacement cannot work. It does not
exclude lower bounds compatible with `O(log d)`, nor variants introducing
dense cohorts or destroying the separation condition.

**Still open:** WC-TARGET v1. The missing bridge is a mechanism that controls
dense groups of comparable weights without losing their exact equal-weight
congestion structure, and can coexist with interactions across scales.
The present positive linear cost selector has no such universal bridge.

## 5. Evidence, provenance, and the five independent assessments

- **Truth:** the two exact claims have finite, elementary general proofs.
  The internal reviewer first pursued a different mechanism, then attacked
  the displayed route and independently reconstructed the sharp moment bound.
- **Value:** the bound is uniform in player count on a well-defined structural
  class; it gives a genuine existence restriction on sparse-spectrum lower
  constructions and an explicit sufficient ordinal potential.
- **Novelty:** not certified. Searches on 2026-10-14 checked the original
  existence/nonexistence papers and queries for weight-density and sublinear
  existence bounds; this is not an exhaustive prior-art search.
- **Mechanism:** weak polynomial sensitivity is multiplied by a concave
  weight moment. Geometric separation bounds that moment relative to the
  actual total incumbent load.
- **Ambition:** structural progress only. No full-class `o(d)` upper bound,
  new infinite nonexistence family, or exact growth order is claimed.

The audit uses rational weights with rational `p`th powers and `Fraction`
throughout. It tests all unilateral moves on its finite games, including
retained resources, empty strategies, zero latencies, mixed degrees, repeated
weights, and exact geometric-window endpoints. General real parameters are
covered by the proof, not by those finite tests. The evidence file records
the exact ranges, seed, interpreter, and replay command.

Literature checked: Christodoulou et al., arXiv:2002.07466v3, Sections 2, 3,
6, 7; Caragiannis--Fanelli, arXiv:1902.07173, existence statement. The first
supplies the precise model and the separate `n`-PNE baseline; the second
supplies the separate `d` baseline. Neither is an unverified import in the
new proof.

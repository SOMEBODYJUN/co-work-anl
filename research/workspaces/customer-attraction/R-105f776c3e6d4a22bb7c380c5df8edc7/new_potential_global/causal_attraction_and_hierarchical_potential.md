# Causal attraction, extra insertion, and the unpaid hierarchical potential term

2026-10-24. Independent general-input attempt. Q-CAG-HALF remains **OPEN**.
All statements below use the original unit-customer, common-catalogue,
full ordered-history pure-SPE model. No statement changes the population,
catalogue, equilibrium quantifiers, or permissible tie breaking.

## 1. Actual-node definitions and exact scalar decomposition

Fix any legal ordered history h, with old customer loads b_x and r>=1
players left. Fix one complete pure SPE sigma on the original tree. Force
the current action to A and then follow the same sigma. Write Y_A for
the r-1 actual follower topics on that branch, and Z_A=(A,Y_A). The fixed
old prefix is retained in all payoff calculations.

Take any probability distribution p over legal topics. For one customer x
write

    I_A = 1_(x in A),       q = Pr_(A~p)(I_A=1),
    K_A = load_(Y_A)(x),    b = b_x.

Thus I_A is Bernoulli(q) and 0<=K_A<=r-1. The actual tree can correlate
I_A and K_A arbitrarily subject to its further SPE constraints. We do not
assume that K_A is an independent or frozen continuation.

For this customer define

    D_x = E_A I_A/(b+1+K_A),
    C_x^+ = q E_A 1/(b+1+I_A+K_A).

D_x is the source player's expected true payoff contribution. C_x^+
is the contribution of an independent extra query T~p to the complete
branch consisting of the old prefix and Z_A. Let

    F_A = 1/(b+1+K_A),
    J_A = 1/[(b+1+K_A)(b+2+K_A)].

Using 1/(b+1+I_A+K_A)=F_A-I_A J_A gives the exact identity

    D_x-C_x^+ = Cov(I_A,F_A) + q E_A[I_A J_A].          (1)

When 0<q<1 this is equivalently

    D_x-C_x^+
      = q(1-q)(E[F_A | I_A=1]-E[F_A | I_A=0])
        + q^2 E[J_A | I_A=1].                         (2)

At q=0 or q=1 use (1), so no conditional expectation on an empty event is
needed. The insertion term is nonnegative. If source coverage attracts
followers, the first conditional reciprocal can be smaller than the
second, producing a negative causal-covariance term. Neither term can be
discarded. Summing (1) over customers is only a decomposition, not a sign
theorem.

The current SPE comparison gives, for the same node's actual payoff u,

    u >= D := sum_x D_x.

Consequently the true local menu slack is

    u-C^+ = (u-D) + sum_x Cov(I_A,F_A)
                     + sum_x q E[I_A J_A].           (3)

Every object in (3) refers to real original branches. The IC slack u-D
cannot be silently omitted in a comparison to u.

## 2. Sharp envelope in the relaxed coordinate model

The following scalar bound holds without using follower rationality:

    C_x^+-D_x <= E_(b,r)(q),                          (4)

where

    E_(b,r)(q)
      = q(1-q)/(b+1) + q^2/(b+r+1) - q/(b+r).

Here b is any nonnegative integer, r>=1, and q in [0,1]. More generally
the proof only requires b>=0 and the stated integer tail-load interval.

Proof. Conditional on I_A=0, the contribution to C_x^+-D_x is

    q/(b+1+K_A),

which is decreasing in K_A and at most q/(b+1). Conditional on I_A=1,
the contribution is

    g(K_A) = q/(b+2+K_A)-1/(b+1+K_A).

This is increasing in K_A. One may see this by extending its argument
to a nonnegative real k and differentiating:

    g'(k) = 1/(b+1+k)^2-q/(b+2+k)^2 > 0.

It is therefore at most q/(b+r+1)-1/(b+r). Multiplying the two conditional
bounds by 1-q and q respectively proves (4). The endpoint q=0 causes
no problem; q=1 uses only the second bound. All denominators are positive.

For 0<q<1 and r>1, equality in this relaxed scalar problem is attained by

    K_A=r-1 when I_A=1,     K_A=0 when I_A=0.          (5)

Thus (4) is sharp over arbitrary joint distributions of (I_A,K_A) with
the stated coordinate ranges. A common catalogue need not permit the
coordinatewise prescription (5) simultaneously for all customers, and
even a compatible prescription need not be an SPE. No such realization
or sharpness over actual SPE is claimed.

The envelope has the useful exact form

    E_(b,r)(q) = a q-d q^2,
    a=(r-1)/[(b+1)(b+r)],
    d=r/[(b+1)(b+r+1)].                               (6)

For r>1 its maximizer on [0,1] and its maximum are

    q_*=(r-1)(b+r+1)/[2r(b+r)],
    E_max=(r-1)^2(b+r+1)/[4r(b+1)(b+r)^2].             (7)

Indeed q_* is in (0,1/2), since
(r-1)(b+r+1)=r(b+r)-(b+1). For r=1, (4) instead reduces
to the negative insertion term -q^2/[(b+1)(b+2)].

Equations (4)-(7) are unconditional algebra, not a new lower bound on W.
They isolate what information is missing when only load ranges and root
IC are retained: the extra source insertion does not itself dominate
arbitrary adaptive tail attraction.

## 3. Whole-tree harmonic expansion uses real IC but does not pay the remainder

Fix any current node h, source A, and a legal target tail
B=(B_1,...,B_(r-1)). For k=0,...,r-1 let P^k be the complete r-slot suffix
obtained by fixing the legal history

    (h,A,B_1,...,B_k)

and following the original sigma afterwards. In particular P^0 is the
true A branch and P^(r-1)=(A,B). For k>=1 let j be the player whose forced
action at that step is B_k. Actual full-history SPE gives

    gamma_k=u_j(h,P^(k-1))-u_j(h,P^k) >= 0.           (8)

Define the relative harmonic potential

    Phi_b(P)=sum_x sum_(ell=1)^(load_P(x)) 1/(b_x+ell).

The exact same-leaf marginal identity is

    u_j(h,P)=Phi_b(P)-Phi_b(P without j).

Hence

    Phi_b(P^k)-Phi_b(P^(k-1))
      = -gamma_k
        + Phi_b(P^k without j)-Phi_b(P^(k-1) without j). (9)

Summing (9) controls the actual whole-tail potential change by a sum of
deletion residuals after retaining every valid one-action IC. The last
residual is zero. Earlier residuals retain a ghost action in the actual
strategy history while deleting it only in the potential calculation.
They therefore do not form a smaller-player SPE.

This is the already recorded hybrid expansion, not a new proof:
[old exact remainder](../terminal_query/hybrid_ic_expansion.md).
The present attempt found no sign or jointly paid upper bound for these
mutually incompatible leaf residuals. Calling their sum a coalition or
potential debt would not add an inequality.

The integral representation

    1/(b+1+K)=integral_0^1 t^(b+K) dt

rewrites (1) as integrated causal covariance. It leaves the same sign
problem and creates no independent credit. Neither a harmonic nor an
entropy-style integral changes which branches the IC compares.

## 4. Stationary-flow attempt and its exact unsupported step

One can route a root topic to a chosen follower topic from its true
branch and take a stationary distribution on this finite directed map.
Stationarity balances the expected incidence of the source and the
chosen successor topic. It does not make their joint law with the full
branch load exchangeable. The denominators in (1) or (9) retain that
joint law.

This distinction is essential. The existing general model contains the
middle-incidence scalar pattern where root-to-tail stationary customer
incidences balance but the resulting root-minus-tail average coefficient
is negative; see [the explicit boundary](../../../../current/customer_attraction/extreme_maximal_membership_floor.md#6-一般目录的精确停界).
That pattern alone is not a full SPE. It does show why a new stationary
proof has to incorporate deeper genuine follower IC or other constraints
on ordered histories; a one-point stationary equation is insufficient.

An attempted claim that balancing the source and follower marginals
allows their reciprocal-load denominators to be exchanged is unsupported
and is not used here. No higher-order stationary-flow construction with
the required all-history consistency was obtained.

## 5. Candidate de-duplication and the required pressure test

The local all-p claim

    C^+(p) <= D(p)

would immediately pay (1), but it was recognized as already false from
the existing [complete-root-menu source](../../R-d22a706a03c5499d941a6a97f94128a8/induction/full_root_menu_mixed_obligations.md).
That source explicitly distinguishes this failed diagonal claim from the
weaker open free-mixing Mfull claim. Therefore no duplicate search was
run. The local comparison C^+<=u, aggregate FTA, Mfull, and Mpath have
different quantifiers; none is refuted here.

The same general envelope (7), evaluated at r=m=5 and b=0, gives

    q_*=12/25,        E_max=24/125>0.

This is the user's m=5 pressure test applied to the general derivation.
It says only that the relaxed covariance/insertion calculation still
permits an unpaid positive local deficit. It does not exhibit a legal
five-player SPE, does not establish a global deficit, and does not
disprove half or the open aggregate/full-menu candidates. No five-player
specialized coefficients, catalogue, or search were introduced.

## 6. Current stopping line

The all-input statements established in this note are (1)-(4) and the
sharp relaxed envelope (6)-(7). The full-tree expansion (8)-(9) is a
reconstruction of an existing exact identity. These do not prove
OPT_m<=2W, do not enlarge the known half-coverage range, and do not supply
the missing cross-tree payment.

A continued potential proof must use actual follower IC to constrain
the conditional load laws in (2), or pay the residuals in (9) jointly
without spending the same actual utility on incompatible leaves. Neither
bridge has been established in this attempt. No general impossibility,
target counterexample, external review, or novelty certification follows.

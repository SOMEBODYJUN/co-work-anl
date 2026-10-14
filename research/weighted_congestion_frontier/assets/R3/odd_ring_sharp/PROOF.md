# Odd hub/cohort rings: a growing lower bound and the exact certificate envelope

Authorship and provenance: the odd hub/cohort strategy construction was posted
by R1 in public-board message 42 (`aa0ccec68ec54eed9ce2e6b3c0e5c909`). R3 independently
reconstructed its full-state proof, then derived the scalar envelope and a
uniform-degree rational construction. Internal agents independently reconstructed
the coverage and attacked the parameter and envelope arguments; see the linked
reviews. This is unrefereed mathematical work. Global priority is not certified.

While this proof was being completed, R1 posted independently frozen message48
(`a3541c655682451584ef4a38c9b6c430`, commit `ba6fb27b6b5e1d5b00fe6fbb40178f1b5e334194`)
with a linear reset and the equivalent scalar function H_d(t). Substitution
R=1/t identifies sup H_d(t) with T_d exactly. Thus the d/ln d advancement is
a shared, independently reconstructed mechanism, not a claim that this R3
record alone originated that growth. Our additional exact upper bounds the
entire specified positive test system and our realizing construction uses only
degree-d monomials.

## 1. Exact claims and epistemic scope

**WC-R3-ODD-RING-CERTIFICATE-v1.** Fix integer d>=1, odd integer m>=3,
integers n_i>=1 and 1<=k_i<=d, positive real weights u_i,v_i, and alpha>1.
Indices are modulo m. Define x_i=v_i/u_i, t_i=v_i/u_(i+1), and

    N_i=(1+x_i)^k_i-alpha(n_i x_i)^k_i,
    M_i=alpha(1+n_i x_i)^k_i-1,
    P_i=alpha(1+t_i)^d-t_i^d,
    Q_i=(1+t_i)^d-alpha.

The two strict local tests in section 3 have positive resource coefficients
if and only if every N_i,Q_i is positive and

    G=product_i n_i N_i Q_i/(M_i P_i)>1.

These tests imply that the game in section 2 has no alpha-PNE. The iff describes
this sufficient test system, not all possible nonexistence proofs for the topology.

**WC-R3-ODD-RING-ENVELOPE-v1.** Put

    f_d(R)=[R(1+R)^d+1]/[(1+R)^d+R^(d+1)],
    T_d=sup_{R>1} f_d(R).

For fixed d>=2 and alpha>1, some finite odd ring can satisfy the above positive
test system if and only if alpha<T_d. The supremum is attained by the scalar
function, but the strict certificate does not attain alpha=T_d. Moreover,

    H_d<T_d<=H_d+1/(2^d+1),
    H_d=d/[(d+1)d^(1/(d+1))-d],
    T_d~d/ln d.

**WC-R3-ODD-RING-LOWER-v1.** For every integer d>=2 and every real
1<=alpha<T_d there is a finite game in MODEL's G_d, with positive rational
weights and coefficients and all latencies monomials of degree exactly d,
which has no alpha-PNE. Thus

    a_*(d)>=T_d,   liminf_{d->infinity} a_*(d) ln(d)/d>=1.

For each alpha a new finite game may be chosen. No one fixed finite game is
claimed to obstruct every alpha<T_d. This is a full-model lower bound, with
player count and resource support allowed to grow; no efficient input-size
construction or full-model upper bound is claimed.

Objects, domain, quantifiers, assumptions and definitions are exactly those
displayed here and in [MODEL](../../../MODEL.md). Conclusions concern weak
alpha-PNE inequalities; our witnesses strictly violate them. Dependencies are
elementary inequalities and the explicit construction, not an imported
existence theorem. General proofs establish the claims; finite computations
are supplementary evidence. The current proof and independent internal reviews
record no unresolved fatal objection in the stated scope. Novelty remains
unassessed globally. Value is the growing lower family and reusable certificate;
mechanism is odd parity plus multiplicative weight/coefficients feedback;
ambition is a lower-bound stage breakthrough, not resolution of WC-TARGET.

## 2. The actual game

Hub H_i has weight u_i. Cohort i contains n_i players L_ij of common weight v_i.
There are distinct resources A_i^b and B_ij^b for b in {0,1}, with fees

    c_(A_i^b)(z)=a_i z^k_i,
    c_(B_ij^b)(z)=b_i z^d,

where a_i,b_i>0 do not depend on the player using the resource or on b.
Hub H_i's action h uses A_i^h and every incoming B_(i-1),j^h.
Light L_ij's action l uses A_i^l and B_ij^(1-l).
Each player has exactly these two resource-subset strategies. Its weight is
the same on every resource; its cost is the sum of resource latencies, without
multiplying by weight. There are m+sum_i n_i players and 2m+2sum_i n_i resources.
All are finite. In particular this is neither a player-specific-cost game nor
a weighted-resource-demand model.

## 3. Coverage of every state and the coefficient cycle

If any light L_ij is aligned with its own hub, its current cost is at least

    a_i(u_i+v_i)^k_i+b_i v_i^d.

After flipping its action its cost is at most

    a_i(n_i v_i)^k_i+b_i(v_i+u_(i+1))^d.

The first bound allows all other cohort actions and either neighboring hub
action; the second includes the deviator and at most all n_i cohort members.
Consequently every aligned light has a strict alpha improvement if

    A_i N_i>B_i P_i,                       (L_i)

where A_i=a_i u_i^k_i and B_i=b_i u_(i+1)^d.

Otherwise all lights are anti-aligned with their own hubs. An odd binary ring
has an edge with h_(i-1)=h_i: if every adjacent pair differed, following all
m edges would flip the initial bit an odd number of times and not return it.
At this edge H_i has current and flipped costs exactly

    a_i u_i^k_i+n_(i-1)b_(i-1)(u_i+v_(i-1))^d,
    a_i(u_i+n_i v_i)^k_i+n_(i-1)b_(i-1)u_i^d.

It therefore strictly improves if

    n_(i-1) B_(i-1) Q_(i-1)>A_i M_i.       (H_i)

This proves all-state nonexistence from the local tests; it is stronger than
finding a cycle of improving states. All constructed current/deviation costs
are positive, so no 0/0 convention is used. Empty strategies and zero fees
permitted in MODEL do not impose additional obligations on this positive
subclass construction.

M_i,P_i are positive for alpha>1. Positive A_i,B_i satisfying (L_i),(H_i)
force N_i,Q_i>0 and

    B_i<R_i B_(i-1),
    R_i=n_(i-1)Q_(i-1)N_i/(M_i P_i).

Multiplication proves G=product_i R_i>1. Conversely suppose these signs and
G>1 hold. Let delta=(G-1)/(2mG). Set B_0=1 and, successively for i=1,...,m-1,

    B_i=(1-delta) R_i B_(i-1).

Bernoulli's inequality gives

    G(1-delta)^m >= G(1-m delta)=(G+1)/2>1.

It follows that the wrap edge also satisfies B_0<(1-delta)R_0 B_(m-1),
and hence all B_i<R_i B_(i-1). Choose A_i as the arithmetic midpoint between
B_i P_i/N_i and n_(i-1)B_(i-1)Q_(i-1)/M_i. Both tests are strict. Recover
a_i=A_i/u_i^k_i and b_i=B_i/u_(i+1)^d. All quantities are positive rationals
if weights, alpha and x_i,t_i are rational. This is a constructive coefficient
formula with no root extraction and no unspecified feasibility oracle.

## 4. The exact necessary envelope

Let y=n x and define, for alpha>1,

    F_(k,n)(x)=n x[(1+x)^k-alpha(n x)^k]/[alpha(1+n x)^k-1].

On a positive certificate edge,

    F_(k,n)(x)<=F_(k,1)(n x),
    Q/(tP)=F_(d,1)(1/t).

The first inequality uses 1+x<=1+n x and the common positive denominator.
The second is obtained by multiplying numerator and denominator by t^(-d).
Also, for every y>0,

    F_(k,1)(y)>1  iff  alpha<f_k(y).

For 0<y<=1, f_k(y)<=1: after multiplying out, this says
(1+y)^k>=sum_{j=0}^k y^j, which holds since every binomial coefficient is >=1.
For y>1, f_k(y) increases in k. To check this without an imported theorem,
write A=(1+y)^(-k), B=(y/(1+y))^k. The numerator of f_(k+1)-f_k, after
using the positive denominators, is

    [A y/(1+y)] [y^(k+1)-1-(y-1)B]>0.

Indeed y^(k+1)-1=(y-1)sum_{j=0}^k y^j>(y-1)B.
Therefore f_k(y)<=T_d for every k<=d,y>0.
If alpha>=T_d every F_(k,1)(y)<=1. Since

    product_i x_i=product_i t_i,
    G=product_i [x_i n_i N_i/M_i] [Q_i/(t_i P_i)],

the preceding inequalities imply G<=1, a contradiction. Thus every positive
certificate has alpha<T_d. This argument does not construct an alpha-PNE
when the certificate fails; it does not upper-bound the actual topology or a_*.

For d>=2, the binomial argument is strict when R>1, so f_d(R)>1 there.
At R=1 and as R tends to infinity its value tends to 1. Continuity therefore
puts the supremum at a finite interior R>1. For d=1 the function is identically 1.

## 5. Rational attaining families below the envelope

Fix integer d>=2 and a real 1<=alpha<T_d. Continuity and density of the
rationals allow rational a,R such that alpha<a<f_d(R), R>1. Write

    E=(1+1/R)^d,
    q=(E-a)/(aE-R^(-d)),
    B=ceil(4ad).

One has 0<q<1 and Rq>1. In fact a<f_d(R) is precisely Rq>1 after multiplying
by positive denominators. Also f_d(R)<E since R^(-d)<E^2, so E>a.
Choose an odd m>=3 such that, with ell=2m-1,

    (Rq)^ell>12Ba.                         (S)

Such m exists because Rq>1; this strict rational inequality is an effective
parameter-selection rule. Define

    u_0=R^ell, v_0=1,
    u_i=R^(2i-1), v_i=R^(2i)  (1<=i<m),
    n_0=floor(R^ell/B), n_i=1 (1<=i<m), k_i=d (all i).

Then x_0=R^(-ell), x_i=R for i>=1, and every t_i=1/R, including the wrap
edge. In particular product_i x_i=product_i t_i is exactly realized by the
actual resource-independent weights. At ordinary nodes N_i/M_i=q; at every
outgoing edge Q_i/P_i=q. Hence

    G=n_0 (N_0/M_0) q^ell.

Because q<1, (S) implies R^ell>12Ba>2B. Thus n_0>=R^ell/(2B)>=1. Moreover

    n_0 x_0<=1/B,
    N_0>=1-a/B^d>=1-a/B>=3/4>1/2,
    M_0<a(1+1/B)^d<=a exp(d/B)<e a.

The last inequality uses B>=4ad and a>1. It follows that

    G>(Rq)^ell/(4Bea)>3/e>1.

All N,Q,M,P are positive. Section 3 now constructs positive rational
coefficients and proves no a-PNE, and therefore no alpha-PNE, at every state.
Every latency has degree exactly d. The family need not have polynomial
size in d or in the precision of alpha; no such claim enters MODEL's threshold.

## 6. Growth and sharpness of this certificate's leading constant

Write

    f_d(R)=g_d(R)+1/[(1+R)^d+R^(d+1)],
    g_d(R)=R/[1+R(R/(1+R))^d].

For d>=2 differentiation gives the unique maximizer

    R*=1/[d^(1/(d+1))-1]>1,
    max_{R>0} g_d(R)=H_d=d/[(d+1)d^(1/(d+1))-d].

Indeed the derivative has the sign of 1-d(R/(1+R))^(d+1); it changes from
positive to negative at R*. For R>1 the extra term lies in (0,1/(2^d+1)),
giving H_d<T_d<=H_d+1/(2^d+1). Taylor expansion with z=ln d/(d+1)->0 gives

    (d+1)exp(z)-d=1+ln d+O((ln d)^2/d),

so T_d~d/ln d. This asymptotic is for all integer d, not just a sparse
subsequence. Section 5 gives a_*(d)>=T_d at every d>=2. Combined with the
verified literature upper bound a_*(d)<=d, a logarithmic gap remains.

An independent budget proof is useful for reuse. Set tau=alpha^(1/d)-1 and
y_i=n_i x_i. N_i>0 gives y_i<1/tau; Q_i>0 gives t_i>tau. Then

    x_i n_i N_i/M_i <1/[(alpha-1)tau],
    Q_i/(t_i P_i)  <1/[(alpha-1)tau].

Thus G>1 requires (alpha-1)(alpha^(1/d)-1)<1, which implies
(alpha-1)ln alpha<d. This confines the certificate to leading scale
(1+o(1))d/ln d, consistent with the exact envelope. It is not a full-model
existence result.

For d=1, f_1(R)=1 identically and no alpha>1 certificate is possible. For
d=0 the stated positive-degree input class is empty. Even rings do not supply
the parity step; the alternating all-anti profile evades this coverage proof.
Neither failing local tests nor a tool failure implies equilibrium existence.

## 7. Evidence, comparison, and remaining obligations

The published nonexistence baseline is Theorem 1 / formula (3) of
[Christodoulou et al., arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3),
explicitly exhibiting Omega(sqrt(d)/ln d). The recovered R3 proof of that
same formula's sharp envelope is (2/sqrt(e))sqrt(d ln ln d)/ln d. Both are
strictly smaller in order than T_d~d/ln d. The source-envelope improvement
is a separate joint dependency for comparison with its exact supremum; this
new lower proof does not depend on it.

The upper d and the finer finite-degree potential factor are checked in
[Caragiannis--Fanelli, arXiv:1902.07173v5, Theorem 2](https://arxiv.org/html/1902.07173v5).
The literature audit records later sources and scope; the search did not
discover a stronger same-model growing lower bound, but does not certify
global firstness. Arbitrary nondecreasing-cost step lower bounds, bounded
weight-ratio algorithms, and price-of-anarchy/stability bounds have different
quantifiers and cannot be substituted as this nonexistence baseline.

Reproducible exact tests are in `verify.py` / `verification.json`; clean
strategy reconstruction is in `../odd_ring_independent/verify_literal.py`.
Independent reviews are `../odd_ring_independent/REVIEW.md`, its separate
`EXACT_ENVELOPE_REVIEW.md`, and `../odd_ring_parameters/exact_envelope_review.md`.
Tests check rational inequalities and full states of small actual games;
they do not enumerate the huge growing family and do not replace this proof.

WC-TARGET remains OPEN: the next obligation is a full-class O(d/ln d)
existence bound or a stronger all-state mechanism exceeding this certificate
envelope. Raising ring length or tuning its monomial degrees cannot bypass
the proved positive-test-system envelope. Resources involving many players,
extreme rational scales and a low-total-weight large cohort are the present
amplification mechanism; minimum potential-user density alone was already
shown nonrestrictive by the separate padding theorem.

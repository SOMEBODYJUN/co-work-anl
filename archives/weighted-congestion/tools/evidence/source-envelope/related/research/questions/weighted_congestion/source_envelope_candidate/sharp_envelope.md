# 文献两攻击公式：锐渐近的另一份候选推导

Author: R1/lower_family, with independent internal reconstruction by
R1/lower_family/asymptotic_attack and R1/root. Date: 2026-10-14.

**Status:** complete candidate proof, internally attacked; not externally reviewed.
Novelty is not certified. This evaluates the parameter supremum already present in
Christodoulou–Gairing–Giannakopoulos–Poças–Waldmann, arXiv:2002.07466v3,
Theorem 1, equation (3). It improves the *explicit asymptotic estimate printed in
that paper* by an unbounded factor of order sqrt(log log d); it does **not** exceed
the paper's exact parameter supremum, and is not a new universal existence bound.

## Claim identity and scope

- ID/version: WC-R1-LF-SHARP v1.
- Objects: the two-ratio certificate for the heavy/light game defined below.
- Domain: integer d≥2; n≥1 integer; k in {1,…,d}; real 0<w≤1,
  0≤β≤1. The excluded w=0 is outside WC-TARGET; the paper allows it in the
  optimization. At w=0 the heavy ratio is 1, so including its well-defined boundary
  values cannot affect the asymptotic conclusion.
- Quantifiers/conclusion: if F_d is the supremum over this domain of min(R_H,R_L),
  then

      F_d = (2/sqrt(e)+o(1)) sqrt(d log log d)/log d   as integer d→∞.

  Consequently, for each fixed 0<c<2/sqrt(e), there is d_c such that for every
  integer d≥d_c the explicit game below has no α-PNE for any
  1≤α<c sqrt(d log log d)/log d.
- Assumptions/definitions: all logarithms are natural; α-PNE uses the non-strict
  inequalities of MODEL.md; nonexistence is asserted only below a strict cutoff.
- Dependencies: the source supplies the strategy architecture and equation (3).
  The all-state argument is reconstructed here. All asymptotic analysis below is
  a new derivation in this session. The independent note
  `../envelope_ceiling/README.md` supplies a complementary finite necessary
  condition; the proof here is also self-contained.
- Evidence: general proof below; `verify.py` and `verification.json` give exact
  rational state checks and high-precision Decimal samples. Tests are not proofs.
- Counterevidence/objections: no proof of novelty; no claim that F_d is the exact
  worst equilibrium factor even for this architecture; no bound on the full
  WC-TARGET threshold from above; no new architecture.
- Related files: `verify.py`, `verification.json`, `source_audit.md`.

## 1. All-state interface and exact state formulas

There is a weight-1 player and n weight-w players. Resources are
a_0,…,a_n,b_0,…,b_n. Main resources a_0,b_0 have cost x^k, and every other resource
has cost βx^d. The heavy player chooses all a-resources or all b-resources. Light
player i chooses {a_0,b_i} or {b_0,a_i}. These are finite games in WC-TARGET, with
positive player weights and nonnegative polynomial coefficients.

By swapping a and b, orient the heavy player on side a. Let m be the number of
light players using a_0. Every state is represented by one m in {0,…,n}; identities
of the light players do not affect costs. Put t=(1+w)^d and q=βt. The exact
current/deviation ratios are:

| Player type | Current cost | Cost after its only different strategy |
|---|---|---|
| Heavy | (1+mw)^k+(n−m)q+mβ | (1+(n−m)w)^k+mq+(n−m)β |
| Light on heavy side, m≥1 | (1+mw)^k+βw^d | ((n−m+1)w)^k+q |
| Light opposite heavy, m≤n−1 | ((n−m)w)^k+q | (1+(m+1)w)^k+βw^d |

All denominators in these formulas are positive in the stated domain. The first
row at m=0 gives

    R_H = (1+nβ(1+w)^d)/((1+nw)^k+nβ).

For every m≥1, the second row is at least

    R_L = ((1+w)^k+βw^d)/((nw)^k+β(1+w)^d),

because its numerator increases and denominator decreases with m. Thus every
state has an available deviation with ratio at least min(R_H,R_L). For every
α<min(R_H,R_L), this deviation violates C_i(s)≤αC_i(t_i,s_−i) strictly.

This closes **all** states, rather than merely giving a cycle. The exact table
also gives an independent reusable interface: the game's best equilibrium
factor equals the minimum over m=0,…,n of the maximum of 1 and all available
ratios in the corresponding row types. The two-ratio lower certificate can be
strictly weaker than this exact minimax expression. We do not optimize that
larger expression here.

## 2. Explicit parameter sequence and lower asymptotic

Write

    D=log d, H=log D, S=sqrt(dH)/D, h=H−log(2H).

For all sufficiently large integer d, define

    w = D/(2d),
    n = floor(4dH/D²),
    k = ceil(D/(2h)),
    q = sqrt(e)/(2S),
    β = q/(1+w)^d.

Here h>0, n≥1, 1≤k≤d, 0<w≤1, and 0<β≤1 for sufficiently large d. Indeed
h/H→1, n→∞, k=O(D/H)=o(d), w→0, q→0 and (1+w)^d≥1. This verifies the
legal game domain without using zero weights or a limiting game.

Let x=nw. The floor error is at most w, and the ceiling error at most 1, so

    x ~ 2H/D,       kx→1,       kw→0.

Since dw=D/2 and dw²=D²/(4d)→0,

    (1+w)^d ~ sqrt(d),    (1+x)^k→e,    (1+w)^k→1.

The choice of the ceiling gives the particularly useful one-sided estimate

    x^k ≤ (2H/D)^k = exp(−hk) ≤ exp(−D/2)=d^(−1/2)=o(q).

Finally,

    nq ~ 2sqrt(e) S,
    nβ = nq/(1+w)^d ~ 2sqrt(e) sqrt(H)/D →0,
    βw^d ≤ β →0.

Consequently

    R_H/S → 2/sqrt(e),
    R_L/S → 2/sqrt(e).

For the second limit one may note βw^d/q=(w/(1+w))^d→0, while q→0 and the
main numerator tends to 1. Each d specifies one finite game which excludes
*all* α below its certificate. No attainment of the global supremum is used.

### Optional explicit finite threshold

For integer d with H≥4 the same formula guarantees

    min(R_H,R_L) > S/32.

Here are elementary bounds to make the quantifier effective. Since
h≥(2/5)H for H≥4 and 2H/D≤8/e^4<1/2, we have
kx≤H/h+2H/D≤3, hence (1+x)^k≤e³. Also k≤D≤d, the unrounded n is at least 2,
and nq≥sqrt(e)S. The logarithmic bound log(1+w)≥w−w²/2 yields
(1+w)^d≥sqrt(d)exp(−D²/(8d)). For D≥e^4, D²/(8d)<1/2, so
nβ≤2e sqrt(H)/D≤4/e³<1. Thus

    R_H ≥ sqrt(e)S/(e³+1) > S/32.

Moreover d^(−1/2)≤q, so R_L≥1/(2q)=S/sqrt(e)>S/32.
The positivity and β≤1 checks follow from
q≤D/sqrt(d)≤1 for D≥e^4. A fully explicit valid starting degree is
ceil(exp(exp(4))); the sharp constant statement only needs eventual validity.

## 3. Parameter elimination for an upper bound on the certificate

Take any legal parameters and put R=min(R_H,R_L)>2. Let

    t=(1+w)^d, q=βt, A=(1+nw)^k, B=(1+w)^k,
    y=nw/(1+w), L=log R, ε=(w/(1+w))^d.

We have 0≤ε<1. The heavy inequality implies

    1+nq ≥ R(A+nq/t) ≥ RA,
    nq ≥ RA−1 ≥ (R−1)A.                         (1)

The light inequality implies

    B+εq ≥ R((nw)^k+q),
    q ≤ B/(R−ε) ≤ B/(R−1),
    (nw)^k < B/R.                              (2)

Combining (1) and (2),

    (R−1)² ≤ nB/A,     0<y<1,
    k ≥ L/log(1/y).                            (3)

The strict bound in (2) is valid because R>2 forces q>0 by (1). Also
R_H<t: its denominator times t is tA+nq>1+nq. Therefore t>R.
The identities

    (1+nw)/(1+w)=1+(1−1/n)y,
    t=(1−y/n)^(−d)

give the exact further restriction

    n < y/(1−exp(−L/d)).                       (4)

These statements concern the two-ratio certificate, not arbitrary games.

## 4. A coarse bound needed for uniform asymptotics

For completeness, the following elementary argument proves R=O(S) uniformly
over legal parameters. The case R≤e is harmless because S→∞. If n=1 then
A=B and (3) gives R≤2, so assume n≥2.

Since 0<y<1,

    log(A/B)=k log(1+(1−1/n)y) ≥ ky/3.

The inequality log(1+w)≤w and t>R give w>L/d. As w≤1,

    n=y(1+w)/w ≤2dy/L.

Consequently

    (R−1)² ≤ (2d/L) sup_(0<y<1)
                   y exp(−Ly/[3 log(1/y)]).    (5)

For y≤1/L, the expression inside the supremum is at most 1/L.
For y≥1/L, log(1/y)≤log L, and the standard elementary maximum
max_(u>0) u exp(−bu)=1/(eb) bounds it by 3log L/(eL).
Thus, for L>1, the right side of (5) is
O(d(1+log L)/L²), with absolute constants.

We also have (R−1)²≤n≤2d/L, so L=O(D). If R≥d^(1/4), then L≥D/4 and
log L≤H+O(1); (5) now gives R=O(S). If R<d^(1/4), the same conclusion is
immediate since d^(1/4)=o(S). This proves the promised uniform coarse bound.
The root agent's independent finite ceiling note records explicit constants.

## 5. Uniform one-dimensional asymptotic lemma

Let L_j→∞ and a_j→1 with 0<a_j≤1. Define

    f_(L,a)(y)=y exp(−L log(1+ay)/log(1/y)),  0<y<1.

Then

    sup_(0<y<1) f_(L_j,a_j)(y) ~ log L_j/(eL_j).                (6)

Proof. Suppress the index j. Split the domain into three parts.

1. If 0<y≤1/L, f≤1/L=o(log L/L).
2. If 1/L≤y≤L^(−1/2), uniformly on this interval
   log(1+ay)≥(1−o(1))y, because a→1 and y→0 uniformly. Also
   log(1/y)≤log L. Therefore

       f≤y exp(−(1−o(1))Ly/log L)
        ≤(1+o(1))log L/(eL).

3. If L^(−1/2)≤y<1, the quotient log(1+ay)/log(1/y) increases with y:
   its positive numerator increases and positive denominator decreases.
   At the left endpoint it is (2−o(1))/(sqrt(L)log L). Since y≤1,

       f≤exp(−(2−o(1))sqrt(L)/log L)=o(log L/L).

For the matching lower bound, take y=log L/L. Then
L log(1+ay)/log(1/y)→1, yielding f~log L/(eL). All o(1) terms above are
uniform on their indicated subintervals, for each arbitrary sequence a_j→1.

## 6. Sharp upper bound, including the supremum quantifier

Fix any c>0 and consider any sequence of legal parameters, indexed by degrees
d_j→∞, whose certificates satisfy R_j≥cS_j. The coarse bound gives
R_j=Θ(S_j), hence

    L_j~D_j/2,    log L_j~H_j,    L_j/d_j→0.

Equation (3) implies n_j≥(R_j−1)²→∞, so a_j=1−1/n_j→1.
Combining (3), (4), and k≥L/log(1/y),

    (R_j−1)²
      ≤ [1/(1−exp(−L_j/d_j))] f_(L_j,a_j)(y_j)
      ≤ (1+o(1))(d_j/L_j) [log L_j/(eL_j)]
      = (4/e+o(1)) S_j².

Since R_j→∞, this proves limsup R_j/S_j≤2/sqrt(e).

To pass from parameter sequences to F_d, suppose for contradiction that
limsup F_d/S_d>2/sqrt(e). Some ε>0 and infinitely many degrees then have
F_d>(2/sqrt(e)+2ε)S_d. By the definition of a supremum, for each such d
there are legal parameters with R>(2/sqrt(e)+ε)S_d; no supremum attainment is
required. This sequence contradicts the preceding bound. Thus
limsup F_d/S_d≤2/sqrt(e). The explicit construction gives the reverse liminf,
proving the claim.

## 7. What this does and does not settle

The analysis identifies the sharp first-order behavior of the **published
certificate envelope**, and explains the hidden log-log gain: total light mass
nw is tuned to 2 log log d/log d, making the heavy main-resource burden tend to
e while retaining about 4d log log d/(log d)² light players.

The full all-state minimax formula in Section 1 has not been upper-bounded here.
Alternative designated attacks in intermediate states, asymmetric costs,
heterogeneous light weights, or additional heavy players might surpass F_d.
The universal threshold a_*(d) could also be much larger. Conversely, the
result already implies the stated stronger lower rate for a_*(d), because
every parameter instance is a valid game and every state is covered.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。

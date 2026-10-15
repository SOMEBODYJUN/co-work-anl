# Independent literal-cost attack of the odd ring

## Audit identity and result

- **Claim ID/version:** `R1-ODD-RING-INDEPENDENT-v1`.
- **Objects/domain:** weighted atomic congestion games under `MODEL.md`, positive monomial coefficients, positive player weights, integer degrees at most `d`; a player's cost is the sum of latencies without an additional weight factor.
- **Scope:** the odd-ring family specified below, rather than all congestion games.
- **Quantifiers/conclusion:** the sufficient inequalities imply that **every** pure state has a strictly alpha-improving individual deviation. The degree-10 fixture below has no 2-PNE.
- **Dependencies:** literal strategy incidence, group permutation symmetry, odd-cycle parity, elementary positive-product feasibility. No improvement-cycle argument is used.
- **Evidence:** exact Fraction verification of all 62,240 count states, representing all `2^1949` labelled states, and a symbolic all-state certificate.
- **Counterevidence/objections:** the anticipated missing hub baseline is present in the candidate's `Q`; the explicitly supplied fixture passes the attack. A growing-ring argument must control its product loss uniformly in `m`.
- **Status:** finite fixture verified exactly; the asymptotic sufficient family below is independently derived and still requires the overall project's novelty/literature review.
- **Related files:** `MODEL.md`, `attack.py` in this directory.

The primary comparison is Christodoulou, Gairing, Giannakopoulos, Poças and Waldmann, [arXiv:2002.07466v3](https://arxiv.org/pdf/2002.07466v3), Section 3/Theorem 1. Its gadget has one heavy player and `n` equal light players. The two ratios in its Theorem 1 agree with the `m=1` specialization of the sufficient ratios below. This audit reconstructs the ring directly rather than assuming the paper's symmetry reduction applies to a heterogeneous ring.

## Literal costs, including all baseline terms

Indices are cyclic. Group `i` has `n_i` lights of weight `v_i`, and hub `H_i` has weight `u_i`. Main resource `A_i^b` has latency `a_i x^{k_i}`; each side resource `B_ij^b` has latency `b_i x^{d_i}`. The strategies are

\[
H_i(h)=\{A_i^h\}\cup\{B_{i-1,j}^{h}:1\le j\le n_{i-1}\},
\qquad L_{ij}(\ell)=\{A_i^\ell,B_{ij}^{1-\ell}\}.
\]

Let `c_i(b)` count group-`i` lights on bit `b`, so `c_i(0)+c_i(1)=n_i`. For a light currently on bit `ell`, its literal current and post-deviation costs are

\[
C_L=a_i(c_i(\ell)v_i+u_i\mathbf1_{\ell=h_i})^{k_i}
+b_i(v_i+u_{i+1}\mathbf1_{1-\ell=h_{i+1}})^{d_i},
\]

\[
C_L'=a_i((c_i(1-\ell)+1)v_i+u_i\mathbf1_{1-\ell=h_i})^{k_i}
+b_i(v_i+u_{i+1}\mathbf1_{\ell=h_{i+1}})^{d_i}.
\]

The `+1` is mandatory: the deviating light enters the other main resource. It also remains on one of its own side resources, so the side load always includes `v_i`.

For hub `i`, put `c=c_i(h_i)` and `r=c_{i-1}(1-h_i)`. Its two literal costs are

\[
C_H=a_i(u_i+c v_i)^{k_i}
+b_{i-1}[r(u_i+v_{i-1})^{d_{i-1}}+(n_{i-1}-r)u_i^{d_{i-1}}],
\]

\[
C_H'=a_i(u_i+(n_i-c)v_i)^{k_i}
+b_{i-1}[(n_{i-1}-r)(u_i+v_{i-1})^{d_{i-1}}+r u_i^{d_{i-1}}].
\]

Thus every hub pays the unavoidable side baseline `n_(i-1)b_(i-1)u_i^{d_(i-1)}` on both strategies. This is included throughout.

## A sufficient certificate covering every state

Normalize

\[
x_i=v_i/u_i,\quad t_i=v_i/u_{i+1},\quad q_i=a_i u_i^{k_i},\quad p_i=b_i u_{i+1}^{d_i}.
\]

For a target `alpha >= 1`, define

\[
N_i=(1+x_i)^{k_i}-\alpha(n_i x_i)^{k_i},\quad
M_i=\alpha(1+n_i x_i)^{k_i}-1,
\]
\[
P_i=\alpha(1+t_i)^{d_i}-t_i^{d_i},\quad
Q_i=(1+t_i)^{d_i}-\alpha.
\]

The sufficient system is

\[
q_iN_i>p_iP_i\quad\text{for every }i,\qquad
n_{i-1}p_{i-1}Q_{i-1}>q_iM_i\quad\text{for every }i.\tag{S}
\]

To prove coverage, first suppose any light shares its own hub's main bit. Its current main load is at least `u_i+v_i`, its current side load at least `v_i`, its deviating main load at most `n_i v_i`, and its deviating side load at most `u_(i+1)+v_i`. The first inequality of (S) therefore gives a strictly alpha-improving deviation for that light, regardless of every other group's configuration.

Otherwise all lights use bit `1-h_i`. On an odd ring there is an `i` with `h_i=h_(i-1)`. That hub has an empty main resource and collides with **all** previous-group lights on its sides. Its exact costs are

\[
C_H=q_i+n_{i-1}p_{i-1}(1+t_{i-1})^{d_{i-1}},\quad
C_H'=q_i(1+n_ix_i)^{k_i}+n_{i-1}p_{i-1}.
\]

The second inequality of (S) says exactly `C_H > alpha C_H'`. The baseline is responsible for the `-alpha` in `Q`, rather than merely `-1`.

## Coefficient and weight consistency

For positive `N_i,Q_i` (and hence positive denominators in the nondegenerate setting here), coefficients satisfying (S) exist **if and only if**

\[
\prod_i R_i>1,\qquad
R_i=\frac{n_i N_i Q_i}{P_iM_{i+1}}.\tag{C}
\]

Indeed, the permissible interval for `p_i` is

\[
\frac{q_{i+1}M_{i+1}}{n_iQ_i}<p_i<\frac{q_iN_i}{P_i},
\]

which is nonempty exactly when `q_(i+1)/q_i < R_i`. Multiplication proves necessity. For an explicit sufficient construction set `rho=(product R_i)^(1/m)>1`, `q_0=1`, and `q_(i+1)=q_i R_i/rho`; the product-one condition closes the cycle. Take `p_i` to be the midpoint of the displayed open interval. With rational data, rational coefficients may alternatively be chosen by density. Recover actual coefficients as `a_i=q_i/u_i^{k_i}` and `b_i=p_i/u_(i+1)^{d_i}`.

This equivalence concerns this **sufficient certificate**, not a necessary characterization of every nonexistence instance in the family.

Independently, realizable weight ratios must satisfy

\[
\prod_i x_i=\prod_i t_i.\tag{W}
\]

It is also sufficient: take arbitrary `u_0>0`, propagate `u_(i+1)=u_i x_i/t_i`, and set `v_i=x_i u_i`. Therefore independently optimizing all `x_i,t_i` without (W) would be invalid.

## Exact attack of the supplied degree-10 fixture

The supplied data are

\[
t=1/6,\quad u=(1,t^4,t^2),\quad v=(t^5,t^3,t),\quad
n=(1944,1,1),\quad k=(2,10,10),\quad d_i=10,\quad\alpha=2.
\]

Here `x=(t^5,1/t,1/t)` and every `t_i=t`, so (W) holds. Exact values are

\[
N=(52923457/60466176,161542897,161542897),\quad
M=(17/8,564950497,564950497),
\]
\[
P_i=564950497/60466176,\qquad Q_i=161542897/60466176.
\]

The coefficient product is

\[
\prod_i R_i=
\frac{5822205627009247064806722143568473674042250846449}
{3803883021016715937113819138173711735906644378672}
\approx1.5305953402986263>1.
\]

A simple rational feasible choice is

\[
q=(1,1/1250000,3/50000000),\qquad p=(9/100,13,9/10).
\]

The exact positive slacks are:

| Group/hub `i` | Light slack `q_iN_i-p_iP_i` | Hub slack `n_(i-1)p_(i-1)Q_(i-1)-q_iM_i` |
|---|---:|---:|
| 0 | `207791227/6046617600` | `18775537/67184640` |
| 1 | `36714729081367/4723920000000` | `16704323717/1080000000` |
| 2 | `6737623888291/5248800000000` | `19700738291653/23619600000000` |

The actual positive rational coefficients are

\[
a=(1,835468408677733379239927873536/78125,85691213438976/390625),
\]
\[
b=(30076862712398401652637403447296/25,47530059720818688,9/10).
\]

Running `python attack.py --enumerate` independently computes the literal current/post-deviation costs for every available individual type at every count state. Each hub bit vector and each tuple of group zero-counts is considered. Permutations of equal lights are exact symmetries, so this covers all labelled states rather than sampling them.

- Count states checked: `2^3*(1944+1)*2*2 = 62240`.
- Labelled states represented: `2^1949`.
- 2-PNE: zero.
- Certificate's light branch: 62,232 count states; hub branch: 8 count states.
- Exact best equilibrium factor for these particular coefficients:
  `1434444625245301/707371943476824 = 2.027850607411458...`.
- A minimizing state has hub bits `(0,1,1)` and group zero-counts `(0,1,1)`; its maximum improvement is hub 2's deviation.

The result is a successful finite nonexistence certificate, not a fatal counterexample to the candidate.

## Independent uniform asymptotic sufficient family

The consistency equations admit an elementary uniform family. For integer `d>=4096` and any odd `3<=m<=d`, put

\[
K=\lceil\ln d\rceil,\quad t=8K/d,\quad
u_0=1,\quad u_i=t^{2(m-i)}\ (1\le i<m),\quad v_i=t u_{i+1},
\]

\[
x_0=t^{2m-1},\quad x_i=1/t\ (i>0),\quad
n_0=\left\lfloor\frac1{K t^{2m-1}}\right\rfloor,\quad n_i=1\ (i>0),
\]

\[
k_0=K,\quad k_i=d\ (i>0),\quad d_i=d,\quad
\alpha=\frac{d}{8K}(16d)^{-1/(2m)}.
\tag{F}
\]

All weights are positive rational, and weight consistency holds by construction. Write `T=(1+t)^d`. The following bounds establish coefficient feasibility:

1. `0<t<1`, `alpha<1/t<d`, and `T>=exp(dt/2)=exp(4K)>=d^4`.
2. `K^K>=d^2>=2alpha` for `d>=4096`, since `K>=ln d` and `ln ln d>2`.
3. `n_0 x_0<=1/K`, so
   `N_0>=1-alpha/K^K>=1/2` and
   `M_0<=alpha(1+1/K)^K<=e alpha`.
4. For the regular groups, exactly
   `N_i=t^{-d}(T-alpha)` and `M_i=alpha t^{-d}T-1`, hence
   `N_i/M_i >= (1-alpha/T)/alpha`.
5. `Q_i/P_i >= (1-alpha/T)/alpha` because `P_i=alpha T-t^d<=alpha T`.
6. Since `alpha/T<=d^{-3}<=1/(4m)`, Bernoulli's inequality gives
   `(1-alpha/T)^{2m-1}>=1/2`.
7. `K t^5<2^{-19}` is a uniform elementary bound: `K<=2ln d`; the function `(ln d)^6/d^5` decreases on this range; and at `d=4096`, using `ln4096<9`, one obtains
   `8^5 K^6/d^5 <= 2^21*9^6/4096^5 <2^{-19}`.
   Consequently `1/(K x_0)>2` and the floor retains at least half.

Combining these estimates and using
`alpha^(2m)=1/(128K t^(2m-1))` yields

\[
\prod_i R_i
=n_0\prod_i\frac{N_i}{M_i}\prod_i\frac{Q_i}{P_i}
\ge\frac{n_0}{4e\alpha^{2m}}
\ge\frac{16}{e}>1.
\]

Thus positive coefficients satisfying (S) exist, with a strict constant product margin. The argument proves nonexistence at the displayed alpha itself; in particular it proves nonexistence for every smaller target.

For fixed `m=3`, (F) is

\[
\alpha=\frac{d^{5/6}}{2^{11/3}\lceil\ln d\rceil}
=\Omega(d^{5/6}/\ln d).
\]

Let `m` be the least odd integer at least `K`. Then `m<=K+1<=d` and, for `d>=4096`, `(16d)^(-1/(2m))>=1/2`. Hence

\[
\alpha\ge\frac{d}{16K}\ge\frac{d}{32\ln d}.
\]

Only `Theta(ln d)` hubs are needed for this estimate. The enormous `n_0` and coefficient/weight disparities are allowed by the stated unrestricted finite-game model. They would be material restrictions in a bounded-player or bounded-bit-complexity variant.

The growing-`m` proof above explicitly controls the factor `(1-alpha/T)^(2m-1)`. Merely treating that factor as a fixed constant while allowing `m` to grow would leave a gap. None of these calculations supplies a universal existence upper bound or proves a novelty claim without further literature checking.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。

# 依游戏选择的资源可分序势：线性障碍候选

Date: 2026-10-14. Independent derivation by `dense_bridge/local_curl`.

## Claim WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER v1

**Exact Statement.** Define

    rho_d = sup_{t>0}
        ((d+1)(1+t)^d+t^(d+1))/(d+(1+t)^(d+1)).             (G1)

For every integer d>=2 and every real 1<=alpha<rho_d, there is one finite WC-TARGET game G with positive weights, identical monomial latencies c_e(x)=x^d, and full strategy families S_i=2^E, for which no potential of the form

    Phi(s) = sum_{e in E} F_e(S_e(s)),                     (G2)

with arbitrary real set functions F_e:2^[n]->R, strictly decreases at every unilateral alpha-improvement. The functions F_e may be chosen after the entire game is specified and may depend arbitrarily on its weights, strategy families, resource count, resource identities, and all latency data.

The game's full strategy families include the empty strategy, so the all-empty profile is an exact PNE. Thus this is a certificate obstruction, not an equilibrium nonexistence result.

**Objects / Domain.** Finite positive real player weights; finitely many identical monomial resources; arbitrary real resource-set functions; WC-TARGET's unmultiplied player costs. The strategy family 2^E is finite because E is finite.

**Quantifiers.** For every d,alpha in the stated range, choose R with alpha<R<rho_d. First choose the finite weight vector using the frozen multiplier obstruction at factor R. Next choose the finite resource count M by the formula below, depending only on d,alpha,R and that vector. The game is then fixed. Only afterward are arbitrary F_e considered. In particular, M is not selected in response to their values or marginal ratios.

**Assumptions / Definitions.** A unilateral alpha-improvement has old cost > alpha times new cost. Strict ordinal decrease is required for every such move in this one game. Separability means exactly (G2); no uniform rule across different games and no coefficient linearity is assumed.

**Scope.** Game-specific resource-separable potentials that certify all alpha-improvement edges. This claim does not exclude nonseparable ordinal potentials, potentials that decrease only on selected moves, or separable objectives whose global minimizers happen to be approximate equilibria without decreasing on every improvement. The earlier universal-template bridge has different quantifiers and a separate every-global-minimizer implication.

**Conclusion.** Since rho_d>d^((d-1)/(d+1)) and rho_d/d->1, game-specific separable strict ordinal certificates cannot yield an o(d) guarantee on the full class.

**Dependencies.** `WC-R1-MULTIPLIER-BARRIER v1`, frozen in commit `809b032` at `assets/R1/upper_mechanism/arbitrary_multipliers.md`; finite resource-permutation averaging; finite rational approximation with an explicit bound; full subset strategy families.

**Evidence.** Full elementary proof below. The multiplier obstruction was independently reconstructed and reviewed. There is no numerical evidence used in this extension.

**Counterevidence / Objections.** The witness game has an exact PNE. Its additive incidence-count objective has the all-empty profile as its unique global minimizer, so an every-global-minimizer statement for this single game is not ruled out. The strict ordinal hypothesis is essential. Averaging must use automorphisms of the one fixed game, rather than changing its resources or strategy families after F_e are chosen.

**Status.** Self-contained internal theorem conditional on the frozen, independently reviewed multiplier obstruction; internal informed review passed by `dense_bridge` (see `REVIEW.md`). No external review or novelty claim.

**Related Files.** `universal_additive_ordinal_bridge.md`; `../upper_mechanism/arbitrary_multipliers.md` at `809b032`; `../../../MODEL.md`.

## 1. Choose the finite game before considering any potential

Fix d>=2 and 1<=alpha<rho_d. Choose a real R with

    alpha < R < rho_d.                                    (G3)

By `WC-R1-MULTIPLIER-BARRIER v1`, there is a finite positive vector w=(w_1,...,w_n) such that no real set function H and no positive multipliers h_i satisfy

    h_i(w(S)+w_i)^d <= Delta_i H(S)
                      <= R h_i(w(S)+w_i)^d                 (G4)

for every i and every S not containing i.

Put W=sum_i w_i and w_min=min_i w_i, and define

    eta = (w_min/W)^d > 0.                                (G5)

For any two contexts of the same player i, write

    A=(w(S)+w_i)^d,  B=(w(T)+w_i)^d.

Every such latency is positive. Since w_min<=w(S)+w_i<=W and the same holds for T,

    eta <= B/A <= 1/eta.                                  (G6)

Choose a positive integer L with

    L > 1/((R-alpha) eta),                                (G7)

and set

    M = L + floor(alpha L/eta) + 1.                       (G8)

For each pair of contexts define the positive integer

    m = floor(alpha L B/A) + 1.                           (G9)

These integers are used only to select bundles inside the game. From (G6)-(G9),

    m+L <= M,
    alpha B/A < m/L <= alpha B/A + 1/L < R B/A.            (G10)

Now fix the game G with these n players, M resources all having latency x^d, and S_i=2^E for every player. Its weights, resource count, and strategies have all been specified without using any candidate F_e.

## 2. Average a purported ordinal potential over resource automorphisms

Suppose, for contradiction, that arbitrary real set functions F_e produce a separable Phi as in (G2), strictly decreasing at every alpha-improvement in this fixed game.

Every permutation g of E acts on strategy profiles by applying g to every player's strategy. This is an automorphism of G: full subset strategy families are invariant, and identical resource latencies imply

    C_i(gs)=C_i(s) for every i,s.

Thus if s->t is an alpha-improvement by i, then gs->gt is the same kind of improvement. Define the finite average

    Psi(s) = (1/M!) sum_g Phi(gs).

For every alpha-improvement, every summand has Phi(gs)>Phi(gt), so Psi(s)>Psi(t) strictly.

Expanding the average of the separable expression gives

    Psi(s) = sum_{e in E} H(S_e(s)),
    H(U) = (1/M) sum_{e in E} F_e(U).                      (G11)

Each original resource-set function occurs equally often at each resource position. Hence a game-specific separable ordinal potential would yield a common set function H that is still a strict alpha-ordinal potential for the same game. No assumption about how the F_e were generated has been used.

## 3. Positivity of every marginal

Fix i and S not containing i. Choose a resource e. Consider the profile where i uses {e}, every j in S uses {e}, and all other players use the empty strategy. Player i may deviate to the empty strategy because its full strategy family is 2^E.

Its old cost is (w(S)+w_i)^d>0 and its new cost is zero. This is a strict alpha-improvement. In (G11), only resource e changes, so strict ordinal decrease gives

    Delta_i H(S)>0.                                       (G12)

Define the positive finite ratio

    q_i(S) = Delta_i H(S)/(w(S)+w_i)^d.                    (G13)

All contexts occur as profiles in this one game. The other players are held fixed during each considered unilateral move; their strategy families are not changed.

## 4. Finite bundles force the forbidden R-sandwich

Fix i,S,T and use A,B,m from Section 1. Select disjoint bundles U,V of resources with |U|=m and |V|=L, possible by (G10). For every other player j, prescribe the profile strategy

    s_j = (U if j in S, otherwise empty)
          union (V if j in T, otherwise empty).

These strategies are available in 2^E. At the old profile i uses U; at the new profile i uses V; all other players keep s_j. Resources outside U union V are unused.

Player i's costs are mA and LB. The first strict inequality in (G10) gives mA>alpha LB, so the move is a strict alpha-improvement. Strict ordinal decrease of (G11) therefore gives

    m Delta_i H(S) > L Delta_i H(T).

Normalize using A,B and use the last strict inequality in (G10):

    q_i(T) < (m/L)(A/B) q_i(S) < R q_i(S).                (G14)

This is true for every ordered pair of contexts. Since there are finitely many subsets, define the attained positive minimum

    h_i = min_{S: i notin S} q_i(S)>0.                     (G15)

By definition h_i<=q_i(T). Taking in (G14) a context S attaining the minimum gives q_i(T)<R h_i. Multiplying by the positive latency shows that H,h satisfy (G4), even with a strict upper inequality. This contradicts the choice of w.

Therefore no game-specific separable strict alpha-ordinal potential exists for G.

## 5. What this does and does not close

All-empty is an exact PNE because every player's cost is zero and costs are nonnegative. The witness therefore separates equilibrium existence from convergence certificates.

The separable objective

    K(s)=sum_{e in E}|S_e(s)|

has the all-empty profile as its unique global minimizer in this game. It therefore satisfies an every-global-minimizer equilibrium guarantee here, while the theorem rules out strict ordinal separable certificates at the stated alpha. This explains why the game-specific every-global-minimizer guarantee cannot be substituted for the hypothesis.

The universal-template bridge can infer strict ordinal decrease from an every-global-minimizer guarantee by restricting a game to two profiles without changing its template. In the present game-specific setting that inference is unavailable: restricting strategies can change a potential chosen from the whole game.

Thus a possible sublinear existence mechanism remains free to select an equilibrium globally, to use nonseparable objectives, or to orient only selected improvements. This extension closes the escape in which an additive potential is chosen using the whole game but is still required to decrease on all alpha-improvement moves.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。

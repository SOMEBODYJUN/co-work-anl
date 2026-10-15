# Universal additive ordinal rules imply a local marginal sandwich

Date: 2026-10-14. Independent derivation and review by `dense_bridge/local_curl`.

## Claim WC-R1-ORDINAL-COPY-BRIDGE v1

**Exact Statement.** Fix an integer d>=2 and a finite positive weight vector w=(w_1,...,w_n). Suppose a rule assigns a real set function H_{d,w,c}:2^[n]->R to each nonzero polynomial latency c with nonnegative coefficients and degree at most d. For every finite WC-TARGET game with this same weight vector, define

    Phi_G(s) = sum_{e in E} H_{d,w,c_e}(S_e(s)).             (O1)

The rule may depend on the full ordered weight vector and on c. It must not depend on the game's strategy families, resource count, resource identities, or other resources. Identical latency functions use the same H. If Phi_G strictly decreases at every unilateral alpha-improvement in every such game, then there are positive numbers h_i, depending on d,w and the rule but independent of c,S and the game, such that

    h_i c(w(S)+w_i) <= H_{d,w,c}(S+{i})-H_{d,w,c}(S)
                      <= alpha h_i c(w(S)+w_i)              (O2)

for every nonzero c, every S not containing i, and every i.

The same conclusion follows from the weaker-looking hypothesis that **every global minimizer** of (O1) is an alpha-PNE in every finite game with the vector w.

**Objects / Domain.** Finite positive weight vectors; nonzero polynomial resource latencies of degree at most d with nonnegative coefficients; arbitrary finite strategy families, including the empty strategy; finite resource copies. It suffices to assume the hypotheses only for monomial resources c(x)=x^d to obtain the obstruction below.

**Quantifiers.** For each fixed w, one common resource-local rule H must work for all finite games with vector w. There is no limit game. The rational-approximation argument uses a sequence of separate finite games to infer an inequality about this same H.

**Assumptions / Definitions.** An alpha-improvement means old cost > alpha times new cost, with alpha>=1. Multipliers h_i are fixed for a player, across all resource contexts and resource costs. A latency is excluded from the normalized-ratio argument only when it is identically zero; any nonzero allowed polynomial is strictly positive at a positive load. Zero-cost resources are unnecessary for the construction.

**Scope.** Universal additive, resource-local potential templates. Coefficient linearity is not assumed: H may depend nonlinearly on the entire latency polynomial. Resource copying replaces coefficient scaling. This claim does not cover a potential whose resource functions are chosen anew using the whole game's strategies, resource count, resource identities, or other resources. It does not cover nonseparable objectives, state-dependent player rescalings, or a rule that decreases only on selected improvement moves.

**Conclusion.** Together with the finite arbitrary-multiplier obstruction frozen in commit `809b032`, this excludes such ordinal rules for

    alpha < rho_d := sup_{t>0}
        ((d+1)(1+t)^d+t^(d+1))/(d+(1+t)^(d+1)).             (O3)

In particular, rho_d>d^((d-1)/(d+1)) and rho_d/d->1. Therefore replacing a cardinal sandwich certificate by a universal additive ordinal template does not produce an o(d) guarantee.

**Dependencies.** Positivity from deletion; finite replication of resources; density of positive rational numbers; two-state games. The asymptotic obstruction uses `WC-R1-MULTIPLIER-BARRIER v1` in `assets/R1/upper_mechanism/arbitrary_multipliers.md`, reviewed at frozen commit `809b032`.

**Evidence.** Self-contained proof below. The frozen multiplier proof was independently reconstructed and checked: within-class simultaneous averaging of H and h, monotonicity of the two-path ratio, finite Riemann sums, and the finite multiscale contradiction all hold. No computation is needed for this bridge.

**Counterevidence / Objections.** A guarantee that **some** global minimizer is an alpha-PNE does not imply this bridge. A constant objective makes every profile a global minimizer, so its some-minimizer guarantee is precisely the original alpha-PNE existence question. Also, an additive objective chosen separately for each whole game does not satisfy the universal resource-local assumption merely because its final expression is a sum over resources.

**Status.** Self-contained internal theorem; internal informed review passed by `dense_bridge` (see `REVIEW.md`). No external review or novelty claim. This is a mechanism obstruction, not an alpha-PNE nonexistence theorem.

**Related Files.** `../upper_mechanism/arbitrary_multipliers.md`, frozen at `809b032`; `../upper_mechanism/proof.md`; `../../../MODEL.md`.

## 1. Every positive-cost marginal is positive

Fix i, a subset S not containing i, and a nonzero allowed latency c. Create one resource e of latency c. Every other player has a singleton strategy family: use e if in S and otherwise use the empty strategy. Player i has two strategies, {e} and the empty strategy.

The change from {e} to the empty strategy changes i's cost from c(w(S)+w_i)>0 to zero. It is a strict alpha-improvement for every finite alpha. Strict ordinal decrease therefore gives

    Delta_i H_c(S) := H_c(S+{i})-H_c(S) > 0.               (O4)

Here and below, subscripts d,w are suppressed. The full vector w remains the same even when some players are fixed on the empty strategy.

Define the positive normalized ratio

    q_i(c,S) = Delta_i H_c(S)/c(w(S)+w_i).                 (O5)

## 2. Resource copies compare any two marginal ratios

Fix i and two contexts (c,S) and (c',T), with i absent from S and T. Write

    A = c(w(S)+w_i) > 0,
    B = c'(w(T)+w_i) > 0.

For arbitrary positive integers m,n, create m copies of c and n copies of c'. Fix every other player on all old copies if that player lies in S, and on all new copies if that player lies in T. Player i has exactly two strategies: all m old copies, or all n new copies. These are legal finite WC-TARGET strategy families.

When i moves from the old bundle to the new bundle, its old and new costs are mA and nB. The potential difference is

    Phi(new)-Phi(old)
      = n Delta_i H_{c'}(T) - m Delta_i H_c(S),            (O6)

because identical resource copies use the same set function and all fixed-player terms cancel.

Whenever m/n > alpha B/A, this move is a strict alpha-improvement. Consequently (O6) is negative and

    q_i(c',T) < (m/n)(A/B) q_i(c,S).                       (O7)

Choose any sequence of positive rational numbers m/n converging from above to alpha B/A. Each pair gives a separate finite game. The template H is unchanged across these games by assumption. Taking the numerical limit in (O7) gives

    q_i(c',T) <= alpha q_i(c,S)                            (O8)

for every pair of contexts. Neither the game, its resource count, its potential, nor a multiplier is passed to an infinite-resource limit.

## 3. A single positive multiplier works for every context

Set

    h_i = inf_{c,S: i notin S} q_i(c,S).                   (O9)

Fix any reference context with ratio q_0>0. Applying (O8) with that reference context on the left gives q_i(c,S)>=q_0/alpha for every context. Hence h_i>=q_0/alpha>0. By definition h_i<=q_i(c,S).

Conversely, fix a target context on the left of (O8) and take the infimum over the right-hand context. This gives q_i(c,S)<=alpha h_i. Multiplying these two bounds by the positive latency yields (O2). The infimum need not be attained.

For the multiplier obstruction it is enough to restrict (O9) to c(x)=x^d; then only finitely many subsets occur, and the minimum is attained. The broader infimum is included to show that nonlinear dependence on latency coefficients is not an escape under the stated universal rule.

## 4. An every-global-minimizer guarantee already forces strict ordinal decrease

Assume instead that every global minimizer of Phi_G is an alpha-PNE, for every finite game with vector w. Take any two profiles of any such game that differ only in i's strategy and form a strict alpha-improvement.

Construct a two-state game by fixing every other player at its strategy in these profiles, and leaving i only its old and new strategies. Keep the same resource latencies and the same full vector w. The two potential values are unchanged because H is independent of strategy families.

If Phi(old)<=Phi(new), the old profile is a global minimizer of this two-state game. It is not an alpha-PNE, since the new strategy is a strict alpha-improvement. This contradicts the hypothesis. Thus Phi(old)>Phi(new). The strict ordinal premise follows, and Sections 1-3 apply.

Only two-state games are needed for this implication. No assertion is made that a some-global-minimizer guarantee forces strict ordinal decrease.

## 5. Applying the frozen finite multiscale obstruction

Fix d>=2 and alpha<rho_d. `WC-R1-MULTIPLIER-BARRIER v1` at commit `809b032` supplies one finite positive vector w such that no real set function F and no positive player multipliers h_i satisfy

    h_i(w(S)+w_i)^d <= Delta_i F(S)
                      <= alpha h_i(w(S)+w_i)^d

on all subsets of that vector. If a universal additive ordinal rule existed, applying this bridge to H_{d,w,x^d} would produce exactly that forbidden pair (F,h). This is a contradiction.

The conclusion concerns universal certificates. The games used in the bridge can have pure equilibria; for example, the deletion game has an equilibrium at the empty strategy. Failure of the certificate is not failure of equilibrium existence.

## Primary-source consistency check

[Caragiannis and Fanelli, *On Approximate Pure Nash Equilibria in Weighted Congestion Games with Polynomial Latencies*, ICALP 2019](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.133/LIPIcs.ICALP.2019.133.pdf), Definition 1 and Theorem 3(a), provide an additive d-approximate potential. For a monomial resource, their gamma=1 set function is

    H(S) = (w(S)^(d+1) + d sum_{j in S}w_j^(d+1))/(d+1).

Its marginals satisfy a fixed-weight sandwich with ratio at most d. Thus the obstruction rho_d/d->1 is consistent with that upper bound. A d+1-epsilon obstruction for all such set functions would be false; the frozen arbitrary-multiplier asset makes the correct asymptotic, rather than that stronger, claim.


---
整理来源与当前文件用途见[逐文件登记](../../../weighted_congestion_frontier/FILES.md)。程序统一通过 `python3 tests/audits/weighted_congestion/replay.py --list` 选择；历史命令、输出摘要与源码哈希属于原冻结版本。

# Global-minimum payoff cannot in general be moved to the last two positions

2026-10-21. Two separate statements in the exact [CAG-MODEL](../../../../current/customer_attraction/model.md): finite unit customers, finite nonempty common menu, unit providers, pure SPE on every ordered history, arbitrary history-dependent ties, repeats and empty topics allowed. These are auxiliary normalization obstructions. Q-CAG-HALF remains OPEN. No external review or novelty certification is claimed.

## G1: a general threshold obstruction

For an instance with m>=2 providers define

\[
\theta_m=\min_{h\in\mathcal S^{m-1}}\max_{T\in\mathcal S}
\sum_{x\in T}\frac1{1+c_x(h)}.
\]

Every complete pure SPE gives each of its last two providers payoff at least theta_m. Consequently, every SPE having a globally minimum-payoff provider at either of those positions has W>=m theta_m.

In particular, if one SPE has welfare W0<m theta_m, then every SPE with W<=W0 has every global-minimum payoff occurrence strictly before the last two positions. Any attempt to obtain an SPE with a minimum-payoff provider in the last two positions must raise welfare by at least m theta_m-W0. This holds even if the complete strategy is replaced, rather than merely relabelled. No reordering of the original terminal action multiset can achieve the proposed normalization: such a reordering preserves welfare and the multiset of terminal utilities.

### Proof from genuine last replies

The last provider's payoff is the maximum at its own (m-1)-action prefix, hence is at least theta_m.

Fix the actual ordered prefix P of length m-2, write d_x for its load, and let b(a) be the given full strategy's last reply after P,a. Put

\[
 U_d(a,b)=\sum_{x\in a}\frac1{d_x+1+\mathbf1_{x\in b}},\qquad
 F_d(a)=\sum_{x\in a}\frac1{d_x+1}.
\]

For all legal themes a,b, customerwise

\[
 U_d(a,b)-U_d(b,a)=F_d(a)-F_d(b).
\]

The finite directed map a -> b(a) has a cycle C. On that cycle the F differences telescope, so

\[
 \frac1{|C|}\sum_{a\in C}U_d(a,b(a))
 =\frac1{|C|}\sum_{a\in C}U_d(b(a),a)\ge\theta_m.
\]

Each term on the right is the true last player's best-reply value at ordered prefix P,a. The penultimate provider can deviate to every a in C and then the same full strategy really replies b(a). Its own SPE inequality therefore bounds its actual payoff below by the maximum, and hence the average, of the left-hand terms. Its actual payoff is at least theta_m.

If a global minimum occurs in the last two positions, all m terminal utilities are at least theta_m. Summing gives W>=m theta_m. The remaining conclusions follow by contraposition and by payoff symmetry within a fixed terminal multiset. The proof uses no count-dependent policy restriction.

This last-two floor is already established in [CA-LAST-TWO-FLOOR](../../../../current/customer_attraction/last_two_floor.md), and the cycle identity is [CA-STATIONARY-PAIR-TRANSPORT](../../../../current/customer_attraction/stationary_pair_transport.md). G1 applies those existing mechanisms to a different normalization question.

## E1: an exact two-unit relocation gap with 36 unit customers

Use the existing [36-customer aggregate-floor instance](../../../../current/customer_attraction/aggregate_theta_counterexample.md), canonical [input](../../../../../examples/customer_attraction/aggregate_theta_failure.json), and [original complete certificate](../../../../../evidence/certificates/customer_attraction/aggregate_theta_failure.json).

There are two disjoint groups of theme labels X={0,1,2}, Y={3,4,5}. For each pair x in X,y in Y there is one customer interested in exactly {x,y}. For each two-element I subset X and J subset Y there are three distinct customers interested in exactly I union J. Thus there are 9+27=36 unit customers. Theme covers are pairwise different.

Direct equal-share calculation gives the complete terminal-pattern table, up to exchanging groups and labels:

| Three selected themes | Individual payoffs | Welfare |
| --- | --- | --- |
| Three distinct themes in one group | 12,12,12 | 36 |
| One in one group, two distinct in the other | 10,12,12 | 34 |
| Two copies of one theme and another in its group | 9,9,15 | 33 |
| Two copies of one theme and one in the other group | 25/3,25/3,37/3 | 29 |
| Three copies of one theme | 7,7,7 | 21 |

At a repeated length-two prefix, the last provider's maximum is 15; at either kind of distinct prefix it is 12. Therefore theta_3=12.

In every SPE, at every first-action prefix a, the second provider can select a different theme in a's own group. The last provider then strictly prefers the third member of that group (payoff 12, versus 9 for repeating or 10 for switching groups). Thus the second provider can guarantee 12. A second provider repeating a instead receives 9: the last provider strictly picks a new same-group theme and obtains 15. Hence repeating the first action cannot be second-player optimal. If the first two actions are different and in the same group, the terminal welfare is 36. If they are in different groups, every best last reply is fresh and joins either group, giving terminal welfare 34. Every SPE therefore has welfare either 34 or 36.

The existing complete policy realizes W=34: root 0; second chooses the smallest opposite-group label; last chooses the smallest unused label in the second provider's group. The root gets 10 after every first-action choice; the second gets 12 and cannot gain; all last replies are best responses. Thus the minimum SPE welfare is exactly 34, with utility vector (10,12,12).

For exact attainability of the relocation threshold, retain the same last-reply policy and change the second policy only after first label 0: there choose label 1. At every other first label keep the opposite-group policy. Set root to 0. The actual path is (0,1,2), all utilities equal 12, and W=36. The second provider still receives its maximum 12 at every prefix: a fresh same-group or a suitable fresh opposite-group choice gives 12, and repetition gives 9. The root receives 12 from 0 and 10 from every other choice. All 43 ordered decision nodes are optimal, so this is a complete pure SPE with a global minimum at each tail position.

It follows exactly that

\[
 \min_{\sigma\ {\rm SPE}} W(\sigma)=34,\qquad
 \min_{\substack{\sigma\ {\rm SPE}\\
 \min_i u_i\text{ occurs at position }2\text{ or }3}}W(\sigma)=36.
\]

The proposed welfare-preserving minimum-to-tail normalization fails, and its minimum additive welfare increase on this instance is exactly 2. Its multiplicative increase is 18/17. This auxiliary gap is not a half-coverage counterexample: OPT_3=36 and all SPE have W>=34.

## Independent definition-level audit

`audit_tail_minimum.py` expands all 36 customers as separate unit objects, computes shares directly, and imports neither the canonical model nor its SPE solver. It checks both complete strategies at all 43 ordered decision nodes (258 comparisons each, including 43 self-comparisons; 215 nonself each), all 36 last prefixes for theta_3, and all 216 ordered terminal payoff vectors against the pattern table. An independent set-valued recursion enumerates every ordered SPE outcome and confirms the two exact welfare minima above; this finite recursion is a check of E1, not a proof of G1. The elementary classification above proves E1 directly.

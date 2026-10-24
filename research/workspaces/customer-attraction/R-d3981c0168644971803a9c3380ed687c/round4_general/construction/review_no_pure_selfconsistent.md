# Independent audit: no pure self-consistent query

2026-10-24. **PASS for the precise auxiliary counterexample.** This independently checks the 16-client witness discovered by `../direct/probe_pure_self_fixedpoint.py`. It refutes universal existence of a pure self-consistent query for the true averaged-competitor-load map in `../root/self_consistent_pool.md`. It does not refute mixed self-consistent payment or Q-CAG-HALF.

## Independently reconstructed model and strategy

The common catalogue has labels 0,...,5 and three unit players. A customer type is its six-bit topic-interest mask. The unit multiplicities are

| mask | count | mask | count |
|---:|---:|---:|---:|
| 2 | 1 | 14 | 1 |
| 16 | 1 | 18 | 1 |
| 29 | 3 | 38 | 1 |
| 41 | 1 | 43 | 2 |
| 45 | 2 | 47 | 1 |
| 49 | 1 | 52 | 1 |

There are 16 distinct unit customers and all six topic coverages are distinct. The strategy is root 0; second player chooses 3 after a first label in {0,1,2}, otherwise 0; last player selects the smallest label in the second player's group {0,1,2} or {3,4,5} absent from the observed two-action history. Three labels per group ensure this last rule is defined even after repeated choices.

The independent script `audit_no_pure_selfconsistent.py` transcribes the counts and this rule, expands distinct unit customers, enumerates every ordered decision history, and evaluates all actual continuations and alternative continuations directly. It imports neither the discovery program nor the repository model/SPE solver. All 258 comparisons over 43 histories are nonnegative; the minimum is zero and 81 comparisons, including self-actions, are ties. Thus all off-path histories and duplicate actions are retained.

The actual path is (0,3,4), with profits (9/2,5,9/2), welfare W=14, and OPT_3=16. Its half margin is 12.

## Independent pooled-load calculation

For every forced query A and each of the three actual prefixes, the script forces A and follows the original strategy. It deletes the queried player's slot, then averages those true competitor loads over the three positions. The sums of competitor **topic counts** are

| A | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 1 | 0 | 2 | 1 | 0 |
| 1 | 2 | 0 | 1 | 2 | 1 | 0 |
| 2 | 2 | 1 | 0 | 2 | 1 | 0 |
| 3 | 3 | 1 | 0 | 1 | 1 | 0 |
| 4 | 3 | 1 | 0 | 2 | 0 | 0 |
| 5 | 3 | 1 | 0 | 2 | 0 | 0 |

Each row sums to six. Divide by three to obtain the average competitor-topic loads μ; divide by six to obtain the topic distribution q. The payoff denominator is 1+μ_x, with μ_x equal to the sum over labels covering the customer. In particular no extra factor of two is omitted or inserted.

The independently computed g_T(e_A) table is

| A \\ T | 0 | 1 | 2 | 3 | 4 | 5 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 113/28 | 149/40 | 61/14 | 113/28 | 149/40 | 247/56 |
| 1 | 219/56 | 237/56 | 159/40 | 219/56 | 18/5 | 1193/280 |
| 2 | 113/28 | 149/40 | 61/14 | 113/28 | 149/40 | 247/56 |
| 3 | 111/28 | 153/40 | 156/35 | 579/140 | 1023/280 | 243/56 |
| 4 | 15/4 | 15/4 | 107/24 | 15/4 | 35/8 | 35/8 |
| 5 | 15/4 | 15/4 | 107/24 | 15/4 | 35/8 | 35/8 |

Every row has a unique maximum. The best-response map is

    0,1,2 -> 5;    3,4,5 -> 2.

Thus none of the six catalogue labels is a best response to its own pooled background. The strict excess over the diagonal for A=0,...,5 is respectively

    3/8, 1/35, 3/56, 9/28, 1/12, 1/12.

This checks every catalogue action, rather than exhibiting only an uncovered subcycle. The map has a two-cycle 2 -> 5 -> 2, and the other four actions flow into it.

Finally, the audit checks the exact Jensen/IC diagonal statement separately for every A:

    3 g_A(e_A) <= sum_i d_i(A) <= W.

Therefore the failure is strictly one of pure self-consistency existence. It does not come from a missing SPE comparison, an incorrect averaging convention, or failure of the diagonal payment.

There is an additional clean separation from mixed payment in this particular witness: the maximum of **all 36** displayed entries is 107/24, whereas W/3=112/24. Every g_T is convex in p, because the load is linear and the reciprocal is convex. Consequently

    g_T(p) <= sum_A p_A g_T(e_A) <= 107/24 < W/3

for every p and every T. Thus every mixed self-consistent point in this witness is paid; in fact every distribution is paid, with margin at least 5/24. Absence of a pure point cannot be presented as a failure of the mixed payment candidate.

## Independent analytic review of the whole-simplex classification

**Additional review completed, §§4–6 of `../direct/self_consistent_pure_shortcut.md`.** This is a separate analytic review of its later full-simplex claims, not an inference from the six pure rows or a numerical check at one mixed point. The review passed. The exact value/isolation calculation delegated to capacity is not independently re-certified in this section.

I first reconstructed the pooled numerator vector as

    (2,1,0,2,1,0) + x(0,-1,1,0,0,0)
                      + y(1,0,0,-1,0,0)
                      + z(1,0,0,0,-1,0),

where x=p_1, y=p_3, z=p_4+p_5. This gives precisely the displayed q_pool(p) after division by six. The domain x,y,z>=0, x+y+z<=1 is exact. On dividing each query payoff by three, the twelve type denominators reconstructed directly from the unit masks are:

| mask | denominator in h=g/3 |
|---:|---|
| 2 | 4-x |
| 14 | 6-y |
| 16 | 4-z |
| 18 | 5-x-z |
| 29 | 8+x |
| 38 | 4 |
| 41 | 7+z |
| 43 | 8-x+z |
| 45 | 7+x+z |
| 47 | 8+z |
| 49 | 6+y |
| 52 | 4+x-z |

Adding them with their stated multiplicities and topic memberships reproduces **all six** displayed h_a formulas. Every denominator is strictly positive on the closed domain.

The exclusions of topics 0 and 3 are valid. In h5-h0, the uniform bounds 1/(4+x-z)>=1/5 and 3/(8+x)<=3/8 give the claimed lower bound 3/40. Subtracting 2y/(36-y²)<=2/35 then gives h5-h3>=1/56>0.

For topic 1, direct subtraction gives exactly the author's h5-h1 formula. In x<=1/2, its (1-2x) numerator is nonnegative and may be discarded; the four remaining uniform bounds give 9/280>0. In x>=1/2, the numerator is nonpositive. Since z<=1-x, its denominator satisfies

    (4+x-z)(5-x-z) >= 4(3+2x).

Dividing a nonpositive numerator by the larger denominator makes the result larger, so the displayed lower bound by B(x) has the correct direction. The remaining uses of z,y<=1-x are also in the correct direction. Independently differentiating gives

    B'(x) = 1/(8-x)^2 - 1/(4-x)^2 - 2/(3+2x)^2
             + 2[36+(1-x)^2]/[36-(1-x)^2]^2.

On [1/2,1], the author's bounds give

    B' <= 1/49 - 4/49 - 2/25 + 74/1225
        = -99/1225 < 0.

The bound on the last positive term is valid even using the weaker range 0<=1-x<=1. As B(1)=1/105, this proves h5-h1>=1/105 and hence g5-g1>=1/35 everywhere; the smaller-x bound is stronger.

For topic 4, direct cancellation gives exactly the displayed R(x,t), with t=1-z>=x. Each of its six t-dependent terms has a strictly positive derivative. Thus R(x,t)>=R(x,x). After the cancellation 2/8-1/4=0, its diagonal expression is exactly the one in the manuscript; all five x-dependent terms have strictly positive derivatives. Its value at x=0 is zero. Therefore equality occurs only at x=t=0, equivalently x=0,z=1, which also forces y=0. At that boundary the independently audited pure-row calculation gives g2=107/24>35/8=g4=g5. Thus topic 4 cannot have positive mass in a self-consistent distribution, even at the equality boundary.

These strict exclusions genuinely apply to the entire simplex and leave support only in {2,5}. Neither endpoint is self-consistent by the strict pure comparisons. Writing p=t e2+(1-t)e5, independent cancellation gives

    g5-g2 = 3[-3/8 + 1/(8-t) + 2/(9-t)].

Its derivative is 3[1/(8-t)^2+2/(9-t)^2]>0; its endpoint values are -1/12 and 3/56. Clearing the positive denominators gives exactly

    3t²-27t+16=0.

The unique root in (0,1) is (27-sqrt(537))/6. At that root topics 0,1,3 remain strictly below 5, and topic 4 is also strictly below because z=1-t<1. Topics 2 and 5 therefore tie for the global maximum. This proves existence and uniqueness of the manuscript's mixed self-consistent point, not merely a unique tie after assuming the support.

The analytic classification does not imply payment in other instances. Payment in this instance was already certified above by the uniform convexity cap, independently of this support classification.

## Other exploration stopped on discovery of this witness

Before receiving this witness I tested exactly one separate fixed-policy cone: the pre-existing 13-player refined-tax automaton, its eight existing client types, all 112050 IC, and prescribed challengers A->D, B/T/D/E->P, P->T. That proposed pattern produced no positive witness; the numeric optimum was negative. Files `probe_self_consistent_13.py` and `self_consistent_13_probe.json` preserve that exploratory computation. It is neither an exact nonexistence proof nor evidence for universal pure existence, and it is not used in this audit. No additional policy or instance scan was undertaken.

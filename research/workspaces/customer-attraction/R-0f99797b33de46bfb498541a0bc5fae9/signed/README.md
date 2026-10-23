# Signed harmonic / query budgets: exact quantifiers and attack state

2026-10-23. Personal research backup, not a new general theorem. Q-CAG-HALF
and both signed budget candidates below remain OPEN. No commit, push or
external message was made by this subagent.

Fix the entire ordered-history pure SPE and its actual terminal customer loads
`c`, actual covered set `C`, welfare `W=|C|`. For an optimal **m-tuple** of
catalog topics let its loads be `d` and its union be `O`, and put `G=|C\O|`.

The candidate is that at least one optimal tuple satisfies

    B(c,d) = sum_x sum_(t=1)^d_x 1/(c_x+t) <= W+G.

The stronger candidate replaces B by `Q(c,d)=sum_x d_x/(c_x+1)`.
The exact gap is

    Q-B = sum_x sum_(t=2)^d_x (t-1)/[(c_x+1)(c_x+t)] >= 0.

Consequently a Q counterexample need not refute B. For either budget, a missed
optimal customer contributes at least one. Thus the candidate gives
`|O\C| <= W+G` and hence `OPT_m=|O\C|+W-G <= 2W`.

## Repetition reduction (proved elementary quantifier lemma)

Fix a support P of r distinct catalog topics, 1<=r<=m. Among m-tuples whose
support is **exactly** P, the minimum of B is attained by taking every member
of P once and putting all m-r additional repetitions on a single member of P.
The same statement holds for Q. Therefore the existential optimal-tuple
candidate can be checked by all coverage-optimal supports P of size <=m and,
for each P, at most r such completions. One must still compare every optimal
support; a single failing completion is insufficient.

Proof: extend `H_(c+t)-H_c` piecewise linearly between nonnegative integer t.
Its slopes `1/(c+t+1)` decrease, so it is concave. If `n_a>=0` are the extra
repetitions and `sum_a n_a=L=m-r`, the B objective is a concave function of n,
since each customer's count is affine in n. For L>0 write
`n=sum_a (n_a/L)*(L e_a)`. Concavity gives
`B(n)>=sum_a(n_a/L) B(L e_a)>=min_a B(L e_a)`.
All vertices are legal integral completions. L=0 is immediate. Q is linear,
so the same conclusion follows, with the repeating topic minimizing its
query weight `sum_(x in topic)1/(c_x+1)`.

If r<m and P is coverage-optimal, its union is the entire coverable customer
universe: otherwise one spare slot could add a topic covering a new customer.
This does not make P the only optimal support, and does not justify ignoring
optimal tuples which add actual topics to P.

## Existing families sharply delimit the candidate

The existing collision-free 3/2 family has m=k+1, actual path
`C_1,...,C_k,D`, W=2k+2, and optimal tuple `A_1,...,A_k,D`, with G=0.
All actual and optimal loads are one, except the k missed private customers
whose actual load is zero. Thus

    B=Q=k+(2k+2)/2=2k+1=W-1.

So the coefficient of W cannot be lowered uniformly below one even with G=0,
disjoint optimal topics and collision-free actual play. This computation uses
the previously proved full-history family; it is not a new SPE construction.
Source:
`research/current/customer_attraction/collision_free_three_halves_family.md`.

In the existing 71-customer family (parameter k>=3), the unique optimal
support is {T,Q}, the two optimal topics are disjoint, and

    W=13k-4, G=13k-6, B=Q=14k-5.

The unsigned deficit is k-1; with coefficient lambda on G this family requires
`lambda >= (k-1)/(13k-6)`, asymptotically 1/13. It does **not** refute the signed
candidate with coefficient one. Source:
`research/workspaces/customer-attraction/R-171cd7d518434f36a48cd50df29c9303/global/optimal_omission_exchange_counterexample.md`.

## Targeted full-strategy cone diagnostic

`attack_signed_budget.py` changes customer multiplicities only inside existing
complete ordered-history strategy cones. It imposes every legal SPE comparison
and that the tested m-distinct support attains maximum m-topic coverage. The
objective is precisely B-W-G or Q-W-G. Positive floating candidates would be
accepted only after Fraction feasibility, all optimal m-tuple checks, integer
unit-customer expansion and two full-history certificate checks.

The saved `signed_budget_report.json` contains 768 floating LP diagnostics on
15 archived full strategies. Every nonempty support of size at most m is
tested; within a support the LP maximizes the minimum excess over all extremal
completions from the lemma. No positive point was found; the closest maximum
was -0.05 after normalizing W=1. This proves no universal assertion. There is
no new signed-budget counterexample here and no exact dual family was
extracted. A potential positive point with coincident topic sets would be
rejected: differently named copies of the same subset cannot silently provide
additional public signals in the set-catalog model.

## Mechanism attempted and the genuine earlier incentive obstruction

An attempted Q/B separation added a customer core shared by all optimal A_i
topics, with actual core load one. This makes Q charge approximately m/2 per
core customer, whereas B charges `H_(m+1)-1`. To deter an early player from
expanding a private C_i to A_i, many later A topics would dilute the core. This
suggested horizon-dependent private increments a_i.

The proposed continuation is not credible: at its final punishment node,
an **earlier already played C_j** can be expanded to A_j. Its fresh private
increment a_j can exceed the designated punisher's compensation, making that
older A_j a strictly better real last action. Omitting these earlier C_j
histories falsely permits the desired horizon-dependent increments. No
counterexample or proof relies on this construction. A next construction
would have to pay that exact old-prefix expansion incentive, rather than
merely verify the final two players after a fresh deviation.

The live mathematical obligation remains a general inequality obtained from
credible earlier nodes paying `B-W-G` (or the stronger Q debt). Finite absence
of a violation and identities rewriting this debt do not pay it.

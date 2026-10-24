# True optimal-portfolio queries and their exact unpaid credit

2026-10-24. Exploratory general-input analysis, not a new welfare theorem.
Q-CAG-HALF remains **OPEN**. The formula below is an exact accounting
diagnostic; the cross-branch payment inequality is explicitly unproved.
No external review or novelty claim is made.

## 1. Quantifiers and three different interfaces

Use [CAG-MODEL](../../../../current/customer_attraction/model.md): every finite
unit-customer common catalogue, every m>=1, and every complete ordered-history
pure SPE sigma, including arbitrary ties. Fix its actual ordered leaf
z=(S_1,...,S_m), actual union C and welfare W. Fix any optimal indexed m-tuple
T=(T_1,...,T_m), allowing repetitions. Its union O has size OPT.

At the original actual prefix z_<i, define

    V_ij = u_i(z_<i,T_j, original sigma afterwards).

These are true one-action deviations. Every subsequent action may change.
Let u_i=u_i(z). Thus Gamma_ij=u_i−V_ij>=0. Three distinct proposed bridges are:

1. **ROW:** at every actual i, sum_j V_ij>=OPT−W. This is the existing
   [same-node proposal](../../R-b6d636d360e14c11aeb4b76415ed422b/general_payment/net_gap_handoff.md).
2. **True net-gap matching:** for some optimal tuple and permutation pi,
   sum_i V_i,pi(i)>=OPT−W. This also suffices for half by true IC.
3. **Static optimal assignment:** replace V_ij by the frozen-leaf query
   F_ij=u_i(T_j,z_-i), and require some optimal assignment's sum to be <=W.
   This is [already false](../dynamic_exchange/static_optimal_assignment_counterexample.md).

The old omission-matching counterexample asks for |O\C|, rather than
OPT−W=|O\C|−|C\O|, and therefore does not refute item 2. Nothing below applies
SPE optimality to F_ij. F is used only to display an exact static credit.

## 2. Explicit nonnegative credit for a whole menu at one actual node

For each customer x put c_x=# actual topics containing x, d_x=# indexed
comparison topics containing x, and a_i(x)=1_(x in S_i). Set I=O∩C,
H=O\C, G=C\O. Define the nonnegative number

    L_i = sum_(x in H) (d_x−1)
        + sum_(x in I∩S_i) (d_x−1)/c_x
        + sum_(x in I\S_i) d_x/(c_x+1)
        + sum_(x in G∩S_i) (1−1/c_x)
        + |G\S_i|.

Every used denominator is positive. The formula includes multiplicities of
distinct unit customers in the usual way. All five terms are nonnegative;
in particular comparison overlap is a credit and must not be erased before
controlling its associated adaptive penalty.

The frozen query is

    F_ij = sum_(x in T_j) 1/(1+c_x−a_i(x)).

Directly splitting customers into the five cases above proves, for every
comparison tuple (optimality is not needed for this identity),

    sum_j F_ij = OPT−W+u_i+L_i.                    (1)

For example, on I∩S_i the left contribution is d_x/c_x; subtracting u_i's
contribution 1/c_x leaves (d_x−1)/c_x. On G∩S_i, OPT−W contributes −1 and u_i
contributes 1/c_x, leaving the credit 1−1/c_x. The other cases are immediate.

Now retain the exact signed adaptive penalty

    Q_i = sum_j (F_ij−V_ij).

Then the genuinely dynamic whole-menu total R_i=sum_j V_ij satisfies

    R_i = OPT−W+u_i+L_i−Q_i.                     (2)

Consequently ROW would follow from Q_i<=u_i+L_i. It does **not** require the
much stronger and unsupported sign condition Q_i<=0. The exact row slack is
u_i+L_i−Q_i; this is the same unresolved net demand as the older ROW identity,
now with the static nonnegative part and adaptive part displayed separately.
This decomposition itself adds no payment theorem.

At the actual last node, no follower can change, so Q_m=0. Therefore the
unconditional statement

    sum_j V_mj >= OPT−W+u_m                      (3)

is valid in every instance, for every comparison tuple. It is a familiar
static coverage consequence at a true terminal query node, not a new
all-player induction.

## 3. The two aggregate payment thresholds

Summing (2) gives

    sum_ij V_ij = m(OPT−W)+W+sum_i L_i−sum_i Q_i. (4)

Since sum_ij V_ij<=mW, either of the following would be useful:

    sum_i Q_i <= W+sum_i L_i                     (HALF?)
    sum_i Q_i <=   sum_i L_i                     (SHARP?)

HALF? would imply OPT<=2W. SHARP? would imply
OPT<=(2−1/m)W, and is exactly the existing unproved uniform-portfolio
interface m·OPT<=(m−1)W+sum_ij V_ij. Neither is established here. HALF? is
weaker than imposing ROW at every i and allows cross-position compensation.

Keeping the true IC slacks yields the exact target decomposition

    m(2W−OPT)
      = sum_ij Gamma_ij + W+sum_i L_i−sum_i Q_i.  (5)

Thus allowing all Gamma credit makes the resulting condition equivalent to
the target and cannot itself count as progress. A useful proof must bound
the Q terms by independently available credit, instead of defining a debt
whose desired sign merely restates half.

## 4. Direct true matching and its precise relationship to the aggregate

For a permutation pi put

    M_pi = sum_i V_i,pi(i),
    Q_pi = sum_i (F_i,pi(i)−V_i,pi(i)),
    L_pi = sum_i F_i,pi(i)−(OPT−W).

The last quantity is nonnegative for purely static coverage reasons. More
explicitly,

    L_pi = sum_(x in H) (d_x−1)
         + sum_(x in I) sum_i 1_(x in T_pi(i))/(1+c_x−a_i(x))
         + |G|.                                  (7)

This gives the exact exchange account

    M_pi = OPT−W+L_pi−Q_pi,
    2W−OPT = sum_i Gamma_i,pi(i)+L_pi−Q_pi.       (8)

Consequently **some** pi with Q_pi<=L_pi would prove the true net-gap matching
interface. Requiring a frozen assignment itself to cost <=W is neither the
payment in (8) nor a valid replacement for it.

Uniformly averaging index permutations is legitimate here because only a
finite matrix of queries at the original actual prefixes is being averaged;
no random forced prefix, new strategy, or position-exchange claim is used.
It gives exactly

    E_pi L_pi = (W+sum_i L_i)/m,
    E_pi Q_pi = sum_i Q_i/m,
    E_pi M_pi = (sum_ij V_ij)/m.                 (9)

Thus HALF? is an average **true matching** payment with each actual player's
source used once. If it held for one optimal tuple, a suitable permutation
would follow. The logical hierarchy is: ROW at every position implies HALF?,
which implies existence of a net-gap true matching, which implies half.
SHARP? is stronger than HALF? by exactly one copy of W. None of these
unproved implications is reversed or assumed established by (7)–(9).

## 5. Where the adaptive penalty lives

At actual prefix i write b_x for past load, k_x for the actual later load,
and k'_ij(x) for the later load in the true branch after T_j. For x in T_j,

    F_ij−V_ij
      = sum_(x in T_j) (k'_ij(x)−k_x)
          /[(b_x+1+k_x)(b_x+1+k'_ij(x))].         (10)

This term can have either sign. In the frozen comparison leaf, the current
player has already been replaced by T_j; that leaf is not generally a SPE.
True follower incentives therefore do not compare k'_ij to k_x directly.

Per customer in T_j, the total later-player share increases by exactly
(b_x+1) times that customer's term in (10); the current queryer loses one
copy and the fixed older players lose b_x copies. This gives the correct
same-leaf redistribution account, but the different j branches are mutually
exclusive. Summing their later-player profits and treating that sum as one
actual wallet would repeat the known capacity error. A proof needs actual
descendant comparisons coupling those branches; a whole tail is not one
follower's legal action.

The existing [true-hybrid expansion](../terminal_query/hybrid_ic_expansion.md)
expresses a transplanted tail's harmonic change as real nonnegative IC slacks
plus residual potential changes with a moved player algebraically removed.
Those residuals are not SPEs of a deleted-player game. It supplies no sign
for the combined Q_i and cannot be substituted for HALF?.

## 6. Exact named checks and the required five-player distinction

[audit_dynamic_slack.py](audit_dynamic_slack.py) independently replays all
prescribed histories and all legal action comparisons, using Fraction only.
It also enumerates every terminal topic multiset for the optimum and every
index permutation for best true matching. Its [output](dynamic_slack_audit.json)
records:

| Existing complete policy | W / OPT | True row totals R | Adaptive penalties Q |
| --- | --- | --- | --- |
| Static assignment witness, m=3 | 1735 / 1740 | (1733,1733,1736) | (2,5,0) |
| Omission matching witness, m=2 | 44 / 45 | (38,44) | (13/2,0) |
| Prefix insertion-bill witness, m=4 | 14 / 22 | (173/12,155/12,155/12,155/12) | (−2/3,0,0,0) |
| Existing all-big family at m=5 | 5 / 9 | (5,5,5,5,5) | (0,0,0,0,0) |

For the static assignment witness, L=(3457/3,3463/3,3457/3). Its assignment
failure does not challenge the true net payment: the best true matching is
1734, whereas OPT−W=5. The omission matching witness's best true matching is
41<|O\C|=42 but far above its net gap 1. The negative Q in the insertion
witness also rules out treating adaptivity as a nonnegative tax by definition.

For the entire already-known all-big family, every actual player gets 1,
W=m, OPT=2m−1. Each optimal-menu query is worth 1, and L_i=Q_i=0. Thus SHARP?
is exactly tight for every m. Specializing the **same** formula to m=5 gives
R_i=5, W=5, OPT=9 and passes this sanity check with no special coefficient.

This does **not** unconditionally prove OPT_5<=2W for arbitrary common
catalogues and every complete SPE. HALF? still has no general payment. The
pressure-test answer is therefore: the conditional mechanism would give 2,
the available unconditional calculation does not. No five-player-only rows,
coefficient fitting, new structure class, or finite negative search was used.

## 7. Status and next mathematical requirement

The parent was given the precise unpaid inequality and the existing-source
distinctions. No new half range, general proof, or true target counterexample
was found. Repeating static optimal assignment or omission matching would
attack a different, already settled interface. A substantive continuation
must prove a joint true-descendant-IC bound for Q using the explicit L and
actual W once, or find a complete SPE violating the chosen auxiliary budget.
The formulas here are useful only as a diagnostic for such a continuation.

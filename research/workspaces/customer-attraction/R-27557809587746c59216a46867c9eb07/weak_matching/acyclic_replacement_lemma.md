# Acyclic replacement lemma for once-charged optimal queries

Status: a general conditional lemma and an exact four-row witness for an
existing full SPE policy. The existence condition is not asserted for arbitrary
SPE. Q-CAG-HALF remains OPEN. Independent review is pending.

## Precise condition

Use CAG-MODEL. Fix any complete-history pure SPE sigma, its actual ordered
terminal profile z, and its topic-count vector q. Let m>=1. Fix any ordered
comparison tuple T_1,...,T_m from the common catalog; it need not be optimal.

Suppose the following finite data exist:

1. An assigned actual topic a_j for each comparison occurrence j, with
   sum_j e_(a_j)=q. Thus comparison occurrences are matched to the actual
   positions by topic; identical actual topics supply indistinguishable slots.
2. For each j, an actual on-path decision history h_j whose prescribed action
   is a_j. Histories h_j may be reused. They need not occur in comparison order.
3. Let b^j be the terminal count vector after choosing T_j at h_j and then
   following the original sigma. For every j and every catalog label a,

       b^j <= q-e_(a_j)+e_(T_j)+sum_(l<j) e_(T_l)        (coordinatewise).

The right side allows any submultiset of the frozen actual opponents and any
submultiset of earlier comparison occurrences. It forbids contamination by a
new topic or by a later comparison occurrence except to the extent its label
was already available among the actual opponents. This is a count-vector
condition, so repeated catalog labels are handled with their multiplicities.

## Lemma and proof

Under this condition, the partitioned frozen query R for this matching is at
most W(z). Consequently

    |union_j T_j| <= (2-1/m) W(z),
    |union_j T_j| <= W(z)+sum_(x actually covered) c_x/(c_x+1).

Proof. Let P_j be the clients for which j is the first comparison occurrence
containing them. The P_j form a disjoint partition of the comparison union.
For x in P_j every earlier T_l omits x. The coordinatewise condition therefore
gives

    load_(b^j)(x) <= c_x-1_(x in a_j)+1.

Both sides are positive because x belongs to T_j. Hence the share earned by
the real deviator on client x is at least the frozen share assigned to that
client at slot a_j:

    1/load_(b^j)(x) >= 1/(c_x+1-1_(x in a_j)).

Sum first over P_j and then over j. Discarding the other nonnegative clients
in each real query gives

    R_min <= R_first <= sum_j U_(T_j)(b^j).

Each h_j lies on the actual path, so the current player's prescribed terminal
payoff there is U_(a_j)(q). SPE gives U_(T_j)(b^j)<=U_(a_j)(q). Reusing h_j is
legitimate: we are summing separate true incentive inequalities, and the slot
condition ensures that their left budgets sum exactly to

    sum_j U_(a_j)(q)=sum_a q_a U_a(q)=W(z).

This proves the payment inequality without freezing any real successor.

Every missed comparison client contributes one to R_first. Every actually
covered comparison client contributes at least 1/m, because its frozen
denominator is at most m. Thus the comparison union is at most
R_first+(1-1/m)W, giving the first welfare bound. Alternatively its frozen
share is at least 1/(c_x+1), so the unpaid part of that client is at most
c_x/(c_x+1); summing gives the second bound. QED.

The proof uses the real complete strategy sigma at all query branches. It does
not assume anonymous histories or a tie rule. Only the explicitly selected SPE
inequalities are needed once those branches have been supplied and verified.

## Four-row witness repairing the strong static-matching obstruction

Take the existing complete policy in
`R-a0bb57fa24044a8794bc7991918a19c6/static_matching/static_matching_counterexample.json`.
Its actual path is (3,3,2,2). Use comparison order (0,1,4,5), matched actual
topics (2,2,3,3); equivalently the comparison topics assigned to the original
four actual positions are (4,5,0,1). Choose the following true comparisons:

| Comparison topic | Assigned actual topic | Actual history used | Real terminal profile, as a multiset |
| --- | --- | --- | --- |
| 0 | 2 | (3,3) | (0,2,3,3) |
| 1 | 2 | (3,3) | (1,2,3,3) |
| 4 | 3 | empty | (0,2,3,4) |
| 5 | 3 | empty | (0,2,4,5) |

The first two branches are exactly frozen replacements. The third additionally
uses earlier comparison 0. The fourth additionally uses earlier comparisons
0 and 4. Each contains only a submultiset of the permitted actual opponents.
Therefore the condition holds. Two root inequalities spend 2U_3(q), and two
inequalities at (3,3) spend 2U_2(q); their sum is W.

This proves R_(4,5,0,1)<=W for **every nonnegative customer multiplicity vector
making this fixed policy SPE**, with no optimality condition on {0,1,4,5}.
It is not restricted to the original 52-client point. The earlier strong
frozen query Q<=W failure is therefore explained by duplicated client charges,
which this ordered partition removes.

`acyclic_source_audit.py` independently reconstructs all real branches directly
from the stored action map, checks the count condition, checks all source
ordered-history incentives with Fraction, and verifies the earliest-owner
charge against the four real queries for all 63 nonempty interest types.

## Boundary: existence is not universal

The known two-player real-portfolio-matching counterexample has actual topics
(E,A), unique optimal pair {B,D}, and both true deviation matchings total 41,
below the 42 missed clients. Since the two actual topics are different, the
slot condition permits no same-topic history reuse. An acyclic witness for
that pair would force real query total at least R_first>=42, a contradiction.
Thus the existence condition above already fails on a complete SPE in two
players. It is a reusable sufficient mechanism, not a new universal route by
itself. Allowing off-path budgets or more general weighted reuse would require
an additional payment argument.

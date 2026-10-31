# Why disjoint replication does not amplify the old security deficit

Private research result, 2026-10-21. This is a bound for one explicit family,
not a general aggregate-security theorem, PAIR proof, or half-coverage proof.

Take K >= 1 disjoint copies of the standard 36-customer gadget. Each copy has
six labels X={0,1,2}, Y={3,4,5}; every cross pair has one distinct unit customer,
and every two-X/two-Y subset has three distinct unit customers. Copy labels
and customers are mutually disjoint. All 3K unit providers face the union
catalog. The true static mixed-security game has 3K-1 opponent actions and an
independent random query. Then

    v_(3K) <= 15/2 + 5/(2K).                         (1)

This bound has an explicit query-independent static opponent distribution.

For one copy, let Q2 be uniform over the six pairs of distinct labels lying
in one group, and let Q3 choose the complete X group or complete Y group
with probability 1/2 each. Against Q2 every pure query has payoff 10; against
Q3 every pure query has payoff 15/2. Here is a direct check for an X query.
Under Q3, its three cross-pair clients each have denominator 2, and its
eighteen two-X/two-Y clients each have denominator 3, giving 3/2+6=15/2.
For Q2, regardless of which group is chosen, a cross-pair client has
background load 1 with probability 2/3 and load 0 with probability 1/3,
giving total cross-pair contribution 3[(2/3)/2+1/3]=2. Each four-label client
has background load 2 with probability 1/3 and load 1 with probability 2/3,
giving total contribution 18[(1/3)/3+(2/3)/2]=8. The sum is 10. Group symmetry
gives the same values for every label.

Now choose a special copy J uniformly among the K copies. Place a Q2
background in J and independently place a Q3 background in every other
copy. This uses exactly 2+3(K-1)=3K-1 legal opponent actions. The distribution
is selected before, and independently of, the query. A query in copy i has
payoff 10 if J=i and 15/2 otherwise, so every pure query has expectation

    (1/K)10 + ((K-1)/K)(15/2) = 15/2+5/(2K).

The same cap holds for every mixed query, proving (1) by weak minimax.
No opponent menu from an actual continuation was substituted for all static
backgrounds.

Consequently any terminal profile with coverage 34 in each copy satisfies

    W - 3K v_(3K) >= 34K-(45K+15)/2 = (23K-15)/2 > 0.       (2)

This statement does not assume that this particular terminal profile is a
full SPE for every K. It says that even if a strategy preserved the original
bad gadget profile independently in every copy, that profile could not
refute the strong aggregate bridge. The root static security drops as the
opponent can spend three actions in almost every copy. The static upper
bound, rather than a per-player payoff floor, is the obstruction.

For K=2, exact backward induction with local history-dependent priority for
the original bad rule yields the full SPE path

    (0,3,4,6,9,10), with utilities (10,12,12,10,12,12), W=68.

The priority first tries to open a less occupied copy, but all comparisons
are performed before applying it. In this run the second player strictly
prefers completing the current copy (payoff 12) to opening the other copy
(payoff 10). Uniform independent queries over the twelve labels give exact
value 35/4 against the worst five-action background; (1) matches this upper
bound, so v_6=35/4. The intermediate safety-chain values in the exploratory
output are floating screens, not exact certificates.

`disjoint_replication_audit.py` independently expands the 36K unit customers,
enumerates the displayed static distributions for K=1,...,5, checks every
pure query by Fraction, and for K=2 enumerates all 4368 static opponent
multisets to check the uniform-query lower bound. Its finite checks verify
the formulas and K=2 certificate; the all-K proof is the construction above.

The construction and algebra have not received independent mathematical
review. The exact deterministic SPE construction is defined by backward
induction in `disjoint_copy_probe.py`; it retains the second local action's
group as a history flag, so reversed two-action local histories need not
share a continuation.

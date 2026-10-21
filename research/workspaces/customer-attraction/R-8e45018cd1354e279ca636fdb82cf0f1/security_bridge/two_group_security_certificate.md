# A static security certificate for a full-history two-group policy

Status: self-contained candidate proof, not independently reviewed. This is an
infinite restricted policy cone, **not** a proof of Q-CAG-HALF and not a
novelty claim. Its purpose is to exclude a structured family of aggregate
security attacks, including the previously used two-group last-floor gadget.

## Exact statement

Fix integers k>=m>=3. There are two groups X,Y of k topic labels each. Every
customer is unit valued, every provider has unit weight, all providers use
the same catalog, and the number of customers is finite. The customer
interest multiset is invariant under all permutations within X, all
permutations within Y, and the exchange of X and Y. This means equality of
the multiplicity of every two interest subsets in the same permutation
orbit; it does not identify ordered histories or impose a tie rule.

Consider the following complete pure strategy sigma. The first provider
chooses a fixed label. At a one-label prefix, the second chooses an unused
label from the other group. At every ordered history of length at least
two, the current provider chooses an unused label in the second provider's
group. Any fixed ordering inside each group can specify the chosen unused
label. This defines every history, including all repeated prefixes, since
the history length is at most m-1<k.

**Claim TG-SEC-v1.** If sigma is a pure SPE at all ordered histories, its
root welfare satisfies W(sigma)>=m v_m(0), for the genuine static security
value with unrestricted (m-1)-topic opponents who do not see the sampled
query. In particular, the entire nonnegative symmetric customer cone in
which this fixed strategy is SPE cannot refute the strong aggregate bridge.

## Four scalar payoffs and two genuine incentive comparisons

By symmetry the actual terminal profile has one provider in X and m-1
distinct topics in Y. Let a be the minority provider's payoff and b the
common payoff of the majority providers. Thus W=a+(m-1)b.

Let t be each provider's payoff in a profile of m distinct topics from one
group. Let r be the payoff of a query that repeats one of the m-1 distinct
topics of a pure-group opponent background. Neither t nor r depends on the
particular labels or the selected group.

Two SPE rows provide

    b >= t >= a.                                      (1)

For b>=t use the second provider's real deviation at the actual one-topic
prefix: choosing a fresh label in the first provider's group makes every
subsequent provider choose a fresh label in that group, so the deviator
receives t. For t>=a use a length-m-1 ordered prefix consisting of distinct
topics in Y. Its second label is in Y, and the prescribed last move is a
fresh Y label with payoff t. A deviation to any X label gives exactly the
minority payoff a. This prefix exists and has at least two labels because
m>=3. These are rows of the same complete strategy, not frozen followers.

## Fresh versus repeated queries

Nonnegative customers and within-group permutation symmetry give

    t >= r.                                           (2)

Take a pure-group background with m-1 distinct labels. Let b0 be one used
label and c0 an unused label in that group. Pair customer types under the
transposition b0<->c0. Types containing both or neither contribute zero
to the fresh-c0 minus repeated-b0 payoff. For a paired type containing
exactly one of b0,c0, let ell count its other background labels. Equality
of the paired multiplicities makes its net contribution

    1/(ell+1) - 1/(ell+2) >= 0.

All other memberships, including memberships in the opposite group, are
unchanged by the transposition. Sum these nonnegative contributions.

## One common static opponent distribution

Define Q without reference to a query: select X or Y with equal
probability, select uniformly an (m-1)-element subset of that group, and
use its distinct topics as opponents. The order of these opponents is
irrelevant to the static payoff. Every query label has the same expected
payoff

    beta = (a+t)/2 - (m-1)(t-r)/(2k).                  (3)

Indeed, the opposite-group background gives a, while the same-group
background contains the query with probability (m-1)/k, yielding r, and
otherwise yields t. Because Q is one legal static distribution shared by
all queries, finite minimax (or simply the maximin upper bound) gives
v_m(0)<=beta. Q does not adapt to the realized query.

The exact identity is

    W-m beta = (m-1)(b-t) + (m-2)(t-a)/2
               + m(m-1)(t-r)/(2k).                   (4)

All three terms are nonnegative by (1)-(2). Therefore W>=m beta>=m v_m(0).
Zero customers and empty coverage give all four scalar payoffs zero, so
no division by welfare is needed. Repeated and arbitrary off-path prefixes
remain in the stated SPE hypothesis; the proof uses two of their rows.

## Evidence and research boundary

`symmetric_policy_probe.py` independently reduces the case k=m to complete
prefix integer partitions, including repeated prefixes, and optimizes the
whole symmetric customer cone numerically. The saved n=3,...,9 run finds
minimum W/v=m, but that finite numerical result is not the proof. The
proof is the explicit Q and identity above. `audit_two_group.py` checks
the identity, Q, and all ordered histories of small genuine instances by
Fraction without importing the canonical SPE solver or this numerical LP.

The certificate relies on the two-group action transitivity and the real
pure-group continuation after the second provider's deviation. For an
arbitrary catalog neither scalar t nor this common Q is available. The
general aggregate security bridge and Q-CAG-HALF remain OPEN.

# Exact on-path incentives and every terminal layer still miss credibility

Status: self-contained analytic template obstruction, not a full SPE and not a
counterexample to Q-CAG-HALF. No novelty or independent-review claim. This is a
personal continuation note; the general target remains OPEN.

## Exact scope

For every fixed integer k>=1, there are common-catalog unit-customer games and
full pure strategies satisfying both:

1. every one-step deviation inequality at every actual-path node, using that
   full strategy's actual continuation, separately for every catalog topic;
2. all one-step deviation inequalities at **every** ordered history with at
   most k players remaining, whether or not that history is on the actual path.

Nevertheless OPT_m/W is unbounded as m grows with k fixed. In particular, taking
k=2 includes every genuine last-two subgame, its full menu, every retained-
overlap pair-envelope inequality, and every equality-pattern sum thereof.
Thus neither nonuniform multipliers nor more queries within those exact
terminal subgames can complete this explicitly truncated system.

This strengthens the information retained in
`R-077c0cacfba24288be91dee1acf6d484/terminal_menu/bounded_suffix_security_obstruction.md`:
that construction keeps a single actual-prefix tail subgame and worst-dilution
early bounds. It is also closely related to
`R-64201cd12083425899e2d643ec9bc087/next_tree/fixed_rank_proof.md`, which retains
all rows through a fixed deviation rank. Neither predecessor is being claimed
as new here. The present version is an elementary way to expose the union of
on-path exactness and globally credible terminal layers.

## Unit-customer game

Choose m>k, write n=m-k, and let L=lcm(1,...,n). Every catalog topic is disjoint
from every other catalog topic. There are:

- n early topics E_i of size L/(n-i+1), for i=1,...,n;
- m+k unit-size topics U_1,...,U_(m+k), each of size L.

All sizes are nonnegative integers and each represented customer has unit
value. The word "unit-size" here means size L after scaling, not a weighted
customer. Every topic has size at most L.

The strategy at an early stage i<=n follows E_i if the preceding history is
exactly E_1,...,E_(i-1). Otherwise it copies the topic chosen at the **first**
earlier departure from that planned early path. Subsequent departures do not
change that first-departure topic. At each of the last k stages, choose the
least-index U_j absent from the entire ordered history. This rule defines a
pure strategy at every ordered history; at most m-1 topics have appeared and
there are m+k U topics, so the last rule is always defined.

The actual path is

    E_1,...,E_n,U_1,...,U_k.

Its welfare and optimum are

    W=L(H_n+k),             OPT_m=mL.                    (1)

The first equality uses disjointness. For the second, m distinct U topics
attain mL, and no m topics cover more than mL. For fixed k,
m/(H_(m-k)+k) tends to infinity since H_n<=1+log n.
For example k=2,m=10,n=8,L=840 gives W=3963 and OPT=8400, so
OPT/W=2800/1321>2.

## All actual-path comparisons are exact and nonnegative

At actual early position i, set s=n-i+1. Its actual utility is L/s. If it
chooses a different topic T, the remaining s-1 early players all copy T and
the last k players select fresh U topics, avoiding T whenever T is a U topic.
Let p be T's count in the actual prefix (p is zero or one). The deviator's
utility is exactly

    |T|/(p+s) <= L/s.                                    (2)

If T is a non-U E topic, final players also avoid it by definition. If T is a
U topic, it is now used and hence is avoided. Formula (2) therefore executes
the actual specified continuation rather than freezing any follower. The
self-action comparison gives equality by definition.

At every actual final stage, the current player gets L from a fresh U topic,
and no deviation can give more than its topic size, which is at most L.
This proves every rank-zero comparison, not merely a worst-case lower bound.

## Every terminal-k subgame is a genuine SPE

Fix an arbitrary ordered history with r<=k players left. A fresh U topic
exists. Choosing it yields exactly L: all later prescribed actions are fresh
and hence avoid it. Any deviation gives at most |T|<=L regardless of subsequent
play. This holds at every terminal history, so all these subgames are pure
SPE. Their background may include arbitrary repeated E or U choices.

For k>=2, the strong identity

    H >= f(T)+f(S)-g(T,S)

therefore holds at every genuine last-two history for every two catalog
queries T,S, including queries from different early deviations. The failure
of half in (1) cannot be fixed using only any number of such rows together
with the actual-path rows.

## The exact missing credibility row

Assume n>=2. After the first player departs to U_(k+1), the second player is
prescribed to copy it. All n early players then copy it, so this second
player gets L/n. Instead it can choose a different fresh U_(k+2). The remaining
early players continue copying the **first** departure U_(k+1), while all
final players avoid the second player's now-used U_(k+2). Its deviation pays
L. Thus this off-path row has slack

    L/n-L < 0.                                           (3)

This row is outside both retained classes when n>=k+2: it is off the actual
path and has more than k players remaining. The strategy is explicitly not
SPE. Already the first missing intermediate off-path incentive destroys its
punishment. The precise task for a positive general proof is to propagate
such credibility through unbounded intermediate depths, not to enlarge the
terminal query list.

## Relation to fixed deviation rank

There is a direct variant combining the existing fixed-rank obstruction with
globally credible terminal layers. Take the cited n-player fixed-rank-K
construction, enlarge its B catalog to n+k topics of size L, and append k
players who always choose a fresh B. Their actions never cover a topic used
by an earlier player, so every earlier actual or deviating utility is
unchanged. Consequently all early rows of deviation rank <=K remain true,
while every last-k ordered history is genuinely optimal. Actual welfare only
increases by kL; optimum becomes (n+k)L. The old estimate
W_early/L<=2^K H_(ceil(n/2^K)) implies an unbounded ratio for fixed K,k.

This is a reduction from the cited fixed-rank proof, not a newly audited
implementation of that more complicated strategy. It rules out the union of
any fixed deviation-rank cutoff and fixed terminal-depth cutoff; full-depth
SPE rows remain completely outside this obstruction.

## Audit and next work

`audit_hybrid_obstruction.py` independently uses Fraction utilities and the
literal full strategy. It checks the m=10,k=2 actual-path inequalities and
the explicit missing row; smaller instances enumerate all terminal histories.
The arbitrary-m,k statements come from (1)-(3), not finite computation.
The numerical `terminal_transport_probe.py` and `probe_m*.json` are an earlier
relaxation exploration, not needed for the proof and not exact certificates.

No general positive invariant was obtained in this branch. A full-depth
argument must exploit exactly the intermediate off-path comparisons omitted
here. The final-two pair identity itself remains valid and useful.

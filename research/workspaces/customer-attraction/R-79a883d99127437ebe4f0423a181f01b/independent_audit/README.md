# Independent audit and general matching candidate

2026-10-24. Q-CAG-HALF remains OPEN. This directory contains independent
mathematical checks and an unproved general candidate, not a proof of half
coverage. No status is inferred from finite negative searches.

## Independent reconstruction of the bottleneck

Fix a complete history-dependent pure SPE, its terminal path z=(S_i), actual
covered set C, utilities u_i, and any optimal m-topic union O. A genuine
deviation at actual position i to T secures at least

    |T \ C| / (m-i+1).

All future players may change their actions. Summing this primitive guarantee
does not pay the m-topic aggregate: distinct deviations may reuse the same
future players on different branches. Root was informed of this bottleneck
before the current general proof draft and fractional path budget were read.
The draft's stronger prefix product budget was subsequently read and is not
claimed as a new result here.

## Candidate: an optimal comparison admits a cheap static matching

For a terminal z, define the *frozen* assignment cost

    F_i(T) = u_i(T,z_{-i}).

The current candidate is:

> For every full-history pure SPE terminal z, there exist an OPT_m-attaining
> m-tuple (T_1,...,T_m) and a permutation pi such that
> sum_i F_i(T_{pi(i)}) <= W(z).

These are simultaneous-game deviations with the other terminal actions
frozen. They are not the true dynamic deviations licensed by SPE optimality.
The assertion is only a candidate. It is distinct from the existing true
dynamic portfolio-matching candidate discussed by the parent.

If the candidate holds, half coverage follows: every client in O\C belongs to
at least one comparison topic; every frozen deviation to a topic covering that
client receives its full unit value. Consequently

    |O\C| <= sum_i F_i(T_{pi(i)}) <= W,

and |O| <= |O\C|+W <= 2W. This implication is independently proved. The
candidate itself remains unproved.

The initial stronger assertion for *every arbitrary comparison tuple* is
false. In the established eight-client instance A=two core clients,
B=four disjoint clients, Q_2=A+one private client, Q_3=A+another private client,
the full SPE terminal is (A,B,B), W=6. For the comparison tuple
(Q_2,Q_2,Q_2), every permutation has frozen total cost 7. This is not an
optimal comparison tuple, and does not refute the present existential
candidate. For the optimal tuple (B,Q_2,Q_3), assigning B to the A-player and
Q_2,Q_3 to the B-players gives 4/3+2+2=16/3 < 6. Uniform random assignment
instead has cost 58/9 > 6, so uniform averaging is too strong even here.

### Precise induction gap

The last actual player is a best response to the actual preceding actions,
so F_m(T)<=u_m for every T. Assigning any comparison topic to that player
pays its row. The remaining terminal prefix is not established to be an SPE
of the shortened game, either with or without the frozen last action as
background. Thus the remaining m-1 topics cannot be charged by induction.
Resolving that change of continuation, or a genuinely global assignment
argument, is the missing step.

### Exact terminal identity

For a fixed permutation let c_x be actual coverage count, d_x the comparison
count, and e_x the number of assigned player/topic pairs both containing x.
Then direct unit-share arithmetic gives

    sum_i F_i(T_{pi(i)})
      = sum_{x:c_x=0} d_x
        + sum_{x:c_x>0} [ d_x/(c_x+1) + e_x/(c_x(c_x+1)) ].

In particular it pays uncovered comparison multiplicity as well as overlap
taxes on already covered clients. This identity is valid for every terminal,
with no equilibrium hypothesis. It is not itself an upper bound by W.

### Finite exploratory evidence, stopped on parent's request

`attack_optimal_static_matching.py` uses the repository's complete-outcome
SPE solver and exact Fraction assignment costs. Its search tested the
existential optimal-tuple candidate only. Runs with seeds shown below found
no counterexample; none is a general proof:

| topics | players | trials | seed |
|---|---|---|---|
| 5 | 3 | 300 | 20261024 |
| 6 | 3 | 3000 | 20261025 |
| 6 | 4 | 500 | 20261026 |

`attack_matching_cone.py` generated LP proposals in the fixed complete
six-topic paired-group strategy cone used by existing security examples.
All 20 three-topic comparison supports returned proposed optimum margin zero,
both when the selected support was constrained weakly optimal and in a
separate run requiring a common positive optimality margin. Floating LP
negative outcomes are only proposal evidence, not exact infeasibility
certificates. No matching counterexample was found or promoted.

## Independent reviews completed

`review_covariance_tiny.md` and the standalone exact
`audit_covariance_tiny.py` verify the covariance peer's four-client,
two-player full SPE and its clientwise counterexample. The frozen program
output is `covariance_tiny_exact_output.json`. Aggregate payment and the
original half target both hold in the witness.

`review_potential_reset_identities.md` independently checks the parent's
POT and RESET algebra. Those identities are valid general representations;
their missing reset-debt budget is not established by that check.

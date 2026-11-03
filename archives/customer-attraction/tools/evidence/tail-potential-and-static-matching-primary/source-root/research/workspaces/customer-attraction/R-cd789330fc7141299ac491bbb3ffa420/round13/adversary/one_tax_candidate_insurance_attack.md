# Analytic attack on security13's one-tax candidate

2026-10-25. This checks one explicit previously known mechanism. It is not
a universal proof or counterexample. The candidate remains OPEN.

For five providers, write v5 for the true zero-background integer-opponent
oblivious security value. Let q be the actual first-three-topic client loads,
let actual last two actions be D,E, and define

`Gamma2=max_(T,S) Phi(q+T+S)-Phi(q+D+E)`.

The candidate is `u1+u2+u3+Gamma2 >= 3v5`.
Its sufficiency check is exact: the independently reviewed tail-two envelope
gives `Gamma2<=tax(D minus E)<=u4/2`, so this candidate implies

`W>=3v5+u4/2+u5>=9v5/2`,

using the existing actual last-two floors u4,u5>=v5. Together with
`OPT5<=9v5` it would prove half coverage.

## Named Cartesian insurance controller

Use five economic blocks, each of a unit clients, and four insurance banks,
each of b unit clients. A legal topic chooses one economic block and one bank.
The known BASE/PUNISH/EXIT complete controller from
`R-d3981c0168644971803a9c3380ed687c/round5_general/security/global_extra_individual_counterfamily.md`
remains valid when `b>=3a/2`: a middle BASE provider receives a/4+b, while any
deviation has at most a+b/2. EXIT and intermediate PUNISH actions receive the
bare-size upper bound a+b; the terminal PUNISH action is a genuine best reply.
Root actions all restart the same anchored controller. Equalities use allowed
history dependent ties. Integer a,b compile directly to unit clients.

The actual economic labels are `(0,0,0,0,1)` and banks `(0,1,2,3,0)`. Thus

`(u1,u2,u3,u4,u5)=(a/4+b/2,a/4+b,a/4+b,a/4+b,a+b/2)`,

`W=2a+4b`, and `u1+u2+u3=3a/4+5b/2`.

The integer-opponent security value is exactly

`v5=3a/5+b/2`.

Proof: uniform topic queries against any four competitors have economic
average at least 3a/5, since distributing four integer loads among five bins
minimizes the reciprocal sum by four distinct bins. Their bank average is
at least b/2, with four bins each loaded once minimizing it. Conversely,
randomize uniformly over rival profiles using four distinct economic bins
and all four banks. Every fixed topic then has expected payoff 3a/5+b/2.
This uses four integer rivals and does not substitute a fractional-background
value for v5.

After the first three actual actions, the economic loads are (3,0,0,0,0),
and bank loads are (1,1,1,0). The two-player potential optimum can choose two
fresh distinct economic labels, gaining 2a. The actual tail gains a/4+a.
Both optimal and actual bank increments are b+b/2. The Cartesian catalog
permits these coordinate choices simultaneously. Therefore

`Gamma2=3a/4`.

The candidate's exact residual on this entire legitimate controller family is

`u1+u2+u3+Gamma2-3v5 = b-3a/10 >=6a/5`.

Consequently this known insurance mechanism cannot refute the candidate.
The weaker earlier front-three candidate also survives, with residual
`u1+u2+u3-(5/2)v5=5b/4-3a/4>=9a/8`.
These are analytic family diagnostics only; a different complete strategy
may behave differently, and no universal statement follows.

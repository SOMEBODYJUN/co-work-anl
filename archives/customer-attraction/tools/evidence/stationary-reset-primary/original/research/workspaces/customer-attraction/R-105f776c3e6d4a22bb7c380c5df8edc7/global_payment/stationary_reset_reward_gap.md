# Incidence-stationary reset is not reward exchangeability

2026-10-24. Exact test of a named general candidate, not a new half proof or new
SPE instance. Q-CAG-HALF remains OPEN. The numerical witness is the pre-existing
36-client SPE in `research/current/customer_attraction/aggregate_theta_counterexample.md`.
The independent reconstruction here does not import the canonical code. The already-existing
`research/current/customer_attraction/stationary_pair_transport.md` §3 contains a
more directly budget-targeted failure of the prescribed stationary-tail kernel
(cap 6 > W/3 in a 22-client full SPE). The present calculation is only a
first-moment/reward formulation and is not claimed as new progress.

## Candidate and exact valid relation

Fix an arbitrary common-catalogue CAG and full-history pure SPE. For each forced
root action A let z(A) be its genuine full continuation leaf, and set

    P(A,T) = (# players selecting T in z(A))/m.

P is a row-stochastic finite matrix. For every stationary distribution p=pP,
writing a_x=Pr_(A~p)(x in A), one has exactly

    a_x = E_(A~p)[c_x(z(A))]/m.                         (INC)

The tempting additional step would identify the root's sharing reward with the
reward of a uniform terminal player, or at least give

    E_p u_root(z(A)) >= E_p W(z(A))/m.                  (REWARD?)

This implication is false even for a complete pure SPE. INC controls first
incidence moments; root membership and terminal load remain correlated.

## Full-SPE witness and stationary distribution

Take six topics X0,X1,X2,Y0,Y1,Y2. There is one unit client on every cross pair
{Xi,Yj}, and three separate unit clients on every interest set with two X and two
Y topics. There are 9+27=36 clients. Use the existing full strategy:

- root chooses X0;
- second chooses the least topic in the group opposite the first action;
- third chooses the least unused topic in the second action's group.

All 43 ordered decision histories and all 258 comparisons, including self
comparisons, are checked directly in `stationary_reset_check.py`.

For forced root A in X, z(A)=(A,Y0,Y1); for A in Y, z(A)=(A,X0,X1).
Every such leaf has root payoff 10, follower payoffs 12 and 12, and welfare 34.
The stationary distribution

    p=(1/4,1/4,0,1/4,1/4,0)

satisfies p=pP. Indeed each X0/X1 coordinate receives its own p/3 plus total
Y-mass/3, hence 1/12+1/6=1/4; similarly for Y0/Y1. Unused coordinates stay zero.
But

    E_p u_root = 10 < 34/3 = E_p W/3.

The strict gap is 4/3. Thus a reset chain that merely copies a uniform terminal
action and takes its stationary law has not constructed a common actual wallet.
The test neither rules out other stationary kernels nor a proof adding a true
full-continuation reward inequality. It does not refute any existing open safety
or menu bridge, and this SPE satisfies 2W>=OPT.

## Stopping point

No new full-input payment inequality was obtained from this candidate. The
other saved result in this folder is the separate route5a arithmetic repair.
One should not interpret either item as a solution of shared-omission payment.

# Shared-K 61-row dual: independent mathematical review

2026-10-25. Internal independent review of `../dual/exact_shared_root.json`,
the separate active-row implementation `../dual/separate_shared_root_audit.py`,
and the mathematical meaning of every newly active row. No external review or
novelty claim. The five-player half-coverage question remains OPEN.

## Accepted conclusion and exact input

For the exact model in `research/current/customer_attraction/model.md`, every
complete ordered-history pure SPE with five unit players satisfies

\[
\operatorname{OPT}_5\le\beta W,
\qquad
\beta=\frac{183538199237294659142159872004505983652023685928609569}
{90987354041588112882665017023745484527941187490861917}
\approx2.017183609421193>2.
\]

This conclusion uses the accepted meanings of the original indexed rows and
the retained-overlap/terminal closure rows, plus the new shared-global-size
rows reviewed below. Empty themes, repeated choices, duplicate comparison
indices, and arbitrary full-history ties are retained. The proof never
chooses a replacement equilibrium continuation. The relaxation's primal is
neither revalidated as a matching optimum nor claimed to be an SPE instance.

## New shared-global-size rows

Let `u` be the actual first player's terminal payoff, and let
`K=max_{S in catalogue}|S|`. The finite nonempty common catalogue guarantees
that this one global maximum exists. It need not be an already represented
topic, and the actual first topic need not attain it.

For every legal `T,Q`, the reviewed copy-reply theorem is

\[
|Q\setminus T|+|Q\cap T|/5
\le (44/3)u+(13/5)K-(16/3)|T|.                 \tag{1}
\]

The two active `KRS:fixed:3:4` and `KRS:fixed:5:3` rows therefore have client
coefficient `440 u_x-160 t_x-30 q_x+24 t_x q_x` and common-K coefficient
`78`; these are exactly **30 times** (1). Their pairs are `(D,E)` and `(U,D)`
in the fixed label order `ABCDEUVWXY`, so all queried actions are legal
catalogue topics. The active `MAX:fixed:i` rows have coefficients
`-1_{topic_i}` and `+1` on the same K.

Independently reconstructed the proof of (1) using the original true root-T
branch `(T,B2,B3,B4,B5)`, and the original true last reply C after the fourth
player copies B5. The nonnegative slacks are root IC, four catalogue-size
caps, the fourth player's true copy-B5 comparison, both original last-node
comparisons with Q and C, and the copied history's last comparison with Q.
The root/size coefficients are `44/3` and `(1/2,1/2,11/15,13/15)`; the four
remaining coefficients are `(4/15,14/15,2/15,1/15)`. Their exact residual was
recomputed for all 128 unrestricted binary client memberships. Every
residual is nonnegative; minimum zero, with 13 zero types. This is complete
coefficient coverage of the algebraic proof, rather than a game sample.

The other active new row is

\[
574700u-12000\operatorname{OPT}_5-88940K\ge0.    \tag{2}
\]

It is 20 times `28735u-600OPT_5-4447K>=0`. Reconstructed its derivation:
force a true globally largest T at the root and retain the original strategy;
let its root payoff be z, so z<=u. Every follower topic has size at most K.
For loads c=1,...,5 on T,

\[
c+20/c-9=(c-4)(c-5)/c\ge0.
\]

This and the follower size caps give outside tail coverage
`V0<=-4K+20z`; inside tail profit is exactly `V1=K-z`. For the same four-tail
SPE, the binary-background theorem gives every legal comparator quartet
profit at most `(1999/1000)V0+(5/3)V1`. Averaging the five optimal-complement
quartets gives a lower bound `(4/5)OPT_5-(2/5)K`. Combining these statements
and using the positive z coefficient yields (2). The 64 raw assignments of
root membership and five comparator memberships check the complement bound.
The integer arithmetic yields K and z coefficients `-4447/750` and
`28735/750`, respectively, before multiplication by 750.

The binary-background dependency was also independently rechecked here from
its submitted 13 rational multipliers and raw terminal shares, individually
summing all six comparator-index pairs. All 4096 raw memberships / 1280
compressed types pass; exact minimum zero, with 19 compressed zero types.
This recheck imports no author evaluator or optimizer. The two-player tax
lemma used for those six comparisons remains an explicitly inherited theorem.

## Newly active old rows and inherited closure rows

`F:third` is the original third player's true comparison of C with E at
history `(A,B)`, retaining the original true suffix `(X,Y)`. `second:5:O` is
the last player's aggregate coverage-floor row
`5v5+sum_x p_x/(p_x+1)-OPT_5>=0` on true path `(A,E,U,V,W)`.
The pointwise inequality producing that row is
`d/(p+1)+p/(p+1)-1_{d>0}>=0`, for d=0,...,5 and p>=0.

`Sbranch:3:K:Y` sums the genuine third players' safety comparisons with Y
after `(A,T_i)`; its denominator is `a+t_i+3`. `Sbranch:3:sum-W` additionally
sums those comparisons with all five genuine branch last topics W_j.
Its coefficient is `5 sum_i v3_i-(sum_j w_j)sum_i 1/(a+t_i+3)`. These are
all comparisons at genuine optimizing nodes. The forced second players on
those branches are never assumed to optimize there.

The remaining old active rows are within the established indexed-row proof.
The active terminal offdiagonal rows are the exact `j!=i` sums of genuine
last-player comparisons. The active pair rows are `j=k!=i` sums of the
retained-overlap two-player inequality
`H_i>=f_i(M_j)+f_i(N_k)-g_i(M_j,N_k)`. In particular, the overlap coefficient
is 1, not the weaker residual-profit coefficient 2. For q=5 their client
formula is
`4 sum H_i-(B+C)sum a_i+sum a_i(b_i+c_i)+Ksum g_i-sum g_i b_i c_i`.
It agrees with the separately implemented histogram formulas. These rows
involve one local family only, which is essential for the pricing argument.

## Full-domain coefficient check and its scope

Reviewed the separate implementation, rather than treating an import of the
discovery `Universe` as independent verification. Its active old-row
definitions are reconstructed directly from shares; all small fractions are
checked to become integers on the 120 grid. Large multiplier operations use
Python arbitrary-precision integers, including numpy object arrays.

Every actual client maps into the following enlarged domain: ten arbitrary
fixed action-membership bits; one shared optimal multiplicity d=0,...,5;
two compositions of five into eight binary cells; one composition of five
into sixteen binary cells; and three menu-overlap pairs satisfying
`0<=h<=d` and `0<=ell-h<=5-d`. Actual cross-history equality constraints can
only shrink this domain. Conditional on the fixed bits and d, all active
histogram terms separate by family. No active mixed-family product is
omitted. All menu terms are affine, so the four corners
`(0,0),(d,d),(5-d,0),(5,d)` suffice separately for each menu.

Checked the cache dependencies as well: family scores depend only on their
fixed prefix load, their cross-menu coefficients, and, for the second-position
family, the fixed membership in Y used by `3:K:Y`. Fixed-path constants stay
outside cached histograms. This covers all 1024*6 conditional cases without
identifying or omitting distinct cases.

Reran that separate implementation with its report redirected here, leaving
its author evidence unchanged. It checks all 792 histograms per third-player
family and all 15504 second-player histograms, conditional on the shared d,
and all menu corners. Its result is 6144 nonnegative conditional residuals,
minimum 0, 43 zero cases, and no negative case. Its 160 cache contexts are an
implementation reduction, not a smaller mathematical input domain. The rerun
is the reviewed separate implementation, not an additional independently
authored pricing engine.

Finally checked all 61 positive integer multipliers against their rational
versions, the exact beta, and the original source's K column. The exact
weighted K coefficient is zero. Thus with legal slack rows
`G_r=sum_x g_{r,x}+k_r K>=0`, the identity is

\[
\beta W-\operatorname{OPT}_5
=\sum_r\lambda_rG_r+\sum_x\rho_x
-K\sum_r\lambda_rk_r,
\qquad\rho_x\ge0,
\qquad\sum_r\lambda_rk_r=0.
\]

This proves the accepted upper bound for every genuine instance and full
pure SPE in the stated five-player model. It does not require an actual
instance to realize every enlarged-domain column.

## Reproduction and evidence

- `audit_shared_root_math.py/.json`: independently authored COPY-128,
  binary-tail dependency, capacity algebra, and rational/K-column checks.
- `separate_shared_root_audit.json`: rerun of the reviewed separate 61-row
  complete conditional pricing implementation, with report redirected here.
- Original dual input SHA-256:
  `bfc96c49c3b6da6edb76e8bbb5708672aad00965b03d922e720372121a663e44`.

No SPE counterexample or solution at factor 2 is claimed. The exact bound is
strictly above 2, and matching primal optimality is a separate obligation.

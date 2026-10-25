# Positive-loss token exchange and capped shadow continuation: exact stop

2026-10-25, matching12. Arbitrary player count, common finite catalog,
unit clients/providers, every complete-history pure SPE throughout.
**HALF, weak frozen assignment, and optimal fresh reserve remain OPEN.**
This note records the actual continuation attempt, not a new welfare bound
or a new method-impossibility claim. No policy-cone scan was run.

## 1. Why the old gate has not acquired a positive-loss amount

Round11 proved the copying identity f_i(B_j)=u_j-R_ij and the cross-role
block gate after jointly minimizing frozen cost over all optimal tuples
and assignments. For equal-size token/role sets I,J, zero net coverage
loss permits a legal equally optimal hybrid and hence pays its removed
frozen cost from actual profits less the best copying refund.

Positive loss is different. In the inherited old1953 complete SPE, one
cross-role block already has corrected cost excess165 but net coverage
loss2. Thus a unit price on the lost clients cannot be inserted after the
gate. This is not a new counterexample or the main deliverable here; it
is the existing exact arithmetic that prevents repeating that step.

The attempted extension was to replace an optimal source token by a true
future coverer and choose off-path tail SPEs extremally. The obstacle is
feasibility, before any amount estimate: swapping two leaf actions is not
automatically a complete-SPE continuation at the new ordered prefix.
Common catalogs make the copied action legal but do not preserve later
best replies. A shadow-improving endpoint must first have a genuine tail
SPE witness under the same entering payoff cap. No such replacement map
was constructed, so shadow extremality was not invoked as a payment.

## 2. Which capped selectors do preserve the given actual leaf

Fix the actual path B and utilities u_i. The offactual first-deviation
children (B_<i,A), A!=B_i, are pairwise disjoint ordered subtrees.
For each child, choose any complete tail SPE whose entering payoff for
the forced current A is at most u_i. These choices can be assembled
independently with the fixed actual path into another full pure SPE with
that same actual leaf: every actual-node deviation stays capped and every
offactual node belongs to one selected genuine tail SPE. Original sigma
shows every such capped child set is nonempty.

Pointwise truncation before convexification matters for this conclusion:

    conv{credible endpoints e: d_i(A,e)<=u_i}

preserves a distribution over such pure selectors. In particular, if a row
mixture uses several capped leaves for the same forced A, sample each
child's witness independently before drawing the analytical query; this
gives a distribution over full pure SPEs with the same actual leaf.

The larger set

    {E_q L_i(A,e): E_q d_i(A,e)<=u_i}

can include individually uncapped endpoints. It is a legitimate analytical
mean-cap domain of legal static loads with genuine tail witnesses, but is
not by this argument a distribution over full pure selectors satisfying
the original entering IC pointwise. Tree12 explicitly distinguishes these
domains and retains the original source queries for its global-cap dual.
No objection to that analytical relaxation is asserted here.

Neither domain's compactness nor the existence of a maximizing shadow
selector gives a numerical bank. The unresolved operation is still a
genuine child-SPE replacement that improves the chosen shadow while
preserving the applicable cap, or a bound on the cost of violating it.

## 3. An optimal-portfolio price slack at a shared saddle

This is retained static accounting, not new dynamic money. Let L* be any
shared-domain saddle load with total topic mass m-1, t=(1+L*)^-1 and
gamma=max_T sum_(x in T)t_x. Define Hbg=sum_x L*_x t_x and
Qstat=(m-1)gamma-Hbg>=0. Among coverage-optimal m-tuples choose one
minimizing K_t=sum_j g_t(T_j), and put

    Popt=m gamma-K_t>=0.

For its incidence k_x and optimum union O, exact client accounting gives

    Sopt=K_t+Hbg-|O|
        =sum_(k_x>0)(k_x-1)/(1+L*_x)
           +sum_(k_x=0)L*_x/(1+L*_x)>=0,

    OPT=(2m-1)gamma-Qstat-Popt-Sopt.                (STATIC)

Hence if the original-source Bregman balance is
W-m gamma=I-C+D, the sufficient condition with the first two retained
static slacks is

    C<=D+I+(gamma+Qstat+Popt)/2.                    (PAY-OPT?, OPEN)

Retaining Sopt as well gives the exact original HALF balance, not a new
inequality. In fact Popt+Sopt=m gamma+Hbg-OPT is independent of which
optimal tuple is selected; minimizing K_t only reallocates that fixed
static gap, increasing Popt and decreasing Sopt. This prevents counting
an optimized optimal tuple as an independent additional wallet.

Small Popt forces the chosen optimum slots close to maximal t-price;
large Popt relaxes the sufficient target. I found no full-history payment
linking either regime to the mixed covariance. The earlier zero-loss
optimal-token gate remains unweighted coverage selection, whereas these
KKT weights maximize a weighted repeated competitor load. No identification
between those two extremal objects has been proved.

## 4. Required five-player pressure and current status

The same derivation at m=5 yields

    OPT_5<=9gamma-Qstat-Popt,
    C<=D+I+(gamma+Qstat+Popt)/2  ==>  OPT_5<=2W.

The payment premise is unproved for arbitrary catalogs/full-history SPE.
No fixed-five coefficient adjustment or finite nonseparation was used.
The current positive-loss route is exhausted at this feasible-replacement
and common-budget gap; no claim is made that another general route fails.

# 实际Kronecker平方的完整任务证书与幂次反放大

This proof accompanies EXACT_ONLY.md. The square witness below is finite but exact, and suffices for a mathematical counterexample. A uniform closed-form family is still being sought.

## Base lower and upper bounds

For C<2, each resource machine accepts at most one unit incidence job. Each selector chooses one of its group's state machines. The two selected supports, one with slope 0 and one with slope 1, each contain two resources and intersect in exactly one resource, regardless of the two selected labels. If both selected state machines were to send both incidence jobs outward, the common resource would receive two distinct unit jobs. Therefore one of the four selected incidence jobs stays at its selected state machine and cohabits with a unit selector, giving load at least 3/2.

The bound 3/2 is attained by choosing labels zero for both groups, assigning resources R00,R10 to the slope-zero selected state, assigning R11 to the slope-one selected state, and keeping the one remaining selected incidence job private. All unselected-state incidences stay private. Selected loads are 1 and 3/2, unselected states have load 1, resource machines have load at most 1. This accounts for all ten jobs, so OPT(P)=3/2.

## The square is a real complete schedule

The separately recorded list has exactly 100 machine destinations, one for every ordered pair of original jobs. It is verified from the raw base formulas: if the destination pair is (i,k) for the job pair (j,l), then p_ij and p_kl are finite and the square load is p_ij*p_kl. Rational summation gives exactly 1 at each of all 64 tuple machines. The list is an exact proof certificate; no optimization oracle is invoked by the checker.

Every destination of an A_g x A_h selector-pair job costs exactly 1. Such jobs exist, so every full square schedule has makespan at least 1. Combining this lower bound with the complete certificate gives OPT(P^[2])=1.

## Every even power also has exact optimum 1

If sigma schedules P^[2] with each load 1, the coordinatewise product of k copies schedules every job of P^[2k]. At a tuple of k square machines, its load is

    sum_(j_1,...,j_k : sigma(j_s)=i_s for all s) product_s p_(i_s,j_s)
    = product_s sum_(j_s : sigma(j_s)=i_s) p_(i_s,j_s)
    = 1.

All 10^(2k) jobs are assigned and all 8^(2k) loads are covered; this does not delete mixed tuples. The tuple of 2k selectors still has time 1 at every eligible destination, proving the opposite inequality OPT>=1. For each fixed k, explicitly generating this schedule is polynomial in the explicit output size; no polynomial in binary k is claimed.

## Assignment-LP multiplicativity

Write F(P) for the unpruned assignment-LP minimum load. Its dual is

    F(P)=max_(y_i>=0,sum_i y_i=1) sum_j min_(i:p_ij finite) y_i*p_ij.

Finite/infinite entries are interpreted via the eligible set, with no 0*infinity convention. A product of primal solutions proves F(P tensor Q)<=F(P)F(Q). A product of dual optimizers y_i*z_k gives

    min_(i eligible j,k eligible l) y_i*z_k*p_ij*q_kl
    = min_(i eligible j) y_i*p_ij * min_(k eligible l) z_k*q_kl,

and summing over all job pairs proves the reverse inequality. The zero-value case is included by nonnegativity. Standard finite-dimensional LP duality applies to these feasible bounded LPs.

For the stated base P, assign every selector half to each eligible state, and every incidence half private/half to its eligible resource. Each state then has selector load 1/2 plus its two incidences' combined private load 1/2; each resource sees two incidence jobs at mass 1/2 each. Hence F(P)<=1. Give each state dual weight 1/6 and each resource weight 1/12. These eight weights sum to 1. Each selector contributes 1/6 to the dual objective; each incidence contributes min((1/6)*(1/2),1/12)=1/12. Thus the dual objective is 2/6+8/12=1 and F(P)=1.

This establishes the ratio collapse 3/2 -> 1 under the actual full square, not just under a menu-state product.

# Genuine maximal-size root branch: internal SAFE and final PAIR

Boss1; RUN `six-boss1-20261111`. Written before matrix generation and before the one authorized LP call. This is a new obligation; the completed `universal_true_x_tail/` package stays frozen.

## Model, branch, and all Boolean types

Use the finite unit-client common-label-catalog complete ordered-history pure-SPE model. Let u be the actual root player's payoff. Select one genuine legal C of maximum naked size K=|C|. Force C at the root, then follow the fixed strategy's actual ordered continuation B2,B3,B4,B5,B6. No f_P-maximizing X is selected or assumed.

Choose six legal optimum labels, let their union be O, and write the same symbol O for its cardinality when unambiguous. For every client retain the bits

    h=(p,y2,y3,y4,y5,z,o) in {0,1}^7,

where the first six bits are memberships in C,B2,...,B6 and the last bit is optimum-union membership. Introduce all 128 nonnegative masses w_h, including o=0 and the all-zero type, plus the nonnegative scalar u. They satisfy exactly

    sum_h p_h w_h = K,       sum_h o_h w_h = O.

At the sole discovery call fix K=24376964954228547006/142891298915142483961 and O=1. The final dual must preserve the two independent right-hand-side parameters K and O so that its derived bound is universal, not merely a fixed-K assertion.

Let l=(p,y2,y3,y4,y5,z), c=sum l, and define genuine branch payoffs

    v_j = sum_h w_h l_j/c, j=1,...,6,

with zero contribution when c=0. For source j, let b_j=sum_{k<j} l_k. Every prefix is the ordered prefix of this same true root-C branch.

## Root and size constraints: 8 raw rows

Root IC gives u-v1>=0. Each of the five tail labels is a genuine common-catalog action, so |Bj|<=K for j=2,...,6. The six branch labels are legal, hence their union is no larger than OPT6=O. Finally the root can choose C and obtain at least K/6, giving u>=K/6. These give 1+5+1+1=8 rows.

The K/6 row is retained even though the root IC and the Boolean load bound already imply it. No duplicate or zero raw row will be deleted.

## Internal true SAFE: 35 raw rows

At each genuine source j=2,...,6 on this branch and each of the six legal query roles C,B2,...,B6, a deviation to Q followed by its own prescribed true continuation gives at least sum q/(b_j+7-j): at most 6-j successors can cover a queried client. Thus

    v_j - sum_h w_h q/(b_j+7-j) >= 0.

Add one Omean query per source by averaging the six legal optimum-label deviations, then weakening their membership count d_opt to their union indicator o. Its coefficient is q=o/6. Since the denominators are positive and independent of the query index, the weakening is valid. Omean is not a synthetic action. The five sources times seven query descriptors give 35 rows, including terminal self-query B6 whose coefficients are identically zero.

The wallet on the left is v_j of this genuine branch, not the actual-root-path player's payoff. The right side does not freeze later actions from this branch after a different deviation; it is a worst-case load bound on that deviation's own true continuation.

## Genuine final PAIR: 28 raw rows

The final two players' true four-action prefix is (C,B2,B3,B4). For each client put r=p+y2+y3+y4 and D=r+1. Let Y=B5 and Z=B6, with bits y5,z. Define

    f(Q)=sum q/D,        g(Q,R)=sum qr/[D(D+1)],
    U(Q,R)=f(Q)-g(Q,R),
    H=v5+v6+g(Y,Y).

For every legal pair Q,R, let J_Q be the true last reply after forcing Q at this precise prefix. Then

    H-f(Q)-f(R)+g(Q,R)
      = [v5-U(Q,J_Q)]
        +[U(J_Q,Q)-U(R,Q)]
        +[v6-U(J_Q,Y)]
        +[g(Y,Y)-g(Y,J_Q)] >= 0.

The first three terms are three genuine ICs and the fourth is pointwise nonnegative. They use the same J_Q; none is a static frozen-tail deviation. This payment remains valid for repeated or aliased labels and arbitrary weak ties.

Take every unordered pair with repetition from the seven descriptors C,B2,...,B6,Omean: 28 rows. Pure/pure overlap is the exact product. Pure/mean overlap comes from six true rows and weakens d_opt to o because its coefficient in the query cost is positive. For Omean/Omean explicitly average all 36 ordered optimal-menu pairs. The exact query cost is

    d_opt/(3D) - d_opt^2/[36D(D+1)].

For 1<=d_opt<=6 its excess over the d_opt=1 value is

    (d_opt-1)*(12*(D+1)-(d_opt+1))/[36D(D+1)] >= 0.

Therefore the weakened query cost is o/(3D)-o/[36D(D+1)], with overlap o/36. This is the full Cartesian 36-pair average, not the six-diagonal average.

## Exact input orientation and universal dual signs

There are 71 raw rows and 129 nonnegative columns. Store every row in the form

    A_r x >= bK_r*K+bO_r*O.

The five caps use A=-size and bK=-1. The branch-union cap uses A=-coverage and bO=-1. The K/6 floor has A=u and bK=1/6. Other right sides vanish. The two equalities are E_p x=K and E_o x=O. The objective is c*x=u.

For exact nonnegative row weights lambda and unrestricted equality multipliers pi_p,pi_o, require

    h = c - sum_r lambda_r A_r - pi_p E_p - pi_o E_o >= 0

in every one of the full 129 columns. Define

    a = pi_p + sum_r lambda_r bK_r,
    b = pi_o + sum_r lambda_r bO_r.

Then the exact all-column identity is

    u-aK-bO
      = sum_r lambda_r(A_r x-bK_r K-bO_r O)
        + sum_j h_j x_j
        + pi_p(E_p x-K)+pi_o(E_o x-O).

The equality terms vanish for every true instance, giving the universal affine homogeneous root bound u>=aK+bO. Both equalities and all five cap contributions must be retained in a and b; evaluating a numerical dual only at K0 is not enough.

## Discovery, comparison, and scope

One 129-column LP minimizes u at the fixed K0 and O=1. Numerical output is discovery only. Recover a rational primal satisfying all 71 raw rows and both equalities, and rational dual weights with nonnegative residual in all 129 columns. Matching objectives establish only this specified necessary cone's exact optimum at K0.

Compare the new root line at K0 with Main's universally valid (1658K+87O)/10980, whose proof uses the true fifth-source Omean SAFE in addition to root transfer. The new LP is not a reoptimization of the former 217-row point: only its specified scalar K0 is reused.

No feasible point of this projection is asserted to be a complete SPE, a realizable optimal-label catalog, or a counterexample. No discovered supporting line is asserted to be the globally optimal root bound. Zero clients, outside-O clients, empty or repeated labels, aliases, and all original weak ties remain allowed. In particular C is chosen by naked size and need not maximize any prefix potential.

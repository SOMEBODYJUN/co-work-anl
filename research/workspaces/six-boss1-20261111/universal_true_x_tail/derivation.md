# Four genuine forced-X tails over the universal atom point

Boss1; RUN `six-boss1-20261111`. This derivation is written before the one authorized phase-I discovery call. All work is confined to this new directory and its adjacent summary. The released point is the 256-type universal-union projection, not the earlier sixteen-history projection and not an SPE.

## Model and variables

Fix a finite unit-client instance, one complete ordered-history pure SPE, its actual actions A1,...,A6, one common legal label X maximizing `f_P(L)=sum l/(P+1)` for `P=a1+...+a4`, and an optimal six-label menu with coverage union O. O is a membership event, never an additional legal action. Let K be the genuine global maximum cardinality of a legal label.

For `v=(a1,...,a6,x,o)` retain all 256 Boolean types in universal statements. At the released fixed point only 13 have positive mass. For each actual source i=1,...,4, force the same X at the actual history `(A1,...,A{i-1})` and follow the prescribed true successors. Write their ordered membership tuple as `s=(y1,...,y{5-i},t)` of length `6-i`. The last intermediate bit `z=y{5-i}` is player 5's label; t is player 6's label. We impose no distinctness of these labels, of X, or of actual actions.

The fixed feasibility variables are nonnegative `mu[i,v,s]`, with exactly

    sum_s mu[i,v,s] = fixed_mass[v].

For the 13 positive types there are `13*(32+16+8+4)=780` variables and `4*13=52` mass equations. Omitted zero-mass types have zero mu at this particular point by nonnegativity. They must be restored in every universal projection certificate.

For each i let `b=sum_{j<i} a_j`; for each actual source j let `b_j=sum_{k<j}a_k`. Let `u_j=sum a_j/c` with `c=sum a` (zero if c=0), `F_X=sum x/(P+1)`, and all sums include the relevant nonnegative mass.

## Row convention

Every row is stored as

    sum_s A[row,i,v,s] mu[i,v,s] <= b_row(z,K).

The right side is a homogeneous linear expression in the original 256 atom masses and K. Every row belongs to one branch i. The fixed phase-I LP uses the exact frozen value of this right side. Row semantics and the complete coefficients are retained; no row is discarded for numerical redundancy.

## Genuine source IC and actual queries

For each forced-X branch, source IC is

    sum mu x/(b+1+sum s) <= u_i.                 (4 rows)

The denominator is the real deviator's load when x=1. For every new tail label Q, all six actual sources can legally query Q. Their own prescribed continuations give

    sum mu q/(b_j+7-j) <= u_j.                 (84 SAFE rows)

This does not freeze the continuation of the branch where Q was discovered. Since X maximizes f_P over the whole common catalog, and K is its real maximum size,

    sum mu q/(P+1) <= F_X;                     (14 MAX rows)
    sum mu q <= K.                            (14 CAP rows)

At actual history `(A1,...,A4)`, source IC, a true terminal reply's BR, and the same global maximum give

    sum mu q/(P+1+x) <= u5.                    (14 MX rows)

One direct payment for MX uses the actual source-5 deviation to X and its true terminal reply V: source IC for X, V's BR against Q, and `F_X-f_P(V)` sum to `u5-U_P(Q,X)`.

## Genuine branch terminal BR

The branch's genuine five-action background has client load `B=b+x+sum(s[:-1])`. Its terminal payoff is `sum mu t/(B+1)`. For X, each A1,...,A6, every earlier own tail label, and the six-optimal-label mean weakened to o/6, impose

    sum mu (q-t)/(B+1) <= 0.                   (42 rows)

For Omean this follows by averaging six real legal terminal queries and weakening their membership count d to their union indicator o. All denominators are positive. The mean is never used as an actual action or prescribed reply.

## Genuine last-two-player PAIR

The true last-two-player background is `p=b+x+sum(s[:-2])`, so `D=p+1`. Its actual final two labels are Z,T, with membership z,t. Define

    f(L)=sum l/D;  g(L,R)=sum lr/[D(D+1)];
    U(L,R)=f(L)-g(L,R);
    H=sum mu [z/(D+t)+t/(D+z)+z/(D(D+1))].

For any legal L,R, let J_L be the true player-6 reply after the player-5 deviation to L at this exact four-action history. The necessary inequality

    f(L)+f(R)-g(L,R) <= H

is paid by player 5's IC for L, J_L's terminal BR against R, the original terminal BR against the same J_L, and `g(Z,Z)-g(Z,J_L)>=0`. All three ICs are genuine full-history ICs. No actual-path payoff replaces a branch payoff.

For each branch take all unordered pairs with repetition from A1,...,A6, X, all its own tail labels including its terminal label, and Omean. There are 13,12,11,10 descriptors and 91+78+66+55=290 rows. Pure/pure overlap is the literal product. Pure/mean overlap is `q o/6`, paid by six real query rows. Mean/mean is paid by all 36 ordered pairs from the same optimal menu. Its exact right-hand query expression at menu multiplicity d is

    d/(3D) - d*d/[36D(D+1)].

For d>=1 its excess over the d=1 expression is

    (d-1)*(12*(D+1)-(d+1))/[36D(D+1)] >= 0.

Thus the weakened mean/mean overlap is `o/36`, with query expression `o/(3D)-o/[36D(D+1)]`. It is not the six-diagonal overlap o/6, and is not an independence assumption.

## Actual RC involving the new labels

At the single actual four-action history, for legal Q,R and the true reply V_Q after Q,

    f_P(Q)+f_P(R)-g_P(Q,R) <= u5+F_X

is paid by actual player 5's IC for Q, V_Q's terminal BR against R, and `F_X-f_P(V_Q)`. Use each new tail paired with each actual A, X, Omean and with every own-branch tail, without repeating unordered own-tail pairs. This gives `14*8+(15+10+6+3)=146` rows. Pure/mean weakening uses the positive coefficient of optimal-menu multiplicity. No cross-branch tail intersection is supplied by a conditional-product fiction.

There are 608 raw inequalities in total.

## One phase-I call and exact separation signs

The only optimization call minimizes a nonnegative common relaxation epsilon:

    A mu - epsilon*1 <= b(fixed_z,fixed_K),
    E mu = fixed_z,  mu>=0, epsilon>=0.

Its numerical output is discovery only. Any infeasibility conclusion will be certified with nonnegative rational row weights lambda. For each branch and each of all 256 types define

    m_i(v) = min over all 2^(6-i) tails s of sum_r lambda_r A[r,i,v,s].

For any nonnegative true mu, mass equations imply

    sum_i,v m_i(v) z_v <= sum_r lambda_r A_r mu
                              <= sum_r lambda_r b_r(z,K).

Hence the universal valid necessary cut is

    C(z,K) = sum_r lambda_r b_r(z,K) - sum_i,v m_i(v)z_v >= 0.

Its fixed-point value being strictly negative is an exact Farkas certificate. Equivalently, with mass equations `E mu-z=0`, multiplying them by `-m` gives nonnegative residual columns `lambda*A-m*E>=0`; their scalar right-hand side is C. The minimum is computed on ALL 256 types, including all zero-support and o=0 types, and every tail state. No additional optimization is required to extend the cut universally.

## Boundaries

This is a necessary completion system. It omits cross-source tail intersections and all unmodeled continuation constraints, conditional identity constraints when two labels alias, explicit membership of the six optimum labels, and the global K-maximizer's membership. A feasible completion would not certify an SPE. An infeasible result excludes only this released visible point (with this common-X membership and K), not half, not every point on the old optimal face, and not the original game's conjecture. Arbitrary weak ties, empty labels, aliases, repetitions, outside-O clients and zero clients remain permitted by all derivations.

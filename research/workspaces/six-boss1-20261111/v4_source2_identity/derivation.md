# The entire old225 optimal face fails a genuine source2 terminal comparison

Boss1; RUN `six-boss1-20261111`. This is a zero-optimizer exact linear-algebra and source-identity task. It reads only the Main-released v4 input/certificate, the formal model and frozen mathematical sources. It does not add or depend on Main's later 320-row family and does not bind or modify the frozen 243-row symbolic template.

## Released finite system and face identity

The input is the complete 256 old types (a1,...,a6,x,o), plus the independent K column. Its 225 raw rows have convention R_k=A_k z-b_k>=0, all 257 variables are nonnegative, and the sole normalization is O=sum(o_v z_v)=1. W=sum_{sum a>0}z_v. The zero client type 0 remains a genuine nonnegative column. Nine normalized cap rows have b_k=-1 and are retained with that right side; every one of the eleven positive-dual rows has b_k=0.

Input SHA256: `b520abb0565c6df7ae4192971bf90d712ddf92a4304f3ce51710cd9b2617b8f5`.
Original certificate SHA256: `290f90feba9bf7ec8232e16e59f02b7f4e05dc41413f14510592c3d16ef28819`.

The old certificate claims and this package independently replays

    W - w* O = sum_{11 positive budgets} lambda_k R_k
                 + sum_{j=0}^{256} rho_j z_j,

with lambda>0 and rho>=0. The exact value is

    w* = 393354291273355731388235883588451948
         /899229760032273191421693253016184735.

At every optimum, every positive-budget row is zero and every column with rho>0 is zero. This is an all-column consequence, not a support assumption extracted from the displayed primal.

## Exact zero domain and full face

There are 243 strictly positive column residuals. The only zero-residual columns are

    0,1,3,7,9,11,25,37,153,165,229,241,249,256.

Column 256 is K. The original positive primal has columns

    1,7,9,11,25,37,153,165,229,241,249,256.

Thus the non-primal zero columns 0 and 3 must be checked, rather than discarded. The eleven positive budgets together with O=1 have rank 12 on this fourteen-column domain. A nonzero exact 12-by-12 minor is supplied; all other columns are accounted for by the 243 positive residuals.

Let z* be the released exact primal and let e_j denote the complete 257-coordinate unit vector. The full affine solution is

    z = z* + t(-e1+e3+e9-e11) + sigma e0.

All raw225 rows and nonnegative variables restrict it exactly to

    sigma>=0,
    0<=t<=130432152540345931391239458166315
             /179845952006454638284338650603236947.

The lower endpoint is z3>=0; the upper endpoint is actual SAFE_6_7 (terminal query X). Every original inequality and every nonnegative variable is verified at both endpoints, which proves sufficiency for the whole interval by affinity. Every original row, the objective and the normalization have coefficient zero on e0; the unrestricted zero-type ray is retained.

The exchange changes only X membership between two actual coverage types: t units move from type1 to3 and from type11 to9. All actual A-label masses, all actual payoffs and K stay fixed.

## Why a genuine source2 continuation must have four equal coverage sets

Among the positive dual budgets are SAFE_2_5, K_ge_size_5 and K_ge_size_6. Hence the entire optimal face has

    u2 = sum_{clients in A5} 1/(a1+5),
    K=|A5|=|A6|.

Here K has its original semantic meaning: the maximum naked size over the whole common legal catalogue. It is not merely a maximum among the visible labels. The formal [complete-history model](../../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md) supplies the true IC at every ordered history, with arbitrary weak ties and legal empty/alias/repeated labels.

At the actual source2 history (A1), force the legal label T=A5 and let its genuine successors be R3,R4,R5,R6 in the given complete pure SPE. If s_c is the number of these four successors covering c, then

    u2 - sum_T 1/(a1+5)
      = [u2 - sum_T 1/(a1+1+s_c)]
        + sum_T (4-s_c)/[(a1+1+s_c)(a1+5)].

The first term is the genuine source2 IC slack and the remaining client terms are nonnegative. The left side is zero throughout the old optimal face. Therefore s_c=4 for every c in T: T is contained in all four true successor coverage sets. Every successor is a legal label with size at most K=|T|, so

    cov(R3)=cov(R4)=cov(R5)=cov(R6)=cov(A5).

This is equality of coverage, not equality of labels. The proof retains the actual ordered labels and their potentially different history-dependent continuations. No successor is transplanted from another history. It also excludes any successor covering outside-T clients, including clients in the free all-zero old type.

## The two genuine terminal gaps

At the genuine history (A1,A5,R3,R4,R5), the prescribed R6 has A5's coverage and payoff u2. Its preceding load on each client is a1+4a5. Therefore any legal label Q satisfies the necessary terminal BR inequality

    G_Q := sum_v z_v q_v/(a1+1+4a5) - u2 <=0.

The old A6 and the same stored X are both legal queries here; X's maximum property is not transferred to this history and is unnecessary for this BR.

For A6, the exact full-face value is the constant

    G_A6 = 104997578333106831070437069794935859
           /899229760032273191421693253016184735 >0.

For X,

    G_X = 367236037058350577615317768596918154
          /4496148800161365957108466265080923675 + (4/5)t >0.

The all-zero ray has zero coefficient in both gaps. Each gap is therefore strictly positive at every point of the old225 optimal face. Either legal deviation contradicts the required true terminal BR, independently of label aliases or weak tie choices.

## Exact identities and claim boundary

The certificate contains all 257 dual residuals, the 12-by-12 rank witness, both full257 affine directions, both endpoints and all225 endpoint row slacks. It also supplies signed full-column identities

    G_A6 = g6 O + sum_k theta6_k R_k
                     + sum_{j:rho_j>0} eta6_j z_j,
    G_X  = gx O + (4/5)z3 + sum_k thetaX_k R_k
                     + sum_{j:rho_j>0} etaX_j z_j.

These identities use only the eleven positive old225 budgets. Their theta and eta coefficients may have either sign; they certify the value on the exposed optimal face and are not universal nonnegative duals or new global welfare bounds.

The source2 same-coverage conclusion and the two strict terminal gaps exclude SPE realization of the entire normalized optimum face of the existing225 necessary cone. The old exact LP optimum and its valid lower bound remain correct. This package proves neither a quantitative global improvement beyond that lower bound, nor half coverage, nor a complete SPE counterexample. It uses no new320 row, no new LP, and no 243-row phase-I attempt.

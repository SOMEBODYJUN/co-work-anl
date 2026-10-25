# Pure egalitarian portfolios do not receive a full actual-welfare payment

2026-10-24, netglobal10. This note tests one exact proposed **general**
alternative to the joint-payment interface. It supplies an analytic
parameter family, not a fixed-player scan or a new positive catalog class.
**Q-CAG-HALF remains OPEN.** No novelty or external-review claim is made.

## 1. The alternate bridge being tested

For an original m-player instance, let

    P_m = max_(T in S^m) min_i u_i(T)

be the best minimum final provider utility attained by any pure portfolio.
This is a static comparison value; T need not be an equilibrium. A tempting
aggregate bridge would be

    W(actual SPE) >= m*P_m.                         (EG)

That bridge is false. The failure below is valid for every m>=2 and every
ordered history of a completely specified pure strategy. No inference is
made about mixed static safety, which has a different minimax quantifier.

## 2. Integer unit-customer family and complete policy

Fix any integer m>=2. Take pairwise disjoint customer blocks

    |C_j|=m,  |E_j|=m-1,   j=1,...,m,

all blocks mutually disjoint. Every entry denotes that many distinct unit
customers. The common catalog is

    A = union_j C_j,
    T_j = C_j union E_j  (j=1,...,m).

All m+1 themes have different coverage sets. Prescribe A at **every** legal
ordered history, including all off-path histories.

To check SPE, consider any current node. Let t_j be the number of past
choices of T_j, and t=sum_j t_j. All future prescribed players choose A.
If the current player chooses A, the final number of A players is m-t,
and the current profit is

    U_A = m*sum_j 1/(m-t+t_j).

If instead the player chooses the legal theme T_k, its own core block has
the same final load m-t+t_k and its private block has load t_k+1. Thus

    U_(T_k) = m/(m-t+t_k) + (m-1)/(t_k+1).

The exact deviation slack is

    U_A-U_(T_k)
      = m*sum_(j!=k)1/(m-t+t_j) - (m-1)/(t_k+1).

Since t>=t_j, each denominator m-t+t_j is at most m and is positive.
Consequently

    m*sum_(j!=k)1/(m-t+t_j) >= m-1
                                   >= (m-1)/(t_k+1).

Every deviation slack is nonnegative. This verifies every legal action at
every ordered history and proves the constant-A policy is a complete pure
SPE, with arbitrary equality cases resolved in favor of its prescribed A.

## 3. Welfare, optimum, and exact pure egalitarian value

The actual leaf is A^m. Therefore

    u_i=m,  W=m^2.

The m themes T_1,...,T_m are pairwise disjoint and cover the whole catalog
universe. Hence

    OPT_m=m(2m-1),
    u_i(T_1,...,T_m)=2m-1.

This gives P_m>=2m-1. For any m-theme portfolio, its total utility is its
coverage and is at most OPT_m; its minimum utility is at most its mean.
Thus P_m<=OPT_m/m=2m-1, proving

    P_m=2m-1,
    W/(m P_m)=m/(2m-1)<1.

So (EG) fails for every m>=2. In fact this family prevents any universal
coefficient larger than 1/2 in W>=c*m*P_m when m is unbounded. This is only
a restriction on that alternate bridge. Its welfare ratio satisfies

    OPT_m/W=2-1/m<2,

so it is not a HALF counterexample.

## 4. Explicit feasible point of the enlarged payment certificate

Fix the optimal comparison tuple (T_1,...,T_m). Every comparison customer
has a unique owner, so variable ownership introduces no choice.

For x in C_i, actual load is m, its comparison owner is i, and the full-O
initialization gives r_ix=1/m. Each other actual role receives H_lx=1/m.
The m core customers owned by i therefore contribute 1 to initial current;
all other core blocks together contribute m-1 to H_i.

For x in E_i, r_ix=1, and its m-1 private customers contribute m-1 to
initial current. Under a query to T_i, every other player still chooses A,
so no private customer has a future coverer. Every core customer is already
covered by each future actual A, so it has no new initial future edge
either. Thus the initial edge set is empty, I-future and R-future are zero,
and one can take

    d_i=m,   H_i=m-1,   J_i=0,
    all R flow variables=0,
    F_i=d_i+H_i=2m-1 <= 2u_i=2m.

This point belongs to the enlarged certificate as well as the original
fixed-ownership interface. No invocation of OFF-history IC beyond the
complete SPE proof is hidden in its ROLE verification. The family therefore
does not separate the enlarged sufficient certificate.

## 5. Direct m=5 substitution and scope

The same formulas at m=5 give |C_j|=5, |E_j|=4, |A|=25, |T_j|=9,

    u_i=5,  W=25,  OPT_5=45,  P_5=9,
    d_i=5,  H_i=4,  F_i=9<=10.

The alternate bridge would demand 25>=45 and is false, while the original
half inequality 45<=50 and the joint payment certificate both hold. This
is the pressure substitution of the same all-m derivation. It is not a
five-player project and supplies no universal five-player welfare result.

The useful conclusion is to abandon (EG); no iterative weaker variant is
proposed here. The original distinct-query ROLE funding gap is unchanged.

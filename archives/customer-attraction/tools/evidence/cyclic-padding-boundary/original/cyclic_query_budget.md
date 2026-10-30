# Cyclic contamination kernels and weighted query budgets

Status: general conditional payment lemmas, a verified old-instance boundary,
and an open global existence obligation. Q-CAG-HALF remains OPEN. The main
target here is the weak once-charged bound R<=(1+1/m)W; the stronger R<=W is
not required.

## Actual budgets and once-charged queries

Use CAG-MODEL. Fix a complete-history pure SPE sigma and its actual terminal
profile z, with counts q, client loads c_x, welfare W and per-topic payoff
U_a(q). Fix m comparison occurrences T_1,...,T_m; repeated labels are allowed.
Let a_1,...,a_m be assigned actual topics whose multiset is exactly q. For each
j select an actual on-path history h_j at which sigma chooses a_j. The h_j may
be reused. Write b^j for the real terminal profile after choosing T_j at h_j
and following the original sigma. SPE supplies

    V_j := U_(T_j)(b^j) <= U_(a_j)(q).

For each comparison-covered client x, let J_x={j:x in T_j}, k_x=|J_x| and
H_x={j in J_x:x in a_j}. The minimum once-charged frozen contribution under
this fixed slot matching is

    r_x = 1/(c_x+1),   if H_x is a proper subset of J_x;
    r_x = 1/c_x,       if H_x=J_x.

The second case implies c_x>=1, so no zero denominator occurs. In particular a
missed client has r_x=1. Define R=sum_x r_x. This is the optimal client
partition for the fixed matching, not the sum of whole-topic frozen queries.

As before,

    |union_j T_j| <= R+(1-1/m)W.

Thus R<=(1+1/m)W pays the general half-coverage conclusion directly.

## Customerwise contamination matrix

Let P be any nonnegative m-by-m matrix satisfying, for every comparison-covered
client x and each j in J_x,

    load_(b^j)(x)
      <= c_x-1_(x in a_j)+1+sum_(l in J_x) P_(j,l).       (C)

This is a customerwise condition. It permits reply topics outside both the
actual and comparison portfolios. A sufficient catalog-count condition is

    b^j <= q-e_(a_j)+e_(T_j)+sum_l P_(j,l)e_(T_l),

but (C) is the actual hypothesis; the catalog-count inequality is unnecessary.
Diagonal P_(j,j) measures extra self-crowding of query j beyond its one own
occurrence. Off-diagonal entries allow arbitrary cyclic contamination.

## Weighted harmonic-kernel lemma

For nonnegative query weights lambda_j and nonempty J subset {1,...,m}, set

    K_lambda(J) = sum_(j in J) lambda_j /
                     (1+sum_(l in J)P_(j,l)).

It suffices to consider the realized incidence sets J=J_x. Suppose

    K_lambda(J_x) >= alpha > 0

for every comparison-covered client type with positive multiplicity. Then

    alpha R <= sum_j lambda_j V_j
            <= sum_j lambda_j U_(a_j)(q).                 (PAY)

Proof. For a client with some eligible owner omitting x, condition (C) implies
all eligible query denominators are at most c_x+1+s_j, where
s_j=sum_(l in J_x)P_(j,l). For s>=0 and c>=0,

    1/(c+1+s) >= 1/[(c+1)(1+s)].

Hence the weighted sum of real query shares on x is at least
r_x K_lambda(J_x)>=alpha r_x. This includes c_x=0.

If every eligible owner covers x, then c_x>=1 and (C) gives denominator at most
c_x+s_j. Now

    1/(c+s) >= 1/[c(1+s)]

for c>=1, giving the same lower bound with r_x=1/c_x. Sum over all comparison
clients, discard other nonnegative query contributions, then use the real SPE
inequalities. QED.

This reduces every covered-client load to the missing-client harmonic kernel.
No scalar maximum dilution, acyclicity, or anonymous continuation is needed.

With alpha=1 and lambda_j>=1, (PAY) takes the direct excess-budget form

    R <= W + sum_j (lambda_j-1)U_(a_j)(q).

Therefore the sufficient global obligation is to route total extra query
budget at most W/m. For example lambda=1 except for one entry increased to 2
would suffice if that query is assigned to an actual player of minimum payoff:
its extra budget is at most W/m. This is a conditional observation; the
existence of such a routing in general remains unproved.

## Matrix corollaries and genuine cyclic improvement

For lambda=1 define

    kappa(P) = max_(nonempty J) 1/K_1(J).

Including all subsets gives a geometry-independent certificate, since every
possible interest pattern is then covered. Singleton subsets imply kappa>=1.
By (PAY),

    R <= kappa(P) W.

Thus kappa(P)<=1+1/m suffices for HALF. This is an aggregate harmonic condition
and can be much better than the largest branch contamination.

For example consider the two-query matrix

    P = [[0,3],[1/10,0]].

The singleton kernels both equal 1 and the full-set kernel equals
1/4+10/11=51/44>1. Hence kappa(P)=1 and strong R<=W is paid. The per-branch
rho k condition below would need rho>=2, and the density criterion
below gives 51/40>1. This example verifies a conditional cyclic mechanism;
it is not asserted to be a new CAG instance or full SPE.

A simpler sufficient bound uses strongly connected induced subsets. Give P
the directed edges l->j when P_(j,l)>0. Define

    tau(P) = max_(nonempty K with P[K] strongly connected)
               [ |K|+sum_(j,l in K)P_(j,l) ] / |K|^2,

where singletons count as strongly connected. Then kappa(P)<=tau(P). Indeed,
for any J choose a source strongly connected component K of P[J]; no
contamination enters it from J\K. Cauchy's inequality gives

    K_1(J) >= K_1(K)
      >= |K|^2 / [|K|+sum_(j,l in K)P_(j,l)] >=1/tau(P).

This recovers arbitrary acyclic replacement matrices with zero diagonal:
only singleton strongly connected subsets matter, so tau=kappa=1 even if
forward contamination entries are large. It also covers complete single-copy
cyclic replacement, P_(j,l)=1 for j!=l and diagonal zero, with tau=kappa=1.

More generally the customerwise scalar condition

    load_(b^j)(x) <= c_x-1_(x in a_j)+rho k_x, rho>=1,

is the special matrix P_(j,l)=rho for j!=l and P_(j,j)=rho-1. Its kernel is
exactly 1/rho on every nonempty J, proving R<=rho W. No c=0/all-owners-cover
degeneracy is hidden in this reduction.

## Exact existing-instance boundary: a selected route needs slack

Use the already verified two-player portfolio-matching counterexample with
catalog (A,B,T,D,E), actual profile (E,A), W=44 and payoffs (22,22). The unique
optimal pair is (B,D), covering 45. These two topics are disjoint.

For the matching B to the first player and D to the last player, the frozen
once-charged query is

    R = U_B(B,A)+U_D(E,D) =45/2+22=89/2 >44=W.

Thus strong payment fails for this **fixed** optimal matching, even after every
client is charged only once. The swapped matching gives R=44, so this is not a
counterexample to existence of an optimal matching with R<=W, nor to HALF.

The real query branches in the first matching are (B,T) and (E,D), with query
payoffs 19 and 22. Their total 41 is below the 42 missed clients; the acyclic
replacement existence condition fails as recorded earlier.

Customerwise condition (C) nevertheless holds on every actual source client
with P=diag(1,0). Weights lambda=(2,1) give K_lambda(J)>=1 for every nonempty
J, so

    R <=2u_1+u_2=66=(1+1/2)W.

This uses exactly the W/m extra budget available in HALF and allows the real
reply topic T outside both the actual and optimal portfolios. It distinguishes
the weak payment obligation from unnecessarily imposing strong payment on an
arbitrarily selected route. The kernel estimate is sufficient, not tight at
this source point.

`audit_cyclic_budget.py` independently replays this complete six-history SPE,
both optimal matchings, every source client type in (C), and the exact weighted
kernel inequality. It also checks the cyclic matrix example with Fraction.

## Remaining main gap

No argument here bounds the optimized routed excess budget by W/m for every
complete SPE. The self-loop constraints expose the missing mechanism: if a
comparison topic has private comparison clients and real followers repeat that
same topic, a singleton kernel needs lambda_j>=1+P_(j,j). Same-topic history
reuse can remove some self-crowding; otherwise weighted off-path budgets or a
different query routing must pay it. Merely applying a maximum dilution to
every row would lose the relevant W/m allowance.

## Separating query slots from payoff nodes

The harmonic proof itself does not require the selected node to choose the
assigned frozen topic a_j. More generally select any genuine decision node g_j
of the complete sigma, on or off the actual path, and let L_j be its prescribed
current-player payoff. Query T_j at that node and call the resulting real
terminal profile b^j. If the same customerwise condition (C), still expressed
using the assigned actual slot a_j, holds, then the identical proof yields

    alpha R <= sum_j lambda_j V_j <= sum_j lambda_j L_j.

Now the required global budget is sum_j lambda_j L_j <=(1+1/m)W. An on-path
node supplies an actual player's payoff, but may be reused across different
frozen slots. An off-path node supplies a genuine continuation payoff whose
charge to actual W must be independently proved. This is an enlarged payment
interface, not an assertion that arbitrary off-path budgets are affordable.

The [padded boundary family](padding_kernel_boundary.md) makes this distinction
concrete for every m: requiring the node to choose its assigned actual topic
forces kernel budget exactly (1+1/m)W, while cross-topic reuse of the last node
already proves R<=W. Its complete SPE construction also demonstrates why the
strong same-topic interface should not be imposed on the global problem.

# 集合包含原矩的 raw SH3 入口容量切：作者证明

2026-10-18. Proof of `sol_raw_sh3_inclusion_entry_cut_exact_v1.md`. No independent review is asserted. Earlier raw SH3 boundary files and their precision note retain their bytes. The numerical binomial audit is distinct from this proof and does not enumerate the exponentially large family matrices.

## 1. Projection and degree payments

Write A for one selector endpoint at U_S, and p=L(A). For a unit row v, let C_v be the sum of its incoming unit endpoints. Full CONFIG(T<2) first/pair agreement gives zero pair moment for any two different incoming endpoints R,R'. Their degree-two product n=RR' has norm squared L(n)=0, hence is an M3 null vector. It annihilates every polynomial of degree at most three.

It also annihilates degree-four multipliers: for every linear form l, n l has degree at most three and norm squared

    L(n^2 l^2)=L(n l^2)=0.

Thus n l is null in M3 and is orthogonal to every degree-at-most-three polynomial. Splitting a degree-four monomial into a linear factor and a degree-three factor proves L(n w)=0 for every w of degree at most four. All Boolean reductions here have total degree at most six. Consequently C_v, and any subset of its incoming endpoints, behaves as an idempotent in each displayed degree-at-most-six expression.

Products of up to three of these linear projections (and original endpoint indicators or their complements) have nonnegative expectation. Indeed their degree-at-most-three product P satisfies L(P^2-P)=0 using the preceding null identities, so L(P)=L(P^2)>=0. This is a paid M3 fact, not an assumed nonnegative cross-machine moment.

## 2. Conditional load and head-capacity inequalities

Let O_S be the number of U_S jobs exported to unit B endpoints. The home/one-hot identity is

    load_(U_S)=A+1-O_S/d1.

The localizer with polynomial A gives

    L(A O_S)>=delta d1 p, delta=2-T.             (2.1)

For a machine B_W, let C_W be all its incoming original unit endpoints, O_W all its outgoing original unit endpoints, and

    b_W=L(A C_W),
    y_W,R=L(A C_W X_W,R),

where X_W,R is the sum of the d2 original e-job endpoints going from B_W to Z_R. It is a subset of the unit row at Z_R and hence a linear projection modulo the preceding nulls. Three-projection positivity gives

    0<=y_W,R<=b_W.                               (2.2)

For every original incoming unit endpoint R_j at B_W, use the degree-two polynomial A R_j in its load localizer. Summing these localizers gives

    sum_R y_W,R >= delta d2 b_W.                 (2.3)

Here load_(B_W)=C_W+1-O_W/d2 and C_W^2=C_W inside the relevant degree-five expectations.

The unit endpoint exports from U_S form a subset of the incoming row at each B_W containing S. All other original unit arrivals to B_W have nonnegative A-conditioned mass. Therefore (2.1) implies

    sum_(W containing S) b_W >= delta d1 p.       (2.4)

For every original export endpoint x of B_W, the degree-three square A x(1-C_W) proves

    L(A x)-L(A C_W x)>=0.                        (2.5)

After Boolean reduction its square minus itself has expectation L(Ax(C_W^2-C_W))=0 by the unit-pair nulls. Summing (2.5) at a terminal and using its unit incoming cap gives

    sum_W y_W,R <= L(A C_(Z_R)) <= p.            (2.6)

The last comparison is the nonnegative norm of A(1-C_(Z_R)). No inactive-all-home normalization or original-job identity compression has been used.

## 3. Common weighted-terminal cut

Fix S and split terminals into

    H_S={R: |R intersect S|>=q/4}

and its complement. Its cardinality is the integer H in the exact statement. For each W containing S, write W=S union V with |V|=q and S disjoint V. Exactly binom(q,j)^2 of its q-subsets R have |R intersect S|=j. Thus it has exactly M terminals outside H_S.

At B_W, (2.2)-(2.3) imply

    sum_(R in H_S) y_W,R >= (delta d2-M)b_W.

If delta d2>=M, sum over W containing S and then apply (2.4) and (2.6):

    delta d1(delta d2-M)p <= H p.

If delta d2<M, inequality (3.1) is automatic because its left side is negative and H>=0. For p>0, divide by p. Symmetry gives the same inequality for every original selector endpoint. A strict reverse numerical inequality forces them all to have zero mass, contradicting selector one-hot.

For an actual T-schedule the same cut has an elementary complete-job interpretation. Its selector chooses S. At least delta d1 distinct U_S original jobs go to distinct B_W containing S. Every such B_W receives a unit and must export at least delta d2 of its own original jobs to distinct terminal machines. At most M of these destinations lie outside H_S; globally at most H unit jobs can enter H_S. Additional exports from any inactive row consume capacity and cannot repair this count. This also proves sound FAIL without a hierarchy solver.

## 4. Complete CONFIG(1) first-moment certificate and actual upper assignment

There is an explicit polynomial-in-matrix-size CONFIG(1) certificate. Set

    a_U=1/N,
    a_B=K d1/(NC).

The selector chooses every U_S with marginal 1/N. Each f_S,j has home marginal 1-a_U and marginal 1/(NC) at each eligible B_W. Each e_W,l has home marginal 1-a_B and marginal a_B/K at each eligible terminal. Every original job's endpoint marginals sum to one.

At U_S use its one-selector configuration with mass a_U, and its all-home-f configuration otherwise. At B_W use each singleton incoming original f endpoint with mass 1/(NC), a total a_B, and its all-home-e configuration otherwise. At each terminal use each eligible singleton original e endpoint with mass a_B/K, and its empty configuration with the remaining mass. The terminal total is

    C d2 a_B/K=d1 d2/N<=C/N<=1.

The B mass also lies in [0,1]. All configurations have actual load at most one. Their support sizes are bounded by the explicit original incidence list. The selector's unit processing time gives the lower bound one for every relaxation or actual schedule, so the CONFIG optimum is exactly one.

For the actual upper assignment, fix S, W containing S and R contained in W. Put the selector at U_S, one f_S,j at B_W, and one e_W,l at Z_R. Put every other f/e job at its own original home. This assigns every original job exactly once. Its only possibly nonunit loads are 2-1/d1 at U_S and 2-1/d2 at B_W. All other internal rows have load one and all terminals have load at most one. This is an upper bound, not a claim that this path is optimal at finite q.

## 5. Exact finite binomial estimates

For j>=q/4 and m>=100q,

    binom(m-q,q-j)/C
      = (q)_j / (m-2q+1)^(overline j)
      <= [q/(m-2q+1)]^j.

The bracket is strictly less than 1/98. Sum the remaining binom(q,j) by 2^q:

    H/C <= 2^q [q/(m-2q+1)]^(q/4)
        < (8/49)^(q/4).                         (5.1)

For j<q/4, monotonicity of binom(q,j) before its midpoint gives

    M <= (q+1)binom(q,q/4)^2.

The binomial theorem at probability 1/4 gives binom(q,q/4)<=4^q/3^(3q/4). The central binomial coefficient obeys K>=4^q/(2q+1). Therefore

    M/K <= (q+1)(2q+1)(256/729)^(q/4).           (5.2)

Finally C=binom(m-q,q)>=((m-q)/q)^q>=99^q, while K<=4^q, proving K/C<=(4/99)^q. These are elementary finite inequalities, not an unverified entropy estimate.

## 6. Floors, fixed scaling losses, and bit complexity

Write e1=K s1/C and e2=s2/K. From the actual integer definitions,

    d1 >= C/(K s1)(1-e1),
    d2 >= K/s2(1-e2).

If delta d2>=M, their product gives

    delta d1(delta d2-M)/C
      >= delta^2/(s1 s2)(1-e1)(1-e2-s2 M/(delta K)).   (6.1)

For fixed a,b and s1<=q^a, s2<=q^b, inequalities (5.1)-(5.2) imply that e1, e2 and s2 M/(delta K) tend to zero exponentially up to polynomial factors, uniformly over the stated s1,s2. For sufficiently large q they are at most 1/2, 1/4 and 1/4 respectively. The right side of (6.1) is then at least delta^2/(4q^(a+b)), while H/C is exponentially small. Thus the strict cut eventually holds and d1,d2 are positive. The actual upper assignment and the sound lower cuts for every fixed delta imply OPT tends to two.

All displayed binomial integers have O(m) bits; H and M use O(q) terms. Exact comparisons use rational integer arithmetic and do not evaluate square roots. Checking all original input entries against their stated subset menus is polynomial in the explicit matrix length. The number of jobs d1,d2 is paid by that input. The finite arithmetic code only checks the binomial formulas and separately a small complete-matrix CONFIG/path example; it does not claim to materialize the huge m>=100q family.

## 7. Relation to the source paper and remaining main obligation

The inclusion graph and demands C/K,K are those of the depth-three construction discussed in the primary Bamas paper. The weighted rare-terminal count is the same source mechanism. The precise use here is different: the given ordinary-job raw SH3 contract forces the conditional parent-bounded flux needed in Section 3. The paper's assignment-LP subtree in general does not have that parent bound. Rejecting its direct labelled-SH3 import does not refute the paper's stated hierarchy result or prove any algorithmic hardness.

The primary text was target-read at its graph/assignment-LP/shadow sections; literal_budget_attack separately target-checked the same definitions and reported that the paper only chooses an unspecified sufficiently-small constant rho. Our proof works directly for every m>=100q and does not require certifying any particular rho for the paper's other estimates. For fixed rho, q is proportional to log of its explicit graph size; a fixed polylog loss is covered only after bounding its scale by some fixed power of q.

This family still has a single-entry fractional capacity defect. It does not address the remaining source needed for a genuine near-two gap of the stronger necessary system: every low-degree conditioned first-flow test would need to pass, while a complete actual schedule is obstructed by shared integer owners. The general UM target is unresolved.

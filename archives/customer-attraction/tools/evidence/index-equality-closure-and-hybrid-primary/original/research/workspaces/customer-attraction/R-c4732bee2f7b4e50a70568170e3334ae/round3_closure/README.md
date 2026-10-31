# 末两人比较主题对的索引等号模式闭包

Status: proved necessary inequalities, exact frozen-marginal noncompletion,
and exact optimization **restricted to the old 64 customer types**. The general
Q-CAG-HALF target remains OPEN. No relaxation point here is claimed to be an
SPE, and the restricted optimization does not certify an unrestricted bound.

## 1. Retaining the comparison overlap in the two-player tax identity

Fix any legal ordered history of the original common-catalog game with exactly
two players left. This includes the last two players of a game with arbitrary
total player count. Let the background load of client x be p_x. Define

\[
 f(T)=\sum_{x\in T}\frac1{p_x+1},\qquad
 g(T,S)=\sum_{x\in T\cap S}\frac1{(p_x+1)(p_x+2)},\qquad
 U(T,S)=f(T)-g(T,S).
\]

Let A,B be this subgame's actual SPE actions, u_A=U(A,B), u_B=U(B,A), and

\[
 H=u_A+u_B+g(A,A).
\]

For any catalog topics T,S, let Q be the **same full strategy's actual reply**
after choosing T. Three genuine one-step SPE comparisons are

\[
 \delta_1=u_A-U(T,Q)\ge0,\quad
 \delta_2=U(Q,T)-U(S,T)\ge0,\quad
 \delta_3=u_B-U(Q,A)\ge0.
\]

Direct expansion gives the sharper version of the existing tax identity:

\[
\boxed{
 H-[f(T)+f(S)-g(T,S)]
 =\delta_1+\delta_2+\delta_3+g(A,A)-g(A,Q)\ge0.}
\tag{1}
\]

The last difference is a sum over A\Q with positive coefficients. Thus (1)
retains the nonnegative g(T,S) term that the older comparison
H >= f(T)+f(S)-2g(T,S) dropped. This is a strengthening of that existing proof,
not an independent new general-player tax theorem. It controls the two-topic
harmonic potential rather than only the two-topic remaining profit.

All comparisons are legal because the catalog is common. Empty or repeated
topics and arbitrary history-dependent ties are allowed. The background can be
arbitrary and need not be disjoint from the query topics. In particular T=S is
allowed. There is no frozen-continuation step.

## 2. Five equality patterns of branch and two query indices

Take any q>=1 genuine two-player decision histories, with local quantities
H_i and background loads p_{i,x}, and two indexed lists of catalog topics
M_j,N_k (j,k=1,...,q). Equation (1) holds for every triple (i,j,k). It is therefore
legitimate to sum it separately over each equality partition of these three
indices. These partitions cannot in general be replaced by their total sum.

For one client and one fixed branch i, write

\[
 b=1_{x\in M_i},\quad c=1_{x\in N_i},\quad
 B=\sum_j1_{x\in M_j},\quad C=\sum_j1_{x\in N_j},\quad
 K=\sum_j1_{x\in M_j\cap N_j},\quad D=(p_i+1)(p_i+2).
\]

For each row of the following table, let h_i be the client's contribution to
H_i. Its contribution to that row's necessary comparison is

\[
             n h_i-\frac{L}{p_i+1}+\frac{r M}{D}.
\tag{2}
\]

Here r=1 gives the retained-overlap inequality (1); r=2 gives the older,
weaker tax comparison. Summing (2) over clients and branches is nonnegative.

| Index condition | n | L | M |
| --- | ---: | --- | --- |
| i=j=k | 1 | b+c | bc |
| j=k, j!=i | q-1 | B-b+C-c | K-bc |
| j=i, k!=i | q-1 | (q-1)b+C-c | b(C-c) |
| k=i, j!=i | q-1 | B-b+(q-1)c | (B-b)c |
| i,j,k pairwise distinct | (q-1)(q-2) | (q-2)(B-b+C-c) | (B-b)(C-c)-(K-bc) |

For q=1 and q=2 the empty orbits have zero coefficients, including the last
line. The table follows by summing b_j+c_k and b_j c_k over the indicated
query pairs. Its counts sum to q^2. It requires neither a distribution on
histories nor an exchangeable/independent membership lift.

This is the mechanism beyond the previous single-query diagonal/offdiagonal
closure: two distinct query topics can jointly expose a branch's coverage
deficit, while query pairs involving that branch's own index hide it. The
all-pairs sum allows the latter surplus to offset the former deficit.

## 3. Applying the rows to the five-player histograms

Use the named branches of the original five-player indexed certificate. For
AB or AE, the histogram state is (t,r,s). The last-two background is the
fixed prefix AB or AE followed by T_i, so p_i=p_fixed+t. The actual last two
membership bits are r,s. For the second-position branch the state is
(t,h,i,j), the last-two background is (A,T_i,H_i), and the actual last two
membership bits are i,j. In both cases

\[
 h_i=\frac{v_i+w_i}{p_i+v_i+w_i}
             +\frac{v_i}{(p_i+1)(p_i+2)},
\]

with the zero numerator term defined as zero.

Choose M,N among positions of the **same** family histogram. Its totals B,C,K
and each branch's p_i,b_i,c_i are already recorded. Therefore every table row
is determined by the existing marginal atom, independent of all couplings to
other families or any ordering of the q indices. We use the six unordered
position pairs (including repeats) of each 3-bit family and the ten pairs of
the 4-bit family. The five patterns give 30+30+50=110 necessary rows for each
r. Swapping M,N only exchanges the third and fourth equality patterns.

## 4. Exact noncompletion of both previously frozen points

`partition_pair_closure.py` loads the source files without changing them.
For every atom it expands the histograms to five literal branch states and
computes all 125 branch/query triples. Their Fraction sums must agree with
the compact formulas separately on every atom. It also checks all paired-bit
assignments for q=1,2,3,5, backgrounds 0,1,9, both overlap coefficients:
6648 exact compact-versus-literal checks, including the empty orbits.

Sources and SHA-256 hashes:

- Original 64 atoms: `evidence/certificates/customer_attraction/five_player_indexed_bound.json`,
  `18e074ba51357dfa03090fe9b97b8ff868b9c83b2687c7da7ff6f7b39489abe1`.
- The 42-atom point from `continuation_completion/frozen_support_augmented.json`,
  `7db100ac5027a6aa427d2ee50da79a8f173e8d226d9484b8ffa30ea42aa71c09`.

The original point violates 24 weak partition rows and 38 strong rows.
The strengthened 447-row point violates 19 weak partition rows and 42 strong
rows. For example, already using the **weaker** tax, the strengthened point's
AB row comparing two optimal topics with i,j,k all distinct equals

\[
 -\frac{4269167732702451742681436056882608491846}
        {2034051454380937197928169143552074377943}<0.
\]

Consequently neither frozen point has a full SPE completion retaining its
exact recorded marginals and the advertised branch meanings. The second
statement does not rely on the failure of the first point, any particular
exchangeable lift, or conditional independence across families.

Parent independent audit `round3_parent/audit_pair_credibility.py` reconstructs
the literal triples and the strengthened identity without importing this
row evaluator. Its separate report is the source of any independent-audit
status, not the self-checks in this directory.

## 5. What reoptimizing the old support proves

`frozen_pair_reoptimization.py` uses floating LP only to select rational bases;
it then solves these bases by Fraction elimination and checks all primal
slacks, dual residuals, and multiplier signs exactly. It starts with the old
437 rows, adds the ten previous single-query offdiagonal rows, then adds the
110 pair-partition rows. Total: 557 rows.

For the **weak** r=2 pair rows and only the old 64 allowed atom types, exact
primal and dual certificates agree at

\[
 \beta_{64}=\frac{14245589264472028054661837896118665}
                    {7663171675475998318101970058002733}
             \approx1.8589677835433802.
\]

There are 29 positive primal masses and 28 positive dual multipliers. Thus no
point on this fixed 64-type support remains above two after the pair rows.

For the **strong** r=1 rows the normalized 64-type system is infeasible. The
report gives 19 nonnegative exact multipliers with

\[
 \sum_r\lambda_r s_r(z)\le-w(z)
       \quad\text{for each of these 64 permitted types }z.
\]

Any nonnegative mixture satisfying all rows would therefore imply 0<=-W,
contradicting W=1. All 64 coefficient inequalities are checked exactly. This
means the old support itself cannot represent any positive-welfare true SPE
with those necessary rows; it is stronger than just eliminating its >2
region. It does not imply infeasibility for the full histogram universe.

`frozen_pair_reoptimization.json` contains the full rational primal, dual,
and Farkas certificates. The dual and Farkas coefficients have been checked
on these 64 types only. They have **not** been priced over all types and
must not be used as universal five-player or general-player bounds.

## Recovery and next obligation

Run both scripts from any directory. The reports are reproducible and all
written output remains in this personal directory. Next, add the split and
retained-overlap rows to an unrestricted pricing scheme, or use (1) and the
index partitions directly in a general-player charging argument. The present
work establishes common-catalog constraints and concrete noncompletions;
it does not settle Q-CAG-HALF.

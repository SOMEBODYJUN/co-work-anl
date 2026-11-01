# Blind audit: nonnegative triangular retraction

2026-10-24. Reconstructed solely from the parent-supplied contract, before opening the application draft. No new SPE incentive comparison is assumed.

Let there be n ordered indices. Let b_i>=0, and define t_il>=0 for i<l, with all other t_il zero. In the stated contract t_il=K_il/b_i when b_i>0; if b_i=0, nonnegativity and sum_l K_il=b_i force that row K to vanish, and set t_il=0. Let a_i=c_i-F_i be arbitrary finite real numbers. Seek

\[
0\le y_i\le b_i,\qquad y_l-\sum_{i<l}t_{il}y_i\le a_l.
\tag{1}
\]

The row-sum-one condition for positive b is not needed for this feasibility lemma: nonnegative strict triangularity suffices. Row conservation matters for the later meaning of the transfers.

## Greedy theorem

At each l in ascending order set

\[
z_l=a_l+\sum_{i<l}t_{il}g_i.
\]

If z_l<0, stop and report failure. Otherwise set g_l=min(b_l,z_l).

**Theorem.** System (1) is feasible if and only if this algorithm completes. If it completes, g is feasible and is its componentwise greatest feasible point.

**Proof.** Completion explicitly gives 0<=g_l<=b_l and g_l<=z_l at every l, hence feasibility. If y is any feasible point and earlier coordinates satisfy y_i<=g_i, nonnegativity of t gives

\[
y_l\le a_l+\sum_{i<l}t_{il}y_i\le z_l,
\quad y_l\le b_l,
\]

so y_l<=g_l whenever the algorithm continues. At its first failure j, every feasible point would instead satisfy 0<=y_j<=z_j<0, impossible. This also proves componentwise greatestness upon completion. Zero b, zero z, negative a, and tied saturation z=b are all included. There is no division by zero.

## Dual cuts and exact first-failure witness

For any lambda>=0 put q_i=sum_(l>i)lambda_l t_il. Any feasible y obeys

\[
\sum_i\lambda_i a_i
\ge\sum_i(\lambda_i-q_i)y_i
\ge-\sum_i b_i(q_i-\lambda_i)_+.
\]

Consequently every feasible instance satisfies

\[
\boxed{C(\lambda):=\sum_i\lambda_i(c_i-F_i)
+\sum_i b_i(q_i-\lambda_i)_+\ge0.}
\tag{2}
\]

At the first greedy failure j define lambda_j=1 and lambda_l=0 for l>j. Compute backwards for i<j:

\[
q_i=\sum_{l>i}\lambda_l t_{il},\qquad
\lambda_i=\begin{cases}q_i,&g_i<b_i,\\0,&g_i=b_i.\end{cases}
\tag{3}
\]

No g_j is required. All prices are nonnegative. At i<j, if g_i<b_i then g_i=z_i and lambda_i=q_i; if g_i=b_i then lambda_i=0 and the upper-bound payment b_i q_i is exact. This remains true when g_i=b_i=z_i, or b_i=0. Extend g_i=0 for i>=j only for the following algebra. Then

\[
\begin{aligned}
C(\lambda)
={}&\sum_i\lambda_i(z_i-g_i)\\
&+\sum_i\big[(\lambda_i-q_i)g_i+b_i(q_i-\lambda_i)_+\big]
=z_j<0.
\end{aligned}
\tag{4}
\]

Here z_i for i>j can be defined by the same expression using the extended g; its value is multiplied by zero. Every term in the second sum vanishes, and the only nonzero first-sum contribution is index j. This gives an explicit infeasibility certificate and also shows that feasibility is equivalent to all cuts (2).

**Sign correction.** The violating cut equals **z_j**, which is negative. It does not equal -z_j. If “negative z_j” meant merely “the negative-valued quantity z_j,” there is no disagreement. A one-coordinate example b_1=0 and c_1-F_1=-1 gives z_1=C(lambda)=-1 and rules out the opposite sign.

## Scope before inspecting the application

The theorem is an exact ordered capacitated-flow feasibility statement, not automatically a guarantee that the particular game-derived caps permit a solution. Its computational characterization and separating witness are nontrivial and useful after a sound construction of F,b,t,c. It supplies no missing universal nonnegativity of the cuts, no new current or successor IC, and no automatic bound on OPT or on the total repair cost. The application must separately show that all available repairs have exactly the asserted source refunds, nonnegative future increments, independent per-source upper bounds, and no omitted shared capacity.

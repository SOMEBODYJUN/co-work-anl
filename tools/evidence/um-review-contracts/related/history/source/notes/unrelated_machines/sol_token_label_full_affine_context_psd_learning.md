# 原作业共同 M2 的完整 affine-context 容量块

Scratch follow-up to SCRATCH-TOKEN-LABEL-M1-POSITIVE-M2-NO-CP-v1. This does not edit its frozen Exact or author proof. No independent review is claimed. It gives a directly checkable necessary matrix inequality for any original-job M2 point. It does not turn the earlier abstract nonextension point into a native integrality gap or give a general scheduling algorithm.

## Exact object and all-context block

Fix any explicit group of k>=1 original indivisible jobs. For each job a and each category i in a finite index set I, let x_a,i be an original endpoint indicator. An unavailable endpoint is zero. More generally i may index disjoint endpoint categories of this job; then x_a,i is the sum of its endpoint indicators in that category. The only algebra required is

\[
 x_{a,i}^2=x_{a,i},\qquad x_{a,i}x_{a,j}=0\quad(i\ne j)
\]

through total degree four, as follows from the original job Boolean/one-hot ideal. The chosen categories need not cover every endpoint. Define the linear aggregate occupancy

\[
 X_i=\sum_{a=1}^k x_{a,i}.
\]

It need not be Boolean; several original jobs may occupy one category. No assumption about processing times, canonical supports, identical menus, head capacity, or activation is needed in this paragraph.

Let L be any degree-four original-job functional whose common M2 is PSD. Let z_0=1,z_1,...,z_s be any fixed affine polynomials in all original assignment variables. They may include variables belonging to the selected job group itself. Then the single matrix indexed by (i,l) is necessarily PSD:

\[
 K_{(i,\ell),(j,t)}
 =k\,\mathbf1_{i=j}L(X_i z_\ell z_t)
  -L(X_iX_j z_\ell z_t),\qquad K\succeq0.                 \tag{1}
\]

All terms have degree at most four. This is a whole head-by-context matrix assertion, not merely one scalar constraint for each context or the Boolean context Y. Constants, arbitrary affine combinations, and distinct z_l,z_t are included.

## Direct SOS identity, without a true conditional law

For any real coefficient family c_i,l set t_i=sum_l c_i,l z_l and B=sum_i X_i t_i. Each t_i is affine and B has degree at most two. Put

\[
 q_a=\sum_i x_{a,i}t_i-B/k.
\]

These are degree-at-most-two original polynomials. Original same-job exclusion and Boolean equations give, through degree four,

\[
\begin{aligned}
 k\sum_{a=1}^k L(q_a^2)
 &=k\sum_a L((\sum_i x_{a,i}t_i)^2)-L(B^2)\\
 &=k\sum_i L(X_i t_i^2)
   -\sum_{i,j}L(X_iX_jt_it_j)\\
 &=c^T Kc.                                                \tag{2}
\end{aligned}
\]

The first equality uses sum_a sum_i x_a,i t_i=B. The second uses x_a,i x_a,j=0 for i!=j and x_a,i^2=x_a,i with affine products of degree at most two. The left side is nonnegative by common M2 PSD. This proves (1) for arbitrary global affine contexts, with no group averaging and no unproved completely positive stochastic lift.

For k=1 the matrix is zero by the same-job ideal. If the contexts are invariant under permutation of these k token labels, (1) is exactly the corresponding standard-label contrast block, up to positive normalization and redundant directions. If contexts include individual labels from this same group, (1) is still necessary, but it can carry higher label types as well; it should not be described as only that standard isotypic block.

## Replaying the frozen nonextension point

Use the frozen abstract point of `sol_token_label_lift_exact_v1.md`: k=4, ten X, delta=1/100, and context Y. Choose t_i=s_iY for its half-sign vector s. Then (2)'s right side is

\[
 L\left[Y\left(4\sum_iX_i-(\sum_is_iX_i)^2\right)\right]
 =\delta(16-20)=-1/25.
\]

Consequently no original-token M2 extension preserving those aggregate moments can exist. The sum of the four would-be q_a squared norms would be -1/100. This gives a shorter direct proof of the frozen Exact's nonextension assertion, without altering its earlier symmetrization proof or claim bytes. The actual ordinary context still has OPT1; rejecting this particular aggregate point is not a sound rejection of all schedules of that input.

## Computational scope

For any explicitly selected group and affine context basis, (1) is a rational linear matrix expression in moments of degree at most four. Its dimension is |I|(s+1), coefficients are exact, and writing or evaluating it is polynomial in the explicit data and the moment encodings. With the global original M2 present it is redundant, because (2) is its explicit SOS certificate. After projecting away job identities it need not be redundant: the frozen counterexample passes aggregate M2 and fails (1).

Adding all these blocks for a given polynomial list of groups and contexts is a valid way to strengthen an anonymous representation. No claim is made that they suffice to reconstruct every original M2 point. Enumerating all possible job groups is not free, an arbitrary exact SDP-feasibility solver is not assumed, and pointwise nonextension is distinct from infeasibility of the entire necessary system. Completing the full label-partition/Young blocks is a separate obligation.

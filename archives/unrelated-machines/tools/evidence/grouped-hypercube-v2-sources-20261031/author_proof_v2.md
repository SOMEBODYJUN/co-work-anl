# Proofs: grouped hypercube-slice scheduling, v2

Candidate ID: **UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2**.

Frozen on 2026-10-18. All hypotheses and exact statements A–E are in `um_grouped_hypercube_slice_scheduling_v2_exact.md`. This file provides proofs A–D. It preserves the v1 Hall and DGR arguments and adds the full-class `3/2` upper bound and exact sharpness proof. The new `3/2` strengthening was first proposed by root; independent reviewer rainbow supplied the concise Bernoulli argument below and independently obtained the same conclusion. This author independently verified both the argument and the sharp example.

## Proofs


### Proof of A

Fix an arbitrary choice `s(g)` and an arbitrary subfamily `F subseteq G`. Work first in a single variable gadget `U_x`. Let

\[
r_x:=|F\cap G(x)|\le d,
\]

and, for each label `i in [Q]`, let `t_i` be the number of groups in `F cap G(x)` whose selected state uses label `i` at `x`. These `t_i` are **nonnegative integers**, `sum_i t_i=r_x`, and the incidence-index injection guarantees that the `t_i` chosen cells of coordinate `i` are distinct.

Therefore the number of points not in any selected slice is exactly

\[
\prod_{i=1}^Q(d-t_i),
\]

and the selected union in this gadget has size

\[
\tag{P1}
d^Q\left(1-\prod_{i=1}^Q(1-t_i/d)\right).
\]

If `r_x=0`, the union and its required lower bound are both zero. If `d=1`, the separate disjointness argument in A establishes the result. Now assume `d>1` and `1 <= r_x <= d`, and set `z=1-1/d`, so `0<z<1`.

For an integer `t` with `0 <= t <= d`, Bernoulli's inequality gives

\[
1-t/d\le(1-1/d)^t=z^t.
\]

This is where integer slice counts matter; this inequality is not asserted for arbitrary fractional `t`. Multiplying the nonnegative factors yields

\[
\prod_i(1-t_i/d)\le z^{\sum_i t_i}=z^{r_x}.
\]

The sequence

\[
\frac{1-z^r}{r}=(1-z)\frac{1+z+\cdots+z^{r-1}}{r}
\]

is nonincreasing for positive integers `r`: the right side is `1-z` times the average of the first `r` terms of a nonincreasing sequence. As `r_x <= d`,

\[
\tag{P2}
\frac{d(1-z^{r_x})}{r_x}\ge1-z^d=c_d.
\]

Combining (P1) and (P2), the gadget union is at least

\[
c_d\,r_xd^{Q-1}=c_d r_xh.
\]

Sum over variables. The tagged universes are disjoint, so union sizes add, and

\[
\sum_xr_xh=\sum_{g\in F}|X_g|h=\sum_{g\in F}k_g.
\]

This proves (A1). Moreover `c_d >= 1-1/e`, since `(1-1/d)^d <= e^{-1}` for `d>1`; `d=1` was handled directly. The finite-Q integer restriction poses no additional problem: the product argument holds for every nonnegative integer vector `(t_1,...,t_Q)` of sum at most `d`.

For integral allocation, each subfamily `F` has at least

\[
|N(F)|\ge c_d\sum_{g\in F}k_g\ge\sum_{g\in F}b_g
\]

neighboring resources. The capacitated Hall condition therefore holds. Equivalently, clone group `g` into `b_g` unit-demand copies and apply ordinary Hall: any set of copies has a neighbor set equal to the union for its represented groups, which is at least the total demand of those groups and hence at least its own number of copies. This gives (A2), and standard integral max flow finds it. The same inequalities, without flooring, establish the fractional version. This proves A.

### Proof of B

In one `5 x 5` gadget let `a` and `b` count the selected slices of its two labels. They are rows and columns with distinct incidence indices, and `r=a+b <= 5`. Their union size is `5r-ab`, whereas their total slice size counting overlaps is `5r`. For fixed integer `r`, `ab` is maximized by balanced `a,b`, with maximum `floor(r^2/4)`. The exact minimum ratios are

| `r` | Maximum `ab` | Minimum union / total slice size |
|---:|---:|---:|
| 1 | 0 | 1 |
| 2 | 1 | 9/10 |
| 3 | 2 | 13/15 |
| 4 | 4 | 4/5 |
| 5 | 6 | 19/25 |

Thus the ratio is always at least `19/25`, with equality at `(a,b)=(2,3)` or `(3,2)`. Sum over variables and use the same Hall argument as in A. When `k_g=15`, `floor((19/25)15)=floor(57/5)=11`. This proves B.

### Proof of C

For C1, place each selector on its chosen state machine. Move all incidence jobs of chosen states to their corresponding resource machines; disjointness ensures at most one job per resource machine. Leave every incidence job of each unchosen state on its own state machine, where their total processing time is exactly `1`. All machine loads are at most `1`. At least one selector exists and has processing time `1` on every eligible machine, so the optimum is at least `1` as well.

For C2, place each selector `J_g` on `M_{g,s(g)}`. Move exactly the incidence jobs indexed by `u in B_g` from that chosen state machine to `R_u`. Leave all other incidence jobs on their own state machines. The disjoint `B_g` guarantee resource-machine loads at most `1`. Each unchosen state machine has load exactly `1`. A chosen state machine has load

\[
1+(k_{g,s(g)}-b_g)/k_{g,s(g)}=2-b_g/k_{g,s(g)}.
\]

Every job is scheduled, proving (C2) and then (C3). This proof also applies to the general nonuniform set-menu definition in C; the equal-cardinality specialization is used only to obtain the numerical bound `19/15`.

### Proof of D

For `d>1`, Bernoulli's inequality gives

\[
\left(1+\frac1{d-1}\right)^{d-1}\ge
1+(d-1)\frac1{d-1}=2.
\]

After taking reciprocals and multiplying by `(d-1)/d`,

\[
\left(1-\frac1d\right)^d
=\frac{d-1}{d}\left(\frac{d-1}{d}\right)^{d-1}
\le\frac{d-1}{2d}.
\]

Therefore

\[
\tag{P3}
c_d\ge\frac{d+1}{2d}.
\]

When `Q>=2`, every positive set size `k_g=q_g d^{Q-1}` is a positive integer multiple of `d`, so

\[
\tag{P4}
c_dk_g\ge\frac{k_g}{2}+\frac{k_g}{2d}
\ge\frac{k_g}{2}+\frac12
\ge\left\lceil\frac{k_g}{2}\right\rceil.
\]

For every group subfamily `F`, A1 and (P4) imply

\[
|N(F)|\ge c_d\sum_{g\in F}k_g
\ge\sum_{g\in F}\left\lceil\frac{k_g}{2}\right\rceil.
\]

Capacitated Hall or integral max flow thus supplies the resource subsets in D1. This proves the bound simultaneously for all groups, including odd sizes, without replacing `floor` by `ceil` without justification. The construction C2 now gives D2. If `d=1` or `Q=1`, apply A's separate disjointness argument and C1 instead; nonempty groups contain size-1 selector jobs, so the optimum in these degenerate cases is exactly `1`.

For sharpness, consider D3's explicit four-cell example. Suppose its UM instance had makespan `C<3/2`. Each state machine must carry its forced selector of size `1`, leaving capacity strictly less than `1/2`. No incidence job of private size `1/2` can remain there. Thus all four incidence jobs must go to their indexed resource machines. Every such job has size `1`, and `C<3/2<2`, so every resource machine can carry at most one incidence job. Only the three resources in `S_1 union S_2` are eligible for any incidence job. Four jobs cannot occupy three unit-capacity resource machines, a contradiction.

Conversely, export the job for `(1,1)` from the first state machine and the job for `(2,2)` from the second. Keep the other incidence job on each of its own state machines. The two state-machine loads are `1+1/2=3/2`; the two occupied resource-machine loads are `1`; all remaining loads are zero. This is a schedule of makespan `3/2`, completing D3.

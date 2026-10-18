# Author proof: one conditioned primary and pairwise-independent onehot helpers admit unit escape

Claim ID: UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1.

Author proof corresponding to the immutable Exact file tagged_affine_line_one_primary_pi_onehot_helper_unit_escape_exact_v1.md, SHA256 59e71e7d7c496b9dda2a993af5d0253072601190b5e78a8599dd06093fb47bbd.

This proof is frozen separately after root reported that general had completed its independent Exact-only reconstruction. Root had previously seen the strategy and is not a blind reviewer. The author sends this file only to root; any later reviewer release is controlled by root. No claims beyond the Exact domain are intended.

## 1. Condition each helper on the prescribed main label

Fix the arbitrary input indexed state \(s_M\) of the main. For each primary \(u\), let
\[
t_u=a_{M,s_M}(u).
\]

For a helper \(h\), write \(u=u(h)\). Its supplied primary marginal equals \(1/R\), so the following distribution on its original indexed states is well-defined:
\[
\mu_{h,s}=
\begin{cases}
R\lambda_{h,s},&a_{h,s}(u)=t_u,\\
0,&a_{h,s}(u)\ne t_u.
\end{cases}
\]
It is nonnegative and sums to \(1\). The primary label is always \(t_u\). For every auxiliary \(x\in A_h\) and \(a\in\mathbb F_R\), the specified primary–auxiliary pair marginal gives
\[
\sum_{s:a_{h,s}(x)=a}\mu_{h,s}
=R\!\sum_{\substack{s:a_{h,s}(u)=t_u\\a_{h,s}(x)=a}}\lambda_{h,s}
=\frac1R.
\]
No joint independence between two auxiliary variables has been used. The construction conditions one original indexed state distribution and never assembles separate coordinate labels into an invented state.

Every helper state has one positive cell of weight \(1\). Denote that resource by \(r(h,s)\). Define the rational flow
\[
f_{h,r}=\sum_{s:r(h,s)=r}\mu_{h,s}.
\]
Each helper has total outgoing flow \(1\).

## 2. Primary-plane capacities and avoidance of the main

Consider a primary variable \(u\). Every helper \(h\) with \(u(h)=u\) has its primary label fixed to \(t_u\) under \(\mu_h\). Its full primary line is therefore
\[
L_h=\{(u,z,t_u z+j_u(h)):z\in\mathbb F_R\}.
\]
The prescribed main state has the line with the same slope and intercept \(j_u(M)\). All these intercepts are distinct. Parallel lines of the same slope and distinct intercepts have no common resource point.

Consequently a resource in this primary plane is used by positive conditional flow of at most one helper, with total flow at most \(1\). No helper conditional positive resource in this plane can belong to the main's full selected line, hence none can be one of the main's positive resources. A helper has no other primary incidence, so no other helper can claim the plane except through the incidences just considered.

## 3. Auxiliary-plane capacities, including abscissa zero

The main contains no auxiliary variable. Fix an auxiliary variable \(x\), and a resource \((x,z,y)\).

If \(z\ne0\), then a helper \(h\) incident to \(x\) can have this point on its selected line only when its auxiliary label equals the unique field value
\[
a=(y-j_x(h))/z.
\]
Its conditional auxiliary label is uniform, so
\[
f_{h,(x,z,y)}
\le \Pr_{\mu_h}[(x,z,y)\text{ lies on the selected line at }x]
=\frac1R.
\]
There are at most \(R\) helpers incident to \(x\), because their intercepts are injective. Thus the total incoming flow at the resource is at most \(1\).

If \(z=0\), the selected line of \(h\) contains the point precisely when \(y=j_x(h)\), independently of its slope. Injectivity permits at most one such helper, whose total flow to the point is at most \(1\). Thus this case also obeys resource capacity \(1\).

These bounds do not require auxiliary neighborhoods from different primary blocks to be disjoint, do not impose auxiliary–auxiliary independence, and do not use a bound smaller than the stated variable degree \(R\).

## 4. Integral matching and recovery of actual original indexed states

Make a bipartite graph with one left vertex per helper and one right vertex for every resource with positive \(f_{h,r}\). Include the edge \(h r\) exactly when \(f_{h,r}>0\). The preceding sections give a fractional matching with left degree \(1\) and right degree at most \(1\).

For completeness, every helper subset \(J\) satisfies Hall's inequality:
\[
|J|=\sum_{h\in J,r}f_{h,r}
\le\sum_{r\in N(J)}1=|N(J)|.
\]
Therefore there is an ordinary integral matching covering every helper. A deterministic bipartite matching algorithm finds one. Every right vertex of this graph avoids all positive resources of the prescribed main state, by Section 2 and the disjoint primary/auxiliary namespaces.

For a matched edge \(h r\), positive \(f_{h,r}\) certifies at least one original state \(s\) with \(\mu_{h,s}>0\) and \(r(h,s)=r\). Store or find such a state by scanning its original indexed state table, and output that state. This recovers a legal full original indexed state, including all its auxiliary labels. It does not merely recover an independently chosen label for each variable.

Give helper \(h\) its matched resource, of weight \(1\), and give the main all positive resources of \(s_M\). The main's resources are distinct within its own complete state set and sum to \(1\). The matching and the primary-plane avoidance make all groups' assigned positive resources pairwise disjoint. Every group has quality exactly \(1\); no group can exceed \(1\), because all its state weights are nonnegative and sum to \(1\). This proves \(V=1\), for every prescribed main indexed state.

When there are no helpers, this construction simply gives the main all its positive resources. Empty auxiliary sets and unused auxiliary variables cause no change. The argument applies to \(R=2\) as stated.

## 5. Complete scheduling of all original jobs

Use the private roots and incidence jobs exactly as defined in the Exact file. For the main, put its selector on the root of \(s_M\). For each helper, put its selector on the root of the matched original state just recovered.

For every selected state, export precisely its positive incidence jobs to their assigned resource machines. Keep every zero-private-time incidence job of that selected state on its own private root. A selected root has load \(1\) from its selector and \(0\) from these zero jobs.

For every unselected indexed state of every group, keep all its incidence jobs on its own private root. Its load is exactly the sum of its original row weights, namely \(1\). This includes all states with zero supplied distribution mass and all baseline jobs; none is deleted or replaced. Every group has exactly one selector, already scheduled.

Every exported resource job has processing time \(1\). At most one such job is exported to each resource machine, so their loads are at most \(1\). All jobs in the complete instance have now been assigned to eligible machines, with makespan \(1\). Conversely every selector has finite processing time exactly \(1\), and at least the main selector exists. Hence the actual optimum is exactly \(1\).

The matching does not assert disjointness of all zero-weight portions of selected full geometric supports; these remain represented by original jobs kept on their private roots.

## 6. Rational certificates and total bit complexity

With explicit rational \(\lambda\), each \(\mu\) is obtained by multiplying by the integer \(R\), and each \(f\) is a sum over a subset of the explicit state table. Exact addition and comparison have bit complexity polynomial in the total input bit length. The graph has at most one left vertex per helper and no more right vertices or edges than the explicit onehot resource occurrences; it may also be constructed by scanning the full resource planes already present in the input. Deterministic matching, edge-state lookup, and the schedule output are polynomial in this expanded input. No denominator is unfolded into copies, and no \(1/\lambda\), permutation space, or compact implicit line family is enumerated.

If a suitable \(\lambda\) is asserted to exist only as nonnegative real values, write the finite feasibility LP on the original state variables of each helper. Its constraints are nonnegativity, total mass \(1\), the \(R\) primary marginal equations, and the \(R^2\) primary–auxiliary marginal equations per auxiliary incidence. All coefficients are rational with polynomial encoding length. The input state and line tables bound the numbers of variables and constraints polynomially. Standard rational linear programming either finds a rational feasible certificate of polynomial bit length or detects infeasibility. In the feasible case the construction above applies. In the infeasible case the algorithm reports only failure of this additional distribution interface, as the Exact statement requires.

The complete UM output has exactly the machines and jobs counted in the Exact. Its schedule can be output by scanning all original state-resource incidences. Unused planes can retain load \(0\). No polynomial bound in \(\log R\) alone is claimed.

## 7. Scope and standard technique attribution

The mathematical backend is ordinary conditioning of a finite distribution, line geometry, and Hall's bipartite matching theorem. No new matching or Santa-Claus rounding algorithm is claimed. The useful conclusion is the exact all-state/actual-job escape for this specified physical interface.

The proof uses every structural restriction that matters: one primary per helper, no main auxiliary incidence, one positive unit cell in each helper state, injective incidence intercepts, and the conditioned primary–auxiliary marginals. In particular, conditioning several primary labels at once need not preserve uniform auxiliary labels. Helpers with several positive cells also do not reduce to the same unit matching. No conclusion about those broader interfaces or about all balanced/pairwise-independent tagged-LINE menus follows.

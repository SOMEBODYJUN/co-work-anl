# Author proof: the common-simplex-coset pairwise-independent tagged-LINE family

Claim ID: UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1.

This proof corresponds to the immutable statement-only Exact file tagged_affine_line_pairwise_independent_simplex_tiny_value_exact_v1.md, SHA256 670bd2deb41f4b5fc9df6ca3f0ed460ca2daaa3a9cca38604561bfff3d7b10d2. It is frozen after root reported a separately frozen independent Exact-only reconstruction by bicriteria, SHA256 db3db1a1f09f1392ba880a749959171ea131d044acdb7772e0c315dcadf2112f. The author has not read that reviewer record or received its proof. Root and author discussed the construction before the Exact freeze, so root is not a blind reviewer. This author Proof is sent only to root for controlled later release.

Throughout, \(R\ge3\) is the odd prime of the Exact, \(K=\mathbb F_R[\omega]/(\omega^2-\nu)\), \(B=R^2+1\), \(\mathcal B=K\cup\{\infty\}\), \(\mathcal T=\{1+c\omega:c\in\mathbb F_R\}\cup\{\omega\}\), \(q=B(R+1)\), and \(G=1+B(R-1)\). We prove the padded construction actually stated in the Exact.

## 1. Trace pairing and projective representatives

The nonresidue assumption makes \(K\) a field of \(R^2\) elements. Its trace to \(\mathbb F_R\) is
\[
\operatorname{Tr}(a+b\omega)=2a.
\]
For \(t=a+b\omega\) and \(w=c+d\omega\),
\[
\operatorname{Tr}(tw)=2(ac+\nu bd).
\]
The resulting bilinear form is nondegenerate: its diagonal matrix in the basis \(1,\omega\) has entries \(2,2\nu\), both nonzero. In particular, for every nonzero \(t\), the functional \(w\mapsto\operatorname{Tr}(tw)\) is surjective onto \(\mathbb F_R\).

The displayed set \(\mathcal T\) represents exactly the one-dimensional \(\mathbb F_R\)-subspaces of \(K\). A nonzero element with nonzero constant coefficient has a unique scalar multiple of the form \(1+c\omega\); one with zero constant coefficient represents the subspace of \(\omega\). Distinct representatives are not scalar multiples over \(\mathbb F_R\).

Consequently, for nonzero \(w\), the kernel of \(t\mapsto\operatorname{Tr}(tw)\) is one-dimensional and contains exactly one projective representative from \(\mathcal T\). For \(w=0\), every representative is in the kernel. This proves that \(t_0(w)\) in the Exact is defined for every state.

We also need a converse. For every prescribed \(t\in\mathcal T\), the nondegenerate trace pairing provides a nonzero \(w\) satisfying \(\operatorname{Tr}(tw)=0\). Its kernel is the projective direction of \(t\), so \(t_0(w)=t\), independently of the ordering tie rule used at \(w=0\).

## 2. The one common four-dimensional code and local pairwise independence

For \(\zeta=(u,v)\in K^2\), write
\[
E_{a,t}(\zeta)=
\begin{cases}
\operatorname{Tr}(t(u+av)),&a\in K,\\
\operatorname{Tr}(tv),&a=\infty.
\end{cases}
\]
These are linear functionals of the four-dimensional \(\mathbb F_R\)-vector \((u,v)\).

The map \(E\) is injective. Indeed, its coordinates for block \(\infty\) determine \(v\), since their trace coefficients include a spanning set of \(K\). Its coordinates for block \(0\) likewise determine \(u\). Thus its image \(C\) has dimension \(4\) and exactly \(R^4\) codewords. Every group therefore has exactly the \(R^4\) distinct local tuples indexed in the Exact.

Each coordinate is uniform under uniform \((u,v)\). To check two distinct coordinates explicitly, first suppose they are in the same block \(a\). The variable \(w_a=u+av\), or \(v\) at infinity, is uniform in \(K\). For distinct \(t,t'\in\mathcal T\), the two trace functionals \(w_a\mapsto(\operatorname{Tr}(tw_a),\operatorname{Tr}(t'w_a))\) are linearly independent. The resulting map \(K\to\mathbb F_R^2\) is bijective, so this pair is uniform.

For two finite distinct blocks \(a,b\), the map
\[
(u,v)\longmapsto(u+av,u+bv)
\]
is an invertible \(K\)-linear map. Thus its two outputs are independent uniform elements of \(K\), and applying either specified nonzero trace functional gives a uniform independent label pair. A finite block and block \(\infty\) are handled by the invertible map \((u,v)\mapsto(u+av,v)\).

This proves all pairwise marginals for the main. Every helper's tuple is the same \(E(\zeta)\) plus a fixed offset vector \(-j\) on its original block and \(0\) elsewhere. Translation does not change either the one-coordinate or two-coordinate uniform distributions. In particular the proof covers every pair involving fresh variables, not just the original primary variables.

For identification with the full projective simplex code, its coefficient vectors in \(K^2\) are
\[
(t,ta)\quad(a\in K,t\in\mathcal T),\qquad (0,t)\quad(t\in\mathcal T).
\]
They represent every one-dimensional \(\mathbb F_R\)-subspace of \(K^2\) exactly once. A vector with nonzero first coordinate can be uniquely rescaled over \(\mathbb F_R\) to make that coordinate its representative in \(\mathcal T\), and then the ratio of the second coordinate to the first specifies \(a\). A vector with zero first coordinate is represented by \((0,t)\). This also explains the count \(q=(R^4-1)/(R-1)=(R^2+1)(R+1)\). No property of this code beyond the explicitly proved statements is required below.

## 3. Validity of every positive private weight and every incidence

For a main state \(\zeta=(u,v)\), if \(v\ne0\), then \(u+\alpha(\zeta)v=0\) for \(\alpha(\zeta)=-u/v\). If \(v=0\), its designated infinity block has \(w_\infty=v=0\). Therefore all main labels on its designated block are \(0\). Its intercept there is \(0\), so the resource \((x_{\alpha,t},1,0)\) is on its state line for every \(t\in\mathcal T\). The row has \(R+1\) such positive resources, each of weight \(1/(R+1)\), and hence total private weight \(1\).

For helper \(H_{a,j}\), in every state \(\zeta\), its original primary variable \(x_{a,t}\) has slope \(\operatorname{Tr}(t w_a(\zeta))-j\) and intercept \(j\). At abscissa \(1\) its line has ordinate \(\operatorname{Tr}(t w_a(\zeta))\). Thus, for \(t=t_0(w_a(\zeta))\), its designated positive point has ordinate \(0\) and is an actual state resource. Its weight \(1\) is its only positive private weight.

All other incidences in all full tagged lines are retained at private weight \(0\). The fresh-variable lines have no positive private weights. Every group contains one distinct variable per part; different variables' resource planes are disjoint. Each state consequently has exactly \(qR\) distinct state/resource incidences, regardless of coincidences in field coordinates inside different tagged planes.

At an original primary \(x_{a,t}\), the incident groups are the main with intercept \(0\) and the \(R-1\) helpers \(H_{a,j}\) with the nonzero distinct intercepts \(j\). There are exactly \(R\) such groups. A fresh variable has only its designated helper, with intercept \(0\). This verifies the injectivity and all degree claims without altering a supplied numbering.

## 4. Each helper's positive neighborhood is exactly its whole designated block

Every positive resource of every state of \(H_{a,j}\) belongs to
\[
\mathcal D_a=\{(x_{a,t},1,0):t\in\mathcal T\}.
\]
Conversely take any specified \(t\in\mathcal T\). Section 1 gives nonzero \(w\in K\) whose unique zero projective trace direction is \(t\). There is an original indexed state \(\zeta\in K^2\) with \(w_a(\zeta)=w\): for finite \(a\), use \((u,v)=(w,0)\), and for \(a=\infty\), use \((u,v)=(0,w)\). In that state the helper's unique positive resource is \((x_{a,t},1,0)\). Thus every point of \(\mathcal D_a\) can be its chosen onehot resource in a legal original state.

The expansion from an unpadded two-dimensional helper parameter \(w\) to the actual padded four-dimensional parameter \(\zeta\) only introduces distinct choices of fresh-variable labels. For each prescribed \(w_a\), there are exactly \(R^2\) states \(\zeta\) giving that value. Every such state is an original state of the padded menu and remains present. It is unnecessary to identify these different states or to delete their zero jobs.

## 5. Exact value against arbitrary state choices and partial allocations

Consider any state choice and any partial allocation of positive minimum quality \(v>0\). Every helper has only one positive cell in its chosen state, of weight \(1\). Positive quality therefore forces that whole cell to be allocated to the helper. For each block \(a\), its \(R-1\) helpers occupy \(R-1\) distinct resources of \(\mathcal D_a\), by pairwise disjointness of allocations.

Let \(\alpha\) be the block designated by the chosen main state. The main has positive weight only on the \(R+1\) points of \(\mathcal D_\alpha\), and the corresponding \(R-1\) helper cells already occupy distinct points of that set. At most two of its positive cells are available. Its quality is at most \(2/(R+1)\), so \(v\le2/(R+1)\). Allocations with minimum quality \(0\) obey the same upper bound trivially. Nothing in the argument requires complete selected supports to be allocated or disjoint; arbitrary zero or omitted cells cannot increase private-weight quality.

For the lower bound, choose the main state \((0,0)\), whose designated block is \(\infty\). In that block reserve any two points of \(\mathcal D_\infty\) for the main. Assign the remaining \(R-1\) points bijectively to its \(R-1\) helpers. In every other block assign any \(R-1\) different points of \(\mathcal D_a\) to its \(R-1\) helpers. Section 4 recovers an original helper indexed state for every assigned point. Every helper receives quality \(1\), the main receives quality \(2/(R+1)\), and resource sets from distinct blocks are disjoint. This proves the exact value.

This construction is algorithmic: finite-field linear equations or a scan of the original state table find a state for each desired positive point. It uses neither supplied full-allocation witnesses nor a constrained selection of permissible main states.

## 6. Complete ordinary-UM optimum, with no omitted original jobs

First use the attaining allocation of Section 5 to construct a full ordinary-UM schedule. Place each group's selector on its chosen private root. For the main's chosen state, export the two assigned positive incidence jobs to their resource machines. Keep its other original incidence jobs on that root. Their private-time sum is \(1-2/(R+1)\), so this root has load \(2-2/(R+1)\). Every chosen helper exports its unique positive incidence job; all its remaining original incidence jobs have private time \(0\), and its selected root has load \(1\). For every unselected state of every group, keep every original incidence job on its own private root. That root has load exactly \(1\). The assigned resource machines each receive one processing-time-\(1\) job, and all other resource machines receive none.

This schedules all selectors, all states' incidence jobs, every fresh-variable incidence, and every zero-private-time original job. There are no new outside options and no deleted baseline jobs. It gives the asserted upper bound.

For the lower bound, let an arbitrary complete eligible schedule have makespan \(C\). If \(C\ge2\), then \(C\ge2-2/(R+1)\) already. Suppose \(C<2\). Each group's selector identifies the private root of one of its original indexed states. In a selected helper root, keeping the unique positive job privately would make load at least \(1+1=2\). It must be exported to its own resource machine. Since each resource incidence job has processing time \(1\) on its resource machine and \(C<2\), two such exported jobs cannot share a resource.

For each block the selected helpers therefore occupy \(R-1\) different points of \(\mathcal D_a\), exactly as in Section 5. Let \(\alpha\) be the designated block of the main state whose private root contains its selector. No more than two of that state's positive jobs can be exported, because its other \(R-1\) block points are already occupied by selected helpers. Thus its private root has load at least
\[
1+\left(1-\frac{2}{R+1}\right)=2-\frac{2}{R+1}.
\]
Additional exports of unselected states can only consume resource capacity and do not invalidate this lower bound. Any additional jobs kept on the selected root can only increase its load. The lower bound covers every full schedule and proves the exact actual optimum.

## 7. Exact CSP value, including the fresh-variable completion

On a fixed original block, write
\[
C_{\rm block}=\{(\operatorname{Tr}(tw))_{t\in\mathcal T}:w\in K\}.
\]
This is a linear subspace of \(\mathbb F_R^{R+1}\). Every vector in it has at least one zero coordinate by Section 1. Therefore it contains no nonzero constant vector.

On the shared primary variables of block \(a\), helper \(H_{a,j}\) requires the tuple to belong to
\[
-j\mathbf1+C_{\rm block}.
\]
The cosets for distinct \(j\in\mathbb F_R\) are disjoint: their intersection would put a nonzero constant \((j-j')\mathbf1\) in \(C_{\rm block}\). The \(j=0\) coset is \(C_{\rm block}\) itself.

If a global assignment satisfies the main, then its restriction to every block lies in \(C_{\rm block}\), because it is the corresponding restriction of one main codeword. It then satisfies none of the nonzero-\(j\) helpers in any block. Such an assignment satisfies exactly the main, or at most one constraint in total.

If a global assignment does not satisfy the main, it can satisfy at most one helper in each of the \(B\) blocks, by the coset disjointness just proved. Hence no global assignment satisfies more than \(B\) constraints, since \(B\ge1\).

This bound is attained. Put primary label \(-1\) on every original variable. In every block \(a\), the helper \(H_{a,1}\) accepts these primary labels using its indexed state \(\zeta=(0,0)\). Give all fresh variables of these chosen helpers label \(0\), as required by that state; they are distinct across helpers and from all primary variables. Give all remaining fresh variables arbitrary labels. This satisfies all \(B\) chosen helpers simultaneously. The main cannot be satisfied by the all-\(-1\) primary tuple, because every main codeword has a zero coordinate, whereas \(-1\ne0\). Thus exactly \(B\) constraints can be satisfied, yielding the displayed value \(B/G\).

The proof is about ordinary global CSP assignments and fully specified common-coset tables. It does not substitute the local uniform distributions for global consistency.

## 8. Explicit size and the finite-table versus dense-matrix distinction

The field can be constructed with the stated nonresidue, or by scanning the explicitly bounded field for one; primality is part of the parameter promise. Field operations and all coefficients have bit length polynomial in \(\log R\). The lists of blocks, representatives, states, fresh variables, line incidences, and weights can be generated directly in polynomial time in their output sizes.

There are \(q\) original variables and \(H(q-(R+1))\) fresh variables. Every group has \(R^4\) states with \(qR\) incidence jobs per state. This proves the exact counts in the Exact:
\[
N_{\rm var}=q+H(q-(R+1)),\quad
N_{\rm state}=GR^4,\quad I_{\rm line}=GqR^5.
\]
The resource planes contribute \(N_{\rm var}R^2\) resource machines. The private roots contribute \(GR^4\) machines. There are \(G+I_{\rm line}\) jobs. Every incidence job has exactly its two finite entries, including private \(0\), and each selector has \(R^4\) finite entries. Hence the finite eligibility table has \(2I_{\rm line}+GR^4\) entries.

Here \(q=O(R^3)\), \(G=O(R^3)\), \(N_{\rm var}=O(R^6)\), \(N_{\rm state}=O(R^7)\), the number of resource machines is \(O(R^8)\), and \(I_{\rm line}=O(R^{11})\). Thus the explicitly listed states, full line incidences, and finite-option table have total size \(O(R^{11}\operatorname{polylog}R)\), as asserted. This is not the size of a dense all-jobs-by-all-machines processing-time matrix. If that representation is required, it has \(O(R^{19})\) entries, up to logarithmic tag encoding; it remains polynomial in \(R\), but must not be described as an \(R^{11}\) dense representation.

The explicit uniform local certificates assign \(1/R^4\) to every original state. Constructing those rational certificates, attaining allocations, global assignments for the CSP lower bound, and full schedules all takes total-bit-polynomial time. No expansion polynomial merely in \(\log R\), no compact-predicate oracle, and no artificial \(1/p\)-copy encoding is claimed.

## 9. What the example proves and what remains open

The exact family supplies an actual vanishing export value with uniform pairwise-independent local distributions, equal arity, partiteness, and one common additive-coset code. It rules out a universal constant actual-export guarantee derived solely from those structural facts. It has arbitrarily large helpers' joint primary sets, which is precisely outside the one-conditioned-primary obstruction.

It does not prove hardness or provide a partial-allocation decoder for arbitrary NO inputs. Its common code and arity vary with \(R\), and its \(q\asymp R^3\) lies outside the previously checked LST sparsification regime requiring \(R\) sufficiently large relative to fixed arity. Moreover, this particular construction has only one diffuse main group: deleting it leaves a unit-allocation matching for every remaining helper. A dummy-budget or deletion-robust hardness claim does not follow from its tiny minimum value. Those scope limits do not affect any exact value above.

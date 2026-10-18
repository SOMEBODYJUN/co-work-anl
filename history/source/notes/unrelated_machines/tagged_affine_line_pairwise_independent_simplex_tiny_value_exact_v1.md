# Exact statement: a common-simplex-coset, pairwise-independent tagged-LINE family with vanishing actual export value

Claim ID: `UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1`.

Status: statement-only author freeze for independent Exact-first review. This file supplies the complete finite objects and claims, without an author proof. It is a new claim, distinct from the one-conditioned-primary obstruction and the earlier merely single-incidence-balanced LINE family. No earlier version of this simplex family was frozen. The author and root discussed the construction before this freeze; root is not an independent blind reviewer.

## 1. Parameters, field, parts, and one common code

Let \(R\ge 3\) be an odd prime. Choose a quadratic nonresidue \(\nu\in\mathbb F_R\), and use the explicit quadratic field

\[
K=\mathbb F_R[\omega]/(\omega^2-\nu),\qquad
\operatorname{Tr}(a+b\omega)=2a.
\]

All arithmetic below is in these explicitly represented fields. Fix the projective representatives

\[
\mathcal T=\{1+c\omega:c\in\mathbb F_R\}\cup\{\omega\},
\]

in the displayed order, with \(c=0,1,\ldots,R-1\). Thus \(|\mathcal T|=R+1\). Put

\[
\mathcal B=K\cup\{\infty\},\quad B=R^2+1,\quad
\Pi=\mathcal B\times\mathcal T,\quad q=B(R+1).
\]

The set \(\Pi\) is the common set of \(q\) parts. For \(\zeta=(u,v)\in K^2\), define

\[
w_a(\zeta)=
\begin{cases}
u+av,&a\in K,\\
v,&a=\infty,
\end{cases}
\qquad
E_{a,t}(\zeta)=\operatorname{Tr}(t w_a(\zeta)).
\]

There is one common, explicitly specified linear code

\[
C=\{(E_{a,t}(\zeta))_{(a,t)\in\Pi}:\zeta\in K^2\}
\subseteq\mathbb F_R^q.
\]

The claim includes that \(C\) has dimension \(4\) over \(\mathbb F_R\), hence exactly \(R^4\) codewords, and that the uniform codeword distribution is uniform and pairwise independent on its \(q\) coordinates. In particular, every indexed state below corresponds to a different local label tuple. The common code is the four-dimensional full projective simplex code in this concrete representation.

## 2. Variables, groups, shared incidences, and all indexed states

For every part \((a,t)\in\Pi\), create a primary variable \(x_{a,t}\). There is one main group \(M\), containing these \(q\) variables, one in each part.

For every \(a\in\mathcal B\) and every \(j\in\mathbb F_R^*=\mathbb F_R\setminus\{0\}\), create a helper group \(H_{a,j}\). It contains the primary variable \(x_{a,t}\) in each part \((a,t)\) of its own block. In every other part \((b,t)\), with \(b\ne a\), create a fresh variable

\[
d_{a,j;b,t}
\]

belonging only to this helper, and put that variable in that part. All these fresh variables are mutually distinct and distinct from all primary variables. Thus every group has exactly \(q\) distinct variables and exactly one variable in each common part. There are

\[
H=B(R-1),\qquad G=1+H
\]

helpers and groups, respectively.

Every group has the full indexed state set \(K^2\), of size \(R^4\). No state is deleted. In main state \(\zeta\), variable \(x_{b,t}\) has label \(E_{b,t}(\zeta)\). In helper \(H_{a,j}\), state \(\zeta\) gives labels

\[
\begin{cases}
E_{a,t}(\zeta)-j,&\text{to its primary variable }x_{a,t},\\
E_{b,t}(\zeta),&\text{to its fresh variable }d_{a,j;b,t},\quad b\ne a.
\end{cases}
\]

Equivalently, every group's complete allowed local relation is a coset \(b_g+C\) of this one common code: \(b_M=0\), and \(b_{H_{a,j}}\) is \(-j\) on all parts of block \(a\) and \(0\) on every other part.

For each primary variable \(x_{a,t}\), the main incidence has intercept \(0\), and its incidence in \(H_{a,j}\) has intercept \(j\). Each fresh variable has just its own helper incidence, of intercept \(0\). Intercepts for distinct groups incident to any given variable are therefore injective. Every primary has group degree exactly \(R\); every fresh variable has degree \(1\).

The uniform distribution \(1/R^4\) on each group's indexed states is an explicit rational local distribution. The claim includes that, for every group and every two distinct variables of that group, the joint labels are exactly uniform on \(\mathbb F_R^2\). Each individual label is exactly uniform on \(\mathbb F_R\). This applies to all original and fresh variables and to all main and helper groups.

## 3. Complete tagged affine lines and the state-dependent weights

Each variable \(x\), primary or fresh, owns a disjoint resource plane

\[
\{(x,z,y):z,y\in\mathbb F_R\}.
\]

If group \(g\) has incidence intercept \(j_x(g)\) at variable \(x\), and state \(\zeta\) labels \(x\) by \(\ell_{g,\zeta}(x)\), its full state resource set is

\[
S_{g,\zeta}=
\bigcup_{x\text{ in }g}
\{(x,z,\ell_{g,\zeta}(x)z+j_x(g)):z\in\mathbb F_R\}.
\]

Every one of these \(qR\) state/resource incidences is retained. A zero private weight below does not remove an incidence, an indexed state, or an actual job.

For each block \(a\), define its \(R+1\) distinguished resources

\[
\mathcal D_a=\{(x_{a,t},1,0):t\in\mathcal T\}.
\]

Define a block index for every main indexed state by

\[
\alpha(u,v)=
\begin{cases}
-u/v,&v\ne 0,\\
\infty,&v=0.
\end{cases}
\]

The private weights of main state \((u,v)\) are \(1/(R+1)\) on all \(R+1\) resources of \(\mathcal D_{\alpha(u,v)}\), and \(0\) on every other resource of its complete state set. The claim includes that the displayed positive resources belong to that state set, and that these weights sum to \(1\).

For \(w\in K\), let \(t_0(w)\) be the first element of \(\mathcal T\) satisfying \(\operatorname{Tr}(t_0(w)w)=0\). This element exists for every \(w\), including \(w=0\). In state \(\zeta\) of helper \(H_{a,j}\), put private weight \(1\) on its single resource

\[
(x_{a,t_0(w_a(\zeta))},1,0)\in\mathcal D_a,
\]

and put private weight \(0\) on every other resource of that complete state set. The claim includes that this positive resource is on that helper's line in that indexed state. Every helper state has exactly one positive resource and total private weight \(1\).

All groups and all indexed states consequently have total private weight exactly \(1\). State weights may depend on the entire indexed state; there are no omitted exceptional states.

## 4. Exact partial-allocation and complete ordinary-UM conclusions

For this explicitly listed menu instance, define

\[
V=\max_{\substack{\text{one indexed state }\zeta_g\text{ per group}\\
A_g\subseteq S_{g,\zeta_g}\text{ pairwise resource-disjoint}}}
\min_g \sum_{r\in A_g}p_{g,\zeta_g}(r).
\]

Assignments may omit arbitrary resources and may use arbitrary subsets; they are not required to allocate full selected supports. The exact claim is

\[
\boxed{V=\frac{2}{R+1}.}
\]

There is a deterministic algorithm, polynomial in the total expanded input bit length, producing a state choice and disjoint allocation attaining this value. The upper bound quantifies over every indexed state choice and every partial allocation.

The associated ordinary unrelated-machines instance is defined completely as follows. There is one private machine \(P_{g,\zeta}\) for each indexed state and one machine for each resource in every variable plane. For every group \(g\), add one selector job eligible at processing time \(1\) on exactly its \(R^4\) private state machines. For every state/resource incidence \(r\in S_{g,\zeta}\), add its own distinct job, eligible at processing time \(p_{g,\zeta}(r)\) on \(P_{g,\zeta}\) and at processing time \(1\) on resource machine \(r\). All unspecified processing times are \(+\infty\). This definition retains every selector, every zero-private-time incidence job, and every incidence job of every unselected state. No extra jobs, preloads, or machines are implicit.

For this complete ordinary instance, the claim is

\[
\boxed{\operatorname{OPT}_{\rm UM}=2-\frac{2}{R+1}.}
\]

An attaining full schedule of all original jobs can be computed in deterministic total-bit-polynomial time. In particular the actual optimum tends to \(2\) as the prime \(R\to\infty\), despite all local state distributions being pairwise independent and all allowed local relations being cosets of the same common code.

## 5. Exact value of the associated ordinary additive-CSP instance

There is also a fully specified, unweighted additive-CSP instance over alphabet \(\mathbb F_R\). Its variables are all the primary and fresh variables above. For each group \(g\), include one constraint on its \(q\) variables in their common part order, with accepting relation \(b_g+C\), and no other constraints. An assignment is one global label in \(\mathbb F_R\) per variable. The objective is the fraction of the \(G=1+B(R-1)\) constraints whose complete tuples are accepted.

The claim includes the exact value

\[
\boxed{\operatorname{val}_{\rm CSP}=\frac{B}{1+B(R-1)},\qquad B=R^2+1.}
\]

This is a value calculation for this explicit family, not a complexity assertion. There are no assumptions about an actual satisfying assignment or a supplied global witness. The local rational distributions in Section 2 do not require such a global assignment.

## 6. Explicit representation and bit complexity

The construction may take \(R\) and a nonresidue \(\nu\) as parameters, or find a nonresidue by a finite-field scan. It outputs the explicitly listed states, labels, full line resources, all rational private weights, and the complete ordinary-UM jobs above. It does not assume a succinct cube or succinct state oracle.

With the common-arity fresh variables retained, the exact numbers are

\[
\begin{aligned}
N_{\rm var}&=q+H\bigl(q-(R+1)\bigr),\\
N_{\rm state}&=G R^4,\\
I_{\rm line}&=G R^4 qR,\\
N_{\rm resource}&=N_{\rm var}R^2,\\
N_{\rm machine}&=N_{\rm state}+N_{\rm resource},\\
N_{\rm job}&=G+I_{\rm line}.
\end{aligned}
\]

There are \(2I_{\rm line}+GR^4\) finite job/machine eligibility entries. Apart from tags and integer indices, the only finite numerical processing times are \(0,1/(R+1),1\). The explicit expanded size is \(O(R^{11}\operatorname{polylog}R)\); the code tables and local uniform rational certificates also have polynomial expanded size and bit length. Construction and the claimed attaining allocations/schedules are polynomial in that expanded size. No running-time claim is polynomial in \(\log R\) alone, and no enumeration with exponent depending on the numerical value of a hidden reciprocal weight is used.

The fresh-variable padding is part of this statement, not a free assertion of common arity or partiteness. It gives common arity \(q\), exactly one variable per part in every constraint, common code \(C\), and maximum variable group degree \(R\). If fresh variables and their zero-weight incidences are discarded, one obtains an auxiliary unpadded menu family with main arity \(q\) and helper arity \(R+1\), with the same actual allocation and scheduling values; common-arity claims in this file concern the fully specified padded construction.

## 7. Scope and nonclaims

This statement refutes a constant actual-export lower bound based only on the existence of uniform pairwise-independent local label distributions, even within this common-coset tagged-LINE setting. It does not establish an NP-hard promise gap or a reduction from a hard source family. The arity and the chosen common simplex code vary with \(R\); the exact family is not asserted to be the image of any particular Chan/LST reduction. The CSP value calculation is not a substitute for a decoder that works on every NO input of such a reduction.

Helpers here contain \(R+1\) primary variables jointly, so the statement lies outside the one-conditioned-primary interface. The main is diffuse, helpers are onehot, and all auxiliary fresh variables have only zero private weights. The statement does not contradict results requiring one primary per helper, a wide coordinate rectangle in each menu, or uniform positive weights on every full line resource.

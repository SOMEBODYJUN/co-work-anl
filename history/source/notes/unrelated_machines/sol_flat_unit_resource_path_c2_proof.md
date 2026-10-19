# Proof: flat unit-resource paths preserve the stated degree-four contract

Author: `/root/sol_literal_budget_attack`, 2026-10-18. Scratch mathematics, not independently reviewed or claimed novel. This proves only the contract of `sol_flat_unit_resource_path_c2_exact.md`, SHA256 `c2c590f3e916d992e6d591e25ccad0f1c8818586ed8a2b4d0a8fd5a2ab1be0d9`. It does not modify any earlier conditional-Hall claim or review. The observation that products of two linear Boolean forms are nonnegative at M2 when their Boolean defects are null was previously emphasized in discussion with `/root/sol_global_certificate`.

## 1. Representation and degree convention

Every incidence job e has private-root indicator 1−E_e and unit-head indicator E_e. Each selector has one assignment indicator per indexed state root; their sum is one. These substitutions use the exact one-hot job identities, including their allowed multipliers, and so are legitimate throughout degree four. All finite assignment indicators remain in the certificate; the reduced notation does not delete any job or endpoint.

A moment functional L is defined on real polynomials of degree at most four with rational monomial values. Boolean relations mean L((x²−x)h)=0 whenever deg h≤2; job identities are imposed against every multiplier keeping degree at most four. Its M2 condition is L(p²)≥0 for all real polynomials of degree at most two. A quadratic q is called null if L(qr)=0 for every r of degree at most two.

**Null lemma.** If L(q²)=0 for a polynomial q of degree at most two, PSD of M2 and Cauchy–Schwarz make q null. In particular, if x,y are Boolean assignment indicators and L(xy)=0 or L(x(1−y))=0, the corresponding quadratic is null: Boolean identities give L((xy)²)=L(xy), and likewise for x(1−y). All products used here have total degree at most four.

At a machine whose eligible jobs all have time one, any CONFIG of load at most T<2 contains at most one job. Therefore distinct eligible indicators x,y satisfy L(xy)=0 by same-machine pair agreement, and xy is null. This remains true when one of those jobs has private time zero elsewhere: its time on this resource is still one.

For any collection of mutually exclusive unit indicators x_e let K=Σ_e x_e. The polynomial K²−K is a linear combination of their null quadratic pairs and Boolean relations. Consequently

\[
L((K^2-K)h)=0\quad(\deg h\le2),\qquad
0\le LK\le1.
\tag{1}
\]

The lower bound follows from Lx_e=Lx_e²≥0. The upper bound follows from L((1−K)²)=1−LK≥0. For affine-linear q and T≥1, (1) gives

\[
L((T-K)q^2)
=(T-1)L(q^2)+L(((1-K)q)^2)\ge0.
\tag{2}
\]

Thus a unit resource's load localizer can be rebuilt from M2 and pair exclusivity. No positivity of arbitrary quartic literal products is being assumed.

## 2. Forward extension of the moment functional

Fix an old resource u with d≥1 positive-neighbor groups, ordered as in D_+. Its ports are 1,…,d. Partition **all original incidence jobs at u** according to their prescribed routed port. This includes every explicit zero incidence: it uses its group's port if that group has positive incidence at u, and otherwise the fixed fallback port. Let

\[
O_i=\sum_{e\text{ routed to }i}E_e,\qquad K=\sum_iO_i,
\qquad Q=1-K.
\]

Old unit-resource CONFIG implies that all distinct E_eE_f are null. Thus O_i are linear Boolean forms modulo these null relations, O_iO_j is null for i≠j, and O_iQ is null. Choose one fixed port f, for example d, and put

\[
H_i=O_i+\mathbf1[i=f]Q.
\tag{3}
\]

They satisfy Σ_iH_i=1 identically. Each H_i²−H_i and each H_iH_j, i≠j, is a linear combination of old null quadratic pairs and Boolean relations. These identities are valid against any multiplier of degree at most two. The H_i can be regarded algebraically as mutually exclusive hole indicators, without asserting a global probability distribution.

For path leaf j between ports j and j+1, define its two selector indicators and its two unit incidence head indicators by the same affine forms

\[
L_j=\sum_{i>j}H_i,\qquad R_j=\sum_{i\le j}H_i=1-L_j.
\tag{4}
\]

Here L_j is assigned to its left state/root at port j, and R_j to its right state/root at port j+1. Its left incidence private indicator is 1−L_j, and its right private indicator is 1−R_j. Each new assignment indicator is affine-linear in old indicators. Formulae (3)–(4) show that each is Boolean modulo the same old null relations, and all new job one-hot identities hold identically after substitution.

Define the new functional L' on every monomial of degree at most four by this affine substitution into L, leaving every original job-assignment variable unchanged except its physical head label. For a polynomial p of degree at most two, its substituted polynomial still has degree at most two. Hence L'(p²)≥0. Each new Boolean defect times a degree-at-most-two multiplier reduces to old null relations times permitted multipliers; all degree-four Boolean identities hold. New exact job identities hold as polynomial identities; old ones are preserved. Every original joint moment through degree four is unchanged.

For d=0 no path or port is added and the old resource is retained. For d=1, (3) gives H_1=1 and (4) adds no leaf. The formulae still apply, and the sole port has old occupancy K.

## 3. Forward machine CONFIG and load localizers

Keep every old private-root CONFIG list verbatim: its job identities, memberships, processing times and moments did not change. This includes all unselected states and all explicitly listed zero-time jobs. For each new leaf private root, use the singleton selector with weight L'L_j and the singleton private incidence with weight 1−L'L_j (or the analogous R_j pair). The two first moments are nonnegative and sum to one because the corresponding linear form is Boolean at M2. Their same-root product has moment zero. Both singleton configurations have actual load one≤T, and the private-root load polynomial substitutes identically to one.

At port i set R_0=0 and L_d=0. Its total load substitutes to

\[
O_i+R_{i-1}+L_i=O_i+1-H_i
=\begin{cases}1&i\ne f,\\K&i=f.\end{cases}
\tag{5}
\]

Every distinct pair of its job indicators has moment zero. Indeed, two original jobs are covered by old resource exclusivity. The two incident leaf jobs are disjoint sums of H_t. An original E_e routed to i is orthogonal to every H_t with t≠i: for t≠f this is old pair exclusivity; for t=f≠i use E_eQ=E_e(1−K), which is null by the same old pairs and Boolean identity. This proves orthogonality to both adjacent leaf sums. All these arguments are degree at most four.

For each port rebuild its CONFIG list as every eligible singleton job with its first-moment weight, plus the empty configuration with residual weight. First moments are nonnegative, and their sum is one for i≠f and LK≤1 for i=f. These lists therefore are rational probability lists of legal configurations and have the required first and pair moments. Resources with d=0 retain their old lists.

If load localizers are part of the contract, old private roots inherit them: an arbitrary new affine q pulls back to an old affine polynomial, while their old load polynomials are unchanged. New leaf roots and nonfixed ports have constant substituted load one, so their localizers are (T−1)L(q²)≥0. A fixed port has substituted load K, exactly the old resource load, so its localizer follows from the old global load localizer with that pulled-back q (also from (2)). Retained d=0 resources inherit their old localizers. Thus the forward direction preserves the full stated contract. If localizers are omitted on both sides, this paragraph is simply unnecessary.

## 4. Reverse: the path forces pair exclusivity of old head jobs

Take any valid lifted certificate, with no assumption that an original inactive state keeps its jobs private. Restrict attention to one old resource's d≥2 ports. For leaf j denote its selector indicators by L_j,R_j=1−L_j, and its incidence head indicators by F_j^L,F_j^R. The unit selector and the unit incidence private endpoint at its selected leaf root cannot coexist in a CONFIG when T<2. Hence

\[
L_j(1-F_j^L),\qquad R_j(1-F_j^R)
\tag{6}
\]

are null quadratics.

If an original job head indicator E uses a port also used by a leaf state selector X whose head indicator is F, then EF is null by unit-port CONFIG. From (6),

\[
L(EX)=L(EXF)=0.
\tag{7}
\]

The first equality uses X(1−F) against E, and the second EF against X. Since E,X are Boolean indicators, EX is null. Similarly if selectors X,Y of two adjacent leaf states use the same port, with head indicators F,G, then

\[
L(XY)=L(XYF)=L(XYFG)=0.
\tag{8}
\]

This uses X(1−F) against Y, Y(1−G) against XF, and FG against XY. No expression has degree more than four. Thus XY is null.

Set L_0=1 and L_d=0. Equation (8) says N_i=L_i(1−L_{i-1}) is null for every internal port i; boundary N_1,N_d vanish identically. Define linear forms

\[
H_i=L_{i-1}-L_i\quad(1\le i\le d).
\tag{9}
\]

They telescope to Σ_iH_i=1 and satisfy

\[
H_i^2-H_i=2N_i
\tag{10}
\]

modulo Boolean identities, so (10) vanishes against any multiplier of degree at most two. For i≠j this implies

\[
L((H_iH_j)^2)=L(H_iH_j)\ge0.
\tag{11}
\]

For the equality replace H_i² by H_i against H_j² (degree two), then H_j² by H_j against H_i (degree one). The inequality is M2 PSD for the quadratic H_iH_j. On the other hand

\[
1=L((\sum_iH_i)^2)
=\sum_iLH_i^2+2\sum_{i<j}L(H_iH_j)
=1+2\sum_{i<j}L(H_iH_j).
\]

All summands in the last sum are nonnegative by (11), so each vanishes. Equation (11) and the null lemma show that every H_iH_j, i≠j, is null. This argument uses M2 rather than an assumed global quartic literal positivity condition.

For an original head E routed to port i, (7) applied to its adjacent leaf states gives

\[
L(EL_i)=0,\qquad L(E(1-L_{i-1}))=0,
\]

with missing boundary states replaced by zero as above. Therefore L(EH_i)=LE. The quadratic q=E(1−H_i) has Lq=0; Boolean reduction of E gives

\[
L(q^2-q)=L(E(H_i^2-H_i))=0.
\]

Thus q is null. If original heads E,F use different ports i,j, their pair satisfies

\[
L(EF)=L(EFH_i)=L(EFH_iH_j)=0.
\tag{12}
\]

The first two equalities use E(1−H_i) against F and F(1−H_j) against EH_i; the final equality uses null H_iH_j against EF. Same-port original heads have pair zero directly from unit-port CONFIG. Consequently **all distinct original jobs at the same old resource have pair moment zero**, even when routed to different ports. Each original pair is then a null quadratic by Booleanity. This includes every original zero incidence head, whose processing time at its routed port is still one.

For d=1 all original heads share the one unit port, so no path argument is needed. For d=0 the old resource and its certificate are unchanged. These cases include resources with only zero incidences and entirely unused resources.

## 5. Reverse certificate and all original jobs

Keep the principal moment functional on all original assignment variables, identifying each original resource endpoint indicator with its routed port indicator. Principal restriction preserves M2 PSD, Boolean relations and the exact original job identities. Copy every old private-root CONFIG list from the lifted certificate. No new job belongs to those roots, so their legal loads and their first/pair agreements are unchanged.

For an old resource let K be the sum of **all** original head indicators there. Section 4 proves pair exclusivity; (1) gives 0≤LK≤1. Rebuild this old resource's CONFIG as each eligible original singleton job e with weight LE_e, plus empty with weight 1−LK. All are legal at T≥1, and they match every retained first and same-machine pair moment. Thus the linked CONFIG job marginals still cover every original selector and incidence exactly once. No other job is substituted for a zero incidence, and no unselected state's jobs are deleted. Retained d=0 resources may instead simply keep their supplied CONFIG lists.

Old private-root localizers are inherited by restricting affine q to old variables. Original unit-resource localizers follow from (2) for the rebuilt K. This proves the reverse direction with load localizers and also when they are omitted. Restriction preserves every original joint moment; it need not preserve a prescribed old resource CONFIG list or impose any global law of schedules.

## 6. Finite size, bit cost and parameter limits

Let I_+ be the number of explicitly positive original incidences. The sum of positive group-neighbor counts d_u is at most I_+. The number of new path leaves is Σ_u max(d_u−1,0)≤I_+. Each adds two private state roots, one unit selector and two unit incidence jobs; all their assignment endpoint counts are constant. Ports and retained d=0 resources are polynomial in the original explicit representation. Tags distinguish every original/new group, state, machine and job even when the old coefficient rows coincide. No grouping by identical rows is required.

The supplied certificate is a complete finite rational moment table through degree four and finite rational CONFIG lists; its actual length is charged. A sparse table can be expanded to the polynomially many monomials of degree at most four in the explicit variable count. Forward substitution replaces each new variable by an affine sum of at most a linear number of old variables with integer coefficients. Expanding a degree-four monomial uses at most a polynomial number of old moment entries; coefficients, rational sums and products have polynomial total bit length. Reverse restriction and the sums defining singleton weights have the same property. There is no expansion into 1/λ, inverse processing times or joint distributions, and no need to optimize or find arbitrary CONFIG lists. Copied private-root lists are charged to the supplied certificate size. All newly built resource and leaf-root lists have polynomial support.

The maps are deterministic with any fixed ordering and fixed slack port f. They construct valid rational certificates from valid rational supplied certificates in deterministic total-bit polynomial time. They do not assert a solver for finding such certificates, nor rational feasibility for arbitrary real semidefinite certificates.

The assumption T<2 is used precisely for unit-pair exclusion on ports and new leaf private roots. The assumption T≥1 makes each singleton legal and the rebuilt localizers nonnegative. For T<1 either side retains an original unit selector and hence cannot have a legal CONFIG job cover. At T≥2 the unit-pair exclusion need not hold, and no preservation claim is made. The proof allows arbitrary original inactive-state exports, all rational coefficients and zeros, and makes no additional canonical activation assumption.

# Fixed-degree whole-row CONFIG consistency: Exact only

ClaimVersion: SCRATCH-UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-d-v1.
Status: new author construction, not a new blind review. The subset interpolation strategy has been shared with identity; root has separately read the earlier first/pair construction. This is a distinct stronger claim, leaving every earlier frozen file unchanged. No hardness, canonical-C2, joint-CONFIG-indicator M2, or higher-degree load-localizer gap is asserted.

## 1. Quantifiers and ordinary input

Fix an integer d>=2. For every integer k>=d set

    s=d-1,
    Z=sum_(u=0)^s binom(k,u),
    Amax=binom(k-1,s),
    L=2k^2,
    M=1+120Lk^4+4k Z Amax,
    a=1/M,
    T=1+s/k,
    D=max(4,d).

Use M disjoint components, each with U_i, L machines B_i,b and k terminals Z_i,t. All types and all different indices are physically distinct. The complete original jobs are:

- one h, time one at each U_i;
- f_i,j for every i in [M], j in [k], time1/k at U_i and time one at every B_i,b;
- e_i,b,ell for every i in [M], b in [L], ell in [k], time1/k at B_i,b and time one at every Z_i,t.

Unlisted endpoints are infinity. All original jobs are indivisible and must run exactly once. Machine, job and finite-endpoint counts are respectively

    M(1+L+k), 1+Mk(1+L), M+Mk(1+L)+MLk(1+k).

This is an ordinary explicit binary-rational matrix with no source assignment, hidden good state, or oracle. Its true optimum is claimed to be exactly

    OPT=2-floor(sqrt(k))/k.

## 2. Stronger raw certificate contract

There is one common functional F on degree-at-most-D polynomials, with F(1)=1. Impose Boolean and same-job endpoint-exclusion equations multiplied by every monomial of degree at most D-2, and original-job cover equations multiplied by every monomial of degree at most D-1. Impose global M2 PSD on degree-at-most-two monomials.

Every original machine has a full CONFIG(T) distribution whose moments of EVERY same-machine endpoint monomial of degree at most d agree with F. This includes all mixed incoming-unit/home monomials, all pure-home monomials, repeated factors, and zero unit-clique products. The matching is not merely first/pair.

For every original machine v and every affine q involving all original endpoint variables, also impose the global load localizer F[(T-load_v)q^2]>=0. No higher-degree q or product-event load localizer is required. There are no common Boolean configuration-selector variables with all-degree links to endpoints, and no export<=activation or inactive-all-home restriction.

Claim: the explicit rational certificate in Sections 3-4 satisfies this entire system. For every fixed d, its degree-D moment table, CONFIG lists and global affine-localizer matrices can be generated in total time and total bit length polynomial in the expanded input length. The polynomial exponent may depend on the fixed d; no uniform polynomial claim for variable binary-encoded d is made.

## 3. Full finite global moment law

Select I uniformly from [M], assign h to U_I, and conditionally independently sample component I from H and every other component from Qnew.

H: choose a uniform injection sigma:[k]->[L]; put each f_i,j at B_i,sigma(j), and put every e job at its tiny home.

Let Qold be this finite complete-assignment law:

- probability1/2: all f/e jobs at home;
- probability1/4: choose (j,b) uniformly; put f_i,j at B_i,b, all other f at home; put all k e jobs of B_i,b at the k terminals using a uniform bijection, all other e at home;
- probability1/4: choose (b,ell,t) uniformly; export only e_i,b,ell to Z_i,t, all other f/e at home.

Define a second complete-assignment law Rfill:

1. choose b uniformly from [L];
2. choose S uniformly from all Z subsets of [k] with |S|<=s;
3. choose unit/no-unit by a fair coin; in the unit case choose j uniformly from [k] and put f_i,j at B_i,b; in the no-unit case keep all f home; every other f remains home;
4. keep exactly the e_i,b,ell with ell in S at B_i,b, and assign the other k-|S| original e jobs to distinct terminals by a uniform injection; keep all e jobs at every other B at home.

Set Qnew=(Qold+Rfill)/2 and define F(p)=E[p] under the global law. Each sample assigns every original job exactly once, including every unselected component's jobs. Qold has actual load at most1; Rfill has actual load at mostT; H has load1 at U/terminals and load1 or2 at B. The support can be exponentially large; only its degree-D moment table is output.

## 4. Explicit legal whole-row moment trade

For every concrete subset S of [k] with |S|<=s define

    b_S=(-1)^(s-|S|) binom(k-|S|-1,s-|S|).

At U_i and every terminal use the actual row marginal of the global law; those rows have load at most1 in every sample.

At a fixed B_i,b, let rho_Q be its actual legal row distribution under Qnew. Let C0,all denote no incoming unit and all k home e jobs. Let Cj,S denote incoming original f_i,j and exactly the home e jobs with labels in S; let C0,S denote no unit and those same home e jobs. The proposed CONFIG distribution is the following explicit signed expression, claimed to have nonnegative final masses after combining identical configurations:

    rho_CFG=(1-a)rho_Q+a delta_(C0,all)
              +(a/L) sum_(j in [k]) sum_(|S|<=s) b_S delta_(Cj,S)
              -(ak/L) sum_(|S|<=s) b_S delta_(C0,S).         (4.1)

This formula starts with the background (1-a)rho_Q; the full foreground baseline is exactly a delta_(C0,all). It does not add a second foreground term to an already retained raw H marginal.

Every configuration in (4.1) has load at mostT. Rfill supplies, in rho_Q, each Cj,S with probability at least1/(4LkZ) and each C0,S with probability at least1/(4LZ). Since |b_S|<=Amax and M-1>=4k Z Amax, these background masses absorb every possible negative correction. The final distribution sums to one.

Claim: (4.1) agrees with F on every same-B monomial of degree at most d. Its pure-home marginal in fact agrees in every degree, but no additional mixed-degree matching is asserted. For fixed d, all required row lists and their probabilities have polynomial output size and bit length.

## 5. Gap and precise boundary

Uniformly scale all finite processing times by k/(k+s). The same certificate is feasible at target1, and its true optimum is

    (2-floor(sqrt(k))/k)/(1+s/k) -> 2       (k->infinity, d fixed).

Since the ordinary CONFIG first-point two-approximation upper bound still applies, the raw system with this fixed same-row degree d has gap supremum2.

The certificate is not claimed to extend to stronger cross-row event conditioning. If A_i is the selector endpoint and C_i,b the incoming unit occupancy at B_i,b, then

    F[A_i C_i,b(T-load_B)]=a(k/L)(T-2)<0.

It also fails the next mixed same-row degree: for k>=d and any d distinct home labels ell_1,...,ell_d,

    F[R_j product_(u=1)^d Y_ell_u]=a/L>0,

whereas every legal CONFIG(T) containing R_j has at most s=d-1 home jobs and gives zero to that degree-(d+1) monomial. This states failure of this supplied point, not infeasibility of every point in the stronger system.

The common finite assignment law supplies PSD moment extensions in every degree; this must not be described as a full higher-order SOS gap, because the load-localizer and joint-configuration contracts have not been strengthened accordingly. Theorem status is mathematical construction pending separate proof review. Software status: none for this enhanced claim; the earlier k=2 first/pair finite audit is not relabeled as an audit of the present d-degree construction.

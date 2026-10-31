# Proof of fixed-degree whole-row consistency

This proves the new Exact `sol_diluted_shared_terminal_row_degree_d_exact_only.md`, SHA256 `e23ae495b4a997f081e0de06323e5dd9563c98d3828b78804ddc7670b16c9f6a`. The interpolation strategy and quantitative domination have been discussed with identity; this is an author proof, not a blind review. The earlier first/pair Exact/Proof remain unchanged.

Use exactly the new Exact's s=d-1, k>=d, L=2k^2, Z, Amax, M, a, T=1+s/k, D=max(4,d), physical machines, original jobs, H, Qold, Rfill and Qnew. In particular 1<=s<=k-1 and 1<T<2.

## 1. Original instance and its actual optimum

The number of components does not affect the exact optimum calculation. If h is at U_i in a complete actual schedule of target t<2, at least r=k-floor(k(t-1)) f jobs export to distinct B's. Each of those B's must export at least r original e jobs. The k original terminals therefore imply r^2<=k. With u=floor(sqrt(k)), this gives t>=2-u/k. Exporting exactly u f jobs to u distinct B's, then u e jobs from each to u^2 distinct terminals, and leaving every other original job home, attains 2-u/k. This covers all jobs of all M components and proves the stated true optimum.

The new global moment law is a finite rational law on complete assignments. Its expectation satisfies every original-job quotient equation in every degree and is PSD on squares of every degree. Restrict it to degree D to obtain the stipulated functional and M2. Under H, U and terminals have load at most1; under Qnew the same holds there. Rfill has at most one unit B, at most s home jobs there, and a matching of exported e jobs into distinct terminals. Consequently Qnew is pointwise legal at target T, and only H's B rows need replacement by a separate CONFIG law.

## 2. The explicit interpolation identity

Let s<k. For every |S|<=s set

    b_S=(-1)^(s-|S|) binom(k-|S|-1,s-|S|).

For every multilinear polynomial f(Y_1,...,Y_k) of degree at most s,

    f(1,...,1)=sum_(|S|<=s) b_S f(1_S).                   (2.1)

One proof uses finite differences at zero: f(1)=sum_(|A|<=s) Delta_A f(0), where Delta_A f(0)=sum_(S subset A)(-1)^(|A|-|S|)f(1_S). Collecting the coefficient of f(1_S) gives

    sum_(u=0)^(s-|S|) (-1)^u binom(k-|S|,u)
      =(-1)^(s-|S|)binom(k-|S|-1,s-|S|),

which proves (2.1). This also gives sum_S b_S=1. For |S|=t,

    |b_S|=binom(k-t-1,s-t)<=binom(k-1,s)=Amax.            (2.2)

Indeed the ratio to the t=0 coefficient is (s)_t/(k-1)_t<=1, with the empty ratio equal to one.

Fix a B row. On its at-most-one-unit state space, every endpoint polynomial p of degree at most d reduces pointwise, using Booleanity and the unit clique, to

    p(R,Y)=p0(Y)+sum_(j=1)^k R_j p_j(Y),

where deg p_j<=d-1=s. Pure-home p0 can have degree d. Let Cj,S mean unit label j and home subset S; C0,S mean no unit and home subset S. From (2.1),

    p(Cj,all)=p(C0,all)
               +sum_(|S|<=s) b_S[p(Cj,S)-p(C0,S)].       (2.3)

The pure-home part cancels in each difference, so it does not require interpolation of p0. All repeated-factor and multiple-unit monomials are handled by the same pointwise reduction.

## 3. Whole-row CONFIG lists, mass and nonnegativity

Let rho_Q be the B-row marginal under Qnew. Every configuration in its support is legal at T. Conditional H, this row has distribution

    (1-k/L)delta_(C0,all)+(1/L)sum_j delta_(Cj,all).

Insert (2.3), multiply by a, and add (1-a)rho_Q. The resulting measure is exactly

    (1-a)rho_Q+a delta_(C0,all)
       +(a/L)sum_(j,S) b_S delta_(Cj,S)
       -(ak/L)sum_S b_S delta_(C0,S).                     (3.1)

Thus (3.1) matches every degree-at-most-d row monomial of the moment law. It also preserves the pure-home marginal exactly in every degree, since the two corrections with the same S cancel whenever the incoming unit is ignored. The baseline a delta_(C0,all) is the full rewritten H contribution; it is not added on top of an unreplaced H marginal.

All states in (3.1) are legal: Cj,S has load1+|S|/k<=T, C0,S has load at most1, and C0,all has load1. Qnew's Rfill half supplies each Cj,S with probability1/(4LkZ), and each C0,S with probability1/(4LZ). A negative unit correction has absolute value at most a Amax/L, and a negative no-unit correction at most ak Amax/L. Both are absorbed by their background masses precisely when

    M-1 >=4k Z Amax,

which holds by definition. Other overlaps of configuration types only add nonnegative background mass. The corrections' total signed mass is zero because the sum over unit labels has k terms. The background and baseline have total mass (1-a)+a=1. This proves that (3.1), after combining equal states, is a genuine probability distribution, not merely a signed moment identity.

U and terminal rows use their actual row marginals and are already legal. For example U has h alone with probability a, exactly one f omitted with total probability3(1-a)/8 (uniform missing label), and all f home otherwise. All terminals contain at most one unit in each global sample. Every original machine is therefore covered.

## 4. Explicit global affine-localizer domination

Fix one B and let g=T-load_B. Under Qold, load<=1, so g>=s/k>=1/k. Under Rfill, load<=T, so g>=0. Therefore for every single-component affine q,

    E_Qnew[g q^2] >= (1/2k)E_Qold[q^2].                  (4.1)

Use nonhome endpoint variables to write q=beta+sum c_jb F_jb+sum d_b,ell,t G_b,ell,t. The old Qold has the following coefficient inequality, uniform in beta and d:

    E_Qold[q^2]>=||c||^2/(30Lk^3).                        (4.2)

For completeness, if q0, qN and qF denote its all-home, single-e-export and single-f-export values, the exact relation c_jb=qF_jb,pi-sum_ell qN_b,ell,pi(ell)+(k-1)q0 gives, by the three-term square bound and averaging the bijection,

    ||c||^2 <=3sum E_pi qF^2+3k sum qN^2+3kL(k-1)^2q0^2
              <=(12kL+12Lk^3+6kL(k-1)^2)E_Qold[q^2]
              <=30Lk^3 E_Qold[q^2].

The bounds on the three sums use Qold weights1/4,1/4,1/2 respectively. Thus (4.1) gives the quantitative, M-independent bound

    E_Qnew[gq^2]>=||c||^2/(60Lk^4).                       (4.3)

Under H, g=s/k-1{B selected}, so |g|<=1 and

    mu=E_H g=s/k-k/L=(s-1/2)/k>=1/(2k)>0.

All G variables vanish. If S=sum_j c_j,sigma(j), then E_H S^2<=(k/L)||c||^2. Completing the square in any intercept beta gives

    E_H[g(beta+S)^2]
      >=-(1+1/mu)E_H S^2
      >=-(1+2k)(k/L)||c||^2
      >=-2||c||^2.                                      (4.4)

Now take any affine q involving every original endpoint of all M components. Conditional on the selector I=h, components are independent. Center all components other than the fixed row's component i by their conditional means, and absorb those means and the selector coefficients into an arbitrary intercept beta_h. Exactly as a conditional variance identity,

    E[gq^2|I=h]
      =E[g(beta_h+q_i)^2|I=h]
        +E[g|I=h]sum_(j!=i)Var(q_j|I=h).                 (4.5)

Under Qnew, E g>0 because its Qold half has g>=1/k and its Rfill half has g>=0. Under H, E g=mu>0. The variance term in (4.5) is always nonnegative and can be discarded, with no factor depending on M or the number of contexts.

For h!=i apply (4.3) to the arbitrary beta_h; for h=i apply (4.4). Averaging gives

    F[gq^2]>=((1-a)/(60Lk^4)-2a)||c||^2>=0,

since M-1>=120Lk^4. This handles every global affine context and the growing number of components uniformly. At U and terminals, g>=s/k pointwise under the full law, so their global affine localizers hold immediately. No higher-degree q or product-event localizer is inferred.

## 5. Fixed-d output and bit complexity

For fixed d, s is fixed, Z=sum_(u<=s)binom(k,u)<=d k^s and Amax<=k^s. Hence M is a polynomial in k (with degree depending on fixed d), as are all ordinary input counts. The number of subset corrections in a B CONFIG list is at most(k+1)Z, also polynomial. The background Qnew row list is a mixture of the finite Qold row list and these low-home unit/no-unit Rfill states plus the all-home state. All probabilities in (3.1) are explicit rational quantities of polynomial bit length.

The common degree-D moment table has O(E^D) entries, where D=max(4,d) is fixed. Expand home variables affinely and condition on the selector; components factor. H and Qold head moments are partial-injection/permutation probabilities with at most D fixed heads. For Rfill, let r compatible distinct e heads be specified in one B. Their original e labels must be outside S, with probability

    sum_(u<=s)binom(k-r,u)/Z,

and their specified distinct terminal heads have conditional probability1/(k)_r. With one specified f head at that B, also multiply by1/(2kL); with no f head and at least one e head multiply instead by1/L. More than one distinct f head, e heads in different B's, or incompatible specified heads give zero. The empty monomial is one. Orders exceeding available labels are treated as zero before forming falling-factorial denominators. Qnew averages these rules with Qold. These formulas, or direct enumeration of the polynomially many S, generate every required moment with polynomially many rational operations for fixed d.

All relevant falling-factorial orders are bounded by fixed D. Their bit lengths and the binomial sums' bit lengths are polynomial in the expanded input. No enumeration of full injections, permutations or all-component support is required. The global M2 and machine affine-localizer tables are computed from this same moment table; their dimensions are polynomial in E. This proves the asserted deterministic total-bit polynomial certificate generation for each fixed d. It is not a uniform polynomial algorithm with variable d and is not a generic exact SDP solver.

## 6. Scaling, sharp raw gap, and limits

Scaling by k/(k+s) changes the target to1, preserves every local configuration's legality and every same-row moment match, and multiplies each load-localizer polynomial by a positive scalar. The actual optimum becomes (2-floor(sqrt(k))/k)/(1+s/k), tending to2 for fixed d. Every certificate's CONFIG first point still admits the standard assignment-slot two-approximation, so the gap supremum is exactly2.

The foreground H remains unchanged. With selector A_i and B unit occupancy C_i,b,

    F[A_i C_i,b(T-load_B)]=a(k/L)(T-2)<0.

In the explicitly specified finite-law extension, a unit R_j together with any d distinct home indicators has expectation a/L: H contributes this value, Qold contributes zero, and Rfill unit states have at most d-1 homes and contribute zero. Every legal CONFIG(T) assigns zero to that degree-(d+1) monomial. Thus the supplied finite-law extension meets degree d and fails the next stated mixed degree. When d+1>D, this observation does not assert that the degree-D restriction has no different extension. It also does not assert infeasibility of all possible stronger points.

Common Boolean configuration-selector M2, canonical inactive-home restrictions and higher-order load/event conditioning are not part of this construction. The first/pair local k=2 audit of the old claim provides no software verification of this new theorem; its proof is the explicit trade, quantitative inequalities and finite moment-generation formulas above.

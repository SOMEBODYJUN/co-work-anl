# One outer normalized-flat UM: a deterministic 13/8 algorithm

Root/boss11 author proof, 2026-10-18. Exact-only v2 SHA256 81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69. The typed explicit-menu domain is exactly that Exact. This is a special-case algorithm, not UM-TARGET-v1. No general algorithm or novelty claim is made. The old supplied-point epsilon-squared statement and its frozen sources are unchanged.

The proof uses the already independently reconstructed singleton closure and a stronger CDF-max welfare backend. This author has read the old supplied-point proof and the old Exact-first reconstruction; it is not an independent review. The new algorithm below uses eleven rational LP queries and a fixed rational safety margin. Its proof does not rely on a future reviewer or any unknown-source gated draft.

## 1. The actual flat value and explicit necessary LP

For each group and original indexed state, the complete ordinary matrix has its own private machine; there is one unit selector per group and one job for every listed incidence, with its original coefficient at the private machine and unit cost at its resource. All unselected states and zero incidence jobs remain. Put V=max over disjoint group bundles of their minimum maximum-state utility. The standard complete-flat identity is OPT=2-V: a witnessing allocation exports only the selected states' allocated positive jobs, leaving all other original jobs private; selected loads are 2 minus value, unselected loads one, resources at most one. Conversely any complete schedule of peak C<2 has at most one exported unit job per resource, and each selected state exports value at least 2-C. Since 0<=V<=1, actual OPT lies in [1,2].

For each rational 0<epsilon<=1 form precisely the plain common primitive-SA1 LP in Exact v1: state partitions, boxes, claim gates, resource capacities, and each state quality sum pZ>=epsilon A, all multiplied by every original A/Z primitive and its complement, with a single symmetric binary degree-two array. There are polynomially many explicit variables and rows, all rational. There is no PSD feasibility query and no extra unit-FSLP condition.

An actual allocation of quality V yields a zero-one state/claim point and its rank-one moments feasible for every epsilon<=V. Thus LP infeasibility at epsilon implies V<epsilon. This is the only rejection implication needed below; LP feasibility is never treated as an actual allocation. Standard deterministic rational LP supplies an exact feasible rational point of polynomial encoding length or correctly reports infeasibility.

## 2. Conditioning once supplies one common fallback packing

For a helper own singleton write A for its state and Z for its claim. The quality row Z-epsilon A>=0 multiplied by 1-Z gives Y_AZ>=mu_A; the gate and box rows give Y_AZ=mu_Z<=mu_A. Hence mu_A=mu_Z. The nonnegative gate A-Z, multiplied by any primitive F and by 1-F, then gives Y_AF=Y_ZF. Only the original common degree-two array is used; no triple moments are introduced.

Choose an outer state a with positive marginal rho and condition on its state primitive. Let w_j be its positive home coefficients, summing to one; let b_j be its conditional claims. For the corresponding row's helper j let alpha_js and zeta_jsu be its conditional fallback state and claim marginals, and f_j=sum_s alpha_js. All these come from the same row of the supplied point. Original partition/gate/value/resource rows under this one condition give

    sum_j w_j b_j >= epsilon,        f_j >= b_j,
    0<=zeta_jsu<=alpha_js,           sum_u p_jsu zeta_jsu >= epsilon alpha_js,
    sum_(j,s) zeta_jsu <= 1,         sum_s alpha_js=f_j<=1.

Other helpers' nonnegative claims can be omitted for this temporary packing. They are restored to their distinct homes later. Zero fallback state mass has zero claims; no division by zero is needed. The weighted fractional welfare Wf=sum_(j,s,u) w_j p_jsu zeta_jsu is at least epsilon^2>0.

## 3. Exact CDF-max welfare rounding, stronger than the uniform winner backend

Independently for each helper j choose fallback state s with probability alpha_js, or an empty algorithmic option with the remaining probability. Given a positive-mass state, request resource u with probability zeta_jsu/alpha_js. Give a requested item to a helper of largest score w_j p_jsu. These are new auxiliary random variables for a rounding proof, not a presumed joint law of the old moments.

For a fixed resource and positive score level d let beta_j(d)=sum_(s:w_j p_jsu>=d) zeta_jsu. Then q=sum_j beta_j(d)<=1. Independence across helpers implies

    P(max score>=d)=1-product_j(1-beta_j(d))
                     >=1-exp(-q)>=(1-1/e)q.

Summing the finite score-layer integrals and resource contributions gives expected weighted welfare at least (1-1/e)Wf > (5/8)epsilon^2. The last inequality follows from e>8/3 and Wf>=epsilon^2>0. No irrational comparison is used in the algorithm.

Derandomize by fixing helper states in a fixed order. Under any partial state choices compute the exact expected maximum score of the remaining requests by its finite CDF product at each original rational score level; for a fixed state its tail probability is 1[score>=d] zeta/alpha, for an unfixed helper it is beta_j(d), and for the empty option it is zero. Enumerate the next helper's positive-probability states/empty option and take the one of maximum conditional expectation. The average identity ensures no decrease. After all states are fixed, give each resource to a chosen-state helper of largest w_j p_jsu, or leave it unused if all scores vanish. This dominates the remaining request experiment item by item. Obtain disjoint real fallback bundles and chosen-state values Q_j in [0,1] with

    W=sum_j w_j Q_j > (5/8)epsilon^2.

The empty option has Q_j=0 and is not a new physical state. All CDF levels and choices are explicit. Conditional probabilities, CDF products and finite sums contain polynomially many supplied rational factors, with polynomial bit lengths. Fixed-order conditional expectation and final item maxima are deterministic total-bit polynomial. The stronger constant is for this CDF-max backend; it is not attributed to the earlier uniform-winner implementation or its audit.

## 4. A fixed rational quality line

Let a=13/8, b=10/8, d=1/256 and q=a epsilon-b+d. If q>0, then q<1 and

    (5/8)epsilon^2 > 2q-q^2.

Indeed for q0=a epsilon-b,

    (5/8)epsilon^2-(2q0-q0^2)
      =(209epsilon^2-468epsilon+260)/64 >=1/64

on [0,1], since this quadratic decreases up to epsilon=1. If q>0 then q0>-d, and replacing q0 by q0+d increases 2q-q^2 by at most 2d+d^2<1/64.

Let Good={j:Q_j>=q}, with outer weight z=sum_Good w_j. Since every value is at most one,

    W<=z+q(1-z).

If z<=q, this is at most 2q-q^2, contradicting the strict welfare bound. Thus z>q. Give the outer group these helpers' distinct home resources, retain Good's disjoint fallback bundles, and return every remaining helper of every outer state to its own home. All groups have quality at least q. Every selector and every original incidence job is then assigned by the complete-flat restoration of section1, with peak at most 2-q.

## 5. Unknown V: eleven explicit rational LP calls

Initialize l=0,h=1, with no feasible point stored. Repeat exactly eleven times: test the plain LP at epsilon=(l+h)/2; if feasible set l=epsilon and retain its point, otherwise set h=epsilon. Initially V<=h. Infeasibility implies V<epsilon, so V<=h remains true regardless of whether a feasible l exceeds V. At the end h-l=eta=1/2048 and l>=V-eta. No feasibility claim at epsilon=0 is used.

Set q=a l-b+d. If q<=0, use the explicit baseline complete schedule of peak two. In this case aV-b<=-d+a eta<0, hence V<10/13 and 2<(13/8)(2-V).

If q>0 then l>0 and there is a stored feasible point. Apply sections2–4 with epsilon=l. Its actual complete schedule has

    C<=2-q,
    q>=aV-b+d-a eta > aV-b,

because d-a eta=51/16384>0. Therefore C<(13/8)(2-V)=(13/8)OPT. This proves the claimed non-strict 13/8 approximation uniformly over this complete special-case domain, with no input-dependent approximation constant.

## 6. All original tasks and total bit cost

There are eleven LP calls, with dyadic thresholds of at most eleven fraction bits, and at most one conditional-expectation rounding. The LP dimensions are polynomial in the original state/claim count. Rational LP points, conditioning by a positive marginal, exact CDF products and comparisons all have polynomial total bit cost; no numeric reciprocal is used as a loop bound. This argument needs neither an input denominator lattice nor an exact nonlinear/SDP solver.

All helpers not kept in Good execute their original own state. Good uses a real original fallback state, since q>0 excludes the empty algorithmic option. Other outer-state payloads remain at their own distinct private machines. Every listed zero incidence may remain at its private zero endpoint; every original unused machine is retained. Duplicate indexed states are not collapsed. The output enumerates every original job exactly once at an original finite endpoint. There are no free auxiliary jobs, dropped groups or hidden occupancy constraints.

This proof uses the supplied structural presentation Q; recognizing that presentation from an arbitrary matrix is not claimed. It covers neither general normalized multicore menus nor arbitrary R||Cmax. Independent reconstruction/read-after, actual software scopes and novelty must be recorded separately; this author proof does not certify them.

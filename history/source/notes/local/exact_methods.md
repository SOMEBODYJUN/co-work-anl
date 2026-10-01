> **Historical research note (superseded frontier statements).** Preserve the derivation below as provenance; use [the current mathematical map](../../../../README.md), [claim registry](../../../curation-2026-10-01/CLAIMS.md) and [source-status guide](../../../curation-2026-10-01/PROVENANCE.md) for current scope.

# Exact algorithms for the two-facility client game

Research checkpoint, 2026-09-30. These results are independent of the unreviewed global golden-ratio proof. Only the final SPE corollary uses that proof. The code `threshold_dp.py` implements the pseudo-polynomial algorithm with exact Python fractions and retained parent layers. Its full load spectra were checked against independent ternary support enumeration on 530 instances with 0–8 common customers and rational private loads; every reported interval midpoint witness was independently Nash-checked. This is implementation evidence, not a substitute for the proofs below.

## 1. Coordinates and the threshold decomposition

Let A,B be the forced private loads, and let the common customers have weights w_i>0. Put δ=A−B, W=Σw_i, V=A+B+W, and Δ=L_A−L_B. For each common customer let c_i=w_i(2p_i(A)−1). Its Nash conditions are

* pure A: c_i=w_i and Δ≤w_i;
* pure B: c_i=−w_i and Δ≥−w_i;
* designated mixer: c_i=Δ and |Δ|≤w_i.

Designated mixers may have endpoint probability. This convention includes only genuine equilibria and simplifies boundary handling. The load identity is Δ=δ+Σc_i.

If Δ<0, every customer with w_i<|Δ| must choose A purely. If Δ>0, every such customer must choose B purely. All customers of weight at least |Δ| may take any of the three statuses, provided their common gap equation holds. Thus the support inequalities can be replaced by one sign and one cutoff in the sorted weight list.

Sort w_1≥...≥w_n. For j=0,...,n let H_j={1,...,j}, let ℓ_j=Σ_{i>j}w_i, and set

    low_j = w_{j+1} if j<n, otherwise 0;
    high_j = w_j if j>0, otherwise +∞.

Fix a sign ε∈{−1,+1}. All light customers i>j choose the lower-load side, A for ε=−1 and B for ε=+1. Assign statuses A,B,M to H_j. Let k be the number designated M, and z the signed pure weight in H_j (pure A contributes +w_i, pure B contributes −w_i, M contributes 0). Then precisely

    (1−k)Δ = δ−εℓ_j+z,
    low_j ≤ εΔ ≤ high_j.                         (1)

Every state satisfying (1) gives an equilibrium by assigning each designated mixer p_i(A)=(1+Δ/w_i)/2. Conversely, every equilibrium is represented: choose ε according to Δ, and put all weights at least |Δ| into H_j. At Δ=0 take j=n and either sign. Closed cutoff intervals deliberately duplicate boundary equilibria without adding false ones.

For k≠1, a state gives one rational gap. For k=1 it gives no gap unless δ−εℓ_j+z=0, in which case it gives the entire closed signed cutoff interval. Therefore the equilibrium load set is a finite union of rational points and rational closed intervals.

## 2. Pseudo-polynomial exact spectrum algorithm

### Theorem 1

If the common weights are positive integers, all equilibrium load values, the minimum load m(A,B), and any equilibrium satisfying rational load quotas can be computed in O(n²W+n log n) exact arithmetic operations. The private loads A,B may be arbitrary nonnegative rationals; their numerical magnitudes do not enter W. The operation bit lengths are polynomial in the original rational input length and log n.

The minimum value alone needs O(nW) state space. Retaining all parent layers for direct witness reconstruction uses O(n²W) space and preserves the stated time. Uniform bounds replace n²W by (n+1)²(W+1) when n=0. These are pseudo-polynomial bounds, not bounds polynomial in log W.

### Pseudocode

```
sort common weights decreasingly
D_0 = {(k,z)=(0,0)}
light = W
for j = 0,...,n:
    for (k,z) in D_j:
        for sign in {-1,+1}:
            numerator = δ - sign*light + z
            if k != 1:
                gap = numerator/(1-k)
                if low_j <= sign*gap <= high_j:
                    emit gap with witness reference (j,k,z,sign)
            else if numerator == 0:
                emit [low_j,high_j] for sign=+1,
                  or [-high_j,-low_j] for sign=-1
    if j<n:
        D_{j+1} = union over (k,z) in D_j of
                     {(k,z+w_{j+1}), (k,z-w_{j+1}), (k+1,z)}
        light -= w_{j+1}
```

The k=1 case cannot occur at j=0, so no emitted interval is unbounded. For j=n, low_j=0 covers the zero-gap equilibrium case. At j=0 the two signs also cover forced all-A or all-B equilibria with |Δ| greater than every common weight.

### Complexity proof

D_j has at most (j+1)(2W+1) states. Every transition and state/sign check has constant arithmetic cost. Summing over j gives O(n²W). Sorting costs O(n log n). The emitted piece count is also O(n²W); it can be streamed when only the minimum or one quota witness is required. For each state retain one predecessor because all Nash eligibility information depends only on j, sign, k, z; histories sharing this state are interchangeable. Reconstruct one chosen path in O(n), then recover the probabilities.

To enforce quotas L_A≥a and L_B≥b, intersect each emitted gap piece with [2a−V,V−2b]. Any nonempty intersection yields a witness. The minimum A load is (V+minimum emitted gap)/2. The minimum B load is (V−maximum emitted gap)/2, so one spectrum gives both ordered m-values.

Rational common weights can be multiplied by a common denominator, but the resulting W can be exponential in input length. This does not make the algorithm polynomial for arbitrary rational input.

## 3. Fixed-parameter algorithm for the number of distinct weights

### Theorem 2

Let d be the number of distinct common weights; they may be arbitrary positive binary rationals. The minimum equilibrium load and the existence/construction of an equilibrium with given rational quotas are fixed-parameter tractable in d: f(d)·poly(n,L), where L is the ordinary explicit-client input length. By a standard fixed-dimension integer programming bound one may take f(d)=2^{O(d³)}. This is an FPT statement, not merely n^{O(d)} count enumeration.

### Reduction to fixed-dimension ILP

Enumerate a sign ε, one of d+1 weight cutoffs, and the total designated mixer count K=0,...,n. Let H be the heavy weight classes and ℓ the total light weight. A heavy class h has weight v_h and multiplicity n_h. Use two nonnegative integer variables b_h,m_h for its numbers of pure B and designated M customers. The number pure A is n_h−b_h−m_h. Impose

    b_h+m_h ≤ n_h,
    Σ_h m_h = K,
    z = Σ_h v_h(n_h−2b_h−m_h).

There are at most 2d integer variables. For K≠1 substitute

    Δ = (δ−εℓ+z)/(1−K).

The signed cutoff and any quota bounds are linear inequalities in the integer variables, with rational coefficients. The objective of minimizing Δ is also linear (its sign changes when 1−K is negative, which is handled explicitly). Denominator clearing has polynomial bit cost. A fixed-dimension ILP algorithm solves each branch in f(d)·poly(n,L). For K=1 require δ−εℓ+z=0 and check whether the signed cutoff intersects the requested gap interval; any point in the intersection works. Individual customer probabilities are reconstructed from the counts.

The number of branches is O(dn). This claim assumes each customer is explicitly listed, as in the facility-location model. It does not establish an FPT polynomial bound for binary-encoded multiplicities with log n input length.

For golden-ratio quota endpoints, exact arithmetic in Q(√5) is sufficient. After clearing rational denominators, each ILP left side is integer; an algebraic upper or lower bound is replaced by its exact floor or ceiling. The K=1 interval intersection can be tested directly in Q(√5), and its endpoint supplies an exact algebraic witness. Thus the SPE application does not require floating-point approximations.

## 4. Global construction corollaries (conditional on the main phi theorem)

For every unordered layout, compute both ordered minima from its gap spectrum; obtain all d(t)=max_s m(s,t), and retain a minimizing equilibrium for either orientation when needed. Pick any maximizer map b and any directed cycle T. The main proof says that some layout in T² meets L_u≥q d(v), L_v≥q d(u). Search those layouts using the same quota oracle. The searches may recompute rather than retain spectra; this changes only a constant factor in the worst-case bound.

With integer customer weights of total W_all, the full procedure takes O(N² n² W_all) arithmetic operations, up to sorting/lower-order terms. A sharper instance bound sums k_{st}² W_{st} over queried layout pairs. With d globally distinct weights it runs in f(d)·poly(N,n,L). Thus both statements are genuine improvements on ternary enumeration.

To output a subgame-perfect profile, keep the on-path equilibrium and the minimizing equilibria only for its O(N) unilateral deviation profiles. On other labeled profiles use a deterministic pure-equilibrium routine: start from private loads, insert common customers in decreasing order of weight, assigning each to the currently less-loaded facility. This is a pure NE. Indeed, if a facility ends with larger load, its last assigned common customer had weight no greater than its earlier common customers; when it was assigned the facility was the lower-loaded one, and later assignments to the other facility only decrease the final gap. Therefore the final gap is at most this customer's weight, so every common customer on the higher side is stable. Customers on the lower side are automatically stable. The routine takes O(n log n). This gives a compact continuation rule and avoids unnecessary output of all N² client profiles.

The NP-hardness result in the companion hardness note blocks a general exact-polynomial m-oracle, unless P=NP. It does not rule out a polynomial algorithm for constructing a phi-SPE that bypasses exact m; the global existence search is a different problem.

## 5. Literature boundaries

* Krogmann–Lenzner–Skopalik–Uetz–Vos, IJCAI 2024, Section 2, records polynomial verification and efficient construction of some pure client equilibrium. Section 3's unweighted facility procedure has polynomial work per iteration, with its iteration count left open. Neither statement optimizes a designated facility's load over all mixed client equilibria.
* The same paper's Theorem 6 concerns deciding existence of alpha-SPE for alpha<phi, a global facility problem. It is not the local minimum-load hardness proved in the companion note.
* The fixed-dimension ILP solver is existing machinery (Lenstra 1983 and subsequent implementations/improvements). The new reduction here is the threshold/sign/K decomposition with 2d class-count variables.
* No claim of first-in-literature novelty is warranted from this limited search. A focused survey of extremal mixed Nash equilibria in weighted two-link routing remains appropriate before submission.

Primary sources read: https://www.ijcai.org/proceedings/2024/0315.pdf ; H. W. Lenstra, Integer Programming with a Fixed Number of Variables, Math. Oper. Res. 8(4):538–548, 1983, author-hosted copy https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1983i/art.pdf . A primary conference abstract documenting the classical parameter dependence is Kannan, STOC 1983, https://doi.org/10.1145/800061.808749 .

## 6. Highest-value next challenge

Prove a polynomial algorithm for finding a phi-SPE without computing exact m. A useful target is an adaptive certificate method that uses realizable upper bounds on deviation loads (specific punishment equilibria), and refines only failed inequalities. The local strong-chord polynomial constructor can discharge certain quota queries, while the NP-hardness result shows why demanding exact local minima everywhere is too strong. This remains a research target, not an algorithmic result established here.

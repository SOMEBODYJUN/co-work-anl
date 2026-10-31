# v2 partial-MinRep source: Exact-only independent blind review

## Provenance, frozen verdict, and scope

I read only the designated Exact Statement file:

`/workspace/scratch/038d9dcc4cac/near_unit_label_transfer_review/partial_minrep_linear_degree_source_v2_exact_statement.md`

Its actual SHA256 was verified as:

`067ebfea168a2047d4b9a533c17430afdfefff78a14c0cb473f61a401b83c906`.

I did not read the related proof, another review, or the parent agent's proof discussion, and did not discuss the proof with another reviewer before freezing this verdict. The argument below is my own reconstruction from the Exact Statement. No Git, Work, identity-registration, or credential operation was performed.

**Frozen verdict:** I find no fatal error in the explicit-game sparsification theorem, the strict degree-necessity statement, the total-bit complexity assertion, or the conditional fee calculation. The claimed probability 0.9 has generous room under the displayed constants. The fixed-parameter source-hardness conclusion remains conditional on the stated external perfect-complete Label-Cover PCP and parallel-repetition premises; I have not read or verified those external results or their citations. I independently reconstruct the two stated normalization operations below.

This review does not construct a UM instance, a physical scheduling compiler, a partial-trigger mechanism, or a projection/fee interface, and does not certify novelty.

## 1. Notation and the exact numerical parameters

The input is an explicit balanced D-regular bipartite total-projection game with N vertices, N/2 on each side, alphabet size Q>=2, and

    M = ND/2 >= 1

constraint edges, counting parallel edges separately. The integer g>=2 and rational 0<rho<=1 are binary-encoded. Write

    ell = floor(log_2 g),
    lambda = 1+ceil(log_2 Q),
    tau = rho/(100 g^2),
    gamma = rho^3/(10^9 g^8),
    mu = ceil(1000 g lambda/(rho ell)),
    Delta = 1000 mu.

Every projection is total. A multilabeling is a family of subsets of the common alphabet, with empty subsets allowed, and has cost equal to the sum of their cardinalities.

In the soundness analysis assume val(Pi)<=gamma.

## 2. Every cheap list family already covers less than tau in the original game

Fix any multilabeling psi of cost at most gN. Let alpha be its fraction of covered original edges. Define a vertex to be heavy when its list size is greater than

    L = 4g/tau.

There are at most gN/L heavy vertices. By D-regularity, the fraction of edges incident to at least one heavy vertex is at most

    (D gN/L)/M = 2g/L = tau/2.

This upper bound remains valid when an edge is counted twice in the incidence sum. If alpha>=tau, at least tau M/2 edges are both covered and have two light endpoints.

Choose a single label independently and uniformly from each nonempty light list; at other vertices choose an arbitrary label. Every covered light-light edge has some witnessing pair of labels, and that pair is selected with probability at least 1/L^2. Thus some singleton labeling satisfies at least the fraction

    tau/(2 L^2)
      = tau^3/(32 g^2)
      = rho^3/(32*10^6 g^8)
      > gamma

of original edges. This contradicts val(Pi)<=gamma. Consequently, simultaneously as a deterministic consequence of the original value promise,

    alpha(psi) < tau                              (1)

for every cost<=gN multilabeling psi.

There is no need to enumerate the multilabelings in the actual algorithm. This is an analysis lemma, and it handles empty lists and arbitrary alphabet size.

## 3. The low-degree branch

When D<2mu, the stated algorithm returns the original game unchanged. Its maximum degree is then below 2mu and hence below Delta. It is nonempty because D>=1 and N/2>=1. By (1), every cheap multilabeling covers less than tau<=rho of its edges. Therefore all the stated NO properties hold deterministically in this branch.

## 4. Sampling parameters in the other branch

Suppose D>=2mu. Let s be the least integer with 2^s mu>=D, and let p=2^(-s). Put

    d = pD,
    A = pM = Nd/2.

Minimality of s gives

    mu/2 < d <= mu,
    mu N/4 < A <= mu N/2.                        (2)

Let H denote the intermediate graph after independent p-sampling, and Y its number of edges. Then E[Y]=A.

For any fixed cheap list family, let X_psi be the number of its covered original edges that survive in H. By (1),

    E[X_psi] < tau A.                            (3)

The one-time trimming stage cannot increase X_psi. Its effect on the denominator will be bounded separately.

## 5. A uniform upper tail for all cheap list families

The number K of cost<=gN multilabelings is the number of subsets of at most gN among NQ vertex-label slots. An upper bound valid even when gN>NQ follows from the generating function at t=1/Q:

    K <= Q^(gN) (1+1/Q)^(NQ)
      <= exp(gN ln Q + N)
      <= exp(gN lambda).                         (4)

For one fixed multilabeling, set

    T = rho A/8.

Since T is well above the mean bound (3), the elementary binomial upper-tail bound gives

    Pr[X_psi >= T]
      <= (e tau A/T)^T
      = (8e/(100 g^2))^(rho A/8).

The inequality is also valid when the mean is zero, in which case the event has probability zero. Real thresholds cause no problem: the event is understood using the integer-valued random variable.

The logarithmic gain is essential. For g>=2,

    ln(100 g^2/(8e)) >= ell.                     (5)

Indeed g>=2^ell, the coefficient 100/(8e) exceeds one, and 2 ln 2>1. Combining (2), (4), and (5) yields

    Pr[there exists a cheap psi with X_psi >= rho A/8]
      <= exp(gN lambda - rho mu N ell/32)
      <= exp(-(121/4) gN lambda)
      < 0.01.                                   (6)

Here rho mu>=1000 g lambda/ell was used. In particular gN lambda>=8. This is why the sampled mean degree can be proportional to g lambda/ell rather than g lambda: the original cheap-list coverage was driven down to order rho/g^2, so the upper tail contributes a factor comparable to log g.

Thus, with probability greater than 0.99, every cost<=gN multilabeling covers fewer than rho A/8 intermediate edges, simultaneously.

## 6. Total edge count and loss from one-time trimming

The usual binomial lower-tail estimate gives

    Pr[Y < A/2] <= exp(-A/8) < 0.01.             (7)

For the last numerical inequality, ell<=g, lambda>=2, and rho<=1 imply mu>=2000. Since N>=2, equation (2) gives A>1000.

For a vertex v, its intermediate degree Z_v is Bin(D,p), with mean d<=mu. The exact size-biased binomial identity gives

    E[Z_v * 1{Z_v>Delta}]
      = d * Pr[Bin(D-1,p) >= Delta]
      <= d * (e/1000)^(1000 mu).

This also holds if Delta is larger than the possible binomial support, when the probability is zero. Write

    beta = (e/1000)^(1000 mu).

Let R be the actual number of edges deleted by the prescribed one-time trimming. Each deleted edge is incident to a vertex marked high using its degree in H, so

    R <= sum_v Z_v * 1{Z_v>Delta}.

Double counting only helps. Therefore

    E[R] <= Nd beta = 2A beta,
    Pr[R>A/4] <= 8 beta < 0.01.                 (8)

No independence between the high-degree vertex events is needed, and no iterative degree rule is substituted for the specified single intermediate-degree test.

On the simultaneous good events from (6)-(8), the final graph has

    M' = Y-R >= A/4 > 0.

Every cheap list family covers fewer than rho A/8 final edges. Consequently its final coverage is strictly below

    (rho A/8)/(A/4) = rho/2 < rho.

The success probability exceeds 0.97 by the union bound, so the promised lower bound 0.9 follows. In particular nonemptiness and the strict universal cheap-list coverage ban hold on the same good event.

## 7. Maximum degree and perfect completeness, for every seed

In the sampling branch, any vertex marked by its intermediate degree has all its incident edges removed. Every unmarked vertex originally has intermediate degree at most Delta, and later deletion cannot increase that degree. Thus the final maximum degree is at most Delta for every seed. The low-degree branch was handled in Section 3.

If val(Pi)=1, take any satisfying singleton labeling of the original game, with total cost N. Both sampling and trimming only delete original constraints and preserve their projections. The same singleton labeling satisfies every remaining edge for every seed. If the output is empty, the advertised completeness statement is vacuous, exactly as specified.

## 8. Uniform total-bit polynomial complexity

The displayed arithmetic quantities can be computed using binary integer/rational arithmetic with bit lengths polynomial in the explicit input length. In particular mu and Delta are not expanded in unary.

If D<2mu, the algorithm immediately returns the explicit original game. Otherwise mu>=1 and the required s is at most ceil(log_2 D). Each edge is sampled using exactly s independent fair bits, retaining it precisely when all bits are zero. Thus the random-bit count is at most M ceil(log_2 D), polynomial in the explicit graph size. The independence required in the statement is obtained by disjoint blocks of random bits.

Degrees can be computed by counting surviving edge records, and compared with the binary number Delta. One pass marks high vertices from these intermediate counts, and a subsequent pass deletes incident edges. The alphabet and each surviving projection are copied from the input. Output length is no greater than a polynomial in the explicit input length.

There is no loop of length g, 1/rho, mu, or Delta. The proof's enumeration of all cheap list families and the probability estimates are not performed by the algorithm.

## 9. Independent verification of the strict degree necessity

This conclusion does not need regularity or the random construction. Consider any nonempty balanced bipartite game with N/2 vertices on each side, M edges, and total projections.

Choose an arbitrary single label at every left vertex, at cost N/2. For any set of t selected edges, add the projected image of the chosen left label to the right list of each selected edge. This adds at most t labels in total and covers all t selected edges, even with parallel constraints. The resulting cost is at most N/2+t.

Let

    K0 = gN-N/2 = (g-1/2)N,

which is an integer. If rho M<=K0, then

    t = ceil(rho M) <= K0

and t<=M because rho<=1. The construction then produces a cost<=gN multilabeling covering at least a rho fraction of edges, contrary to the strict cheap-list ban. Hence necessarily

    rho M > K0,
    M > (g-1/2)N/rho.

Finally the maximum degree is at least the average degree 2M/N, so

    Delta_max > (2g-1)/rho.

The integer/ceiling step proves the displayed strict inequalities, not merely asymptotic versions. Total projections and balanced side sizes are exactly what the construction uses.

## 10. Independent normalization constructions

These constructions can be checked without reading the separate proof manuscript.

### Biregular to balanced regular, with exact value preservation

Suppose an explicit bipartite projection game is biregular with positive left degree d_A, positive right degree d_B, and M original edges. Let h=gcd(d_A,d_B). Make d_A/h copies of each left vertex and d_B/h copies of each right vertex. Replace each original constraint edge by the complete bipartite set of corresponding copy-pair edges, keeping its original projection on every copy.

The two new sides each have M/h vertices. Every new vertex has degree d_A d_B/h. A consistent copy labeling preserves any original labeling's value. Conversely, from any labeling of the copies, choose one uniformly random copy for each original vertex and use that copy's label. The expected original satisfied-edge fraction is exactly the satisfied-edge fraction of the copy labeling in the complete blowup. Hence some original labeling has value at least that copy labeling's value. Values are therefore equal, and perfect completeness is preserved.

There are at most M^3 copied edge records, so the blowup is polynomial for an explicit input. Parallel original edges are treated separately.

### Two alphabets to one common alphabet, with total projections

Suppose the left and right alphabets are Sigma_A and Sigma_B. Let Q=max(2,|Sigma_A|,|Sigma_B|), choose a surjection f:[Q]->Sigma_A and an injection i:Sigma_B->[Q], and replace each projection pi_e by

    pi'_e = i composed with pi_e composed with f.

These are total maps [Q]->[Q]. Every original assignment lifts to one with equal value. For a new assignment, any right label outside the image of i satisfies no incident edge; replacing it by any label in that image cannot reduce its satisfied-edge count. After those replacements, apply f on the left and i^(-1) on the right to obtain an original assignment with equal value. Thus the optimum value is exactly preserved. The alphabet size increases only to the larger original alphabet size, with the harmless lower bound 2.

The same argument works with explicitly given vertex-specific alphabets by using a separate local retraction/embedding at each endpoint and a common alphabet of maximum size. These operations do not by themselves supply the external PCP theorem.

## 11. Fixed-parameter source conclusion: verified algebra, external premise reserved

Conditional on a perfect-complete constant-alphabet Label-Cover PCP with suitable biregularity and an exponential soundness reduction under repetition, the target

    gamma = rho^3/(10^9 g^8)

requires repetition length O(log g+log(1/rho)). An alphabet exponential in that repetition length then has Q<=poly_rho(g). The normalizations in Section 10 preserve value and do not increase this alphabet order. This explains the stated parameter algebra, conditional on those external theorem hypotheses and their quantitative guarantees.

When Q<=poly_rho(g), lambda/ell is bounded by a constant depending only on fixed rho. Hence

    Delta = 1000 ceil(1000 g lambda/(rho ell)) = O_rho(g).

For arbitrary explicit Q without this source premise, the unconditional theorem promises the displayed Delta, which may be larger than O_rho(g); the Exact Statement correctly distinguishes these scopes.

I have not consulted or verified the external PCP/repetition citations. Thus this review establishes the full explicit-game deletion theorem and the two normalization mechanisms, but leaves the external source theorem as a stated prerequisite rather than claiming an independently sourced hardness theorem.

The complexity distinction is correct: g and rho may be fixed before the SAT reduction, and the polynomial exponent of that external reduction may depend on those fixed parameters. This does not claim a uniform polynomial PCP chain for binary parameters that grow with the SAT input. The deletion stage itself is uniformly total-bit polynomial, as proved in Section 8.

The randomized reduction assumption is also correctly scoped. If the resulting promise problem had a deterministic polynomial-time solver, composing it with the reduction would decide SAT with no error on YES and at most 0.1 error on NO. Thus NP not contained in BPP is a sufficient contradiction hypothesis. P!=NP alone does not provide that contradiction for this randomized reduction.

## 12. Conditional physical-fee calculation

Assume, only as a separate compiler obligation, that an actual weak schedule produces lists covering at least rho M real source edges and satisfying

    cost <= N+B(sigma)/F,
    B(sigma) <= cM,

where F>0. Maximum degree Delta gives M<=N Delta/2, hence

    cost <= N + cN Delta/(2F).

If F>=c Delta/[2(g-1)], the right side is at most gN. On the good NO source event this contradicts the strict coverage ban. Thus that conditional implication is algebraically valid.

For fixed rho and Delta=O_rho(g), the ratio Delta/(g-1) is bounded independently of g>=2, so a sufficiently large constant fee suffices if c is also bounded as stipulated by the compiler. This proves neither that the fee equals 1 nor that a physical implementation realizes it. The Exact Statement properly leaves those obligations open.

## Final review status

Accepted as a correct explicit-game sparsification statement, including perfect YES for every seed, simultaneous cheap-list NO soundness with probability at least 0.9, strict degree necessity, and binary-parameter complexity. The larger-alphabet fixed-parameter source conclusion is conditional on the unread external PCP/repetition prerequisites. No physical UM compilation or novelty claim is certified by this review.

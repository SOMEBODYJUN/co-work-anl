# Independent review: overlap gives an unrestricted price certificate

Reviewer: internal researcher f_adversarial, 2026-10-21. Reviewed `orbit_overlap_price_certificate.md` by independently rebuilding its inequalities. Verdict: the principal theorem, the two-block overlap calculation, and the stated one-minority SPE consequence are valid under their explicit hypotheses. The proof does not settle general Q-CAG-HALF. No numerical experiment is needed for this review.

The source theorem can be strengthened: its principal argument needs only a balanced partition, rather than an automorphism group. The author and parent were notified of this strengthening before this review was written.

## 1. Independent principal theorem, with the weaker hypothesis

Partition the finite unit-customer set into cells O. Assume that for each cell O there is p_O in [0,1] such that every menu theme T satisfies

    |T intersect O| = p_O |O|.

Empty cells can be omitted. Fix any actual m-provider profile and one provider i. Suppose on every cell that

    R_O := sum_(j != i) |S_i intersect S_j intersect O|
          <= (m-1) p_O^2 |O|.                         (OC)

No equilibrium assumption is imposed here.

Let A_O=|S_i intersect O|=p_O|O|. For p_O>0, Cauchy-Schwarz gives the exact chain

    u_i(O) = sum_(x in S_i intersect O) 1/(1+L_x)
           >= A_O^2/(A_O+R_O)
           >= |O| p_O/[1+(m-1)p_O],                  (L)

where L_x counts the other actual providers covering x. If p_O=0, A_O=0 and both the desired lower bound and the actual contribution are zero. Repeated actual actions create repeated terms in R_O and cause no change to this argument; (OC) itself must still be checked.

For any nonnegative real portfolio z of total mass tau, put d_x=sum_(T contains x)z_T. The balanced-cell assumption gives

    sum_(x in O) d_x = sum_T z_T |T intersect O|
                      = tau p_O |O|.

Jensen for the concave function s -> min(1,s) therefore yields, directly on the customers in each cell,

    C_O(z) <= |O|min(1,tau p_O).                      (U)

There is no need to average the theme vector under a group. In particular, the principal theorem applies to any equal-cardinality menu satisfying the corresponding one-cell overlap condition, even when no theme-transitive group exists.

For p in [0,1] and tau>=0 set t=tau p and alpha=(m-1)p. Then

    min(1,t) <= (t+alpha)/(1+alpha).

For t<=1 this is alpha*t<=alpha; for t>=1 it is 1<=t. Consequently

    min(1,tau p) <= (tau+m-1)p/[1+(m-1)p].

Combining this with (U) and (L), then summing the cells, proves

    C(z) <= (tau+m-1)u_i

for every real tau>=0, including tau<1 and tau=0. Taking the supremum over all finite theme-weight vectors gives

    B(u_i) <= (m-1)u_i.

If i has minimum actual utility, then m*u_i<=W. An optimal m-theme tuple, with repeated themes combined into their integer weights, is a legal portfolio of mass m. Hence

    OPT_m <= (2m-1)u_i <= (2-1/m)W.

Every division above has been restricted to its positive-denominator case. The m=1 case is valid as well: alpha=0 and the price bound is B(u_i)<=0. If u_i=0, the displayed C(z) inequality immediately gives C(z)=0 for all z, so zero welfare requires no ratio convention.

## 2. Verification of the original orbit hypothesis

If a finite incidence-preserving group acts transitively on the themes and O is a customer orbit, the membership count t_O is constant across O. Theme transitivity makes |T intersect O| constant across themes. Double counting gives q*|T intersect O|=t_O*|O|, exactly the balanced-cell assumption with p_O=t_O/q. Thus the original group formulation is a valid special case of the reconstruction above.

The inference requires actual invariance of the customer incidence multiset, not only equal aggregate theme sizes. The one-cell version mentioned above separately states its stronger global overlap requirement and does not pretend to recover arbitrary orbit information from equal sizes.

## 3. Independent two-block covariance calculation

For k>=2, full within-block permutations plus block swap give customer orbits with a memberships in one block and b in the other, together with the swapped pattern when a!=b. Let t=a+b and p=t/(2k). For two distinct labels in the same block and for a cross-block pair, respectively,

    rho_same = [a(a-1)+b(b-1)]/[2k(k-1)],
    rho_cross = ab/k^2.

These remain correct when a=b; there is no need to count a swapped copy twice. They satisfy

    rho_cross <= p^2,
    rho_same+rho_cross-2p^2
      = [(a-b)^2-t(2k-t)]/[4k^2(k-1)] <= 0.

The last sign follows from a^2<=ka and b^2<=kb. If the chosen provider has r-1 distinct same-block opponents and m-r opposite-block opponents, and r<=(m+1)/2, then

    (r-1)rho_same+(m-r)rho_cross
      = (r-1)(rho_same+rho_cross)+(m-2r+1)rho_cross
      <= (m-1)p^2.

Multiplication by |O| gives exactly (OC). All coefficients are nonnegative because r>=1 and m-2r+1>=0. The full conclusion therefore holds for the stated minority or near-minority provider. Repeated actual labels would replace some distinct-pair probabilities by p; they are not covered by this covariance computation. The source correctly keeps this restriction.

## 4. Review of the one-minority SPE consequence

For a profile using one distinct X label and m-1 distinct Y labels, within-block symmetry makes every majority provider's terminal payoff the same number b, regardless of move order. Call the minority payoff a.

If a<=b, the minority provider is a minimum-utility provider satisfying (OC), so the principal price theorem applies directly. If b<a, at least one of the last two providers is a majority provider. The genuine last-player or genuine penultimate-player price certificate applies to that provider at its actual position. The cited penultimate source gives

    B(u_penult) <= W-kappa_m*u_penult,
    kappa_m=(m+1)/[2(m-1)]>0,

for m>=3, and has an independent actual-menu proof retaining arbitrary histories and ties. Thus the source's case split validly proves B(min(a,b))<=W. The last-player source can also be recovered directly with prices y_x=p_x/(p_x+1), using the actual fixed-prefix loads.

This price statement retains useful information even though the simpler two-image geometry already proves half coverage for every distinct-label profile in this two-block symmetric class. The stronger endpoint deduction when the minority moves first is also valid, because the last provider must then be in the majority.

The source's cross-workspace endpoint reference should use its full relative path or an explicit link in a final shared version; the mathematical dependency is the file `research/workspaces/customer-attraction/R-e5d83af532dc495c966f99cf70cda2a2/parent_tail/penultimate_price_defect.md`.

## 5. Limits that must remain explicit

A minimum provider need not satisfy (OC), and incidence symmetry alone does not force that provider into a qualifying block. The theorem cannot be extended to a general menu by assuming the missing overlap inequality. The two-block calculation assumes distinct actual themes; the general balanced-partition theorem permits repeats only when its independently stated overlap condition holds. These are mathematical boundaries, not gaps in the proved conditional theorem.

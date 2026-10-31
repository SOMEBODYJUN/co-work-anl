# Independent checks: aligned fixed point and canonical reset-floor domain

2026-10-25, matching12 continuation. Arbitrary players/common finite
catalog/every full-history pure SPE remain the research object. HALF and
all numerical covariance payments remain OPEN. No finite scan was used.

## 1. Aligned conditional-menu fixed point

Read `../tree/aligned_credible_menu_fixedpoint.md` in full. Its product Q
of conditional mean-cap lottery polytopes is fixed independently of p,
nonempty, compact and convex. The actual-action component is a singleton,
which causes no problem. All complete pure tail-SPE witnesses form a
finite set in a finite game, so this is finite-dimensional Kakutani.

The load map L(p,q) is continuous and affine in q for fixed p. All
denominators are at least one. Thus the q objective is jointly continuous
and convex in q, and its fixed compact feasible domain gives a nonempty
compact convex argmin correspondence with closed graph by Berge's
theorem. The p correspondence is the simplex face over whole themes
maximizing the continuous t-price at the CURRENT load; it likewise has
nonempty compact convex values and closed graph. Their product meets
Kakutani's conditions. The existence argument is sound.

At p_A>0, q-minimality does imply conditional maximization of the gradient
shadow rho*t^2 within that action's mean cap. At p_A=0 no such condition is
asserted. Price support is a best response to the fixed produced load,
not a p derivative internalizing the load's p dependence. Accordingly this
is not a minimax saddle and no minimax-small gamma is inferred.

The fixed-point set is closed in a compact domain, and gamma is continuous;
a minimum-gamma fixed point exists. This is an existence fact, not an upper
bound on that minimum.

The source/background mean action marginals are the same p. Consequently
the decoupled C term is zero and C equals centered Cov. The displayed
ALIGNED-BAL signs and the Qfuture alignment check. The old positive KKT gap
cannot also be retained as a separate bank. Conditional I>=0 uses the
mean-cap definition, not a pure entering IC at every sampled endpoint.

The full-load version has average deleted load Lplus-rho, so C0 equals
Cov0-m||rho*t||^2. This proves the stated positive norm term with factor m.
Current-price slack is zero on p support; its Qplus split and static
2m-gamma implication have the stated signs. No amount follows merely from
the fixed point.

## 2. Canonical floor characterization

For exact ordered history h, let R(h) be all full pure-SPE endpoints and
M(h)=max_A min_(z in R(h,A))u_current(z). Read
`../tree/reset_floor_domain_independent_check.md` and checked the recursion
independently. A raw endpoint extending h is in R(h) iff each suffix role
k has u_k(z)>=M(z_<k).

Necessity compares its prescribed payoff to selected endpoints at every
alternative child, each no smaller than that child's minimum. For
sufficiency, the remaining path satisfies the same condition inductively;
offpath siblings can independently use their current-payoff-minimizing
child SPEs. The maximum of those minima is exactly M. No frozen original
best reply is assumed. Empty themes, equalities and all-zero games are
included.

In a row with entering role i already forced, only k>i receives a floor.
The entering current role need not be best responding in that forced
child. Imposing its M(h_i) as well would change the domain incorrectly.

For mean constraints Delta_h(z)=1_(z extends h)[M(h)-u_k(z)] and
E d_i<=u_i, the finite maximization dual is

    s(z)<=eta+mu d_i(z)+sum_h lambda_h Delta_h(z),
    H=eta+mu u_i,       mu,lambda_h>=0.

These signs are correct. Every ORIGINAL true source has Delta_h<=0, so
its KKT gap contains positive mu*I, priced canonical floor surplus, and
nonnegative reduced costs. This is not a bound on the remaining reset
demand or on the lambda multipliers.

Important domain correction: with actual-action tag A=B_i fixed, the dual
inequality covers every ALLOWED raw endpoint, not all mathematical reset
leaves. A reset inside that actual-action source which changes later
actions is forbidden under that tag. It needs a separately freed-tag
analytical domain or a genuinely different first-deviation row and wallet.
This exception was reported to root/tree and tree corrected its text.

Freeing actual-action tags in the canonical-floor analytical relaxation
would restore literal all-terminal pricing. Original sources still witness
feasibility. That larger domain is not called a pure-selector realization,
and no proof was made that its canonical constraints yield a numerical
shadow bound.

## 3. The outstanding obligation

The fixed point aligns which future price discounts occur, and the floor
dual prices reset leaves explicitly. Neither result yet transports the
positive reset deficits into the SAME original canonical-slack/reduced-cost
banks with valid masses and no reuse. No lambda cap or global payment was
proved here. The exact one-shot ledger is separately recorded in
`canonical_one_shot_reset_ledger.md`.

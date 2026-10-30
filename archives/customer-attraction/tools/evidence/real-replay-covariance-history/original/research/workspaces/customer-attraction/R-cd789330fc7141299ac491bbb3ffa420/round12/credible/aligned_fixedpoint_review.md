# Independent existence and scope check: aligned conditional mean-cap fixed point

2026-10-25, credible12. Review of tree12's
`../tree/aligned_credible_menu_fixedpoint.md`. The existence argument was
reconstructed from the supplied contract before reading the full note.
No fatal issue found in its stated scope. Original all-m HALF stays OPEN.

The product Q of conditional mean-cap endpoint lottery polytopes is fixed,
nonempty, compact and convex, independently of p. The domain Delta(S) x Q
is compact convex. Its load map L(p,q) is bilinear continuous and always a
legal fractional catalog background.

The query best response is the simplex on maximal theme t-prices at the
current load L(p,q). It has nonempty compact convex values and a closed
graph by continuity and finiteness of the catalog. For fixed p, the
q-objective F_p(L(p,q')) is continuous and convex in q'; its argmin is
nonempty compact convex. The feasible compact Q is fixed, so Berge gives
upper hemicontinuity. Their product correspondence therefore satisfies
Kakutani and has a fixed point.

At the fixed point, all query-supported themes have maximal t-price gamma.
For supported A, q_iA maximizes its conditional shadow a=rho t^2. At p_A=0
no such extremality is needed. The p response keeps the current load fixed;
it does not internalize p's effect on L. Hence this is not a minimax saddle
or a claim that its gamma is no larger than a shared minimax value.

The SAME q sources and background have average deleted load mL*. Thus the
decorrelated G term is identically zero, and

    W-m gamma=sum_i I_i+D-Cov.

I_i>=0 comes from the conditional cap, not from original whole IC at every
cap-violating mixture component. Endpoint variance is retained inside D.
Every genuine descendant IC must remain paired with its own witness.

This alignment makes the source-future price discounts exactly Qfuture
from the chosen background's prefix/future split. It does not preserve the
different minimax formulation's positive G bank as well. Source/background
alignment is a genuine coupling component, not a covariance payment.

The full-load variant has the same Kakutani properties. Deleted source
average becomes Lplus-rho, giving the positive m||rho t||^2 term while G
remains absent. Supported own-current action has zero price discount, so
the full static slack is Qpast+Qfuture on those same source leaves.

All existence, support, convexity and signs pass, including p on the
boundary and zero client coordinates. No bound proving the required
covariance inequality, or existence of a fixed point satisfying it, follows
from this argument. At m=5 its HALF pressure remains conditional. No finite
computation or equilibrium-lottery implementation claim was used.

## Additional raw/real replay check

Geometry12's `conservative_raw_tail_replay.md` and tree12's
`real_replay_covariance_flow.md` were read and independently checked.
Independent source/target sampling gives nonnegative unit-conservative
path masses and the exact selected target endpoint law. The final tag
rewrite has zero DELETED-load shadow work. Fixed signed floor or net-cost
potentials telescope; edgewise positive parts do not inherit the bound.

Geometry's posterior refresh preserves the complete current tag/raw-tail
law by the conditional tower, using target independence. Its reverse
martingale identities, one-query variance energy and cumulative-prefix
multiplier in DIAGONAL are correct. Refreshing a tag cannot silently
replace the fixed original diagonal coefficient.

In tree12's real replay, each preceding endpoint equals the original
sigma completion after the already forced target prefix. Thus every
future edge has its genuine original IC gap; coefficients are exactly
p_A Q_i(y), and each original source's initial mass is p_A once. The
terminal hybrid tail is independent of A before the final tag rewrite,
so the covariance-flow sign is correct. The tangent error
`E=sum_(x in A)(1-t_x c_x)^2/c_x` has
`-w_A dot Delta ell=Delta d-Delta E`, as stated.

For root's NEW uniform net-cost domain, selected root cap and floor
expectations need not be separately nonpositive. Use the combined net
cost telescope, not two independent banks. For a FULL-slot dual imported
into a DELETED-score replay, use `r_deleted=r_full+a(tag)`. Its original
source reserve is R_full+m||rho t||^2, exactly the existing self-norm
bank, not additional money. These scope distinctions do not produce the
remaining adaptive edge/tangent amount bound.

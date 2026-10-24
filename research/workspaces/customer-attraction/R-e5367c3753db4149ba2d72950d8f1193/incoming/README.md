# Incoming joint-payment check: exact finite scope, no new general bound

2026-10-24. Task: Q-CAG-HALF for arbitrary player count, arbitrary finite common
catalogue, and every complete ordered-history pure SPE. The general claim remains
OPEN. This subtask found neither a new all-input credit inequality nor a complete
SPE obstruction to the joint payment criterion.

## Saved useful material

* `check_natural_full_cover.py` independently verifies each supplied complete
  ordered strategy, computes ordinary natural actual-prefix reset prices, and
  optimizes over **all ordered optimal tuples and all owner choices** when an
  optimal tuple covers every customer. It does not generate games or policies.
* `natural_full_cover_diagnostic.json` freezes the three explicitly selected
  prior mechanism failures: individual-security, aggregate-theta, and global
  decorrelation. Their exact minimum full costs are respectively 2, 2, and 4,
  equal to their omitted mass. Thus none is an obstruction to this certificate.
  These are finite implementation checks, not support for a universal claim.

For one fixed ordered optimal tuple in this full-cover diagnostic, G=0 and no
cancellation is available or needed. A type can be owned at any slot whose
comparison topic contains it. The unit full cost starting there is determined
independently of all other owners, so minimizing that price separately for every
type exactly optimizes all integral owner partitions, including partitions that
give different copies of a type different owners. Exhausting all optimal orders
preserves repetitions and ties. Each supplied policy is checked at every ordered
history; equal-count histories are never forced to use the same reply.

## Analytic stopping point

The SOURCE-NET wallet is one and the same eta_i=u_i(I)+gamma_i, with total W.
Source costs already fit it. The whole natural-flow cost satisfies the existing
identity

    K_src + K_in = (OPT-W) + E_rho,
    E_rho = sum_s (A_s^rho/D_s)(u_role(s)-D_s) >= 0.

Therefore paying the complete flow from W requires E_rho<=2W-OPT. This is the
previously known IC-tax obligation, not a new inequality. A successor's
off-history prescribed-action IC gives OFF-IC only with all C migration,
untracked fresh R, new outside customers, and its negative off-history slack
retained. Its tracked positive reset coefficient is at most one half **per
recipient in the same true leaf**. Neither that bound nor the diagonal priority
witness controls all whole-query broadcasts across mutually exclusive leaves.
No way to turn them into an integral price-tail bound was proved here.

The weaker unrestricted-total cancellation criterion and its order-statistic /
tail-integral evaluation were already stated in review message 217 (as reported
by the parent). They are solver identities and a different sufficient interface;
they do not supply a new all-input credit or preserve a separately claimed
SOURCE-NET payment automatically. This subtask does not claim them as an advance.

No further zero-instance expansion, special-class theorem, new shared Claim,
commit, or external message was made. The parent can retain the checker as a
regression tool; it should not be described as resolving the incoming debt.

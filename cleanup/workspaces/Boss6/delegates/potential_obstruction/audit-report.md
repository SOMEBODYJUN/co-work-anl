# Independent audit report

This report is for frozen source IDs `9ead0718e1f922fb0462` and `b81e4d0d48f6fad07a88`.  I read both complete files and the frozen verifier `f3001ca6d7e2a9123d95`; byte-for-byte local copies and SHA-256 values are recorded in `batch-manifest.json`.  The output is a candidate object draft, not a formal archive promotion, and no source was marked `clean done`.

## Replay result

The verifier was run with the frozen JSON and the `customer_attraction` implementation from frozen `main` commit `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`.  Exact `Fraction` arithmetic and `verify_certificate` returned:

| field | value |
|---|---:|
| status | `passed` |
| checked history nodes | 43 |
| checked unilateral deviations | 215 |
| prescribed terminal history | `(1,3,4)` |
| forced-root terminal history | `(0,0,4)` |
| actual harmonic potential | `9/2` |
| forced-root harmonic potential | `5` |
| deleted actual potential | `7/2` |
| deleted forced-root potential | `4` |
| potential gap | `-1/2` |
| deletion gap | `-1/2` |
| actual welfare | `4` |
| exact 3-player optimum | `4` |

The action certificate contains one action at each of the 43 ordered histories.  The prescribed root action is theme (T_1); forcing (T_0) ties the root payoff at 1 while changing the continuation.  The source explains the customer signatures and computes the potential by customer load.  The exact runtime independently confirms the same values from the JSON, rather than trusting text fields.

## Boundary audit

The exact identity (u_i(z)=\Phi(z)-\Phi(z^{-i})) is a static terminal identity.  SPE compares these *differences* after a forced action and its complete continuation.  The witness has a negative terminal-potential difference despite a tied root payoff, because the two deleted-player potentials differ by the same signed amount.  Thus it rejects the local inference “SPE makes the continuation maximize (Phi)” and nothing stronger.

The instance is common-catalog, three-player, four-unit-customer, and has (W=\mathrm{OPT}_3=4).  It is therefore neither a low-welfare SPE nor a counterexample to (2W\ge\mathrm{OPT}_3), and it says nothing by itself about arbitrary (m,n), six providers, mixed security, or alternate potentials.

## Cross-object checks

* The full-tree averaging obstruction keeps every real history/action row separate and derives deletion-position remainder terms.  Its later correction limits the Farkas statement to fixed policy/distribution cones.  The present witness is a finite pointwise branch obstruction; it does not refute the uncompressed per-deviation certificate.
* The static iid benchmark and the six-theme conditional iid certificate remain valid in their stated domains.  The former is simultaneous play; the latter is one fixed strategy and (q) cone.  Neither gives universal sequential branch monotonicity.
* The future-response obstruction is a distinct four-theme, three-player, 21-history witness with positive unobserved response terms; it also has (W=\mathrm{OPT}_3).  The two finite obstructions reinforce the sign/boundary warning but are not merged into one certificate.
* The last-two-player welfare theorem uses single-step marginal identities and explicitly avoids treating SPE as a potential extremum.  Its (n=3) coefficient (8/15) is compatible with this optimal-welfare witness.
* The conditional terminal-reply dual lift exposes incumbent/deletion transfer terms and only proves a certificate-transport implication when its remainder is nonnegative.  The negative gap here is exactly the term that cannot be silently omitted.
* The governance correction `CA-CROSS-BRANCH-RELAY-v1/v2` repairs a false non-root welfare comparison by retaining an early-player profit term.  The present root comparison has no such non-root term and does not undo that correction.

These comparisons preserve the later repository boundary: a finite method obstruction is not a theorem-level impossibility result, and a fixed-policy positive certificate is not a general half-coverage proof.


# Weighted Bernoulli shifted inverse moment — actual author-Proof read-after review v1

Date: 2026-10-18. Reviewer: fee_cascade_review. Scratch-only review.

## Provenance and actual read scope

After root confirmed its actual full read of my frozen independent Exact-first record, I actually read the complete author-Proof file
`/workspace/scratch/038d9dcc4cac/weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md`.
Its actual SHA256 is
`891c56ecb28481957e93adb3e70e80ae946e152d440e901aebcdcb17421584c7`.
The entire proof was returned without truncation and read, including its provenance paragraph, zero case, scaled logarithm argument, XOS corollary, and final scope restrictions.

The previously frozen independent record is
`/workspace/scratch/038d9dcc4cac/weighted_bernoulli_shifted_inverse_moment_independent_exact_review_v1.md`,
SHA256 `1c2649e6e1c85412c41ab30979d3f8dca6d2c2b205ac8e6419b7da14eb77b284`.
It was completed before this author Proof was released to me. Neither that record nor the statement-only file was modified. This new document is explicitly a proof-aware read-after review. The author's own disclosed co-developer provenance is not relabeled as a blind review.

## Mathematical comparison and verdict

**PASS for the complete stated lemma and explicit nonnegative XOS corollary.** The author's argument agrees with the independently established mechanism and has no newly discovered gap in this scope:

1. Convexity of `a -> t^a` for `0<t<1` gives the correct chord inequality `t^a <= 1-a+at` on `[0,1]`. Finite independence justifies the product formula. Each product factor is nonnegative, and `1-x <= exp(-x)` gives the claimed upper bound on the generating function.
2. Integration over `t in (0,1)` gives exactly `(1-exp(-mu))/mu` for `mu>0`. Finite support permits interchange. When `mu=0`, nonnegative summands vanish almost surely, so the expectation is exactly 1, including the empty family.
3. Scaling by positive `nu` yields `E[1/(nu+W)] <= 1/M`. Jensen is applied in the correct direction to the positive random variable `V/(nu+W)`. It does not require positive logarithms or `V >= M`. The positive shift and finite support ensure all logs and expectations are finite.
4. A finite explicit XOS maximum attains its value on `S` at an actual original additive clause. Its weights on `S` sum to `v(S)` and are bounded by the singleton values and hence by `nu`. With independent actual inclusion probabilities at least `p`, their retained mean is at least `p*v(S)>0`.
5. Nonnegative coefficients imply `v(T)` is at least the selected clause's retained weight on `T intersect S`, even if `T` contains other elements. Monotonic decrease of `log(V/(nu+x))` then gives the stated expectation inequality. Only independence on `S` is needed; different probabilities are allowed.

The author's proof does not assert equality in the finite positive-mean inverse bound. Thus it is consistent with my earlier strictness and limiting-sharpness observations. These observations remain optional strengthenings in the independent record rather than missing obligations in the author Proof.

## Certification limits

This read-after review certifies only this standalone inverse-moment lemma and its stated XOS log-expectation consequence. It does not certify any downstream NSW algorithm, external numerical constant, simultaneous high-probability event, promise/RP reduction, source attribution, or new canonical asset. I have not read such a downstream replacement proof in this task. There was no software implementation or enumeration to run, and no repository, Work, or Git file was changed.

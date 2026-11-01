# General mechanism and enhanced five-player pricing

Research checkpoint 2026-10-21; no general half-coverage proof has been found.

The initial attempt used the exact last-node identity
`OPT <= W + (m-1)u_last - R`, where
`R=sum_{covered x outside the last theme}1/(c_x+1)`.
The sufficient condition `W+R >= (m-1)u_last` is too strong: independent
random exact outcome enumeration found a four-player all-covered outcome with
`W=30`, `u_last=12`, and `R=9/2`. The parent team independently already has
a complete five-player obstruction. This route was abandoned, without any
claim about the main conjecture.

The current task is full-type pricing of the sibling `next_credible`
five-player necessary-row system. Its first 64-column restricted LP has
2196 rows, 36 positive dual multipliers, and floating objective
1.9844871781654265. A restricted-support objective below two is **not** a
five-player theorem. New customer types must be priced over the entire
specified histogram/membership domain, then the resulting certificate
reconstructed exactly if no negative column remains.

For this particular dual the nonzero cross-family interactions are sparse:

* AE receives the Sbranch W count through one floor comparison.
* AB receives the Sbranch V/W counts and their dot product through one
  aligned two-player tax.
* AB and Sbranch receive the old third reply-menu count ell_2 through tax
  comparisons with fixed letter themes.

Thus conditioning on ell_2 and the Sbranch statistics `(v,w,dot(v,w))`
separates the AB and AE histogram maximizations; the Sbranch histogram can
then be directly enumerated. Other old menus are independent linear corner
optimizations. `price_aligned.py` implements this decomposition for the
current active dual, checks its formulas against the direct Fraction row
definitions on sampled atoms, and reports any violated column. Its floating
output is exploratory and cannot itself certify a universal inequality.

Full-domain pricing found a new W=0, O=1 atom. The sibling's 65-column
reoptimization, including 200 further background three-player profit rows,
then recovered a positive exact obstruction to all 2396 rows. The independent
review is `review_2396.md`; its `review_2396.py` expands common indexed menus
and independently reconstructs all 1959 new row coefficients on all 38 positive
atoms (74442 exact equalities). W=1, O approximately2.03010659458; all2396
slacks nonnegative, 44 zero. This proves insufficiency of that row template,
not a main-conjecture counterexample. The review identifies the missing true
root T_i deviation continuations as a natural next structural obligation.

`block_price.py` is a reusable heuristic pricing tool for arbitrary positive
duals over the2196 rows. It vectorizes original exact row definitions, checks
them against direct Fraction evaluations, then optimizes one entire finite
atom block at a time. Its20-restart output is `block_price.json`; coordinate
ascent is not a global certificate. `price_aligned.json` also retains one
negative column for each of the1024 fixed masks under the first sparse dual.
These tools are retained for diagnosis; the2396 obstruction means that merely
reweighting those rows cannot prove two.

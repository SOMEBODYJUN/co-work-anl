# Hard route after adding all full maximal-deviation floors

## Exact scope

Fix seven distinct maximal coverages, six providers, and restricted-growth
route `(0,0,0,0,1,0)` with actual final maximal action `B_0`.  The target
portfolio omits `B_6`, so the customer-column target is

`W - (U - |X_{\{6\}}|)/2`.

The usual route-conditioned rows are retained: six mixed floors `M_t` (the
private-incidence suffix is `1/12`, while the shared suffix is the seven-maxima
`B_t`), seven last-player best-response rows `L_j`, and 28 genuine
two-remaining tax rows `T_{jk}`.  I also added all 42 valid full
maximal-deviation floors

`D_{t,j}=u_t-Σ_{I∋j}1/(p_I(t)+6-t)`.

Here `p_I(t)` counts prior route positions whose routed maximal label lies in
incidence `I`.  The row is valid because forcing provider `t` to choose `B_j`
gives every customer with `j∈I` denominator at most `p_I(t)+6-t`, regardless
of the prescribed continuation.  Thus this is stronger than the earlier
mixed-floor-only family and still uses only genuine full-history SPE IC.

## Exact obstruction

`audit_full_max_floor_obstruction.py` stores an 18-column rational Farkas
distribution over legal route columns.  It verifies all 83 row averages are
nonnegative, while the target average is

`-42280/9125787 < 0`.

The support includes singleton columns whose included maximal blocks are not
covered early, for example `I={1}, J={4}` and `I={2}, J=∅`; this is precisely
the mixed-private gap left after dense/shared certificates and early-private
conditions.  The negative distribution is a separation of a proof template,
not a realizable customer instance or a SPE counterexample.

## Reproduction and boundary

From the repository root run:

```sh
python3 research/workspaces/customer-attraction/R-3e135db039f84d4da6f5625813469d5d/six_research_4/audit_full_max_floor_obstruction.py
```

Expected output reports 83 rows, minimum row average `0`, and target average
`-42280/9125787`.  This does not disprove Q-CAG-HALF-6.  It rules out this
stronger aggregate-floor extension on the route where the penultimate maximum
is absent from all four earlier route labels; a successful proof must use a
different cross-branch/early-to-tail payment or construct a complete original
model counterexample.

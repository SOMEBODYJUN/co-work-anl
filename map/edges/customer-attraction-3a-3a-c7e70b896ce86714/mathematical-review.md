# c7e70 fixed latest point and actual last price boundary

## Scope and hypotheses

The assigned object is the finite necessary system produced by the `--latest --local-v2` wrapper for the labelled common-catalogue model. The model has finitely many unit customers, a finite nonempty labelled catalogue (duplicate labels may have the same coverage), six sequential unit providers, complete pure strategies on every ordered history, and real continuation after every deviation. The stored point is a fixed 16-hist slice with actual B conditional states; it is not a full catalogue strategy or a full SPE certificate.

The wrapper selects the frozen `coupled_latest_exact.json` point with 2,033 columns and 5,277 rows. The columns are one capacity coordinate, 16 hist coordinates, 582 joint-reply coordinates, 1,306 overlap coordinates, and 128 actual-B branch states. The normalisation is `O=1`.

## Exact finite result

The saved rational point has 230 positive coordinates and

\[
W=\frac{269468671081390973287603081586427543021284243}
{551682258751855243720540411834195825411675776}
<\frac12.
\]

`verify_latest_point.py` rebuilt the original row builder once and checked all 2,033 descriptors, all matrix and vector lengths, the normalisation, all 5,277 rational slacks, the conditional branch masses, and the coordinate comparison with the 5,259 point. The replay exited with code 0 and empty stderr. Every saved row is nonnegative, the minimum slack is 0, and 2,120 rows have zero slack. Positive coordinates by kind are K=1, hist=11, joint-reply=98, overlap=103, and actual-B branch state=17.

The exact replay records the new row groups as 37 explicit rows, 10 cross rows, 16 marginal rows, and 16 reverse-marginal rows. Their minimum slack is 0. The ordinary seven Y-menu price checks are deliberately outside the saved matrix; five actual-player price slacks are positive and the sixth is negative.

## Actual last-price obstruction

After each actual four-prefix, force B and then force one of the six comparison themes `T_i`, yielding legal common-catalogue themes `Y_i` under the same complete strategy. For the true last provider, the six best-response inequalities add to

\[
6u_6-\sum_x\frac{\ell_Y(x)}{1+L_{actual}(x)}\ge 0,
\]

where `ell_Y` counts membership among the six `Y_i` menus and `L_actual` is the actual first-five load. The frozen 916-byte checker evaluates this row on the stored point and reproduces the exact negative slack

\[
-\frac{37649034345157581458948354799628857270185177}
{275841129375927621860270205917097912705837888}<0.
\]

Thus no complete pure SPE can retain these exact mass and `ell_Y` coordinates. The obstruction targets completions of this fixed point; it is not a global welfare counterexample, because the finite necessary rows do not certify a realizable catalogue, a complete strategy, or `OPT_6`.

## Comparison and migration boundary

The 5,259 point has the same 2,033 descriptors, the same exact `W`, and the same capacity coordinate, but 168 mass coordinates differ: 80 joint-reply, 70 overlap, and 18 actual-B states. Its price slacks cannot be substituted for the current point. The pending-cut ledger contains three portfolio and two requery cuts with negative rational slacks; they are related evidence for future tightening, not rows already included in this 5,277-row matrix.

The result therefore closes only a local statement: this fixed finite point satisfies the recorded necessary system and is excluded from completion by one separately checked legal last-price inequality. It leaves open the full SPE reconstruction, exact LP optimality, six-player `2W >= OPT_6`, and any migration to other points or support families.

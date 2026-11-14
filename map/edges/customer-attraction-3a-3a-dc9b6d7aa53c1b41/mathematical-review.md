# M-f626 fixed five-player common-Q scope review

## Exact result

The assigned core is a finite five-player, six-label candidate on one reconstructed full pure strategy. The seed has 458 unit customers, actual path `(4,3,3,2,2)`, root welfare `W=427`, and `OPT=458`; its 868 deduplicated Gamma rows and the complete policy reconstruction establish that this is a legitimate fixed-strategy cone input. The saved common-Q candidate has six query blocks and 120 stored multiplier rows. Reading the exact decimal Q as rationals gives total mass `999999999999999471/10^18`, 123 negative residuals, and minimum residual `-5349/(2*10^18)`. `limit_denominator(10^4)` (and the recorded 10^6/10^8 prechecks) also fails. This is a failure of the saved numerical candidate and denominator attempts, not a proof that the five-player cone has no rational common Q.

## What is certified in the same package

The four-player A/B/C fixed seeds admit a separate exact rational common-Q reconstruction: `Q=(3/4,1/4)` on two four-slot backgrounds, with the listed rational multipliers and nonnegative residuals for all 378 query/type equations. The reconstructed policy DAGs preserve every ordered history and give the same 306-row Gamma matrix. Thus, for those three fixed four-player strategy cones, the displayed certificate implies `W >= 4 v_4` for every nonnegative customer mass in the cone. The 20 `cone_n4_k6` endpoints are only the all-six-label unit type: `W=OPT=1` and `v_4=1/4`, an exact equality case, not 20 independent geometries.

The four-player certificate does not transfer to the five-player D seed. The D seed uses a different root/path and a different 868-row Gamma system; its stored Q is uncertified. The certificate also does not provide a universal common Q over all strategies, all customer masses, or the six-player target.

## Quantifiers and boundaries

The common-Q contract is a fixed full ordered strategy and zero past background. Q is shared across all pure queries and all customer weights in that one cone; multipliers may depend on the query. The report retains off-path histories and weak ties. The finite cone certificate is sufficient for aggregate welfare divided by player count, not a per-player guarantee. The numerical five-player status cannot be promoted to `refutes` or `equivalent_to`; a rational feasibility solve or an exact Farkas infeasibility certificate is still required.

The 4-player rational reconstruction is contextual evidence for the core's version boundary. No logical edge to the five-player claim is asserted because its model, strategy, and quantified target differ. The unresolved obligations are: exact five-player Q feasibility or exact infeasibility, a universal-in-strategy result, and any bridge to the six-player `2W >= OPT_6`/half target.

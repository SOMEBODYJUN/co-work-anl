# Counterexample-hunt round (2026-10-24)

Scope: attack the original Q-CAG-HALF target, preserving arbitrary finite common catalogs, arbitrary `m`, all ordered histories, history-dependent ties, and pure SPE. No main-target counterexample was found.

## Exact finite search attempted

The existing full-history target-index MILP (`R-d51.../true_counterexample/full_history_milp.py`) was rerun on the original unit-customer model (not an auxiliary bridge). For `m=p=5`, root count `(5,0,0,0,0)`, target portfolio all five labels, imposing normalized `OPT/W >= 2.00001` returned infeasible in 0.97s. Removing the threshold timed out at 30s with incumbent 1 and dual bound 1.8; neither status is a universal theorem. A `m=5,p=5` root `(4,1,0,0,0)` threshold run timed out without an incumbent. These are implementation/search observations only.

## Necessary terminal condition for any target counterexample

Fix an actual SPE path `S_1,...,S_m`, actual coverage `C`, and a chosen optimal tuple `T_1,...,T_m`. Write `D_j=T_j\\setminus C`. At the actual penultimate history `h=(S_1,...,S_{m-2})`, force player `m-1` to choose `T_j` and let `B_j` be any best reply of the final player in that branch. Since every customer in `D_j` has zero prior load, the deviator's payoff from those customers is

`|D_j| / (1 + 1_{x in B_j} per customer)`;

more precisely it is `sum_{x in D_j} 1/(1+1_{x\\in B_j})`, plus nonnegative terms. SPE therefore implies

`u_{m-1}(actual) >= sum_{x in D_j} 1/(1+1_{x\\in B_j^sigma})`,

where `B_j^sigma` is the particular final action prescribed by the fixed complete
strategy after the forced history `(h,T_j)`. This is a condition on the selected
continuation, not on every tied best reply. If all best replies after `T_j` are
disjoint from `D_j` (in particular, if the best reply is unique and disjoint),
then `u_{m-1} >= |D_j|`; otherwise a candidate can survive by selecting an
overlapping tied reply. The bank/risk constructions in `R-7c3...` fail exactly
because their selected/unique best reply is an unused bank or another disjoint
risk theme, leaving the deviator's omitted block undiluted.

This criterion is a direct SPE inequality and applies to arbitrary catalogs. It is
a useful filter for genuine counterexample search: shared omissions alone are
insufficient; each selected terminal reply after a large optimum theme must
provide real overlap (or all tied replies must do so), while preserving low
actual welfare.

## Boundary already independently checked

The existing private-seat spectrum gives: if the chosen optimum has only globally-private omissions, then `OPT <= (2-1/m)W`; hence a genuine half counterexample must contain shared omitted customers (at least two maximal themes). The `R-7c3...` matching/shared-omission path satisfies every coarse prefix/spectrum row but is not SPE by the penultimate criterion.

No claim here upgrades finite infeasibility, and no claim is made about general truth/falsity of Q-CAG-HALF.

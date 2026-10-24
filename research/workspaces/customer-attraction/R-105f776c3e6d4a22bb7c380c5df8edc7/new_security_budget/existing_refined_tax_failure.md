# Existing legal full-SPE failure of the refined fixed-load budget

2026-10-24. Reconciliation only, not a new counterexample. This matters because the shared `fractional_actual_load_counterexample.md` still describes `mM <= W+G` as another unproved sufficient bridge.

The existing self-contained source is [the refined-tax counterexample](../../R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md). Its exact 13-player, 36-unit-client instance has six common topics A,B,T,D,E,P and customer types

| Type | Multiplicity |
| --- | ---: |
| A | 2 |
| B | 2 |
| T | 1 |
| TD | 1 |
| TE | 1 |
| ADE | 3 |
| BDE | 1 |
| P | 25 |

It supplies a closed full-history policy automaton with 27,243 nodes and all six observed-action edges at every nonterminal node. Its actual outcome is `P^10 A A B`, with twelve payoffs 5/2 and the last payoff 3, hence W=33 and OPT_13=36. The source records independent unit-customer and compressed-policy full IC audits. I read the proof and exact arithmetic here; I did not rerun the original auditor or recertify its full action table in this subtask.

At alpha=12/13, its actual-load query vector is

    (65/37, 39/25, 3, 2381/925, 2381/925, 325/133).

Thus M=3 and G=708669/123025, giving the strict exact failure

    13 M - W - G = 29481/123025 > 0.

This refutes the precise fixed-actual-fractional-load budget even after retaining its exact covered-client tax. It does not refute a freely selected static integer minimax background or Mfull/Mpath. The legal fixed opponent tuple `A,B,T,P^9` has all six pure-query values at most 5/2, so v_13<=5/2 and

    W - 13 v_13 >= 1/2 > 0.

The same mechanism has an existing [arbitrary-padding analytic continuation](../../R-731efdb50dd844178e597d804bdd4596/credible_counterexample/all_k_padding.md).

Its source says the arbitrary-k argument was then awaiting independent blind review. The fixed 13-player audited source suffices for the status correction above; no arbitrary-k certification is asserted here.

This concrete failure concerns a stronger, prescribed-background auxiliary bridge. It cannot be used as evidence that genuine aggregate security, full-menu minimax, or Q-CAG-HALF is false.

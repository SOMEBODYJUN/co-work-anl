# Round 2: positive pair circuits over existing customers

Q-CAG-HALF remains OPEN. This round does not produce a general half proof or game counterexample.

`background_pair_circuit.md` supplies:

- An exact positive error formula extending the peer zero-background two-topic circuit to an arbitrary fixed prefix and all r>=s>=1.
- A three-active-provider error represented as a fixed cohort's lost rent, with an exact fixed-cohort telescope.
- Positivity of that three-active error for every common monotone submodular Shapley set function, including a truncated one, using an algebraic universal label. Parent and tree_coupling independently reconstructed this extension; no legal universal action is assumed.
- A shared-pivot identity showing that the remaining error is an original payoff comparison filtered by h/(h+r), and a genuine last-provider transport inequality whose additional charge lies only on already prefix-covered clients. One r=2 transport charges at most 1/6 per such unit client.

`verify_background_pair_circuit.py` checks 11,984 exact finite algebra cases. The general identities are proved by the membership-case derivation, not by that finite check.

The precise global bottleneck is controlling repeated charges while moving across different actual prefixes. A positive filter does not preserve aggregate SPE incentives, and changing the cohort invalidates the simple rent telescope. These local tools currently prove neither F(T)<=W+G_alpha nor mM<=W+G_alpha.

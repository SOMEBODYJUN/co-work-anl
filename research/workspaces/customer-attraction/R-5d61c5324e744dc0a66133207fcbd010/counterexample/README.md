# Scalable credible punishment and Cartesian amplification

2026-10-23. General Q-CAG-HALF remains OPEN. No primary counterexample found. No Git or credential operations by this subagent.

## New general mechanism and actual boundary

[coupled_cartesian_family.md](coupled_cartesian_family.md) gives an explicit complete pure SPE for every m=n+2>=4 in a nine-theme Cartesian common catalog. It uses two early choices to couple continuation selection across otherwise additive customer groups. The first-coordinate projected policy fails its root SPE inequality; the second coordinate's continuation reward compensates that failure. This exhibits exactly why arbitrary product-game SPEs cannot be treated as componentwise SPEs.

Parameters: integers b,s,d>0 with d<=b and nd<=2s. Disjoint first-coordinate resources have sizes (2b-d,b,bn); second-coordinate resources (s,s(n+1),s). Actual final counts are (2,0,n) and (1,n,1), so

    W=b(n+2)-d+s(n+3),    OPT=W+b.

The full-history proof supplies every proper subtree through explicit component policies, with ordinary BI only in a precisely identified unused first-coordinate domain. It checks both coupled levels separately.

The same architecture has the proved ceiling OPT/W<=(n+3)/(n+2)<=5/4. More strongly, standard safe disjoint catalog padding at t<=K/m cannot cross half for any parameters, and neither can same-m componentwise products of these policies followed by that padding. These are exact all-population architecture obstructions, not a general half theorem.

## Files and verification

* [verify_coupled_cartesian.py](verify_coupled_cartesian.py): independent Fraction audit of the complete policy DAG, every legal action edge, exact coverage, and padded optimum. It imports no canonical solver.
* [coupled_cartesian_padding_audit.json](coupled_cartesian_padding_audit.json): 12 cases, main n=2,...,9 plus exact parameter-boundary cases. All **80,803 DAG nodes** and **439,866 global comparisons** pass, minimum slack zero. The represented ordered-history trees are much larger; the report gives the exact count separately. General quantification rests on the symbolic proof, not this replay.
* [coupled_cartesian_audit.json](coupled_cartesian_audit.json): earlier replay before adding the padding check; retained unchanged.
* [cartesian_scout.py](cartesian_scout.py): exact all-SPE marginal-state recurrence for Cartesian products of disjoint resource menus. This is a discovery diagnostic. A state contains each coordinate's prefix counts; actions are all coordinate tuples, so terminal payoffs and all continuation games depend only on these marginals. Induction on remaining players gives the ordinary set-valued all-SPE recurrence without imposing common tie choices across histories.
* [finite_component_diagnostics.json](finite_component_diagnostics.json): exact finite all-SPE comparison for n=2,...,13 (m=4,...,15), b=3n,s=2n,d=3. All targets are feasible. The sum of component minimum welfare exceeds product minimum welfare by n in these cases. The displayed family itself has W=5n²+12n-3 and OPT=W+3n. This finite component-minimum observation is not claimed for all n and is unnecessary for the general construction.

Reproduce the complete finite-policy audit from repository root:

```sh
python3 research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/counterexample/verify_coupled_cartesian.py --max-n 9
```

## Relation to earlier barriers and next discriminating route

Read the old Cartesian product-policy lemma, the reciprocal-isolation 3/2 barrier, and the multiple-punisher old-private-client obstruction before constructing this family. The new policy is genuinely coupled above its component continuation subtrees, so it is outside the old componentwise-product no-amplification hypothesis. Its failure to approach half is proved directly rather than inferred from finite no-counterexample data.

To improve the route, one must reuse the second-coordinate compensation across many missing groups or avoid the bn customer mass making C competitive for n future players. Repeating independent copies, scaling sizes, or standard safe catalog padding is now ruled out for this constructed family. No such reusable compensation mechanism is supplied here. The unresolved four-copy disjoint-union mixed-root-menu scheduler is a different auxiliary-bridge task and was not treated as a primary counterexample.

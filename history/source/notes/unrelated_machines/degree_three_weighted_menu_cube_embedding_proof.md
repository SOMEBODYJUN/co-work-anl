# Proof: degree-three weighted menus embed in zero-weight cubes

Identity: `UM-DEGREE-THREE-WEIGHTED-MENU-CUBE-EMBEDDING-v1`.

Frozen Exact dependency: `degree_three_weighted_menu_cube_embedding_exact.md`, SHA-256 `b7cd715acf14005fdda54865a23d6d31a956b6f20a7cb19f211189cc154e76ef`.

This Proof is frozen separately at root's instruction after the Exact was sent for independent Exact-only reconstruction. Its disclosure to that reviewer is withheld until root releases it. No completed independent review is asserted in this file.

The result is an exact embedding of two explicitly defined complete scheduling formats. It does not import a hardness theorem, change a Santa Claus objective into a scheduling objective without a bridge, or assert an all-positive-cell result.

## 1. Construction is well defined

Use the source domain and construction in Exact A--C. For an original resource u, the group set incident to it is `{g:u in U_g}`, whose size is at most three. Therefore distinct indices `j_{x_u}(g)` in [3] can be assigned. In every indexed state of g, the chosen coordinate label is this index itself. If the index is i, the selected slice is

`{a in [3]^3:a_i=i}`.

This slice has exactly nine distinct resource cells. The vector a*=(1,2,3) satisfies a*_i=i for all i, hence it belongs to every such slice. Thus every original incidence I_gsu has a valid target active-cell incidence at exactly its mapped state and resource.

For a fixed group and indexed state, each original resource in its complete union U_g contributes one different tagged variable, so different original resources cannot identify target cell jobs. Within a variable, a selected slice has distinct cells. It follows that all original incidence-job identities map injectively into target incidence-job identities. An original zero-private-time job still maps to the active cell as its own original job. When u was absent from a particular original state, the newly present active-cell zero job is auxiliary rather than an identification with any other source job.

All other selected slice cells carry private time zero. Consequently the private mass in target indexed state (g,s) is exactly

`sum_{u in S_gs} p_gsu = W_gs<=1`.

If U_g is empty, the group's unique dummy variable y_g occurs in no other group. Its nine zero jobs in each indexed state contribute no private mass. This provides a nonempty variable set for that group while leaving all original state private masses zero. Dummy and original variables are tagged separately.

There is exactly one target indexed state and private machine for each original indexed state and private machine. Identical coordinate-label vectors are allowed to retain different indexed state cost tables and jobs. This construction uses that allowance expressly: the original state menu is preserved in the processing times and identities rather than encoded in the coordinate-label vector.

## 2. Eligibility and schedule extension

Map original resource R_u to target active-cell resource `(x_u,a*)`; retain each original private machine and selector with its index. The target incidence corresponding to I_gsu has private time exactly p_gsu and resource time exactly one. Its only finite choices are the mapped original private and resource machines. Its finite processing times and all other infinite eligibility entries therefore agree with the source after identity mapping.

Take any complete legal source schedule. Assign every mapped original job to the image of its original destination. All original private-machine and active-resource loads are unchanged. Assign every auxiliary target zero-private-time incidence, including those of selected indexed states, to its own indexed private machine. These assignments are legal and add zero load. Every nonactive auxiliary resource remains unused. All original jobs, all indexed states' jobs, and all target selectors have now been assigned. The target makespan is exactly the source makespan.

Unused original resources cause no difficulty: they still have all 27 target resource machines, their active resource represents an unused original machine, and no job of any group uses that variable. All 27 machines have load zero in an extended schedule.

## 3. Schedule projection and actual optimum equality

Take any complete legal target schedule. Delete all auxiliary incidence jobs, including active-cell zero jobs added for missing original state incidences, and delete auxiliary machines. Every remaining original selector is still at one of its original group's mapped state machines. Every remaining original incidence has exactly its original pair of finite eligibility options by Section 2. Apply the inverse maps to these original jobs and destinations.

This assigns every original job exactly once on an original eligible machine. Loads at corresponding machines cannot increase when auxiliary jobs are removed. Deleting unused auxiliary machines also cannot increase the maximum. Thus the projected source schedule has makespan at most the target makespan.

Schedule extension proves `OPT(C(P))<=OPT(P)`; projection proves the reverse inequality. Hence

`OPT(C(P))=OPT(P)`.

The equality concerns the complete ordinary UM instances with all original jobs retained. It includes the case OPT=2 and every strict or weak actual-makespan threshold. It needs no assumption about selected-state witnesses or positive weights. If a separate source theorem supplies an actual gap in this exact flat-menu domain, this embedding transfers it; the embedding itself supplies no such source theorem.

## 4. Interaction, resource degree, and strict-unit positive support

If two different source groups g,h have disjoint U_g,U_h, all their target variables are different tagged original variables or private dummy variables. Their target resource unions are disjoint.

If g,h share an original u, their target slices both contain the active cell `(x_u,a*)`, in every indexed state. Thus their complete target resource unions intersect. These two implications show that the group interaction graph is preserved exactly. In particular its maximum degree M is unchanged. Dummy variables create no new edge.

Every target resource lies inside one tagged cube. An original-variable cube has at most three incident groups, so each of its resource cells belongs to complete menu unions of at most three groups. A dummy-variable cube has only its own group. Resource group degree is at most three, regardless of menu size or M. No bound on M follows: one group may use arbitrarily many different variables that are shared with different other groups.

For strict-unit feasibility, take any schedule of makespan at most one. At a private state machine with its unit selector, no job of positive private time can remain. Hence every positive job in the selected indexed state must be exported. Two such selected positive jobs cannot use the same resource, since their external times are both exactly one. Their selected positive supports are therefore pairwise disjoint across groups.

Conversely, suppose one indexed state per group has pairwise disjoint positive support. Put each selector there, export all positive jobs of the selected states, and keep all zero jobs and every unselected state's jobs privately. Selected private machines have load one. Unselected private loads are their state masses, at most one. Each resource receives at most one exported unit job. This is a complete makespan-one schedule.

Under the embedding, positive target cells are exactly the mapped original positive incidences, and active-cell resource identities identify exactly the original shared-resource identities. Positive supports are thus preserved. The full geometric slices can have additional intersections at cells whose jobs have private time zero. Those jobs can remain beside a selector without adding load, so these geometric intersections impose no extra consistency requirement at makespan one. This explains why no unqualified all-positive-cell or automatic label-consistency conclusion follows.

## 5. Explicit polynomial size and binary encoding

There is one explicit 27-cell cube per original resource and one per empty-union group. If e groups have empty unions, the resource-machine count is exactly `27(|U|+e)`. Indexed state machines and selectors have their original counts S and |G|.

Let q'_g=max(1,|U_g|). Every target state of g lists q'_g distinct variables and one nine-cell slice for each. Its incidence count is exactly 9q'_g. The full target incidence count is therefore

`9 sum_g K_g q'_g`.

One original incidence has one target identity and cannot require several positive copies; all extra incidences are explicitly listed zeros. Since `q'_g<=max(1,|U|)` and menus, groups, and U are explicit, this count is polynomial in the source input. It need not be linear in the source incidence count: an old state omitting a resource from its group's union gains nine zero or active-cell incidences for that variable.

Every new processing time is zero, one, infinity, or an unchanged original rational. Tags, indices, coordinate labels, and each of the 27 cell addresses have polynomial descriptions. No numerical processing-time value is expanded into job multiplicity. In sparse eligibility format the listed output size is polynomial by the preceding counts. In dense format the number of entries is the product

`(|G|+9 sum_g K_g q'_g)(S+27(|U|+e))`,

which is again polynomial in explicit source input size. Construction, extension, and projection scan only these explicit objects.

## 6. Composition boundary

The exact embedding permits application of the bounded-interaction v2 positive theorem to this same domain. With resource group degree bounded by Delta=3, its factor is `2-1/(M+5)`. This remains below two for fixed M; arbitrary source interaction survives this embedding and can grow.

The remaining source task is still to prove normalized strict-unit YES and near-two actual NO in the degree-three menu domain, including all state choices and partial exports. General positive-allocation, aggregate welfare, unconstrained additive Santa Claus, or ungrouped set-packing hardness does not automatically supply that contract. Nor can zero weights be replaced by a positive perturbation while assuming exact OPT=1 survives: geometric slices shared by two selected groups can overlap outside the preserved positive support and acquire new forced unit exports after such a perturbation.

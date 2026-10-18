# Independent Exact-only reconstruction: resource-degree-three path reduction

Reviewer: `/root/rainbow_gap_source`, 2026-10-18.

Reviewed identity: `UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1`.

Actually read in full: `/workspace/scratch/038d9dcc4cac/flat_menu_resource_degree_three_path_reduction_exact_v1.md`.

Measured SHA-256 of that Exact: `7bbfc817db6081f574f7d2dd6c171c2b587152809c87adb071f99e5334635835`.

**Read boundary and chronology.** The author first sent a short construction-level description and the Exact path. I then actually read the entire Exact file, independently reconstructed the two schedule directions and the positive partial-allocation directions, and reported those arguments to root and the author. I have not read the author's Proof or a root-authored proof/argument. Root subsequently reported that it had also independently closed the construction and requested this frozen record; that report is not used as mathematical evidence. No earlier review hash is invented here. No repo, Work, or Git action was performed.

**Verdict: PASS for the stated full domain and conclusions.** No standing fatal issue was found. The proof is a direct explicit matching construction, not a new hardness source; historical overlap with BCG or other degree-reduction techniques and global novelty are not certified.

## 1. Reconstructed input and target

The source is the stated complete flat-menu ordinary UM instance. Each indexed state has distinct resource identities, nonnegative private times of state sum at most one, and one resource-time-one incidence job per listed resource. Every group has one unit selector and a nonempty indexed menu. All indexed states' jobs remain in the instance. Membership in a resource's complete group union includes original zero-private-time incidences.

For a source resource u, list its d incident old groups as g_1,...,g_d. Replace u by ports z_1,...,z_d, and map every original incidence of g_j on u, in every state of that group, to resource z_j at the same external time one. Keep each original job identity, private endpoint, private time, indexed state, and selector menu. Add d-1 helper groups H_j, with singleton states (z_j, private time one) and (z_{j+1}, private time one). Each helper is implemented with its two actual private state machines, one selector, and both incidence jobs.

Each port lies in the old group g_j and at most its two adjacent helper groups. Thus complete-menu resource group degree is at most three. The same old group's states never obtain several different ports for one old resource. Source menus stay the same size, helpers have exactly two states, and the maximum target menu size is at most max(K,2). Every helper state has private mass one. Original private masses are unchanged, so W<=1 remains true and W=1, if required, remains true as well.

## 2. Source schedule with C<2 extends without extra load

Take any actual complete source schedule of makespan C<2. Since all external jobs on u have external processing time one, at most one original incidence job can be externally assigned to u. This counts jobs of selected states, unselected states, and private-time-zero original jobs alike.

If such a job exists, let k be its old group's port index; otherwise choose any k in {1,...,d}. Leave z_k unoccupied by helpers. Match helper H_j to z_j for j<k, and to z_{j+1} for j>=k. These d-1 ports are distinct and are exactly all ports other than z_k.

For each helper, select the state of its matched port, export that state's incidence job, and park its other state's incidence job privately. The selected helper root has selector load one; its other root has incidence load one; its matched resource has unit load. All helper jobs are explicitly assigned. Original private choices and loads are unchanged. The only possible original external job on this path uses the free port z_k. Thus every new resource load is at most one and every new private root load is at most one.

The source has a selector, so C>=1. Therefore the complete target makespan is at most C. The formula applies independently to every used original resource and never calls an unknown matching oracle or searches over old state selections.

## 3. Arbitrary target C<2 projects, including extra helper exports

Take an arbitrary complete target schedule of makespan C<2. Each helper's actual selected private machine has its unit selector. Its selected state's private-time-one incidence cannot remain there, since that would give load two. It must be exported to one of the helper's two eligible ports.

All unit external jobs have distinct resource destinations under C<2. The d-1 selected helper incidences therefore occupy at least d-1 different ports in the path. An unselected helper state's incidence might also be exported in this arbitrary input schedule. Such extra exports only occupy additional distinct ports and cannot invalidate the lower bound of d-1 ports already consumed by helpers.

At most one of the d ports can consequently receive an **original** job. This statement also counts unselected old-state jobs and original zero-private-time jobs, because their external processing times are still one. Map each original external job on a port back to u and leave every original privately assigned job on its original private machine. At most one original unit job is now assigned to each u, so each source resource load is at most one<=C. Original private loads are unchanged after helper groups are deleted. Every original job is retained exactly once on an original eligible endpoint. This yields a complete source schedule of load at most C.

The argument does not assume a preferred helper orientation, one exported job in total per helper, or full export of selected old states. It applies to every target schedule below two and all its partial exports.

## 4. d=0, d=1, C>=2, and exact OPT

When d=0, the source resource has no incidence in any old state. It can be retained unused, which I take as the definite implementation convention, or omitted as allowed by the Exact. It cannot affect any job destination or makespan. There are no helpers or ports to scan for it.

When d=1, there is one port and no helper. The one old group's incidences are simply renamed to that port. The at-most-one-external-unit condition below two handles projection directly, including multiple indexed states of that same group.

Both complete instances always admit the all-private schedule of makespan at most two, and the original nonempty group set implies both optima are at least one. For an input schedule of makespan C>=2 in either direction, a safe fallback is the complete all-private schedule of the other instance, with load at most two<=C. This fallback need not preserve the input's private-versus-external choices, and the Exact only promises that stronger private-choice preservation in its C<2 source-extension statement.

If the source optimum is below two, Section 2 gives target OPT no larger. If it equals two, the target all-private bound gives the same inequality. Conversely, if the target optimum is below two, Section 3 gives source OPT no larger; if it equals two, the source all-private bound gives that inequality. Hence the optima are exactly equal, including the endpoint two. In particular, a hypothetical target optimum below two when the source optimum equals two would immediately contradict Section 3.

## 5. Independent positive partial-allocation argument

Now assume every original state is normalized to mass one. The helper states are normalized as well. Use exactly the allocation objective in Exact D: one state per group and an arbitrary subset of that state's resources, with all groups' subsets pairwise disjoint; maximize the minimum exported private mass.

Given a source allocation of common value at least v>0, each original resource belongs to at most one allocated old-group subset. For every resource path choose that old group's port as the hole, or an arbitrary hole if none was allocated. Use the explicit helper matching from Section 2. Keep all old allocated private masses and give each helper its matched singleton resource, hence value one>=v. This is a target partial allocation with the same threshold. It does not require full selected-state export.

Conversely, in a target allocation of common value at least v>0, every helper's selected singleton state must receive its sole entire resource: its exported private value is either zero or one. Thus the d-1 helpers consume d-1 distinct ports, leaving room for at most one old allocated group subset per original u. Mapping those old allocated ports back to u produces disjoint old bundles and preserves each old group's selected-state private value. Helpers are deleted. This proves the reverse threshold conversion for every positive v<=1.

At v=0, both domains have feasible empty allocated subsets. If either optimum were positive while the other were zero, a positive threshold below or equal to that attained optimum would contradict the two directions above. Therefore V is preserved at zero as well. This supplies an independent combinatorial proof of the V identity, without needing to infer it only from the already established normalized UM optimum formula.

## 6. Explicit size and binary complexity

Let I be the original incidence count, a the indexed-state/private-machine count, m the original resource count, and n the original group count. Every distinct group membership of a resource is witnessed by at least one original incidence, even when its private weight is zero. Thus `sum_u d_u<=I` and the total helper count h=`sum_u(d_u-1)_+<=I`.

The target has at most I used ports plus at most m retained unused resources, a+2h private state machines, and n+I+3h jobs. Each helper contributes exactly two private machines, one selector and two incidence jobs, and six finite eligibility entries. Old selectors and jobs are not replicated. Complete target resource count and all dense matrix dimensions are therefore polynomial in the explicitly given source input size. For example the dense target has at most

`(a+m+3I)(n+4I)`

entries under these loose bounds. Each finite time is an unchanged source rational or one; unlisted times remain infinity. Tags, job identity maps, path indices, and actual assignments have polynomial bit length.

Build membership lists by scanning and deduplicating explicit state-resource incidences. The two schedule/allocation maps traverse actual finite paths of length d_u and original jobs; their loop bounds are at most the explicit incidence count. No loop expands a processing-time denominator, a binary threshold inverse, or a numerical weight. Exact load checks use polynomial-length binary rational sums.

## 7. Scope of the pass

The pass covers original W<=1 and its normalized subdomain, original zero jobs, all indexed states, d0/d1, arbitrary target helper behavior below two, exact OPT2, partial normalized V including V0, bounded old K with target max(K,2), and explicit dense bit complexity.

It does not turn a normalized-menu one-versus-tiny-value source into an already proved hardness theorem; that source is still missing. It also does not change each helper's actual heavy-only two-singleton menu into an endogenous mixed heavy/diffuse state. The construction is a concrete physical degree reduction whose overlap with prior literature remains a separate attribution question.

# Grouped hypercube-slice scheduling v2: rainbow independent and read-after audit

Reviewer identity: `rainbow_gap_source` / rainbow. Review date: 2026-10-18.

Scope: `UM-GROUPED-HYPERCUBE-SLICE-SCHEDULING-v2`, its frozen Exact/Proof pair, and only the new grouped-menu section of the canonical composition. No repository files were edited by this reviewer. This report is a scratch audit artifact.

Verdict: **PASS**, including the full-class actual makespan upper bound `3/2`, its exact normalized sharp example, and the stronger `19/15` DGR specialization. One genuine scope ambiguity in the first canonical composition was reported and then corrected by root; both the objection and the correction are retained below. No near-2 hardness source or NP-hard approximation threshold is established.

## 1. Independent-first history, without retroactive hash claims

Before opening either author file, the reviewer received only root's mathematical input description and candidates. The reviewer independently established and sent root the following results:

1. For a fixed arbitrary state choice and a variable appearing `t <= d` times in a group subfamily, label bucket counts `t_i` give the exact local union `d^Q - product_i(d-t_i)`. Distinct incidence indices are what make each coordinate's forbidden values distinct.
2. Bernoulli and the decreasing geometric-prefix average imply the all-subfamilies lower bound with `c_d = 1-(1-1/d)^d`, and hence integer demands `floor(c_d L_g)` satisfy capacitated Hall.
3. For `d=5,Q=2`, local union is at least `5t-floor(t^2/4) >= 19t/5`; three-variable groups therefore simultaneously receive 11 resources. Five groups sharing the same three variables, with labels split 2 versus 3, have total union 57 and rule out 12 resources per group for that fixed state choice.
4. The actual UM schedule exports only matched jobs of selected states; every unselected state's jobs remain at its private root. Chosen-root load is `2-|B_g|/L_g`, unchosen-root load is 1, and each resource has at most one unit job.
5. The reviewer independently supplied the short estimate `c_d >= (d+1)/(2d)`, from `(1+1/(d-1))^(d-1) >= 2`. Because `Q>=2` makes each positive `L_g` a multiple of `d`, `c_d L_g >= ceil(L_g/2)` follows. This yields the full-class `3/2` bound. Root also independently proposed this strengthening; this record establishes the reviewer's independence before reading author files, not a priority claim.
6. The reviewer independently checked the two-group `d=2,Q=2` sharp example and its actual optimum `3/2`.

These earlier messages were prompt-based mathematical reconstruction. **The reviewer had not hashed or opened the author files at that stage. No earlier-file hash or timestamp is manufactured here.** The hashes below were measured during the subsequent read-after phase.

## 2. Actual read order and observed hashes

The actual file-reading order was Exact, then Proof, then the canonical composition. Exact and Proof were read fully.

| Read object | Observed SHA-256 | Result |
|---|---|---|
| `/workspace/scratch/038d9dcc4cac/um_grouped_hypercube_slice_scheduling_v2_exact.md` | `edc9658d7f33ece188b4542178f7b82cf7d657099da1c6fd90dcf5979cf6ee55` | Matches root's frozen Exact hash |
| `/workspace/scratch/038d9dcc4cac/um_grouped_hypercube_slice_scheduling_v2_proof.md` | `f773a57f681556f331f7d9804cf0c30d2fedbd00ac9ac595804cfda2330e7db0` | Matches root's frozen Proof hash |
| Initial canonical whole file | `569cdf292d99ad4caab97926e0d3cd0b62f5d14b1d0252762a26e4c6eaae8c47` | Mathematical proof passed; one completeness-sentence scope ambiguity reported |
| Corrected canonical whole file | `5e20015fe743dd4ac4aa5fa08560a7f9b4c8adc0e0fbf77a0221b3c513ea1875` | Corrected new section read in full; PASS |
| Corrected canonical new section, bytes starting at its `## 超立方分组菜单的 Hall 保留与锐3/2实际界` heading through EOF | `80edd5d2dd4c379574233c67125188e28ed02865dbd5187e69cbf22e23439712` | Final composition scope frozen by this review |

Canonical path:
`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/coordinate_slice_source_compilation_counterexample.md`.

The whole canonical file was read to locate and distinguish the new object. The earlier v4 source-compilation claims are not newly certified by this audit, and no claim is made to have compared their bytes against an unavailable earlier baseline. This reviewer made no repository mutation.

## 3. Read-after attacks on Exact and Proof

### Quantifiers and local union

The proof fixes an arbitrary state choice and an arbitrary group subfamily. It never requires satisfiability, a YES promise, an optimized menu choice, or consistent labels across groups. The exact product complement holds because each state uses each variable at most once and `j_x` is injective across all groups containing that variable. Labels may repeat; the associated incidence values remain distinct within a label bucket. The variable tag makes different gadgets' union sizes additive.

For integer bucket counts, `1-t_i/d <= (1-1/d)^{t_i}` is valid. All factors are nonnegative. The geometric-prefix argument is correctly restricted to `1 <= t <= d`; the zero case and `d=1` are handled separately. Hence the union lower bound applies simultaneously to every subfamily, not merely to the entire group family.

### Hall, integer rounding, and nonuniform sizes

For every subfamily `F`, its neighbor count is at least `c_d sum_{g in F} L_g`, which dominates `sum floor(c_d L_g)`. This is the required capacitated Hall condition. Unit-demand cloning also proves ordinary Hall for partial selections of clones: their represented groups have at least the full group demands as neighbors, hence at least the chosen clone count. Integer max flow therefore gives exactly the claimed integral allocations.

No global equal-size assumption is used. Group sizes may vary; only each group's states share its fixed variable set and hence its size. The theorem does not replace a floor by a ceiling without proof.

For the half-allocation strengthening, with `d>=2,Q>=2`, `L_g/d` is a positive integer. Thus

`c_d L_g >= L_g/2 + L_g/(2d) >= L_g/2 + 1/2 >= ceil(L_g/2)`.

This covers both parities, including the smallest allowed sizes. The cases `d=1` and `Q=1` really do have disjoint selected sets and optimum 1. Empty groups are excluded, so the processing time `1/L_g` is defined.

### Actual UM bridge and complete task accounting

Selectors are distinct group jobs, allowed only at their group's indexed state machines. Each state-resource incidence is a distinct job with exactly the two stated finite processing times. Resource tags and state tags prevent unintended identification.

For any selected states and any pairwise disjoint `B_g`, the schedule places their selectors on their selected roots, exports precisely the selected incidence jobs indexed by `B_g`, and leaves every other job on its own state machine. Thus every unselected state is accounted for, even if its resource set overlaps many selected states. The private total incidence load is exactly 1 per state. This proves the actual makespan calculation and not an altered allocation objective.

The full-disjointness completeness schedule exports all jobs of the selected states and leaves all jobs of the unselected states at their own roots. At least one unit selector proves `OPT>=1`.

### Sharpness and interpretation

In the two-group, one-variable example, each root is forced to carry its selector. If `C<3/2`, no root can also carry a private incidence job of size `1/2`. All four incidence jobs must then use resources. Their eligible union has only three resource machines, and `C<2` lets each machine carry at most one unit job. This is impossible. Exporting one distinct resource job per group and keeping the other job at each root attains `3/2`.

The unused fourth cube resource remains present but offers no eligibility edge. The lower bound is an exact actual optimum on one finite instance. It is not an NP-hardness result, not a configuration-LP gap, and not a YES/NO source gap. The claimed sharpness is solely the normalized absolute upper bound on the stated construction class.

For `d=5,Q=2`, the table of five possible local incidence counts is an exact finite symbolic verification of the formula, not an enumeration offered as a general proof. The five-group 57-resource obstruction proves that the fixed-choice universal integer guarantee cannot be 12; it does not assert a lower bound after optimizing a richer menu.

### Explicit bit complexity

The resource-side maximum-flow network has polynomially many vertices and edges in the explicitly materialized resource and incidence lists. Integer capacities are at most total selected incidence count, so their bit lengths are polynomial in that explicit input. The constructed UM instance lists every state and every incidence job; rational times `1/L_g` have logarithmic-size denominators.

For `d>1`, the exact rational `c_d` requires `O(d log(d+1))` bits. Nonempty explicit cubes have at least `d` resources, making this polynomial in explicit input size. The `d=1` case is handled directly. When only binary `d,Q` and succinct labels are provided, the cube may be exponentially larger. Neither Exact, Proof, nor the corrected new canonical section claims a polynomial algorithm in that succinct encoding. No hidden fixed-parameter assumption is needed for the explicit-instance result.

No LP/flow implementation, random sampling, or finite computational experiment was used as mathematical proof in this review. Constructibility by standard integral max flow is distinct from claiming production software has been written.

## 4. Original DGR result versus the new bridge

The reviewer independently opened the primary full text at <https://arxiv.org/html/2511.00184v1> and checked Definition 3, Theorems 2–4, Section 3, and Section 5. Its displayed specialization uses degree-five 3SAT, binary labels, seven sets per clause, size 15, `alpha=1/7`, `beta=(1-epsilon_0)/7`, and `epsilon<1/30`. Section 3 supplies the separate Santa Claus reduction with normal and dummy items. Those facts agree with the frozen note.

The original selection problem is ungrouped. Clause groups and the selector/incidence UM construction are additional definitions in this project. Their unconditional Hall and scheduling bounds are proved directly here; they are not attributed to DGR. Retaining a `(1-epsilon)` fraction of a 15-element set with `epsilon<1/30` forces retaining all 15 elements. No arbitrary-small-retention hardness or near-2 ordinary-UM theorem is imported.

The recorded `beta` boundary is not silently converted into a strict NO inequality. The Exact note explicitly proposes an intermediate constant target if a strict decision gap is required. The full source, rather than its brief-announcement abstract, supports the mathematical audit. This review did not independently authenticate a downloaded PDF's bytes or its manifest; the final canonical sentence assigning that separate check to root remains correctly attributed to root.

## 5. Genuine canonical objection, repair, and final composition verdict

The first canonical reading contained the sentence:

> 若完整所选集不交，全部 incidence jobs 外放即可达1

Read literally over all indexed states, this is not justified: unselected states may overlap, so exporting every job of every state need not have makespan 1. The reviewer reported this exact ambiguity to root, while observing that frozen Exact and Proof already used the correct selected/unselected distinction.

Root corrected the sentence to specify that all incidence jobs of selected states are exported and all incidence jobs of unselected states remain at their own roots. The reviewer then actually re-read the entire corrected new section and measured its new whole-file and section hashes listed above. The ambiguity is resolved; the correction is not silently erased from this audit history.

The final new section preserves the input hypotheses, all-state-choice quantifiers, floors, divisibility argument, full original-job scheduling, normalized sharpness meaning, original-DGR/new-bridge distinction, and explicit bit-complexity scope. It explicitly leaves the general UM target open and presents outside-hypothesis mechanisms only as possible escapes from this lemma, not as hard sources.

**Final result: PASS for the frozen v2 Exact/Proof pair and the corrected canonical grouped-menu section at the hashes recorded above. No repository edit was made by this reviewer.**

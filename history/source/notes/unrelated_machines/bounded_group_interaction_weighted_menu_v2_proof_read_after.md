# Actual Proof read-after: bounded-interaction weighted menus v2

Candidate: `UM-BOUNDED-GROUP-INTERACTION-WEIGHTED-MENU-v2`.

Frozen read-after review, 2026-10-18. This is the first review by this reviewer after actually reading the author's entire Proof_v2. The earlier Exact-only independent derivation is preserved unchanged; this note does not retroactively describe the author's proof as independently derived.

## Files actually checked

| File | SHA256 |
|---|---|
| `bounded_group_interaction_weighted_menu_v2_exact.md` | `6267e81738a786ad1145e067637a7792b411328ee35842e8db889ebb22e62c16` |
| `bounded_group_interaction_weighted_menu_v2_proof.md` | `30801c243a88a39ce5b97909e251ff84ca469ebef5b903f436d0353c01266c84` |
| Earlier immutable `bounded_group_interaction_weighted_menu_v2_independent_review.md` | `8b6fb6504c9689d67236263a74321bf85143bbdb1acc0b57759df4a24c5aa947` |

All three paths are in `/workspace/scratch/038d9dcc4cac/`. The author's Proof hash was checked before its full text was read. The other two hashes were rechecked when this note was frozen.

## Verdict

**PASS.** The author's complete Proof_v2 agrees with the earlier independent reconstruction. Its six sections jointly prove the declared all-input relative guarantee for the precise original-job model. No fatal gap, missing source witness, hidden optimum input, or unproved allocation backend was found. No revision to the frozen Exact or Proof is requested by this reviewer.

The within-state distinct-resource assumption remains load-bearing. The noninjective counterexample recorded in the older review is retained as an out-of-domain boundary example. Neither this note nor the author's proof authorizes a noninjective extension.

## Section-by-section actual comparison

| Author section | Read-after finding |
|---|---|
| 1. Domain and normalization | Correct. It adds bonuses for every deficient indexed state and exports every bonus when extending an arbitrary original schedule. This establishes exact optimum equality; adding only bonuses for selected states would not have defined the same fixed normalized input. Unique bonus resources preserve both degree bounds. |
| 2. Heavy failure certificate | Correct. A putative makespan below `1+beta` forces a heavy export from the actual selector-chosen state of every H group. Since that threshold is at most 2 and the makespan inequality is strict, the resource jobs yield a covering matching. The contrapositive supplies the required lower bound on OPT. |
| 3. Actual heavy-resource reservation | Correct. Every matched H group reserves one resource. Every group that removes a resource from a diffuse selected state is a neighbor in the complete-menu interaction graph. Thus at most M incidences are removed, of total weight at most `M beta`; zero-weight incidences are harmless. |
| 4. One full-slot matching and lower utility | Correct. Every full slot has Delta distinct resources, each resource has degree at most Delta across slots, and Hall covers all slots. The shifted accounting ranges prove the stated `Delta-1` loss, while the actual matching blocks remain the ordinary consecutive full blocks. These two kinds of ranges are not conflated. |
| 5. Actual schedule and ratio | Correct. It accounts for selectors and all incidence jobs of all states. Success gives absolute load `2-beta`; failure gives load at most 2 together with `OPT>=1+beta`. The relative guarantees are combined without claiming an unconditional absolute bound in the failure branch. Bonus projection returns every original job exactly once. |
| 6. Binary complexity and cube bounds | Correct for explicit input. The graphs are bounded by actual incidence-list sizes, not numeric Delta. The complete-menu cube degree bounds agree with the independent counting argument, provided q bounds the union of variables of a group as in the fixed-variable coordinate-slice model. |

## Boundary checks requested for this read-after

### Empty tail, nonempty tail, and an empty sampled sum

The author writes `n=m Delta+r`, `0<=r<Delta`, and accounts for the first Delta-1 entries separately. Its remaining ranges are

\[
[t\Delta,\min\{n,(t+1)\Delta-1\}],\qquad 1\le t\le m.
\]

They cover exactly positions Delta through n and have at most Delta terms each. When the actual tail is empty (`r=0`), the last accounting range contains just index `m Delta`; it is still bounded correctly. When the actual tail is nonempty, the last range has `r+1<=Delta` terms. The argument does not require a positive tail or a full last accounting range.

When `m=0`, at most Delta-1 weights remain and their total is at most `(Delta-1)beta`, exactly as stated in the Proof. A normalized diffuse group in the success branch cannot actually have this case: the independent mass lower bound gives

\[
W'\ge1-M\beta=(2\Delta-1)\beta>(\Delta-1)\beta.
\]

Thus the empty-sum inequality is valid algebraically, and the success assumptions rule it out for a group that must obtain positive mass. The author's proof explicitly makes this distinction.

### Endpoint beta=1

The endpoint forces `Delta=1,M=0`. Every normalized state is diffuse because each nonnegative private time is at most the total private mass 1. H is empty; a covering matching of H is the empty matching. Diffuse blocks have size one. Resource group degree one makes the chosen states' resources disjoint across groups, and every selected incidence can be exported. Returned makespan and optimum are exactly 1. The failure ratio inequality is also valid at beta=1, although that failure branch cannot occur here.

### Large binary Delta and M

The proof creates only `floor(n/Delta)` slots for a list with actual length n, and at most one slot-graph edge per retained selected incidence. If a binary upper bound Delta is enormous relative to n, no loop up to Delta and no Delta-copy graph is needed: integer comparison/division decides that there are no full blocks. Such a list cannot be a normalized success-branch diffuse group by the preceding mass argument. A large loose upper bound therefore weakens the approximation constant but does not cause pseudopolynomial graph construction.

M occurs only in the exact rational threshold, degree verification, and inequalities. Its numerical value is not realized by creating M objects. The denominator `M+2 Delta-1` has polynomial bit length in the binary parameter encoding.

### Positive and zero private times; empty original states

Sorting uses nonincreasing nonnegative values and admits zero ties. Both the first-entries bound and the shifted accounting ranges remain valid for zero entries. A zero-time job remains a genuine original job and, when not exported by the matching, is legally parked on its own private machine; its external time is still 1 if it is exported. The schedule does not delete zero-time original jobs or treat them as resource-free external jobs.

An empty original state has mass zero and receives a private-to-that-indexed-state bonus of private time 1. This normalization is well-defined and exact. After projection, the original state and its selector remain, while only the auxiliary bonus job/resource are removed. Nonempty menus guarantee an eligible private machine for every selector, even when all original states are empty.

## Dense matrix and complete output clarification

The author describes an explicit structural input and a job-to-machine output, rather than requiring a dense processing-time matrix as the output artifact. This is not a complexity gap. The dense convention is polynomially compatible with the proof:

Let `a` be the number of indexed states, `u` the number of resource machines, `g=|G|`, and `L` the total original state-resource incidence count. The original instance has

\[
n_M=a+u,\qquad n_J=g+L.
\]

If b states receive bonuses, `0<=b<=a`; the normalized instance has `n_M+b` machines and `n_J+b` jobs. A dense normalized processing-time matrix therefore has

\[
(n_M+b)(n_J+b)
\]

entries, polynomial in the explicit original counts. Fill unlisted entries with a distinguished infinity marker, selector-eligible entries with 1, and incidence-eligible entries with their declared private rational or external 1. Every rational entry and each bonus deficit has polynomial bit length. A dense matrix supplied as input can likewise be read and checked in polynomial time; its length is larger than, not succinctly smaller than, the structural counts.

The required output schedule is simpler: one eligible machine identifier for each of the `n_J` original jobs, with size `O(n_J log(n_M+1))` bits apart from fixed separators/identifiers. The algorithm constructs that complete assignment by exporting the designated original incidences and parking every other original incidence, then placing every selector. It need not output or materialize a normalized dense matrix to produce this assignment. If a dense representation is requested for auditing, the preceding count shows it can be materialized without changing the polynomial claim.

The word “ordinary” is respected: no other eligibility, resource constraint, rejection, or objective is introduced by the returned assignment. In particular, zero private times are actual finite processing-time entries, infinity entries remain forbidden, and distinct resource/private machine tags prevent unintended identifications.

## Verification status

The previous Exact-only review's 18,018 exact-rational sorted-list checks included zero weights, Delta=1, empty lists, empty tails, and nonempty tails. Those checks are supplementary; the read-after verdict relies on the full proof and the independent derivation, not on finite enumeration. No implementation or performance benchmark is asserted. This review adds an explicit dense-matrix/output-size accounting without changing the candidate's theorem or assumptions.

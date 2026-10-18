# Canonical actual read-after: path reduction and composition, sections 6--7

Reviewer: `/root/rainbow_gap_source`, 2026-10-18.

Canonical actually read in full: `/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md`.

Measured full-file SHA-256: `2081da9992ec465d5e6abaa96ab35f245c99ca879f848de780bf2b9e3f4d6399`.

**Formal certification scope: PASS for the path Claim in sections 6--7, its composition with the unchanged sections 1--5, and preservation of the old canonical prefix.** Sections 8--9 were actually read as surrounding context, but their three-state normal-form Claim is expressly not certified by this record; root assigned that independent review to general. The full-file hash identifies the version read and does not turn this into an endorsement of every appended Claim.

No canonical, source, repo, Work, or Git modification was performed.

## 1. Actual independent-first and read-after chain

The path Claim is `UM-FLAT-MENU-RESOURCE-DEGREE-THREE-PATH-REDUCTION-v1`. Before seeing its author Proof, I actually read the complete Exact and froze an independent proof reconstruction. Root then released the author Proof; I actually read it in full and separately froze its read-after. Those original records remain separate and unchanged.

Hashes remeasured for this canonical audit:

- Author Exact `flat_menu_resource_degree_three_path_reduction_exact_v1.md`: `7bbfc817db6081f574f7d2dd6c171c2b587152809c87adb071f99e5334635835`.
- Author Proof `flat_menu_resource_degree_three_path_reduction_proof_v1.md`: `41ed38ba1aff5b549a0599bb81290562b5bf3882688155d84aafdc122e11c1f7`.
- Independent Exact-only record `flat_menu_resource_degree_three_path_reduction_rainbow_exact_only_review.md`: `2932c421e7531ff1cd6d2e60cbbb1df0526814b2b6f4090668b291d2f095b77a`.
- Author-Proof read-after `flat_menu_resource_degree_three_path_reduction_rainbow_proof_read_after.md`: `a3a75b7bea09e2272523334f793c1285acee50af66ae7372947485ca76722184`.

This canonical audit compared the actual appended text with that frozen chain rather than treating root's reported independent check as proof evidence. No historical hash was invented.

## 2. Old sections 1--5 prefix preservation

The current canonical file has 21,318 bytes. Its first **7,915 bytes** have SHA-256

`def740ba49bb83b495f034ecd80efdb88d7a291fa6c048a6209db19dd5d6869e`.

That is exactly the old full-file canonical hash recorded in the actually read earlier `degree_three_weighted_menu_cube_embedding_canonical_read_after_review.md` and in the release manifest. Thus the old canonical, including sections 1--5 and its final LF, is still an unchanged prefix under the recorded cryptographic identity.

The append adds one new separating LF immediately after that prefix. Section 6 begins at zero-based byte offset 7,916. Consequently, hashing every byte before the `## 6.` marker, including the newly appended separator, yields a different and expected hash:

`8d18bbff7d42a9b36259ce009c8d9f0c124159cd529dd1dc38d9beac38d0d02b`.

This is an append-boundary newline, not an edit to the old Claim. The distinction is recorded so that a future raw section cut does not incorrectly report that the old 7,915-byte file changed.

The region from the start of section 6 to immediately before section 8 has 6,246 bytes and SHA-256

`63c9983a60ef9231c6a57f2a7dbeb1b07219de7229bf980e200d611462f4ee0d`.

Section 8 starts at zero-based byte offset 14,162. This region hash includes sections 6--7 and their trailing separator; it excludes the old prefix and the separate three-state Claim.

## 3. Section 6: exact domain and physical construction

The new domain is the old complete flat-menu ordinary UM domain with only the old resource-group-degree-three restriction removed. It retains nonempty explicit groups and menus, distinct resource identities within a state, W<=1, actual selectors of time one, actual incidence jobs of resource time one, private machines distinct from resources, and no extra jobs or constraints. Zero private times, empty states, duplicate indexed states, and unused resources remain allowed.

The text correctly defines resource memberships over complete menus, including zero-private-time original incidences. Old states, selectors, original private processing times, job identities, and private-versus-external choices are preserved in the source C<2 extension. One port is assigned per (old group, old resource), consistently across every state of that group. The two-state helpers are fully represented as two private state machines, one selector, and both singleton incidence jobs; no free matching or abstract capacity is substituted for their actual jobs.

The prescribed hole-a orientation covers all ports except a. Each helper's selected incidence is exported, its selector stays on that state machine, and its other state's incidence stays privately at load one. Both helper private machines and the used port have load one. Since source selectors force C>=1, adding them cannot raise a source C<2 schedule's peak.

For arbitrary target C<2, each helper's selected private-time-one incidence is forced out by its selector. These d-1 jobs occupy distinct ports. The text expressly permits unselected helper-state exports and counts them as additional occupancies. Thus at most one old job, including an unselected old-state job or a private-zero old job, can be externally assigned in the path. Collapsing original jobs back to the old resource is legal and nonincreasing. It does not require a preferred helper matching or full export of an old selected state.

The d=0 convention is now definite: retain the old resource unused. The d=1 case has one port and no helper. Both are within the proof. For supplied C>=2 the all-private schedule of the other complete instance is a valid fallback; the text properly does not promise preservation of that supplied schedule's private/export choices at this endpoint. Both optima lie in [1,2], and the two actual C<2 maps close exact OPT equality at OPT=2 without applying exclusivity at load two.

## 4. Normalized partial value, sizes, and precise boundaries

The V statement is restricted to normalized W=1 input. Its object is one actual state per group and an arbitrary resource subset of that state, with disjoint subsets across groups, maximizing common private exported mass. For every v>0 a helper must receive its selected singleton, value one, so the same d-1-port count projects every target partial allocation. Forward leaves the old allocated group as the hole and gives all helpers their singleton. Old selected states and all old allocated weights remain identical. The positive threshold directions imply preservation at V=0 as stated. No full-state or unknown YES witness is substituted for this partial decoder.

Each port is incident to one old group and at most two helpers, hence complete-menu degree at most three. Old K_g are unchanged and helpers have exactly two states, giving maximum menu size at most max(K,2). Old state masses are unchanged; all helper states have mass one. The text clearly disclaims preservation of the old interaction graph or M and keeps the heavy-only helper role distinct from endogenous mixed heavy/diffuse roles.

The counts are correct: sum d_u<=L, h<=L, at most L used ports and at most |U| retained unused resources, plus two private machines and three jobs per helper. Target machines are at most a+|U|+3L and jobs at most n+4L, so their dense product is polynomial. Rational times are copied unchanged or written as one; remaining finite eligibility lists, tags, path scans, and all-original-job mappings have polynomial binary size. No denominator, threshold inverse, or numeric processing time is expanded into objects.

No production implementation, finite enumeration, general-UM degree reduction, historical priority, or new hardness theorem is asserted. Standard matching-path attribution remains appropriately uncertified.

## 5. Section 7: composition with the old cube embedding

The composition order is valid: first apply the new path map D to an arbitrary complete explicit flat input P, then apply the unchanged old cube map C to D(P), whose resource group degree is now at most three. The second map's input hypotheses hold, including source groups and menus being nonempty, state resource identities being distinct, W<=1, and unit external costs.

The composition gives

`OPT(C(D(P)))=OPT(D(P))=OPT(P)`.

If the original input has W=1 everywhere, path helpers and old states are normalized, and the cube map adds only zero-private-weight incidences; normalization is therefore preserved. The path map has maximum menu size at most max(K,2), and the cube map retains every input group's indexed menu size, so that bound persists. Helpers increase group count, and D need not preserve M; C preserves D(P)'s interaction graph rather than restoring the original P interaction graph. Section 7 states these limitations correctly.

The cube target still requires zero-cell weights and state-dependent cost tables for indexed states that may share a label vector. It remains fixed d=Q=3 with explicit 27-cell variables and complete nine-cell slices. The composition does not require all-cell positivity, label-determined pricing, a one-heavy/two-diffuse role, or an implicit state enumeration. Two polynomial explicit constructions and their actual schedule maps compose with polynomial bit size; unused resources and empty old unions are handled by the old cube convention.

The resulting source obligation is stated accurately: an independently proved normalized tiny-export gap, with explicit small representation and a sound decoder for every state choice and partial export, is still missing. Removing resource degree is no longer that missing step. Arbitrary additive SC rows of mass greater than one are not admitted by these maps, and the existing same-universe normalized-menu size obstruction is not bypassed. This is a flat-to-flat-to-cube construction, not a free reduction from general ordinary UM or a proof of near-two hardness.

## 6. Certification limit

For the identified whole-file version, sections 6--7 agree with the frozen Exact and author Proof, and the old sections 1--5 remain the original hash-matching prefix. No standing fatal issue was found in this formal scope. Sections 8--9 were read but remain outside this record's certification; their separate Claim, review chain, and any additional consequences belong to general's assigned review.

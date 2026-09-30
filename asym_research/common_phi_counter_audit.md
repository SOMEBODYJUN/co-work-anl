# Independent adversarial audit of the shared-catalog phi construction

Date: 2026-09-30. Scope: the original two-facility common finite catalog, weighted atomic clients, and all independent mixed customer Nash equilibria. The asymmetric factor-2 lower example is not used.

## Verdict

No proof or implementation defect was found in the reviewed steps. This is an internal independent audit, not external peer review. The finite experiments below audit code and boundary handling; they are not the proof of the universal theorem.

Reviewed `phi_global_proof_candidate.md`, every section of `strong_cross_chord_arbitrary_n_proof.md`, `astra_local/construct.py`, `common_phi_algorithm.py`, and `asym_research/common_phi_menu_quantifier_audit.md`.

## Critical quantifiers

1. **Global Section 3.3.** If a response edge has menu minimum above the source reach, an all-common-to-source seed rules out responder private mass at most that reach. In the remaining case the private mass is larger, and every common client strictly prefers the source for every independent mixed profile. Thus the actual equilibrium is unique, and the menu minimum equals its responder load. No full-Nash minimization is needed.
2. **Section 6.** Start with a pure menu equilibrium and move all forwarded clients except H back to the source. If their total moved weight is F, the original H condition gives `P <= Q+H = r-F`, while `P0=P-F <= r-2F <= r`. Hence H remains stable. In the repair branch the sole common client on the lower side is H and the stated strict gap bound is below H; precisely the guarded singleton repair belongs to the menu.
3. **Sections 9.2 and 12.1.** A reverse singleton seed rules out `sigma >= R_s-R_t`. Once `sigma < R_s-R_t`, H strictly prefers the responder regardless of other customer actions. Given H there, the other common customers strictly prefer the source because its largest attainable load is below q, whereas the responder's fixed private-plus-H mass exceeds q. Actual uniqueness, including all mixed NE, follows independently of the menu minimum. The equality `d(s)=R_t-sigma` is justified.
4. **Section 7.** With the lower-reach site first, `D=B-A+W >= 0`, mixer coordinates are D, and all remaining common customers choose the other site. The load gap is exactly D. Both designated customers satisfy the indifferent-action equation; every other customer is on the lower-load side. At D equal to a designated weight the probability is an endpoint and its one-sided Nash inequality remains valid. At equal reaches both orientations are retained.
5. **Local exact iff.** The maximum-square argument, its positive and negative gap cases, the necessity by strict dominance, and the removal of the maximum-weight assumption were independently rederived. No counterexample or missing branch was found. The polynomial constructor needs the stated pairwise local exchange inequalities, not global quadratic maximization.

The code's T submenu uses the lower-reach orientation, with both orientations at equal reaches. This covers the global proof. An earlier audit description allowed both orientations at unequal reaches as well; those extra equilibria are optional, and the distinction should be explicit.

## Exact exhaustive implementation checks

`common_phi_counter_audit.py` independently computes each customer's conditional costs by summing every other customer's expected mass. It also calls the separate exact support enumerator `asym_research/bounded_overlap.py` to compare output loads with the full equilibrium spectrum.

The completed deterministic run checked:

* **10,206 local cases:** zero through four common customers, every nondecreasing weight list from `{1,2,3,4,5}`, and each private load in `{0,...,8}`. Every menu witness was an actual independent mixed NE; its load belonged to the exact full-support spectrum; independently constructing the swapped layout gave exactly the reflected probability menu.
* **1,771 complete common-catalog instances:** all multisets of three customer types, where a type consists of a nonempty subset of three sites and a weight in `{1,2,3}`. Every returned on-path and deviation witness was checked directly. The largest factor in this finite family was `4/3`.
* The strict three-mixer example below was checked against all `3^3=27` support patterns, and the proposed menu included its required equilibrium.

An additional 2,500 seeded rational instances in the strong-chord regime, with one through six common customers and no maximum-weight restriction, matched the exact local iff. This is a bounded counterexample search, not a universal existence argument.

## A sharp warning against truncating the local mixed support

Take reaches `R=100`, `r=99`, private loads `40,39`, and three common customers, each of weight `20`. The strong-chord hypotheses hold: `60<99q` and `20<100(1-q)`.

The total load is 139 and the private-load difference is 1. Exact support enumeration gives only these load vectors:

| Number of mixing customers | All attainable load vectors |
| --- | --- |
| 0 | `(60,79)` |
| 1 | None |
| 2 | `(79,60)` |
| 3 | `(277/4,279/4)` |

For one mixer the other two signed weights cannot cancel the private difference 1. For two mixers, placing the pure customer at the first site would require gap -21, outside the mixers' weight bounds; placing it at the second site gives gap 19 and loads `(79,60)`. With three mixers the gap is `-1/2`, each independent probability of choosing the first site is `39/80`, and loads are `(277/4,279/4)`.

Both pure and two-mixer vectors fail the target `(99q,100q)`, while the three-mixer vector meets it. The implementation returns this witness through `strong_chord_positive_large_three`. Therefore a proof that silently restricts this local lemma to at most two mixers is false. This local example does not claim to refute any global SPE existence theorem.

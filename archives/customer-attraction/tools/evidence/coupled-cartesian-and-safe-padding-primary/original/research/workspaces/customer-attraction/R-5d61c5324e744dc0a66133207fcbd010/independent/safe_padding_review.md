# Independent mathematical audit: fixed-population safe catalog padding

Reviewed `../security/safe_catalog_padding.md` and
`../security/audit_safe_catalog_padding.py` from the stated lemma, independently
of the author's proof reconstruction. The general extension argument is sound.
The zero-size catalog correction identified in the initial audit has now been
applied to the statement and exact implementation and independently replayed.
No conclusion about Q-CAG-HALF follows merely from this audit.

## All-history construction

At every old-only history the original SPE gives its current mover at least
K/m: deviation to a maximum old theme guarantees this amount against every
continuation. A new topic yields at most t<=K/m. Thus preserving the original
entire old-only policy is incentive compatible even after all new actions are
added.

After a new action has appeared in the prefix, solve the old-action restricted
subgame with that actual prefix, using one consistent backward-induction policy
at all old-action descendants. Every selected mover again gets at least K/m.
Every new-action child can enter its own restricted recursion, since the
deviator's payoff upper bound t is independent of its continuation. A history
containing a new action can never return to the old-only case, so these two
policy pieces do not conflict. The construction works separately at every
ordered history and preserves arbitrary original tie behavior.

## Optimum and quantifiers

For positive t, p>=m supplies enough distinct nonempty, mutually disjoint new
sets. An m-tuple with r old choices has coverage at most OPT_old,r+(m-r)t;
choosing a maximizing old tuple and distinct new topics attains it. The all-new
r=0 value mt is dominated by r=1 because K>=t. Equivalently one can state the
convolution with 0<=r<=m and OPT_old,0=0, then remove r=0.

The proof fixes m and quantifies every old complete pure SPE. Its restricted
continuation does not require that the original policy specify histories with
new actions. Positive rational t is implemented by one common integer scaling
of old customer multiplicities and new topic sizes. All payoff comparisons and
the threshold t<=K/m scale together. The padding consequence PF_r and the
universal equivalence with F are valid: use t=K/m in the forward implication;
the r=m member recovers F in the reverse implication.

## Zero-size correction

Under the exact set-catalog convention S subseteq 2^N, p different new topics
of size zero cannot be adjoined: they are all the same empty set, possibly
already old. The original audit implementation used distinct labels for such
identical empty sets. This has no incentive effect, but the literal statement
must handle t=0 separately: add at most the one empty set, or add no topic; retain
the original policy, extending after a newly introduced empty action by the
same restricted-old recursion. Empty deviations pay zero. The optimum remains
OPT_old,m, which equals the displayed convolution at t=0. If K=0, all topics
are empty and this case covers the entire game. This is a wording/model repair,
not a failure of the positive-size construction.

The corrected implementation quotients old topic labels that cover exactly the
same positive-multiplicity customers before building the old SPE. When K=0 it
adds no new topics, so it uses the strict set-catalog representation directly.
For K>0 the added topics contain K new customers after scaling, and are therefore
nonempty, mutually disjoint, and distinct from every old topic. The corrected
statement explicitly separates the zero case.

## Code replay

The corrected independent replay passed all 36 finite cases and **15,849** exact
all-history comparisons. The source was executed without changing it; its output
path was redirected to this directory by changing only the runtime __file__
value. `safe_padding_strict_catalog_replay.json` contains the actual corrected
output plus the source hashes and representation description.

The exact corrected source versions reviewed and replayed are:

* `../security/audit_safe_catalog_padding.py`, SHA-256
  `60ca4bcd48585c50b68a15d1041614ca51f8bb6e75ca8e8d2a1216923c6556ed`.
* `../security/safe_catalog_padding.md`, SHA-256
  `b622ac3039ae96b24626ef0a1c7335f98f62c0278aa8899ed551b33fc4314a4a`.

The earlier `safe_padding_audit_replay.json` is retained as the **pre-repair
labeled-representation** receipt with 17,106 comparisons. It allowed repeated
labels with the same old coverage and multiple newly labeled empty sets in the
zero case; it is not the strict-catalog implementation receipt. The count
difference is due to quotienting these equivalent topics and omitting the zero
padding, not to a failed payoff comparison.

Both implementations use only exact Fractions and their own backwards recursion.
The deterministic old tie choice tests one policy per input, as accurately
stated; the all-policy quantifier rests on the symbolic argument.

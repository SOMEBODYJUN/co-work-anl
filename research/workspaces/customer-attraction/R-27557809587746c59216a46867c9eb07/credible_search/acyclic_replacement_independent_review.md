# Independent review: acyclic replacement lemma

Review date: 2026-10-21. Verdict: **the stated conditional lemma and its two
source-policy assertions pass independent mathematical reconstruction**. No
fatal objection found. This does not establish universal witness existence or
Q-CAG-HALF. The general witness-existence assertion is false, as the note says.

Reviewed source: `../weak_matching/acyclic_replacement_lemma.md`, SHA256
`9607fcdcb4770ca6832fd8d032fe640fb5df59516b58e075da20dea872038cc4`.
I reconstructed the inequalities from individual-client shares and replayed
the original stored action maps, without running the author's lemma probe or
source audit. The deterministic replay is `review_acyclic_sources.py`; exact
results and input hashes are `acyclic_independent_source_review.json`.

## Exact quantifiers and independent proof

Fix the entire pure strategy, its actual ordered terminal history z, and an
arbitrary ordered comparison tuple of exactly m occurrences. No optimality,
distinct-label, anonymous-history, or tie assumption is needed. The branch
after each selected history and comparison action must follow this **same
entire original strategy**, not a newly selected equilibrium continuation.

Assign actual labels a_j with precisely the actual count vector q, and choose
actual-path histories prescribing those labels. Let P_j consist of comparison
clients whose first covering comparison occurrence is j. For a client x in
P_j, dot the proposed coordinatewise terminal-count bound with its Boolean
interest row. All earlier comparison occurrences omit x, giving

\[
1\le b^j(x)\le c_x+1-\mathbf1_{x\in a_j}=:d_{j,x}.
\]

Hence its actual deviating share is at least 1/d_{j,x}. The P_j are disjoint,
so their total frozen charge is bounded by the sum of the m true query
utilities, even though each query may also earn other nonnegative shares.
At each chosen actual-path history, SPE bounds the corresponding true query
by U_{a_j}(q). Since the assigned-label counts are exactly q,

\[
R_{\rm first}\le\sum_j U_{T_j}(b^j)
\le\sum_jU_{a_j}(q)=\sum_aq_aU_a(q)=W.
\]

The cheapest-owner partition R for this same occurrence matching is at most
R_first. This proves the asserted payment inequality.

There is one implicit denominator argument worth spelling out. Always
d_{j,x}≤m: if a_j covers x it equals c_x≤m; if a_j omits x, the actual profile
has at least one omitting slot because q_{a_j}>0, hence c_x≤m−1 and d=c_x+1≤m.
For a missed client c_x=0, every actual label omits x and its charge is exactly
one. For a covered comparison client, its charge is at least both 1/m and
1/(c_x+1). Adding the unpaid portions gives respectively

\[
|\cup_jT_j|\le R_{\rm first}+(1-1/m)W\le(2-1/m)W,
\]

\[
|\cup_jT_j|\le R_{\rm first}
+\sum_{x\text{ actually covered}}\frac{c_x}{c_x+1}
\le W+\sum_{x\text{ actually covered}}\frac{c_x}{c_x+1}.
\]

## Repeated labels and ordered histories

- Comparison occurrences remain separately indexed even when labels repeat.
  A client belongs only to its earliest covering occurrence; every earlier
  occurrence therefore omits that client. Multiplicities in the count bound
  are essential and have been preserved.
- If the same actual topic is used by several actual players, they have the
  same terminal payoff U_a(q). A selected on-path history may consequently be
  reused several times, up to its assigned topic's total q_a budget. This sums
  copies of a valid inequality; it does not require distinct physical players
  to supply distinct histories. The total assigned-label condition supplies
  exactly W, including reused histories.
- Histories with the same topic counts are never identified by this proof.
  Each b^j is the real continuation from the specific ordered history h_j.
  Repeated coverage sets with distinct catalog labels also cause no problem:
  client loads are dot products of label counts with Boolean interest rows.
- Empty comparison topics create empty owner blocks. If m=1, the same proof
  yields comparison coverage≤W. All-zero customer instances are harmless.

## Independent source replays

The four-player/six-topic/52-client source has actual history 3322, W=47,
all four actual payoffs 47/4. I directly verified all 259 ordered decision
histories and 1295 nonself deviations, including root. The queried branches
reconstruct in their actual order as 3302, 3312, 4230, 5042; their multisets
and count bounds match the note. Query utilities are

\[
47/4,\quad35/3,\quad139/12,\quad35/3,
\]

whose sum is 140/3≤47. The first-owner frozen sum at the saved customer point
is 277/12. Independently checking every nonempty Boolean interest type gives
the owner load/share inequality for all 60 comparison-covered types; the
remaining three types have zero owner charge. Thus the typewise argument
really applies to every nonnegative customer vector making this fixed policy
SPE, rather than just the original 52-client input.

I also directly verified the two-player portfolio source's complete SPE
(six histories, 24 nonself deviations). Actual history is (E,A), W=44,
OPT=45. For each of the two comparison orders of (B,D), and each of the two
assigned-topic matchings, at least one proposed coordinate count bound fails.
All four choices have true query sum41, while42 comparison clients are missed.
An acyclic witness would force its true query sum≥R_first≥42, so this is a
valid obstruction to **universal existence of this witness**, not to the
conditional lemma or half coverage.

## Requested clarifications, not objections

It would help to add the explicit d_{j,x}≤m argument above and consistently
distinguish cheapest-partition R from the chosen first-owner R_first. Both
inequalities are already logically valid in the source. No mathematical
change or additional tie convention is required.

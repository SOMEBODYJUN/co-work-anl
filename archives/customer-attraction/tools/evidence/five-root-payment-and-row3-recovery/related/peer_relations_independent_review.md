# Independent review: crossed-reply tax and second-to-D separator

2026-10-25. Reviewer: direct_coverage subagent. This review accepts the
specific statements below. Neither is a proof of OPT5<=2W or an actual
five-player counterexample. No claim of external review or novelty is made.

## Crossed-reply tax: accepted

Reviewed `../fresh_proof/crossed_reply_tax.md` directly. Every one of the
three slacks is a valid current-player IC at its precise ordered history:
first follower copies R_j and faces the actual K_ij; K_ij is last-player BR
at (h,T_i,R_j); S_i is BR at (h,T_i,R_i), where K_ij is a legal alternative.
No old-player payoff is transported between branches.

I reconstructed identity (3) from the exact congestion potential on three
and two topics, rather than assuming the requested conclusion. The two
pair-potential terms cancel after independent i,j averaging under the same
law. Identity (4) is the same-background two-player share difference.
Adding the proposed tax leaves the pointwise nonnegative remainder

    1_(R_i minus K_ij) / [(b+1+1_Ti)(b+2+1_Ti)].

Thus the general taxed decorrelation inequality and its weighted-query
version follow for every nonnegative integer background, including all
ties, repeated queries and empty themes. This does not assert ordinary
nonnegative decorrelation or ROW3.

The independent audit represents each rational expression by its exact
coefficients of 1/(b+1),1/(b+2),1/(b+3), using
1/[(b+k)(b+k+1)]=1/(b+k)-1/(b+k+1). All 64 membership cases vanish exactly
as symbolic rational functions of b; this is stronger than checking finitely
many background values. The proof of the universal statement remains the
legal ICs and averaged identity.

## Seven-row second-to-D envelope: accepted for the frozen primal

Reviewed `../branch_geometry/separate_second_D.py` and its seven formulas.
The new path is (A,D,R,S,T), obtained when the actual second player deviates
to the actual fourth player's legal topic D. The first row is that player's
true IC. The next two are exact final-player BR comparisons with E and the
sum of five optimal themes. The next two use the existing (A,E,T_i,R_i,S_i)
fourth-player nodes to query the newly named R and S, with valid
worst-denominator bounds. The final two use the existing
(A,T_i,H_i,I_i,J_i) third- and fourth-player nodes to query new T, again with
valid worst-denominator bounds.

The independent audit reconstructs these rows without importing either
peer helper or an optimizer. It also checks that all three old histogram
families give the same optimal-theme multiplicity at each old atom. It then
enumerates all eight possible new (R,S,T) membership triples at each of the
64 old atoms, with the exact seven rational nonnegative weights read from
the stored certificate. Every computed maximum agrees with the stored list.
Their old-mass-weighted sum is exactly

    -336525906357864252494704662357779526105596687
    /24837228663957176671172182423497877773536000000 < 0.

Any real extension must split an old atom among those eight triples and
must have all seven global slacks nonnegative. Its weighted sum would
therefore be nonnegative, but cannot exceed the strictly negative sum of
per-atom maxima. This contradiction excludes extending this exact old
primal to the new true second-to-D branch. Ignoring any additional theme
collisions or ordered-history coincidences only enlarges the extension
space, so does not weaken this exclusion.

The conclusion is a fixed-primal nonextension certificate. It neither
bounds the strengthened relaxation globally nor excludes other putative
half counterexamples.

## Reproduction

`python3 audit_peer_relations.py` uses only Python's standard library. Its
exact output is `peer_relations_independent_audit.json`. It does not run an
optimizer, import the peer row builders, modify old certificates, or claim
the original matching primal is a full SPE.

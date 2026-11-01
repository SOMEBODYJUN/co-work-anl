# Minimal leader failure: no dominated follower theme and outside-root expansion

2026-10-24. Conditional general reduction, elementary direct proof, not independently reviewed. This is not a proof of Q-CAG-HALF, FF-LEADER, or an extra-one leader bound. The original half target remains OPEN.

## General contract

Fix the unit-customer common-catalog model. A legal background b is the load of a fixed finite ordered prefix; the catalog remains fully available. Let G_r(b) be a nonnegative benchmark for a subgame with r remaining providers. Suppose it has legal-prefix monotonicity

    G_(r-1)(b + 1_A) >= G_r(b)

for every legal catalog action A and r>=2. This is the embedding property enjoyed by free fractional safety t_r(b), extra-one fractional safety t_(r+1)(b), and true extra-one static safety v_(r+1)(b). No strategic interpretation of hidden random queries is used here.

Assume the universal leader statement u_current >= G_r(b) fails, and select the least remaining population r for which it fails, allowing all common catalogs and all legal backgrounds. Fix one failing full-history pure SPE at background b and denote its current equilibrium utility by u<G_r(b)=t. The r=1 case must be ruled out separately for a chosen benchmark; for the three named benchmarks it follows directly from last-player optimality and adding permissible static competition.

For every root action A, retain the original SPE's actual continuation after forcing A. Let d_A be the root utility in that branch. Root optimality gives d_A<=u<t. Write a_x=1_(x in A), k_x for the r-1 followers' load in this branch, and use full denominator b_x+a_x+k_x.

## Claim 1: every true-branch follower earns at least t

A follower at any position on that branch acts at some legal extension b' with s<r remaining providers. Minimality of r gives its utility at least G_s(b'). Repeated prefix monotonicity gives G_s(b')>=G_r(b)=t. These are utilities at the same branch leaf, not utilities imported from the original on-path terminal.

Consequently every branch follower strictly out-earns the forced root, because its utility is at least t>d_A.

## Claim 2: no follower theme is contained in A

If a follower selected B subseteq A, same-leaf comparison gives

    u_B = sum_(x in B) 1/(b_x+a_x+k_x)
        <= sum_(x in A) 1/(b_x+a_x+k_x) = d_A.

This contradicts Claim 1. In particular no follower copies A. Empty A and empty follower themes are included; t>u>=0 excludes an empty follower theme in a minimal failure.

This conclusion concerns the actual leaf of every forced-root branch. It does not assert that the whole child strategy avoids subsets of A at arbitrary further deviations: at those leaves, the original root utility need not remain at most u.

## Claim 3: expansion paid by the child, with a branch-specific gap

Let V_out(A) be the sum of followers' profit from customers outside A in this branch:

    V_out(A) = sum_(x notin A) k_x/(b_x+k_x),

with zero terms when k_x=0. Followers earn at least (r-1)t in total. Their profit from A is

    V_in(A) = sum_(x in A) k_x/(b_x+1+k_x)
            <= (r-1) sum_(x in A) 1/(b_x+1+k_x)
            = (r-1)d_A.

Therefore

    V_out(A) >= (r-1)(t-d_A) >= (r-1)(t-u) > 0.

Each outside-A customer contributes at most one to V_out(A), so the followers' coverage outside A is at least the same quantity. If background customers are present, V_out is remaining-provider profit rather than total coverage; the displayed inequality is still valid.

## Precise stopping point

The reduction uses successor rationality at every forced-root branch and is valid for arbitrary catalog, history-dependent ties, repetitions, and legal backgrounds. It does not identify V_out(A) with any actual-root-path profit or sum the separate branch budgets. The same customer may supply expansion in many branches. A proof still needs a new common payment across those branches, or another mechanism. No claim of novelty is made.

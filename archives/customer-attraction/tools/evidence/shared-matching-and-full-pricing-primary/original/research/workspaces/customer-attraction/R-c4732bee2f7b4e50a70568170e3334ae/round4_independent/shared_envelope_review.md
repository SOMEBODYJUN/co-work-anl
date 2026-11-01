# Shared-incidence final-menu envelopes: independent check

2026-10-21. This checks the algebra and matching extrema proposed by `coupled_menus`. The conclusion is a necessary-condition interface at genuine final-player histories. It is not a welfare theorem or an SPE construction.

For one client at q genuine final-player histories let `d_i=1/(load(h_i)+1)`, let `f_i` indicate the actual final action's membership, and write `A=sum_i f_i d_i`, `D=sum_i d_i`. Two indexed legal query lists have bits `z_i,w_i`, totals `K,L`. Summing their offdiagonal final-player comparisons gives exactly

\[
2(q-1)A-(K+L)D+\sum_i d_i(z_i+w_i).
\]

The two diagonal comparison sum is `2A-sum_i d_i(z_i+w_i)`. A diagonal comparison for the z list and an offdiagonal comparison for the w list sum to `qA-LD+sum_i d_i(w_i-z_i)`. These exact identities hold before any matching relaxation.

Inside each preserved anchor class t, suppose the two query membership counts are k,l and their shared membership count is h. The multiset of weights `z_i+w_i` has h copies of 2, k+l-2h copies of 1, and the remaining copies of 0. Sorting the positive d values proves the exact per-client extrema

\[
\max\sum_{i\in t}d_i(z_i+w_i)=\mathrm{Top}_t(h)+\mathrm{Top}_t(k+l-h),
\]

\[
\min\sum_{i\in t}d_i(z_i+w_i)=\mathrm{Bottom}_t(h)+\mathrm{Bottom}_t(k+l-h).
\]

The weight `w_i-z_i` has l-h copies of +1 and k-h copies of -1. These can occupy disjoint slots because their sum is at most the class size. Thus its exact per-client maximum is `Top_t(l-h)-Bottom_t(k-h)`. Empty classes, h=0, repeated d values and q=1 cause no exception.

Using the maximum in the first and third exact identities, or the minimum in the negative term of the second, increases the relevant comparison sum. Hence summing these per-client upper envelopes preserves the necessary nonnegativity of genuine SPE comparison sums.

The qualifiers “per-client” and “upper envelope” are essential. Different clients can select different maximizing permutations. Their summed extrema need not equal the maximum under one globally consistent assignment of actual query topics. This does not invalidate necessity because the optimization is over a superset; it does prevent claiming an exact globally realizable query matching.

There is a strict gap even for legal final histories. Take two unit clients x,y and common catalog `{empty,{x},{y},{x,y}}`. Let `h_1=({y})`, `h_2=({x})`, and let the actual final action at both histories be `{x,y}`, which is a best reply at both. Then `d_x=(1,1/2)` and `d_y=(1/2,1)`. The query list `({x,y},empty)` has k=1,l=h=0 for each client in a single anchor class. Either one common permutation has total query contribution 3/2. The sum of separate per-client maxima is 2. This example attacks exact global realizability, while confirming the direction of the necessary relaxation.

`shared_envelope_audit.py` independently enumerates q=1,...,6, 44 load/anchor configurations and 49,064 literal pair-membership assignments. It verifies 147,192 literal-comparison identities and matches the three extrema in all 7,511 resulting anchor-count classes using exact Fraction arithmetic. The actual report is `shared_envelope_audit.json`. These finite checks audit the implementation; the sorting argument above proves the general formulas.

## Retained-overlap two-player cross-family version

The subsequent `coupled_menus` extension is also algebraically valid. At q genuine two-player decision histories define `a_i=1/(p_i+1)`, `e_i=1/(p_i+2)`, `b_i=a_i-e_i`, and let H_i be the actual two-player total payoff plus the first remaining action's self-tax. The already established retained-overlap inequality compares H_i against every legal pair of query topics. For two target query lists, summing `j=k != i` gives exactly

\[
(q-1)\sum_iH_i-(B+C)\sum_i a_i+K\sum_i b_i
+\sum_i\bigl[a_i(z_i+w_i)-b_i z_iw_i\bigr].
\]

The last summand has values 0, a_i, a_i+e_i as `z_i+w_i` equals 0,1,2. Its score is precisely the harmonic increment for adding that many query-coverers. If an anchor class has union count u and intersection count h, then h<=u and its exact per-client maximum is `Top_a(u)+Top_e(h)`. Both inverse-load lists have the same ordering in p, so selecting nested initial segments attains both terms simultaneously. Their minimum is `Bottom_a(u)+Bottom_e(h)` by the same reasoning. Applying the maximum to the positive score gives the offdiagonal upper envelope. For the diagonal comparison sum `sum H-score`, applying the minimum gives its upper envelope.

This construction requires the preserved anchor classes to have the same cardinalities on the source and target sides; it follows when both use the identical common indexed anchor membership list. It retains the same cross-client realization caveat as the final-player envelopes. The exact per-client optimization and the necessary direction are correct; it does not certify the existence of one globally consistent assignment of target topics across clients.

The same independent audit was extended and actually rerun: 98,128 retained-overlap literal comparison identities and 7,511 harmonic-score extrema classes pass exactly, in addition to the final-player checks above.

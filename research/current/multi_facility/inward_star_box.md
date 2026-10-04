# SC-K-INWARD-STAR-2: polynomial box selector for light edges pointing to a late center

Internal proof, 2026-10-04. The star may have arbitrarily many leaves,
individually named clients, and mutually unequal positive binary rational
weights. No external review, priority check, or canonical implementation is
recorded.

## Exact statement

Run SC-K-GREEDY-BUDGET on an MF-MODEL input with positive reach. Write `gamma`
for the last insertion score, `q_s` for each occupied site's facility count,
and freeze clients having only one occupied option as well as those of weight
at least `gamma` at their original greedy sites. Suppose each nontrivial
component of the remaining light-client overlap is either a single site or
an **inward star**: one center `c`, leaves `l`, and every remaining client
in the component has exactly the two occupied options `{l,c}` for one leaf.
Each leaf opens strictly before its center, so these clients were initially
assigned to their leaf. The original greedy maximum-multiplicity lemma gives
`q_l>=q_c`. Frozen clients may have options across components; the final
full boxes certify their optimal responses.

**Claim.** A polynomial number of exact rational operations constructs a
site-pure, within-site-uniform exact customer NE satisfying
`q_s gamma<=W_s<=(q_s+1)gamma` at every occupied site. BOX-TO-2 then
constructs the complete exact continuation with facility deviation ratio
at most two in input-bit-polynomial time. This theorem concerns the
specified greedy occupancy and full-box pure site assignment; it does not
assert an algorithm on arbitrary overlap graphs.

## Algorithm

Process star components independently. Let `r=q_c`, `C=W_c`, and
`A_l=W_l`. Sort the variable clients on each leaf edge in **nonincreasing**
order of weight. The head weight `w` of each nonempty leaf queue has key

`U_l(w)=r A_l/q_l+(1-r/q_l)w
       =r(A_l-w)/q_l+w.`

Repeatedly take a head of maximum current key, with arbitrary tie-breaking.
If `r(A_l-w)/q_l>C`, strictly move that client from `l` to `c`;
otherwise permanently leave it at `l`. Pop the head in either case and
update `A_l,C` and that leaf's next key. Each client is processed once.
Other occupied sites remain at their initial assignment.

## Boxes and best responses

For a light client `w<gamma`, a strict leaf-to-center improvement is exactly
`r(A_l-w)/q_l>C`. Because `q_l>=r`, the standard forward-move box
inequality says such a move preserves both sites' full boxes: source lower
bound follows from strict improvement and target load at least `r gamma`;
target upper bound follows by contradiction from `w<gamma`,
`q_l>=r`, and the source upper bound. All other site boxes are unaffected.
The original greedy assignment lies in every box, so all intermediate
states do too.

The sequence of popped keys is nonincreasing. If a head is left in place,
`A_l` stays fixed and its next weight is no greater; the coefficient
`1-r/q_l` is nonnegative. If it moves, `A_l` falls by its weight and
the next weight is again no greater. Thus the updated key of that leaf
cannot increase; taking a maximum head preserves global nonincrease.

A client left at a leaf has no strict move at its processing time. Later
the leaf load can only decrease and the center load can only increase, so
it remains stable. For a client `j` previously moved to the center from
leaf `l`, the exact no-return condition is

`C <= V_j := r A_l/q_l+w_j.`

Immediately after its own move of weight `w_j`, the strict improvement
test gives `C_new<C_old+w_j=U_l(w_j)=V_j`. Suppose a later selected
head of weight `w` and key `U` moves. Its new center load satisfies
`C_new<C_old+w<U`. If `j` came from another leaf, its `V_j` is unchanged
and remains at least the key at which `j` was moved, hence at least `U`.
If `j` came from the same leaf, the nonincreasing within-leaf order gives
`w_j>=w`, and after the new move

`V_j(new)=r(A_l(old)-w)/q_l+w_j=U+(w_j-w)>=U>C_new.`

This induction keeps every center client stable throughout, including when
`q_l=r` or keys tie. All unprocessed light clients are examined eventually.
Frozen singleton clients have no alternative. Any frozen heavy client
`w_i>=gamma` at site `s` is stable under the final boxes because
`(W_s-w_i)/q_s<=gamma<=W_t/q_t` for every occupied alternative `t`.
Thus the output is an exact customer NE, not just a boxed assignment.

Sorting, heap updates and at most one decision per movable client take a
polynomial number of comparisons and rational additions. Every accumulated
weight, key, and cross-multiplied comparison has input-polynomial bit length.
The inherited BOX-TO-2 routine then supplies all labeled deviation
continuations; the star routine itself does not need to enumerate layouts.

## Relationship to existing results and open boundary

An explicit strict family shows the scope is not limited by a fixed
center-weight diversity. For any integer `n>=3`, let `G=n^3`. There
are `n` leaves `H_j`, a center `C`, and a separate isolated site `R`.
At `H_j` put a private client of weight `3G-2j` and a light client
of weight `j` with options `{H_j,C}`; at `C` put a private client
of weight `G+1`, and at `R` one of weight `G`. Take `k=2n+2`.
The initial leaf reaches are `3G-j`. Greedy strictly opens
`H_1,...,H_n`, then adds their second seats in the same order with
scores `(3G-j)/2`, then opens `C` and `R` with scores `G+1,G`;
third-seat scores are below `G`. Thus the final multiplicities are
`q_{H_j}=2,q_C=q_R=1` and `gamma=G`. All `n` different light
weights are initially at their leaves; the algorithm transfers them to
`C`, ending with `C=G+1+n(n+1)/2<3G/2`. At each step the leaf's
post-transfer normalized load is `3G/2-j`, larger than the current
center load; the final center-client no-return threshold is exactly
`(3G-2j)/2+j=3G/2`. Hence this family gives genuine greedy
outputs with unbounded `d_C=n`, outside a fixed-local-weight-diversity
condition. For `n=3`, the initial pools are `80,79,78,28,27`,
the greedy scores are `80,79,78,40,79/2,39,28,27`, and the final
loads after client moves are `79,77,75,34,27`.

SC-K-STAR-LIGHT-GREEDY-2 treated a center opened before all leaves and
selected a lowest-load leaf. This theorem treats the opposite opening
orientation by a highest-key queue. The directed depth-one existence
theorem already implied a boxed NE for these stars, but did not supply a
bit-polynomial selector. Unlike the bounded-local-weight-diversity DP,
this algorithm allows arbitrarily many distinct light weights incident
to its center. General components with both inward and outward edges,
or a client having three occupied options, remain outside its statement.

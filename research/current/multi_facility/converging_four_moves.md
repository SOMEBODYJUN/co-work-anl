# Four strict moves for a converging four-site light path

**Internal research draft, 2026-10-03.** Independently reviewed by Sol Reviewer
after removal of the earlier draft's tight-A and equal-A/C restrictions. No
external review or literature-priority assertion.

## Exact scope

Run the canonical greedy construction on positive-reach explicit rational
MF-MODEL input, and let gamma>0 be its last score. Freeze every customer of
weight at least gamma and every customer with one occupied option at its
initial greedy site. Suppose a component of the movable light overlap graph
is the four-site path with edges DB, BA, AC, and precisely one light client
on each edge:

* T has weight t and occupied options D,B; its initial assigned site is D.
* X has weight x and occupied options B,A; its initial assigned site is B.
* Z has weight z and occupied options C,A; its initial assigned site is C.

Thus the opening directions converge at A: D->B->A and C->A. Write
`q_D=Q, q_B=p, q_A=r, q_C=R`. GREEDY-MAX-MULT already implies
`Q>=p>=r` and `R>=r`. No equality between A,C multiplicities or tight load
bound at A is required. All frozen clients may have arbitrary weights and
arbitrary heavy incidence across different light components.

**Theorem.** This component admits a site-pure, within-site independent-uniform
exact customer NE in every greedy box, and the construction uses at most four
strict site moves. Combining independent such components with existing
component constructors gives a bit-polynomial box NE and the complete exact
factor-two continuation of BOX-TO-2.

This strengthens the finite existence result on opening-directed height-two
light graphs by giving an explicit polynomial constructor on this particular
nonstar subclass. It does not assert polynomial minimization of global
customer potential on all height-two graphs or general greedy box existence.

## Algorithm

Let P_A,K,c,d be the frozen background totals at A,B,C,D. Initial totals are
`P_A, M=K+x, c+z, d+t`; each is in its greedy box.

1. If `c/R>P_A/r`, move Z:C->A. Otherwise keep Z at C. Let A0 be A's
   normalized load after this step: `A0=(P_A+z)/r` if Z moved, and
   `A0=P_A/r` otherwise.
2. Check whether T strictly improves D->B, namely `d/Q>M/p`. If so, move T.
3. Check whether X strictly improves B->A. With T at B the condition is
   `(K+t)/p>A0`; with T at D it is `K/p>A0`. If so, move X.
4. If T was not moved in Step 2, check its strict D->B improvement again
   after Step 3 and move it if improving.
5. If Z is at A, check whether it strictly improves A->C after Step 3 and
   return it if improving.

There are only four possible actual moves: Z initially enters A, T enters B,
X enters A, and Z returns C. Checking T twice permits its improvement to
become active when X leaves B. The final T and Z checks are independent.

## Box invariant

A strict site move i:s->u means
`(W_s-w_i)/q_s>W_u/q_u`. It always preserves every lower box: the source's
new normalized load exceeds the target's old load, which is at least gamma.

Every strict move with `q_s>=q_u` also preserves the upper boxes. Its weight
is below gamma because the source external load is at most
`gamma+(gamma-w_i)/q_s` while the target load is at least gamma. If the
target overflowed after receiving the client, its old normalized load would
exceed `gamma+(gamma-w_i)/q_u`, which is at least the source external load,
contradicting strict improvement.

The initial Z move, X move, and T move all have source multiplicity at least
target multiplicity. The only possible upward-multiplicity move is the final
Z:A->C return. C has no other movable client, and this return merely restores
its original total c+z, which is in its original upper box. Its source lower
box survives because the return is strict. Thus every actual move stays in
all boxes, without any global optimization.

## Permanent stability of T and X

After Step 1, Z is stable: if it moved, its external cost at A is P_A/r,
strictly below C's load c/R; if it did not move, its external cost c/R is at
most A's initial load P_A/r.

If T moves in Step 2, its future B external cost is at most M/p, because X
can only stay B or leave B. This is strictly less than d/Q by the move test.
T therefore stays a best response permanently.

If T does not move initially but moves after X leaves B, its B external cost
is the constant K/p, strictly below d/Q. It is again permanently stable.
If it never moves, the final check certifies `d/Q<=W_B/p`.

Whenever X moves to A, its A external cost is at most A0: Z may remain A
or leave for C, and no other movable client enters A. If T already moved,
the B load after X's departure is `(K+t)/p>A0`. If X moved before T,
the B load is initially `K/p>A0` and can only increase when T enters.
Hence X is permanently stable at A.

If X stays B, T has already received its first check. T cannot newly improve
without X's departure. Thus the Step 3 comparison certifies X's final
stability at B; Z's subsequent final check changes neither A nor B unless
X moved. In this no-X-move case Z remains stable after Step 1 and stays put.

## Final stability of Z

If Z stayed C in Step 1, its external cost c/R is at most P_A/r. A's load
can only increase with X, so Z remains stable forever.

If Z entered A, the final check considers exactly its two options. If it stays
A, the failed strict test certifies its best response. If it returns C, its
external cost there is c/R, strictly below A's final load `(P_A+x)/r`.
No later move affects A,C. In either case it is stable.

Every frozen heavy client remains stable because within all boxes its source
external cost is at most gamma, while every alternative occupied site has
load at least gamma. Frozen single-option clients have no site alternative.
Thus the final assignment is a site-level exact equilibrium, and independent
uniform mixing inside each assigned site is an exact MF-MODEL client NE.

## Complexity and separation

Each component has three movable clients. Its four actual moves and five
strict comparisons use only rational sums and divisions by facility counts,
with polynomial bit length. Component recognition, the greedy constructor,
and the off-path BOX-TO-2 completion are bit-polynomial on explicit input.

Take k=9, sites A,B,C,D,R, private weights respectively
`(105,200,214,340,100)` and light customers X:(20,AB), Z:(5,AC), T:(50,BD).
Greedy strictly inserts

```
D:390, B:220, C:219, D:195, D:130,
B:110, C:219/2, A:105, R:100.
```

Thus gamma=100 and `(q_A,q_B,q_C,q_D,q_R)=(1,2,2,3,1)`. A is not at its
tight lower box and qA differs from qC. The algorithm makes four strict moves,
so its bound is attained:

| Client move | source external load | target normalized load |
| --- | ---: | ---: |
| Z:C->A | 107 | 105 |
| T:D->B | 340/3 | 110 |
| X:B->A | 125 | 110 |
| Z:A->C | 125 | 107 |

The final totals are `(125,250,219,340,100)`. Every step is in all boxes;
every final customer satisfies its exact conditional NE inequalities.
The old RANGE certificate fails for Z (`(219-5)/2=107>105`) and T
(`(390-50)/3>219/2`). The light graph is a nonstar path, the three unequal
weights exclude the uniform-light constructor, no common anchor covers all
light clients, and the converging orientation excludes the consistently
directed-path constructor. The JSON input and independent exact checks are
in [the canonical JSON](../../../examples/multi_facility/greedy_converging_four_moves.json) and
[exact arithmetic audit](../../../tests/audits/kfac_converging_four_moves.py).

The old `greedy_repair_order_escape.json` also lies in this class; the
constructor chooses its known good box NE at the same occupancy.

The class still requires one light client on each of exactly three path
edges and this specified converging orientation. The earlier bad on-path
NE and its forced mixed off-path deviation at the same occupancy remain
valid; this algorithm selects a different on-path NE.

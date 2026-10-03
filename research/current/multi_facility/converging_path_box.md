# A converging four-site light path admits a box NE

Complete conditional proof, independently reverse-audited internally. No external or literature-priority review.

This narrower theorem is subsumed by the later [four-move version](converging_four_moves.md), which drops the tight-A and equal-A/C restrictions. Its original finite-state argument remains an independent proof.

## Conditional input class

Run the canonical greedy procedure on explicit positive-rational MF-MODEL
input, with final positive score gamma. Freeze every single-occupied-option
client and every client of weight at least gamma at its initial assigned site.
Suppose a component of the remaining light overlap graph consists of the path

```
D -- B -- A -- C
```

with precisely one light client on each edge and no other movable client:
T on DB of weight t, X on BA of weight x, and Z on AC of weight z. Their
initial sites are respectively D,B,C. Assume

```
q_D=Q >= q_B=p >= q_A=q_C=r >= 1,
W_A^0=r gamma.
```

These are checkable conditions on the greedy output. The initial directions
are D->B->A<-C, so this is a nonstar component and is not a consistently
directed path. Heavy clients may cross this component and any others, but
remain frozen. For this component write its frozen background totals as

```
P_A=r gamma, P_B=K, P_C=c, P_D=d.
```

Initially its totals are `(r gamma, K+x, c+z, d+t)` at A,B,C,D, and the
greedy box says

```
p gamma <= M=K+x <= (p+1)gamma,
r gamma <= c+z <= (r+1)gamma,
Q gamma <= d+t <= (Q+1)gamma.
```

**Conclusion.** A site-pure, within-site independent-uniform exact customer
NE in all component boxes exists and is found by at most seven strict site
moves. Processing independent such components, together with any other
already established component constructors, yields a full box NE and hence
a bit-polynomial complete factor-two continuation by BOX-TO-2.

## Construction

1. If `c/r>gamma`, move Z from C to A. Otherwise leave Z at C.
   Let `A0` denote A's normalized load after this step: it is either
   `gamma+z/r` or `gamma`.
2. If T now strictly improves D->B, move T first and then perform any strict
   moves of X,Z,T until none remain.
3. Otherwise, if X strictly improves B->A, move X, freeze it at A, and perform
   any strict moves of Z,T until none remain. If Z was initially left at C,
   freeze it there as well.
4. If neither T nor X improves after Step 1, the state is already a NE.

## General box facts

A strict move i:s->u means `(W_s-w_i)/q_s>W_u/q_u`. From a box state its
source's new normalized load exceeds the target's old normalized load, which
is at least gamma, so every lower box survives any strict move.

If `q_s>=q_u`, every upper box also survives. The move implies `w_i<gamma`,
because the source external load is at most `gamma+(gamma-w_i)/q_s` while
the target load is at least gamma. If the target overflowed after receiving
i, its old load would exceed `gamma+(gamma-w_i)/q_u`, which is at least
`gamma+(gamma-w_i)/q_s`, contradicting strict improvement.

Every frozen heavy client is stable in any box: its source external cost is
at most `gamma+(gamma-w_i)/q_s<=gamma`, while every alternative occupied
site has normalized load at least gamma. Frozen single-option clients have
no site alternative. Thus only X,Z,T need to be checked in this component.

## Correctness of Step 1

Initially Z has external cost `c/r` at C and sees load gamma at A, so it
moves precisely when the move is strict. This is an equal-multiplicity move
and preserves the box. After moving, Z's external cost at A is gamma, at
most C's load `c/r>gamma`; if it did not move, its external cost `c/r` is
at most A's load gamma. Hence Z is stable immediately after Step 1.

At this state the only possible strict moves are

```
T: d/Q > M/p,
X: K/p > A0.
```

## Correctness of Step 2

The strict T move implies `d>Q M/p>=Q gamma`. From
`d+t<=(Q+1)gamma`, it follows that `t<gamma`. Also

```
M+t < (p/Q)d+t
    <= p(Q+1)gamma/Q + (1-p/Q)t
    <= (p+1)gamma.
```

The final inequality uses `p<=Q` and `t<gamma`; the first inequality is
strict even when `p=Q`. B's maximum possible total over all choices of X,T
is now bounded by `(p+1)gamma`. D's maximum is its original `d+t`, and
C's maximum is its original `c+z`.

Continue any strict site moves. Moves X:B->A and T:D->B descend in
multiplicity and therefore preserve the boxes. Moves Z between A,C have
equal multiplicity. A return X:A->B respects B's upper box by the bound
`M+t<=(p+1)gamma`. A return T:B->D respects D's upper box by
`d+t<=(Q+1)gamma`. Every strict move preserves all lower bounds, so the
whole suffix stays in the box.

## Correctness of Step 3

Now X strictly moves B->A, so `K/p>A0`. Freeze X at A.

If Z was moved to A, X's future source external load is at most
`gamma+z/r=A0`; B's load is always at least `K/p>A0`, regardless of T.
Thus X can never improve by returning B.

If Z was left at C, `c/r<=gamma`, so it remains stable forever: A's load
is always at least gamma, and Z's external cost at C is the constant c/r.
Freeze Z at C. Then X's external load at A is gamma=A0, again strictly
below B's load.

Allow strict moves of the remaining unfrozen Z,T. Z's moves have equal
multiplicity, and T:D->B descends; these preserve the upper boxes. A return
T:B->D cannot exceed the original D total `d+t<=(Q+1)gamma`.
All lower boxes survive. Frozen X and all frozen heavy clients remain
best responses throughout.

## Termination and exact equilibrium

The exact site-uniform weighted potential

```
P = sum_s (W_s^2 - sum_{i assigned s} w_i^2)/(2q_s)
```

changes under i:s->u by
`w_i[W_u/q_u-(W_s-w_i)/q_s]` and strictly decreases at each move. Only
three binary-option clients can move, so there are at most eight assignments
and at most seven strict moves on the entire path. At termination every
unfrozen client is stable, and the preceding arguments certify every frozen
client. Within-site independent uniform mixing makes all co-located facilities
indifferent. This is the exact independent-mixed customer NE of MF-MODEL.

All arithmetic is rational addition and comparison with input-bit-polynomial
length. Seven moves per component give an explicit polynomial bound without
using finite-state termination as an unbounded iteration estimate.

## Existing finite instance and scope

The repository's escape input already has a strict instance of this class:
its light component is D--B--A--C with Q=3,p=2,r=1, gamma=80,
T=52, X=32, Z=40; Y=96 is frozen at B. Its initial A total is gamma.
Step 1 moves Z to A; neither X nor T then improves, producing the known
good box NE. The unequal edge weights exclude the uniform-light condition,
the four-site path excludes the star condition, and its converging direction
excludes the consistently directed path condition.

This lemma requires one light client per edge and the tight initial lower
box at A. It does not imply all trees, all converging paths, or general box
NE existence. The original bad exact NE at this same occupancy still has
its forced mixed off-path threat; this constructor chooses another NE.

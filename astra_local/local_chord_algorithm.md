# Deterministic polynomial construction for the exact strong cross-chord criterion

Research note, 2026-09-30. This note does not edit the main manuscript. It replaces the only apparently non-polynomial operation in `strong_cross_chord_arbitrary_n_proof.md` by a finite exchange algorithm with a weight-independent polynomial bound.

## 1. Result and scope

Put \(q=(\sqrt5-1)/2\). Given binary rational reaches \(R\ge r>\phi R/2\), positive common-customer weights \(w_1,\dots,w_n\), and \(C=\sum_iw_i<qr\), one can in deterministic polynomial time either:

* construct an independently mixed customer Nash equilibrium with \(L_R\ge qr\) and \(L_r\ge qR\); or
* certify impossibility by a largest weight \(x\) satisfying \(x>R-qr\) and \(C-x<R-r\).

Thus the existence test remains a linear scan, and the positive case now has an explicit polynomial-time witness construction. A conservative implementation uses \(O(n^4)\) exact rational arithmetic operations and polynomial bit complexity. This is a local two-location result. It neither computes the general minimum-equilibrium-load function \(m(s,t)\) nor asserts a polynomial-time algorithm for the full facility game.

The new step is the polynomial construction of a vertex with the precise exchange inequalities needed in the strong-chord proof. Pure maximum-weight repair is established load-balancing machinery, not a new result.

## 2. A general box-slice exchange lemma

Let \(v_1,\ldots,v_m>0\), let \(|t|\le\sum_i v_i\), and define

\[
P=\{c\in\mathbb R^m:-v_i\le c_i\le v_i,\ \sum_i c_i=t\},
\qquad F(c)=\sum_i c_i^2.
\]

A vertex of \(P\) has at most one interior coordinate. Call its index \(j\), its weight \(z=v_j\), and its value \(d=c_j\). If there is no interior coordinate, \(F=\sum_i v_i^2\) is already globally maximal and the algorithm stops.

For every other index \(i\), write \(v=v_i\) and \(c_i=sv\), \(s\in\{-1,1\}\). Holding their sum \(b=d+sv\) fixed, the feasible pair is the segment

\[
c_j=u,\quad c_i=b-u,\qquad
u\in[\ell,h]:=[\max(-z,b-v),\min(z,b+v)].
\]

The current \(d\) is an endpoint. Inspect the opposite endpoint. If it strictly increases \(F\), replace the pair by that endpoint and restart the scan. Fix the input order for deterministic tie breaking. If no pair improves, stop.

### Pseudocode

```text
PAIR_VERTEX(v, t):
    c_i := -v_i for all i
    fill := t + sum_i v_i
    for i in input order:
        h := min(2v_i, fill)
        c_i := c_i + h; fill := fill - h
    loop:
        if all |c_i| = v_i: return c
        j := unique i with |c_i| < v_i
        for i != j in input order:
            b := c_j + c_i
            lo := max(-v_j, b-v_i)
            hi := min( v_j, b+v_i)
            u := the endpoint of [lo,hi] different from c_j
            if u²+(b-u)² > c_j²+c_i²:
                (c_j,c_i) := (u,b-u)
                restart loop
        return c
```

The empty-dimensional case is allowed: it has the unique feasible point if \(t=0\).

### Feasibility and vertex invariant

Only two coordinates change, their sum is preserved, and the new pair is a segment endpoint. At least one of these two coordinates is at a bound. Every other coordinate was already at a bound. Therefore every iterate is feasible and has at most one interior coordinate. No numerical tolerance or infinitesimal perturbation is required.

### Polynomial termination

There are two possible nonterminal moves.

**A. The pivot changes from weight \(z\) to weight \(v\).** If the old pure coordinate was \(+v\), the old pivot reaches \(+z\), and the exact gain is

\[
2(z-d)(z-v).
\]

If it was \(-v\), the old pivot reaches \(-z\), and the gain is

\[
2(z+d)(z-v).
\]

The factors \(z\pm d\) are strictly positive. Thus a strict gain implies \(v<z\). The pivot weight strictly decreases whenever its identity changes. There are at most \(m-1\) such changes, even with equal input weights.

**B. The pivot does not change.** The other coordinate flips from \(sv\) to \(-sv\), and

\[
d'=d+2sv,\qquad |d'|>|d|.
\]

Fix a maximal phase with a single pivot. Throughout the phase \(|d|\) strictly increases. If a flip reverses the nonzero sign of \(d\), its weight satisfies

\[
v>|d|,\qquad |d'|=2v-|d|>v.
\]

Consequently the weights used for consecutive sign reversals strictly increase: a later reversal requires weight larger than the current \(|d|\), which already exceeds the previous reversal's weight. There are at most \(m-1\) sign reversals in the phase.

Between sign reversals, each nonpivot coordinate flips at most once. A nonreversing improving flip has \(s\) aligned with the sign of \(d\); afterwards that coordinate is opposed to the unchanged sign and cannot make another nonreversing improving flip. If the phase starts at \(d=0\), its first flip establishes a sign and is charged to the first segment. A strict improving flip never returns to zero.

There are therefore \(O(m^2)\) flips per pivot phase and at most \(m\) phases. The total is \(O(m^3)\) moves; scanning at most \(m-1\) candidate edges per move costs \(O(m^4)\) arithmetic operations. A terminal all-bound point can add only one final move. The argument is independent of the magnitudes and separations of the rational weights.

### The output supplies every inequality used in the chord proof

Assume the output has an interior pivot \((z,d)\). On every pair segment the objective is convex. Because its other endpoint has no larger value, no point of the segment has larger value. The directional derivatives therefore give

\[
c_i=+v\Rightarrow d\le v,
\qquad c_i=-v\Rightarrow d\ge -v.
\tag{2.1}
\]

When \(d>0\), the output also satisfies

\[
c_i=+v\Rightarrow v\ge z,
\qquad c_i=-v,\ v<z\Rightarrow v\le d.
\tag{2.2}
\]

For the first statement, if \(2v\ge z-d\), moving the pivot to \(+z\) is feasible and has gain \(2(z-d)(z-v)\); if \(2v<z-d\), flipping \(+v\) to \(-v\) has gain \(4v(d+v)>0\). Thus \(v<z\) is impossible. For the second statement, if \(2v\ge z+d\), moving the pivot to \(-z\) gives the forbidden gain \(2(z+d)(z-v)>0\); otherwise the full flip has gain \(4v(v-d)\), forcing \(v\le d\).

For \(d<0\) the signs reverse: pure negative coordinates have weight at least \(z\), and positive coordinates below \(z\) have weight at most \(-d\).

These are exactly the four exchange comparisons in the original maximum-square proof. Every proposed move above is the opposite endpoint of one of the segments inspected by the algorithm. Equal-gain moves need not be performed; all conclusions are weak inequalities at equality.

### A necessary distinction: the algorithm does not find a global maximizer

The independent audit found the following explicit counterexample. Let the three remaining weights be \((14,13,19)\), with target \(-10\). The greedy vertex \((14,-5,-19)\) already has no strictly improving pair edge, and its objective is \(582\). The feasible vertex \((-14,-13,17)\) has objective \(654\). Both statements can be checked by inspecting the two edges at the first vertex. This example even embeds into the strong-chord regime by adding a largest customer of weight \(19\) and setting \(R=120,r=110\). The weaker output is sufficient because the proof only requires (2.1), (2.2), and their sign reversal. This example rules out describing the subroutine as an efficient global convex-maximization algorithm.

## 3. From this vertex to a customer equilibrium

Normalize \(R=1\), set \(\delta=1-r\), and choose a largest common weight \(x\). The coordinate of customer \(i\) is \(c_i=w_i(2p_i(A)-1)\), and the expected load gap is

\[
\Delta=\delta+\sum_i c_i.
\]

If \(C-x\ge\delta\), call `PAIR_VERTEX` on all customers other than \(x\), with target \(-\delta\).

* At an all-bound output, set \(c_x=0\). The load gap is zero; the largest customer uses probability \(1/2\), and every pure customer is stable.
* Otherwise let \((z,d)\) be its unique interior pivot, and set \(c_x=d\). Since \(x\ge z>|d|\), both designated customers mix, and the load identity gives \(\Delta=d\). Conditions (2.1) prove every pure customer's stability. Both mixed customers satisfy their indifference condition \(c_i=\Delta\).

The probabilities are explicitly \(p_i(A)=(1+c_i/w_i)/2\). They are independent individual probabilities; no grouping or correlated randomization occurs.

If \(C-x<\delta\), the polytope is not used. When \(x\le1-qr\), fix \(x\) at \(B\), start the others at \(A\), and repair the remaining pure game. Customer \(x\) remains stable because its worst possible reverse load advantage is below \(x\). The existing strong-chord argument proves the quota bounds. If also \(x>1-qr\), the exact-iff obstruction applies and the unique equilibrium is the pure profile with loads \((1-x,r-(C-x))\).

## 4. Complete remaining construction and global-optimum dependency audit

Write

\[
V=1+r-C,\quad U=V-2q,\quad Z=V-2qr.
\]

The quota interval is \(-Z\le\Delta\le U\). If the equilibrium from Section 3 is in this interval, return it. Otherwise apply precisely the following finite choices from the existing proof.

### Bad positive gap \(d>U\)

By (2.2), a pure \(A\) customer would imply \(C\ge\delta+5d\), which contradicts the numeric bounds in the strong-chord regime. Thus all other customers are at \(B\), with total \(\delta+d\). Call their weights at least \(z\) large; every other weight is at most \(d\).

1. If a nonlarge weight \(v\in[d/3,d]\) exists, mix it together with \(x,z\), use gap \((d-v)/2\), and leave every other customer at \(B\).
2. Otherwise all nonlarge weights are below \(d/3\). If there is no large customer, sort these weights decreasingly and take the prefix of total \(T<d\) immediately before the first running total at least \(d\). If the prefix has \(m\) customers, mix the prefix together with \(x,z\), use gap \((d-T)/(m+1)\), and leave all others at \(B\).
3. If there is exactly one large customer \(y\), and the other small total \(T\) satisfies \(\delta+T\le2z\), mix \(x,y,z\) at gap \(-(\delta+T)/2\) and put the small customers at \(A\).
4. In every remaining branch the original algebra yields \(d\le\delta\). Put \(x\) at \(A\), all others at \(B\), and run pure repair.

In the first three branches there are at least three designated mixers; the mass estimates in the original proof ensure both quotas, including when a designated probability is an endpoint. In branch 4 the initial and subsequent pure loads satisfy the same quota-preservation argument as the original proof.

### Bad negative gap \(-e<-Z\)

The sign-reversed (2.2) makes every other customer pure \(A\), with total \(e-\delta\).

1. If any such weight \(v\ge e/3\) exists, mix it with \(x,z\), use gap \(-(e-v)/2\), and keep all others at \(A\).
2. Otherwise put \(x\) at \(B\), all others at \(A\), and run pure repair.

The negative-gap calculation in the exact strengthening proves \(x<1-qr\) in this branch even without a maximum-weight hypothesis. Thus the original target-preservation argument applies verbatim.

### Audit table

| Original use | What is actually required | Supplied here |
|---|---|---|
| Section 2: NE of the pivot construction | Pair directional inequalities | (2.1) |
| Section 2: pure weights versus pivot | Four full-segment endpoint comparisons | (2.2) and its sign reversal |
| Section 3: bad positive gap has no pure A customer | Pure A weights at least z | (2.2) |
| Section 3: all nonlarge B weights at most d | The second positive exchange inequality | (2.2) |
| Section 4: bad negative gap has no pure B customer | Pure B weights at least z | Sign reversal of (2.2) |
| Section 4: tiny weights before pure repair | Explicit case split, no optimization | Unchanged |
| Section 5: exact iff without max-weight bound | Dominance and displayed mass inequalities | Unchanged |

After the Section 2 exchange inequalities, the original Sections 3–5 do not compare objective values again. They use only the load identity, \(x\ge z\), these local exchange inequalities, the regime bounds, and explicit case choices. Consequently global optimality of \(F\) is unnecessary throughout.

## 5. Pure repair has a polynomial bound

This paragraph is included to avoid replacing one finite-but-unbounded subroutine by another. Under a strict pure improvement of weight \(w\) from the higher-load location, the absolute gap \(g>0\) changes to \(|g-2w|<g\). At a sign reversal, the new gap is below \(w\); that moving customer is therefore permanently stable. At most \(n\) sign reversals can occur. Between reversals, every customer moves from the current high side to the low side at most once. Thus **any** strict pure repair sequence takes \(O(n^2)\) moves for two locations, also with fixed private base loads.

For the implementation one may choose the largest improving customer each time and get at most \(n\) moves. Before a reversal the set of improving customers on the high side can only shrink, so chosen weights are nonincreasing. After a reversal the new absolute gap is below the last chosen weight; every customer moved so far has at least that weight and is permanently stable. The next chosen weight is smaller, and induction proves that every customer moves at most once. Scanning for the largest improving customer costs \(O(n^2)\) arithmetic operations overall.

The maximum-weight rule and its \(n\)-move convergence for identical-machine load balancing are prior work: Even-Dar, Kesselman, Mansour, *Convergence Time to Nash Equilibria*, ICALP 2003, Theorem 8 in the authors' manuscript; expanded journal article *Convergence Time to Nash Equilibrium in Load Balancing*, ACM TALG 3(3), article 32 (2007), DOI 10.1145/1273340.1273348. The private-base two-location proof above is supplied explicitly. Vos 2023 Lemma 29 already supplies the special quota-preserving repair used in the facility manuscript.

Primary sources consulted:

* https://www.math.tau.ac.il/~mansour/course_games/nash-load.pdf (Theorem 8, manuscript p.10; also notes prior observation in its reference [26]).
* https://cris.tau.ac.il/en/publications/convergence-time-to-nash-equilibrium-in-load-balancing/ (journal metadata).
* https://essay.utwente.nl/fileshare/file/96484/Vos_MA_EEMCS.pdf (Lemma 29 and Chapter 8).

The local box-slice construction above is proved here. A limited literature search did not locate this exact lemma; it does not establish that the lemma itself is new. General convex quadratic minimization on a box slice is a different optimization direction and does not justify maximizing this objective efficiently.

## 6. Exact arithmetic and implementation

`construct.py` provides the full construction, not support enumeration. It uses Python `Fraction` throughout. A rational number \(u\) is compared with \(q\) by its sign and the sign of \(u^2+u-1\). All comparisons with golden-ratio thresholds reduce to such tests; no floating approximation to \(q\) occurs.

Every exchange coordinate is either an input endpoint or \(t\) minus a signed sum of input weights. Its bit length is polynomial in the input encoding. Subsequent mixer gaps divide a signed sum by an integer at most \(n\), and final probabilities divide by an input weight. Hence all output probabilities and all intermediate exact numbers have polynomial bit length. This establishes polynomial bit complexity in addition to the \(O(n^4)\) arithmetic bound.

The executable has explicit assertions for the local exchange conditions, final NE conditions, quota conditions, pivot descent, per-move gain, and once-only maximum-weight pure repair. Its reproducible verification record is `verification.json`.

The final recorded run contains **14,646 exact-rational instances**: 12,000 seeded random cases, 2,640 valid cases from the small-integer grid, and six directed edge/branch cases. Every output branch of the implementation is exercised. In particular, the three branches missing from the original random sample are covered by:

| Branch | r (R=1) | Common weights |
|---|---:|---|
| positive prefix with more than three mixers | 0.85 | 0.16, 0.11, eight copies of 1/32 |
| positive-gap pure repair | 0.82 | 0.15, 0.095, 0.13, 0.13 |
| negative-gap pure repair | 0.985 | 0.21, five copies of 0.037, 0.202 |

The positive-repair example enters the pure branch and is already a pure equilibrium; the negative-repair example actually moves customers. The empty game, the boundary \(C-x=\delta\), the single-customer equal-reach case, and the local-versus-global counterexample are checked separately in the same script. These computations audit the implementation; the mathematical proofs above supply the universal guarantee.

## 7. Research directions for a stronger next target

1. Improve the conservative \(O(n^4)\) bound, ideally by finding a direct sorted construction of the required exchange vertex or amortizing flips across descending pivots. A better bound is useful but is not needed for polynomial constructibility.
2. Study the full attainable two-location equilibrium-load interval/set. The current subroutine answers one special two-sided quota request; it does not optimize an arbitrary linear facility objective over NE.
3. Combine this subroutine with exact or parameterized methods for \(m(s,t)\) and \(d(t)\). The remaining global computational difficulty lies there, not in the strong-chord existence witness.
4. Check whether the same exchange stopping conditions suffice for other ratios or overlaps. The vertex lemma is valid for arbitrary positive weights and feasible targets; the golden-ratio assumptions enter only when repairing a quota-violating equilibrium.
5. The local result extends to a common quadratic realized-congestion function \(f(z)=az^2+bz+c\) whenever \(a(W+w_i)+b>0\) for each relevant customer: for a fixed realization of all other choices, its two alternative realized load arguments sum to \(W+w_i\), so their quadratic cost difference is this positive constant times their linear load difference. Taking expectations preserves every best-response comparison and hence the entire mixed-NE set. This extension is independently derived by the applications agent and is recorded here only as an interface observation.

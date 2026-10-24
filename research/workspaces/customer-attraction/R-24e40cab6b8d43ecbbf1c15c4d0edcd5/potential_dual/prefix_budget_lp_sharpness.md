# Exact sharpness of the all-prefix fractional-cover budget

**Status (2026-10-24).** General-purpose obstruction for one potential/dual
route; Q-CAG-HALF remains OPEN. This note concerns only the already proved
prefix inequalities and does not construct a game counterexample.

Fix (m\ge2), a complete pure SPE, a comparison union (C) of size (O),
and actual terminal payoffs (u_i\ge0). Write
(P_i=\sum_{j\le i}u_j) and (r_i=m-i+1). Taking the comparison themes
with unit weights in the true prefix argument gives, for every position (i),

\[
 O\le P_{i-1}+m r_i u_i. \tag{PB}
\]

The linear system consisting of (u_i\ge0), \(\sum_i u_i=W), and all rows
(PB) has an exact extremal value:

\[
 \inf W/O
 =F_m(m):=1-\prod_{r=1}^m\left(1-\frac1{mr}\right). \tag{1}
\]

Thus the whole family of prefix rows alone implies only

\[
 W\ge F_m(m)O,
\]
which is below (O/2) for every (m\ge4). No nonnegative linear
combination of these rows, nor a scalar potential whose only certified rows
are (PB), can close Q-CAG-HALF for unbounded (m).

## Proof of exact LP value

Normalize (O=1). For any target (W), the least prefix mass compatible
with (PB) is obtained by taking each row tight. With (D_i=1-P_i), row (i)
requires

\[
u_i\ge\frac{D_{i-1}}{m r_i}.
\]

Since (m r_i\ge2), the choice on the right keeps (D_i>0), so no
nonnegativity truncation is active. Consequently

\[
D_i=D_{i-1}\left(1-\frac1{m r_i}\right),\qquad D_0=1,
\]

and therefore

\[
P_m=1-D_m
 =1-\prod_{r=1}^m\left(1-\frac1{mr}\right)=F_m(m).\tag{2}
\]

This sequence is feasible and has total mass (F_m(m)), proving the upper
bound on the LP infimum. Conversely, induction gives
(D_i\le D_{i-1}(1-1/(mr_i))) for every feasible sequence, hence
(D_m\le\prod_r(1-1/(mr))) and (W=P_m\ge F_m(m)).

For (m=4),
\[
F_4(4)=1-(15/16)(7/8)(11/12)(3/4)=893/2048<1/2.
\]
As (m\to\infty),

\[
F_m(m)=1-\exp\!\left(-\frac{H_m}{m}+O(m^{-2})\right)
\sim H_m/m\to0.
\]

## Interpretation and boundary

The tight sequence is an abstract payoff vector, not asserted to be realized
by a CAG SPE. It proves a precise method boundary: the already established
true-prefix inequalities carry no hidden half factor, even when every prefix
position is used simultaneously. To obtain (2W\ge O), a new row must use
additional information: genuine cross-branch continuation credit, a
customer-level incidence constraint, or another non-prefix relation. Calling
the product recurrence a potential proof would silently assume such a row.

The argument is independent of tie-breaking, does not identify ordered
histories, and does not claim that Q-CAG-HALF is false.

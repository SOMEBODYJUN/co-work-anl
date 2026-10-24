# Static insertion versus true continuation debt

**Status (2026-10-24):** exact general reduction, not a proof of Q-CAG-HALF.
The statement below keeps the fixed complete ordered-history pure SPE and all
of its true post-deviation continuations.  It isolates one remaining scalar
obligation that would be sufficient for the half bound.

## Setup

Let the actual terminal profile be (z=(A_1,ldots,A_m)), with customer
loads (c_x), actual utilities (u_i), welfare (W=sum_i u_i), and actual
covered set (A=igcup_iA_i).  Fix any optimal comparison tuple
(T_1,ldots,T_m), and write (O=|igcup_iT_i|).  Set

\[
 f_c(T)=\sum_{x\in T}\frac1{c_x+1},\qquad
 \delta_i(T)=\sum_{x\in T\cap A_i}\frac1{c_x(c_x+1)}.
\]

If player (i) switched to (T) while every later action were frozen at its
actual action, the resulting payoff would be

\[
 q_i(T)=f_c(T)+\delta_i(T).
\]

Indeed, for (x\in T\setminus A_i) the other actual providers contribute
(c_x), giving (1/(c_x+1)); for (x\in T\cap A_i) the switch removes and
re-adds (i), so the other load is (c_x-1), giving (1/c_x).

Let (d_i(T)) be the payoff from the *true* SPE continuation after forcing
(T) at the actual prefix before (i).  Define the continuation (retaliation)
debt

\[
 R_i(T)=q_i(T)-d_i(T).
\]

SPE optimality at the actual history gives (u_i\ge d_i(T)), hence

\[
 f_c(T)\le u_i+R_i(T)-\delta_i(T). \tag{1}
\]

## Exact coverage accounting

Define

\[
 V=\sum_{x\in A}\frac1{c_x+1}.
\]

For every customer (x) in the comparison union, let (e_x) be its number
of occurrences among (T_1,ldots,T_m).  Its contribution to
(W-V+\sum_i f_c(T_i)) is (1-1/(c_x+1)+e_x/(c_x+1)) when (c_x>0), and
(e_x) when (c_x=0).  Since (e_x\ge1), this is at least one.  Therefore

\[
 O\le W-V+\sum_{i=1}^m f_c(T_i). \tag{2}
\]

Substituting (1), and using (sum_i u_i=W), yields the exact dynamic
debt inequality

\[
 \boxed{
 O\le 2W-V-\sum_i\delta_i(T_i)+\sum_iR_i(T_i).
 } \tag{3}
\]

Consequently the original half target follows from the single general
cross-branch obligation

\[
 \boxed{\sum_iR_i(T_i)\le V+\sum_i\delta_i(T_i).} \tag{4}
\]

Here (R_i) is exactly the loss caused by allowing the true continuation to
react to the deviation, while (V+sum_i\delta_i) is the available harmonic
insertion credit.  Formula (3) never freezes a continuation and never treats a
branch payoff as a root-path payoff.

## Scope and current boundary

The identity is valid for arbitrary finite common catalogs, arbitrary (m),
empty/repeated themes, zero customers, all ordered histories and arbitrary
history-dependent pure SPE ties.  It does **not** assert (4).  Existing
Cartesian-product reset examples show that local slack terms and pairwise
nonnegative caps do not by themselves imply (4): the missing term is a signed
membership/tail-share covariance across different true branches.  Any proof
of (4) must therefore supply a genuinely cross-branch flow or another global
credit, and cannot double-count (V) or the (delta_i)'s.

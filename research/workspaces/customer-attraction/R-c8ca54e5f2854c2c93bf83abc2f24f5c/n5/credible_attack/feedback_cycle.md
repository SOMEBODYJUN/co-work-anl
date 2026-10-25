# Actual last replies create a feedback constraint

2026-10-25. Original CAG-MODEL, five providers, arbitrary finite common
catalogue and complete ordered-history pure SPE. The half claim remains OPEN.
This note records a valid conditional inequality and a narrow exact exclusion;
it does not provide an actual counterexample or a universal half proof.

## 1. A legal inequality at a genuine two-player tail

Fix any ordered history h of length three and its complete SPE continuation.
Let b_x be the number of earlier providers covering customer x. For each legal
catalogue topic S define

    R(S) = sum_(x in S) 1/(b_x+1).

Let d be the fourth provider's actual final utility in this subgame. Write
f(S) for the actual fifth-provider action after history (h,S), preserving all
history-dependent ties. For every S,

    q(S) = u_S(h,S,f(S)) <= d.                         (1)

Take any five legal comparison topics T_1,...,T_5, with repetitions allowed,
and put O = union_i T_i. Suppose for some i and legal V the actual reply map
has the two-cycle

    f(T_i)=V,  f(V)=T_i.

Both providers' utilities in the common terminal (h,T_i,V) are at most d by
(1). Denote them by u_T and u_V. Two identities/inequalities suffice:

    u_T-u_V = R(T_i)-R(V),                            (2)
    4u_V >= R(O \ T_i).                              (3)

For (2), a customer in both topics contributes equally; a customer in only
one contributes 1/(b_x+1). For (3), after the fourth provider chooses T_i,
the actual last best reply V is compared separately with every T_j, j!=i.
Every customer in O\T_i is covered by at least one of those comparison
topics and has no fourth-provider background. All other contributions are
nonnegative. Summing the four genuine best-response inequalities gives (3).
No disjointness, anonymous ties, or optimality of the comparison tuple is used.

Because T_i is contained in O, (2)+(3) gives the conditional full-tree row

    4d >= u_T+3u_V >= R(O)-R(V).                     (FB)

The first displayed relation means 4d>=u_T+3u_V, followed by the lower bound.
The conditioning is substantive: an arbitrary last best reply to T_i need not
be the branch used after V, and then its last-player utility need not be <=d.
One cannot append (FB) to a histogram-only relaxation without recording and
justifying the relevant actual reply identities.

## 2. Directed cycles of any length

The two-cycle condition can be weakened to: T_i lies on a directed cycle of
the actual last-reply map f. This includes a self-loop.

Let Phi be the usual exact harmonic potential, and define the symmetric matrix

    P_AB = Phi(h,A,B)-Phi(h).

A last best reply f(A) maximizes P_AB over B. If
A_0 -> A_1 -> ... -> A_(k-1) -> A_0 is a directed cycle, symmetry and the
row-maximality inequalities imply

    P_(A_i,A_(i+1)) >= P_(A_i,A_(i-1)).

The right edge is the preceding left edge. Around the finite cycle all these
inequalities must be equalities, so every selected cycle-edge value is one
constant C. A provider choosing A_i first on its prescribed branch receives
C-R(A_(i+1)); by (1) this is <=d. Consequently at every selected cycle edge
(A_i,A_(i+1)), *both* endpoint utilities are <=d: the other endpoint utility
C-R(A_i) is the prescribed first-player utility at its predecessor's edge.
For a self-loop the two utilities are equal. Applying the proof of (FB) to
the cycle edge starting at T_i therefore gives (FB) with V=f(T_i).

This is a conditional general statement about the actual complete strategy.
Every finite reply map has a cycle, but the cycle need not contain one of the
five comparison topics. No such membership is assumed without evidence.

## 3. Unconditional reply-of-reply row

The conditional row has an unconditional version if one more actual reply
identity is retained. At the same genuine two-player tail, take

    A=T_i,  B=f(A),  C=f(B).

Last optimality after B and symmetry give P_BC>=P_BA=P_AB. Therefore

    u_B(h,A,B) = P_AB-R(A)
                <= P_BC-R(A)
                = q(B)+R(C)-R(A)
                <= d+R(C)-R(A).                       (4)

The proof of (2)+(3) still gives

    u_A(h,A,B)+3u_B(h,A,B) >= R(O)-R(B).

Combining this with q(A)<=d and (4) yields the valid **unconditional** row

    4d >= R(O)-R(B)-3R(C)+3R(A),
    A=T_i, B=f(T_i), C=f(f(T_i)).                       (FF)

All topics and replies in (FF) are genuine choices in the same fixed ordered
history h. Comparison topics may overlap or repeat; f may use arbitrary ties.
This row needs the actual reply-of-reply menu C, which a template retaining
only (T_i,f(T_i)) does not supply. It may be included in a richer atom LP by
recording those additional identities; it cannot be asserted with C chosen
independently to make the right side large.

An explicit nonnegative certificate for (FF) is available. Put

    I_A=d-u_A(h,A,B), I_B=d-u_B(h,B,C),
    L=P_BC-P_AB,
    K=4u_B(h,A,B)-sum_(j!=i) u_(T_j)(h,A,T_j),
    H=sum_(j!=i) u_(T_j)(h,A,T_j)-R(O\A).

Every I and L is a genuine SPE incentive/best-response slack, K is the sum
of four genuine last-player BR slacks, and H is pointwise nonnegative. Exact
algebra using the swap identity gives

    4d-R(O)+R(B)+3R(C)-3R(A) = I_A+3I_B+3L+K+H.

Thus this new row requires no optimization to certify. The corresponding
all-five identity uses multipliers 1,4,4 and the five-row K. The independent
small coefficient audit `audit_feedback_identity.py` enumerates all 512
membership/background patterns for (FF) and all 1024 for (FF5), with original
three-provider prefix background 0,...,3; both exact identities and H>=0 pass.
It is a coefficient audit, not an equilibrium search or a general half proof.

For an arbitrary legal A, compare the last reply B against all five T_j.
The same argument instead gives

    5d >= R(O union A)-R(B)-4R(C)+4R(A).                (FF5)

Indeed five BR comparisons bound 5u_B below by R(O\A), and adding the
swap identity gives u_A+4u_B>=R(O union A)-R(B).

A globally largest residual topic A satisfies R(C)<=R(A), so both utilities
in (h,A,f(A)) are <=d. Thus (FF) reduces to (FB) when such an A is one of
the comparison topics, and (FF5) gives 5d>=R(O union A)-R(B) in general.
The same simplification applies whenever the local two-step condition
R(f(f(A)))<=R(A) holds. This condition is not automatically true for every
comparison topic.

## 4. An exact exclusion for one attempted lift of the old 64-atom point

The frozen source is
`evidence/certificates/customer_attraction/five_player_indexed_bound.json`.
Keep its 64 atoms, exact masses, and fixed `ABCDEUVWXY` memberships. Every
source atom has optimal multiplicity d=1. Thus any lift into five actual
comparison topics T_0,...,T_4 partitions its customers among these topics.
The desired path is ABCDE. This source has comparison coverage >2 times
that path's welfare; it is only a necessary-condition point, not an SPE.

The attempted lift considered here uses the *same actual T_0* as the fifth
provider's reply after each of the fourth-provider deviations

    E, V, W, X, Y

at the prefix ABC. The theorem below excludes exactly that mechanism, for
all customerwise assignments to the five T topics; it does not exclude other
reply-identity partitions or other masses/catalogues.

**Narrow exclusion.** No such lift supports the path ABCDE in a complete SPE.

To verify, let x_k in [0,1] be the fraction of old atom k assigned to T_0.
The other four topics have total fraction 1-x_k. For necessary inequalities
involving only T_0 and fixed topics, their four comparisons can be averaged;
this preserves the exact total and loses no necessary condition used here.
The code imposes:

* each individual on-path guaranteed deviation floor for T_0, and the average
  of the corresponding four floors for the other T topics;
* genuine last best-response comparisons after the five listed fixed
  deviations, and each resulting fourth-provider incentive comparison;
* after a fourth-provider deviation to T_0, its chosen last reply's genuine
  comparisons with all fixed topics, T_0 itself, and the average of the four
  other T topics, together with the fourth-provider incentive comparison.

There are eleven cases for the last reply after T_0: each of the ten fixed
labels or a copy of T_0. `verify_universal_punisher.py` uses hard-coded,
nonnegative rational multipliers (two to four nonzero values per case), and
checks the weighted linear inequality coefficient by coefficient in Fraction
arithmetic. If A x <= b are the necessary rows, the certificate computes

    kappa = sum_k min(0,(mu*A)_k) - mu*b > 0.

For every x in [0,1]^64, mu*A*x >= sum min(0,mu*A), contradicting mu*A*x<=mu*b.
The smallest kappa is approximately 0.0144468142; exact fractions and all
coefficient residuals are in `universal_punisher_exact.json`.

The twelfth case is a last reply T_j, j!=0. Disjointness then leaves the T_0
first chooser its whole R(T_0). Since T_0 is assumed a last best reply after
the deviation V, it must beat the fixed reply W there. That fixed W payoff
is approximately 0.3223199962, whereas the desired D payoff is approximately
0.2957281846. Hence this case also gives a strict profitable deviation.

The V and X cases contain the general feedback row above. In the V case,
using only its genuine BR against the other four T topics plus the two
fourth-provider IC comparisons gives

    d >= (R(O)-R(V))/4.

The source violates this by approximately 0.0288936284. The common-row-
violation certificate uses half that value because its selected multipliers
are normalized to sum one. This identity is independent of the frozen masses.

The exact certificate verifies an exclusion, not feasibility. The exploratory
`joint_alignment.py` initially omitted the T_0 fourth-provider deviation and
found an apparent universal-punisher alignment. `realize_alignment.py` builds
an exact unit-customer instance from that proposal (repairing one equality)
and its canonical all-SPE prefix audit rejects ABCDE at ABC. That failure
motivated the general feedback identity; it is not counted as a counterexample.

Reproduce the exact exclusion without running an optimizer:

    python research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5/credible_attack/verify_universal_punisher.py

No general half theorem, unrestricted five-provider counterexample, or full
frozen-support alignment exclusion has been obtained in this subtask.

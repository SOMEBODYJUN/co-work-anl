# A precise all-history approximate-IC boundary and a regret-aware product bound

2026-10-24. General-input working result, not independently reviewed and without
a novelty claim. Q-CAG-HALF remains OPEN. No main-question counterexample or
new half-coverage range is claimed.

## 1. Scope and the exact stability contract

Use CAG-MODEL: an arbitrary finite common catalogue, unit customers and unit
players, arbitrary player count m, and complete pure plans on all ordered
histories. A plan below is **not assumed to be an SPE**.

For a complete plan tau, history h of length i-1, prescribed leaf z_h, and
true forced leaf z_(h,T) obtained by choosing T now and then using the same
tau, put

    R_tau(h) = max_(T in S) [u_i(z_(h,T))-u_i(z_h)].

The prescribed action is included, so this maximum is nonnegative. Define

    e_i = max_(|h|=i-1) R_tau(h),
    B(tau) = sum_(i=1)^m e_i.                            (N)

This norm pays the worst defect at **every depth over all ordered histories**;
it is at least the sum of actual-path defects. It does not merely test the
actual path. It still evaluates each deviation using tau's own continuation.

The precise stability candidate attacked here is: there exists an absolute
constant C>=0, independent of m, the catalogue, and the customer set, such
that every complete plan satisfies

    OPT_m <= 2 W(tau) + C B(tau).                       (S?)

The family in Section 2 disproves this contract, even when the last player's
plan is a best reply at **every** history. This is not a counterexample to
Q-CAG-HALF, whose complete plans must satisfy R_tau(h)=0 everywhere. The
family is also not asserted to arise by deleting a player from an SPE.

## 2. An arbitrary-m complete-plan family

Fix m>=2 and an integer q>=0. There are m pairwise distinct petal customers
p_1,...,p_m and a common core Q of q distinct customers. The common catalogue
has exactly the m themes

    A_a = Q union {p_a},       a=1,...,m.

Define tau on every ordered history as follows.

1. At the root, choose A_1.
2. At positions 2,...,m-1, choose the theme chosen immediately previously.
3. At position m, choose the least-label theme whose petal has never been
   chosen previously.

The last rule is always legal: a history of length m-1 has used at most m-1
distinct petals, while the catalogue has m. Its private-petal payoff is 1;
every previously used petal gives at most 1/2. Every action gives the same
common-core payoff q/m, so the last rule is a best reply at every history.

The actual leaf is

    A_1^(m-1), A_2,

and therefore

    W = q+2,               OPT_m = q+m.                (F1)

For m=2 the two displayed themes are simply A_1,A_2. The m available actions
can cover all m petals, proving the stated optimum exactly.

### All ordered histories and all true deviations

Fix a middle position 2<=i<=m-1, let r=m-i+1, and let t be the number of
previous occurrences of the immediately previous theme. Thus

    1<=t<=i-1=m-r.

If the current action is any theme A_a with previous count b_a, then all
positions through m-1 repeat A_a and the final player selects a fresh petal.
The current player's **true** final payoff under this forced branch is

    q/m + 1/[b_a+r-1].                                 (F2)

An unused petal exists, so the maximum over a occurs at b_a=0. The prescribed
branch uses b_a=t. Hence

    R_tau(h) = 1/(r-1)-1/(t+r-1)
             <= 1/(r-1)-1/(m-1).                      (F3)

Equality holds at a history in which every past action is A_1. Such a
history is legal at every depth, and is the actual history here. At the
root all forced actions are repeated through m-1 and then avoided by the
last player, so every root action gives q/m+1/(m-1) and root regret is zero.
Last-position regret is zero by the preceding BR proof. Consequently,

    e_i = 1/(m-i)-1/(m-1)       (1<=i<=m-1),
    e_m = 0,
    B(tau) = H_(m-1)-1.                                (F4)

The expression for i=1 is zero as required. This computes the maximum over
all ordered histories exactly; histories with a previous theme count one
have a larger prescribed payoff and cannot increase the defect.

### Failure of every absolute-C robust half contract

First take q=0. Equations (F1),(F4) give

    OPT_m-2W = m-4,
    (OPT_m-2W)/B = (m-4)/(H_(m-1)-1) -> infinity.       (F5)

Thus no fixed C can satisfy (S?). More quantitatively, any m-dependent
coefficient in (S?) must be at least the positive part of the ratio in (F5),
which is asymptotic to m/log m. This is a necessary condition for that exact
contract, not a characterization of all possible approximate-SPE bounds.

To make even the total all-history error small relative to the actual
welfare, take q=floor(sqrt(m)). Then

    B/W = [H_(m-1)-1]/[floor(sqrt(m))+2] -> 0,
    OPT_m/W = [m+floor(sqrt(m))]/[floor(sqrt(m))+2]
              -> infinity,                            (F6)
    OPT_m-2W = m-floor(sqrt(m))-4.

The bad difference is positive for m>=8. The limits use H_n=O(log n) and
floor(sqrt(m)) asymptotic to sqrt(m). Every customer and core multiplicity
is an integer; no vanishing customer weights are used. This disproves a
dimension-free inference from B=o(W) to any fixed coverage approximation.
It says nothing about the extra structure of a deletion replay.

## 3. What a genuine suffix reset does in this same family

Consider any ordered prefix in this common-core petal game. Every complete
pure SPE of the remaining subgame chooses a fresh petal at each remaining
position. Proof is by backward induction. The last player strictly prefers
a fresh petal's private payoff 1 to a used petal's payoff <=1/2. If all later
SPE moves choose fresh petals, then a current fresh choice is never revisited
and gives private payoff 1; a current used choice gives at most 1/2 and is
also never revisited. Fresh choices exist because there are m petals and
fewer than m actions so far. Common-core payoff q/m is independent of all
choices. This proves the assertion for every prefix and every tie choice.

For an incumbent fixed to A_a at a prefix with count b_a before its move,
all genuine successor SPE therefore give that incumbent exactly

    ell_i(A_a) = q/m + 1/(b_a+1).                      (R1)

At the actual prefixes of tau there is an unused petal, hence the genuine
exit menu maximum is

    M_i = q/m+1.

For the prefix compiler with j=m-1, the supplied suffix is exactly the
credible final BR above. For every i<=j the target payoff is
q/m+1/(m-1), so its defect is exactly

    Delta = 1-1/(m-1).                                 (R2)

In particular, the virtual-plan root regret is zero, but the genuine root
exit defect is positive for m>=3. A root deviation using the original tau
is followed by repeated petals and gives q/m+1/(m-1); a genuine SPE exit
uses fresh petals and gives q/m+1. This is the explicit continuation-reset
term that a repair argument must preserve.

This compares directly with
`R-65d0f88edf3849b39ca5eb79760e970b/credible_attack/prefix_credible_exit_compiler.md`.
That compiler uses minimum genuine SPE continuation payoffs, including the
unchanged old action when only the bank action changes. It permits an
arbitrary new credible suffix after the first deviation; it does not
preserve the virtual deletion tree. Here its half dilution at j=m-1 is

    (2m-1)Delta = (2m-1)(m-2)/(m-1).

This exceeds m-q-4 for q>=0 and m>=2, so this family does **not** cross its
counterexample threshold. There is no conflict with that compiler or the
main half conjecture.

## 4. A positive bound that needs no credibility repair

The existing exact-SPE fractional-cover prefix proof has a direct robust
version valid for every complete plan. This is a relaxation of an existing
general lemma, not a new proof of half coverage.

Fix a coverable comparison customer set C of size O and a fractional theme
cover z_T>=0 of C with total weight kappa>=1. Let actual final profits be u_i,
P_i=sum_(j<=i)u_j, and let rho_i=R_tau(h_i) be actual-path true regret. Put
r=m-i+1. The genuine forced payoff lower bound gives

    u_i+rho_i >= g_i(T)
      := sum_(x in T cap C) 1/[b_i(x)+r].

The same client counting as the existing prefix lemma gives

    O <= sum_(j<i)g_i(S_j)+r sum_T z_T g_i(T)
      <= P_(i-1)+r kappa (u_i+rho_i).                 (P1)

Only the original complete plan's true forced leaves occur here. Past
profits are evaluated at its one actual leaf. No child is called an SPE.
Rearrange to

    P_i >= (1-1/(r kappa))P_(i-1)+O/(r kappa)-rho_i.    (P2)

All recurrence multipliers are nonnegative. Iteration yields the exact
regret-weighted relation

    W >= O F_m(kappa)-sum_i w_(m-i+1)(kappa)rho_i,      (P3)

where

    F_m(kappa)=1-product_(r=1)^m(1-1/(r kappa)),
    w_r(kappa)=product_(s=1)^(r-1)(1-1/(s kappa)),
    w_1=1.

Because 0<=w_r<=1 and rho_i<=e_i, this also implies

    OPT_m <= [W+B(tau)]/F_m(m).                        (P4)

Here tau is the complete plan in norm (N), while kappa is the fractional
cover total. Formula (P4) uses the m optimal themes as a fractional cover
of total at most m. Nonempty comparison sets have kappa>=1; empty comparison
sets are trivial.

The factor 1/F_m(m) is asymptotic to m/H_m, exactly as in the old exact-SPE
lemma. The family above has cover number m and demonstrates why mere
additive-regret control does not supply a constant factor at unbounded m.
This bound can consume ASD's actual regrets directly, without repairing
the child, but its multiplicative factor is already too weak for half.

## 5. Five-player pressure test of the same general formulas

No five-player-specific row or coefficient is added. At m=5, q=0, this
family has

    W=2, OPT_5=5,
    (e_1,...,e_5)=(0,1/12,1/4,3/4,0),
    B=13/12, Delta=3/4.

The approximate plan violates half because it is not an SPE. Its root
one-step regret is zero while genuine root reset costs 3/4. For q=2 the
same errors hold and W=4, OPT=7, satisfying half; this does not affect the
general asymptotic failure.

The positive product relaxation gives, even when all errors are zero,

    F_5(5)=6049/15625,
    OPT_5 <= (15625/6049) W,

whose factor exceeds two. For deletion to four players the corresponding
factor is 1/F_4(4)=2048/893, also above two before adding error. Thus (P3)
does not pass the required general-mechanism five-player half pressure
test. Known stronger exact four-player theorems cannot be called on its
noncredible deleted plan without a separate robust theorem.

## 6. Relation to the parent's deletion components and stopping line

The parent deletion-regret envelope and ASD are special-source statements:
the complete plan comes from an actual full SPE before deleting specified
loads/roles. They additionally constrain old IC slacks and per-client refund
differences. Section 2 has not been embedded as such a deletion replay and
does not refute a theorem exploiting those extra constraints.

In fact the known all-history multiplicative guarantee already separates
this family from single-deletion replay at large m. A single-deletion replay
has best forced payoff at most twice its prescribed payoff at every
history. At our actual penultimate history the ratio is

    [q/m+1]/[q/m+1/(m-1)].

For q=0 this is m-1; for q=floor(sqrt(m)) it tends to infinity. Thus these
two sequences cannot be single-deletion replays for all sufficiently large
m. A stability theorem using both full-history factor-two approximation
and a regret budget remains a distinct open candidate; this note has not
proved or disproved it.

What is ruled out is replacing that structure by only the norm (N), then
claiming an absolute-C approximate-half stability theorem. The norm even
controls all histories, so merely upgrading actual-path ASD to same-depth
worst-history regret would still be insufficient for that contract.
The credible prefix compiler solves a different operation: replace the
old suffix by genuine complete SPEs and pay its exact exit-floor Delta.
Equations (R1)--(R2) show explicitly why the original virtual-plan regrets
do not already include that reset.

The positive component (P3) is a valid no-repair welfare transfer, but does
not improve the half frontier. No additional global induction invariant
controlling genuine suffix reset for deleted SPEs was obtained here. This
is a precise failure of the tested generic stability contract, not a claim
that deletion induction, all repairs, or Q-CAG-HALF are impossible.

Sources used: CAG-MODEL; the parent's `deletion_regret_envelope.md` and
`average_suffix_deletion.md`; the older `virtual_replay_regret.md`; the
peer `prefix_credible_exit_compiler.md`; and the established
`fractional_cover_path_budget.md`. The only finite audit below checks the
family against the definitions; the arbitrary-m proofs above do not depend
on computation.

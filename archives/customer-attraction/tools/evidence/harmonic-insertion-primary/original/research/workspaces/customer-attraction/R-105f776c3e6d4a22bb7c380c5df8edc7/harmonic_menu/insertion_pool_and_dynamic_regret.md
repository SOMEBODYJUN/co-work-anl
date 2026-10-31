# One fixed insertion pool does not pay adaptive deletion defects

2026-10-24. General sensitivity calculation and an explicit attack on one
precise general candidate. This is a working note, without independent
review. Q-CAG-HALF, H4, Mfull and Mpath remain OPEN. No welfare bound for the
main question is proved or disproved here.

## 1. The fixed-terminal common-customer budget

Fix any old integer background b, a unit inserted action A, and an arbitrary
tuple q of later unit actions. Write c_x for the tuple's load and L_x=b_x+c_x.
The inserted player's profit is

    d_A(q) = sum_(x in A) 1/(L_x+1).

For a tail player j, its loss from adding A while preserving this one tuple is

    delta_j(q) = sum_(x in A cap S_j) 1/[L_x(L_x+1)].

Only clients with c_x>0 occur in this expression, so every denominator is
positive. Hence all tail players together lose exactly

    E_A(q) = sum_(x in A:c_x>0) c_x/[L_x(L_x+1)] <= d_A(q).

The corresponding old-player loss is

    E_old(q) = sum_(x in A:b_x>0) b_x/[L_x(L_x+1)].

Consequently

    E_A(q)+E_old(q)
      = d_A(q) - |{x in A:L_x=0}|.

Each client supplies one common pool. Summing player losses does not give
each player an additional copy of d_A. This is a fixed-terminal insertion
calculation, consistent with the incumbent refunds in the existing full-depth
ledger; it is not claimed as a new conservation principle.

There is also a useful certificate form. Suppose a nonnegative weighted
collection of genuine child IC rows has prescribed and forced leaves z_e^+
and z_e^- and moving player j(e). For the same complete strategy, compare
the weighted IC sum with A present and with A removed. The exact difference is

    Sum lambda_e Gamma_e^without - Sum lambda_e Gamma_e^with
      = Sum_e lambda_e[delta_j(e)(z_e^+) - delta_j(e)(z_e^-)].

Grouping by terminal tuple z and client x gives coefficient

    kappa_z(x) = Sum_(e:z_e^-=z) lambda_e 1_(x in S_j(e)(z))
               -Sum_(e:z_e^+=z) lambda_e 1_(x in S_j(e)(z)).

If some rho_z>=0 satisfy kappa_z(x)<=rho_z c_x(z) for every x in A, then

    Sum lambda_e Gamma_e^without
      >= Sum lambda_e Gamma_e^with - Sum_z rho_z E_A(z).

This is a sufficient occupancy-capacity condition, not a construction of
rho or of the IC multipliers. It explains exactly which additional condition
would lift the fixed-terminal pool to a collection of adaptive comparisons.

## 2. A genuine general IC-stability inequality

The full SPE inequalities do imply a quantitative bound after removal.
Let sigma be a complete pure SPE of the child with fixed background b+A
and n tail players. Let q be its actual tail leaf, and let b_j be b plus
the actual earlier tail load at player j's node, excluding the inserted A.
Keep exactly the same complete child strategy after removing A. Let

    epsilon_j = max_T [u_j^without(z_(h_j,T))
                      -u_j^without(q)]_+.

Every forced terminal here uses the original sigma after the same ordered
tail prefix; the removed-root strategy need not be an SPE. Define

    k_j = max_(T in catalogue) sum_(x in A cap T)
                  1/[(b_j(x)+1)(b_j(x)+2)].

Then the all-input inequality is

    epsilon_j <= k_j - delta_j(q),

    Sum_j epsilon_j <= Sum_j k_j - E_A(q)
                    <= n K_b(A)-E_A(q),

where

    K_b(A) = sum_(x in A) 1/[(b_x+1)(b_x+2)].

Indeed, at a forced leaf for T, the moving player covers every client in T,
so its no-root final load at x in T is at least b_j(x)+1. Its insertion
loss delta_j at that leaf is therefore at most the displayed T sum and
hence at most k_j. Original full-history SPE gives

    u_j^without(forced)-u_j^without(actual)
      = -Gamma_j(T)+delta_j(forced)-delta_j(actual)
      <= k_j-delta_j(q).

The right side is nonnegative because it also bounds the actual action's
insertion loss. Taking the maximum including the actual action and then
summing proves the first two inequalities. The last follows from b_j>=b.
The subtraction E_A(q) is one common pool at the original leaf, not n
separate copies. The next family attains n K_b(A)-E_A(q) exactly, so the
n factor cannot in general be replaced by an absolute constant when the
right side is normalized by K_b(A).

This stability inequality is new to this working note's derivation, but
no novelty or independent-review claim is made. It is a complete general
bound on the specified defects; it does not establish a small enough
aggregate loss to close the desired welfare induction.

### Root's separately derived extension to deleting an integer background

After receiving the unit-insertion statement, root independently supplied
the following extension on 2026-10-24. It is recorded as root's extension,
not silently included in this branch's original claim. Let d be any deleted
nonnegative integer background, let b be the retained integer background,
and let sigma be a complete SPE of the n-tail child with background b+d.
For an actual tail leaf q with load c and true prefix tail load p_j, put

    delta_j^d(q) = sum_(x in S_j(q))
                       d_x/[(b_x+c_x)(b_x+c_x+d_x)],

    E_d(q) = sum_(x:c_x>0)
                       c_x d_x/[(b_x+c_x)(b_x+c_x+d_x)],

    K_j^d = max_(T in catalogue) sum_(x in T)
             d_x/[(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)].

With exactly the same strategy after deleting d, the actual-path positive
one-step IC defects satisfy

    epsilon_j <= K_j^d-delta_j^d(q),
    Sum_j epsilon_j <= Sum_j K_j^d-E_d(q).

The proof is the same monotone denominator comparison, now using
1/L-1/(L+d)=d/[L(L+d)]. Every displayed denominator on a selected-client
term is positive. Terms with d_x=0 are zero. This branch has checked the
algebra but has not independently reviewed the full generalized statement;
root sent it separately for blind reconstruction. The extension does not
remove the cross-leaf capacity problem or establish a new welfare range.

## 3. The precise stronger stability candidate that fails

One might hope that, when the child with A present is a complete SPE, the
sum of its actual-path incentive defects after deleting A is at most a
universal constant times the inserted player's original profit, or times
E_A at the original leaf. Both statements fail without a dependence on the
number of remaining players.

For each n>=1 use n+1 pairwise disjoint singleton themes

    A={x}, B_1={y_1}, ..., B_n={y_n}.

Take an old background with exactly one incumbent on each B_j and none on A.
Insert a fixed unit root choosing A. There are n tail players. Thus every
singleton has baseline load one when the tail child starts.

At every ordered tail history, call a theme fresh if no tail player in that
history has selected it. The child strategy selects the first fresh theme
in the fixed priority order B_1,...,B_n,A. This definition includes arbitrary
repetitions and every off-path history. After k<n tail actions at most k
themes are nonfresh, so at least n+1-k fresh themes remain, more than the
n-k remaining players.

This is a complete pure SPE of the child with A present. A prescribed fresh
theme is never selected by a later prescribed player, so the current payoff
is exactly 1/2. A deviation to another fresh theme also yields exactly 1/2.
A deviation to a nonfresh theme has final load at least three and yields at
most 1/3. These inequalities hold at every ordered history, not just the
displayed path. This credible child can be extended to a full-history SPE of
the original common-catalog game by independently filling every other
subgame and applying backward induction at its ancestors.

The displayed tail path is B_1,...,B_n. The inserted root is the sole player
on x, so

    d_A(q)=1, E_A(q)=0.

Now delete that fixed root, retaining the old B_j background, the same n tail
players, and exactly the same complete tail strategy. On the displayed path
each tail player still earns 1/2. At each displayed position it can deviate
to A; all later prescribed players choose fresh B themes, so that deviator
is the unique player on x and earns 1. The actual-path one-step incentive
defect is exactly 1/2 at every position, and therefore

    Sum_(j=1)^n defect_j = n/2,
    Sum defect_j / d_A(q) = n/2,
    E_A(q)=0.

The n defects use n mutually exclusive leaves. At each such leaf the queried
deviator covers x; their fixed-terminal insertion losses are all 1/2, but
there is no common leaf containing n such players. In the certificate form
above, the n forced leaves each require separate occupancy capacity. The
single original leaf supplies none of it.

This does not refute a corrected stability theorem with a true cross-leaf
capacity condition, nor any H4/Mpath/free-menu candidate. In particular the
deleted-root strategy is deliberately not asserted to remain an SPE. It
only refutes using the fixed-terminal common pool to bound its summed
adaptive defects.

## 4. Consequence for the current proof attempt

The insertion/refund calculation does give a sharp common-customer bound on
one terminal tuple. It does not give the required stability of a complete
continuation tree. The counterfamily realizes the failure through entirely
credible original children and one deleted customer; old B incumbents remain
present throughout. A direct induction which deletes an inserted player
must either repair the child and charge the new leaves using an additional
capacity invariant, or avoid claiming that the original child's aggregate
IC distortion is paid once by that player's original terminal profit.

The general IC-stability inequality above retains true prefix information
and pays the original overlap only once, but its worst-case n/2 term is
realized by the credible child family. The remaining obstacle is therefore
precisely cross-leaf occupancy capacity, beyond this removal operation. No
nonnegative bound for the intermediate PEEL drift was obtained. Replacing
that drift by a sum of deletion defects would reintroduce the unbounded
quantity above, unless a new cancellation or weighting condition is proved.

Relevant sources read before this derivation:

- `research/current/customer_attraction/model.md` and `general_half_proof.md`.
- `R-868a6ab8c81345f28335d75046b756b0/harmonic_debt/h4_quantifiers_and_owner_thinning.md`.
- `R-79a883d99127437ebe4f0423a181f01b/GENERAL_PROOF_WORKING.md` (POT/RESET).
- `R-059140e622784d85a4e3a4dd6554f506/menu_covariance/last_successor_peeling.md`.
- `R-2e5a6ea95aff4f4c89f75237a74ba472/relay_credit/full_depth_ledger_and_harmonic_obstruction.md`.
- `R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md`.

The general statements above are established by the displayed derivations.
The accompanying audit only checks the explicit sensitivity candidate on
small members of its analytically proved family; it is not a search for a
Q-CAG-HALF counterexample.

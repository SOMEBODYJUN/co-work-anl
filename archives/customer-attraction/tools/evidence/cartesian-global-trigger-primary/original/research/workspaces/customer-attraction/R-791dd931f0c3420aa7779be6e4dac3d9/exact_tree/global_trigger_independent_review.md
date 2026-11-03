# Global-trigger Cartesian path implementation: independent reconstruction

2026-10-25. Exact CAG-MODEL, finite unit clients, a common finite catalog,
complete ordered histories, pure SPE, arbitrary ties, repeats and empty topics.
**HALF(5) and the general half conjecture remain OPEN.** This note independently
reconstructs a sufficient implementation interface requested by the parent.
It is not a necessity claim or a welfare proof. No external review or novelty
certification is asserted.

The reconstruction below was written from the statement supplied by
`credible_attack`, without reading its proof or implementation. The only
finite example is checked directly from utilities by the adjacent script.

## Exact interface

Fix the same number m>=1 of players in finitely many components c. Component c
has its own finite unit-client set N_c and finite nonempty common catalog S_c.
The client sets are pairwise disjoint. Fix an arbitrary legal ordered script
a^c=(a_1^c,...,a_m^c) in each component; it need not be a local SPE outcome.

At any local ordered history h of length i-1 and any legal action b, let
E_c(hb) be the nonempty finite set of full terminal profiles obtainable after
hb by a complete pure SPE of the remaining players. Define

    ell_c(h,b) = min_{z in E_c(hb)} u_i^c(z),
    M_c(h) = max_{b in S_c} ell_c(h,b).

The payoff being minimized is that of **the player i who has just chosen b**,
not that of player i+1 who first moves inside the suffix. At i=m there are
no remaining players and E_c(hb) is the singleton terminal profile hb.
Minima are attained because the finite game has finitely many pure strategies.
Existence of each suffix SPE follows from backward induction.

Write h_i^c=(a_1^c,...,a_{i-1}^c) and

    delta_i^c = u_i^c(a^c) - M_c(h_i^c).

Form the full Cartesian common catalog whose action tuple (b_c)_c covers
the disjoint union of the component topics b_c. If

    sum_c delta_i^c >= 0               for every i=1,...,m,       (GT)

then a complete pure SPE of the product game has the joint scripted path.
Empty topics, repeated actions and zero-client games do not require strict
inequalities. This is a sufficient statement only.

## Construction and proof

On the joint script, prescribe its next joint action. Suppose the first
joint mismatch occurs at position i, with action vector b differing from
(a_i^c)_c. In **every** component c, including components whose current action
did not change, choose a full suffix SPE attaining ell_c(h_i^c,b_c). From
then on, permanently use the product of these chosen component suffix SPEs.
Do not restart the trigger construction after later deviations.

These choices define a complete strategy. Every non-script history has a
unique first mismatch, hence a unique selected product suffix. Two distinct
global trigger subtrees are disjoint even when their projections share the
same local ordered history. Full global history dependence permits different
local suffix equilibria in those different global subtrees; no count-only or
component-local strategy restriction is imposed.

At a history already inside a selected product suffix, a joint deviation
changes a vector of component actions. Each local suffix is an SPE, and the
player's total payoff is the sum of the local payoffs. Summing their genuine
local comparisons proves the joint comparison at every such history.

At script position i, a proper joint deviation b triggers total payoff

    sum_c ell_c(h_i^c,b_c)
      <= sum_c M_c(h_i^c)
      <= sum_c u_i^c(a^c),

where the last inequality is (GT). Obeying the script continues along the
joint script and gives precisely its displayed total payoff. Thus its
comparison is also valid. This argument applies at every script position;
equivalently one can verify these positions in reverse order. All other
histories were covered by the selected product suffix argument. The complete
strategy is therefore a pure SPE.

The proof does not assume the scripts are locally credible. Their local
positive and negative deficits can compensate. At the final position every
local delta_m^c is nonpositive because M_c is the ordinary last-player best
reply value; (GT) consequently forces all positive-weight component final
scripts to be best replies individually.

## Exact example: all-coordinate switching is necessary for this construction

Take two disjoint copies of the following four unit-client, two-player game:

    A={x1,x2}, B={x1,x2,y}, C={y,z}.

The last player's best replies after A are B,C; after B they are B,C; after
C the unique best reply is B. Choosing the root player's least favorable
best reply always selects B. Thus the three minima ell(root,A/B/C) are
1,3/2,3/2, so M(root)=3/2.

Use script AB in the first component and AC in the second. Their root
deficits are respectively -1/2 and +1/2; their last-position deficits are
both zero. Neither requiring all individual deficits to be nonnegative nor
requiring every local script to be an SPE would admit this example: AB is
not a local SPE outcome, since its root payoff 1 is below M(root).

The product strategy prescribes root (A,A), then (B,C). At every other root
tuple its last reply is (B,B). The root gets 3 on the script and at most 3
after any proper deviation. Every last response is a genuine product best
reply. This is a complete product SPE.

If a trigger changed only the coordinates whose action changed, the root
deviation (B,A) would be answered by (B,C). Its payoff would be
3/2+2=7/2>3. Both local last responses are still best replies; the error is
the missing switch in the unchanged second coordinate, not a false child
equilibrium. The all-coordinate clause is therefore essential here.

The adjacent definition-level verifier enumerates every joint root and last
action, checks all 90 SPE comparisons for the correct strategy, and checks
this explicit 1/2 profitable deviation for the changed-only strategy. It
also adds an empty local topic and repeats the checks.

## Counts, scaling, physical actions and welfare

One may replace ordered h by its count vector in the definition of E and M,
but only because the **sets of feasible suffix outcomes** are invariant:
two fixed histories with the same counts have isomorphic future games under
the map that keeps the future ordered suffix unchanged. This does not force
the actual selected continuation to depend only on counts.

Nonnegative rational mixtures are implemented by deleting zero-weight
components first, then multiplying by a common positive denominator and
cloning each component's clients by the resulting positive integer. Positive
scaling preserves the local SPE set and scales ell, M and delta. Deleting
zero factors avoids artificial action labels that would become the same
physical theme after their distinguishing clients disappear. With positive
weights, disjoint component client sets make the tuple-to-union map injective
whenever the local catalogs are actual sets of distinct customer subsets.

For the full Cartesian catalog, both actual welfare and OPT_m are additive.
Every m-tuple of joint actions yields one feasible local m-tuple in each
component, giving OPT_m(product)<=sum_c OPT_m(c). Conversely independently
choose each component's optimal local m-tuple and combine their coordinates
player by player, giving the opposite inequality. Therefore a finite rational
mixture satisfying (GT) and sum_c[2W_c(a^c)-OPT_m(c)]<0 would give a genuine
unit-client counterexample after cloning. No such negative mixture is
provided here, and failure to find one would not prove the half conjecture.

## Review conclusion

The precise sufficient interface above survives the independent reconstruction.
Its scope includes arbitrary local scripts, complete joint histories and
arbitrary local tie choices. The proof critically uses the full Cartesian
action catalog, a common player horizon, minima of the just-acted player's
payoff, switching all coordinates at the first mismatch, and permanently
following the selected local suffix equilibria after that mismatch.
Necessity, an unconditional half result, and the existence of a negative
mixture remain unproved.

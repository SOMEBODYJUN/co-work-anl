# Blind audit: deleting background mass and summing actual-node regret

2026-10-24. Status: **proved auxiliary inequality, pending root's comparison with its derivation**. I reconstructed this proof from the statement sent by root, without reading any `harmonic_menu` files. This component does not close Q-CAG-HALF.

## Exact statement used

Fix a finite unit-customer set X and finite nonempty common topic catalog S. Let b_x,d_x be nonnegative integers for every customer, and n>=0 the number of tail providers. Fix a complete ordered-history pure strategy sigma that is an SPE when the fixed background load is b+d. The background providers do not change their actions.

Freeze sigma's actual tail path q=(S_1,...,S_n), let c_x be its total tail load, and let p_j(x) count only S_1,...,S_(j-1). After deleting background d, retain exactly the same complete strategy sigma. For every actual history h_j and alternative T, denote by z_j(T) the complete tail path with actual prefix h_j, forced current action T, and original sigma thereafter. Thus all later actions may change with T.

Write u_j^a(z) for current provider j's payoff on tail path z with fixed background load a. Define the actual-node one-deviation positive regret after deletion by

    R_j = max{0, max_(T in S) [u_j^b(z_j(T)) - u_j^b(q)]}.

The outside zero is redundant because T=S_j yields z_j(T)=q. This is a regret of a complete prescribed plan, not a claim that sigma is an SPE after deletion.

Set

    K_j = max_(T in S) sum_(x in T)
            d_x / [(b_x+p_j(x)+1)(b_x+p_j(x)+d_x+1)],

and

    E_d(q) = sum_(x:c_x>0)
            d_x c_x / [(b_x+c_x)(b_x+d_x+c_x)].

Then

    sum_(j=1)^n R_j <= sum_(j=1)^n K_j - E_d(q).

No assumption about count-dependent tie choices, nonempty topics, distinct actions, or preservation of SPE after deletion is needed.

## Pointwise removal gain

For any tail leaf z where current provider chooses T, write c_x(z) for total tail load. On x in T the denominator b_x+c_x(z) is at least one, so

    u_j^b(z) - u_j^(b+d)(z)
      = sum_(x in T) d_x / [(b_x+c_x(z))(b_x+d_x+c_x(z))].

Call this quantity Delta_j(z). It is nonnegative. For fixed b_x,d_x>=0, the summand is nonincreasing in positive c_x(z), because both denominator factors are nondecreasing and the numerator is fixed.

The true deviating leaf z_j(T) retains the actual prefix and the current cover T. Therefore c_x(z_j(T))>=p_j(x)+1 for every x in T, regardless of the later response. Hence

    Delta_j(z_j(T)) <= K_j(T) <= K_j.

This is a denominator envelope for the removal gain, not a claim that the followers are frozen.

Let A_j=Delta_j(q). Since c_x>=p_j(x)+1 on S_j,

    A_j <= K_j(S_j) <= K_j.

Thus K_j-A_j is nonnegative, which is essential when taking positive regret.

## Compare the original, genuine IC row

The original SPE condition at the actual node gives, for every T,

    Gamma_j(T) := u_j^(b+d)(q) - u_j^(b+d)(z_j(T)) >= 0.

Subtract and add these original payoffs in the deleted-game deviation gain:

    u_j^b(z_j(T)) - u_j^b(q)
       = Delta_j(z_j(T)) - A_j - Gamma_j(T)
       <= K_j - A_j.

Since K_j-A_j>=0, taking the maximum over all T and the positive part gives

    0 <= R_j <= K_j-A_j.

Now exchange the finite player and customer sums. Each actual cover of x contributes the same removal gain d_x/[(b_x+c_x)(b_x+d_x+c_x)], and there are c_x such covers. Therefore

    sum_j A_j = E_d(q).

Summing the pointwise bounds proves the statement.

## Exact nonnegative-slack identity

Because the prescribed action is an admissible deviation and has zero gain,

    R_j = max_T [Delta_j(z_j(T)) - Gamma_j(T)] - A_j.

Consequently the nonnegative residual can also be written

    K_j - A_j - R_j
       = min_T {K_j - Delta_j(z_j(T)) + Gamma_j(T)} >= 0.

The two retained sources of slack are the congestion envelope and the genuine original IC slack. No comparison of unrelated leaves or replacement of an off-path old-player payoff is used.

## Quantifiers, edge cases, and actual strength

- n=0 gives empty sums and E_d(q)=0.
- Empty topics contribute zero. Repeated topics and customers interested in no topics cause no denominator issue.
- In E_d(q), only c_x>0 occurs, so b_x+c_x>0. In K_j, denominators are at least one. d_x=0 gives a zero numerator with positive denominators.
- All zero-customer instances satisfy equality zero.
- Full SPE is more than the proof needs: it suffices that sigma is a complete plan satisfying its original one-deviation inequalities at the actual n nodes. It need not be sequentially optimal at other nodes for this algebraic implication. For the intended application, full original SPE supplies those rows.
- The same proof works for finite nonnegative customer values and nonnegative real b,d with the displayed positive denominators. This is an algebraic extension, not a change to Q-CAG-HALF's unit model.
- An analogue for a different starting history holds after placing its frozen old tail-prefix load into b. One must recompute that subgame's actual path, K_j, and E_d rather than transporting the root quantities unchanged.

## Sharp one-tail example with nonzero E_d and positive regret

There is one tail provider and two disjoint topics A,B. Topic A has three unit customers with b=0,d=2; topic B has two unit customers with b=0,d=1. Under b+d both topic payoffs equal one. Choose B as sigma's actual action; this is a complete pure SPE.

After deletion, B pays two and A pays three, so R_1=1. The removal envelopes are K(A)=3*(2/3)=2 and K(B)=2*(1/2)=1. Thus K_1=2. The actual removal rebate is E_d(q)=2*(1/2)=1. Equality holds:

    R_1 = K_1-E_d(q) = 1.

Here d is even realizable as a legal fixed prefix: two background A choices and one B choice.

## Independent finite implementation audit

`audit_background_deletion_blind.py` directly expands unit customers, constructs complete ordered-history SPE strategies by definition-level backward induction, and checks the original IC rows plus every displayed node and summed inequality with Fraction. It imports no repository solver or prior harmonic-menu code. Its finite output is `background_deletion_blind_audit.json`.

The finite audit checks the implementation and the sharp example. The general theorem is established by the algebra above, not by the finite run.

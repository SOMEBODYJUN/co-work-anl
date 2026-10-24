# Full-terminal minimax: the actual cross-subtree term

2026-10-24. An attempted all-input proof diagnostic, not a new solved claim. All the quantities below are defined from one fixed complete ordered-history pure SPE. The formulas retain the actual continuation after every observed action. They do not replace a true continuation by frozen opponents.

## 1. Root menu and exact comparison

Fix a legal background b, r remaining players, and a complete pure SPE sigma. For every legal root action A let

    Z(A) = (A, B_2(A), ..., B_r(A))

be the true complete outcome after forcing A and then following that same sigma. Let q_A(x) be the successor load from B_2(A),...,B_r(A), and let

    d_A = sum_(x in A) 1 / [b_x + 1 + q_A(x)].

If u is the actual current payoff, all root IC rows say d_A <= u, including ties. Define the extra-query matrix

    K(T,A) = sum_(x in T) 1 / [b_x + 1 + 1_(x in A) + q_A(x)].

Each column is a legal static background with all r current players still present. The desired root full-menu bridge is

    min_Q max_T E_(A~Q) K(T,A) <= u.                     (FM?)

Q is sampled independently of the extra query T. Finite minimax writes (FM?) as

    for every p, there exists A with E_(T~p) K(T,A) <= u.

This is the existing Mfull candidate, not a new interface.

For x in T, the true root-T payoff uses denominator b_x+1+q_T(x). Direct subtraction gives the exact transfer

    K(T,A) - d_T
      = sum_(x in T)
          [q_T(x) - q_A(x) - 1_(x in A)]
          / [(b_x+1+1_(x in A)+q_A(x)) (b_x+1+q_T(x))]. (TR)

This identity compares two different real root subtrees. It is valid for every finite catalog, every r, every legal background, every full-history tie choice, and nonnegative integer client multiplicities expanded into unit customers. Its role is diagnostic: it is a subtraction identity, not a new positive budget.

Write J(T,A) for the right side. For a fixed p, set

    e(p) = u - sum_T p_T d_T >= 0.

Then the exact missing minimax payment is

    min_A sum_T p_T J(T,A) <= e(p).                     (PAY?)

Indeed E_p K(T,A)-u = E_p J(T,A)-e(p). Thus (PAY?) is equivalent to the existing root menu bridge; writing it does not prove it or strengthen the known welfare range.

The negative term -1_(x in A) in (TR) is the genuine collision credit from retaining the forced root player in the full menu. Omitting that term changes the matrix to the already weaker r-1-slot menu and discards exactly the extra-slot discount. Likewise e(p) is the real root IC slack and cannot be dropped merely because its sign is known.

## 2. Why the stationary-label attempt did not prove PAY

A tempting construction routes root label A to one of its prescribed true successor labels B_j(A), chooses a stationary distribution over root labels, and tries to use the resulting marginal load conservation to show nonpositive total J. Its stationarity only balances label frequencies in that selected routing. The denominator in (TR) still depends on both the source subtree q_A and the target subtree q_T. It is not a difference of a scalar function of one root label, so ordinary stationary telescoping does not apply.

More concretely, label balance is a relation of the form sum_A pi_A P(A,T)=pi_T. The quantity to pay is instead

    sum_(T,A) p_T Q_A sum_(x in T)
      [q_T(x)-q_A(x)-1_(x in A)] / [(...q_A...)(...q_T...)].

The query coefficient is p_T, the background coefficient is Q_A, and neither is justified as the stationary distribution of the true-successor routing. Even identifying them would leave the two different reciprocal denominators. No valid inequality turning these terms into a nonpositive cycle sum was obtained.

This is the precise failure of this attempted proof, not an impossibility theorem for arbitrary transports and not a full-SPE counterexample to (FM?). Existing failures of fixed stationary pair transport already warn against declaring the missing sign automatic. The present computation does not claim another such counterexample.

## 3. Why minimal-player extra-one induction does not repair the step

The existing minimum-remaining-population reduction for the unrestricted free extra-one floor correctly proves the following conditional normal form: in a minimal bad background subgame with threshold t>u, every prescribed real successor in every forced root branch has final payoff at least t. In particular each successor gets positive payoff outside that branch's root theme.

That assertion is about the actual outcome Z(A). Applying a child Mfull hypothesis to a particular p may select a different action at the child's first node and hence a different leaf Z(A,B). It does not make Z(A,B) equal to the prescribed root endpoint Z(B), because their ordered prefixes differ. The full-history model expressly permits their continuations to differ. Replacing one by the other would discard the very q_T-q_A transfer in (TR).

The actor's deletion-regret envelope controls the error of replaying one prescribed strategy after changing its fixed background. It does not identify the newly prescribed strategy in another root child, and it does not provide a shared refund budget over all those different new leaves. Consequently it cannot currently supply (PAY?).

## 4. Coverage consequence and m=5 pressure test

If the root full-menu bridge were proved for all legal backgrounds and all r, it would give each actual player at least the unrestricted root extra-slot value v_(m+1)(0). The known static comparison OPT_m <= 2m v_(m+1)(0) would then give half coverage.

At m=5 this substitution is exactly

    OPT_5 <= 10 v_6(0),
    [unproved FM at all actual positions] => W >= 5 v_6(0),
    hence [conditionally] OPT_5 <= 2W.

There is no unconditional five-player half bound in this note. The missing inequality remains (PAY?) for the real ordered-history menus. No finite negative search or inability to pay J decides its truth.

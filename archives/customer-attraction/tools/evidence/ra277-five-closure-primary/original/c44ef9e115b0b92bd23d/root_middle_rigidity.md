# Five-player root rigidity with a genuine penultimate comparison

Status: exact self-contained certificate; sibling independent mathematical review passed. This
strengthens `root_rigidity.md` by using a genuine intermediate player's IC.
It remains a necessary inequality, not a five-player half-coverage proof.

## Exact statement, including the common maximum topic size

Fix any five-player complete-history pure SPE in CAG-MODEL, with actual first
payoff u. Define M=max_(S in catalog)|S|. For all catalog topics T,Q,

    F_T(Q):=|Q\T|+|Q intersect T|/5
       <= (311/21)u+(55/21)M-(113/21)|T|.           (M-RIG)

The displayed (M-RIG) itself also holds if M is replaced by any common upper
bound for topic sizes. For the chosen maximum M, every root deviation has
payoff at least its topic's size divided by five, so M<=5u. Consequently

    F_T(Q) <= u+(113/21)(5u-|T|).                   (RIG-113)

The common M must be retained when available. Substituting a separate 5u for
each topic size discards valid common information. Compared with the old
common-M version 16u+(5/2)M-(11/2)|T|, the new right side minus the old is

    (5/42)(M+|T|-10u) <= 0.

Thus (M-RIG) weakly dominates the preceding inequality in every instance.
All actual/comparison topics may repeat or be empty. No tie selector is fixed.

## Genuine branch and nonnegative comparisons

Force root action T and then execute the original strategy. Write its true
leaf (T,B_2,B_3,B_4,B_5), and player payoffs r,v_2,v_3,v_4,v_5. The following
slacks are nonnegative:

    R = u-r,
    K_j = M-|B_j|               (j=2,3,4,5),
    L = v_4 - sum_(x in B_5) 1/(1_T+1_(B_2)+1_(B_3)+2),
    Z = v_5 - sum_(x in Q)   1/(1_T+1_(B_2)+1_(B_3)+1_(B_4)+1).

R is true root IC. K_j are catalog size bounds. For L, the true player 4 at
history (T,B_2,B_3) may deviate to the legal topic B_5. The original last
player is allowed to change; its load is merely bounded by one, so the
written lower bound is valid. In particular L does **not** freeze B_5 after
that deviation. Z is the genuine player-5 best reply comparison with Q.

Only the penultimate and final players' IC on this root-deviation branch are
used. Player 2 and player 3 require no extra IC in this certificate.

## Exact 64-type identity

For a customer write t=1_T, q=1_Q, a=1_(B_2)+1_(B_3), b=1_(B_4),
c=1_(B_5), ell=t+a+b+c. Shares with a zero numerator and ell=0 are zero.
Define

    rho(t,q,a,b,c) =
        -(113/21)t-q/(1+4t)+(311/21)t/ell
        +a/2+(31/42)b+(37/42)c
        -(5/21)[b/ell-c/(t+a+2)]
        -c/ell+q/(t+a+b+1).                         (1)

Then the exact summed identity is

    (311/21)u+(55/21)M-(113/21)|T|-F_T(Q)
      = (311/21)R+(K_2+K_3)/2+(31/42)K_4+(37/42)K_5
        +(5/21)L+Z+sum_x rho_x.                    (2)

Indeed the M coefficients sum to 1+68/42=55/21, the u coefficient is
311/21, and each of the remaining terms follows directly from (1).

For t=0, the q coefficient in rho is 1/(a+b+1)-1<=0, so the worst q is 1.
For t=1, it is 1/(a+b+2)-1/5>=0, so the worst q is 0. Thus the following
24 rational values prove all 64 binary membership residuals nonnegative;
a=1 corresponds to either order of the B_2,B_3 memberships.

| t | a | worst q | 1260rho, bc=00 | bc=01 | bc=10 | bc=11 |
|---|---|---|---:|---:|---:|---:|
|0|0|1|0|0|0|780|
|0|1|1|0|580|570|1410|
|0|2|1|420|1185|1145|2040|
|1|0|0|11880|3130|3330|1060|
|1|1|0|3180|835|900|240|
|1|2|0|700|0|0|0|

Equation (2), the nonnegative slacks and this complete type calculation
prove (M-RIG). This finite calculation is over **all possible customer
memberships** for the displayed topics, rather than over a finite sample of
games, catalogs or strategies. It imposes no extra consistency or distinctness
restriction, so repeated labels and equal sets are included automatically.

## Coverage corollary

For any five legal comparison topics with union O,

    sum_j F_T(T_j) >= |O|-(4/5)|T|.

This follows pointwise: a customer in O\T contributes at least one, and a
customer in O intersect T at least 1/5; |O intersect T|<=|T|. Therefore

    OPT_5 <= (1555/21)u+(275/21)M-(2741/105)|T|.     (3)

With the chosen M=max catalog size, using M<=5u and delta_T=5u-|T| gives

    OPT_5 <= 9u+(2741/105)delta_T.                  (4)

These are valid global OPT inequalities for every legal T. They alone do not
bound delta_T sufficiently to prove OPT_5<=2W. Parent work combines the common
M version with the preexisting actual-path and other genuine branch rows.
No claimed numerical closure is part of this note.

## Exact implementation audit

`audit_middle_rigidity.py` independently evaluates (1) in Fraction on all
64 bit states, derives the complete 24-entry table and records the rational
weights in `audit_middle_rigidity.json`. It does not import the optimizer or
old template implementation. The optional discovery script
`probe_middle_rigidity.py` solves a 65-variable root-branch relaxation and
suggested these rational coefficients; its floating optimum has no role in
the final proof. Strong pair-tax rows were inactive in that exploratory
slope calculation. Nothing here proves that the improved slope is optimal
for full SPE.

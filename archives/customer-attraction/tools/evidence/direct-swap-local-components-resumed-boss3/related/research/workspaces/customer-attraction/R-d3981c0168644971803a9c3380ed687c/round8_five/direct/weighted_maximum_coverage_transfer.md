# A paid coverage reset to the same weighted maximum

2026-10-25. Original five-provider common-catalog unit-customer model, arbitrary finite inputs and every complete-history pure SPE. Empty themes, repetitions, zero customers, and arbitrary off-path ties are retained. This is an author coverage-omission consequence of the existing BNS mechanism, with an exact coefficient audit. The parent independently checked the source kernel and sharpened the amount from u-K to the retained forced-H payoff v-K. It is not HALF(5), an external review, or a novelty claim.

## Precise local payment

Fix any actual decision history h with exactly three providers remaining. Let p_x in {0,1,2} be its past load, and let its original-sigma continuation be (A,B,E). The current provider's final payoff is u. Choose one legal theme H maximizing

    K = sum_(x in H) 1/(p_x+3),       delta = u-K >= 0.

Force this current provider to H and then follow the SAME original sigma, obtaining (H,Q,R). The forced provider's payoff is v<=u. Put eta=v-K, so 0<=eta<=delta. Let U be the full covered set at (h,A,B,E), and U_H that at (h,H,Q,R). Then

    |U_H minus U| <= 24 eta <= 24 delta.                         (RESET)

In particular W(h,H,Q,R)-W(h,A,B,E)<=24 eta. This controls the aggregate old-player refunds together with the suffix change; it does not incorrectly discard old players' payoff changes. All quantities belong to this one source history and its one genuine child. Multiple mutually exclusive source eta values still require a common payment; RESET does not supply that payment.

## 1. At most 12 eta new H-customers are missing from the source leaf

Put w_x=1/(p_x+3), and define

    F(H,E)=sum_(H cap E)1/(p+3)+sum_(E minus H)1/(p+1).

Retain the forced-H payoff in the existing weighted-max BNS proof at k=3, total load bound 5. Its original steps give

    F(H,E)-K <= eta+(3/2)D+(1/4)D_R <= 8 eta,

where D is the forced-H missing-seat weight defined below, D_R=w(H minus R)<=D, and D<=4eta. In particular

    F(H,E)<=K+8 eta.                                (BNS)

The actual last player's comparison to H gives

    q_H=sum_H 1/(p+1_A+1_B+1) <= u_E.

Let M=|H minus (past union A union B union E)|. The following pointwise identity has a nonnegative remainder:

    q_H + F(H,E) - u_E - K >= (2/3) M.                (OMIT)

Indeed, for client bits a,b,e,h, the pointwise left side is zero if h=e; if h=1,e=0 it is

    1/(p+a+b+1)-1/(p+3) >= 0;

if h=0,e=1 it is

    1/(p+1)-1/(p+a+b+1) >= 0.

A client counted by M has p=a=b=e=0,h=1, giving exactly 2/3. Consequently

    (2/3)M <= F(H,E)-K <= 8 eta,
    M <= 12 eta.                                   (1)

The omitted-H comparison is made at the original actual last node. It does not pretend that E is the last response after forcing H.

## 2. At most 12 eta fresh customers outside H enter its genuine child

In the forced-H leaf define the missing-seat weight

    D=sum_(x in H) (2-1_Q-1_R)/(p+3).

The forced player's excess satisfies

    v-K = sum_H (2-1_Q-1_R)/[(p+1+1_Q+1_R)(p+3)] >= D/4.

Whenever the numerator is nonzero, p+1+1_Q+1_R<=4. Hence D<=4(v-K)=4 eta.

Both Q and R are legal catalog themes. The SAME H is maximal for the SAME original weight w, so

    w(Q minus H)<=w(H minus Q),
    w(R minus H)<=w(H minus R).

Their combined outside-H incidence weight is therefore at most D. On a customer outside the past union p=0 and w=1/3. The number B of prefix-fresh customers covered by Q or R outside H is at most three times this incidence weight. Thus

    B <= 3D <= 12 eta.                              (2)

Every newly covered customer in U_H minus U is either counted by M or by B. Equations (1),(2) prove RESET. We need no relation between the original and forced-H suffixes beyond their actual prescribed actions.

## Explicit common-account certificate and source attribution

Write G0=u_E-q_H>=0, G1=K+8eta-F(H,E)>=0, GQ=K-w(Q)>=0, GR=K-w(R)>=0, and GD=4eta-D>=0. With

    rho0=(3/2)[q_H+F(H,E)-u_E-K]-M >=0,
    rho1=3[w(Q minus H)+w(R minus H)]-B >=0,
    rho2=M+B-|U_H minus U| >=0,

there is the exact identity

    24eta-|U_H minus U|
      =(3/2)G0+(3/2)G1+3GQ+3GR+3GD+rho0+rho1+rho2.

This exposes every use of the same eta. In particular the two 12eta charges are not separate free budgets. Replacing eta by delta is only the genuine current-node IC v<=u, used once at the final projection.

## Why individual old refunds cannot replace this net/coverage payment

The complete five-player SPE in weighted_maximum_old_refund_obstruction.json has two disjoint singleton themes C,H. Its actual leaf is C,C,C,H,H, payoffs (1/3,1/3,1/3,1/2,1/2). At prefix (C,C), H is the unique weighted maximum, K=1/3>1/5=w(C), and u=K. Forcing H gives C,C,H,H,H with payoffs (1/2,1/2,1/3,1/3,1/3). A self-contained full strategy is: the first three players always choose C; each of the last two chooses H exactly when the current history contains at least two C choices, and otherwise chooses C. The independent audit checks all 31 histories and 62 comparisons. Thus both old players get 1/6 back, even though delta=0 and the current IC slack is zero. The two future profits decrease by exactly 1/3; coverage does not increase, as RESET correctly predicts. In particular the original root IC upper bound 1/3 cannot be reused for the old root's 1/2 payoff in the forced-H child.

This specializes the already-known old-player-refund obstruction to the precise weighted-max H interface. It does not invalidate BNS, hinge, or HALF(5), nor does it establish that RESET is a sharp coefficient.

The old BNS and missing-seat tools belong to R-a0bb57fa24044a8794bc7991918a19c6/credible_counterexample/background_near_saturation.md. The new amount recorded here is the added-coverage stop bound obtained by combining that existing forced-H branch account with the original source last-node comparison. It is not a rediscovery claim for BNS or its zero-gap branch rigidity.

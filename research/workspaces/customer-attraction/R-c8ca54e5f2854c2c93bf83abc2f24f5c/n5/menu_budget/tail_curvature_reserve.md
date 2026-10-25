# Five-player fullslot menus: exact last-two query reserves

2026-10-25. **Proved identities and lower bounds; HALF5, SUMmin-full, and the different-query joint role payment remain OPEN.** Domain: arbitrary finite unit clients, finite nonempty common catalog, five unit providers, and any complete ordered-history pure SPE. Empty topics, repeated choices, zero clients, and all ties remain. This is an actor workspace result, without external review or a novelty claim.

The known last-two fullslot individual payment is reconstructed and refined below. The refinement keeps the exact IC, terminal best-response, and reciprocal-curvature reserves that are discarded by the individual inequality. It does not add the separate query maxima from the R-only layer-density lemma.

## 1. Data and convention

Fix one original full SPE sigma and its actual terminal tuple B. Actual final profits are u_i. For each actual position i and legal action A let Z_i(A) be the complete five-slot leaf after forcing A at the actual ordered prefix and following the same original sigma. In particular, the original past is retained and all future actions may change.

Fix any distribution p on the legal catalog. Let A,T be independent draws from p and write

    q_x = Pr[x in A],
    G_p(z) = E_T sum_(x in T) 1/(1+c_x(z)),
    Q_i(p) = E_A G_p(Z_i(A)),
    M_i(p) = min_A G_p(Z_i(A)).

Thus M_i<=Q_i. Both A and T are legal pure-query samples; no player commits to a hidden mixed strategy. Distributional averaging only forms nonnegative combinations of original IC rows.

The static safety comparison is OPT_5<=10 v_6(0). Every fullslot column is a legal five-slot static opponent tuple, so M_i(p)>=v_6(0) when p is a static maximizing query distribution. Therefore proving sum_i M_i(p)<=W for every p would prove HALF5. That payment has not been established here.

## 2. Exact final-player reserve

Let b_5(x) be the actual first-four load and define

    Gamma_5(A)=u_5-sum_(x in A)1/(b_5(x)+1)>=0.

The final player's actual-prefix IC gives the inequality. The fullslot leaf is just that fixed prefix followed by A. Expanding the independent extra-query denominator gives the exact identity

    u_5-Q_5(p)
      = E_A Gamma_5(A)
        + sum_x q_x^2/[(b_5(x)+1)(b_5(x)+2)].       (LAST)

Indeed, the uninserted independent-query mean is E_T sum_(x in T)1/(b_5+1), equal to the A-query mean. Inserting A changes a client denominator exactly when x belongs to A intersect T. Its probability is q_x^2, and the difference of the adjacent reciprocals is the displayed curvature term.

## 3. Exact penultimate reserve

Let b=b_4 be the actual first-three load. Let D(A) be sigma's true last-player action after this fixed prefix and A. Set

    U_b(X,Y)=sum_(x in X)1/[b_x+1+1_(x in Y)],
    Gamma_4(A)=u_4-U_b(A,D(A))>=0,
    R(A,T)=U_b(D(A),A)-U_b(D(T),A)>=0.

Gamma_4 is the original position-four actual-prefix IC. R(A,T) is a true last-player best-response row at prefix (B_<4,A), using the legal action D(T) as competitor. It does not transport D(T)'s continuation to another history: no players remain after this last move.

Define

    K_4(p)=E_(A,T) sum_(x in A intersect T)
       1/{[b_x+1+1_(x in D(A))][b_x+2+1_(x in D(A))]}.

Then

    u_4-Q_4(p)
      = E_A Gamma_4(A)+E_(A,T)R(A,T)+K_4(p).       (PENULT)

For the proof, first omit A from the extra-query fullslot background. Its expected value is E_(A,T)U_b(T,D(A)); adding A back subtracts exactly K_4. The same-background two-action identity

    U_b(X,Y)-U_b(Y,X)
      = sum_(x in X)1/(b_x+1)-sum_(x in Y)1/(b_x+1)

and exchange of the independent A,T labels yield

    E_A U_b(A,D(A))-E_(A,T)U_b(T,D(A))
      =E_(A,T)[U_b(D(A),A)-U_b(D(T),A)]
      =E R(A,T).

Insert the definition of Gamma_4 to obtain (PENULT). Every right-hand term is nonnegative. Moreover, the denominator in K_4 is at most (b_x+2)(b_x+3), so

    K_4(p)>=sum_x q_x^2/[(b_4(x)+2)(b_4(x)+3)].   (CURV4)

The argument uses terminal BR rationality and the exact reciprocal kernel. Nonnegative DR alone does not give these reciprocal reserves.

## 4. A genuine reserve for different early-query debt

Let

    R_45(p)=E Gamma_4+E R+K_4
             +E Gamma_5+sum_x q_x^2/[(b_5+1)(b_5+2)].

The exact identities show R_45=u_4+u_5-Q_4-Q_5, and hence

    (u_4-M_4)+(u_5-M_5)>=R_45(p)>=0.              (PAY45)

This reserve is paid by the actual fourth/fifth complete profits exactly once. In particular, the following concrete early-three inequality would suffice for SUMmin-full:

    sum_(i=1)^3 [M_i(p)-u_i] <= R_45(p).           (EARLY3?)

It is not proved. Replacing M_i by Q_i is a stronger sufficient candidate, also unproved. The root individual insurance-floor counterexample does not contradict (PAY45); it only shows why the early positive debt cannot be discarded player by player.

Write C=union(B), and let R be any subset of the actual missed clients. For x outside C, b_4=b_5=0, giving a combined curvature reserve at least (1/6+1/2)q_x^2=(2/3)q_x^2. On C, b_4<=3 and b_5<=4 give at least (1/30+1/30)q_x^2=q_x^2/15. Therefore

    R_45(p)>=(2/3)sum_(x outside C)q_x^2
                   +(1/15)sum_(x in C)q_x^2.     (MISS)

The first sum may safely be restricted to any chosen R. If p is uniform over five comparator topics, repeated topics included, every client in their union O has q_x>=1/5, and q vanishes outside O. With I=O intersect C and R=O\C this gives

    R_45(p)>=(2/75)|R|+(1/375)|I|.                (FIVE-COMP)

This is a paid positive amount, not a proof that it covers all early debt. No five-player half conclusion is drawn from it.

## 5. Definition-level verification and targeted discovery

`audit_tail_reserves.py` constructs complete pure SPEs with exact Fraction backward induction and then independently expands LAST, PENULT, all IC rows, CURV4, and MISS. Four fixtures include genuine overlap, an empty topic, six disjoint themes with one actual missed client, and the all-zero singleton empty catalog. All checks pass in `tail_reserves_audit.json`. The finite audit supports the formulas; the proofs above give their unrestricted scope.

`probe_summin.py` is a float discovery tool for true CAG client-type representations. Each fixed policy is complete on all ordered histories; its client-weight LP retains every ordered IC. A separate query LP maximizes the fullslot SUMmin defect. Alternating these LPs tested five-player k=5 (40 policies), k=6 (100), and k=7 (30), with no positive defect. A role-three individual contract probe at k=6 (100 policies) and a stronger same-p pushforward aggregate probe (100 policies) likewise found no positive. These negative probes are not proofs or reliable global feasibility bounds.

`probe_three_tail_milp.py` tested the stronger individual fullslot floor for three remaining players with an arbitrary legal two-slot background, fixed uniform p, k=4. It retains all ordered subtree histories and CAG type weights. Its 45-second run timed out, with a negative incumbent and a dual bound allowing positive violation. This is inconclusive and cannot promote the three-tail shortcut to a theorem. Such a background counterexample would in any event still require showing that background is reached by a five-player complete SPE before refuting an actual-position floor.

The no-spawn/no-git/no-external instructions for this actor were retained. Only this actor directory was written. The actual unresolved step is EARLY3 or another authentic crossquery payment; neither finite negative output nor the R-only per-client normalized-current layer inequality pays it.

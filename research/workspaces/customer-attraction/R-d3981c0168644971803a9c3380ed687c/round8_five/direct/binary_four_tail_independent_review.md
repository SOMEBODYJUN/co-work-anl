# Independent review: binary-background four-tail auxiliary certificate

2026-10-25. **PASS, within the stated five-player auxiliary scope.** This is an internal independent mathematical reconstruction and exact standard-library coefficient audit. It is not external review, an optimality/sharpness certification, a new HALF(5) bound, or a claim of novelty for the old twelve-row mechanism.

## Accepted statement and exact scope

In the original unit-customer, unit-provider common-catalog game with exactly five providers, fix ANY ordered one-provider prefix. Write its customer load as p_x in {0,1}. For EVERY original full-history pure SPE continuation of the remaining four providers, let

    V4=sum_x k_x/(p_x+k_x),
    F4(p)=max_(T1,T2,T3,T4) sum_x e_x/(p_x+e_x).

The accepted certificate proves

    F4(p) <= beta V4,
    beta=22869393/11445824 <1499/750<2.

Zero numerators are zero; the claim includes V4=0. The comparison tuple can repeat themes or contain empty themes, and the prefix can coincide with any of the later or comparison themes. No anonymous continuation or fixed favorable tie rule is assumed. F4(p) is the four remaining providers' comparison PROFIT, not total coverage, not OPT5, and not a five-player root welfare bound. This review makes no claim for p>=2.

The exact improvement over the old coefficient is 2622713/4292184000; the gap below two is 22255/11445824. Only existence of this feasible certificate is reviewed; its optimality in any row cone is not claimed.

## Reconstructed twelve legal rows

I rebuilt the rows from four_remaining_profit_bound.md, equations (3)--(13), not from the new generator's row function. Let the genuine continuation be A,B,C,D and, after the remaining first provider forces D, let the SAME original strategy give D,Q,R,S. Write u1,...,u4 and zD,zQ,zR,zS for the respective four remaining-role profits. All occurrences of the fixed old prefix are retained.

For any arbitrary fixed four-theme comparison tuple put O=R_p(T1,T2,T3,T4). The twelve nonnegative slacks are:

| Rows | Reconstructed definition and legitimate source |
|---|---|
| K_T, T=C,D,Q,R,S | u2-sum_T1/(p+1_A+3); actual remaining-second player's genuine deviation, bounded only by the valid maximum final load |
| current_IC | u1-zD; remaining-first player's true D deviation |
| Q_query_S | zQ-sum_S1/(p+1_D+3); true optimizing Q node, valid load bound |
| R_query_C | zR-sum_C1/(p+1_D+1_Q+2); true optimizing R node, valid load bound |
| R_query_S | zR-sum_S1/(p+1_D+1_Q+2); same true R node |
| S_query_B | zS-sum_B1/(p+1_D+1_Q+1_R+1); exact final-player best reply |
| P | 2H+sum delta2(p,1_A+1_B)-O |
| E | 4u4+sum delta3(p,1_A+1_B+1_C)-O |

Here

    H=u3+u4+sum_C1/[(p+1_A+1_B+1)(p+1_A+1_B+2)],
    D4(p)=(p+1)(p+2)(p+3)(p+4),
    tau(p,v)=1/(p+1)-1/(p+v+1),
    delta2(p,v)=tau(p,v)+1_(v=2) 2p²/[3D4(p)],
    delta3(p,v)=tau(p,v)+1_(v=3) (p²+p)/D4(p).

In particular the P correction uses the TWO-action load 1_A+1_B; E uses the THREE-action load 1_A+1_B+1_C. The tax correction inside H is paid on C, the first of the actual final two. No one-step shift or missing aggregate correction was found.

The five K rows and four post-deviation rows compare legal original-catalog themes at their stated original histories. Only Q,R,S optimize on the forced-D branch; the forced D player is not falsely treated as an optimizing node there. All deep continuations can change after a deviation.

## Aggregate corrections were independently checked

For comparison membership t in {0,1}^4, let e=sum t. I explicitly summed the SIX unordered comparison pairs at background p+v, rather than relying only on the compressed polynomial. For P the necessary client inequality is

    (1/3)sum_(i<j) (t_i+t_j)/(p+v+t_i+t_j)
        +delta2(p,v)-e/(p+e) >=0,    v=0,1,2.

For E it is

    sum_i t_i/(p+v+1)+delta3(p,v)-e/(p+e)>=0,
        v=0,1,2,3.

The audit checks all 96 P states and 128 E states for p=0,1, exactly. Both minima are zero. Thus the same P/E definitions remain legal for an arbitrary four-theme comparison tuple; the nonzero weights of these rows cannot silently change their comparison target.

## Exact coefficient conclusion

The supplied JSON's twelve rational weights are all nonnegative, and

    lambda_E+lambda_P=1.

For each of the 256 states (p,a,b,c,d,q,r,s), p=0,1 and the seven memberships binary, I reconstructed every row twice: first from the OLD common-denominator numerator formulas, then independently from terminal payoffs and the explicit corrections. All 3072 row coefficients agree.

With O set to zero in those client coefficients, the audit computes

    rho=beta*(a+b+c+d)/(p+a+b+c+d)
         -sum_row lambda_row row_client_coefficient.

Every rho is nonnegative and independently matches the corresponding exported JSON coefficient. There are 17 zeros. The smallest strictly positive rebuilt coefficients are 22255/34337472 for p=0 and 4774397/103012416 for p=1. Summing clients, the E+P normalization gives the exact identity

    beta V4-O=sum_row lambda_row Slack_row+sum_x rho_x >=0.

Taking the maximum over four legal comparison themes proves the accepted statement. The original RHOMIN residual is not imported, reused, or inferred: changing beta and weights changes the residual.

## Uncorrected binary version

I also independently checked the follow-up claim that the two positive arbitrary-background corrections may be dropped on p=0,1. The 70 full (p,v,e) cases of the preceding two aggregate inequalities remain nonnegative with delta2=delta3=tau. This is a restricted binary-background fact, not an extension to arbitrary p.

The uncorrected JSON has exactly the same beta and all twelve weights. Its independently reconstructed residual satisfies

    rho_uncorrected=rho_corrected
       +lambda_P 1_(a+b=2)2p²/[3D4(p)]
       +lambda_E 1_(a+b+c=3)(p²+p)/D4(p)
       >=rho_corrected>=0.

All 256 uncorrected exported coefficients agree exactly. Thus the uncorrected binary version is also a valid F4(p)<=beta V4 auxiliary certificate. It does not justify replacing any old residual floor in a larger indexed system without rebuilding that system's exact client coefficients.

## Reproduction and limitations

Run audit_binary_four_tail_independent.py. It imports only fractions, itertools, pathlib, json, and hashlib. It does not import either new generator, SciPy, an old audit, or RHOMIN. The output audit_binary_four_tail_independent.json records counts, rational minima, and exact hashes for both reviewed JSONs.

The binary domain is forced by one previous unit provider in this five-player application. The finite 256-state check therefore exhausts all client coefficient patterns for these legal rows; it is not an inference from finitely many games. Whether this auxiliary improvement changes the main n=5 payment is a separate pending question. No other coefficient tuning or background extension is needed for this review.

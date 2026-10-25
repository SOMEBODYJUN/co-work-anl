# Signed old-role swap payment across two ordered histories

2026-10-25. Original five-provider model, all complete-history pure SPEs. This is an author exact local inequality and a failed route to a sufficient global amount. HALF(5) remains OPEN. It is not an external review or novelty claim.

Let Y=(A,C,Y1,Y2,L) and Z=(C,A,Z1,Z2,R) be the genuine original-sigma three-provider continuations after the indicated forced two-action histories. The tails may differ despite equal prefix counts. Write a_Y,c_Y,a_Z,c_Z for the final payoffs of their two old roles, and V_Y,V_Z for their three future profits. Then

    J=a_Y+c_Z-c_Y-a_Z <= (7/12)(V_Y+V_Z).             (SWAP)

The opposite sign follows by relabeling A,C. Empty/repeated themes and zero customers remain allowed. A,C need not be maximum themes.

For the Y leaf put b=1_A+1_C, let s1,s2,s3 be its future payoffs, and define

    K0A=s1-sum_A1/(b+3),
    K0L=s1-sum_L1/(b+3),
    K2A=s3-sum_A1/(b+1_Y1+1_Y2+1),
    K2R=s3-sum_R1/(b+1_Y1+1_Y2+1),
    T_AL=s2+s3+sum_Y2 1/[(b+1_Y1+1)(b+1_Y1+2)]
             -sum_x(1_A+1_L)/(b+1_Y1+1_A+1_L).

Zero-numerator fractions are zero. The first four quantities are genuine current-node IC consequences (the first two only use the valid final-load bound); the final one is the existing two-remaining tax. Define

    G_Y=(1/9)K0A+(1/6)K0L+(23/36)K2A+(1/3)K2R+(5/18)T_AL.

Define G_Z by interchanging A,C, Y1,Y2,L with Z1,Z2,R. Every slack is nonnegative, and the exact identity is

    (7/12)(V_Y+V_Z)-J=G_Y+G_Z+sum_x rho_x.

For completeness rho is defined by this pointwise identity. All its possible coefficients are nonnegative: after fixing old membership (a,c) and final-tail membership (l,r), minimizing by direct substitution over the four first/middle tail bits gives the following COMPLETE 16-entry table.

| ac \\ lr | 00 | 01 | 10 | 11 |
|---|---:|---:|---:|---:|
|00|0|0|0|0|
|01|0|73/216|0|73/216|
|10|0|0|73/216|73/216|
|11|59/90|659/1080|659/1080|16/27|

The independent-from-discovery Fraction implementation audit_swap_payment.py expands every one of the 256 full membership states and checks the exact residual. This is a finite algebraic branch proof for arbitrary customer multiplicities, not a finite-game inference.

## Why this did not close HALF(5)

If Y is the actual suffix after its first two actions, the existing three-remaining-profit theorem gives V_Z<=(5/3)V_Y, but SWAP then pays only J<=14V_Y/9. That amount is much too large for a direct half argument, and repeated swaps reuse V_Y. It is not legitimate to add mutually exclusive V_Z values and call them actual early profits. The weighted-max coverage RESET in weighted_maximum_coverage_transfer.md is the useful subsequent direction: it pays a particular genuine H reset from its own retained near-saturation amount, while explicitly preserving old refunds. Cross-source payment of those retained amounts is still missing.

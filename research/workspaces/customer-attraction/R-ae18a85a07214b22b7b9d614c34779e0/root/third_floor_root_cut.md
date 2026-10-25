# A root rigidity cut retaining the third player's comparison to the terminal topic

2026-10-25. Exact coefficient proof for the five-player restriction of
Q-CAG-HALF. This is a necessary inequality for every complete ordered-history
pure SPE, not a half-coverage theorem, full SPE witness, external review, or
novelty claim. The parent independently checked all 128 customer memberships
in `parent/verify_root_cuts.py/.json`.

## Exact statement

Use precisely `research/current/customer_attraction/model.md`: finite unit
customers, finite nonempty common catalogue, five unit providers, arbitrary
complete-history pure SPE, empty and repeated topics, and arbitrary off-path
ties. Let `u` be the actual first provider's final payoff and
`K=max_(S in catalogue)|S|`. For every two legal topics `T,Q`,

\[
\boxed{763\left(|Q\setminus T|+\frac15|Q\cap T|\right)
\le11033u+2085K-4139|T|.}\tag{1}
\]

If `T` is a true maximum topic, (1) gives

\[
763F_T(Q)\le11033u-2054K.\tag{2}
\]

The coefficients of (1) improve the previous copy-reply line in a different
direction; no global domination is asserted. Its fixed-topic form cuts the
old floating shared-K point with objective about `2.0171836094`: on represented
topics `T=bits[5],Q=bits[3]`, the right minus left side of (1) is approximately
`-2.5833177246`. That point is a relaxation, not a full SPE.

## Genuine histories and nonnegative slacks

Force root `T` and follow the same original strategy, obtaining
`(T,A,B,C,D)`. At the genuine history `(T,A,B)`, force the fourth provider
to copy `D`, and let `E` be the same strategy's true last reply. The second
leaf is `(T,A,B,D,E)`. Write `r,v_B,v_C,v_D` for the first, third,
fourth, and fifth profits on the first leaf.

For each customer use binary indicators `t,a,b,c,d,q,e` and `p=t+a+b`.
Let `ell=p+c+d`, `ell'=p+d+e`, with zero-numerator shares defined as zero.
The following are nonnegative:

\[
\begin{aligned}
R&=u-r, &H_X&=K-|X|\quad(X=A,B,C,D),\\
J&=v_B-\sum_x\frac{d_x}{t_x+a_x+3},\\
L&=v_C-\sum_x\frac{d_x}{\ell'_x},\\
Z_Q&=v_D-\sum_x\frac{q_x}{p_x+c_x+1},
&Z_E&=v_D-\sum_x\frac{e_x}{p_x+c_x+1},\\
Y_Q&=\sum_x\frac{e_x}{\ell'_x}
-\sum_x\frac{q_x}{p_x+d_x+1}.
\end{aligned}
\]

`R` is root IC; `H_X` uses the common catalogue cap. `J` follows from
the third provider's genuine deviation to legal topic `D` at `(T,A)`: its
true last-two continuation can be arbitrary, but each customer of `D` has
final denominator at most `t+a+3`. `L` retains the true reply `E`, so it
does not freeze the last action. `Z_Q,Z_E` are last-provider comparisons
at the original history, while `Y_Q` is last-provider IC at the copied
history. These do not require anonymous histories, favorable tie-breaking,
or equilibrium of the deliberately forced fourth action.

## Exact certificate

Put `alpha=11033/763`, `beta=2085/763`, and `gamma=-4139/763`. For a
customer let `J_x,L_x,Z_Qx,Z_Ex,Y_Qx` be the above summands and define

\[
\begin{aligned}
\rho_x={}&\gamma t-\frac{q}{1+4t}+\alpha\frac t\ell
+\frac a2+\frac{1093}{1526}b+\frac{77}{109}c+\frac{618}{763}d\\
&-\frac{165}{763}J_x-\frac{180}{763}L_x
-\frac{673}{763}Z_{Qx}-\frac{135}{763}Z_{Ex}
-\frac{90}{763}Y_{Qx}.
\end{aligned}
\]

Direct expansion gives the identity

\[
\begin{aligned}
\alpha u+\beta K+\gamma|T|-F_T(Q)
={}&\alpha R+\frac12H_A+\frac{1093}{1526}H_B
+\frac{77}{109}H_C+\frac{618}{763}H_D\\
&+\frac{165}{763}J+\frac{180}{763}L
+\frac{673}{763}Z_Q+\frac{135}{763}Z_E
+\frac{90}{763}Y_Q+\sum_x\rho_x.
\end{aligned}\tag{3}
\]

The four cap weights sum exactly to `beta`. The coefficient of `q` in
`rho` is

\[
-\frac1{1+4t}+\frac{673}{763(p+c+1)}
+\frac{90}{763(p+d+1)}.
\]

It is nonpositive for `t=0` and nonnegative for `t=1`, so `q=1-t`
minimizes `rho`. The table gives all remaining values of `45780 rho`;
each is a nonnegative integer. It exhausts the exact binary membership
domain and proves (1) via (3).

|t|a|b|e|cd=00|cd=01|cd=10|cd=11|
|---|---|---|---|---:|---:|---:|---:|
|0|0|0|0|0|0|1350|30990|
|0|0|0|1|2700|0|0|26940|
|0|0|1|0|0|25590|25160|57330|
|0|0|1|1|1350|26040|25160|56430|
|0|1|0|0|0|19815|20210|49905|
|0|1|0|1|1350|20265|20210|49005|
|0|1|1|0|20210|48405|47235|79545|
|0|1|1|1|21110|48855|47460|79320|
|1|0|0|0|413640|103365|109590|29855|
|1|0|0|1|414990|103815|109590|28955|
|1|0|1|0|110490|28805|30550|8145|
|1|0|1|1|111390|29255|30775|7920|
|1|1|0|0|105540|21710|23950|225|
|1|1|0|1|106440|22160|24175|0|
|1|1|1|0|24700|0|0|0|
|1|1|1|1|25375|405|270|0|

## Optimal-query aggregate and open payment

For any five legal comparison topics covering `O`,
`sum_j F_T(T_j) >= |O|-(4/5)|T|`. Consequently (1) gives

\[
3815\operatorname{OPT}_5
\le275825u+52125K-100423|T|.
\]

Taking a true maximum source gives

\[
\boxed{3815\operatorname{OPT}_5+48298K\le275825u.}\tag{4}
\]

The same common `K` appears in every fixed or optimal-query row. These
rows do not close `OPT_5<=2W`. The new information beyond the previous
copy-reply certificate is the third provider's comparison to the terminal
topic on the true root branch; its exact continuation has not yet been
paid by this certificate.

`audit_third_floor_cut.py/.json` independently evaluates the raw summands
in rational arithmetic on all 128 types. `probe_query_reply.py/.json`
and `probe_third_true.py/.json` are floating discovery artifacts only;
they assert neither stronger exact inequalities nor SPE realizability.

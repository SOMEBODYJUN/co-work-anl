# Actual five-player obstruction to a local tail-surplus payment

2026-10-25. Exact author certificate, pending independent replay at writing.
This is an auxiliary-budget counterexample, **not** a half-coverage
counterexample. HALF(5), the global aggregate security bridge, and ONE-GAP
remain OPEN. No external review or novelty certification is asserted.

## Exact false strengthening

For a five-player complete-history pure SPE, let `q` be its actual first
three actions' customer load and `(D,E)` its actual final two actions.
Write

\[
U_q(T,R)=\sum_{x\in T}\frac1{q_x+1+\mathbf1_{x\in R}},\qquad
w(q)=\max_p\min_R\mathbb E_{T\sim p}U_q(T,R).
\]

Let `Phi(q)=sum_x H_(q_x)` and

\[
\Gamma_2(q)=\max_{T,R}\Phi(q+1_T+1_R)
             -\Phi(q+1_D+1_E).
\]

The proposed universal payment

\[
\Gamma_2(q)\le u_4+u_5-2w(q)
\tag{FALSE-LOCAL-SURPLUS}
\]

is false **on an actual five-player SPE path**, even though both final
players individually receive at least `w(q)`.

## Thirteen unit customers and four common topics

Each row is a disjoint class of distinct unit customers; compression creates
no nonunit player or customer values.

| Class | Multiplicity | Topics containing each customer |
| --- | ---: | --- |
| ab | 3 | A, B, X |
| c | 3 | C, X |
| ac | 1 | A, C, X |
| abc | 5 | A, B, C |
| x | 1 | X |

The complete ordered-history policy in
[actual_tail_surplus_policy.json](actual_tail_surplus_policy.json) has actual
path `X,X,C,B,C`, with final profits

\[
(u_1,u_2,u_3,u_4,u_5)=(5/2,5/2,8/3,8/3,8/3).
\]

It covers all thirteen customers, so `W=OPT_5=13`.
The policy specifies all `1+4+16+64+256=341` decision histories; no count-only
or favorable tie restriction is imposed. The exact direct replay checks all
`4*341=1364` one-action comparisons, including the prescribed action.

## Local minmax and potential certificates

The actual old prefix is `X,X,C`, hence `q=(0,0,1,2)` in topic-count notation.
The local payoff matrix, with both rows and columns ordered `A,B,C,X`, is

\[
U_q=\begin{pmatrix}
157/60&8/3&43/15&69/20\\
29/12&29/12&8/3&13/4\\
157/60&8/3&37/15&33/10\\
61/30&25/12&32/15&9/5
\end{pmatrix}.
\]

Pure row `A` guarantees `157/60`; pure column `A` bounds every row by
`157/60`. Thus `w(q)=157/60` with exact primal and dual certificates.

The two-action potential-increment matrix is

\[
P_q=\begin{pmatrix}
191/30&37/6&191/30&347/60\\
37/6&71/12&37/6&67/12\\
191/30&37/6&179/30&169/30\\
347/60&67/12&169/30&62/15
\end{pmatrix}.
\]

Its maximum is `191/30`; actual `(B,C)` gives `37/6`. Consequently

\[
\Gamma_2=1/5>1/10=16/3-2(157/60)=u_4+u_5-2w(q).
\]

## Scope: the original global safe value is smaller

The original five-player independent static security value is
`v_5=202/85`. A primal topic distribution is `(5,0,5,7)/17`. An exact dual
distribution on four-topic competitor count vectors is

| Competitor counts `(A,B,C,X)` | Probability |
| --- | ---: |
| `(1,0,1,2)` | `3/17` |
| `(1,0,2,1)` | `7/17` |
| `(2,0,1,1)` | `7/17` |

The script checks the primal against all 35 legal competitor count vectors,
and the dual against every topic, with `Fraction` arithmetic.
In particular the candidate

\[
u_1+u_2+u_3+\Gamma_2\ge3v_5
\]

holds here with slack `188/255`; the example does not refute it. It also
does not refute replacing `w(q)` by the smaller original `v_5` in
FALSE-LOCAL-SURPLUS.

## Reproduction and remaining obligation

Run `python actual_tail_surplus_certificate.py` from this directory, or pass
its full repository path. It constructs the policy, replays the JSON policy
directly, checks both minmax certificates and all sixteen potential entries,
and writes [actual_tail_surplus_audit.json](actual_tail_surplus_audit.json).
Its attainable-count recursion is used only to construct the policy; the
subsequent direct IC replay does not call that recursion.

The reusable information is a precise stopping boundary: even on a genuine
five-player path, one cannot charge the entire actual tail potential gap to
the tail's surplus above its **local** two-player safe value. A successful
global budget must use the original global safe value or preserve additional
cross-prefix credit. No full-tree payment of the early three roles was
established in this work.

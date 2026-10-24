# Customerwise continuation covariance is positive in a complete SPE

Status: exact auxiliary obstruction, 2026-10-24. This does not refute
Q-CAG-HALF, the free complete path-menu candidate, or the aggregate
same-query pushforward candidate. It rules out paying the continuation
covariance customer by customer merely from full successor IC.

## Definitions

At a fixed true decision history, force a legal action F and follow the same
complete pure strategy to its terminal Z(F). Set

\[
h_F(v)=c_v(Z(F))-\mathbf1_{v\in F},\quad q_v=\Pr_{F\sim p}(v\in F),
\]
\[
D_v=\mathbb E\frac{\mathbf1_{v\in F}}{h_F(v)+1},\qquad
C_v=\mathbb E\frac{q_v}{1+c_v(Z(F))}.
\]

For a customer with 0<q_v<1 let

\[
H_v^0=\mathbb E[(h_F(v)+1)^{-1}\mid v\notin F],\quad
H_v^1=\mathbb E[(h_F(v)+1)^{-1}\mid v\in F],
\]
\[
J_v^1=\mathbb E[((h_F(v)+1)(h_F(v)+2))^{-1}\mid v\in F].
\]

The existing exact debt identity is

\[
C_v-D_v=q_v(1-q_v)(H_v^0-H_v^1)-q_v^2J_v^1.
\]

## Four-customer complete SPE

There are two providers, four unit customers x,y,z,w, and common catalogue

\[
A=\{x,z\},\quad B=\{y\},\quad D=\{x,y\},\quad E=\{z,w\}.
\]

The last provider replies to first actions A,B,D,E with D,E,E,D respectively.
Here is its full payoff table; columns are its possible actions:

| First action | A | B | D | E | prescribed |
|---|---:|---:|---:|---:|---|
| A | 1 | 1 | 3/2 | 3/2 | D |
| B | 2 | 1/2 | 3/2 | 2 | E |
| D | 3/2 | 1/2 | 1 | 2 | E |
| E | 3/2 | 1 | 2 | 1 | D |

The first provider's true continuation payoffs after A,B,D,E are
3/2,1,2,2. Prescribe D at the root. These five nodes are every decision
history, so the table and root comparison prove a complete full-history
pure SPE. Its terminal is (D,E), utilities are (2,2), and W=OPT_2=4.

Take p(A)=p(B)=1/2. For customer x, the residual load is 1 after A and 0
after B, hence

\[
q_x=\tfrac12,\quad H_x^0=1,\quad H_x^1=\tfrac12,\quad
J_x^1=\tfrac16.
\]

Thus both proposed pointwise controls fail strictly:

\[
H_x^0-H_x^1=\tfrac12>0,\qquad
C_x-D_x=\tfrac18-\tfrac1{24}=\boxed{\tfrac1{12}}>0.
\]

Equivalently D_x=1/4 and C_x=1/3. Even the extra-slot collision discount
does not pay this customer's positive covariance. Any general payment
argument must be allowed to transfer credit between customers.

## Exact aggregate payment and the surviving obligation

The aggregate quantities at this root are D=5/4 and C=5/6, so D-C=5/12>0.
The example does not refute aggregate payment. In fact, the existing
last-successor identity explains exactly where the credit comes from.

Let L(F,F') be the last provider's genuine BR slack when, after F, it
compares its prescribed response with the response prescribed after F'.
Then E[L]=1/8. Let

\[
J=\mathbb E_F\sum_v
\frac{q_v\mathbf1_{v\in F}}{(h_F(v)+1)(h_F(v)+2)}.
\]

Here J=7/24 and the general one-successor formula gives

\[
D-C=\mathbb E L+J=\tfrac18+\tfrac7{24}=\tfrac5{12}.
\]

This formula follows by applying the known last-two decorrelation identity
to the root-deleted query and subtracting the extra-slot collision term.
It is valid for every background, common catalogue, query distribution,
and full-history last-player tie selection. It cannot be extended by
treating several successors as one player choosing their whole tuple:
that tuple is not a legal unilateral action.

The general all-input missing payment remains an aggregate comparison of
multi-successor harmonic-potential regret with root IC slack and collision
discounts. The present obstruction only shows that customerwise residual
monotonicity and customerwise nonpositive debt are unavailable.

## Tie-free variant

The obstruction does not rely on ties. Take unit customers
x,z,w_1,w_2,y_1,y_2,y_3 and catalogue

\[
A=\{x,z\},\quad B=\{y_1,y_2,y_3\},\quad
D=\{x,y_1,y_2,y_3\},\quad E=\{z,w_1,w_2\}.
\]

Use the same reply map and root D. Every last reply is now uniquely best,
and root D is uniquely best, with true root payoffs 3/2,3,4,3. The same
query distribution gives exactly the same x-wise calculations above.
Actual (D,E) covers all seven customers.

## Reproduction and targeted candidate test

`audit_customerwise_covariance.py` independently evaluates both complete
strategy trees using Fraction arithmetic and checks the displayed root
quantities. No equilibrium solver is imported.

`test_pushforward_cone.py` is a targeted numerical test of the separate
stronger candidate sum_i C_i(p)<=W on two existing fixed full-policy cones
(the 36-customer and 89-customer policies). It preserves all ordered-history
IC while varying customer multiplicities and alternates a query update.
It produced no violating witness. This supplies no universal conclusion;
it is retained only to reproduce the exact candidate test and avoid
mistaking the older root-deleted query counterexamples for extra-slot
counterexamples. It is not an additional mathematical result.

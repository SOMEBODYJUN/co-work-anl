# Background errors in positive pair circuits are incumbent rent losses

Research backup, 2026-10-21. Exact model and target: **CAG-MODEL / Q-CAG-HALF**, unchanged; the general half-coverage statement remains **OPEN**. These are universal local identities and inequalities, not a global SPE welfare bound. They extend the zero-background positive pair circuit in the peer asset `R-fa8dd4ddea574a74a634ebc71e6f9ccb/tree_coupling/pair_circuit_repair.md`.

## Exact pair circuit at an arbitrary fixed prefix

Fix any legal prefix multiset H, with customer loads h_x>=0. Let a,b be different catalog topics, and let r>=s>=1 be integers. Write U_a(H+r a+s b) for one a-provider's payoff in that terminal multiset, and set

\[
f_H(b)=\sum_{x\in b}\frac1{h_x+1}.
\]

Then

\[
\begin{aligned}
&rs\,U_a(H+r a+s b)+r(r-s)U_b(H+s a+r b)\\
&\quad=s^2U_a(H+s a+r b)+(r-s)f_H(b)+E_H^{r,s}(a,b).
\end{aligned}\tag{1}
\]

The nonnegative error is the sum of the following customer coefficients:

| Membership relative to a,b | Error coefficient |
| --- | ---: |
| neither | 0 |
| a only | (r-s)h s / ((h+r)(h+s)) |
| b only | (r-s)h(r-1) / ((h+r)(h+1)) |
| both | (r-s)h(r+s-1) / ((h+r+s)(h+1)) |

These formulas prove (1): substitute payoff coefficients 1/(h+r),1/(h+s), or 1/(h+r+s) in the four membership cases and subtract the displayed right side excluding E. Every error coefficient is nonnegative because h>=0 and r>=s>=1. The identity itself also holds with signed customer masses; nonnegativity of E uses nonnegative customer values. Earlier appearances of a or b inside H cause no problem, since their loads are already included in h.

For h=0 the error vanishes, recovering the peer zero-background circuit. Thus one must retain an error when transporting a pair circuit over an arbitrary existing prefix.

## Three active providers: a fixed-cohort rent identity

For r=2,s=1,

\[
2U_a(H+2a+b)+2U_b(H+a+2b)
=U_a(H+a+2b)+f_H(b)+E_H(a,b),\tag{2}
\]

where, writing l_x=1_{x in a}+1_{x in b},

\[
\boxed{E_H(a,b)=\sum_x h_x\left[\frac1{h_x+1}-\frac1{h_x+1+l_x}\right].}\tag{3}
\]

A term is zero unless that client is already covered by the prefix. Formula (3) follows from the table: l=1 gives h/((h+1)(h+2)), and l=2 gives 2h/((h+1)(h+3)).

It has an exact rent interpretation. Keep the H-providers as a fixed cohort and put one fictitious universal unit of load on every client. Their aggregate customer profit starts at h/(h+1). Inserting a and b reduces it to h/(h+1+l). Thus the pair-circuit error is precisely that fixed cohort's lost profit. The universal unit is an algebraic device, not a legal catalog action and not a new model assumption.

More generally, for an inserted load q define

\[
L_H(q)=\sum_x\frac{h_x}{h_x+1+q_x}.
\]

For any sequence of inserted profiles q^0<=...<=q^t,

\[
\sum_{j<t}\bigl[L_H(q^j)-L_H(q^{j+1})\bigr]
=L_H(q^0)-L_H(q^t).
\]

This exact telescope keeps the original cohort H fixed. It does not justify telescoping E_{H+q^j} as if the numerator were still h: newly inserted providers have their own rent and would need a separate payment.

## Positivity of the three-active error for common submodular Shapley games

The rent identity (3), and its positivity for r=2,s=1, extend beyond nonnegative coverage-customer representations. Let C(empty)=0 be one common monotone submodular set function, with common Shapley payoffs on repeated topic labels. A truncated C on supports of size at most m is sufficient when every profile below has at most m providers.

Add an auxiliary label Omega and set C(S union {Omega})=K for all retained S, where K is at least every retained C-value. Leave C unchanged on sets omitting Omega. This extension is monotone and submodular. If only one of the two sets in a submodularity inequality contains Omega, that inequality reduces to C(Y)>=C(X intersection Y), which follows from monotonicity. If both contain Omega it is equality; if neither does, it is the original inequality.

Let U_j denote the extended common Shapley payoff of each fixed H-provider j. Then the exact identity is

\[
E_H(a,b)=\sum_{j\in H}\left[U_j(H+\Omega)-U_j(H+\Omega+a+b)\right].\tag{6}
\]

Here each repeated H-provider is counted separately. To establish (6), take any signed customer representation of the common set function, put Omega into every customer interest set, and if necessary add an Omega-only signed mass to change C(P) to K. The latter mass never affects an H-provider. For each signed customer, (6) is precisely (3); linearity proves it for the common set function. This signed calculation establishes the identity only, not positivity.

Positivity now has a separate argument. Under nonnegative decreasing Shapley marginals, increasing the counts of other topic labels decreases an incumbent's payoff by the clock coupling. Increasing the count of its own label also decreases the payoff, by the larger own kill rate. Thus adding a and b weakly reduces each fixed H-provider's extended payoff. Every summand in (6) is nonnegative, proving E_H(a,b)>=0 for common monotone submodular Shapley games.

This construction is entirely algebraic: Omega is not asserted to be an available action, and no SPE comparison uses it. Both extended profiles have at most |H|+3 providers, so the argument stays within the truncated domain. The parent and tree_coupling researchers independently reconstructed the extension and positivity argument. It still does not preserve original SPE incentives under the client filter below.

## Shared-pivot transport and the incentive filter

For a third topic c, subtract the errors for a,b and c,b. The table yields the exact identity

\[
\boxed{
E_H^{r,s}(a,b)-E_H^{r,s}(c,b)
=s(r-s)\sum_x\frac{h_x}{h_x+r}
\frac{1_{x\in a}-1_{x\in c}}{h_x+s+r1_{x\in b}}.
}\tag{4}
\]

To check it, clients outside b have coefficient (r-s)hs/((h+r)(h+s)); clients inside b have coefficient

\[
(r-s)h\left[\frac{r+s-1}{(h+r+s)(h+1)}-
\frac{r-1}{(h+r)(h+1)}\right]
=\frac{(r-s)hs}{(h+r+s)(h+r)}.
\]

The same filter rho_r(h)=h/(h+r) therefore applies independently of whether the pivot b covers the client.

For s=1, the unfiltered sum is a genuine last-provider a-versus-c payoff difference at a prefix consisting of H and r copies of b. Suppose the given full SPE selects c at that ordered history. Define

\[
P_H^r(a,b)=rU_a(H+r a+b)+r(r-1)U_b(H+a+r b).
\]

The actual last-provider inequality and (1),(4) imply the valid budgeted transport

\[
\boxed{
P_H^r(a,b)\le P_H^r(c,b)+
(r-1)\sum_{x\in a\setminus c}
\frac{h_x}{(h_x+r)(h_x+1+r1_{x\in b})}.
}\tag{5}
\]

Proof: P(a,b)-P(c,b) is the unfiltered payoff difference (nonpositive by the true SPE comparison), plus (r-1) times its rho_r-filtered difference. Drop the filtered negative coefficients, retaining only clients in a minus c. Every remaining client is covered by H. This uses the actual prescribed reply c; it does not freeze a different continuation or change tie rules.

For the important r=2 case the charge per such customer is at most 1/6. Indeed h/((h+1)(h+2))<=1/6 for integer h>=0, since (h-1)(h-2)>=0 for integral h; pivot membership can only enlarge the denominator. For general r>=1 it is at most

\[
\frac{\sqrt r-1}{\sqrt r+1}<1,
\]

because (h+r)(h+1)>=(sqrt r+1)^2 h, with difference (h-sqrt r)^2. These are local one-transport bounds; repeated charges on the same client are not yet controlled.

## What remains missing globally

The filtered payoff difference in (4) need not have the sign of its unfiltered SPE incentive. Multiplying different client types by different positive factors does not preserve an aggregate inequality. Consequently one cannot invoke SPE of an auxiliary reweighted game without a separate proof.

Equation (5) confines the error to clients already covered by the chosen prefix. A possible global route would construct genuine full-tree transports and charge each such client's incumbent rent a controlled number of times, using a fixed-cohort telescope or another conservation rule. No such global routing is proved here. In particular, neither (1) nor (5) supplies F(T)<=W+G_alpha or mM<=W+G_alpha, and neither proves Q-CAG-HALF.

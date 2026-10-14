# Independent parameter audit for the odd-ring certificate

This note was derived from the displayed certificate formulas before reading
the construction proof. It is an internal mathematical review, not a claim of
external review or novelty. It checks the parameter and coefficient interface;
the separate ring argument is responsible for covering every pure state.

## Certificate interface

For each ring index $i\in\mathbb Z/m\mathbb Z$, let $x_i,t_i>0$,
$n_i\in\mathbb Z_{\ge1}$, and $0\le k_i\le d$. Put

\[
\begin{split}
N_i&=(1+x_i)^{k_i}-\alpha(n_i x_i)^{k_i},\\
M_i&=\alpha(1+n_i x_i)^{k_i}-1,\\
P_i&=\alpha(1+t_i)^d-t_i^d,\\
Q_i&=(1+t_i)^d-\alpha.
\end{split}
\]

The interface requires all four quantities to be positive, weight consistency
$\prod_i x_i=\prod_i t_i$, and the strict inequality

\[
T=\prod_i\frac{n_iN_iQ_i}{M_iP_i}>1. \tag{1}
\]

## A complete uniform check of the proposed dyadic parameters

Let $s\in\mathbb Z_{\ge6}$, $r=2^s$, $d_s=2sr$,
$\alpha=r/4$, and let $m$ be the least odd integer at least $s$.
Thus $s\le m\le s+1$. Choose

\[
x_0=r^{-(2m-1)},\quad
n_0=\left\lfloor\frac{r^{2m-1}}s\right\rfloor,\quad k_0=s;
\qquad
x_i=r,\ n_i=1,\ k_i=d_s\quad(1\le i<m),
\]

and $t_i=1/r$ at every index. Set $B=r^{2m-1}$.
The degree restriction $s\le d_s$ is immediate, and every displayed
parameter is rational except the integer quantities, which are integral.

Weight consistency holds exactly:

\[
\prod_i x_i=r^{-(2m-1)}r^{m-1}=r^{-m}=\prod_i t_i.
\]

For a concrete realization, take $u_0=1$,
$u_i=r^{-2(m-i)}$ for $1\le i<m$, and $v_i=x_i u_i$.
Then $v_i/u_i=x_i$, $v_i/u_{i+1}=t_i$, including the cyclic last
index, with $u_m=u_0$. All weights are strictly positive rational numbers.

Write $A=(1+1/r)^{d_s}$. The binomial theorem gives
$(1+1/r)^r\ge2$, hence

\[
A=\bigl((1+1/r)^r\bigr)^{2s}\ge2^{2s}=r^2.
\]

Consequently the common values $Q=A-\alpha$ and
$P=\alpha A-r^{-d_s}$ are positive. Moreover

\[
\frac QP>
\frac{A-\alpha}{\alpha A}
\ge\frac{1-1/(4r)}\alpha
\ge\frac3r. \tag{2}
\]

For every ordinary index, $N_i=r^{d_s}Q>0$ and
$M_i=r^{d_s}P>0$; its contribution to (1) is $(Q/P)^2$.
For the exceptional index, $n_0/B\le1/s$, so

\[
N_0\ge1-\frac{\alpha}{s^s}
=1-\frac14(2/s)^s
\ge1-\frac1{2916}>\frac12.
\]

Also $M_0\ge\alpha-1>0$ and

\[
M_0\le\alpha(1+1/s)^s-1<3\alpha.
\]

Here the elementary bound $(1+1/s)^s<3$ follows from its binomial
expansion and $j!\ge2^{j-1}$ for $j\ge2$, without needing a numerical
value of $e$. Since $B/s\ge r/s\ge2$, the floor obeys

\[
n_0=\lfloor B/s\rfloor\ge B/(2s)>0.
\]

Combining these estimates with (2) proves

\[
\begin{split}
T
&=n_0\frac{N_0}{M_0}\left(\frac QP\right)^{2m-1}\\
&>\frac{r^{2m-1}}{2s}\frac1{6\alpha}
\left(\frac3r\right)^{2m-1}
=\frac{3^{2m-2}}{sr}
\ge\frac{3^{2s-2}}{s2^s}>1.
\end{split}
\]

The last expression is $59049/384>1$ at $s=6$, and its ratio at
successive integers is $9s/(2(s+1))>1$. This proves (1) for every
integer $s\ge6$, with the oddness, floor, degree, strictness, and sign
obligations explicit.

## Extension to every integer degree at least 768

For $D\in\mathbb Z_{\ge768}$, let $s\ge6$ be the largest integer for
which $d_s\le D$. A degree-$d_s$ instance is also a degree-at-most-$D$
instance. Since

\[
D<d_{s+1}=4(s+1)r,
\qquad
\log_2D\ge\log_2d_s=s+1+\log_2s>s+1,
\]

we obtain the strict bound

\[
\alpha=\frac r4>\frac D{16\log_2D}.
\]

If the ring lemma converts (1) into a strict improving deviation of factor
$\alpha$ at every pure state, the same instance excludes every smaller
factor as well. This note does not replace that all-states lemma.

## A ceiling on the entire positive-product certificate mechanism

There is a parameter-independent obstruction for this certificate, not just
for the dyadic choice. Assume $d\ge1$, $\alpha>1$, $n_i\ge1$,
$k_i\in\{0,\ldots,d\}$, all $N_i,M_i,P_i,Q_i>0$, and consistency.
Let

\[
\tau=\alpha^{1/d}-1>0,\qquad y_i=n_i x_i\ge x_i.
\]

Positivity of $N_i$ excludes $k_i=0$. For $k_i\ge1$, it gives

\[
\alpha^{1/k_i}y_i<1+x_i\le1+y_i,
\quad\text{so}\quad
y_i<\frac1{\alpha^{1/k_i}-1}\le\frac1\tau.
\]

Because $N_i<(1+y_i)^{k_i}$ and
$M_i\ge(\alpha-1)(1+y_i)^{k_i}$,

\[
x_i\frac{n_iN_i}{M_i}
=y_i\frac{N_i}{M_i}
<\frac1{(\alpha-1)\tau}. \tag{3}
\]

Similarly, $Q_i>0$ gives $t_i>\tau$, while
$Q_i<(1+t_i)^d$ and
$P_i\ge(\alpha-1)(1+t_i)^d$ give

\[
\frac{Q_i}{t_iP_i}<\frac1{(\alpha-1)\tau}. \tag{4}
\]

Consistency lets us multiply (3) and (4) without changing (1):

\[
T=\prod_i
\left(x_i\frac{n_iN_i}{M_i}\right)
\left(\frac{Q_i}{t_iP_i}\right)
<\bigl((\alpha-1)\tau\bigr)^{-2m}.
\]

Thus the certificate $T>1$ has the necessary condition

\[
(\alpha-1)(\alpha^{1/d}-1)<1,
\qquad\text{and therefore}\qquad
(\alpha-1)\ln\alpha<d. \tag{5}
\]

The latter follows from $e^z-1\ge z$. Since the positive root of
$(a-1)\ln a=d$ is asymptotic to $d/\ln d$, this certificate mechanism
can achieve at most $(1+o(1))d/\ln d$. This is not an upper bound on
the universal equilibrium threshold, nor on every possible use of the same
game topology: it bounds exactly the positive quantities and product
conditions stated above. In particular, an $\omega(d/\ln d)$ lower
bound would require a different certificate mechanism.

## Exact finite checks

`check_parameters.py` uses only Python integer arithmetic. It checks the
original rational expressions for $s=6,7,8$, not merely the estimates
above, by clearing every denominator. The computation is finite evidence;
the preceding inequalities are the proof for all $s\ge6$.

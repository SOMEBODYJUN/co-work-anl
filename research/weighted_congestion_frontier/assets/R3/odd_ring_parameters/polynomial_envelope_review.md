# Independent review: nonnegative polynomial shapes do not enlarge the envelope

## Exact statement and scope

Fix an integer $d\ge2$ and $\alpha>1$. Ring index $i$ has positive
weights $u_i,v_i$, an integer cohort size $n_i\ge1$, and two nonzero
polynomials

$$
F_i(z)=\sum_{k=0}^d c_{i,k}z^k,\qquad
G_i(z)=\sum_{k=0}^d e_{i,k}z^k,\qquad c_{i,k},e_{i,k}\ge0.
$$

Shapes may differ at every ring index and between $F_i$ and $G_i$.
Within group $i$, the action copies of its $A_i$ resources use the same
shape $F_i$; all cohort resources $B_{ij}$ and their action copies use the
same shape $G_i$, as in the original two-test interface. Positive scalar
amplitudes can be selected separately at each group. This theorem does not
silently extend the interface to action-asymmetric resources or
clone-specific shapes.

Set $x_i=v_i/u_i$, $t_i=v_i/u_{i+1}$, with cyclic indexing, and define
the actual shape differences

$$
\begin{aligned}
N_i&=F_i(u_i+v_i)-\alpha F_i(n_iv_i),\\
M_i&=\alpha F_i(u_i+n_iv_i)-F_i(u_i),\\
P_i&=\alpha G_i(u_{i+1}+v_i)-G_i(v_i),\\
Q_i&=G_i(u_{i+1}+v_i)-\alpha G_i(u_{i+1}).
\end{aligned}
$$

If $N_i,Q_i>0$ and

$$
\prod_i\frac{n_iN_iQ_i}{M_iP_i}>1,
$$

then necessarily $\alpha<T_d$, where

$$
T_d=\max_{R>1}\frac{R(1+R)^d+1}{(1+R)^d+R^{d+1}}.
$$

Conversely, the monomial construction already establishes feasibility of
the same strict tests for every $\alpha<T_d$ (using a rational larger
factor when needed). Thus allowing nonnegative polynomial mixtures does
not change the exact threshold of this sufficient certificate interface.
The proof below is independent of numerical searches.

## Denominators and boundary cases

For nonzero $F_i,G_i$, monotonicity at positive arguments gives
$M_i>0$ and $P_i>0$, since $\alpha>1$. More explicitly, each monomial
denominator introduced below is strictly positive, including degree zero.

A zero $F_i$ has $N_i=M_i=0$, so it cannot satisfy the strict light test
$a_iN_i>b_iP_i$, whose right side is nonnegative. A zero $G_i$ has
$P_i=Q_i=0$, so it cannot satisfy the strict following-hub test
$n_ib_iQ_i>a_{i+1}M_{i+1}$, whose right side is nonnegative.
Consequently zero shapes cannot be used to rescue feasibility, and no
undefined $0/0$ is evaluated. Constant nonzero shapes have negative $N_i$
or negative $Q_i$ and hence fail their own positive-sign requirement.
Constants inside a mixture remain permitted and are handled below.

## The two exact convex combinations

Suppress index $i$, and write $x=v/u$, $t=v/u_{\rm next}$, $n=n_i$.
For each $k\in\{0,\ldots,d\}$ put

$$
\begin{aligned}
N_k&=(1+x)^k-\alpha(nx)^k,&
M_k&=\alpha(1+nx)^k-1,\\
P_k&=\alpha(1+t)^k-t^k,&
Q_k&=(1+t)^k-\alpha.
\end{aligned}
$$

All $M_k,P_k$ are positive, even when $k=0$.
The exact expansions are

$$
N=\sum_k c_ku^kN_k,\quad M=\sum_k c_ku^kM_k,\qquad
Q=\sum_k e_ku_{\rm next}^kQ_k,\quad
P=\sum_k e_ku_{\rm next}^kP_k.
$$

Define

$$
\mathcal F_{k,n}(x)=nx\,\frac{N_k}{M_k},\qquad
\lambda_k=\frac{c_ku^kM_k}{M},\qquad
\mu_k=\frac{e_ku_{\rm next}^kP_k}{P}.
$$

The $\lambda_k$ and $\mu_k$ are nonnegative and each family sums to 1.
There is no need to assume individual $N_k,Q_k$ are positive. We have
the exact convex identities

$$
xn\,\frac NM=\sum_k\lambda_k\mathcal F_{k,n}(x),\qquad
\frac Q{tP}=\sum_k\mu_k\mathcal F_{k,1}(1/t).
$$

The second follows by multiplying its monomial numerator and denominator
by $t^{-k}$. At $k=0$ the factors are exactly
$\mathcal F_{0,n}(x)=-nx$ and
$\mathcal F_{0,1}(1/t)=-1/t$. These negative terms cannot invalidate an
upper bound on a convex combination.

## The uniform monomial bound and multiplication

For $y=nx\ge x$,

$$
\mathcal F_{k,n}(x)
\le\mathcal F_{k,1}(y).
$$

The denominators are identical and positive, while
$(1+x)^k\le(1+y)^k$. For $k\ge1$,
$\mathcal F_{k,1}(y)>1$ is equivalent to $\alpha<f_k(y)$.
The independent exact-envelope proof establishes $f_k(y)\le1$ for
$0<y\le1$, and $f_k(y)\le f_d(y)\le T_d$ for $y>1$,
$k\le d$. The degree-zero factor is negative. Therefore, if
$\alpha\ge T_d$, every monomial factor in both convex combinations is
at most 1, and

$$
xn\,\frac NM\le1,\qquad \frac Q{tP}\le1.
$$

The positive weights satisfy $\prod_i x_i=\prod_i t_i$ identically.
Since the certificate assumes $N_i,Q_i>0$, both normalized local factors
are positive. Multiplying yields

$$
\prod_i\frac{n_iN_iQ_i}{M_iP_i}
=\prod_i\left(x_in_i\frac{N_i}{M_i}\right)
 \prod_i\left(\frac{Q_i}{t_iP_i}\right)\le1,
$$

contradicting the required strict product. This proves the claimed ceiling
with resource-specific group shapes, arbitrary degree mixtures, constants,
and arbitrary positive real weights.

An equivalent proof avoids convex division: at $\alpha\ge T_d$ the
monomial inequalities $nxN_k\le M_k$ and $Q_k/t\le P_k$ can be
multiplied by their nonnegative shape coefficients and summed directly.
This also makes clear why signed monomial differences are harmless.

## What remains open for the actual topology

The proof establishes necessity for the two uniform local tests. It does
not establish that every game on this topology has a $T_d$-PNE.
The aligned-light test uses a lower bound on current cost and an upper
bound on deviation cost, uniformly over all cohort and neighboring hub
actions. Failure of this test does not determine the actual light's
improvement at a particular state. Further, some states can be covered by
another hub or light even when the selected uniform test fails.

To turn this envelope into an existence theorem for the whole topology,
one must prove an additional reduction: whenever these positive two-test
certificates are infeasible at $\alpha$, there is an actual pure state in
which every player satisfies its $\alpha$-PNE inequality. No such reduction
follows from a product bound or from the convex identities.

An informative subcase is an all-anti-aligned state with exactly one equal
hub edge, which exists on any odd binary ring. Every hub away from that
equal edge faces an increase in both its outgoing $A$ load and incoming
$B$ loads after flipping. The hub at the equal edge has the exact hub test.
But anti-aligned lights can still prefer to align: their outgoing $B$ load
can fall at the equal edge, and with a large cohort their $A$ load can fall
as well. Thus merely finding a failed hub test does not automatically
produce equilibrium. Controlling these reverse light deviations and
partially aligned cohorts is a concrete missing obligation.

For $d=1$, the monomial envelope equals 1 and the same argument excludes
such certificates at every $\alpha>1$. For $d=0$, positive $N_i,Q_i$
are impossible. No endpoint statement at $\alpha=1$ is inferred by
dividing the degree-zero denominators, which vanish there.

The companion check_polynomial_envelope.py verifies the exact convex
identities, the monomial comparisons, constants, and zero-shape exclusions
using rational arithmetic. Its finite checks supplement the proof and do
not settle the actual-topology existence question.

For clarity, its test factor $\alpha=d$ is certainly above $T_d$.
Indeed, subtract the numerator of $f_d(R)$ from $d$ times its denominator.
The constant and degree-$(d+1)$ coefficients are both $d-1>0$.
The intermediate degree-$j$ coefficient is
$d\binom dj-\binom d{j-1}\ge0$, since
$\binom d{j-1}/\binom dj=j/(d-j+1)\le d$.
Thus $f_d(R)<d$ for all $R>0$; because its maximum at $R>1$ is
attained, $T_d<d$.

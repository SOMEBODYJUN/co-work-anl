# Independent review of the exact certificate envelope

Scope: this note bounds and attains the positive-product certificate
interface, assuming the separate all-states odd-ring reduction. It does not
prove a universal equilibrium upper bound. The initial parameter audit was
independent; the exact-envelope optimization was independently developed by
the delegated agent and then checked by this reviewer. The rational special
block below is the parent's subsequently supplied simplification.

For $d\ge2$, define

$$
f_d(R)=\frac{R(1+R)^d+1}{(1+R)^d+R^{d+1}},\qquad
T_d=\max_{R>1}f_d(R).
$$

The maximum exists: $f_d$ is continuous, $f_d(1)=1$, its limit at infinity
is 1, and $f_d(2)>1$. This last inequality also follows from
$2(1+2)^d+1>(1+2)^d+2^{d+1}$ for $d\ge2$.

## Exact necessity for the whole certificate interface

Fix $\alpha>1$. Let

$$
F_{k,n}(x)=nx\,\frac{(1+x)^k-\alpha(nx)^k}
                    {\alpha(1+nx)^k-1}.
$$

Assume the certificate signs and $n\ge1$. Positivity excludes $k=0$.
Writing $y=nx\ge x$, comparison of numerators with the same positive
denominator gives $F_{k,n}(x)\le F_{k,1}(y)$. Also,

$$
F_{k,1}(y)>1
\quad\Longleftrightarrow\quad
\alpha<f_k(y).
$$

For $0<y\le1$, $f_k(y)\le1$. Indeed,
$(1-y)(1+y)^k\ge1-y^{k+1}$, since the binomial coefficients in
$(1+y)^k$ are all at least 1. At $y=1$ equality holds.

For $y>1$, $f_k(y)$ is nondecreasing in $k\ge0$. For clarity, set
$A=(1+y)^k$ and $B=y^{k+1}$. Clearing the positive denominators in
$f_{k+1}(y)-f_k(y)$ gives

$$
yA(B-1)-(y-1)B
=(y-1)\left[yA\sum_{j=0}^{k}y^j-B\right]\ge0.
$$

The inequality is strict for $k\ge1$ and is an equality for $k=0$.
Consequently, if $\alpha\ge T_d$, all $F_{k,n}(x)\le1$ whenever
$1\le k\le d$. The identity

$$
\frac{Q_i}{t_iP_i}=F_{d,1}(1/t_i)
$$

and weight consistency give

$$
\prod_i\frac{n_iN_iQ_i}{M_iP_i}
=\prod_i F_{k_i,n_i}(x_i)\prod_iF_{d,1}(1/t_i)\le1.
$$

Thus $\alpha<T_d$ is necessary for this strict positive-product
certificate, even with unrestricted heterogeneous parameters.

## Exact rational sufficiency

Take rational numbers $a>1$ and $R>1$ with $a<f_d(R)$. Write

$$
E=(1+1/R)^d,\qquad
q=\frac{E-a}{aE-R^{-d}},\qquad B=\lceil4ad\rceil.
$$

The denominator is positive. Rewriting $a<f_d(R)$ shows $Rq>1$,
which also proves $E-a>0$; comparison of denominator and numerator shows
$0<q<1$. Choose the least odd integer $m\ge3$ such that
$(Rq)^{2m-1}>12Ba$. This is a terminating exact rational search.
Put $L=2m-1$ and

$$
x_0=R^{-L},\quad n_0=\lfloor R^L/B\rfloor,\quad k_0=d,
\qquad
x_i=R,\ n_i=1,\ k_i=d\quad(i\ne0),
\qquad t_i=1/R\quad(\text{all }i).
$$

The products of $x_i$ and $t_i$ both equal $R^{-m}$. All weights can be
realized rationally by $u_0=1$, $u_i=R^{-2(m-i)}$ for $1\le i<m$,
and $v_i=x_i u_i$.

For the exceptional block, $n_0x_0\le1/B$ gives

$$
N_0\ge1-\frac a{B^d}\ge1-\frac aB
\ge1-\frac1{4d}\ge\frac34,
$$

while $0<M_0<a(1+1/B)^d<ae^{d/B}<ea$. Since
$R^L>(Rq)^L>12Ba>2B$, the floor satisfies $n_0\ge R^L/(2B)$.
The ordinary block ratio $N_i/M_i$ and every $Q_i/P_i$ equal $q$,
so

$$
\prod_i\frac{n_iN_iQ_i}{M_iP_i}
=n_0\frac{N_0}{M_0}q^L
>\frac{(Rq)^L}{4Bea}>\frac3e>1.
$$

All signs are positive. Every resource degree in this variant can equal
$d$; smaller-degree padding is unnecessary.

For any real $1\le\alpha<T_d$, continuity and density provide rational
$a,R>1$ with $\alpha<a<f_d(R)$. A strict all-state certificate at $a$
also excludes $\alpha$. Therefore, after the separate ring reduction is
verified, this proves $a_*(d)\ge T_d$ with rational data, at every integer
$d\ge2$. Endpoint attainment at $T_d$ is neither claimed nor needed.

## Almost closed form and asymptotics

Write $f_d(R)=g_d(R)+\varepsilon_d(R)$, where

$$
g_d(R)=\frac{R(1+R)^d}{(1+R)^d+R^{d+1}},
\qquad
0<\varepsilon_d(R)=\frac1{(1+R)^d+R^{d+1}}
<\frac1{2^d+1}.
$$

With $z=d/R$, the reciprocal is

$$
\frac d{g_d(R)}
=h_d(z)=z+d(1+z/d)^{-d}.
$$

Here $h_d''(z)>0$ and
$h_d'(z)=1-d(1+z/d)^{-d-1}$, so the unique minimum occurs at
$z_*=d(d^{1/(d+1)}-1)$. Its corresponding
$R_*=(d^{1/(d+1)}-1)^{-1}$ is greater than 1, since
$d<2^{d+1}$. Therefore

$$
H_d:=\max_{R>1}g_d(R)
=\frac{d}{(d+1)d^{1/(d+1)}-d},
\qquad
H_d<T_d\le H_d+\frac1{2^d+1}.
$$

If $\lambda=\ln d$, Taylor expansion with its usual positive exponential
remainder gives

$$
(d+1)e^{\lambda/(d+1)}-d
=1+\lambda+\frac{\lambda^2}{2(d+1)}
 +O(\lambda^3/d^2),
$$

and hence

$$
H_d=\frac d{\lambda+1}
-\frac{d}{d+1}\frac{\lambda^2}{2(\lambda+1)^2}
 +O(\lambda/d)
=\frac d{\ln d+1}-\frac12+o(1).
$$

The exponentially small difference between $T_d$ and $H_d$ yields the
same expansion for $T_d$. Thus the certificate mechanism has an exact
finite-degree envelope and achieves the leading constant 1 in
$d/\ln d$. Changing ordinary exponents, ring length, or heterogeneous
parameters cannot improve that leading constant within this interface.

## Review objections and disposition

- This necessity concerns the stated positive-product certificate, not all
  games or all proof methods on a ring topology.
- The universal lower bound still depends on strict improvement at every
  pure state; the product alone does not establish that game-theoretic step.
- The rational search terminates because $Rq>1$; no numerical approximation
  to logarithms or roots is needed to construct its finite instance.
- For $d=1$, $f_1(R)=1$ identically, so this mechanism provides no lower
  factor above 1. The exact-envelope claim starts at $d=2$.
- No literature priority or novelty conclusion is inferred from this audit.

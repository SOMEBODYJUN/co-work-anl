# Independent audit of the stronger integer family

The parent supplied this family after the initial independent dyadic audit.
Every estimate below was reconstructed separately. Its significance is a
rational-data leading-constant-one lower family; the exact envelope review
gives a stronger finite-degree formulation.

For each integer $r\ge64$, put

$$
\ell=\lceil\ln r\rceil,\quad t=\lfloor\sqrt\ell\rfloor,\quad
d_r=r(\ell+4t),\quad a_r=\frac{rt}{t+1}.
$$

Let $m$ be the least odd integer at least $6t\ell$, and let $k$ be the
least positive integer such that $t^k\ge2r$. Use

$$
x_0=r^{-(2m-1)},\quad n_0=\lfloor r^{2m-1}/t\rfloor,\quad k_0=k;
\qquad
x_i=r,\ n_i=1,\ k_i=d_r\ (i\ne0),\qquad t_i=1/r.
$$

All the weights and $a_r$ are rational. The $t$ without index is an
integer; $t_i$ is a weight ratio. The product constraint holds exactly.

For $r\ge64$, $\ell\ge5$, $t\ge2$, and
$\ell<\ln r+1\le r/4$. The final inequality follows since
$r/4-\ln r-1$ is increasing for $r\ge64$ and is positive at 64,
using $\ln64<6$. Thus $t\le\sqrt r/2$. Also

$$
k<\frac{\ln(2r)}{\ln t}+1
\le\frac\ell{\ln2}+2
<\frac32\ell+2,\qquad
\frac kt<\frac34\ell+1<\ell.
$$

Here $\ln2>2/3$ follows by integrating the strict tangent lower bound
for the convex function $1/x$ on $[1,2]$. Hence $k<d_r$.

Set $E=(1+1/r)^{d_r}$. The inequality
$\ln(1+1/r)>1/(r+1)$ and
$\ell\le r/4<(r-3)t$ give

$$
\ln E>\ell+4t-\frac{\ell+4t}{r+1}>\ell+3t,
\qquad E>re^{3t}.
$$

With $Q=E-a_r$ and $P=a_rE-r^{-d_r}$, both are positive. Furthermore

$$
r\frac QP>
\frac r{a_r}\left(1-\frac{a_r}E\right)
>\left(1+\frac1t\right)(1-e^{-3t})
>1+\frac1{2t}.
$$

The last step follows from $e^{3t}>1+3t>2(t+1)$ for $t\ge2$.
Since $m\ge6t\ell$ and
$\ln(1+1/(2t))>1/(2t+1)$,

$$
\left(r\frac QP\right)^{2m-1}
>\exp\left(\frac{2m-1}{2t+1}\right)
>e^{3\ell}\ge r^3.
$$

Indeed $12t\ell-1>3\ell(2t+1)$ for $t\ge2,\ell\ge5$.

For the exceptional index, $n_0x_0\le1/t$ and
$a_r<r\le t^k/2$, so $N_0>1/2$. Also

$$
0<M_0<a_r(1+1/t)^k<a_re^{k/t}<a_re^\ell.
$$

Writing $B=r^{2m-1}$, the bound $t\le\sqrt r/2$ gives $B/t>2$,
so $n_0\ge B/(2t)$. The certificate product therefore satisfies

$$
T=n_0\frac{N_0}{M_0}\left(\frac QP\right)^{2m-1}
>\frac{r^3}{4ta_re^\ell}
>\frac r{4et}
\ge\frac{\sqrt r}{2e}>\frac43>1.
$$

The final inequalities use $e^\ell<er$, $a_r<r$, $r\ge64$, and $e<3$.
The ordinary $N_i,M_i$ equal $r^{d_r}Q,r^{d_r}P$ and are positive.
Every strictness, floor, sign, degree, and odd-ring obligation is thus
explicit.

The sequence $d_r$ strictly increases. In one step, $\ell$ and $t$ can
each increase by at most one, giving

$$
1<\frac{d_{r+1}}{d_r}
\le(1+1/r)\left(1+\frac5{\ell+4t}\right)\longrightarrow1.
$$

Also $d_r\sim r\ln r$, $\ln d_r\sim\ln r$, and $a_r\sim r$.
For every integer $D\ge832=d_{64}$, use the largest $r$ with
$d_r\le D<d_{r+1}$. Nesting of the degree classes then yields

$$
\frac{a_r\ln D}{D}\longrightarrow1.
$$

This inference still assumes the separate all-states odd-ring reduction.
It is a lower construction and a parameter proof, not an equilibrium
existence upper bound or an independently established novelty claim.

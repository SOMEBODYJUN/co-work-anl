# Independent review of the shrinking-weight Boolean limit

Review identity: R3 internal independent reconstruction, 2026-10-14. This review concerns a new scaling family, not the separately checked degree-32 game. The reviewer read the exact `MODEL.md`, independently rebuilt the auxiliary game, its costs and its witnesses, and only afterwards read `crossover_audit/verify_limit.py`. At that first inspection, `limit_family.md` did not yet exist; its full subsequently completed text was then reviewed. This review does not constitute external peer review.

## Verdict and scope

The stated auxiliary game has no 2-PNE for the positive amplitudes

\[
(a,b,c,d,e,f,g)=(49/100,11/10,49/100,3/5,1/50,3/100,1).
\]

Its exact best equilibrium factor is \(100/49\); it has no \(\alpha\)-PNE precisely for \(1\leq\alpha<100/49\). The endpoint is attained by four states in this finite auxiliary game. The auxiliary game itself is not being claimed to have polynomial congestion latencies.

The specified weights \((1,1/(10m),1/(20m),1/(50m))\), first-six-pair degree \(32m^2\), and last-pair degree 2 do transport every selected strict inequality for all sufficiently large integer \(m\). A separate explicit bound below certifies all \(m\geq20\). Thus there is a genuine infinite family of four-player, fourteen-resource polynomial congestion games with no 2-PNE. The construction has fixed player count and provides a constant lower bound. It provides no lower bound growing without limit in degree.

The retuned amplitudes do **not** give a no-2-PNE game for all positive \(m\): exact independent checks find best factors about 1.67614 at \(m=1\) and 1.95498 at \(m=2\). At \(m=3\), degree 288, the factor is about 2.01312. These are distinct games from a degree-32 construction using different amplitudes.

## Independent auxiliary reconstruction

Players are numbered 0 through 3, actions are 0 and 1. For every representative mask

\[
0101,0112,1022,1100,1120,1122,1211
\]

create a resource and the mask obtained by swapping labels 1 and 2. A nonzero mask digit equal to \(s_i+1\) means player \(i\) uses that resource. Both resources in a pair have the same amplitude. In pairs 1 through 6, a used resource charges its amplitude exactly when every player in its support uses it. In pair 7, a used resource charges \(g\) exactly when player 0 uses it. All other charges are zero. Every player pays the sum of latencies on resources it uses, without multiplying by its weight.

The complete exact vectors of current and unilateral flip costs for all 16 states are in `independent_evidence.json`. Complementing every action preserves each vector. The following table therefore records all eight complement classes. `C` and `D` are the selected player's current and flip costs; the last column is the maximum ratio over all four deviations, not merely the selected ratio.

| State and complement | Player | Formal C | Formal D | C−2D at fixed amplitudes | Best ratio |
|---|---:|---|---|---:|---:|
| 0000,1111 | 2 | g | e | 24/25 | 50 |
| 0001,1110 | 2 | b+g | c+e+f | 51/50 | 35/9 |
| 0010,1101 | 3 | a+g | c+f | 9/20 | 149/52 |
| 0011,1100 | 0 | c+d+e+f+g | g | 7/50 | 107/50 |
| 0100,1011 | 3 | g | a | 1/50 | 100/49 |
| 0101,1010 | 2 | g | c | 1/50 | 100/49 |
| 0110,1001 | 3 | b+g | a+c | 7/50 | 15/7 |
| 0111,1000 | 1 | a+g | d+e+f | 19/100 | 149/65 |

Every current and every unilateral flip cost in this fixed-amplitude auxiliary game is strictly positive. The verifier checks this before division. More generally, the model's rule is retained: a positive current cost with zero flip cost violates every finite approximation factor; zero current and zero flip costs satisfy the equilibrium inequality and must not be treated as a ratio.

The eight rows prove nonexistence by covering every state. An improving cycle alone would not suffice. At \(\alpha=100/49\), the four states `0100,0101,1010,1011` satisfy every deviation inequality, including equality in the selected bottleneck deviation. Consequently, the strict endpoint is excluded from the auxiliary obstruction statement.

## General amplitudes: the actual selected-witness cone

For positive \(a,b,c,d,e,f,g\), the selected witnesses give the following sufficient strict inequalities:

\[
\begin{aligned}
g&>\alpha e,\\
b+g&>\alpha(c+e+f),\\
a+g&>\alpha(c+f),\\
c+d+e+f+g&>\alpha g,\\
g&>\alpha a,\\
g&>\alpha c,\\
b+g&>\alpha(a+c),\\
a+g&>\alpha(d+e+f).
\end{aligned}
\]

An initial message by this reviewer mislabeled `0100`'s flip cost as \(c\) and `0111`'s current cost as \(c+g\), after inferring labels from numerical values with \(a=c\). The lead reviewer caught this, and a fresh symbolic resource enumeration independently confirmed the corrected table above. The fixed-amplitude numerical verdict and transport bounds were unaffected. No general-amplitude claim should use the incorrect labels.

For this selected-witness cone, there is a complete feasibility characterization for \(\alpha\geq1\). Let \(\beta\) be the unique root greater than 1 of

\[
\beta^3-\beta^2-2\beta-1=0,
\qquad \beta\approx2.1478990357.
\]

The cone is strictly feasible exactly for \(1\leq\alpha<\beta\). To see necessity, divide by \(g\), put \(g=1\) and \(X=d+e+f\). Its four relevant inequalities imply

\[
a,c<1/\alpha,\qquad \alpha-1-c<X<(a+1)/\alpha.
\]

Therefore \(\alpha^2-\alpha-1<\alpha c+a<1+1/\alpha\), which requires the strict cubic inequality. For sufficiency, select

\[
\max\{0,(\alpha^2-\alpha-1)/(\alpha+1)\}<r<1/\alpha,
\qquad a=c=r,
\]

then choose positive \(X\) strictly between \(\alpha-1-r\) and \((r+1)/\alpha\). Choose positive \(e,f\) sufficiently small that \(e<1/\alpha\), \(e+f<X\), and \(r+1>\alpha(r+f)\), and set \(d=X-e-f\). Finally choose positive \(b\) larger than both \(\alpha(r+e+f)-1\) and \(2\alpha r-1\). This satisfies every inequality. All selections may be rational, because the intervals are open.

This proves feasibility of the displayed witness template, not global optimality over all possible witness assignments, strategies, or congestion games. In particular, the endpoint \(\beta\) is excluded from this strict cone; no finite endpoint obstruction is asserted from the limiting argument.

## Rigorous finite polynomial transport

Fix integer \(m\geq1\), the specified positive weights, and \(D_m=32m^2\). For pair \(j\), let \(W_j(m)\) be the sum of weights on its nonzero mask positions. The finite resource latency is

\[
c_{j,\pm}^{(m)}(x)=t_j(x/W_j(m))^{D_m}\quad(j\leq6),
\qquad c_{7,\pm}^{(m)}(x)=g(x/W_7(m))^2.
\]

These are monomials with positive rational coefficients. Their degrees are at most \(D_m\), so the finite game belongs to the exact class \(G_{D_m}\). The fact that the last pair has degree 2 is permitted by the model's degree-at-most convention.

For a proper subset of any support in the first six pairs, a missing weight is at least \(1/(50m)\), and the support capacity is at most \(1+17/(100m)\). Hence its normalized load is at most

\[
\rho_m=1-\frac2{100m+17},\qquad
E_m=\rho_m^{32m^2}\leq\exp\!\left(-\frac{64m^2}{100m+17}\right)
\leq\exp(-64m/117).
\]

Full-support latency is exactly its limiting amplitude, and every other latency lies between zero and \(t_j E_m\). The maximum sum of first-six amplitudes available to any one player is \(56/25\). Thus its first-six cost can only increase from its auxiliary value, by at most \((56/25)E_m\).

For the last pair, if the heavy player uses a resource then its fee lies between \((m/(m+17/100))^2\) and 1, so the reduction from the auxiliary fee is at most

\[
\delta_m=1-(m/(m+17/100))^2\leq17/(50m).
\]

If the heavy player is absent, its load is at most \(17/(100m)\), so its fee is at most

\[
q_m=(17/(100m+17))^2\leq289/(10000m^2).
\]

Every selected auxiliary current cost includes last-pair fee 1. For selected light-player deviations, that limiting last-pair fee becomes zero. For the selected heavy-player deviation it remains 1, and its finite last-pair fee is at most 1. Consequently, a single valid lower bound for all selected finite margins is

\[
C_i^{(m)}(s)-2C_i^{(m)}(s^{\oplus i})
\geq\frac1{50}-\delta_m-2q_m-\frac{112}{25}E_m.
\]

For all \(m\geq20\), the exponential bound gives \(E_m<(3/8)^{10}\), using \(e>8/3\) and \(64m/117\geq10\). Therefore the total error is at most

\[
\frac{17}{1000}+\frac{289}{2000000}
+\frac{112}{25}(3/8)^{10}
=\frac{18235650607}{1048576000000}<\frac1{50}.
\]

The resulting common strict margin lower bound is

\[
\frac{2735869393}{1048576000000}>0.
\]

This establishes the quantified assertion: **for every integer \(m\geq20\), for every one of the 16 states, there exists a player whose flip strictly improves by a factor greater than 2**. No interchange of a maximum and a limit, and no unproved uniform convergence over an infinite state space, is needed.

For the fixed amplitudes, each current and flip cost converges to its auxiliary value, and the auxiliary flip costs have a positive minimum. Thus the finite game's best factor converges to \(100/49\). Equivalently, for every \(1\leq\alpha<100/49\), there exists \(m_0(\alpha)\) such that every integer \(m\geq m_0(\alpha)\) has no \(\alpha\)-PNE. This does not establish no-\(100/49\)-PNE at any finite \(m\).

If the general strictly feasible cone is used instead, fix any \(\alpha<\beta\) and choose its amplitudes first. The finite set of selected limit margins has a positive minimum. The same vanishing errors then give some \(m_0(\alpha,t)\). Amplitudes and the starting index depend on \(\alpha\); there is no claim of a single fixed amplitude vector obstructing all \(\alpha<\beta\).

For a statement covering every sufficiently large target integer degree \(d\), choose \(m=\lfloor\sqrt{d/32}\rfloor\). Since \(32m^2\leq d\), the corresponding game also lies in \(G_d\). In particular, the explicit fixed-amplitude no-2-PNE conclusion holds for every \(d\geq12800\). The four-player constant lower bound remains separate from the main target of degree-dependent growth.

## Verification and attack of the supplied checker

`check_independent.py --write` reconstructs exact auxiliary vectors, all 16 flip vectors, formal selected witnesses, finite games \(m=1,2,3\), and the rational uniform \(m\geq20\) bound. It imports no supplied checker or frozen evidence.

The supplied `verify_limit.py`, as first read, agrees with the auxiliary resource rules, exact fixed-amplitude factor \(100/49\), strict margins, and positivity checks. Its absolute-cost bound using the sum of all first-six amplitudes and a factor \(1+\alpha\) is more conservative than the directional witness bound here, but mathematically valid; in particular its \(m\geq52\) fixed-amplitude assertion is not contradicted by the smaller certified threshold here. Its finite scans explicitly include the failures at \(m=1,2\), so they must not be summarized as an all-\(m\geq1\) obstruction for the retuned vector.

The subsequently completed `limit_family.md` was reviewed in full. Its auxiliary four-component table and selected witnesses agree with the independent formal reconstruction. Its rational interval construction satisfies every selected inequality, including the separate upper bounds on both \(a\) and \(c\); its strict cubic endpoint exclusion applies specifically to this template. Its explicit logarithmic threshold has the correct constants, and its degree embedding preserves the stated quantifier order. No substantive mathematical error was found in `WCF-R3-SCALED-RETUNED-v1` or `WCF-R3-SCALED-TEMPLATE-v1`.

As an additional check, the independent formal implementation applied to the original amplitudes reconstructs factor \(65/34\), minimum selected margin 28 at \(\alpha=9/5\), and the positive rational uniform \(M=13\) margin \(8111103609/1703936000\). The supplied checker also reproduces the finite cases within its stated scope; its original-coefficient finite enumeration is reproduction evidence, not a second independently implemented scan of all twelve cases.

The remaining obligations concern external peer review, priority and literature assessment, and broader witness optimization, rather than an identified gap in this scaling proof. Any published statement must retain the endpoint, parameter dependence and fixed-player scope above. No repository board or Git changes were made by this independent review.

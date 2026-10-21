# Common-marginal iid mixtures: independent mathematical attack

2026-10-21. Reviewed `round4_security/iid_closure.md` and its local audit source without importing that implementation. The general Jensen lemma, the exact eight-client optimum iid cap, and the distinction from independent non-identical opponent marginals all pass this review. The status closure of `W>=Z_n` is separately recorded in `iid_bridge_status_audit.md`.

For an arbitrary fixed background load b and k opponent seats, put

\[
G_{b,k}(t)=\mathbb E\frac1{b+1+\operatorname{Bin}(k,t)}.
\]

The proposed integral `int_0^1 z^b(1-t+tz)^k dz` is correct: expand the kth power in its binomial form and integrate `z^(b+j)`. Every integrand has nonnegative second derivative in t, including its endpoints by polynomial continuity. An independent discrete proof writes `h_j=1/(b+1+j)` and uses the Bernstein second derivative formula

\[
G_{b,k}''(t)=k(k-1)\sum_{j=0}^{k-2}\binom{k-2}{j}t^j(1-t)^{k-2-j}
\frac{2}{(b+1+j)(b+2+j)(b+3+j)}\ge0.
\]

For k=0,1 the function is constant or affine; for k>=2 it is strictly convex. Therefore every pure-query payoff is convex in the common action distribution q. A latent distribution over q is fixed independently of the query in the security game. Jensen gives `alpha_A(E q)<=E alpha_A(q)` for every pure query A at once. Consequently the mean q supplies a single iid opponent background whose cap is no larger than that of the arbitrary mixture. The converse inclusion is immediate from a point mass latent distribution. Thus the infima over all common-marginal iid backgrounds and over all their arbitrary mixtures are exactly equal. This is a universal argument, not a finite-support claim about the latent distribution.

For the eight-client instance, moving mass from theme0 to its superset theme2 weakly increases every client's opponent-coverage probability. `g_3` decreases, so no pure-query payoff increases. The cap is a convex function invariant under swapping themes2 and3. Averaging this swap permits restricting the minimization to `q=(0,t,(1-t)/2,(1-t)/2)`. On this interval,

\[
\alpha_1=4-4t+\tfrac43t^2,\quad
\alpha_2=\alpha_3=\tfrac54+t+\tfrac34t^2,\quad
\alpha_0<\alpha_2.
\]

The first displayed function strictly decreases and the second strictly increases on [0,1], with opposite order at the endpoints. Their unique intersection in that interval obeys `7t^2-60t+33=0`, hence

\[
t^*=(30-\sqrt{669})/7,\qquad
\rho_3=(1448-52\sqrt{669})/49>2.
\]

This proves the global iid cap optimum, including q with nonzero theme0 mass and asymmetric themes2,3 before the reductions. The strict inequality is exact: `1350^2-52^2*669=13524>0`, with both sides positive before squaring. Three positive-probability actions all attain rho3; the unused action has lower payoff. The same q is a static symmetric mixed Nash distribution, so its expected welfare is `Z_3=3rho3` as claimed. Equality between rho3 and Z3/3 is an instance-specific conclusion here; the Jensen lemma alone does not imply it for every game.

The independent-product boundary is essential. Let one opponent choose theme1 with probability one and the other choose themes1,2,3 with probabilities `(3,10,10)/23`. Their actions are independent, with different marginals. The four pure-query expected payoffs are exactly `(26,44,44,44)/23`, all less than2. This reproduces a legitimate security dual cap `44/23`. It disproves any assertion that correlation is necessary for a cap at the actual mean payoff2. Randomly swapping the two seats makes the dual exchangeable and negatively correlated, but symmetrization is optional. The excluded class is common-marginal iid and arbitrary mixtures of that class. General independent product distributions with different marginals remain available.

`iid_cap_audit.py` implements a separate exact number field `Q[t]/(7t^2-60t+33)`, selecting the smaller root by the rational isolating interval `(59/100,3/5)`. It enumerates16 ordered iid opponent backgrounds per query and64 static ordered outcomes, independently confirming the cap, strict inequalities, and `Z_3=3rho3`. It also verifies the different-marginal product caps,120 reciprocal finite differences, and1,728 rational Jensen instances. The actual successful report is `iid_cap_audit.json`. The general convexity and minimax claims rely on the analytic arguments above; finite checks do not enlarge their scope.

No general half-coverage proof or aggregate true-security proof or counterexample is obtained. This audit supports formally recording the common-marginal iid mixture obstruction and correcting the old stronger bridge's open status, while preserving the still-open true security bridge.

# Primary-source audit

Checked live on 2026-10-14 UTC:
[arXiv:2002.07466v3](https://arxiv.org/html/2002.07466v3), version dated
27 March 2022, §2 and §3, especially Theorem 1, equation (3), and its proof.
Web retrieval reference in this agent's session: `turn2view0`.

- §2 defines positive player weights and unweighted latency sums as player
  costs; its equilibrium inequality is non-strict.
- §3 writes the optimization domain as `n in N`, `1 <= k <= d`,
  `w,beta in [0,1]`. Its construction has one weight-one player and `n`
  equal-weight light players, with latencies `x^k` and `beta x^d`.
- Equation (3) is exactly the minimum of the two quotients analyzed here.
  For `d=2`, only `k=1,2` occur.
- The two proof cases require both improvement factors to be strictly
  larger than the target approximation factor.
- Positive-weight game validity excludes `w=0`; the formula includes it as
  a boundary. Our polynomial statement handles that boundary without a
  quotient convention.
- The source gives an approximate degree-two value `1.054` and describes
  `n=1` as optimal for degrees two through four. Our ceiling does not
  independently certify those optimization or optimality statements.

No later-literature/priority search is claimed. The source statements above
are paper facts; the rational ceilings in `proof.md` are our independently
reconstructed algebraic consequences.

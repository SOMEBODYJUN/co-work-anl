# Extra fractional local chain: exact boundary and aggregate direction

2026-10-25. Personal exploratory note. Original Q-CAG-HALF, root aggregate security, AFC and arbitrary-background aggregate remain OPEN. This is an immediate indexing corollary of an already proved auxiliary counterexample, not new welfare progress or a new game.

Let delta_{r+1}(b) use fractional competing mass r. A tempting local helper is

    u+(r-1)delta_r(b+S) >= r delta_{r+1}(b).    (EXTRA-LOCAL)

If valid at every actual node it would telescope to a sufficient aggregate bound. It is FALSE at a legal arbitrary background. Source: peer R-d3981c0168644971803a9c3380ed687c/round4_general/security/pb_fractional_saddle_plateau.md, itself using our round5/menu/pair_attack.md complete-SPE theorem. These inherited sources establish the complete ordered-history SPE; this note does not redo that huge construction.

Use all the old PB parameters k=3,d=20,q=12,r=2475,Q=2063,H=100000,M=10^9, and f(c)=11/(M+c)+1/(M+c+1), g(c)=Hq/(HM+c). Replace the source plateau load 3(r-1)/Q by

    L=3r/Q.

The same saddle proof works: competing q chooses three uniform real blocks in each segment; querying p chooses one uniform real and both dummy blocks. Its value is

    Delta_plus=d[f(1+L)+2g(1)].

The exact strict comparisons f(1+L)<g(1), H_R>H_D still hold, where H_R=[11/(M+1+L)^2+1/(M+2+L)^2]/Q and H_D=Hq/(HM+1)^2. Singletons remain strictly below the query value and gradient maximum. Hence delta_(r+1)(b)=Delta_plus by the same convex KKT and query-support argument.

After the prescribed F, a child competitor has mass r-1. Each hot block needs extra load L-1, each outside block L. A mixture of one-hot-plus-two-outside and three-outside themes with mixture probability 3(L-1)/(r-1) realizes precisely these marginals. Thus every query denominator is preserved. Prefix-domain embedding gives the opposite inequality, so delta_r(b+F)=Delta_plus. The actual current payoff is u=3d f(3), while Delta_plus exceeds the old published security lower s=d[f(1+L)+2g(r+1)]>u. EXTRA-LOCAL therefore has strict negative balance u-Delta_plus.

This is a counterexample to a local induction helper only. The background already covers every customer and need not lie on a root SPE path. The full r-player utility still exceeds r Delta_plus: its exact expression is

    U=d[9 f(3)+1648 f(1)+824 f(2)+4944 g(2472)].

Indeed U-r Delta_plus>0. Consequently this source does not refute arbitrary-background aggregate U>=r delta_(r+1)(b), and does not refute the original half conjecture. Its role is to rule out paying that aggregate debt one step at a time.

The accompanying script checks only the exact scalar/KKT/marginal corollary and this aggregate comparison. It is not a new full-tree SPE audit or a general aggregate proof. Future work must allow a joint settlement of early debt, or produce a genuine global inequality; extending this arithmetic or scanning more PB parameters would not supply it.

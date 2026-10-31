# A tax-sensitive static envelope and true terminal-reply cycles

Status: direct algebraic interfaces and a still-unproved global payment
candidate, 2026-10-21. This file is separate from the proved personal repeated
theme result B2-REPEATED-LAST-ABSENCE-v1. It uses the unchanged Q-CAG-HALF
model, not a restriction to anonymous or fixed tie-breaking strategies.

## 1. Pure and mixed static envelopes

For every legal (m-1)-theme tuple h, let b_x(h) be its load and set

    f_h(T)=sum_{x in T}1/(1+b_x(h)),
    tau(h)=sum_x b_x(h)/(1+b_x(h)).

For any fixed m comparison themes, write a_x for their customer load.
The pointwise inequality 1_{a_x>0}<=(a_x+b_x)/(1+b_x) gives

    OPT_m <= sum_{j=1}^m f_h(T_j)+tau(h).

Taking an expectation with respect to any static distribution Q over legal
h, independent of the query theme, then maximizing the individual queries,
proves

    OPT_m <= E_mix
       := min_Q [m max_T E_Q f_h(T)+E_Q tau(h)]
       <= E_* := min_h [m max_T f_h(T)+tau(h)].              (1)

Finite LP duality, or finite minimax with query distribution p, gives exactly

    E_mix=max_{p in Delta(S)} min_h
       [m sum_T p_T f_h(T)+tau(h)].                         (2)

This is an equality of finite optimization problems. It does not construct a
payment by actual SPE welfare. The sufficient global bridges

    E_* <= 2W(SPE), or the weaker E_mix <= 2W(SPE),

remain unproved here. Neither follows from a finite number of successful
strategy cones. In particular, the old failure of W>=m theta_m does not
automatically refute (1)'s tax-sensitive bridges.

The dual objective also has a useful exact customer form. If p_x is the
probability that a p-query covers x, its contribution at background load b is

    (b+m p_x)/(b+1).

Adding one cover to that background changes the contribution by
(1-m p_x)/[(b+1)(b+2)]. Thus the static minimizer pays for covering customers
with p_x<1/m and gains from covering customers with p_x>1/m. This sign
distinction prevents importing an ordinary nonnegative coverage greedy
argument without additional proof.

## 2. What a genuine last-two-player reply cycle pays

Fix any ordered history P of length m-2 in the given full SPE, including an
off-path history. Let p_x be its customer load. Write A*=sigma(P),
b(a)=sigma(P,a), and u(P) for the penultimate mover's final payoff from P.
For themes a,b define

    U_P(a,b)=sum_{x in a}1/(p_x+1+1_{x in b}).

Choose any directed cycle C of the genuine reply map a->b(a); length-one
cycles and distinct labels with identical coverage are allowed. Let Q_C be
uniform on the legal static backgrounds P+a for a in C. The existing exact
stationary-pair identity states, for every query T,

    u(P)-E_{a in C} f_{P+a}(T)
      = E_{a in C} [Gamma_(P,a)+Gamma_(Pa,T)] >= 0.          (3)

These are actual original full-strategy rows at their own ordered nodes.
No reply is moved to another history. Therefore all query values against
Q_C are at most u(P).

Tax has the exact increment

    tau(P+a)-tau(P)
       = sum_{x in a}1/[(p_x+1)(p_x+2)].

Set D_C equal to this increment averaged over C. Combining with (1) proves

    OPT_m <= E_mix <= m u(P)+tau(P)+D_C.                    (4)

There is also a universal upper bound on D_C. For x in a, its increment
1/[(p+1)(p+2)] is at most its payoff 1/(p+1+1_b) in U_P(a,b).
After summing customers and averaging,

    0<=D_C<=E_C U_P(a,b(a))<=u(P).                          (5)

The last inequality uses the current mover's own SPE comparisons to every
cycle action. Hence

    OPT_m <= (m+1)u(P)+tau(P).                              (6)

Equations (4)--(6) hold for every genuine P and every reply cycle C. Taking
the minimum over these objects is a legal improvement over one arbitrarily
chosen actual terminal node. This is a direct combination of the already
proved stationary-pair identity with the tax envelope, not a claim that the
stationary-pair identity itself is new.

For any candidate full-SPE counterexample to half coverage, every such
affine budget must exceed 2W. This is a structural necessary condition; no
argument here proves that some budget must be small enough.

## 3. Connection to static CCE, without the failed welfare bridge

For completeness, if mu is any static coarse correlated equilibrium on m
players, let Q be the distribution obtained by choosing a uniform player and
deleting that player from a mu-profile. CCE conditions, averaged over players,
give max_T E_Q f_h(T)<=E_mu W/m. For a deleted player's actual set A_i,

    tau(s_-i)=W(s)-u_i(s)-R_i(s),
    R_i(s)=sum_{x in union(s) outside A_i}1/(c_x(s)+1)>=0.

Thus E_Q tau <=(1-1/m)E_mu W, and

    E_mix <= (2-1/m) E_mu W.                               (7)

This is a static comparison only. The known full SPE with welfare below
every static CCE rules out simply paying E_mu W by the actual W. Formula
(7) gives no reverse inequality and does not import that failed bridge.

## 4. Computation status

The pure-envelope cone experiment retains every full ordered-history SPE
row for a fixed policy and all length-(m-1) count prefixes. It maximizes
E_*-2W with W normalized to one. Twelve random m=5,p=7 policies and seven
canonical small-instance policies all gave floating maximum -1/m. These
are finite cone observations; rational dual certificates have not been
reconstructed, and there is no general theorem inferred from them.

The next experiment adds every available affine cycle budget (4), retaining
its own actual P and original reply map. Even a successful finite LP would
only cover the policies supplied. A positive optimum would obstruct the
specified collection of affine budgets, not automatically (1)'s unrestricted
mixed envelope and not Q-CAG-HALF.

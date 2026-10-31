# Random optimal permutations do not equalize prefix seats

Scope: the finite common-catalog, unit-provider, unit-customer sequential CAG,
with a pure strategy at every ordered history and arbitrary history-dependent
ties. This is an auxiliary obstruction, not a counterexample to half coverage
or to the uniform-portfolio inequality (6).

## Exact rejected identity

Fix an optimal comparison tuple of length n, randomly permute its **indices**,
force its first k actions, and then follow the given complete SPE's real
continuation at that forced ordered prefix. Let z_k be the resulting terminal.
The newest forced provider is the kth provider. A tempting exchange step is

    E[u_k(z_k)] = (1/k) E[sum_{i=1}^k u_i(z_k)].

This equality is false. The lower-bound variant with >= is false as well.
The randomness of the comparison tuple does not randomize the original
strategy's treatment of player positions.

## Three providers, three distinct disjoint optimal themes

Take three pairwise disjoint themes A, B, C of sizes 2, 2, 1. Define the whole
strategy:

| Ordered decision history | Prescribed action |
| --- | --- |
| empty | A |
| A | B |
| B | A |
| C | A |
| AA | B |
| AB | B |
| AC | B |
| BA | A |
| BB | A |
| BC | A |
| CA | B |
| CB | A |
| CC | A |

At AA and BB the last player strictly takes the uncovered size-two theme.
At AC/CA the last player strictly takes B, and at BC/CB strictly takes A.
At CC, A and B both give 2 and the rule takes A. At AB and BA, all three
actions give 1; the strategy takes the second theme. After first action A or
B, each second-player action gives 1 under its true last reply. After C,
the second-player actions A, B, C give 2, 2, 1/2. Finally the root actions
A, B, C give 2, 2, 1. Thus all thirteen decision nodes satisfy SPE optimality,
including every off-path node.

The actual path is ABB, with payoffs (2,1,1), welfare 4, and OPT_3=5.
The unique optimal support is {A,B,C}; each theme has customers covered by
no other theme, so all three are necessary. Use this three-index optimal
tuple (A,B,C) and k=2. Its six index permutations induce the six distinct
ordered prefixes below, each with probability 1/6:

| Forced prefix | True completion | First payoff | Newest payoff | Prefix total |
| --- | --- | ---: | ---: | ---: |
| AB | ABB | 2 | 1 | 3 |
| BA | BAA | 2 | 1 | 3 |
| AC | ACB | 2 | 1 | 3 |
| CA | CAB | 1 | 2 | 3 |
| BC | BCA | 2 | 1 | 3 |
| CB | CBA | 1 | 2 | 3 |

Therefore

    E[u_2(z_2)] = 4/3 < 3/2 = (1/2) E[u_1(z_2)+u_2(z_2)].

The difference is exactly 1/6. This construction uses distinct, disjoint,
necessary optimal themes and does not freeze followers,
use static Nash inequalities, or assume anonymous ties. Its genuine reply
changes between AB and BA despite equal customer loads.

## A valid replacement for the lost symmetry

Although reply **actions** and earlier payoffs need not be symmetric,
the last reply's payoff and the terminal harmonic potential are symmetric
under reordering an equal-count prefix.

Precisely, let h and h' be any two ordered histories of length n-1 inducing
the same customer load d_x, and let M and M' be their respective prescribed
last-player actions in a complete SPE. Both maximize the same function

    f_d(T)=sum_{x in T} 1/(d_x+1).

Consequently f_d(M)=f_d(M'). If Phi(d)=sum_x H_{d_x}, where H_0=0, then

    Phi(d+1_M)-Phi(d)=f_d(M)=f_d(M')=Phi(d+1_M')-Phi(d).

Thus the two complete terminal harmonic potentials are equal. In particular,
for three players and optimal themes T_j,T_k, the genuine nested replies

    M_jk=sigma_3(T_j,T_k),  M_kj=sigma_3(T_k,T_j)

satisfy the exact legal equality

    U(M_jk;T_j,T_k)=U(M_kj;T_j,T_k).

This can be included as two directed best-response comparisons in a
cross-branch certificate. It never licenses M_jk=M_kj or prefix-seat
exchangeability. The example above has equal final potential 5 at AB and
BA while its first and second seats have different payoffs.

## Main interface remains open

The sufficient uniform-portfolio conjecture is

    n |union_j T_j| <= (n-1)W + sum_{i,j} V_ij,

where V_ij is a real deviation at player i's original actual prefix followed
by the same full strategy. Neither this example nor the scalar symmetry
lemma decides that conjecture. A promising stronger certificate must retain
genuine second-level indexed replies M_jk, their stage-two deviation
comparisons, their last-node best-response comparisons, and the equal-count
payoff equalities above. For coefficient separation, after fixing the other
membership bits, each such indexed reply bit enters these rows affinely;
this permits pricing reply bits individually when no other row couples them.
Cross-reply comparisons that contain products of two reply bits must still
be handled jointly or represented by additional valid variables.

In the current three-player charging template, the unresolved next decision
histories are root T_j followed by a second-player deviation to T_k or to a
real branch theme S_k. Their genuine last replies are respectively
M_jk=sigma_3(T_j,T_k) and N_jk=sigma_3(T_j,S_k). They cannot simply be replaced
by arbitrary actions or by the denominator upper bound 2. This identifies
the next candidate structure; it is not a proof that a particular node set
is mathematically minimal or sufficient.

The independent audit random_position_audit.py checks the whole ordered tree,
all six index permutations, all stated rational payoffs, and the potential
equalities directly from the five explicit customers. It imports no shared
model, SPE solver, or certificate verifier.

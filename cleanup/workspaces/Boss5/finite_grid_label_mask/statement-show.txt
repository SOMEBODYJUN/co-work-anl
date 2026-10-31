# Finite-grid label-mask logarithmic potential — Exact-only v1

2026-10-18, root/boss11. Scratch exact mathematical contract, no author proof/strategy included; not a repository asset. Independent attack requested.

Let U be a finite explicitly listed set of m items, [a] a finite agent list, and labels {0,1,...,L}, L>=1. For each item j give rational probabilities pi_(j,t)>=0 summing to one over labels. Let random labels r_j be independent with those probabilities.

For each agent i give a label t_i in [L], a subset S_i of U, binary positive rationals V_i, nu_i, and weights w_(i,j)>=0 for j in S_i. For a positive integer Q, require every w_(i,j) to be an integer multiple of 1/Q, and sum_(j in S_i) w_(i,j)<=1. Weights are zero outside S_i. Empty sets and zero weights are allowed. Q is charged by its value in the algorithm bound, and in the intended application Q=4m (m>=1), hence polynomial in the explicit input; no bit-polynomial claim for arbitrarily large binary Q is made.

For a complete label assignment r define

    W_i(r)=sum_(j in S_i) w_(i,j) * 1[r_j=t_i],
    Phi(r)=sum_(i in [a]) ln(V_i/(nu_i+W_i(r))).

For each given positive rational epsilon, there is a deterministic algorithm which returns a complete assignment r, with every chosen item label of positive input probability, such that

    Phi(r) <= E[Phi(r)] + epsilon.

Its total bit complexity is polynomial in the explicit input length, a, m, L, Q and log(1+1/epsilon). It need not represent the generally irrational expectation or Phi exactly. Semantic logs exist since V_i,nu_i>0. The statement includes m=0 and/or a=0, with the natural empty input branches.

Additional physical allocation consequence, only when explicitly assumed: if for every fixed t in [L], the sets {S_i:t_i=t} are pairwise disjoint, then the returned T_i={j in S_i:r_j=t_i} are pairwise disjoint across ALL agents. This is a statement about the same actual items, with no copies or independently assembled item labels.

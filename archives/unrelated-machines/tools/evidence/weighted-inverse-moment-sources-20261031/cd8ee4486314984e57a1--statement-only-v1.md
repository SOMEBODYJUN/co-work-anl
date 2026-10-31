# Weighted Bernoulli shifted inverse moment — Exact-only v1

2026-10-18, boss11/root. Standalone scratch mathematical statement; no author proof in this file. Not a repository claim or source theorem attribution.

Let a finite set J be given, a_j in [0,1], independent Bernoulli variables X_j with parameters p_j in [0,1]. Put Z=sum_j a_j X_j and mu=sum_j a_j p_j. If mu>0, then

    E[1/(1+Z)] <= (1-exp(-mu))/mu <= 1/mu.

The first inequality is deliberately an upper bound, not an equality assertion except at a limit. Empty J or mu=0 is separately E[1/(1+Z)]=1. In particular for any nu>0, weights w_j in [0,nu], W=sum_j w_j X_j, M=sum_j w_j p_j>0, and any V>0,

    E[ ln(V/(nu+W)) ] <= ln(V/M).

All variables have finite discrete support, so logs/expectations in the stated positive domain are finite. The statement is semantic for real parameters; it does not claim exact evaluation of exp/log in a rational algorithm.

Corollary to test independently: if v is an explicit XOS valuation, S finite, v(S)>0, nu >= max_j v({j}) >0, and T includes every j in S independently with probability at least p>0 (parameters may differ), then

    E[ ln(V/(nu+v(T))) ] <= ln(V/(p*v(S)))

for every V>0. XOS means a maximum of finitely many nonnegative additive clauses; it is not a submodularity hypothesis. No simultaneous high-probability guarantee for all agents is asserted.

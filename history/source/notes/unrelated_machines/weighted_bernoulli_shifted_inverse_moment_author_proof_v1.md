# Weighted Bernoulli shifted inverse moment — author Proof v1

2026-10-18, root/boss11. Exact SHA148cfe5ba2f6da74d9ce178281310373a31a057db2cfb0811216a4f7332c5801. Written only after root actually fully read fee Exact-first record SHA1c2649e6e1c85412c41ab30979d3f8dca6d2c2b205ac8e6419b7da14eb77b284. Root had already derived the mechanism before routing, so this is author/co-developer work, not a blind root review.

For 0<t<1 and 0<=a<=1, convexity in a implies t^a<=1-a+at. By finite independence,

    E[t^Z] = product_j(1-p_j+p_j*t^a_j)
           <= product_j(1-p_j*a_j*(1-t))
           <= exp(-mu*(1-t)).

Since 1/(1+Z)=integral_0^1 t^Z dt, integration gives

    E[1/(1+Z)] <= (1-exp(-mu))/mu <= 1/mu

for mu>0. When mu=0, nonnegative summands each vanish almost surely and Z=0. The finite expectation/interchange uses no limit or sampling algorithm.

Scale a_j=w_j/nu and mu=M/nu. Then E[1/(nu+W)]<=1/M. For V>0 concavity of log on the positive inverse variable yields

    E log[V/(nu+W)] <= log E[V/(nu+W)] <= log(V/M).

For explicit nonnegative XOS take an actual clause attaining v(S). On S its weights w_j sum to v(S) and each w_j<=v({j})<=nu. The same additive clause lower-bounds v(T) for every T. Its random retained weight has mean M>=p*v(S)>0. The logarithm of V/(nu+x) decreases in x; substitute the last bound and use M>=p*v(S). This proves the complete stated corollary, including unequal inclusion probabilities. The condition p>0 and v(S)>0 keeps its denominator positive. All finite-log and zero branches are as in Exact. No claim for arbitrary subadditive valuations without an additive support, for correlated inclusion, or for downstream NSW constants follows without further proof.

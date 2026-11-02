# Five-player root-maximum cuts from one genuine branch

Status: author exact complete-type certificate; independent review requested. These are necessary inequalities for the exact complete-history pure-SPE model. They are not a half-coverage proof or an SPE counterexample.

Fix a finite common catalogue, five unit players, a fixed complete ordered-history pure SPE, actual first payoff `u`, and `O=OPT_5`. Let `K` be the largest catalogue topic size. Force the root to choose a topic `T` attaining `K`, and execute the same original strategy to obtain `(T,A,B,C,D)`. Write its payoffs `(r,v_A,v_B,v_C,v_D)`. Root IC gives `R=u-r>=0`; each true follower topic has size at most `K`, giving `Cap_A=K-|A|`, etc. Root on this forced branch is the specified deviator; it is never treated as an optimizer.

Fix five optimal indexed topics `Q_1,...,Q_5` and put `j_x=sum_i 1_Qi(x)`. Their union has size `O=sum_x 1_(j_x>0)`; repetitions and empty topics are allowed. The following slacks are nonnegative:

```
OPT2 = 5 v_B - sum_x j_x/(1_T+1_A+3),
OPT4 = 5 v_D - sum_x j_x/(1_T+1_A+1_B+1_C+1),
K2_4 = v_B - sum_x 1_D/(1_T+1_A+3),
K3_4 = v_C - sum_x 1_D/(1_T+1_A+1_B+2).
```

`OPT2` uses player 3 at the genuine history `(T,A)`, comparing each `Q_i` and retaining the original continuation after each deviation; its final total load is bounded above by the displayed denominator. `K2_4` similarly compares legal topic `D` at that node. `K3_4` uses the true penultimate node `(T,A,B)` and legal action `D`, again bounding its potentially changed final reply by one. `OPT4` is the exact last-player best-reply aggregate at `(T,A,B,C)`.

The only theorem dependency is the established two-remaining-player tax bound in `research/current/customer_attraction/two_remaining_tax.md`. With `p=1_T+1_A+1_B`, it says, for each pair of legal topics `X,Y`,

```
H := v_C+v_D+sum_x 1_C/[(p+1)(p+2)]
  >= sum_x (1_X+1_Y)/(p+1_X+1_Y).
```

Sum this over the ten distinct optimal index pairs `i<k`. A customer in `j` optimal indices occurs in `j(5-j)` pairs with exactly one occurrence and `j(j-1)/2` pairs with two. Hence

```
PAIRopt = 10 H - sum_x [j(5-j)/(p+1)+j(j-1)/(p+2)] >= 0.
```

Equal topics indexed differently cause no problem: the tax theorem explicitly permits repetitions.

## Five exact inequalities

The attached certificates prove simultaneously:

| Necessary inequality | Approximate root-only line |
|---|---|
| `12380 O + 26881 K <= 326100 u` | `O <= 26.3409 u - 2.17132 K` |
| `23888 O + 64639 K <= 678285 u` | `O <= 28.3944 u - 2.70592 K` |
| `1753 O + 4851 K <= 50200 u` | `O <= 28.6366 u - 2.76726 K` |
| `3506 O + 29147 K <= 178180 u` | `O <= 50.8214 u - 8.31346 K` |
| `5365 O + 56053 K <= 328550 u` | `O <= 61.2395 u - 10.4479 K` |

Every `K` coefficient on the left is positive. Thus each row remains valid when `K` is replaced on that left side by the size of **any** legal topic. This introduces no new branch state in an existing representation.

Since `O<=5K`, the first row also gives the global root-payoff bound

```
88781 O <= 1630500 u,
O/u <= 1630500/88781 = 18.36541602369876...
```

when `u>0`. The linear inequality includes the zero case.

## Exact slack identity and all possible customer states

For one customer use bits `(t,a,b,c,d)` for `(T,A,B,C,D)` and integer `j=0,...,5`. Let `ell=t+a+b+c+d`, and use zero for a payoff with zero numerator. The per-customer terms of `R` and `Cap_i` are respectively `-t/ell` and `-i`; their global constant terms are `u` and `K`.

Each certificate records nonnegative weights `w_s`, `alpha=w_R`, negative `beta`, and positive `lambda`. Put `G=sum_s w_s s`. They satisfy

```
beta = sum_(four size caps) w_s - lambda.
```

Define the exact customer residual

```
rho = -1_(j>0) - lambda*t - sum_s w_s * (s)_x.
```

Since `sum_x t=|T|=K`, there is the exact identity

```
alpha*u + beta*K - O = G + sum_x rho.
```

`audit_root_max_direct.py` independently reconstructs all raw payoff coefficients with `Fraction`, verifies the constant identity, and checks all `2^5 * 6 = 192` possible `(bits,j)` states for each certificate. Each residual is nonnegative, with minimum zero and eleven zero states. This is exhaustive over the customer coefficient domain and therefore applies to any finite customer multiplicities. It does not treat finite game searches as universal proof.

The exact weights are in `root_max_direct_certificates.json`; the audit imports no discovery optimizer or old template evaluator. Floating discovery generated candidate multipliers only and has no role in the final inequalities.

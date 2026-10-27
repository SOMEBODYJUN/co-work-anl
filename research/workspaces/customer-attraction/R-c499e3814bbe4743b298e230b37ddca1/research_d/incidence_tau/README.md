# Independent reconstruction: six-player incidence-LP half condition

Status: internal independent reconstruction of `CA-INCIDENCE-LP-DYNAMIC-BUDGET-v1`, with a strictly stronger six-player numerical threshold. This is a conditional theorem for a catalog's maximal-incidence hypergraph; it does not close unrestricted `Q-CAG-HALF-6` and is not an SPE counterexample.

## Exact statement

Let a finite common catalog have distinct inclusion-maximal coverages `B_1,...,B_s`, core `C=∩_j B_j`, union `U=|∪_j B_j|`, and incidence blocks
`X_I={x:{j:x∈B_j}=I}` with masses `w_I`. Define

```
tau_inc = min { sum_j alpha_j : alpha_j>=1 when w_{\{j\}}>0,
                sum_{j in I} alpha_j>=1 for every positive non-singleton I,
                alpha_j>=0 }.
```

If there are six providers and `U>c=|C|`, then every pure SPE defined on all ordered histories satisfies

```
W >= c + (U-c) * sum_{r=1}^6 1/(6 + (tau_inc-1) r).
```

Consequently, since the displayed sum is decreasing in `tau_inc`, the exact rational condition

```
tau_inc <= 149/50
```

implies `U<=2W`, hence `OPT_6<=2W`. At `tau_inc=149/50`, the exact coefficient is

```
1006430343355 / 2012347307572
= 1/2 + 256689569 / 2012347307572 > 1/2.
```

The source candidate used `tau_inc<=8/3`; `149/50` is a numerical strengthening obtained after independently re-deriving the same backward-induction inequality. The threshold is only a convenient rational sufficient value; no sharp threshold claim is made.

## Proof reconstructed from the original model

Route every legal catalog theme to a maximal coverage containing it. At a prefix of length `t`, let `p_j` be the number of earlier routed actions, `r=6-t`, and set `p_I=Σ_{j∈I}p_j`. For a maximal label `j`, define

```
f_j(p,r) = w_{\{j\}}/(p_j+1)
           + Σ_{I∋j, |I|>=2} w_I/(p_I+r).
```

For any feasible incidence-LP vector `beta` at this `r`, put `y_j=p_j+beta_j`. Then every private block contributes at least `w_{\{j\}}` to `y_j f_j`, and every non-private block contributes at least `w_I`, because `Σ_{j∈I} beta_j>=r`. Hence

```
U-c <= Σ_j y_j f_j <= (t + B(r)) max_j f_j,
```
where `B(r)` is the minimum LP objective and `D_t=t+B(6-t)`.

Let `E_t=max_{q>=t} D_q`. At a prefix, choose a maximal `j` maximizing `f_j`. If no later action is routed to `j` after forcing `j`, the deviation to `B_j` earns at least `c/6+(U-c)/E_t`: core customers have final load at most six, and the displayed denominators bound private/non-private customers. If a later action is routed to `j`, take the first such follower at depth `q`. Its theme is contained in `B_j`; on the forced branch the deviator and that follower cover every customer of the follower theme once each, so the deviator's terminal payoff dominates the follower's. Backward induction gives the follower payoff at least `c/6+(U-c)/E_q >= c/6+(U-c)/E_t` because `E_q<=E_t`.

Thus every actual provider at position `t+1` has payoff at least

```
ell_t = c/6 + (U-c)/E_t.
```

Summing along the actual root path gives `W>=Σ_t ell_t`. Since `tau_inc>=1` whenever `U>c`, `B(r)<=r*tau_inc` implies

```
E_t <= 6 + (tau_inc-1)(6-t),
```

and the displayed bound follows after substituting `r=6-t`. The all-core case `U=c` is immediate from the last-player maximal-action lemma (and `U=0` is trivial).

The argument uses the original all-history SPE inequalities and does not identify the terminal profile with a static Nash equilibrium. It also does not assume count-dependent tie-breaking: routing is only an analysis map, while the actual ordered continuation remains the given strategy.

## Structural corollary

If there are no singleton incidence blocks and every non-core customer belongs to at least `d>=2` maximal coverages, then `alpha_j=1/d` is feasible and `tau_inc<=s/d`. Therefore six-player half coverage follows whenever

```
s/d <= 149/50.
```

For example, all catalogs with at most 11 maximal coverages and minimum non-core incidence 4 satisfy the condition (`11/4 < 149/50`), as do 14 maxima with minimum incidence 5 and 8 maxima with minimum incidence 3. This extends the earlier convenient `s<=2d` corollary. It remains a condition on the entire maximal-incidence hypergraph, not a reduction of arbitrary catalogs.

## Independent exact audit

`audit_incidence_tau.py` uses only `Fraction` and enumerates every incidence subset for the structural corollary examples. It checks the LP certificate `alpha=1/d`, the exact six-player coefficient at `tau=149/50`, the source value `8/3`, and the strict failure at `tau=3`. It does not pretend to enumerate all SPE or to certify unrestricted six-player half coverage.

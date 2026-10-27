# Seven maximal coverages, six providers: dense incidence half certificate

**Status:** exact finite coefficient certificate for a structural sub-class; internal artifact, not a proof of unrestricted Q-CAG-HALF-6. It proves the missing `s=7,n=6` case whenever singleton incidence is concentrated in at most one maximal coverage (in particular, when every coverable customer belongs to at least two distinct maximal coverages). The mixed case with singleton customers in two or more maxima remains open.

## Statement

Let `B_0,...,B_6` be the distinct inclusion-maximal coverages of a finite common catalog and let `U=|union_j B_j|`. Assume that at most one maximal coverage, say `B_6`, has any singleton-incidence customers (customers belonging to no other maximal coverage). For every complete ordered-history pure SPE with six providers, `OPT_6<=2W`. If `B_6` has no singleton customers this strengthens to `U<=2W`; in the general one-singleton case, `OPT_6=U-|X_{\{6\}}|` and the same certificate proves the claim.

This is the same model and all-history quantifier as `Q-CAG-HALF-6`. Internal subthemes, repeated actions, empty actions, and history-dependent ties remain allowed. The proof uses only genuine full-history SPE inequalities, so no static NE identification or anonymous tie rule is introduced.

## Exact rows

Relabel the actual final maximal action as `B_0`. For a customer, let `I` be its maximal-incidence set and `J` its true membership set on the actual root path. The final maximal-action lemma gives

`1_{5 in J}=1_{0 in I}`.

For the dense columns `|I|>=2`; the only permitted singleton columns are `I={6}`, the one maximal coverage omitted from the six-theme optimum. Earlier memberships are otherwise unrestricted. For `n=6,s=7`, the shared part of the mixed floor is

`B=(1/21, 2/37, 1/16, 2/27, 1/11, 7/72)`.

The full mixed floor has core coefficient `1/6`; replacing it by the smaller `B_t` gives a valid weaker row for every nonprivate type. Define

`M_t = u_t - B_t` for `t=0,...,5`.

For every maximal index `j`, the true last-player comparison to `B_j` gives

`L_j = u_5 - 1_{j in I}/(|J\setminus{5}|+1) >= 0`.

At the true prefix of length four, the genuine two-remaining tax theorem gives, for every pair `(j,k)`,

`T_{jk}=u_4+u_5+d/((p+1)(p+2)) - m_{jk}/(p+m_{jk}) >=0`,

where `p=|J\cap{0,1,2,3}|`, `d=1_{4 in J}`, and `m_{jk}=1_{j in I}+1_{k in I}`; the final term is zero when `m_{jk}=0`. These are the same valid rows used in the seven-maxima source proof.

Use the following nonnegative multipliers:

| row | multiplier |
|---|---:|
| `M_0,M_1,M_2,M_3` | `207/355, 417/710, 253/426, 133/213` |
| `M_4,M_5` | `0,0` |
| `L_0` | `0` |
| `L_1,...,L_6` | `8/71` each |
| `T_{00}` | `0` |
| `T_{01},...,T_{06}` | `7/71` each |
| all other `T_{jk}` | `0` |

## Residual identity and exact audit

For each customer column `(I,J)`, the coefficient in `W-U/2` is `1_{J != empty}-1/2`. Subtracting the displayed nonnegative row combination leaves a residual `r(I,J)`. The exact audit enumerates all `120` incidence sets with `|I|>=2`, plus the allowed singleton `I={6}`, across all `32` earlier-membership masks. The unrestricted dense subcase has `3840` columns; the one-singleton extension has `3872` columns and the same minimum. It verifies every residual is nonnegative and obtains

`min r = 15591089/238321440 > 0`,

at `(I,E,J)=(3,8,40)` in bitmask notation (`I={0,1}`, earlier mask `E={3}`, final membership forced by `0 in I`, so `J={3,5}`). Therefore

`W-U/2 = sum_q lambda_q S_q + sum_{I,J} w_{I,J} r(I,J) >= 0`,

and `U<=2W` follows for arbitrary nonnegative customer multiplicities. Since `OPT_6<=U`, the claimed half bound follows for this dense seven-maxima subclass.

The standalone exact checker is [audit_dense_shared_seven_n6.py](audit_dense_shared_seven_n6.py). Run:

```sh
python3 audit_dense_shared_seven_n6.py
```

Expected output is `columns=3840`, `minimum=15591089/238321440`.

## Boundary

This certificate does not cover singleton incidence types on two or more different maxima. It cannot simply be combined with the unrestricted target `OPT_6=U-min_j w_{\{j\}}`: the same rows have negative residuals on singleton columns whose maxima are not omitted. The unresolved seven-maxima six-provider obstruction is therefore concentrated in mixed singleton/dense incidence with at least two nonzero private blocks, and in finding a cross-type payment that uses the smallest omitted private block. A negative residual here is a certificate-template boundary, not a Q-CAG-HALF-6 counterexample.

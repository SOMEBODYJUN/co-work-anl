# Dynamic path Farkas candidate: exact audit and failure boundary

Status: **candidate refuted as a general certificate** (2026-10-24). This note records the exact formula and a smallest history-dependent SPE witness; it does not refute Q-CAG-HALF.

## Intended candidate

Fix a complete pure SPE `sigma`, its actual root path `S_1,...,S_m`, and a comparison tuple `T_1,...,T_m`. A tempting certificate gives every actual-path node `i` and comparison slot `j` multiplier `1/m` on the SPE row for forcing `T_j` at the prefix `h_i` and then following `sigma`.

For an interest type `B`, write

- `c(B)=|{i:S_i intersects B}|`,
- `q_i(B)=1_{S_i intersects B}`,
- `d(B)=|{j:T_j intersects B}|`,
- `b_i(B)=|{k<i:S_k intersects B}|`.

The actual term of the row is `q_i(B)/c(B)` when `c(B)>0`.

The forced branch does **not** generally end with the original suffix. Define instead

```
hat c_{i,j}(B) = b_i(B) + 1_{T_j intersects B}
                   + |{k>i : sigma(h_i,T_j,S_{i+1},...,S_{k-1}) intersects B}|,
```

where the last terms are the actions selected by `sigma` at the altered ordered histories. The exact row coefficient is

```
Gamma_{i,j}(B) = q_i(B)/c(B) - 1_{T_j intersects B}/hat c_{i,j}(B).
```

The tempting simplification `hat c_{i,j}(B)=c(B)-q_i(B)+1_{T_j intersects B}` is valid only when the continuation is suffix-invariant under this deviation. Full history-dependent SPE allows arbitrary changes of the suffix action, subject only to the off-path subgame incentives.

## Minimal complete-SPE witness of the mismatch

Take `m=2` and three labels `A,B,C` with themes

```
A={a1,a2}, C={a1,a2}, B={b}.
```

Use a complete strategy whose root action is `A`; after prefix `A`, choose `A`; after prefix `B`, choose `C`; after prefix `C`, choose `A` (any tie choice works). At every one-player subgame after a prefix, `A` and `C` give the same payoff on `{a1,a2}`, while `B` gives payoff `1` only when it is not already used; at the root every first action gives payoff `1`, so choosing `A` is a valid tie. Thus the strategy is a complete pure SPE (all off-path histories are specified and are best responses).

Actual path is `(A,A)`. Force the root to `B`; the same strategy then chooses `C`, so for type `B0={a1}`

```
c(B0)=2, q_1(B0)=1,
 hat c_{1,B}(B0)=1,
```

whereas the suffix-invariant expression would use `c-q_1+1=2`. Hence the proposed `lambda_{i,j}=1/m` full-path identity is not valid for general SPE.

The witness has `W=2` and `OPT_2=3`, so it is not a Q-CAG-HALF counterexample.

## What remains valid

1. At the terminal actual-path node `i=m`, there is no suffix, so `hat c_{m,j}(B)=c(B)-q_m(B)+1_{T_j intersects B}` exactly.
2. The full Farkas contract remains exact if every forced branch retains its own `hat c_{i,j}` coefficients. Existence of nonnegative multipliers for

```
2*1_{c(B)>0} - 1_{d(B)>0}
  = sum_{i,j} lambda_{i,j} Gamma_{i,j}(B) + eta(B),
```

with `lambda,eta >= 0`, is sufficient, but no universal construction is supplied here.
3. If a strategy has suffix-invariant continuation for all actual-path forced comparison actions, the simplification becomes valid and the former `1/m` calculation can be checked directly; this is a restricted class only.

The dynamic obstruction is therefore a real cross-tree continuation debt, not a notational omission. It is separate from the robust denominator lower bound `u_i >= max_T sum_{x in T}1/(b_i(x)+r_i)` used in the existing prefix-budget results.

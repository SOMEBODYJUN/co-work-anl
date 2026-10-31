# Target-union incidence budget and shared-omission obstruction

Status: candidate/general tool plus an exact algebraic obstruction; not a proof of Q-CAG-HALF and not an SPE counterexample.

## 1. Restricting the incidence budget to one optimal union

Fix a complete-history pure SPE and any optimal `m`-theme portfolio with union `O` (so `|O|=OPT_m`). Let `B_1,...,B_s` be all inclusion-maximal catalogue themes. Every catalogue theme is contained in at least one `B_j`. For each nonempty incidence set `I` of maximal themes put

`X_I = {x in O : {j:x in B_j}=I}`, `w_I=|X_I|`.

At a prefix of length `t`, route every earlier action to one containing maximal theme and let `p_j` be the number routed to `j`; write `r=m-t`. For a maximal theme `B_j`, retain only the target clients `O` in its immediate deviation value:

```
f_j^O(p,r) = w_{ {j} }/(p_j+1)
             + sum_{I contains j, |I|>=2} w_I/(p_I+r),
 p_I = sum_{j in I} p_j.
```

For this target union define the finite LP

```
B_O(r) = min sum_j beta_j
 beta_j >= 1                  if w_{ {j} }>0,
 sum_{j in I} beta_j >= r     if w_I >0 and |I|>=2,
 beta_j >=0.
```

For any feasible beta, `y_j=p_j+beta_j` gives

```
|O| <= sum_j y_j f_j^O(p,r)
    <= (t+B_O(r)) max_j f_j^O(p,r).                 (A)
```

The first inequality is clientwise: singleton clients use
`(p_j+beta_j)/(p_j+1)>=1`; an incidence-I client uses
`(p_I+sum_{j in I}beta_j)/(p_I+r)>=1`.

A deviation to the full `B_j` earns at least `f_j^O`: if no later action is routed to `j`, each target client's final load is bounded by the displayed denominator; if a later action is first routed to `j`, that follower's theme is contained in `B_j`, so the deviator's terminal payoff dominates the follower's payoff on the same branch. Backward induction with the suffix envelope

```
E_t^O = max_{q=t,...,m-1} (q+B_O(m-q))
```

therefore yields, for every ordered-history pure SPE and every prefix,

```
u_current >= |O|/E_t^O,
W >= |O| * sum_{r=1}^m 1/E_{m-r}^O.                (B)
```

This is a target-union refinement of the existing incidence-LP budget, which was stated for the union of all maximal themes. It is useful because it applies directly to an optimal union even when the global union of all maximal themes is much larger. It still does not imply half in general: with all-pair incidences on `s` maxima and no singleton target clients, `B_O(r)=s r/2`, so the coefficient in (B) decays with `s`.

## 2. Exact stationary-flow obstruction for shared incidences

The extreme-membership proof uses a stationary distribution over root maximal-theme branches. That algebra cannot be extended to arbitrary shared incidence sets. Let `k=4`, `r=3`, and let the follower-routing matrix (rows = routed maximal theme, columns = root branch) be

```
n = [[0,0,0,1],
     [0,0,1,0],
     [0,0,0,1],
     [2,2,1,0]],
```

so every column sums to `r-1=2` and `n_ii=0`. A stationary distribution is
`pi=(2/9,1/9,2/9,4/9)`. For a client with maximal incidence `J={1,2}`, use the sharp load upper bound `K_i=sum_{j in J} n_{ji}`. The root-minus-follower-average coefficients (background load zero) are

```
delta_i = (2-K_i)/(2*(1+K_i))  if i in J,
          -1/2                    if i not in J and K_i>0,
           0                       otherwise,
```

which gives `delta=(0,1,1/4,-1/2)` and

```
sum_i pi_i delta_i = -1/18 < 0.
```

Thus one stationary flow cannot guarantee nonnegative root-minus-tail credit for all arbitrary incidence sets. This is a precise algebraic obstruction to simply replacing the singleton/full/co-singleton cases by an arbitrary shared-omission incidence argument. It is not a complete SPE counterexample: the matrix is only a feasible routing certificate, and a valid proof would need additional constraints from the complete strategy tree or a different cross-client credit.

## 3. Remaining obligation

Any general shared-omission proof must add a genuinely new ingredient beyond (B) and a single stationary routing vector: e.g. a client-coupled flow, a dynamically selected (possibly nonstationary) distribution, or a direct argument tying high pair-incidence LP cost to covered target clients. Reusing private-seat and shared-incidence budgets as two independent copies of `W` would double-count.

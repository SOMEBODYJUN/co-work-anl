# Candidate: directories with at most three themes

Status: exact elementary proof candidate; not yet promoted to the shared
mathematical map.  This is a strict subcase of `Q-CAG-HALF`.

Assume the common directory has at most three nonempty themes (there may also
be the unique empty theme).  Fix any complete history-dependent pure SPE and
its terminal outcome.  Write `U` for the set of nonempty themes actually used.

If `|U|=3`, every customer that any admissible selection can cover is already
covered, so `W=OPT_m`.  If `|U|=2`, let `C` be the only unused nonempty theme.
The customers in `C\\(U_1\\cup U_2)` each give one unit to the last mover if that
mover deviates to `C` at the terminal prefix.  SPE optimality therefore gives
```
|C\\(U_1\\cup U_2)| <= payoff(last mover on the equilibrium path) <= W.
```
Every `m`-theme union is contained in the actual union together with those
customers, hence `OPT_m <= 2W`.

If `|U|=1`, call the used theme `A`.  When the empty theme is absent, every
provider chose `A`, so the last mover's equilibrium payoff is `W/m`.  For each
unused theme `B`, put `D_B=|B\\A|`.  A last-mover deviation from `A^(m-1)` to
`B` covers every customer in `B\\A` alone, so `D_B <= W/m`.  For `m=1`,
`OPT_1=W`; for `m=2`, any two-theme union is contained in `A` plus one or both
unused themes and the elementary deviation bounds give `OPT_2 <= 2W`; for
`m>=3`, both unused themes may be used but
```
OPT_m <= W + D_B + D_C <= W + 2W/m <= 2W.
```
If the empty theme is present, there are at most two nonempty themes.  A
terminal outcome using both is already optimal; if it uses only `A`, the one
omitted nonempty theme is bounded by the same last-mover deviation (and an
empty last action forces that omitted-only mass to be zero).  If no nonempty
theme is used, SPE implies all customer mass is zero because the last mover
could deviate to any nonempty theme.

Thus directories with at most three themes satisfy `2W>=OPT_m` for every
complete pure SPE, including empty themes and zero-customer boundaries.
The argument is independent of tie-breaking and uses only the terminal
last-mover subgame; it does not address unrestricted directory size.

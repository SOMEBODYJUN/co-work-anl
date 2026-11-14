# Core theorem versus shared finite separator

## Objects and model

The core is the fixed four-provider, five-label strategy cone for the archived
zero-indexed strategy 9.  Each of the 31 nonempty customer masks has an
arbitrary nonnegative mass.  The realized root path is `2222`, so `W` covers
customers containing label 2.  The comparison set is `J={1,2,3,4}`.  The
screened system keeps exactly the 41 histories of lengths 0, 1, 2 and 3 that
use distinct labels from `J`; at each such history it averages the true
continuation payoff gaps over the unused labels in `J`.

The shared object `M-68040e6e0ae74ae49a327f789f12ddaf` records the same model,
strategy, `J`, customer masses and 41-row system.  Its point has integer masses
`(19,96,38,45)` on masks `(2,5,9,17)`, giving `W=96`, `O_J=OPT_4=198`, and
`O_J/W=33/16`.  It therefore refutes the implication from this screened
average system (even with `J` optimal) to the factor-two bound, while retaining
the warning that this point is not a full SPE witness.

## Exact strengthening

The core theorem supplies the missing matching dual.  For all nonnegative
mass vectors,

```text
(33/16) W - O_J
  = (9/4) Rbar_(2) + Rbar_(2,1) + (1/2) Rbar_(2,3)
    + sum_M rho_M x_M,
```

where the three screened average rows have positive multipliers and all 31
listed `rho_M` are nonnegative.  Thus every point in the shared screened cone
satisfies `O_J <= (33/16) W`, including the `W=0` boundary.  The same point
annihilates the three dual rows and the four positive mass columns, so the
bound is attained.  Since its `J` coverage equals `OPT_4`, the restriction
`O_J=OPT_4` does not lower the sharp value.

This is a one-way logical edge from the exact core theorem to the weaker
shared finite separator.  It is not an equivalence: the shared record alone
contains no upper-dual certificate and does not establish exact optimality.

## Preserved limits and open obligations

The same rational point has 92 negative rows among the 780 true single-action
IC inequalities, three negative rows among the 64 retained individual `J`
comparisons, and negative all-`J` averages at repeated histories `(2,2)` and
`(2,2,2)` (`-5/256` and `-5/64` after normalization).  Consequently the edge
does not claim a complete pure-SPE counterexample, a full-history-average
counterexample, or any general four-/six-player welfare theorem.  Those
systems remain separate obligations.

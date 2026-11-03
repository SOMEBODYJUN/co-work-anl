# HALF(5): reviewed maximum-root envelopes and an exact template separation

Scope is only the original model's five providers: finite unit customers, one
finite nonempty common theme catalogue, and every full ordered-history pure SPE.
Empty themes, repeated themes, zero customers, all off-path histories, and any
history-dependent ties remain allowed. HALF(5) is still open. No point below is
claimed to be a game or a SPE.

This independent subtask first reviewed Boss16 `five_only/maxroot_envelope.md`
and `weighted_root_saturation.md`, then reused Boss14
`round8_five/certificate/trueH_seven_rows.md`. No shared canonical file is changed.
`envelope.py/json` holds the new exact coefficient certificates;
`joint_obstruction.py/json` specifies a tested larger family;
`joint_obstruction_integer.json` is its compact exact separation witness;
`audit.py/json` independently reconstructs coefficients using only the standard
library. This is internal mathematical review and separate implementation,
not external peer review or a novelty claim.

## 1. Review of the original 192-state proofs

Fix the original complete strategy and force a largest-cardinality theme M at
the root. Its genuine continuation is (M,A2,A3,A4,A5). For each customer let
b=(c,a2,a3,a4,a5) and let d count membership in five optimal indexed themes.
The full coefficient domain is 32 times 6 = 192 states. Actual repeated themes
or coincident histories impose additional equalities; checking the larger
192-state domain remains sound.

The nonzero original rows are legal:

* size:j is |M|-|Aj|, nonnegative by the global cardinality maximum.
* IC:2:4 is genuine third-player IC at (M,A2), comparing legal A5. On the
  deviation's true continuation the final load is at most c+a2+3.
* opt:4 is the exact last-player IC summed over five optimal indices.
* r2:opt is the genuine final-two tax bound summed over ten distinct optimal
  index pairs. With p=c+a2+a3, H=v4+v5+sum a4/[(p+1)(p+2)], its per-customer
  comparison sum is d(5-d)/(p+1)+d(d-1)/(p+2).
* r2:O follows because that comparison sum is at least 4/(p+1) when d>0;
  then (5/2)H+sum p/(p+1)>=O, including d=0 customers.

Finally actual root IC gives r>=v1; every displayed B is nonnegative, so
O<=Bv1-CK implies O<=Br-CK. No root forced action is treated as an optimizer.
`audit.py` checks every old certificate on all 192 states, including both
different multiplier representations of the first new old line.

The weighted proof's three steps also reconstruct correctly: seat deficits
d_total<=20(v1-K/5), follower vi<=v1+3di/4, and true follower deviation to D
using 1/(t+k)>=1/t-k/[t(t+1)]. Its convex combination and union-counting signs
are correct. All four exact (B,C) constants are separately recomputed.

## 2. New globally valid envelopes

Write K=|M|, r=actual root payoff, and O=OPT5. The reviewed true-H relation at
the genuine third node has p=c+a2, current payoff v3, and any legal five-item
menu of customer count j:

    sum [17040 v3_x +1085 c -2679 j/(p+3)-F(p,d)] >= 0.

F is Boss14's exact 3 by 6 table. Its hidden H,Q,R construction uses the same
exact (M,A2) history: H maximizes sum_H1/(p+3), and Q,R are its genuine replies.
Only current v3>=V_H is used; no ancestor payoff cap is inherited. The seven
raw row weights and all 144 hidden states are reconstructed in `audit.py`.

Take j=5a5. The following two new lines have especially small shared support:

| B | C |
| --- | --- |
| 6291370/137873 | 1983595/275746 |
| 3539900/137873 | 303930/137873 |

For either pair, **O<=Br-CK** holds for every allowed five-provider input.
The nonnegative multipliers, excluding final root IC, are identical:

| Row | Multiplier |
| --- | --- |
| size:1 | 559907/1102984 |
| size:2 | 684353/275746 |
| size:3 | 670295/275746 |
| size:4 | 651245/275746 |
| opt:4 | 37685/137873 |
| r2:opt | 21087/137873 |
| trueH:repeat:4 (j=5a5) | 33/275746 |

For every one of the 192 states the exact residual

    B v1_x-C c-1[d>0]-sum multiplier*row_x

is nonnegative. Both certificates have 11 zero residuals. Thus these are
complete finite coefficient proofs, rather than sampled games or a numerical
optimizer conclusion. The first improves the previously published envelope
at r/K=249/1000. The second improves it at r/K=263/1000.

`envelope.json` also records three other strict improvements at particular
discovery ratios, including (65710/1073,56053/5365), which already follows
from old rows and was missed by the earlier coarse ratio samples. It is a
completion of that discovery sampling, not a new mechanism. The ratio grid
does not claim to enumerate the entire parametric frontier. Each recovered
line itself is globally valid and has no ratio restriction. As always, C>0
permits O<=Br-C|Q| for every legal Q, and legal five-item menu summation.

## 3. A precise family still cannot pay beta=2

The tested family is exactly the following 266 rows on all 6144 states
(actual A..E membership, maximum-root M,A2..A5 membership, optimal count d):

1. Boss14 `round8_five/maxroot/joint_paths.py`'s 240 rows: joint actual and
   one maximum-root path, cross-label worst-denominator IC, optimal sums,
   exact final-two tax, cited three/four-tail bounds, maximum-size rows,
   and the genuine root-to-maximum comparison.
2. Twenty-two true-H projection rows: at the actual and the maximum-root
   genuine third nodes, use each of the ten labels five times, or use the
   optimal five-item menu.
3. The four weighted-root (B,C) relations reviewed above.

It includes the information needed for the old and new envelope lines, but
does not include Boss16's larger indexed/shared-menu family. No impossibility
claim about that larger family follows.

The following nonnegative integer point satisfies all 266 rows exactly. Bit
order is actual ABCDE, then maximum-root M,A2,A3,A4,A5. Every listed type has
d=1; omitted types have zero mass.

| Ten bits | Mass |
| --- | ---: |
| 0000000000 | 10 |
| 0000000001 | 3 |
| 0000000010 | 3 |
| 0000000100 | 1 |
| 0000100000 | 2 |
| 0000111100 | 3 |
| 0001000000 | 3 |
| 0001100000 | 1 |
| 0010000000 | 1 |
| 1011011011 | 1 |
| 1110000001 | 2 |
| 1110011110 | 3 |

Its exact totals are W=16, O=33, K=7, actual root payoff r=2. Actual payoffs
are (2,5/3,3,23/6,11/2); maximum-root path payoffs are
(2,2,11/4,4,21/4). The minimum of all 266 exact slacks is zero.

Therefore no identity expressing **2W-O** as a nonnegative combination of
these 266 rows plus nonnegative customer-type residuals can exist: evaluating
such an identity at this point would give -1>=0. This is an exact separation
of this specified coefficient cone. The integer masses do not turn the point
into a game: indexed optimal labels, all true replies, and full strategy-tree
consistency were relaxed. It is not a counterexample to HALF(5).

## 4. Remaining obligation and reusable next step

The new envelope pairs and the true-H projection can be inserted as valid
negative-size menu projections in the larger shared-index system. The compact
12-type witness is useful for checking whether a new bridge contributes
information beyond this 266-row family; a candidate bridge can first be
evaluated against its exact masses. A violated new row must then receive its
own all-history proof and full coefficient certificate. Repeating optimization
with these same rows cannot close half.

What is still missing is a full exact coefficient-two payment in a stronger
family, a direct universal proof, or a real finite unit-customer catalogue
with an all-history pure SPE violating HALF(5). No such outcome is supplied here.

Reproduction from repository root:

```sh
python3 research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/boss16_maxroot_review/envelope.py
python3 research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/boss16_maxroot_review/joint_obstruction.py
python3 research/workspaces/customer-attraction/R-bfbfe64dd5f94fa09d36b75198633f2b/boss16_maxroot_review/audit.py
```

The first two scripts use SciPy only for discovery; the last audit uses exact
Fraction arithmetic and no discovery-code imports or SPE solver.

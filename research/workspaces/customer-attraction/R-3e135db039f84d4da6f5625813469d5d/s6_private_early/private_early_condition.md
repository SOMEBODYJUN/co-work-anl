# Seven maximal themes, six providers: early coverage of included singleton blocks

**Status:** exact finite coefficient certificate for a conditional subclass; it
does not close unrestricted `Q-CAG-HALF-6`.

Let `B_0,...,B_6` be the distinct inclusion-maximal coverages of a finite
catalog, and fix a complete six-provider SPE. Relabel the actual final maximal
action as `B_0`. Assume that an optimal six-maximal portfolio can be chosen as
`B_0,...,B_5`, so `B_6` is the omitted maximal. Assume further:

* every customer with singleton maximal incidence `{j}`, `1<=j<=5`, is
  covered by at least one of the first four actual provider actions; and
* singleton incidence `{0}` is covered by the final action automatically,
  while singleton incidence `{6}` is unrestricted (these customers are outside
  the selected optimum).

Then `OPT_6<=2W` for every such complete SPE, with all original history,
tie, repetition, empty-theme and zero-customer quantifiers preserved.

The argument is a direct customer-level budget.  For a customer, let `I` be
its incidence among the seven maximal coverages and `J` its actual root-path
membership positions.  The final-action lemma gives
`1_{5 in J}=1_{0 in I}`.  Use the established mixed-floor rows with private
suffix coefficient `alpha_t=1/12` for singleton `I` and shared suffix
coefficient `beta_t=(1/21,2/37,1/16,2/27,1/11,7/72)` for `|I|>=2`.  Add the
same genuine final-player rows `L_j` and two-remaining tax rows `T_{jk}` as in
the dense seven-maxima certificate.

The nonnegative multipliers are

| row | multiplier |
|---|---:|
| `M_0,M_1,M_2,M_3` | `207/355, 417/710, 253/426, 133/213` |
| `M_4,M_5` | `0,0` |
| `L_0` | `0` |
| `L_1,...,L_6` | `8/71` each |
| `T_{00}` | `0` |
| `T_{01},...,T_{06}` | `7/71` each |
| all other `T_{jk}` | `0` |

For each allowed `(I,E)`, where `E=J∩{0,...,4}` and the final bit is forced
by `0∈I`, the target coefficient in `W-OPT_6/2` is

`1_{J!=empty}-1/2` for `I != {6}`, and `1_{J!=empty}` for `I={6}`.

The standalone exact checker `audit_private_early.py` enumerates all 4,054
allowed literal columns (`120*32` non-singleton, 32 singleton `{0}`, 30 each
for singleton `{1},...,{5}`, and 32 singleton `{6}`), evaluates every row in
`Fraction`, and obtains minimum residual

`49/2130 > 0`, at `(I,E,J)=({0},empty,{5})` in bitmask notation `(1,0,32)`.

Thus

`W-OPT_6/2 = sum(lambda_q * valid_slack_q) + sum_x w_x * residual_x >= 0`.

This is a conditional structural result. It extends the previously recorded
case with singleton incidence concentrated in the omitted maximal by allowing
singleton blocks in several included maxima, provided those included private
customers are already covered before the penultimate move. It does not address
the unrestricted mixed class where an included singleton block can remain
uncovered or be covered only by the penultimate provider; for example the same
certificate has residual `-1/30` on `(I,E,J)=(\{4\},\{4\},\{4\})`.

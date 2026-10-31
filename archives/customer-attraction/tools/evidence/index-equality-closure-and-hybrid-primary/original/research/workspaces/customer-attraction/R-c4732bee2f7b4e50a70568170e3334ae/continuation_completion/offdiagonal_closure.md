# Off-diagonal terminal closure excludes the frozen five-player bad point

Status: exact necessary-row derivation and exact frozen-point obstruction. This
is not a half-coverage proof or an SPE counterexample. The original 437-row
template optimum remains correct for its original stated relaxation.

## General common-catalog row

Fix a full pure SPE in the common-catalog customer-attraction model. Let
`(P_i,Q_i)`, for `i=1,...,q`, be any list of genuine final decision histories
`P_i` and their chosen last topics `Q_i`. Let `M_i` be any additional indexed
list of catalog topics. Each final player at `P_i` may choose every `M_j`, so

\[
\Gamma_{ij}=u(Q_i\mid P_i)-u(M_j\mid P_i)\ge0
\quad\text{for every }i,j.
\]

In particular, summing only `i != j` is legitimate. If a client has membership
`z_i` in `Q_i`, `b_i` in `M_i`, background load `p_i` under `P_i`, and
`b=sum_i b_i`, its coefficient in this necessary row is

\[
\boxed{\sum_i\frac{(q-1)z_i-b+b_i}{p_i+1}.}
\]

The denominator is `p_i+1`: whenever the query client's numerator is one,
deviating to that query adds exactly one cover. The formula is exact, including
repeated topics and histories. It depends on each branch's joint local state
and the indexed menu total, but it needs no cross-family coupling information.

The all-pairs sum and diagonal sum can both be nonnegative while this
off-diagonal sum is negative. Therefore retaining only all-pairs comparisons
and the diagonal comparisons loses necessary information.

## The frozen five-player point

Use the 64 atoms in
`evidence/certificates/customer_attraction/five_player_indexed_bound.json`, with
their original masses and meanings. For the second-position deviation branch,
the final histories are

\[
P_i=(A,T_i,H_i,I_i),\qquad Q_i=J_i,\qquad M_i=I_i.
\]

For a client with fixed `A` membership `a` and local indexed state
`(t,h,i,j)`, write `I=sum_i i_i`. The new row is

\[
\sum_x\sum_{r=1}^5
\frac{4j_{r,x}-I_x+i_{r,x}}
{a_x+t_{r,x}+h_{r,x}+i_{r,x}+1}\ge0.
\]

Every ingredient is already recorded in `bits` and `second_hist`. Reordering
histogram entries among the five indices does not change this coefficient.
The frozen point instead evaluates to

\[
-\frac{472389383909475144797520617350241251969}
{908679097461847926994104235006019918544}<0.
\]

Consequently **there is no full pure SPE completion of these exact frozen
customer marginals with the advertised named branches**, under any assignment
of the common indices or coupling between families. This rules out upgrading
this particular LP witness to a game counterexample without changing its
marginals. It does not rule out other points of the relaxation or other SPE.

The same method also gives negative terminal rows comparing `S_i^AB` against
`R_j^AB`, comparing `S_i^AE` against `R_j^AE`, and comparing `J_i` against
`H_j`, always with `i != j`. The script records all exact values.

## Verification and assets

Run `python .../continuation_completion/offdiagonal_closure.py` from any
directory. It reads the source certificate, expands each histogram into five
literal indexed states, and independently checks all twenty same-history
deviations against the compact histogram formula on each atom. The `.json`
records all ten terminal closure rows and four violations, plus the source
hash. Parent and sibling agents independently reconstructed the strongest
row directly from the source, with the same exact result.

The earlier `exchangeable_last_closure.py/json` also constructs and examines
one conditional-independent exchangeable lift. Its cross-family failures only
exclude that lift. The four same-family off-diagonal failures above are stronger:
they exclude every lift of the fixed marginals, so the independent-lift
assumption is not used in the obstruction proof.

Next: add the off-diagonal rows to the unrestricted type relaxation and
re-optimize. A finite-support re-optimization is merely a diagnostic unless its
dual residual is checked over every allowed type.

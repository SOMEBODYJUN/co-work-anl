# Support — fixed six-player/seven-topic LP cone

## Exact object and model

The target is the registry object `cag-r70-six-player-seven-topic-fixed-complete-strategy-lp` at pin `b85fbfeafe5b02e918438e2de0d948d6296a19524e6f06adb310a997d34eb2bb`. The model is the common-label customer-attraction game: finite unit customers, a finite nonempty labelled topic catalogue (labels may have identical coverage or be empty), six ordered unit providers, all ordered histories, repeated actions, and arbitrary weak ties. A forced action is followed by the same original strategy on the changed history. At the root \(W=\sum_i u_i\) is the covered customer count; an already occupied prefix has a separate remaining-profit quantity \(R_b(c)\), which is not the root welfare and is not paid by this object.

The saved complete policy has 19,608 entries, exactly
\[
1+7+7^2+7^3+7^4+7^5=19,608
\]
ordered decision nodes. Its root continuation has count \(q=(1,0,5,0,0,0,0)\). The complete JSON was parsed in full: all history prefixes exist, actions lie in the seven-label domain, and the terminal continuation from the root reproduces that count. In this concrete policy every action is 0 or 2 and the action is constant over histories with the same count vector; this is an observed property of this σ, not a licence to replace the complete ordered-history contract by a count-only strategy in general.

## What the LP actually constrains

There is one nonnegative variable \(x_M\) for each of the 127 nonempty customer-interest masks \(M\subseteq\{0,\ldots,6\}\). For every ordered decision history and every alternative label, the row is the true continuation comparison
\[
G_{h,b}=f_{a_\sigma(h)}(q_\sigma(h))-f_b(q_\sigma(h,b)),
\qquad G_{h,b}x\ge0,
\]
where the second terminal count is recomputed after forcing \(b\) and then following σ. The original 117,648 nonself comparisons collapse only to 3,048 equal coefficient keys; the exact audit reconstructs all 387,096 matrix coefficients and checks the 198,672 nonzero entries against independently evaluated reciprocals. This is the full SPE cone for this one σ, not a static PNE system and not a frozen-on-path deviation.

The root welfare coefficient is \(c_M=1_{M\cap\{0,2\}\ne\varnothing}\). For each omitted label \(j\), \(v^j_M=1_{M\cap(\{0,\ldots,6\}\setminus\{j\})\ne\varnothing}\) is the coverage by the six-label support omitting \(j\). The LP normalizes \(v^j x=1\), imposes all other six-label coverage rows \(v^k x\le1\), and minimizes \(cx\). Since six slots can repeat labels, extending any optimum with fewer than six distinct labels gives the same optimum; with seven labels an optimum is represented by at least one omitted-label support. This is the static OPT normalization only; all dynamic incentive rows remain the true full-tree rows above.

## Exact lower bound and attainment

The independent cone audit recovers seven rational duals. Their inequality multipliers use the scipy sign convention in the stored JSON; after converting to \(Gx\ge0\), they are nonnegative multipliers. The omitted-label bounds are \(6/11\) for \(j=0,2\) and \(3/5\) for \(j=1,3,4,5,6\). Every one of the 889 dual-column residuals is an exact nonnegative Fraction with minimum zero; the five \(3/5\) entries are lower bounds only, not claims of individually attained optima.

The added dependency `M-c5e460641b3e47729159aa9e7cb6a175` was read through `map read-add` because its paired exact audit supplies the lower endpoint. Its 11-customer point has multiplicities
\[
x_{\{1\}}=1,
 x_{\{0,2\}}=6,
 x_{\{3\}}=x_{\{4\}}=x_{\{5\}}=x_{\{6\}}=1,
\]
and zero elsewhere. Under the same σ, the actual path is \((0,2,2,2,2,2)\), so \(W=6\); choosing labels \(0,1,3,4,5,6\) covers all 11 customers, so \(\mathrm{OPT}_6=11\). The independent point audit checks all 137,256 ordered comparisons (including 19,608 self rows), all 924 terminal multisets, and obtains minimum exact IC slack zero. Thus the dual lower bound and this feasible point give the exact fixed-cone minimum \(W/\mathrm{OPT}_6=6/11\), with \(2W-\mathrm{OPT}_6=1\).

The same added package also records a separate 58-customer all-SPE construction with \(W=43,\mathrm{OPT}_6=58\). That point is not the 11-customer equality witness and must not be silently merged with it.

## Scope and unpaid obligations

The whole result is only the exact minimum over the nonnegative customer-type cone satisfying every true IC for this one saved σ. It does not quantify over all complete six-player strategies, all catalogues, or other numbers of players/topics. It does not prove the global six-player half target \(2W\ge\mathrm{OPT}_6\); \(6/11>1/2\) is a fixed-policy value and therefore leaves the universal quantifier unpaid. It also does not pay a remaining-player/background theorem: \(R_b(c)\) and root \(W\) are different quantities, and no transfer to a nonzero-prefix budget is made.

The 37 static PNE count reported for the 11-customer point is diagnostic only. It neither establishes the full SPE cone nor substitutes for the 3,048 true IC rows. The model is also distinct from simultaneous facility/customer-load models and from any static security-value or CCE interface. A future relation may reuse the cone theorem’s exact-row semantics, but must preserve the one-σ, root-welfare, all-history and six-slot scope.

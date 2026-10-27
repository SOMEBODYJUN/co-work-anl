# Seven-maxima, six-provider mixed-private obstruction for the incidence-seat certificate

**Status:** exact method obstruction only; not a Q-CAG-HALF-6 counterexample. This records a concrete mixed-private incidence pattern where the existing incidence-seat sufficient interface cannot close with total weight `<=2n`. It does not assert that the welfare claim fails.

Use seven distinct maximal coverages `B_0,...,B_6` and `n=6`. Let `P_0={p_0}` and `P_1={p_1}` be global-private singleton blocks. For each unordered pair `{j,k}` of the five indices `j,k in {2,3,4,5,6}`, add one customer `x_{jk}` belonging to exactly `B_j` and `B_k`. There are no core customers and no other customers. Thus `p_0=p_1=1`, `p_j=0` for `j>=2`, and every nonprivate incidence set is a 2-edge in `K_5`.

For the incidence-seat interface, `f_j(k)=p_j/k+q_j/n`, where `q_j=4` for `j>=2` and `q_0=q_1=0`. Hence

- `f_0(k)=f_1(k)=1/k`;
- `f_j(k)=4/6=2/3` for `j=2,...,6` and every `k=1,...,6`.

The sixth-largest seat is `nu=2/3`. For the two private maxima, exactly one seat is strictly above `nu`, so `a_0=a_1=2`; the nonprivate maxima have no private lower-bound constraint. The sufficient interface requires

```
y_0 >= 2,  y_1 >= 2,
 y_j+y_k >= 6   for every edge {j,k} of K_5,
 y_j >= 0.
```

The five-node edge constraints have minimum total `sum_{j=2}^6 y_j=15`, attained by `y_j=3` for all five nodes. Therefore every feasible `y` has `sum_j y_j >= 2+2+15=19>12=2n`.

The exact LP-dual witness is equally simple: set private multipliers `lambda_0=lambda_1=1`, all other `lambda_j=0`; set `mu_{jk}=1/4` on each of the ten `K_5` edge constraints. Every nonprivate vertex is incident to four edges, so its dual load is `1`; the private constraints have load `1`. The dual objective is

```
2*lambda_0 + 2*lambda_1 + 6 * (10/4) = 4+15 = 19.
```

Thus the incidence-seat route's condition `(sum y_j <= 2n)` is exactly separated on this pattern. The instance is only a structural witness against that certificate: no complete SPE, actual welfare, or target violation is supplied here. It confirms that the remaining seven-maxima gap genuinely includes two-or-more private blocks and cannot be removed by reusing the existing seat LP unchanged.

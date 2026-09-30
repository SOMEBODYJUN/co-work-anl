# Exact extremal equilibrium load is weakly NP-hard

Let `d=A-B`, let each common player have positive integer weight `w_i`, and write their expected signed contribution as `c_i` (`+w_i` for pure A, `-w_i` for pure B). Put `Delta=d+sum_i c_i`. At equilibrium:

- a pure-A player requires `Delta <= w_i`;
- a pure-B player requires `Delta >= -w_i`;
- a genuinely mixed player has `c_i=Delta` and `|Delta|<w_i`.

The following reduction shows that deciding whether an equilibrium with `Delta <= -Q` exists is NP-complete, even for positive integer weights and integer private loads. Consequently computing the minimum equilibrium expected load at A is NP-hard, since that load is `(A+B+sum_i w_i+Delta)/2`.

## 1. The source problem

**2-bounded subset sum:** given positive integers `a_1,...,a_n` and an integer `R`, determine whether there are `t_i in {0,1,2}` such that `sum_i t_i a_i=R`.

This problem is NP-complete. Here is an explicit reduction from ordinary SUBSET SUM, so no external hardness theorem about the variant is required. Given positive `b_1,...,b_N` and target `S` with `0<=S<=sum b_i`, let `M=2 sum b_i+1`. For each `i=0,...,N-1`, produce two numbers

```
a_{2i+1} = M*5^i + b_{i+1},
a_{2i+2} = M*5^i,
R = M*sum_{i=0}^{N-1}5^i + S.
```

If the two multiplicities are `x_i,y_i in {0,1,2}`, then their low-order contribution `sum_i x_i b_{i+1}` is less than `M`, and each base-5 digit `x_i+y_i` is at most 4, so there are no carries. Equality to `R` therefore forces `x_i+y_i=1` for every i and `sum_i x_i b_{i+1}=S`. Thus `x_i in {0,1}` gives exactly an ordinary subset-sum solution, and conversely. The constructed numbers have polynomial bit length.

We may assume `0<=R<=2 sum_i a_i`; out-of-range targets are immediate NO instances.

## 2. Game construction

Write `U=sum_i a_i` and choose `Q=2U+R+1`. Make:

- `n` variable players of weights `Q+a_i`;
- `n+1` anchor players of weight `Q`;
- private-load difference `d=R-U`, implemented by `A=max(d,0)` and `B=max(-d,0)` (add the same positive constant to both if positive private loads are required).

The construction has polynomial size and uses positive integer common weights. Its total common weight is

```
W=(2n+1)Q+U,
d+W+Q=2(n+1)Q+R.
```

## 3. No equilibrium can have Delta < -Q

At such a difference every anchor must be pure A: pure B would require `Delta>=-Q`, and mixing would require `|Delta|<=Q`. Even allowing every variable contribution to be as low as its negative full weight gives

```
Delta >= d+(n+1)Q-sum_i(Q+a_i)
      = Q+R-2U
      > 0,
```

contradicting `Delta<-Q`.

## 4. Characterize equilibria at Delta=-Q

Every anchor is pure A or pure B. (A declared mixer at its boundary is simply pure B.) Every variable can be pure A, pure B, or genuinely mixed with signed contribution `-Q`. Define `t_i=0,2,1` respectively for these three states. Let `r` be the total number of non-A players, including anchors and variables.

Relative to the all-A contribution, a non-A anchor reduces the difference by `2Q`; a pure-B variable reduces it by `2Q+2a_i`; a mixed variable reduces it by `2Q+a_i`. Therefore

```
d+W+Q = 2Qr + sum_i t_i a_i,
2Q(n+1-r) = sum_i t_i a_i-R.
```

Because `0<=sum_i t_i a_i<=2U` and `Q=2U+R+1`, the right side has absolute value less than `2Q`. It follows that

```
r=n+1, and sum_i t_i a_i=R.
```

Conversely, suppose such `t_i` are given. Assign variables in states A, mixed, B for `t_i=0,1,2`. If `s` variables are non-A, make `n+1-s` anchors pure B and all remaining anchors pure A. Then `r=n+1`, the resulting difference is exactly `-Q`, and every best-response condition holds. In particular the mixed variable of weight `Q+a_i` uses

```
p_i = (1-Q/(Q+a_i))/2 = a_i/[2(Q+a_i)] in (0,1).
```

Thus the constructed game has an equilibrium with `Delta<=-Q` if and only if the 2-bounded subset-sum instance is YES.

## 5. Membership in NP and interpretation

A support pattern has three choices per player. With k mixed players it gives `(1-k)Delta=d+sum_pure signs*w`. For `k!=1`, this determines a rational `Delta` of polynomial bit length, after which all inequalities can be checked in polynomial time. For `k=1`, the numerator must vanish and the feasible values form an interval whose endpoints are input weights with signs (intersected with the requested threshold). Thus a polynomial certificate exists. The equilibrium-threshold decision problem is NP-complete.

This is a weak hardness result, compatible with a pseudopolynomial dynamic program in integer total weight. It rules out an exact algorithm polynomial in the binary input size unless P=NP.

# Unbounded number of genuinely mixed players may be necessary

Let `A=B`, take `n=2r` common players all of weight 1, and assume `r>=2`. Then the minimum possible equilibrium difference is

```
Delta_min = -(r-1)/r.
```

It is attained by `r-1` pure-A players and `r+1` genuinely mixed players, each with `c_i=Delta_min` (hence A probability `1/(2r)`). Every minimizing equilibrium has precisely this composition, so the number of genuinely mixed players in an extremal equilibrium has no constant bound.

**Proof.** A pure equilibrium has even integral difference in `[-1,1]` and hence difference zero. A one-mixer equilibrium would require an odd number `2r-1` of signs `+1,-1` to sum to zero and is impossible. For `k>=2` mixers, write `b` for the number of pure-B players. If the difference is negative, then

```
q=-Delta = (2r-k-2b)/(k-1), 0<q<=1.
```

The numerator has the same parity as k, while the denominator has the opposite parity, so q cannot equal 1. For `2<=k<=r`, this gives `q<=(k-2)/(k-1)<(r-1)/r`. For `k>=r+1`, the nonnegativity of b gives `q<=(2r-k)/(k-1)`, which is strictly decreasing in k and equals `(r-1)/r` exactly at `k=r+1,b=0`. This proves the assertion.

The smallest counterexample to a proposed two-mixer bound is four unit-weight players: the extremum `Delta=-1/2` needs three mixers, whereas all equilibria with at most two genuinely mixed players have difference zero.

# Strengthening: no private load is necessary

The same NP-hardness holds with `A=B=0`, so every customer can choose either facility. First replace the 2-bounded subset-sum target `R` by `R'=max(R,2U-R)`. This preserves solvability through the complement map `t_i -> 2-t_i` and guarantees `U<=R'<=2U`. Use `Q=2U+R'+1` and the previous variable and anchor weights. Set the private loads to zero. Instead, if `d=R'-U>0`, add one common player of weight d; if d=0, add nothing.

Since `0<d<Q`, this extra player must be pure A in every putative equilibrium with `Delta<=-Q`. It therefore simulates the former private-load difference d exactly in every equilibrium relevant to the threshold. The exclusion of `Delta<-Q` and the characterization of `Delta=-Q` remain unchanged. Consequently the minimum equilibrium expected load of a specified facility remains NP-hard to compute even in the completely symmetric two-facility game with no private customers. The corresponding load threshold is `(W-Q)/2`, where W includes the optional extra player.

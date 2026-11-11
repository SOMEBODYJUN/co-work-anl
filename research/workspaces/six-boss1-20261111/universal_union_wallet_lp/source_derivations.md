# Universal actual-atom / optimal-union wallet projection: source derivation

Boss1; RUN `six-boss1-20261111`. This file is written before matrix generation or optimization. The only optimization authorized for this workspace is one new finite LP. No old LP point is an input.

## Scope and variables

Fix any instance and any complete ordered-history pure SPE from `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`. Let its actual actions be A1,...,A6, and let X be one globally maximizing label for f_P, where P is the actual first-four load. Fix any optimal six-label menu and let O be its coverage union. O is never treated as a legal label. If OPT6=0 the desired half inequality is immediate. Otherwise divide all customer counts and K by OPT6.

For every tuple (a1,...,a6,x,o) in {0,1}^8 introduce a nonnegative atom mass z; keep all 256 tuples, including the zero tuple and customers outside O. Introduce K=max_L |L|/OPT6 as one further nonnegative scalar. Then sum(o z)=1. All expressions below are sums over these same atoms. Write

    c=sum_i a_i; P=a1+a2+a3+a4; b_i=sum_{j<i}a_j;
    u_i=sum z a_i/c (zero if c=0); W=sum z 1[c>0];
    D=P+1; F_X=sum z x/D;
    f(q)=sum z q/D; g(q,r)=sum z qr/[D(D+1)].

There is no 16-history restriction, no symmetry restriction, and no independent-customer or independent-query assumption. Identical label coverages remain permitted. The LP is a necessary projection, not a representation theorem for full SPE.

## 1. Actual source SAFE: 48 rows

At the actual source-i history, a true deviation to any legal label Q, followed by that history's prescribed continuation, gives the deviator at least sum q/(b_i+7-i): at most 7-i remaining players can cover each queried customer. Source IC therefore gives

    u_i >= sum z q/(b_i+7-i), i=1,...,6.

Use every q in A1,...,A6,X. Averaging the six legal optimal-menu queries gives the same inequality with their membership count d/6. Since d>=o and the denominator is positive, weaken to q=o/6 for one further row at each source. The source-6 pure rows are the exact actual terminal BR inequalities. The source-6 query A6 row is identically zero and may be pruned.

## 2. Common-X union-prefix inequalities: 4 rows

`main_optimal_union_prefix.md`, backed by `main_averaged_menu_prefix.md`, proves for i=1,...,4 and C=(31,25,19,10):

    C_i u_i - (C_i-1) sum z x/(b_i+7-i)
      >= sum z (o/6)[x/(b_i+7-i)+(1-x)/(b_i+1)].

The same X works at all four sources. For sources 1,2,3 the source-X IC, last-label SAFE, every intermediate label's actual-P maximum inequality, and the true last node's six-query average have fixed nonnegative weights (25,6,4/5,1), (20,5,19/20,1), and (15,4,7/6,1). The exact all-type residual in the cited Main derivation is nonnegative for theta=o/6 in {0,1/6}. Source 4 uses the proved C4=10 H3 residual, affine in its query bit. Thus the union operation weakens paid true queries; it never adds O to the catalog.

## 3. Global maximum and actual fifth MX: 14 rows

Global maximality supplies F_X>=f(A_j), j=1,...,6. Averaging the six optimal-menu inequalities and d>=o supplies F_X>=f(o)/6.

At the true actual fifth node, let Q_L be the true last reply after forcing a legal L. Source IC and this reply's BR against X give

    u5 >= f(L)-g(L,Q_L)
       >= f(L)+f(X)-g(L,X)-f(Q_L)
       >= f(L)-g(L,X) = sum z l/(D+x).

The last step uses the one global maximum F_X>=f(Q_L). Use L=A1,...,A6 and average/weakly replace the optimal-menu count by o for the seventh row. These seven rows are exact duplicates of certain RC rows below; their source derivation and alias names are retained.

## 4. The two actual terminal wallets: 36 rows each

The old true-reply owner `真实末回复的共同潜力上限与重叠参数端点--引理.md` gives, at the single actual first-four history,

    RC(L,R): u5+F_X >= f(L)+f(R)-g(L,R).

Its payment is fifth-node IC for L, the true reply Q_L's terminal BR against R, and F_X-f(Q_L)>=0. These three inequalities use the same Q_L. No frozen actual reply appears in the deviation branch.

For the second wallet, `main_full_average_pair.md` gives

    PAIR(L,R): u5+u6+g(A5,A5) >= f(L)+f(R)-g(L,R).

Payment is the same source IC and Q_L's BR against R, the actual terminal BR against that same Q_L, and the pointwise slack g(A5,A5)-g(A5,Q_L)>=0. Equivalently the actual terminal BR against X first gives F_X<=u6+g(A5,X)<=u6+g(A5,A5), so PAIR also follows from RC and this comparison. We retain PAIR as a requested paid family; being different rows does not establish cone independence.

For each wallet use all unordered pairs with repetition from the eight query roles A1,...,A6,X,Omean:

* For two pure roles q,r, retain the exact overlap qr in f(q)+f(r)-g(q,r).
* For pure q and Omean, average six true queries. Its RHS is f(q)+sum z[d/(6D)-qd/(6D(D+1))]. The coefficient of d is positive, so replacing d by o gives f(q)+sum z[o/(6D)-qo/(6D(D+1))].
* For Omean with itself, average all 36 ordered optimal-menu pairs. The exact RHS is sum z[d/(3D)-d^2/(36D(D+1))]. For d>=1, subtracting the d=1 value yields (d-1)[12(D+1)-(d+1)]/[36D(D+1)]>=0. Since d=0 iff o=0, the paid weakened RHS is sum z[2o/(6D)-o/(36D(D+1))]. This is the 36-pair average, not a diagonal six-pair average and not an independence assumption.

There are 28 pure/pure, seven pure/mean and one mean/mean rows per wallet. All share the same actual P, X, u5, u6, and actual fifth membership a5.

## 5. Optimal-cover and global-size constraints: 22 rows

Every six-of-seven union from {A1,...,A6,X} is a union of six legal labels, so its normalized coverage is <=1: seven rows. All smaller submenus are covered by one such superset or repeated-label completion. The actual W<=1 is listed as well and deduplicates against the union omitting X.

By definition of the true global maximum size, K>=|A_j| for j=1,...,6, K>=|X|, and K<=1. Every actual source can truly deviate to a K-maximizing legal label; no final load exceeds six, giving u_i>=K/6 for all six i. These use K's true global meaning, rather than asserting that the visible seven labels attain K.

## 6. Root near-saturation: one additional proved row

Main supplied and this worker fully read `最大主题根近饱和的覆盖阈值--推论.md` before optimization. For a largest legal C, set E=6u1-K. On the true root-C branch, its seat deficit d=sum_C(6-c) obeys d<=5E; if d_L is the last label's missed C mass, cardinality bounds give outside incidences <=d-d_L and last outside size <=d_L. Its last payoff t satisfies t<=v+4d_L/5. The true terminal query Q pays at least |Q\\C|+|Q∩C|/6-(d-d_L)/2, because 1/(1+k)>=1-k/2 for integer k>=0. Thus

    |Q\\C|+|Q∩C|/6 <= v+d/2+3d_L/10 <= (K+25E)/6.

Sum over the six optimal queries and retain their union; its intersection with C is at most K. This proves OPT6<=(11/6)K+25E=150u1-(139/6)K. The normalized added row is

    150u1 - (139/6)K - sum z o >= 0.

K here is independent of the f_P-maximizing X. Combining with the other five size floors gives W>=(889K+6)/900, hence half when K>=444/889. This prior conditional bound already dominates the large-X condition of Main's union-prefix draft; none is claimed as a new sharp universal theorem.

## 7. Root rigidity with retained K: 56 additional rows

Main supplied and this worker fully read `任意人数近饱和根主题刚性--引理.md` before optimization, including its all-integer pointwise transfer proof and factorization. For a root-forced legal T, write true branch first and last payoffs v,w, middle memberships n, actual root payoff u1, and t=|T|. Its pointwise transfer inequality sums to

    F_T(Q)-k_Q+w-v
      <= (1/2)sum_{j=2}^5(|B_j|-t)+(|B6|-t)+24(v-t/6),

where F_T(Q)=sum q(1-5t_bit/6) and k_Q is the true last node's payoff from querying Q. Use that node's w>=k_Q, every |B_j|<=K, and v<=u1. The result is

    F_T(Q) <= 25u1+3K-7|T|.

The underlying pointwise inequality holds for every p,z,q in {0,1} and n in {0,...,4}; it is proved in the owner by explicit p=0 estimates and the p=1 factorizations, without any restricted-history hypothesis. Use the seven legal anchors T=A1,...,A6,X and the eight queries Q=A1,...,A6,X,Omean. For Omean average the six legal queries and replace d by o, valid because 1-5t_bit/6 is positive. Never use O as an anchor. This adds 56 rows without additional hidden atom bits.

## Matrix and certificate protocol

The original requested families contain 160 inequality rows. The two subsequently authorized root families add 57, for 217 raw rows. Keep all 257 variable columns; remove only zero rows and exactly duplicate affine rows, keeping alias provenance. All other pointwise nonnegative or redundant rows remain. Use one floating LP solely for discovery, save its full result and all exact input coefficients, then recover a rational feasible point or rational dual by exact linear algebra. Every delivered conclusion must be checked against all 217 raw rows and all variable nonnegativity conditions using exact rational arithmetic. A feasible objective below 1/2 establishes only insufficiency of this specified necessary system, not an SPE counterexample and not a no-go theorem for other valid inequalities.

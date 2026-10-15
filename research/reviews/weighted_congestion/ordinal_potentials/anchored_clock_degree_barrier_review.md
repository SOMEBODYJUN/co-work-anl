# 三次锚定三元时钟的保边障碍：独立重构、简化对偶与强化审查

Reviewer: boss4 internal `stronger_lower` agent. No Git writes or public
publication are performed by the reviewer.

## Frozen targets and reconstruction order

Author claim: `WC-ANCHORED-DEGREE-THREE-LOCK-OBSTRUCTION-v1`.
Author frozen source:
`/workspace/scratch/ecf05625b47b/degree_three_anchored_clock_obstruction_frozen.md`,
SHA-256 `575dbf4fe1ad0b533d188d54e1ad32aad5f143a1e3f1828d524e22d2f33547b2`.
Author audit:
`/workspace/scratch/ecf05625b47b/verify_degree_three_clock_obstruction.py`,
SHA-256 `508c37f6cbdb76d77ac995215011dae7860080e2f2ed6c8c399fa5ab76d23e2b`.

The reviewer first received the precise architecture, then the fixed base,
without reading the author's proof or certificates. The reviewer reconstructed
all twelve raw-power columns and the base costs from literal resource user
sets. A discovery LP suggested the dual cone, after which a direct integer
search produced the four simple exact witnesses below. Those witnesses were
reported to the boss before the author certificates were supplied. The final
audit uses only standard-library Fraction arithmetic and fixed exact witnesses;
neither solver output nor floating-point feasibility is a premise.

Afterward the frozen author proof and code were read and attacked separately.
Both sets of witnesses are independently recomputed in the final audit. The
author's stated full-strict-cycle claim and the reviewer's stronger two-edge
weak-retention conclusion are distinguished explicitly below.

## Exact scope and stronger conclusion

Fix weights `(1,1/2,1/4,1/8)` and `alpha=21/20`. The base is precisely the
four complementary cubic resource pairs with signatures and coefficients
listed in the frozen source. Let `gamma>0` multiply every base latency.
For each of `T012,T013,T023`, add zero or finitely many complementary pairs
with local literal patterns `010/101`. The two sides of each pair must have
the same arbitrary nonnegative-coefficient polynomial of degree at most
three. Different triples may have independent polynomials and may be omitted.
Adding these resources augments the same two strategies of each participant;
it creates no extra actions or players.

Write `G_j` for the *total* alpha margin on sweep edge `j`, with the sweep

    0000 --0--> 1000 --1--> 1100 --2--> 1110 --3--> 1111
    1111 --0--> 0111 --1--> 0011 --2--> 0001 --3--> 0000.

The strengthened conclusion proved here is:

    If G_0>=0 and G_2>=0, then at each of 0101 and 1010 every
    nontrivial unilateral alpha margin is strictly negative.

In particular both states are alpha-PNE. Thus preserving all eight original
strict alpha improvements cannot remove these off-cycle equilibria. This
does not prohibit higher degree, another anchor, other literal patterns,
different fees on opposite phases, auxiliary players, or other clock graphs.
It is a fixed-architecture obstruction, not a full-model lower bound.

## Literal reconstruction of the base

A signature entry `+` maps action `s_i` to resource side `s_i`, entry `-`
maps it to side `1-s_i`, and `0` means unused. Each actual resource load is
the sum of the positive weights of its actual users. Applying `z x^3` then
gives the first-half sweep margins

    b0 = 55201793/7500000000,
    b1 = 1725121/234375000,
    b2 = 248398189/33750000000,
    b3 = 49676111/6750000000.

All are strictly positive. Complementing all action bits interchanges every
resource with its equal-fee mate, so the second-half margins repeat them.

At `b=0101`, the four pairs of current and flipped costs are

| Player | Current | Flipped |
| --- | --- | --- |
| 0 | 32540497/375000000 | 37816003/140625000 |
| 1 | 581175629/3375000000 | 373299779/562500000 |
| 2 | 18078389/187500000 | 56643761/70312500 |
| 3 | 158884799/1687500000 | 26108689/112500000 |

Every current cost is strictly smaller, proving exact PNE for the unaugmented
base and its positive rescalings. Its alpha margins `h_i^base` are

    (-122240519/625000000,
     -17706129787/33750000000,
     -234206903/312500000,
     -1009308211/6750000000).

No deviation load is frozen. The same calculations hold at `1010` by
complement symmetry.

## All twelve clock columns and exact row table

For each triple and each degree `k=0,1,2,3`, use the raw column whose two
resource fees are exactly `x^k`. Let the coefficient vector `a>=0` contain
the twelve arbitrary real polynomial coefficients in this order. Every
allowed augmentation is exactly their nonnegative linear combination;
duplicate pairs add coefficients. Constants and sparse/zero polynomials are
included, without any continuity or numerical-search inference.

Let `M_j` be the clock-only margin row on sweep `j`, and `T_i` the clock-only
margin row for player `i` at `0101`. Each entry below is multiplied by the
same positive scale `10240`; each cell lists its degrees `0,1,2,3` in order.

| Row | T012 columns | T013 columns | T023 columns |
| --- | --- | --- | --- |
| M0 | (-512,-3328,-8192,-16288) | (-512,-4608,-11232,-21708) | (-512,-1920,-3840,-6420) |
| M2 | (-512,-5760,-11040,-16680) | (0,0,0,0) | (-512,8768,14488,19433) |
| T0 | (-512,7168,20608,44128) | (-512,3264,9432,19251) | (-512,-4544,-10088,-17711) |
| T1 | (-512,12544,28672,53536) | (-512,8640,18840,31935) | (0,0,0,0) |
| T2 | (-512,15232,30688,54712) | (0,0,0,0) | (-512,-9600,-15360,-20460) |
| T3 | (0,0,0,0) | (-512,-16192,-28232,-46117) | (-512,-8256,-12168,-14769) |

The scale is exact: every load is an integer multiple of `1/8`, and the
margin is `x^k-(21/20)y^k`, so `20*8^3=10240` clears every denominator.
Whenever degree zero is charged, the user has positive load; empty resources
have no user cost and are not evaluated through a gratuitous `0^0`.

## Independent simpler certificates and strengthened proof

The row table directly verifies the following twelve-column inequalities:

    T0+3M0<=0,
    T1+4M0<=0,
    T2+3M0+M2<=0,
    T3<=0.

Equivalently the five-coordinate witnesses on `(M0,M1,M2,M3,Ti)` are

    (3,0,0,0,1), (4,0,0,0,1), (3,0,1,0,1), (0,0,0,0,1).

Their corresponding base bounds are

| Player | h_i^base + mu_i dot b |
| --- | --- |
| 0 | -433760283/2500000000 |
| 1 | -16712497513/33750000000 |
| 2 | -48601446259/67500000000 |
| 3 | -1009308211/6750000000 |

They are all strictly negative. If `H_i=gamma h_i^base+T_i a` is the total
off-state margin and `G_j=gamma b_j+M_j a`, nonnegative coefficients give

    H_i <= gamma(h_i^base+mu_i dot b)-mu_i dot G.

Only `G0` and `G2` appear, with nonnegative multipliers. Under the two weak
retention hypotheses the last term is nonpositive, while the first term is
strictly negative because `gamma>0`. Thus every `H_i<0`.

All resource pairs preserve global complementation, including constant and
zero terms, so the same four strict inequalities hold at `1010`. There is
only one nontrivial alternative action per player, so this checks all legal
nontrivial deviations. Self-deviation satisfies the approximate inequality
automatically. This closes the stronger claim over the complete real
nonnegative coefficient cone and every positive common base scaling.

## Attack on the frozen author's separate certificates

The author instead uses normalized columns `(x/W_T)^k` and five-coordinate
witnesses

    (58,0,18,0,24), (70,0,10,10,10),
    (86,0,0,7,7), (44,0,28,0,28).

Those are genuinely different from the independently found simpler witnesses.
The audit checks all 52 author inner products (base plus twelve normalized
columns for each player) and obtains the strict negative values stated by the
author. Conversion between column conventions multiplies each raw column by
the positive factor `W_T^(-k)`; it does not change the cone of allowed fees.

All first four author coordinates are nonnegative and the target coordinate
is positive. The base inner product is strictly negative, so positive common
base scaling and arbitrary nonnegative clock sums remain strictly separated.
The author proof therefore establishes its stated full-strict-cycle result;
indeed its same witnesses also allow all four first-half sweep margins to
be weakly nonnegative. The independent witnesses further reduce the required
set to only sweep edges 0 and 2. No statement about arbitrary cycle compilers
or the target growth rate follows from either certificate.

No fatal objection was found in the author's scope, constant-term handling,
base scaling, real-coefficient coverage, full off-state action checks, or
complementation argument.

## Audit interface and frozen independent evidence

Canonical independent audit:
`tests/audits/weighted_congestion/cyclic_clone/independent_clock_degree_barrier.py`.
It uses only Python's standard library, with all mathematical inputs literal
in the script. It emits JSON to stdout by default; `--output NEW_PATH` uses
exclusive creation and refuses to overwrite. The JSON includes the exact
invocation, Python version, script hash, canonical literal-input hash, all
resource data, full column matrices, both certificate families and exact
arithmetic counts.

Independent frozen run:
`evidence/runs/weighted_congestion/cyclic_clone/independent_clock_degree_barrier.json`.

* Script SHA-256:
  `7b5a3d4c672c2f142f2e1de59b678166f825e989b7495c5fbdfea725b23f6a80`.
* Literal-input SHA-256:
  `12880d31d1b6af4c060018eaa2a1223ab0a26bb34497180da9f15d94d3bb63ba`.
* Run SHA-256:
  `fc9439eddf9e0751d8a0aa7aeafb36aed73fe7d55d048fc2452e3ea856b13cce`.

The run checks 48 independent nonpositive column residuals, four strict base
bounds, 52 strict author products, eight strict base sweep edges, eight base
off-state cost comparisons, and 832 complement-margin identities. Stdout JSON
and the refusal to overwrite an existing output were also executed and checked;
the existing run bytes remained unchanged. There is no random input, numerical
tolerance, or solver dependency in the final certificate.

Truth: exact proof of the specified architecture obstruction and the stronger
two-edge premise. Value: a reusable finite-column separation and explicit
degree-preserving compiler failure. Novelty: unverified. Mechanism: positive
column-cone duality with fixed original base. Ambition: method boundary only;
the unrestricted main existence/nonexistence question remains unresolved.

## 入库强化版本合同

现行正文为[三次锚定时钟次数保持障碍](../../../current/weighted_congestion/anchored_clock_degree_barrier.md)。它把本审查预读阶段独立发现的简单四个dual及两条弱环条件纳入同一新Claim身份；原作者冻结稿的全严格环命题是其推论，不静默改写其他既有Claim。作者代码迁入`tests/audits/weighted_congestion/cyclic_clone/verify_clock_degree_barrier.py`，主研究者在原代码上追加本节简单证书逐项检查并冻结新结果`evidence/runs/weighted_congestion/cyclic_clone/clock_degree_barrier.json`；它仍核查原52个严格内积。独立源码逐字迁移，运行所得新规范路径记录见上述独立证据，所列旧run hash只标识审查时先前冻结版本。正文表格的12列上界和全部承重不等式在本审查已完整给出，两份代码均重算它们；不把入库路径变更当新数学证明。


## 原全三元统一幅度80次证书：独立重构与冻结攻击

本节只审查新增的 `WC-ANCHORED-FULL-UNIFORM-BUDGET-ESCAPE-v1`，不改变前述degree≤3架构障碍。审查者为本轮独立 `uniform_fixture_review`。先仅接收精确statement及canonical显式基体，未读作者稿、作者实现或作者输出，独立按每一个实际资源及动作membership重建16态64个成本/偏离。随后攻击冻结正文 `research/current/weighted_congestion/anchored_clock_degree_barrier.md`，SHA256 `2d9591c0c341fe4623f1d2f2c219e8c7d8dda27a8293d63bf47b7629481f2019` 的新增第4节。

独立核验全部三个三元、相同幅度M=2αB、局部010/101、D=80，没有省T013、改变两侧费用或借用43次输入的clock。全16态的指定出口严格，其中合法态用原环，非法态用first opposite；任意玩家偏离的真实负载、互补成本/margin及策略非空且不同均直接核对。八行有理外包表按精确分数检查，所有下端点>1/500。B、η、δ、M、阈值以及80不满足(U)、90仍不满足、91首次满足(U)均以有理幂及正分母反乘确认。未找到fatal objection。

独立规范代码 `tests/audits/weighted_congestion/cyclic_clone/independent_full_uniform_clock.py`，冻结结果 `evidence/runs/weighted_congestion/cyclic_clone/independent_full_uniform_clock_degree80.json`。不导入作者代码。默认stdout和`--output`独占创建已检查；旧冻结输入和结果未改写。另一路从不同pair表示实现的 `verify_full_uniform_clock.py` 保存独立复算。

本节结论为固定有限证书及(U)对原架构也非必要；既不反驳满足(U)时的普适次数障碍，也不证明最优80或增长族。内部核验通过不代表外部同行评审或新颖性认证。

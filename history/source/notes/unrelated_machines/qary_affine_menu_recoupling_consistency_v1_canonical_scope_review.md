# q 元 recoupling 的 canonical 实际读后：限定章节审查

审查 ID：`UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1`。

日期：2026-10-18。已实际通读 canonical **全文**，但正式数学认证严格限于 §1–4 及 §9 中对应本 qary v1 的对象、复杂度、证据归属和 scope。§5–8 的另两个 Claim 仅作为上下文读取，不在本次认证中。旧 Exact-only 和作者 Proof 读后记录不修改。

## 实际读取版本

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md`

实际字节数：`16,914`。

实际核对 SHA256：

`b859a872faf453265f3a4d0b99439df104ae7fac4af1dca92ca969e39f6e8b30`

认证仅对应本次读取的该 hash，不预先覆盖未来 canonical 改动。

## 限定结论

**限定范围 PASS；未发现 qary v1 的 standing fatal。** canonical 在 §1–4 完整正确重构了此前 Exact-first 独立证明和作者 Proof 的全部承重步骤，并在 §9 的相应部分正确列出显式总位复杂度、实验归属和主目标仍 OPEN 的边界。

没有认证整个混合 canonical 的所有 Claim。具体说，`UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1` 和 `UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v2` 的断言、端点、K(d) 等仅按本次授权读取为上下文；本记录不替代它们各自的独立审查。

## §1–4 实际落地核对

| 范围 | 实际核对结论 |
|---|---|
| §1 ordinary P 的完整矩阵 | 所有 groups、indexed states、tagged private/resource machines、selectors、incidence jobs 和有限时间均齐全，支持大小 N、private 总量 1 正确。明写全部未选 states 的 jobs 必须执行，没有免费侧条件或机器合并。 |
| §1 固定选择域的实际峰 | `C_L=2-V_L` 明确是选择域受限的真实最优。正向回填每一个原 job；反向包含任意未选-state exports，只提取 selected-state 实际 exports 即得下界。C>=2 分支单独平凡覆盖。 |
| §2 三域与量词 | cyclic、全部 affine A,c、任意 coordinatewise f_i 的定义与源 Exact 一致；partial bundles 始终自由，不要求 product。q>2 affine 上界不冒充全部 nonlinear 选择的上界。 |
| §2 精确数值与 floor/ceil | cyclic/affine 的 ordinary ceil 缺项与 coordinatewise 的整个幂后 floor 均正确；达到值可构造，不靠枚举全部 A 或所有函数。没有把整数配额换成分数物品。 |
| §3 固定 affine 的 Hall/rank 公式 | 对每个 a 的像 fiber 大小、不同 a 的资源层不交、所有组子集的 Hall 下界与全部组总 union 上界，正确闭合 `k=floor Lambda(A)`。c 只作平移。 |
| §3 全部 A 上界 | multiaffine 非零点归纳包含末变量系数为零与非零两种情形；det 的末变量系数非零最高乘积项保证至少 `(q-1)^(t-1)` 个 singular a。没有 A 的形状、rank 或可对角化前提。 |
| §3 cyclic 达到 | 实际方程严格给 `A-diag(a)`、核递推和 `prod a_i=1`；奇异层核维数 1、左度 L/右度 q 的共同 matching 和精确 floor 配额均正确。不是扔掉全部 singular 层。 |
| §4 任意 coordinatewise 非线性 | 一维不同斜率线并集界适用于任意 f_i；全部 groups 遍历 product，故总 selected union 精确 factor。任意全局 partial 分配的上界只用总资源，不假定 B_g factor。 |
| §4 达到 | 取 f_i=0 的 concurrent fractional 证书，每资源容量至多 1、每组质量 alpha^t。由 Hall 或先缩放到 floor(alpha^t) 再用整数 flow，得到真正全局不交 subsets；tensor 不是最终整数 bundle 的结构限制。 |
| §4 极限和端点 | 固定 q 时 cyclic 趋 1、coordinatewise 趋 0；t=1 和 q=2,t=1 的值正确。否定的是指定事后 coordinatewise repair 合同，未声称实现物理一致性。 |

特别确认：全文没有把 `C_sep` 标成无约束普通 P 的 OPT 下界。§1 已用“选择域受限实际最优”明确限定，§2、§4 继续保持该 scope。普通 P 自身允许 cyclic 高值选择；禁止跨坐标依赖的规则仍是逻辑分析条件，不是原 job eligibility。

## §9 中本 qary v1 部分

对 N=q^t，machines `2N^2`、jobs `N^3+N`、finite entries `2N^3+N^2`、dense entries `2N^2(N^3+N)` 正确。标签及普通有理数 1/N 的位长 `O(t log q)`；达界选择和实际整数 flow 只操作完整显式实例。返回所有原 jobs 的 machine identifiers，复杂度不是 `poly(t,log q)`。

给定 A 的 rank 求和只需显式 N 个 a，与 §3 的自足公式一致。§9 中另两个 Claim 的 H 分子分母、K(d) 二分等复杂度不在本次正式认证范围。

canonical 明写审查记录中的有限辅助计算归各 reviewer 自行完成，不记作 root 运行，且不作为一般数学结论前提。此前 1,504 矩阵、24,664 次 rank、3,412 一维函数检查确由本 reviewer 在 Exact-only 阶段执行。本次没有重跑或新增局部参数扫描。

最终段将三个逻辑量尺同真实 source/compiler 义务区分，保持 UM-TARGET-v1 OPEN。这个 scope 声明可以认证；不据此认证 §5–8 的另两个数学主张。

## 保留的源与旧审查

以下旧文件的 hash 在本次冻结时实际复核，未被本记录修改：

| 文件（均位于 scratch 根） | SHA256 |
|---|---|
| `qary_affine_menu_recoupling_consistency_exact_v1.md` | `9d5d0cebf3daa9c78217d32e95f71b80696cd4732f442a22beaf8b22ef50dbd6` |
| `qary_affine_menu_recoupling_consistency_proof_v1.md` | `bc9aa19019bb8466932192253ff148824589aedfc587061df64f016f6bb8461d` |
| `qary_affine_menu_recoupling_consistency_v1_independent_review.md` | `cdd8fcbe71dd9b2d282871b71f9be15321d14d5bca624a1efeb677da411575df` |
| `qary_affine_menu_recoupling_consistency_v1_proof_read_after.md` | `a168d81d40767e8c71be90a2f51b4930bc358dfd6ff6ceeb2cb1e3f2a8eec5b9` |

本次未改 repo、Git、Work 或以上冻结记录。没有外审、新颖性、实现或其它 Claim 的认证升级。

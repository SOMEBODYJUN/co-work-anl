---
id: "customer-attraction/四主题无碰撞两人回复策略LP有限穷举"
kind: "calculation"
type_tag: "计算"
title: "四主题无碰撞两人回复策略LP有限穷举"
status: "finite-experiment-exact-witness-not-global-proof"
summary: "在四个主题、实际末局 C,D 无客户同时覆盖的模型中，枚举 384 个末位回复映射与 6 个比较主题对；浮点 LP 找到 5/4 候选，并用 Fraction 直接核验该候选的所有根/末位最佳回复不等式。该脚本本身不是任意目录上界证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/construction/two_player_collision_free.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/construction/two_player_collision_free.py"
legacy_source_id: "0d96e50335c33022effb"
---

# 对象与冻结来源

冻结源是 `two_player_collision_free.py`（blob `94521d789726e418be817c953562eac3c716ecd6`，SHA-256 `c7390c9a74878e92cd3dd7e41589310761118c5a4823e035f2b745e54a5d8842`，1783 字节）。`legacy-cleanup` 与 `main` 两个冻结提交的同一路径字节相同。脚本依赖 `numpy`、`scipy.optimize.linprog`、`Fraction`；它把四个主题标成 A、B、C、D，并固定实际首位/末位行动为 `(C,D)`。

这里的“collision-free”是实际两主题不重叠：客户类型用四位掩码表示，枚举所有非空掩码，但删掉同时含 C、D 的掩码。对客户类型 (v)，`mem[v,a]` 是其是否属于主题 (a)，而

\[
 u(a,b)=\frac{\mathbf 1_{v\in a}}{1+\mathbf 1_{v\in b}}
\]

是主题 (a) 的单位客户份额（另一位选 (b) 时有重叠则减半）。客户权重总和归一化为实际覆盖 (W=\mathbf1_C+\mathbf1_D=1)。

# 脚本实际枚举与量词

`replies` 是一个从首位主题 (a\in\{A,B,C,D\}) 到末位回复的映射，共 (4^4) 个；只保留 `replies[C]=D`，所以保留 (4^3=64) 个映射。对每个映射，脚本加入：

* 对每个首位 (a) 和所有候选 (b)，末位回复 `replies[a]` 的收益不小于 (b)（真实末位最佳回复）；
* 根在实际选择 C 的收益（因 C、D 无重叠即为 `mem[:,C]`）不小于先选任意 (a) 再按 `replies[a]` 继续的收益。

然后枚举四主题中任意二元比较对，共 6 对，以其并集覆盖 (O) 为 LP 目标。总计运行 64×6 = **384 个 LP**。这是四主题、两名单位玩家、固定完整两阶段策略的有限量词；它没有声称任意主题数的全称结论。

# 精确可复现的输出与候选构造

脚本实际运行输出两次改进，最终 `LPs 384 best 1.25`。最佳记录为：

* 回复映射 `(B,A,D,A)`（按首位 `(A,B,C,D)` 排列）；实际 `(C,D)`；比较对 `(A,D)`；浮点 LP 值 5/4。
* 非零客户类型权重（按掩码）：`1:1/4`、`7:1/2`、`8:1/4`、`10:1/4`。乘以 4 即为五名单位客户：A-only 1 名，A∩B∩C 2 名，D-only 1 名，B∩D 1 名。
* 实际覆盖 (W=4)；A∪D 覆盖 5 名客户，故候选比 (5/4)。实际 C、D 没有交集。

LP 返回后脚本把浮点权重转成分母不超过 100000 的 `Fraction`，逐项断言所有末位最佳回复和根偏离约束，并把最佳实例写入 `two_player_collision_free_best.json`。因此该**具体五客户证人**的最佳回复约束被有理数直接核对；这不是对 LP 最优值或更大主题目录的精确全称证明。脚本没有保存每个 LP 的精确有理对偶，也没有用 exact simplex 重做 384 个问题。

# 证明层级与失败边界

这份源文件是“有限实验 + 有理候选核验”，不是完整数学证明。它确实覆盖四主题下所有被编码的末位映射和比较对，但以下量词不在源文件内：任意有限主题目录、任意主题数、任意完整历史树（超过两名玩家）、以及 LP 浮点最优性的严格有理证明。`Fraction(float(x)).limit_denominator(...)` 只能核验找到的候选，不能排除另一个更高的浮点/有理解。

若要把 5/4 升为普遍两人无碰撞上界，应使用同批 `two_player_collision_free_bound.py`/`two_player_collision_free_bound.json` 的六主题逐客户掩码对偶证书（其输出 β=5/4，乘子和 63 个掩码残差均为非负），或使用已保留的逐客户恒等式定理。不能把本脚本的 384 次有限搜索单独当作该上界证明。

# 相关对象与去向

* `d9e2deb241f3440413f7`（`two_player_collision_free_best.json`，SHA-256 `8470454396d1ae7e138a08c7b01451c648bcc58c7ea7230693f9af91d329958e`）是本源直接生成的最佳候选数据；应与本计算对象同处证据包。
* `23c59afb9f2a6498f7c7`（`two_player_collision_free_bound.py`，SHA-256 `867f6f89eb97ab84a4098ed3fb5bd8113e3b3710a2dda2fabf7f037799e79ad3`）及 `a8d42614cbe6ed3610f9`（其 JSON，SHA-256 `b3d276debe470caa39b299fe7dafcdefe3924b832f1cc20721528bbaaa3efbdb`）是独立的六主题必要回复锥 LP/有理残差证书；它们比本源承担更强的普遍上界角色，不能冒充本源内容。
* `4157a234ca8cf21dc537`（`two_player_overlap_refinement.md`，SHA-256 `1646a1fff26071882c8578f96cf2dc3dcff56ffb86bd4c284bd7db8e0a1205a9`）给完整两人 SPE 的解析界 (8\mathrm{OPT}_2\le10W+2I)，无重叠时 5/4；`410387249f58e966c0db`（`background_two_player_refinement.md`，SHA-256 `5dbd316deac78f041204965d5a6b9ced25a5564a95a616b2ec7d22caad8ce86f`）给整数背景下的剩余利润界。二者已是保留正文，量词比本脚本清楚且证明完整。
* R-2fc 的 `collision_free_occupancy_obstruction.md` 及其 Fraction 审计对同一五客户实例逐历史核验完整 SPE、(W=4)、\(\mathrm{OPT}_2=5\)。因此本脚本的数学证人不是新的反例或新定理；它的独有内容是“枚举 384 个四主题末位映射并用 LP 发现该证人”的计算轨迹。R-2fc 的对象属于另一来源族，不能把来源身份合并。

# 处置建议与接续

建议将本源**保留为计算/证据资源**，而不是升级为定理；稳定对象可命名为“customer-attraction/四主题无碰撞两人回复策略LP有限穷举”，目标路径放入 customer-attraction 的 `state/计算` 或相应 evidence 包，并与最佳 JSON、bound 证书建立“有限发现/有理候选核验/普遍对偶证书”关系。若仓库只保留解析正文，数学内容可按“重复证人”并入 R-2fc 的五客户障碍证据，但应保留本源哈希和有限枚举范围，不能写成一般半覆盖反例。

后续若复用：先引用六主题对偶或 `末两人新生重叠的顺序利润税界` 的逐客户证明，再把本源作为端点发现与回归测试；任何向多人、非整数背景、或完整全树量词的推广都需要新增证明。

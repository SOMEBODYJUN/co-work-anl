# ZZ split rational point：固定必要系统支持记录

## 1. 固定输入与精确系统

输入 `split_basic_exact.json` 是固定 16-hist、194 组 `(R,Z)`、582 个显式 01/10/11 joint 和 1306 个 `R-R` overlap 的 1905 列点；`K` 为共同容量，`O=1`。当前点不把 1905 列作为自由变量，而是在 22 个共同 `R` 阈值 slab 内选 275 个 `Z` 质量。`zz_split_exact.json` 的原始 metadata 明确为 old 3889 graph + 60 个 ZZ classes、rows 4005、variables 275、positive 125、free vertex 21、minimum slack 0、非 SPE/non-game。

\[
W=77122220724026571141557320969163/161324472800190691224726909402699,
\qquad O-2W=7080031352137548941612267464373/161324472800190691224726909402699>0.
\]

旧 `split_basic_exact` 本身报告 3945 行、165 个正列和同一 `W`；当前 4005 点在新 `Z` 坐标上重新核旧 3945 行并追加 60 ZZ 行，不能把旧点的 1905 质量与当前点拼接。

## 2. 共同阈值与有理 lift

每个正 hist 的固定 `R` 边缘 `q_g` 把质量轴切成 slab `s=[l_s,u_s)`，质量 `m_s=u_s-l_s`，固定 `r_{s,g}=1[u_s\le q_g]`，并设 `0\le z_{s,g}\le m_s`。阈值回填为

\[
x'_{10,g}=\sum_{r=1}(m_s-z_{s,g}),\quad
x'_{11,g}=\sum_{r=1}z_{s,g},\quad
x'_{01,g}=\sum_{r=0}z_{s,g},
\]

而 `R-R` 辅助坐标取 `min(q_g,q_h)`。层内再以 `0,m_s` 和全部 `z` 端点嵌套分割，得到 43 个正质量原子；`point-audit` 的 `all_582_joint_and_1306_RR_columns_equal_joint_atom_integrals=true` 支付了该重构点的共同会员测度实现。它不支付完整 labelled-catalogue strategy 或 all-history SPE。

## 3. 对角拆分必要性

程序对象从同一完整策略的实际 `A_1,…,A_6`、比较主题和真实末位 `R_{ij},Z_{ij}` 取得 C 族行。36 个有序 `(i,j)` 先聚合，再按 `i\ne j` 与 `i=j` 各拆一行；每项分别来自真实源偏离、末位查询、容量或强 PAIR 必要不等式，所以各子行非负，且逐列相加回旧合行。56 条新增行不是 56 个新客户、不是新策略自由度，行秩也未被声明为 28。

## 4. 证据分工

- `execution.json`：原 verify 真实执行一次，4005 行/275 变量、exit 0、LP 0、stderr 0；不是独立矩阵生成器。
- `interface-audit.json`：完整读取 split 输入字段并核 60 ZZ 行，60 槽为 31 零、29 正，复用已有分数表；不是本轮重新 build 全图。
- `point-audit.json`：独立标准库读取、22 slabs/43 atoms、1905 坐标重构、62 joint + 193 overlap 变化、45 Z 组变化、7931 的 103 变量差异；`graph_builds=0`、`LP_calls=0`。
- `split_basic_exact.json`：旧 3945 行源点，存在 189 个 overlap 低于真实下界的字面障碍；这解释为什么当前重构必须换坐标，而不否定当前 4005 必要系统通过。

## 5. 严格边界

本记录支持一个固定输入、固定阈值域、固定必要行集合上的 exact rational feasible point 及其共同会员 lift。它不支持：任意 `R` 联合、释放 `Z/RZ` 边缘后的新点、全部真实续局 IC、完整目录容量/标签可达性、pure-SPE 存在策略、精确最优性或 `OPT_6`。后继 7931 使用同描述但不同的 103 个 `Z` 质量，且全 pair graph 未重验，必须另证。3B 对端比较保持开放，不在本边中制造跨对象 implication/refutation。

# 一般条件子树流与包含容量合并稿：v2 实际全文读后记录

日期：2026-10-18。审者：sol_true_hardness（6.1sol max）。仅 scratch。

## 1. 实际顺序与 hash

parent 先实际全文读了本审者的两份独立重构，才释放此合并稿：

- inclusion Exact-first：`sol_true_hardness_raw_sh3_inclusion_entry_cut_exact_first_attack.md`，SHA256 `00c51ccf3cc89270d0b1f6b9aa328bf91272fd555a8b605683c6c6495e0ef8a2`；
- general 陈述先行重构：`sol_true_hardness_raw_sh3_general_firstflow_statement_first_reconstruction.md`，SHA256 `f758700937f7ccb7526327eb0f6757639cb69cb0a468e8aadbf1cdf300047e8f`。

本轮实际全文读取 `sol_raw_sh3_conditional_flow_and_inclusion_capacity_canonical_draft_v2.md` 的标题、引言、第一至八节及末尾 v2 说明，SHA256 `011eab0db7ecc5f0b52e09b6d61b1241d46661711bbc1a76565f02f05cbef10d`。
inclusion 作者 Proof 此前已实际全文读后，其本审者记录 SHA256 是 `704bd6ca24eb1a059275bb54e3601b695fd5e6bde735bd56aedd227271a8b96a`。早期所有冻结记录保持原字节；这里不倒填为 general 对全部背景 blind。

未读取作者 flow addendum 其他版本、作者软件、作者输出或 Bamas primary。没有运行新代码。parent 关于其软件全文读取/两路重放的消息只作为 parent 报告，不转为本审者的软件签名。

## 2. 第一至四节：与独立重构逐项对照

原 jobs 的两类、sink 无 home/quota、内部行完整 home 总一、非 home entry E、不同 token 菜单、所有原 one-hot 共同 L 均明确。即使 k=1，home 的 unit 时间也没有让它被误算成根入口。若 E 来自某 native token，其 owner 在 v 的前驱而非 v 后代，因此辅助子实例只保后代 owned tokens 时不会把同一原 job 计两次。

第二节的 degree-4 multiplier null 提升、三投影非负性和第五节以后用到的 unit cap 已在 inclusion 读后核过；本稿同一工具未越界。第三节 b_u=L(E C_u)、y=L(E C_u x) 的 per-token、per-arc、每 head incoming<=b_w，与独立稿完全相同。负载 localizer 的 q=E R 原次数<=2，原乘积次数<=5；不是先条件化再免费拥有原 CFG。

作者先给 f=(a/b)y 的 >=quota 版，再给 f=(r a/S)y 的 exact-quota 版；我独立稿先固定 r y/S 系数直接给 exact 版。两种作者输出都有 f<=y，故按 DAG 新 incoming 定 a 时 a<=b<=p。其他额外 selectors/entries 不产生新流源，也没有把原 b 全部冒充为新 a。

k=1 的特殊 pair 是 incoming/home，而非只有 incoming/incoming。由 L(RY)=0 提升到 L(E C_uY)=0，S_u=b_u，确实可用 out=a 不衰减。与 generic exact r=delta k 的输出分开，不能同时要求非网格 k=1 的 out=a 与 out=delta a。第四节已按可选有效系数表述，没有泛化 ceil。

整数网格时，conditional active home vector 的坐标在 [0,1]、和为 h=(T-1)k，hypersimplex 分解成立。与 incoming 原端标签独立配对，再混 inactive-all-home，可恢复**新流的** row first marginals。没有匹配给定原 row seconds，也没有补齐原实例其他 entry jobs。非网格不声称 full CFG，与我独立稿的 T=9/5,k=2 basic-output 反例一致。

## 3. 第五至七节：完整输入、切与实阈值

包含族的全部物理机器/原 jobs/finite entries、H/M 计数、正 selector mass 及共同 terminal cap 与独立 Exact-first 和作者 Proof 一致。允许 inactive 外送，没有假设 F_SW 是单路径。若 delta d2-M<0，单独用左边非正；非负分支使用入口下界，符号正确。

CONFIG(1) 用完整 marginals 支付所有原 h/f/e，terminal 总质量 d1d2/N<=C/N<=1。实际链调度只是一份完整上界，未改成有限 q 的精确 OPT。四个二项式界与真实 floors 的 polynomial shrink asymptotic 都已核回。

本版明确用有理 0<delta'<min(delta,1)、T'=2-delta' 解释任意固定实 delta 的实际渐近，修复 Exact-first 的定义域澄清。一般算法与必要系统输入仍是 rational T。m>=100q、q 正四倍数、fixed powers of q 和 fixed rho 的范围没有扩大。

## 4. 两项自足证明补款与两项文字精度

未见新的核心 fatal，但本版对迭代删除和位复杂度只给结论，以下付款应直接写入正文或准确引用独立重构第七、八节，才能把稿内证明做全。

其一，删零 marginal 后继续 same raw certificate：Boolean endpoint x 满足 L(x)=0 时，x 是 M3 零列；对任意次数<=2 的 Boolean 单项式 m，L((xm)²)=L(xm)=0，故 xm（次数<=3）也是零列。分解任意 deg<=5 的 multiplier 为 m n，得所有含 x 的次数<=6 moments 为零。由此限制余变量保 ideals、M3 和负载 localizers。原 row CFG 的 first x=0 及非负权重又使其支持不含 x，因而 first/pair 同样保留。只用实际调度也能证明 sound FAIL，但该补款还支付了稿中所有 raw points 的迭代含义。home、job 与 k 一律不删，menu 空的 internal 不变成免费 sink。

其二，位复杂度不能只从每次有理加乘自动推出；本稿可以合法补：先将 c=y/b（>=quota）或 c=r y/S（exact）作为固定有理 transition，再作 DAG 线性递推。每条 path 无重复 arc，全部 transition denominators 的乘积是路径乘积和的共同分母上界，其 bit 数是输入 coefficient bits 的和；a<=p 又控分子大小。故没有反复平方或按 1/p 数值展开。CFG hypersimplex 分解也可给 polynomial support，不要求指数支撑枚举。

两处文字宜明说：第三节的“内部后继行 u”应包括 root v 本身（即“根及其内部后继”）；第四节混 row configurations 前先令 a←a/p、f←f/p，因此 inactive 概率才是 1-a，未归一化时则为 1-a/p。现有上下文意图足够恢复正确证明，这两点不构成数学反例。

上述建议已同步 parent；parent 表示会补迭代 zero 全矩与 metadata。没有把尚未收到的最终正文记为已修、已读或已核。

## 5. 第八节的未代签范围与冻结结论

作者 primary target-read、literal 的文献核验、120 cases/85 FAIL 和小 q=2,m=6 完整矩阵审计，都是该稿作者/parent 的具体 evidence 报告；本审者未读代码/primary，所以不认证其运行字节或论文对应。稿中已说明 q=2 小矩不属于 m>=100q 且 q 四倍数的渐近反证域，未拿小矩替代大族证明。

本稿不是 raw SH3 near-two gap，不给一般 unrelated 近似或困难性，也不由辅助 single-root CFG 合成原全实例完成调度。对进一步细分 B-terminal 的 growing-depth 图没有免费保留同 owner 的路径容量；本轮未审后续探索。

**冻结意见：v2 核心数学与前置独立重构一致，无新 standing fatal。** 迭代全矩与 rational-flow bit 细节可按第四节补为稿内自足证明；本记录只签实际读过的 v2，最终 canonical 仍须另实际读取。

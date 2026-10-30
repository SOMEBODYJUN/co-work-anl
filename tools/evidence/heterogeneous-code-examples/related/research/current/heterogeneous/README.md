# 异构目录双设施：单交叠尖锐 ρ 与一般因子二候选

两个设施分别从有限非空目录 U₁、U₂ 选址；目录可以不同、相交或不交。同一物理地点在两目录中是两个带标签行动。客户有正权重和固定可达集，覆盖后强制参与，费用为包含自身的实现总负载；客户混合采用独立随机化。目标是选择每个合法有标签布局的精确客户 NE，组装一套完整续局并找到近似稳定位置。零收益使用乘法不等式。

本分支必须分开两件事：**一般异构因子二上界仍是内部候选；跨对至多一名共有客户的任意长目录已给尖锐 ρ 的内部完整证明。** 两者均未获外部同行评审；新颖性和优先权另查。存在性论证可用正实数，位复杂度只对显式关联和二进制正有理输入陈述。

## 主要结论与证据状态

| 命题 | 必要范围与结论 | 状态与关键限制 |
| --- | --- | --- |
| HC-2-UP / HC-2-SHARP | 任意上述目录；四种子纯菜单给一般因子二候选，上下界合成尖锐二须同时接受上界 | 上界保持候选；不依赖共同目录 φ 定理；实现或下界不能独立证明上界 |
| HC-2-LOW | 六顶点无向图，每方两个位置，每跨对恰两名共有客户 | 严格占优、唯一客户续局和直接代数给趋近二的整数族 |
| HC-RHO | 跨对至多一共有客户，且至少一侧目录至多两个位置 | 当前全分支证明与内部逐式核对；ρ=2cos(π/7)；纯上界及唯一续局下界 |
| SPARSE-RHO-ALL | 跨对至多一共有客户，双方目录均可任意长 | 高区下降、首个低区入口及同一客户身份已闭合全类 ρ；多路线内部攻击，未外审 |
| SPARSE-HIGH-ACYCLIC / SPARSE-BALANCED-R | 单交叠；平衡子类另需各自最小 reach 达到最大 reach/r | 任意坏回应环须进低区；平衡子类有 r 上界，是全类证明的前置工具 |
| SPARSE-LONG-CYCLE / SPARSE-BAD-LONG[-ALL] | 单交叠任意长目录；后者分别保留旧区间和全部亚 ρ 版本 | 精确回应核心可任意长；亚 ρ 真坏环不反驳 ρ 上界，固定短核心路线受阻 |

## 按数学成果族阅读

1. 使用已闭合的稀疏阈值：先读 [短目录 ρ](restricted_rho.md)核对下界，再读 [高区传播](sparse_high_reach_barrier.md) 与 [任意长 ρ](sparse_unbounded_rho.md)。原 Q-SPARSE 的阈值已在内部证明意义下闭合，不再列为开放。
2. 攻一般异构上界：先读 [四种子算法](four_seed_algorithm.md)，再审查 [任意交替环](full_catalog_cycle.md)的全环最大客户与统一身份压缩；[六顶点下界](sharp_two_lower.md)独立成立。
3. 选择方法或改费用：先读 [核心提升与单调迁移](core_lift_and_monotone.md)，再看两份长环边界。单共有客户的有限输入精确求解不能替代全类 ρ 证明。

## 全部分支数学正文

| 中文资产名 | 文件 | 数学内容与读取时机 |
| --- | --- | --- |
| [异构目录因子二候选的四种子纯均衡算法](four_seed_algorithm.md) | `four_seed_algorithm.md` | 从局部纯修复连接全目录威胁和离轨选择；一般上界仍按内部候选使用。 |
| [四种子候选算法的任意长度交替回应环论证](full_catalog_cycle.md) | `full_catalog_cycle.md` | 给全环最大原子与统一客户身份压缩的关键不等式，是一般因子二候选的承重步骤。 |
| [异构目录趋近因子二的六顶点整数下界族](sharp_two_lower.md) | `sharp_two_lower.md` | 以严格占优和唯一客户续局计算实例最优倍率；不单独证明普遍因子二上界。 |
| [单交叠且一侧短目录的尖锐 ρ 阈值](restricted_rho.md) | `restricted_rho.md` | 在跨对至多一共有客户且至少一目录至多两个行动时证明纯上界与唯一续局下界。 |
| [任意长单交叠异构目录的尖锐 ρ 阈值](sparse_unbounded_rho.md) | `sparse_unbounded_rho.md` | 以首个高区到低区入口、同一客户身份及三次式闭合全长上界，接短目录下界。 |
| [单交叠坏回应环的低 reach 必经与平衡子类](sparse_high_reach_barrier.md) | `sparse_high_reach_barrier.md` | 给任意环长的高区严格下降和平衡 reach 子类上界，是全类 ρ 证明的前置引理。 |
| [全目录回应核心提升与纯客户费用单调迁移](core_lift_and_monotone.md) | `core_lift_and_monotone.md` | 说明独立续局选择如何保留全目录威胁，并限定纯构造向单调费用迁移的适用域。 |
| [单交叠目录不存在统一短精确回应核心](sparse_long_cycles.md) | `sparse_long_cycles.md` | 显式构造任意长全目录精确威胁闭核心，否定固定大小核心压缩；不反驳 ρ 存在性。 |
| [全部亚 ρ 倍率的真实坏长环与版本边界](sparse_bad_long_cycles.md) | `sparse_bad_long_cycles.md` | 保留旧 3/2<r<ρ 版本及新 1≤r<ρ 版本；真实坏倍率、唯一 NE 与任意长回应环不削弱 ρ 上界。 |

## 来源差异、独立复核与程序

| 来源定位 | 实际差异 | 本说明采用的处理 |
|---|---|---|
| [主稿](../../../history/source/manuscripts/heterogeneous/main.tex) §§2–8；标签 `sec:model`、`sec:repair`、`sec:fourcycle`、`sec:rho` | 主稿将各定理按完成证明书写；现行 ρ 已全分支重写并内部核对，一般因子 2 仍列内部候选 | 分命题查[现行命题](../claims.md)与[五轴状态](../../review_status.json)，均尚无外部评审 |
| [历史任意环稿](../../../history/proofs/heterogeneous/universal_two_prior.md) §1 | 采用所有 singleton 的较大菜单 | 当前四种子须另有全环最大客户、统一 ID 的压缩证明，不能仅改复杂度数字 |
| [下界详稿](../../../history/source/notes/heterogeneous/tight_two_lower.md) §7 | 仍保留“上界尚未闭合前”的时点式条件句 | 视为历史阶段措辞；sharp 2 在当前仍明确依赖上界候选 |
| [稀疏历史稿](../../../history/proofs/heterogeneous/sparse_lower_prior.md) §§9、11 | “尚不知两共有客户能否超过 ρ”和区间 [ρ,2] 已过时 | sharp-2 整数族已反驳；不能作为当前开放问题 |
| [响应核心笔记](../../../history/source/notes/heterogeneous/response_core.md) §§1、2A、2C | 既含依赖共享 φ 的旧充分条件，又含独立异构 2 | 不把旧共享菜单当作四种子定理前提 |
| [最终审计](../../../history/source/audits/heterogeneous_final.md) 开头、§3.7；[攻击审读](../../../history/source/audits/heterogeneous_adversarial.md) §7 | 使用迁移前 `r_menu_solver.py`、`universal_two.md` 等名称；“独立”指同一研究流程内的审读；压缩说明有不同写法 | 当前代码映射至 `facility_spe/heterogeneous_two.py`；正式采用主稿全环最大原子证明；外部独立重构仍待完成 |
| [CLAIMS](https://github.com/SOMEBODYJUN/co-work-anl/blob/bd7798d5bbcc8086217ff54d7f91b445d0374b4f/history/curation-2026-10-01/CLAIMS.md) HC-2 与 CORE-LIFT 项 | 个别证据名称仍写 `r_menu_solver.py`、`meta.md` | 对应现行 [facility_spe/heterogeneous_two.py](../../../facility_spe/heterogeneous_two.py) 与 [history/source/notes/heterogeneous/response_core.md](../../../history/source/notes/heterogeneous/response_core.md)，不凭旧名称新增来源 |

历史上失败的推断也必须区别于现行命题。`response_core.md` §3.1 的 A=1、B=0、共有权重 (2,4) 具有均衡负载差集合 {-1,3}，却无法满足双方各得自身 reach 一半的配额；所以“配额失败必有唯一支配原子”是**错误命题**。两目录均任意大、跨对至多一共有客户的统一 ρ 已由本轮新证明闭合，不能再列为开放边界。


待独立重构的一般候选义务包括四种子调用的菜单归属、严格边界、完整证书规则及核验器。已有有限测试不能证明普遍上界；[规范实现](../../../facility_spe/heterogeneous_two.py)的一次有效证书只证明那个输入达到相应 SPE。

文献优先权须独立核验：主稿已明确早期文献陈述过一般设施数上界，不能把这里的数值二称为首次提出。精确身份见[现行账本](../claims.md)、[五轴状态](../../review_status.json)；[原问题页](../../questions/sparse_catalogs.md)保留原题和闭合后的边界。

---
id: "unrelated-machines/rooted-dag-transit-route-composition-finite-audit"
kind: "computation"
type_tag: "计算"
title: "根DAG守恒扩区与路线拼接有限审计"
status: "retained-finite-evidence"
summary: "保留守恒扩区/非单位分叉搜索与共同容量路线拼接的两份冻结精确审计，明确其有限输入范围、独有计数、实现依赖和不能外推的算法边界。"
legacy_ids:
  - "7434abd5a798786e1550"
  - "384a14e7fa00781e7e4f"
  - "UM-DAG-TRANSIT-CONGESTION-v1"
  - "UM-DAG-NONUNIT-PARAMETER-EXACT-v1"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/rooted_dag_transit_branch_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/rooted_dag_transit_branch_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/route_composition_review_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/route_composition_review_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/rooted_dag_congestion_flow.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/rooted_dag_congestion_flow.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/rooted_dag_congestion_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/rooted_dag_congestion_review.md"
---

# 1. 对象身份、读取范围和真值等级

这是两个冻结 JSON 运行的计算对象。它登记的是代码在明确有限输入上的整数/Fraction 精确结果、依赖哈希和边界字段；JSON 中的 passed 或输出哈希不能替代守恒流、根树或路线拼接的一般证明，也不把历史来源的 claim 名升格成已经解决的主目标。

本轮通过 clean show 完整读取两个源文件及其全部字段，并读取、比较了现有根DAG共同拥塞正文、根DAG冻结审查、既有有向需求桥/共同拥塞三源审查和共同容量路线拼接的审查入口。两个源均来自冻结提交 68fad804ec5946cb296f77dc5b336308a66abf12（legacy-cleanup）与 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c（main），同一路径的字节和 SHA 相同。本对象不重复抄录已有证明；下文只保留这两份审计的独有证据、量词和未实现接口。

对应证据副本：

- [守恒扩区审计 JSON](../../../../tools/evidence/private-tree/rooted-dag-route/rooted_dag_transit_branch_audit.json)，源字节 SHA-256 为 2ae046a87828886205e02ec4cc3f50d89c77eb0bc13bf7936791679b23ac6c77，长度 12,244 字节。
- [路线拼接审查 JSON](../../../../tools/evidence/private-tree/rooted-dag-route/route_composition_review_audit.json)，源字节 SHA-256 为 22a98a20325f0b0db3da9b90bf6488b4d4d529295831e4e6818435137d63bcea，长度 3,871 字节。

算术均为 Python 3.12.14 的整数和 fractions.Fraction 精确运算；没有浮点容差。运行结果是冻结记录，重跑不得覆盖该副本。

# 2. 守恒扩区与非单位分叉搜索

## 2.1 合同与量词

源 7434abd5a798786e1550 把结果标为 UM-DAG-TRANSIT-CONGESTION-v1 和 UM-DAG-NONUNIT-PARAMETER-EXACT-v1。它的数学输入仍是显式有限简单 DAG、指定根、二进制非负需求、整数 K 和支撑 W 上的一份共同边流。新合同把高点和守恒点的分界写成 k_v >= 2K 与 1 <= k_v <= 2K-1；非根输入不超过 K，高点输出至少 k_v，非根低点守恒，低根输出至少 K，零需求点不输出。所有这些条件是同一份共同证书的全称合同，不是每个点各自存在一份流后再拼接。

该源的 proof_sha256 字段为 32bdbb8c6fe3274d2facf4e9193a194c65d70102a8ae00a7429833a039adab73；本字段只作为冻结来源指纹记录。已有根DAG共同拥塞正文的第 7--10 节承担该合同的拆点流、守恒区间扩大、只枚举高点和非单位需求参数算法的数学推导。本计算对象承担对应实现/审计的有限核验，不宣称仅凭 JSON 重建那些全称证明。

## 2.2 规范程序的有限覆盖和独有结果

规范命令记录为：

    python3 tests/audits/unrelated_machines/rooted_dag_transit_branch_search.py > <new scratch result>

输出标题为“可守恒中等需求通道与非单位分叉参数的精确探索”，报告使用整数/Fraction、运行时间 1.282 秒、输出 SHA-256 b61709532d1abfd0bf9c7d99364ea0b693ec13232657385235c4ba7312cc1191。有限计数如下：

| 检查单元 | 计数 | 语义 |
| --- | ---: | --- |
| 全部有序 DAG 案例 | 9,496 | 规范有限图/需求输入上的精确搜索 |
| 枚举父选择 | 63,736 | 对记录的有限结构做的父节点选择枚举 |
| 完整支撑 K 案例 | 28,488 | 预给支撑/拥塞参数的有限候选 |
| 合法完整支撑提取 | 4,179 | 从这些候选中实际通过的根树提取 |
| 随机图样本 | 500 | 伪随机检查，seed=7,102,026 |
| 随机父选择 | 13,938 | 上述随机样本中被实际测试的父选择 |
| 任意根重标号 | 500 | 根标签不固定时的边界检查 |

这些数字不等同于所有 DAG 或所有二进制需求。随机列是有固定种子的附加实验，不是独立于规范程序的概率保证。

冻结 fixtures 保留了以下承重边界：

- 单边尖锐族在根需求 K=1、3、5、9 时分别出现 new_K=1、2、3、5，真实分数及新保证为 1、1/3、1/5、1/9；同一模式还在约 10^100 量级的二进制大需求上运行，输出仍为精确倒数。
- unit_merge 给出 old_K=2、new_K=1、score=1，说明新守恒区间不是旧合同的文字重命名。
- terminal_root_remote_dead_high 的最小 K 是一个约 10^100 的整数，保留根为终端但支撑内仍有远端正需求点的检查；不能在根终端时无条件把支撑搜索的 K 报为 1。
- old_certificate_requires_trimming 明确旧流被拒为新证书且 new_found=true：旧合同中的额外出流需要裁剪，不能把同一条 f 静默重标成新合同。
- huge_nonroot_arbitrary_root 在 h=1 上产生精确分数 2/(...039)，验证非根大需求和任意根编号的有理边界。
- deep_unit_corridor 使用 n=1,502、h=0，score=1，说明深走廊的单位点合同可被实际处理；它不证明深度无界时整体算法为多项式。

这些 fixtures 是实现边界和反例压力测试；它们没有把固定 K 失败转成原模型 NO 证书，也没有把 h 有界的参数算法变成一般多项式算法。

## 2.3 独立 oracle 与锐界信号

独立命令记录为：

    python3 tests/audits/unrelated_machines/rooted_dag_transit_independent.py > <new scratch result>

它不把规范搜索的核心 finder 当成唯一 oracle，报告：

| 检查单元 | 计数 |
| --- | ---: |
| 精确 oracle 案例 | 9,496 |
| 固定支撑案例 | 5,350 |
| 固定支撑可行 | 695 |
| 旧证书到新证书案例 | 504 |
| 免费扩展案例 | 695 |
| 规范输出 SHA | b61709532d1abfd0bf9c7d99364ea0b693ec13232657385235c4ba7312cc1191 |
| 独立输出 SHA | e00600477410af8bec19ea2d7064c23fd19849495ec72346400bf79d88f0be |

单边 sharp 序列从 K=1 到 100 给出 1/(2K-1)，另有两个巨大 K 例分别保持同一精确倒数形式；canonical_new_boundary_fixtures=3，canonical_minimum_crosschecks=1,516，canonical_support_search_crosschecks=1,390。这里的 sharp 只表示已记录证书合同的单边族在这些构造上达到边界，不是一般 DAG 根树问题的不可近似性。

因此本审计支持三条有限结论：规范搜索和独立 oracle 在列定有限输入上同意；旧证书转新证书需要实际重配流；固定支撑/给定 K 的局部接口与已有正文的量词一致。它没有实现从一般 D,k 找到好支撑 W，也没有消除非单位点子集的 2^h 因子。

## 2.4 失败和开放边界

源 JSON 明确写出：这是 finite experiment only；没有全局新颖性主张，没有 h 无界时的多项式算法，也没有 UM-TARGET solution。其独立结果还明确保留 2^h 指数因子、无一般 R||C_max 算法、无全球新颖性或外部审查认证。

复用本对象时，必须先给出合法的共同 W、K 和证书，再使用正文中一次整数流提取的结论。不能把以下任一项当成普遍算法：

1. 9,496 个有限 DAG 案例；
2. 单边 1/(2K-1) 尖锐序列；
3. 固定支撑 5,350 个实例；
4. 随机图 500 个样本；
5. 只枚举高点的 2^h poly(B) 参数程序。

## 3. 共同容量路线拼接的独立审查

## 3.1 审查对象、依赖和接口

源 384a14e7fa00781e7e4f 的标题为“共同容量路线拼接接口的有限独立审查”。它不是新定理陈述，而是对两类拼接实现的有限范围核对。代码 SHA-256 为 636643cd87ca9893cb2ee7e7f2069eac79b2b0b70b039c7083fa4a6ed420ca7c，依赖的冻结代码指纹为：

- tests/audits/unrelated_machines/forest_two_boundary_menu.py：
  8346c844235046a2f0b82fba3ca9de2dbd956615934fcea3a786226f19b37d28
- tests/audits/unrelated_machines/rooted_dag_token_bridge.py：
  825e60011c2777e45d4c71a48b9988c9293bc0346293a7502657748d79fef409

它用 Python 3.12.14、整数/Fraction、seed=null；没有声明外部输入。因而“独立”在这里是代码审查/重算的身份，不是外部同行评审或全球新颖性认证。

## 3.2 菜单、流和有界需求检查

菜单接口实际覆盖 48 个正单任务案例、1,885 个组装实例、14,425 个分配、4 个零目标案例。其合同只检查单任务时两个正端点都被覆盖和组装恒等；它没有推出一般菜单核心近似或任何全局调度保证。

流接口覆盖 1,076 个实例、8,956 个树子集和 1 个根终端案例。所有图是 n<=4 的拓扑标号 DAG；每个非根非汇点需求 1，每个汇点独立选择 terminal/deadend，根需求含 4 个值，含一个 102 位整数。alias examples 对 m=2,...,8 都是 full_ratio=1、frozen_ratio=1/m。它们说明完整支撑比与冻结/固定接口比在该系列可相差 1/m；这是有限别名压力测试，不是全输入下界或新颖性证据。审查使用的指数 oracle 仅用于审计，不能被包装成调度算法。

有界需求接口覆盖 9,176 个实例、87,776 个树子集；非根正需求取 {1,K}，K 取 2、3，汇点另允许 0，根仍有四个需求值；count_backcheck=9,176。该接口核对的是标准最大流推论在小图上的数量一致性，不是一般 scheduling progress，也不把 K=2,3 推广到任意 K。

## 3.3 矩和有限候选的真实范围

moments 部分覆盖所有非空 Boolean support 的维数 0..3 和两种精确权重方案：548 个分布，count_backcheck=548，rank_zero=30，extra_affine_candidates=1,032，fake_psd_rank=2，fake_psd_boolean_candidates=0。固定边界 fixtures：

| numbers | delta | s | feasible |
| --- | --- | ---: | --- |
| [1,1] | 1/3 | 4 | true |
| [1,1] | 1/10 | 11 | true |
| [1,2,3] | 1/3 | 4 | true |
| [1,2,3] | 1/10 | 11 | true |
| [2,2,2] | 1/3 | 4 | false |
| [2,2,2] | 1/10 | 11 | false |
| [1,1,1,3] | 1/3 | 4 | true |
| [1,1,1,3] | 1/10 | 11 | true |

尽管找到 fake PSD rank 2，Boolean 候选数为 0；这只能说明该小范围候选没有满足筛选条件的对象。源明确没有 moment extractor，也没有 truth-promise verifier，所以不能写成存在普遍矩提取算法或可验证的真实性承诺。

## 4. 与既有根DAG对象的关系和去重决定

既有 [共同拥塞双路冻结审计](有向需求树共同拥塞双路冻结审计--计算.md) 已保存旧合同 k>=K、新合同 k>=2K、固定支撑流、1/(2K-1) 解析锐界、2^h 参数算法和激活走廊反例的自足数学正文。本对象不复制这些证明，也不把 JSON 计数当作另一个定理。它的独有内容是：

1. 7434 源把规范搜索与独立 oracle 的两组精确计数、单边大需求 fixtures、旧到新裁流和深走廊边界冻结到同一 SHA；
2. 384a 源把根树流、森林菜单路线和 bounded-demand 两条拼接依赖的代码哈希、有限实例数和 moments false-PSD 边界放在单独的审查接口中；
3. 两源都把失败机制写清：固定支撑/固定 K 的失败不等于一般实例不可行，有限 alias 或 fake PSD 不等于全局障碍，有限 random 样本不等于概率定理。

既有根树流审查仍是一般证明和反例解释的入口；本对象是可追溯的计算/接口证据层。第三阶段若要连边，应将本对象作为“有限检查”证据连接到既有共同拥塞对象，而不能把它连接成“得到一般算法”的推导。

## 5. 可复用接口和未完成义务

后续研究可按以下顺序使用：

1. 给定显式 D,k、支撑 W 和整数 K，先检查共同证书的全量合同，再调用固定支撑流；不得只使用某一局部点的可行流。
2. 若证书提取出真实根树，才可接到既有 token bridge 的树到调度构造；route composition 的菜单/森林接口不改变 token 的身份或需求量词。
3. 如使用非单位参数程序，必须把 2^h（h=点数 k_v>=2）保留在复杂度中，并说明候选阈值由显式边数而非巨大需求值枚举。
4. 如复核 moments 或 fake PSD 结果，应限定在维数 0..3、两种权重方案和列出的 Boolean 支持；任何普遍矩提取/真实性验证仍是开放接口。

未完成义务包括：从一般 unrelated-machines 输入发现共同支撑 W、统一 K 或更好路线；把有限路线拼接提升为可扩展菜单核心近似；为 moments 接口提供真实性承诺的验证器；以及解决 UM-TARGET-v1。没有一个义务由本批的 passed 计数或代码哈希自动完成。

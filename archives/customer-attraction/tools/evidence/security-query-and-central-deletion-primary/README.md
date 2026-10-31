# 两人共同查询、六人原审查与中央优化删除证据

实际EH认领为四源，Boss4、pushed/synced、tip `dcb3ed8215b54897407083772daecb22a37bd235`；[完整原回执](claim-receipt.json)和[逐源指纹/owner](primary-inventory.json)均保全。17439B主原件以本地冻结缓存重新核size、SHA256及Git blob SHA1后复制，没有网络、show、共享Git写入或额外claim/done。此包为本地成熟正文，待Root串行保存，不称已推送。

| ID | 原文件 | 字节 | SHA-256 |
|---|---|---:|---|
| becef1c5468e09354331 | [security README](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/security_global/README.md) | 3283 | 06b733fee57f0eac63f9123e7b1fe727b821629f07858732cfb1be9a6fbf0a70 |
| 61534f23b5e3d32cbef6 | [六人原独立审查](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/security_global/padded_residual_m6_review.md) | 3854 | db3a4a5d8685fd8ca6ff3e50c85e5cf426a0a733ea0546b8a3c8b078eaccc3f7 |
| 171d1eb9926a6dce681d | [两人共同查询](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/security_global/pair_common_query.md) | 3109 | 5ab4cd385b4c9c8d072af7ca0a1a29ee4d3ed674b483c58503c055d80b422e3a |
| 4e1e8aeab1f13c634eca | [中央优化删除](original/research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/security_global/round2/optimizer_deletion_budget.md) | 7193 | 0653ae40ac35305056638487819ab9e0107ddac47be37965af8575669ee0acee |

## 三篇自足数学正文

- [两名剩余玩家共同静态查询预算](../../../state/引理/两名剩余玩家的共同静态查询最小收益预算--引理.md)：所有非负实背景、P1/P2逐客户证明及同一真实回复下的两SPE预算，保剩余利润不是总覆盖。
- [中央后缀安全保留与联合删除预算](../../../state/引理/中央后缀优化的安全保留与联合删除预算--引理.md)：先于查询选固定共同优化器，完整一般k删除税及统一k/(k+1)收入系数、全k单位客户锐族、四真客户非次模及Γ真实后缀差。
- [有限审查与残余模型分流](../../../state/资源/安全查询工作区的有限审查与残余模型分流--资源.md)：九主题旧DAG独审与Root另构造证书分开；一般共享索引族m6有17标签，不能套九标签SPE；全部历史阴性扫描和后来13人分数桥纠正保留。

十篇正式比较全文的快照及原路径/SHA见[context inventory](formal-context/inventory.json)，包括现有CQ-min反例/私块收益下界/Root资源、13人分数桥反例、共同删除势与同叶返还/删除缺陷。快照保持旧链接字节，按其原正式路径解释，不覆盖共享页或另done比较源。

## 缺失原程序与历史证据边界

[主本地缓存清单](primary-local-export-manifest.json)记录587B pair audit、2891B中央验证器、4293B中央报告缺失；[另核padded原件](padded-original-availability.json)记录旧DAG/生成器/5740B审计/1433B报告四项缺失。均未网络fallback或占primary。原入口、原LP/MIP和原DAG运行次数0，未以空目录或异schema输入报告原证书PASS。

原六人review的旧目标SHA555d309…、5440/2437/3003节点、21933比较及14160严格/7773平局只保原有限声明。Root此前已从明文单位输入另写[完整新反例](../../../state/反例/六人共同静态查询最小收益桥的三十客户反例--反例.md)和新DAG；本包复制其[源码/结果/清单指针](reused-root-reconstruction/inventory.json)，核新DAG SHA9c7c751e…，**不重复运行、不把新构造冒原文件重现**。该源清单写实际stdout曾观察但未另存raw；这里不补造event/stdout，不回填旧strict/tie给新result。490137B新DAG已有稳定正式路径，不重复复制。

[scope comparison](scope-and-later-state-comparison.json)保存九标签与17标签的完整身份区别及后续13人算术。共同数值W25/F30/G150/11不意味着同策略、同SPE或同静态安全列；前者v6≤4，后者仅静态背景给≤10/3。本包没有给后者任何完整SPE。

## 一次新标准库静态检查

[完整程序](check_static_query_and_optimizer.py)不导入原求解器/审计，固定有限客户类型并用Fraction计算；没有SPE搜索或检查、优化器或网络。一次新空目录运行，exit0：

| 实际有限域 | 检查数 | 数学作用 |
|---|---:|---|
| 背景0、1/2、1、2、10^40全部P1/P2 membership | 80 / 40 | 核逐客户代数，不替任意实背景解析证明 |
| 固定四客户目录，k0..2/前缀长0..3/全部中央最优器 | 113 | 核共同删除预算(B) |
| 同目录，k0..2/活跃1..3/四纯分布及均匀分布/全部对手前缀 | 225 | 核安全保留(S)，未求安全最优分布 |
| 同目录，全部候选后缀及前缀位置 | 1260 | 核Γ/δ精确恒等式，后缀不冒SPE |
| 充分锐族k1..3与小k2(a12,t5,g3) | 4成员 /117响应多重集 | 核精确中央最优器与达到比，不替全k证明 |
| 一般共享索引族m2..8及20 | 8成员 | 只核W/F/G和合法不观察查询背景 |
| 九标签明文输入静态量及全部至多六主题支持 | 固定一个输入 | v上界、分数余95/11与OPT26，不重跑DAG |

所有完整客户规格/逐行数值/锐族全部响应枚举保存在[208080B结果](new-static-check/result.json)，实际[stdout](new-static-check/stdout.txt)、[stderr](new-static-check/stderr.txt)、[event](new-static-check/event.json)绑定程序SHA和唯一一次执行。普遍结论由正文证明；原main0、LP/MIP0、新SPE核验0。完整执行层级见[boundaries](execution-boundaries.json)。

本次没有新盲审、外审、新颖性或一般half认证。候选/有限实验/解析证明/辅助桥反例分别保留；已done原反例和Root新证书只是比较复用，不重复领/done。

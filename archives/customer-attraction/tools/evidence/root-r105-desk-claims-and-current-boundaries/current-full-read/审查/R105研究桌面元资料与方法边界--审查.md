---
id: "customer-attraction/r105-research-desk-metadata-boundaries"
kind: "review"
type_tag: "审查"
title: "R105 研究桌面元资料与方法边界"
status: "read-only-draft-claim-blocked"
truth_status: "source-specific metadata and method-boundary synthesis; Q-CAG-HALF remains open"
review_level: "full-source-read-from-clean-show; remote claim blocked by approval layer"
summary: "五份 R105 研究桌面元资料分别给出精确 claim 清单、失败接口、一般工作稿、恢复导航和研究状态。它们共同确认 Q-CAG-HALF 的模型与量词不变，保存 DR/ASD/VR、静态排列反例、根可达性必要条件及若干未闭合桥的边界；没有新增一般 half 证明或目标反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/CLAIMS.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/CLAIMS.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/FAILED_ROUTES.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/FAILED_ROUTES.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/GENERAL_WORKING.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/GENERAL_WORKING.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/RESEARCH_STATE.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/RESEARCH_STATE.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/CLAIMS.md"
legacy_ids:
  - "B16-R105-RESEARCH-DESK-METADATA-v1"
evidence_manifest: "../../tools/evidence/R105-meta-20261031/manifest.json"
---

## 读取范围与版本身份

五个文件均通过 `clean show` 导出并完整读取；legacy-cleanup 与 main 的同路径字节按一个冻结源版本计数。`CLAIMS.md` 是对象与量词账本，`FAILED_ROUTES.md` 是接口失败与可回收信息，`GENERAL_WORKING.md` 是父方推导和停止线，`README.md` 是恢复导航，`RESEARCH_STATE.md` 是当前前沿交接。它们是研究桌面元资料，不应被误当作新的 canonical 定理。

本次 clean claim 写端点被自动审核层拒绝（其理由是对未验证 github.com 的网络写入风险），因此本页当前仅为本地 read-only 草稿；正文和证据可 checkpoint 后，五源的正式 `done` 仍需在授权写端点可用时按 receipt 登记。

## 共同模型与主问题

五页共同冻结：有限单位客户、有限非空共同目录、任意玩家人数、六人目标作为特例、每份完整有序历史纯 SPE、空主题/重复/零客户/任意平局均保留。主命题是 `Q-CAG-HALF: 2W>=OPT_m`，状态仍 OPEN。文件明确区分内部证明、内审、外审与新颖性；元资料没有新增外部文献或一般复杂度结论。

## 已承重的可复用组件

- `B16-DELETION-REGRET-ENVELOPE`（DR）对任意背景删除给出原实际节点 regret 的目录敏感包络 `ΣR_j<=ΣK_j-E_d`。依赖原 IC、删除收益差和单调分母；它没有把 `ΣK_j` 变成同一实际利润可支付预算。
- `B16-AVERAGED-SUFFIX-DELETION`（ASD）给出 `ΣR_ij+D/2<=Σ min{u_j,K_ij}` 及 `ΣR_ij<=((m−1)W−D)/2`。该式只控制原实际节点；较早虚拟回放（VR）和离轨叶退款仍需另证，不能直接调用精确 SPE 归纳。
- 静态最优排列桥在三人、1953 客户的精确完整策略中失败：`W=1735`、`OPT=1740`，全部最优支持排列的静态支付至少 1736。该例只否定静态辅助桥，`2W-OPT=1730>0`，不是 half 反例。
- 根可达性 incidence 条件若 `B>I/a` 且 `qB>β+floor(I/α)+r+1`，则某合法前缀不能成为完整根 SPE 的实际前缀。它排除特定同背景/同剩余人数实现，不排除离轨 child 或新编码。

## 失败接口与严谨边界

失败表明确拒绝：把单插入返还池支付全部删除误差；把平均删位误差直接当作精确 SPE 归纳；用驻留终局的一阶矩支付收益；将遗漏 `H` 独立交给 `W`；以及旧 route5a 的算术推论（`W>=(OPT-W)/2` 只给 `3W>=OPT`）。正确门槛可写成 `B>=OPT-W` 的条件桥，但一般成立未证。

对任意完整计划的全历史 regret 稳定性反族有 `B=H_(m-1)-1`、`W=q+2`、`OPT=q+m`，说明无人数无关的 `OPT<=2W+CB` 桥可直接替代精确 SPE 结构；它不是删位 SPE 反例。固定背景零 regret 的 18 客户例中，保留策略投影福利 17，而删后全部精确 SPE 福利 16，说明“实际 regret=0”不足以无损修复；背景不必是原根实际前缀，因此仍不否定主命题。

鲁棒前缀乘积式本身有效，但五人零 regret 时因子仍为 `15625/6049>2`；因子 2 的额外结构仍是开放义务。真实最优菜单账需要共同支付 `ΣQ_i<=W+ΣL_i`，额外槽因果包络和完整菜单安全预算均未闭合。下一步必须在真实分支切换时同时支付主题重选和新叶退款，或绕开删位直接证明 `OPT-W` 的共同付款；局部失败、低人数例、代数等价和多人赞同都不足以改变状态。

## 处置与接续

本页把五份元资料合并为一个资源审查对象，保留所有稳定 ID、冻结指纹、失败路线和下一义务；不新造 theorem/hardness/half 节点。正式入库前应在写端点可用时以本页和 manifest 为目标执行五条 `done` receipt；在此之前，状态为 read-only draft，不能计作远端完成。

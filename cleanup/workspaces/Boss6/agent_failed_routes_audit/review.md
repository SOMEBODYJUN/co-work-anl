---
id: "unrelated-machines/failed-routes-full-audit"
kind: "review"
type_tag: "审查"
title: "不相关并行机失败路线账本的完整读取与回收边界"
status: "full-file-reviewed-retained"
summary: "完整读取冻结 FAILED_ROUTES.md（531行、87517字节），按66个标题分段核对尝试机制、精确失败步骤、排除范围、可回收接口与重试条件；保留为历史方法边界，不把任何单一障碍升级成一般近二不可行性。"
source_refs:
  - "source:68fad804ec5946eb5d7a47d087dd2c62b5aa9974c:research/unrelated_machines/FAILED_ROUTES.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/unrelated_machines/FAILED_ROUTES.md"
  - "source:ee89424fe6a7d5e3f7314f80ada57429efd72a37e104208565212c8ca9cd05ba:research/unrelated_machines/FAILED_ROUTES.md#sha256"
legacy_ids:
  - "UM-FAILED-ROUTES-v1"
---

# 读取范围与版本核对

`clean show cc584ad9d6a5b325af85` 导出的冻结源为 `cleanup/workspaces/Boss6/FAILED_ROUTES.md`，字节数 87,517、行数 531、SHA-256 `ee89424fe6a7d5e3f7314f80ada57429efd72a37e104208565212c8ca9cd05ba`。全文逐行读取，并按标题切成 66 段；每段的起止行、字节数、段 SHA、引用路径和命中稳定 ID 保存在同目录 `reading-log.json`。没有把标题、摘要或旧图当作证明。

文件以一个根入口和 65 个有内容/空内容的专题段落记录历史方法边界。第 453–454 行“消环、次模导入与严格批次的三项边界”只有标题、没有正文；它被保留为编辑痕迹，不能被解释为一个已陈述的失败定理。

# 逐段语义归类

1. **量词、算术与证据边界（行 1–39）。** 随机完备源缺少物理 compiler/低负载 decoder；固定处理时间字母表反而有 gcd/最大值的 `2-g/B` 正面舍入，因此近二反面必须让 `g/B→0`。有限分母、零最优值、不可用边和很小 ε 都不是单独的不可行性证据。配置间隙、有限 Fraction 审计、局部搜索终止和平均表现分别被限定在其实际合同，不能替代全称复杂度归约。
2. **逐边、逐星、逐机局部证书的共同容量缺口（行 40–107）。** GHMR/大边匹配、二阶互补与计数闭包、逐边 LST 探针、全任务多槽匹配、单边完整配置延伸和全部单机配置探针，都能保持安全删除或给出条件证书，但在不同查询之间没有同一任务身份、共享端容量或跨机相关性。稀释 sink、深树、共享 z 与紧凑逃逸族给出精确反例；这些反例只否定列明合同，仍明确保留联合容量、完整 SA/配置层级和相对 OPT 算法的重试口。
3. **槽输出、势函数、循环和微任务后处理（行 108–166）。** 真实最优凸包点配固定槽匹配、循环批量局部最优、固定工作量/凸势、冻结宏任务后重开微任务、给定矩运输和激活边际等尝试分别在输出选择、全程单调性、宏占位和矩保持上失效。文件同时记录可回收的最小迁移、单 sink 宏匹配、重新耦合以及有限树宽补全，不把局部坏点当作一般困难性。
4. **复杂度、条件 witness 与结构限制（行 167–242）。** 独立/共享配置、有限阶矩、固定阈值中任务、整轨标签编译、强配置相容、固定 arity 过滤器、PCSP/MinRep/三维匹配等条目反复区分“给定见证的舍入/条件算法”与“从输入找见证/源 decoder”的额外义务。多条半单位、三半、五三或 13/8 结果均限于明确菜单、树、密度、home 或资格合同；文件明确没有把这些升级为 UM-TARGET-v1 的统一反面。
5. **菜单、仿射线、资源标签和复制 compiler（行 243–374）。** 价格/门控/归一化菜单、XOS minorant、仿射线与笛卡尔张量、标签矩、unit-presence、同型克隆和 component 收费等条目保留真实 state/资格/资源计数。成功的有限域算法、实际三半上界、完整复制坍缩和短 list 地板都和失败的物理 compiler 分开；“增加 states、资源重数、degree、背景或标签独立性”若不保共同容量与 decoder，不能放大为近二 hard image。
6. **高阶矩、条件配置与实际负载（行 375–429）。** 逐段记录强配置相容不等于真实共同二阶 law；raw K2、整行固定阶、全局 M2、SH3 子树流、七态局部核、多 outer tiny-home 的 19/10 限域算法等，均带精确输入域和未覆盖范围。首步可算不等于全程进展；重轻 saddle 需纯自洽条件；固定超载 arity 与拟阵外包数量的边界只限制列明合同。
7. **纠错、阈值编译与最终边界（行 430–531）。** 记录了公屏对“最终支持量是逐批能垒”的实质反驳，撤回旧的多轮外推；保留单任务局部极小结论。pDM 的有限 NO 例只保留 `OPT≥bd+1`，否定未经全局守卫的 gap amplification；空模式 rank、完整同型复制、固定 arity、鲁棒环与两层标签收费都只限定其失败范围。结尾再次声明一般 UM 正反面、任意低载 decoder 和复杂度闭合仍 OPEN。

# 与现有对象的比较和处置

逐段引用的 canonical 链接共 108 个；当前结果分支仍保留同名对象或其中文路径的 40 个，另有 68 个旧 `research/current`/`reviews`/`tests` 路径在本结果树中没有同名落点。这是仓库迁移/路径重写问题，不能据此判定数学来源缺失。现有对象（如 `heavy_matching_residual_and_escape`、`bundle_coupling_subdivision_barrier`、`row_count_escape_gap`、`configuration_preserving_elimination_support_loss`、`pdm_threshold_scheduling_bridge`、`private_graft_and_resource_repetition` 等）与本账本的失败范围一致；本审查保留其原始 source_refs 和局部证明，不复制成重复定理。对于旧链接尚未映射的条目，后续应由第三阶段按稳定对象 ID 补边，不能在此阶段臆造目标文件。

`FAILED_ROUTES.md` 的独有内容是“尝试→失败步骤→排除范围→可回收接口→重试条件”的方法学边界，以及对错误外推的多次纠正。它不承载一条脱离所列合同的普遍不可能定理，也不改变 `UM-TARGET-v1` 仍为 OPEN 的状态。建议源处置为 `retained`，目标为本审查对象，并在总入口资料页中以链接引用；不建议把它标成 `integrated` 后删除历史上下文。

# 复现与后续工作

- 原始字节、源 SHA、66 段索引和 108 条链接已在本工作区保存；没有执行远端 claim/done/push。
- 若第三阶段要建立关系，应把“失败机制”边与对应 canonical 对象、有限证据和纠错审查分开；不能把单条反例边解释成一般 hardness。
- 任何新路线必须同时给出共同容量状态、实际整数输出、可靠 `FAIL` 证书、统一余量、位复杂度和从低载调度到源问题的 decoder；重复固定字母表或局部配置 gap 不增加证据。

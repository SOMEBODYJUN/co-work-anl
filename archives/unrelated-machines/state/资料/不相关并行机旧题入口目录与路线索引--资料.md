---
id: "unrelated-machines/entry-catalog-route-index-review"
kind: "resource"
type_tag: "资料"
title: "不相关并行机旧题入口目录与路线索引：语义清洗审查"
status: "integrated-as-navigation; mathematical-claims-remain-scoped"
summary: "完整读取 research/unrelated_machines/README.md 的 424 行、72,477 字节冻结入口。该源是旧题存档的路线目录与阅读协议，集中列出 UM-TARGET-v1 的精确量词、当前 OPEN 状态、共同容量/整数输出/sound FAIL/位复杂度四项承重义务，并按匹配残余、共同槽、矩/配置、私有复制、菜单与树结构等组织数十个受限对象。它不替代所链接 canonical 正文、审查或证据；本审查将其唯一的导航和范围警告保留为资源对象，不把目录摘要升级为一般算法或困难性证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/unrelated_machines/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/unrelated_machines/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/README.md"
legacy_ids:
  - "UM-READ-MAP-v1"
---

# 不相关并行机旧题入口目录与路线索引：语义清洗审查

## 实际读取与版本关系

冻结源 `46a002184c7580ebe0db` 的路径是 `research/unrelated_machines/README.md`。我用清洗程序从其登记提交取回全文，得到 424 行、72,477 字节；`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的登记内容具有相同源 SHA-256 `3f500dbd1f48aa31778b5fa3e59603b29708d79c0ffb2032fbcb3c6550fd803d`。源首行明确把该入口标为旧题对话使用，当前全仓主攻已经转为 `Q-CAG-HALF`；这是一条路由元数据，不能当作不相关机问题的数学结论。

全文按标题、链接段和正文逐段阅读，未只依据文件名或搜索命中。它包含：旧题的目标与协作入口、长期资产位置、四项承重义务、P0/P1/P2 路线分诊、许多受限接口的短摘要、每条路线的下一缺口，以及“主目标仍 OPEN、有限证据不等于一般结论、内部审查不等于外部新颖性”的反复范围警告。源中关于具体定理的短句都指向 `research/current/unrelated_machines/`、`research/reviews/unrelated_machines/`、`tests/audits/unrelated_machines/` 或 `evidence/runs/unrelated_machines/` 的独立文件；目录本身没有把这些链接内容重新证明一遍。

## 保留的数学身份与量词

入口目录保持 `UM-TARGET-v1` 的一般 unrelated parallel machines makespan 身份：机器数和任务数可随输入增长，处理时间为非负二进制有理数（允许禁用边），任务不可拆分且必须完整分配。目标是寻找一个与机器数、任务数、数值精度和尺寸比无关的统一 `ε>0`，让确定性总位长多项式算法在每个合法输入输出实际整数调度并满足

\[
C_{\max}(A(P))\le (2-\varepsilon)\operatorname{OPT}(P).
\]

源把该命题标为开放，并把“全体主攻否定”写成历史研究方向，而不是已证的不可近似性。任何升级到一般结论都必须另外给出每个固定 `ε` 的真实整数 YES/NO 间隙、低负载完整调度的可靠解码、明确复杂度假设和输入总位长多项式界。配置 LP 的间隙、固定机器数的 `2-1/m`、给定菜单/分组/矩证书的条件舍入和有限枚举均不能替代这些量词。

## 入口目录中真正可复用的四项承重义务

源把不同路线反复归约到四个共同义务；它们是清洗后仍应附在后续对象上的复用说明：

1. **共同容量状态。** 从原始输入本身构造可检验的 big/medium/tiny 或等价联合状态，不能免费调用最优支撑、矩、home/sink 分组或已知共同分解。
2. **完整整数输出。** 同时给出每台机器上的全部任务，并按真实处理时间回算负载；分数解、期望值和存在性证书不算实际调度。
3. **sound `FAIL` 语义。** 若算法报告失败，需要独立可检验证书推出 `OPT>T`；“LP 不可行”或“有限搜索没有找到”本身不够。
4. **统一余量与位复杂度。** 误差参数、阈值搜索、分母、循环次数与输出长度必须按输入总位长控制，不能随机器数、深度、菜单数、重数或尺寸比退化。

这些义务是路线接口的判断标准，不是新的不可能性定理。它们与已存在的资源对象《不相关机研究入口、路线义务与文献状态》相容；本源补充了更完整的路线目录和“何时停止重复局部 probe/slot/repair”的导航规则。

## 路线摘要的正确语义

源的路线矩阵按 P0（任意输入共同容量桥）、P1（受限正面接口、共同迁移/repair、证书/矩/需求树、反向困难性）和 P2（经典共同前提、菜单/Cartesian/局部结构边界）组织。逐条阅读链接后，摘要应按以下层次解释：

- 受限正面接口（例如唯一 home、共同资格、固定汇点、给定矩/配置证书）是条件算法或舍入合同。它们的程序和有限审计可以证明所列输入族，但没有一般结构提取器，也不把 `UM-TARGET-v1` 变成已解。
- 配置、矩、逐边探针、价格、局部 repair、长链、复制和菜单对象多是精确障碍、反例族或有限边界。它们说明某个合同缺少共同相关性、任务身份、真实容量或可靠失败语义；不能合并成“一般近二困难性”。
- 复杂度路线（PCSP、MinRep、Santa、复制等）只有在物理编译、完整任务输出、绝对阈值 decoder 和位复杂度全部闭合时才可升级。源明确保留这些缺口。
- 目录中大量重复出现的 `UM-TARGET-v1` OPEN 标记不是证据计数，也不表示所有局部对象已被独立复核；每个链接仍需回到对应 canonical 正文、审查和证据。

## 与现有结果树的比较及独有去向

我比较了现有 `archives/unrelated-machines/README.md`、`archives/unrelated-machines/问题--问题.md`、`archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md` 以及 `archives/unrelated-machines/state/` 下的具体定理/审查对象。现有资料页已经吸收了模型量词、文献证据层级、四项共同义务与若干主要失败机制；当前 `state/定理` 和 `state/审查` 已分别承接源中许多受限对象。该源没有一条需要另立为一般定理的证明。

仍有独有内容，不能按“重复 README”丢弃：

- 一份按 P0/P1/P2 的路线导航和最短读取顺序，说明先读哪个 canonical 文件、审计和审查，再决定是否停线；
- 对许多摘要的范围护栏，例如“给定证书算法不等于生成器”“固定 `K/q/home/sink` 不等于任意输入”“局部 gap 不等于复杂度 hardness”；
- 旧题与当前 `Q-CAG-HALF` 主攻的路由分离、保存规则和资产位置，帮助后续 mapper 不把两个模型混成一个对象。

这些内容写入本页作为 `resource`，并保留指向实际 canonical 资产的相对链接。它们应作为导航/范围说明关系进入第三阶段图，不能建立 `derives` 边，也不能替代各条数学对象的来源处置。

## 未完成的承重与接续

- 本入口没有提供一般 `UM-TARGET-v1` 算法、一般近二困难性、外部同行评审或全球新颖性认证。
- 目录中提到的许多链接仍需逐源检查是否在当前结果树存在、是否有独立审查、以及审计代码覆盖哪些量词；入口的存在不能视作这些检查已完成。
- 反面路线仍需真实整数 `OPT` gap、全部低负载调度的 sound decoder、明确假设和总位复杂度；不得用固定一族、配置 LP gap 或有限枚举替代。
- 该文档是旧题路线快照，后续若路线、模型或证据状态变化，应修订本页或另建版本，而不应悄改 `UM-TARGET-v1` 身份。

## 处置结论

对源 `46a002184c7580ebe0db` 的语义处置为 **integrated**：保留其导航、路线分诊、范围警告和旧题/当前主攻的身份分离，写入本资源对象；其数学短摘要均回指既有或待逐源清洗的 canonical 对象，不复制为新定理。两个冻结版本同 SHA，不再拆成两条独立数学来源；版本差异已作为比较结果记录。该结论不声称远端已登记 `done`。

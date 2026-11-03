# 2.5 实现复核：已复现的问题与待复测项

本复核只读产品代码，临时 fixture 在独立 Git 测试目录运行，未改共享实现或数学正文。代码处于并发开发中；下述失败绑定于实际运行时源码指纹，不代表最终实现仍未修复。结构测试不认证数学正确性。

## 绑定的初始实现

- `tools/maps.py` SHA-256：`f372a99bbef541815e124a3e909dc4672f11933ee6f3a7370b22f54e65b93ad2`
- `tools/curation.py` SHA-256：`00d1f472bb2a6cfc4e26996112819b0021780689aa087096dcd3ddf8e4d9ffdc`
- 初次结果：`implementation_review_initial.json`
- 临时复现脚本：`review_fixtures.py`

## 已复现的需要修复项

### R1：map scope 符号链接可使 build 写出仓库范围

**失败输入：** 一个合法、已准入的 A 对象；`archives/demo/map` 为指向测试仓库外目录的符号链接，外部已有 `graph.json`，内容为 `UNRELATED DATA`。

**观察：** `maps.build(root,draft=True)` 成功，输出 `projections=2`；外部 graph.json 被覆盖。

**原因：** `scopes` 和 `edge_paths` 检查名义目录形状，但不调用 `curation._safe_path`；最终输出跟随 map 链接。数学对象本身的安全路径检查不能保护图输出位置。

**修复：** 对每个 scope 的 map 目录、edge 文件和输出路径执行同样的仓库范围/符号链接检查；包括根 `map`，以及文件本身是符号链接的情况。拒绝外部读写，且在检查完成前不写任何投影。

### R2：准入检查后再次读取，允许旧声明准入并发修改后的新正文

**失败输入：** manifest 绑定 A 的原 SHA；包装 `curation.check`，让它校验通过返回前后立即把 A 的 summary 改成新数学主张，再让 `maps.read_records(include_edges=False)` 继续。

**观察：** read_records 未拒绝。NodeRecord 的新 SHA 与 manifest 原 SHA 不同，新 summary 进入节点，仍继承已准入状态。

**原因：** maps 先调用 check，再独立读 text 和 bytes；加载时未重新比对 manifest 声明的 SHA，且元数据解析和散列读取不是同一缓冲区。

**修复：** 对每个节点一次 read_bytes，由同一 bytes 解码、解析并算 SHA；加载时核对准入声明 SHA。构建/导出结束前再次检查当前准入和证据版本，或使用不可变 Git 快照；不能将“此前某次检查通过”当作并发写入期间的持续许可。

### R3：未经过 2.5 的任意本地文件可被 accepted 边当作证据

**失败输入：** manifest 仅有数学对象 A，没有任何 evidence 项；在 `notes/workflow.txt` 写 actor/UUID/提交时间，accepted 边把此文件列为 evidence，按 fingerprints 填好哈希。

**观察：** read_records 接受该边。

**原因：** 边的本地证据只要求文件存在和当前 SHA 对应；没有要求它是明确准入的数学对象/证据附件，也没有核附件 owner 与边端点的关系。这允许通过边证据入口绕开已设计的 2.5 角色分离。

**修复：** 本地证据只接受 manifest 已声明的数学/附件路径；附件的数学 owner 应与边的实际作用对象一致，必要跨对象证据需明确范围。固定 `source:<commit>:<path>` 可作为另一路不可变证据绑定，不能由可变工作区文件假冒。

### R4：未解析的原数学文件可只降成不相关对象的附件

**失败输入：** A 没有 frontmatter，但正文有精确平方非负命题和证明；B 是另一个无关数学结论。冻结基线时 A 的 kind 缺失。把 A 作为 B 的 evidence，删除正式 A，给原 A 的 action=attach。

**观察：** `curation.check(final=True)` 无错误，状态 ready-for-stage3，只有 B 进入 admitted。

**原因：** delete 分支对 `kind` 缺失要求误分类更正；attach 分支只检查 PROTECTED_KINDS，漏了未解析/未知类型。这违反“解析失败不应使原数学失去保护”的设计意图。

**修复：** attach 至少同 delete 一样保守：缺失/未知数学身份需要数学替代，或明确的误分类判断，不能直接只作附件。不能以元数据损坏自动推断无独立数学内容。

## 设计选择，需要契约明确而不宜误报为程序真值判断

### B1：未拆 bundle 能 final 准入，并可能显示整页 proved

初始 fixture 的 `dependency_scope=bundle-pending-split` 在 final 检查中通过，并导出 `knowledge_status=proved`。当前逻辑边端点已拒绝 bundle；motivates 等非逻辑关系允许它，这与宽义关系设计一致。

剩余风险是阅读端把一页内不同状态的多个命题看作一个已证结果。建议 bundle 仅作为待拆阅读容器，前台明确“无整页真值”；未完成拆分是否阻止最终数学投影完成应写进契约。不能把 bundle 的任意一个 status 自动分配给全部内部结论。

### B2：未知关系类型可绕过逻辑类别限制

现实现 `kind` 是任意非空字符串，bundle/条件前提限制依赖有限 `LOGICAL_KINDS`。拼写为 `IMPLIES`、新增 `entails` 或中文“推出”，在缺少关系类别登记时可能默认落入非逻辑分支。

建议 accepted 边只使用已登记的逻辑/非逻辑类别；未知 kind 保持 proposed 或明确登记类别。不能依赖作者准确拼写一个列表之外的同义词来维护边界。

### B3：格式化的人工声明不是数学验收

preservation、classification_correction、statement/support/use 都是实质审读声明，程序只能核存在及绑定，不能判其内容真实。“填满字段”仍可能与实际数学无关。前台应保留这一限度，Agent 提示词必须要求按原结论/证明/边界实际对照，不以自动扫描取代数学判断。

## 已看到的有效保护

- 正式对象枚举排除了 evidence、workspaces、history 等副本路径。
- baseline 与固定 Git 提交的完整文件集合、原字节和原 kind/ID 对照，不能通过只改原 kind 绕过数学删除保护。
- 无判定原文保持原字节；局部 final 不能跳过 pending 和未覆盖新增正文。
- 数学与附件分角色，附件不能作普通数学节点；附件 owner 必须是准入数学 ID。
- accepted 关系绑定关系正文、端点和可变证据哈希；固定 source 证据检查冻结 inventory。
- 多前提保留 source_ids，未在构建中拆成各自充分的二元边。
- impact 只返回 `needs-review-not-refuted`，没有给后继节点赋假；替代证明仍可能有效。

## 最终复测记录

修复后已复测 R1–R4：对应失败输入均被正确拒绝，外部 graph.json 未覆盖。final 未拆 bundle 已拒绝；partial 的 bundle 显示 unresolved-bundle，并可仅作非逻辑 motivates 端点。

补测通过：

- 未证前提的默认 unconditional 逻辑边被拒绝；显式 conditional 可保留，端点仍为 conjecture，`asserts_endpoint_truth=False`。
- 未登记的 accepted 关系类型 `IMPLIES` 被拒绝。
- 合取前提 `{A,B}->C` 与备选证明 `D->C`、后继 `C->E` 的 impact 从 A 仅扩展 C/E；不把 B/D 变成后继，不改变 manifest 或给后继赋假。

### R5：第二次构建检查通过，却仍写出第一次检查的旧状态

补测版本：maps SHA `20a33f5d69ee0b9d9bdf4938a37c6a86ce87a6a2420a0ff6c558d48e577310e5`；curation SHA `c2d304b72fde9a11dd66f9f3d9f4ec7a1b5f1b64375f5f397652956a3919fa77`。

**失败输入：** 第一遍 read_records(final=True) 得到准入对象 A 的 status=proved。测试把 cleanup 的来源清点缩为空集合，并在 `curation_target_routes` 阶段将 manifest 中 A 的状态改为 gap、保存新的有效 manifest。最后一遍 read_records 能正常验证新状态。

**观察：** build 成功，当前 manifest 为 gap，输出 graph 的 knowledge_status 却仍为 proved。因为最终检查的返回值被丢弃，真正写出的仍是第一遍节点。这是状态版本混合，不是在判断 A 数学上真或假。

**修复建议：** 初次读取之前固定 manifest/基线、端点和边内容的快照签名；首次读取后、写出前验证签名不变。或在最后完整读取一组一致的 nodes/edges 并真正采用该返回值。只增加一次 check 而不比较两次快照不能解决本例；边文件也要纳入绑定，不能只复核节点。

已通知父代理；初始失败另存 `implementation_review_initial.json` 不覆盖。

### 最终复测：R1–R5 及两项设计缺口均已闭合

实际复测代码：

- maps SHA `56d4f9d85a40d5c08d619303be52f5ef3e60f886999e64216ed29580faddc8dd`
- curation SHA `c2d304b72fde9a11dd66f9f3d9f4ec7a1b5f1b64375f5f397652956a3919fa77`

运行前后两文件 SHA 相同。最新结果为 `implementation_review_fixtures.json`，共11个针对性情景：

- R1–R4 仍正确拒绝，R1 外部文件保持原样。
- R5 在 manifest 改变时拒绝输出，报 `graph inputs changed during build; no projection was written`。输入签名包括 manifest、基线、对象/附件、当前正式候选、关系和来源门槛相关文件；输出携带输入签名，并使用临时文件替换 graph.json。
- 未拆 bundle 的 final 准入拒绝；partial 容器可以通过非逻辑 motivates 保留，不被当成一个已证逻辑端点。
- 未证前提默认拒绝；显式 conditional 保持端点 conjecture，`asserts_endpoint_truth=False`，没有真值提升。
- 未登记关系类型拒绝。
- 合取与替代证明的影响查询只产生复核范围，不改 manifest，不把另一前提或替代证明源误列成后继。

本次未发现上述已测边界仍可通过；这不是对所有输入的安全证明，也不是数学正文语义验收。remaining 人工责任为：核正文和声明是否实际相符、判原数学是否完整保全、核 accepted 关系的论证及适用条件。程序只能保证这些已声明对象、角色、版本与路径约束的一致性。

最终请求的单次复测已完成：在输入指纹新增 cleanup/progress 源完成门后的最终版本上，仅重新运行原11个fixture，未新增审查范围。运行前后代码SHA一致，11项仍全部符合当前契约；原始失败证据保持不变。

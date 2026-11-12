# MMO 三条 pending 关系：独立 3D 数学审查

审查范围为 Boss1 clone `/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1` 中三条具名关系。最后元数据采集时 HEAD 为 `378f8d9198c219dc3379dffe3d40b7459dc86280`，registry 文件 SHA256 为 `2c0f5ca74f80649eee11c1cb84ad5d70091435566a67181fa2133c885f4902bf`。Boss 同期可能继续整合其他包；本报告逐项绑定的四个对象与七份证据以随附 `current-inputs-and-verdicts.json` 为准。

**三条边当前数学均正确，均覆盖完整目标，原有 accepted / unconditional / whole_result 可以保留。它们目前不是可直接当作 current 的绑定资产：三条 read-only edge-check 均以同一 Asahiro 正文的 stale content binding 退出。正式 3A repair 尚待完成，本审查不代替该任务、不清队列和 3D pending。**

| 精确 edge_id | 当前实际结论 | whole 判断 | 必须修复内容 |
|---|---|---|---|
| `um-35169397-parallel-mmo-to-promised-exact-target-search` | 双点平行 MMO 的精确阈值困难族，经两个私有 anchor 的固定负载平移，给出满足实际最大件初态承诺的精确目标生成障碍；全输入总位多项式精确 finder 会使 PARTITION 属于 P | 完整目标；无需降为 contribution 或 proposed | Asahiro 全文 SHA、源对象 pin 与 review 绑定 |
| `um-35169397-parallel-mmo-to-simple-series-parallel-mmo` | 三边路径 `(w_i,B,w_i)` 双向保持共同阈值可行性；简单系列并行 MMO 弱 NP 困难 | 完整目标；无需降为 contribution 或 proposed | Asahiro 全文 SHA、源与目标两对象 pins、review 绑定 |
| `um-35169397-partition-to-multi-outerplanar-mmo` | 正二进制 PARTITION 全输入位多项式多对一归约到正整数多重外平面 MMO；目标弱 NP 困难 | 完整目标；无需降为 contribution 或 proposed | Asahiro 全文 SHA、目标对象 pin 与 review 绑定 |

## 实读范围与证据身份

先读 `AGENTS.md`、`research/IMPLEMENTATION.md` 第三阶段及 `prompts/03-map-worker.md`。独立实读四份当前完整 registry record、三份现有边、原收据、现有正式 repair 定义与当前 integration/coverage 的具名 pending 项。旧收据的枚举数量没有用来承担本次证明。

本次直接读取的正文和冻结源如下。路径均相对于上述 clone。

1. `archives/unrelated-machines/state/资料/Asahiro等--图取向最小最大加权出度--资料.md` 全文；尤其第30–43行模型/调度对应、第70–86行当前安全伪多项式 DP、第90–96行 Theorem 11/12、第104–111行图类和模型边界。当前 SHA256 为 `3fe059248d81113e400a7c5fe3084cccc9eb53267d4c4f1a570e086bc1a06e0f`。
2. `research/registration/evidence/boss6-0104/asahiro-miyano-ono-2011.pdf`，SHA256 `5db93652d80fd92b6440e0a0e22edfdeb09f78e2b886c95cb4adf171c67ee147`。直接提取并阅读 §1.1/1.2、§2.1/2.2 的模型定义，以及印页/PDF页13–15 的 Theorem 11、Fig.4、Theorem 12、Fig.5 和双向证明；13–15页均渲染目视。印页14明确说明 Theorem 11 仅证明 multigraph 情形，Theorem 12 才进入 simple series-parallel，且不能用于 outerplanar。
3. `archives/unrelated-machines/state/文献/Karp归约框架与完全问题--文献.md`，SHA256 `40c532477ca603c4366c545d4c41c39b056725b73e9a165ca1e8b21782792e1d`。实读 §§1、2、4.1–4.3、5.4–5.5 的语言、二进制位长、证书、全串归约延拓、正数处理和 PARTITION 重构。
4. Karp 冻结重印 PDF `archives/unrelated-machines/tools/evidence/Boss7-karp-restored/karp_1972_reprinted_2010_reducibility.pdf`，SHA256 `ae57cf641ae4f1924bdc4d7ef865edb2411c44e3040e8e546d01f1545e288e89`。扫描主体须目视：PDF9/原印89的二进制约定；PDF14/原印94主定理；PDF15/原印95的 KNAPSACK；PDF17/原印97的 PARTITION 精确语言；PDF18–19/原印98–99的 3SAT/着色/精确覆盖构造；PDF20/原印100的 Exact Cover→KNAPSACK 和 KNAPSACK→PARTITION 公式均已渲染阅读。原文的整数字域记号不替代当前正整数合同：当前正文通过无进位 Exact Cover 编码、删除零项和超界常量分支给出正整数版本。没有将 Figure 1 本身当证明。
5. `archives/unrelated-machines/state/障碍/给定目标路径的未知整数搜索--障碍.md` 全文，SHA256 `5382e2f89ff3e70e1e6b5b75f57028312238b0b655be47ec2ef6443d3b4b1d2e`；尤其第20–32行带 anchor 归约/全输入时界、第38–42行路径边界。
6. 障碍的冻结源 `archives/unrelated-machines/tools/evidence/unknown-target/original/research/current/unrelated_machines/unknown_target_partition_search_obstruction.md` 全文，以及对应 `research/reviews/unrelated_machines/held_cycle_unknown_target_obstruction.md`。二者 SHA256 均为 `939dfdca85e22ea0828df222b74d889d8b02f3023a33ecfe60b370bade043aaa`，故只视为同一源的重复副本。当前正文和边比原文更明确地写出了 NO 输入也必须受总多项式时界约束；这是本次正确使用的合同。

## 1. 平行 MMO → 带承诺精确目标搜索

源为 `M-91ba949b418b4026aa3c2dc2e5a62834`，目标为 `UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1`。这里使用的源不是“任意 NP 困难图类”的抽象名称，而是其正文和 frozen Theorem 11 明写的两点独立平行边困难族。

取非空正整数列表，`sum_i w_i=2B`、`w_i<=B`、`B>0`。奇和、非法输入、超大单件和空表均可在调用搜索器前直接决定，因此这一限制没有丢掉 PARTITION 的困难核心。把端点 `s,t` 变成机器，每条权 `w_i` 的边变成两机都可运行且处理时间均 `w_i` 的不可拆残余作业，以边的尾端为所派机器。这与 frozen PDF §1.2 的模型翻译吻合。另添两件处理时间 `B` 的私有 anchor，每件仅在所属机器合格；新实例因此在允许私有件的普通 UM 类内，而不是仍然冒称纯二端点 MMO。

每机固定支付自己的 `B`，令 `T=2B`，则任意完整合格调度的负载为 `(B+d_s^+,B+d_t^+)`。因此存在 `Cmax<=T` 的完整目标当且仅当源两点同时满足 `d_s^+,d_t^+<=B`。平行边总权为 `2B`，故等价于残余精确半分。anchor 合格限制没有可逃逸的机器，反向也没有把部分调度当完整解。

初态所有残余均在机1、anchor各回本机：`S=(3B,B)`。由于全部 `w_i<=B` 且每机真有大小 `B` 的 anchor，**实际已分配最大件**恰为 `M_1=M_2=B`，不是外加松上界。于是 `Cmax=3B<=2T`、`S_1=T+M_1`、`S_2<=T+M_2`，所有有限处理时间也至多 `T`。这些承诺在 YES 和 NO 的整个构造族中均成立。

量词必须保留：存在一个确定性 finder，在所有输入上受同一个输入总位长多项式时界约束，并且在每个满足承诺且有解的输入上输出完整合格 `tau`、`Cmax(tau)<=T`。运行它后检查每件作业恰被分配一次、资格、精确整数负载。YES 一定通过，NO 没有任何能通过的输出；运行和验证均位多项式，故决定 PARTITION。仅在 YES 上会终止而 NO 可无限运行的过程不满足这一推论。现边条件、scope、whole_result 均保了这个区别；“finder ⇒ P=NP”是完整无条件的归约结论，“P≠NP 时不存在该 finder”是它的标准条件推论。

已给目标时，恰有总量 `B` 的残余从机1移到机2，故 `Q=(0,B)`；`U=max(2T,C+T/2)=4B`，于是 `h_i=(S_i+Q_i-U)_+=0`。这只核出构造不攻击给定目标路径的合同；本审查没有以该数值计算代替另一个路径定理的全证明。边本身未把临时路径峰值当成最终近似率，也未生成固定乘性近似 gap。

结论：该 `transfers / accepted / unconditional / whole_result` 完整且正确。无需增添数学前提或收窄 whole_result；正式 repair 仅需使用当前证据 SHA 与源对象 pin 重绑定，并记录本次实际审读。

## 2. 平行 MMO → 简单系列并行 MMO

源仍为 `M-91ba949b418b4026aa3c2dc2e5a62834`，目标为 `M-dcc092193be04e8b9b143a1ed5ba1d4d`。每条源边独立替成 `s-u_i-v_i-t`，权依次为 `(w_i,B,w_i)`，内点不共享。下面的可行性等价对任意正整数 `B` 成立；NP 困难性使用半总和源族。

前向：若源在 `B` 可行，每件 `w_i<=B`；沿源方向将整条路径同向定向。端点支付原来的 `w_i`，内点分别支付 `B` 和 `w_i`，所以所有点均不超过 `B`。若 `w_i>B`，源没有可行方向，新图也因对应外边在任何尾端支付 `w_i>B` 而不可行，没有遗失的边界。

反向：中边若为 `u_i→v_i`，`u_i` 已支付 `B`，严格正权迫使外边为 `s→u_i`；据此把源边选为以 `s` 为尾。中边反向时同理迫使 `t→v_i`，据此把源边选为以 `t` 为尾。每个恢复的源尾端支付都已在新图相应端点真实发生，故恢复后两端出度逐坐标不超过新图出度。新图一条路径可能在两个端点都付外边，但解码只取中边指定的一个端点，因此只会降低载荷，不破坏反向。半总和源族还给出两端都恰为 `B` 的精确证书。

图的简单性、规模和图类均已核：独立内点给 `2n+2` 个点、`3n` 条边，无重边；根袋 `{s,t}` 下每路接 `{s,t,u_i}`，再接 `{t,u_i,v_i}`，覆盖全部边且满足逐点袋连通性，所以树宽至多2，也没有 `K4` minor。位长只涉及拷贝 `w_i,B`。若从 PARTITION 全输入生成该正整数图，奇和/非法输入映常量简单 NO、空表映常量 YES；不把半整数 `B` 当正整数边权。n至少3时取三路并各收缩中边，得到 `K2,3` minor，故不能将该终点升级为简单外平面图。

“弱”标签的算法侧不依赖原 Theorem 10 未付的快速 join 指数。当前正文第82–86行允许显式枚举两子表，固定宽度2下坐标载荷截在 `B`，join 的成对状态费用仍对 `B` 的数值为多项式，因此有伪多项式精确算法。它不是输入二进制位长多项式。这足以保住目标原陈述，没有借第3节已勘误时间界来偷付缺步。

结论：该 `transfers / accepted / unconditional / whole_result` 完整且正确。当前正文第3节的 join 计费澄清和第2节 gate 方向澄清没有侵入上述 Theorem 12 归约；安全伪多项式论证仍在。保留现边数学语义，更新全文 SHA、两端点 pins 和 review 绑定即可。

## 3. PARTITION → 多重外平面 MMO

源为 `M-e8d9614430ab49fc99125452d10388f1`，目标为 `M-91ba949b418b4026aa3c2dc2e5a62834`。源合同是显式正二进制整数的精确等分语言，不是多维、近似、计数或一元数值问题。frozen Karp 原印100页的附加两数确为 `b+1` 和 `A+1-b`。在 `0<=b<=A` 的分支新增数都正，总和 `2A+2`、半和 `A+1`；二附数和 `A+2` 迫使分居两侧，恢复原目标和 `b`。当前正文的越界与零/空常量处理以及无进位编码保留了正二进制 NP 完全源，没有将总和数值误当位复杂度。

归约对每个下标建立独立平行边，重复整数也不能合并。非空偶和取 `A=sum_i w_i=2B`；若子集和为 `B`，其边以 `s` 为尾，其余以 `t` 为尾，则出度都是 `B`。反向每边恰在一个尾端计一次，所以两端出度和始终为 `2B`；若两端都至多 `B`，必都恰为 `B`，`s` 的尾边下标集就是见证。两点及全部平行边可以嵌入同一外部面，故目标是多重外平面图。

奇和/非法编码映“权2单边、阈值1”的固定 NO；合法空表若按 YES 约定则映“权1单边、阈值1”的固定 YES。非空正偶和自动有 `B>0`。某项大于 `B` 时两边都 NO，不需要伪造额外的假设。求和、除二和线性条边的输出均位多项式，故是保持 YES/NO 的全输入多对一归约。

整个多重外平面类的伪多项式侧也成立：底层简单外平面图树宽至多2，将每条平行边单独 introduce；袋内每坐标只记 `0..B` 的整数出度，叶子初始化、引边尝试两方向、忘点检验容量、join逐坐标相加。显式枚举两子表，即便取最保守 `(B+1)^6` 级的固定宽度 join，也仍是伪多项式；超过总边权的阈值可直接 YES。分解构造另付多项式费用。当前正文安全 DP 明确禁止把多重图度数界成 `n-1`，现边也没有作此误用。

结论：该 `implies / accepted / unconditional / whole_result` 完整且正确。它完整证明正整数多重外平面 MMO 弱 NP 困难，不能推出简单外平面、固定最大权、异端点异权或固定乘性近似困难性。

## 当前 pins 与正式 repair 的最小处置

四对象当前完整 record 的 registration pins 已经分别由 `research show` 取得，并按 runtime 的 canonical JSON SHA256 算法从 registry 独立重算一致。

| 对象 | 版本 | 当前 registration_pin |
|---|---:|---|
| `M-91ba949b418b4026aa3c2dc2e5a62834` | 4 | `ae93438090367c13292d23e02b543d73bbd50224a27654b147b135b748408eba` |
| `M-dcc092193be04e8b9b143a1ed5ba1d4d` | 4 | `a23cd4f1b9eecd584c58374f6a346e73d1911536cd5c8dd5c2276cd8d55f7116` |
| `M-e8d9614430ab49fc99125452d10388f1` | 1 | `8235a2ee5b9dcca8eed3e1083fdc0e9d32a10ffc64b264ea13b6c6de967c0ab4` |
| `UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1` | 1 | `ad443406701c850f8875133cc83ffd13a2399a7872bb54368221d8398e58963a` |

三现边共同仍绑定 Asahiro 旧 SHA `58b4be48da7c01dac6a3e5eeff733d7e211dbae675690684e4142742d5bc4740`，源/目标 M91 仍是旧 pin `fd137caa008d902027799278ce88cf69fc35dc0b35350e45472e2e53e08c179d`；简单系列并行终点仍是 `d6e64697e257f820f93b54fbfb90ef9ce179a4e80aad92cf2900f1d859210007`。其余两对象 pins、冻结 Asahiro PDF、Karp 正文、目标障碍正文均仍 current。三边当前字节 SHA 依次为：

- 精确搜索：`cee9226350f59e61e49f157eb8480f30c1db3e07f1db85c355310b7b379d7b35`。
- 简单系列并行：`8b5812e7d5ba76a7e6eef4f8784f51dd3ac5969307b18976ca13ce0e5e2737a9`。
- 多重外平面：`866dd7628061c215d6aa9d59cb932c3e2431307e31d4b7e38014d5130d69b811`。

正式 repair 最小处置是保留三条关系的端点身份、kind、status、ALL、unconditional 和当前数学文字/whole_result；把所有 Asahiro evidence 条目及 evidence_pins 更新到当前 `3fe059...`，相关 endpoint_pins 更新到上表，并在完成实读后更新审读说明、重新生成 review_digest。若按现行任务规范发布替换资产，再在正式收据中逐一处置三份 prior assets，核心 coverage 使用当前 M91 pin，所列新资产 SHA 取最终字节。这里不需要新数学节点、追加非必要前提或将完整结果缩成一步贡献。

**已有正式任务** `boss5-asahiro-sha-current-repair-16bd7e5e49c5be05` 初始观察为 `available`、owner为空，本次未 claim/修改。其定义在观察时也已落后：M91 input_pin 为 `0b25a871b32274036d4a476c7d720976444b6b6bfbdfbb5a8fb47be3793d3db9`，简单系列并行 input_pin 为 `c66cf774f4c8e2fcb93db1d602fee974f13253d7a67956b432c1aa2e45f88fe2`，Asahiro reading_ref 为 `93be27e188d71bd0194088dc7c4a2d96afbaa9513c6f3754900c5b972fd9d6f0`。runtime 第1226行起已有未完成任务原 ID 的 current-pin refresh；由 Boss 用原生 `research map-draft --repair-task` 刷新同一 available 包即可，不需要另造重复3A。正式接续者不能把中间版本当 current；本报告不替其操作队列。观察时 integration 的 pending 列表确列三边及 M91，coverage 对 M91 为 needs-decision。应等待正式 repair 的有效交付后再按准确资产清除对应 pending，而不是把本次外部审查视为已完成3A。

旧资产应按 `research/IMPLEMENTATION.md` 第291行的 supersession 合同逐一标为 **replaced**，不能 retained 原 SHA，因为原字节均有 stale Asahiro 绑定；也不应 retired 数学结论，因为三个归约仍正确。建议新收据对旧任务 `unrelated-machines-3a-3a-35169397311361c0` 给统一理由“当前源SHA及登记版本刷新，原数学语义完整保留”，再以每份旧资产的精确 path/SHA 指向新收据内对应的 replacement_paths：

| 旧 asset basename（原目录 `map/edges/unrelated-machines-3a-3a-35169397311361c0/`） | 旧 SHA256 | 建议替换路径（目录 `map/edges/boss5-asahiro-sha-current-repair-16bd7e5e49c5be05/`） |
|---|---|---|
| `parallel-mmo-to-promised-exact-target-search.json` | `cee9226350f59e61e49f157eb8480f30c1db3e07f1db85c355310b7b379d7b35` | 同 basename，新绑定字节，保原 edge_id |
| `parallel-mmo-to-simple-series-parallel-mmo.json` | `8b5812e7d5ba76a7e6eef4f8784f51dd3ac5969307b18976ca13ce0e5e2737a9` | 同 basename，新绑定字节，保原 edge_id |
| `partition-to-multi-outerplanar-mmo.json` | `866dd7628061c215d6aa9d59cb932c3e2431307e31d4b7e38014d5130d69b811` | 同 basename，新绑定字节，保原 edge_id |

这里的目标路径是供 Boss 采用的最小建议，不表示本次已创建这些正式资产。新收据 assets 列表须以实际最终路径和 SHA 为准，supersession 的 replacement_paths 要与之闭合。

本轮只读取仓库、冻结源并运行三个只读 edge-check，写入均在本仓库外报告目录。未进行 Git 写、claim/done/plan、sync/checkpoint、源/registry/edge 修改，没有重跑成熟科研程序，也没有新建枚举实验。两个图归约另经 fresh 子审查独立核对，所得数学判定与本报告一致。

# BLMRS 正式 repair 的最终窄核采用说明

结论：`boss2-wave4-repair-8a7f75234096249d` 的本范围正式交付可以采用。任务实际为 **done / Boss2**；新边绑定当前 **a3 v3/open**，仍是 **accepted / conditional / contribution（step）**。前轮指出的旧目标 pin 问题已经由正式 supersession 修复，不能继续把它当作当前待修事项。完整算法的数学开放义务则仍然存在，未因本次采用而解除。

本轮只读仓库，没有写 Git、队列、源、registry、edge 或 child；产物仅在 clone 外。复用前轮已实读的冻结算法、外层可达反例和严格槽证明，只完整补读新 task/receipt、新正文和新边，并用文本差分核新正文对旧独有内容的保留。未重读整篇 PDF，未运行科研回放。所审精确 pins、文件 SHA、supersession 逐项结果及最终快照见同目录 `final-repair-bindings.json`。

## 实际交付与当前身份

本轮开始及复验时已见 HEAD/origin 均为 `013e6e5f6574b9ee1afb2f8f2ce3b8a7329f4967`。正式任务有两个核心：

| 对象 | 当前身份 | 当前 registration_pin |
| --- | --- | --- |
| `M-737cbc9ea3b54c03b847026018cf5b19` | v2 / proved，给定分数基的减最大资源值舍入 | `8cf0ef3b2e88c2a2e1253b318c333e212f60184c7482c182cee8e33434f8d758` |
| `M-a3feff9f6a574834925528d0f9d9d658` | v3 / open，完整一般值及两值近似算法目标 | `a75b5c172facac3d19078ee9bcb0d06f3642a8256d5f7aa8196f7553ded5df01` |

新正文 `given-witness-rounding-and-open-search.md` 的 SHA 为 `b1df30e880dd56f19c72466833bd291eb2bb70d7efd3a5b3c5a2189c4c6af654`。新边 `rounding-finishes-given-witness.json` 沿用稳定 ID `blmrs-resource-rounding-finishes-local-search-heavy-light`，实际 SHA 为 `3ebb41af1effd7bd92064cbb826963c2a39d9ca79f115c112a2eba4916cae20f`，与本次指定值一致。

可达反驳的来源与目标也仍为原当前版本：obstruction v1/proved 的 pin 为 `1dfd9f62acfd5f4e77823f41173a567ec5941b5773f59fc305fd81ff7fac6a64`；invariant v1/refuted 的 pin 为 `5f24a8cea92d3a10535d501805e8c58ea5b1f63f5c029f37e506d08a76f3532c`。原正式 refutes 边 SHA 仍为 `de32541d89c5944b98ce238e64aa632ef4ef3005c51c6c68cb7911363028965a`。新正文明确采用其“已从外层单元素合法到达”的结论，不再把可达性写成当前未决。

任务文件中的 embedded receipt 与实际 receipt 完全相同；收据两核心均 linked，均使用当前 pin。新边及保留的舍入等价边都在当前 registry 的 canonical edge_files 中；旧 71b 边已退出该清单。本范围六个 input 对象及新边均不在当前 integration.pending_changes 中。这些定位结果与独立数学判断一致，不是以 pending 已清除替代数学审查。

## 两个给定见证入口的数学核查

一般值入口明列所有见证条件：有限非空玩家集、原资源公共有限非负有理值、归一化单调整数次模秩 oracle；H、L不交并覆盖原项集；重值至少 V/(2α)、轻值小于 V/(2α)，V>0、α≥2。重项给定整数独立向量，W中每人至少得一个重资源单位；U=E\W上给定轻项有理分数独立向量，逐人轻值至少V/α。这个入口不要求W有同样的轻值下界。

“限制U→分数补基→舍入→补原整数基”每一步合法：

1. 对任一轻项j及S⊆U，限制向量满足 x_j(S)≤f_j(S)，所以属于限制 polymatroid 的独立多面体。它可逐坐标增加至限制分数基，坐标不减，且价值非负，因此U的已给值下界保留。
2. 在限制底集U上调用现行严格资源舍入，得到逐项整数基（至少已是整数独立向量），每人值至少 `V/α−max_{j∈L}v_j≥V/(2α)`。这使用有限原资源值；没有把规范 infinity/1 资源送入最大值式。
3. 将每项在U上的整数向量在E\U置零，仍是原 polymatroid 的独立向量：对任意S⊆E，其质量为 z_j(S∩U)≤f_j(S∩U)≤f_j(S)。随后在原底集补成整数基只增坐标，不降U收益。
4. 重项整数独立向量同样可补成各自原整数基，不降W收益。H、L是互斥原项，每项最终只使用一份合法原基，故两侧合并不存在资源重复使用。W原有一个重单位已足以给V/(2α)，因此全体达到同一下界。

U空时直接补基；U非空且L空时给定的正阈值见证不可能存在。新稿保留这些边界。分数/整数补基复用严格证据的逐坐标次模最小化，压缩槽舍入避免展开二进制大重数；本次修订没有加入新的指数展开操作。

两值大阈值入口另给原实例整体有理分数基、每人值至少V及最大项w<V/α。直接舍入给

`V−w>V(1−1/α)≥V/α`，

最后一步恰由α≥2保证。它不需要一般值入口的重轻见证，也不声称支付两值小阈值/中阈值分支。新边明确说“分别处理两个入口，各结论须相应全部见证条件”，没有把一种入口的前提套到另一结论，也没有漏掉其各自的联合条件。

因此源737→目标a3这一局部使用关系完整成立。取α=4+ε/2只说明：若另有有效后端确实构造相应重轻见证，则该最后一步给2α=8+ε的数值界。它没有自行构造见证，也没有支付完整a3算法。新边无whole_result，contribution.remaining及scope均保留这一限制，结构检查也准确识别为step。

## 已证反例和保留辅助推导的边界

本轮没有重跑反例。新稿采用的结论与前轮解析核查一致：首子成功只覆盖一个旧候选，而父成功阈值大于1；下一次仍用整个B0∪B，导致候选与I_M\C相交。直接被否对象是冻结v1 Lemma30(1)的不交输入全称主张。C明显更正和空A保护不能阻断已证外层轨迹。

新稿没有由此否定资源减最大项舍入、逐项补向量等价或所有可能的近似算法。它明确令完整a3仍open，并将合法入口、部分覆盖后的交换秩、失败证书、复杂度、阈值搜索、见证构造和其他两值分支列为未付义务。旧combined-rank证书及递归计数仍只在明列的不交输入、秩、收缩与阻塞收缩假设下使用；不能循环用这些条件句证明冻结执行已满足它们。

## Supersession 是否完整保留旧有效数学

新任务直接 supersedes 71b 与 `boss2-6405-source-repair-2b7402c49967e1c2`；后者原本 supersedes 566d。故这是正确接续实际现役旧done包的替代链，未绕过中间修复。

| 旧资产 | 正式处置 | 本轮核查 |
| --- | --- | --- |
| 71b `rounding-and-search-certificate.md`，SHA `8c46153d…` | replaced→新正文 | 完整差分显示重轻收尾、C更正、空A分支、combined-rank证书全部推导、旧内部反例、条件计数与两值数值桥均保留；新增可达反驳说明，旧“本内部构造不带外层到达证明”改成准确历史归属 |
| 71b `rounding-finishes-heavy-light.json`，SHA `3cae32b6…` | replaced→新同ID边 | 当前a3 v3 pin已更新；两个给定见证入口与局部贡献保留，完整目标仍open |
| 566d `complement-rounding-proof.md` | retained，原SHA `bc6259d4c44a1c234f5c92c091d1aae458d3ed235cc28d38930b8bb43c8b56d6` | 实际字节等于旧资产SHA，并原SHA列入新收据；本轮未将其重新全文核验冒作新增实读 |
| 566d `resource-job-rounding-equivalence.json` | retained，原SHA `f0055ee600e79a9c91e1e5a2cf9c362d94884f8542b222b639a39b673c154991` | 实际字节、现役canonical身份及完整whole边绑定均保持；没有被a3/open改版误删 |

每个旧owner名下的每项prior_asset均有单独处置；所有replacement_paths均实际列在新收据assets里，所有retained均用相同路径及原SHA。两个旧71b文件的历史字节仍原样保全；将旧附证正式replaced并不丢数学，因为新正文保留了全部有效独有内容，且旧文件仍可供既有精确引用定位。

资源/作业给定分数基的补向量等价独立于规范搜索，保留其whole边是正确处置。旧单点上界/私有补偿、原项完整基和2近似边界仍留在原证明资产中，并在新正文、737的coverage和supersession里明确承接。旧a3/e7的数值比较也已改成“若另外支付有效两值算法，再联合桥”的条件陈述，没有把桥当作算法存在性证明。

本轮两次只读edge-check分别通过：新重轻边为 `proof_scope:step`，保留补向量等价边为 `proof_scope:whole`。这解决了前轮实际观察到的旧endpoint_pins拒绝；数学采用依据仍是上述独立范围与推导核查。

可供Boss采用的审查短句：

> 窄核正式done/Boss2的boss2-wave4-repair-8a7f75234096249d及其新正文/新边增量。新边3ebb41af…绑定当前a3 v3/open和737 v2/proved；限制U、补分数基、固定见证舍入、补原整数基均合法，一般值收尾V/(2α)及两值整体基入口V/α分别在所列全部见证条件下成立。现行可达反驳已确立，但不进入这些固定见证舍入前提；完整算法、入口与复杂度仍open。supersession逐项替代71b并原SHA保留566d等价资产，新正文完整保留旧有效辅助数学及其条件边界。当前pins/SHA、收据资产与canonical路径一致，本范围可采用，无需再次定向修复。

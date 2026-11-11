# Boss2：恰六人半覆盖

- RUN：`six-boss2-20261111-cross`
- 分支：`rebuild/research-v2`；存档：`customer-attraction`；子存档：`six-providers`。
- 当前clone：`/workspace/scratch/0ecc5caed424/co-work-anl-boss2`。
- 实际工作文件：`research/workspaces/six-boss2-20261111-cross/`；主笔记`main.md`；输入`spec.json`。
- 事件与证据包：`research/runs/six-boss2-20261111-cross/`。
- 原题仍开放：对任意有限单位客户、有限非空共同标签目录、每份完整有序历史纯SPE，证明`2W >= OPT_6`或给全离轨IC精确反例。
- 首个义务：沿已被两条不同真行排除的5692点，加入已认证同源/容量切面并重优化；推导仍缺的真实跨枝约束及其覆盖预算。

## 恢复

用同Boss/分支/存档/子存档执行start --resume；打开本README及主笔记、各solver笔记和计算产物，再执行`python work.py research resume six-boss2-20261111-cross`。

当前为新RUN：start --resume返回本Boss六人工作区created=true；起始远端fee00e0b8f6ec7509fa178975e24769547aab8e9。仅以checkpoint实际pushed回执判定后续可恢复。

## 当前可接续成果与边界

最新Main整轮笔记为 `research/workspaces/six-boss2-20261111-cross/round4-main-update.md`，已追加进 `main.md`。该页逐项区分已证、有限结论、失败机制和下一问。

1. `master_cuts/`保存5716、5727、5744、5752、5775、5783六轮精确原始/对偶证书。最新5783准确最优W约0.4926332627883867，点SHA `525139e949098e14426d483a334b7ad7acb454ff692f76ee19769dd305c227df`；Main全行/列复核PASS。全部仅限固定16hist/4849列必要图，不是SPE或一般半覆盖下界。
2. 5752早期对偶恢复问题已准确解决；原点字节未改，全部146正乘子与4849列通过。不要把早期失败记录误读为现状态未闭合。
3. 新严格层级 P616⊊P332⊊交P76 有两份独立有理见证；共享真实V的独立初段/折扣尾合同、任意尾长平衡权统一正价已证明。新增对象ID分别为 `M-b1b4276f0ec747ed8c347bda65c9e0af`、`M-63c882b0c8414805a43d4d8d4e43f4e3`、`M-043045ec129b4a5f82a3368b324accf9`。有限计算对象 `M-ddceaa3d53064498b3e833a32e1f3b6f` 升version2至5783。正式路径/哈希在 `formal-round4-identities.json`，登记和边审回执在 `formal-round4-integration-receipt.json`。
4. 删12条beta非零行而保留所有同期普通更新的5763系统有准确可行点，证明这12条具体正尾合同对有限目标有严格增益；不扩大成整个旧无限锥的严格分离。
5. 5783当前仍被3条现有616再权行排除；Main `main_verify_cross_pairs_5783_three.json` PASS，包 `joint_requery/cross_pairs_selected_5783_three_compact_v1.json`。下一5786矩阵将在本轮checkpoint后生成，未预称最优。
6. 三代理保持Boss2身份：master_cuts正复审Boss1新增H/M/Y与跨e/f ZZ行的具体代入；joint保当前616缺步与对称差R相关性；coverage推K=0承重行的解析覆盖桥。对应实际路径/反馈见最新Main笔记及RUN。

本次checkpoint前最后确认pushed的远端提交为 `6b918bd36ee3b87a435a84d0475629f1aacf6691`，回执 `checkpoint-third-confirmed.json`。本轮新结果完成后，以最新checkpoint的 `pushed` 与 `pushed_head` 为恢复上限。工作区未标已确认回执的更新须先检查Git；不要将本地草稿当作远端已保存。

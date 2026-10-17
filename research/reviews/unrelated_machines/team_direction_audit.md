# UM-TARGET-v1：阶段方向与工作模式审计

审计基线：`origin/main=ede1392dd5ea07457f188865a5f72fe8eb194409`，审计日期 2026-10-17。审计只判断当前研究状态和路线效率，不把 Git 提交、文件数量或有限计算升级为数学真值。

## 结论

**数学方向没有完全跑偏，但搜索过程确实局部化。** 已有路线都仍指向 `UM-TARGET-v1`：它们把配置值、逐机探针、固定槽、单目的地 repair、给定矩/支撑和受限 home/sink 接口逐一收窄，并共同把未解问题压缩成全输入桥。因而这些反例和边界有诊断价值。

局部化出现在研究动作层：多轮重复固定 `K/q/home/sink`、独立 probe、逐坐标修复和大规模枚举；这些动作大多没有减少“任意 `P,T` 生成共同容量状态并一次性输出全机整数调度，或给出 sound `FAIL => OPT>T`”这一承重义务。有限审计可以核对公式和最小反例，不能替代全称证明。`seq339` 的 threshold-cover 恢复漏洞和 `seq348` 的 C2 条件负载抵消错误说明，公式测试曾早于语义/全机承重检查。

所以当前准确表述是：**反例、结构边界和受限正面接口正在有序收敛；一般统一低于 2 的证明桥仍尚未真正闭合。** 不能说已经接近完成，也不能说此前工作全部无效。

## 证据与范围

- `research/unrelated_machines/CLAIMS.md:5-14`、`research/unrelated_machines/RESEARCH_STATE.md:1-9` 明确 `UM-TARGET-v1` 仍 `OPEN`，没有一般确定性位多项式 `(2-epsilon)` 算法。
- 当前共同承重义务见 `research/unrelated_machines/RESEARCH_STATE.md` 的路线矩阵和“全输入桥”段：共同容量的可计算提取、所有机器的实际整数输出、统一不退化 `epsilon`、可靠失败语义以及总位复杂度。
- 当前结构检查结果是 1051 个目录资产、195 个 scoped entries、747 个关系节点、874 条超边；这些只证明登记结构可追踪。`assets.json` 中与本题有关的 package 约 84 个，绝大多数是受限范围的 complete proof/obstruction/interface，只有少数仍是 candidate。规模本身不是数学进展。
- 正向红队复核表明，threshold-cover、weighted/heterogeneous macro、common-size reopen 和给定矩/支撑路线都要求额外结构或给定证书；没有一条覆盖任意输入的共同状态、实际全机输出、sound FAIL 和位多项式四项合同。
- 反向红队复核表明，D_K/3DM、共享标签、bundle collision、dual-rail 和 unit-readout 目前都只关闭局部 soundness 接口；仍缺对每个固定 `delta>0` 的真实整数 YES/NO gap、任意低调度 decoder 以及位多项式归约。

## 状态分层与地图问题

当前 canonical 只指 `research/current/unrelated_machines/` 中有稳定账本入口、对应 review/evidence 的正文；`research/questions/unrelated_machines/` 是候选和未闭义务；`research/workspaces/` 是协作桌面。HEAD、push、内部审查和有限代码都不会单独升级 Truth。

最新 `UM-HEAVY-LIGHT-JOINT-RESIDUAL-MINMAX-v1`（`research/questions/unrelated_machines/heavy_light_joint_residual_minmax_obstruction.md`）的 Farkas/min–max 两机例是 **candidate obstruction**：它只说明“逐个对偶向量选 heavy 放置”不能交换为“同一放置满足所有对偶向量”，尚无独立审查，也不是一般算法不可能性。它暂不进入 `current`、`graph` 或 `review_status`，地图应明确这一点；只有完成 statement-first 独立攻击并确定其可回收范围后才考虑提升。

## 下一轮工作模式

保留自主并行和直接攻证明，不再增加审批层。角色按数学职责分开：

1. 每条主线一个 Builder/证明者，只绑定一个承重义务（共同状态、全机整数输出、sound FAIL、统一余量或位复杂度之一）。
2. 一个独立 Blind Red-team 先只读精确 Claim 和承重义务，先构造最小退化/反例，再读证明；不按投票升级。
3. 位复杂度、oracle、分母增长、终止和输出合法性作为每轮强制字段；只有候选跨过主线时才临时指定专门审计者。
4. Root 只在出现真实引理、归约、参数化障碍或审计纠错时更新地图、账本和 checkpoint，不设常驻协调员或秘书。

每轮交付固定为一页：

```text
Claim ID/version；route=F/R/B
唯一承重义务 O
本轮新引理/构造/反例（关键不等式或 decoder）
独立攻击与仍存 fatal objection
总位复杂度、输出与 FAIL 语义
状态：closes / partial / blocked / salvage / retire
文件入口与下一条最有信息量的动作
```

探索阶段不要求把每条想法先包装成表格；只有进入长期资产、跨路线合并或 checkpoint 时整理 Claim Card。若连续两轮只增加样本、换参数或重复同一局部机制，却没有关闭承重义务，就做 honest salvage 并换线。建议保留四条活动主线：全输入共同容量正向、真实整数近二反向、障碍综合、非 LP 的全局交换/势方法；每条都必须对照同一个全输入桥。

## 下一条高信息动作

正向只保留一个候选：构造任意 `P,T` 的带任务身份联合容量状态，其失败能给整数不可行证书；先把“行内大小跨度任意但支持受限/树宽受限”的状态→实际输出→sound FAIL 闭环作为校准，再证明如何从一般矩阵生成该状态。常数树宽上的 R∥Cmax FPTAS 已在 Jansen–Maack–Solis-Oba 的来源中登记，因此这一步是复现/校准，不登记为新算法。反向只保留一个候选：固定 `delta` 的 robust all-level matching，要求同时压低所有 `t=1,...,K` 束匹配层并给任意低调度 decoder；若不能得到跨层一致性和位多项式规模，立即记录为复杂度缺口而非继续扩展样本。

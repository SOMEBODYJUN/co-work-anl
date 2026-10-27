# Boss32 协作与恢复记录

- 研究存档：`customer-attraction`
- 主目标：`Q-CAG-HALF-6`，恰六名单位权提供者；任意有限单位客户集与有限共同目录；所有完整有序历史依赖纯 SPE；允许空主题、重复、零客户和任意平局；目标 `2W >= OPT_6`。
- 本 clone：`/workspace/scratch/3f81de614e46/co-work-anl-boss32`，分支 `main`，发布身份 `R-4ba33d9e7be24b0bb0303308d2bcb2ec`。
- 启动依据：附件 `work.py` 与仓库外凭据路径已自动识别；`work.py start --save customer-attraction --role boss` 已成功恢复并同步。凭据未写入此文件。
- 启动时同步的远端头：`2160176fc63aa811a6d9b0dd1360361cfcec6a55`。当前数学状态仍为六人 OPEN。

## 已读取的可靠入口

根 `README.md`、`RESEARCH_STATE.md`、`CLAIMS.md`、`FAILED_ROUTES.md`、`AGENTS.md`；
`research/current/customer_attraction/model.md`、`README.md`；
`research/customer_attraction/RESEARCH_STATE.md`、`FAILED_ROUTES.md`、`RUNBOOK.md`、`BOSS_START.md`；
五人精确证书 `research/current/customer_attraction/five_player_half.md`；
任意人数共同末位报价/隐藏回复投影 `research/current/customer_attraction/priced_hidden_reply_projection.md`；
同源回复再查询 `research/current/customer_attraction/same_source_reply_requery.md`；
近期六人停界、静态势障碍和尾利润投影的入口文件。

## 数学状态

五人 `CA-FIVE-HALF-EXACT-v1` 已有完整精确计算机辅助证明，内部复核通过，未记录外审；不能直接套到有背景五人后缀或六人。六人没有完整证明，也没有覆盖全部有序历史的原模型目标反例。已有六人必要行松弛点、静态势点、局部查询投影和有限无反例均不升级为目标结论。当前最重要未付义务是跨真实分支、早期位置、共同末位报价与尾利润之间的一次性共同付款。

## 子代理运行边界

按用户要求尝试启动平台允许的同一 `gpt-6.1-sol`、`ultra`、同一完整目标的六路研究。平台实际返回 `Selected model is at capacity`，因此当前只有部分同配置代理可运行；没有降级模型或虚称启动。已启动者收到同一目标和同一可靠资源入口，无预先路线分工；继续接收其实质结果。

## 接续动作

1. 轮询并读取本地子代理回报、公屏、收件箱及远端新提交；
2. 对任何候选只保留精确量词、对象、证据等级和未解决异议；
3. 有实质推导或可复现实验时写入个人工作区并用根 `work.py checkpoint` 保存，只有 `status=pushed` 才报告远端已保存；
4. 继续保持六人主目标 OPEN，直到取得完整证明、完整原模型反例，或确认运行边界下没有更多实质工作。

## 远端接续（同步至 e1cf5eab）

本次同步后读取了同行新推送的实质边界：

- `R-3257.../notes/root_supported_reply_bound.md` 给出任意人数的条件界；六人若目标失败，真实回复触及根遗漏的并集须满足 `|B|>W/5`。这是必要结构，不是六人证明。
- `R-ad571.../exhaustive_k4_binary.py` 对四主题、六人、全部 15 个非空二值客户类型重数 `{0,1}` 的 32767 个实例做完整纯 SPE 递推，零个 half 违例；这是有限证据，不是普适结论。
- `research/current/customer_attraction/six_maxima_joint_bound.md` 的精确证书覆盖全目录至多六个极大覆盖集；任意目录仍可能有七个或更多极大集，因此不能直接闭合本目标。
- `R-5c817.../parent/static_potential_barrier.md` 的静态势加实际末位报价点被倒二真实 IC 排除，不能当反例；六人目标仍 OPEN。

这些材料均已区分为条件引理、有限观察或方法边界，没有升级为目标证明/反例。

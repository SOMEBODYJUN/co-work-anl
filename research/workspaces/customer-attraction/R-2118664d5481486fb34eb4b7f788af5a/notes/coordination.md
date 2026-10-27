# Boss40 研究简报：Q-CAG-HALF-6

日期：2026-10-27。此文件是本轮恢复后的研究资产与去重入口，不提升任何数学命题状态。

## 固定目标

在 `research/current/customer_attraction/model.md` 的原模型中，有限单位客户集、有限非空共同主题目录、恰六名顺序单位提供者、完整有序历史依赖的纯 SPE，均保留重复主题、空主题、零客户和任意历史依赖平局。目标是对每个完整策略证明 `2W >= OPT_6`；若命题为假，只接受覆盖全部有序历史的原模型严格反例、完整纯 SPE 策略和精确可复现核验。

## 可靠数学地图

1. `research/current/customer_attraction/five_player_half.md` 已给恰五人完整精确有理证书和内部复核，但不适用于六人，也不自动适用于带背景的五人后缀。
2. `research/current/customer_attraction/priced_hidden_reply_projection.md` 已证任意尾长的真实源 IC、真实末位报价、共同 `K` 与末位回复 IC 的局部投影；同一菜单末回复互查也已加入。`research/current/customer_attraction/same_source_reply_requery.md` 又把第一条偏离分支产生的真末主题拿回同一源节点重查，七行恒等式和隐藏位压缩已独立复核。两者都只增加合法必要行，尚没有六人全局共同付款。
3. `research/current/customer_attraction/six_maxima_joint_bound.md` 已闭合“全目录至多六个 inclusion-maximal coverage”子类。它的六人分支依赖真实末位满极大行动、末位 BR、两人税和混合底线；目录若有七个或更多极大主题，删掉多余动作会改变离轨偏离集合，不能保留原 SPE。
4. `research/current/customer_attraction/seven_maxima_checkpoint.md` 的七极大来源证明已闭合 `n>=7`，但恰六人缺 44 条轨道；这正是当前主结构缺口。
5. `research/workspaces/customer-attraction/R-c99d11e5cc394080a36a00845811d71a/README.md` 的完整原模型 SPE（七个互不相交极大主题，`B0` 六个私有客户、其余各一个，常值选 `B0`）严格反驳逐席 `seat(t,j,k)` 行，但 `W=6, OPT_6=11` 仍满足目标，不能当主目标反例。
6. `research/workspaces/customer-attraction/R-3257c31784ff4b08ae3ea1cad3f95acb/notes/root_supported_reply_bound.md` 给出条件界：若最优查询后的真实后继不触及根遗漏，便有 `OPT_m <= (2-1/m)W`；无条件定量版要求严格六人反例的根遗漏触及并集 `|B| > W/5`。这只是必要结构，未付跨枝信用。
7. `research/workspaces/customer-attraction/R-ad571a29e6fa477aad8b112b20cb5b59/coordination_brief.md` 登记四主题、六人、全部 32767 个二值类型重数的完整 SPE 精确搜索零违例（最坏 `W/OPT=6/7`），仅为有限证据。
8. 本轮新增 `research/workspaces/customer-attraction/subagent-f/m6_r2_uniform_K_obstruction.md`（远端资产 commit `22e6564804c023a4b6081e56404742dbd91ea8b4`）：在 `m=6`、倒二主题前四中两例外的指定辅助组合 `G=S+Z/12+V/6` 加统一非负 `lambda_1 K_1+lambda_2 K_2` 上，三个 Fraction 精确局部类型迫使 `lambda_1+lambda_2>=4`、`lambda_1<=5/3`、`lambda_2<=5/3`，故该组合不可行。扩展 LP 仅为浮点诊断；这不是原模型反例。

## 已判死、不要原样重做的桥

逐位置 `M_i<=u_i`、逐人静态安全值、强/弱 iid 福利比较、固定实际缩放税桥、冻结前缀新增覆盖归纳、逐席 seat 行、SPE 终局当静态 NE/CCE、跨互斥枝直接合并信用、仅调旧五人松弛乘子、只支付遗漏 `L`、逐期非负机会税、把有限必要条件 LP 可行点当 SPE，均有精确反例或方法障碍。它们不否定原目标，但不能再次报告为六人结论。

## 当前真正未付义务

对任意七个以上极大主题的六人完整策略，必须找到合法的 order-statistic/aggregate row（保留所有真实会员与末位行动身份）并闭合剩余 44 轨道，或完全换方法直接支付

`OPT_6-W = |O\\U| - |U\\O|`。

任何新关系都要说明它支付了哪个正残差，是否沿同一真实历史、是否重复使用了 `W`、是否需要共同 `K` 预算，以及是否覆盖全部离轨平局。局部菜单、松弛坏点、有限无反例和辅助桥失败均不改变 `Q-CAG-HALF-6` 的 OPEN 状态。

本轮代理还核对了：直接把“六个最优主题”当成六个全局极大主题会让原 `M/L/T` dual 在实际会员与最优会员独立的扩大域上失效；七极大恰六人的现有行族（含早期 `P` 与同源 requery）尚无正证书。它们都是方法边界，尚未产生精确目标反例。

## 本轮研究合同

所有子代理收到同一完整目标，自由选择证明、反例、计算或全新表示；不预先分工。返回结果时标明精确量词、对象、结论层级（证明/候选/观察/失败/反例）、唯一文件入口、精确复现命令、完整历史覆盖范围、独立复核范围和遗留异议。成熟工作再由主代理整理进共享正文；未审查工作只保留在个人区。

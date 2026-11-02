# Boss coordination brief — Q-CAG-HALF-6

更新时间：2026-10-27；发布身份 `R-a76c0a0600614bfbb73c784d28202256`。

## Exact target

固定六名单位权提供者，有限客户集 `N`，有限非空共同目录 `S⊆2^N`。提供者按固定顺序观察全部有序历史选主题，允许重复、空主题、零客户和任意历史依赖平局。客户价值在最终覆盖自己的提供者之间均分；`W` 是终局被覆盖客户数，`OPT_6` 是六个目录主题的最大并集大小。目标是对每个完整历史依赖纯 SPE 证明 `2W≥OPT_6`。若命题为假，只接受原模型覆盖全部有序历史的完整纯 SPE 策略和精确可复现 `2W<OPT_6`。

## 已核对的可靠入口

- `research/current/customer_attraction/model.md`：完整模型、SPE 量词、计数压缩边界。
- `research/customer_attraction/RESEARCH_STATE.md`：当前前沿、已证关系和真正缺口。
- `research/customer_attraction/FAILED_ROUTES.md`：逐席/逐人/静态势/固定前缀/税桥等已失败范围。
- `research/current/customer_attraction/five_player_half.md`：恰五人完整精确证书；不外推六人。
- `research/current/customer_attraction/six_maxima_joint_bound.md`：至多六个包含极大覆盖集的任意人数半覆盖；证明依赖完整极大集路由。
- `research/current/customer_attraction/seven_maxima_checkpoint.md`：恰七极大在 `n≥7` 已证，但 `n=6` 缺 44 个轨道。
- `research/current/customer_attraction/priced_hidden_reply_projection.md`、`same_source_reply_requery.md`：真实末位/同源再查询局部非负投影，尚未闭合全局跨枝付款。
- 近期公屏消息 384–397：条件根回复界、四主题 32767 个有限全历史搜索、七极大六人逐席 seat 行反例和合法 aggregate 缺口。

## 去重后的数学边界

1. 不能把静态势加末位报价、逐席 `seat(t,j,k)`、逐位置 `M_i≤u_i`、逐人安全值、SPE→静态 NE、固定前缀 `P+λΔ`、逐期税、有限无反例或松弛 LP 点当作目标结果。
2. 七极大六人逐席行确实不是 SPE 必然式：七个互不相交极大主题，`B_0` 有 6 个私有客户、其余各有 1 个，所有历史常值选 `B_0` 是完整 SPE，`W=6, OPT_6=11`，但仍满足目标；该例只反驳辅助 seat 行。
3. 六人真正未付的是跨早期、倒二、末位互斥分支的共同净预算。固定最优并集 `O`、实际并集 `U` 时应支付 `OPT_6-W=|O\\U|-|U\\O|`，不能只付遗漏。
4. 目标六人任意目录可取六个最优极大容器 `O_1,…,O_6` 加实际末位所选的极大容器 `B_0`，最多七个极大集。若 `B_0` 属于六个容器，可调用六极大定理；真正缺口是 `B_0` 不在 `O` 时的七极大六人情形。直接删去一个极大集再套六极大定理不合法，因为删目录改变离轨动作集合、容器路由和 SPE 续局。

## 代理工作要求

所有代理拥有同一完整目标，自由选证明、反例、精确计算或独立审查路线。优先寻找：

- 七极大六人 44 缺失轨道的合法 aggregate/order-statistic 关系；
- 六个最优集与末位 `B_0` 不同的跨枝共同付款，明确补偿 `|O\\U|` 与 `|U\\O|`；
- 完整原模型全历史策略反例。

任何新文件必须说明 Exact Statement、量词、适用范围、证据等级和未解决义务；实质工作按根 `work.py checkpoint` 保存，只有 `status=pushed` 才算远端保存。局部坏点、必要条件、有限阴性和非法 LP 只记录为相应边界，不升级为六人结论。

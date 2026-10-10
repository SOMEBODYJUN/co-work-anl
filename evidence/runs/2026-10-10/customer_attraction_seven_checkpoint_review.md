# 七极大主题 checkpoint：独立审查与精确完成范围

2026-10-10。仅审查已有成果，未进行新的 LP/博弈泛搜，未改仓库登记、原报告、证书或提交。

**结论：恰七极大、n≥7 的 `U≤2W` 证明通过独立数学与精确算术审查。任意 n 的七极大半覆盖定理尚不能由现有资产直接宣布完成；仅剩 n=5、6 的全轨道证书覆盖缺口，分别为 16 与 44 个轨道。** 已有覆盖部分全部精确重放通过，没有发现错误证书。

## 1. 可确认的七极大 n≥7 定理

审查对象是 `general_joint_analytic/seven_maxima_seven_plus.md`，内容哈希
`b186dfbc3a245c62af59e8165279dd3d8fbab4f3e3ea31f9079573568bea645e`。
报告的 `independent review pending` 尚未由作者改写；本文件提供该版本的独立审查结果。

| 范围 | 独立核验 | 结果 |
|---|---|---|
| n=7 | 全部 8,128 个 literal incidence/true-membership 列 | 最小余项 `344541/320450000` |
| n=8 | 全部 16,256 个 literal 列 | 最小余项 `15483/775000` |
| n=9 | 全部 208 个压缩列 | `13083575/3480880788` |
| n=10 | 全部 234 个压缩列 | `288689/22822800` |
| n=11 | 全部 260 个压缩列 | `17649416027/867723576720` |
| n=12 | 全部 286 个压缩列 | `866272417771/32017930648704` |
| 所有 n≥13 | floor 解析下界、完整 case 分解、凹二次式端点 | 非负余项普遍成立 |

独立程序 `independent_seven_plus.py` 不导入作者审计、LP、模型程序或发现代码。
它重建原始均分收益和三种 slack 家族，并独立重放 24,384 个 literal 列、988 个压缩列。
输出见 `independent_seven_plus.json`。有限代数点用于检验清分母后至多二次多项式的恒等式；n≥13 的普遍结论来自下述解析符号论证，不由有限 n 扫描外推。

### 数学审查要点

1. **末位满极大。** 给定实际前缀，合法严格超集保留全部原客户支付，并给新增客户严格正支付；末位没有后继反应，因此最后行动必为整个合法极大覆盖。较早的真实行动不作此假定。
2. **mixed floor 的完整历史合法性。** 当前完整极大偏离没有同路由后继时，用 prefix route counts 作负载上界和带权平均；存在同路由后继时，完整极大偏离包含该后继的真实子主题，故在同一个偏离终局的收益支配后继。后继由原策略在该实际偏离历史的 SPE 给出。两个 suffix envelope 单调，能同时传递 private/shared 保底，无冻结回复步骤。
3. **真实两剩余 tax。** 仅使用已登记的恰两剩余定理；实际前缀背景是 true load p，tax 的 d 也是倒数第二位真实会员。完整策略的实际离轨回复使 slack 合法。这里不调用已被否定的根总税或一般人数税桥。
4. **同一个客户账本。** 早期 mixed aggregate、六个末位 BR、六个 `T_0j` 和十五个内部不同 tax pair 的逐客户和，精确给出式(11)。`q=6c_*+15e=12/19=6b`；真实 core 的 aggregate floor 为 `(n−2)/n`，允许较早子主题遗漏 core。
5. **n≥13 floor。** 私有原系数下界的完成平方正确：`5(t−(n−1)/2)^2+(3n²−18n−5)/4≥0`，所以 `F_P≥(n−2)/(2n)`。共享递减和大于积分，n≥13 时 log 参数至少 `7/3`，而正级数给 `log(7/3)>316/375>5/6`，所以 `F_V>1/3`。
6. **所有余项 case。** private 四种 covered case 和 uncovered case 正确，统一下界在 n=7 为 `1/1064`，随后递增。shared/core 的 f,d 四种 case 完整；非负内部 pair 可丢弃；`C_1` 和 `E` 为凹二次式，在 k∈[1,6] 的端点均严格正。
7. **67/532 更正。** uncovered shared 的较粗下界确为 `−1/4+2(b+c_*)=67/532`。这由 `b+c_*=25/133` 直接得到；当前报告数值正确。

因此该版本可作为恰七极大、任意 n≥7、全部完整有序历史纯 SPE 的普通半覆盖 checkpoint。n≥7 时七个合法极大主题都能放入比较组合，所以 `OPT_n=U`。没有证明一般 arbitrary-maxima 半覆盖，也没有证明 core 强化 `U≤2W−c`。

## 2. n=5、6 的现有证书实际覆盖

完整 route 采用长度 n 的 restricted-growth strings，而非仅分类前 n−1 位。对每条 route，比较组合取 n 个不同极大覆盖；使用过的 labels 保留是否属于 K，未使用 labels 只按加入数量取一个 canonical representative。该操作保持全部 incidence 列与所有行的排列等价。

任意最佳 n 主题组合都可扩成包含其覆盖的合法极大主题，再补到 n 个不同极大主题；在 s=7≥n 时有足够极大主题，最优性阻止覆盖继续变大。因此这里的目标是 `OPT_n`，不能把小人数的目标自动替换成 U。

独立生成 orbit universe 得到：n5 有 52 routes / 363 `(route,K)` 轨道；n6 有 203 routes / 877 轨道，与 scan 清单完全一致。

| 人数 | 当前已有精确资产 | 通过的不同轨道 | 全部轨道 | 尚缺 |
|---|---|---:|---:|---:|
| n=5 | `seat_trees_n5/` 中全部 347 complete 树；其中194为直接叶、153为席位析取树 | 347 | 363 | 16 |
| n=6 | `scan_n6_seat.json` 中832个 direct exact multiplier；加 `000101,K126` 的完整席位树 | 833 | 877 | 44 |

n5 共 2,381 nodes、1,374 leaves；n6 该单树有7 nodes、4 leaves，其余832证书各一个直接叶。
全部现有证书已在 `independent_seat_assets.py` 中独立重放。检查 n5 的 1,037,946 与 n6 的 1,021,240 个 leaf/customer accounting inequalities，总计 2,059,186，最小余项均为0。没有使用浮点 LP 最优值。

另用原独立 Fraction auditor 交叉重放 n6 的唯一完整树，6,524列、7 nodes、4 leaves、最小余项 `93889/88800000` 与新整数审计完全一致；记录见 `original_n6_replay.json`。

程序独立恢复 base 行顺序、真实 incidence/会员列、所有路径席位行、每条析取 clause 的 r 个互异席位和全部 children。每叶 multiplier 非负，每客户余项非负，每叶冻结最小值匹配。整数共同分母覆盖全部行分母，精确计算与 Fraction 恒等式等价。完整结果与逐证书记录见 `independent_seat_assets.json`，其中保存每个缺失轨道。

**n5 缺失轨道：**

| route | 缺失 K masks |
|---|---|
| 01230 | 122,124 |
| 01231 | 115,117,118,121,122,124 |
| 01232 | 115,117,118,121,122,124 |
| 01234 | 103,107 |

缺失16份在旧 root 目录也没有完整文件，且 `seat_trees_n5_summary.json` 当前不存在。已存在347份不能当作363份完整批处理完成。

**n6 缺口：** `scan_n6_seat` 的45个无 exact multiplier 项中仅 `000101,K126` 已有完整树；其他44项列于独立结果文件。`n6_route_assets` 的3508个 correlated LP 记录仅保留 numeric/support/slack，没有精确 nonnegative dual；其中6项还在数值上低于半覆盖。它们不能替代完整精确轨道证明。

## 3. n5/n6 席位证书的全部历史与子主题依赖

席位树的 base families 全都在真正的实际有序前缀上取 true load：

| 行家族 | 数学来源与适用范围 |
|---|---|
| 个别 mixed floor | `CA-DYNAMIC-MAXIMA-MIXED`，完整历史归纳；允许子主题遗漏 private/shared/core |
| 最后玩家 BR | 真实末位节点相对每个合法完整极大主题 |
| 最后两名 tax | `CA-TWO-REMAINING-TAX`，任意合法固定背景与完整历史回复 |
| 最坏新负载偏离 | 当前玩家偏离合法 B_j，使用真实前缀负载 h 与最多 r 名新覆盖者；不固定后继行动 |
| subset-H | 新 true-load r-th-largest seat 定理的线性平均推论 |
| 末三名利润 | 已登记 `CA-THREE-REMAINING-PROFIT-5-3`，比较利润 `e/(h+e)`，任意合法背景 |
| 末四名利润 | 已登记 `CA-FOUR-REMAINING-PROFIT-1499-750`，任意合法背景；需其新增背景校正的原证明 |
| 析取路径 seat 行 | 当前真实收益至少 r-th largest；任意 r 个互异 seat 中至少一条 slack 非负 |

新 true-load seat 证明本身通过数学审读。固定所有 legal actions 的 containing-maximum routing 后，新增行动最多使所属 route 的 private true load 加一，其他 route 的 private load 不变，shared 的 `h+r` 不增加。各 route 的 seat 单调排列确保老 r 个 qualifying seats 至少留下 r−1 个。完整极大偏离若有同路由后继，包含该后继真实行动；原策略在该实际偏离历史给出后继 SPE，并传递单调 threshold。这一步覆盖所有离轨有序历史和全部 history-dependent ties。core 的 c/n 始终是全局人数 n 的保底，未假设实际早期行动覆盖 core。

树在每个分叉选任意 r 个互异 seat：真实收益低于的 seats 最多 r−1 个，所以这些 r 条中的至少一条成立。children 添加对应有效条件；证书是合法析取证明，不是把全部 seats 无条件相加。每份 unrestricted 树覆盖所有 private/shared mass ratios，因此不需要另外乘五个/四个 correlated mass-region case 数。

## 4. 保留历史成果和失败边界

以下对象继续保持各自原有地位，不能因新 checkpoint 合并或删除其身份：

- `CAG-MODEL` 是固定均分、单位客户/提供者模型；不导入主动客户 Nash 续局或其他设施模型。
- n≤4 的一般目录结果已经给 `OPT_n≤2W`；至多六极大的任意人数 theorem 仍完整有效。因此七极大任意人数的新缺口确实只有 n5/n6。
- 旧 dynamic mixed、correlated mixed mass partition、subset-H averages 和 full continuation seats 是不同强度的合法约束，不能把 correlated region hypotheses 作为无条件行。
- n5/n6 的 exact primal row obstructions 仅否定指定较弱线性机制；它们被完整 continuation seat floors 排除，没有完整 SPE，不能升格为原半覆盖反例。
- root-only seat order、全 p 补偿、根总税、一般税桥等先前失败边界不被本证书恢复。只有已证的真正两剩余 tax 被使用。
- 旧至多六极大 no-private/core 加强结论继续在原范围成立；七极大 n≥7 本 checkpoint 仅给普通 `U≤2W`，不冒用这些 core 加强界。
- 安全值完整树锥对偶、一般安全值/支付桥仍是不同未完成主路线；任意多数极大主题尤其 n<s 时应跟踪 `OPT_n`，不可无条件用全 union。

## 5. 可整合的范围和下一步缺口

可以现在整合成“至多七极大、n≥7” theorem（包含既有至多六结果）；也可分别归档 n5/n6 已覆盖轨道的完整 exact 证书。不能现在登记“至多七极大、任意 n”。要闭合后者，仍需获得并精确验证 n5 的16、n6 的44缺失轨道的合法证书，或提供替代这些轨道的解析论证。现有树成功并不证明剩余树生成必然有限闭合。

本审查不展开这些缺失轨道的新搜索；主组继续一般安全桥工作不会损失已完成 n≥7 checkpoint 或现有小人数证据。

# SOLVER-FRECHET-OBSTRUCTION-FRESH 审读记录

## 结论

已完成 task `customer-attraction-3a-3a-5d1038b171e5589d` 的 declared refs 全文/全字节读取与语义复核。对象结论保持 `proved`，但作用域是“固定旧六人必要点的 own 四态边缘无共同扩张”，不是完整纯 SPE、不是六人 `2W>=OPT_6` 的反例，也不是全增强系统不可行。现有 Boss1/Boss2 逻辑边复用；本包不新增边，仅以 support/review 资产固定 scope-boundary，供图上防止误读。

## 实读范围与核对

1. `固定末回复四态边缘的Fréchet共同扩张障碍--障碍.md`（SHA `749f...1aec`）：逐段核对一般 m>=2、恰余两人、真实 Z_e、IC 恒等式、Fréchet 上界、稳定子平均、六人 66 标签/16 hist/194 组、四个冻结负类、3949 修复和完整 SPE/half 边界。
2. `共同目录完整历史模型--定义.md`（SHA `cc4a...0e88`）：核对标签目录（同覆盖别名/空标签）、完整有序历史纯 SPE、真实后继 IC、重复/平局/零客户和背景利润不等于福利。
3. `source-manifest.json`（SHA `9f39...1739`）：逐条核对 6 主来源的 blob、路径、双冻结 commit 和 size。
4. `stdout.json`（SHA `ebab...55ab`）：核对独立入口的 16 hist、1920 labelled comparisons、7 非零块、最强负分数和 SHA。
5. `independent_zz_bound.py`（SHA `4f5c...e622`）：全文读取；只用标准库/Fraction，硬核唯一旧点 SHA，解码 hist 和三态，遍历 16*120，硬断言预期负分数，不读作者程序或旧报告。
6. `zz_bound_exact.json`（SHA `b9d4...938c`）：全文读取三层字段、六个具体负值、六个逐行最大值、四个任意联合宽界及最小值；不把三层数组合并。
7. `attractive_nested_exact.json`（SHA `cc48...6b1`）：完整 read_bytes 816498B 并 JSON 解析全部 1905 列；结构为 `hist=16`、`joint-reply=582`、`overlap=1306`、`K=1`，列内字段和四态组键全部检查。
8. `一般机制建议与六人Fréchet判别工作区--资源.md`（SHA `50d3...ef9d`，指定章节）：核对历史提案身份与“新增判别”范围，禁止把资源建议当定理。
9. `末回复Fréchet上界的双程序与三层有限报告--程序.md`（SHA `be45...bcdb`，指定两章节各全文）：核对任意联合宽上界、独立 4433B 入口、运行边界与三层量词。

为解释 half 边界，另直接实读已登记问题页 `archives/customer-attraction/state/问题/任意人数完整均衡半覆盖--问题.md`（SHA `bc5a...4d15`）；该页的原题量词是任意 m、任意目录、任意完整历史纯 SPE，且明确 `|R|<=W` 等加强支付条件不能代替 `2W>=OPT_m`。它只是范围参照，不是本任务的新增逻辑前提，也未修改 task state。

## 数学复核

按 `1/(a+1+r)=1/(a+1)-r/((a+1)(a+2))` 展开，在每个恒负载 H 块得到
`L=(v_e-v_f)/(a+1)+(J_ef-t_e)/((a+1)(a+2))`；own 四态固定 `q,v,t`，任意联合仅给 `J_ef<=min(q_e,v_f)`。乘以非负 IC 权重后，严格负右端确实排除任何保持这些边缘的共同联合。稳定子平均只恢复字面边缘，不改变相位；没有假设所有 Fréchet min 同时达到。

独立脚本一次输出的精确值为
`-77805114978912902524965135501273065957/176731722247831414031521292083980140160`，小于 0；它对应 source family 0、query family 1、index partition 0102，16 hist*120 个互异三索引=1920 项。该值已与冻结 JSON 的同一宽界逐字符核对，输入/源码 SHA 前后不变。

## 量词和反例分级

- 可以作为 whole 的，只是固定旧点/固定 own 四态下的局部不可扩张命题。
- 可向单环等新对象贡献的，是 IC 恒等式和独立 Fréchet 基准；单环的奇集充分性、可达修复、全权分离另由其自身证明承担。
- 新 self-check 是 context；不把固定点检查当完整游戏定理。
- refutes 仅针对“这份固定边缘存在共同联合并满足指定真实 Z-to-Z IC”这一精确陈述。它不针对 Q-CAG-HALF，不针对 `customer-attraction/six-providers/exact-six-full-history-half-cover`，也不针对任意完整 SPE 的存在性。

## 未重跑和不宣称

本轮没有重跑作者 6952B、旧 3889 verifier、LP/SLSQP/BI/SPE、全部 60 类或完整六人策略树；后三层旧数组按冻结 SHA 读入。没有把负的必要 LP 投影当整数客户实现或全模型 half 反例。没有修改 registry、map/coverage、map/integration 或 task state，没有 commit/push。

## overlap 处置

- `customer-attraction/six-providers/exact-directed-cycle-rz-marginal-transport`：已由现有 `cag-fixed-reply-frechet-contributes-single-cycle-free-baseline` 接收本对象的恒等式/自由基准；单环其余四类步骤独立完成，固定点负值不支撑其一般达到性。关闭，不另发重复 3B。
- `customer-attraction/six-providers/shared-rz-exact-pair-and-three-cycle`：现有 Boss1 cycle 包已比较 pair/three 精确运输与本对象的单向 Fréchet 松弛；共同双向/三节点闭包并非本对象推出。关闭，不另发重复 3B。

reviewed_by: `SOLVER-FRECHET-OBSTRUCTION-FRESH`

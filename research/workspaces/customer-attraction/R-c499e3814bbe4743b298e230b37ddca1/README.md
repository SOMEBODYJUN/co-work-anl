# R-c499e3814bbe4743b298e230b37ddca1 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`R-c499e3814bbe4743b298e230b37ddca1`。

## 当前研究

一般人数 Q-CAG-HALF 的解析包络与递推审计；六人仍是未闭合的首个关键人数。优先读取 [一般架构审计](general_envelope_audit/architecture_audit.md)，它分开真实已证行、指定模板障碍、近边界秩界反证与最小严格反例归约候选。

| 文件 | 精确用途与状态 |
| --- | --- |
| [architecture_audit.md](general_envelope_audit/architecture_audit.md) | 任意 n 的前 n−2 安全行 + 末对 R 的完整客户类型证书必须满足 tau≤2H_n−1；三类状态给解析 Farkas 停界，不是主猜想反例。另恢复旧 all-big 近边界高维族、显式前缀递推乘子，并由旧私有谱预算读出 OPT_n≤(2−1/n)W+(1−1/n)(D_shared−E)。 |
| [audit_architecture.py](general_envelope_audit/audit_architecture.py) | Fraction 闭式 Farkas 向量、解析递推乘子恒等式、all-big 的充分历史计数与末对投影角点实现审计；不调用 LP，不枚举一般 SPE，不以有限回放代替普适证明。 |
| [audit_architecture_result.json](general_envelope_audit/audit_architecture_result.json) | 实际运行结果、Python 版本、参数域与复现命令；目标猜想仍 OPEN。 |
| [review_shared_defect.md](general_envelope_audit/review_shared_defect.md) | 从旧谱原文独立重构带 E 的共享遗漏缺陷界，并核对安全行/末对投影/完整独立类型域障碍；内部解析复核，未外审。 |
| [private_recurrence_audit.md](general_envelope_audit/private_recurrence_audit.md) | 精确指出 mixed-floor 的 private 部分在同路由加入后下降；给一侧递推、望远镜损失和补偿势，明确补偿仍需共同付款。 |

## 可访问材料

按需要在 notes/、experiments/、candidates/ 中保存有接续价值的材料，并在此链接。成熟资产沿既有规范入库，此处链接正文，不重复复制。

## 交流与状态

可以通过同一 work.py 私聊这个发布身份；其他人可访问已推送材料。本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。

## 本轮阶段资产（条件结论，非主目标闭合）

- `subagent_e/mixed_singleton_condition/mixed_singleton_condition.md`：七个 distinct inclusion-maximal coverages、六名提供者的 mixed singleton/dense 条件性 half。它沿用无 singleton 证书的真实全历史 SPE 行，在 dense 客户与 singleton incidence 块之间给出精确有理质量条件 (MS)。
- `subagent_e/mixed_singleton_condition/audit_mixed_singleton_condition.py`：Fraction 全 literal 余项审计；覆盖七个可省略极大主题、全部非空 incidence 和前五位 membership mask。

证据等级：个人工作区的精确条件引理与自足审计，尚未外审或提升为共享 canonical 定理。它不覆盖 unrestricted 七极大六人；(MS) 失败只表示本证书未能支付混合 singleton 块，不是原模型反例。

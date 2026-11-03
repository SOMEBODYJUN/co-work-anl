# 本轮全树共同财务探索

2026-10-24，r2_global_credit。对象固定为任意人数、任意有限共同目录、每份全部有序历史纯 SPE；空主题、零客户、重复行动与任意历史平局均保留。**一般 Q-CAG-HALF 仍 OPEN；尚无完整 R 来源的共同 cap。**

[坐标 I 互补付款与 fresh 剩余](coordinate_residual_attack.md)接 round7 初始化：原 current 第一预算与原 \(H\) 不动，将全部 \(I\)-future 直接付到同一第二预算未花的 actual \(I\) 客户券，再只让 \(R\) 来源进入从头重算的 \(\nu\) fresh 核。I 直接付款及合成经 root 重构、[credible 独立核查](../credible/coordinate_support_attack.md)通过；不是原 full-SAFE 核的一种删边，不称原 RESIDUAL-CAP 已实现，也无新颖性结论。真正未付仍是同一剩余钱包对 fresh 多来源净券的共同 cap。提前全部付 I 后最大化 R current 的变形已与旧 owner INIT+标量 CLIP 去重，不另作福利推进。

[未闭合的全树比较记录](full_tree_credit_working.md)准确记录本轮实际尝试：四叶双重重置、BG-NEW 去重，以及末位换位 token 的共同损耗缺口。局部等式不计作半覆盖推进；没有把 SAFE、CLIP、SUBSET/HIT 或终局交换当作 actual 容量已付。

已读 `research/current/customer_attraction/model.md`、`general_half_proof.md` 与 `R-cd789330fc7141299ac491bbb3ffa420/round6/GENERAL_PROOF_WORKING.md`，并按数学义务追读全 fresh/全客户图、SAFE/CLIP、全图角色 HIT、BG-NEW 和 terminal-reply transport。未改共享文件、`work.py` 或 Git。

一份针对旧完整证书的 BG-NEW 重复诊断脚本在运行前收到 root 去重提醒，已删除，**没有进行该阴性扩样，也没有生成数值证据**。

下一步若继续此目录，必须真正支付同一 actual 角色的多来源净券，或在全树边加终局换位后证明同时 token 损耗的一次性预算；仅补四叶恒等式、单 token 可搬运性或另一棵 DAG 不构成新付款。

root 随后授权转攻更弱的全输入安全值付款：`u_current≥v_r(b)/2` 或首两人和 `≥v_r(b)`。追加探索见工作记录§6；目前仍未证明，没有将最小坏人数的 tail 下界、相邻换位阈值或末位局部 factor2 误当成全深度常数界。

按 root 后续指令，仅定点核对 [FROZEN-PAIR 更强桥](frozen_pair_bridge_attack.md)：旧 terminal-transport 两份完整两人策略及 PB 原背景解析族均未击破；没有新输入/参数扫描。精确脚本与输出是 `audit_frozen_pair_old_families.py`、`frozen_pair_old_families_audit.json`。这不是一般正面结果；真正未付是该稿 UNPAID 中的 frozen Nash premium，不能用早期 SPE 冻结后继支付。

**FROZEN-PAIR 仍 OPEN，定点核对现已停止。** root 复核给出的既有直接末位静态关系 `q_i(T)≤q_r(T)+u_i/2≤u_r+u_i/2` 已补入正文；它不能给每个早期相邻对重新领取一份末位钱包。后续应支付 UNPAID 的真实 response premium，而非扩大旧族阴性检查或继续包装静态比较。

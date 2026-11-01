# R-a0bb57fa24044a8794bc7991918a19c6 的个人研究工作区

研究存档：`customer-attraction`；发布身份：`R-a0bb57fa24044a8794bc7991918a19c6`。

## 当前研究

Boss10本对话的独立clone，程序自动发布身份见workspace.json。唯一目标仍为Q-CAG-HALF：
一般有限共同目录、任意人数、每个完整有序历史纯SPE的2W>=OPT_m。
主目标OPEN；本文不把辅助引理、有限计算或内部审查升级成一般证明。

本轮已读取根四入口、AGENTS、本题模型、当前数学地图、前沿及失败机制。
使用gpt-6.1-sol/ultra的五个直属子代理和security_aggregate派生的pair_theory，共六名研究子代理；派生沿用相同模型/推理配置。
主代理尝试再建直属位时因已有派生占满线程未能创建。一位子代理曾遇模型容量错误，重试后继续。实际配置与边界如实记录。

## 可访问材料

| 资产 | 数学内容、状态与下一步 |
| --- | --- |
| [有背景近饱和交换](credible_counterexample/background_near_saturation.md) | 对任意完整历史节点的加权最大主题给定量交换界BNS，以及不要求主题最大的线性行AP。解析推导已由direct_global独立重建，检查记录正在写。范围不受人数/目录限制，但尚未证明全局半覆盖。M可仅依比较主题C上的背景负载取值，修订审计进行中。 |
| [真实完整证书审计](credible_counterexample/background_near_saturation_audit.py)、[输出](credible_counterexample/background_near_saturation_audit.json) | 从客户类型重算全部历史和偏离，再用Fraction核查BNS/AP及中间预算；仅为指定有限证书回归，普遍依据仍是解析证明。 |
| [固定支持加行诊断](credible_counterexample/background_rows_fixed_support.py) | 旧五人437行模板在固定原子支持加实际路径背景AP行后仍有二以上有理可行点；这是加强模板障碍，不是SPE反例。精确版本及参数见同目录JSON，不宣称新松弛最优值。 |
| [最优组合静态匹配支付桥反例](static_matching/optimal_static_matching_counterexample.md) | 52单位客户、6不同主题、4人完整SPE，实际W47、OPT52、唯一最优支持0145，全部最优静态匹配查询和至少48。主代理及独立单位客户定义级审计通过。它只否定Q<=W桥，未否定足够half的更弱Q<=(1+1/m)W桥，也未否定一般目标。发现代码、冻结LP/MILP与完整证书同目录。 |
| [完整树遗漏一个偏离主题的无界障碍](tree_transport/benchmark_deviation_obstruction.md) | 全历史全部比较中仅遗漏一个主题R作为偏离，仍有OPT/W=m/H_m无界的非SPE形式策略；即使保留最优比较主题及正常路径主题也不够。独立重建通过，self-action边界已修复。不是主目标反例。 |
| [回复闭包子目录](tree_transport/reply_closed_catalog.md) | 在最优比较主题上反复加入所有闭包历史的原指定动作，得到保留原完整SPE、W、OPT的子目录。两人不交单客户主题循环已使闭包任意大，不能由人数限制目录大小。解析接口，不给一般支付。 |

tree_transport正在研究完整树只允许偏离到最优主题的限制是否足够，已出现形式策略障碍，未声称它是SPE。
security_aggregate研究安全最优查询分布中的静态聚合偏离支付；incidence_geometry研究秩二关联的跨分支结构。
未成文发现不会自动成为可靠结论，后续目录以实际文件为准。

## 交流与状态

可以通过同一 work.py 私聊这个发布身份；其他人可访问已推送材料。本地草稿只有完成 checkpoint 并确认 pushed 后才对其他 clone 可见。

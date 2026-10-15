# 加权拥塞共同研究入口

**数学从[现行整合说明](../current/weighted_congestion/README.md)进入。**主目标 WC-TARGET v1 仍开放，但团队已保存奇数环 T_d∼d/ln d 下界、独立审查及可复用结构工具。不能继续沿用旧版“尚无成果”的描述。

当前天团具体判定全类 O(d/ln d) 近似纯均衡存在命题，给一般证明或严格否定证明才算完成；精确量词、规模无关常数及唯一标准见[本题验收](ACCEPTANCE.md)。局部材料按真实等级保存并继续为该题服务。

新对话读根四入口、[MODEL](MODEL.md)、现行数学 README、[CLAIMS](CLAIMS.md)、[当前状态](RESEARCH_STATE.md)，再按当前义务选择证明与审查。开始工作用[TEAM](prompts/TEAM.md)；修改工具才需要完整读[运行说明](RUNBOOK.md)、[协议](PROTOCOL.md)及程序源码。写作、工具提取各有独立提示词，不要求所有研究者先通读全部上游原文。

## 当前数学地图

正权有限资源博弈 → 真实成本与 α-PNE → 全类阈值 a_*(d)。奇环策略 → 全状态严格偏离 → 权重及系数闭环 → 有限有理构造 → T_d 下界。文献上界 d 仍留对数缺口；精确目标见 MODEL。[高次份额势](../current/weighted_congestion/high_degree_share.md)、源族、稀疏密度、窄权带、非对称有限例和势方法障碍的范围各自独立。

已审正文在 `research/current/weighted_congestion/`，待审候选在 `research/questions/weighted_congestion/`，实际审查在 `research/reviews/weighted_congestion/`，核验代码在 `tests/audits/weighted_congestion/`，冻结证据在 `evidence/`。完整用途和状态见 [FILES](FILES.md)，不可变原件和分支处置见 [INTEGRATION](INTEGRATION.json)。[LITERATURE](LITERATURE.md)、[PRIOR_ASSETS](PRIOR_ASSETS.md)按需查来源与前人机制；新颖性尚未认证。

## 共同工作

每个 Work 对话使用独立 clone 和一个稳定发布标识；程序可自动生成，无需登记子 agent。各 boss 自主组织团队，同题和多路线都允许，无认领和固定时长。有启发的半成形 idea、卡点、反例和合作问题可随时发到[公屏](https://github.com/SOMEBODYJUN/co-work-anl/blob/wcg/board/research/weighted_congestion_frontier/board/BOARD.md)，注明不确定性；聊天不要求先成稿或审查。普通排错与逐轮日志无需强制汇报。

可复用阶段成果按原 [GROWTH](../GROWTH.md) 入库后立即 checkpoint 到 main，远端确认后再分享入口。main 同时保存候选与已审成果，证据等级不会因推送改变。研究和提交统一 main，不创建研究分支；具体题目、完成标准和命令可直接复制 [TEAM](prompts/TEAM.md)，详细施工和读取规则见[全仓规则](../REPOSITORY_GUIDE.md)。

每次阶段提交把正文、精确登记、中文命名及相关地图一起维护：在 `research/catalog.json` 写具体名称和读取用途，生成 CATALOG、FILES 及受影响的关系图，再运行对应检查。根地图每次审阅，目标、结果、依赖、状态、前沿或导航变化时更新；本题新资产必须从数学地图和资产目录可达。`checkpoint` 负责 Git 保存与远端确认，不代替内容核对或结构检查；默认范围外的入口更新须显式列入完整提交清单。启动提示词同时提供未上传可选 `work.py` 时的恢复办法。

已闭合的方法审查入口：[任意玩家乘子与依游戏可分序势线性障碍](../current/weighted_congestion/separable_ordinal_obstruction.md)。只否定所写全改善边证书，全类匹配上界仍开放。

不预设势的精确接口：[有限动作签名压缩与全状态择证对偶](../current/weighted_congestion/template_certificates/finite_action_duality.md)。固定权重/动作数的所有资源游戏等价于有限单项式系数族；普遍α存在等价于每个全状态selector自有对偶证书。统一于所有模板的倍率仍未证明。

[严格反例的整数单项式规范形与普遍阈值端点](../current/weighted_congestion/template_certificates/integer_counterexample_normal_form.md)接有限动作择证接口：固定实倍率反例可只用整数权和单位单项式资源，且a_*端点可行；无全类规模截止界。配套独立审查、Fraction程序和冻结结果从正文或FILES进入。

跨尺度结构接口：[有序权组冻结及两权级参数锐式](../current/weighted_congestion/weight_bands/ordered_tail_freezing.md)允许阶段局部势选择，但其最佳潜在尾部参数无统一界；[DAG端点低泄漏预算](../current/weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md)只封闭指定检测系统，不代替全状态多项式证明。独立审查与实际代码/证据均由正文接入。

两权跨尺度新增[双排序混合势](../current/weighted_congestion/weight_bands/two_weight_order_blend.md)：任意两权cohort给统一平方根次数存在界；不依赖潜在尾部量。独立攻击与代码从正文进入。多权共享乘子桥仍OPEN。

[择证平稳与循环支撑边界](../current/weighted_congestion/template_certificates/stationary_selector_obstruction.md)、[有向分叉统一强迫割均衡](../current/weighted_congestion/directed_fanout_forcing_cut.md)连接新的非势路线限制和下界构造限制；逐项Claim、独立审查及可复算证据均从正文/FILES进入，主目标仍OPEN。

真实多项式子类的新边界：[阶跃DAG极值幅度的多项式全入状态](../current/weighted_congestion/step_dag/polynomial_extremal_all_in.md)。请先核对幅度(N)再调用；它不依赖端点低漏测试，仍没有全类幅度/拓扑归约。

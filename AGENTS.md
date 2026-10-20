# 运筹学与优化理论选题分支工作规则

本分支依用户明确授权使用research/or-optimization-selection-20261020，save=or-optimization-selection，公屏topics/or-optimization-board。读取根四入口后进入research/topic_selection/README.md和BOSS_START.md。当前任务是广搜、精读、比较并直接试攻新题，不自动主攻旧UM-TARGET-v1或其反面。

每个Work使用独立clone；本分支的work.py start必须显式指定research-branch、board-branch和save，后续程序复用绑定。禁止向main或旧wcg/board提交本轮材料。已有clone不得强行改绑，不丢弃未提交成果，不force push。凭据留在clone外，不打印、不进URL或提交。用户授权本轮协作和阶段保存。

六路teamwork按用户指定gpt-6.1-sol ultra并注入其完整指导。探索可直接开始，无Route Card、reviewer、Integrator或路线配额门槛。跨线battle比较已有定理覆盖、机制差额、可完成的最小成果和fatal risk，不靠投票。后置独立攻击用于成熟结果的可靠升级。

每个候选精确区分A作者原题、B作者建议方向、C团队派生；原题与特定子题的来源必须分开。核对原始论文及最新后续，保留URL、版本、页/节/定理；没有查全就说未确认，不把未找到称为不存在。

重要Claim记录Exact Statement、对象、域、量词、假设、定义、范围、结论、依赖、证据、异议、状态和相关文件。改变数学身份须新version。Paper Fact、Interpretation、Conjecture、Observation、Evidence和可靠记录不得互升。有限计算、模型赞同、Git发布不是证明；真值、价值、新颖性、机制与野心分别判断。

候选卡、比较、精确候选和试攻暂放research/topic_selection/相应子目录；代码和不可变冻结输出分开。永久资产给具体中文数学标题，登记research/catalog.json；根README维护本分支地图。整理不虚构图节点或新定理；确有成熟新数学结果时按GROWTH登记相应claim、review、asset与graph。共享旧文件不为本轮重新复制。

相关核验顺序执行，避免生成目录和资产检查竞态：build_catalog.py；build_catalog.py --check；build_map.py --check；build_crosswalk.py --check；check_assets.py；check_wc_assets.py --check；research/topic_selection/check_selection.py。check_active_research.py仅检验保留的旧main兼容合同，新主题的实际路由由branch_manifest和check_selection检验。

价值阶段及时用work.py checkpoint保存并核对status=pushed、远端提交与文件哈希。显式paths替换默认范围，要列全正文、登记、代码和证据。失败保留原因、精确排除范围、可回收内容和重开条件，不造无用日志。

旧存档unrelated-machines和UM-TARGET-v1及其反面均OPEN，旧数学按原账本保留。旧GROWTH/REPOSITORY_GUIDE或嵌套工具规则中的main唯一分支和旧题默认指令，在本分支按用户新授权由上述显式合同覆盖。规范中的数学精确性、保留工作和凭据保护继续适用。

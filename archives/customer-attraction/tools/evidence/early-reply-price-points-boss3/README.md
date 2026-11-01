# 实际四五位显式新回复补价及阶段精确点

正式计算对象：[显式新回复的实际四五位补价与精确点](../../../state/计算/显式新回复的实际四五位补价与精确点--计算.md)。

四个primary源的完整冻结来源在 source-manifest.json。original保存原early_reply_prices.py及两个新原点；cross_source_priced_optimum_exact.json逐字节匹配已持久保存的[旧完整原件](../cross-source-graph-program/related/cross_source_priced_optimum_exact.json)，按storage_scope=repository复用，没有再复制。两个大新JSON均保全部1905列及全部有理质量。related-manifest.json绑定原排序helper、原36行代码及旧4963旁读点；旁读不追加done。

实际事件与范围：

- replay/base-execution.json及对应stdout/stderr：原默认early_reply_prices.py --verify一次，5251行/1905列、全部Fraction余量非负/min0、精确W匹配、44.146秒、exit0。
- replay/floors-execution.json及对应stdout/stderr：原 --floors --verify一次，5287行/1905列、min0、另一精确W匹配、44.414秒、exit0。
- 全部数学代码、依赖、输入、输出与组织脚本均在clone外新stage/runtime运行，没有重新优化、没有旧4927或4963整图重跑。
- audit_added_price_rows.py不构建继承全图、不调用main或LP。原新增build函数以AST摘出并接空行基底；原侧用排序helper，独立侧逐二元隐藏态及具体有序索引边核324行。原36行与另一份有序边实现也比较。合685800个精确系数相同。
- replay/added-row-and-point-audit.json保三主点及旧4963相关点的全部360条有理余量、全部顶层字段、1905描述符、194/2612联合质量上界、O/W/gap与逐列差异；没有把局部独立实现称第二套完整矩阵。

重要区别：324=actual4的216+actual5的108；--floors的360=324+36。新324在两个旧保存点上已经严格正。4927→5251同K/hist/W但118辅助质量变化；4963→5287同K/hist/W但95辅助质量变化。5251点尚有5条早源36floor为负，5287点36行全非负。两新原点是不同条件图，均未给完整SPE。

从仓库根可在新独立绝对路径材料化：

    python3 archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/materialize_runtime.py /absolute/new-runtime

这个工具先核SHA恢复已有47份冻结依赖，再覆盖本批四源；根work.py仅注释性找根标记。它不自动执行任何研究入口。需要复现时再显式运行：

    python3 -B /absolute/new-runtime/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/early_reply_prices.py --verify
    python3 -B /absolute/new-runtime/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/early_reply_prices.py --floors --verify
    python3 -B archives/customer-attraction/tools/evidence/early-reply-price-points-boss3/audit_added_price_rows.py /absolute/repository-root

原完整verify需要NumPy/SciPy且assert开启；独立局部审计只用标准库，读取明确归档原件并只重写本包replay中的当前审计报告。run_original_once.py是两次真实事件的组织脚本，拒绝覆盖已有事件记录。默认优化模式会写同目录exact/status，本批没有运行该模式。

有限图点、全输入合法必要行、精确最优证书、共同客户实现与全部有序历史SPE分别保存；本包没有half证明、完整反例、外部评审或新颖性认证。

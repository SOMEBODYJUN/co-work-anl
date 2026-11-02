# 实际删位封顶与离轨槽预算：四主源

四原件27465B完整保在original/，来源ID、双冻结commit/path/blob、SHA和大小在[source-manifest.json](source-manifest.json)。两个py均逐字读完整，两个JSON全部字段、十九个矩阵及概率向量都已实读。自足数学与软件合同见[正式正文](../../../state/程序/实际删位静态封顶的原扫描与离轨槽预算--程序.md)。

## 原件的不同责任

- 3321B leave_one_out_probe.py：从给定完整SPE实际叶删一个占用主题槽，形成全部纯query×不同删除主题矩阵；两次float LP提出概率，限分母/截负/归一后按Fraction保存L、U及阈值判断。扫描文件对而非全数学实例。
- 16214B leave_one_out_existing.json：十九项，每项完整14字段及矩阵/两有理概率/实际path/counts；L=U、无strict_failure。原verified:true是历史全策略验证字段，本包不重新认证十九策略。
- 5751B audit_offpath_dual_budget.py：独立标准库DAG审计旧m13/36客packet，另精确计算实际删位列、T遗漏客户的支持限制和离轨槽期望下界；不是新的SPE。
- 2179B offpath_dual_budget_audit.json：27243node/112050含self真IC历史报告、三删除列全部六query、阈值66/25、cap3/差9/25、两个6/25必要期望下界、91520恒等式回归及只限query的二点混合。

## 唯一新增数学运行

[check_saved_matrix_witnesses.py](check_saved_matrix_witnesses.py)只用标准库Fraction读取原16214B有理报告，未导入原探针、模型、verifier、DAG或LP。只执行1次：19矩阵共300个有理项，概率非负归一，counts/support/path维度一致，所有纯row/column重算的上下界精确匹配原字段且相夹。十九值均严格小于阈值，strict_failure全false。

[matrix-review.json](matrix-review.json)保完整row/column值与精确非负slack；不是原float优化器残差。原报告不保float result.x/fun、原环境或残差，不能反推那些值。当前事件Python3.12.14，exit0、stderr空，内部0.003541473秒、进程0.063407895秒；[event](matrix-review-event.json)绑定argv、输入前后SHA、检查器SHA、输出SHA与标准流。stdout/stderr独立保存；检查器的输出新建模式拒绝覆盖。

这是**保存矩阵游戏的精确证书检查**：不新核矩阵从原客户抽取的身份，不认证其全部SPE、不重新运行扫描，不外推全目录/全部策略。不能把source-report verified:true当成本次verifier调用。

## 十三人输入与成熟证据复用

旧gzip SHA为bad2b15d1abe89d9fa8671df84de8638a4b1ca46279712baa5482abb2bdf18ce；原27243node/112050IC已有fractional-load-boundaries精确成功证据充分认证。本批只核同SHA身份并读该既有完整报告及正式数学，**不解压逐node再认证、不重复旧全IC**。相关原件和既有事件路径在[dependency-manifest.json](dependency-manifest.json)。

解析新读序将两个来源特有结论分开：仅actual支持{A,B,P}的任意十二槽背景，T价恒3，排除弱cap66/25；实际三删除列T恒3且全部query≤3，故固定删除矩阵κ=3。源码只min纯删除cap一般不计算混合minmax，这个固定表的上下相夹才保证结果正确。

若完整静态对偶Q能cap所有query，遗漏T三个客户的平均期望命中槽以及期望非actual槽必须≥6/25。原两字段的minimum是此必要下界，不授全约束下精确最小值。19/25零T、6/25一T只对T切面sharp，其他query可能超cap。实际例的合法十二槽背景(A,B,T,P九次)已cap5/2，故该13点不反真正静态安全值或half。

本批原offpath audit执行0、原leave-one-out probe执行0、规范SPE验证0、LP0、旧DAG/静态矩阵回放0。91520只归原有限恒等式报告，不冒本批新运行或SPE数。

## 再运行原入口的准确要求

offpath入口仅标准库，在原research/workspaces/.../independent_reviewer布局用HERE.parents[4]找根，依赖ROOT下指定gzip。它有guard但没有CLI解析，--help会执行main，成功覆盖相邻报告。不要将它在original目录执行后声称恢复原相对布局，也不要用-O关assert。

leave-one-out入口还需NumPy/SciPy及正确可import的customer_attraction包，从ROOT下examples与同basename certificates动态发现可处理文件。只找到actions的对象才处理；结果由那份文件树决定。原报告没有十九对输入SHA，因此依赖清单中的同路径冻结定位仅是未来重放候选，**不冒充原历史实际字节绑定**。本包无需重新取得它们即可核现有完整矩阵证书。未来若重建，要按新文件SHA和真正处理/跳过列表另记事件；不能保证重放十九项恰同，亦不以失败后遗留JSON充新输出。

## 处置与接续

[relation-review.json](relation-review.json)解释受限静态与不受限静态、已有SPE与新推论、SA冻结总额与本矩阵、真实偏离匹配及19有限成功与13人反例的区别；没有编辑共享图。四主源分别完整integrated，receipt由根串行checkpoint后done。

原报告缺失的环境/旧argv、十九策略文件的历史SHA、query-only与全对偶的差别都明确保留，不用额外运行掩盖。完整性/链接/指纹及数学量词自查见[self-check.json](self-check.json)。

# 背景利润储备递归：原始材料与复用证据

九份本批主源36624B均按冻结size/SHA保原字节，见[source-manifest.json](source-manifest.json)及`original/`。另两份相关源42075B由父方正常导出，仅作阅读依赖，不新增done，见[related-source-manifest.json](related-source-manifest.json)及`related-original/`。完整原相对路径和提交定位保留，未改写旧OPEN/FALSE状态字段或历史身份。

正式正文：

- [合法背景剩余利润的精确盈余递推与静态保底](../../../state/引理/合法背景剩余利润的精确盈余递推与静态保底--引理.md)：共享最终分母、精确盈余、floor、条件递推与指定前提反例分开。
- [背景利润储备递归的原审计与弱诊断合同](../../../state/资源/背景利润储备递归的原审计与弱诊断合同--资源.md)：九源全文代码/所有报告字段、历史审查先验与真实执行边界。

## 本次阅读与唯一静态比较

全文读取九主源，包括39项family行、原独立报告全部25个数学/元字段、三份程序的完整逻辑；相关8250B独审全文八节与33825Bpacket全字段亦实读。packet只有一记录，instance九类69单位客户、strategy全部259条动作均已解析。

本轮只做一次小型策略身份比较：逐条将packet动作与成熟69客户闭式规则对照，0差异。深度0/1/2全部A，末层A200/E3/F13。该比较没有运行任何收益、完整IC、F/floor、LP或随机扫描，结果与实际边界保于[policy-identity-check.json](policy-identity-check.json)。

成熟69客户同闭式策略已在4347B标准库`audit_reserve_states.py`原入口成功一次；本次全文读其源码、旧event及冻结比较，核代码SHA与旧event一致。`prior-success-reference/`保这三个实际文件及当时890B报告/真实stdout的副本；其中旧event的cwd是历史运行位置，不是本轮再执行位置。具体读路径与SHA见[reuse-manifest.json](reuse-manifest.json)。与packet逐动作同一后，充分复用该策略的259历史/1295非自身偏离成功，不重复旧工作。

另一成熟R18大题族已有更广公式与全树成功，当前九主源家族/平方公式是同族独立重现；同样不重跑旧公式。原稿本组的3423Breview是另一历史独立实现，本轮没有运行它；独审的“盲推再对照再改状态”按原八节时序保存，不新增盲审事件。

## 原程序未来如何复现

`slack_audit.py`有main guard，默认只print family/3408比较JSON，`--diagnostic`只print其有界reserve诊断，不自动写邻接报告。`probe.py`也有main guard、只print，seed731/1750输入的历史阴性仅MD自报，本包无其历史stdout。`review_reserve_counterexample.py`无main guard，导入即读取相邻`../credible_construction/recursive_step_attack.json`首记录并核验/print；复现须保这一层级，不能在未准备输入时import，也不能据它认证原LP的504行最优。

本包`original/`只放九主源；`related-original/`另保所需攻击JSON，未来如执行原review，应在空的临时根复制两树到共同原相对路径，输出另存，勿覆盖冻结原件。当前**没有做这个执行**。

## 当前运行与数学边界

本批原默认slack入口0、--diagnostic0、probe0、review0；新游戏收益核验0、旧69IC0、旧R18公式0、LP0。只有原件SHA/文本/语法/字段与上述一次静态动作身份比较；没有新随机样本、策略求解或程序PASS。三个程序各自的历史输出与未附输出在资源正文单独解释。

原主稿解析记账/floor为真；`max{Fchild,2rhchild}`储备台阶被69>65否定；原260输入325转移中仅4困难的阴性不再支撑该候选为OPEN。更强额外槽probe是另一未证命题，不能因reserve失败一并判假。所有反例整体half余额仍正，一般背景half与当前六人问题没有被解答或反驳。

[relationship-review.json](relationship-review.json)提供依赖、纠错、有限实现与来源优先权的逐条理由，留第三阶段判断，不修改旧图。本内部代理未进行Git、认证、claim或done；父方checkpoint确认pushed后再串行登记。

# 完整624共同隐藏系统增广：精确保留、继承下界与Actions接续包

状态：**本地一次全矩阵发现已达到时间上限；完整输入与接续程序冻结，等待Main提交Actions。新最优值是否高于19662行基线仍未判定。** 本轮没有新增精确原始可行点，不能把内部迭代目标当作上界，也不能宣称同值最优或严格提高。原六人共同有限非空标签目录、单位客户、全有序历史纯SPE的 `2W ≥ OPT6` 义务仍为 **OPEN**。

执行范围仅为 `actual4 / 强制旧R / family0-off / 原16hist`。本代理只写本文件及 `full624_augmented_lp/`，没有改Git、registry、RUN、token或任何旧冻结成果。

## 1. 本轮已完成的严格结论

完整通用符号包已追加到19662×15593基线，得到 **20910×20585** 矩阵，含 **3,208,797** 个非零系数。其中新增1248行、4992个非负隐藏质量列、新增2,254,128个非零系数。原19662行及15593个列描述符、目标、归一全部逐项原样保留；10744旧辅助坐标没有替换或删除。

对所有新系统可行点，旧精确下界仍然成立：

\[
W\ge W_0=
\frac{10253811004692596155799640372033533039869218889763722158006672884316683593385089}
{20796753557630743087919205753819570281394973295085477880648801884521745817566822}
\approx0.49304863743650357.
\]

证书使用原309个严格正对偶行权，在新增1248行上补零。原对偶恒等式

\[
c=W_0a+\sum_{i=0}^{19661}\lambda_i A_i+r,
\qquad \lambda_i\ge0,\ r\ge0
\]

在新4992列上补零后仍逐项成立。独立核验实际检查了全部20585个列残差，最小残差精确为0；新列残差全部为0。结合 `a·x=1`、`Ax≥0`、`x≥0`，即得上述下界。这里没有引入新的福利下界数值。

独立核验同时重新检查旧精确点的全部19662行、15593列及旧原始/对偶互补关系。旧点在完整624系统中没有共同提升的两条负投影见证仍有效，但它们只排除该点。旧恢复面有6个自由坐标，不能由此推断新LP最优值严格增加。

## 2. 通用符号系统的保留核验

已实读 `union_augmented_lp.md`、其完整精确矩阵、原始恢复程序、最终对偶修复程序、独立核验程序；随后实读 `complete624_transfer.md`、构造脚本、完整提升包及manifest。装配核对了上一工作区freeze manifest中的全部52项资产SHA。

| 部分 | 增广编号（从0起） | 本轮处理 |
|---|---|---|
| 原语义坐标 | 0…4848 | 原样保留 |
| 7954个canonical max与2790个canonical min辅助坐标 | 4849…15592 | 原样保留 |
| 新共同隐藏质量 | 15593…20584 | 全4992列非负，目标/归一补0 |
| 原19662条行 | 0…19661 | 编码不变，新列系数为0 |
| 312个边缘等式的正反行 | 19662…20285 | 全624行保留 |
| 完整624预算 | 20286…20909 | 全部保留 |

全部16hist、78个有效有序词对组、312个旧R/Z四态边缘和每个边缘的16个新隐藏态均保留。没有根据当前点的零质量删hist、词对、边缘或隐藏态。原固定点的6个零质量hist仍在系统中。

独立核验器 `verify_certificates.py --structure-only` 不导入装配、数值求解、恢复或同行特征程序。它从原4849列描述符独立恢复每个词对的字面有序异索引配对，核对重数与 `multiplicity/30`；重新构造全部312个符号边缘及其正反行；重新构造全部624预算在原坐标上的actual `u4`、`u6`、`K`系数，再把整个1248行/4992列新块逐项与绑定bundle比较。

新增每条行在10744旧aux上的系数都为0。原符号质量没有被固定点rhs替代。四条恒零middle预算行20312…20315仍保名保行。两条已知负投影行以及正的备用616行没有额外追加；本次严格使用完整提升包。

## 3. 唯一一次本地数值尝试及真实失败状态

实际使用 Python **3.12.14**、NumPy **2.3.5**、SciPy **1.17.0**；求解日志报告 **HiGHS 1.8.0，git hash 222cce7**。

完整LP使用全部20910条齐次不等式、全部20585个非负变量与 `O=1` 等式，逐行按最大绝对系数缩放后送入 `linprog(method="highs-ipm")`。配置为primal/dual feasibility tolerance各 `1e-10`、IPM optimality tolerance `1e-12`、presolve开启、**170秒时间上限**。

该次调用在43次IPM迭代后达到时间上限，crossover未运行。HiGHS报告运行时间170.32秒，Python求解调用171.285秒，完整子进程172.632秒；真实退出码为 **1**。SciPy返回 `success=false`、status 1、`x=None`、`fun=None`。日志中的内部末次目标约0.62227587636只是未完成IPM的迭代诊断，不是已认证可行上界或最优值。

由于没有数值原始数组返回，本轮**没有执行精确原始恢复或精确对偶恢复**，也没有失败恢复候选可以声称成功。完整失败stdout、stderr、argv、源SHA、执行源码快照与退出状态都已保留。本地优化调用总数严格为1，没有第二次优化，也没有隐藏批量计算。

## 4. 实际执行记录

以下均在仓库根执行；驱动保存真实子进程argv、UTC时间、Python版本、源SHA、逐字stdout/stderr及退出码。

```sh
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/run_stage.py assemble assemble_solve.py assemble
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/run_stage.py solve assemble_solve.py solve
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/run_stage.py verify_structure verify_certificates.py --structure-only
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/run_stage.py actions_dry_run actions_pipeline.py --method highs-ds --time-limit 1800
```

| 阶段 | 真实退出码 | 结果 |
|---|---:|---|
| 完整符号装配 | 0 | PASS，36.97秒 |
| 唯一本地完整LP发现 | 1 | 时间上限，172.63秒，无可恢复数组 |
| 独立结构与继承下界核验 | 0 | PASS，15.67秒 |
| Actions接续命令dry run | 0 | 只校验输入与输出计划，没有执行优化 |

六个Python程序的AST语法解析通过。Actions中的新原始/对偶恢复及最终证书核验路径尚未在新数值点上执行，不把语法检查或dry run描述为数学证书。

## 5. Main可直接提交的Actions接续

`actions_request.json` 给出完整输入SHA、依赖版本与一条运行命令。它尚未dispatch。本代理不处理凭据、不调用外部Actions API，也不改工作流。默认接续在标准Actions runner上做一次完整 `highs-ds` 求解，时限1800秒；更改求解器或时限时，实际参数仍进入各阶段receipt。

```sh
python3 -B research/workspaces/six-boss1-20261111/full624_augmented_lp/actions_pipeline.py --execute --method highs-ds --time-limit 1800 --output actions_run
```

执行程序检查真实runner的 `GITHUB_ACTIONS=true` 标志，防止把接续命令误当成第二次本地优化。结果写入本工作区的全新 `actions_run/`，不会覆盖本轮日志或旧冻结文件。失败阶段也保留输出供接续。

单次发现成功后，程序先尝试在旧精确W上恢复原始点。旧10744辅助量以canonical max/min符号消元，原质量与新隐藏质量联合做精确稀疏有理消元，然后检查全部20910行和20585列。若得到同W点，直接使用继承对偶，便证明同值最优；无须额外求解对偶。

若同W活动面恢复失败，失败输入、所选精确方程、traceback和退出码会完整保留，随后仅用同一数值数组恢复未固定W的点，不再调用优化器。若W提高，必须恢复新精确对偶并逐列核验。最终独立核验器只有在完整原始/对偶非负性、归一、目标相等、互补性以及所有输入结构都通过时，才写出 `certificate_verification.json` 和 `actions_completed.json`。任何失败都不会自动循环数值优化。

同W恢复失败只说明当前选取的数值活动面/支持恢复失败，不证明旧W不可达。即使Actions发现W上升，也仍需完整有理证书后才能作精确最优值结论。必要LP的最优值比较不等于原题的SPE构造、反例或全域half证明。

## 6. 固定输入与输出身份

| 文件 | SHA256 |
|---|---|
| 原19662矩阵 | `99253e05bfe4c5705619777a5989ec9fab5c38dc7e56f934bbe8d9c071040ded` |
| 原精确点 | `b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3` |
| 原精确对偶 | `78a7cb206f9e807d0228d20ca7eaeafaf088fc551c719ba44dad4ed10f70f5ef` |
| 完整通用624 bundle | `3031a0710bd3b99fe421889ccb891e671d11f019f7d9cc9b3165818adc759d03` |
| 本轮完整20910矩阵 | `96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30` |
| 完整数值CSR输入 | `bdf06ee0ac8e10d4a7e8b19c6b90ab7f85b170a3ee87179816103ceea5074c52` |

`freeze_manifest.json` 保存本文件、全部程序、输入、输出、执行记录和源快照的完整SHA清单。下一步唯一未完成的具体计算义务是：在完整增广系统取得成功发现，恢复/独立核验新精确原始点及所需对偶，并据此比较W。当前已达到获准的本地计算边界，交Main提交Actions后可继续。

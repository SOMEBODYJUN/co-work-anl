# 共享匹配、相邻负载与固定边缘运输十二源

Boss2对本批12主源共31869B逐份完整实读；四py全部函数/循环/副作用、八JSON全部字段/列表/精确负分数均已比较。原件位于[original](original/)，[source-manifest.json](source-manifest.json)保存每份稳定源ID、完整原路径、双冻结commit、blob、SHA、大小和对应父方clean-show回执。所有源均来自 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同内容版本。

三份正文分别为：

- [共享匹配损失与相邻负载恢复的原精确核验器](../../../state/程序/共享匹配损失与相邻负载恢复的原精确核验器--程序.md)：原四份代码/报告的全部功能与准确有限域。
- [固定三族边缘的共同运输与自由余量浮点探针](../../../state/程序/固定三族边缘的共同运输与自由余量浮点探针--程序.md)：两个LP、四报告、自由ε、代码/旧报告字段差异与重复路径。
- [单菜单与共同菜单增强点的精确联合分离](../../../state/计算/单菜单与共同菜单增强点的精确联合分离--计算.md)：两份原精确分离报告，69点成熟结果复用及65点首次指定行核验。

## 原件逐份去向

| 稳定源ID | 原件 | 数学/实现去向 |
|---|---|---|
| a50a9bc540129404e3ec | [adjacent_load_checks.json](original/adjacent_load_checks.json) | 原1555列表、210已见边缘组、1742兼容边缘对的准确字段 |
| 838ed77a77ae3b76dafb | [exact_joint_727_separation.json](original/exact_joint_727_separation.json) | 69点AB→second两个single正、joint负；与成熟精确输出同值 |
| d558f49f04920b5f5078 | [exact_joint_728_separation.json](original/exact_joint_728_separation.json) | 65点AB→AE两个single非负、joint负；当前新指定检查同值 |
| 437a537e7a538f33cbed | [joint_pair_feasibility.json](original/joint_pair_feasibility.json) | 最终717点两个独立族对各30行的原浮点记录 |
| f8f37addfd2643eefaea | [joint_pair_feasibility.py](original/joint_pair_feasibility.py) | 分数运输边缘、30共同pair行及自由ε；terminal参数未使用 |
| 9e223a4fac70729c6223 | [multimarginal_exact_optimum_primal_joint_terminal.json](original/multimarginal_exact_optimum_primal_joint_terminal.json) | 65点三个模式、312变量/483等式、四负single、归一余量/发现权 |
| 849add527f09a0c17994 | [multimarginal_exact_optimum_primal_terminal_cross.json](original/multimarginal_exact_optimum_primal_terminal_cross.json) | 69点三个模式、321变量/510等式、五负single、归一余量/发现权 |
| da8de8f6baf2ef40f573 | [multimarginal_feasibility.json](original/multimarginal_feasibility.json) | 与上一原件逐字节相同的旧无后缀路径；按具体重复处置，不算第二次数学实验 |
| 8a04acadadbd75a67345 | [multimarginal_feasibility.py](original/multimarginal_feasibility.py) | 一份客户内三族联合槽供全部220 pair和所选28 terminal共用 |
| 7dede78e1048028f9ac6 | [shared_incidence_loss_checks.json](original/shared_incidence_loss_checks.json) | 原9360/9008与69点原子级检查报告，保持历史运行身份 |
| cc8bfc2a587bb668d412 | [verify_adjacent_load.py](original/verify_adjacent_load.py) | 四格递推、唯一性/交错验证及顶层写回副作用 |
| 6da9749f7545ae3c3e9a | [verify_shared_loss.py](original/verify_shared_loss.py) | 不导入发现者程序的原层式/梯形/69点核验器 |

两份4291B别名SHA均为 `04320e2a559297bf72a104fa23f1b8a0b0c770499f5ecee198ae55070220b308`。727原报告键 `omitted_negative_single_terminal` 与当前py的 `negative_single_terminal_envelopes` 不同；没有宣称当前源码字节重现旧报告。all模式下这些负行实际保留，旧键名不改变248行系统。

## 当前唯一新数学入口

此前65点原件缺失，父方现只读导出为相关依赖；[related-input-manifest.json](related-input-manifest.json)保131961B原件稳定ID `f631b972df940d1edbb7`、双冻结路径及SHA。该相关源**不在本批done**。

[check_728_joint_only.py](new-728-run/check_728_joint_only.py)仅标准库，不导入旧运输/发现程序；实际在session根成功运行一次，再将代码、固定输入、原报告和完整输出逐字节复制到相同相对布局。本次复制后没有再次运行。记录见[run-scope.json](run-scope.json)，[summary](new-728-run/summary.json)，[完整逐原子/逐配对输出](new-728-run/new-728-joint-only-check.json)。

其范围为65原子域/正质量、W/O、AB source→AE位置1/2的两个single与共同OO；247个非空标签组不同完整tuple配对、6344个去对角系数项、13个严格loss原子，精确值与原728报告完全相同。728个storedslack仅读取及判号，74零；未重建728行、全型dual或原优化最优性。247不是全客户共同置换数，6344不是完整策略IC通过数。

**原CLI0、原generic0、成熟69点0、外部solver0、LP0、网络0；当前新数学1次。** 已成熟69点的single/joint/loss与原727报告逐值绑定，直接复用[既有输出](../shared-matching-loss-and-adjacent-load-primary/new-loss-layers-adjacent-and-727.json)，没有再次枚举成熟217匹配或重跑9360/9008/1555回归。资料核对见[identity-and-binding-review.json](identity-and-binding-review.json)；源字节/AST/报告算术整理不是又一次数学运行。

## 依赖、证据边界和接续关系

[reuse-manifest.json](reuse-manifest.json)列明成熟数学、69点、B6运输实现与65点当前检查的具体复用角色。两族对原浮点输入为最终61点SHA27bc7b95…，不是早期initial61；本批不为复现旧float另抓输入或补造数组。所有原float报告都只有摘要/稀疏发现权，不能直接组成精确原始/对偶证书。

自由ε的solver success只指扩展优化成功；负最优ε提示零门槛共同运输数值不可行。精确非补全由指定共同OO有理负值承担，浮点报告没有被当成完整SPE、真实OPT或六人反例。两个成熟普遍引理及[第三阶段关系证据](relations.json)保留来源、实现、发现、精确有限检查与重复别名的不同角色；本批不改正式图，六人全目录half仍开放。

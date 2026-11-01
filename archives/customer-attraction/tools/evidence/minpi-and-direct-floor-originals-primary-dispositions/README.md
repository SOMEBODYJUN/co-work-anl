# MIN-PI与逐人floor原程序五源的首次primary处置

本批五source共22262B：5892B独立MIN-PI代码、2272B报告、5839B输入，5378Bdirect-floor代码与2881B报告。此前它们在PU5只是必要related完整保全；本次Root实际claim十二源中的本五项后，才逐源首次承担primary语义处置。不能把前次related阅读称为已经done，也不因当前数学已充分保存而重跑熟悉程序。

五原件已在`round4global-and-private-exit-primary/original/`正式保全。本批逐个核正常show清单、原冻结SHA256/Git blob内容指纹与已发布字节相同，**不再复制**22KB原件或23KB依赖。精确双冻结来源、发布原件路径和当前owner在[source-binding.json](source-binding.json)、[ownership-gate.json](ownership-gate.json)。Root原claim的完整12ID回执另原样保留，但本批receipt严格只有下列五项。

## 数学全文去向与准确duplicate

现三份正式正文均全文读，SHA与已发布PU5字节相同：

- [有限凹窗口的最小调和势增量保底反例](../../../state/反例/有限凹窗口的最小调和势增量保底反例--反例.md)：全部15748单位客户、25正类型、43有序动作、258含self比较的输入/原审计合同、P0…P4全部极大者及窗口范围、OPT与纯额外背景界。
- [新私有花瓣的全历史退出与逐人门槛正规形](../../../state/定理/新私有花瓣的全历史退出与逐人门槛正规形--定理.md)：固定原m/OPT的前缀floor、fresh-petal及最深坏点归约、后来银行反证、direct-floor单锥15支持的准确范围。
- [真实遗漏查询的自由取消覆盖与全价格分离](../../../state/候选/真实遗漏查询的自由取消覆盖与全价格分离--候选.md)：同一σ整行IC/COVER/PRICE/ROW-MASS，说明此处两个辅助floor/MIN-PI失败及数值阴性均不决定该共同付款候选。

五源的数学内容/实现/数据均已有明确载体，本批作五项`duplicate`处置，保留现正式数学对象与既有原件；不是把程序当同一个新定理再造一页。逐段差分见[duplicate-coverage.json](duplicate-coverage.json)。本批新建的仅是准确来源绑定、代码控制流/字段覆盖说明及首次primary receipts，没有新增数学命题或修改PU5正文。

## MIN-PI：原码实际读什么、算什么

5892B代码只导入标准库，顶层读取相邻`../parent/min_increment_counterexample.json`。求值依赖仅`integer_weights`和`strategy`（含声明terminal_counts）；不读取输入的旧430客户数值、HiGHS状态/objective或verified_counterexample作为证明依据。正整数重数按不同单位客户位置展开，从动作/历史自身推出m3、k6，并断言全部43有序历史、键无重复、合法动作、六覆盖互异。`isinstance(weight,int)`并非排bool的通用schema，但本冻结输入的25个实际重数均为JSON整数，未利用这一宽接口。

`completion`沿改变后的完整有序历史递归查同一动作表，`unit_scores`逐个单位客户求负载。三名玩家收益用尺度6；P0…P4及三竞争槽额外查询用尺度12，所需负载分母分别不超过3与4，均整除。辅助函数对部分未占用标签会有数值，但真实IC只查询当前已选动作，不把未出现标签当作真实玩家。

原码遍历43×6=258项含self比较；全部n=0…4、六坐标总和n的计数profile数1/6/21/56/126，共210项。它保存每层**全部**最大者，区别于5839B父输入只保存一个最大计数代表。原报告完整保非零层极大者2/5/2/1个、增量(6013,8249/2,3709,3709)、根3481、最小差228；8249/2是第二项单值。

实际(0,3,4)收益(3481,3709,3481)、W10671、Φ27237/2，OPT3=12546；P3=27693/2，actual势少228。MIN-PI已被该完整证书否定，**只**认证所需有限P0…P4窗口的非增增量。没有P5以后数据，不反驳额外假设全k凹的条件命题。三槽纯静态背景的最优capθ4=6283/2，由(1,0,0,1,0,1)达到，仅给真正混合安全值v4≤θ4<根；没有求精确v4，故该例不否EI。2W−OPT=8796>0，不否half。

程序无main guard：执行或import都会读输入、枚举、断言，再覆盖相邻`min_pi_independent_audit.json`并打印完整answer。本批只读源码和原报告，**没有import、runpy或CLI**。原2272B报告及3013B审查写“passed”属于原内部审查事件；本次没有新增绑定该SHA的执行记录，不把report.status或输入中Optimal当成当前run。原审查明确先按root陈述核对象，再读integer_weights/strategy，未读发现器；本次知情语义复核不是新盲审/外审。

## direct-floor：单个旧完整策略锥的浮点诊断

5378B代码无main guard，顶层导入NumPy/SciPy、读取`evidence/certificates/customer_attraction/prefix_balance_failure.json`，构造固定策略IC锥并调用HiGHS。REPO由原脚本目录向上六层恢复，必须保原相对布局；不能把孤立脚本import成“只取得函数”。该依赖是纯策略表、不是客户实例：terminal_counts=(0,1,3,0,0,0)，259有序动作。当前本批另实际完整读该23093B已发布依赖并绑定SHA98ce95…，未复制、不调用其中策略计算新数学值。

策略表推m4、k6；目标固定合法历史h=(1,)，余三人，但分母仍用**原总m4**，测试2m=8。63个非空兴趣type可变、保259×5=1295非self完整历史IC；每个偏离都沿改变后的原策略完成。比较支持为全部15个四标签子集，优化`2m*u_target−coverage(support)`，归一target收益1，非负type质量。覆盖最优可以补到min(m,k)个不同标签，故该固定m/k下这些支持足以评价每个提案点的OPT，不是只测一个比较元组。

若浮点目标小于−1e−8，源码才进入正点分支：以分母上限10^8恢复每个坐标的Fraction，精确核非负、target归一及全部IC；重算全部支持的OPT并核严格违反，统一公分母/gcd整数化，再对全部历史找最深低节点。输出会含整数客户、整策略、目标/原actual路径、W、2W−OPT和all_latest_low_nodes。这是**条件控制流**，当前2881B报告exact_positive_witness=false，没有执行到的正点文件、实例或失败反例不能凭代码存在而生成。

原2881B保存15个浮点gap，最大约−1.038461538461539，对应支持(2,3,4,5)；不含有理最优对偶。它只说该一锥/一目标节点未找到分离，不能认证固定锥精确最优，更不能证明全部策略或一般FLOOR。源码输出的report摘要排掉comparisons_tested后再打印best_numerical_gap，与MIN-PI打印完整报告的行为不同。

同名round3/shared/diagnose_direct_floor.py是另一个3217B、三人root、单比较支持的程序；其原单次成功与713B报告已有[独立正式资源](../../../state/计算/固定六主题根收益下界的单锥诊断与精确复现--计算.md)，不能借作本5378B/m4前缀程序的运行。一般OPT/(2m)逐人floor后来已被银行m≥5否定，half仍成立；现正式花瓣对象已完整更新此状态，本批不另授银行发现或新half结果。

## 本次自查与接续

本五源2py/3JSON全部全文；必要3013B原审查、23093B策略依赖与七份相关正式数学也全文实际读，详[comparison-and-dependency-bindings.json](comparison-and-dependency-bindings.json)。字节绑定、JSON语法/结构和owner/link检查不执行收益、IC、profile、LP或SPE代码；数学入口、原CLI、原import和新算术checker均0。

五source首次primary只处理这五项；raw claim另外七项由Root分别安排。现有24份PU5比较清单不自动当成本worker又读过24份，本批只列自己实际阅读。关系说明见[relation-review.json](relation-review.json)，仍是数学语义关系而非第三阶段建图。发布/完成回执由Root串行操作，本stage本身不宣称当前已checkpoint或done。

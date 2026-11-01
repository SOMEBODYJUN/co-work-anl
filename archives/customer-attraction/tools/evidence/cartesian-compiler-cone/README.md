# 固定笛卡尔编译种子的客户锥

[自足程序对象](../../../state/程序/三人笛卡尔编译菜单的固定种子客户锥--程序.md)保存21列108行的完整语义、两种客户权、全部报告字段，以及有理有限编译仍缺的义务。

两个主源：[3302B源码](original/cartesian_cone.py)，ID `efa605cb5b3bb7506f54`；[3498B原报告](original/cartesian_compiler_cone_k4.json)，ID `fc3fb90ca9e58f0da046`。原报告有12个顶层字段，seed有18字段。源码及报告的SHA256、blob、双冻结提交和实际原路径见[source-manifest.json](source-manifest.json)。六份全部读过的原始材料共27732B；另外四源保存在各自包，不重复登记处置。

## 实际依赖与复现合同

原源码急切导入[cartesian_limit.py](../cartesian-limit-program/original/cartesian_limit.py)，但不调用它的analyze或main。实际输入是[cartesian_convexification_k4.json](../cartesian-finite-convexification/original/cartesian_convexification_k4.json)的analysis；sample/drop不用。两份依赖的精确SHA和本次运行前后指纹都保存，避免同名替换。

main没有参数解析，直接覆盖同目录compiler报告。新复现应先新建一个隔离目录，在其中建runtime和replay子目录，把未改源码、依赖和输入复制至runtime，**不要预置输出报告**。再把[原观测脚本](run_original_once.py)放在该隔离目录，使用安装NumPy/SciPy的Python执行。脚本拒绝已有输出，利用runpy执行一次原main，并用sys.setprofile被动观察返回；它不是另写数学模型。这里说明如何复现，不是在本包封装后再运行一次。

## 唯一新增原事件

[execution.json](replay/execution.json)记录原main1次、cone1次、linprog1次、limit.main/analyze各0次、finite0次；Python3.12.14、NumPy2.3.5、SciPy1.17.0，assert启用。耗时2.995744747997378秒包括被动观测。退出0、stderr为空，输入三源前后SHA一致；外层工具观察另见[process-observation.json](replay/process-observation.json)。

[capture.json](replay/capture.json)完整保存108×21原矩阵、目标/等式/边界、18所需三元组顺序、16末回复、64组原P与V以及OptimizeResult。求解器自身返回status0、28迭代、最小ineqlin残量0；并非独立有理复验。[本次输出](replay/cartesian_compiler_cone_k4.json)与历史3498B报告逐字节同，[stdout](replay/stdout.txt)为443B、[stderr](replay/stderr.txt)为空。

原目标是正的 `0.08351636654282657`；根裕量 `5.551115123125783e-17` 不作严格有理证书。原报告没有有限K、单位客户恢复或完整策略。本包没有运行相邻数值筛选、完整有限SPE编译、旧72点四个精确LP，也没有独立恢复这21列点的有理可行性或最优性。

## 共享精确证据与差异

完整[三人菜单定理](../../../state/定理/三人笛卡尔可信菜单与根门槛凸化极限--定理.md)给出真实phi、g及G_K/K极限、严格根裕量的充分编译条件；它原来记录本108行尚未重放，当前新增事件不倒写旧历史。程序phi/g是保守上界，t是固定查询的下界；客户变动后不必等于真实极值。

[旧72客户精确包](../security-cartesian-and-disjoint-primary/README.md)的四小LP及两副本SPE不重复。相邻[字面数据审查](../cartesian-finite-convexification/reported-data-audit.json)和[其事件](../cartesian-finite-convexification/reported-data-execution.json)是唯一新增概率字面核，复用既有paytable，不新求LP或核IC。本包只读共享结果。保存概率的和与1有10⁻¹⁷量级差，旧点实际第二人盈余为−41/10¹⁷，不能静默归一后称为原点认证；这也不是新21列点的独立精确审计。

[review-record.json](review-record.json)区分全部主源/相关原件阅读、当前正文全文比较及此前已完整阅读的模型/银行结论复用。[check_package.py](check_package.py)只作SHA、JSON/AST、完整捕获结构、输入输出一致性、链接和两回执检查；[self-check.json](self-check.json)记录结果。它不导入研究程序，不求LP、不重建paytable、不重做有理数学。

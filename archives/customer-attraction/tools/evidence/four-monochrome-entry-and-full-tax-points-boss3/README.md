# 四份恒A入口/全终局税保存点：证据合同

主源为 R-ab183d14fb74403091d09db766b05f73 的 coupling 四检查点、6034B发现程序及150B workspace，共六份686743B。[source-manifest.json](source-manifest.json)保存每源稳定ID、两个完整冻结提交、原路径、size/SHA/blob及本包副本位置；`original/` 保全部原字节，不改写旧字段或旧程序。

正文为[恒A固定策略锥和四保存点](../../../state/计算/恒题完整策略锥的精确入口界与四份保存点--计算.md)及[原发现器检查点合同](../../../state/程序/入口与全终局税交替策略锥探针的检查点合同--程序.md)。前者含自足必要/充分条件及解析目标上界，后者区分原114条有限历史、固定target、精确恢复与浮点最优。关系仅收在[relationship-review.json](relationship-review.json)，不在本阶段自动改图。

## 真正执行

[audit_saved_points.py](audit_saved_points.py)是本轮新写的独立标准库实现；没有导入原程序、规范模块、NumPy/SciPy，没有LP、BI、RNG。输入仅本包四份冻结保存报告及source-manifest；workspace和原代码只核副本字节，未执行。代码拒JSON重复键、重复历史，检查所有完整有序键/合法动作，然后从每个原map递归求真实续局并精确比较规定与所有改选收益；另枚举全部静态比较支持、所有entry主题，并核逐题恒A充分条件。

一次成功事件见[execution-record.json](replay/execution-record.json)：UTC2026-11-02T14:20:13.561836+00:00、elapsed1.2885755730003439秒、returncode0、断言开启、stderr空。原入口/LP/BI/RNG均0次。新驱动9706B，SHA256 `9793246031776996228edc23b78166bfe23a82568e1aab38675b938bbd25c191`；stdout286B，SHA256 `81cd7c91ef844d6332847ed4d82782490d1d651d746735691eb8ebec1da5c5e6`。这不是原114轮发现器重放，也不声称盲审。

结果[exact-saved-point-review.json](replay/exact-saved-point-review.json)共四记录，保输入SHA、正质量、完整键及IC计数、全利润/目标、所有最优静态支持、逐题恒A条件以及原历史读取范围。全部6120节点和42322含自身真实IC通过，非自身36202；四份都实际全A，W=1。entry两份真最大分数1，全税两份真最大分数19/20、29/30，后者余量分别1/20、1/30。

[complete-ordered-IC-and-comparison-supports.json.gz](replay/complete-ordered-IC-and-comparison-supports.json.gz)保存全部6120条历史各自的规定利润、所有p个偏离利润及slack，并保存每图全部15或21静态比较支持。解压1023717B、SHA256 `b0f8b73a792ad0d0fdef0d8ac3cc9112b4ac0707547cfc534fe7eb94fac1edbe`。保留完整账使后续能逐条定位，不拿汇总PASS代替策略认证。

## 原报告全读与范围

四图动作都逐记录解析并与精确完整有序域比较：259/2801/259/2801；不是只读root或旧布尔值。四份history的24/19/24/47条全部字段也已读取，114条均记LP_success=true，其中106带精确score；entry5缺8,16，全税5缺8,9,16,17,32,40。这8条只能说旧有理恢复未被记为通过，原记录不说明具体失败条件。四个原elapsed约5.012/95.762/5.305/213.830秒保持历史身份，不能叫当前耗时。没有原argv/exit或全部逐轮输入，不断言19/47轮正常完成某一计划。

原固定target是进入LP前按旧masses选，candidate恢复后不重新最大化目标；本保存点恰为真最大由这次独立精确核及正文结构另证。原字段 `exact_O_minus_tau_over_W` 在entry模式仍是entry值，不能因同名错减税。

[dependency-and-comparison-reading.json](dependency-and-comparison-reading.json)区分新审计的四个实际输入与原程序才需的四份规范代码；规范代码从既有同SHA包全文读，没有重复保存字节、运行或新增done。其它正式对象仅作数学比较：[一般entry反例](../../../state/反例/实际终局额外查询的三人反例--反例.md)已否一般桥，[九客户税点](../../../state/计算/五人九客户终局税点的完整历史核验--计算.md)及[不交极大主题](../../../state/定理/不交极大主题锐福利界--定理.md)保既有锐性族。旧成熟验证均不重复。

## 数学级别

正文新解析结论限固定完整形式策略σ_A：SPE iff 对每题T有mμ(T\A)≤μ(A\T)，充分性显式保每客户所有旧主题负载h_x。由此该锥entry≤1、全税分数≤1−1/[m(m+1)]；四保存点恰达相应上界。它是证明加精确可行点的条件最优结论，不是旧HiGHS数值结果自动升级。

一般entry命题已有另一个非恒A完整SPE反例；一般全税及当前六人half均未由本包解决。所有空题、重复标签、离轨历史、弱平局与W0边界按正文处理。六源逐件receipt在stage的 `receipts.json`，关联依赖不追加done。

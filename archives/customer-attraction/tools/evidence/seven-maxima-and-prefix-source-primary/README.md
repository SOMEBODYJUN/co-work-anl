# 七极大、前缀源切面与关联阈值的九主源证据

本包归属 Boss3 第二阶段清洗。九份原件共28946B，全部完整实读，两个冻结版本的来源、blob、字节数和SHA见 [source-manifest.json](source-manifest.json)。source-root 保留原路径和原字节；主源有数学/程序错误时在正式正文解释，不改历史原件。

## 四个正式对象

- [七极大四族预算](../../../state/障碍/七极大六人四族预算的精确负余量与漏税纠错--障碍.md)：补足原浮点程序未做的精确原始/对偶证明，130放宽列上的最优统一余量严格负。仅指定模板障碍。
- [七列前缀见证](../../../state/障碍/单早期包含的七列Farkas见证与源切面实现边界--障碍.md)：保16/18行增量、原字面代码、真实公式修正和全客户数N容量弱化。修正后对偶由解析单调性延续，不冒充原输出。
- [149比50关联阈值](../../../state/推论/六人关联阈值149比50的核心外保底与原审计--推论.md)：核心外残余预算与完整历史倒推；保加性定量界及原审计范围，半覆盖条件已被后续9/2范围推广。
- [混合私有质量条件](../../../state/推论/七极大混合私有质量的定量半覆盖充分证书--推论.md)：正确私有后缀系数1/12、最优遗漏argmin及五类精确余项。

上列相对链接以证据目录位置为准；实际路径核验另存静态自查，不用字段校验替代数学判断。

## 真正新增的两次数学执行

|执行|实际范围|次数|
|---|---|---:|
|four-family-exact-001|从原稿五个活跃列解两组有理线性方程，核全部130列与五点对偶；标准库|1|
|prefix-original-001|未改2875B强版原程序的18个字面行和七列Fraction见证|1|

四族核的0.00485199700051453秒是保存结果里的**核内计时**；exit0、stdout/stderr指纹和实跑源码见 [执行绑定](four-family-exact-001/execution-binding.json)。完整130列结果为 [root10-four-family-exact.json](four-family-exact-001/root10-four-family-exact.json)，实跑源码 [root10_exact_four_family.py](four-family-exact-001/root10_exact_four_family.py) 保留当时scratch输入定位，不将路径适配倒填该次运行。

强版原程序的外部进程计时0.15462851199845318秒、exit0、stdout272B/stderr0，见 [execution.json](prefix-original-001/execution.json) 与 [原stdout](prefix-original-001/stdout.txt)。其中source-4/source-3数值是**错误转写版本的字面值**；正确真行的对偶有效性来自正式正文中逐点增大行值的证明。没有执行一个“偷偷改过的原程序”。

原浮点LP、弱版2667B程序、关联阈值2192B程序、混合私有2697B程序、任何LP/发现扫描/完整SPE枚举、成熟数学重放均为0。完整账见 [execution-accounting.json](execution-accounting.json)。

## 不覆盖历史记录的复现

在本目录下运行便携四族核：

~~~sh
python -I -B verify_four_family.py four-family-new-result.json
~~~

若输出已存在，程序拒绝覆盖。便携版本仅改原件清单路径、包内相对路径和新输出位置；两个数学函数及从私有系数到全部残差断言的核体保持相同，见 [portable-adaptation.json](portable-adaptation.json)。本批便携版本只静态比较，运行0次。

强版原件没有文件写副作用，可在本目录下运行：

~~~sh
python -I -B source-root/research/workspaces/customer-attraction/R-c499e3814bbe4743b298e230b37ddca1/notes/r2_q1_prefix_source_all_obstruction.py
~~~

该命令重现的是原字面18行，不是更正公式或保留精确K坐标的更强行族。需新实验时应另立文件和执行事件，不能覆盖本次原输出。

## 阅读、比较和第三阶段关系

[dependency-and-comparison-reading.json](dependency-and-comparison-reading.json)分别记录完整阅读与定向段落比较，不把SHA核同说成全文阅读。[relation-evidence.json](relation-evidence.json)写明关系、逐式证据和限制；不直接导入旧图。九源逐件处置见 [receipts.json](receipts.json)，每件含原阅读、成熟比较、独有内容去向及理由。

这些正文区分完整证明、条件结论与方法障碍。它们没有宣称六人half已解决；清洗完成不要求将开放数学问题解完。

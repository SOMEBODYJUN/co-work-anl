# R291 四主题复制税输入域勘误

本次A8修复具体矛盾：旧《R286链式重查询与R291复制税边界》§5把“四主题只取单/双兴趣、二值重数、32767”写在一起，后续《复制税的固定策略锥与全SPE最小税递推》留下疑点。原程序与JSON一致，错误在清洗措辞。两篇正文直接更正，原程序、JSON、日志、旧比较笔记和done记录不改。

这是Boss3已done来源的针对性修复：**新增来源完成数0、claim/done0、Git写入0**。未重跑32767/59048/其它穷尽扫描，未执行SPE递推、LP、BI、随机。新checker只作AST/域计数、保存输出一致性、指纹和正文资产检查，不导入或调用原程序。

## 1. 准确输入域和递推

4807B R291源码全文读取，`types=tuple(product((0,1),repeat=topics))[1:]` 仅排全零兴趣型，未筛兴趣大小。四主题有4单型、6双型、4三型、1四型，共15型。main调 `run_case(6,4,1)`，每型重数0/1、排全零，故2^15−1=32767。若另造10单/双型二值扫描才是1023，该独立分支不在原main。

三主题main取m=2…6、七型重数0…2，各2186输入。六份JSON全部字段和stdout完整实读，均无正gap、最大gap恰0；具体scale/最大计数态/根终局数在两篇修正正文及domain-and-record-check.json。源码largest_gap从None取真实最大值，不把负值夹0，与后来30个浮点政策锥报告不同。

每计数态保全部可由完整子SPE实现的终局q及其最小剩余有序税。当前收益只依q，各未选有序孩子可分别拼接最低当前收益的子SPE，故max-min阈值保全部历史依赖平局；计数缓存不要求统一Markov策略。最小税只沿遵从孩子累加，不能只由终局计数决定。完整归纳见[递推正文](../../../state/程序/复制税的固定策略锥与全SPE最小税递推--程序.md)，本次不重跑它。

源码Python任意精度整数，scale=lcm(1,…,m)，b+剩余r≤m使所用分母整除scale。三主题客户至多14、四主题至多15，scale≤60；粗界scale·C≤scale·m·N≤5400，原最小税哨兵10^100在本域安全，不据此认证无界重数实现。允许单实例空主题和重复行动；全零客户向量被扫描跳过，该模型边界目标均0。

## 2. 三域、两目标与运行状态

|来源|兴趣域/重数|输入数|目标与结果|现存运行证据|
|---|---|---:|---|---|
|R291 / exhaust_copy_tax_three_topics|全部15非空型，0/1|32767|最大调和势≤实际W+有序复制税；无正gap；scale60、最大210计数态/84根终局|stdout与JSON完整相同、stderr空；旧README记exit0，既有程序receipt记实际运行|
|R286 / counterexample_search_m6|10单/双型，0/1/2|59048|最坏SPE福利/OPT，来源报告8/11、零half违例|旧尝试ModuleNotFoundError，不借R291成功升级|
|R-ad571 / exhaustive_k4_binary|全部15非空型，0/1|32767|最坏SPE福利/OPT，completed报告6/7、零half违例、一个最坏点规范核验|JSON script_sha256匹配驱动；成熟范围复用，本次不重扫或重核最坏点|

R291类型顺序为二进制tuple字典序，另两来源重数记录为mask1…15；抽象域相同不代表权重坐标同序。两个32767不是同一程序/目标/JSON/运行。210与84也是共同计数几何界，不能据同数混并算法。R286另有三主题七型0…3、16383输入、9/11的福利报告，亦不同于R291的2186。

## 3. 历史执行和保存的边界

现存R291 stdout完整解析为保存2366B JSON，同六条结果的所有域/scale/状态/根终局/gap字段相同，stderr零字节。旧README记exit0；既有done程序receipt的source_sha256匹配4807B冻结源码，并记完整实读、编译和实际运行。这里只确认**现存历史证据支持该域和输出**；没有另存独立argv、墙钟时间、逐实例中间日志或进程内嵌codeSHA，不猜这些信息，不称本次新独立复现。

旧evidence的comparison-notes.md也含“单/双兴趣”误词，作为历史生成笔记原样保在saved-records；本勘误和正文覆盖其技术解释，不改旧证据。原R291工作区README写“四主题全部0/1兴趣类型”，与源码/JSON相符。

[成熟四主题福利扫描](../../../state/计算/四主题六人二值客户全集的精确递推与保存最坏点--计算.md)已说明R-ad571 helper、规范最坏点和缺失运行元数据；本次全文比较该正文及2312B驱动/1161B报告，不重复审核16033B helper及32767扫描。一般复制税候选仍未证、三人逐枝接口反例仍有效，域更正不提高一般六人结论。

## 4. 文件、自查和准确变更范围

- `before/archives/...` 保两正文修前完整字节，工作目录formal-before-after.json保前后指纹，formal-changes.patch保精确diff。
- `frozen-source-root/<原路径>` 保六件已done原件，共15591B；source-manifest.json列精确ID、双commit/path/blob、SHA、现路径。R291两件ID为4567df5291710117cab5、6844b47df933ffb8a9a4，均不是新增主源。
- `saved-records/` 保10件历史日志/旧说明/两个既有receipt/原工作区README；saved-record-manifest.json列修复前路径、字节、SHA。
- `domain-and-record-check.json` 保一次静态检查：AST types/main、域公式、全部六JSON结果、stdout相等、stderr空、原字节、两篇YAML/链接。未调用run_case、原helper或任何游戏搜索。

正式改动仅两篇约定页面：[R286/R291审查](../../../state/审查/R286链式重查询与R291复制税边界--审查.md)的§5及frontmatter缩进/summary；[递推程序](../../../state/程序/复制税的固定策略锥与全SPE最小税递推--程序.md)的比较疑点段。其余数学段、原有限报告及日志保留。工作目录为cleanup/workspaces/Boss3/resume-20261102/a8。

# 复制遗漏池的严格末两人偏离

[自足障碍正文](../../../state/障碍/复制遗漏客户池的末两人严格偏离障碍--障碍.md)证明：对整数k≥1、q≥2，目录A/B/P及q组T/D/E的指定路径P^k AAB不能由任何完整纯SPE实现。D_j偏离后，任意末位BR都是另一池T_h，偏离者恒得7>5；不排其它路径或一般构造。

|原件|主源ID|字节|SHA256|
|---|---|---:|---|
|[replicated_omissions_failure.md](original/replicated_omissions_failure.md)|e828f5d0e87a440be274|1697|2cdd306878f958435688f8fef3c27b398f53f0c98b076aa605cf2edafc93ea9e|
|[replicated_k17_direct_audit.json](original/replicated_k17_direct_audit.json)|90e1e51f8ab1cd80dd62|1412|7809033bee8c3b787c86685b3039fa72ddfc9ea9f9493d6345d84509cdd8346a|

两个冻结提交同字节，各有逐源回执。[source-manifest.json](source-manifest.json)保blob/路径/模式和实际比较。原JSON有13顶层字段、54行动值及16个全BR；k17为20玩家、54主题、203客户，形式W101/OPT203的缺口1不是真SPE反例。原生成入口、argv与执行记录未识别，不把相邻all_k程序算作生产者。

## 新有限事件

[audit_direct.py](audit_direct.py)仅标准库，从兴趣定义展开203名单位客户，以Fraction核偏离后的54个末位行动及16个BR下的当前收益，再核提出路径的20位份额及一个盖全203客户的20主题静态比较组合。它没有导入作者程序、运行DP/LP或展开整个完整SPE树。

- [direct-audit.json](direct-audit.json)：完整单位客户清单、54条双角色收益、16BR、形式覆盖/OPT证书、全部精度与局限。
- [execution.json](execution.json)、[stdout](stdout.txt)、[stderr](stderr.txt)：一次新独立事件，exit0、stderr空，外层约0.0452秒；0原入口、0DP、0LP、0长扫描。
- [check_package.py](check_package.py)、[self-check.json](self-check.json)：原字节、保存结果结构、AST/JSON、实链接与两份回执自查，不重复数学运行。

正常复用现有报告即可；若后续输入改变，接口为 `python -B audit_direct.py --source original/replicated_k17_direct_audit.json --output NEW.json`，输出须不存在。这会产生新事件，本轮没有为了封包再次执行。

## 单池与复制池的不同真菜单

相关[all_k原稿](../credible-padding-theory/original/all_k_padding.md)10930B及[程序](../credible-padding-program/original/all_k_padding.py)4780B均全文读。它们固定单池六标签，在D之后可选同池E作为末位BR，将偏离者压到5；复制出另一池后，未拥挤T_h给末位6，同池E的5便不再最优。故本失败不反单池全k可信定理或真正安全值聚合。

一般k/q排除依正文解析表与严格偏离证明，有限k17核仅验证这份原表；无原完整策略认证、真实最差SPE福利、外审、新颖性或一般half声明。

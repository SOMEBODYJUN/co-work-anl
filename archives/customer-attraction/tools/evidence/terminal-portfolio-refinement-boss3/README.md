# 共享末回复组合查询的四源清洗证据

正式正文为[发现与有限精化程序](../../../state/程序/共享末回复组合查询的发现与有限精化程序--程序.md)和[八切面有理点](../../../state/计算/八条末回复查询切面的有理精化点--计算.md)。本包只完成这四个源版本；旁读旧图、13Q局部审查、pending包及其它点不自动done。

## 原字节与独有内容

`source-manifest.json` 保双冻结commit、原路径/blob、字节数、SHA及当前保留路径。原文件全部未改。

| 源ID | 文件 | 字节 | 本次准确去向 |
|---|---|---:|---|
|b4dd5c92d5e5f049779e|refine_terminal_portfolio.py|3600|默认5075+8=5083及容量5083+29=5112的分支、有限发现/有理恢复/核验合同|
|f47ef34b903234e3eb35|terminal_portfolio_cuts.py|5223|共同真末回复先合再min、同价人数压缩、13/16查询映射、1905仿射读出、参数LP|
|a2933368a00aed4a0c18|terminal_portfolio_refinement_cuts.json|2838|原8条完整有理参数，全mu13、单正actual A6、无beta即0|
|7f3e20e49ad37edc1d64|terminal_portfolio_refinement_exact.json|815964|全部12字段/1905记录、169正坐标、有限精确可行及字面交叠障碍|

所有冻结8cut的参数、零项和次序已全文读；没有以文件名portfolio推断本批实际用了多个正Q或容量。完整点保含零坐标的原1905记录，不只存正支持。

## 唯一原默认核验事件

`run_original_once.py` 从现共享 `combined-branch-master-program/source-manifest.json` 物化冻结依赖，并按原repo相对路径放入本四primary；根work.py仅写路径定位注释，不导入或执行控制器。原命令为 `python3 -B <原层级>/refine_terminal_portfolio.py --verify`，assert开启。代码自动加四个基础旗标；没有加--capacity，也没有启动发现器。

实际38.681秒、exit0、stderr空。`runs/original.stdout` 为原146B字典repr，记录5083行/base5075/cut8/min0/W；不是JSON文件。`runs/original-execution.json` 保UTC开始、真实argv/cwd/耗时、全部可用输入路由/源SHA及前后不变结论。

原执行记录的输入清单有51条角色记录，实际对应49个唯一原路径：portfolio源码与8cut JSON此前也在共享依赖中，本次primary以同SHA覆盖相同原路径。`materialization-identity.json` 将这点明确区分；51不是51个不同文件，更不是加载追踪。所有49个实际文件前后字节不变，原运行没有写trace、cuts或新point。

未来主动重做一个新事件可运行：

```sh
python3 archives/customer-attraction/tools/evidence/terminal-portfolio-refinement-boss3/run_original_once.py /absolute/repository /absolute/new-empty-runtime
```

新runtime必须尚不存在。脚本会生成新的执行记录，不能冒充本包已存事件。普通发现会写旧目录同名前缀文件，本批没有执行这种模式。完整共享原件路由及当前比较输入SHA见 `dependency-manifest.json`。

## 知情独立的完整记录与八行检查

`audit_point_and_cuts.py` 复用已读1905结构审计，并针对当前源身份/12字段改写，新增字面隐藏位八向量构造。该入口恰执行一次，约0.472秒、exit0、观察到stderr空，真实参数与已执行脚本SHA在 `runs/independent-execution.json`。完整机器可读结果为 `independent-audit.json`，stdout另存 `runs/independent.stdout`。

本次独立检查包括全部1905权非负、16hist及旧/新索引、194组3显式状态和隐含00、1306辅助交叠及2612上界、O/W/六实际利润、六分轨道CAP/十二旧B-C价/三十六新R-Z价，共54局部数学行。它不导入原图生成器、不做LP，也不宣称核全部5083矩阵的第二实现。

八条行从实际六索引对及字面2^n后继位重构，没有调用原count-compressed psi计算独立向量。仅为逐坐标对照，通过AST提取原qvec/share/psi/row及原groups纯函数，未执行这些文件顶层或CLI。八条×1905=15240系数全等；将每个原mu13末尾补三零后，另15240系数也全等。冻结8条当前余量3零5正，所有精确分数保报告。

这验证13前缀的真实读取兼容，不代表非零16Q全域数值独审。一般第三索引平均的合法性由正文中真实IC平均及qvec公式证明；旧2493B局部独审明确只13Q，不倒填它已审16Q或整图。

## 当前点、其它点与字面交叠边界

当前169正列为1K/10hist/87joint/71overlap。完整辅助交叠有168项低于Fréchet下界；原图只要求非负及上界，仍准确满足其有限原行。报告保全部168项和一条完整短见证：列992在hist117上，两R组边缘均等该hist正质量，原overlap却0，不能作为同客户真实交叠。程序页/数据页给全group及分数，不将该局部实现障碍泛化为所有点或六人SPE反例。

与旧5075/5108全部非weight描述符、K和16hist质量相同，但分别111/110个隐藏权坐标不同。把本八行作用于旧5075，8条全负；作用于旧5108，6负2正；当前5083为3零5正。比较只重算8行及完整坐标身份，不重建其它两图的全矩阵，也不继承它们所有额外关系。

本批还全文只读父方已认领的pending JSON，核其3portfolio仍是mu13单正查询但有beta_last，绑定另5277输入；另2requery为对角重复Ci/Cj。父方另批核该包，本包不重复求值、不替它done、不把5记录叫5独立约束。

源代码/原有理点/完整原核验/独立局部实现分别保身份。容量5112、后续5277/5692以及完整SPE均另有合同，本包没有运行它们或升级一般六人half。关系已在正文解释，三级超图留阶段三逐边整理。

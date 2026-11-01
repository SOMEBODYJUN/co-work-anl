# 三源共同容量投影及旧702联合程序的四源证据

本包只处置四个正式主源。正文为[三源完整表与精确复核](../../../state/计算/实际末主题三源共同容量投影的完整表与精确复核--计算.md)和[旧702投影/条件lift程序](../../../state/程序/旧七百零二行与实际末主题分支的联合松弛程序--程序.md)。原源码、JSON和新运行产物各自保身份，相关旁读不自动done。

## 四份冻结全文

`source-manifest.json` 保存两冻结提交、原路径/blob、字节数、SHA及持久位置；原字节不修复或覆盖。

| 源ID | 原件 | 字节 |
|---|---|---:|
|519adddb8a5e5058acc5|original/519adddb8a5e5058acc5/early_B_projection_certificate.json|138135|
|b724ae73630ef1019a70|original/b724ae73630ef1019a70/early_B_projections.py|3799|
|6810944411e73238bda4|original/6810944411e73238bda4/combine_old702.py|1543|
|bb302c2f87c0e23a435a|original/bb302c2f87c0e23a435a/old702_plus_B_families.py|3282|

完整原JSON共三个448表，1344格均逐字段和Fraction比对。其4个根字段、每行7字段和全部域标志已核，不只核header或表格长度。源程序仅标准库，从三组固定正整数权及全域max生成必要行，再求指定旧点负值。

## 一次原export及一次知情独立重构

`run_original_once.py` 按原repo相对路径复制未改源码与共享5108点到一个新空clone外目录，保留原 `__file__.parents[5]` 定位。实际命令 `python3 -I -B <原层级>/early_B_projections.py --export`，未复制原证书到将写目标，避免FileExistsError。运行约3.369秒、exit0、stderr空。新138135B完整证书保存为 `runs/generated-certificate.json`，与冻结证书逐字节相同，SHA为b68b72b030fac2922f745adaabd34b627ae2c8ff70ec3e645f276a942f5a7959。

`runs/original-execution.json` 保真实argv、cwd、UTC时间、耗时、源码/输入前后SHA及新产物SHA；`original.stdout` 是2048B无table摘要，`original.stderr` 为真实空输出。不是用摘要重构或伪装成原完整JSON。

`review_tables.py` 不导入原投影器，从S/Z/V未消同索引交集式重算三源：87808完整隐藏态、150528可行交集态、1344表格及全部表顺序一致。它完整读本次指定输入的16个hist及1K，核非负、直方图总数/d、O、W，保8个正边缘的每项贡献。三个负值逐Fraction等冻结记录，ell端点与全域max全同。实际独立入口恰一次，约3.293秒、exit0；`runs/independent.stdout` 保完整报告，`independent-execution.json` 单独记真实执行范围。它不核余1888隐藏列或5108矩阵，不称全图第二实现。

本批原数学入口1次、知情独立系数入口1次，两个浮点发现主程序0次、LP0次、完整SPE搜索0次。后续静态自查不重复这些入口。

## 旧输入、共享依赖及不同程序接口

`dependency-manifest.json` 列实际持久位置及SHA。指定816453B旧5108点为源5e6ada29cce2eeda7f9e，SHA d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8，复用父报告原件，不为本批另复制整份大点。它不是旧1033点、旧5277点或新5692四菜单点。

旧702完整树复用 `combined-branch-master-program/source-manifest.json` 的已持久原件；当前全文比较直接接口 `new_reply_budget.py`、`joint_system.py` 与旧 `tail3_B_projection.py`。相关 `max_branch_lp.py` 原件以精确字节放 `related/`，其源e3d515121a7c7779a302由并行批另处置；本批不替它done。

`combine_old702.py` 调旧无K actual4的table/204，不调新三K表，矩阵703×449。`old702_plus_B_families.py` 默认actual1/2/3/4四族，完整448边缘、同一K、端点条件质量，静态978不等式/1793等号/54209变量；没有最大根身份或所有菜单Yi价。历史浮点值仅来自全文已读原research2 README，本包没有假造新LP运行或精确最优证书。

`review_interfaces.py` 只读AST、旧702接口及提取的qf/menus/branch_rows三个纯函数，以4次代表性调用核默认行名长度/CAP客户项及静态尺寸。`runs/interfaces.stdout` 明示没有执行历史main、旧702生成器或LP。它不是全矩阵重建或完整数学域复核。

原lift函数接受自定义sources却未检查真节点范围。正文另给两主题7客户完整SPE：前五全历史选A，末位全A前缀平局选B、其他选A；若错误加入actual第五源，菜单M=−6/5。该反例仅排原默认域之外的行族，默认前四源不受影响；另一内部清洗者已独立核此解析证明，没有另跑LP。

## 可主动复现的入口

如需一次新的原执行事件，在保存后的仓库中运行（新runtime路径必须尚不存在）：

```sh
python3 archives/customer-attraction/tools/evidence/early-b-projection-and-old702-boss3/run_original_once.py /absolute/new-empty-runtime
```

这会产生新的真实记录，不应冒充本包已保存的原事件。独立重构可另显式运行 `review_tables.py`；程序默认以该包在结果仓库内的层级找共享输入。两浮点程序若要复现，需完整旧原相对目录及NumPy/SciPy；本批原件归档路径不能直接当作旧目录层级，且自定义源须限制到已证真节点域。

本次阶段二关系判断已在正文解释：原表的实现/完整域核验、旧点分离、primitive族解析蕴含投影，以及同K但不同隐藏域的比较。没有从浮点发现建立六人half或策略反例边；三级超图仍待阶段三逐条审边。

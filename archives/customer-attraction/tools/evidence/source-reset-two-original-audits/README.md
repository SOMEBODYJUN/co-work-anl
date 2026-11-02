# 完整行接口与双副本菜单的两原入口

正式对象：[完整行接口与双副本可信菜单的原始精确审计](../../../state/程序/完整行接口与双副本可信菜单的原始精确审计--程序.md)。本目录保留四件主来源14990B、一件必要运行依赖9623B，以及2026-11-02对两个未改原入口各恰一次的固定重放。冻结报告与新输出分开放置，未覆盖旧原件。

## 原字节和读取身份

[source-manifest.json](source-manifest.json)逐件列冻结commit/path/blob/size/SHA256及保留路径；四件都完整实读，不以程序名或PASS字符串代替语义阅读。

|主来源ID|原件|字节|语义去向|
|---|---|---:|---|
|9c53330bd5e32c6c75d0|[interface_audit.json](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/interface_audit.json)|3199|scalar节全部两记录/12含自身IC/金融字段|
|38110a735f0a9464db66|[interface_audit.py](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/interface_audit.py)|2864|scalar节真实输入、完整策略、两点计算与stdout合同|
|0e485eaf7830aa8fc02b|[product_independent_audit.json](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/product_independent_audit.json)|3036|product节全部19字段、4/16全表和11可信叶、原policy结果|
|672d37fd305738d1844b|[product_independent_audit.py](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/source_reset/product_independent_audit.py)|5891|product节独立重建、唯一外部依赖、全树验证、文件/摘要合同|

唯一外部输入是[作者原完整策略证书](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_certificate.json)，源ID `bf80a9f01870df490225`。其[dependency-manifest](dependency-manifest.json)保持related-only，不为它写主来源done。全部instance/91条原policy/forced元数据已实读；[结构和范围记录](certificate-structure-and-scope.json)另保列表无重复、1/9/81完整有序节点、十名不同单位客户及强制BB元数据身份。

## 本次真正执行的事件

两份脚本和证书复制到clone外隔离目录，保持`source_reset`和`dynamic_matching`相邻结构。每个脚本用Python3.12.14 `-I -B`各运行一次，断言未被`-O`关闭；两次退出0、stderr0。无导入作者或规范求解器，无随机发现、LP/BI扫描。原来MD批的数学CLI运行0与本次两次新运行分开记。

|入口|完整结果及冻结等同性|stdout|
|---|---|---|
|interface|[新stdout](current-replay/interface_audit-stdout.json)3199B，逐字节同原interface报告|同一个完整3199B报告；两参数0/7同进程|
|product|[新生成文件](current-replay/product_independent_audit-generated.json)3036B，逐字节同原product报告|[新stdout](current-replay/product_independent_audit-stdout.json)706B，删除全部键名含rows字段的摘要|

[execution.json](current-replay/execution.json)保真实argv、cwd、时间、版本、输入/代码/输出SHA256；两份空stderr也保留。此记录只属于当前两个入口；父方另处理parent/path_menu的运行有各自不同报告和合同，不互借字段或计成同一次执行。

如需再次运行，先复制`original`中该工作区的`source_reset`和`dynamic_matching`到可写临时目录，保相邻结构，再执行所需原脚本；product会在脚本目录生成完整报告。不要在本证据原件目录执行它来覆盖冻结报告。

## 有限验证范围与复用关系

interface只计算t0、7；每参数3有序节点、6含自身/3非自身IC。scalar最优1与COORD最优(t+2)/2的普遍全t证明已在既有正式反例，不冒两个点为全参数运行。product只对该五客户双副本枚举4/16个末位BR叶，用总第二门槛3保11可信叶；原作者策略91节点、819含自身/728非自身比较。actual为CC AA BB、4/3/3、W=OPT10；BB BC CA是离轨低菜单叶。没有half或SM反例。

两个源码/报告的所有语义单元逐项列于[semantic-units.json](semantic-units.json)，与正式对象段落对应。全t金融族、任意背景恰两尾FILTER、三原审查范围、后加同质边界、后来银行Mfull反例等全文比较及SHA见[comparison-bindings.json](comparison-bindings.json)。既有对象准确的“当批未读代码/JSON”声明保持历史；本次补的是实际原件、必要完整表与一次原入口重放，不重做已有解析普遍证明。

[relation-review.json](relation-review.json)逐条区分有限检查、联合证据、读取范围扩展和后续状态边界；未写正式阶段三图，不把来源链接自动当推导。新对象两个锚点分别为`scalar-interface`、`product-credible-menu`。

## 交付检查的作用

[publication-check.py](publication-check.py)只检查冻结字节、JSON字段覆盖、91原表结构、完整/摘要输出身份、正文数据表抄录、收据和链接，不执行两个原入口或重新证明SPE。检查输出为[publication-check.json](publication-check.json)，不把字段通过当数学完成。正文、逐源收据及精确文件清单由父Boss串行审阅、checkpoint远端核验后再done；本目录不声明本地stage已经推送。

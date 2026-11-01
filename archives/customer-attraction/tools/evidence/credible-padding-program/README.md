# 独立吸收主题填充策略的精确有序历史审计程序

主源 `6f957bfb27488f5b01db`，4780B，两冻结提交同字节。完整数学、输入/异常、全部特殊转移和BI合同见[正式程序对象](../../../state/程序/独立吸收主题填充策略的精确有序历史审计程序--程序.md)。

[原件](original/all_k_padding.py)固定六主题八客户类型，参数k≥1、m=k+3；构造S/F状态的全部六行动边，再核该份完整策略的真实偏离。它不是随机探针、任意实例搜索器或所有策略枚举器。[规范依赖](dependencies/customer_attraction/__init__.py)四模块逐字保存；[来源清单](source-manifest.json)绑定唯一主源、四实际依赖及六相关源的原SHA。证书模块被导入，但原main没有调用certificate/verify_certificate。

唯一原k1入口见[包装器](replay_main.py)。包装器复制未改源码及四依赖至新目录、以runpy执行原main，用profile旁观main返回局部对象和调用次数；不替换函数或补调求解器。[执行记录](replay/execution.json)是同一事件的0.149796729秒原main区间/0.159819458秒含序列化区间；[进程记录](replay/process-capture.json)是启动Python至退出的0.215547208秒墙时，exit0。不是多个尝试或性能基准。

[新报告](replay/report.json)1418B与[k1冻结原件](../credible-padding-data/original/padding_k1.json)逐字相同；[stdout](replay/stdout.txt)784B保存同对象的紧凑JSON，[stderr](replay/stderr.txt)为空。[原DAG](replay/original-dag.json.gz)4315B解压29200B，231节点/99决策/594条边；S40/F191，决策S34/F65。[原BI缓存](replay/original-solver-cache.json)81658B保190计数终局集、64阈值、126收益向量和218终局条目。[原main局部值](replay/original-main-locals.json)与[捕获摘要](replay/capture-summary.json)都只是已有原对象的序列化，没有重算。

比较含每节点self，所以minimum_slack0不是存在非self平局的独立信息。k1是四人27客户点，P,A,A,B，W21/OPT27，税差−51/7。只对这一次运行认证当前代码/依赖；[k5](../credible-padding-data/original/padding_k5.json)与[k10](../credible-padding-data/original/padding_k10.json)仅完整阅读保留历史报告，不在本轮重跑。旧36客户13人packet有18675决策/112050比较，当前k10报告18669/112014；同27243总节点和同实际叶不能证明同一离轨策略。

[全k反族正文](../../../state/反例/独立主题饱和续局的全人数实际分数税反族--反例.md)给无界参数的解析归纳；[三个有限点](../../../state/计算/独立主题填充完整策略的三个有限审计点--计算.md)保原记录及另行标注的标量核。[复制遗漏池障碍](../../../state/障碍/复制遗漏客户池的末两人严格偏离障碍--障碍.md)是不同目录，不能用此生成器或S/F证明替它认证。税查询M不是真正安全值；本族2W−OPT=5k+10>0。

未来确需复现时，从本目录运行，run-dir必须尚不存在：

```sh
python3 -I -B replay_main.py --source original/all_k_padding.py --dependencies dependencies --run-dir /absolute/new/run-directory --k 1
```

原脚本自己的output存在检查不是原子独占；不建父目录。k变大可能耗费内存或触及递归深度，有限测试不替代全k证明。此包已执行一次，无需再跑阅读流程。

[阅读与数学判断](review-record.json)、[全仓比较](comparison-manifest.json)、[运行范围](execution-scope.json)区别实际事件和未做事项。[check_package.py](check_package.py)只做字节、语法、已捕获图的结构/引用和链接检查，不导入原程序、不重算收益/BI/IC。[成果指纹](artifact-manifest.json)与[静态结果](self-check.json)保封包；manifest排除自己和self-check以免循环。

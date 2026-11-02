# 五人根约束父方份额重建的证据

正式对象：[五人根约束的父方原始份额重建](../../../state/审查/五人根约束的父方原始份额重建--审查.md)。

`source-root/parent/`完整保留三份primary：2423B数学评语、6955B标准库源码、1547B冻结JSON输出。源码运行闭包的两份真实JSON输入放在原相对位置`source-root/realizability/`及`source-root/background/`；相邻三个数学原稿完整保留，以便核对每条SPE合同。所有文件均来自冻结版本，原程序和历史报告本轮没有运行或覆盖。

`acquisition/<id>.json`为`work.py clean show ID --out ...`的真实取得回执。清单的路径以当前证据目录为基准；回执中scratch绝对路径只记录取得位置，不是正文依赖。`content-manifest.json`记八份实际原件的大小/hash与冻结定位，`static-check.json`记本轮静态输入绑定和算术元数据检查。该检查不代替完整客户型枚举，不冒充新执行报告。

原目录关系保持可运行：若需要再现，可先复制整个`source-root`到临时位置，再在普通Python 3（不加`-O`）运行`parent/verify_root_cuts.py`。原main将写同名JSON；不要覆盖本证据中的冻结输出。它不需要LP、科学包、游戏求解器或网络；但运行通过仅证明明确合同的系数恒等式/余项，SPE合法性仍由正式正文解释。

本对象只对认领的三primary登记处置；五份related是实读比较和必要输入闭包，不在本批追加done。更早的direct主文已充分保有父direct报告，故不重复运行同SHA成功。全量语义回执及交付清单由父Boss串行接入。

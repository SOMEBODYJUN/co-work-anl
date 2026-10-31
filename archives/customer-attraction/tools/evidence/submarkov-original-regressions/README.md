# 完整历史消元：双旧证书原程序回归

本目录支持[正式计算对象](../../../state/计算/完整历史子马尔可夫消元的双证书精确回归--计算.md)。四主源9721/1603/2479/1759字节共15562字节，逐件全文实读、按冻结blob和SHA恢复，见`source-manifest.json`；四真实输入只读依赖共30256字节，见`dependency-manifest.json`，不在本批额外done。

- `original/`：四主源原字节，保原相对路径。现9721字节源码含v2 probe代码；没有初版源码来源，不伪称重放初版程序。
- `dependencies/`：两输入游戏、两完整历史策略证书原字节，保原相对路径。
- `pre-execution-current-file-search.json`：执行前扫描结果仓库和external缓存当前文件，排除.git对象库，无同SHA主源程序/报告副本；源码/报告名和SHA文字检索仅命中冻结定位、claim和前批历史说明。
- `replay/source-root/`：复原HERE.parents[5]与四输入路径。原源码字节完全不改，普通Python只运行一次，输出新建`reproduced_v2.json`。它是新的根目录，不是原机器绝对路径。
- `replay/execution.json`、`original.stdout.txt`、`original.stderr.txt`：实际命令、环境范围、UTC、exit0及完整输出。stderr为空；stdout与新报告均2479字节，逐字节同冻结v2。
- `replay/version-comparison.json`：v2只新增两模式初始化transfer计数及probe对象；删除新增字段后与初版完整JSON和1603字节全同。
- `replay/definition-derived-input-and-probe-details.json`：直接按定义补展开输入、源和非零all probe，便于读稿，不是第二次原程序执行或独立实现。
- `related-manifest.json`、`REVIEW.md`：当前数学对象比较、后纠错及本批范围。

有限run核1584项完整历史IC、2411个角色子集、1916项past类型标签域，两个OPT-owner源图均无正future传播；root_tax另在历史(5)注一单位，仅一条all边转移1/23，fresh始终无正边。不得称覆盖非零fresh链、全部游戏/平局或共同钱包cap。原程序未实现SAFE/CLIP/同客户取消；没有重跑另一3098字节fresh-count程序。

再次执行须另建干净root并保持原层级，或使用尚不存在的同目录输出名；源码的open('x')拒绝覆盖报告。本批无失败运行，没有删除失败、覆盖冻结输出或Git写操作。

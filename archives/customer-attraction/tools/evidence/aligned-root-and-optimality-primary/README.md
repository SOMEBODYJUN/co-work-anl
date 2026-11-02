# R-feb aligned root, exchange rows and fixed saved points

Boss3 / cleaner A9。17主源1062548B，正式claim pushed/synced `46b55760ba511a498cf3c24031c01c89c54a6857`。两冻结提交和逐源完整路径、SHA、大小、保全地址见[source-manifest.json](source-manifest.json)。原件位于[original](original/)，均保持原字节；[receipts.json](receipts.json)逐件给全文实读、比较和独有内容去向。

## 四个数学对象

- [对齐根程序](../../../state/程序/对齐根直方图列生成的双版本与零质量越界--程序.md)：756行保存版与765行当前代码分版；全部934原子/934质量/65对偶/9轮读取；原d5 exact/vector越界的隔离定点证据；新定义34行回代。
- [最优替换必要行](../../../state/引理/最优五索引的子集替换并集必要行--引理.md)：固定并集、同索引并集、锚定keep/drop、多匹配换及单换计数的自足证明；两个旧投影点全d1，原阴性不补SPE。
- [40客户原计数点](../../../state/计算/四十客户根尾付款保存点的完整策略补全--计算.md)：新完整781节点政策、3124字面非self IC，COARSE严格缺口243397/30。
- [定义攻击和LAST原范围](../../../state/资源/五人定义攻击与实际末位菜单探针的原范围--资源.md)：Cauchy同对象复用、历史OPEN、63客户原path的新恒5完整SPE及纯阻挡菜单上界17/2，原8.38仍浮点发现。

## 一次新固定数学运行

在结果仓库根执行：

```sh
python3 archives/customer-attraction/tools/evidence/aligned-root-and-optimality-primary/audit_fixed.py
```

此入口只读本包原件/七份已清洗依赖，不需要恢复整个原研究树。核心用Python标准库；原向量函数的单次异常定点需要NumPy，无SciPy。它只覆盖本说明的固定域；输出到本包replay。代码是本次精确审查与新构证据的可复现实现，绝非原研究main重跑。

已保存一次成功事件：[execution.json](replay/execution.json)、[process-event.json](replay/process-event.json)、[stdout](replay/fixed-audit.stdout.txt)、[stderr](replay/fixed-audit.stderr.txt)和[完整数学结果](replay/fixed-audit.json)。核心1.6871464849991753秒、exit0、stderr空。隔离原函数体/完整输入见[isolated-function-inputs.json](replay/isolated-function-inputs.json)，两个完整trace包含在结果CG项；它们是捕获到的原缺陷，未当作原主程序运行成功。

| 本次真实项目 | 范围 |
|---|---|
| 初版160表的新映射绑定 | 160×8=1280候选值，全部同表 |
| 加强版160表 | 逐160同成熟充分审查表；旧1280/4096新核0 |
| 保存CG回代 | 934×34=31756个贡献，仅34对齐行；完整731继承行0 |
| 隔离冻结aligned_rows | 3调用：d1 exact同值、d5 exact异常、两列vector异常；模块/main0 |
| 40客户保存点新构 | 252计数态、126终局；781有序政策、3124非self IC，3087严37平 |
| 63客户保存path新证 | 2801有序恒5政策、16806非self IC全严，min1；7×7菜单和纯列上界 |
| 两旧投影结构 | 64/38正质量原子全d1；28868交换松弛重算0 |
| 原随机/solver/LP/price/Universe | 全0 |

原程序、冻结输出和新补全策略严格分开：[direct-complete-policy.json](replay/direct-complete-policy.json)和[security-complete-policy.json](replay/security-complete-policy.json)均是本次新完整策略，不能回填原作者未保存的有序行动。

## 全文阅读和依赖合同

近1 MB原JSON未被摘要替代。[review-view](review-view/)从当前本次原件构造可反构字典视图，全部字典、934条原子/质量/extra记录、756行名、完整meta均已逐项读取；static_self_check重新检查逻辑反构相等。它仅省去重复字符串和JSON缩进，全部原数值仍完整原样保在original/template/aligned_root_cg.json。

[reused-dependencies.json](reused-dependencies.json)列七份普通文件原字节副本、原repo位置、大小/SHA；复用不计新primary done。两个旧点及底层证书是先前已充分清洗/全文实读资产；root/full_pricing相关源码本批又全文读。固定核无需root/full代码或其未收入的全部研究树输入；两份代码仅保继承接口及原CLI依赖证据。本包不伪造work.py/模块或宣称原完整CLI可直接运行。

[comparison-and-reuse.json](comparison-and-reuse.json)列14篇本批完整读成熟正文及指纹，注明足够证据复用和新核具体风险；[relationship-evidence.json](relationship-evidence.json)仅为有证据的关系登记，未生成阶段三图。[intake-and-scope.json](intake-and-scope.json)保真实认领、模型、执行零项及一次视图提取前的非数学语法错误，不隐去尝试。

## 静态自查

```sh
python3 archives/customer-attraction/tools/evidence/aligned-root-and-optimality-primary/static_self_check.py --repo .
```

它仅核字节、receipts、无损视图、固定结果形状和链接；不导入或运行数学核，不重复底层成功事件。阶段状态只表示这17源已完整清洗待父方串行review/checkpoint/done，Git写入与远端保存状态由父方单独回执。


## 父方发布副本

十三篇正式页均由父方实读；本包menu说明的残留求和下标在发布副本校为k≠j，未改原程序、定点数学核或原事件。parent-publication-updates.json保原/发布后SHA，并列成熟反例页的日期追加。初版静态helper保在initial-review；发布helper只接受这份明确指纹变化，限制检查本包四篇新页并另写publication-static-self-check.json，不覆盖代理原静态结果，也不重跑数学。

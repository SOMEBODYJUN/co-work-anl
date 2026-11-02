# CAG–UM两个直接编码：七源与实际复核

Boss3清洗七主源52753B，双冻结完整出处、源ID/blob/SHA和原字节在manifest/original；七receipt逐件给实际完整阅读和语义去向。没有将旧Boss9/actor/独立Astra身份变成本轮身份或调用。

数学出口：

- [不交主题与相关机纯SPE同构及倍率失真](../../../state/等价/不交主题与单位任务相关机的纯SPE同构及倍率失真--等价.md)：任意m完整历史双向证明、趋二覆盖而调度最优、一般共同客户平移。
- [分组配置与无色目录边界](../../../state/等价/分组配置全覆盖与无色共同目录的精确边界--等价.md)：每机一配置全覆盖iff阈值调度；任意q合并身份失败族、标记和位长边界。
- [归约合同和原论文审查](../../../state/审查/客户吸引与不相关机的归约边界及原文献核对--审查.md)：正面UM–Santa–MMDA链、中央覆盖骨架、负成本/分数分享/异目录等精确限制及PSPACE范围；没有无归约定理。
- [原Fraction入口和九组报告](../../../state/程序/两个自然编码的原Fraction审计与有限范围--程序.md)：70482含self IC、3578终局倒数、3412原指派的不同计数合同。

## 真实唯一数学执行

original/equivalence_audit/verify_direct_encodings.py 原字节只读执行一次，Python3.12.14，0.704190983秒、exit0/stderr0。stdout3002B与冻结encoding_audit.json逐字节同，SHA f1a7cade127be0da66e0b03a27a793b2bc3b8ff6bb5e579412e92f53ad93dd29。全部七原件前后大小/SHA不变。

完整argv/cwd/UTC/Python/输出与退出码在original-entry-001/execution-record.json，stdout/stderr各自保存。新数学核0、项目solver/verifier0、LP/随机0、成熟六人见证重跑0。任意m/q结论由自足证明，原代码只核两个列明有限区间。原独立审读自己明确未运行根代码，本轮不倒填其历史。

可从仓库根执行：

```sh
python3 archives/customer-attraction/tools/evidence/cag-um-direct-encoding-review-primary/original/equivalence_audit/verify_direct_encodings.py
```

只需标准库，无项目数据、旧Git对象、stub或网络依赖。脚本只stdout，main有guard但无CLI解析；--help也会运行。若保存新输出，请用新路径，勿覆盖冻结报告；本次成功后未重复科学核。

## 文献证据

literature-read-record.json保存本次经父方授权的八篇一手公开论文定点读取、题名/作者/精确版本/URL/定理位置、初始地址失败与替代公开PDF路线。只核本批明确引用位置，没有引用二手站代替原文，没有保存整篇版权全文或声称复证全部论文。未做全球最新查新；原2024/2026开放语句各按日期保留。

公开Bamas v2工具返回56页，旧成熟资源自述冻结副本5页；未导出/字节比对冻结PDF，不静默更改其SHA/页数。这项相关元数据差异不改变本七源的数学结论。后续参数审查已纠正损失λ越小越好；本对象遵守该方向。

comparison-record.json绑定六篇直接相关成熟正文的实读SHA，未把先期同名MILP编码页当CAG↔UM归约。未修改跨档共享文件，建议由父方串行。

## 静态交付对账

`reconcile_delivery.py`只读取本包、四正文与`--repo`给定的成熟正文，不import或执行原数学程序。它核七源字节、七receipt去向、已有唯一事件及stdout、九行表格和字段和、25个正文链接、八篇文献记录范围与六成熟比较SHA；结果在`self-check.json`。本次静态对账通过，数学重执行为0。

```sh
python3 archives/customer-attraction/tools/evidence/cag-um-direct-encoding-review-primary/reconcile_delivery.py --repo .
```

## 本批不授予的结论

没有CAG全目标与一般UM算法的双向归约、逻辑独立、任何gadget不可能、难度/耗时排序、新颖性或外部审查。五人half已有独立证明，当前六人和一般UM目标不由这两编码关闭。机器身份、完整SPE与多项式获得它、资源不可拆分、全部任务和统一比率均保其原义务。

## 2026-11-02：父方发布补读与复现入口修复

子批冻结后，Boss3 父方经 `clean show` 导出同一冻结 Bamas 相关 PDF，825616B/SHA 与成熟页相符；页树和 pypdf 均确认 **56 页**。只定点读第 1、3、44、56 页，并核实损失参数越小越好、MMDA 实例到 Santa 的方向。见[实际记录](bamas-frozen-metadata-review.json)、[冻结源指纹](bamas-related-source-manifest.json)和[相关原件](related-original/bamas-frozen-v2.pdf)。前述未导出状态属于子批冻结时刻；没有把此补读回填为子代理阅读，也没有多记一源完成。公开 PDF 二进制没有下载比较。

原 `reconcile_delivery.py` 依赖父目录恰名 `deliverables`，并扫描该目录全部正文；移入实际仓库后会失效。父方只修其静态定位：以本包已列四个 receipt 目标定位正式正文、使用实际含 `archives` 的根、允许已记录的父方成熟页更正哈希；现在输出单独 `publication-self-check.json`，不覆盖历史 `self-check.json`。原 7983B checker 另保在 `initial-review/reconcile_delivery.py`。它仍不 import 或执行任何数学程序。父方更正及前后哈希见[发布审读](parent-publication-review.json)。

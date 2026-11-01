# 七极大六人整数集合搜索：源码、ELF及新末点证据

[自足程序正文](../../../state/程序/七个极大主题的六人整数终局集合搜索程序--程序.md)合并两主源的数学对象与实现身份，逐源回执分别保留。

| 原件 | 主源 | 字节数 | SHA256 |
|---|---|---:|---|
|[search7.cpp](original/search7.cpp)|5e061edecf721d433678|5433|56cac2ec12dccba09010c0dd188b0cc974439ce612f2726773c952220886424a|
|[search7](original/search7)|a7ba166b252219cc543d|27160|b37ce54e8a47ce77995a3e24dadab26836facfa2c4cafece9ac2f968bb3f7d2c|

两冻结提交均同字节。[source-manifest.json](source-manifest.json)保blob、模式、完整路径、全读材料及执行边界。ELF不是一份历史运行报告；源码标题中的exact也不取消32位串号溢出条件。

## ELF与一次编译、两个短入口

[inspect_and_run.py](inspect_and_run.py)是已实际执行的保全驱动。它先保存file/readelf/nm/objdump，再用g++13.3.0、`-std=c++17 -O2`编译一次。新产物[rebuilt-search7](binary-event/rebuilt-search7)为23096B，与27160B旧ELF字节不同；不认定恢复了历史flags。旧/新产物各执行一次预算1、seed192711，均实际2次solve、0LP；stdout/stderr逐字相同，仅为这个有限输入上的行为一致。

- [execution.json](binary-event/execution.json)：逐命令argv、时刻、退出码、耗时、原件前后SHA和编译差异。
- [file](binary-event/file.stdout.txt)、[readelf](binary-event/readelf.stdout.txt)、[符号](binary-event/symbols.stdout.txt)、[rodata](binary-event/rodata.stdout.txt)、[完整反汇编](binary-event/disassembly.stdout.txt)：静态实读证据。承重反汇编与C++对应，但没有正式证明两版本全域等价。
- [旧ELF stdout](binary-event/original-short.stdout.txt)、[旧ELF stderr](binary-event/original-short.stderr.txt)、[新产物 stdout](binary-event/rebuilt-short.stdout.txt)、[新产物 stderr](binary-event/rebuilt-short.stderr.txt)：该次真实短入口。eval1为W352/OPT359，完成行eval2；未运行scan_36155长历史。

保留的驱动以自身所在目录作为临时根，要求同目录有两个原件，并独占创建binary-event。若未来确需重现，复制驱动与两个original文件到一个新目录再运行；本轮不为封包重跑。短运行不是权重输入接口，原程序没有evaluate模式。

## 日志末点的一次独立精确认证

相关日志及12输入静态核在[数据包](../r70-search7-log/README.md)，原[scan_36155.txt](../r70-search7-log/original/scan_36155.txt)2509B。本包全文读原24行及数据核脚本，不重算12×924静态覆盖；basename不作为seed证明。

[audit_last_point.py](audit_last_point.py)只处理最后eval47752的159客户输入。它展开单位客户、独立算占用标签的60倍收益，以Python任意整数作1716状态集合DP，再生成19608有序节点策略并核137256真实比较。覆盖与OPT直接复用[static-coverages.json.gz](../r70-search7-log/static-coverages.json.gz)及[log-audit.json](../r70-search7-log/log-audit.json)，输入绑定同时保gzip与解压SHA。

- [last-point-execution.json](last-point-execution.json)、[stdout](last-point-stdout.txt)、[stderr](last-point-stderr.txt)：唯一新独立事件，外层约1.243秒、exit0，0原helper/ELF/LP/静态覆盖重扫。
- [point-audit.json](last-point/point-audit.json)：root R只含(0,2,0,0,0,0,4)，W131/OPT158、比例131/158、half余量104及全部余量频数。
- [complete-strategy.json](last-point/complete-strategy.json)：本次新完整σ，实际路径(6,6,6,6,1,1)，不是原日志已保存的顺序。
- [exact-details.json.gz](last-point/exact-details.json.gz)：924收益表、1716个R以及每个有序历史的动作、真实叶、规定收益与七项余量。压缩不省检查域。

记录里的19608个零余量恰为自身行动，全部117648个非自身比较严格正，最小1/10；由末层唯一最优逐层归纳，此指定实例的完整纯SPE唯一。不能只凭根R大小1证明策略唯一，更不能外推一般目录。前11点的根最低SPE断言未在本次独立事件重算。159是总客户、158是OPT、131是福利，三者不混用。

重新核验新对象时的接口为：

```text
python -B audit_last_point.py --log-audit ../r70-search7-log/log-audit.json --coverages ../r70-search7-log/static-coverages.json.gz --output-dir NEW_DIRECTORY
```

该命令会重新执行DP，不是本轮已重复调用。现存证据直接读取即可。[check_package.py](check_package.py)和[self-check.json](self-check.json)只核原字节、保存结构、余量记录一致性、AST、链接及两份回执，不调用数学程序、编译器或ELF。

# 联合必要图程序证据

正式对象：[索引主题与实际第四步B分支的联合必要图程序](../../../state/程序/索引主题与实际第四步B分支的联合必要图程序--程序.md)。主源 `9aa0e3af9d15dc62a830` 的4621B原件及45份依赖保持冻结字节；身份、SHA、实际路径和默认/扩展用途见 `source-manifest.json`。这里的清洗目标是主程序，保全依赖不等于替其他来源完成逐源清洗。

本轮唯一的原入口是隔离环境中 `python -B combined_branch_master.py --verify`。它重建5108行1905列并精确通过，最小slack=0，W为 `7788343487189316604380335059457339/16141009471373384499891913301798724`。没有运行主程序的浮点优化模式或扩展模式。

`rerun/execution.json`、`stdout.txt`、`stderr.txt` 是真实事件原字节。`replay_default_once.py` 是当时在clone外实际使用的组织脚本原字节，故其运行布局以脚本所在目录为ROOT，要求邻接 `current-frozen-files-manifest.json` 及原repo相对路径；归档后的文件不假装能在本证据目录直接执行。`available-frozen-files-manifest.json` 是当时49份**可用且前后检查过SHA**的冻结文件，并非加载跟踪日志。9份扩展文件未由默认入口加载；两个其他程序的独立大点也不是本入口依赖。本包避免复制这两个大点和已共享保存的master点。

本轮补充的 `check_interfaces.py` 只读数据和AST，不导入历史程序、不重建全图、不求LP。其 `interface-audit.json` 核47份当前持久/共享原件，补核1905列布局、O/W、历史权重非负、702行数据计数、三个448项查找表合同，以及扩展开关的静态行数。它没有重建历史AB/maxroot投影证明，也不作为第二套5108行实现。

如需以后再做一个独立的执行事件，可从仓库根运行：

```sh
python3 archives/customer-attraction/tools/evidence/combined-branch-master-program/materialize_runtime.py /absolute/new-empty-runtime
python3 -B /absolute/new-empty-runtime/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/combined_branch_master.py --verify
```

第一条只按清单核SHA并复制原字节，不执行原程序。新ROOT标记 `work.py` 仅含注释，供旧模块寻找根目录，不是仓库控制器或凭据入口。第二条需要NumPy和SciPy，必须保持assert开启；运行时间可以不同。原入口不应从冻结原件目录执行优化模式，以免覆盖exact/status文件。这个材料化程序没有在本轮触发第二次原入口运行。

扩展静态阅读范围：latest增加72行，new-local增加9行，两者组合为5189行；latest+local-v2为5198行。单独local-v2的8个portfolio条目会引用只在latest块导入的局部变量，属于已保存的原码问题；本轮未修原件、未伪造扩展运行事件。恢复这些模式的完整核验还需要各自对应exact点，本包没有声称保存那些点。

文件分工：

| 路径 | 内容 |
|---|---|
|`original/combined_branch_master.py`|主冻结原件|
|`dependencies/`|45份冻结依赖，原repo相对路径；包括默认的旧702行JSON树及扩展静态阅读材料|
|`source-manifest.json`|源ID、冻结提交、SHA、实际保存位置、用途；共享master点指向父报告原件|
|`rerun/`|唯一原入口事件、原输出、实际组织脚本、当时49源清单|
|`check_interfaces.py`、`interface-audit.json`|当前新增的精确输入/静态域检查及结果|
|`materialize_runtime.py`|复原独立运行目录的当前工具，不自动执行入口|
|`package-check.json`|JSON、平坦frontmatter、本地链接、receipt targets和SHA自查|

`--verify` 对旧master点通过，不证明改变Z后的pair点也通过旧5108行；必要图点、共同客户实现、固定前缀两尾均衡及完整历史SPE分别保存证据。关系解释在正式对象中，阶段三另建图。

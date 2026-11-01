# 完整156主题作者尾审计器证据

正式合同见[程序对象](../../../state/程序/完整156主题的作者两人尾审计器--程序.md)，19字段另见[作者报告对象](../../../state/计算/完整156主题的作者可信尾与实际缺陷报告--计算.md)。本包状态`local-prepared`，待Boss串行推送；没有Git、claim或done动作。

保全2013字节原件在`original/audit_full156_tail2.py`；唯一运行数据依赖复用[共享kernel](../full156-tail-parent-report/original/research_5/full156_tail2_kernel_10344.json)，不再持久复制大矩。原程序按`__file__`寻找同级`research_5`，且没有main guard，导入即执行并相邻写报告，不能直接在原件目录运行或import。

本次已执行的唯一原入口由以下包装器完成：

```sh
python3 archives/customer-attraction/tools/evidence/full156-author-tail-auditor/run_original_once.py
```

包装器独占创建`rerun/`以保护已有事件，不应在当前包重复执行。它只临时复制源码/kernel，执行`python -I -B`，保存stdout、stderr、原格式报告及execution，随后删除临时大副本；没有调用客户矩生成器或父方原入口。stdout和报告均4630B、逐字节等冻结c758报告。

可再次运行的不执行原入口的交付检查：

```sh
python3 archives/customer-attraction/tools/evidence/full156-author-tail-auditor/build_manifest_and_check.py
```

该检查核源与共享kernel SHA、完整矩形/F-G/U内部一致性、尺度和前缀身份、JSON/frontmatter/links/receipt targets，以及已保存原运行报告的字节身份。它不重新构造阈值客户或证明全六人SPE。

文件角色见[manifest](manifest.json)，实读和关系见[comparison](comparison.json)，矩读取见[matrix-inspection](matrix-inspection.json)，唯一原运行见[execution](rerun/execution.json)，交付检查见[self-check](self-check.json)。

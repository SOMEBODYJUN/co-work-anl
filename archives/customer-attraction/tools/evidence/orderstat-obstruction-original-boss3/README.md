# 七极大对称列分离与原论文语境的四源证据

本包保留Boss3正式认领的四份冻结全文、来源指纹、原41行程序的一次实际执行及知情独立重构。数学正文为[对称列分离与共同容器边界](../../../state/障碍/七极大六人混合保底与末两位税的对称列分离--障碍.md)与[原论文模型及效率边界](../../../state/文献/顺序客户吸引原论文的对称模型与效率边界--文献.md)。这里只声明这四个源版本的处置，不把相关旁读自动done。

## 精确原件

所有原件均与 `source-manifest.json` 的SHA-256一致，双冻结提交各自的原路径/blob/字节数保存在清单中。原件不改复现命令、字段或数学表述。

| 源ID | 原件 | 字节 | 去向 |
|---|---|---:|---|
| `6dc6252149e13cfb3967` | `original/6dc6252149e13cfb3967/arxiv_sequential_context.md` | 2853 | 文献语境；核原网页并纠正完整历史量词、v2年份及静态势/复制机制混称 |
| `b250332e48ded26029d4` | `original/b250332e48ded26029d4/README.md` | 2983 | 对称4064列域、八质量和分离证明；补真实共同容器缺失边界 |
| `496e74b295821f1b098e` | `original/496e74b295821f1b098e/dual_obstruction.py` | 3923 | 原字节程序、全部41行及一次实际stdout |
| `6e4e8f74db4d005dfe14` | `original/6e4e8f74db4d005dfe14/workspace.json` | 150 | 完整四字段历史来源身份；无数学命题，不作当前身份或认证资料 |

## 数学执行与新增边界

`runs/original.stdout`、`runs/original.stderr`、`runs/execution-record.json` 记录原 `dual_obstruction.py` 的一次普通断言启用执行。它只用标准库，无输入文件或策略求解器，重建4064列/416组，验证八轨道质量和为1、41行均值非负及负基础平均 `-2027846/107130789`。最小行均值为0。原代码的“唯一有理解”注释未附活跃系统，唯一性没有认证。

`review_exact.py` 是知情独立标准库实现，不import或调用原脚本。其一次stdout在 `runs/independent.stdout`，给完整38个正字面支持、41个具名平均、各省略标签的比较目标平均、固定000010合法列数及逐实际位置可能的共同极大容器。本次原程序一次、独立程序一次，均exit0/stderr空。没有运行LP、ASR入口、全树SPE枚举或策略搜索。

共同容器检查是新增数学范围审查：真实行动A_t必包含于某一个B_j，故所有正客户列要共用一个标签a_t，满足`t∈J => a_t∈I`。原八轨道的`I={j},J={4}`对j=1,…,6均有正质量`2017043/428523156`，任取j1/2即排除合法A4；其共同容器集合为空。原见证不能实现任何实际路由，固定000010下另有10个正支持不合法。分离仍准确成立于原4064列松弛域，不能升级成1631列固定真实路由域或完整SPE反例。

若主动复现，可从仓库根依次运行：

```sh
python3 -I -B archives/customer-attraction/tools/evidence/orderstat-obstruction-original-boss3/original/496e74b295821f1b098e/dual_obstruction.py
python3 -I -B archives/customer-attraction/tools/evidence/orderstat-obstruction-original-boss3/review_exact.py
```

原README里的旧`R-research18-orderstat-obstruction`路径仅保原字节，不作为当前入口。

## 文献与相关实读

`bibliography-review.json`登记实际核读的权威arXiv v2链接、章节、版本日期与核验范围，不保存整篇第三方网页。论文Definition4已有完整有序前缀和任意偏离量词；文献页对原note作此纠错，没有误称核了最新文献全景或外部新颖性。

相关全文比较包括：共同目录完整历史模型、私有共享混合保底、普通两人税及强PAIR、七极大n≥7定理、五路由41行分离、83行粗路由/真实负载边界、顺序统计表达式错位审查、六人all-big完整SPE对象；另读已保存的原ASR README和`audit_asr_dual.py`。后者复用本八轨道分布，固定路由参数不代表客户列已通过共同容器约束；本批没有重跑其数学入口，也没有撤销五路由另外的17列000010见证。

第二阶段关系在两正式正文解释：必要行来源、相同公式与不同列域、外部模型出处、独立完整策略下界，均不等于一般六人半覆盖的推导。三级超图仍留第三阶段实际逐边整理。

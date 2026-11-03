# 独立包络复核：原程序、旧日志与当前恢复

本包保全 `round4_independent` 五件冻结原件，共12,502B，逐件以 `python3 work.py clean show ID --out`取得，再核冻结size/SHA。完整双提交、blob、路径与原字节位置见[source-manifest.json](source-manifest.json)。Boss2只新增本包与[正式审查](../../../state/审查/独立包络复核的局部匹配与静态封顶合同--审查.md)，不修改其他组入口或历史记录。

`original/`是准确冻结字节；`replay/`中的两份Python与原件字节相同，但其相邻JSON是本次新执行输出。两原入口均只用标准库，无输入文件；从本目录可分别在`replay`运行 `python3 -B iid_cap_audit.py` 与 `python3 -B shared_envelope_audit.py`。这些命令会覆盖replay内相邻JSON，正常复用本次已成功结果即可，无需例行重跑。

## 已完成的数学恢复

- `iid_cap_audit.py` 一次成功，约0.183秒，原793B报告逐字节一致：二次数域的小根隔离、八客户16背景/64终局、不同边缘独立product、120二差、1728有理Jensen。源码另断言Z3>544/87，报告不单列此断言。
- `shared_envelope_audit.py` 一次成功，约18.936秒，原660B报告逐字节一致：44种指定负载/锚点配置、49064二位赋值、147192末位恒等式、98128保交叠恒等式、两机制各7511配置内极值类。它不检验所造局部记录满足真实IC，也不恢复跨客户共同目录匹配。
- `cross_final_row_audit.json` 原455B报告保全。其同SHA61点单行值与已发表Boss3 `mixed_saved.json` 的 `AB:direct:2:all-AE.S` 相等；同点2016行已充分成功，不新增数学重算。原独立求值脚本未随这份主源出现，不推称已恢复其实现独立性。

[runtime-record.json](runtime-record.json)保命令、exit、stderr字节、耗时和前后SHA；`replay/*.stdout.txt`、`*.stderr.txt`为实际捕获。新原数学入口共2次成功、0失败；优化器0、完整SPE检查0、cross新求值0。metadata/旧结果绑定见[dependency-and-reuse-manifest.json](dependency-and-reuse-manifest.json)，不把本次数值比对称为另一次2016行核验。

## 解析证明和旧范围

普遍排序必要性、两人真实IC与self-tax、任意latent共同iid混合的Jensen结论及全q最优cap已由正式定理/引理自足承担，正式审查逐项链接并比较。有限运行只恢复实现证据，不外推全负载、任意人数或恰六人完整有序历史纯SPE半覆盖。先前正文“缺原程序/未重跑”是当时实际状态；此次新增恢复不倒填旧事件。

五件逐源receipt草稿、交付和自查在 `cleanup/workspaces/Boss2/resume-20261103b/independent/`，等待父Boss串行checkpoint及done；本组没有Git写入、claim、done或公屏动作，也没有启动2.5/图。

# 同覆盖商编译父方重放报告的来源与当前执行

主源 `011c8217d27ee1a1e23f`，636B，SHA256 `55f8b8ff482456604a8b32c650c62309d892197290e2da58070d370b36cd96b2`，在 `original/action_quotient_replay.json`保原字节。`related/`保全文已读的2506B原编译器、4370B作者测试、339B作者报告及三原MD，都是相关材料，非本次主源认领。

正文：[同覆盖商编译的作者测试重放报告](../../../state/计算/同覆盖商编译的作者测试重放报告--计算.md)。`manifest.json`列两个冻结来源、每份原件SHA与实际阅读范围。父报告两源码hash已逐字节匹配；父报告前九字段等于作者报告，review是历史身份说明而非测试自动证明的结论。

当前重放命令：

```sh
python3 archives/customer-attraction/tools/evidence/action-quotient-parent-replay/replay_author_tests.py
python3 archives/customer-attraction/tools/evidence/action-quotient-parent-replay/explain_counts.py
```

第一程序在隔离目录执行原样作者CLI，断言开启；exit0、stderr空，stdout339B与原作者报告逐字节一致。事件在 `replay/execution-event.json`，stdout在 `replay/author-stdout.json`。该包装器为本轮新写，不能称历史父runner。冻结Python检索action_quotient_replay和compiler_sha256无命中，尚未定位原父报告写入程序；未据此捏造原命令或时间。

第二程序用两人私有收益抵消共享c/2独立核856个SPE及商IC3840；三人信号诊断明确复用作者seed和BI，不称独立完整实现。确认67626=3840+7800+55986；43个标签信号案例中16个覆盖类也改变、27个仅别名改变，原43谓词本身未变。所有200项诊断保在 `replay/count-semantics.json`。

一般双向商等价由已有证明承担；代码是正向编译器、有限测试是固定域实现核查。原输入允许零类型、空覆盖、重复标签；每个商历史含终局有一致lift；不得把label差异直接叫覆盖差异或把一次原代码复跑算另一套独立测试。六人全大主题回归W6/OPT11，不是half反例。

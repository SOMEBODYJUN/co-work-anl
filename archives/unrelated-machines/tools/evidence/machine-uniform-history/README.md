# 逐机统一查询返回v2五份历史原件证据

实际claim pushed/synced f40bb0dfb2d9e9aa7aba6b9e890c5b5311b4f66b确认后，五主源逐份完整读取，size/SHA核inventory。旧主稿806238bb6efd4db5b901已完成；其旧证据包保存七notes/root作过comparison，不能替本批五源语义处置。此包全部11份来源都复用已有同SHA原字节，无原件改写或重复造v1 Proof。

[证明补充](../../../state/证明/容量查询返回的平行元证明与双增广实现--证明.md)自足展开共同C收缩/非loop平行元、物理cap与rank两截断、作者双起点及独立先q_j失败再b_i两实现、全部原A及任务投影、合法外封装guard和v1真实时间恢复。[五稿历史审查](../../../state/审查/逐机统一交换的五稿原义与封装前件--审查.md)逐源保实际先验、八义务、最终完整1–5及guard补清；已有[主定理](../../../state/定理/逐机统一容量的查询返回严格交换--定理.md)不重复done。

| 证据 | 用途 |
| --- | --- |
| [source-manifest.json](source-manifest.json) | 五主源Exact/Proof/rank独立/作者读后/canonical读后原字节及双冻结定位。 |
| [comparison-manifest.json](comparison-manifest.json) | 六完整比较：v1两件、8046B canonical、root七原链、6074/3e6ac不同域。 |
| [scope-and-sha-chain.json](scope-and-sha-chain.json) | 六条原文SHA链、whole b930及五章节字节切片、唯一v2 Proof与真正阅读顺序。 |
| [guard-and-version-ledger.json](guard-and-version-ledger.json) | 旧笼统封装和最终guard的实际原句、合法性充分/必要区别；v2 Exact原已准确写v1模式化约。 |
| [proof-variants-and-quantifiers.json](proof-variants-and-quantifiers.json) | 精确cap/parallel rank/两增广、strict/weak输入量词、全原任务与位成本。 |
| [non-run-provenance.json](non-run-provenance.json) | 各原源无通用软件/有限实验，本轮数学run0与blind0；不借其它族5184/4328为本源运行。 |
| [relation-review.json](relation-review.json) | 补充现有主定理、不同证明表示、模式化约/封装guard及跨域边界，阶段二无正式超图。 |
| [verify_delivery.py](verify_delivery.py) / [实际结果](delivery-self-check.json) | 只验来源字节、原文链/章节/guard片段、receipt与链接，不做容量匹配或数学实验。 |
| [五receipt](../../../../../cleanup/workspaces/Boss4/r3-machine-uniform-history/semantic-receipts.json) | 3 retained/2 integrated，每源完整read/compare/独有内容去向。 |

最后canonical实际whole SHA为b930c8d0e8f2607495eb4addb94c071c60a2edfa85669c36847d5f77599feb5a，8046B，正式完整§1–5，但仍只限逐机uniform非负时间、固定A、局部/私有outside。该final明确aligned前件可行足以保证每A有finite内部端；A无端则带该原job封装非法，局部仍可判aligned不可行。这个充分guard不能倒成“UM合法必须有aligned”；旧措辞不回改。

v1 finite p∈(B/2,T]、T≤B<2T允许同机异权；uniformize为T求matching后恢复原p是模式化约，不是原矩阵逐项包含。v2 Exact/Proof原本已经准确说明，不虚构后来才纠正此点。独立rank与作者Proof信息顺序保真；本轮已读Proof是read-after，未新造blind或单独v1作者Proof。

## 完整性复核

`ROOT`为本staging，`REPO`为保存依赖原件的仓库根，合入后两者可都指仓库。只写指定完整性JSON，无Git/claim/done操作：

```bash
python ROOT/archives/unrelated-machines/tools/evidence/machine-uniform-history/verify_delivery.py --root ROOT --fallback-root REPO --output ROOT/archives/unrelated-machines/tools/evidence/machine-uniform-history/delivery-self-check.json
```

Checker核原文/记录一致性，不能代数学判断或把PASS升级为新颖性、外审、一般UM算法或全局source反面。当前没有原入口需要运行，也未执行其它旧程序。

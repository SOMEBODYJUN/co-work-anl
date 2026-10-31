---
id: "customer-attraction/transport-two-three-tail-script-review-20261031"
kind: "review"
type_tag: "审查"
title: "transport_round 两加三尾部脚本来源与精确重放"
status: "complete-source-read-and-exact-replay"
truth_status: "exact-specified-path-rejection-not-coverage-counterexample"
review_level: "clean-show-full-read-fraction-runtime-and-cross-source-comparison"
scope: "history/source/notes/customer_attraction/transport_round/two_three_tail_check.py；75单位客户、5提供者、10主题的指定两加三目标路径必要可信偏离检查"
summary: "源脚本完整读取、py_compile 与运行均通过；输出与既有冻结 two_three_tail_check.json 逐字段相等。它只证明 bare 25 omitted-pair populations 中目标路径 (3,4,5,6,7) 不能出现在任何完整 SPE，严格偏离增益为 1/20；不构成完整策略树福利反例、五人全称定理或六人 half 反例。"
source_refs:
  - "source:70e701bc5d683a704dcd:history/source/notes/customer_attraction/transport_round/two_three_tail_check.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/two_three_tail_check.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/two_three_tail_check.py"
related_objects:
  - "../审查/五人半覆盖上传证书与个体安全运输尾部五源接续审查--审查.md"
  - "../审查/两步安全归纳与策略锥精确边界--审查.md"
  - "../定理/末两人回复循环静态运输恒等式--定理.md"
  - "../计算/末两人运输与指定核的双实现核验--计算.md"
  - "../审查/新策略安全锥与半顶点候选增量审计--审查.md"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/transport-tail-script-20261031/two_three_tail_check.py"
  - "archives/customer-attraction/tools/evidence/transport-tail-script-20261031/replay.json"
  - "archives/customer-attraction/tools/evidence/transport-tail-script-20261031/replay-metadata.json"
  - "archives/customer-attraction/tools/evidence/transport-tail-script-20261031/source-manifest.json"
---

# 1. 来源身份、版本和完整阅读

`clean show 70e701bc5d683a704dcd --out .../two_three_tail_check.py` 实际导出并逐行读取冻结源。源路径为

```text
history/source/notes/customer_attraction/transport_round/two_three_tail_check.py
```

源元数据为：blob `a6f2d1e8f88ab87faaec14e5b5fd1fa0ff397577`，1768 字节，SHA-256

```text
ba0e9a96f2a920086ce48180ede0e01aeeba223b497cd67087d5b5f5223203c0
```

inventory 同时绑定 legacy-cleanup 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 main 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。直接对两提交执行 `git show`，均得到 1768 字节和上述同一 SHA；它们是同一冻结源版本，不应计为两项独立实验。

源只导入标准库 `Fraction`、`product` 和 `json`，没有调用仓库均衡求解器、线性规划器或外部数据文件。证据目录保留原脚本、运行输出、既有 JSON 的 SHA 比较、版本比较及 `source-manifest.json`。

# 2. 脚本实际定义的有限游戏

脚本定义

```python
types = [(frozenset(set(range(10)) - {a,b}), 3)
         for a,b in product(range(5), range(5,10))]
```

因此客户类型由 5 个低标签 `0,...,4` 与 5 个高标签 `5,...,9` 的所有遗漏对组成，共 (5\times5=25) 个类型；每个类型重数为 3，总单位客户数 (75)。每名客户喜欢十个主题中的八个主题，恰好遗漏一个低标签和一个高标签。脚本的 `utility(action,z)` 对含有当前动作主题的类型求

\[
\frac{3}{\#\{b\in z:b\text{ 覆盖该客户类型}\}},
\]

因此重复主题和重叠覆盖严格按照均分规则处理；分母由完整行动序列 `z` 的覆盖者数量给出，分式全部使用 `Fraction`。

脚本没有构造完整策略树，也没有给每个有序历史指定动作。它只检查一个候选终局路径及其中一次偏离后的末位最佳回复。故其结论天然是指定路径的必要条件拒绝，而不是存在一个完整纯 SPE 的反例实例。

# 3. 目标路径与两层可信偏离

代码固定

```python
h = (3,4,5)
actual = (3,4,5,6,7)
```

并将第四位实际行动 6 的收益计算为 `utility(6, actual)`。随后假定第四位在历史 (h) 偏离到 0；若末位选择 (a\in\{0,\ldots,9\})，末位收益由 `utility(a, h + (0,a))` 计算。十个精确值为

\[
\left(
\frac{143}{10},\frac{303}{20},\frac{303}{20},
\frac{143}{10},\frac{143}{10},\frac{69}{5},
\frac{297}{20},\frac{297}{20},\frac{297}{20},\frac{297}{20}
\right).
\]

最大值为 (303/20)，最佳回复集合是 ({1,2})。再把第四位偏离者的行动固定为 0，分别计算末位回复 1 和 2 时第四位收益；两者都为 (303/20)。实际第四位收益为

\[
\frac{151}{10}=15.1,
\]

所以在偏离到 0 后，只要末位按自己的最佳回复行动，第四位得到

\[
\frac{303}{20}-\frac{151}{10}=\frac1{20}>0.
\]

这排除了该路径作为完整 SPE 的终局路径：任意声称实现该路径的完整策略，在历史 ((3,4,5)) 上都给第四位一个严格有利的可行偏离，而末位的回复 1 或 2 都是其最佳回复。这个论证不依赖任意平局选择；两个最佳回复对第四位给出同一个严格增益。

源还检查了实际第五位行动 7 的局部可信性：

```python
assert utility(7, actual) == max(utility(a, h + (6,a)) for a in range(10))
```

这只确认在未偏离前缀 ((3,4,5,6)) 后，7 是末位最佳回复之一；它不能修复第四位偏离后的严格增益。

# 4. 独立运行与冻结 JSON 对照

对 clean-show 导出的脚本执行：

```sh
python3 two_three_tail_check.py
python3 -m py_compile two_three_tail_check.py
```

两项均通过。运行 JSON 的 SHA-256 为 `e13f78158c8c78a761f8ca88793bd7fd7b54178097f5c2c158df91fd92291027`，与已保存在 `cleanup/workspaces/Boss2/transport_round_two_three_tail_check.json` 的冻结输出 SHA 完全相同；解析后的两个 JSON 对象逐字段相等。运行输出保留 `status=PASS`、75 客户、5 人、10 主题、目标路径、10 个末位支付、最佳回复 `[1,2]`、第四位两个偏离支付、可信偏离下界 `303/20` 和严格增益 `1/20`。

该重放是源程序自身的标准库精确运行，不是把摘要重新录入 JSON。`replay-metadata.json` 记录源 blob、两个冻结提交的同 SHA、脚本编译状态、运行状态和 JSON 相等性。

# 5. 与既有正文和相邻来源的关系

既有 `两步安全归纳与策略锥精确边界--审查.md` 已从研究记录层面写出同一数值向量和 `1/20` 增益；本源脚本补足了该数值的实际定义来源、25 类型构造、最佳回复枚举和可执行重放。两者不是两个独立数学实例，应在第三阶段标为“历史审查 + 生成脚本 + 重放输出”同一对象。

它与 `末两人回复循环静态运输恒等式--定理.md` 的关系是：该定理给出任意完整形式策略末两人回复图的共同静态背景和逐类型运输恒等式；本脚本则在一个具体 75 客户、五人、十主题的 omitted-pair 人口上，用末两层的真实最佳回复证明一个候选路径不可能。脚本没有构造循环、共同 (Q) 或全策略锥，因此不能替代该定理，也不能从一个路径障碍推出所有路径的失败。

它与 `末两人运输与指定核的双实现核验--计算.md` 的关系是：后者核验两个三人完整策略的全部历史与指定核，属于完整策略树的有限证书；本脚本没有完整策略表，也没有 5 人全树 SPE 检查，证据等级较弱，必须单独标为“指定路径严格偏离见证”。

它与 `五人半覆盖上传证书与个体安全运输尾部五源接续审查--审查.md` 中的 JSON `two_three_tail_check.json` 是同一运行对象：JSON 是脚本输出，脚本是生成机制；不能将二者记作两份互相独立的反例。

# 6. 数学边界和接续

可确认的结论仅为：在这 25 个 omitted-pair 客户类型、每类重 3 的具体模型中，终局路径 `(3,4,5,6,7)` 不能由任何完整纯 SPE 实现。它提供一个严格的偏离见证，具体增益为 (1/20)。

不可确认的内容包括：

- 该模型是否存在其他完整纯 SPE 终局路径；
- 所有两加三路径是否都被排除；
- 五人任意共同目录或任意客户实例的半覆盖定理或反例；
- 六人 Q-CAG-HALF 目标的证明或反例；
- 全局 (operatorname{OPT}) 与任意完整 SPE 福利比较；
- 客户人口构造的最小性、搜索穷尽性、外部同行评审或世界新颖性。

第三阶段应把该对象连接为：

```text
25 omitted-pair population
  -> specified path (3,4,5,6,7)
  -> deviation 0 at history (3,4,5)
  -> last-player best replies {1,2}
  -> fourth-player strict gain 1/20
  -> path rejected in every complete SPE
```

关系标签必须保留“指定路径、五人十主题、75 客户、Fraction 精确、非完整策略树”的限制，不应把它导入六人半覆盖主线作为一般反例。

# 7. 处置记录

| 字段 | 内容 |
|---|---|
| 实际阅读 | clean show 源全文 1768B；逐段读取类型、收益函数、路径、最佳回复和断言 |
| 实际运行 | `py_compile` PASS；标准库运行 PASS；输出与冻结 JSON 逐字段相等 |
| 独有内容 | 可执行的 25 omitted-pair 类型生成、两层末位最佳回复和 (1/20) 严格偏离 |
| 去向 | 本审查正文；`transport-tail-script-20261031/` 原脚本、replay、metadata、manifest |
| 既有关系 | 与既有 JSON/两步审查合并为同一指定路径障碍对象；不重复建定理 |
| 未解缺口 | 未枚举其他路径或完整 5 人策略；不涉及六人全称目标 |
| 状态 | integrated；等待父 Boss checkpoint/pushed 后逐来源 done |

---
id: customer-attraction/early-3227-input-and-dual-audits
type_tag: 审查
kind: review
title: 早期3227输入与双审计增量
status: ready-for-checkpoint
truth_status: finite-exact-audit-and-input-cross-check-no-general-half-result
review_level: full-source-read-independent-stdlib-consistency-check
summary: 三份 transport_round 冻结源分别给出 3227 个单位客户的 22 类输入、完整顺序审计摘要和不导入项目验证器的 Fraction 独立审计；它们复核早期3227证书的输入与局部安全值边界，但只反驳两条一步安全值归纳式，不反驳聚合桥或 half 目标。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_input.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_input.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_audit.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_independent_audit.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_independent_audit.json
evidence_paths:
  - archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/local_security_increment_initial_3227_input.json
  - archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/local_security_increment_initial_3227_audit.json
  - archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/local_security_increment_initial_3227_independent_audit.json
  - archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/verify_3227_audits.py
  - archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/verify_3227_audits.json
  - archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/manifest.json
related_objects:
  - archives/customer-attraction/state/计算/早期3227安全值增量证书--计算.md
  - archives/customer-attraction/state/计算/安全值链与五人逐人安全值的精确核验--计算.md
  - archives/customer-attraction/state/审查/transport_round候选政策与特殊种子障碍接续审查--审查.md
---

# 早期 3227 输入与双审计增量

本增量处理三个仍未单独处置的冻结源：输入 `local_security_increment_initial_3227_input.json`、顺序审计摘要 `local_security_increment_initial_3227_audit.json` 和独立审计 `local_security_increment_initial_3227_independent_audit.json`。它们与已入库的 `早期3227安全值增量证书--计算.md` 属于同一早期 transport_round 实例，但分工不同：输入文件保存 22 类客户及六个主题的原始计数；顺序审计给出摘要字段；独立审计保存 258 条逐动作比较、两个精确鞍点和来源哈希。这里补充这三份来源的实际内容，不重写既有 certificate 对象。

## 原件身份

| 源 ID | 文件 | 大小 | SHA-256 | 两个冻结提交 |
| --- | --- | ---: | --- | --- |
| `a193f346881b36d9636a` | `history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_input.json` | 2330 | `205c3074d5e7f891fbbb61af194526e2ba20cd3effbf6b9771c07923b0135147` | `68fad804ec5946cb296f77dc5b336308a66abf12`, `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` |
| `344a65063ec55c4bd479` | `history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_audit.json` | 1363 | `9e874f560a3bb871b72bccddd73f632594ce423bf8cd3f2f02401f1682ab693b` | 同上 |
| `f912d84d3c0b5416f225` | `history/source/notes/customer_attraction/transport_round/local_security_increment_initial_3227_independent_audit.json` | 102448 | `5a4dafb5d0ad3a8fe00bc3a9550edd5347522d1bc2e0bc5008509b8c7dd9a4d8` | 同上 |

独立审计的 `source_sha256.input` 为输入文件的 `205c…35147`，`source_sha256.certificate` 为已经入库的 certificate 文件 `4f458…b9e8`。因此它明确连接输入与既有 certificate，而不是另一个客户实例。三个源的原字节和本轮核验脚本均保存在 `security-chain-boundary/original/transport-round/`。

## 输入模型

输入文件声明 3 名提供者、6 个主题 `X0,X1,X2,Y0,Y1,Y2`，有 22 个客户类型。每行给一个主题子集和整数 `multiplicity`；所有 multiplicity 之和为 3227。客户按单位权展开，允许重复主题集合和空离轨历史的完整顺序策略解释由审计文件承接。该文件只定义客户数据，不声明策略、均衡或福利结论；不能仅凭输入文件推出 SPE。

## 顺序审计的有限结论

`audit.json` 报告 `status=PASS`，在 43 个完整有序决策历史上比较每个历史的 6 个动作，共 258 个比较；严格负 slack 为 0，平局 92。选定策略的路径为 `[0,3,4]`，三位提供者效用为 `(888,1041,1021)`，总福利
\[
W=2950.
\]
所有客户最优三主题覆盖的有限整数值为 `OPT=3227`，所以双倍 half 余额为
\[
2W-OPT=5900-3227=2673>0.
\]
该摘要还给出全局安全值
\[
V_3=\frac{8734869174}{9663953},
\]
根动作固定为 0 后剩余两位的局部安全值 `V_2=906`。根的六个实际续局支付均为 888。

审计中的两个一步安全值差额为
\[
 u+2V_2-3V_3=-\frac{111934422}{9663953}<0,
\]
以及弱式
\[
 u+\tfrac32V_2-\tfrac52V_3=-\frac{122270544}{9663953}<0.
\]
这两个负数只说明把局部安全值按这两种**逐步统一不等式**强行连接是不成立的。相反，聚合桥余量
\[
\frac{2304053828}{9663953}>0
\]
和全局弱桥余量
\[
\frac{6671488415}{9663953}>0
\]
均为正；因此该实例不是聚合安全桥的反例，更不是六人 `Q-CAG-HALF` 反例。

## 独立 Fraction 审计的增量

独立文件声明 `method = Independent Fraction checks; no project/witness-verifier imports`，完整保存每个历史、规定动作、五个偏离动作的终局和精确 payoff。其字段给出：

* 43 个决策历史、216 个终局历史、258 个动作比较；
* 0 个负比较、92 个零 slack；
* 路径 `[0,3,4]`、效用 `(888,1041,1021)`、`welfare=2950`、`optimum=3227`；
* 四个最优支持：`[0,2,5]`、`[1,2,5]`、`[2,3,5]`、`[2,4,5]`；
* 全局鞍点的 primal minimum、dual maximum 和 value 都是 `8734869174/9663953`；
* 固定前缀 `[0]` 后的局部鞍点 primal/dual/value 都是 `906`，其 primal 为 `[0,1/2,1/2,0,0,0]`，dual 对 `[1]`、`[2]` 的权重分别为 `3/5`、`2/5`；
* 432 个背景矩阵嵌入恒等式被检查，完整望远镜项为 `(-111934422/9663953, 250, 0)`，弱式项为 `(-122270544/9663953, 385/2)`，末位弱 slack 为 `1021/2`；
* `mathematical_errors_in_witness` 为空。

源文件的 `scope` 采用与摘要略不同的措辞，但语义相同：它否定两条普遍局部一步式，不否定 aggregate bridge 或 half coverage。独立审计还记录下标提示：路径索引的 `V_n` 表示末位安全值，而 telescoping 使用根值 `V_1`（也记为 `v_n(0)`），不可把二者混写。

## 本轮独立核对

`verify_3227_audits.py` 只用 Python 标准库和 `Fraction` 读取上述三份原字节，未导入项目求解器或验证器。它重算并通过：输入 multiplicity 总和 3227；22 类、43 历史，每个历史恰有 6 个备选动作，258 比较覆盖 216 个唯一终局；所有 slack 非负且恰 92 个为零；独立审计声明的输入 SHA 与输入原字节一致；摘要和独立审计的路径、福利、OPT、`V_3`、`V_2` 全部一致；全局与局部鞍点 primal=dual=value；`2W-OPT=2673`；两审计的范围说明都包含“局部一步式失败而 aggregate/half 未被反驳”。核验输出为 `pass=true`。

这一步是对冻结 JSON 的一致性和精确字段复核，不是重新运行缺失的原始生成程序，也不把源文件中的 `PASS` 升格为一般数学证明。相关命令：

```sh
python3 archives/customer-attraction/tools/evidence/security-chain-boundary/original/transport-round/verify_3227_audits.py
```

## 与既有对象的关系和处置

* 与[早期3227安全值增量证书](../../../../../archives/customer-attraction/state/计算/早期3227安全值增量证书--计算.md)是同一 3227 客户、六主题、三提供者实例。既有对象承载 certificate 的 `strategy`、`security_global` 和 `security_after_root`；本增量承载输入、顺序审计全局摘要及独立审计的 258 条逐历史记录，不能把三份源误记为另一个证书。
* 与[安全值链与五人逐人安全值的精确核验](../../../../../archives/customer-attraction/state/计算/安全值链与五人逐人安全值的精确核验--计算.md)中已重放的 113 客户规范版本不同。113 客户版本的数值不能替换本处 3227 客户数值；本批也不声称重新运行 113 客户程序。
* 与[真实前缀逐步安全值付款](../../../../../archives/customer-attraction/state/反例/真实前缀逐步安全值付款--反例.md)相容：局部安全值和局部付款可以为负而全局桥余量为正。这里的 `2673` 是 `2W-OPT` 的双倍余额，不能写成未加倍半覆盖余量。

正确语义处置为：三个来源均 `integrated` 到本增量审查；输入保留为有限模型定义，顺序审计保留摘要字段，独立审计保留精确逐动作与鞍点证据。它们共同支持“两个局部一步式不是普遍定理”的有限证书，不支持任意客户数、任意完整 SPE、聚合安全桥或六人 half 的全称结论。

## 接续

第三阶段可以把本对象接到既有 3227 certificate、局部一步安全值障碍和聚合安全桥对象；每条边必须保留不同源版本的输入/证书身份及 `2W-OPT` 的双倍口径。若要构造新的反例或一般定理，仍需在允许重复主题、完整有序历史和实际客户价值均分的原模型上重新证明，不能从这三个有限 JSON 文件外推。

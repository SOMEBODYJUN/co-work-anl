---
kind: source-review-draft
source_id: 6d08e55bce1a5336932c
source_path: examples/customer_attraction/prefix_coupled_seats_strict.json
source_sha256: 8fa88f66e5ebf2bdc8239f61d2e0ee32b2c49786edc05a6308d30b5ba2304ccc
status: ready-for-parent-review
recommended_disposition: integrated
recommended_targets:
  - archives/customer-attraction/state/审查/前缀耦合席位与尾水位边界增量审计--审查.md
  - archives/customer-attraction/tools/evidence/cag-20261023-20261030/manifest.json
---

# 严格前缀耦合席位输入的语义清洗

## 来源和输入语义

冻结源 `6d08e55bce1a5336932c` 是 1486 字节的 JSON 输入夹具，两个冻结版本内容相同，SHA-256 为 `8fa88f66e5ebf2bdc8239f61d2e0ee32b2c49786edc05a6308d30b5ba2304ccc`。它给出 5 个主题、3 名顺序玩家、11 类客户兴趣集合及重数，总客户数为

\[
15+14+14+11+15+14+3+9+5+13+11=124.
\]

输入中的 `path=[0,4,2]`、`welfare=95`、`new=127/2`、`old_combined=184/3` 和 `gap=13/6` 是结果夹具字段；JSON 本身没有策略动作表、SPE 证明或偏离收益定义。不能把这些字段单独读成完整结论。

客户类型逐项为

\[
\{0\}:15,\ \{1\}:14,\ \{2\}:14,\ \{0,2\}:11,\ \{3\}:15,\ \{0,3\}:14,\ \{2,3\}:3,\ \{4\}:9,\ \{0,4\}:5,\ \{1,4\}:13,\ \{2,4\}:11.
\]

## 已有完整证据如何承接

同批冻结的 `customer_attraction_prefix_coupled_seats.json` 明确标记 `source JSON contains no strategy; independently completed one full SPE realizing its path`。现有审计对象已独立补全全部 31 个有序决策历史、155 项含自身比较（124 项真正偏离），得到实际路径 `(0,4,2)`、收益 `(37,30,28)`、福利 `W=95`，并以 `(0,1,2)` 见证 `OPT=100`。最小 slack 为 0，121 项严格比较、34 项平局；因此这是合法完整纯 SPE 的有限实例，不能称严格均衡或由输入夹具本身推出。

五个主题都标为 maximal。其 `private_sizes=(15,14,14,15,9)`，`omitted_private_sizes=(0,14,0,15,0)`。这些是席位计算使用的私有质量，不能替换为真实终局每个玩家的收益。

三条位置行的精确字段为：

| 位置 | 实际利润 | 新 lambda | 旧最大值 | 新旧差的贡献 |
|---:|---:|---:|---:|---:|
| 1 | 37 | 15 | 15 | 0 |
| 2 | 30 | 41/2 | 55/3 | 13/6 |
| 3 | 28 | 28 | 28 | 0 |

故新席位总和为 `127/2`，旧逐位置最大值总和为 `184/3`，差为

\[
\frac{127}{2}-\frac{184}{3}=\frac{13}{6}.
\]

这证明该具体三人完整 SPE 上的前缀耦合席位聚合严格改善旧界；它不是任意玩家数或任意 SPE 的半覆盖支付定理。已有正文还保留 124 客户的单位展开、动作表、Fraction 核验和证据 manifest，因此本 JSON 应作为原始输入身份接入该对象，而不是新建第二个“前缀席位”对象。

## 处置和边界

建议将来源标为 `integrated`：

1. 输入身份、客户类型和哈希接入 `前缀耦合席位与尾水位边界增量审计--审查.md`；
2. 由 `archives/customer-attraction/tools/evidence/cag-20261023-20261030/manifest.json` 和既有 `customer_attraction_prefix_coupled_seats.json` 保留完整结果证据；
3. 不把 `gap=13/6` 单独当作普遍结论，也不把 `W=95<OPT=100` 当作六提供者 half 反例。

该源与同批水位 JSON、任意人数联合席位解析证明、完整 SPE 审计分别保持身份。继续使用时应同时给出 31 历史、124 偏离、`W=95`、`OPT=100` 和两种席位总和；输入夹具没有外部文献、新颖性认证或六人全称结论。

复现边界：先用 `clean show 6d08e55bce1a5336932c` 导出并核哈希，再运行既有 `customer_attraction_prefix_coupled_seats` 审计；不要把本 JSON 当作包含策略的自足验证器。

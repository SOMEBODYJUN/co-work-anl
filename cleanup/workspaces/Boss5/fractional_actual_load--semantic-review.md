---
kind: source-review-draft
source_id: 107f7f83354596e1ffd4
source_path: examples/customer_attraction/fractional_actual_load_failure.json
source_sha256: fba8f2ed045b903d639d666e4b43333ac8e5671cce89d7c69d013c81ca587f72
status: ready-for-parent-review
recommended_disposition: integrated
recommended_targets:
  - archives/customer-attraction/state/计算/分数负载四主题族的全历史核验--计算.md
  - archives/customer-attraction/tools/evidence/fractional-load-boundaries/source-manifest.json
---

# 分数实际负载输入夹具的语义清洗

## 来源和实际读取

冻结源 `107f7f83354596e1ffd4` 的路径是 `examples/customer_attraction/fractional_actual_load_failure.json`，源 SHA-256 为 `fba8f2ed045b903d639d666e4b43333ac8e5671cce89d7c69d013c81ca587f72`，在两个冻结提交中内容相同。JSON 本身是四人、四主题、17 名单位客户的输入夹具；它不独立定义策略、SPE 或静态查询分布。

主题按 `0=A, 1=B, 2=Q, 3=D` 编码。四类客户为 `A:3`、`Q:1`、`AD:1`、`BQD:12`，总数为 17。该输入与既有证书和策略的客户重数逐项一致。

## 与既有完整数学对象的关系

既有 `分数负载四主题族的全历史核验--计算.md` 已承载该夹具的全部数学语义：统一的四主题完整纯 SPE 构造、85 个有序决策节点、255 个真实偏离比较、原路径 `B,B,B,A`、终局福利 `W=16` 和最优覆盖 `OPT_4=17`。该输入配对的冻结证书和标准库审计实际重放通过，最小 SPE 松弛为 0；四位玩家收益均为 4。

本次从原审计入口重跑，输出与既有对象一致：查询值为
\[
(16/7,48/13,61/13,388/91),
\]
实际分数负载最大值 `M=61/13`，覆盖查询总量 `G=544/91`，粗弱桥差为 `11/26>0`，精确税桥余额为 `292/91>0`，而 `2W-OPT_4=15`。因此该夹具只参与反驳“用实际均匀缩放负载支付弱桥”的辅助接口；它不反驳真实静态安全值聚合，也不是六人 half 反例。

既有审计还对同一解析策略族的 `m=2,3,4,5,6` 做了有限完整树回归（节点 5、21、85、341、1365），并明确任意 `m` 的结论依赖解析证明而非枚举。该回归中的 `m=4` 项正是本源夹具；不要把其他族输出倒填成这个 JSON 的直接内容。

## 独有内容和处置

该 JSON 的独有贡献是可复现的紧凑客户输入与源版本/哈希身份。它不是独立证书、审计脚本或新反例。建议标记 `integrated`：将两 `source:` 引用和 `source_sha256` 补进既有计算对象，并确认 `fractional-load-boundaries/source-manifest.json` 的输入条目与该哈希一致。无需新建数学对象，也不应标记 `duplicate`，因为本次源版本的逐文件语义处置尚未被单独记录。

建议复现：

```sh
python3 archives/customer-attraction/tools/evidence/fractional-load-boundaries/original/tests/audits/customer_attraction_fractional_actual_load.py
```

审计输出应保留 `concrete_full_history_audit` 与 `family_full_history_audits` 的范围字段；有限重放不扩大为任意模型或六人 half 证明。

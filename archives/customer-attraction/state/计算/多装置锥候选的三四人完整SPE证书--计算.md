---
id: customer-attraction/multigadget-spe-certificates
kind: computation
type_tag: 计算
status: exact-finite-certificates-m3-m4
truth_status: complete-pure-spe-witnesses; finite-family-only; no-half-theorem
source_refs:
  - clean:aae47277d64d22d4a121 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/multigadget.py
  - clean:4965c677e7d2d6835222 research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/multigadget_m3.json
  - clean:070355aa559a4a7a07ad research/workspaces/customer-attraction/R-27557809587746c59216a46867c9eb07/direct_global/multigadget_m4.json
  - related:archives/customer-attraction/tools/evidence/exact-spe/customer_attraction/model.py
  - related:archives/customer-attraction/tools/evidence/exact-spe/customer_attraction/exact.py
  - related:archives/customer-attraction/tools/evidence/exact-spe/customer_attraction/certificate.py
evidence_paths:
  - archives/customer-attraction/tools/evidence/R275-multigadget-spe-certificates-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/R275-multigadget-spe-certificates-20261031/replay/verification.json
  - archives/customer-attraction/tools/evidence/R275-multigadget-spe-certificates-20261031/source/multigadget.py
  - archives/customer-attraction/tools/evidence/R275-multigadget-spe-certificates-20261031/source/multigadget_m3.json
  - archives/customer-attraction/tools/evidence/R275-multigadget-spe-certificates-20261031/source/multigadget_m4.json
---

# 多装置锥候选的三四人完整 SPE 证书

## 1. 构造的真实定义

源程序令 `k=m-1`、主题数 `p=3k+2=3m-1`，并把前 `k` 个索引分成两两客户对。对每个 `i=0,…,k-1`，加入

\[
\{i,k+2i\},\qquad \{i,k+2i+1\}
\]

两个乘数为 2 的客户类型；再加入两个单主题 `{B}`、`{T}` 类型（各乘数 3），以及两个把所有中间主题与 `B` 或 `T` 连接起来的类型（各乘数 2），其中 `B=3k`、`T=3k+1`。这是源代码的确切构造，不是从摘要反推的模型。

因此两个已冻结实例分别是：

| 文件 | 玩家 | 主题 | 客户类型 | 单位客户数 | 证书终局计数 |
|---|---:|---:|---:|---:|---|
| `multigadget_m3.json` | 3 | 8 | 8 | 18 | `(1,1,0,0,0,0,1,0)` |
| `multigadget_m4.json` | 4 | 11 | 10 | 22 | `(1,1,1,0,0,0,0,0,0,1,0)` |

模型是单位客户、同一有限目录、每个玩家选一次、被覆盖客户在占用主题间均分的模型。证书和求解器都只讨论纯策略 SPE；混合行为均衡没有被导入。

## 2. 完整证书和独立核验

`multigadget.py` 对 `m=3,4` 调用 `ExactSPESolver.outcomes()`，并要求路径 `0,1,…,m-2,B` 的目标计数属于可实现终局集合；实际输出为 `target=True`，可实现终局计数集合大小分别为 18 和 32。随后 `certificate(..., on_path=...)` 生成完整有序历史动作表。

我用保全的 `model.py`、`exact.py` 和 `certificate.py` 重新读取 JSON，并用不调用求解器的 `verify_certificate` 逐历史检查：

| 实例 | 目标收益向量（占用主题） | 福利 | OPT | `OPT/welfare` | 历史动作数 | 偏离检查数 | `verify_certificate` |
|---|---|---:|---:|---:|---:|---:|---|
| m=3 | `(4,4,5)` | 13 | 14 | `14/13` | 73 | 511 | pass |
| m=4 | `(4,4,4,5)` | 17 | 18 | `18/17` | 1464 | 14640 | pass |

这里的 `OPT` 是模型中对至多 `m` 个主题支持做有限枚举得到的覆盖最优值；它只用于这两个实例的比较。`verify_certificate` 的 73/1464 个历史和 511/14640 个偏离检查覆盖证书树的全部有序历史，故这两份是完整纯 SPE 证书，而不是只核根路径的摘要。

## 3. 能够、不能够推出的结论

这两份证书确实证明：上述两个具体客户目录中，目标终局计数各自由一个完整纯 SPE 策略实现，且其福利与该实例的枚举 OPT 如表。它们同时提供了一个可运行的构造基准：`m=3` 有 18 个单位客户，`m=4` 有 22 个单位客户；源脚本运行分别报告 18、32 个可实现终局计数。

它们没有证明目标是最坏纯 SPE，也没有证明任意 `m` 都有同样证书，更没有给出六人、六主题以上或半覆盖阈值的反例。`m=3` 的 `14/13` 和 `m=4` 的 `18/17` 反而接近 1；不能据此宣称一般半因子紧性。任何从 `m=3,4` 归纳到任意 `m` 的公式都只是候选模式，必须另给所有 `m` 的完整历史证书和偏离证明。

## 4. 与已有对象的衔接

本对象与前一批 q32、R275 固定锥/随机锥记录的关系是：q32 与锥对象主要提供固定策略或有限 LP 诊断；这里则直接使用完整有序历史纯 SPE 证书和独立验证器。因而它可作为后续比较“锥候选是否真的落在完整 SPE 空间内”的基准，但不能反向把其他锥对象升级为 SPE。

它也与现有 `ExactSPESolver` 审计合同一致：求解器缓存的是每个计数前缀的全部可实现终局集合，不把续局强行 Markov 化；证书验证器逐有序历史枚举全部动作和真实偏离。当前唯一保留的开放项是把这一具体构造推广到任意 `m` 并同时控制最小纯 SPE 福利，这不在三份源文件的证明范围内。

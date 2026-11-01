---
id: cag-r373-fixed-bridge-mult3-source
kind: evidence
type_tag: 审查
title: R-373 固定桥 mult=3 源版本的精确核对
status: finite-obstruction
summary: 六个主题、三个顺序玩家的固定完整策略锥中，mult=3 的有理桥扫描输出；整数克隆实例和 43 个有序决策历史的纯 SPE 证书可精确复核，但只说明该固定锥的桥模板失败，不是六人 half 反例。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json
---

# R-373 `fixed_bridge_mult3.json`：固定策略锥桥筛的精确源版本

## 身份与实现语义

源文件是 `R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_mult3.json`，源版本 ID 为 `3c4874a0fc772404d552`，1880 字节，SHA-256 为 `c3b17b2b8b9e03caafcd3656ddb6904613e1430b5e75f9c3348310e09f283d84`。它是 `fixed_bridge_attack.py` 对固定完整策略锥的 `mult=3` 输出，而不是独立的新搜索器或一份 LP 对偶证明。

实现中的 `p=6,m=3` 具有明确含义：`StrategyCone(topics=p, players=m, ...)` 和 `instance_from_clones(p,m,...)` 使用六个带标签主题、三个顺序玩家。这里的 `p` 不是提供者数、`m` 也不是主题数；把它写成“六提供者/三主题”会错置模型。当前六提供者 Q-CAG-HALF-6 的主量词不能由此源直接继承。

`weights` 按非空主题子集的位掩码顺序编码 63 类客户，策略树在深度 0、1、2 给出全部 $1+6+6^2=43$ 个有序历史的动作。`terminal_counts=(1,0,0,1,1,0)` 表示根路径选择主题 `(0,3,4)`。

## 精确字段与重放

源记录的固定筛参数为

- `mult=3`，候选组合 `portfolio=(1,2,5)`；
- 有理筛目标 `objective=-123/206`；
- 63 个主题子集重数向量之和为 164，非零位置 15 个；
- 根路径 `(0,3,4)` 的玩家收益为 $(69/2,73/2,32)$，福利 $W=103$；
- 同一六主题、三玩家实例的覆盖最优值为 $OPT=145$。

用冻结依赖包中的 `StrategyCertificate`、`verify_certificate`、`integer_clones` 和 `instance_from_clones` 重建实例后，源的整数重数向量不再缩放，完整证书验证通过：43 个决策历史和所有对应偏离均检查，收益、$W$、$OPT$ 与源字段逐项相等。`2W-OPT=61>0`，所以该具体完整纯 SPE 仍满足 $2W>OPT$；它不是当前 half 目标的反例。

## 桥筛究竟否定什么

`fixed_bridge_attack.py` 对每个三主题 `portfolio` 计算

\[
 v_{P}-w-3u,
\]

其中 $v_P$ 是该组合的覆盖行，$w$ 是固定策略锥的福利行，$u$ 是根动作的玩家收益行；随后在非负策略锥与 $w\cdot q=1$ 的归一化截面上做有限 LP，并对接受的顶点恢复有理整数克隆。`objective=-123/206` 只是这个固定策略锥、固定乘子 3 和该候选组合下的最大有理目标值为负，说明该桥证书模板没有得到正裕量。它不量化所有 SPE、所有主题组合或所有客户分布，也不证明任何普遍不等式的否定。

同一脚本的 `mult=2` 兄弟源（ID `7cdb308f85a723cb0b0d`）给出另一实例：目标 `-6/23`、路径 `(0,3,4)`、组合 `(1,2,4)`、收益 $(48,48,42)$、$W=138$、$OPT=198$。两份源分别保留；`mult=3` 不是对 `mult=2` 的重复拷贝，而是同一固定策略证书在不同乘子下的独立输出。

## 处置与接续

该源应 `integrated` 到既有对象 `archives/customer-attraction/state/障碍/R-373d耦合桥与计数MILP有限证书--障碍.md`，并保留本源的 JSON、SHA、完整策略摘要与精确验证报告；不得把它单独升级为当前六人六提供者 half 定理、真实通用桥反例或所有完整 SPE 的结论。后续若研究一般桥，必须改变量词并重新证明：遍历任意完整历史策略、任意平局与重复主题，且给出真实客户实例的全量 SPE 激励核验；本源只能作为固定锥模板失败的有限障碍和可复用的精确回放输入。

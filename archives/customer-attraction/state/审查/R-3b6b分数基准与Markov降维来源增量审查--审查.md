---
id: "customer-attraction/r3b6b-fractional-global-proof-source-increment"
kind: "review"
type_tag: "审查"
title: "R-3b6b 分数基准与 Markov 降维来源增量审查"
status: "finite-exploration-sources-retained"
truth_status: "finite-numerical-searches-and-scoped-exact-witness; no-universal-half-conclusion"
review_level: "full-source-read-and-cross-compared-with-R3b6b-obstacle-objects"
scope: "Six R-3b6b global_proof/structural_reduction source versions"
summary: "三份分数基准搜索、一个最大主题启发式、一个 Markov 报告和一个 exact witness 提取器共同补全 R-3b6b 的有限来源链。分数工具是 SLSQP/随机筛查；Markov 报告是固定三人四主题的有限证书构造。它们均不证明六人 Q-CAG-HALF。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/global_proof/fractional_explore.py#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/global_proof/search_fractional.py#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/global_proof/search_fractional_floor.py#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/global_proof/search_maxsize.py#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/boss_markov_alternative.json#source"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/structural_reduction/extract_markov3.py#source"
evidence_paths:
  - "archives/customer-attraction/tools/evidence/R-3b6b-fractional-global-20261101/original/"
related_objects:
  - "archives/customer-attraction/state/计算/R-3b6b有限残余循环锥搜索--计算.md"
  - "archives/customer-attraction/state/障碍/R-3b6b最后平均选择严格SPE边界与最小支付搜索--障碍.md"
  - "archives/customer-attraction/state/障碍/R-2fc分数地板与安全动作有限探针--障碍.md"
---

## 分数 benchmark 与三类随机筛查

`fractional_explore.py`（1169 字节，SHA-256 `54f30639ccaa3305010ba51370ff8c5e2fee1079767510f7e83997300db1b162`）把客户关联矩阵、整数重数和计数前缀转成连续分数 benchmark。令 `r=n-Σb`、`z=Cb`；`r=1` 时返回
\[
M(b)=\max_a\sum_x C_{xa}w_x/(1+z_x),
\]
`r>1` 时用 SLSQP 在单纯形上优化
\[
\sum_xw_x\log(1+z_x+(r-1)(Cq)_x).
\]
返回的 `g·q` 和 `max(g)-g·q` 只是一次浮点候选与 KKT 样残差，没有全局最优证书、有理误差界或离散策略实现。源码首行已明确数值发现不是证明。

`search_fractional.py`（源 `2eb5e65540a85e23fdeb`，SHA-256 `4fb30eeb9b32c4ef24084d76941289d78f36ae47301fa80b0cc23e4426355549`）固定 seed `6709884`，对 `n=3..6` 各 100 个 `k=7` 随机实例，检查 `D=u+(n-1)V(e_a)-nV(0)`，只有 `D<-1e-4` 才写 obstruction。`search_fractional_floor.py`（源 `f34f2dceb0a09e0b629a`，SHA-256 `f346d8c5e1cb8a72dd2a77ad4df03869dedc4978e52a495af62c431a219bfa8f`）固定 seed `77128912`，每个 `n=3..6` 做 200 个 `k=6` 实例，比较 exact 根 floor 与浮点 benchmark，并筛查静态 safe-action 见证。`search_maxsize.py`（源 `08145efe1e5aefe4cf92`，SHA-256 `af52a3e6d65e234f34a1fc181008c0ae901a49c8d9911f8da326b4d909cd7ef1`）固定 seed `883`，每个 `n=3,4,5` 做 1000 个 `k=6` 实例，只检查按静态客户需求选出的一个最大主题。

后三个程序均是有限随机/组合筛查。没有冻结 obstruction 输出；未触发写文件不等于全称不等式成立。`ExactSPESolver` 给出的根 floor 是精确有限递推，但 benchmark 仍是 SLSQP 浮点候选；最大主题筛选也不要求候选终局来自任何完整 SPE 历史。

## Markov 报告与有限 exact witness

`boss_markov_alternative.json`（源 `a8d3de786e77e4336c5a`，3830 字节，SHA-256 `e71cde81a4608b55c8187e2083e8b4e4d130c021d64f3b400cc386af001f916a`）给出一个固定三人、四主题、六类客户重数的终局计数 `[1,0,0,2]`、完整动作表和 10 个二步计数状态。`extract_markov3.py`（源 `0fcebf2f4f2f4fd36ce8`，2057 字节，SHA-256 `7ce0df18c8abfee36ffa29452c78044585ee2b23ce01282684cfac0d7ab1325b`）枚举二步计数的末位最佳菜单，构造根/第二位动作，再调用 `StrategyCertificate` 与 `verify_certificate` 检查完整有序历史。

这是一份固定实例的有限证书构造；生成阶段使用计数状态，不能把一般模型限制为 Markov 策略。即使该证书通过，也必须单独核对 `W`、`OPT` 和 `2W-OPT`，不能直接迁移为六人 half 反例。它应与已有 R-3b6b residual-cycle、last-player 和 R-2fc fractional-floor 障碍分开。

## 失败机制与处置

分数工具的主要限制是 SLSQP 局部性、没有误差界、连续 `q` 不等于离散行动和有限随机样本；Markov 提取器只认证给定小实例，未枚举所有完整策略。六个源版本均保留为 `retained` 的有限探索/证书生成材料，不创建新的定理或反例对象。若后续出现浮点 obstruction，必须恢复整数客户重数、逐有序历史验证完整 SPE、精确计算 `OPT` 与 `2W-OPT`，再改变数学状态。

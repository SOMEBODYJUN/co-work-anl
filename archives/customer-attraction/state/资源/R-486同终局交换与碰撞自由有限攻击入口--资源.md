---
id: customer-attraction/r486-credible-same-terminal-exchange-checkpoint
kind: resource
type_tag: 资源
title: R-486 同终局交换与碰撞自由有限攻击入口
status: readme-scoped; conditional-obstruction-not-general
truth_status: navigation-and-conditional-claim-only
summary: "R-486 credible README 记录同终局交换引理、条件负载失真完美匹配证书和有限 MILP 审计入口；不含其证明正文、一般匹配存在性、完整 SPE 证书或六人半覆盖结论。"
source_refs:
  - "clean:f51dcc0ad5619beb9b24"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/credible/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-486bb9adb8cd4d9a940dbf3b1ab0b1de/credible/README.md"
source_sha256: "5c8b0614a226c4e2cf1fa3b16e3785e436d7307fe25748adeeaae75a37d8051e"
related_objects:
  - "customer-attraction/collision-free-family-welfare-obstruction"
  - "customer-attraction/five-client-collision-free-load-bridge"
  - "customer-attraction/r2fc-global-proof-eight-source-audit"
  - "customer-attraction/tail-price-certificates-cannot-replace-complete-continuation-incentives"

evidence_refs:
  - "../../tools/evidence/r486-credible-readme-20261101/source-README.md"
---

## 来源性质与当前可确立范围

该 2083 字节 README 是 R-486 工作区 `credible/` 的 checkpoint 导航，日期为
2026-10-21。它明说：没有得到 genuine Q-CAG-HALF 反例，也没有一般半覆盖证明；
本文件只描述该目录及其下一步，不能代替目录中被引用的证明稿、程序或审计 JSON。
因此本对象把它作为资源入口保存，不能把 README 的摘要升级成定理、完整策略或
新颖性声明。

README 指向的主要数学入口是 `common_terminal_exchange.md`：它声称一个“同终局
交换”引理和条件的负载失真 perfect-matching 证书。摘要中的承重条件是：比较来自
同一个完整有序历史纯 SPE，两个比较都是真实的偏离/回复比较，并且终局相等和负载
条件显式写出。按 README 的表述，若早期与末位惩罚者返回同一最终多重集、其他组
不受影响，则该证书可阻止把已有碰撞自由 3/2 族简单推广为更多惩罚者后得到更好
渐近比率。该结论仍是**条件路线**：惩罚者内部奖励、共同 reservoir 重叠、异质组
大小和惩罚者数量虽被声称允许，但匹配存在性、所有 SPE 的适用量词和完整证明正文
不在本 README 内，需逐源读取 `common_terminal_exchange.md` 及其依赖后才能升级。

## 已知有限审计的准确边界

README 另指向 `common_terminal_audit.py/.json`，称其对 14 个 literal cases 做
expanded-unit arithmetic。该审计应保存为有限障碍证据；它不是完整策略证书，也
不能从“14 个案例”推出任意客户目录、任意人数或六人模型的普遍不可能性。

`collisionfree_joint.py`、`cf_m3p6.json`、`cf_m4p7_failed.json` 是两个低信息
有限 MILP 尝试。README 的准确摘要是：m3,p6 的 ratio-one endpoint 有完整动作图，
并在全部有序历史上做了 exact verification；m4,p7 没有保留下来的候选，失败报告
只应如实记录为一次有限运行失败。README 没有给 solver upper bound，不能把超时、无
候选或浮点结果解释成最优性证明。

## 与既有对象的关系和防止重复升级

现有的[任意 (k) 碰撞自由完整纯 SPE 族](../反例/三人碰撞自由族福利障碍--反例.md)
已经证明存在路径的 (\operatorname{OPT}/W\to3/2)，且只给统一纯负载桥的
(f(1)\ge3/2) 必要条件；[五客户无拥挤障碍](../反例/五客户无拥挤SPE负载桥障碍--反例.md)
和 R-2fc 审计则固定了 exact obstruction 的客户与全历史范围。R-486 README 的
同终局交换路线与这些对象相邻，但没有把“完美匹配条件对任意 SPE 总能成立”证明
出来；README 还明确提醒该条件可能失败。因此不能把它改写为统一的 3/2 上界，
也不能声称 t>2 惩罚者推广已被普遍排除。

既有[尾部价格证书不能替代完整续局激励](../障碍/尾部价格证书不能替代完整续局激励--障碍.md)
已经确立静态尾价不能替代完整后继 SPE 的方法边界。R-486 README 与其一致：
每个有限比较必须保持原完整策略和真实离轨回复；`common_terminal_audit` 的
有限算术不能替代全树 IC。

## 需要后续源级读取的开放义务

1. 逐源读取 `common_terminal_exchange.md`，核对同终局等式、负载失真项、匹配图的
   顶点/边定义和其适用的惩罚者量词；在没有这一步前，本文只保留 README 的条件摘要。
2. 逐源读取 `common_terminal_audit.py/.json`，确认 14 个案例的客户输入、完整历史
   数量、Fraction/浮点状态和是否确实为同一策略树；不得把“expanded-unit”写成一般
   证明。
3. 逐源读取两个 MILP 文件和失败报告，区分 m3,p6 exact endpoint、m4,p7 failed
   run、候选策略是否完整，以及任何 timeout/infeasible 的真实含义。
4. 若将来证明匹配条件可由任意完整 SPE 产生，仍需在原六人、六提供者、允许重复、
   空主题、零客户和任意平局的模型中重做量词；该 README 本身没有六人半覆盖结论。

本资源的用途是给第三阶段提供准确关系入口：它把“同终局交换的条件路线”“已有
碰撞自由 3/2 障碍”和“有限 MILP 失败”分开保存，避免导航摘要被误读为一般证明。

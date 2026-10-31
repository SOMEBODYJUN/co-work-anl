---
id: unrelated-machines/single-circuit-exact-first-priors-rational-parameter-version-evidence
kind: review
type_tag: 审查
title: 真单环审查的Exact先序与有理参数版本证据
math_scope: single-physical-circuit-with-full-config-path-and-true-optimal-atoms
status: proved-specified-circuit-contract; no-general-elimination-impossibility
summary: 保两位先Exact独立构造与各自后读范围、root知情重构、两JSON仅canonical指纹差；D7不虚填矩阵消元秩，有限软件不当全调度枚举。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/configuration_preserving_single_cycle_endpoint_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/configuration_preserving_single_cycle_endpoint_review.md
---

# 真单环审查的Exact先序与有理参数版本证据

## 主载体完整实读与数学落点

本批全文读637行/41152B review，其中嵌入两份Exact先行稿和两份作者/最终实际读后稿；另读624行canonical及两份规范JSON全部字段。数学与三份真实原子/上界自足写在[三基态证明页](真单环双坏端点的三种实际基态与全支撑证明--审查.md)。读内嵌完整文本不冒称另取全部scratch原字节，其64位hash只作冻结来源元数据，不认证外部时间戳或当前新增盲审。

| 实际阶段 | 已读材料与不能倒填的独立性 |
|---|---|
| 共同Exact | 两审者都只收到d769a5237c0a7ab1e12db589e24ea536bf2bb5558480759069c740e7d8737cbc纯陈述，不读作者Proof/audit。 |
| common_capacity先行 | 自建pivot h+1基态、N真实原子/单环/端点证明和独立软件，冻4b41796a66c90a13d8d3ee4ed03f70ed0897fa1ad98934146876b5a06a5f3cdc。不是旧直和例当新前提。 |
| literature_mechanism先行 | 自建pivot h、不同E停车基态及上界，冻4739ec18947f6bef3dd5fd243d373b59d015a23b101c1bab530c1ef9d13eadad，软件/结果另冻；不是第一份基态的重新命名。 |
| 解封作者 | 作者Proof1be1946b438c2e3bbef5abac2a4d74b237887fa764c0b99dc80b5ab929ba5c4f使用railsD/D+1、跨block E回绕；两人各实际全文读后，与己稿的不同表逐job核。 |
| 最终canonical读后1 | bb7800430089ea541bdc5af5a8fcdec38dbf8d4c4c58cf9e8faf1eeede6d9f08：完整读a9c99…全稿含新§4及旧§1/2/3，**没读/跑作者audit，没新计算**。 |
| 最终canonical读后2 | a65a42bd3e58ff37323ef01072b3a16875a2c9816cd223ddfc0923746b35ebd3：新§4.1–4.8全文，旧§3非circuit尾段及必要context；不夸成全部旧前缀重审，没读/跑作者audit或据root消息冒领。 |
| root | 先收到作者数学梗概，再从unit停车matching独立重构/核D3/5/7/9/11，后完整读作者/两独立稿/读后记录、新canonical节和代码；此阶段知情，非盲审票。 |

两份独立稿原字节不回写；后知情读与先行证明分阶段保存，不计成四张独立票。旧27043B前缀在当前a9c99e79cc528a0a278a812708d410852c5c022a170bfe3ba5f5a5941c5a29d7逐字保留且SHA693ece…，不让新单环ID升级旧三个身份。

## 两个实际表述修正

作者冻结稿把全部路径证书权重笼统写O(logD)，漏一般有理θ可有任意大分母编码。最终§4.7区分初始/两端O(logD)、给定有理θ另计encθ，无有限编码实θ只仿射存在。它修复计算量词，不影响三份真实原子、circuit或任意调度端点下界。

“两个整数端点”易被误读为箱端点本身整数，最终改“两端点的整数支撑最优值”；实际每job仍≥2正分数端，峰B是限制实例**真实整数调度OPT**。没有任务固定为1，损失来自0端删除，不能拿旧固定任务核心的条件补全替换它。

首次冻结规范JSON仍引用旧canonical ef5125c858d0e7afd0e8bcfbc3b0d75a423530e3b77c56d011d67dcb5b990be0；修后另存rational_parameter输出SHA76ea1bf3816769936c728007ed024c96d3184e3747d77e9342e023fc8e3b963d。脚本c45446a1dc07a45ebef614452f8cecb23cb9e3b019b678055ac68cd2968f4c9b相同。本批完整读两raw JSON并逐字段比较：**唯一差异canonical_sha256**，其余数学/环境/命令字段同；它们不是两份不同数学族或两轮独立一般证明。

## 规范三参数的精确有限范围

原Python3.12.14/Fraction，命令为configuration_preserving_single_cycle_endpoints.py。两份JSON均scope明确无完整调度枚举/一般证明。

| D,L,N | 机/任务/有限端 | 原子 | circuit列 | 实际矩阵消元rank | CONFIG项检查 | 选定label匹配检查 | 端点实际上界 |
|---|---|---:|---:|---|---:|---:|---|
| 3,5,15 | 60/62/160 | 15 | 60 | 59 | 950 | 16 | 5/3 |
| 5,7,35 | 126/142/364 | 35 | 140 | 139 | 2100 | 64 | 9/5 |
| 7,9,63 | 216/254/648 | 63 | 252 | **null，未运行该矩阵消元** | 3690 | 256 | 13/7 |

三组合113原子、6740配置、336选定label所有外送子集的unit-matching检查；D7只核连通二度图并使用已证rank4N−1，不能把251填成实际消元结果。每组样本θ是−γ、−γ/2、0、γ/2、γ；数据字段initial_C_edge/max_box_steps均γ，base_hard_A/B为6/6、15/15、28/28。两端上界分配安排全部原jobs，但没有枚举全部端点调度，普遍下界来自任意调度论证。

原root重放同代码后的数学结果同，递归unit matching只为这些有限参数，不是任意规模生产后端。本批不重跑旧程序，只做字节/JSON字段比较，不把此比较说成新数学实验。

## 两份先行软件各自来源

common_capacity先读作者前自编audit712e336d8fc1263196e9ff12c8558641d6dd596bd3b2271fd5caad711ace2415，stdout7899893a0470545a3194ae4466e5ef23ce9f74690967916d40ebbaa63c726d11：D3/5/7/9/15/21/31全部N原子、5444198次原任务位置核验、42个CONFIG路径点、45260关键双外送局部模式、两端实际上界/单环守恒。未全枚举端点调度；这是其不同基态有限软件，不是canonical的113/6740计数。

literature_mechanism先行代码dfa763e01688c474d565ce85cfce28c06b10299f73e80e9014197d0e49dbc5b1，摘要d9dda4850b14179c5a6b7dbec6604dd0b2d278bb5cfc78cbaba6f4b101b18f7d，D3完整原子文件b4a02c7b8502e854867c4b90136e30d967a809dc10ccb5a861ca765b71caf28a。实际D3/5/7/9、各N不同真实原子、每D5个有理路径点、单环/Ad/秩恒等、无整数任务/两端完整上界/最小excessρ；D3全部15原子另显式保存。其后读作者/最终稿没有追加运行，也未取得/跑作者canonical代码。

审查只限指定circuit两个最大箱端点及永久删零端。support-minimal不是全矩阵最小基数；完整正支撑下界不是固定背景原子的失败。初态原子直接是OPT1，构造容易解，未排换方向、保存原子、回退重开或一般sub2算法。外审、优先权、独立成文价值均未认证。[原件/实际读取范围/版本比较](../../../../tools/evidence/um-foundation-composition-configuration-reviews/README.md)。

# 条件子树流与包含容量证书：最终规范稿实际读取冻结

日期：2026-10-18。审者：sol_true_hardness（6.1sol max）。scratch-only，仓库只读。

## 1. 精确文件与读取次序

规范路径：`co-work-anl-boss11/research/current/unrelated_machines/raw_sh3_conditional_subtree_flow_and_inclusion_capacity.md`。

本审者先实际全文读取该页 **202 行 / 19034 bytes** 的版本，SHA256 `1e513ab3803bbaf884fc6d3b159fbe15ef06c9078888c52042a33ca918bfe58e`，覆盖标题、正式身份表、第一至八节及末尾说明。
随后指出第四节“先将 a、f 同除以 p”又使用活动概率 a_u/p 的符号重赋值歧义。parent 修正文句并释放新 hash；本审者再实际定向完整读取第四节，同时做唯一替换的逆向字节核验。

最终版本是 **202 行 / 19125 bytes**，SHA256
`d36fa70bfea517257af13a0054432ed0dae65e4c623f5ffa1e9acecc178ba516`。
其唯一新句为：

> 仍令 a、f 表示第三节根质量 p 的流，不对这两个符号重新赋值。归一化后的行活动概率为 a_u/p，非活动概率为 1-a_u/p；active incoming 与 home 的条件边际仍按 a_u 归一。

精确替回原句后 SHA256 恰为 `1e513ab3803bbaf884fc6d3b159fbe15ef06c9078888c52042a33ca918bfe58e`，且新句只出现一次。因此本记录签的是“旧全文实际读 + 唯一差分实际读/逆向核验”，不虚称最终 hash 的又一次全新 blind review。

此前作者 v2 `011eab0db7ecc5f0b52e09b6d61b1241d46661711bbc1a76565f02f05cbef10d` 的全文读后记录单独保留为 `sol_true_hardness_raw_sh3_flow_inclusion_v2_author_read_after.md`，SHA256 `0d2c4fc28e203d04dbe49f5724ee0ee1b5c9097fbb35e15733034045a8900ecb`。所有此前 Exact-first、陈述先行重构、作者 Proof 读后记录都没有回写。

## 2. 最终稿中实际核到的数学付款

完整输入是明确的 native unique-home/unit-head DAG 加全部 unit-only entry jobs；sink 没有自有 jobs 或导出需求。入口 E 必是非 home unit endpoint。M3、原 degree-six ideals、全局 deg<=2 平方负载 localizers 与完整 row CONFIG first/pair 使用同一个 L。

unit-pair null 及其 deg-4 multiplier 提升合法，三投影 positivity 没有把任意 PSD 非对角元当成非负。条件 b_u/y_ujw 满足 per-token、per-arc、共同 head-cap；由 q=ER 的原 localizers 得实数 quota。DAG 前推确实重造只来自 v 的新 firstflow，不保给定矩，也不免费重排原实例其他 entry jobs。

第三节现在明确包括 root u。两种 >=quota / exact-quota flow 的 transition 在给定 rational point 下可先固定，DAG 路径分母乘积的 bit bound 已加入。迭代删除的零 marginal 全 degree-six moments 付款亦已加入：Boolean x 零列、xm 零列，再 restriction 保 ideals/M3/localizers；row CFG 的 first x=0 与非负支持排除该端。只删 unit heads，保留所有 home、原 jobs 和 k。

第四节最终记号不重赋值，活动概率 a/p、inactive 1-a/p 与 active 条件 f/a 一致。整数网格 hypersimplex 分解、finite polynomial support 与 incoming 标签配对均明确；非网格不外推 full CFG 或 ceil。k=1 借 incoming/home unit-pair 零矩的可选 out=a 单独列明，与 generic exact delta k 合同不混用。

第五至七节的包含族全 jobs/counts、H/M、共同终端预算、delta d1(delta d2-M)<=H、CONFIG optimum 一、完整路径上界、binomial/floor payment 都与先前独立重构一致。负系数分支独立处理，正 selector mass 由原 mandatory one-hot 支付。实 delta 通过较大的 rational T' 解释，未要求 exact 实数输入。固定多项式 q 损失、m>=100q 和 fixed rho 范围没有扩大。

此前指出的三项自足细节——iterated zero moments、flow bit growth、row normalization——在本次实际读取的最终文本中均已核到正确表述。未发现新的 standing fatal。

## 3. metadata 与未代签范围

正式 ID/version 为 `UM-RAW-SH3-CONDITIONAL-SUBTREE-FLOW-AND-INCLUSION-CUT-v2`。身份表正确分开新 firstflow、整数网格辅助 CFG、包含族 sound FAIL；其 scope 明说 UNKNOWN 不保证可行、不是原全局点、不是 raw SH3 gap 或主目标计算困难性。root 已知作者论证不计独立重构的历史也保留。

第八节现列了 source primary 的 root/作者实际 target-read 范围和软件版本、hash、重放方式。**本审者只实际读取了该页的这些 evidence 文字，没有读取对应 PDF、程序或冻结 JSON，也没有执行它们。** 不代签 120/85 数值、完整小矩审计或两次 byte-identical 运行；那些保留给实际执行者。q=2,m=6 小矩不属于大族渐近域的边界已写明。

本审者也没有读取或验证进一步 growing-depth/shared-owner 探索；最后一段对多路径 owner 重合的保留未被当成新定理。规范页不关闭一般 UM 正反面，没有从本必要 LP/辅助 CFG 输出一般真实 schedule 或源 decoder。

**最终冻结意见：对上述最终 hash，限定数学合同可由独立记录和本页自足证明核回，无 standing fatal；软件、primary 全文、新颖性及外审均不在本签名内。**

---
id: customer-attraction/heavy-block-singleton-individual-floor-saved-points
kind: computation
type_tag: 计算
title: 重块与单例目录的逐人floor保存点
status: 两原完整策略43与259行全读；以全重块解析证明认证保存点，原LP与2000探针均0运行
summary: 原归一是比较元组覆盖1并非保证其最优，整数候选才重核OPT；5/7客户点实际u全1/W3或4/OPT5或7，等弱2m−1门槛且高于2m，不是新反例。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/recursion/README.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/recursion/probe_floor.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/recursion/floor_discovery.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/recursion/floor_m4_discovery.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ab183d14fb74403091d09db766b05f73/independent/probe_disjoint.py
---

# 重块与单例目录的逐人floor保存点

4019B floor程序、4701/27909B两个JSON和1168B disjoint程序全部原字节/字段/函数读齐。JSON各10root字段、全部客户类型、43及259个有序策略行逐行读取并核完整历史域；[每行结构阅读记录](../../tools/evidence/independent-recursion-and-background-entry-versions-primary/floor-policy-complete-structural-reading.json)保索引/history/action/摘要。它不是仅看ratio头部，也不把结构读取称作求解器执行。原顶层LP模块未导入，两个探针均0原入口，当前数学认证依下面全历史解析证明，非旧verified字段或浮点最优值。

## 两份保存点的完整对象

六个标签0…5，各类客户为不同单位个体。

| 原文件 | m3保存点 | m4保存点 |
|---|---|---|
| trial字段 | 0 | 4 |
| 重块H客户数/覆盖标签 | 3人；0,1,3,4 | 4人；1,3,4 |
| 单例各一人/覆盖标签 | 2；5 | 0；2；5 |
| 物理不同主题数/标签数 | 3 / 6 | 4 / 6 |
| 所有规定动作 | 仅H标签 | 仅H标签 |
| 根有序路径 | (1,3,0) | (3,4,1,1) |
| terminal_counts | (1,1,0,1,0,0) | (0,2,0,1,1,0) |
| 完整非终局有序历史行数 | 1+6+36=43 | 1+6+36+216=259 |
| 每人实际利润/W/OPT | 全1；3；5 | 全1；4；7 |
| 保存ratio=u1/OPT | 1/5 | 1/7 |
| 保存comparison | (2,4,5) | (0,1,2,5) |

所有正兴趣类恰重块m客户和m−1个互不交单例，没有未披露交叠。每条JSON action行都在表中的H标签集合，历史集恰全部合法6^d、d0…m−1，无缺/多/重复。按给定actions从根恢复路径与原path一致，计数与原certificate声明一致。policy有6标签的历史分支，不能以3/4个物理题缩表后声称仍是原43/259行。

## 无需重跑LP或SPE搜索的全历史证明

考虑已有重块族的任意m≥2：H含m客户，另m−1个互不交单例，各与H不交。允许H有数个同覆盖标签，每个有序历史都规定其中某个H标签，具体标签可依历史变化。任意历史已有b次H、总过去t、余r=m−t。遵从后所有未来仍H，因此当前得到
\[
 \frac m{b+r}\ge1\quad(b+r\le m).
\]
改选另一H标签不改物理覆盖、后继仍H，利润相同。改任一单例，未来都H不碰它；若过去已有c名选该单例，则只得1/(c+1)≤1。于是每个具体有序历史的每个真实偏离都不获利，包括已有任意单例重复的离轨历史，所有平局合法。上述两份完整label-policy因此均为纯SPE，无需对数值证书作有利补全。

根全H、每人1、W=m。用H及m−1个单例恰m槽覆盖全部2m−1客户，所以OPT_m=2m−1；表中comparison恰包含H及全部单例，确实最优。此论证不除W，对零未用类型无额外要求。它是[现完整大主题族](../构造/完整大主题策略的额外槽零遗憾紧族--构造.md)的L=m−1实例，以及规范model.py中big_theme_lower_bound的额外同覆盖标签表示，不重新认领经典底层构造。

原文件是canonical允许的同覆盖异标签输入。合并H标签后，物理规定动作仍恒为H，完整SPE与上述数值有同一直接证明，所以集合目录也有该解析族；原保存策略表的标签身份和计数则仍按原JSON保留。它们没有利用重复标签作严格分离。与另两份价格枚举点W=m、OPT=m+1也不同：那两个点只有一个轻块，此处有m−1个独立单例。

原README“最低1/5、1/7”只能定位这些保存的有限探索改进记录。它们恰等u1=OPT/(2m−1)，而严格高于OPT/(2m)，不是所搜逐人OPT/(2m)失败，更不是half反例。也没有证书证明该有限策略锥或所有SPE的全局最低ratio；现银行族的真正逐人失败另有完整证明，不能用这些等号点覆盖它。

## probe_floor真正归一了什么

原main默认m3/k6/trials100/seed7112，可由CLI改。保存JSON只记m/k/trial，没有保存完整argv、seed、trials或全部改进日志，因此不能将默认值回填为两份实际历史调用。

每trial对63个非空兴趣类型随机取初始0…7重数（按0.6保留），canonical精确求解器产生可实现有序路径，至多取前16条；每路径恢复一份全部有序历史certificate。固定这个σ，terminal(h)始终沿同一策略。每历史h的规定收益向量与真偏离h+b收益向量作差，A行是“偏离−规定”，令A r≤0；m3的43节点各5非自比较共215行、m4的259节点共1295行，列为63种非空类型。行不只取在轨节点，也没有枚举全部完整策略。

对抽到的至多5个min(m,k)不同题比较集合Q，令o_B=1_(B∩Q非空)。LP求
\[
 \min_r c_{root}\cdot r,
 \qquad A r\le0,\quad o\cdot r=1,\quad r\ge0.
\tag{1}
\]
**归一的是这个Q的覆盖，不是已证明的OPT。** 原代码没有加“Q支配所有其它m题并集”的约束，不能把ans.fun直接叫最小u1/OPT或通用门槛。整数候选产生后才调用optimal_welfare重新求真正OPT，并以u1/OPT记ratio；这两个保存Q碰巧覆盖全客户，已由表和解析证明核实。

exactify把大于1e−8的浮点坐标限分母100000成Fraction，小者置0，清全部分母得到整数客户重数，再对**同一份完整certificate**调用规范verify_certificate；只接受其valid候选，重新算真实payoffs/OPT后保存。该流程使已接受候选有精确点级验证意图，不把浮点LP上界、最优性或所有锥证明一并认证。当前未运行这个发现器或其顶层SciPy导入，也未重新执行verify；保存点已用前节统一解析证明覆盖所有节点。

筛选还有一个探索边界：只有ans.fun<best−1e−8时才exactify，而best随后记真实ratio；当Q并非最优时二者不是同一目标，故本流程不保证筛到所有更佳u1/OPT候选。每trial只采≤16路径/≤5比较集，末尾best<1/(2m)才早停；保存trial0/4没有证明搜索已完或无更好点。原raw逐字节保持，本页没有把这种启发式改成完备算法。

## probe_disjoint的实际有限合同

1168B脚本在顶层循环，导入它会实际开始搜索，因此本批仅文本阅读。它固定m3、q6、Random9475和至多2000trial：先造三个两两不交base，大小各随机1…6；再加0…5个潜在外客户，用逐客户随机阈值0.2/0.4/0.6/0.8生成三个额外主题。

只保留target_counts=(1,1,1,0,0,0)可由完整SPE实现的输入，遍历这个目标的可实现有序路径（只用三个base各一次）。这些路径的实际覆盖无碰撞，利润就是各base大小；所测严格分离为某早期位置2u_i<u_last。命中才恢复完整certificate，写disjoint_low_early.json并打印FOUND后退出；否则部分可行trial打印进度，最终打印none。它检一个有限机制，不穷尽所有无拥挤SPE或一般线性约束。

本原入口没有附该disjoint输出或完整运行日志，目录README也没给某个发现点；当前0执行，不据脚本文本补“2000全完成/没有命中/已经发现”。原程序有可复用的确切条件搜索合同，保留作为必要相关资源；其数学作用与未成形r-reservoir候选的警告不同，不从同目录位置推导两者等价。

## 证据和接续

[完整原件与结构阅读](../../tools/evidence/independent-recursion-and-background-entry-versions-primary/README.md)保存六个必要相关来源的指纹/正常取得回执及全部43/259策略行，primary仍只五分支入口。没有导入原LP、没有新原程序/求解器/随机扫描运行，也没有将解析核对称为新的外审或盲审。

若接续同一σ的其他重数，须保全部有序IC与真正OPT比较；若接续其它策略，不能复用两份点的等号作全锥证书。若接续早期不交路径分离，应给该脚本真实输出或新的完整可验证SPE，而非从无命中日志推普遍线性界。

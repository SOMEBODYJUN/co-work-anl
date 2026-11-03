---
id: customer-attraction/six-index-ab-literal-audits-and-data-versions
kind: review
type_tag: 审查
title: 六索引AB投影的字面独审与数据版本
status: mature-two-exact-replays-reused; literal-original-reports-retained; zero-new-runs
summary: 完整绑定两份448系数与231argmax、10/11正权、两独立字面公式及历史报告，保输出minimum/maximum文案差而不重扫。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/AB_projected_row.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/AB_projected_row_joint.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/verify_farkas_and_project.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_maxroot/AB_literal_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_maxroot/ab_k0/report.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_maxroot/ab_k0/verify_literal.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_maxroot/audit_AB_literal.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/full_AB_extension.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/joint_full_AB_extension.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/joint_AB_input.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/fixed_graph_priced.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d1fe1e0c444e40d68b6813bf88db8fba/six_lift/README.md
---

# 六索引AB投影的字面独审与数据版本

## 复用的已证明数学对象

[完整AB引理](../引理/真实第三位六索引菜单的完整直方图投影--引理.md)已对六人完整历史纯SPE自足给十五种合法原始行、60倍份额及γ_L(a,d)=max全部六隐藏四位词的必要方向。[两条有理证书](../计算/两条六索引AB投影的有理证书重构--计算.md)已列全10/11个非零正整数L、全部33/13支持质量和两个严格负值。本批新增责任是本次实际领取的两个代码/报告及全部原数据，不另造相同必要行或重复充分成功。

同一策略在实际AB后强制T_i，真实尾(F_i,B_i,C_i)；每客户(t_i,f_i,b_i,c_i)十六词，六词联合直方图有54264个，p=1_A+1_B∈{0,1,2}共162792。d0…6及64实际六位共448系数；t1组和d、t0组和6−d。保同索引b_i c_i，不能分离边缘后假设独立。重复标签/相同历史一致性若缩小真实域，并不破坏全直方图上包络必要性。

第一表只需(p,p_f,d)共63条件；第二需(p,a_A,p_f,ℓ,d)共168条件。两份原JSON分别63810/100938B，全部896整数系数、231个16格argmax、每个key/max/metadata本批均完整逐项实读，原字节保全。第一全局K系数37823040=360×105064，第二**恰0**；不是浮点近零。第一33点与第二697系统13点的严格负上界分别为

\[
-105837198790011822662124212696232256/4196040267817038685502527597,
\]
\[
-91349718500898376119822922846103334631798555340791880/21162912871981828450039063390798893871166580197.
\]

它们排相应actual/d边缘的完整AB菜单，故也排任何具有该固定边缘的原SPE。必要点“曾满足旧行”与“违反新合法行”可同时成立，二者不组成目标反例。

## 原两种字面独审究竟怎样独立

4398B audit_AB_literal.py不导发现器/作者核验器，按t0/t1两组8格composition展开成六字面词，对每p重建每个i≠j、i,j,l互异项；对p_f∈{p,p+1,p+2}求隐藏最大值。源码保SOURCE、cap:3、三floorfamily、query_equal以及两all_distinct，补实际末对常数，生成448查表；核33个per_fixed_type_integer_maxima与有K负值。原AB_literal_audit.json报告162792背景直方图、每背景54264、448系数、63条件、κ37823040、原13.654153108596802秒。它会覆盖同目录报告，且运行中打印七个d进度。

4648B ab_k0/verify_literal.py同样不导作者实现，枚举十六词的全部六重多重集，对每p与兼容实际条件(a_A,p_f,ℓ)逐i,j显式计算，补真实u₂/u₆/H常数，再核448系数、13支持负值、κ0。原report.json报告162792直方图、168条件、原5.40399956703186秒，另有evidence_note明确该文件是保存先前完成输出、保存当时没有新增运行。主程序只stdout打印；报告额外的审查文字不是本入口当前自动生成的字段。两独审的词排序与聚合路径不同，不能把代码独立说成本批新增盲审或外部评审。

两代码均用60倍整数份额并保零分子0；PAIR的g分母(p+t+f+1)(p+t+f+2)整除60，实际常数相同。literal第一使用显式互异三指标120项，第二活跃权只有query_equal的30同查询对，不能给第二补上未活跃的all_distinct。原支持点身份分别c5d623…与b09ce6…，不是后续701的595e…。

## 成熟原核验事件的准确复用

6552B verify_farkas_and_project.py标准库独立从22特征重构15种行，严格拒绝不支持的正权名称；对完整p,d域求γ，输出所有448系数与每条件最大化见证。它的CLI实际能指定两种certificate/input；原README提到不存在的verify_joint_farkas_and_project.py不补造。

已有正式证据包tools/evidence/cag-background-sources-and-AB-projection-primary/runs/AB-original-runs/execution-manifest.json记两次原入口，源码SHAe7f2cbc76d697436033892ab98a7c00c39942213329ace7efe366a4e16eb98db与本次85fd原件相同：

|既有事件|cut / point SHA前缀|墙时秒|exit/stderr|数学输出|
|---|---|---:|---|---|
|with-K|43ab6817 / c5d62321|1.92984057799913|0 /0B|448系数、63argmax、全部数学字段等冻结|
|K-zero|ac95af6f / b09ce6d5|4.579161693007336|0 /0B|448系数、168argmax、全部数学字段等冻结|

原运行各在新外目录，见真实事件CWD；本次stage不是这些事件曾执行的目录。已充分成功故本批两个原核验入口均0，不再扫描2×162792态；两字面独审入口也0，保原历史报告，不能把旧事件次数加成本批新增。

## 输出文字、矩阵域与版本差

两冻结projection JSON已写why_no_offpath_bits的“their maximum is identical”，同SHA原代码生成“their minimum is identical”；实际实现始终取max，且该句只论另外七个固定枝位不影响活跃系数。已有两次真实输出与冻结**不是字节同**，不同字段恰elapsed_seconds和该why文字；896系数、231argmax、L、κ和负上界全相同。原字节/新输出并列，不能修改源码再假称原逐字复现。

原full_ab构造器和joint_ab构造器是浮点phase-I/整数恢复实现，不等于这个certificate-only入口；它们的209088/82368列是两个固定d1点的兼容域，不是普遍448可见格上的全部游戏。一般必要性由完整上投影和强PAIR解析证明，未以浮点infeasible判号代替。详见[固定图与两类扩张](../程序/六人十三主题固定查询图与两类索引扩张--程序.md)。

## 当前状态及来源路由

本批对源8515/ea95/85fd及两字面代码/报告完成全文责任，复用上述成熟sameSHA证据；两报告独有秒数/字段/输出位置已单列，全部表格数据未被摘要删除。后继701点另被[第四源五行](六人第四源五行完整索引投影的独立重建范围--审查.md)排除，不能混成这两个AB输入或借后续5108点给旧701补认证。六人half未由这些必要投影闭合。本批0新数学/LP/随机/隐藏遍历，指纹、既有事件定位与完整数据在[证据](../../tools/evidence/six-background-moment-and-maxroot-source-primary/README.md)。

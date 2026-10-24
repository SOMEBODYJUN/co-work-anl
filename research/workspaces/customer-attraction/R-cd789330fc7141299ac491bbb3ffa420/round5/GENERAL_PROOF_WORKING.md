# 一般半覆盖第五轮：真实传播与替代证明

精确目标Q-CAG-HALF，原单位客户共同目录、任意人数、每个完整有序历史纯SPE，仍OPEN。全部离轨历史、任意平局、空主题与零客户均保留。

本轮恢复同一actor/clone及round4未提交资产。当前已证表示与准确停界见[上轮一般稿](../round4/GENERAL_PROOF_WORKING.md)。联合Hall投影、适应取消、rank层积分均不构成费用上界。六名研究员和root并行直接攻一般目标；个人草稿保存不等于canonical提升。

## root当前论证对象

固定实际完整SPE sigma、最优m元组T、实际覆盖C及最优并集O。目标是同一实例中2|C|>=|O|，不必先证明更强逐人安全保底。源归一与静态最优性已经给出合法取消|G|；真正承重点仍是所有捕获后重置的共同价格或另一全树支付。不将同一叶的返还重用到互斥分支。

并列精确义务：V0<=W（priority终端及同worldHall取消）；Mpath<=W/m（自由跨位置完整菜单）；全部可信续局最小收益L_i的同序矩阵；或完全不同的一般关系。以上均是候选，不是已证前提或方法白名单。

## 文献边界

本轮联网复核Deng等arXiv:2307.07174v2第5、6节，原文明确给两人sPoA、一般下界及二上界猜想，未据此导入一般证明。Brethouwer 2018 thesis第7节的shared-misery条件要求任意后入者降低早入者收益时自身收益不高于其新收益；一般交叠集合不满足该条件，故不能导入其保底引理。本轮没有作无后续文献的一般断言。

## 本轮已证表示及未证支付

一般Q-CAG-HALF仍OPEN，无目标反例。下列均为原模型的全输入组件或明确候选，不是新增人数无关福利下界。

| 资产 | 已经成立、为什么保留 | 真正未付或状态 |
|---|---|---|
| [自然incoming密度总账](rank/incoming_density_diagonal_ledger.md) | 全父子对角项精确为M−H，完整K_in=M−H+T+COV−L，L是真off-history整行IC slack；当前吸收不变时captured可自然重分配 | T+COV−L共同预算未证；[独立盲重构](dynamic/review_density_ledger.md)及[补审](dynamic/review_density_ledger_supplement.md)通过 |
| [全fresh/全客户消元](credible/all_fresh_submarkov_elimination.md) | 利润归一化正广播是严格角色DAG；fresh子集行质量≤k/(k+1)；全客户past正边落actual券，不调用错误的过去IC | whole-actual行、past券、source三者同一C容量未证；[root解析与证据审查](parent/review_broadcast.md)、[独立单位回归](parent/broadcast_audit.json)；另有独立盲审待完成 |
| TOTAL-TRIM，见自然密度稿§7 | 若只求总费，可任删G个比较R源，剩源OPT−W；最低费为R−G个最低自然价格之和，旧Hall是更强约束 | 费用≤W未证；任意trim不继承旧SOURCE-NET/逐行钱包 |
| [PB-extra](independent/two_block_security_reduction.md) | 若任意背景剩r≥2的前两位最终利润和≥2v_(r+1)(b)，则沿actual两位置成块得W≥m v_(m+1)(0)≥OPT/2；奇数与零端点已核 | PB-extra本身OPEN；复制首主题只有同枝等利，不支付跨尾子树；有限阴性非一般正证，已停扩样 |
| [全菜单包络](menu/continuation_envelope_and_open_payment.md)、[L矩阵](menu/li/README.md) | actual路径外各孩子可同时独立拼合；在轨孩子不能极小化后仍保原叶；与旧真实偏离/自由matching对齐 | SM/TB/Mpath仍OPEN；量词消元不算新预算 |

全客户消元可先同context同客户净取消，残余past券受正前缀负载缺额控制；沿单谱系过去差异区间不重叠。但整行归一化会重采客户，不同谱系仍重叠，不能把这些结构提升成全树cap1。新增结构的独审范围以实际审查文件为准。

下一项有信息价值的关系必须实际调用真实孩子IC，约束T+COV或source/whole-row/past券的共同需求。再次消元fresh、重排静态rank、扩大有限阴性或只看单谱系单次收费都不够。基础广播核本身未使用ell≥0，不能因有完整σ输入就声称已经支付了全部孩子激励。

个人checkpoint仅是可恢复研究备份。外审与新颖性未认证，未把上述表示升级为共享canonical福利结果。


来源更正：TOTAL自由trim已由同行incoming_payment.md式(5)–(6)公开，root实际回读确认；本轮同类推导仅保留与自然重分配/密度账的衔接，不计新的预算发现。PB-extra出现完整解析背景分离候选，见menu/pair_attack.md及parent/review_pair_counterexample.md；两名独立审查正在完成前，状态仍按候选，原half未受否定。

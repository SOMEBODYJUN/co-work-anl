# 两份 UM 已完成交付的独立数学整合审读

结论：本次两份官方 done 收据可按现行端点整合。四条新 accepted 逻辑边均支持目标整条陈述；其中三条为 MMO 内部或向普通 UM 的无条件关系，一条为 AFS 数值估计的无条件关系。另有一条已经 canonical 的 AFS 条件边原样共享复用，保持 conditional，不替换或抹去其原有前提。未发现须阻止这两包整合的数学缺口。此结论只覆盖下列精确交付，不清除其它并行变化。

## 交付与当前输入

已读 AGENTS.md、research/IMPLEMENTATION.md、prompts/03-map-worker.md，随后实读两份任务原文及独立收据。两任务在本地当前官方任务记录中均为 Boss5 的 done，任务内 receipt 与独立收据逐项相同。

| 任务 | 独立收据 SHA256 |
|---|---|
| unrelated-machines-3a-3a-35169397311361c0 | 292ede1c6937fd6143d54032970860998924fc69b230e56c36ed76f155ea17c0 |
| unrelated-machines-3a-3a-3e4187a25db3d265 | 218710b40df5e57cf7b2d874b4ad5e19508a2352a1f6a0979b45455f856c69fa |

本次读取的 research/registry.json 文件 SHA256 为 `525c6c5ab4fc4e7b28e636f5d06bfed998ed0b204c4d65893a955f2bd2df0fb1`。七个端点均实读当前完整登记记录，另由 research show 返回 current 的 body/evidence binding；版本和 registration_pin 如下，均与两任务 input_pins 和相应边的 endpoint_pins 一致。

| 对象 | 版本 | registration_pin |
|---|---:|---|
| M-91ba949b418b4026aa3c2dc2e5a62834 | 2 | fd137caa008d902027799278ce88cf69fc35dc0b35350e45472e2e53e08c179d |
| M-e8d9614430ab49fc99125452d10388f1 | 1 | 8235a2ee5b9dcca8eed3e1083fdc0e9d32a10ffc64b264ea13b6c6de967c0ab4 |
| UM-UNKNOWN-TARGET-PARTITION-SEARCH-OBSTRUCTION-v1 | 1 | ad443406701c850f8875133cc83ffd13a2399a7872bb54368221d8398e58963a |
| M-dcc092193be04e8b9b143a1ed5ba1d4d | 2 | d6e64697e257f820f93b54fbfb90ef9ce179a4e80aad92cf2900f1d859210007 |
| M-af4186a632934efda5df11453c86a4a6 | 2 | 1327fd46ec124c0d3fd531eb5e6cfcd87e6e60809e04f576d8d04590164442db |
| M-ca617ca816f74198b08235417c005de5 | 2 | 1a7cb900788dd805e72895946463dd116bc498d223d07a0678d1bc6782a01bcf |
| M-45f29a8d9e9f4e45acad4efb363adbfb | 2 | e30390208fe4b0a1b78f6e9ec3f941dc7840c4a29e7d7e6731ed3b90027a9824 |

两收据列出的全部六个资产引用均与当前文件 SHA256 相符；五条边的全部 evidence 引用文件 SHA256 也相符。这仅核输入身份，不代替下面的数学审读。

## 实读范围与成熟证明复用

本次全文实读四条新边的全部语义及新附件 `map/edges/unrelated-machines-3a-3a-3e4187a25db3d265/scaled-threshold-flow.md`。该附件 SHA256 为 `bd8e172d1dee0c0fc1333275a5e7516655a99ae3c5d7436f46c47671f8f0110c`。

必要来源范围为：

- Asahiro 资料页 §§1（含1.1）、3、4.1、4.2；冻结作者稿 PDF 第1、3、5、13–15页，包含模型/调度对应、Theorem 10 的结论、Theorems 11–12 的完整归约及 Figures 4–5 的提取文字。没有宣称重审整份21页 PDF，也未重审完整有界树宽 DP 证明。
- Karp 现行文献页 §§1、2、5.5。PARTITION 的已发布 NP 完全性及其成熟上游归约链按登记的精确语言复用；未重新读取 §§4.1–4.3、5.4 或 Cook 原文。新边承重的是本轮独立核对的 PARTITION→MMO 映射，不把上游全链冒作本轮新证明。
- `给定目标路径的未知整数搜索--障碍.md` 全文。
- AFS 资源页全文；冻结作者稿 PDF 第2–7、9–10页，包括模型、Theorem 1/§1.1、Theorem 3 及其证明、Theorem 4 的构造/结论、signature 终止及 Theorem 6。没有重新完整审读第8页 Lemma 5。源对象的既有五分之一整数界沿用已发布独立审读；本轮新核的是配置阈值后端及估值夹界。

已全文阅读旧条件边 `map/edges/unrelated-machines-3a-3a-54ba68179f7ae25c/finite-rounding-gap-to-polynomial-value-estimation.json`。当前文件 SHA256 为 `3a63d41f0ba10fb38dc8b3188bb88d647ea9d2a0a98c10e258792116173fac85`，在 registry canonical 清单内，其规范 JSON 语义 pin `3d47811e4165f7efdac25dc11dbec5a44a497ce031bc9b31e79fb92313288007` 与现行 map/integration.json 已发布 edge_pins 完全相同。该边 review_note 已记 Boss2 完整11页独立审读，integration 的既有审读也明确保留“AFS有限整数界加显式LP后端给完整条件估值”。因此对未变 canonical 沿用原审读，没有重新执行其成熟科学程序。

## 逐边数学判断

### PARTITION→多重外平面 MMO

`um-35169397-partition-to-multi-outerplanar-mmo`，文件 SHA256 `866dd7628061c215d6aa9d59cb932c3e2431307e31d4b7e38014d5130d69b811`。

可整合为 accepted / implies / unconditional / whole。源是显式正二进制整数的精确等分 NP 完全语言，目标是允许平行边且按尾端计出度的 MMO。对总和2B的列表，每个下标各建一条权 w_i 的平行边；重复数的下标没有合并。每条边恰贡献一次，总出度2B，所以两点都不超过B当且仅当都等于B，恰恢复等分。奇和的固定 NO、空合法表的固定 YES 以及非法编码处理保持全输入多对一合同。所有数值运算与输出位长为多项式。

“弱”的数值范围也可成立：底层简单外平面图有宽度2树分解，逐条引入平行边，对袋点维护0…B整数载荷，遗忘时核阈值、合并时相加，给关于阈值和显式图规模的伪多项式算法。此处无须把作者稿针对简单图的具体运行时间表达式直接套到任意多重图。结论没有外推到简单外平面、固定权上界或近似gap。

### 多重 MMO→简单系列并行 MMO

`um-35169397-parallel-mmo-to-simple-series-parallel-mmo`，文件 SHA256 `8b5812e7d5ba76a7e6eef4f8784f51dd3ac5969307b18976ca13ce0e5e2737a9`。

可整合为 accepted / transfers / unconditional / whole。每条边替成独立三边路径，权为(w_i,B,w_i)。源可行时w_i≤B，顺原方向定向整条路径，两个内点的出度分别为B和w_i。反向若中边尾为u_i，则u_i已付B，正权外边必须从s指入u_i；另一方向同理强制t付w_i。按中心尾端选择原边尾端，恢复原两点各自出度不超过新端点出度，故双向保持同一阈值。

每路两个新内点保证简单；可给袋 {s,t}、{s,t,u_i}、{t,u_i,v_i} 的宽度2分解，亦直接是两端点间三边路径的并联。至少三路时收缩得到K2,3 minor，故没有把简单系列并行困难性误当成简单外平面困难性。迁移保留同边两端同权，未产生任意两端异权结论。单一源对象已包含该精确困难族，边内给出全部替换桥；没有遗漏另一个独立命题前提。

### 双点 MMO→带真实最大件承诺的精确未知目标

`um-35169397-parallel-mmo-to-promised-exact-target-search`，文件 SHA256 `cee9226350f59e61e49f157eb8480f30c1db3e07f1db85c355310b7b379d7b35`。

可整合为 accepted / transfers / unconditional / whole。将每条边作两机同处理时间残余作业，再各加一件只能在本机执行、时长B的anchor，T=2B。减去每机固定B负荷后，目标≤T与原出度≤B精确等价。初态为(3B,B)，两机实际最大已分配件均B，逐项满足Cmax≤2T、S_i≤T+M_i及有限端≤T。奇和、超大单件及空输入的直接处理不损失困难性。

全输入总位多项式运行界是判定推论不可删的条件；YES必须给完整可验证目标，而NO无任何输出能通过精确验证。只在YES停机的半判定过程不够。边的 unconditional 指上述归约和“若该finder存在则P=NP”的蕴含本身无未付数学前提，并不宣称已经证明P≠NP。若具体目标已给出，改变的残余总量B进入第二机，Q=(0,B)、U=4B、h=(0,0)，没有反驳给定目标路径。此构造没有固定乘性近似间隔。

### AFS整数界→显式后端的数值估计

`um-3e41-afs-gap-with-explicit-scaled-threshold-flow`，文件 SHA256 `8e148d9e65e8a19c6d0d334b7074e2bb26c03be2c5a8bfc77097c61032d94ba4`。

可整合为 accepted / implies / unconditional / whole。单一源给L/5≤OPT，整数解的Dirac配置给OPT≤L；新附件完整支付了旧边保留的近似阈值后端。

独立核得固定t的两向保证：截单件至t不破坏原值≥t的配置；h=t/(mk)，逐件向下舍入总损失≤mh，故整数阈值H=m(k−1)可行。反向达到H的配置原值≥(1−1/k)t。网络每玩家分别有层(j,s)，每层至多选一次物品，取用/跳过即使同端点也分别编号，避免零舍入值时混淆物品边际。单位流的路径分解与配置权重互相对应，共同逐物品容量保全部玩家的同一物品不被超用。规模O(|P|m²k)，显式有理LP可在位多项式时间判定；这里只使用普通显式有理LP算法这一标准基础工具。

阈值搜索也闭合：有正LP阈值时，所有正值配置至少含一个正合资格物品，故最优阈值L≥最小正合资格价值a。若a测试失败，由正向蕴含得L=0。否则网格a(1+1/k)^j测到首个超过总价值U的点；最大不超过L的网格点必通过，因此最大通过值t*满足L_-=(1−1/k)t*≥(k−1)L/(k+1)，同时每个通过值的反向保证给L_-≤L。没有依赖舍后测试随t单调。网格步数及其有理位长均为输入位长与k的多项式。空物品或无正合资格价值时直接返回零，不进入m≥1的缩放公式。

取2/(k+1)≤5ε，E=L_-/5同时满足E≤L/5≤OPT及E≥(1/5−ε)L≥(1/5−ε)OPT。零最优值及ε≥1/5的零输出边界均已覆盖。目标是每固定有效ε的数值估计整条合同；分数流的路径分解没有被说成多项式整数分配。该边不支持一般v_ij的五分之一整数gap。

### 未变 AFS 条件替代分支与 ALL

旧边 `um-54ba-afs-finite-rounding-gap-yields-polynomial-estimate` 保 accepted / implies / conditional / whole。其条件明确要求近似配置阈值后端，估值夹界方向正确；新边独立构造后端使另一条无条件分支成立，不应静默把旧边改成unconditional。两条是同一源/目标间各有自己完整证据的支持分支，而非把旧条件假装已由有限局部搜索支付。

本次五条边每条都只有一个 source_id，premises_mode:all 没有拆失联合前提或反向等价端点。上述额外域条件和新证明步骤保存在各自conditions/explanation/evidence中。未见任何contribution冒作whole；全部whole_result均与当前完整目标逐项吻合。

## 覆盖、未解决问题及整合口径

两份收据各自核心的 linked 处置有相应真实 accepted 逻辑边支撑；读取M-45f29…是精确比较背景，并未因此增加一个不实的引理→任意权估值边。单位值配置清分母只能在相同候选数l、全局出现次数≤l的条件下使用Theorem 3；候选展开可能指数，不能替代本次多项式阈值后端。此限制在新附件中明确保存。

两任务没有声明需另行闭合的follow-up对象对；AFS收据的空closed_overlaps/follow_up_tasks没有隐藏一个已列明的未处置重叠。建议整合时接入三条MMO新边、一条AFS新边及其证明附件，旧canonical条件边按相同路径/SHA复用并去重。

本范围无待修复的身份、版本、证据或推导缺口。仍保留的数学边界包括：P≠NP是复杂度假设；目标生成困难性只是精确搜索；MMO迁移不覆盖简单外平面、任意端点异权或固定近似gap；AFS有限局部搜索没有升级为多项式整数输出，组合引理不单独承担任意权五分之一结论。没有以源证明复用或结构一致性声称第三阶段整体完成。

本次未运行成熟枚举、LP科学实验、局部搜索、证书或其它历史科学程序；也未把收据中的旧有限计数作为本轮执行。除本审读文件外未写资产，未操作Git、队列、done收据或共享总图。

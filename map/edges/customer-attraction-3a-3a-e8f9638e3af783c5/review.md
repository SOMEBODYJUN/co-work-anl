# 最优fresh槽预算与固定最优势：完整比较审查

Boss6；任务`customer-attraction-3a-3a-e8f9638e3af783c5`；2026-11-11。初领任务SHA256为`957afa00fd390151592340ed0006a124cfba6be7789928283ae8a63274f11141`，claim request `33f10b05d5034b698b3fc64e8432a879`。Root定向read-add REP后的当前任务SHA256为`c07cd17bcc5fe04e7ab24f07f85095916ebc8ad0805f0d3bc7a856ba2b06065d`，owner仍Boss6，当前request_id `c81e106dee444e4d958d1fd502eeab72`。本包只写独立staging，未改clone、Git、registry、队列或凭据；交Root复制并原生bind/check后再更新资产SHA及发布。

## 输入、模型与实际阅读

已全文读AGENTS.md、prompts/03-map-worker.md、research/IMPLEMENTATION.md、初领及read-add后的实际task，及registry中15 core与3 read对象的完整原记录。原35条reading_refs对应31个不同文件；指定全文和精确章节均按有序范围实读，所有输入文件SHA与task一致。新REP完整body/evidence共8 refs另逐项读齐（共同模型复用，7个新文件），task对象声明的实际阅读合计38个不同文件。大report共4955行，以完整JSON语义的无遗漏compact分段读取：根所有字段、cases 0–3全部字段与14条records、case4所有非records字段与0–149全部150条records，总164条。源码230行全文读，没有执行import/main。另为R18读取README、两个原完整策略证书与25客户完整精确审计。范围、行号、SHA和用途逐项见reading-ledger.json。

共同目录使用标签集，允许同覆盖异标签、空覆盖、重复行动、零客户和任意弱平局。真实策略在全部有序历史定义，IC使用同一原策略改变历史后的真实后继；计数压缩收益不限制历史平局。静态组合结论不需SPE。fresh自留R0=Σ_(c>0)1/(1+c)与模型R_b(c)剩余总利润是不同量，不能因为符号相同而替换。除具体跨组问题外，六comparison_groups分别审查。

本轮无新数学程序调用、随机/LP/BI/旧图审计；只执行文件读取、JSON解析、字节SHA和交付结构检查。原文中“本轮重跑”“精确通过”等是历史来源身份，不计作本次执行。两个owner证明另外有一次有提示非盲独立窄审，准确结果另存owner-proof-review.md。

## 第一组：最优共同fresh预算

HF保d_x重数，在全部m上给K0≤mW/H_m；结合R0≥W/(m+1)，m=1、2的S?实际已付，W=0全0端点成立。这是对开放RES对象的局部贡献；m≥3的一般上界仍未从HF得到。m5系数及300W/137保原已证身份，不把它当五人half证明。

零净损失GATE量化共同min-fresh最优T及等势I/J，不是冻结费用Q极小者。实际叶本身覆盖最优时，取I=J全索引，门给K0≤W−R0，从而S?成立；若W<OPT，全替换净损失正，不能继续用该门。这个已解边界单列部分贡献，不制造正损失支付。

开放RES的恰m槽域包含于P*的所有1≤k≤m域，故RES⇒P*是完整条件方向。精确静态余项给OPT≤P*+W−R0，预算足half。13人旧例的P*=557/66与K0=724/33严格不同且都通过；ENT1的重复最大query并非覆盖最优，不能反这两预算。

RES下界为K(T)+W−R0−OPT≥0；它与预算上界的结合给half。RES舍去余项，故是half的更强充分候选；没有从half反向得到RES。SQ只给非负平方下界；GATE只给零损失门；旧有限未分离/65个浮点目标不授全锥或全SPE上界。本包不以这些材料写fresh⇔half。

R7已证任意整数背景SUPPORT、MIX、B≥0与同叶CUT。根b0的SUPPORT只有OPT≤m maxg+W−R0，不能倒推K0或P*上界；其同叶价格L固定，换child价变后相消失效。这个对象在已读比较范围内isolated-after-review，理由是不存在本包已付的fresh存在预算逻辑关系，不声称它永远无关系。

## 第二组：静态交换、Beta与owner

E1–E5的全子列表E2非负平均完整推出Bernoulli B/I/Ia/BH/NU/FL：二项矩、Beta积分、锚定减少覆盖问题、初等对称及指数辅助质量均已在proof-notes逐式支付。它是表示压缩，不给全E2系统新限制。

Bernoulli取s=m和组合数对称式恢复P_m(a,c)，积分得到参数对象的MATCH、平均参数核与任意锚平均式。它没有固定J信息，故这一方向仅为contribution，不写whole_result或反向等价。参数对象的固定J BER、FIRST与槽内注入仍依原逐实现合法替槽。

参数对象固定配对HARM给Φ_T≤0，同一硬币覆盖增量表示给归零有限F_T、单调次模及形式空槽边界，差分给ell/e和同叶信用。真实最优前缀query首次误差≤1−1/a、后第s次≤1/s，合H_(a−1)。这支付Beta目标整个陈述，且没有将actual-prefix matching混成最优前缀。

owner目标有两条独立完整支持。第一条逐客户证明未归零Φ_Q≤Φ_T，结合Beta上界得owner上界；直接差分给单位表、同叶κ及firstowner H_a−1。第二条构造纯静态扩充目录S'=S∪{Q_i新标签,空标签}，以逐个Q_i扩回原T_i证明OPT(S')=OPT(S)。Q元组因此在S'最优且a'=1，真正调用源参数定理的固定配对HARM，Beta(1,c+1)=1/(c+1)，得到独立owner上界，再给全部单位/前缀合同。Q_i未被声称在原目录合法，没有把任何SPE移到S'。这使源定理结论承重，避免仅“借用方法”而伪作逻辑迁移。

窄审确认关键限定：Q_i须是覆盖O的owner分割；c=0没有被覆盖incidence，不代1/c；形式缺动作槽若active仍删除Q；次模扩展允许的不可行同槽多动作配置不授OPT cap。未归零Φ比较不能同向搬到F比较，事实上分别归零后F_T≤F_Q，proof-notes已另给准确证明。目标原first-owner前缀合同得到≤H_a−1，未回填任意/分数owner后续量词，亦不把真实后缀删成空槽。

IC障碍只否完整原IC任乘内部非负权保符号的步骤。合法末位平局2t−1原积分0，权1−t后−1/6，不能写成对参数、Beta、owner或half的refutes边。保存参数对象引用该局部边界的一条cites语境边；障碍覆盖仍记isolated-after-review。

## 四个singleton组

第三组R18：正文及两原证书/精确审计支持25<29、21<25的中间桥反例；half余量21和17仍正。本包没有“最差PNE桥”目标端点，也不把反例连到真模型或真静态势上，故准确孤立覆盖。已有审计21有序节点/84含自身比较是历史证据，本轮未重核。

第四组R44入口：各行只保准确导航、参数、既有/未付界及恢复边界；README不替代所指原件，未把共同定义或目录导航建成逻辑hub。当前无具体需发布后续的端点数学问题，保孤立覆盖。

第五组M-642：完整读五图报告及审计代码，明确二进literal与十进token精确资格区别、另定义9/11单位客户点、固定图覆盖全有序历史的层级证明及全部164保存records。负数不舍入；六人正margin不外推全策略；整数校准不回填float已修复；设定迭代数不冒实际全跑。该固定输入资格与本组以外一般预算没有已付逻辑蕴含，保孤立。

第六组M-a6：Root指出实际成熟REP可承担精确前提后，已read-add REP并实读其完整声明/证明refs。μ=max_B min_true-child U_B就是REP的Θ。任意父SPE当前≥μ给必要性；任意孩子d+1维联合向量当前坐标≥μ时，保所选孩子的同一个联合终局，其它互斥有序孩子各贴达到最低当前收益的子SPE，可拼父SPE，投影精确得到整个祖先集合递推。因此新增REP→M-a6的完整无条件边。不能把纯集合凸包点作纯SPE，不能提前丢当前坐标，d每步增到d+1、不宣称固定维闭合。绝对祖先接触税同叶受付不等于当前收益差斜率，也不付跨枝。此为真实源定理承担前提，不凭BI/锥同名与第五组强连。

## 十条交付边与目标核对

| 文件 | 数学作用 | 完整/部分/语境 |
| --- | --- | --- |
| reserve-to-short-optimal.json | RES⇒P*，保长度域、静态信用及13例严格区别 | accepted / conditional / whole |
| harmonic-to-reserve-bound.json | HF⇒K0调和界及m≤2的S? | accepted / unconditional / contribution；一般m未付 |
| zero-loss-to-optimal-actual-reserve.json | GATE⇒actual已最优域K0≤W−R0 | accepted / unconditional / contribution；正损失未付 |
| portfolio-to-bernoulli.json | 全E2子列表⇒B/I/Ia/BH/NU/FL | accepted / unconditional / whole |
| bernoulli-to-averaged-kernels.json | Bernoulli⇒MATCH/平均参数/锚 | accepted / unconditional / contribution；固定J等未付 |
| fixed-kernels-to-beta-potential.json | 固定J参数核⇒Beta整个合同 | accepted / unconditional / whole |
| beta-minorant-to-owner.json | Φminorant⇒owner整个合同 | accepted / unconditional / whole；第一独立证明 |
| legal-completion-to-owner.json | 合法补全桥⇒owner整个合同 | accepted / unconditional / whole；第二独立证明 |
| kernel-cites-ic-reweighting-boundary.json | 静态核接原IC时引用非重权边界 | accepted / context / cites；无逻辑支持 |
| representation-to-ancestor-filter.json | REP⇒祖先联合先筛后投影完整集合递推 | accepted / unconditional / whole；新read-add的实际跨包桥 |

每条边的共同输入保持ALL。两owner方向分别交付，不把独立证明写为联合必要前提。完整目标的定义域、量词、边界和附加结论均由proof-notes对应节支付；其余三个逻辑部分边使用contribution.result/remaining。没有把开放预算源当无条件已证。

## 覆盖、后续与交付边界

15 core全部覆盖，10 linked、5 isolated-after-review；2只读定义用于条件和证据，新增只读REP用于完整集合递推，没有机械模型hub。任务没有明确status=follow-up的对象对，因此closed_overlaps=[]；全部已解本包/共享阅读比较及REP新依赖放additional_comparisons。没有需要Root发布的空泛后续；follow_up_tasks=[]。若后续实际追正损失预算，应给具体最优共同选择与真实后继IC金额，而不是把已有同叶钱包或SQ重新计作付款；本包不为这种一般研究建议制造未发布任务ID。

未发现必须修原文版本的数学错误。原14/18等历史源的独审、0-run、浮点边界、全参数压力均按正文准确身份保留。资产包括10边、本review、完整reading ledger、本轮proof-notes及实际窄审记录；receipt不自列为asset。copy-manifest仅作Root运输清单，不自列SHA。最终边未手写endpoint_pins/evidence_pins/review_digest，必须由Root原生bind/check，再刷新receipt边SHA并push/done。

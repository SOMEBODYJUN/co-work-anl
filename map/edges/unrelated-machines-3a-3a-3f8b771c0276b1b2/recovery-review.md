# 双small包恢复接续核查（2026-11-12）

任务为 `unrelated-machines-3a-3a-3f8b771c0276b1b2`，沿用Boss5既有claimed任务及本地10核心、7只读端点合同。本恢复不操作Git、远端队列或凭据，不修改公共原正文或registry。任务归属依父Boss最近成功同步确认，本页不把本地claimed重新当作远端核验。

## 1. 复用与本轮实读的区别

前序worker已留下9条边、完整comparison-review及reading-manifest。其77声明引用、56文件、57连续区间的阅读成果继续复用。本轮逐一核了当前引用SHA与manifest覆盖区间；这些字节/区间核验不构成重新阅读56文件，也不重新证明此前每个独立对象。

恢复worker实读了AGENTS、worker提示词、IMPLEMENTATION中的构图/绑定/coverage/follow-up合同，当前任务definition与当前registry中17端点的模型、陈述、量词、假设及正文定位；读取9条边与comparison-review全文、manifest/receipt字段。独立新数学复核直接读取《广义指派的费用保持与加性负载舍入》全文、《不相关机器与两个调度松弛》全文、《两份复制多数地板与共同激活复制障碍双源审查》第三节及证明层级/用途、《激活与共享费用源去重补录》全文。另有辅助worker独立复核同一复制链，未写文件。对其它7条边的原始证明只复用前序worker明示成果，并以当前端点合同和本包证明核作用范围；未声称重新读取其全部来源、冻结PDF或候选池。旧数学审计程序本轮运行次数为0。

## 2. 完成时间的槽费用桥独立复核

设输入矩阵及共同阈值M,T为有理数，存在同一无释放、不可抢占调度同时达到平均完成时间M与峰值T。每机倒数位置s∈{1,…,n}的job恰贡献s p_ij；给定共同见证因此嵌入位置LP：每job总质量1，每位置至多1，每机负载至多T，正支撑p_ij≤T，总位置费用至多nM。LP有O(mn²)变量，给定有理阈值的总位规模多项式。

投影x_ij=Σ_s z_isj后，同机只重排这些分数片段：按p非增，从槽1起依次装满。若p≥q分别占s>t位置，交换ε质量的费用变化为−ε(s−t)(p−q)≤0；空缺向更小位置压紧亦不增费用。这在保留全部job分数与逐机负载的同时，给出费用Σ_sj s p_ij x'_isj≤nM的分数覆盖匹配。

在该图上用槽边费用d_isj=s p_ij求最小费用覆盖匹配。分数解已可行，二部匹配整数性给整匹配费用不增。这个新费用依赖slot，不能字面代入只允许c_ij的分配费用主定理。可用的正是ST独立的负载证明：第s≥2槽所选job的p不大于前一完整槽内每段p，该完整槽质量为1，因而p可收费给其分数负载。不同选中槽使用不同前槽；首槽至多r_i，故同一最小费用匹配同时满足L_i≤ℓ_i+r_i≤2T。未匹配槽、末槽、跨槽片段与零时间均不改变此界。

实际执行时按所选槽s由大到小排job。若某job原槽为s，执行序列中它及其后jobs的数量至多s；所以其实际倒数位置系数至多s。于是总完成时间≤Σ匹配边 s p_ij≤nM，平均≤M。空任务单列空调度与零目标，不作除零。每x_ij≤1，装槽后至多跨两槽，槽数至多mn；s p_ij只增加O(log n)位，精确LP与最小费用匹配保持总位多项式。

这支付整个共同(M,2T)目标。取平均最优M*时，T只能取共同见证中的T_M*；没有将独立T*替入，也没有从文献附注制造未核反例。

## 3. 复制界与编码独立复核

全局原UM定义要求每job至少一有限端，故原未剪枝assignment-LP有有限最优F；空任务直接为0。每job带身份复制k份，保原机器及原有限端。任意复制整数调度的各机份数除k给原LP点，故kF≤O_k。

反向取原最优有理x，把同一列分数逐份赋给每个复制job。行负载为kℓ_i≤kF，正支撑最大件r_i不随k变化。ST取费用0覆盖全部nk件，给O_k≤kF+max_i r_i≤kF+p_max≤kF+S，其中S=max_iΣ_{j有限}p_ij。因此F≤O_k/k≤F+p_max/k，固定原实例时极限为F。F=0时LP正支撑只能用零端，ST亦给零值。

F没有被换成T剪枝LST、CONFIG阈值或另一个有额外限制的LP。构造与输出时间按显式nk任务及有理输入总位长计；二进制k的log k长度不包含列出nk个任务的成本。两侧原目标及更强p_max上界均已支付，无新增数学欠款。

## 4. 当前9边的完整/局部/语境界线

| 边文件（省略.json） | 保留的作用范围 | 恢复核查结果 |
|---|---|---|
| st-and-perfect3dm-jointly-support-two-small-sharpness | whole_result | ST与perfect3DM保ALL；结构流与解码由本包§1补付；仅common-b双small域，困难性仍以P≠NP为条件。 |
| st-copy-lift-proves-clone-collapse | whole_result | 本页§3重新支付原双侧界与极限；显式nk成本。 |
| full-config-pins-imply-compact-count-pins | whole_result | 同族每(v,C)各自的完整CONFIG点投影为整数容量b-matching；其余机器仅count合法；原OPT/GPC2/无初始删除由源及本包§3保留。 |
| ordered-slot-method-transfers-common-average-and-peak | whole_result | 本页§2重新支付slot费用桥；同一个输出同时保平均与2T。 |
| higher-nc-pays-frozen-sink-probability-frontier | contribution | 仅NC期望、尾概率和采样；资源的确定性row/count包络仍需自身证明，不将finite资源整体提升为一般定理。 |
| gated-value-bridge-to-full-unknown-opt-ratio | whole_result | 只用源无FSLP前提的值桥；一般LP、两阶段条件期望及平衡提取由本包§6补付；不承诺全类绝对13/8。 |
| gated-general-welfare-proves-robust-two-threshold-decider | whole_result | 源一般福利保证配NO严格福利上界，两个高阈值分别处理；无NP可靠源结论。 |
| fourteen-row-triple-gap-motivates-eighteen-full-row-law | context | 两个不同矩阵；不写特化、whole逻辑推导或反驳实际调度。 |
| cross-row-negative-triple-motivates-paid-s3-lifts | context | 指定K2点不付完整S3前提；不反驳条件S3桥，不声称存在实际schedule decoder。 |

因此保留6条完整逻辑关系、1条已成立局部贡献、2条语境关系。receipt六个linked核心中NC资源仍只受局部贡献支持；SH3、稀疏review、18机K2和14机K2仍为isolated-after-review。没有提升coverage、truth_status或一般UM结论。

## 5. 收据字段修复与剩余范围

发现一处实际交付合同错误：当前任务没有overlap_comparisons，而旧receipt把17个普通已比较对象对填入closed_overlaps。原生validate_map_follow_ups要求closed_overlaps仅包含任务明确声明的follow-up对，因此会报Unknown or repeated closed overlap。现将17条理由原样保存到comparison_outcomes，closed_overlaps置空；comparison-review第10节同步改为正确字段。follow_up_tasks仍为空，没有凭空创建或关闭任务。

77声明refs均由既有manifest覆盖，当前17个input_pins与registry一致，9边所有端点均在核心/只读集合。没有遗漏应read-add的新依赖。25个deferred_candidate_ids仍只是未读候选池；本次没有承担其逐对研究。跨query共同相关性、SH3到共享integer owner、改变extraction/保矩修复、一般UM目标与可靠hardness源，仍保持原开放边界，不在本包假报已解决。

修复后以原生本地函数核assets、9边绑定/证据、coverage及follow-up合同，另核全部task refs与manifest区间/SHA。检查只校合同与字节，不替代数学。未作Git checkpoint/push/done，由父Boss串行保存和交付。

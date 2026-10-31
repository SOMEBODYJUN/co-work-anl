# 鲁棒环共享背景的独立重构、作者稿攻击与最终实读

2026-10-19；实际内部数学审查，外审与全球新颖性均未认证。下列记录按真实顺序完整保留。记录中的 scratch 绝对路径是当时的读取路由，不是现行依赖；数学内容和反驳已一并收在本文，不声称那些临时路径会永久可读。正文、审计代码和冻结结果以仓库登记路径为准。

---

原记录 `cycle_core_exact_first_independent_v1.md`；SHA256 `0bb6a72b29511fc9b342cd327f0bb55aee4370579c0be22722290482a1040f6d`。

# 鲁棒双端环共享背景定理的 Exact-first 独立重构与攻击

阶段：仅实读指定 Exact，未读作者 Proof 或 physical_consistency_notes 中其它文件，也未向作者询问证明。Exact 为 `/workspace/scratch/6bd6916818c5/physical_consistency_notes/cycle_core_shared_context_phase_exact_v1.md`。以下是独立证明，不是对作者 Proof 的转述。

## 1. 量词与必要合同

T 是正有理数，T<=B<2T。每个 core 有 n>=2 台互异物理机器和 n 件互异原作业；作业 j_i 恰有 home M_i:a_i、successor M_(i+1):b_i 两个 finite 端，0<=a_i,b_i<=T。不同 cores 的机器集、任务集分别不交。context 可以任意跨这些 core 机器与额外机器连接，但不能给 core 作业增加第三端。

此不交条件用于 Exact B 在一台 core 机上只有一份 core 的 old/new load。Exact 中“不同 context 任务、各个 core 之间允许真实共享机器”一语应读作 context 可跨 cores 共享其已有物理端；若字面允许不同 cores 彼此重用同一物理机器，则与前文直接冲突，且一般 3T-B 界不成立。见第6节具体反例。该项属于陈述措辞建议，不是在明确 disjoint 域内发现 fatal。

完整 sigma 是整个 ordinary UM 的全部原作业各执行一次、所有机器同时 <=T 的实际调度。结论只给定该 sigma 后换 phase；不求未知 sigma。theta 对每个 core 任意给0/1，不依赖 context 的模块划分。context 原作业逐件原端不变，所以共享网络本来怎样占机器，切换后仍是同一完整网络，不需分模块重新求解。

## 2. Exact A 的两向独立证明

用 x_i=0 表示 j_i 留 home，x_i=1 表示它去 successor。M_i 至多接到 j_i 与 j_(i-1)。两件同时到达的充要条件是 (x_(i-1),x_i)=(1,0)，实际负载 a_i+b_(i-1)。单件负载最多T<=B，空机0。

若每个 a_i+b_(i-1)>B，则任一 B-feasible 指示循环不能有10转折。有限 Boolean 循环若不是常值，必同时有01及10；因此只能全0、全1，即两个 phase。

反向，若某 i 满足 a_i+b_(i-1)<=B，令仅 x_(i-1)=1，其余 x=0。机器 M_i 碰撞，负载正好该和<=B；M_(i-1) 空；其余机器至多单件、负载<=T<=B。n=2 也成立，两件不同任务恰同到 M_i。所得实际调度混合且不是任一 phase，故不鲁棒。等号必须在非鲁棒端。

鲁棒时 a_i+b_(i-1)>B 且每项<=T，所以 a_i>B-T、b_(i-1)>B-T。两个 phase 在 M_i 的负载就是 a_i 与 b_(i-1)，故绝对差严格小于 T-(B-T)=2T-B。包括 T=B 端点，此时全部 phase core 负载严格正，差严格小于T。B=2T 不可能鲁棒，正是排除的端点。

## 3. Exact B：共同原背景负载逐机回算

去掉 sigma 的 context 作业后，每个 core 的限制调度仍峰<=T<=B，由 A 必为某一原 phase。对一台 core 机器 M_i，记原 phase 的 core 负载为 c_i，theta 指定新负载为 c'_i，原 context 总负载为 K_i。它是所有真实 context 作业在该物理机上的非负原时间总和，已经共同计算，不把各模块分开占用容量。

原 sigma 给 K_i+c_i<=T。A 给 c_i>B-T 与 c'_i<=T，故

    K_i+c'_i <= T-c_i+c'_i < T+(2T-B)=3T-B.

这一个不等式同时涵盖同 phase、不同 phase、phase 值相等及所有共享 context。即便切换使负载降低或不变，也有全局所需弱界。额外机器无 core 任务，负载逐件不变且<=T<3T-B。因此所有原机器同时满足 Cmax(tau_theta)<=3T-B；实际上在此有限输入域可得到全局严格 Cmax<3T-B，无需额外假设切换有正增量。Exact 保留非严格版本当然正确。

tau_theta 的实际构造只改 core 原作业目的地到其原两端之一；context 各原作业保持 sigma 的原端。没有复制、丢弃、拆分、第三端或隐藏预载。各 core machine-disjoint，故不同 core 的改派可以同时做，不发生两份 core 负载叠加。

当 B>=3T/2 时，3T-B<=B，所有 theta 确实 weak B 可行。B=3T/2 时上面的真实严格界还给 Cmax<B；T 正且 B<2T 保障剩余裕量。此为保持给定实际背景的相位切换，不是全局求源赋值或近二 hardness。

## 4. Exact C 的最小解析锐例

对任意 T<=B<3T/2，取两机 M1,M2、两件 core 原作业：

| 原作业 | M1 | M2 |
| --- | --- | --- |
| j1 | T/2 (home) | T (successor) |
| j2 | T (successor) | T (home) |

再取一件 context k，仅有 M1:T/2 一个 finite 端。

M1 两件 core 的碰撞和为3T/2>B，M2 为2T>B，故 A 保证此 core 在B鲁棒。phase0 是 j1->M1、j2->M2；加固定 k 后两台实际负载恰(T,T)，所以 strictT 完整可行。phase1 是 j1->M2、j2->M1；context 没有别端，故 M1 必负载3T/2>B，无任何 weakB 扩展。这覆盖 T=B 端点，并在 B 上升到3T/2 时恰失去鲁棒性（M1 碰撞可行），与临界结论相合。

此例显示三半阈值锐；没有显示每个 B 的数值包络3T-B都被恰取，Exact C 也未要求后者。

## 5. 位复杂度与其它边界

验证 sigma 按每件原作业的 finite 原端检查及逐机有理求和。每 core 读一件作业目的地即可确定候选 phase，再全量核验；也可直接应用 A。theta 显式给出，切换写每件 core 作业的原机器编号，context 直接保留。所有步骤按显式任务/机器/finite 条目与有理输入总位长多项式；有限有理求和的公共分母位长至多相关输入分母位长之和，不循环分母或(2T-B)的倒数。

零 a/b 在 Exact A 的一般对象中允许，但 B>=T 下含零的相应碰撞和<=T<=B，所以该 core 不可能鲁棒；无遗漏的鲁棒零分支。零 context 作业可照原端保留，不占额外负载；多端、medium、巨大但 sigma 未用的资格均不影响回算。无 core 时定理退化为 tau=sigma，且T<3T-B；空 context 也正常。每个 core n=2 与多个任意大小 cores 均已覆盖。

## 6. 若删去 machine-disjoint 的明确域外反例

T=1，B=6/5。两个两机 core 共用同一台 M，但另机分别为 N1,N2，原作业仍互异。每个 core 在 M 的 phase0 负载3/10、phase1 负载19/20；在 N_l 两 phase 负载均9/10（对应两件作业：一件 M:3/10,N_l:9/10；另一件 N_l:9/10,M:19/20）。每 core 的两碰撞和分别5/4>6/5、9/5>6/5，故各自单独B鲁棒。

取一件仅 M 耗时2/5 的真实 context。两 core 都 phase0 时 M 负载2*(3/10)+2/5=1，N_l为9/10，strict1完整可行。两 core 都切换为 phase1 时 M 负载2*(19/20)+2/5=23/10，超过3T-B=9/5。所有 context 固定且 core 任务确实只有两端。因此 machine-disjoint 是完整包络的一项真实必要域条件，不可被“允许共享机器”一句覆盖。

## 独立阶段结论

在 Exact 明确的不同 core 机器集不交、core 作业不加资格、给定完整 strict 实际 sigma 的域内，A/B/C 全部独立重构成立，未发现 standing fatal。建议把上述含糊“各个 core 之间允许真实共享机器”改为“context 可跨多个 core 机器共同连接；不同 core 的机器集仍彼此不交”，以免读者扩域。该阶段未读作者 Proof；待冻本文件哈希后由 root 决定是否解封。

---

原记录 `cycle_core_post_proof_review_v1.md`；SHA256 `090f9d7171e624a51477c4fdadfe6af1b3e7dc0a07bb5e8bae6c843e3ef7f15b`。

# 鲁棒双端环共享背景定理：v2与作者全文的读后审查

审查顺序保真：先仅实读 Exact v1，自行重构 A/B/C 并冻结 `cycle_core_exact_first_independent_v1.md`，SHA256 `0bb6a72b29511fc9b342cd327f0bb55aee4370579c0be22722290482a1040f6d`；该阶段未读作者 Proof。root 后续明确解封，才实读下列两份当前文件。旧独立稿与 overlap 反例原字节均未覆盖。

本次实读：

* Exact v2：`/workspace/scratch/6bd6916818c5/physical_consistency_notes/cycle_core_shared_context_phase_exact_v2.md`。
* 作者完整 Proof v1：`/workspace/scratch/6bd6916818c5/physical_consistency_notes/cycle_core_shared_context_phase_author_proof_v1.md`。

## 1. v2域改动的核验

v2明确“core彼此始终机器/任务不交，不允许core机器重用”，而 context 可以关联多个 core 的不同机器、多个 context 任务可共享这些原机器及任意额外机器。此修复消除了v1先声明disjoint、后用“各个core之间共享机器”可能造成的混读，没有改变明确disjoint域内的数学命题。

因此独立稿§6两core重用同机的数值例仍是更宽域反例，不能记作v1明确disjoint域或v2的fatal。独立稿A/B/C全部证明直接适用于v2，不需重构新数学假设。允许任意有限多个core（含零个）与给定单个完整strict sigma的量词保持一致；没有免费获取未知strict见证。

## 2. 对作者证明逐项核验

作者§2的z循环碰撞证明与独立重构一致：混合循环必有10；若某碰撞和<=B，单独翻该前驱作业就给完整混合调度，n=2也正常。>B的严格端点必须保留。

作者§3由a+b>B和各项<=T推出每项>B-T，再得差<2T-B，成立；特别鲁棒分支自动无零端。没有把phase身份一致等同于两phase在机器上的负载相同。

作者§4确实使用同一个完整原context：对每台core机器，原所有context真实负载合为c，原core为x、新core为y，c+x<=T，y-x<2T-B，所以c+y<3T-B。全部context原任务逐件固定，跨core资格或共同辅助资源均未另算容量。不同core机器不交使每台机器恰只计一份x/y；额外机器负载原样<=T<3T-B。这给同一份完整actual，而非为每个模块分别选择不相容扩展。

在有限机器域内作者明确证明全局Cmax<3T-B，强于Exact的非严格界。即便theta等于旧phase、无切换或增量为零，严格包络依旧成立；Exact那句“若有正变化可严格化”不是必要条件，但较弱陈述不假。B=3T/2时新调度严格<B，B>3T/2时3T-B<B；没有等号漏洞。

作者§5的三半锐例与独立稿用的非对称例不同，但同样正确：两件core分别在两机都耗T与T/2，任一碰撞为3T/2>B；把轻作业放有固定T/2 context的M1，重作业放M2得实际(T,T)。换phase后M1为3T/2>B，context唯一端不能逃走。作者称其为“所选phase”而未固定0/1编号，与Exact C一致。

作者§6给出的实际实现只做核验、读phase、按theta重排原core作业和完整原负载回算。θ作为一次显式输入，不枚举2^(core数)个phase向量。有理分母乘积的位长至多输入分母位长之和，不按δ倒数循环，复杂度成立。

## 3. 作者全文新增的sharp-envelope补充

额外包络声称：对任意T<=B<2T、任意有理0<e<2T-B，存在符合域的两机core及固定context，使strict实际可行，指定另一phase的峰恰3T-B-e。这不在Exact C所要求的阈值锐性之内，但已独立逐数核算。

令d=B-T+e。由B>=T与e>0得d>0；由e<2T-B得d<T。core作业j1在两机均T，j2在两机均d，context仅M1耗T-d>0。两机的core碰撞和T+d=B+e>B，故B鲁棒。把j2放M1、j1放M2后，加context得到(T,T)；相反phase的负载为(2T-d,d)=(3T-B-e,d)。因为d<T，2T-d>T>d，故全局峰恰3T-B-e。所有finite时间都在[0,T]且为有理数，位长由T/B/e输入控制。

随e取任意小正有理数，指定phase实际最小扩展值趋近3T-B；context唯一端且phase指定，不能通过改派其它任务降低。严格上界从不达到，故“上确界锐”准确，不应写“有限实例达到3T-B”。此补充没有提供近二计算hardness或新的source decoder。

## 4. 限制与结论

本定理的全部域条件都承重：core作业恰两finite端；这些端时间<=T；core机器/任务彼此不交；给定完整strict实际见证；结论保持所有context原端。它没有覆盖core任务增加clause端、其它非环共同core、或不以phase直接作源标签的全局解码。

后读结论：v2措辞修复准确，作者完整证明及额外sharp-envelope补充均通过本次数学攻击，无standing fatal。新颖性、外部评审或一般UM近二反面没有因此升级；本次未新跑软件，不把解析验证说成独立生产实现。

---

原记录 `cycle_core_canonical_actual_final_read_v1.md`；SHA256 `d41195e61c97b94f55e38f1227e37353959dfb6aa5458754a18e3afbe0294d78`。

# 鲁棒双端环正文与 Fraction 审计的 actual final-read 记录

本阶段是在 Exact-first 独立稿、修复Exact和作者Proof读后记录都已经分别冻结以后进行。root给出最终canonical正文与audit code后，本人实际完整读取下列两个文件，没有只据梗概、diff或他人结论确认；未编辑任何repo文件。

## 1. 本次实际读取的字节身份

* `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/research/current/unrelated_machines/robust_cycle_shared_context_phase_boundary.md`
  SHA256 `4812acc602a87e6cf4d5e0283a688969def8d47a6f7bbae74171deff0f7c98f6`。
* `/workspace/scratch/6bd6916818c5/co-work-anl-boss4/tests/audits/unrelated_machines/robust_cycle_shared_context_phase.py`
  SHA256 `1bd44372d676945516163cb9a8e2d9152bb33a9be71b49837475e94c111bc3da`。

两项实际hash均与root指定值一致。前次Exact-first原稿hash仍为 `0bb6a72b29511fc9b342cd327f0bb55aee4370579c0be22722290482a1040f6d`，读后Proof记录hash为 `090f9d7171e624a51477c4fdadfe6af1b3e7dc0a07bb5e8bae6c843e3ef7f15b`；本次另存，未覆盖原字节。

## 2. 最终数学scope逐项确认

正文明确T>0、T<=B<2T；每core至少两台互异机、任务彼此不同，core任务恰两个原端且各时间在[0,T]；不同core机器/任务集都不交；context可在多个core机器与额外机器上真实共享、含任意非负有理时间、零时间、未用>T端。整个sigma是已给定的全部原任务strict实际见证，theta是一次显式输入。

实际全文A/B/C、严格3T-B包络和sup锐补充都与独立重构及作者Proof一致：循环10碰撞充要条件必须>B；old/new core load都>B-T且<=T；同一个原context c满足c+x<=T，故c+y<3T-B；有限机器最大值保持严格；B=3T/2时峰严格<B。无core也由T<3T-B闭合。sharp family的d=B-T+e在(0,T)，反相最小扩展值精确2T-d=3T-B-e；每个有限实例严格低于包络，整个OPT为T，所以没有把相位扩展界写成OPT gap。

最终正文完整保留了本人的overlap域外反例，明确其不在disjoint theorem范围；没有把这项措辞攻击错记成原明确域fatal。第7节也准确限制结论：没有说所有source NO都有strict见证或weak可行，没有统一读出新一般hardness/algorithm，也没有把两个不同页面的宽scope合并。

本次数学审查未发现standing fatal。原定理是standard碰撞/负载差的限定推导；本记录不认证全球新颖性或外审。

## 3. code实际读到的覆盖及边界

已实读全部函数与main。`options`只给core原两端，`schedule`按原任务选端；`loads`核assignment key集恰为全部原jobs并拒绝不可用原端及负时间。`audit_core`真的枚举所列core的2^n orientations，用真实逐机负载独立核robust iff collision条件，并在非鲁棒分支核单翻转完整见证。

shared-context例的两core物理机器不交且原任务名互异，context跨A/B/额外X关联；原sigma全部11件任务、6台机器实际<=1，保同一context逐件原端对四个theta核全部机器，同时枚举全部32 core orientations确认weak只有四个coherent组合。未用7/3端、零端及细分数均保留。sharp/envelope族按每个实际参数枚举四种原core orientations；overlap例故意复用M只作域外反例。

此程序是明确小输入的Fraction审计，不是一般UM求解器或任意context找sigma算法。代码没有声称覆盖全部输入；例如无core分支的普适结论仍靠正文解析证明，而非该有限audit。

## 4. 本人实际执行的软件结果

本阶段本人实际执行：

    python tests/audits/unrelated_machines/robust_cycle_shared_context_phase.py

将stdout另写scratch `/workspace/scratch/6bd6916818c5/independent_negative_attack_notes/robust_cycle_phase_final_read_replay.json`，没有覆盖repo冻结证据。该次执行exit code 0；输出 `all_assertions_passed=true`。实际覆盖7个local cases、11 jobs/6 machines的shared context全部32 orientations及4 targets、6个三半锐例、8个包络例、阈值碰撞等号和overlap域外反例。该次stdout JSON SHA256为 `bd0c5dae68edd3cae71f3881e151cdccd07e2dc77a8d28bbba13dc8da7d31cf1`。

本软件状态是“审查者实际重跑指定audit且所列断言通过”；有限检查不升级一般证明或hardness。本人本次没有修改repo、共享登记或root冻结证据。

最终确认：已actual final read上述完整canonical正文与指定code，数学scope及内部审查历史准确，所列软件本人实际重跑通过；无standing fatal。

## root 保存核验与结论

本次正文一般性证明与有限核验分层。root 实际重跑相关登记程序，冻结证据含命令、输入约定、代码及正文 hash。现有审查在明确域内没有尚成立的 fatal objection；不表示自动保证真值，更不升级 UM-TARGET-v1 或其反面。

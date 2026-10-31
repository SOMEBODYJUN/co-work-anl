# Take/continue actual escape：含证明来源实际 read-after

实际全文读取对象：`partial_sum_take_continue_flat_menu_actual_escape_exact_v1.md`。该文件虽名含 Exact，但正文含达界 allocation、actual schedule 和 lower proof，故本次明确记为 **source-proof read-after**，不称盲重构。

Source SHA-256：`27d2926563eeb34591ca44a75cf09ca623719827a67eedff485edf78e22053ac`，已核验。

此前唯一 statement-only SHA：`c78b878296d50e7d84ee1389e0eeb7e3796e1ee7b3c1242b54dd5d4cd3d1e41c`。本审查的真正 statement-first 记录 `partial_sum_take_continue_statement_first_independent_review.md` 本次复核 SHA 仍为 `8c5980dbbf6234cf34d2900d98359fc51c50318a932bfb184b6676ee2ab6ba46`，原字节未改。

读取次序：先读新 statement-only、独立给出 SC0/V2/5/30-job8/5/任意调度 lower 并冻结，root 实际读后才授权本次首次接触旧含证明来源。未读取其它 review/json 或另一审查者证明；另一审查者曾先读本 source 的经历不被记成本审查的先验读取，也不把其 Fraction 校验冒称本审查运行。本次未运行软件或枚举，未写 repo、Work 或 Git。

**判定：source-proof read-after 通过，无 standing fatal。** 所有主要构造与下界均与此前真正 statement-first 独立推导相合，且 scope 仅否给定 take/continue additive 规则的 all-agents positive partial decoder。

## 1. §1–3：源值、credit 与实际完整矩阵

源每 item value=3/5、两 item、三 agents，任意合法 allocation 至少一 agent 无 item，故 max-min=0。单 agent 的 unit bundle 确实需要两件，cap-at-1 记账的第二 credit 2/5≤原 item value3/5；source 没有偷换第二 item 的原价值。

候选规则每 take state 用 item:c 与 next-own:1-c，下一节点有 own/off，末端 fresh accept。具体三个 a 的矩阵与新 statement-only 完全相同：5 states/a、7 incidences/a、3 selectors/a；全局 private15+resource11=26 machines，incidences21+selectors9=30 jobs。

每 private incidence 保留自己的 state 身份，共享资源只有一台 global resource machine。未选 off-state jobs 保留。不存在只为 partial certificate 生成 selected-state jobs 的暗删。

## 2. §4：达界 allocation、全 jobs actual schedule 与 lower

作者选择每 a 的 r_take1/m_take2/l_accept，分别领取 x_a/y_a/z_a。资源全局互异，质量2/5、3/5、1，共同值2/5，原 u1/u2 都未用。这与独立重构相同。

作者实际 schedule 的分配规则也与先前30-row时刻证书相同：9 selectors落上述 states，9个 own/accept incidences 导出，所有其它12 incidence留各自 private。每 a 的 private loads 分别为 r_take1=8/5、m_off=1、m_take2=7/5、l_off=1、l_accept=1，九个辅助 resource各1，R(u1)/R(u2)为0。来源虽不逐行列 start/finish，但普通 UM 可按机串行，本审查此前已显式给全部30job时刻，证明义务闭合。

任意 C<8/5，三个 r 的 selector 均被唯一 take1 端强迫；各自 u1-incidence 不能留 private，否则仅 selector+它就有8/5。因此三枚原 jobs 必须同上 R(u1)。来源使用 C<2 下 resource至多一 unit 作矛盾，正确；也可直接算三 unit负载3>C。此 lower 不限制 m/l choices、不限制其它未选 state jobs 的 exports 或任务顺序，是全部完整 actual schedules 的 lower。

V 的 upper 也正确：若全 groups min>2/5，每个 r 都需唯一共享 u1；不交分配不可能。与具体 allocation 合起来 V=2/5，与 actual上下界合起来 OPT=8/5。没有仅从部分资源分配推断未经执行的完整矩阵。

## 3. Decoder 的量词及 §5 的范围

对本 source 不存在让三个 agents 都正值的原 item allocation。因此给定 δ=2/5 的目标 certificate，任意 c>0 都不能兑现每名原 agent≥cδ；允许重新安排全部原 items也无效。这个反例证明分配不存在，不只是算法慢或解码只看到错误 path。

同一完整 take1/take2/accept state 选择对应源中真实可累计到 unit 的单 agent路径，失败来自 additive partial mass只领 continuation/fresh资源，而不是丢了某条 take edge、数值近似或 DAG merging。

来源没有由本例否定所有 partial-sum DAG、全部 source-to-UM compiler、existing selector-tree 正规形或所有 unit witness。full target threshold1与positive partial soundness明确区分；其它 AND/guards、完整 leaf、耦合 obligations、不同processing times等仍需另立矩阵分析。该 scope 与 statement-only 相同。

源中开头引用的外部 selector-tree 文件及其 SHA，本审查本轮没有读取，故不认证那份外部接口的具体证明或字节。当前矩阵反例本身不依赖该引用；本记录只确认作者没有把反例逻辑外推成对该外部定理的否定。

## 4. §6：复杂度和证据归属

对象常数规模，权仅1、3/5、2/5，足以构成具体显式反例，不涉及隐藏展开或求解器假设。没有软件/枚举被用于声称一般不可能性。本审查此前的30job手工证书与本次来源读后核对均不冒称其它人的 Fraction测试。

## 5. 冻结结论

**含证明来源 read-after 通过；真正 statement-first 记录保持原字节。** 尚未读取 root canonical 或 root未来独立矩阵回算结果，不能以本记录预先认证它们。未来可在实际收到后另作 scope明确的最终组合审查。

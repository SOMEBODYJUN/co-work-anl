# 任意异权内部 committer 双见证分摊：作者 Proof v2

作者 fee_cascade_review，2026-10-18。对应完整 statement-only `unrelated_aux_bulk_or_commit_backbone_split_statement_only_v2.md`，SHA256 `aca76d26e2536e770143076b0c09df909a86e7f3422ac8b67189168b3427fa64`。root 与作者共同提出并核算此路线，root 非 blind reviewer。此 Proof 仅给 root hold，独立 reviewer 先仅读 v2 Exact 冻结后才可解封。v1 原字节不改。仅 scratch，不写 repo/Work/Git。

## 1. 两份完整 strict modes 给出的全部 C 计数

用 statement-only 的变量数 r、偶 k、ρ>1/2 及两份实际完整 σ^u、σ^v。任何一份 strict 调度中，每台 ring M 至多一件 q/b，因为这类有限时间均≥ρ>1/2；每正 C 至多一枚 J，因为它们在 C 的时间均1。

某变量 a 的 f 在正 pool 时，strict 正 pool 没有正 q 可入。于是 k 枚正 q 全在 ring；若另有 t 枚正 b 返回，则这 k+t 件原 jobs 除正末 q_k 可能使用右端 M_(k+1) 外，其余均在该变量 k 台正 M。容量迫 k+t−1≤k，即 t≤1。任何 J 在正 C 都迫该处同编号 b 返回，故该模式下正 C 所接全部 J≤1。负 q/b 的额外入流只减少正 M 余量，不能削弱此界。

在 σ^u 中仅变量 u 的 f 不在正 pool，故 c_a^u≤1（a≠u），而 c_u^u≤k；σ^v 同理。所以 K_u,K_v≤ceil((k+1)/2)=k/2+1，其余 K_a≤1。这些 c 计入 J 的所有 guards/aux；没有忽略未选 branch 的占用。

## 2. 固定同端 J 与剩余两半选择

先固定每个满足 σ^u(z)=σ^v(z) 的 J job，保持其原目的地。对内部 machine h∈I，令这些固定 jobs 的真实总负载为 F_h。两输入 strict，故 0≤F_h≤1。若某正 C 有固定 J，则其 unit 容量已经全用；将该 C 从后续可选机器中去掉。

令 d_a 为正 block a 上的固定 J 数。因为 c_a^u、c_a^v 均包含 d_a，K_a−d_a≥0，后续该 block 的 gate 容量可设 K_a−d_a。

每个其余 J job 在两 witness 用不同原 machines，故恰给两个不同目的地选择，每选项取质量1/2。只保这两个输入已用原端；其真实时间由原 P 沿用，不修改零端或其它成本。各输入所用端的成本都≤1。

## 3. I 的真实成本配对 slots 与 C 的 block gates

对每个 I machine h，列出所有剩余半项 incidences 在该机的真实成本，按非增排序

    w_1≥w_2≥⋯≥w_s≥0。

相邻两项组成一个容量1的分析 slot，奇数尾项单独一 slot。每个半项只接自己的这个 slot；给每个半项质量1/2时，每 slot 总质量≤1。每正 C 仍作为容量1的实际目的地（固定已占者除外），不把它与其它 C 合成一个实际机器。

建立同一个整数流网络：source→每个未固定 J（容量1），job→它两个原端所对应的 I slot 或 C（容量1），I slot→sink（容量1），C→其 block gate（容量1），block gate→sink（容量K_a−d_a）。内部 slots 与 gates 只作分析编码，最终输出所属的原 machine。

两输入均值的两半选择给全部未固定 jobs 的分数满流：每 job 总一；I slots 各≤1；C 的两 witness unit 占用均≤1，且固定 C 已移除；block 的均值剩余占用≤K_a−d_a。整数容量给一个确定性整数满流。每个 J 从它的两输入原端恰选一个；固定 jobs 保持原端。

所有 I 与 C 的选择来自同一次全局流，没有逐机独立选红/蓝，也没有分别给不同 branches 凑局部解。

## 4. 任意 unrelated I 的同时三半负载界

固定 I machine h。在两输入平均中，剩余半项负载为 (Σ_i w_i)/2≤1−F_h。每个 w_i 在其所属原 strict witness 上与全部固定 jobs 同时执行，故 w_i≤1−F_h。

流选择每个配对 slot 至多一项，该机选中成本≤O=w_1+w_3+w_5+⋯。非增排序给 O−(w_2+w_4+⋯)≤w_1，因此

    O≤(Σ_i w_i+w_1)/2。

空半项表的 O=0 单列。非空时加固定负载后，

    F_h+O ≤ F_h+[2(1−F_h)+(1−F_h)]/2
          =3/2−F_h/2 ≤3/2。

这个界允许同机异权、任意不同备选成本和零时间；配对只按现有 incidences 排序，不按成本数值展开。固定 jobs 可能总负载1而剩余半项全为零，此时仍合法。它不声称内部≤1，这正是 v2 对 v1 输出合同的改变。

每正 C 同时至多一 J，block a 上 J 总数 c_a≤d_a+(K_a−d_a)=K_a。固定同端 C jobs 在门容量中已扣除，没有被重复免费安排。

## 5. 任意已选正 C 的真实 backbone 回填

令某变量的 F⊆[k] 为最终被 J 占据的正 C 索引，c=|F|。把这些 b_i 送原 pin M_i，其余全部 b（含负 block）留原 C。f 在原正 pool。所有 C 因而恰一枚原 unit J 或 b，真实负载1。

若 c=0，全部 q 用左端 M_i，rings 每台一 q，负/正 pool 除 f 外为空。

若 c>0，令 p=max F：正 q 的 F\{p} 部分送原正 pool；其余 i<p 的正 q 用左端；所有 p≤i≤k 的正 q 用右端；负 q_(k+1),…,q_(2k−1) 用右端，负末 q_(2k) 送原负 pool。

这样 p 之前的 M_i 恰由相应左 q 或已返回 b_i 填；M_p 由 b_p 填；其后的 M_(p+1),…,M_(2k) 各由前一索引的右 q 填。负末 q 已导出，环尾不会撞 M_1。每 ring 恰一原 q/b，成本ρ或1，故≤1。

正 pool 恰 f 加 c−1 枚 q，负 pool恰一 q。于是两 pool 负载分别为1+(c−1)/k、1/k。对每变量都这样做时，完整 J 已在同一原内部/C 网络固定，backbone 的互异变量 rings/pools 不再引入共同冲突。

这一步对任意 F 成立，不要求连续、固定 guard 身份或与某输入 witness 的 F 一致。每原 q/b/f 恰一次，J 仍由第3节恰一次；没有虚拟 slot/gate 执行。J 不接 ring/pool/负 C，backbone 不接 I，因此覆盖原全部 n jobs 且资格逐项合法。

## 6. 全局界、量词及复杂度

全部 I≤3/2，全部 C=1，全部 rings≤1。u/v 两 branches 的 K≤k/2+1，其余≤1；故所有正 pools≤1+max(K−1)_+/k≤3/2，负 pools≤1/k。完整实际 C_max≤3/2，同时实际 selectors 全 False。

原不固定 selector 的 OPT=1 来自给定 strict witness 及 f 全 unit 资格，不能把 all-False 条件化上界当较大原 OPT 或源 NO gap。只假设两完整 modes 存在时，可先数学上任选其 witnesses 得存在结论；没有输入则不承诺求未知 strict schedules。

每 J 最多两半项，所有 I slots 总数≤2|J|，C 与 block gates 为显式 backbone 的多项式数量，流增广次数至多 |J|；容量整数且可截 |J|。成本只作原有理数排序与部分和比较，不作时间倒数展开。全部 witness 验证、排序、流、逐 job 原目的地输出及有理负载回算均按完整显式总位长多项式。空 I/J、零成本、未用 finite>1 无例外；静止 J 已固定。

本证明使用标准两半项配对与整数流，不冒称新的匹配/舍入工具。范围仅为 statement-only 的完整 backbone、两 actual 一真 strict modes 及 J 只接 arbitrary I / unit 正 C。J 到 pool/ring/负 C 或非unit正 C 的新机制没有被免费纳入。未写软件、未以有限枚举支撑一般命题、未认证 source hardness 或全球新颖性。

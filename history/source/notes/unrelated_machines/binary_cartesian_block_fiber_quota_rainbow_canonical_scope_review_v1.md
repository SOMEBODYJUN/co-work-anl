# Binary block-fiber quota：canonical 实际范围读后

审查者：rainbow。只在 clone 外 scratch 冻结；未修改 repository、Work、作者来源或此前审查。本记录不代替其它审查者负责的 q-ary affine / deficit Claims。

## 实际读取与来源次序

本次实际全文读取：

`co-work-anl-boss11/research/current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md`

实际整文件 SHA256：`b859a872faf453265f3a4d0b99439df104ae7fac4af1dca92ca969e39f6e8b30`，与 root 指定版本相同。正式数学认证仅覆盖 §5–6 的 `UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1`、§1 取 q=2 的共同完整矩阵及 §9 对应的显式位复杂度；§2–4、§7–8 已实际作为上下文读到，不据本记录重新认证其其它 ID。

此前真实次序为：先只读作者 Exact，独立重构并冻结 Exact-only 记录，随后经 root 明确授权才实际读作者 Proof 并另冻读后记录。现再次核得四个旧文件 SHA 均未改变：

- 作者 Exact `binary_cartesian_block_fiber_quota_exact_v1.md`：`8d16b510b4064e6ddaaf59edb04549fc5f2eb42c19ed1356d0129efb34e30a98`。
- 作者 Proof `binary_cartesian_block_fiber_quota_proof_v1.md`：`95f1b5fa0db880c6e0b8596dc1171125f10a9280fe6457bc8aa469ba07c1b3b4`。
- 独立先行 `binary_cartesian_block_fiber_quota_rainbow_exact_only_review_v1.md`：`ea4948935eddae9bccdb8cba4b05484bda2e32df0a2d4ba91d8266fca2c2cb91`。
- 作者读后 `binary_cartesian_block_fiber_quota_rainbow_proof_read_after_v1.md`：`a844c71f9944fcd0d237248b7768421991b183384394e3d1143c4c2dab6e4bd6`。

本次未把 canonical 的其它作者结果或 root 论证回填成先行独立发现。

## 共同普通矩阵与 actual 值

§1 在 q=2 时与冻结来源同一完整对象：N=2^t，N 个 groups，每组 N 个 indexed states；真实资源 (a,b) 共 N²；每 state 有 N 个 private 时间 1/N、资源时间 1 的不同 incidence jobs，全部未选 states 的 jobs 保留。Group unit selector 的实际目的 private 机决定所选 state。

受限值恒等式 C_L=2−V_L 正确。正向仅导出所选 state 的不交 bundles，未选全留 private；反向任意 C<2 时真实资源至多一件 unit，提取 selector 所在 state 的实际 exports，未选 state 的额外 exports 只会消耗资源。所选 private 的实际负载确为 2−|B_g|/N。C≥2 的下界及全 private 的 2 基线补足端点，不把额外选择域当物理资格。

## §5 的整数配额、bounded blocks 与 chain

量词明确要求 partition 的每个 block 非空，F_j 是同一个只看该 block 输入的任意 nonlinear 函数；不得随外部坐标重选。任意 partial bundles 没有被限制成 Cartesian。

一个 b-block 的 h=2^b 个 groups 按补组配 h/2 对。每对两支持恰交一项，大小各 h，所以全部 union≤h²−h/2。独立 blocks 的 selected union 精确 factor，给全 union≤NH；总分配数量逼每组共同整数配额≤floor(H)。

Block cyclic shift 的 a≠1 层唯一 owner，a=1 层两 owners。均分资源并跨 block tensor，每组分数质量 H；只在最后对完整显式图取共同整数 matching，得到每组 floor(H)。没有把各 block 的 floor 相乘。达到的总 union 同时等于 NH。

对 b_j≤L，每个归一化因子≤1−2^(−L−1)，blocks 数 s≥ceil(t/L)，得到正文 (5)；floor 造成的归一化损失严格小于 2^(−t)。

固定 chain 的下双对角矩阵 rank：a=1 为 t，其余为 t−1；t=1 可直接核。对应 union=N(N+1)/2，每组均分 owners 得 (N+1)/2 分数数量。N 为正偶数，floor((N+1)/2)=N/2，完整整数 matching 达到 Q_chain=1/2。该 chain 可跨 blocks，正文没有误说它对每个固定 partition 都 admissible；也没有声称全部 acyclic 函数最优恰为 1/2。

## §6 的 typing、保留边界与历史异议

此前实际独立审查曾对作者 Exact 的 ancillary “任意其它 base 的逐坐标 full-support YES lifting”指出类型须另说：当前 F_j 的定义域和值域是二元幂，不能直接承载任意其它 alphabets。该异议只涉及旁注 typing，不涉及本二元 Claim 的数学核心。

本次 canonical 已明确修复：同二元 group/state alphabets 时才直接提升；其它 alphabets 必须另改 block 函数定义域和值域，且不属于当前二元 Claim 量词。固定二元 base 没有 full-support YES 也已明示。该修复保留旧 raw 来源字节，不静默抹掉原异议。

正文正确区分选择域受限 actual 值与普通 P_t：没有物理 guard，普通全局 cyclic 仍给 OPT=1+2^(−t)，不能将普通 OPT 改写成 2−Q。没有由 bounded-block 逻辑条件建立 source NO decoder 或 near-2 hardness。

## §9 的显式规模与最终结论

N groups、N² private、N² resource、N³ incidence 与 N selectors 的计数相符；有限项 2N³+N²，完整 dense 项 2N²(N³+N)。标签和有理 1/N 的位长 O(t)（本范围 q=2）。H 的分子/分母位长 O(t+s)，显式排序/图/整数匹配及全部任务回填均按完整输入编码长度多项式；不是声称 poly(t) 输出指数多 jobs，也无按分母数值展开。没有有限枚举代替一般证明或新增软件证据。

结论：在上述明确范围内，canonical 与已冻结 Exact / Proof / 独立记录一致，无 standing fatal objection。原 ancillary typing 异议已在 canonical 明确消解，旧文件保持原字节；其它 q-ary / deficit ID 不由本记录代审。真实 coordinate/block 一致性的物理实现与主 source-hardness 义务仍 OPEN。

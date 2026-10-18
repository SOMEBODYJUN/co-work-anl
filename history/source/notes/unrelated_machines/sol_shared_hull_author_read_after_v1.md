# 共享 aggregate 直方图等价的作者 Proof v1 实读后审查

本记录由 sol_true_hardness 编写。root 已实际全文读过独立 Exact-first 冻结记录 SHA256 `473e3da98481251e317fbeaf8aea3548bd159c54958d862a2948ca283a18e6fd`，随后明确授权读取作者原稿与 finite audit。本轮才开始阅读作者 Proof；不倒填为冻结前已读。

## 1. 实际读取的版本与审查 scope

| 文件 | 实际 SHA256 | 本轮读取 / 使用范围 |
|---|---|---|
| sol_global_certificate_shared_hull_exact_statement.md | f73acb0f0eb3b6741d1a8a854fbee1d507aadea2a8f2f5e3a533aee50740163a | 上轮已全文读；本轮保留其原 v1 合同，不改字节 |
| sol_shared_hull_exact_first_attack.md | 473e3da98481251e317fbeaf8aea3548bd159c54958d862a2948ca283a18e6fd | 上轮独立推导的原冻结版本，未修改 |
| sol_global_certificate_face_hull.md | 4a0357981a3f9c3a3ac01e6a2432cb41f88f8e9edc8af76585a3e85abdfccba4 | 实际全文读取；正式数学审查仅§8、必要的§2/3定义与§8.3四机例 |
| sol_global_certificate_face_hull_audit.py | 2dfa7278cbc7677eb3c5927c11a51900cfd6c391a94ad41dc8f882bc08ece09f | 实际全文读取代码；只实际执行与§8有关的 targeted function |
| sol_shared_hull_author_v1_targeted_audit_output.json | 27cb65a6da68dc13fb73824ca2fee374d026374d790771f16b1cd61290c72fc5 | 本轮直接运行未修改作者代码得到的确切输出 |

Proof 与 code 在读取后再 hash 一次，字节未变。本轮未读取作者新 k 层次草稿，未主动查找或读取 Exact/Proof v2，也未读取其他 reviewer 的 Proof 读后记录。

虽然原稿§1–9的文字已全部看过，不把§4均值反例、§5前沿、§6rank、§7matroid或其新颖性列入本次全审，也不因 audit 文件包含它们就将之算成本轮数学认证。这里的裁定只关于已经固定的弱 aggregate Eq 与必要定义。

## 2. 作者§8的双向证明确实包含所需数学步骤

作者正向 Proof 取每阶段 own-row 的 add=z^r_(r,·)、其它 branch 的同一行之和为 stay；两者和是前层 row histogram，平移后是后层 row histogram。每机独立形成 subset-sum layered DAG 的 unit flow，再按路径所选 job 标签产生容量配置。每个 job 的 selected mass 在机器 r 上等于 θ_r，总和 1。它没有用跨机器共同 coupling，正是 CONFIG 所允许的 row-marginal 见证。

作者逆向从任意 row-configuration distribution C_r 出发，逐 job ℓ 构造 v^+、v^-。其 r≠i 的分配

    z^i_(r,s)=x_iℓ v^-_(r,s)/(1−x_rℓ)

在 x_rℓ<1 时行总量确为 x_iℓ；与 own branch v^+ 相加恰为 old histogram。若 x_rℓ=1，非负和 Σ_i x_iℓ=1 强迫其他 x_iℓ=0，且 v^- 总量0，所以该分段取0不会丢质量，不涉及除0。不可用 i 的 x_iℓ=0、own plus 为0，删掉这些 zero branches 与 Exact 的 E_ℓ 版本相同。容量面只检查 own plus，来自实际合法配置而必过。

这与上轮独立证明的 selected-mass x 及 row-wise residual transport 完全一致，不是作者只展示一份指定 CONFIG 证书通过。给任意最终 CONFIG witness，限制到全部旧前缀并按上述规则构造，可得一条完整 weak 轨迹；给任意最终 weak point，有限步递归选 witnesses 可得整条轨迹，随即生成 row flows。两个方向因此覆盖全部最终 histogram points。

作者§8.2也显式保留 zero-time keep/add 两条平行弧的 job 标签，与 Exact-first 对零时间、同时间不同 jobs 不合并的要求一致。原稿没有把 row-flow path decomposition 误说成一个共同 integer schedule。

## 3. 原稿 H / Ĥ 符号有实质歧义，Exact 的定义则正确

原稿§3把 H_j 定义为真实共同前缀调度的 one-hot convex hull。§8.1 的弱化列表却写 aggregate Σ_i z^i∈H_(j−1)，随后才称弱递推可达集合为 Ĥ_j；§8.2 证明后又写“aggregate 虽在真全机 hull”。

若这里 H 始终按§3的真实 hull 逐层理解，(EQ) 并不成立。作者自己的四机例已给反证：

- true H_4 只有 D=(b,b,a,a)、O=(a,a,b,b) 的凸包。
- A 只能从 O 出发，在机1或2插入；故 true H_5 仅由 (b,a,b,b)、(a,b,b,b) 及其凸组合构成，机3、4总为 b=1。
- B 只有机3、4有限端，处理时间 d>0。对 true H_5，两个可选 own faces 都为空。因此从真实 H_5 只作一次 weak split 也不可能完成 B；但 CONFIG_6 明确可行。

正确且已独立证明的递归对象必须是 aggregate∈Ĥ_(j−1)，即前一步**弱系统自己的**可达集合；到第5层时它已经可能含 ghost。作者§8.2两方向实际构造的正是这个递归 weak 对象。Exact v1 已精确写成 Ĥ_(j−1)，所以这不是对已审 Exact 的反例，是作者原稿符号/叙述必须澄清的一处。

不能在专用 Proof 中继续说“每层 aggregate 都在 true common H”。可以说在某一层入口偶然是真 H 的点仍可能经 split 造出 ghost，例如 A 的那一步；后续 weak stages 的 aggregate 只在 Ĥ。

## 4. 四机六 job：完整 jobs、CONFIG 与真实最优值逐项复核

作者矩阵 p 与 finite audit 完全一致，a=2/3,b=1,d=1/3；所有∞资格均未补边。它是 rational-grid 例。与 Exact integer 域对应时应将全部时间和容量乘3：K=3，端时间变成1,2,3；row histogram 的 load labels 同步乘3，所有论证与 witnesses 不变。不能把分数 load 直接塞入 s∈{0,…,K} 的 integer 坐标而不作这一解释。

前4 jobs 的每个 finite edge≥a，任意两件之和≥2a=4/3。因此在容量1，甚至任意 C<4/3 下，四件 prefix jobs 必须一机一件。其 machine-job 支撑是单一8-cycle，两个 perfect matchings 正是 D 与 O；沒有其他完整 prefix pattern。

CONFIG见证每机两个配置，各重1/2：

- 机1：{j1} 或 {j4,A}；
- 机2：{j2} 或 {j1,A}；
- 机3：{j2} 或 {j3,B}；
- 机4：{j3} 或 {j4,B}。

它们负载都 b。逐个 job 的两次1/2覆盖恰1，包括 A、B。阈值不能低于 b，因为 j2 只有两个时间 b 的有限端，故 CONFIG threshold 确为1。

真正 C<4/3 时：D 在 A 的两候选端都已有 b，O 在 B 的两候选端都已有 b；任一 pattern 必遇 b+d=4/3。所以实际 OPT≥4/3。取 D，把 A 放机1、B放机3，机器负载为 (4/3,1,1,2/3)，全部六件原 jobs 恰执行一次，给反向上界。

A 的 weak split 后，机1、2恒 b，机3、4各半 a/b。它不在 true H_5，因为后者机3、4都恒 b。继续允许 aggregate∈Ĥ_5，在 B 的两个 branches 各取 own a，便达最终各机 Dirac load b。这里出现的“Dirac”只是各行 load 的 Dirac，不能据此称全局实际调度存在。

## 5. 本轮实际执行的 finite audit 及其真实覆盖

我用 runpy 读取**未修改的作者代码**，避免触发无关 __main__/rank/frontier 分支，直接调用 `shared_split_actual_counterexample()`。该调用内部实际执行：

1. `shared_split_trajectory` 逐 row 检查每份配置分布总量1、每配置有限资格与负载≤T；逐 job 检查 coverage 总量1；构造 θ,z 后检查每 branch 每行质量、own 容量面、aggregate=上一层、再算新 histogram。
2. 对四机前4 jobs，穷举4^4个完整 machine choices，过滤∞与容量1，断言真实 prefix states 恰 D/O。
3. 对完整四机六件矩阵，穷举4^6 choices，过滤∞并以 Fraction 算所有负载，断言实际最优4/3。
4. 额外调用 `shared_split_trajectory([[0],[∞]], [Dirac{j},Dirac∅], T=0)`；这真正覆盖 θ=1、不可用 alternative、零时间 selected parallel arc 的有限边界。

运行退出正常；确切输出存于已列 hash 的 JSON。输出 after_A 是机1/2 load1 Dirac、机3/4 load1与2/3各1/2，weak_final_dirac 全1；实际 OPT字段为4/3，two prefix states 与原稿相同。

代码没有运行一个 general CONFIG LP solver，也没有对任意 weak z 反向恢复 CONFIG 并做全参数自动验证；一般 EQ 靠数学证明。`config_threshold:1` 是返回字典的固定字段；代码验证了 T=1 的给定 CONFIG witness，阈值下界 j2两端均1由本轮人工数学复核，而不是某个隐藏 LP-search。代码也没有直接枚举 H_5 并 assert ghost∉H_5；这个结论由§4中的完整 prefix/A 论证得到。

因此 finite audit 的实际能力足以验证本例与所列边界，但不能升级为“程序验证了全输入 Eq / polynomial LP theorem”。作者原稿最后一句本来也明确不以有限代码代替一般证明；应保留这个限制。

## 6. 计算合同与保留的 v1 问题

作者§8.4说每机 subset-sum DAG、跨机 add 流逐 job 和为1，与独立 LP 构造相同。系数无需编码 processing-time 大数，整数 a 只决定弧终点；每机 flow 与 job coupling 的 side equalities 一起形成一般有理 LP，不是一个已知 integral pure-flow polytope。

v1 的两项已经冻结、不得抹除：

- Exact v1 的 size O(mj(K+1)+|E_[j]|(K+1)) 在 j=0 的显式 y convention 下 RHS为0；应改 j+1 或明确 j=0 常量点特例。
- 对 arbitrary rational objective，计算时间应包含 objective bits；不能只按不含该新输入的 LP 尺寸。

原稿§8.4更简略写 O(mnK)，在 general integer K=0 时也需要 K+1 或另列常量-load 特例；原始 outer rounding 的 n≥1、δ<1 时 K≥1，那里可吸收+1，但独立 integer Eq 的全域不宜省略。

rounding 的 rejection 方向也与独立记录一致：任意 actual C≤T 的调度，剪枝保其所有 used edges，逐机 Σfloor(p/q)≤floor(T/q)=K，给 Dirac CONFIG，所以 LP infeasible⇒OPT>T。LP feasible 对真实σ不提供反方向承诺。固定δ时 K=O(n)，因此显式 LP、rational certificates 与精确算术位长均为原显式输入的多项式；δ作为输入时需计数值1/δ。

作者援引既有 degree-2 CONFIG gap 来说明不能相对T统一舍入，本轮只确认这个依赖方向：若原 family 有 CONFIG(T)，向下 floor 后同一每机配置仍合法，故通过 weak LP。未借本次阅读重新审查仓库 gap family 的全部证明，也没有把相对T障碍改写成相对OPT的困难性。

## 7. 最终 v1 读后裁定与后续隔离

在 Exact v1 已明确的 aggregate∈Ĥ_(j−1) 定义下，作者§8双向 Proof 完整，与本人的 Exact-first 独立重构吻合；四机 counterexample 的全部原 jobs、真实 OPT、CONFIG witness、weak trajectory 都核对通过。无新核心 fatal。

原稿 H/Ĥ 符号歧义需要修复；若 literal 逐层 true-H 解释，则有§3所列明确反例，不能保留该过强读法。v1 的 j=0、objective-bits 两项仍按原冻结记录保留，原稿 O(mnK) 的 K=0 shorthand 同时应谨慎。

本记录只属于作者 v1 读后阶段，不记 Exact/Proof v2 已读，也不把未来层次草稿作为本 Eq 的依赖。root 实际全文读本记录后，可另行提供 v2 路径；随后审查应另冻独立版本记录，不能覆盖本 v1 字节。

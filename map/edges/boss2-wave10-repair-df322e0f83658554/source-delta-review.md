# 归一化福利两条完整关系的同源差分复核

## 1. 任务、当前合同和阅读时点

本页由 Boss2 的 `wave13_normalized_welfare_formal` worker 为 `boss2-wave10-repair-df322e0f83658554` 写入，内部问题为 `zero-incidence-normalized-welfare-two-whole`。只接续该任务原有的 10 个核心、7 个只读对象及前任 12 份资产；不新增节点、读取对象或比较包。父 Boss 已确认远端 `ca51fd6abc38279a4fe4781910dcbe4efd0644b3` 上本任务为 claimed/Boss2，claim request 为 `8b9bdb8e1a82431980cfca9fccef9491`。worker 本地完整读任务；definition 的规范 JSON SHA-256 为 `217149e7c18c8aac6124dd6b73a0b86344613ca2436b5aef75d987bc867b4333`。远端确认来自父 Boss，worker 未自行调用 Git 或队列。

完整读取了预核 `research/workspaces/map-v2/Boss2/recovery-20261112-e8cf4c/normalized-welfare-source-delta-precheck.json`，实测 SHA-256 为 `f0e81c8b2871a945fb2434034238adc0c3556f7b9efd9f38daff1291db23c746`。预核的 available/null 是其旧只读快照，不是本任务现归属。预核所收录的 WELFARE、13/8、robust 三份完整 record 本轮逐字段读到；各 record 规范 JSON 的独立 SHA 逐一等于当前任务相应 input_pin，故直接核对的是与本任务完全相同的三份完整目标合同。其余 14 个 pin 与预核记录一致，当前性由父 Boss 的远端核验给出；本 worker 不把这项 pin/字节比对说成新读了其全部原证明或全仓 registry。

三份 v6 合同的模型、statement、quantifiers 均保持原数学内容。WELFARE 提供不要求 FSLP 的完整 `OPT(P_gate)=2−β*` 值恒等与回填，另有要求 unit-FSLP 的福利/绝对峰分支；13/8 要求一个仅输入显式菜单的确定性总位多项式算法，包含一般福利 LP、`W≥(1−1/e)L`、排序、全部原 jobs 回填及相对未知 OPT 的比例；robust 要求近完美 YES 与两种分别全称量化所有 allocation 的 NO 的精确 LP 判别。不能用源的绝对峰分支替代一般比例算法，也不能只凭最后的调度比例推出 robust 判别。

本轮新读 AGENTS、IMPLEMENTATION、worker 词、当前任务全文、预核全文，及共享源、v2 完整算法、FSLP、八源溯源、最终比例纠错、robust 和均匀束正文全文；另读平菜单主定理全文来独立核零 job 勘误。该主定理只作源差分交叉核对，不成为新端点或当前两边的新前提。前任 9 边、comparison-review、recovery-review、reading-manifest 和 receipt 全部数学/交付字段已读。完整记录见 `source-delta-reading.json`。

前任 77 refs、56 文件、57 区间及其成熟数学、历史 PDF 和有限程序证据继续继承；本轮只对该 56 文件做当前 SHA 比对，没有重新阅读其所有正文、经典 PDF 或重跑数学程序。旧 manifest 的 `all_declared_sha_current:true`、旧 review 的 current/version/已读语言，均只描述旧交付时点。实测 55 文件 SHA 不变，唯一源文件差分在下节；所有旧资产仍保原字节，时点说明由本页补充。

## 2. 实际唯一源差分与零 incidence 的覆盖

变动源为 `archives/unrelated-machines/state/审查/归一化菜单福利与配置证书双源审查--审查.md`，新完整 SHA 为 `33bd31b883b26f49508808dd7175cd104f391b86642bff90ea2bce7f1142097b`。全文中“以 1−λ 权重放全部 incidence jobs（含零 jobs）；”出现一次；将它逆替换为旧句“以 1−λ 权重放所有 positive incidence；”后，完整 SHA 精确恢复 `63629abaa5cd2bcc0e42ff051936b91882ea63c711dfdac231f238763b682255`。这独立确认只改了 §二.1 这一片段，没有其它正文差分。

给一份正支撑 FSLP，某 state 的 private 机在权 λ 的配置放 unit selector 加全部零私有时间 jobs，在权 1−λ 的配置放全部 incidence jobs。两配置负载分别恰为 1 和 1：前者靠 selector，后者靠 state 系数和为 1。每个零 job 在两配置均出现，覆盖为 `λ+(1−λ)=1`；每个正 job 在 private 的覆盖为 `1−λ`，在其资源 singleton 的覆盖为 λ，合计 1；组 selector 的总覆盖是 `Σ_s λ_gs=1`。每资源仅正 support 消耗 singleton 概率，FSLP 列容量使这些概率和不超过 1，余量给 empty。零 job 不参加正 support 容量。

反向仍用 selector 与正 incidence 在 private 不可共居，以及资源 unit 配置容量，取得各资源 `Σ α≤1`，再按组归一化。零 job 可与 selector 同居，因此不把它当作正 support 约束。主定理 `规范化平菜单的CONFIG与正支撑LP双向保持--定理.md` 的原证明本来就把补配置写成全部 incidence，其 SHA 为 `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`，未改。

本勘误属于 flat machine CONFIG(1) 的证书正向覆盖，未修改 normalized state/coin 福利舍入、一般福利 LP 或完整 P_gate 调度。flat 全组 max-min 值也不能替代门控 balanced 值：两组单 state 共享 unit 资源时，flat OPT 为 2，完整 P_gate 的 β* 为 1/2、OPT 为 3/2。两条待替换边的证明均无需调用这个 flat 配置桥；第一条仍须更新它直接引用的整个共享源文件 SHA，第二条直接证据文件 SHA 均不变。

## 3. 值桥到未知 OPT 全门控算法的完整推导

固定同一个显式 norm1 菜单，`n≥1`，每组 state 非空且带索引，每 state 的非负二进制有理系数和为 1。四类机器互异：root R、gate X_g、private M_gs、resource Q_u。全部原 jobs 为 root pin、每组 connector/selector 及所有 listed incidence，含零项与未选 states；未列效用系数记零，不凭空生成 job。其规模是 `1+n+S+m` 台机器、`1+2n+I` 件 jobs，I 包含全部显式零项。

先独立核源的无 FSLP 前提值桥。给 balanced witness H、bundles、attaining states，pin 留 root；H 的 connector 去 gate、selector 去 private、所领正 incidence 去资源；未选 connector 留 root、selector 去 gate；其它全部 incidence 留 private。root 负载是 `2−|H|/n`，选中 private 为 `2−v_g(B_g)`，其余 private、gate、resource 都至多 1。因此平衡值 b 的见证给完整峰 `C≤2−b`；b=0 用所有 connector 留 root 的完整峰二基线。反向任意 `C<2` 调度的 root 计数给到 gate 的组比例至少 `2−C`；这些组的 selector 必须去某 private，该 state 被导出的正质量至少 `2−C`。资源 unit 端在 `C<2` 时至多接一件，所以 bundles 全局不交，给 `β*≥2−C`。于是精确 `OPT=2−β*`。root pin 的真实独占时间 1 给实际 `OPT≥1`，与任意 LP query 阈值无关。

一般福利 LP 对每 state 有 z、仅正 incidence 有 x，约束 `Σ_s z_gs=1`、`0≤x_gsu≤z_gs`、`Σ_gs x_gsu≤1`，最大化 `L=Σ p_gsu x_gsu`。任选每组一个 state 并令 x=0 即可行。任何真实不交 allocation 可逐组选 attaining state，将相应 z 与获得的正资源 x 置 1，故 `W*≤L`；按组使用 norm1 与 x≤z 得 `L≤n`。这没有假设 unit-FSLP；标准显式有理 LP 给多项式位长最优解与总位多项式求解。

跨组独立按 z 选 state，再在所选正 incidence 以 x/z 独立提议；z=0 不选也不作除法。每资源给原系数最大的提议者，固定编号破平局。固定资源 u 和正 level a，`q_gu(a)=Σ_{s:p_gsu≥a}x_gsu`，初始 `Σ_g q_gu(a)≤1`。跨组独立给 `Pr(max X_gu≥a)=1−Π_g(1−q_gu(a))≥(1−1/e)Σ_g q_gu(a)`。先得的是尾概率，须再按不同原正系数 levels 求 `Σ Δa Pr(max≥a)`，才能得到总赢家加性质量 `E A≥(1−1/e)L`。实际 bundle 福利 W 至少为赢家质量，因组价值对所有原 states 取最大值。

逐组枚举正概率 state、再逐 incidence 固定 coin；当前精确有理期望都是合法候选子期望的加权平均，取最大者不降。概率 0/1 时只取合法分支。每资源每 level 使用 `Φ=Σ_u,ℓ Δa[1−Π_g(1−Q_gu(a))]`，部分条件化后 `Σ Q` 可以超过 1，之后只重算该精确式，不重新套初始容量弦界。组内资源因共享 state 而相关不影响逐资源期望求和，乘积只跨组。候选、coins、levels 都由显式 I、S、n 控制；每次从原 p、z、x 重算有限乘积，分母因子个数与位长多项式，避免递归平方增长。算法不用比较无理 e；完成后 `W≥(1−1/e)L`。

这里 W 是总福利，不能直接写 `C≤2−W`。须把最终质量排序 `r_(1)≥…≥r_(n)`，计算有理数 `b=max_k min(k/n,r_(k))=βhat`。取得最大值的前 k 个组及其原 bundles 给平衡 witness，才可完整回填得 `C≤2−b`。若 `h=#{g:r_g>b}>nb`，则第 h 项使 `min(h/n,r_(h))>b`，矛盾；所以 `h≤nb`，且 `W≤h+(n−h)b≤n(2b−b²)`。最优平衡见证覆盖至少 nβ* 组且各质量至少 β*，给 `W*≥n(β*)²`。合并 `W≥(5/8)L≥(5/8)W*`，得到 `b≥1−sqrt(1−5(β*)²/8)` 及 `C≤1+sqrt(1−5(β*)²/8)`。平方根只用于分析，实际算法仅做有理 LP、乘积、排序、扫描及回填。

对 `0≤β≤1`，令 `D=(13/8)(2−β)−1=(18−13β)/8≥5/8`。精确平方余量为 `D²−(1−5β²/8)=(209β²−468β+260)/64`；分子导数 `418β−468<0`，在 β=1 取值 1，因此余量至少 `1/64>0`。两边可比较正平方根，故 `C≤(13/8)(2−β*)=(13/8)OPT`。β*=0 的完整峰二基线、n=1、重复 indexed states、显式零及 unused 资源都已覆盖。该单一算法不输入 OPT、β*、source YES 或一份 LP 点。全部目标合同已付清，可继续 accepted / unconditional / ALL / whole；没有从 unit-FSLP 的绝对峰结论外推全类，也不把有限 SciPy/Fraction 认证当作生产有理 LP 后端。

## 4. 一般福利到两阈值 robust 判别的完整推导

保持同一显式 norm1 菜单、原价值与真实全局不交 allocation；不增加 coherence、标签相容或共享内部任务。参数为二进制有理数，域为 `0≤η<1`、`0≤δ<1`、`0<γ≤1`，并满足 `E: (5/8)(1−η)≥γ+(1−γ)δ`。源 13/8 的完整合同含一般福利 LP 和实际 `W≥(1−1/e)L`，本边实际用此保证，不是只用其最后的调度近似比。

用 §3 的总可行一般福利 LP 求精确最优 L，`L≥(1−η)n` 时接受 YES，否则 NO。YES 见证有至少 `(1−η)n` 个质量恰 1 的组，嵌入同一 LP 得 `L≥(1−η)n`。近完美 YES 不要求所有组的 unit-FSLP 可行，不用它替换一般福利 LP。

对 NO_≥，每个 allocation 令 `h=#{r_g≥δ}`，低组质量 `<δ`；对 NO_>，分别令 `h=#{r_g>δ}`，低组质量 `≤δ`。两版各自都有 `W≤h+(n−h)δ=δn+(1−δ)h<[γ+(1−γ)δ]n`。最后严格号只用 `h<γn` 与 `δ<1`，不混高阈值与低端互补事件，不加整除假设。

若 NO 被接受，`L≥(1−η)n>0`，因为 η<1、n≥1。`e>1+1+1/2+1/6=8/3` 给 `1−1/e>5/8`，源保证一个真实 allocation 满足 `W>5L/8≥(5/8)(1−η)n≥[γ+(1−γ)δ]n`，与 NO 上界矛盾。因此两个 promise 分别正确，且 E 可取等号。判别只解 LP 和比较阈值，不需要运行 finder。

在统一子域 `0<γ≤δ≤3/8`、`0≤η≤1/40`，右端 `γ+(1−γ)δ≤2δ−δ²≤39/64`，左端 `(5/8)(1−η)≥(5/8)(39/40)=39/64`。故 `η=1/40,γ=δ=3/8` 三重等号有效，n 不必被 8 或 40 整除。δ=0 的 NO_≥ 为空类，NO_> 按其独立合同解释；η=1、δ=1 域外，γ=1 与 E 不相容，不留合法端点漏洞。

LP 有 `S+I_+` 个变量、n 个等式、`I_+` 个链接和 m 个资源容量；菜单、参数总位多项式，无需按参数倒数或分母数值枚举。忽略零 x 变量只是福利表示，不删除物理调度 job。整个 robust 目标已付清，可继续 accepted / unconditional / ALL / whole。该判别没有提供 NP 难源的可靠编译器或一般 UM 结论；这些域外研究边界不应写成本边尚缺步骤。

## 5. 其余十资产、十核心和比较的继续处置

已逐一实际核前任 receipt 的 12 个资产，全部旧 SHA 与磁盘相同。两条本页 §3/4 的边在本任务新目录同名替换，保原 edge_id、方向、ALL、unconditional、accepted 和 whole_result；只刷新实际源证据并增加本页复核。其余十份资产原路径原 SHA 留存，包括 7 条其它边与 3 份旧阅读/审查记录，不覆盖旧历史资产。7 条其它边没有端点 pin 或直接 evidence SHA 差分。其 4 whole、1 contribution、2 context 边界继续成立。

四条其它 whole 分别是：ST 与 Karp 共同支付 common-b 双small 的三分支与实际 3DM 解码；复制原未剪枝点得到 `kF≤O_k≤kF+p_max≤kF+S` 和固定实例极限且显式 nk 成本；同一紧凑族每个 `(v,C)` 各自完整 CONFIG 点投影到整数容量 b-matching 后得到真实 count assignment；共同 `(M,T)` 位置 LP、槽费用匹配给同一个输出平均 ≤M、峰 ≤2T，保 `T_M*`。这些关系既未用本次 flat 零 job 补句，也无相关端点或证据变动。本轮新读其边全文与旧完整比较，原始各源成熟证明继续继承。

NC 边仅贡献固定 x 的期望、精确尾率与增长阶采样，row/count 包络仍在 contribution.remaining；不能把它升成完整资源 whole。14/18 机与 K2/S3 两条语境边仍不算逻辑 linked：不同矩阵不能互作特化，指定负 triple 的 K2 点缺 S3 完整前提，不否条件桥或另一实际调度。actual OPT=1 与 fixed-law/指定点失败并存。

十核心原六 linked、四 isolated-after-review 的实际比较全部保留。SH3 没有从本包其它端点取得共同 M3/native-home 全合同，负 triple 不能保矩扩 M3，紧凑共享 z 的 home 总工作也不符 1；其新一阶流到共享整数 owner 是原开放数学。稀疏深树逐 query 与奇 N 保二阶 law 的两个族保持分开，不能与紧凑单机 pin 按名称拼成共同 law。18/14 机对象仅有上述语境比较，不能变成调度否定。前任 17 条普通 comparison_outcomes 原样保留；任务当前没有 declared overlap/follow-up 对，closed_overlaps 与 follow_up_tasks 均为空，没有指向 stale 接续任务。已证两条边的边界不会改记 open 或 needs-decision。

本页及新 reading JSON 只补差分时点、独立数学核查与真实继承范围。worker 未运行 Git、native 队列、edge-bind/edge-check、全局 registry/coverage/integration 或科学重跑。语义审读已完成；父 Boss 下一步对新边进行原生绑定与检查，再刷新 receipt 中最终边 SHA，保存推送后 done。本页不预报这些后续动作成功。

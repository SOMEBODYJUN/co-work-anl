# 私有汇点族的独立重构、逐行合同与随机负相关审查

## 审查对象与独立性

审查者是 boss9 的内部 subagent `independent_row_attack`；没有独立推送、发表公屏或改共同登记。本审查不是外部评审，不作新颖性背书。

审查首先只取得以下精确问题，未读提出者证明：固定实常数 a,b>=1，x 是所有真实 OPT 整数调度 incidence vectors 的凸包中的有理点；研究逐行合同 `L_i<=a ell_i+b M_i` 下最佳实际 makespan/OPT 的 supremum。审查者先独立重构 ST 上界，并自行得到“K 个 home、每组 N 个大小 1/N 的 small、私有 sink、一个可去任意 home 的单位 big”的构造；之后才取得提出者 r=k^2 的同族证明。

随后读取提出者草稿：

- 最初受审对象为临时候选稿；规范正文现为 `research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md`。
- 被读取快照 SHA256：`597a8c077783b5bd8ca51a674803453343811a929b34c1b560aa440962ae4097`

该快照仍陈述更广 a,b>=0 的不相容性，没有声明下面完整的精确 supremum 结论；本审查将其与拟收窄至 a,b>=1 的正式主 Claim 分开。后续正文改动需要另核最终 hash，不能用本 hash 冒充已审最终正文。

## 一、一般输入上的上界、非空与退化情形

对于 x 在真实最优凸包的任意合法输入，支持边满足 p_ij<=OPT，且每行 ell_i<=OPT。理由分别是该边以正权出现于至少一个最优调度，和 ell_i 是最优调度的该行负载平均值。

对每行依 p_ij 非增排序，把 x_ij 体积依次填入 ceil(N_i) 个单位槽。原体积构成一个精确覆盖每个任务、每槽容量至多一的分数匹配，因此 Hall 条件成立，存在覆盖全部任务的整数匹配。同时满足：

`count_i <= ceil(N_i)`，`L_i <= ell_i+M_i <= 2 OPT`。

最后一个逐行负载结论来自：第一槽匹配任务至多 M_i；任一后续槽中的最大处理时间，不超过它之前满槽中每个分数任务的处理时间。把全部后续匹配任务向前一槽记账，所用分数负载总和至多 ell_i。空槽和未匹配机器槽只会降低负载。

所以在 a,b>=1 时，R_ab 对所有输入自动非空，无需额外“非空实例对”限制；其最优 makespan 比率至多 2。另对整数 b0>=0，合同 `count_i<=ceil(N_i)+b0` 也自动非空并有相同比率上界。合法输出可用全部有限边，不影响这个支持内上界证书。支持外存在极大处理时间不会使这个结论失效。

零值和空任务不构成漏洞：OPT=0 时全部支持边为零，上述匹配输出零负载并满足全部负载合同；空任务对应空匹配。比率声明只排除分母 OPT=0，不是排除这些输入的可行性要求。单可用机器、任意大有理分母不改变论证。精确排序、体积分槽及匹配的规模和算术位长均对给定 (P,x) 表示为多项式；此处没有声称能多项式求出真实最优凸包点或检验其 membership。

## 二、私有汇点下界与精确达到

取整数 k>=2、r>=k。一个 big B 在 r 个 home H_i 的时间为 1，不能去任何 sink。第 i 组有 k 个独立且有标号的 small，每个只能去 H_i 或其私有 Z_i，两端时间同为 1/k。它是 restricted assignment 合法输入。

调度 S_h 将 B 放 H_h，整组 h 移至 Z_h，其他组留各自 home。其 makespan 为 1；由 B 下界知 OPT=1。uniform average x=(1/r)sum_h incidence(S_h) 是真实最优凸包成员，并且

`ell_H=1, M_H=1, N_H=k-(k-1)/r`；
`ell_Z=1/r, M_Z=1/k, N_Z=k/r`。

任何合法输出令 B 落在 H_h，令 q_h 个该组 small 去 Z_h。由于唯一另一端就是 home，必有 `L_Hh=2-q_h/k`。若满足 row 合同，则

`q_h <= floor(a k/r+b)`。

令 q=min(k,floor(a k/r+b))。因 a,b>=1，q>=1，合同内最佳 makespan 恰为 `2-q/k`：下界如上，达到方式是将 q 个 h 组 small 去 Z_h，其他 small 留 home。所有 home 负载至多 2<=a+b，其他 sink 负载为零，选中 sink 的负载不超过合同。也可每组均移 q 个，结论相同。

令 r=k^2，q/k<=a/k^2+b/k 趋零，且对每个固定 epsilon>0 可选足够大 k 使最佳值严格大于 2-epsilon。结合一般输入上界，得到所审 a,b>=1 主 Claim 的 supremum 精确为 2。固定有限实常数的量词没有隐藏随实例变化；构造所有输入数均为有理数。不要求精确计算任意实常数 a,b，因其不是本定理待实现算法的输入。

计数合同在 r>=k 时有 ceil(N_H)=k、ceil(N_Z)=1。令 q=min(k,1+b0)，同样得到精确最优值 `2-q/k`，而不是仅一个算法的坏运行。放 q 个 small 去被选 sink 即满足被选 home 任务数 k-q+1<=k+b0；其他 home 的 k 个任务也合法。令 k 增大得计数合同的 supremum 亦精确为 2。

较宽草稿中 a,b>=0、a+b>=2 的达到结论同样由相同构造成立；a+b<2 则可令 k 大到连 B 所在 home 的合同都不可能满足。这是更宽合同可行性陈述，不能混成所有 a,b>=0 都自动非空或 supremum=2。

## 三、任意改善输出被迫产生的集中迁移

若任意合法输出有 C_max<=2-epsilon，则 B 所在 H_h 的私有 Z_h 至少接收 ceil(epsilon k) 个 small，因此 L_Zh>=epsilon；而其原均值是 1/r。相对 ell_Z+M_Z 的倍率至少 `epsilon k r/(k+r)`；r=k^2 时为 `epsilon k^2/(k+1)`，无界。

这是输出必要条件，未假设输出采用任何匹配、排序或槽。它不排除改选 x、直接用给定最优分解、允许某行正相关集中迁移或任意其他算法。本构造本身易求最优，故不提供 UM-TARGET-v1 的计算困难性。

## 四、独立有限精确枚举

独立代码：`tests/audits/unrelated_machines/independent_marginal_row_oracle.py`。

- SHA256：`1933bb8d44156fb5a1ad9c7c630e4042db8e5259d0cf04ad51c2d5ab9e77dec1`
- 结果：`evidence/runs/unrelated_machines/marginal_row_independent.json`
- 结果 SHA256：`14ad94837033996ff1ca91e21ddbbac3629334cce2811ac745aabf65776afe75`
- 运行：`python3 tests/audits/unrelated_machines/independent_marginal_row_oracle.py > <新输出路径>`；Python 版本见结果，整数/Fraction 无容差，无随机 seed。

它未导入共享数学实现，按每个有标号 small 的两个合法去处枚举每个具体合法分配，同时枚举 B 的全部合法位置。覆盖 (r,k)=(1,1),(4,2),(3,3),(4,3),(4,4)，分别检查 2、1024、1536、16384、262144 个合法分配，总计 281090 个。

每例核验真实 OPT、a,b 取 (1,1),(2,1),(1,3/2),(3,2) 的合同内精确最小值、b0=0,1,2 的计数合同精确最小值；并逐分配验证 epsilon=1/2,1/3 的集中迁移必要条件。全部通过。较大 k 的结果只核对解析恒等式和反算，不枚举调度。这些结果是有限 evidence；一般结论由第二节证明承担。

## 五、与经典 tightness 的关系及尚未取得的新颖性

审查者直接网络核对两个原始来源：

1. Shmoys–Tardos 1993，作者源 PDF `https://www.cs.cornell.edu/~eva/Approx.Algorithm.Generalized.Assignment.Prob.pdf`，印刷 p464 的 Fig.1 及 p465 的紧性说明。其例子是 m 个相同机器、一个大小 m 的任务、m(m-1) 个大小 1 的任务；分数点把大任务均分、小任务分别整数固定。保留这些整数边的舍入产生 2m-1 负载。这个 x 不是实际 OPT 凸包点：一旦所有 small 归属固定，任何 big 的整数落点都超 OPT=m。它是本构造很近的标准祖先；本构造增添私有 sink 及相关撤离，使均值点有真实最优分解，并把限制扩大为任意固定常数行/计数包络。该区别成立，不自动证明全球新颖。
2. Shchepin–Vakhania 2005，作者上传原稿 `https://www.researchgate.net/publication/220060026_Optimal_rounding_gives_a_better_approximation_for_scheduling_unrelated_machines`，§4 末、作者稿 pp9–10。单任务在 m 个相同机器上的例子给整数最优 p、最优可抢占均值 p/m，差 (1-1/m)p。这一例子单独不推出相对真实整数 OPT 的近 2 比率。本审查只在线核原稿该段及定位，不声称取得本地原始 PDF，也未重构该论文完整算法证明。

尚未做全领域优先权和重复定理搜索，不能称本结果新近似算法、困难性、新颖定理或可发表贡献。

## 六、新随机 Claim 的独立重构

这一节先只收到精确候选陈述，再独立推导，未读提出者随机证明。

设随机合法调度 Sigma 保留全部 x 边际。令 Y_it 指 small j_it 去 Z_i，Q_i=sum_t Y_it，H 为 B 所在 home 下标。只要求同一 sink 的不同 small 满足

`E[Y_it Y_iu] <= 1/r^2`，t!=u。

无需独立性，H 与所有 Q_i 可任意相关。任意结果都有 C>=2-Q_H/k。且

`E sum_i Q_i(Q_i-1) <= k(k-1)/r`。

对任意非负整数 v，有 v<=1+v(v-1)/2。因此逐结果

`Q_H <= 1 + sum_i Q_i(Q_i-1)/2`，

得到

`E C >= 2-1/k-(k-1)/(2r)`。

对 q=ceil(epsilon k)>=2，事件 C<=2-epsilon 强迫 Q_H>=q，故 sum_i Q_i(Q_i-1)>=q(q-1)。Markov 直接给

`Pr(C<=2-epsilon) <= k(k-1)/(r q(q-1))`。

常数正确，无遗漏因子二。给定边际条件相容，例如 small 各自独立按 1/r 去其 sink 即可，B 独立 uniform；也可以用下面精确达到的相关分布。

### 两个边界分别 sharp 的显式联合分布

固定 2<=q<=k，r>=k，且 rho=binom(k,2)/(r binom(q,2))<=1。r=k^2 总满足这些条件。

以概率 rho，均匀选择一个 sink h，均匀取该组 q 个 small 移入；再均匀选 k-q 个其他互不相同的 sink，各均匀选本组一个 small 移入；B 放 H_h。

以剩余概率，均匀选择 k 个不同的 sink，各均匀选一个本组 small 移入，并将 B 均匀放到这 k 个 sink 之一所对应的 home。其余 small 全留 home。

每个结果总共恰 k 个 small 去 sink。机器组置换对称和组内任务置换对称给所有 sink-small 边际 1/r，B 的所有 home 边际亦 1/r。固定同 sink pair 联合概率恰为

`rho/r * binom(q,2)/binom(k,2) = 1/r^2`。

集中模式的 C=2-q/k，非集中模式 C=2-1/k。所以任意 epsilon 满足 ceil(epsilon k)=q>=2 时，成功概率恰为 rho，达到上界；q=2 时 E C 恰等于上述期望下界。这是分别 sharp，不声称任意 q 的分布都达到期望下界。

可见 r=k^2 时，所有满足所述边际/负相关条件的输出的期望都趋近 2，成功概率上界对固定 epsilon 趋零。它仍只约束固定 x 上的这一类随机输出，不排除具有正相关集中迁移的最优混合、换 x 或一般随机算法。

### 随机分布的独立 Fraction 核验

- 代码：`tests/audits/unrelated_machines/independent_marginal_pairwise_oracle.py`
- 结果：`evidence/runs/unrelated_machines/marginal_pairwise_independent.json`
- 覆盖 (r,k,q)=(4,2,2),(3,3,2),(9,3,2),(9,3,3),(6,4,2),(6,4,3)。
- 对所定义联合分布的全部结果显式累加精确权重；检查总质量、B 边际、每个有标号 small 的 sink 边际、每对同 sink small 联合概率、每个结果的实际 makespan、期望、成功概率及反算。全部通过。
- 这是对六个有限联合分布的完整核验；一般 sharpness 由上面的对称性和精确联合概率计算证明。

## 审查结论与未解决义务

对收窄的 a,b>=1 主 Claim、ceil(N)+b0 计数 Claim、集中迁移必要条件及随机 pairwise-negative 期望/成功概率 Claim，未发现仍成立的 fatal 数学 objection。两种随机界的 sharpness 有显式一般构造。旧草稿应在定稿时明确 x 的真实最优凸包 promise、只对有限边求和、正式 Claim 的 a,b 范围，并补全一般 2 上界与非空，不能把较宽可空情形混入精确 supremum。

证明完成度、内部审查、外部评审、新颖性和主目标进度必须分轴记录：这里有内部独立重构及有限证据；没有外部评审、全球优先权确认，也没有 UM-TARGET-v1 的统一改善算法。后者仍是未闭合的主 proof obligation。

## 七、规范正文与规范代码的冻结复核

本节复核 `research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md`，覆盖其全部 §1–9，特别是后来加入的 §8 两种 sharp 分布与 §9 的正式精确上确界。审查对照基准为 Git 提交 `47fc71d61cfce748a96da09d2caea178b32b36b1`；该提交尚无这份正文、审查及下面三份私有汇点审计代码，故下述 SHA256 才是本次未提交新增内容的准确冻结指针，不能把旧提交说成已包含新结果。

| 规范资产 | SHA256 |
| --- | --- |
| research/current/unrelated_machines/optimal_hull_marginal_rounding_barrier.md | `f666b407757a58a856f0b76def86707da54ba4868430f9af5ccbaeb5aa2cdf21` |
| tests/audits/unrelated_machines/private_sink_marginal_barrier.py | `70ac45ca0ba393e704b1f4bf411f8a32913ea58d1621979f96ac2c088ed359d2` |
| tests/audits/unrelated_machines/independent_marginal_row_oracle.py | `1933bb8d44156fb5a1ad9c7c630e4042db8e5259d0cf04ad51c2d5ab9e77dec1` |
| tests/audits/unrelated_machines/independent_marginal_pairwise_oracle.py | `378962201d5446e095aa0ab94b4770b275e077a7cde647ccbc69d110d78a2bb4` |
| evidence/runs/unrelated_machines/private_sink_marginal_audit.json | `b52fb55499d7e2671cb61d78195b441f3911381b5ff5baff88757d8a07ecbbae` |
| evidence/runs/unrelated_machines/marginal_row_independent.json | `14ad94837033996ff1ca91e21ddbbac3629334cce2811ac745aabf65776afe75` |
| evidence/runs/unrelated_machines/marginal_pairwise_independent.json | `3f8c20d5ddf159b3abe2d155feca0bb332ea8beff2e6343f098bd34e6440dc9b` |

### 7.1 最终命题与证明覆盖

1. `UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1` 正式固定 a,b>=1，量词为每一组固定常数、所有合法 P 与真实最优凸包有理点 x；合同内集合非空，最优 makespan/OPT 的 supremum 恰 2。上界覆盖一般输入、全部机器同时负载、零最优值的可行性和支持外大边；比率仅取 OPT>0。逐行 a,b>=0 的不相容性另作宽版推论，不得把可空情况混入此 supremum。
2. 同一正文中的计数版本固定整数 b0>=0，合同为每机 count<=ceil(N_i)+b0；ST 同时保持 count<=ceil(N_i) 与 load<=ell_i+s_i，给非空及 2 上界。下界与精确达到 `2-min(k,1+b0)/k` 的整数端点已重核。
3. `UM-OPT-HULL-PAIR-NC-GAP-v1` 与前一身份不同：只限制固定 x 的全边际和同 sink small 的两两联合概率，不限制每态行负载。§8 的一般期望和截断尾界、它们不同的达到分布及达到所需参数条件均正确；特别没有将 B 与 small 独立化。§8.2 的“先选 h 再选其他组”与本审查先前的“先选 singleton 活跃组再选 B 的 h”定义同一分布，因为 `r*binom(r-1,k-1)=k*binom(r,k)`。
4. §5 的集中迁移倍率、§6 的换点和直接最优逃生口成立。这些接口没有改变 UM-TARGET-v1，也没有声称可多项式求最优凸包点、其分解或全部实例的好态。
5. ST1993 和 SV2005 的正文比较与本审查第五节相符。ST 的 tight 祖先保留积分 small，而本族让平均点真有最优分解；SV 单任务例只证相对可抢占分数值的加性差。来源层不能升级为全球优先权结论。

### 7.2 本次实际重跑与证据边界

三份规范 Python 脚本均由审查者独立重新执行，输出写到 scratch 新文件；全部退出码为 0，三份输出解析后的 JSON 分别逐项等于上述三份冻结 JSON，未覆盖冻结证据。主审计结果中的 code_sha256 也等于现行主源码哈希。Python 3.12.14，全部为整数或 Fraction；无浮点容差、无 seed。

- 主审计：Fraction 重构 (k,r)=(1,1),(1,3),(2,2),(2,4),(3,3),(3,4),(4,4),(4,16) 的最优调度与均值。完整分配枚举只覆盖前七组，另对 (k,r)=(2,3) 检查 (a,b)=(0,2),(1/2,1/2)。九次带参数运行累计 281530 个分配检查，同输入在不同参数下的重复枚举按运行计；最大单次 262144。主审计另外完整展开独立小任务分布的四个参数例，以及尖锐分布的六个参数例；后者包括 q=2 的五例及 (k,r,q)=(4,6,3) 的尾界例。
- 独立 row 审计：第四节所列 281090 个分配、四组 a,b、b0=0,1,2 及 epsilon=1/2,1/3。它不导入主生成器，矩阵和 x 来自独立构造；另有大参数公式反算，明确不是全分配枚举。
- 独立 pair 审计：第六节所列六个 (r,k,q) 的联合分布全部原子概率，核对每个有标号任务的边际、每个同 sink pair、期望和成功概率。它不导入主分布生成器；两份实现对非集中分布采用等价的不同选取顺序。

这些运行只支持其列出的有限 evidence；一般 supremum、必要条件和 sharpness 由正文的完整计数和概率证明承担。没有外部评审或一般近似算法实现验证。

### 7.3 相对基准提交的新增数学范围

相对 `47fc71d`，本审查确认的新增内容是：

- 一个有显式真实最优凸包证书的 restricted-assignment 私有汇点族，对任意固定常数 row 包络及有界额外槽给精确近 2 输出障碍；
- 通过已知 ST 上界合成两种合同的非空与精确 supremum 2，明确其下界不是 LP 的错误低估；
- 同一族的集中迁移必要量，以及固定边际/同 sink 两两负相关下的精确期望和尾概率边界，各有显式达到分布；
- 三份可复现有限精确审计与实际独立复核链；
- 与标准 ST tightness 和 SV 加性差的准确关系及全部逃生口。

本审查不覆盖同阶段另一个森林边界正文，也不将其他研究者此前的配置 gap、共享逃逸、条件配置探针计入本结果的新内容。私有汇点族受公屏固定槽讨论启发但不是照搬其原实例；一般 ST 工具、Markov 和对称平均计算仍是已有方法。新颖性未核，不因比率正确或谱系清楚就断言论文价值。

### 7.4 最终身份和范围修复已核

此前规范快照 `be6f02e723befc8ae3c901b1c245ce778d3ae3b73deba114f83182f1431d06e9` 的两个表述点已由正文作者修复并由审查者逐句重核：§1 Exact Statement 现明确 a,b>=1，较宽 a,b>=0 不相容性仅是附带推论；§9 最大成功概率等式现明确要求 r>=max(k,binom(k,2))。§8 仍保留更一般参数下的截断尾界与非截断右侧<=1 时的达到结论。两处范围不再有尚存歧义，本节表中的正文 SHA256 是修复后实际重读的版本。

对该最终正文全部承重结论，未发现仍成立的 fatal proof objection。结论是限范围方法障碍，而非 UM-TARGET-v1 的解决；一般输入的统一确定性 (2-epsilon) 位多项式构造仍未得到。新颖性未核，外部同行评审未发生。

### 7.5 实际输入和可逐原子核验的证书

后加入的两个资产亦由审查者独立读盘核验，未导入主/独立分布生成器：

| 规范资产 | SHA256 |
| --- | --- |
| examples/unrelated_machines/private_sink_k2_r4.json | `bb2f3c3c01a59b52c742fafc205b740d103141adeb42025afb1aef6b6f71f50b` |
| evidence/certificates/unrelated_machines/private_sink_opt_hull_and_nc_k2_r4.json | `4292fca54dd1090d36047732d48f0bef15a93117dbb9d0accdb232b9b58c9934` |

输入以 job-by-machine 方向给出 8 台机器、9 个任务的实际有理矩阵。审查重新枚举该矩阵的全部 1024 个合法分配，确认 OPT=1；4 个 weight=1/4 的证书调度均有 makespan 1，其平均给出完整 x。证书另给 52 个有具体 assignment 的正质量 NC 原子，逐项核查其合法性、总概率 1、全部任务机器边际等于上述 x、全部同 sink small pair 的联合概率恰 1/16。实际 makespan 仅取 1 和 3/2，期望精确为 11/8，且 Pr(C<=5/4)=1/4；反算 `(1/4)*1+(3/4)*(3/2)=11/8` 一致。

下面是本次读盘审查使用的完整简化复核代码；从仓库根运行，所有比较均为整数/Fraction，无容差，无随机性。它只核这个证书，不代替一般证明。

```python
# Independent file-certificate verifier: no research generator imports.
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json

ip = Path("examples/unrelated_machines/private_sink_k2_r4.json")
cp = Path("evidence/certificates/unrelated_machines/private_sink_opt_hull_and_nc_k2_r4.json")
I, C = json.loads(ip.read_text()), json.loads(cp.read_text())
assert C["input"] == str(ip)
k, r = I["k"], I["r"]
n, m = len(I["jobs"]), len(I["machines"])
assert (k, r, m, n) == (2, 4, 8, 9)
P = [[None if v is None else F(v) for v in row]
     for row in I["processing_times_job_by_machine"]]
assert len(P) == n and all(len(row) == m for row in P)
assert P[0] == [F(1)] * r + [None] * r
for j in range(1, n):
    i = (j - 1) // k
    assert [(z, p) for z, p in enumerate(P[j]) if p is not None] == [
        (i, F(1, k)), (r + i, F(1, k))]

def load(s):
    assert len(s) == n
    assert all(isinstance(i, int) and 0 <= i < m and P[j][i] is not None
               for j, i in enumerate(s))
    ans = [F()] * m
    for j, i in enumerate(s):
        ans[i] += P[j][i]
    return ans

atoms = C["optimal_schedules"]
assert len(atoms) == 4 and sum(F(z["weight"]) for z in atoms) == 1
x = [[F()] * m for _ in range(n)]
for z in atoms:
    w, s = F(z["weight"]), z["assignment"]
    assert w == F(1, 4) and max(load(s)) == 1
    for j, i in enumerate(s):
        x[j][i] += w
options = [[i for i, p in enumerate(row) if p is not None] for row in P]
all_makespans = [max(load(s)) for s in product(*options)]
assert len(all_makespans) == 1024 and min(all_makespans) == 1
assert C["optimum"] == "1"
D = C["pairwise_nc_distribution"]
assert len(D) == 52 and sum(F(z["weight"]) for z in D) == 1
marg = [[F()] * m for _ in range(n)]
pairs = {(i, t, u): F() for i in range(r)
         for t in range(k) for u in range(t + 1, k)}
expect, success, values = F(), F(), set()
for z in D:
    w, s = F(z["weight"]), z["assignment"]
    assert w > 0
    c = max(load(s))
    values.add(c)
    expect += w * c
    if c <= F(5, 4):
        success += w
    for j, i in enumerate(s):
        marg[j][i] += w
    for i, t, u in pairs:
        if s[1 + i*k + t] == s[1 + i*k + u] == r + i:
            pairs[i, t, u] += w
assert marg == x and all(v == F(1, 16) for v in pairs.values())
assert values == {F(1), F(3, 2)}
assert expect == F(C["expectation"]) == F(11, 8)
assert success == F(1, 4)
assert success * F(1) + (1 - success) * F(3, 2) == expect
print("certificate exact checks passed", "OPT=1", "E C=11/8", "success=1/4")
```

## 八、同步同行结果后的来源与范围复核

最终同步取得 boss7 的提交 `6c896be` 和 boss6 的提交 `dd2cf2a` 后，正文仅在末尾追加来源衔接段。审查者以字节截取该段之前的正文，除末尾空行外，其 SHA256 仍精确等于上一轮已审正文 `4dfc498a258da47803a2ce8da4be28397895cf568bb127aaf32877b86c2377ee`；因此没有悄悄改动原量词、一般证明、代码入口或证书。第七节表中的正文 SHA256 已更新为包含该来源段的最终字节版本 `f666b407757a58a856f0b76def86707da54ba4868430f9af5ccbaeb5aa2cdf21`。三份代码和三份冻结运行均未因本次来源说明改变，不为纯引用追加重复运行。

本次实际读取并重核：

- `research/current/unrelated_machines/optimal_convex_fixed_slot_gap.md` 全文，身份 `UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1` 及其独立修复身份。它给完全相同机器、所有边均为正且有限、x_ij=1/m 的真实最优凸包点。每机恰 m 个槽且任务总数 m²，故每个覆盖匹配每机恰 m 个任务；大任务机 makespan 精确 2m/(m+1)。离开该图后迁出 m-1 个 small 即恢复 OPT=1，最少修改数证明也有明确的大任务换机分支。来源段对此描述准确。
- `research/current/unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md` 第九节及其对象合同。`UM-COORDINATE-REPAIR-ST-GAP-v1` 是上述相同机器族加总工作量守恒的直接推论：合法调度总负载固定，所有坐标不升迫使所有坐标不变。它不是再造一个独立反例族，也没有排除低负载接收机上升。来源段未将此标准守恒推论误计为本文的新证明。

最终来源段已明确写为“分别给出这些明确合同的边界，不声称与同行命题构成整体严格推广关系”。这是必要的准确区分：固定槽图、允许固定额外数量槽的计数上限、常数行负载包络、固定边际的分布负相关，以及从一个已有调度出发的逐坐标过程，是不同的量词和输出限制。计数上限可放宽输出空间，不等于这几篇全部定理彼此构成严格推广链。

例如 boss7 族的真实最优调度在非大任务机器有 m+1 个 small，所以 ceil(N)+1 已可容纳其最优解；且 ell_i+M_i=2，本来就允许最优解。这说明单靠该特定相同机器族不能代替本文任意固定额外槽数或常数行包络的私有 sink 证书。另一方面，本文不把 boss7 原族或 boss6 的守恒推论重新归属给本组，也不据不同反例的可修复性推出一般算法。

本次追加没有改变前述审查结论：最终主张的精确合同与证明未发现尚存 fatal objection；本结果仍是限范围方法边界。全球新颖性、外部评审和 UM-TARGET-v1 的一般统一改善算法均未完成。

# 门控归一化菜单的完整作业舍入与源参数互补：作者证明

日期：2026-10-18。对应先冻结 Exact：[gated_normalized_menu_fslp_exact_first.md](gated_normalized_menu_fslp_exact_first.md)，SHA256 `591237d47b0330ebe6eb8d8daf509f467bc6fa663986905da13ce08ae40716e5`。作者证明晚于 Exact 冻结；没有修改 Exact。本文采用该文件 E1 的全部对象、零项及显式输入合同。独立攻击尚未发生；不称审查通过。

本页机制的边界：1−1/e 的 XOS 福利配置舍入属于已知工具。实际联网核读了 Feige 的 SIAM 原始摘要，其明确陈述 fractionally-subadditive welfare 的该比例：[2009 官方论文页](https://epubs.siam.org/doi/10.1137/070680977)，L64–68；另取得 Feige–Vondrák [FOCS2006 作者稿](https://theory.stanford.edu/~jvondrak/data/alloc-focs.pdf)的浏览器文本，但未以“取得”冒称全文重构。本页不把福利算法技术或数值常数冒称原创。新增研究用途是原 γ 互补错误、门控全部真实作业恒等与该源 promise 的显式 LP 判别。下文不依赖 NSW 长证明，也不把文献摘要当下述细节的证明。

## 1. 单个资源上的独立抽态不等式

给 E1 unit-FSLP 的有理可行解 λ。每组 g 独立抽一个 state s_g，概率 λ_gs。固定资源 u，设随机系数 X_gu=p_g,s_g,u；没有 incidence 时按零处理。不同 g 的 X_gu 独立。令 q_gu=Pr[X_gu>0]=Σ_{s:u∈P_gs}λ_gs，则 LP 逐资源恰给 Σ_gq_gu≤1。

对任何实数 t>0，令 a_g(t)=Pr[X_gu≥t]，z(t)=Σ_ga_g(t)。有 0≤z(t)≤1，独立性给

  Pr[max_g X_gu≥t]=1−∏_g(1−a_g(t))
                     ≥1−exp(−z(t))
                     ≥(1−1/e)z(t)。                                    (1)

第一不等式用 1−x≤exp(−x)，含 x=1 的分支；第二不等式是 [0,1] 上凹函数 1−exp(−z) 位于两端 chord 上方。z=0 时两边均零。对有限阶梯 tail 求积分（等价逐正系数水平作有限和），得到

  E[max_gX_gu]≥(1−1/e)Σ_gE[X_gu]。                                   (2)

对全部资源求和，归一化逐 state 总量一给

  E[Σ_u max_g p_g,s_g,u]
    ≥(1−1/e)Σ_gΣ_sλ_gsΣ_up_gsu
    =(1−1/e)n。                                                       (3)

这一步的逐资源占用是 positive support 的概率，不是 Σλp 的加权负载。若错用后者，(1) 中 z≤1 无从成立。也没有要求每个资源在所有 states 中的重数有界。

固定抽到的 states 后，把每个 u 分给在该 u 系数最大的某一组（按固定编号打破平局，最大零时亦可留未分配）。所得 bundles 是真实不交集合，其在抽到的 states 上的总质量恰为 Σ_u max_gp_g,s_g,u。因此 (3) 是可实现总福利的期望，不是允许分数资源或复制资源的效用。

## 2. 不枚举所有抽态的精确有理条件期望

全部原表有限。对资源 u，列出全部不同正系数

  0=a_u0<a_u1<⋯<a_uk。

若没有正系数，u 的所有贡献为零。部分组的 states 已固定，剩余组继续按原 λ 独立。定义

  F_gu(a)=Pr[p_g,s_g,u<a | 当前已固定组]。

未固定 g 时 F 是满足比较的 λ_gs 的和；已固定时 F 为 0 或 1。不同组仍独立，所以当前有理条件期望为

  E_current[Σ_umax_gp_g,s_g,u]
   =Σ_uΣ_{l=1}^{k_u}(a_ul−a_u,l−1)
           [1−∏_gF_gu(a_ul)]。                                      (4)

无理数 e 不进入这个公式。每轮取一个未固定组 g，对每个 λ_gs>0 的候选原 state s，用 (4) 重算该条件期望。当前期望是这些候选条件期望按 λ_gs 加权的平均，故至少一个候选不小于当前；选最大的，按 indexed order 打平局。λ=0 的 states 不选，但并不从物理矩阵删除它们。经过 n 轮，最后的确定总福利至少最初期望 (3)。再逐资源分给最大系数组，得到全部真实 bundles；可遍历本组原表重新选择 attaining state，效用只会增加。

由于 e>1+1+1/2+1/6=8/3（后续正项非零），故 1−1/e>5/8。因此输出 W=Σ_gr_g 满足严格 W>(5/8)n。算法没有比较近似的 e，也不需要知道初期望是否等于某个边界。

### 规模与位长

每个资源的不同正 level 数不超过该资源的显式 incidence 数，Σ_uk_u≤I。每次计算 (4) 只需扫描有限 λ 表、资源 levels 和组；至多 S 次候选条件期望计算，故操作数是 n,S,I,m 的固定多项式。可复用 prefix/suffix products 加速，但证明不依赖优化。

所有原 p 与 λ 均是二进制有理数。令 D_p 为原非零系数全部分母之积；每组 λ 的公共分母可取该组全部 λ 分母之积 D_g；D_λ=∏_gD_g。每个 F_gu 的分母整除 D_g，每个资源乘积的分母整除 D_λ，每个 level 差分母整除 D_p。式 (4) 的全部求和分母因而整除 D_pD_λ，值位于 [0,n]。这些整数的位长至多相应输入有理分母位长之和加 O(log n)，为多项式。重算而非重复平方，不会产生未付出的指数幂分母。精确约分的加乘比较可用标准大整数运算。

若 λ 未给，可先用标准确定性有理 LP 算法求 unit-FSLP 的可行解。该 LP 只有明确的 S 个变量和 0/1 系数矩阵，标准基本可行解有输入长度多项式位数。本文没有把浮点 LP 判“似乎可行”当作这个算法合同；有限实现仅接收、检查有理证书 λ，另见第8节边界。

## 3. 高质量组计数及严格边界

每个 r_g∈[0,1]。固定 0≤δ<5/8，令 h 是 r_g≥δ 的组数。所有其它组 <δ，特别均≤δ，所以

  W≤h+(n−h)δ=δn+(1−δ)h。

结合 W>(5/8)n，得到

  h>((5/8−δ)/(1−δ))n。                                             (5)

若 h 改为 r_g>δ 的数量，其余组 ≤δ，同一非严格上界仍成立，(5) 仍为严格号。因此 ≥δ 和 >δ 两个高端语义分别获得相同 count，但源 NO 的集合互补仍需区别。

δ=3/8 给 h>(2/5)n>(3/8)n。h 为整数，因此 h≥ceil(3n/8)，不需要 n 被 8 整除；实际上更强为 h≥floor(2n/5)+1。n=1 等小规模也照常成立。

## 4. 门控完整普通矩阵的值恒等：上界与全作业恢复

构造严格为 Exact E3 的 P_gate；总数为 1+n+S+m 台机器、1+2n+I 件 job、1+3n+S+2I 条有限资格。所有 labels 是新机器/作业的显式身份，四类互异；无 job 拒绝、无免费 source constraints、无不可见预载。

给 ∅≠H⊆G、两两不交原 bundles B_g，取各自一个 attaining 原 state s_g，令

  β=min(|H|/n,min_{g∈H}Σ_{u∈B_g∩U_g,s_g}p_g,s_g,u)>0。

构造具体调度：

* J0 在 R；对 g∈H，C_g 在 X_g、T_g 在 M_g,s_g；对 g∉H，C_g 在 R、T_g 在 X_g。
* 对每个 g∈H 的所选 state，只把与 B_g 对应的 positive incidence jobs 导出到其 Q_u；它的其他 incidences 留 private。
* 全部未选 states 的全部 incidence jobs 留其各自 private；零 incidence jobs 也留 private 零时间。资源没有 positive 导入时空置。

逐机真实负载：R 上为 1+(n−|H|)/n=2−|H|/n≤2−β；每个 X_g 恰承 C_g 或 T_g 一件 unit，所以负载一；未选 M_gs 的 incidence 总量一；选中 M_g,s_g 的负载为 1+1−Σ_{u∈B_g}p_g,s_g,u≤2−β；每 Q_u 至多一件 unit，因为 B_g 不交。β≤1，所以负载一也≤2−β。每一件列出的作业各在原有限端执行一次，未选 states 没有消失。

若 β=0 或 H=∅，另用完整峰≤2基线：J0 与全部 C_g 在 R，所有 T_g 在各 X_g，所有 incidence 留 private。根负载二，其余非空负载一。故 OPT≤2−β*，包括 β*=0。

## 5. 门控值恒等：从任意低于二的真实调度解码

给任意完整实际调度 σ，C=C_max(σ)<2。令

  H={g:C_g 在 X_g 执行}，s=|H|。

所有 connector 恰在 R 或 X_g，因此根负载精确为 1+(n−s)/n=2−s/n≤C，得 s/n≥2−C>0，故 H 非空。

对 g∈H，C_g 已在 X_g 上耗时一，T_g 若也在 X_g 将负载二，违反 C<2。因此 T_g 实际执行在某个本组原 state 根 M_g,s_g。该 state 的 incidence job 每件只可留 M_g,s_g 或外送其 Q_u，故设 B_g 为其实际外送的原 resource 集，便有

  L(M_g,s_g)=1+Σ_{u未外送}p_g,s_g,u
             =2−Σ_{u∈B_g}p_g,s_g,u≤C。

于是实际原 state 的外送质量≥2−C。每个资源机器只接 unit incidence；C<2 保证它最多接一件。因此跨选中 groups 的 B_g 全部不交。显式零外送 jobs 也占一单位，仍满足资源单占；解码时可忽略其零效用或保留资源身份，两者均不增福利、不导致资源复用。未激活 groups 偶然也外送的 jobs 只占用未选资源，直接忽略，不改实际负载或虚构新容量。

这给 β*≥2−C，即任意 C<2 调度有 C≥2−β*；C≥2 时由 β*≥0 同样有 C≥2−β*，但不在该分支误用 unit 独占。与第4节合成

  OPT(P_gate)=2−β*。                                                 (6)

两个映射只扫描原 jobs、端点与资源集合，并做精确有理求和；无需求解未知 β*。

## 6. FSLP 直接给所有作业的 13/8

若 unit-FSLP 可行，运行第1–3节，取 H={g:r_g≥3/8}。有 |H|/n>2/5>3/8，全部选中质量≥3/8，因此第4节 β=3/8 的完整调度使全部机器峰≤2−3/8=13/8。根实际还更低于 8/5；state 根控制 13/8。无 group 被丢弃执行：未激活者的 connector 在根、selector 在 gate，全部 states 的 incidences 仍执行。

这个论证不适用于原 flat 矩阵：原 flat 每个 group 的 selector 必须落在某个 state，不能把低质量 group 的 selector 停在新造 gate。gate 是本文明确的新构造，不是对 flat 最优值保持的变换。

## 7. LP promise decider 与 γ 互补

若有全部 n 组质量一的实际 allocation，有限 max 取得一。非负且每 state 总量恰一，质量一迫该 attaining state 的每个 positive-support item 都在本组 bundle 内。跨组 bundles 不交，因此选择这些 states 的 integral λ 是 unit-FSLP 可行证书。故 YES 必被 LP 判为可行。

反之若 LP 可行，第3节给一次实际 allocation 的高质量组数严格大于 f(δ)n，f(δ)=(5/8−δ)/(1−δ)。当 γ_hi≤f(δ) 时，这违反“每个 allocation 的 high_≥δ 数<γ_hi n”的 NO；high_>δ 版本同样被分别排除。因此 NO 的 LP 必不可行。确定性有理 LP 可行性便是精确 promise decider，不运行随机试验，也不检验未知 OPT。δ=0/high_≥ 的 NO 空类按退化语义解释。

δ≤3/8 时 f(δ)≥2/5≥3/8≥δ，故覆盖全部 0<γ_hi≤δ≤3/8。给定整数 high 数 h，不存在 ≥γ_hi n 个高组的子集等价 h<γ_hi n，包含 ceil(γ_hi n) 的非整除情形；没有暗用把 γ_hi n 四舍五入的例外。

现在定位旧 §F 的错误，而不改旧来源：旧 C–D 的 γ_bad 表示被迫低质量的比例；root robust NO 的 γ_hi 表示被禁止高质量的组数阈值。若 NO 是 high_≥δ 数 h<γ_hi n，则

  low_<δ 数=n−h>(1−γ_hi)n，

因而 low_≤δ 数也>(1−γ_hi)n。这恰可代 C–D 的低质量 count，γ_bad 可取任何略小于或等于 1−γ_hi 的固定值。若 NO 高端是 >δ，互补低端则为 ≤δ，严格 count 关系照样成立。

因此“C–D 要 δ≤c_eta<eta<γ_bad，而 root 源要 γ_hi≤δ，所以未覆盖”的比较把不同、互补的参数当成同一个 γ。C–D 本身及 (F.1) 对任意低质量 γ_bad 的不等式仍可正确；失效的是最后两个参数域段落对 robust root 来源作出的无覆盖判断。本文独立福利论证把该 corrected obstruction 加强为第7节明确常数，而不依赖 C–D 全证明。

这会排除以 E1 完整显式 norm1 菜单、全部组 perfect YES、所有 partial allocation tiny NO 定义的某种源困难性：它的 promise 已可被有理 LP 分离。若一个既有源编译器并不保 norm1、只给隐式指数菜单、YES 只近完美、NO 只控制整束/固定 labels、或需多层私有树一致性，则不能借这份 LP 直接判源。特别没有否定一般 Santa Claus 无常数近似假设，没有构造任何一般 UM 困难性，也没有从 LP gap 推导算法困难性。

## 8. 有限核验与尚未取得的证据

拟执行的 Fraction 核验应独立回算：(4) 与枚举抽态期望相等；每个条件期望决策不降；FSLP 精确合法；真实 bundles 与高质量计数；全部 P_gate jobs 每件一次、端合法、逐机峰≤13/8；小实例 (6) 由独立全调度枚举或所有 bundles 枚举验证。

尚未把有限核验作为一般论证前提；通用有理 LP 生产实现未声称完成。母文件中任何历史全审/新颖性状态不转移到本文。外审、新颖性、独立 Exact-first 与读后审查均待实际发生后另记。

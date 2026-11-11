# 67f2 恢复与独立复核

## 范围与结论

恢复任务 `unrelated-machines-3a-3a-67f21b35ba26bbc2` 已有边和收据。实读根 AGENTS、IMPLEMENTATION 的相关接口、worker 提示词、任务外层 definition、两端当前 registry 记录、共同正文全文及冻结 Manurangsi 九页 PDF 全文；新抽取文本为 31,835 字符 / 32,875 UTF-8 字节 / 九页。另实际查看冻结 PDF 印4、5、7页图，核 Theorem6、Lemma7、参数行、采样、Proposition8、Proposition12 和 union bound。只对同 ID 的其它边作定位检索，没有把检索片段升级为其完整证明已读。

当前两端 registration_pin 与任务一致；正文 SHA 为 `187fcaeed9bc5f98d04f60b9a137c7c117707674a670bed95d876a2529971217`，PDF SHA 为 `259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8`。没有修改 registry、队列、Git 或共享正文。

数学判定仍为 **accepted / conditional / whole_result / ALL**。稀疏化提供完整算法保证；外部 Chan/Laekhanukit 接口明确留在 conditions 中，不能仅由该源算法制造 NP-hardness。没有新增数学缺步或必须 read-add 的新端点。

## 稀疏化重核

非空 D-regular 显式全投影游戏，Q≥2、N=2n、M=Dn、0<γ<1。令 d=10^6·2ln(2Q)/sqrtγ。D≤d 时直接保原图；D>d 时独立以 p=10^-4 d/D 采边，再仅按中间度数一次标记并删除高度顶点的关联边。

1. **保持 N。** 低度分支 YES 从单标签赋值补每条未满足边至多两个标签，成本≤N+2εDn≤(1+εd)N。NO 的原图覆盖比例界本身已排除便宜全覆盖列表。无需原 PDF 的 copy-pairs blowup，N 不会被静默改变。
2. **删边尺度。** 条件于边已采样，任一端高度概率<1/d+10^-4≤0.0002；每条原边删除概率≤0.0004p，所以 E[R]≤0.0004pDn，Pr[R>0.1pDn]≤0.004。冻结 PDF 的 pΔn 无法由求和推出；当前正文已完整改为 pDn。
3. **便宜列表原图覆盖。** 成本≤0.06N/sqrtγ 时，以 L=0.3/sqrtγ 分 heavy/light。heavy 顶点数<0.2N，所触边<0.4Dn。假定覆盖≥0.5Dn，会留下>0.1Dn条 light-covered 边；独立从列表均匀取标签，每条满足概率≥γ/0.09>10γ，矛盾于 val<γ。空列表不见证覆盖，不引入除零。
4. **精确尾界。** 对固定列表的未覆盖边集 U，有 |U|>0.5Dn。取 Y=|U∩E_int|、x=pDn、s=ln2.5，二项 MGF 给 Pr[Y<0.2x]≤exp[-(.3-.2ln2.5)x]。系数约0.116741853625>0.1，故≤exp(-10^-5dn)=(2Q)^(-10N/sqrtγ)。这修复了原 PDF 的方向词和缺少1/2的普通 Chernoff 行，不能沿用其错误中间式。
5. **全列表同时性。** a=.06N/sqrtγ、t=floor(a)。非空全投影给 val≥1/Q，故 NO 下 Q>1/γ，尤其a<NQ。成本恰t的列表≤binom(NQ,t)≤(2Q)^(.5N/sqrtγ)；t=0单独计为1。最后对数不等式可直接看差值：.5ln(2Q)-.06ln(eQsqrtγ/.06)≥.44lnQ+.5ln2-.06+.06ln.06>0（Q≥2）。union bound 后与共同删边事件联合，以至少.98概率每份成本t列表仍留正数未覆盖边；向上补标签覆盖单调，遂同时排除所有成本≤a的列表，并保证好 NO 输出非空。
6. **近完美 YES。** 固定原单标签最优赋值，采样未满足边数期望≤.00005εdN。Markov 给超出.5εdN的概率≤.0001；补标签总成本≤(1+εd)N。不是每个seed的perfect singleton保证。

## 固定参数 gap 与量词

先固定整数g>1和外部合同常数C。取足够大最小素数幂q满足q/lnq>10^5Cg²，置s=C lnq/q、γ=2s、Q=q²。二次幂子序列保证q=Θ(g²ln g)，故γ=Θ(g^-2)、Q=O(g⁴ln²g)、d=O(g ln g)。

取ε=1/d、δ=min{ε,s/2}。同一外部正规化源满足YES值≥1-δ≥1-ε，NO值<s+δ≤1.5s<2s=γ<10^-4/g²。因此YES以至少.9概率OPT≤2N，NO以至少.9概率同时对所有输出后列表给OPT>.06N/sqrtγ>6gN>2gN。两promise分别对各自固定输入计概率，无须将互斥前提的两事件放到同一实例。N明确为外部正规化后的规模。

外部接口是：存在绝对C，对每个先固定q及δ，SAT可多项式归约到共同字母表q²、显式非空正度balanced regular全投影游戏，YES/NO达上述值。这包括正规化及误差账；本次没有实读Chan或Laekhanukit全证明，故关系保留conditional。没有把随SAT大小增长的g当成统一PCP参数。

## 位复杂度与算法排除

在主hardness固定参数合同内，可用固定整数预算d̂∈[d,d+2]，改取ε=1/d̂、δ=min{ε,s/2}、p=10^-4 d̂/D，并按d̂分支与trimming。全部尾界随预算不减弱。每条边使用b=ceil(log2(100M))个独立随机位，将p向下舍入到2^-b网格；每条Bernoulli分布总变差≤2^-b≤.01/M，整个M条试验总变差≤.01。故理想NO≥.98、YES≥.9999仍各≥.9，总随机位O(MlogM)。不依赖精确采样无理概率。

给定确定性g近似算法，检查其可行列表成本是否≤2gN即可区分好YES/NO。随机近似若按常数概率成功，也可重复得到有界错误SAT算法。因此NP⊄BPP足以排除这些算法，P≠NP本身不是本随机归约所需结论的充分替代。

## 交付边界

保持已有whole_result：外部合同和稀疏化共同支付完整目标，目标不是局部贡献。ALL没有拆成两个单独足够的支持。没有反驳目标，也没有仅凭引用造逻辑边。

partial-MinRep的线性degree、simple高围长、typed复制、MZ更小字母表、连通性费用模型及ordinary UM均不由本边自动推出。此次没有指定follow-up对象对；无需新增后续任务。冻结PDF的已知δ、pDn、尾界、γ字面域及N问题均已由当前正文修复，无新源勘误。

恢复时原边已通过edge-check、proof_scope=whole。最终重绑定/独立检查、端点/证据SHA与收据assets最终一致性另存validation.json；Git/push/done交父Boss处理。

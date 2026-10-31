# 正规高围长源 v3：冻结作者证明读后攻击

读取目的：在 Exact-only 独立重构后，专门核两侧 permutation 的 factorial-moment 上尾、短 cycle 延迟揭示，以及采样/ceil/修复细节。

## 实际读取与顺序

先行独立记录：`regular_high_girth_partial_minrep_v3_statement_first_review_row.md`，SHA256 `7493f719723990b2aa4416b151bef1c84e947eaa71392cd378c0195c9b26fc3d`。

该文件冻结并通知 root 后，才收到并实际 SHA、全文读取作者证明 `regular_high_girth_partial_minrep_v3_root_frozen_proof.md`，实际 SHA256：

`f43e32fa61899de87121c161e3ca51ac76dbaa47daccef5fce7a02ba8609e646`。

哈希匹配。未读取其他研究者的本候选审查。

## 1. 新 factorial-moment 简证有效

对一份 \([t]\) permutation 的 \(r\) 个不同 slots，单射 image tuple 的密度相对于独立均匀抽样为 \(t^r/(t)_r\)。递减序列 \(\ln t,\ldots,\ln1\) 的前 \(r\) 项平均至少为全体平均，故
\[
 (t)_r\ge(t!)^{r/t}\ge(t/e)^r,
\]
所以点态密度至多 \(e^r\)，对 \(r=t\) 亦成立。非单射 tuple 的真概率为零，不会反向造成问题。

任意 \(k\) 条不同 (layer,templateedge) 恰涉及 \(2k\) 个不同的 permutation-slot 对：每个 layer 的 template 是 perfect matching，因而同一 permutation 的同一 slot 不会被两条所选边使用。各原点/layer 的 permutations 独立，所以联合点态密度至多 \(e^{2k}\)。在 with-replacement 参照模型中所有这些 slots 独立，每边覆盖概率确为其 \(q_e\)，边间也独立；因此作者的乘积界与 factorial moments 正确。

有限展开恒等式 \(\mathbb E(1+s)^Z=\sum_k\mathbb E\binom Zk s^k\) 给 Poisson 型 MGF 上界 \(\exp(e^2\mu s)\)。在 \(a=\rho M'/2\) 时，\(a>e^2\mu\)，因为 \(e^2\mu/a<e^2/(50g^2)<1\)。故可取正 Chernoff 参数，作者的
\[
 \Pr[Z\ge a]\le(e^3\mu/a)^a\le\exp(-\rho M'\ln g)
\]
成立，且强于我先行记录的 slot-cap witness 尾界。全部列表的生成函数计数及最后 \(\exp(-249gN'\lambda)\) 并界亦正确；没有把不同 copies 的列表偷偷合并。

作者第 1 节用 heavy **copies** 而非我的 heavy 平均原点，也成立：均匀原边再独立均匀取 copies 的两端边际在所有 copies 上均匀；light-covered 见证被随机抽中标签的概率至少 \(H^{-2}\)。\(\tau/(2H^2)=\rho^3/(32\cdot10^6g^8)>\gamma\) 的常数正确。

## 2. 短 cycle 延迟揭示与 switching

闭合一个 simple cycle 的末色必须同时不同于首色与前一色。沿 prefix 揭示的每个 matching edge 同时揭其配对 template slots 的两个 images，所以已揭 slot 集对 template mate 关系封闭。末端当前 copy 在末色未出现，反像 slot 未揭，则其 mate slot 也未揭；目标起点在末色亦未揭。因此末步 image 在剩余 copies 中均匀，闭合概率至多 \(1/(t-G)\)。这个补充说明也排除了“mate 已揭但错误地称 fresh”的潜在疑问。每个原 fiber 在此色最多已有 \(l-1\) 次边揭示，分母下界有效。平行 2-cycle 使用两个不同 layers，仍满足相同论证。

由此 \(\mathbb EX\le NtS/(t-G)\le2NS\)，Markov 常数正确。排除全部短 cycle 上的 vertices 是比排除短 cycle 边更强的选择条件，但顶点数至多 \(GB\)，同 bucket 是 matching，足以保证仍可找到 \(f\)。switch 的两种新 cycle 路径配对覆盖所有可能；不会新生短 cycle，故反复选择性和至多 \(B\) 次成立。

修复最多增加任意列表 \(2B\) 条覆盖，且 \(t\ge z\ge8B/(\rho m_*)\) 给 \(2B/M'\le\rho/4\)。对初始全部列表的同时事件直接使用这个确定界，无需重做并界。simple、balanced、精确 \(d\)-regular、投影继承及完美 YES 保留均正确。

## 3. 采样份数的保守多计与其余细节

实际是每个 layer、每个原顶点一份 permutation，总数 **\(dN\)**，Fisher–Yates draws 正好 \(dN(t-1)\)。作者第 6 节“有 \(2dN\) 份”不是精确份数；应读成一个保守上界。其后的 draws 上界 \(2dN(t-1)\) 仍合法，配原算法不变的 \(R=\lceil\log_2(2000dN(t-1))\rceil\) 得采样 FAIL 至多 \(0.001\)。用实际份数可加强为严格小于 \(1/2000\)。这个多计不影响任何概率或最坏复杂度结论；canonical 宜明确实际份数，勿把 \(2dN\) 当精确算法定义。

每个接受事件不偏置接受值，且所有 draw 的 bounds 预先确定，因此条件全部成功仍为独立 uniform permutations。cycle FAIL 至多 \(0.05\)、soundness 坏事件小于 \(0.001\)，合并概率足够 Exact 的 \(<0.1\) 和 \(\ge0.8\)，无独立性误用。

\(Q\gamma\ge1\) 的数值控制、固定 \(G\) 的 polynomial 输出/随机位界和 rational ceil 运算均正确。对于显式区分平行 edge IDs 的 cycle 枚举，安全复杂度可写 \(O((N'+M')^G)\)，而非我先行记录里不必要的简写 \(O((N')^G)\)；两者只需固定 \(G\) 的多项式结论，Exact 未承诺那个精细次数。

## 结论与范围

没有发现 fatal objection。作者更短的 factorial-moment 证明成立，可替代较保守 slot-cap witness；采样份数是保守多计，建议如上澄清。本文没有升级 PCP 原文核查、新颖性、实现或一般 UM compiler 状态。旧冻结记录保持原字节；本文件是独立的读后记录及复杂度措辞补充。

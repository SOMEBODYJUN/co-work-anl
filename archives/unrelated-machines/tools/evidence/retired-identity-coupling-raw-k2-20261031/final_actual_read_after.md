# 稀释共享终端 raw K2 锐二倍间隙：最终稿全文实读

作者：/root/sol_identity_coupling，2026-10-18。此为知情 final actual-read，不冒称新 blind review；与本人此前的 Exact-first 独立重构、作者 Proof 实读后记录分别保存。

## 1. 本次实际阅读对象与边界

本次完整实读 diluted_shared_terminal_raw_k2_canonical_final_v1.md，SHA256 7128241668e8f7b5abe014775f9d0d3b4f59a5bfecbb2f1aef8e357272bb01b4；实核 19100 bytes、245 行。按 1–130、131–245 两块读取，两块均未截断，覆盖全部十二节及最后的软件范围段落。

历史次序为：先只读 Exact 25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b；独立重构冻结为 622cafcc002d4b507ae8905cf2b4d2cc0cc16f538b33974f51695bd9fb58cb0f；root 实际全文读后释放作者 Proof 2e926c6471c68843602f78c101874198e0ad2808b8db12d737cc8a04f27ad948；本人再完整实读并冻 read-after f960b9f1cf8751aa82396c286929a950e3fa1ef563ea3b2deee5a4eff1f5e4b9。新 final 是本次另作完整攻击的实际对象。

未读 final 所链的新 review；未读或执行 finite audit 代码及 root replay。Higher-d 的后续作者合作思路不作为本 v1 的前提、证明或认证。Source final、旧 records 与 repo 均未修改。

**结论：最终稿的明确 raw K2 合同、全族实际 gap、全球 localizers、显式总位成本，以及全类间隙上确界等于二的新增论证均核通；未发现 fatal。**

## 2. 完整 ordinary P 编码与实际下界

机器 \(M(1+L+k)\)、jobs \(1+Mk(1+L)\)、finite endpoints
\[
E=M+Mk(1+L)+MLk(1+k)
\]
逐个对应原 h、f、e 及其全部 finite eligibility，没有把多 head 的一枚 job 拆成不同 jobs。不同组件和 U/B/Z 类型物理不交；只有 h 跨组件选择。

\(L=2k^2,\ M=1+120k^6\) 均为明确整数多项式。机器数为 \(O(k^8)\)、jobs 为 \(O(k^9)\)，所以完整 dense matrix 的 \(m n=O(k^{17})\) 个位置连同 infinity 单元均可显式写出，finite times 位长 \(O(\log k)\)。本稿没有把 sparse endpoints 当成对 log k 的 succinct 输入承诺。

对每个完整实际 schedule 的 makespan \(C<2\)，h 所在 U 迫至少
\[
r=k-\lfloor k(C-1)\rfloor=\lceil k(2-C)\rceil
\]
枚 f 去不同 B；每个这些 B 又迫至少 r 枚 e 去不同 unit terminals，故 \(r^2\le k\)。这对每个 h 模式都成立。取 \(\lfloor\sqrt k\rfloor\) 枚 f 及每个所选 B 的同样数量 e，配到互异 terminals，并将**全部**其他 jobs 留 home，确实达到
\[
\operatorname{OPT}(P_k)=2-\lfloor\sqrt k\rfloor/k.
\]
若 C 至少二下界显然；\(k=2\) 的 attaining schedule 及公式也包含。因此实际 gap 不是由矩法则的坏支持点冒充出来。

## 3. raw 合同与共同矩完整性

最终第3节精确为 raw assignment variables 的共同四次表、原 Boolean/exclusivity/cover identities、global raw M2、每机 CONFIG first/pair 及所有全局 affine load localizers。未将外给合法配置分布偷换成共同 Boolean CONFIG-indicator M2；这个更强合同已显式分开。

全局有限 law 在每个 sample 中使每原 job 恰执行一次；条件于 I，组件之间独立。故全部原 identities 和 M2 直接成立。Law 中 selected H 的部分 B 负载为二，所以它不是 strong schedule law；其可延高阶 PSD 不代表高阶负载 localizers 或同机 CFG moments 也延拓有效。

## 4. 全部原机 CONFIG 与低阶矩

U 的真实 marginal 是 h-alone、各少一枚 f 的 home 配置及 all-home，全部 load 至多一。Terminal 的真实 marginal 为空或一枚 unit job，指定 singleton 权重
\[
\frac{(1-a)(k+1)}{4Lk^2}
\]
和 distinct pair 零均正确。

B 的四类真实 row events 和五类合法替代 CONFIG，与已独立重构的(1)(2)完全一致。全部 unit/home first、unit-unit distinct pair、home-home distinct pair 和 mixed pair 均按原 labels 逐项匹配；diagonal 由 Boolean 性给出。可能含差的两项质量由
\[
M-1\ge4k(k-1),\qquad M-1\ge4k^2
\]
支付，五质量总和为一，最高 legal load 为 \(1+1/k\)。没有遗漏组件、终端或原 tiny job 的 endpoint。

本 v1 不匹配同 row triple：对不同 \(\ell,\ell'\)，
\[
F(R_jY_\ell Y_{\ell'})=p/k=a/L>0,
\]
而 legal CONFIG 在一枚 unit 外最多含一枚 home，因此该 triple 为零。这个限度在最终稿明确保留，不因另有 higher-d 合作被回填。

## 5. 单组估计及所有全球 affine contexts

对每个 B row，H 下 slack 的均值为 \(1/(2k)>0\)、绝对值至多一，Q 下 slack 逐点至少 \(1/k\)。对任意单组 affine q，包括任意截距和全部 e-head coefficients，最终 §7 的两界为
\[
E_Qq^2\ge\|c\|^2/(30Lk^3),\qquad
E_H[gq^2]\ge-2\|c\|^2.
\]
前界由 \(q_F-\sum q_N+(k-1)q_0=c_{j,b}\)、三项平方和界及 permutation 单边际推出；常数
\[
12kL+12Lk^3+6kL(k-1)^2\le30Lk^3
\]
对全部 \(k\ge2\) 有效。后界的 coefficient 是 \((1+2k)k/L=1+1/(2k)\le2\)，没有假定 injection labels 彼此独立。

对全输入任意原 affine q，先消去 home，再条件化 I。所有其他组件表达式减去 conditional mean 后与被测组件独立，贡献恰为
\[
E[g\mid I]\sum_{j\ne i}\operatorname{Var}(q_j\mid I)\ge0.
\]
所有 selector endpoints 的系数均进入可随 I 变化的截距；上述单组界对这个任意截距一致。因此最终 §8 完整给
\[
F[gq^2]\ge
\left(\frac{1-a}{30Lk^4}-2a\right)\|c\|^2=0.
\]
这里明确 \(M-1=60Lk^4\)，无随全球维度增长的隐藏连续性常数、没有只核局部小 block。U/Z 的 slack 又逐点正，故所有原机、所有跨组件 contexts 均覆盖。\(\|c\|=0\) 仍由同式覆盖。

## 6. 全参数证书的确定性总位生成

Degree 至多四的 monomials 数为 \(O(E^4)\)。每个 home 因子只作原 job complement 展开，最多四个因子，所以总展开项数仍是 E 的固定次多项式；同 job 不同头先判零、重复因子 Boolean 合并。

Condition on I 后至多四个组件非平凡。H 使用至多四阶 partial injection；Q 使用 at-most-one-f-head 和至多四阶 partial permutation，或单 e-export。有没有 f-head 时的 full-export 系数分别为 \(1/(4kL)\)、\(1/(4L)\)；空 monomial 与不合法次数情形单独处理。故从未枚举指数多个完整 injections、permutations 或全局 samples。

有限阶 falling factorial、selector 权重及 polynomially many rational sums/products 的位长均为显式 expanded input 的多项式。CONFIG lists 的大小和各 localizer/M2 条目数亦为固定多项式。最终稿正确将此称为特定证书的生成，不声称一般 exact SDP 或 CONFIG feasibility finder。

## 7. 二倍上界的独立完整核对

给任意普通 UM 的 raw K2 可行目标 \(T>0\)，置 \(y_{jv}=F(x_{jv})\)。原 cover 等式给 \(\sum_v y_{jv}=1\)，CONFIG first 一致性给非负 y、每机 fractional work 至多 T。若 \(y_{jv}>0\)，该 endpoint 出现在某个正质量 legal CONFIG 中，非负 processing times 因此给 \(p_{jv}\le T\)。

对每行按 processing time 降序连续放 fractional assignment mass，切成容量一 slots，最后一 slot 可以不足一。Job-slot fractional matching 覆盖每个 job、各 slot 容量至多一，由普通二部 matching integrality 取得覆盖全部 jobs 的整数匹配。

第一 slot 的 matched job 时间至多 T。任何第 \(\ell\ge2\) slot 若 matched，前一 slot 是完整 slot，且其全部处理时间均不小于该 matched job 的时间。因此该 job 时间至多前 slot 的 fractional work。不同 matched slots 对应不同前 slots，所有这些 work 总和不超过原行的 total fractional work。于是该行完整整数负载至多
\[
T+\sum_jp_{jv}y_{jv}\le2T.
\]
未匹配 slot 不收负载；第一 slot 为空、整行为空、零时间 jobs、最后不足一 slot 都不破坏比较。Infinity endpoints 从未在 fractional support 中出现。

总 slot 数至多 \(n+m\)，因为总 fractional mass 为 n。排序、按累积有理 mass 切点、建二部图和 matching 都在给定有理 first point 的总位长多项式时间内完成，不需要按分母或最小正概率倒数复制。故最终第10节的二倍上界是完整论证。

## 8. infimum、supremum 与缩放

对实际 OPT 正且 raw 可行目标集合非空的 P，最终稿定义
\[
\tau(P)=\inf\{T>0:\text{raw K2 在 T 可行}\}.
\]
由每个可行 T 都有 \(\operatorname{OPT}(P)\le2T\)，该集合全部 T 至少为 \(\operatorname{OPT}/2>0\)，所以 \(\tau>0\)，并可取 inf 得
\[
\operatorname{OPT}(P)/\tau(P)\le2.
\]
不要求 infimum 达到，也不调用可行性 oracle。实际 schedule 的 Dirac raw moments 加其逐机确定配置总可作相同目标的证书，故该 raw 系统确为实际 OPT 的 relaxation；此项从定义直接成立。

对本族已有 \(\tau(P_k)\le T_0\)，因此
\[
\frac{\operatorname{OPT}(P_k)}{\tau(P_k)}
\ge\frac{2-\lfloor\sqrt k\rfloor/k}{1+1/k}\longrightarrow2.
\]
这与全类上界合起来恰证明**上确界为二**，并未声称每个 \(P_k\) 的精确 raw threshold 等于 \(T_0\)。

缩放所有 finite times by \(k/(k+1)\) 时，legal CONFIG loads 与物理 slack 同乘这个正数，raw moments 和列表权重不变；target 变一，实际 OPT 同步缩放。无未缩放单位 job 或遗留外部负载。

## 9. 反证条件与有限软件的诚实范围

\[
F[A_i C_{i,b}(T_0-\mathrm{load}_B)]
=a(k/L)(T_0-2)<0
\]
直接在 H 命中 B 的事件上计算得到，逐原 incoming endpoint 分拆仍负。它说明本点不满足更强跨行两事件条件；同 row triple 的不匹配也已明确。Joint-CONFIG-M2、canonical export gates 均未由此 raw certificate 提供。

第12节的有限 audit 声明定位在 \(k=2\) 的 121 个局部 H/Q states、50维 affine frame、该 B 的 first/pair 与 weighted localizer Gram。本次未读 code、未读 JSON、未执行 replay，不认证其 pivots、代码 SHA 或 root 的逐字运行结论，只核该状态叙述没有冒称全球矩阵重放。

\(k=2\) 时 \(L=8,\ M=7681\)，\(\operatorname{OPT}=T_0=3/2\)，所以有限 audit 比值一。Final 已明确这不是有限数值 near-two 证据；任意大 k 的 gap 来自全文解析证明。未以该局部 frame 代签所有 components 或无穷参数。

本次完整 final 数学实读通过，不把 higher-d 新推导、未读软件、未知链接审查或原历史稿合并进该 ID；一般 UM hardness、native canonical-C2 gap 和主目标仍 OPEN。

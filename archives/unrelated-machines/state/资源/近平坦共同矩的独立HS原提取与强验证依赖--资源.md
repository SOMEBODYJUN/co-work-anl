---
id: "unrelated-machines/near-flat-independent-HS-extractor-and-strong-helper-validation"
kind: "resource"
type_tag: "资源"
title: "近平坦共同矩的独立HS原提取与强验证依赖"
status: "complete-primary-code-read-and-exact-old-run-reuse"
truth_status: "conditional-or-finite-backend-evidence-with-explicit-model-boundaries"
summary: "保Greedy G-HS核心、全空间迹小缺陷门槛、21实际矩输入及168原子；依赖helper强于C2-load，零态和大缺陷范围分开。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/near_flat_hs_independent_audit.py#全文"
evidence_manifest: "archives/unrelated-machines/tools/evidence/um-following-actual-checks-primary/README.md"
---

主源e7775b9dc03055d338e7，10287B，SHA01fe0eec81d789d685e2bf264ecb2ebc896153939b27f9f216f35d4e7f866927，全部独立核心、生成器和main实读。它导入global_assignment_flat_moment_audit.py（16133B、SHA1dfcaee91aaa6886dae201f5b796decbab9e2b667bb96ff24285a6a00c118666），该同SHA helper先前已完整实读，本批再核字节。独立部分是选择/HS/密度及loss；共同矩构建、精确验证和有理线性代数来自helper，不能称完全无规范依赖。[原件、全部21真实输入/原子/轨迹及绑定](../../tools/evidence/um-following-actual-checks-primary/README.md)保全。已有[共同矩helper资源](共同矩有理Gram平坦原子与低阶Latin点原入口--资源.md)与[近平坦审查](../审查/近平坦HS矩提取与负接口有限审计--审查.md)承担一般数学，不重复授予。

## 核心真正接收什么

greedy_hs接jobs、T、η、变量和r2共同矩y，不接造矩原子。job为机器→精确处理时间字典；n>0时要求所有有限p∈[0,T]。operators调用helper.validate，选低阶Gram独立基，G=L(bbᵀ)，H_e=L(bbᵀx_e)，A_e=G^−1H_e；检查0≤H_e≤G、G(A_e−A_e²)半正定及每job的ΣA_e=I。

helper实际validator还要求每存储矩条目在[0,1]、所有正时间阈值的prefix-count localizer，强于数学near-flat定理最小C2-load的共同PSD/one-hot/负载localizer。不能用此helper拒绝证书反驳较弱定理，不能把测试额外条件倒加入主声明。此源没有通用矩生成器或SDP finder。

G-adjoint为K†=G^−1KᵀG，HS²=tr(K†K)。D_e=A_e−A_e²≥0（G内积），δ_e=tr D_e，δ=Σ全部端δ_e，R=dim G；这是全空间迹，不是常数state的零缺陷。NF门槛

\[
\delta\le\min\{1/(64ndR),\eta/16\}.
\]

main的η恒1/10；函数没有另建稳健外部参数验证产品，不能据受控生成器说所有格式/η边界都已测试。

## 独立贪心和共同负载证书

K初I；按原job顺序遍历该job所有端，取最大||A_eK||²_HS并左乘，等分保先遇端（变量按机器排序）。ΣA=I保证K非零时至少一子分支正，不需要逐轮指数小概率选择。NF下更强：任意t前缀由缺陷及共同矩交换子界给||K_t²−K_t||≤nδ。令a=nδ，则s(1−s)≤a。当前所有子HS²之和至少1/8，最大者≥1/(8d)，其范数≥4a，排除小范数根，从而每前缀范数≥1−2a，最终HS²≥961/1024。

最终ρ=KK†/HS²，trace1。对每选端e，穿过较晚因子的交换误差给γ_e≤δ_e+2√(nδδ_e)，γ_e²≤(8n+2)δδ_e。用I−A_e=(I−A_e)²+D_e及NF，loss=1−tr(ρA_e)≤(1184/961)δ_e<3δ_e。程序逐选端核此界；δ_e0时还无条件核loss0。

所有机器共用同一ρ及负载算子S_i=Σ_(e在i)p_eA_e≤TI，因此实际原σ负载

\[
L_i(\sigma)\le tr(\rho S_i)+3\sum_{e\text{选且在i}}p_e\delta_e
\le(1+3\delta)T\le(1+\eta)T.
\]

这里用已剪枝p≤T；不把主实现另允许的未剪枝接口混入此更强界。ρ不是调度分布，最终σ直接由所选原端构成；不借造矩原子反解。所有计算有理，没有在算法中求平方根或特征值。

## 实际run的全部输入

两macro/micro输入有5job/4机器：宏在home0/1耗1，两个home各两微job在原home耗1/2、专属sink耗1/4。全部真实T1调度8份，degree1特征rank6，选6基原子及2稀有原子；总稀有质量q分别2^−30、2^−80，基均分1−q。两例rank M1/M2=6/8，均 genuinely nonflat，却满足NF，门槛1/19200，实际输出峰1。

第三例4unit job/2机器、均匀六份balanced原最优T2调度，rank4/6、δ4、门槛1/8192，不满足NF，输出峰2。再seed20261016取18个3机器4job、每job恰两个端、时间1/4..1，保真实T1调度≥6且支持数大于degree1 rank，给各可行调度正随机整数权归一。全部21输入保完整job字典、原子、前缀HS、δ、阈值、assignment、负载和selected losses。

21例共2小缺陷通过（均非flat）、19普通大缺陷；本有限run的所有输出都≤其T，最大观察比1。这不是大缺陷的一般保证，也不是后来的9job/3机器HS二倍反例；不能把没观察到overshoot改写成算法正确。另empty jobs直接返回空σ/空loads且不做operators；两个T0零时间例含zero-effect，均通过；这些3边界不计入21。

## 运行复用与自查

旧6e5b…同时绑定当前独立码与helper SHA，保存全部上述21输入和3边界；本批原main新run0，未重跑已完成helper main。新增数据核全部168原子真实资格/负载、368小输入候选σ的支持集、21对特征rank、86项输出job、NF算术和已存loss界；未从头重算traceδ或Schur PSD，准确依赖旧同SHA执行。CLI的--output必给但write_text可覆盖，原运行/本次复用不得指向已有冻结输出去重跑。

一般近平坦定理需要额外显式共同矩证书，普通输入上如何生成不免费；原T普遍强近平坦生成还受已存3/2归约限制。此源只测试受控真实分布证书和条件提取；外审、新颖性、任意大缺陷共同舍入及UM主目标未由本程序取得。

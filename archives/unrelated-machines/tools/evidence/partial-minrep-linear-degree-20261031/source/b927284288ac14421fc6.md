# 部分Min-Rep的线性degree源：v2独立Exact Statement

候选ID：`UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2`。

本文件只给精确陈述，供未看证明者独立重构。它改变v1的soundness、采样参数及g的对象域，不能与v1混用。v1冻结文件保持原字节；本v2不宣称新颖性，也不是UM困难性或实际调度编译器。

## Objects、Domain、Definitions

输入是显式有限D-regular二部projection game

Π=(A,B,E,Σ,{π_e})，

其中D≥1，|A|=|B|=n≥1，N=2n，Q=|Σ|≥2；每个π_e:Σ→Σ都是显式总映射。允许同一对端点之间的平行constraint边，分别计数、分别采样、分别计degree。value是单label赋值满足的constraint比例。

multilabeling ψ给每个顶点一个Σ子集，允许空集。cost(ψ)=Σ_v|ψ(v)|；边e=(u,v)被覆盖指存在a∈ψ(u)、b∈ψ(v)使π_e(a)=b。非空图上的coverage是覆盖边数除以全部边数。

附加输入为二进制整数g≥2及二进制有理0<ρ≤1。令

\[
\ell=\lfloor\log_2g\rfloor\ge1,\qquad
\lambda=1+\lceil\log_2Q\rceil,
\]

\[
\tau=\frac{\rho}{100g^2},\qquad
\gamma=\frac{\rho^3}{10^9g^8},\qquad
\mu=\left\lceil\frac{1000g\lambda}{\rho\ell}\right\rceil,
\qquad \Delta=1000\mu.
\]

## Exact Statement、Quantifiers、Conclusion

存在一个随机删边算法，对每个上述合法输入输出同顶点、同alphabet、同剩余投影的Π′，并有：

1. 对每个随机种子，输出maxdegree≤Δ。
2. 若val(Π)=1，则每个随机种子输出仍有cost≤N的singleton multilabeling覆盖全部剩余边；Π′无边时本性质按真空解释。
3. 若val(Π)≤γ，则以至少0.9的概率，Π′非空且**每个**cost≤gN的multilabeling在Π′上覆盖严格少于ρ比例的边。
4. 算法的运行时间、随机位数和输出长度按显式Π及g、ρ的总二进制编码长为多项式。没有按g、1/ρ、μ或Δ的数值做长循环。

具体随机规则也固定如下。若D<2μ，原图原样输出；否则取最小整数s使2^sμ≥D，每条原边独立按p=2^(−s)抽取。得到中间图后，删去所有在**中间图**中degree>Δ的顶点的关联边；只按这一次中间degree判定。所有边随机位独立；无需真实数随机采样。

## 固定参数source推论及复杂度假设

使用已知perfect-complete Label-Cover PCP和parallel repetition后，对每个先固定的g≥2、ρ∈(0,1]可从SAT得到本页输入promise，且Q≤poly_ρ(g)。允许先作精确保value的biregular→regular及共同alphabet正规化；这两步的具体构造和外部来源另见独立证明稿。

因此该输出source有Δ=O_ρ(g)。SAT归约的多项式指数可依赖先固定的g、ρ；不声称把随SAT输入增长的二进制g代入整个PCP链后仍得到统一多项式归约。上述第4项仅对给定显式Π的删边算法作统一总位复杂度保证。

归约是随机的：YES每个种子保留，NO以至少0.9概率满足上述cheap-list禁令。例如NP⊄BPP是排除该source promise确定性多项式判定算法的充分明确假设；不能仅以P≠NP替代随机归约所需条件。

## 线性degree的必要性（独立组合结论）

任何同样保留|A|=|B|=N/2、使用总投影的非空二部game，不要求regular或来自本算法，若满足

“每个cost≤gN的multilabeling覆盖严格少于ρ比例的M条边”，

则必有

\[
M>\frac{(g-1/2)N}{\rho},\qquad
\Delta_{\max}>\frac{2g-1}{\rho}.
\]

整数和ceil按严格覆盖率处理；这不是只在渐近意义上的界。它说明固定ρ时本页的O(g)阶不能改为o(g)。

## 物理scope、未完成义务及Status

若某真实UM编译对source的N顶点、M边能从任意所需弱阈值下的实际σ抽出lists，覆盖≥ρM条真实投影边，且

cost≤N+B(σ)/F，B(σ)≤cM，

那么g>1、F≥cΔ/[2(g−1)]保证cost≤gN，与上述NO矛盾。g≥2、Δ=O_ρ(g)时，足够大的**固定常数fee**即可，不再要求随g增长的log g fee；该常数不可未经证明设为1。

这里没有构造实际P、partial-trigger机制、投影接口或费用实现。新的source参数不补上物理编译缺口。证明完成、独立审查、实现及新颖性分别记录；本文件自身只是一份待独立攻击的精确候选陈述。

Related Files：同目录`partial_minrep_linear_degree_source_v2_proof_and_fee_obligation.md`；旧v1两文件仅作冻结研究历史，不作为本v2的额外前提。

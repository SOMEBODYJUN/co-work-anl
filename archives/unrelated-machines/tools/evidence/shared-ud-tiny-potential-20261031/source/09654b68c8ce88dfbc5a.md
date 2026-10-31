# 知情作者核查：shared-UD primal 势的 k² 扩域

2026-10-18，/root/sol_general_repair。root 已在消息中给出拟用代数，我另行重推并核其余全部 ν 依赖；不是新的 Exact-first 独立票，也不取代正进行 fresh 重构的 truehardness。所有旧冻结文件不改。

## 1. 实际读取及背景

已实际全文读取 `boss11_shared_ud_tiny_home_k2_refinement_exact_v3.md`：2124 bytes/15 lines，SHA256 `cc9d1037da7e86c74226968b890eaad6e646c4179bf16fe789a776818d2b6c39`。它的新域为 k=1 时ν≤1/4096、k≥2时ν≤1/(16384k²)，其他typed对象、算法合同、全部普通jobs与80fd Exact一致。

此前已完整实际读取80fd原Exact、409ce作者Proof §1–9及本人append-v1全部；本轮另用rg列出409ce与append-v2里全部ν/k⁴/H相关出现处逐一核。没有打开truehardness的新重构，也没有将root报告的NSW k⁴证明核查当成自己实际打开其记录。

## 2. 不依赖原k⁴上界的重推

固定当前profile的精确Φ-optimal点，λ_i=θ/k+2d_i，θ=1/32，d_i≤c=5/16，Dsum=Σd_i。stable weighted-matroid coupling只用实际w_j，不用任何tiny上界，给

    B_j=2(λ_i(j)/λ_min)²w_j².

由各outer Σw=1，有Σ_(j∈J_i)w_j²≤ν，因此仅用λ_min≥θ/k得

    Σ_j B_j
      ≤(2νk²/θ²)Σ_i λ_i²
      ≤2νk + (8νk/θ + 8cνk²/θ²)Dsum.

第二步展开λ²并用d_i²≤c d_i，不藏入任何H≥const·k⁵条件。k≥2代新ν，

    2νk≤1/(8192k)≤1/16384,
    8νk/θ+8cνk²/θ²≤1/(64k)+5/32≤21/128.

故仍有ΣB≤1/16384+(21/128)Dsum。benchmark与次模交换照旧给ΣΔ≥(65/128)Dsum−287/8192，在Dsum≥9/80时相减仍为ρ=293/81920。

k=1须保留实际λ_min=λ_1，不能拿floor粗界：ΣB≤2Σw²≤2ν≤1/2048；进展余量177/8192>ρ。新Exact确保持此单独ν≤1/4096分支。

## 3. 其余ν使用处与位复杂度

- target profile benchmark ε²Σλ只用actualV≥ε、homes独占及normalized sums，不用ν。
- weighted rank次模性、任意fractional optimum的stable L∞/L1、Φ一阶与deficit stability完全不用tiny bound。
- k≥2曲率是唯一需要把ν当k函数的地方，上节已完整重推。
- prefix-flow损失≤max a_iu≤ν。新域所有k统一仍有ν≤1/4096，故25/128−ν≥799/4096>19/100，q=1/10与全group回填不变。
- FW域diameter²≤k、每profileN=ceil(4k/ξ)、ξ=1/(2²⁰H²)、τ=1/(2048H)、共同分母及O(kH) moves仅用H≥1和每outer总权重一。没有使用H≥4096k⁵或另一方差lemma；换成新域允许的较小H不损坏任何一处。
- 叶无完整matching的actual FAIL、最终baseline比值32/17、全部零/inactive jobs和完整matrix counts均无ν依赖。

新界分母由输入整数k的平方构成，bit长度多项式，合法域检查仍精确有理比较。算法运行次数不按1/ν循环。原CDF/MW/CE v1有νk⁴方差付款，本核查**没有**把它升级成k²；这里只是新primal profile势的曲率核算。

## 4. 实际有限计算及结论

本轮实际用Fraction计算k=2,3,4,8,64的新constant、Dsum系数、prefix margin；分别确认constant≤1/16384、系数≤21/128、margin≥799/4096及原k⁴域包含。另直接算最坏常数相减，ρ确为293/81920。没有执行新域的完整算法或生成真实tiny输入，未新增软件认证。

旧域包含关系：k1相同，k2两上界均1/65536，k>2新旧允许ν之比为k²/4>1。其余假设不变，所以v3是真量词扩域，须单独审查；旧80fd/409ce及其独审身份保留，不改字节或倒改scope。

在已明确共享的原primal证明机制内，本知情作者核查未发现扩域fatal。root的新Exact-first审查尚须独立完成；不把本记录冒成fresh independent支持，一般UM目标继续OPEN。

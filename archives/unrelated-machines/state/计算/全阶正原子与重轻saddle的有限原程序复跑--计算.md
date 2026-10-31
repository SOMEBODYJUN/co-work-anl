---
id: "unrelated-machines/full-degree-atoms-and-heavy-light-saddle-finite-original-audit"
kind: "computation"
type_tag: "计算"
title: "全阶正原子与重轻saddle的有限原程序复跑"
status: "one-original-CLI-replayed-two-separate-finite-arithmetic-checks"
summary: "2586B同一原CLI分别核2job/2machine给定真分布的4原子/2正存活与四β的YES纯saddle二循环；不冒构造全阶矩表、验证全部q或实现LP/匹配搜索。"
source_refs:
  - "clean:077c6e9d54abd1b5e3be"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/full_degree_moment_and_saddle.py"
legacy_ids:
  - "UM-FULL-DEGREE-MOMENT-DECODING-v1"
  - "UM-HEAVY-LIGHT-SADDLE-CERTIFICATE-v1"
---

# 1. 同一CLI内的两个数学身份

原2586B程序SHA `8ce327de573870b4d4477e1c8dd283ef715ebfe7cc3799df6e84a245efdbfeea`完整读，本轮一次原CLI exit0，不import仓库其它数学实现。它仅用Fraction、product做下列两个有限算术检查。原stdout是Python dict/tuple的**repr，不是JSON**；[证据](../../tools/evidence/um-forest-and-frozen-macro-primary/README.md)原样保存，不把另行解析后的数据冒充原输出。

# 2. 给定真实分布的四个原子

两job、两machine，所有四finite端时间1，T1。product枚举(0,0),(0,1),(1,0),(1,1)，先按真实机器负载筛出恰(0,1),(1,0)，各赋权1/2，其余权0。程序直接核四权非负/总和1，每个原子每台机器的`(T−load_i(sigma))*weight>=0`，至少一正权且全机slack非负；实际两个正存活，stdout为`full_moment_atoms: (4,2)`。

它以合法assignment labels表示原子，one-hot在每状态成立；代码再次核sum(weights)=1，**没有显式生成次数2n+1矩表、所有Boolean理想乘子、M_n PSD或对所有q的localizer矩阵**。可行分布是在这个2×2例上先全枚举出来的，不是从一般未知P/T生成证书或筛出未知可行解。

一般充分桥的承重逻辑另为：同一个尊重Boolean/one-hot理想的L，最高次数2n+1、对deg q≤n有L(q²)≥0和逐机L((T−load_i)q²)≥0。完整原子m_σ次数n、幂等且Σm_σ=1，得w_σ=L(m_σ)≥0/总和1；代q=m_σ得(T−L_i(σ))w_σ≥0，故正权原子可行。这里保精确§1的**2n+1**，不拿当前正文首段的“2n”概述代替最高次数。n0/T0/零时间的一般边界由证明处理，本有限函数没有新跑这些额外参数。[全阶正式审查](../审查/全阶矩提取冻结审查增量--审查.md)已有完整一般桥，不重做done。

# 3. 四个β的自洽纯saddle二循环

对β∈[1/2,1)，δ=(1−β)/4、a=1−δ、b1=β+δ、b2=β+2δ、c=δ，T1。两machine/三job为A=(a,a)、B=(b1,b2)、light ℓ=(c,∞)。程序核A/B均heavy>β，c≤β。两种强制heavy placement H1:A→1/B→2，H2:A→2/B→1，light总给1；完整负载分别(1,b2)、(b2,a)，后者峰a<1，YES真实OPT=a。

自己的唯一最优残余对偶分别λ1=(1,0)、λ2=(0,1)，价矩阵行为H、列为λ：

`g=[[1,b2],[b2,a]]`。

每列另一个H严格更小，故逐次“取当前残余最优对偶、按该价格重选heavy匹配”在两H间回跳；这是这两个显式状态的精确不等式，不是程序实现一般LP或迭代搜索。

| β | δ | b2 | a |
|---|---|---|---|
| 1/2 | 1/8 | 3/4 | 7/8 |
| 3/4 | 1/16 | 7/8 | 15/16 |
| 9/10 | 1/40 | 19/20 | 39/40 |
| 99/100 | 1/400 | 199/200 | 399/400 |

一般saddle充分性是另一正面合同：admissible H的R(H)=max_λ g(H,λ)，若同一λ*为H最优对偶且H在g(·,λ*)全局最小，则R(H')≥g(H',λ*)≥g(H,λ*)=R(H)。给R(H)≤T且light≤βT，ST残余输出≤(1+β)T；源脚本没有执行该匹配验证、LP或ST步骤。可选heavy任务的轻基线μ_j须保留，不能只收费heavy部分。[既有对偶审查](../审查/重边匹配过滤与重轻对偶循环双源审查--审查.md)及完整原证明已比较。

# 4. 资源用途与限制

全阶桥的同一原子/全机局部化与saddle的同一H/λ自洽是不同量词，本程序同文件不使它们相互推出。全阶原子可指数多；纯saddle在YES例也可能不存在。两者均没有普通P到多项式证书生成器，不给一般UM次二算法或hardness。本轮只这1个CLI中的4个β和1个2×2例，知情读原证明/两冻结review，新增blind/外审0，不把数学审查票当软件执行。

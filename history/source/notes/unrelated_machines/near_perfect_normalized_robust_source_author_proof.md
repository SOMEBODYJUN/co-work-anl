# 近完美归一化 robust 菜单源的有理 LP 判别：证明

2026-10-18。对应同目录 `near_perfect_normalized_robust_gap_exact.md` 的 Exact，未并入 v2 文件。这里给本作者证明，供先据 Exact 独立重构后的读后攻击。

## 一般福利 LP 的承重性质

对Exact的LP，记最优值L。任意 actual allocation 为每组取attaining state，将其z置1、bundle内正incidence的x置1，其余0；资源不可复用保证LP容量。因此W*≤L。每组可随意选state z1、全部x0，LP始终可行；归一化及x≤z给L≤n。

给合法rational最优(z,x)，各组独立按z取state，再按conditional x/z对所选state正incidences取独立claims；z0时x0不作除法。固定资源u，其组g正claim概率为sum_s x_gsu，故跨组概率和≤1。每个资源交给成功claim中原系数最大组。单资源tail不等式及凹弦界给E welfare≥(1−1/e)L。全部原权重有限，逐组再逐claim以精确rational CDF条件期望固定所有决策，得到真正不交allocation、每组一个原state，W≥(1−1/e)L。由于e>8/3，对L>0有W>(5/8)L。候选数、tail水平数、概率乘积/加法及分母位长均按显式输入多项式。此段是DNS标准福利舍入的显式特化，具体独立证明已在本目录v2重构稿给出；不调用原NSW长证明或unit-FSLP。

## YES 与 NO 的纯计数

YES 有至少(1−eta)n个unit groups，其余非负，所以W*≥(1−eta)n；由W*≤L，LP判YES。

对任意NO_≥ allocation，令h=#{r_g≥delta}<gamma_hi*n。高组质量≤1，其余<delta，因此

W≤h+(n−h)delta < [gamma_hi+(1−gamma_hi)delta]n=:v_NO*n。

第二个严格号只用h<gamma_hi*n与delta<1，包含所有非整阈值。NO_>同理，高组>delta，剩余≤delta，但同一个第二严格号仍成立，故也有W<v_NO*n。

若NO且LP L≥(1−eta)n，则L>0（eta<1、n≥1）；福利舍入给一个真实allocation，满足

W>(5/8)L≥(5/8)(1−eta)n≥v_NO*n，

与上述所有allocation的上界矛盾。因此NO必L<(1−eta)n，判别闭合，等号(E)安全。算法只求显式rational LP并比目标，不需要实际运行福利finder，后者只用于证明NO下LP目标受限。

## 统一子域与复杂度

gamma_hi≤delta且delta<1时，v_NO=delta+(1−delta)gamma_hi≤2delta−delta²。函数2delta−delta²在[0,1]单调增，delta≤3/8给v_NO≤39/64。eta≤1/40给(5/8)(1−eta)≥(5/8)(39/40)=39/64。因此(E)成立，包括所有等号。

LP变量数S+I_+，约束数n+I_++m及非负性，系数全为0/1或输入p；标准确定性rational LP给精确L和多项式位长最优基本解。比较目标与(1−eta)n只有有理运算，参数位长直接计入，无按1/eta、1/delta、1/gamma枚举。两类promise不相交：YES本身的福利至少(1−eta)n，而NO所有福利<v_NO*n≤(5/8)(1−eta)n，所以也可从原定义直接验证互斥。

若给定相应Karp reduction，组合此decider得到多项式解NP完全语言，故P=NP；随机归约按其成功保证另述。全文未断言这样的hard reduction已存在，亦未推出任何一般UM反面结论。

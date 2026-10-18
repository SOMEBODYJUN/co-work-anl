# 共享外端 small-query / return-pool 接口：冻结 Exact v1

提出者：rank_deficiency_fee，2026-10-18。仅冻结完整对象、实际模式与精确结论，供新的Exact-first审查；不含作者Proof或证明策略。只写clone外scratch。单位pool/共享outside均为标准构件，不主张新的matching理论或全球原创性。

## 1. 完整普通UM矩阵

整数k≥2。给显式正二进制有理数a₁,…,a_k，满足Σ_i a_i≤1。内部机器为一台H及P₁,…,P_(k−1)；外部机器为E₁,…,E_k。所有2k台机器互不相同。

全部原任务恰为2k件不同jobs q₁,…,q_k,b₁,…,b_k；辅助集A=∅，没有预载或其它任务。完整有限端如下：

| 原job | 内部finite端 | 外部finite端 |
| --- | --- | --- |
| q_i | H，时间a_i | E_i，时间1 |
| b_i | 每个P_r（1≤r≤k−1），时间均1 | E_i，时间1 |

其余全部∞。每个job只能整件、恰一次在上述原有限端执行。E_i是q_i与b_i真实共享的一台原机器，外部负载完全计入makespan，没有outside-private替代。内部H的finite时间可随原job不同，全部为正；允许取a_i=1/k，使所有k件q真实共居H时总负载1。

## 2. 任意实际pattern的精确定义

对每一完整实际调度σ，定义

    S(σ)={i:q_i实际在H执行}，
    T(σ)={i:b_i实际在E_i执行}。

给定任意S,T⊆[k]，pattern(S,T)要求：

* i∈S的q_i在H，i∉S的q_i在其E_i；
* i∈T的b_i在其E_i，i∉T的b_i可自由选择任一P_r。

定义OPT(S,T)为这个pattern中、覆盖全部2k件原jobs的完整实际最小makespan。P上的b分配属于优化变量，**不**先固定为matching，也不把每P容量1当免费硬约束。任何S,T都有完整有限端调度，因k−1≥1且普通UM允许共居；未声称它都在strict阈值可行。

## 3. 精确主张与全部partial模式

对每个上述k与a输入，以及每一对任意子集S,T，精确有

    OPT(S,T)=1，若 ∅≠T⊆S；
    OPT(S,T)=2，其余全部情形。

所以对每个1≤B<2，所有实际峰≤B的完整调度都严格满足

    ∅≠T(σ)⊆S(σ)，

且这些weak调度本身已经峰≤1。反之，每对满足该关系的S,T均有可确定性构造的完整原jobs峰1调度。不存在遗漏的多query、多return、空query、空return或非对齐partial模式。

此合同保证至少一枚具体原b返回outside；每个返回的b_i都保证其同索引原q_i已经在内部H。**它不保证S=T、不保证恰一query或恰一return，也不保证每个进入H的q都返回b。**

### 原singleton接口的校准

* aligned_i：S=T={i}，完整实际OPT=1；
* inactive（全部q在outside、全部b在pool）：S=T=∅，完整实际OPT=2；
* cross(j,i)、i≠j：S={j}、T={i}，完整实际OPT=2。

因此任意B<2均排除全部inactive与singleton cross，而允许所有k个strict aligned。对任意有理δ∈(0,1)，取B=2−δ，无需改变矩阵或按δ倒数复制任何job。

## 4. Actual构造与位复杂度合同

给k、全部有理a_i、以及满足∅≠T⊆S的显式S,T，可确定性总位多项式输出每件原job的具体原机器，全部实际负载≤1；不输入最优见证、源assignment或未知formula解。对不满足关系的pattern，亦可在峰2输出一份全部原job调度。给任何实际σ，可按原job目的地算S,T并回算所有2k台机器的有理负载。

规模为2k原jobs、2k原machines、k²+2k条finite资格；dense矩阵4k²项。所有有限时间只为a_i或1，资格及a_i均显式给出。构造、模式解码、全原jobs负载回算按输入总编码位长多项式，不枚举2^(2k)个patterns，不按时间分母、k的隐式指数或δ数值展开。

## 5. 正确范围与source义务

这是一个实际共同负载接口：同一H可以真实共居多件small queries，全部returns在真实共享E_i执行。它不属于“每台内部弱阈值下至多一job”的4×4环合同，亦不能用private outside封装替换其E_i。它仍不反驳只保证内部可替换性的machine-uniform localA Claim。

此孤立完整模块的普通OPT恒1，例如S=T=[k]的pattern属于strict可行范围。故它本身没有任何source NO，不能仅凭near2的模式排除声称困难性。得到多query的身份containment，并没有强制同一源变量的多个occurrences共享truth/label。

任何把E_i识别到已有变量环、给q_i额外outside端、让多个i共享外机、或增添其它实际jobs的编译，都会改变上面完整矩阵，必须重新证明全部原jobs的YES以及所有低负载调度的NO decoder。特别不能给q_i第二个外部端后继续免费使用T⊆S。本文件不给任意外接、费用共享、变量一致性或完整formula可调度性合同。

这里只冻结小任务query/return可共居的局部正面关系，技术扣除为标准unit池与共享端；未提供NP-hard源、一般UM算法、near2 hardness、软件或有限枚举证据。主目标仍OPEN。

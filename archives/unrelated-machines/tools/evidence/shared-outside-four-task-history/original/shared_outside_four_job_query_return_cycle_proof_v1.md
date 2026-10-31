# 共享外端四任务 query/return 环：作者 Proof v1

对应先冻Exact：`shared_outside_four_job_query_return_cycle_exact_v1.md`，SHA256 `c2f73db04495292714a6a083029b707f3c4c246647e4975f1f58bfdcaf15fe19`。

作者：rank_deficiency_fee，2026-10-18。构造先以完整矩阵/Claim发root，root仅据消息独立核查同一matching结构；此Proof另冻先仅交root。不直接发给尚未完成Exact-first的reviewer。只写clone外scratch。

## 1. 完整对象与strict见证

0<ε<1有理。内部机器H,I，真实outside机器E₁,E₂。四件原jobs：q₁只有H:1/E₁:1，q₂只有H:1/E₂:1，b₁只有I:1/E₁:1，b₂只有I:(1−ε)/E₂:1；未述端∞，A空，无其它任务、机器或预载。

Aligned₁的完整assignment为q₁H、b₂I、q₂E₂、b₁E₁，逐机负载(H,I,E₁,E₂)=(1,1−ε,1,1)。Aligned₂为q₂H、b₁I、q₁E₁、b₂E₂，四机负载均1。每件原job恰一次、资格合法，两份实际峰均1。q₁的每个有限端时间都1，故任何完整调度峰≥1，原P的OPT恰1。

## 2. 任意完整低负载调度的全模式解码

取任意完整实际σ，假设C(σ)<2−ε。每台原机至多执行一件job：

* H的唯二eligible jobs是q₁,q₂，两件合计2>C；
* I的唯二eligible jobs是b₁,b₂，两件合计2−ε>C；
* E₁的唯二eligible jobs是q₁,b₁，两件合计2>C；
* E₂的唯二eligible jobs是q₂,b₂，两件合计2>C。

全部四件原jobs必须恰一次、原机也恰四台，所以每台恰有一件，构成原资格图的perfect matching。若H执行q₁，则q₂不能H，只能E₂；b₂不能已占E₂，只能I；b₁只能E₁，恰aligned₁。若H执行q₂，对称推出aligned₂。H没有其它eligible jobs，已穷尽全部完整调度。

此是四机资格环的结构证明，不以“已枚举16份assignment”作一般根据。它同时排除所有其它内部子集，包括零query、两个queries、多return或其它partial模式。读出q₁还是q₂在H即可确定具体原身份的唯一索引。算法只检查给定实际assignment，不输入或寻找隐藏optimum witness。

## 3. 列出的bad模式精确最优值

每个原job恰一个内部、一个外部资格，所以一旦指定内部任务集合，四件job的目的地全部唯一。

Inactive内部{b₁,b₂}，故I上负载2−ε；q₁E₁、q₂E₂各1，H空，峰精确2−ε。

Cross(2,1)内部{q₂,b₂}，故q₂H:1、b₂I:1−ε，而q₁E₁与b₁E₁真实合计2，E₂空，峰2。Cross(1,2)对称在E₂上两unit，峰2。这些都是全原jobs的实际峰，没有丢任何外部job。

全模式分类说明任何非aligned调度峰≥2−ε；inactive确实达到该边界。结论只取C<2−ε或B<2−ε，不把临界等号偷排除。对1≤B<2−ε，全部≤B调度恰两strict见证。

## 4. Near2参数、位长与scope

给δ∈(0,1)有理，取ε=δ/3、B=2−δ。有0<ε<1、B>1且B<2−ε，所以strict aligned峰1、所有非aligned峰>B。四机四job、八finite条目固定，有理1−ε的二进制位长为输入δ的位长O(1)倍，生成与核负载不按δ倒数复制。

该正接口的阻挡同时计入H/I/E₁/E₂；不能将E_i当private测试机而忽略共享。它不反驳只保证内部交换的localA Claim。事实上单看内部，错配{q₂,b₂}和{q₁,b₁}都在峰≤1可行；真正完整模式的外部成本不能免费补齐。

异权1−ε不是这里的机制核心，ε=0时同样是标准unit交替环。所有低负载原机至多一件，且两strict见证每机都满一件；身份状态的machine-presence相同。故本例没有摆脱matching、没有提供可供额外medium/small clause任务读取的空间或cross-role机制，也没有证明把外部机识别到已有变量环仍保YES。

任意额外clause任务、角色变换、模块级联或source编译都需重新给全实际P、全部原jobs的YES与完整NO解码；此Proof不为它们提供免费合同。只有一个标准matching边界对照，没有NP-hard源、near2困难性、新算法或新matching理论结论。

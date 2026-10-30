# Cartesian coordinate-oblivious quota：canonical §6–7 实际范围读后

审查者：general_query_response_review。2026-10-18。

## 实际顺序与正式认证范围

先仅据消息内精确陈述冻结独立Exact-only构证；之后实际全文读作者Exact与Proof并另冻read-after；本轮才实际全文读取canonical候选。未读取其它agent输出、审计代码或冻结软件输出，未改repo/Work/Git及既有源/审查文件。

Canonical：
/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/cartesian_menu_recoupling_and_coordinate_consistency.md

本次whole SHA-256：
50d41b240871e19d82c6cdb82165f13cdfb9087097e7c0162fef3cb45075592a。

**正式认证仅§6–7，与UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1的冻结Exact/Proof对应。明确判断：通过，无fatal，亦未发现需改正文的非fatal数学或复杂度问题。**

其余全文为读取context，不冒称认证整页、ordinary实际矩阵的有限软件审计或§8所有运行计数。本次逻辑后果需要的bare值V_t=1−2^(−t)已在我的先行独立记录§6单独重证；不是以代码或有限实验替代该数学前提。没有读取或认证q-ary新对象。

## §6逐项核验

1. 正确保留t≥1、D=2^t、groups/resources/state完整有限域。每state恰D个资源、每项1/D；函数族固定但任意，限制ell_i(g)=f_i(g_i)，禁止依g其它坐标。进一步优化函数仍同值，因为每一组固定函数已单独证明同一最优值。语义限制与ordinary UM物理约束明确区分。
2. 每坐标所选两条线各2项、恰交一项，另各一独占项，共3项。全体groups遍历二进制bits，使支持union恰为三符号完整积，大小3^t；所有固定函数族均同一incidence结构。与独立构证的全局资源平移同构一致。
3. 任意partial subsets允许非Cartesian形状和不用资源。若最小基数s，则D个groups的全局不交子集至少占Ds项，故Ds≤3^t；s为整数，给floor上界，不把资源切分。公式(3)的floor精确。
4. 一个resource有h个common坐标时恰兼容2^h个groups；邻边2^(−h)使每列总量1，每行总量(3/2)^t。对任意group子集A的全部行求和，由N(A)的容量得到式(4)，没有只验证总union或特殊形状A。
5. 每group拆k个同邻接槽后，任意槽子集X触及的groups为A，其邻集仍N(A)，且|X|≤k|A|≤|N(A)|。普通Hall给覆盖全部槽的整数matching，输出每group恰k个真实资源，跨groups不交。因此fractional证书被正确转成不可分bundle，而非直接称分数行量为实际quota。
6. k=floor(3^t/2^t)≤D，槽数Dk≤D²、边数DkD≤D³，与原全部显式菜单incidences D³的长度计量相容。确定性增广路、整数除法和O(t)位资源标签/权均对显式总编码长度位多项式；没有poly(t)或succinct输入声明，没有浮点取整/按分母数值复制。我的容量网络更省并不改变作者算法合同。
7. t1两组共享一资源、各独占一资源，k1、值1/2。空partial subset仍允许但不妨碍上界/正quota构造。全部finite objects与非空group量词一致。

## §7对照与统一常数修复的逻辑

公式(3)独立于bare主Claim的证明；只有对照和修复限制共同依赖两个精确值。这个依赖分层在正文中已经正确明示。

先行独立bare证明要点：任何补组g,h=g+1的任意两state必有唯一共同资源，所以共同整数quota至多D−1。循环选ell_i(g)=g_(i+1)，令各group取所有a≠1向量对应的资源；碰撞差分满足delta_(i+1)=a_i delta_i，因某a_i=0，沿环得delta=0。故这些D−1项bundles全局不交，bare值精确为(D−1)/D，t1也适用。该数学证据无需代码。

受限值与(3/4)^t的误差小于2^(−t)，所以趋0；bare值却趋1。若有适用于本同一family、所有t及任意高值bare allocation的修复合同，输出必须是相同groups/resources/state family上的coordinate-oblivious allocation，且保证输出值至少c倍输入值，其中c>0与t无关，则把合同应用于上述bare达界witness，必有

c (D−1)/D ≤ floor((3/2)^t)/D，

即c≤floor((3/2)^t)/(D−1)，右侧趋0，矛盾。甚至无须算法性，只要求这种保证的输出存在就被排除。Bare witness对任意固定小于1的“高值”阈值最终都满足，所以不会因高值一词逃开反例。

该结论只排除正文明确的同族/受限输出/统一正乘法保值合同；允许改变状态、资源、任务的新归约，或依t衰减的保值系数，均不受此逻辑排除。正文没有声称更大范围，也没有把语义限制免费放入普通UM source decoder、构造物理一致性gadget或提供near2 NO源。对另有占位胶合界的引用只是范围提醒，不被用为(3)或上述比值矛盾的前提。

## 冻结输入与边界

- 作者Exact：b577a7725a4a3e02c55f3167ef34e0e9f1b335b01573f16ef5e8d32bdb5544d3。
- 作者Proof：b02ceaef1b06f6a0f10c9b06a6b7cf9dff189968049a785fc42a7c49efc88049。
- Exact-only独立记录：ea7403228d00a092ae39cc150208929325ebfb819f6106b0e762db007825ae5a。
- 作者实际读后：7b416b1c2d811f3918fd00620c4832360ea559aa699b47ab467582b5744f0e11。
- Canonical whole：50d41b240871e19d82c6cdb82165f13cdfb9087097e7c0162fef3cb45075592a。

本文没有软件运行或代码认证。仅§6–7实际读后通过，无standing fatal；其它章节/有限审计、全球新颖性及外审不纳本次认证。

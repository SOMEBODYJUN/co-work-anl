# Cartesian 逐坐标受限 quota v1：作者 Exact / Proof 实际 read-after

审查者：general_query_response_review。2026-10-18。

先仅据root消息内精确新陈述独立构证并冻结Exact-only记录；root实际读取该记录后，本轮才实际全文读取作者Exact文件及作者Proof。未读取其它agent输出、canonical或任何q-ary新对象；本文件不改旧独立字节，未改repo/Work/Git。

冻结输入：
- 作者Exact：b577a7725a4a3e02c55f3167ef34e0e9f1b335b01573f16ef5e8d32bdb5544d3。
- 作者Proof：b02ceaef1b06f6a0f10c9b06a6b7cf9dff189968049a785fc42a7c49efc88049。
- 先行Exact-only独立记录：ea7403228d00a092ae39cc150208929325ebfb819f6106b0e762db007825ae5a。

**明确结论：作者Exact与先行消息合同一致，作者Proof有效，无fatal。所有固定函数族的最优quota相同，任意partial bundles上界与全部Hall子集下界、整数floor、t1、显式总位多项式计量均成立。**

## 实际文本核对

1. 作者Exact严格增加状态选择语义ell_i(g)=f_i(g_i)，每个f_i不能依g的其它坐标。它并未声称存在ordinary UM物理约束强迫该语义。每个state仍恰D项，各权1/D；子集任意且全局不交，允许不用资源。与先行冻结的数学对象无差异。
2. 每坐标两真实支持线各2项、交点唯一、各有一独占项。把group的各bit自由遍历，支持并集确为三符号完整笛卡尔积，大小3^t，非仅一个并集上界。任意(f_i)都具有同一incidence pattern，与独立记录的全局资源平移同构一致。
3. 任意实际partial allocation的最小bundle基数为整数k；Dk≤3^t迫k≤floor((3/2)^t)。没有将权1/D的资源可分化，也没有遗漏未用资源或把所有bundle要求为full state。
4. 每个有h个common坐标的resource恰邻接2^h个groups，均分边量2^(−h)使列容量恰1；每行边量和(1+1/2)^t。对任意group子集A，该行总量只来自N(A)，其供给≤|N(A)|，因此全部A满足k-Hall。这个推理完整覆盖任意A，不依压缩或特殊子立方体形状。
5. k个同邻接槽/原group的matching充分性正确：任意槽子集X触及原groups A，其邻集恰N(A)，且|X|≤k|A|≤|N(A)|，普通Hall即覆盖全部槽。所得每group恰k个真实不可分resources，且全局不交。Fractional权仅是Hall证书，不是最终allocation。
6. k≤D，故槽数Dk≤D²，边数DkD≤D³；作者原全部显式menus的incidence数D·D·D=D³。确定性增广matching按展开输入规模位多项式，时间权1/D的位长O(t)，算法不需数值展开分数分母。作者Exact已明确按全部显式groups/resources/menus长度计，不称poly(t)，与我先行冻结的succinct-input范围提醒完全相容。我独立的容量流只需selected-state边D²，属于更省的实现而非不同数学合同。
7. t1时k=1、质量1/2。即使最优函数可任意先选，每个固定函数族的完整结论已成立，因此进一步优化函数仍同值。floor不能被连续值(3/4)^t代替。
8. Exact中的无约束对照V_t=1−2^(−t)未在这份短作者Proof中重证；该对照已在我的先行独立记录§6单独完整证明：任意complement pair的状态必交给上界，循环选择ell_i(g)=g_(i+1)、每group保留所有a≠1^t给D−1项disjoint bundles。因而本轮可确认对照为真，不把它视为受限Hall证明的必要前提，也不因此扩展ordinary UM的结论。
9. 末尾约(3/4)^t的渐近表述正确：精确值与(3/4)^t相差小于2^(−t)，相对误差小于(2/3)^t。它不供应ordinary makespan NO、物理一致性gadget、hardness源或排除其它归约。
10. 未发现需更正的数学或复杂度措辞；未作软件matching实现/运行认证。作者文件中关于reviewer先读顺序的概括不替代本记录实际顺序：我先读的是消息内Exact陈述，而非提前读取作者Exact文件，两个合同在本次实际核对中相同。

**冻结判断：作者Exact / Proof通过，无fatal；等待canonical后再按指定章节另冻最终读后，不扩展到q-ary新对象。**

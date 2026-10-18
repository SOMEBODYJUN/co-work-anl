# 三组菜单零权三坐标嵌入：canonical 最终全文 read-after

审查者：general_query_response_review。2026-10-18。

对象：`co-work-anl-boss11/research/current/unrelated_machines/degree_three_weighted_menu_cube_embedding.md`。

最终审查SHA-256：`def740ba49bb83b495f034ecd80efdb88d7a291fa6c048a6209db19dd5d6869e`。

先后次序：只据Exact独立重构并冻结；root读取该记录后，才首次读作者Proof，另冻read-after；本轮再实际通读整个canonical，针对一处selector措辞反馈后又实际通读修后全文。旧Exact、Proof及两份审查原字节保持不改，审查者未写repo/Work/Git。

**最终结论：canonical整体有效，无standing fatal；新域、完整原job映射、实际OPT及interaction结论与冻结Exact/Proof一致。**

## 全文组合核对

1. 源仍是完整显式flat weighted-menu ordinary UM：非空groups、非空indexed menus、每state私有机、每resource单位外端、selector自组全菜单、W≤1、无其它jobs/约束。未加入K、q_g、M上界，也未排除zero/empty/unused对象。
2. Target固定d=Q=3、每var完整27格、每state每var完整9格；每variable至多三组、group incidence indices互异。允许零cell权及相同labelvector的不同state cost tables，私有state和jobs保原身份。未偷偷换成label唯一决定cost、all-positive cell或succinct几何模型。
3. Active格z*=(1,2,3)位于每个label=index的slice。源u的incident groups使用互异indices，所有原incidences都具有其active格，且不同(g,s,u)对应不同target jobs；原p=0 incidence仍是原job，不因与aux同为零而删掉。
4. 原selector保留全部K_g个private资格；每原incidence恰保原private和active-resource两个有限端。其它∞资格没有获得新finite端。源原state/private/selector/resource inventory保留，unused R_u也保其active像。
5. 扩展针对任意完整source schedule：所有原jobs保原端，所有extra jobs在其自己的state机耗时0，含selected及全部unselected states；原load逐机相同，新资源idle，峰完全相同。
6. 投影针对任意完整target schedule：可有aux jobs导出，亦可峰≥2；依identity删aux而不是按权零删除，再逆映全部原jobs。原job没有其它格资格，故合法完整，load只减。双向直接给实际OPT相等及所有actual makespan阈值转移，不限最优模式或全export。
7. 对源共享u的groups，target共享active格；源无共同u的groups变量tags不交，dummy只属本组。故完整union interaction graph及M精确相同，包含零权membership；每resource group-degree≤3。固定Q=d=3没有给M上界。
8. 正support与full union清楚区分。Unit selector强迫选态的p>0 jobs export，p0可留根；跨组正supports不交既必要亦充分，未选state jobs全部留private≤1。Target正support只是原positive incidences的active像，额外零格几何交集不构成一致性要求。
9. q_g=0使用独占dummy，U甚至可空；unused原u仍列27格。资源机数27(|U|+e)、private数S、selector数|G|、incidence数9ΣK_g max(1,q_g)正确。q'_g≤max(1,|U|)、e≤|G|≤S给poly显式输出，dense乘积也poly；没有3^{q_g}展开或按有理数值复制。
10. 有限原times保持、其它新增times只有0/1，所有tags/labels/job-map编码poly；构造、任意schedule扩展和投影均扫描显式对象，未调用最优见证或未知source decoder。
11. §5的有限交互正定理本轮不重新认证。已核本target恰符合所引用的flat weighted-menu对象、resource capΔ=3、同一M及W≤1；因此给定该既有定理后，2−1/(M+5)参数代入无新增条件障碍。没有把该外部定理、general allocation hardness或SC promise冒当本embedding的源gap。
12. 软件/有限实验、全局新颖性、一般UM算法或hardness均未被新认定。既有uniform cube比较仅说明域不同，不参与embedding证明。Pending review链接由root另登记，本审查不以其暂未落地判数学真伪。

## 本轮措辞精化

首次canonical Exact段写“每个原job身份及其两个有限端时间”，对selector不够准确：selector有K_g个finite选项，K_g未必2。构造和证明本来一直保全部selector资格，因此不是实质对象错误。root仅将短语改为：

“每个原job身份及其全部原有限端时间（incidence jobs恰有两端）”。

最终全文已实际重新读取，旧不精确短语不存在；修后语句与source/target定义一致，冻结source Exact/Proof未被改写。公式及全文字节扫描除正常LF外无ASCII控制字节。

**最终批准范围：上述hash的canonical exact embedding及其参数保持，通过；外部交互算法本身、源hardness及新颖性不在本轮认证范围。**

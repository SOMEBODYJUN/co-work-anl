# q-ary affine 菜单 fiber 缺项 v2：canonical 指定范围实际读后

审查者：general_query_response_review。2026-10-18。

## 实际读取、冻结顺序与认证范围

先分别仅读v1/v2 Exact独立重构并冻结，之后实际全文读两版作者Proof并另冻合并read-after；本轮再实际全文读取canonical：

/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/cartesian_menu_block_coherence_rank_and_deficit.md

本次whole SHA-256：
b859a872faf453265f3a4d0b99439df104ae7fac4af1dca92ca969e39f6e8b30。

**正式认证：§7–8、共定义§1中本near-full-deficit对象及其完整actual还原、§9中对应本Claim的显式复杂度/证据/范围。数学通过，无fatal。另有一处不影响本Claim的非fatal量词措辞建议，见末节。**

§2–6的任意affine、coordinatewise、binary block及rank公式仅实际读取context，不纳本次认证；§9关于这些其它Claim的特定计算亦不纳。没有读取或认证代码、软件运行、其它审查者有限计算或全球新颖性。本记录仅scratch新增，未改repo/Work/Git及任何旧冻结文件。

## 共定义与actual完整性

1. §1与两版Exact保持同一对象：q为prime power、给定有限域表示、t≥1、N=q^t，N个groups、每group全部N个indexed states、N²资源。每state恰N个distinct incidences，private有理时间1/N、resource时间1、selector1，所有其它资格∞。所有未选states任务仍实际存在，未将有限域值当作有理负载。
2. 给定selected-state disjoint bundles，selector停所选private，只有对应B_g incidences外送，其余全部原jobs停车；selected负载2−|B_g|/N、未选private1、资源≤1。任意actual C<2反向按selector实际目的地取真实exports，unit资源容量使其不交；selected private负载仍是该精确式。未选state额外exports只占更多资源。完整normalized identity因此在本Claim非空选择域（全部函数）中成立，包含OPT2端点，非仅selected subset被执行。

## §7–8数学实际核对

3. 全局ell(g)保持任意nonlinear，B_g任意partial且不需product形状。F必须是同一真实resource x的非空fiber子family；该concurrency在Exact Statement和Scope均明列。空投影大小1正确，x不必被实际领取。
4. 共同x=(a0,b0)使F上ell(g)=b0+g*a0。按J={i:a_i≠a0_i}分层，固定非零差值在J中可逆，b输出恰编码π_JF，所以每层(q−1)^|J|·|π_JF|，层间a身份不同，union恒等式准确。没有套用于任意非concurrent family。
5. F内bundles总量≥k(N−d)，且其不交union包含于完整state union，故遗漏预算kd≥kN−union；可有资源不用、外部group另占资源。以projection≤min{k,q^j}给h(k)≤kd，空投影给k−1。粗projection界未声称每k可达到或所有投影能同时饱和。
6. h(1)=0保证K有定义；各实际非空fiber h(k_x)≤k_xd，故k_x≤K(d)。h(k)/k=1−1/k加正系数max(1−q^j/k,0)，逐项不减；合法k为初段，可整数比较二分。K随d不减，故dK(d)对非负d也不减。全文正确限定为必要条件，不当作可行性充分判据、最优分配或selector搜索算法。
7. 每group有(q−1)^t个全坐标不同的其它groups，其选中states无论标签如何都交唯一资源。按全部pairs计得sum binom(k_x,2)至少N(q−1)^t/2，其它pairs的可能多重交点只增加左侧。每资源最多保留一份，故sum(k_x−1)_+≤总遗漏≤Nd；fiber上界给式(7)。第一个比较正确使用≥，未冒用v1严格近满时才有的等号。
8. 旧严格引理仍单列2d<q：共享r≥1坐标pair的非空完整交有q^r≥q项，两端遗漏≤2d无法覆盖，迫同fiber每坐标互异、k_x≤q，继而得d≥(q−1)^t/q。分支整数ceil给式(8)的min；没有将阈值等号纳入，也没有说式(7)逐参数支配所有旧界。
9. q3,t2由式(8)得d*≥2；cyclic只取a_1a_2≠1的7项/组，差分递推排碰撞，达界。完整job还原负载11/9，任意actual反向也被覆盖。此witness已在我先行独证，不需把其它affine Claim当成新证明前提。
10. q3,t3时h(3)=2≤6而h(4)=9>8，结合h/k单调有K(2)=3；d≤2时dK(d)≤6<8，排除全部nonlinear的此种allocation。Cyclic good-a有23个且映射可逆；bad-a恰4个、每个kernel大小3，因此bad图左度4右度3，Hall给每组1个bad资源，加good部分共24项。该固定witness只用于上界，不证明一般q,t中cyclic全域最优。
11. q3,t3完整actual调度执行全部N³ incidences及N selectors：selected state24外送、3件留private，所有未选states各private总量1；峰10/9。任意actual C<10/9由selected private整数未送件数≤2提取d2 allocation，已被式(7)排除。因此式(9)的d*=3、V*=8/9、OPT=10/9全域精确，且没有省略未选任务或假定其不exports。
12. 旧v1“q3,t3尚未闭合”的记录保持原时点，canonical明确v2用新证明推进，不倒改旧字节。本轮未改首写或final独立记录、任一Exact/Proof。

## §9对应复杂度及范围

N³ incidences、N selectors、两类各N²机器、sparse有限项2N³+N²、dense项2N²(N³+N)及O(t log q)位labels/有理权均正确。H用t项整数表达式，结果≤N²，求K的二分及整数比较对log N=t log q和展开编码长度多项式；不是仅log t+log q的succinct标量算法声明。矩阵/完整witness/明确matching按全部显式输入计量，没有poly(t,log q)输出指数对象声称。

本Claim没有软件认证或新增优化实验；reviewer辅助checks不当作一般推理前提。一般q,t全nonlinear最优、physical fiber一致性及normalized tiny-gap复杂性源仍未解决；三个Claim合页不因此变成一般UM分解或主目标反证。

## 一处非fatal措辞精度

§1写“对任意选择域L，最大值V_L……”。若要把这一句另行当作对任意集合L的全量词命题，应明确“任意非空选择域L”；L为空时最大值/受限最优未定义。当前near-full-deficit的L是全部函数，必非空，且页面其它实际使用的cyclic/affine/coordinatewise/block域也非空。因此这不影响本次正式认证的对象、(6)–(9)或actual结论；建议加“非空”二字使共用表述完全精确。

**最终范围判断：指定near-full-deficit v2数学通过，无fatal；仅上述共定义量词有非fatal精度建议。其余affine/block/rank及软件不认证。**

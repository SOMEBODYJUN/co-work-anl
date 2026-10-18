# q-ary affine 菜单缺项 v1/v2：作者 Proof 实际 read-after

审查者：general_query_response_review。2026-10-18。

## 实际顺序及范围

先只据v1 Exact独立构证并冻结首写/final记录；其后只据新增v2 Exact再次独立构证并冻结首写/final记录。Root实际读两版独立final后，本轮才首次实际全文读两版作者Proof。未读其它agent输出、新canonical或相关审计代码；本记录仅scratch新增，不改repo/Work/Git及任何既存冻结字节。

本轮实际读取：
- qary_affine_menu_near_full_deficit_proof_v1.md，SHA 7d1587e9e5d2edb0790a90fd63f288f86e8b5d5f6bf604287242454bc969b911。
- qary_affine_menu_near_full_deficit_proof_v2.md，SHA c319bb93dc40298dd3cedf232c5c3d4cf37e71a40c70d726f0b6dc39c4d95c1a。

**明确结论：两版作者Proof在各自冻结Exact域内均有效，无fatal；与两次独立构证一致。v1的q3,t3未闭合属于原时点正确范围，保原字节；v2新增fiber合同将该端点闭合，不应倒改v1。**

## v1实际核对

1. 任意全局nonlinear标签下，不同groups若有z个相同坐标，其state交为空或恰q^z；在不同斜率坐标有限域方程唯一解，在相同斜率坐标须标签相同才有q种选择。没有偷加affine或coordinatewise选态前提。
2. 每group删≤D且bundles不交，完整state交集必须由两端遗漏覆盖。严格2D<q排除z≥1的非空交，从而同fiber groups每坐标两两不同，fiber大小≤q。等号未被纳入。
3. 每group有(q−1)^t个全坐标不同的其它groups，它们各必交唯一资源；其余pair已被排除。因此pair总计是等号。每重数k_x资源至少删k_x−1份，k_x≤q给所需D≥(q−1)^t/q。Partial形状任意且资源可不使用，证明不受影响。
4. D*为整数，若小于ceil(q/2)确实满足2D*<q，再得另一个ceil下界；排除同时小于两者正好给min，而非max。有限显式对象使最优达到。
5. C<2时按actual selector所在state取真实exports，资源unit使其不交，selected private恰2−|B_g|/N。反向保全部jobs：未选states各private总量1、selected仅导出所选bundle。故normalized恒等式及actual下界包含未选任务和OPT2端点。
6. q3,t2用cyclic state、保留a_1a_2≠1的7项达到D2。其碰撞差分直接强迫g=h；本审查已在先行独立记录自证这一步，不需导入另一个recoupling作者Proof作前提。完整actual负载11/9成立。
7. v1结尾明确不把近满条件外的fiber界继续套用；q3,t3仅知D≥2、cyclic可D3，是该版本当时精确范围。新v2提供额外论证，不构成v1原Proof错误。

## v2实际核对

1. 对任意非空F⊆F_x，concurrency给ell(g)=b0+g*a0；写a=a0+delta，资源输出为b0−g*delta。按delta的非零坐标J分块，乘非零delta逐坐标可逆，实际distinct输出恰|π_JF|，每J有(q−1)^|J|个delta，故union恒等式准确，含空J唯一资源。
2. Restrict到F的实际bundles仍不交，总量≥k(N−D)，即遗漏预算。外部groups占位只会收紧，允许资源未分配或B_g非product形状。Concurrency是明列前提，作者未把恒等式套到任意family。
3. Projection大小≤min{k,q^j}只给H下界；空投影精确为1。对完整非空fiber得到H(k_x)≤k_xD，k1合法保证K非空。作者未声称各投影同时饱和、H tight或K可实现。
4. 一般全局pair计数只取全坐标不同pairs给下界；其它相交pair会额外增加左侧。因此从v1的等号改成≥是必要且正确的。用fiber大小≤K、总遗漏≤ND给D K(D)≥(q−1)^t，不再需要2D<q。
5. H(k)/k逐项不减，合法k集合为初段，可用整数比较二分；K随D不减也从定义立即成立。K及D K(D)单调均未被误用为充分性。整数大小q^(O(t))、H求t项，符合按log N=t log q及展开instance计量，不作仅log t+log q的succinct算法声明。
6. q3,t3、D≤2时，k≥4有H(k)≥7k−19>2k，故K(D)≤3，再得D K≤6<8矛盾，完全覆盖任意nonlinear selectors及任意partial。此为解析全域下界，不是固定cyclic函数的界。
7. Cyclic上界中good-a有23个、映射双射；4个bad-a的rank均2，每group degree4、每实际image resource degree3。任意左子集邻集≥4/3倍自身，Hall给每group再一枚不可分资源，所以各得24。未把fractional量冒充最终bundle。
8. 上界把24件selected incidences外送，余3件及全部未选state jobs停车，selected private10/9、其它private1、资源≤1，所有原jobs各一次。任意actual C<10/9提取真实exports后，由整数性每selected最多2件未送，给D2 allocation，与解析界矛盾。额外未选exports不会解除冲突。因此完整OPT=10/9。
9. v2未主张(C)逐参数包含v1全部强度、未改v1严格等号边界、未证明一般q,t全域nonlinear等于affine/cyclic；没有tiny-gap hardness或免费physical fiber一致性。

## 冻结状态

v1/v2 Exact、两版Proof及四份独立首写/final记录均已核hash，详见伴随manifest。首写中的非数学措辞精确化痕迹保留。没有软件实现、有限枚举或外部文献认证声明。

**两版作者Proof通过，无standing fatal；等待新canonical时再正式按指定§7–8/共定义§1及§9范围另冻实际读后。**

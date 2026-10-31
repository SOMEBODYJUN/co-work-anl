# 私有树配置五三界：v1/v2 作者证明读后审查

审查者：boss11 内部 cover_consistency。本次实际全文读取：

- root v2 proof `private_tree_configuration_floor_v2_root_frozen_proof.md`，SHA256 `e524ac4cf8df7310729477dc12f91c14842a90dff58953e66d3952397574a05a`，绑定 Exact `ad33f6b2c42c184b943651e61437ece2d1372ee1445443017e62534d83487900`。
- shared v1 proof `private_injective_tree_fractional_floor/private_injective_tree_fractional_floor_frozen_proof.md`，SHA256 `f4900b3693d6242cd08f218cbc478bb1e40ee6f072fb3205a5619b21fd1f40c5`，绑定 Exact `aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54`。

两份Exact-only独立稿的原字节保持：v1 `private_injective_tree_fractional_floor_statement_first_review.md`，SHA256 `96e2fd6d3a98093c3aa923457d23fc5ebdfad570656f3762ced2fb2e977f46c7`；v2 `private_tree_configuration_floor_v2_statement_first_review.md`，SHA256 `e197ac223247fb90471bb701dc139440b8f3f2c00419425a8adab8f88e4434d2`。此前未读作者证明的重构与本次读后审查分开记录，不因结论一致倒置来源。

结论：未发现standing fatal objection。v1的hitting/Haxell主链与本人独立稿一致。v2确实独立补齐了全CONFIG(T)、原P负载和非注入promise decision，且用的联合/min行条件足够强；没有误用单纯Σt≥a q。

## 1. 精确配置行与分解

v2 §1 的Σ(q−t_e)_+≤s q等价于我先行稿的Σmin(q,t_e)≥a q，a=d−s。必要性用每个machine真实配置中incoming与out-small同时出现的概率下界，成立。外机unit总边际≤1适用于T<2，并按每枚真实leaf job求和，重复f外机没有去重。

充分性中的区间分解逐项核：c_e=(q−t_e)_+在[0,q]内，Σc_e≤s q。把这些段串接后模q覆盖incoming区间时，每点至多s个段；单段长度≤q，故一个job不会在同一配置中重复。端点可用半开区间处理，零测点不影响有限配置权重。无incoming区间需要的剩余small边际

1−t_e−c_e = 1−q（t_e≤q），或1−t_e（t_e>q），

均在[0,1−q]内。故作者各small用初段的分解合法。q=0、1时跳过零长区间即可，不作非法模0/除0操作。无incoming时d个small总时长1，有incoming时≤s个small，负载≤1+s/d≤T。由所有断点划分只产生有限配置，权重为原概率区间长；不需要一个全局整数调度联合分布。

正部的线性扩展z≥0、z≥q−t、Σz≤s q与原行等价。selector各state根边际总和1、每edge/leaf两个端互补、external singleton/empty共同给完整CONFIG覆盖。T<1的selector障碍、T≥2实际全父置均正确。因此所声称poly-size精确系统不是仅一个必要松弛；finite网格1+j/d可精确判Tconf，仍不等于构造整数σ。

## 2. CONFIG(1)消元

s=0迫t_e≥q_v，沿私有树每leaf≥根y_us，资源行给同一λ系统（计multiplicity）。反向每state所有edges/leafs边际λ_us，机内incoming singleton/全部small两配置、external各真实leaf singleton加empty，完整覆盖正确。该消元本身无需state注入；注入是在后续资源叶集合hitting数才承重，作者已明确区分，没有错误推出非注入结构的配置gap。

## 3. 生成b流及共同a树分布

逐行核了 §3 的新b流。根b=y=q；归纳b≤q。对0<b≤q、每t≥0，min(b,t)≥(b/q)min(q,t)，所以out caps之和≥a b；按固定序从cap min(b,t_e)中装满总量a b可行。得到各b_e≤b、≤t_e，和a b。

条件向量b_e/b的坐标在[0,1]、和恰a，确为uniform-matroid base polytope，可有限分解成恰a个children的子集分布。节点激活概率为b时，该条件分布使child激活概率恰b_e；child原input边际是t_e，故归纳继续。b=0跳过，b>0必q>0，所有除法合法。即使state选择彼此互斥、同一路上的激活相关，也不改变此边际递归；未激活的node不进行选child。

各root先选一个state，再得到满a叉深h局部随机树；每leaf激活概率≤原t_leaf，各外资源共同期望≤1。不同root此时尚可碰撞，作者没有把这些局部分布当最终整数σ。分布可能指数多支持，本结论只用其有限存在和共同capacity，没有隐含多项式输出。原state注入使每生成candidate a树全部叶外机互异；其余虚拟candidate不是新增原P机器。

## 4. Haxell对象、严格差及primary

v1/v2的树阻断递归正确：要杀死全部r叉高h子树，至少a−r+1个child必须被杀，各自最少前一高度阻断数，所以精确数为B_h=(a−r+1)^h。单态注入把原叶数等同不同资源数；失去注入时这一步不能保留。

辅助超图每edge恰一root加R=r^h个不同resources，总edge size R+1。transversal只在resources中选，不能靠root本身命中。任意root子集I的hitting集X打中每个正权candidate内全部r-subtrees，共同分布加权给τ≥B_h|I|。若B_h≥2R−1，则

τ≥(2R−1)|I|>(2R−1)(|I|−1)，

严格差至少2R−1>0。因此不是把Haxell的严格>误用成≥；R=1、I单点、I空均合法。重复超边可去重保一个state/subtree witness；零权states可不列入辅助分布，但原任务仍须回填。

前一阶段已实际读Annamalai arXiv1509.07007v2 PDF2/印1 Thm1.1。此次又实际联网读Asadpour–Feige–Saberi作者稿 *Santa Claus Meets Hypergraph Matchings*, 2008-06-17，https://www.wisdom.weizmann.ac.il/~feige/mypapers/santaclaus1.pdf ，PDF5/印5 Thm2及其前方transversal定义：该稿资源侧rank≤k−1、阈值2k−3，故代入k=R+1恰是2R−1；也读了PDF6/印6 Thm3的普通子集论证作范围比对。没有声称已取得/全文重构Haxell1995原证明。此处依赖的是已核primary研究论文中准确陈述的外部定理，不把该经典定理当新原创。

## 5. 原d树和全部原P回填

匹配得到每root一个真实state和r-subtree，所有selected leaf资源互异。实际父端处理时间仍是1/d，不是1/a。active node收一unit（根为selector），r个out-job下送，d−r个small留父，负载2−r/d；未激活原分枝及未选states无unit incoming，全部d个small留父，负载1；external最多一个unit。每枚原internal/leaf/selector恰分配一端。原d树的额外分枝、同state其它candidate以及λ零state都没有被删掉或各建一份机器。

r=ceil(a/3)给a−r+1≥2r−1，二项式/凸性给(2r−1)^h≥2r^h−1。作者写x=a/d，C≤2−x/3、T0=2−x，C≤(5/3)T0等价x≤1，确实成立；并有T0≤T。其它T≥2全父置C≤2补齐全阈值。未宣称5/3为锐界。

## 6. C仅为判定及非注入原jobs

实际C≤1时，selector所在root被unit塞满，所有positive父端small必须下送；逐层迫使所选state整棵树全部unit下送，所有叶必须外机互异。因此真实C1解不可能用被过滤state；过滤后积分λ存在。无候选或过滤LP失败的NO输出只说明原OPT>1，足以不误拒YES承诺，而不保证NO承诺自身成立。

过滤LP可行时，在保留注入states上用s0存在性得到C≤5/3；每个被排除state全部原jobs父置，由全私有性使其每机负载1、没有selector incoming，不占external。故这是原完整P上的存在调度，不是删掉坏state任务后的新实例。

检查单射及写过滤λ LP按显式P为poly，精确有理LP可行性deterministic bit-poly。因此程序可区分promise YES OPT≤1和NO OPT>5/3。它可以对中间带任答；没有声称YES输出意味着OPT≤1，也没有声称NO输出意味着OPT>5/3。作者显式只输出decision、不输出σ；非注入原CONFIG(T)间隙上界并未被证明，文稿没有错误升级。

## 边界与准确身份

d=1、a=r=1、任意h以及所有零概率分支在上述式子中有效。U空须另返回OPT0/空σ（若使用promise接口则答YES），不套非空selector下界。完全显式P控制矩阵和LP编码长；没有把exp子树support或constructive Haxell未经核的rank依赖藏进算法声称。

本报告只核数学正文及所声明decision机制。未读取/执行实现代码，没有有限实例审计或生产实现认证；未认证全球新颖性或独立论文价值。结论仍是限定私有树结构的配置/threshold边界，不是一般UM五三算法或UM-TARGET-v1反面。

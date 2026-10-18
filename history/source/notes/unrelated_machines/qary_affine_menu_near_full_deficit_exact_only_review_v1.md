# q-ary affine 菜单近满缺项界：Exact-only 独立审查

审查者：general_query_response_review。2026-10-18。

冻结前仅实际读取 /workspace/scratch/038d9dcc4cac/qary_affine_menu_near_full_deficit_exact_v1.md；未读任何q-ary作者Proof、root或其它agent推导。未作软件枚举、求解器调用或代码认证，未改repo/Work/Git。

Exact SHA-256：ed16808a96e27a50e4d02ab8c2ec83e7f0df9046176531e45db38f5af5170afb。

**独立判断：(A)、(B)、(C)全部有效，无fatal。证明量化任意全局nonlinear选态与任意partial subsets。q=3,t=2的D*=2、V*=7/9及完整actual OPT=11/9解析闭合；q=3,t=3仍只给2≤D*≤3，没有关闭全域nonlinear最优。**

## 1. 固定任意选态，先算两个完整支持的交

记N=q^t。任意固定函数ell:F_q^t→F_q^t，不作线性、坐标分解或置换假设。写S_g为该group实际选中的完整state支持，B_g为其任意实际领取子集。每S_g恰N项。

对两个不同groups g,h，令E(g,h)={i:g_i=h_i}、r=|E(g,h)|。

在g_i≠h_i的坐标，两条方程相减给

(g_i−h_i)a_i=ell_i(g)−ell_i(h)，

从而a_i及b_i唯一确定；分母非零，可在给定F_q中求逆。

在g_i=h_i的坐标，若ell_i(g)≠ell_i(h)，两式不相容；若两标签相同，则a_i任意q选、b_i随之唯一确定。

因此完整交集或者为空，或者恰q^r项；特别g,h在每个坐标均不同，则交集总恰一项，与所有nonlinear标签取值无关。

## 2. 证明(A)：近满条件先迫低重数

设整数D≥0，每|B_g|≥N−D，且2D<q。令M_g=S_g\B_g为该group删去/未领取的项，故|M_g|≤D。若S_g∩S_h非空且g,h至少有一个坐标相同，由上一节交集至少q项。但B_g与B_h不交，故交集每一项都必须被g或h删去，即

S_g∩S_h⊆M_g∪M_h，

从而q≤|S_g∩S_h|≤|M_g|+|M_h|≤2D，矛盾。

所以在当前近满条件下，任意相交的两个选中state对应groups必须在全部坐标都不同。这个断言并未约束ell为任何特殊函数型，只由大交集与两端删除预算推出。

对每真实resource u定义重数

r_u=#{g:u∈S_g}，

以及x_u=#{g:u∈B_g}。Disjoint allocation给x_u∈{0,1}。若r_u>0，则所有包含u的groups在每坐标两两不同；固定任一坐标，其group符号必须互异，故r_u≤q。包括r_u=0在内，全部资源均满足0≤r_u≤q。

## 3. 证明(A)：双计数冲突对与缺项

每个group g有恰(q−1)^t个groups h与它在所有坐标均不同；这些pair各恰交一项。上一节又排除了任何有相同坐标的pair相交。因此

sum_u binom(r_u,2)=N(q−1)^t/2。

左侧是按真实交资源数两两冲突，右侧是按无序group pair数冲突；没有重复漏算，也不假定各pair交点不同。

总缺项数L为

L=sum_g |M_g|=sum_u(r_u−x_u)≤ND。

对r_u≥1，x_u≤1给r_u−x_u≥r_u−1。对1≤r_u≤q，有

binom(r_u,2)=r_u(r_u−1)/2≤q(r_u−1)/2。

r_u=0时两者均按0计。于是

ND≥L≥sum_u(r_u−1)_+
      ≥(2/q)sum_u binom(r_u,2)
      =N(q−1)^t/q。

除以正数N即

D≥(q−1)^t/q，

正是(A)。该结论没有假定D是最优缺项数；任何满足前提的allocation都适用。资源可以不用，此时x_u=0只会增加L。B_g可以任意non-Cartesian partial形状，全部计数仍成立。

严格条件不可偷换：2D=q时，大交集大小q可以由两group各删D项覆盖，上面的矛盾失效。本独立证明没有将等号纳入(A)，也未声称等号情形一定反例。

## 4. 从(A)到(B)：整数与min的完整分支

有限显式state及子集数保证最优m*达到，D*=N−m*为非负整数。

- 若2D*≥q，则D*≥ceil(q/2)。
- 若2D*<q，则对其实际达到allocation应用(A)，得D*≥ceil((q−1)^t/q)。

两个分支都蕴含

D*≥b_(q,t):=min{ceil(q/2),ceil((q−1)^t/q)}。

故V*=1−D*/N≤1−b_(q,t)/N，正是(B)。这里不能误把min改为max，或在第二分支取消2D*<q前提。

q=2时(A)仅适用于D=0，其推导给D≥1/2而排除全满；(B)给D*≥1，符合二元端点。t=1时b_(q,1)=1；任意两个不同groups在唯一坐标不同，其支持必交，故全满不可能，也与一般推导一致。所有ceil均为精确有理整数上取整，没有浮点计算。

## 5. 全部ordinary原jobs与(C)

原instance中每selected private机同时有该group唯一selector1，以及该state全部未外送incidence的private负载。对任意完整actual schedule：

若其峰C≥2，则C≥1+b_(q,t)/N已成立，因为b_(q,t)≤ceil(q/2)≤q≤N。

若C<2，每resource机最多容纳一件unit incidence，包括未选states的exports。按每group selector实际所在state，定义B_g为该state真正外送到资源机的incidences对应的资源子集。它们全局不交，是(B)量化内的一份合法allocation；没有忽略其可能nonlinear选态，也没有要求未选state无exports。

令d_g=N−|B_g|，D=max_g d_g。由于所有任务实际完整执行，selected state未外送的每件incidence只能留本private机，因此该机负载恰

1+d_g/N。

这给C≥1+D/N。提取的allocation有共同基数min_g|B_g|=N−D≤m*，故D≥D*≥b_(q,t)。于是任何实际调度皆有

C≥1+b_(q,t)/N，

即(C)。

反向的完整jobs构造也可独立验证：给任意合法selected-state allocation，selector放其所选state，B_g的incidences外送，其余全部原incidences留各自private机，包括所有未选states jobs。Selected负载为1+(N−|B_g|)/N，未选private恰1，资源≤1。因此最优allocation实际给OPT=1+D*/N=2−V*。这条一般normalized identity在此已逐原job证明，不以抽象资源分配代替任务执行。

## 6. q=3,t=2的解析精确witness

此时N=9。若D≤1，则2D<3，(A)给D≥4/3，矛盾；等价地(B)给

D*≥min{ceil(3/2),ceil(4/3)}=2。

独立达界构造：对g=(g_1,g_2)取原列表中的state

ell(g)=(g_2,g_1)。

给该group领取所有满足a_1 a_2≠1的a所对应的唯一资源

b_1=g_2−g_1 a_1，
b_2=g_1−g_2 a_2。

F_3中恰两个a满足a_1a_2=1，即(1,1)、(2,2)，故每group恰7项。若同一(a,b)来自g,h，写delta=g−h，则

delta_2=a_1 delta_1，
delta_1=a_2 delta_2。

因a_1a_2≠1，得delta_1=delta_2=0，故groups相同。所有7项bundles全局不交，给D*≤2。

因此D*=2、V*=7/9。完整actual schedule按上一节反向规则，把全部9个selectors放所选state；各所选state外送这7件原incidences、其余2件留private；所有未选state的原jobs全留各自private。Selected私机负载1+2/9=11/9，未选机1，资源≤1。共有9³=729枚incidences及9枚selectors全部执行；不是只执行81?枚selected jobs的子实例。由(C)反向界，完整OPT_3,2=11/9。此论证不使用MILP不可行返回或有限枚举。

## 7. q3,t3与一般nonlinear范围：不关闭

q=3,t=3时，(B)仅给

D*≥min{2,ceil(8/3)}=2。

D*=2时2D*=4不小于3，不能再调用(A)强迫D*≥3。本Claim绝不能被解读为全域精确3。

Exact引用的cyclic D=3上界也可独立核到，但只作witness上界：一般cyclic选择ell_i(g)=g_(i+1)中，令k=(q−1)^(t−1)为满足prod_i a_i=1的bad-a个数。其余a的g↦b映射可逆，全部资源可各分给唯一group。每个bad-a的线性映射kernel恰q个元素、image恰N/q，故该a每个used resource邻接q个groups；每group在bad资源图中恰degree k，全部resource degree q。

每条边给1/q的fractional量，则每行k/q、每列1；按所有子集Hall可给每group至少floor(k/q)个bad resources。加上每group全部N−k个good resources，得到缺项

k−floor(k/q)=ceil((q−1)^t/q)。

q3,t3为k4，每group匹配1个bad resource，缺项3，所以仅得2≤D*≤3。这里证明的是cyclic指定state族的可达上界，未排除其它nonlinear选择可达D2。一般q>2,t的全域nonlinear最优未被本文关闭；同样未生成tiny-gap困难性或排除所有tensor操作。

## 8. 显式规模与位复杂度

N groups、N² indexed states/private机、N²资源机、N³枚incidences及N枚selectors，sparse有限资格2N³+N²，均与Exact一致。每state恰N项且private总和1，权为普通二进制有理1/N，位长O(t log q)。给定标准有限域表示，涉及的加减乘除及tags、计数整数位长均在显式规模内多项式。

近满下界是任意给定allocation/完整actual的解析性质，不承诺多项式寻找最优nonlinear selector。上述特定cyclicwitness和可选Hall matching可按展开graph生成；没有poly(t,log q)输出全部N³ jobs的声明。未作软件实现/运行认证。未添加任何状态一致性物理gadget或更窄selector量词。

**最终冻结：Exact (A)/(B)/(C)通过，q3,t2全域allocation与actual精确端点通过，无fatal；q3,t3及一般nonlinear全域最优仍未关闭。**

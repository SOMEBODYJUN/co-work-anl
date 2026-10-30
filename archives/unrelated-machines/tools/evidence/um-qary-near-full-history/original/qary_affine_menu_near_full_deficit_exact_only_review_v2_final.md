# q-ary affine 菜单 fiber 缺项合同：v2 Exact-only 独立审查

审查者：general_query_response_review。2026-10-18。

本轮仅读取新v2 Exact：
/workspace/scratch/038d9dcc4cac/qary_affine_menu_near_full_deficit_exact_v2.md

SHA-256：584e7e3ad6ae0ad44b03781a3b9069d6cafa2296e59cfc7eb75070c08eea8759。

未读任何q-ary作者Proof、root其余推导或其它agent输出。仅scratch新增记录，未改repo/Work/Git，也未改v1原记录。v1“q3,t3尚未关闭”保留其旧时点；v2是新增全局必要界并闭合该端点的新版本。

**独立判断：v2 (A)–(D)全部有效，无fatal。Concurrent任意非空子family的projection恒等式、遗漏预算、H/K必要界及单调、全局D K(D)下界均成立；q3,t3全域nonlinear最优现解析精确为D*=3、V*=8/9、完整actual OPT=10/9。没有推出一般q,t的nonlinear最优。**

## 1. 任意concurrent子family的精确union恒等式

记N=q^t。固定任意全局选态函数ell(g)，任其完全nonlinear。固定真实资源x=(a0,b0)，任取非空F⊆F_x、k=|F|。因x属于每个g∈F的完整选中支持，

ell_i(g)=b0_i+g_i a0_i

在F上逐项成立。这里只使用局部concurrency，不要求全局ell采用此形式。

资源(a,b)属于某g∈F的支持，当且仅当

b_i−b0_i=g_i(a0_i−a_i)

对所有坐标成立。令J={i:a_i≠a0_i}。

- i不在J时，a_i=a0_i且必须b_i=b0_i，没有group坐标限制。
- i在J时，c_i=a0_i−a_i非零，a_i有q−1种选择；给定这些a_i，b_i−b0_i=c_i g_i将π_J(g)双射编码为b_J。

所以固定J及非零c_J时，union中真实资源数恰|π_JF|。不同J、c_J给互不相交的资源；总计

|union_(g∈F) S_g|=sum_(J⊆[t])(q−1)^|J| |π_JF|。

J为空时恰资源x一枚，对应非空F的空投影一枚tuple，系数1。这个推导适用于F_x的任意非空子family，并不要求F是整个fiber、Cartesian block或affine subspace。没有假设x被任何B_g实际领取。

Concurrent前提实质必要：若不知各ell_i(g)=b0_i+g_i a0_i，则上述共同基点化约失效；本审查未把恒等式应用于任意非concurrent family。

## 2. 任意partial allocation的遗漏预算

给定各group缺≤D的disjoint allocation，限制到F仍有

sum_(g∈F)|B_g|≥k(N−D)。

这些B_g全局不交且均包含于union_(g∈F)S_g，因此

k(N−D)≤|union_(g∈F)S_g|。

利用N=q^t=sum_J(q−1)^|J|及上一节恒等式，即

kD≥kN−|union S_g|
   =sum_J(q−1)^|J| (k−|π_JF|)。

其它groups占走资源只会进一步限制F的领取，不会削弱此必要界。资源可不用，B_g可任意非product partial子集；未要求state全量导出或分数切割物品。每项k−|π_JF|非负。

## 3. H界、K界及完整单调性

对|J|=j，恒有|π_JF|≤min{k,q^j}，故

k−|π_JF|≥max{k−q^j,0}。

J为空时精确为k−1。按同大小J求和，就得到

H_(q,t)(k)=(k−1)+sum_(j=1)^t binom(t,j)(q−1)^j max{k−q^j,0}
          ≤kD。

尤其取F=F_x，对每个非空实际fiber大小k_x成立。H并未被证明对每种k都可同时达到，当前证明只给粗投影必要界。

k=1时H(1)=0，故定义K(D)的候选集合非空；其余k∈[1,N]有限。因此每个满足H(k_x)≤k_xD的实际fiber必有k_x≤K(D)，不需额外假设K可达。

单调性可以直接逐项核实：

H(k)/k=1−1/k
       +sum_(j=1)^t binom(t,j)(q−1)^j max{1−q^j/k,0}。

当实数k≥1增大时，每一项不减，首项严格增，因此H(k)/k严格增（当然也满足Exact所需不减）。所以固定D的合法整数k组成初段，整数比较H(k)≤kD即可二分求K。D增大时合法集包含关系给K(D)不减；D≥0且K(D)≥1，因而D K(D)也不减。

这仅计算投影必要界，绝非寻找最优nonlinear selector的算法。D=0时H(k)≥k−1迫K(0)=1；空fiber不在K声明内，之后按重数0另处理即可。

## 4. 全局(C)：把全部不可避免pair冲突与fiber上界接起来

对每真实资源u，记r_u=#{g:u∈S_g}，x_u=#{g:u∈B_g}。有x_u∈{0,1}，r_u>0时由上一节r_u≤K(D)，r_u=0时x_u=0。

任意两个groups g,h若在全部坐标都不同，则无论ell如何nonlinear，其支持恰交一枚资源：每坐标方程相减后非零系数唯一解a_i、b_i。每group有恰(q−1)^t个这样的h，故按无序pair计，不可避免交点数为N(q−1)^t/2。

其它pair的交可能为空或多枚，只会增加总pair-incidence，因此一般情形是

sum_u binom(r_u,2)≥N(q−1)^t/2。

这里与v1不同，不排除任何共享坐标pair，也不需要2D<q。

总遗漏L满足

L=sum_g(N−|B_g|)=sum_u(r_u−x_u)≤ND，

且L≥sum_u(r_u−1)_+。因r_u≤K(D)，对r_u≥1有

binom(r_u,2)≤K(D)(r_u−1)/2。

合并得

ND≥L≥sum_u(r_u−1)_+
      ≥[2/K(D)] sum_u binom(r_u,2)
      ≥N(q−1)^t/K(D)。

K(D)≥1，故乘除合法，得到

D K(D)≥(q−1)^t，

正是(C)。它覆盖全部D∈{0,...,N}，包括D0会直接被排除；允许资源不用、任意partial、任意全局nonlinear选态。此为必要条件，未给充分性，也未声称取到K即可构造allocation。

## 5. q=3,t=3：精确排除D≤2

N=27，此时

H(k)=(k−1)+6(k−3)_+ +12(k−9)_+ +8(k−27)_+，
1≤k≤27。

H(3)=2≤2·3，而H(4)=3+6=9>2·4。由H(k)/k的单调性，K(2)=3。K随D不减，所以对所有0≤D≤2，

D K(D)≤2 K(2)=6<8=(q−1)^t。

(C)因此排除D≤2，得D*≥3。这是覆盖所有nonlinear选态与任意partial allocation的解析下界，不是固定cyclic selector的下界，也不依赖MILP。

v1只在2D<q时可用，当D=2,q=3时不能排除；v2新增fiber上界正是补足此处。旧v1记录保留，不用新结论改写其历史。

## 6. q3,t3独立cyclic达界见证及整数matching

取ell_i(g)=g_(i+1)，循环下标g_4=g_1。对每个a，令

L_a(g)_i=g_(i+1)−a_i g_i。

若两groups在同一(a,b)碰撞，则差delta满足delta_(i+1)=a_i delta_i，绕环给delta_1=(a_1a_2a_3)delta_1。

当a_1a_2a_3≠1时，delta=0，故线性映射L_a为双射。F_3^3中恰4个a满足乘积1，因为前两个非零坐标各2选，第三被确定。因此有23个good-a；每group领取它在每个good-a的那一个resource，得到23项，且跨groups完全不交。

对4个bad-a，全部a_i非零且乘积1，kernel由delta_1任意决定，恰3元素；故每个image资源恰属于3个groups。固定group在每个bad-a各有一枚state资源，因此bad-resource二部图有27个groups，每行degree4，每资源列degree3，资源总数4·9=36。

任意group子集A有4|A|条incident edges，其邻集每资源至多承载3条，故|N(A)|≥4|A|/3≥|A|。Hall给覆盖27组的整数matching，为每group再添一枚bad resource。它与good部分a标签不同，不会冲突。

总计每group真实领取24项且全局不交。因此D*≤3，与上一节合并：

D*=3，V*=24/27=8/9。

Matching仅用于这个明确witness，未声称所有selector都同样好、cyclic对一般q,t全域最优、或分数bad资源等于整数bundle。

## 7. 全部原jobs的actual端点

给上述24项分配，把每group selector放其cyclic原state；该selected state恰24枚原incidences外送，余3枚留原private机。所有未选states的全部原incidences都留各自private，不删除或复制任何job。

Selected private负载1+3/27=10/9，未选private恰1，资源机至多一枚unit。因此实际完整上界为10/9，执行的是27³枚incidences及27枚selectors的完整instance。

对任意完整actual schedule，若C≥2，下界10/9平凡成立。若C<2，每resource最多一unit；按每selector实际state取其真正外送incidences，得合法全局disjoint B_g，即使未选states也有exports仍如此。令d_g=27−|B_g|，D=max_g d_g，则selector所在private负载恰1+d_g/27。由v2全域allocation界D≥3，峰C≥1+3/27=10/9。

所以完整ordinary OPT_3,3=10/9。没有把partial allocation直接冒充全部jobs已执行，也没有免费增加任何state-consistency物理约束。

## 8. 位复杂度与范围核验

全部对象计数N groups、N² indexed states/private、N²资源机、N³ incidence jobs与N selectors、2N³+N² sparse finite资格均正确。普通有理1/N位长O(t log q)，给定标准F_q表示即可作所需有限域运算；没有将prime-power整数环误当域。

H(k)有t+1项，powers/binomial及结果的位长O(t log q)量级；例如0≤H(k)≤kN≤N²。逐项整数求值、H(k)≤kD比较及O(log N)次二分均对log N=t log q及这些显式计数的编码位长多项式，因此对展开instance位长多项式；不称仅依log t+log q的succinct标量输入长度多项式。不枚举候选ell，不求一般nonlinear optimum。

显式生成complete matrix、给定见证回算及q3,t3 witness matching也对展开总规模多项式，不声称poly(t,log q)输出N³件任务。此处无软件运行/实现认证。

v1的严格近满合同保持原阈值与原记录，q3,t2端点不受影响。v2没有宣称(C)逐参数支配v1、没有把H粗界说成tight，也没有闭合其它q,t的所有nonlinear selectors；不产生normalized tiny-gap复杂性源，不排全部tensor，不免费强制全fiber或block-fiber一致性。标准投影与matching计数本身不作原创性认证。

**最终Exact-only冻结：v2 (A)–(D)有效，无fatal；q3,t3作为新解析后果现已闭合为D*=3、V*=8/9、完整actual OPT=10/9。旧v1字节不改，尚未读取任一q-ary作者Proof。**

计量措辞冻结说明：首写v2原字节保留（SHA 322d2cc388cc34a34f9ec122e6960b6b72556639b5b3001b185cf6eefb47f626）。本final仅把§8“参数位长”的一句精确为log N=t log q及展开输入计量，明确不作log t+log q的succinct标量复杂度声明；数学证明和结论均未改。

---
id: customer-attraction/fixed-old-group-prefix-three-player-free-two-tail-MILP-contract
kind: resource
type_tag: 资源
title: 固定旧组前缀的三人自由两尾MILP合同
status: two-whole-primary-sources-read;local111-node-model-understood;zero-new-MILP-or-replay
summary: 保存C0固定后C1D0D1三人子局111节点、17客户参数、M3有效界及1437变量7514行的完整语义；超时a0/dual−2仅内置a2盒界，原Infinity和110动作不冒全四人或精确验收。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/anchor_two_tail_milp.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-977d3dbff13346b3b7c0f5a4caa6168e/credible/two_tail_milp.json
---

# 固定旧组前缀的三人自由两尾MILP合同

4610B源码和1656B原报告共6266B全文实读、核原size/SHA256/Git blob。源码依赖刚读完的6482B AnchorSearch及其动态6427B comp原件，均同SHA保原树，无新增依赖取源或primary done。本页完整说明建模等价性在何处成立、有效界从何而来及原超时记录的全部内容；本批未跑MILP、提取策略或精确IC。

## 固定前缀后仍有三人，不是四人整树

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)及[两组两锚参数构造](三锚对称参数族的强制路径DAG与浮点探索合同--资源.md)的k2/r2特例。每组标签依次(C_i,A_i,B_(i,0),B_(i,1))，两锚D₀,D₁索引8,9，p10、全局m4。每组X_i同权x，H_i同权a；公共core为四位(B₀-role,B₁-role,D₀,D₁)全部15非空兴趣类型，每个B位同时喜欢两个组的相应B标签。故17列为x,a,c₁,…,c₁₅。

前缀固定已有人选C₀（索引0），随后三人实际拟选C₁（索引4）、D₀8、D₁9。程序为其后的全部反事实行动a、b、c建模，终局计数q=e₀+e_a+e_b+e_c，使用AnchorSearch的四人pay/scale计算精确收益系数。

当前首剩余者只有C₁上的X₁，没有锚与其重叠，且x=1，所以其规定路径收益恒1。自由选择的是余两层的动作：每个a后选一个b，每个(a,b)后选一个c；a=4的实际孩子强制b8、c9。相对C₀子博弈有1+10+100=111个决策节点；完整四人游戏根域有1+10+100+1000=1111。本模型没有空根C₀玩家的激励，也没有其他首玩家行动之后的整棵子局，不能以111节点局部候选称四人全SPE。

## a2及M3是有效的本地界，不是经验阈值

令Y_b=Σ_(core含B位b)c_core，D_d=Σ_(core含D位d)c_core。若局部根确选C₁并收益1，偏离到fresh A₁或fresh B_(1,b)、锚D_d时，相关客户均未被C₀覆盖，后面只两人，故收益至少主题大小的1/3。于是局部根IC必要给
\[
\frac{1+a}{3}\le1,\quad\frac{1+Y_b}{3}\le1,\quad
\frac{D_d}{3}\le1,
\]
即
\[
a\le2,\quad Y_0,Y_1\le2,\quad D_0,D_1\le3.\tag{1}
\]
因此C_i大小1、A_i和所有B_(i,b)大小≤3、锚大小≤3；任意后续玩家收益均在[0,3]。每个非空公共core至少落在一个B或D边际，故单独c_core≤3也是有效界。代码因此设x1、a∈[0,2]、每公共列[0,3]，另加(1)四个总边际行。

条件常数M=3使两个[0,3]收益差在未选动作时自动松绑；rootpay∈[0,1]更紧但差的绝对值仍≤3。这里归一化是私有x，而非W=1；不能直接搬[一般全树联合表示](../等价/有界联合策略与客户重数表示--等价.md)由根福利归一推出的M=m论证。此M3由本局部fresh主题偏离单独推导，正是源码注释的有效界。

## 1437变量与7514约束的完整语义

变量均先取非负。17个客户参数后，对每(a,b)设first/second/last三个收益量，各100，表示最后c按政策选择时三名剩余者的真实利润；另rootpay[a]10个、vsecond[a]10个。共337连续变量。choose2[a,b]100个和choose3[a,b,c]1000个均0/1，合1100 binary；总1437。

设u_t(a,b,c;w)为固定旧C₀后该玩家t的线性利润。选中最后c的指标z₃使三个value各满足
\[
-3(1-z_3)\le value-u_t(a,b,c;w)\le3(1-z_3).\tag{2}
\]
这三者使用**同一个**choose3，未独立挑选对不同玩家有利的终局。每(a,b)另要求Σ_c choose3=1以及
\[
last[a,b]\ge u_c(a,b,c;w)\quad\forall c.\tag{3}
\]
所以被选末位的收益等于其真实利润且至少每个合法替代，正是末位BR。

对每a要求Σ_b choose2=1，并对每b加入
\[
vsecond[a]\ge second[a,b],\quad
vsecond[a]-second[a,b]\le3(1-choose2[a,b]),\tag{4}
\]
以及rootpay[a]与first[a,b]在choose2选中时相等的两条M3条件。这使被选b达到所有真实末位回复所给收益的最大值，且rootpay[a]传播同一被选叶的首剩余者利润。

最后强制choose2[4,8]=1、choose3[4,8,9]=1，故rootpay[4]=1。虽然代码没另写rootpay[4]≥rootpay[a]，**所有rootpay[a]上界1已经恰好实现这些根IC**，并未遗漏局部根理性。由(2)–(4)倒推可得所有111节点的三人子局纯SPE；反之任何上述指定实际路径的局部纯SPE都满足有效界和这些变量约束。因此精确整数可行点在这个受限参数族内确有局部SPE语义，而非仅有限必要条件。

行数可按源码结构核：4边际行，10个choose2单选行，每(a,b)有5行（(4)两、rootpay传播两、choose3单选一），每(a,b,c)有7行（三收益条件等式的6行与末位BR一行），合
\[
4+10+100\cdot5+1000\cdot7=7514.
\]
该结构核没有构建或求解MILP。它不把局部三人SPE升级成全部四人根SPE，不把箱域内可行点推广成任何目录/参数结论。

## 原目标、超时界与全部13字段

目标系数只有a变量为−1，即最小化−a；调用scipy.optimize.milp，time_limit默认120秒、mip_rel_gap=10⁻⁷。主入口无k/r等参数，始终AnchorSearch(2,2)。

1656B报告顶层13字段全部保留：

| 字段 | 原值 |
|---|---|
|status|1|
|message|Time limit reached. (HiGHS Status 13: Time limit reached)|
|variables|1437|
|rows|7514|
|seconds|120.11263060569763|
|mathematical_status|MILP discovery only; no exact feasibility or universal dual certificate claimed|
|a|0.0|
|weights|下述完整17项|
|choose2|下述完整10项|
|choose3|下述完整100项|
|mip_gap|原token Infinity|
|mip_node_count|8277|
|mip_dual_bound|-2.0|

最小化−a的浮点dual lower bound−2转成最大化a的upper bound2；它恰等代码已给的a≤2盒界，**未比内置边界更紧**。a0只是原数值incumbent，time limit与Infinity不是a0最优/不可行或a≤1/2的证书。没有精确全MILP对偶或最优证明，也不能把8277节点当枚举全部策略。

原Infinity是Python json.dumps允许的非有限字面量，严格JSON不接受；归档原字节不改，当前按Python解码保并另标该token，不能改成null、0或有限gap冒原报告。

## 全部客户权重与局部动作表

完整weights[0…16]为x1.0，a0.0，c₄=0.5（index5）、c₈=0.5（index9），其余13项0.0。即两个组私有X各1、无H、两锚各有不交私有0.5；此处只是原浮点参数内容，没有宣称本轮清分母验证了一份新单位客户SPE。

choose2[0…9]原为[4,4,9,7,8,6,1,5,4,7]。choose3的完整10×10表按a行、b列如下：

| a/b | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|0|5|5|7|5|9|4|7|7|4|4|
|1|5|7|7|7|9|7|4|6|7|4|
|2|7|6|4|6|5|4|6|7|5|5|
|3|5|4|6|7|6|6|7|7|6|7|
|4|6|9|8|4|9|8|9|2|9|5|
|5|5|7|8|7|8|1|8|2|4|5|
|6|5|4|5|7|9|8|2|1|4|6|
|7|7|9|7|7|3|9|2|0|4|4|
|8|7|5|4|4|5|6|4|6|4|4|
|9|5|5|6|5|6|7|5|6|6|5|

配局部根行动4，这110个动作定义全部111相对历史的候选，且数组给actual(4,8,9)、完整全局前缀路径(0,4,8,9)。源码是对result.x每组选argmax打印，**没有**另核binary精确单选、Fraction客户、全部111节点IC或完整四人策略。虽然该权重简单，当前也只静态核数组域/强制项，不冒一次精确收益验收。

输出没有未舍入的连续first/second/last/rootpay/vsecond、完整原binary向量、逐约束松弛或规范策略证书；不能把argmax后的整数动作当原MILP精确可行已自动成立。若未来验收此局部policy，要用原权重、旧C₀背景和全部真实孩子逐节点核，而非把三剩余者当零背景游戏。

## 依赖、输出与全仓比较

本main从相邻anchor_general_cones导入AnchorSearch；该模块顶层动态加载旧R-ffea…cone_search，实际本入口只用AnchorSearch构造int收益表，不调用其solve/cone/另一150步LP。全树MILP自己选择choose2/3，未冻结某个原动作锥。两依赖原字节/先前normal capture同SHA保全，科学依赖numpy/scipy/milp/sparse版本未被原报告锁定。

源码有main guard，仅--seconds默认120与必填--output。记录seconds包含收益表/建模及求解总墙时，不能只由120.1126推回某个参数或纯solver时间。若result.x存在即导出candidate；按属性存在才附gap/node/dual。文件直接覆盖，父目录不自动建，stdout省weights/choose2/choose3；没有exact validation分支、stdout/stderr/argv或源码SHA历史绑定。当前无import、构造表、求解或精确重放。

与[三锚固定DAG探索](三锚对称参数族的强制路径DAG与浮点探索合同--资源.md)不同，本为r2局部111节点的自由两尾选择；那里r3/65参数/固定生成DAG，不把两种最优范围、计数或浮点结果互换。与[复制路径障碍](../障碍/两尾公共锚点族的旧组逃生与复制路径障碍--障碍.md)相比，后者只对固定X6/H4/特定公共块给全k严格偏离，本MILP无最优结果不能给整个锚点族半屏障。与[两尾FILTER](../定理/任意背景两尾产品门槛与可信叶过滤--定理.md)相比，本程序同时选择对每个a的两层回复；其BR逻辑仍是真实有序孩子，不是Cartesian可加问题。

[固定完整策略锥](../定理/固定完整策略的客户重数锥--定理.md)和[一般联合表示](../等价/有界联合策略与客户重数表示--等价.md)解释精确可行点与全历史策略的关系，但别处的原始点/最优对偶成功不替本报告认证。局部参数/动作图若获精确点，也仍需额外全局前缀激励才接成四人完整SPE。

完整5源claim52a70082…pushed/synced、本2 Boss4 owner/sourceSHA/normal-show、两依赖闭包及自查见[证据](../../tools/evidence/anchor-two-tail-milp-primary/README.md)。本批原MILP/main/import、AnchorSearch/comp执行、LP/BI/策略恢复/IC均0；只读公式、字段和动作表。一般模型的空重复/零客户/完整有序历史和离轨平局保，具体x1族按其正归一/箱界限定。无新外审、盲审、新颖性或一般half结论，第三阶段不建图。

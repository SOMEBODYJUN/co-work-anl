# 任意state权重的并行仿射线关系：rank独立Exact-first重构 v1

审查者：rank_deficiency_fee，2026-10-18。仅实际读取指定新Exact后独立重构；未读取作者Proof、作者口头策略或其它agent新推导。Root已见口头策略，不将root之后的核对倒称盲审。本记录先冻，只交root。仅clone外scratch，未改repo/Work/Git。

## 1. 读取对象与独立结论

实际全文读取：

`/workspace/scratch/038d9dcc4cac/weighted_affine_line_parallel_relations_half_escape_exact_v1.md`

wholeSHA256：`780454f7a404d2fd17edf2adbf2e8e2fdd8318f98686478547a3be58d4433c7e`。

对象ID：`UM-WEIGHTED-AFFINE-LINE-PARALLEL-RELATIONS-HALF-ESCAPE-v1`。

**独立结论：主半保留存在/确定性构造、全部原jobs actual≤3/2、计数/显式位长与singleton反例均成立，未发现standing fatal。** 以下给自足完整重构；没有把任意权重当共同item权，亦没有假定预知好state。

## 2. 对象及一族完整合法states

PrimeR≥2、k≥2。Groups j∈F_R，k个共同但tag互异的变量；A_j为全部Σ_i a_i=j的tuples，每组R^(k−1)states。资源(x_i,z,b)∈{x_i}×F_R²。State(j,a)中第i条line的点是(x_i,z,a_i z+j)，z∈F_R。每state恰D=kR个distinct资源。

权w_(j,a,u)任意非负二进制有理、逐state总1，可依赖整个a与各cell，允许0。原CSP任意完整赋值a恰满足j=Σa_i那一条，故value恰1/R。

考虑c,d∈F_R^k满足Σc_i=1、Σd_i=0，定义a(j)=cj+d。则Σa_i(j)=j，属于完整A_j。对这族所选states，tagi、固定z处的资源第二坐标为

    b=d_i z+j(c_i z+1)。

若c_i z+1≠0，j→b是双射；因此在这个tag与z处，各groups的资源互异。若c_i≠0且z=−1/c_i，所有j都使用同一资源

    u_i(c,d)=(x_i,−1/c_i,−d_i/c_i)。

若c_i=0，则全部z处都互异，没有该tag共同资源。因此所选states的所有跨组碰撞仅为这些u_i，且每枚u_i属于全部R组。不同tag的共同资源互异；其余所选资源各只属于一组。

令K(c,d)={u_i(c,d):c_i≠0}。对每组定义普通有理数损失

    L_j(c,d)=Σ_(i:c_i≠0)w_(j,cj+d,u_i(c,d))。

若共同资源都暂不分配，组j领取自己所有非共同点就有质量1−L_j。

## 3. 处理任意state-dependent权的平均界

在集合C={c:Σc_i=1}、D₀={d:Σd_i=0}上分别均匀、独立取c,d。此概率仅作存在性分析，最终算法不需随机性。

固定j。映射(c,d)↔(c,a=cj+d)是C×D₀与C×A_j之间的双射，因为d=a−cj，且Σd_i=j−j=0。故**即使条件在任意具体state a上，c仍在C均匀**。这是允许w任意依赖a的关键，不能只用c_i的无条件边际。

k≥2使每个坐标c_i在F_R均匀：固定c_i任意值后，另一个坐标可由sum条件唯一补足，其余k−2自由，恰R^(k−2)个c。

在固定selected state a中，点u=(x_i,z,a_i z+j)成为共同点的条件是：

* z=0时永不成为共同点；
* z≠0时恰c_i=−1/z，条件概率1/R。

当该条件成立，−d_i/c_i=a_i z+j确是u的第二坐标，故没有另一个未计条件。于是

    E[L_j | a(j)=a]
      =(1/R)Σ_(i,z≠0)w_(j,a,(x_i,z,a_i z+j))
      ≤1/R。

对a再平均及j求和，得

    E[Σ_j L_j]≤R·(1/R)=1。

因此存在合法c,d满足Σ_j L_j≤1。此结论不要求各组/各点权独立、不要求line质量均匀、没有max单项限制；只用非负及逐state总1。

## 4. 整数资源分配与半保留

取上述Σ_j L_j≤1的c,d。因L_j≥0，至多一组满足L_j>1/2。

若没有这样的组，给每组B_j=S_(j,a(j))\K(c,d)，所有B_j共同不交且各质量1−L_j≥1/2；共同资源可不用。

若有唯一j*满足L_j*>1/2，将全部共同资源给j*，令

    B_j*=S_(j*,a(j*))，
    B_j=S_(j,a(j))\K(c,d)  (j≠j*)。

共同资源在每组支持内，故j*可领取它们；其它非共同资源各只属于自己的组，给出真正不可分、pairwise-disjoint分配。组j*质量1，其余各1−L_j≥1/2。

L_j=1/2的等号不算bad，恰满足保证；若L_j*=1、其它0同样有效。最终没有物品分数执行，也不要求B_j按变量/product分解。故V(w)≥1/2，state choices正是Exact指定affine-in-j族。

## 5. 确定性显式位多项式算法

枚举c的前k−1坐标、用最后坐标补Σc=1；同样枚举d的前k−1坐标、补Σd=0。候选总数

    R^(2k−2)≤(R^k)²。

R^k正是输入显式states总数，故此枚举虽不对succinct(k,logR)多项式，却对**完整显式输入**多项式。每个候选计算R个state a(j)、至多k个共同点和Rk个权条目的L_j，精确有理求和并检查ΣL_j≤1；平均界保证至少一个候选成功。可取按枚举顺序第一个，不输入OPT或未知allocation。

全部权表已显式给出，可先按(j,a,tag,z)建立索引或排序查找，读取被用权不依赖隐式oracle。模primeR的加乘、非零求逆用标准整数算法位多项式。每次候选只做显式条目总数以内的有理加法；分母积位长不超过相应输入位长之和，所有精确比较仍多项式。没有按1/w或分母数值展开。

找到候选后按第4节显式列出全部B_j。生成支持及零私时job身份均按输入完整表和原标签输出。不枚举所有global任意state assignments，只枚举上述至多states数平方的结构族。无需随机样本、Hall oracle或未知最优witness。

## 6. 全部原ordinary-UM jobs的同一实际上界

P有每state独立private、每resource独立R_u、每group一selector1。每incidence原job只有private按w执行或对应resource1，含w0 job；所有未选states/jobs实际存在。

每selector放到第4节所选state private，仅将B_j对应incidences送各自真实resource，其余全部incidences留自己的private。Selected private负载

    1+[1−Σ_(u∈B_j)w_(j,a(j),u)]≤3/2。

Unselected private所有jobs总权1；resources因B_j不交至多一枚unit。全部selectors与全部incidences（含零私时、所有未选states）各执行恰一次，所有机器在同一assignment同时受控。故实际OPT≤3/2，selector1给OPT≥1。

计数重核：groupsR；每组statesR^(k−1)，private总R^k；resource kR²；每stateD=kR，incidences kR^(k+1)，selectorsR。Finite为两端incidence加selector资格

    2kR^(k+1)+R^k，

dense为(R^k+kR²)(kR^(k+1)+R)。实际完整输出与有理负载回算均按这些显式规模位多项式，不称poly(k,logR)编译。

## 7. Singleton及k=1边界反例

将关系改成A'_j={(j,0,…,0)}，保留same tags/intercepts/资源line定义。每组唯一state在i1的line满足b=jz+j。令z=−1（R2时−1=1仍非零），则所有j均含共同真实资源u*=(x₁,−1,0)。将该点权置1、其余全部0，逐state归一仍成立。

R≥2，而不可分共同u*至多分给一组，其余某组只有零质量点，所以V=0。完整actual C<2时，每组selector只能在唯一private。其唯一正私时incidence也time1，不能与selector留private，故R件都须去共同resource，各unit合计R≥2矛盾。所有jobs留private给每机负载2、零jobs负载0，因此实际OPT恰2。

此singleton CSP最优value为1/R：取其它坐标全0且a₁任意便满足恰一个j，任何赋值也至多一个。k=1时主关系Σa_i=j本身就是该singleton，故主半值结论不能扩掉k≥2。Singleton易判，不作为hardness。

## 8. 最终范围

主族确为degreeR、alphabetR、value1/R；任意state-dependent normalized权仍有deterministic actual≤3/2。若一个只改这些原incidence权而保全部groups/states/resources/eligibilities的接口，对整个包含本族的NO域声称partial值<1/2，则本族反驳。若另有hard image避开本族、允许改变gadget或预处理，未被排除。

Singleton说明不能把结论升级到任意relations；k≥2及完整all-tuples sum关系承担平均分析。Full-support YES若几何sets原已不交，则任意归一非负权都保full领取1，但未提供真正tiny-NO困难源。

本次独立认证完整Exact主要数学、算法及scope，无standing fatal；没有外部hardness重审、新颖性/外审认证或软件/有限实验。作者Proof与口头策略在本记录冻结时均未读取；后续若给作者Proof须另冻read-after，保持本记录原字节。

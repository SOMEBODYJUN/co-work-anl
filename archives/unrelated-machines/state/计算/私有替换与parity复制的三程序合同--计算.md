---
id: "unrelated-machines/private-graft-parity-three-program-contracts"
kind: "computation"
type_tag: "计算"
title: "私有替换与parity复制的三程序合同"
status: "all-canonical-code-and-fixture-read-with-historical-run-reuse"
summary: "保三套独立实现的父选择/私有根门/完整pool实际域、唯一fixture和13件token原输入；同hash历史输出复用，修明6点cap与16关系边不等于4见证边。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/private_graft_and_resource_repetition.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/private_graft_independent.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/resource_pool_independent.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/parity_3dm_repetition.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/private_graft_repetition_audit.json"
---

# 私有替换与parity复制的三程序合同

一般私有替换min恒等式、异质终端公式、根门公式、完整pool的分母匹配等价及parity全次张量，均由已有[保真障碍正文](../障碍/私有需求组合与共享三维匹配复制--障碍.md)完整证明。本页处理三个原程序和一份输入的全部独有实现、实际范围和复用方法，不重复认领Boss3主稿/审查或Boss2报告，也不把有限token例推广为主目标结论。

全部原字节、两完整来源commit/path和hash见[清单](../../tools/evidence/private-audits/source-manifest.json)。唯一外部数据依赖是[parity JSON](../../tools/evidence/private-audits/original/examples/unrelated_machines/parity_3dm_repetition.json)；其余测试输入由源码生成。三个程序都只用标准库，后两个没有导入规范oracle或仓库模块。

## 规范程序：根连通父选择及有限私有替换

[规范源码](../../tools/evidence/private-audits/original/tests/audits/unrelated_machines/private_graft_and_resource_repetition.py)的`score_tree`从root（默认0）沿children检查无重复到达、根入度0、所达非根入度1，并对**所有选中的原正需求点**取min(1,outdegree/k)，正需求输出叶也收费为0。`optimum`为每个非根枚举None或一个入父，再只保root0连通的active边，丢弃其他父组件；每棵合法根树都被覆盖，同一树可能由多个孤立父选择重复产生。它不是对任意非法图的完整输入验证器，当前构造域为非空有限简单DAG、root0、非负整数需求且零需求只能原终端。

`graft`在修改前一次性记录outer的**原零需求终端**，每处识别一个inner根并复制其余顶点，改接口需求、加独立内部边，不继续替换新生成的终端。不同副本私有，大小恰|G|+z_G(|H|−1)。

`all_small`枚举按编号u<v的n1/2/3全部边子集、需求0/1/2，剔除零需求出边。各n生成3/15/135图，共153；允许正需求死端、不可达点和零需求根。先独立求各值，再遍历全部153²有序图对，只对替换后**总顶点≤6**者检查b*(G∘H)=min(b*(G),b*(H))，冻结实际21384对。这里并未枚举全部六点DAG，也未逐终端选择不同H_z或枚举任意组合表达式。

一般恒等式仍依根树的拼接/投影证明，而不是这些计数。`matching_size`另对给定三元组枚举所有边子集，核每坐标互异，当前只用于四边parity的最大匹配1。

## 唯一fixture的全部内容与读取边界

JSON声明coordinate_size2、pool_clone_factor2，原边为

\[
A=\{000,011,101,110\}\subset\{0,1\}^3.
\]

四条pool双复制见证（元素写成原坐标下标和克隆下标）是

\[
(0_0,0_0,0_0),\ (0_1,1_0,1_0),\
(1_0,0_1,1_1),\ (1_1,1_1,0_1).
\]

每条投影回A，每坐标恰用(0,0),(0,1),(1,0),(1,1)四元素各一次。JSON另保存张量平方公式x=(a,b)、y=(b,a+b)、z=(a+b,a)，加法在F₂，以及“完整pool/直接张量不保NO、非hardness”的scope。

规范脚本实际读取`triples`及`pool_double_matching`，q2/r2由程序固定；coordinate_size、clone_factor、description、公式串和scope是该固定原件的说明，不是被程序解析执行的通用schema参数。pool检查核原坐标投影属于A及各坐标克隆对集合大小4；本文件本身确实恰四行、标签0/1正确，不能据固定文件检查宣称任意JSON的维数/标签/重数验证均已实现。

代码以`Path(__file__).resolve().parents[3]`定位repo，再取`examples/unrelated_machines/parity_3dm_repetition.json`；没有CLI输入参数。证据保存完整tests/audits/unrelated_machines与examples相对结构，保证唯一数据依赖仍存在。独立两个程序不读该JSON，自己写出相同四原边。

## 原parity的实际11机13件token矩阵

`rooted_3dm(A,2)`造root0需求2，X节点1/2需求1，四三元组节点3…6需求2，Y节点7/8和Z节点9/10需求0。边为root→X、X→相应三元组、三元组→其Y/Z。父选择oracle真实得到b*=1/2。

`token_jobs`先加root unit，每正需求v生成min(k_v,outdegree(v))件本地1/k_v、所有孩子端1的任务；不足k_v时另加本地填充1−count/k_v。实际本例无填充。以下完整稀疏矩阵按**原任务标签**列出，未列端全部不可用：

| 任务j | 全部有限端及时间 |
|---|---|
| 0 | 0:1 |
| 1,2 | 0:1/2，1:1，2:1 |
| 3 | 1:1，3:1，4:1 |
| 4 | 2:1，5:1，6:1 |
| 5,6 | 3:1/2，7:1，9:1 |
| 7,8 | 4:1/2，8:1，10:1 |
| 9,10 | 5:1/2，7:1，10:1 |
| 11,12 | 6:1/2，8:1，9:1 |

`schedule_feasible`是原任务分配的递归可行性oracle，不读树值或匹配解：按(资格端数,−最大时间)稳定排序任务，在部分负载加新件≤bound时才递归；非负性保证超容量剪枝合法，首份成功就返回。assignment仍按原j存储。它不枚举所有成功分配，返回的calls统计**含内部节点的递归调用数**。

冻结bound1不可行（514调用）、bound3/2可行（14调用）。所有有限加工时间均为半整数，实际峰在(1/2)Z上，故不存在峰严格介于1和3/2的调度；两查询加这个格点事实给本例真实OPT3/2，而非只证某份坏调度。成功原标签序列为

`[0,0,1,3,2,3,7,4,4,5,5,6,6]`，

逐原矩阵相加得到`[3/2,1,1,3/2,1,1,1,1,0,0,0]`。这只证这一固定token实例；一般OPT=2−b*桥梁由已有正文承担。514/14不是全机器标签分配数，更不是一般多项式求解器复杂度。

## 规范全次张量的有限执行与一般证明

`tensor_map`对偶长度按二维块B₂(a,b)=(b,a+b)，奇长度先用三维块B₃(a,b,c)=(b,c,a+b)再用二维块；main只调用t2…10。逐x∈F₂^t产生y=Bx、z=x+y，逐位核三元组属于A，三个坐标集合各有2^t不同向量，冻结匹配大小4/8/16/32/64/128/256/512/1024。

所有t≥2的结论由B₂、B₃及I+B的可逆分块证明承担，不从十个以内的执行外推；没有引入一致性测试或声称其他张量操作保NO。这个3DM坐标张量亦不是实际加工矩阵的Kronecker积。

## 独立graft/gate：同为父选择，依赖拓扑编号

[独立graft源码](../../tools/evidence/private-audits/original/tests/audits/unrelated_machines/private_graft_independent.py)开头虽写edge-subset，实际`optimum`仍是**父选择穷举**；其独立性是另行实现、不导入规范函数，不是另一种已实现边子集oracle。它只按v1…n−1单次向前更新active，因此要求输入拓扑编号；base的u<v、gate的偏移编号保此条件，`substitute`另用`topo`分批排序ready点、重标并断言root0先行。

需求集是{0,1,2,7,2^60}，相同零端约束的n1/2/3图有5/45/765，共815。tiny为n1/2共50图，2500有序替换对全覆盖；再用seed20261017有放回抽2000个base图对，合4500。每个终端仍接同一h，不是对全部异质H_z穷举。

**这里没有规范程序的6点cap。** 静态公式可生成最多3+3(3−1)=9点的替换图，程序没有对该随机族筛至6点；报告未另记实际最大，本批不为补这一统计重跑。另2000次gate取0…3个base模块、正根需求在{1,2,3,7,2^60}中抽，静态最多10点，检查max_s min(1,s/k,β_(s))，含空模块正需求死根。2^60只作整数/有理评分，不按需求数值展开任务；不能据此给一般输入复杂度证明。

程序还确切检查：两个各值1私有模块加需求2根得1，而合并其叶为共享资源后值1/2；共享图自替换仍1/2、不是1/4。这分别攻击私有性前提及乘法放大误用，一般恒等式仍由证明承担。

旧[有限审查](../审查/私有需求组合与完整复制有限审计--审查.md)把独立替换也描述成最多6点，应据这份代码改读为以上4500具体生成族/静态上界，不能把规范的筛选移植过去；本批不修改旧owner文件。

## 独立pool：两种确切有限判定及4边见证

[独立pool源码](../../tools/evidence/private-audits/original/tests/audits/unrelated_machines/resource_pool_independent.py)的`perfect(q,E)`按第一坐标x依次选一边，用(y-mask,z-mask)记忆DFS禁止重复；选完q个x即为完美匹配。`denominator_matching(q,E,r)`独立枚举每原边n_e∈{0,…,r}，检查每个原元素总次数r。上界r不遗漏见证，因为每条边已占用其各元素总预算r。

`pool`把原边(x,y,z)扩成全部(xr+i,yr+j,zr+k)，i/j/k独立取0…r−1；`tensor`另取每对原边a,b，编码(q a_x+b_x,q a_y+b_y,q a_z+b_z)。前者是完整克隆池，后者为坐标平方，不能混成一种复制。

main枚举{0,1}³全部8边的256支持（含空支持），各r1/2/3，共768组，比较`perfect(2r,pool)==denominator_matching(2,E,r)`。没有测试任意q、二进制巨大r或全部低负载调度；一般分母等价由元素多重出现标号证明承担。

固定parity另核原关系无完美匹配、双pool和平方关系均有完美匹配。其平方显式见证为

\[
(0,0,0),\ (1,3,2),\ (2,1,3),\ (3,2,1),
\]

即JSON公式的四个(a,b)。它恰有**4条匹配边**，而`tensor_square_edges=16`是整个平方**输入关系**的边数；`pool_edges=32`也是整个双pool关系的边数。旧有限审查的“平方见证使用16条边”不能按匹配大小读取。JSON的pool见证若数值编码为000/122/213/331，是另一份操作见证；不与平方000/132/213/321强行合并。

## 历史实际输出、源码身份与本批自查

[完整冻结报告](../../tools/evidence/private-audits/original/evidence/runs/unrelated_machines/private_graft_repetition_audit.json)保base_commit `00f181f0b3767047edd014d8bd60061e56f2f178`（历史生成定位，不是当前清洗claim）、canonical/independent_graft_gate/independent_pool三个完整输出对象，及Python3.12.14、三规范命令和精确算术说明。本批完整读取并按下表核当前源：

| 原件 | 冻结SHA256 |
|---|---|
| canonical | `a538217b275a362d3ab8fef9cb0d6925b8778380136c13d3f5b97f5d16e55065` |
| independent_graft | `8e185af99510f75fcf416349adfca2376ca6414e3ba22bba8d939f82cc2fa626` |
| independent_pool | `0f1e1e3aee5baa75cd66509ffef5f0b30cb435cf0c6b0b16f188a2b6c5245c32` |
| fixture | `94f4d9edd13c74328ef7bcefcb19dd507139d92af5c2a007c9c755c14396f092` |

全部同hash，报告有各自all_passed及真实范围；本批复用既有完整输出，**没有重跑三程序**。原相关正文/审查记录历史实际执行与规范补审，不能写成本批新盲审或新运行。代码assert、固定输入、精确原任务见证和一般证明分层记录；[核验JSON](../../tools/evidence/private-audits/verification.json)保存这些具体映射及数据依赖。

可复用的是有限父选择实现、完整四边输入、原token矩阵和复制见证、明确的私有/共享失败机制。没有由这些程序得到一般UM近二算法或反面、NP/ETH下界、其他复制保真、外审或全球新颖性；已有完整证明及后续整数一致性/统一decoder义务保原身份。

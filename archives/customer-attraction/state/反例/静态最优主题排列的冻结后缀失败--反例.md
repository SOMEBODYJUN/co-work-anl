---
id: "customer-attraction/frozen-suffix-optimal-topic-assignment-counterexample"
kind: "counterexample"
type_tag: "反例"
title: "冻结终局后缀的最优主题排列预算反例"
status: "complete"
truth_status: "static-assignment-bridge-refuted-half-open"
review_level: "full-seven-source-read-frozen-exact-report-and-policy-reconstructed"
scope: "三名提供者、六主题、1953单位客户的完整有序历史纯SPE；仅反驳冻结z的最优主题排列接口"
summary: "唯一最优主题支持{1,2,5}的六种排列中，静态删去实际主题后的收益和最小为1736，而真实终局福利W=1735；2W−OPT=1730，故非half反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md#1-exact-candidate-that-fails"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md"
---

# 冻结终局后缀的最优主题排列预算反例

## 反驳对象和模型

采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、共同有限目录、三名单位提供者、全部有序历史纯SPE、任意重复动作与离轨平局。对一份完整SPE的实际终局 $z=(S_1,S_2,S_3)$，冻结终局并删去原玩家i后，静态替代主题T的收益是

$$f_i(T;z)=\sum_{x\in T}\frac1{1+c_x(z)-\mathbf1_{x\in S_i}}.$$

被否定的精确接口是：对每个实例和每个完整SPE终局，存在一个最优三主题元组 $(T_1,T_2,T_3)$ 及排列π，使

$$\sum_i f_i(T_{\pi(i)};z)\le W(z).\tag{A}
$$

它冻结原终局的其他玩家负载，再把最优主题分派给删去不同实际玩家的三列。接口若成立，可与通常静态覆盖收费结合推出half；本例只否定(A)，不把真正改变后缀的偏离替换成冻结查询。

## 单位客户输入、Möbius偏置和完整策略

主题为0,…,5。原输入由63个非空兴趣类型的整数重数给出，最小类型重数1、最大61，总客户1953；完整原字节见 [assignment_instance.json](../../tools/evidence/dynamic-exchange/original/assignment_instance.json)。它来自一个整数Boolean潜势F的M1 Möbius变换：先给13个非零F值，再令 $c_A,z_A,x_B$ 为两次普通子集反演，最后每个类型取 $r_B=x_B+31$。已读原稿给

$$\min_Bx_B=-30,\quad\max_Bx_B=30,\quad\sum_Bx_B=0,\quad\sum_B|x_B|=456.$$

因此所有单位客户重数正。三种不同主题终局中，统一偏置贡献

$$\beta=31(2^6-2^3)/3=1736/3,$$

而F的边际决定有符号差异。该构造仅使用正整数单位客户，未把signed customer当模型对象。

完整策略根选0；第二动作按首动作 $(0,1,2,3,4,5)\mapsto(3,2,4,0,5,0)$；最后动作表逐一给出全部36个有序二历史，包括六个重复对角历史。保存的 [assignment_full_policy.json](../../tools/evidence/dynamic-exchange/original/assignment_full_policy.json)含43个策略行。

实际路径为 $(0,3,4)$，因为 $F(034)=F(03)=F(04)=0,F(34)=1$，收益

$$u=(1733/3,1736/3,1736/3),\qquad W=1735.$$

每个完整历史的可信性不是从偏置M2充分条件直接继承：原稿先逐项核查固定K=31。偏置斜率分类为0、16/3、32/3，258比较中186、66、6项，正斜率最大阈值仅5/16；因此K=31使所有真实偏离不增，最小SPE slack为0。重复历史也在策略表和审计中包括。

## 唯一最优支持和静态排列成本

对任意三不同主题支持S，覆盖值可写

$$W(S)=1736+3F(S)-\sum_{a\in S}F(S\setminus\{a\}).$$

二十个三元支持的F修正中，唯一最大的是 $S^*=\{1,2,5\}$，修正值4，故

$$\boxed{OPT_3=1740},$$

且不存在另一个最优支持可逃避后面的排列成本。实际支持 $(0,3,4)$ 与S*不相交，所以三列静态查询都获得同一偏置β。去掉β后的收益矩阵（行是实际玩家，列按1,2,5）为

$$M=\begin{pmatrix}0&-1&0\\1&0&1\\0&0&0\end{pmatrix}.$$
$$\min_{\pi}\sum_i(\beta+M_{i,\pi(i)})=3\beta=1736.$$

排列$(1,2,5)$等有六种，原冻结报告逐项给成本1736、1737或1736；最小严格为

$$\boxed{\min_\pi\sum_if_i(T_{\pi(i)};z)=1736=W+1.}$$

因此所有最优主题元组的排列都失败，不能通过换另一份最优支持修复(A)。但

$$2W-OPT_3=3470-1740=1730>0,$$

本例远非half反例。

## 为什么真实分支没有被静态矩阵捕捉

冻结实际后缀(3,4)时，根查询主题1、5的有符号收益为0；真实根偏离到1或5时，第二玩家改变后缀到(2,0)或(0,2)，根有符号收益为−1。相反，在实际第二节点，静态主题1、5各有有符号溢价+1，而沿其真实改变后缀的收益为−1。玩家1若使用唯一负项主题2，玩家2必在主题1或5上承担+1；故所有排列总和仍多出一单位。

这正是(A)把“删去玩家后沿冻结z查询”与“当前行动后按同一完整策略真实续局”混为一谈的量词错位。它不否定真实改变后缀的ROW、响应债务、聚合安全值或半覆盖证明，只说明一个静态终局分派模板不能替代那些动态对象。

## 证据身份、已完成范围和接续

原[assignment_exact_audit.json](../../tools/evidence/dynamic-exchange/original/assignment_exact_audit.json)记录 `exact complete-history counterexample to static optimal-tuple assignment bridge only`：fresh历史43/258比较、客户1953、K=31、唯一最优支持、六排列成本和half_margin1730。原README明确发现Möbius compiler作为偏置来源；该依赖不是本7源，不在本批重复认领。

`assignment_witness.json`、发现MILP和简化脚本不在本批领取范围，故本轮没有声称重跑作者代码；冻结实例、策略、报告已全文读取并逐字段对照。原内部盲审/父代理单位复核在原文中被描述，本轮不改称外部同行评审或新颖性认证。

下一步若要证明half，必须使用真实变化的续局、跨节点支付或另一个全局机制；本例只关闭(A)，不提供Q-CAG-HALF反例。

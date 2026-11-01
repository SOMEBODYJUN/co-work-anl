---
id: customer-attraction/terminal-load-tail-original-fraction-audit
kind: resource
type_tag: 资源
title: 末位负载尾和的原Fraction审计与抽证边界
status: retained-original-program-and-complete-record; no-new-execution
truth_status: historical-finite-exact-audit-report; universal-bounds-have-separate-analytic-proof
review_level: all-three-primary-files-read; actual-code-contract-and-complete-report-compared
scope: m至多12的单客户位串及信用类型，60个m至多5硬编码单位客户游戏，原307个有序SPE终局与11份抽选完整证书的聚合报告
summary: 完整保存原6714B审计与4054B输出；逐项区分单客户排列、信用代数、终局全集及全树抽证，纠正两处代码注释超过实际输入或抽样控制流的表述。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c93f7ed9e4794dc29b320fe10e5bfe40/terminal_geometry/audit_terminal_load_rank.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c93f7ed9e4794dc29b320fe10e5bfe40/terminal_geometry/load_rank_audit.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c93f7ed9e4794dc29b320fe10e5bfe40/terminal_geometry/audit_terminal_load_rank.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-c93f7ed9e4794dc29b320fe10e5bfe40/terminal_geometry/load_rank_audit.json
---

本资源对应[末位负载尾和与最优覆盖主题数定理](../定理/末位实际主题的负载尾和与最优覆盖主题数--定理.md)。原文件名rank指最少最优覆盖主题数，不是线性代数秩。原稿自称个人候选并将解析证明、有限审计分开；本次全读三原17179B并解析重构，未运行原main、导入原模块、重算Fraction断言、BI/SPE、全树校验器或优化器。原输出status=passed是历史字段，不是本次PASS、独立实现、盲审或外审。

## 原字节、实现依赖与输出合同

|原ID|文件|字节|SHA-256|
|---|---|---:|---|
|32875f5b80398ce1d5eb|audit_terminal_load_rank.py|6714|5d7fbec4b7b23e2ac3204eb4162dafd53f66a46863638bbaf9ce4d72bcf33ace|
|0ab6bf8a3b0be715dd32|load_rank_audit.json|4054|0a0e47deb9df67c074f997419501373af496761649382ba59f3585b6ecba92f7|
|6aacaaab21a3713fc1c5|terminal_load_rank.md|6411|94a1305b1445b2788ff0c86184b4f42a72b8407d8fd5c35eaaef35470c38aaa0|

三件原始文件及各normal-show捕获均在[本资源证据包](../../tools/evidence/terminal-load-rank-proof-and-original-audit-three-primary/README.md)；完整原路径和双冻结提交保留于actual-source-manifest.json。6714程序仅用标准库Fraction、itertools、pathlib、json、sys，加规范customer_attraction模块。原ROOT=文件路径parents[5]，sys.path插入ROOT后导入Instance、CustomerType、ExactSPESolver、verify_certificate，包初始化还导入规范各模块；这些实际依赖四文件共25475B，当前同SHA在仓库，先前已全文读，不重复取源或执行：

|规范依赖|字节|SHA-256|
|---|---:|---|
|__init__.py|691|284282dfb35d5612734b979d691d57be9808c07a03857b533248eb2cbd5079ca|
|model.py|8640|ac28fc1a3837954ab9b8fc658701f53aecf0a1da059e316158aab7565dc5f6a8|
|exact.py|9943|a4c76d77fd6c8d18ac668ce2070a65f927d9dca6bbe3cdd36f467d1598b4a892|
|certificate.py|6201|a269b532260b537e67879eba609ef23e046e8f7303458ecf11271c4673aecc45|

[有序终局全集算法](../算法/完整历史纯SPE终局全集--算法.md)枚举可实现有序终局，保留离轨选择，不等于枚举每一份完整策略；给定on_path可重构一份实现该路径的完整策略。[规范精确求解与验证](../计算/完整历史求解器的精确复现--计算.md)是这里的实现基础，历史原审计没有变成第二个独立实现。

程序无CLI参数、无外部JSON输入，三个audit函数都在main中执行，受__main__保护。输出路径固定为代码同目录load_rank_audit.json，以indent=2、单LF覆盖写入；stdout只去掉per_load_minima，其余摘要保留。原目录结构影响导入；单独复制脚本不能据此假定可直接运行。现存JSON没有进程命令、环境版本、stdout/stderr、时间戳、返回码或完整证书，故不补造一次当前可重演通过事件。

## 单客户位串与信用代数的实际穷举域

audit_customer_patterns对m=1,…,12枚举全部长度m−1二元prior，末位追加1；共4095个单客户会员串。tail逐位置精确计算Σ1/(过去会员数+m−i)，phi按(c−1)/m+Hₘ−H_{c−1}定义。断言依次是tail≥phi≥Hₘ/c、1≤phi≤m/c；按最终负载c存最小值，并核前c−1位加末位的early串达到该最小值。这不是4095个客户游戏或4095份SPE。

audit_credit对m=1,…,12、h=0,…,m−1及b,o∈{0,1}枚举312个类型，p=1_{h>0}、u=b/(h+1)。它核

\[
\frac{op}{h+1}+p(1-o)+b(1-p)-\frac b{h+1}
=\frac{p(1-b)o}{h+1}+p(1-o)(1-b)+\frac{pb(1-o)h}{h+1}
\ge\frac{p(1-b)}m.
\]

这里p、b、o仅记录是否过去覆盖、是否末位覆盖、是否最优覆盖；对应定理F(O)展开与粗信用，不是312份策略认证。

以下完整保留报告per_load_minima的12行78个精确分数，每行按c=1,…,m排列。它们是原记录的原值，未由新checker重算。

|m|φₘ(1),…,φₘ(m)|
|---:|---|
|1|1|
|2|3/2, 1|
|3|11/6, 7/6, 1|
|4|25/12, 4/3, 13/12, 1|
|5|137/60, 89/60, 71/60, 21/20, 1|
|6|49/20, 97/60, 77/60, 67/60, 31/30, 1|
|7|363/140, 243/140, 193/140, 499/420, 227/210, 43/42, 1|
|8|761/280, 129/70, 411/280, 529/420, 953/840, 89/84, 57/56, 1|
|9|7129/2520, 4889/2520, 1303/840, 3349/2520, 2999/2520, 185/168, 527/504, 73/72, 1|
|10|7381/2520, 5113/2520, 821/504, 3517/2520, 3139/2520, 2887/2520, 2719/2520, 373/360, 91/90, 1|
|11|83711/27720, 58511/27720, 47171/27720, 40451/27720, 36041/27720, 33017/27720, 30917/27720, 4211/3960, 1019/990, 111/110, 1|
|12|86021/27720, 60611/27720, 49061/27720, 42131/27720, 37511/27720, 34277/27720, 31967/27720, 4331/3960, 2083/1980, 169/165, 133/132, 1|

## 60个真实硬编码客户游戏与307条有序终局

signatures的每个集合是一个客户兴趣型，即该类型喜欢的标签下标，不能反过来当成主题客户集。m=1,…,5，family_index=0,…,3，weight_seed=1,…,3，共60个游戏。族内第j型有1+(j·seed mod4)个单位客户；主题数为兴趣下标最大值+2，最后一个标签恰为空。四族全字面如下。

|family|按j排列的客户兴趣型|标签数|各非空标签所含客户型下标|
|---:|---|---:|---|
|0|{0}; {1}|3|0:{0}; 1:{1}|
|1|{0}; {1}; {2}|4|0:{0}; 1:{1}; 2:{2}|
|2|{0,1}; {0,2}; {1,2}|4|0:{0,1}; 1:{0,2}; 2:{1,2}|
|3|{0,1,3}; {0,2}; {1,2}; {0}|5|0:{0,1,3}; 1:{0,2}; 2:{1,2}; 3:{0}|

所有重数正，所以每族的覆盖列签名确实互异，且各有一个空标签。实际样本包含不交、相交极大主题和严格子主题，**并未实现代码注释所称的不同标签同覆盖**。一般定理的解析证明允许同覆盖标签；不能把这点改写为本有限报告已抽查别名目录。

optimal_support先精确算OPT，再从k=1到min(m,标签数)搜索不同标签组合，取首个达到OPT者；这是跨最优支持的最小k，字典顺序只选其中一个。60个输入均非零，其函数无单列零客户分支，不代表普遍定理排除零客户。

每个游戏调用ordered_outcomes()；对每条可实现有序SPE路径，以实际标签和型重数直接计算u、W、各qᵢ、φ总和、F(O)、B大小，断言uᵢ≥qᵢ≥u/rᵢ、W≥Σqᵢ≥Σφ≥Hₘu、OPT−W≤(k−1)u−F、F≥(W−|B|)/m，并在k−1≤Hₘ时核half。原报告合计307条有序路径，保留全历史SPE可实现性；不是307份不同全策略，也不是对任意目录的有限穷尽。

## 抽选完整策略证书及报告缺项

实际代码在全局paths计数尚未加一时检查paths % 29 == 0，故依跨全部游戏的有序路径序号0、29、58、…抽证。注释“one path per count state”不符合这段控制流；没有按终局计数状态各抽一份的逻辑。原307路径与11证书数符合这一全局抽取规则，但报告未列这些序号对应的全部实例和路径，不补造其身份。

选中时solver.certificate(on_path=history)重构完整树，verify_certificate.assert_valid核该完整策略的所有合法有序历史及偏离。canonical checked_deviations不计self；有序历史、重复动作和离轨平局均由其完整合同保留。原记录为：

|字段|原值|范围|
|---|---:|---|
|status|passed|历史原字段|
|customer_patterns|4095|单客户末位为1的全部m≤12位串|
|credit_type_checks|312|m≤12的信用类型代数|
|games|60|上述确定输入|
|ordered_spe_paths|307|这些游戏的可实现有序终局|
|full_certificates|11|全局每29路径抽取|
|all_history_checks|2464|11份完整证书的历史计数总和|
|all_deviation_checks|8057|相应非self偏离计数总和|

scope原文为“finite exact audit, not general theorem proof”。原JSON没有序列化11份完整策略、307路径、各游戏客户表、逐行IC或slack。硬编码可说明设计输入域，聚合输出不能替这些未保存的逐证书材料。现在已有充分原成功证据不机械重跑；此清洗仅准确保留其历史层级。

tight条件是welfare==Σφ，输出只截全枚举遇到的前12个。全部如下，history用原零起始标签下标；同family与seed的平局路径分别保留。

|m|family|seed|history|u|
|---:|---:|---:|---|---|
|1|0|1|[1]|2|
|1|0|2|[1]|3|
|1|0|3|[1]|4|
|1|1|1|[2]|3|
|1|1|2|[1]|3|
|1|1|3|[1]|4|
|1|2|1|[2]|5|
|1|2|2|[2]|4|
|1|2|2|[0]|4|
|1|2|3|[2]|7|
|1|3|1|[0]|7|
|1|3|2|[0]|7|

这个前缀恰全为m=1，不证明m>1的全局SPE同时达到单客户极小尾和；也不是Hₘu等号样本的专门列表。未保存的其余tight项不补猜。

## 关系与证据用途

6714原码实现单客户式、信用类型和有限完整SPE必要条件；4054记录提供历史有限支持；6411原稿提供一般解析论证，新定理逐式自足承接L1–L12。原末位信用仅需末位BR，整路径φ付款需各实际位置IC；不将两种条件互换。现已发表的鲁棒乘积式可用κ≤k给相关half子域，但不替代φ、客户负载或F(O)的独有证明。至多三极大主题定理、一般五人half与本覆盖数条件的关系均在新定理中精确说明。

获取的17YR原claim为pushed，local_sync的needs-attention原样保留，独立恢复核证1个untracked同字节、tracked空、无missing/different/unmerged且stash保留；未改写为synced。字段、原字节、JSON、格式和链接检查仅为包自查，不称新Fraction/SPE审计。Root先实际checkpoint本正文和必要原件证据，再单独登记本三源done；不由原passed推断一般六人half或全仓完成。

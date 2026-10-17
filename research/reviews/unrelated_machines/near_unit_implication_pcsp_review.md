# 近单位蕴含 PCSP：陈述先行、精确minion及物理范围审查

对象：[现行正文](../../current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md)的两个精确ID。一般源NP-hardness已证明；本记录没有把它升级为实际UM makespan困难性。

## 实际冻结顺序

原构造者先给necessary fixing/一般hardness的statement SHA256 `4512779369d2bbefb6c53ae1f053e3beaed936e1973b157c9e451ebcf55dbeab`，一位审查者仅据陈述独立重构，冻结SHA256 `e3328100b9678c2a1753cc190814e04deed126e4e12ec87601c9b4a65f9f48a4`。其亲读BBKO v3 PDF33的Def5.16/Prop5.17并截图核对，不据搜索摘要导入。

之后才读冻结proof SHA256 `bfb63d258aca04204a95e6ab8c8c256de640997ba33cffaa24eda246639eab3e`及新iff充分性addendum SHA256 `12b6f60a484992766f006a51a750a9b3c1e50c3c9f2049e37651c31c9938b0fe`，分别核必要性/hardness与新增充分性；读后稿SHA256 `46a2f139f78fe2433ab2f3123754a20f099173c376ad45dfb51830b83ad7efbf`。新增iff当时只发生读后攻击，不虚称也曾先陈述独立审。

为了把iff作为独立精确ID再核一次，root另冻结只含两个精确陈述的SHA256 `cdf17889103ed461914ed72ecac723551eba789782613ee87819a84161c31d63`。另一审查者未读上述任何proofnotes，只据此重构iff/strongfixing/hardness，冻结SHA256 `a8603d347aa377e106d0fcdff3dab6855eb9d993f1105acf5e5adfc1371b4d6b`；实际读原始BBKO同页定理。

随后该审查者全文读root独立重写canonical SHA256 `447336832f9aaef221857a491bcfe279b1e1436658eb57aa078c5195960d4e6d`，读后稿SHA256 `d2fffbe86c2671dd6abbcb858ea3f94ace8285dcd8aefd0b46c24e4591dc95e7`。两个ID无standing fatal；§4只审自足三坐标公式，未冒自己亲读Feder/KKR原件。root亲自读取BBKO和KKR原PDF相关页、Feder作者PS转读文本印8–11，原PS字节原样保留。

这些scratch哈希固定实际读取顺序；全部承重证明已经重写在现行正文，不要求读者找scratch稿替代证明。

## 具体攻击及边界

- AMO对S,T包括同一个集合本身，空集winning被排除；ONE保证非空，minimal winner真实存在。没有constant函数漏入。
- 单调性可直接由incoming X⊆Y、k列全部Y的strict矩阵证明；不需要循环引用minimal winner已是fixing。
- singleton deletion矩阵每active row至多缺1，输出却仅r−1个1；审查者另用min(k,|S|)个非空块删除独立重构，结论一致。没有假定全部rows active。
- 充分性必须在incoming support中取minimal winning S，只控制这些active rows；缺S元素的输出列至多|S|，并集上界即够，未要求缺失列互异。
- 同一个S全1由单调迫1，全0由相交性迫0，因此准确满足strong C-fixing。C=k−r固定且正，identity minion homomorphism合法。BBKO v3 Prop5.17而非旧版编号或v3 Prop5.15的bounded-essential theorem。
- x1 AND OR其余的函数族在n≥2有所有n个essential坐标；用bounded essential arity替代strong fixing会是错误证明。
- PCSP仅NP-hard，不把promise语言偷写NP-complete。k,r固定的有限模板规模与所有输入多项式量词明确。
- 物理三型关系按“small job是否离开本机”“unit job是否到达本机”分别反算：out–in EQ、in–in NEQ、out–out NEQ；不提供out–out EQ。端口有限数不等于源变量可随意复用。
- 负载grid核对：若一个实际编译保持{1,1/k}且NO无C≤2−r/k，才可推NO≥2−(r−1)/k及ratio2−(r+1)/(k+1)。r2任意大k若有**physical**hardness才足够主反面；这个compiler保留为OPEN，没有由一般hardness删除条件。

## Ordinary source与适用条件

Feder Theorem3先在ordinary setting取得clauses，Theorem4最小support/三坐标投影并不控制weak support。root亲核相应原文字节及印8–11；KKR v6 Theorem7只对普通CSP/edgeCSP，含两unary constants、普通CSP NP-hard及某non-delta关系。未找到可直接导入的promise typed版不是不存在该定理的证明。

自足投影公式已独立核：pin一个out0、量化k−3个out，则strict b⇒y=z=1，weak b⇒y+z≥max(0,r−k+3)。r≤k−3时weak完整cube，所以该普通提取步骤不能原样做near2 soundness。它不否定更大gadget或一般UM允许的循环/多尺度设计。

## 实现与认证状态

本包没有新生产代码或冻结有限计算，不以scratch小真值表替代一般证明。源原件分别为BBKO v3 73页、KKR v6 33页、Feder作者PS 12页；原字节/hash、来源和实际读取范围入manifest。没有声称BBKO PCP全证明、KKR算法全证明或Feder全篇已经重构。外审、新颖性、UM物理编译仍未认证。

最终canonical在上述实读版本之后仅把无界essential例子明确为n≥2，并在物理范围补native多端任务的one-hot/one-cold精确状态，强调两端Boolean/DAG不是主目标限制。核心两个Claim的对象、矩阵证明及hardness依赖未改；额外scope不冒称已完成新compiler。

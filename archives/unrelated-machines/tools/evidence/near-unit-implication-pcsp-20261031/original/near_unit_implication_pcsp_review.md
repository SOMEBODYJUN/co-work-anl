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

第2–3节两个一般PCSP Claim没有新生产代码或冻结有限计算，不以scratch小真值表替代一般证明。源原件分别为BBKO v3 73页、KKR v6 33页、Feder作者PS 12页；原字节/hash、来源和实际读取范围入manifest。没有声称BBKO PCP全证明、KKR算法全证明或Feder全篇已经重构。外审、新颖性、UM物理编译仍未认证。

最终canonical在上述实读版本之后仅把无界essential例子明确为n≥2，并在物理范围补native多端任务的one-hot/one-cold精确状态，强调两端Boolean/DAG不是主目标限制。核心两个Claim的对象、矩阵证明及hardness依赖未改；额外scope不冒称已完成新compiler。

## Native 流边界与全输入正规形的新增实际审查

最终旧scope稿SHA `6a86f38827e59c84cc5e2c8c89778614e4fae61e5616e462ccc22972186821a1`后来另由一名研究者全文实读，冻结读后稿SHA `a36af57ce54dfe4cdc6b67838a1442073f61c001eef7fbb827db7d474da0eab8`。三型、native one-cold、非DAG范围及grid公式无fatal；其只建议明确unit机器A与small机器M_i互异，正文已澄清。

新增 `UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1` 的仅陈述SHA `c96b39f9e8057edd1e621f6c2efa940e42a271d70ce9675982b6b541f95b17ff`；独立研究者在未读任何构造proof时重构B/F两流、unknownOPT五三、balanced strict iff，冻结SHA `2f755be886cc77e81e64468968c10099776202ee7fc0c39a6ee9ce6a4b06e843`。随后才实读root自写§6的canonical SHA `09496d273a71adf5644814100fc161602cc3a43c6d79107bfe829afd7c78d666`，读后稿SHA `40767446d0b81265199270705a2d1c3b5d0afc153d6de846d2336c4a804f9558`。新增局部rho必要形状此前Statement无，明确仅做读后核查；审者又从rho≤a+b/2独立加强one-small下界到k−2r+1，正文r2改为k−3。没有新native-flow软件实现。

root原先草拟的带r→2r损失的多small消去，在陈述先行攻击中被更强exact选择器支配；旧冻结草稿保留scratch，未注册为本次canonical Claim，不把废弃路线加进证明依赖。

`UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1` 与 `UM-TARGET-TERNARY-SELECTOR-EQUIVALENCE-v1` 的真正仅陈述SHA `cbebbbface83e98cbbdce49c7a7d772a5bcd876fd7c5d03ffcd1fbcf62268176`。一名研究者未读root/row/pcsp任何新证明，独立构出二叉单位树、完整两向实际映射、unknownOPT尺度搜索，冻结SHA `711143edbe0e7681e4c5e4d3fa5ddcf5f213ccfa31de6677e66162d7fa897e9f`。另一名研究者此前仅据较弱Statement独立构出线性路径容量OR构件，稿SHA `ab48b6a9149afbdea7fb6f81ba7ddbf814cb02eac642ad7e42250f583f1a4181`；不把这份旧Statement审查冒称新两个Exact ID的完整盲审。

随后第一名审者实际全文读root canonical SHA `c1f95ee830f09ced1c4840f2177748e8d95e4b7bc2b403efff198ff3734a9a50`，读后稿SHA `2e27367948ab6e07c816ba959a89122778ad113f65983a175778ee0ef229f496`。§7–8无standing fatal；新(7.1)截断恒等式此前Exact无，仅记本次读后核；n0单列、p0/d1、严格C<2b、OPT=b及2b、全私有2b上界、剪枝范围、全机非负子集负载、dense/sparse编码与有理尺度数均实际核。没有从一般PCSP困难性导入物理hardness。此后正文只补规范代码/冻结审计链接，不更改这些数学对象/结论。

## 正规形软件的实际范围

规范 `tests/audits/unrelated_machines/ternary_unit_selector_normal_form.py` SHA `29120eaf7038fc1a79ee7e563243c986059ca32554109a242b20a92472c46bfc` 实现transform/forward/project与非空截断值的有限核验；负载按非零machine字典表示，避免稀疏API在空任务或大unused m时枚举机器数。初版稠密原型保留scratch，没有把它的冻结run覆盖后冒称新run。最终独立冻结 `ternary_unit_selector_normal_form_sparse_audit.json` SHA `959b78a30645da7f11583ec70ed871395a98cd5a29d485d31dcb58857d37985f`。

root实际全文读初版、再逐项读sparse差异，独立重跑最终规范文件，输出JSON每一字段与冻结文件相同：9个关键原输入、13原σ、116新完整τ，其中29份C<2b逐件投影并核逐原机负载不增；6021位十进制/20001bit分母、m=2^80的empty及few-edge、q0、d1、b7/5、OPT跨b/2b、p>b/负值/b0/C=2b拒绝均覆盖。有限运行不承担数学一般证明。

没有实现假设的normal-class次二求解器或一般UM新算法；native F/B完整流软件与一般PCSP求解器也未提供。proof/internal-review/implementation分别记录，外审与全球新颖性仍未认证。

---
id: cag-eight-customer-iid-original-quadratic-bases-and-complete-policy-contracts
kind: resource
type_tag: 资源
title: 八客户iid原审计的两种二次域与完整策略合同
status: 三原件6274B完整实读；完整22claim/本6ownerSHA核真；强iid两原入口0、旧充分成功复用
summary: 同一八客户完整SPE和静态iid Nash在Q(sqrt669)与Q[s]中的两种实现逐式对齐；父固定区间符号器的实际域、作者浮点展示及12个静态约束保真。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/security/iid_nash_bridge_audit.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/parent/audit_iid_bridge_independent.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d321c149379b425493c5e8a5e03c6f39/parent/iid_bridge_independent_audit.json
---

三份原件6274B逐size、SHA256和blob核真，全部全文读取。它们是在[八客户强iid反例](../反例/独立同分布福利支付--反例.md)上两套不同代数实现，不是两个新游戏或两次新增外审。[KN来源资源](对称iid福利闭包与最低收益有限锥的来源合同--资源.md)已保r/s换基、CCE闭包和状态时序；本页新增原代码本身的定义级合同。

## 同一组单位客户、全部历史与真正偏离

八名不同单位客户0…7；四主题为{0,1}、{2,3,4,5}、{0,1,6}、{0,1,7}。根0，第二人恒1，末位完整4×4表
\[
\begin{pmatrix}1&1&1&1\\1&2&3&2\\1&3&1&1\\1&2&1&1\end{pmatrix}.
\]
两代码从任意有序前缀继续同一完整策略，逐个深度0/1/2、所有4进制历史、所有当前替代行动直接按每位单位客户均分求当前利润。共21节点、84含自身比较，不只实际011路径；实际每人2、W6。代码没有调用发现器、规范SPE solver或优化器，也没有从冻结JSON读取动作图。

四主题覆盖全部客户的三槽最优值8、真正安全值44/23以及CCE最低福利544/87由既有完整数学承担。两原程序并未各自重算那套安全原始/对偶证书或CCE最优LP；它们打印的genuine security not refuted是结果范围说明，不能据此冒原代码已算安全值。

## 作者：Q(sqrt669)的准确代数与符号

作者K类用有理对(a,b)表示$a+b\sqrt{669}$。加减和乘法精确按$\sqrt{669}^2=669$约化；除法用共轭及范数$a^2-669b^2$。这里只在实际非零分母上使用，类没有另做通用零除schema检查。

sign先处理零系数/同号；a,b异号时比较$a^2$与669b²，再乘a的符号。669不是有理平方，非零有理对不可能范数为0，故这是正平方根嵌入的精确符号判别。approximate()最后用float和sqrt仅生成展示值，不承担任何assert中的严格不等式。

令
\[
r=(30-\sqrt{669})/7,\qquad q=(0,r,(1-r)/2,(1-r)/2).
\]
代码精确核Σq1、各概率非负及$7r^2-60r+33=0$，再遍历全部64个iid有序终局，乘积概率、覆盖和三人的收益均在该二次域求和。对每玩家再逐四纯行动替换自己的随机动作、保其他两人，实现12个静态单方偏离不等式。

因为原分布是独立产品，12项恰证明q为对称混合Nash；它也构成静态CCE，但没有对任意相关分布分类。客户利润守恒给期望覆盖=三人的期望收益和，并精确等于
\[
Z_3=\frac{4344-156\sqrt{669}}{49}>6=W.
\]
还核$r>15/26$，与KN中的多项式短证一致。强iid支付桥W≥Z3失败；本例真正W−3v3=6/23>0、half余额2W−OPT4，均未被反驳。

作者文件无main保护，顶层即执行全部检查并print Python字典；q/Z以K.__repr__字符串表示，Z_approx是展示浮点。它不是默认JSON CLI，没有邻接JSON输入或--output接口；不能用父426B JSON冒作者stdout或该原程序本轮运行记录。

## 父审：Q[s]换基、隔离区间与部分符号接口

父程序用二元有理对表示$u+vs$，模$7s^2+23s-5=0$乘法，即$s^2=(5-23s)/7$。固定
\[
L=2046453/10^7,\quad H=2046454/10^7,
\]
核P(L)<0<P(H)。P在该正区间严格递增，隔离$s=(\sqrt{669}-23)/14$。sign对零对返回0；对其他u+vs，比较端点u+vL/u+vH，要求两者乘积严格正才返回共同符号。

这对本次检查到的非零式是精确有理证书，但不是任意二次域元素的全能sign算法：若端点夹住0，即使真实值非零，也会assert失败而不自动细分区间。不能把“固定窄区间足够本审计”改写成一个对所有Q[s]元素总能返回符号的实现。

父分布$q=(0,1-2s,s,s)$；同样按全部64 iid终局累加覆盖、三人期望和12纯偏离期望。代码核共同收益、收益守恒及
\[
Z_3=(108/7)-(312/7)s.
\]
代换$\sqrt{669}=14s+23$正好得到作者根式，r=1−2s。426B冻结报告的s_polynomial[7,23,−5]、区间上端1023227/5000000（H的约分形式）、Z_in_basis_1_s[108/7,−312/7]都指这一实现；不是根式程序又发现一个不同Nash。

父文件也无main保护，顶层运行后打印完整缩进JSON；它不写邻接文件。原426B报告保原字节，本批没有运行它，因此不声称本批取得过426B stdout全字节回放。

## 充分旧数学、原运行与源状态

两个原实现输入、完整策略和所欲认证的强iid数学均已由现有成功check_iid_examples.py/replay-iid.json充分验证，源码/输出同SHA保全。本次只读两新取得的原实现及父冻结数据，原作者CLI0、父CLI0、旧八客户84/64入口重跑0。对Q[s]换基和符号前提的完整解析说明不需要再执行同一八客户数学。

旧KN/IP中本地源缺记的是**当时**未取得这几份原字节；现在Root正常show已完整取回，六原件的整个manifest和每份唯一capture原样保全，不改旧缺记录、也不把取源计作run。原“独立/父审”指当时作者关系；当前已同时读过两实现与相关证明，未增加blind或外部评审。

这三source的[原件与精确读取](../../tools/evidence/iid-basis-and-weak-family-original-audits-primary/preclaim-full-reading-intake.json)和[旧成功版本](../../tools/evidence/iid-basis-and-weak-family-original-audits-primary/prior-exact-success-manifest.json)另列。本批逐源receipt在完整22项actualpushed/synced原回执、本6子集/currentowner/sourceSHA核真后封存；一般六人half与真正安全聚合未由这套强iid程序改变状态。

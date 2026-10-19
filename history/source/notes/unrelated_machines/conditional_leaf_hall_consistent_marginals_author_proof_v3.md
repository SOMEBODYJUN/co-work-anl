# 同一全局叶边际仍退化：v3新增条款的作者证明

boss11，2026-10-18。这是熟悉v2完整陈述、作者证明和两份实际审查后的新推导，不是blind或独立重构。仅证明冻结Exact v3的§9（SHA34244f9737bbbe7baa858482d31f8154f0e4146be0f1464c9e0598a402bfb38b）；§1–8的旧v2作者Proof和审查原字节不改。新证明在新条款先行独立记录释放前不送审者。

## 1. 旧点、共同hole边际与global flow

固定Exact§8的designated partition及一个原basic可行点。对于一个旧资源u，其positive neighboring groups依序为c_1,...,c_d。记

\[
b_i=\sum_s z_{c_i s u},\qquad b=\sum_i b_i\le1.
\]

取共同hole概率pi_i>=b_i、sum_i pi_i=1，例如将1-b全部加到第一项。hole i的完整路径匹配M_i按v2定义：leaf j在j<i时取port j，否则取port j+1。d=1取空匹配，d=0无路径与新leaf。

令global叶流为sum_i pi_i M_i。每leaf行恰一，port i的叶占用1-pi_i；加core占用b_i后<=1。不同旧资源路径互不相交，因此同时给全体global叶流。原z、lambda、utility没有改变。

## 2. 同一core的各states与hole作运输

固定core c。先设c=c_i是u的一个positive邻居，注意i按group而非state编号。写lambda_s=lambda_cs，z_s=z_csu（该state非正incidence时为零），所以
0<=z_s<=lambda_s，sum_s lambda_s=1，sum_s z_s=b_i<=pi_i。

构造非负矩阵w_(s,h)，要求

\[
\sum_h w_{s,h}=\lambda_s,\quad
\sum_s w_{s,h}=\pi_h,\quad
w_{s,i}\ge z_s.                                      \tag{1}
\]

先在own column i置w_(s,i)=z_s。剩余row量lambda_s-z_s皆非负；剩余own-column量pi_i-b_i非负，其余column量pi_h也非负。两侧剩余总量都恰1-b_i。以固定次序贪心运输这些剩余量，每步放min(row剩余,column剩余)，有限步即完成(1)。无需除lambda、b_i或pi_i，故zero lambda也自然给整行零。

若c不是u的positive邻居，则此core在该路径无正z，直接取w_(s,h)=lambda_s pi_h。它同样有(1)的row/column marginals而没有own-column lower bound。

每个core与每条旧资源路径分别作这份运输。此处并没有要求所有cores同时选择states的共同law。

## 3. 条件流及新增MC等式

令该路径的core-state条件叶流为

\[
 y^{cs}=\sum_h w_{s,h}M_h .                           \tag{2}
\]

每leaf行质量为sum_h w_(s,h)=lambda_s。若c是neighbor i，它唯一可能占用的正z在port i；该port的条件叶占用为lambda_s-w_(s,i)，因此加z_s后<=lambda_s。其他ports上该state的z=0，叶占用至多lambda_s。c不是neighbor时所有z都为0，结论相同。拼接不同路径就覆盖所有新leaves。

对每个leaf-edge求同一core的state和：

\[
 \sum_s y^{cs}
 =\sum_h\Bigl(\sum_s w_{s,h}\Bigr)M_h
 =\sum_h\pi_h M_h
 =y^0.                                               \tag{3}
\]

因此所有cores使用相同global leaf-edge marginals，MC逐行同时成立。不同cores的w可以不同，但其column marginal都为同一pi，这足以支付(3)。

(2)是lambda_s倍的完整整数匹配的有理混合。一般不是一个匹配；这里没有把旧v2的单整数conditional witness追溯升级成含MC的证书。若lambda_s>0，可把w_(s,h)/lambda_s视作条件分布来解释；构造及证明从不实际需要该除法。

d=1时没有leaf rows，MC为空；z<=lambda给全部conditional列。d=0仅保unused资源，无正core z。原zero incidence仍按Exact的D_+零标签路由以private time0保留，不进入z或改变正值。这与旧repo D的零neighbor名单区别保持明确。

## 4. 反向、必要性与位复杂度

任何R_cons点也是旧R1-R2点。对每旧u将d个global port columns相加，扣去d-1个完整leaf rows，立即得原sum_(c,s) z_csu<=1。其他basic条件逐字保留，所以projection恰为原basic polytope。

真实epsilon allocation的必要性使用v2的deterministic witness：每core只一个state取lambda1，其余0；相同完整叶matching同时作y0和每个positive-lambda条件流。因此对每core其states之和也是y0，新增MC不丢任何actual threshold解。自动threshold-leaf分类必须仍满足Exact§8的non-leaf-original前提；不能因此偷偷重分区。

新增MC最多|C| E_L等式，系数0/±1。运输的row/column量只是输入坐标的加减，贪心至多O(|S_c|+d)次非零填充；每次至少清空一个剩余row或column。所有分子分母位长由输入和 supplied point总位长的多项式控制，匹配0/1权再有理求和亦同。按显式core-state/leaf-edge维度输出全部流是多项式，不按任何概率或系数倒数数值循环。标准rational LP给本必要relaxation的feasibility、点与Farkas拒绝证书；不含SDP exact-feasibility假设。

## 5. 同一近二族与准确范围

旧Q_t basic点lambda_M,a=1/D、lambda_H,home=1-1/D、lambda_H,parking=1/D，z=lambda在每正support，原每资源总占用恰1。因此本证明可取pi=b，运输给R_cons完整有理证书，保持那一个原lambda,z。v2已自足证明同一个完整矩阵V=1/t、OPT=2-1/t；本追加只改变证书条件，不改变P、原jobs或actual值。

epsilon=1时各原core都非threshold-unit-demand，新path leaves全部是。任意fixed epsilon>0取t>1/epsilon仍同分区；同一证书的state值lambda>=epsilon lambda，MC不依赖epsilon，所以仍可行，而actual V<epsilon。不存在从R_cons可行性本身推出统一正value或相对unit threshold统一次二排程的合同。

缺失的是所有core选择与完整叶matching的共同law，而不只是逐core条件边际是否平均一致。本页没有证明某个任意新global law可被poly生成/查询或证明完整law恰足；也不排joint-core条件value/capacity、更高矩、其他下界或相对actual OPT的一般算法。不将此证书gap冒充主算法困难性。新颖性未认证，UM-TARGET-v1仍OPEN。

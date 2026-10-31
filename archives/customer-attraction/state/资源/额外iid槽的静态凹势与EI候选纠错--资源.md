---
id: customer-attraction/extra-iid-static-concavity-and-EI-status-review
kind: resource
type_tag: 资源
title: 额外iid槽的静态凹势与EI候选纠错
status: static-theorem-and-conditional-reduction-valid;universal-EI-refuted-by-later-real-bank-family
source_refs:
  - source:58729d348056d7dd1c40
  - source:d397acf1db904b7b019a
---

# 静态对象和两份原稿

3505B作者候选与4369B独立解析审查全文比较，另完整读[静态iid基准](../定理/静态独立同分布安全基准--定理.md)、[合法背景iid值](../定理/合法前缀残余独立同分布价值与租金--定理.md)及[自由extra-one当前边界](../问题/自由extra-one与iid安全值边界--问题.md)。静态部分已被既有定理完整覆盖；本页保原独审明确的导数、值唯一性、条件归约与后来EI真值，不再造同一凹势定理。

有限单位客户、有限非空共同目录，固定非负整数背景b和n>=1个辅助静态玩家。令t_x(p)=sum_{T含x}p_T，

\[
\phi_{n,b}(t)=\mathbb E[H_{b+\operatorname{Bin}(n,t)}-H_b],\quad
g_{n,b}(t)=\mathbb E\frac1{b+1+\operatorname{Bin}(n-1,t)},\quad
F_{n,b}(p)=\sum_x\phi_{n,b_x}(t_x(p)).
\]

逐项Bernstein差分给phi'=n g；n>=2时

\[
\phi''=-n(n-1)\mathbb E\frac1{(b+1+\operatorname{Bin}(n-2,t))(b+2+\operatorname{Bin}(n-2,t))}<0.
\]

端点也严格负，n1线性。有限单纯形紧，最大者存在，KKT与凹性恰等价于p面对n-1个iid p对手时所有正支持查询取共同最大收益。若n>=2的两个最大者有某客户t不同，中点严格增势，矛盾。因此客户概率向量唯一，不要求p本身唯一；共同收益

\[
\lambda_n(b)=\sum_x t_xg_{n,b_x}(t_x)
\]

良定。n1即最佳主题值，零客户给0。静态最大者不是顺序SPE策略，也未声称它最大化总残余支付。

# 正确的不等式方向与条件half归约

真正v_n(b)允许n-1个不观察查询的任意相关合法竞争主题。对任意静态对称Nash p*，Q=(p*)^(n-1)是一个合法对手分布，各查询期望<=lambda。因此

\[
v_n(b)\le\lambda_n(b).
\]

原EI候选是：任意合法背景后余r人的每份完整纯SPE，其首位u>=lambda_(r+1)(b)。若它对全部背景成立，实际每位有u_i>=lambda_(r+1)(b_i)>=v_(r+1)(b_i)>=v_(m+1)(0)>=OPT_m/(2m)，求和给half。前缀嵌入只限制静态对手槽子集，不搬运不同分支的实际旧收益。

最后一个静态下界可保比较槽k/对手槽ell分离：令任意联合对手Q的均值负载L_x，平均主题边际a_T，故L_x=ell sum_{T含x}a_T。对比较覆盖重数d，1_(d>0)<=(d+L)/(1+L)，客户求和至多(k+ell) max_T sum_T1/(1+L_x)；Jensen使各真实随机背景查询值不小于其均值负载值。取有限minimax得v_(ell+1)>=OPT_k/(k+ell)。ell0独立用OPT_k<=k max|T|；half归约只用k=ell=m>=1。

以上是有效的**条件蕴含**，不证明EI。静态推导即使完整，动态前提仍可为假。

# 后来真银行族已否定EI

[完整银行SPE族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)在m4、零前缀、10名单位客户和12个共同主题上有完整有序策略，根u=4/3、W8、OPT10；原全历史控制器由该既有对象证明，这里不新跑或补猜另一策略。

四个经济客户、三个各两客户的银行块；每主题恰一个经济客户加一个银行块。任意四槽静态对手混合，设经济平均负载a_j、银行平均负载c_i，则sum_j a_j=sum_i c_i=4。Jensen给每个(j,i)查询的期望至少1/(1+a_j)+2/(1+c_i)。存在a_j<=1及c_i<=4/3，故最大查询至少

\[
\frac12+\frac{2}{1+4/3}=\frac{19}{14}>\frac43,
\quad差=1/42.
\]

对所有Q取最小，v5>=19/14；再由lambda5>=v5，得到lambda5>u。**19/14这里只是两个值的下界，不是已求得lambda5或整数v5的精确值。** 该空背景四人完整SPE足以否EI的一般全背景全称，也否更弱ES首位>=v_(r+1)。它严格满足half，不能据此否根半覆盖、真正总安全聚合或所有别的iid候选。

两原稿2026-10-23的“EI仍OPEN/独审未发现致命异议”只保当时范围；独审本来就只审静态对象和条件归约，没有证明EI。不得把新的真反驳归给其当时的LP。

# 原有限诊断和复用

作者原extra_slot_probe在旧69客户四人完整策略锥上变客户质量、对七固定有理查询分布加入五人iid Nash条件；四输出有精确可行原始点但没有全体对偶。原浮点阴性不证明该锥全p，更不覆盖后来银行目录；本批未读或运行其原代码/输出，不据README把其他同名extra-iid报告的115项计数挪进本源。

独审未查发现LP代码，先定义重构的先验仅属历史内部审查；本批同时全文读两稿，不自称盲审/外审或新颖性。原件、比较快照、代码缺件与逐源处置见[证据](../../../../tools/evidence/root-extra-slot-and-dynamic-ledger-primary/README.md)。0原入口、0新数学程序、0solver；银行下界为上述解析推导。

# 后续原实现读取的新增范围

后续KK批已取得并全文读3458B原extra_slot_probe.py及20567B策略锥模块，七个固定有理q、所有Nash支持等式/零支持不等式和精确有理恢复验收条件已自足展开于[固定策略探针合同](固定完整策略的总覆盖机会与额外iid槽探针合同--资源.md)。同批还完整读另37565B动态机会JSON九记录。原本页批次“未读或运行”记录保其当时时点；本次增加的是实现阅读与解析合同，仍0原CLI/LP，未取得七q原stdout或四个恢复向量，也未新证任何阴性最优值。银行EI反驳的来源与解析结论不变。

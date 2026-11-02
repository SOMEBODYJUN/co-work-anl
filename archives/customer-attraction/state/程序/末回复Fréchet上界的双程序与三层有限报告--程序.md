---
id: customer-attraction/last-reply-frechet-two-programs-and-three-level-finite-report
kind: program
type_tag: 程序
title: 末回复Fréchet上界的双程序与三层有限报告
status: 两原程序/完整7367B报告清洗；4433B独立入口一次原样成功；其余成熟成功复用
summary: 完整区分作者具体条件Z、逐行贪心最大和任意联合宽上界，保存全部原负数组与字段；独立1920项只核最强广域负类，不冒全60或3889重放。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/verify_zz_bound.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/independent_zz_bound.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d0dc7461ada541a5a2ab9a2b8ad4e623/strategy/zz_bound_exact.json
---

# 末回复Fréchet上界的双程序与三层有限报告

## 实读、数学目标和本次执行

6952B作者程序、4433B独立程序及7367B JSON全部字段/数组已逐件全文；8990B数学稿在前批已全文，同SHA本批直接复用，不为凑阅读重新扫描。数学论证及固定四态范围见[共同扩张障碍](../障碍/固定末回复四态边缘的Fréchet共同扩张障碍--障碍.md)。代码和输入指纹、原件、运行日志见[本批证据](../../tools/evidence/frechet-fixed-reply-marginal-separation-primary/README.md)。

本批仅把**未改4433B原独立入口**在隔离原布局运行一次：1920项/16hist、最强广域上界严格负，0.09956873899864149秒、exit0、stdout771B、stderr0。作者6952B、旧3889 verifier、LP/SLSQP/BI/SPE、成熟六阈值最大值均0新调用。其它三广域负值和具体完成的长分数按冻结报告保存，不能借这一次最强类成功说它们均已新重算。

## 唯一输入、实际消费字段和路径

两程序输入均旧816498B `attractive_nested_exact.json`，SHA
`cc48d8fdf557be7370ce964ee1d891ea99c8c830011c41cff76293b3819356b1`。本批从已发表精确原件按原路径复制到source-root，前后SHA同。原点有1905列，但程序只用16个hist及其194组三态；K和1306个RR辅助交叠不用。给定负界不要求把这些辅助坐标当真实集合交。

每hist存actual_bits（程序用前四位求a）、八桶词直方图（字典序000…111展开恰六wᵢ）和质量H。后续joint-reply按最近hist归属，组(family,diag,wᵢ,wⱼ)，三状态01/10/11的质量确定R边缘q、Z边缘v、own交叠t。所有质量未除H；不得外层再次乘H。

作者ROOT向上找**文件**work.py，模块顶层即定位；没有该标记时import也会失败。独立程序不用标记，固定`Path(__file__).resolve().parents[5]`为根，必须保持`source-root/research/workspaces/customer-attraction/R-d0.../strategy/`深度；当前运行完全按此布局，没有创建或执行work.py，也没有Git/网络。两个main均有guard，独立程序除标准库/只读输入外没有导入副作用。

作者计算并报告输入SHA，未硬编码真本；末尾硬断言四个广域负类与最强分数。它不重验旧3889行，也不核旧O/W元数据，本report的W/O直接抄输入。独立程序硬断言完整输入SHA，核每组状态键恰01/10/11、各值非负/和≤H；不消费旧W/O或重新证明3889可行。两个合同不能混写成相同“点全验证”。

## 作者实际算了三层，超出开头docstring

原docstring只强调一份共同阈值/条件Z完成；函数main还完整计算逐行最大值和不固定R联合的Fréchet上界。它全程Fraction，无NumPy/SciPy、优化器或容差。

### 第一层：一份保own四态的具体条件生成

各hist取共同阈值R_g=[0,q_g)。给Z_f在R_f内概率t_f/q_f，在外概率(v_f−t_f)/(H−q_f)，附加条件独立辅助随机位即可共同实现所有own四态。零长度区域分支取0，不除0；H0的hist须全部三态为0，作者跳过它。

在该特定完成中
\[
 X_{ef}:=|R_e\cap Z_f|
 =\frac{t_f\min(q_e,q_f)}{q_f}
 +\frac{(v_f-t_f)[q_e-\min(q_e,q_f)]}{H-q_f},
\tag{1}
\]
零分母对应项按0。源码核X_ee=t_e，并用
\[
 L_{ef}=\frac{v_e-v_f}{a+1}-\frac{t_e-X_{ef}}{(a+1)(a+2)}
\tag{2}
\]
累加全部60类。它是一份具体共同完成，不是最优耦合，也不同时保旧RR辅助值。

当前10个正hist、25个R阈值区间，66标签每hist共4356有序边对，作者正质量循环合43560对。所有原negative_rows六个class和完整长分数均保存于原JSON；最小为
\[
 -269116452255245004437772368580110652437/
 530195166743494242094563876251940420480.
\]
其中仅0102的(0,1)和(1,1)两个类的具体值等于下一层最大值，不能用共同最小值相同把整组六值替换。原数组字节保全，不只留一个min摘要。

### 第二层：每个类独立最大化固定R阈值域的Z分配

按共同R断点得到区间s，质量w_s，R位r_sg确定。对每个class C、组g、区间s，逐标签对累加线性系数c_(C,g,s)，使其完整行就是Σc y_sg。变量是Z在该区间的质量，界0≤y_sg≤w_s；own四态要求
\[
 \sum_{s:r_{sg}=1}y_{sg}=t_g,\qquad
 \sum_{s:r_{sg}=0}y_{sg}=v_g-t_g.
\tag{3}
\]
Z-Z行没有Z_eZ_f项，固定R后各g及ownR内/外两桶分别可分离。对每桶按系数降序，依区间容量贪心填足规定总质量，即连续背包的精确线性最大值；剩余质量断言为0。若把低系数的一份质量移到尚有空位的高系数区间，目标不减，所以此贪心正确，不依赖LP求解器。

原`arbitrary_conditional_Z_individual_row_maxima`明确**每类独立**求max，未保存各类最优分配，也不声称共同同步达到。这六个负max如下，与成熟[固定二维阈值诊断](固定二维回复边缘的共同阈值诊断程序--程序.md)的六个同步最大值逐值相同；本批只比原保存分数，不重跑成熟诊断。

| (源族,查询族,模式) | 原逐行最大值 |
|---|---:|
|(0,1,0100)|−1328738393618193677729117997671899078003/6362342000921930905134766515023285045760|
|(0,1,0102)|−269116452255245004437772368580110652437/530195166743494242094563876251940420480|
|(0,1,0122)|−14899412095726297871620235604054324787/1060390333486988484189127752503880840960|
|(1,1,0100)|−56009261350162372188029228238106097801/1413853777982651312252170336671841121280|
|(1,1,0102)|−22991298209394701311475016979769358257/1060390333486988484189127752503880840960|
|(1,1,0111)|−125041678383573250492315909619446368923/1272468400184386181026953303004657009152|

成熟另证在每个ownR内/外均把Z放最低t区间能同步达到所用正交叠上界；这提供更强的共同达到解释，不是原6952程序已经核了一份同步最优赋值。一次max为负只需给该类的域内不可能，不需要其它类最优配置相容。

### 第三层：任意联合的宽上界

将X_ef替为min(q_e,v_f)，e=f则直接取已固定t_e，得到不要求共同阈值R的安全上界。逐类汇总原`unrestricted_pairwise_upper_bounds`有四负，最强0102类为
\[
 -77805114978912902524965135501273065957/
 176731722247831414031521292083980140160.
\]
其它三值与一般证明见[障碍正文](../障碍/固定末回复四态边缘的Fréchet共同扩张障碍--障碍.md)。这些min不要求共同可实现；上界比真值大仍严格负，已经足够排固定边缘的任意联合。它不是精确最大值或Frechet约束充分性。

## 原7367B报告所有字段和未保存内容

根字段完整为scope、source、source_sha256、W、O、rows、negative_rows、min_slack、histograms、arbitrary_conditional_Z_individual_row_maxima、unrestricted_pairwise_upper_bounds。顶层scope仍只描述第1层，不代表文件后两层不存在。

| 字段/子字段 | 保存范围 |
|---|---|
|scope/source/source_sha256|特定必要点完成范围、原相对输入路径、完整旧SHA|
|W/O/rows|旧W分数/1/60；60是名义类数含18空槽，不是60独立非空约束|
|negative_rows/min_slack|第1层完整六负及全60最小值；未存其它54值|
|histograms|10个正hist的质量/组数/R阈值片数，合25片；没有完整actual/词/组表，须原输入|
|arbitrary...scope/strictly_negative_maxima/minimum_of_individual_maxima|第2层完整六负max和最小；未存全部60值或各自最优分配|
|unrestricted...scope/strictly_negative_upper_bounds/minimum_upper_bound|第3层完整四负宽上界和最小；未存其它56值|

冻结JSON有源SHA但没有程序SHA、原argv/环境、墙钟、独立stdout或整个旧矩阵。不得从报告存在补这些历史进程字段。本批每个长分数全部读过并原样保全；不是只读文件头或最小值。

作者CLI只有可选--output；省略则只打印。给路径时以`open('x')`独占新建，不覆盖已有文件，父目录也不自动创建。它**先写报告，再断言四广域负类/最强值，再打印**，所以异常输入下存在报告文件不自动表示最后assert已经成功。没有通用畸形输入验证；组重复键可能覆盖，未给完整列布局/旧可行性验证器。

## 独立4433B入口的真实覆盖

独审源码另写从旧columns顺序解码hist/三态，硬核cc48d8 SHA。用permutations(range(6),3)得到每hist120个互异i,j,l，源组(0,0,w_i,w_j)、查询组(1,0,w_i,w_l)。直接以q_e/v_e/t_e/v_f代入第3层公式，不调用作者partition、行生成器、max分配或特定完成。

它遍历所有16hist，含6个零质量块，故1920 labelled_comparisons；7块subtotal非零，不等于输入仅有7个正hist（实际10个正）。硬断言所得分数等EXPECTED_BOUND且严格负。这个预期常量不是依赖作者代码的计算；`matches_parent_diagnostic`只表示与内嵌预期相等。

它只打印一条JSON、不自写文件；不会生成原7367B全报告。新stdout的class、source SHA和最强值由外部运行器再与冻结报告对应。原独审未读取作者JSON，也不验证其余三宽界、六具体负值、六row maxima、旧3889行或完整SPE。

## 当前事件、原布局与复用边界

本批[run_independent_once.py](../../tools/evidence/frechet-fixed-reply-marginal-separation-primary/run_independent_once.py)先核六primary与旧点SHA/size，按原布局直接子进程`python -I -B independent_zz_bound.py`，捕真实stdout/stderr/UTC/argv/exit及所有字节。已有运行文件时拒绝重复执行。结束后核原件/输入未变，绑定新最强值与冻结JSON；没有修改原代码、monkeypatch或stub模块。

结果为16hist、1920比较、7非零贡献、严格负最强分数，771B stdout和0B stderr；0.09956873899864149秒、exit0。stdout不是找回的旧独审历史输出，原未给旧输出字节不能说“逐字节匹配历史stdout”。它与作者冻结报告的对应最强数值相同，证据身份清楚。

原六阈值max已成熟同值，无新疑点所以不重跑；作者6952、旧3889及五人6144/一般叉回归均0新执行。当前旧点即使不再查其3889通过，也能独立确立这些固定四态无联合扩张；旧图通过身份仍引用成熟证据，不倒填新独审为旧图第二实现。

后续若改Z/RZ边缘，本不可扩张证明前提已撤；若仅改RR、K或共同R联合而保全部四态，负Fréchet界仍在。改变源历史/实际负载/标签组需重做必要行及点绑定，不能把这一次有限负值当任意模型的全称定理。相关范围与新旧证据关系见[关系自查](../../tools/evidence/frechet-fixed-reply-marginal-separation-primary/relations-and-self-review.md)。

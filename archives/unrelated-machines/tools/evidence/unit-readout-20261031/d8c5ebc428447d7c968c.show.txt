# 校准计数槽与有界密度算法：实际审查

正文最终SHA256为 `dd33b681f22b957fecb5c4a29beca173cb7b619d77c542e99e91c0bd88b5bd88`。两正式ID及受限C1必要性没有尚成立fatal；外审、新颖性和独立论文价值未认证。

实际审查顺序：cover与pcsp先只凭精确分数合同和固定D合同独立重构；pcsp还先凭严格YES插值条件独立重构并写独立软件。下方两个全文攻击都实际读取原c3b018...cc23；随后§5只新增最近经典结果扣除段及页码。root机械删除该唯一段后精确恢复c3b018全文hash，两审查者又实际核最终dd33字节并亲读VW Theorem7，数学证明未变。现行定位为原PDF第9页/印8；下附24d6确认是页码精化前的真实旧记录，不冒称其当时就读过新hash。

最近结果扣除：VW Theorem7对整数有限时间给2−gcd/max，将本页处理时间乘k得到{1,k}，代入仅为2−1/k。该已有改善不随k统一，本页固定D仍允许k,h无界；所有有序槽/Hall/容量匹配工具均明确为经典工具，未认证本文全球新颖性。

root亲读两最终程序并实际重跑：规范1464份完整σ、85094原jobs，含895穷举wiring/r、240非均匀强见证、320固定D（156校准、163路径、1失败真OPT2）、3个小原P共1698全σ、空巨大参数/显式深树/巨A/非法域；独立实现90普通有理LP、522比特分母、188个实际C1的密度profile、288固定D（168校准、118路径、2失败），互不import。两程序不调用LP solver，生产路径不调用OPT；规范只有audit枚举用有限原P oracle。

root另不import规范代码，直接读取三份原资格矩阵，独立全枚举162、512、1024份σ，分别真OPT1、7/4、2，并回算给出的所有机器负载。三种CLI（given witness、calibrated、bounded D）都实际运行并重算原边。有限检查不承担一般证明，也不把given-witness充分条件冒称必要LP。

软件改动来源：规范从scratch SHA402a2115...63071b复制，root仅解除Python3十进制字符串4300位默认上限并新增两个>5000位整数/分数精确输入例，再重跑全部审计。最终规范SHA039ac7dbbfc0858aa9f51086ad8debb2b2f403b282e6a516ada328e2ebf175c4；旧source/run保持原字节。独立程序保持SHA b87e5c382ccbe2c85e69cc8c81e98e35fb7967491914d5e5db26896f01608b1e。外来见证运行时间包括其编码长度；bounded-D自产分数按原P位长多项式，无需一般LP集成。原机器未用unit以精确零区间保留，所有任务逐件给具体机器。

[正文](../../current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md)、[原P反例](../../../examples/unrelated_machines/unit_readout_calibrated_counterexamples.json)、[冻结实际输出](../../../evidence/runs/unrelated_machines/unit_readout_calibrated_cardinality_slots_audit.json)。以下保留实审原文，scratch文件名仅定位来源；必要内容已经在本页与登记路径保存。

---

# 校准计数槽与有界密度算法：最终全文数学攻击

内部审查者 cover_consistency。实际全文读取 `research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md`，SHA-256：

    c3b0182635999fb3cdbb3abde2cd0c9cb48286094dca91cd8c2f38257ad6cc23

绑定两个正式身份 `UM-UNIT-READOUT-CALIBRATED-SLOT-v1` 与 `UM-UNIT-READOUT-BOUNDED-DENSITY-SUBTWO-v1`。先前对原fraction合同与固定D候选为仅收到精确陈述后的独立重构，原scratch保持不变；本次新增“受限严格YES必要性”及第二个弱条件反例是在读最终证明后攻击，不冒称同样盲重构。未读hardness_route新稿、未导入/审计新程序、未对原P执行穷举。

## 总判断

两正式合同以及额外严格YES必要性在其各自明确假设下**没有standing fatal objection**。外来有理见证位长、LP仅充分、无pins、unit外端时间1、固定D的量词均已写清。实际代码、LP求解器集成与运行结果由真实软件核验者承担，本页只认证所述数学推导。

## 1. 证书能成为全局共同分配质量

根selector的两incoming非负且和1，故各<=1；非根incoming为父edge的t∈[0,1]。每edge在父端1−t、child端t；leaf在父1−t、外端共t；selector两根质量合1。因此每原job的全列质量恰1，没有隐含丢任务或某端负分数。

每内部机只有一枚incoming大任务时间1、k枚outgoing小任务时间1/k。第一行的精确含义是

    y+sum_out(1−t)<=L=k−r+1,

不是分数处理时间负载。L是整数且>=1，是首槽被大任务占用后还剩L−1个整数位置的承重条件。

clause外质量可按真实port顺序装入至多ceil(sum t)<=min(A,d)台unit，必要时一个port的t跨两相邻units，所有外端都是原资格。A0时sum t0，不造不存在的外机器；binary A不按数值扩空slots。内部edge/leaf多端切片没有破坏每job全列质量1。

## 2. 有理质量槽、Hall与全部真实负载

树row先incoming再small，切单位质量槽。row质量<=整数L，故至多L槽；incoming质量<=1且位于开头，正质量只邻首槽。small片可以跨两个槽，也可能一槽有多个small片，不能使用每槽半片数<=2的旧特殊论证。canonical已改为总质量版Hall：任意job子集总质量|S|全部到N(S)，每slot质量<=1，故|S|<=|N(S)|。

一次覆盖全部jobs的匹配输出完整原sigma。若某机收incoming，只能用首槽，其余至多L−1=k−r枚small，真实负载<=1+(k−r)/k=C_r；若不收incoming，至多k枚small，真实负载<=1。每外unit只有一个槽，真实至多一枚时间1的port。所有selector、内部edge、leaf、未选sign、断开的内部区域都在同一次匹配中，各机负载不是分别选择的存在性证明。

每端片质量<=1，因此在每row至多跨两槽，支持图及slots受显式job数控制。输入有理加法/比较按P加见证编码长度位多项式；canonical已正确将任意超长外来分数计入输入。标准LP可以另给小位长解，但当前实现不因此被宣称已经集成通用LP；固定D算法自己生成见证，完全不需要该模块。

## 3. 两个四机器反例的真实对象

弱条件反例是k4,h1,r2：两个根、每根4ports，各sign接一个独立clause unit、A1。selector各半、ports各下传1/4给每row弱下传1=r*y、clause质量1，但强row质量1/2+4*(3/4)=7/2>L3。真实C<7/4<2时所选根的clause unit最多容一port，至少三枚1/4留根，使负载>=7/4；一port外送、其余父置达到。因此仅Σout t>=r y确不支持C3/2。

非必要反例是k2,h1,r2：两根及同一clause的两unit，四ports各原父端或任一unit。selector选正，正两ports外送不同units，负两ports父置，真实C1。两根强约束合计sum_leaf t>=3却clause cap2，LP不可行。故数学LP不可行不意味着一般目标阈值不可行。

前者4机9jobs、每job两原端，完整sigma数2^9=512；后者4机5jobs，selector两端、每port三个原端，完整sigma数2*3^4=162。这只是本人的资格/计数复算，不声称本人已运行512/162穷举或认证相应程序。

## 4. Uniform校准及所有参数边界

递推kx_l=r−1+x_(l−1)、x0=1/2，给每row分数数量恰L。k>1时a=(r−1)/(k−1)∈[0,1]且

    x_h=a+(1/2−a)/k^h,

是a和1/2的凸组合；k1强制r1，递推恒1/2，不出现0/0。每leaf质量相同，故clause条件仅d_c*x_h<=A_c，不依赖wiring。k4h3r2给a1/3、x_h=1/3+1/384=43/128，条件d*43<=128A确比d<=2A更宽。

分母位长O(1+h log k)，由显式非空树/叶地址总输入界住；空变量先输出0，不计算不存在的指数树。r1给C_r=2−1/k，r=k给C_r=1，全部unit负载1均不高于目标。

## 5. 受限严格YES必要性的读后独立核对

本段另有k>1与每clause a d_c<=A_c的假设，不能删除。若实际C<=1，每selector选中的sign整树全部下传：任何已有incoming1的节点不能再保留正时间small任务，逐层迫使全部children及最终ports下传。因此记每sign s∈{0,1}为selector选择，clause中所有被选sign ports数t_c<=A_c。

取该sign深l分数a+(s−a)/k^l，根incoming取s。分数为a与s的凸组合，合法[0,1]；相邻层等式仍kx_l=r−1+x_(l−1)。设N=k^h，clause全叶分数为

    a d_c(1−1/N)+t_c/N.

额外a d_c<=A与实际t_c<=A使它是两个<=A量的凸组合，故<=A。这样确构造一个强LP见证。因此在此额外域，数学LP不可行能证明OPT>1，但不是说所有OPT>1都被拒绝，也不是一般阈值的LP必要性。

k2非必要例a1,d4,A2违反a d<=A，故没有矛盾。k1未定义a，该段显式排除；V空则条件与见证都平凡。数值求解失败没有被当作已证数学不可行。

## 6. 固定D两分支与乘法保证

D为固定有理常数>=2，密度d_c<=D A_c；允许D以有理输入编码只影响运行位长，D无界时不保统一epsilon。非空实例selector给OPT>=1；空变量无原jobs，先输出0。

k>=D时准确有k>=2，r=1+floor((k−1)/(2D))合法，a<=1/(2D)，N>=k，所以

    x_h=a(1−1/N)+1/(2N)<=1/(2D)+1/(2k)<=1/D.

因此uniform证书可行。1+floor z>z给r/k>(k−1)/(2Dk)>=1/(4D)，实际C_r<2−1/(4D)，乘上OPT>=1即可得到canonical的非严格近似界。保留正文方便保证，不把其常数升级为最优。

k<D时用变量到可达clause容量匹配。每条关系保留一个真实leaf、sign及唯一祖先路径；成功给r1路径正规形，所有inactive jobs父置，实际C<=2−1/k<2−1/D<2−1/(4D)。不比较压缩树中不存在的虚拟路径。

失败时，任一实际C<2会在每selector选轨递归提取至少一条真实下传根叶路径，C<2保证继承unit注入，从而给容量匹配，矛盾。所以OPT>=2。全部非selector jobs父置、每selector任取根给根2、其他内部1、unit0，故非空输入真OPT2且已输出最优。失败分支不靠“没有找到uniform证书”判断不可行。

binary A截变量数/arity、非整数D交叉比较、k1（只进fallback）、A0在密度条件下d0均准确。树、分数slots与匹配的规模按显式P和D位长多项式，不依赖处理时间分母数值或未知OPT，也未调用源SAT。

## 7. 范围与standing状态

该类固定D的epsilon=1/(4D)统一于k,h和实例规模，但一般UM没有这些私有唯一incoming、统一small和共同unit资格，也没有固定D。令D随目标epsilon变化仍可能用于归约，本文没有排除；要说明实际非空YES和所有低负载森林的NO解码。封闭配置gap趋2可以有D随参数增长，不与固定D算法冲突。

最终standing：两正式Claim、uniform证书、两真实反例及受限C1必要性均无数学fatal。泛LP实际集成、软件穷举、外审、新颖性和一般UM主目标未在本次认证。


---

# 校准计数槽正文的最终全文攻击与软件来源核对

审查者：boss11 内部 `pcsp_occurrence`。本报告在陈述优先独立证明/代码冻结之后另写，不改冻结盲稿。

## 阅读版本与独立性

完整实际阅读正文：

`research/current/unrelated_machines/unit_readout_calibrated_cardinality_slots.md`

读前 SHA256：`c3b0182635999fb3cdbb3abde2cd0c9cb48286094dca91cd8c2f38257ad6cc23`。

同时阅读其物理对象引用 `unit_readout_pruned_forest_boundary.md`，核对深度含义、每个内部机器的唯一 incoming、每个子句单位端的共同资格、空任务与私有机器等前提。

此前仅凭精确陈述独立完成并冻结：

- 数学重构 `statement_first_lp_and_bounded_density_review.md`，SHA256 `1873f90bde3f9586e47579e9b0d1419ab1a0039b72d61b85d9394703e61ff3d3`。
- 独立实现 `independent_unitforest_slot_rounding.py`，SHA256 `b87e5c382ccbe2c85e69cc8c81e98e35fb7967491914d5e5db26896f01608b1e`。
- 实际输出 `independent_unitforest_slot_rounding_audit_v2.json`，SHA256 `bb2b5664b6a81de2cf5bfcaf06adbfddbcc310d6c138cf14c133e77d237c4e31`。

这些文件均在 `/workspace/scratch/038d9dcc4cac/unitforest_lp_independent_review/`，没有读取同行候选后再冒称独立构造。

## 数学攻击

**§1–2：LP 与一次联合匹配。** 各内部行满足 `y+Σ(1−t)≤L`，整数 `L=k−r+1` 足以控制上取整槽数。incoming 的全部质量从 0 开始、长至多 1，所以只邻第一槽；不能先逐机独立匹配，正文明确一次覆盖所有原 jobs 的 Hall 匹配，逻辑正确。子句槽映射到不同真实单位机只用原有共同资格，截取 `min(A,d)` 不改变任何原任务的可用端合法性。没有漏计另一符号树、inactive 分支或没有选中的任务。

任意有理质量而非只半质量，Hall 用质量守恒证明，正文没有沿用每槽度 2 的特殊计数。处理时间均为 `1/k` 或 1，排序 incoming 在先同时符合真实处理时间次序；`k=1` 的时间相等不影响指定顺序。实际负载结论成立。

给见证的位复杂度成立：任务在每端质量至多 1，至多跨两个槽，所需有理数的位长受证书输入总位长控制。正规有理 LP 的存在/可求性与“当前实现没有一般 LP solver”的区别也明确，没有把任意外给巨大分母当免费对象。

**§2 两个反例。** 弱激活反例的 `k4,h1,r2` 数据给 `y=.5,t=.25`、每子句质量 1，强行计数为 `.5+4·.75=3.5>3`。任何 makespan 小于 2 的实际调度，每私有单位机最多一个 port；selector 所在根至少保留 3 个小任务，负载至少 `7/4`，且送出一枚达到，故确实反驳 `3/2`。4 机器、9 任务。

强 LP 非必要例 `k2,h1,r2` 的实际完整调度负载 1；两个根行相加要求外送质量至少 3，而唯一子句容量为 2。4 机器、5 任务。该例我也在陈述优先阶段独立得到并运行实际见证，但没有为它运行全物理调度枚举。

**§3：校准与受限必要性。** 深度 `l` 对应从深 `l−1` 内部点下传的任务，递推和 `x_h` 定义与原树的深度相符。`k4,h3,r2` 的数值确为 `43/128`，其绝对调度上界为 `3/2`。`k1` 单独处理避免 `k−1` 除零。

受限严格 YES 的证明只需要计数被 selector 选中轨的全部叶；实际负载 1 强制这些整轨全部下传。未选轨存在额外 down 活动不妨碍 `t_c≤A_c`。深度函数满足内部等式，子句总和是 `a d_c(1−1/k^h)+t_c/k^h`，在两项端点均≤`A_c` 时成立。前提必须是所有实际 ports，包括 dummy；正文的 `actual leaf arity` 与引用模型一致。不带密度的非必要反例不冲突。

**§4：固定 D。** `k≥D` 分支中 `k≥2`，`1≤r≤k`、`a≤1/(2D)`、`N≥k` 和 `x_h≤1/D` 同时成立。严格 floor 不等式给 `r/k>(k−1)/(2Dk)≥1/(4D)`，因此所保守声明的常数有效。该证书完全不需要未知最优值或源赋值。selector 时间 1 给非空实例 `OPT≥1`，将绝对上界变成比例的方向正确。

`k<D` 分支的容量匹配成功时，只沿一条路径下传，路径内部负载为 `1+(k−1)/k`，非路径内部负载 1，子句所选叶可注入不同单位机。失败时任何 `C<2` 实际调度确实会从每 selector 根向下提取至少一条实际路径；不同变量树私有，外部每机至多一枚时间 1 叶，所以必得到被假设不存在的容量匹配。all-parent 的完整实际调度给负载 2，故这个失败分支确实精确最优。`k1,h1,A0` 和空变量边界均已处理。

`D` 可作为输入仍有总位多项式算法，但输入无关常数只有固定 `D` 时成立；正文明确保留这一量词。其归约限制也没有阻止随目标 epsilon 改变 `D`，没有偷换成一般 UM 的结论。

**§5：来源扣除。** 正文将实际新结构信息放在唯一 incoming、统一 small 时间、整数行基数预算和共同单位端资格上，并将有序槽/LP 工具明确归于经典方法。没有将结构类次二算法或一个充分 LP 升为一般目标的解决。全球新颖性和论文价值未认证，身份准确。

## 软件来源与实际运行边界

本审查者亲自编写、阅读并运行的是上述独立 scratch 实现；它实现任意有理质量的切槽、一次确定性增广路匹配、合法实际目的地映射和逐机器负载回算，不导入 root 或其他代理的候选代码。

该实际运行涵盖 90 个普通可行 LP、空任务、一个 522 比特分母见证、188 个实际 C1 的条件必要性 profile，以及 288 个固定 D 密度实例。288 例分支统计是 168 个均匀 LP、118 个匹配成功、2 个匹配失败/实际负载 2，另有故意匹配障碍和无条件必要性负控。

父研究者另行报告两反例的完整物理调度枚举：5 任务例有 `2·3^4=162` 个实际 sigma，9 任务例有 `2^9=512` 个实际 sigma。这两个数量与原资格吻合，但**我没有亲跑那份 root 枚举代码**，不能把其运行归为我的独立软件核验。我的一般最优性判断来自上述自足证明，有限代码结果本身不承担一般定理。没有声称我运行了通用 LP solver 或不可行证书程序。

## 结论和一个措辞建议

读后没有尚存数学 fatal objection。§1 的“无job时添dummy”建议明确为“无job时若需保证 m≥1，只添无任务 dummy 机器”，这样与后文空 sigma / OPT0 完全一致。原引用模型已明确是空闲机器，故这是消歧义建议，不是数学反驳。除该词句外，当前全文不需数学更改。

如正文随后仅采纳此消歧义，需另记新 hash 与 changed-section 复核；本报告当前阅读对象仍是上记 `c3b018…6cc23` 原字节。


---

# 校准计数槽：VW 来源扣除段的变更后确认

本次只复核正文 `unit_readout_calibrated_cardinality_slots.md` 从旧版本 SHA256 `c3b0182635999fb3cdbb3abde2cd0c9cb48286094dca91cd8c2f38257ad6cc23` 到新版本 SHA256 `24d6cb598dde7338eb25a818c1c8afd863cb04bc1e8ac0bc720bc4ae8dd83194` 的变更，不改原陈述优先审稿或原全文攻击报告。

实际字节检查：全文恰有一个以“与最近经典结果对照：”开头的新段；删除该段及其后一空行后，SHA256 精确恢复 `c3b018…6cc23`。所以仅 §5 增加经典结果扣除段，两项正式数学合同、全部证明及边界字节未变。

本次另外亲自实读仓库已登记原文 `history/source/literature/unrelated_machines/verschae_wiese_2010_configuration_lp_v1.pdf` 的 §4、Theorem 7。定理确实给 `2−gcd(p)/max(p)` 保证。对本页非空正时间集 `{1/k,1}`，统一放大 `k` 得整数时间 `{1,k}`，故 `gcd/max=1/k`，精确得到已有 `2−1/k`。因此有界 `k` 的改善不能记作本页新增机制；该已有界在 `k→∞` 时趋 2，而正文固定 `D` 合同仍允许 `k,h` 无界。新增段没有据此认证全球新颖性，表述范围正确。

来源定位小注：本地实际 `pdftotext -f 8 -l 9` 显示 PDF 第 8 页为印刷页 7，Theorem 7 位于 **PDF 第 9 页、印刷页 8**。新增段写的“PDF/印8”建议消歧义为这个精确位置；这不影响数学结论。

截至此报告，当前正文读前/读后均为 `24d6cb…83194`。没有尚存数学 fatal objection；原完整审查的所有数学结论延续有效。软件方面没有新增亲跑声明：此前亲跑独立有理槽实现的范围与 root 独立枚举的归属继续按旧审稿区分。

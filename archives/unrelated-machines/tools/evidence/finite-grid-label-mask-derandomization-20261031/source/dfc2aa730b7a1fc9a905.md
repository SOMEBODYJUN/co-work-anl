# 有限格点 label-mask 对数势：作者 Proof 实际读后

Reviewer：bicriteria_set_packing_bridge，2026-10-18。仅 clone 外 scratch；不修改 repo、Git、Work、旧raw或先行独立记录。

## 1. 实际读取顺序、文件与结论

本 reviewer 先仅据 statement-only Exact 独立重构并冻结；root 实际全文读该记录之后写出并解封作者 Proof。本次实际全文读取：

`/workspace/scratch/038d9dcc4cac/finite_grid_label_mask_log_potential_derandomization_author_proof_v1.md`

SHA256 `8a20ac9d1d0a9381621ff7560e1c3f985db072dba4aafae8125c4c846d54fbad`。

对应不改的 Exact：`finite_grid_label_mask_log_potential_derandomization_statement_only_v1.md`，SHA256 `b6056384c47ed7b201a5666ac0750492fe717d7692aa23d6d775f225fb331165`。

不改的先行 Exact-only 记录：`finite_grid_label_mask_log_potential_derandomization_v1_independent_review.md`，SHA256 `25448b56a0ed6022cfe340c5c1b647f3d7bdbdc7726fd2aa673e601e01ab3633`。

结论：**PASS。作者 Proof 与先行独立重构一致，未发现数学、误差、位复杂度或全局物理不交性方面的 fatal。** 作者/root 此前已推导机制，且此作者文档在 root 实读独立记录后写出；不将 root 记作 blind reviewer，也不把这份后写文档冒称在未见 reviewer 记录下冻结的另一份独立证明。

本次认证仅限该有限格点去随机工具及明确额外前提下的实际item不交后果，不包含下游NSW、常数、source归约或general UM ratio。

## 2. Grid DP 与所有合法概率分支

h_ij=Qw_ij确为非负整数且每行总量<=Q，因此每agent的保留质量有Q+1个整数格点。作者先去掉Σ_i ln V_i常数是合法的：同一常数加在实际势和其期望上，不需表示它或期待值为有理数。

对正概率prefix，独立items的剩余分布维持原π。每agent的remaining mass由两项因子product给出，degree<=Q，DP为精确rational概率，而非只计算均值或将agent质量视为确定值。不同agents间可以相关，线性求和条件期望仍成立，不需要agent独立。

作者给的common-denominator numerator递推正确。每一步coefficient非负且sum等于denominator product，bitlength受实际probability输入分母总位长控制；不因某π或prefix概率很小而按其倒数运行。π0/1、h0、空S和zero weights均合法。

candidate label固定以后，base按其真实h贡献更新，remaining DP不含这个已固定item。求table expectation时仅需对实际positive-probability support求和；base+remaining mass始终<=Q，zero-mass表外index不访问。这是作者所述“actual remaining DP”可直接实现的索引方式，与先行独立记录明确写出的零项省略一致，不是新增数学前提。

## 3. ε 精度与逐步实际条件期望

各表值−ln(ν_i+k/Q)近似absolute error<=α=ε/(2am)。DP每agent是mass1的分布，所以每candidate的rational估计absolute error<=aα。选择rational估计最小的positive-probability label，真实child期望至多最小真实child加2aα；最小真实child<=parent期望由全期望公式保证。因此m步总增加<=2amα=ε。

这一步不对positive label概率作数值下界假设，不除以child概率，也不将近似positive值当作判定π>0的依据；合法labels直接用原精确rational π>0筛选。最后一个prefix的conditional expectation就是完整输出r的实际势，恢复V_i常数仅为数学等式。ties可用rational比较按固定顺序处理，不用判定一般irrational logs相等。

作者同时要求每个chosen label有正原输入概率，算法确按该限制决策，故每个prefix也真有正概率。这一保证包括label0（所有t_i在[1,L]，0可作中性label），并非逐agent独立选择不同item labels。

## 4. Log approximation 的自足位复杂度

作者给positive rational x作x=2^h y、1<=y<2，h的大小由分子分母bitlength控制；无需按x或1/x数值循环。z=(y−1)/(y+1)处于[0,1/3)，atanh幂级数的N项有理截断tail<=9^(−N)。ln2用z1/3同式，lnx的总error<=(|h|+1)9^(−N)。负h通过absolute |h|计账，x1或y1的z0亦无问题。

取N使上式<=α，N由input bits及log(1+1/α)多项式控制。每项rational power和2k+1 denominator的bitlength与有限求和位长也为多项式。α=ε/(2am)只增加log a、log m与log(1+1/ε) precision，不创建1/ε个对象。ε本身是输入positive binary rational，其编码位长计入总输入。

所有log arguments ν_i+k/Q均严格正，包括k0和极小ν；V_i、ν_i正的semantic前提没有被忽略。算法从不按1/ν或1/π展开。误差为绝对加性，允许logs正负，也无需假设每项log非负或设置未知期望上界。

## 5. Q 数值收费、空分支及总输出

a(Q+1)个log值、每个candidate剩余DP及有限表求和，即使从头重算也在poly(inputbits,a,m,L,Q,log(1+1/ε))内；Q确按value收费，而非只按logQ。任意巨大binary Q下这只是pseudo-polynomial格点算法，不应称统一bit-polynomial。应用Q=4m在m>=1且m显式时可转为真实输入位多项式；本工具未认证某个下游具体输入确满足该关系。

m0直接返回空labeling，各W_i确定为0，势与期望相等；a0逐item取第一个positive-probability label，势恒0。两分支不计算α或除以空参数；m0不把Q4m=0引入要求Q正的常规分支。所有S空/weights零的非空实例也由普通DP覆盖。

输出是m个真实items各自唯一的一个label，索引与全表扫描按显式输入和L计费。DP和log近似均为binary integer/rational运算，未使用未知实际allocation、精确log/期望oracle或随机sampling。作者文档没有给实现认证，本次亦无软件或finite-numerical checks。

## 6. 真实全局 disjoint 后果与scope

附加physical结论严格使用fixed-label类内S_i pairwise-disjoint前提。若同一item j在两个不同agent的T中，同一个r_j同时等于t_i、t_h，故二者target相同；再由j∈S_i∩S_h违反该类内不交，矛盾。不同targets靠唯一global label防冲突，相同targets靠额外set前提防冲突。

zero weight items仍按T定义保留在此证明内；没有因为零质量而不算实物，空集合/空agent/item分支也成立。没有额外前提时，势条件期望保证本身不推出allocation全局不交。作者明确区分了两件事，与Exact同域。

本记录只冻结作者实读后的工具核对，旧Exact-only独立记录保持原身份与字节。没有读取或认证下游NSW完整Claim，也不预先认证任何尚未给定的canonical页面、源或常数。未来实际scope review应另冻。

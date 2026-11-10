# Set Cover列表可靠性的真实接口审读

## 阅读与版本

当前核心M-4db1e9e555294998a207d584ce22485f v2，pin 92cb20ca6cde5cda9ed6492d6cf33ed319cc55c1504ec7c6f17cc438fc3a79c0。本轮fresh窄续实际实读当前task、两条v2完整record、未变degree record、唯一源文字改动及round41成熟edge/review/ledger/receipt，复用已保存完整阅读和证明，不声称重新读整PDF。round41证书记录：完整shared body与Moshkovitz 2015冻结PDF全部15页（pp221–235），导出718行，逐段1–240、241–480、481–718连续读完；打印页228–229另渲染核公式。PDF原字节SHA51072837058066469129fdc62ad6b16725bce6ea97dfeb2110172b464cdfa1d7，导出和图均保存在已推送handoff包。

## 主结果及假设隔离

Theorem1.2对每个先固定的0<α<1，把SAT大小n多项式归约到SetCover universe大小N=n^{O(1/α)}的(1−α)lnN近似。算法排除再用P≠NP；SAT指数时间假设只用于规模/时间tradeoff的近最优解释。Theorem2.3为已证明的Dinur–Steurer重复接口，因此本主结果没有未证PGC前提。§5的CVP多项式硬度和MAX3LIN窗口硬度分别另需PGC与linear PGC。它们不迁移成UM makespan困难性或客户目录SPE付款。

共享body的唯一措辞勘误已应用并发布：source commit cc1ed1824283a5600246225c9a4055c804496785，registry commit 47bb9aef01e68c52a48e6e1c36c3a5b29644f270。本轮用新句恢复旧句后重得oldSHA60123b1d742c4ba9e9f1d5847e2454a3e5caa0bb32c4b9a009030ebecda325b0，确认只有此处从PGC依赖纠为已证明PCP/Dinur–Steurer，并保留CVP/MAX3LIN分别依赖PGC/linear PGC；当前newSHAee4b62663ff651341ae40162b5319b31b9230d71c93b81333d43cfbf92d4fb22。core与bridge记录只改变body SHA和version；原数学陈述与PDF不变。旧source_refresh_required待办已解决。

## 平方损失的承重句

有限LabelCover G=(A,B,E)，B非空；对任意单标签赋值，至少1−ε0比例的右点total disagreement。给每个a一个非空列表L_a，|L_a|≤ℓ。令q为存在两个不同邻居及列表内标签投影到同一右标签的右点比例。对每个此类右点固定一对见证。逐左点独立从其列表均匀取标签，这对见证同时抽中概率至少1/ℓ²，故随机单标签赋值的agreement比例期望至少q/ℓ²。每个赋值的agreement比例至多ε0，所以q≤ε0ℓ²。

这里是∀列表的比例上界，并由期望推出存在单标签见证；不是每次抽样均有同等agreement，也不允许把逐点ℓ改成平均列表预算。列表小于ℓ只令见证概率增大；空列表可先任意填标签再应用非空上界；若ℓ大于字母表可用实际列表大小≤ℓ的版本，不要求无意义的ℓ个互异标签。

作为core证明的一步，先付ε0≤η/ℓ²便得list-agreement(ℓ,η)。在Lemma4.4里ordinary edge error s=ε²D²，agreement error为2εD²=2D√s，因此充分收费为s≤η²/(4D²ℓ⁴)。原Corollary4.8使用更强的√s≤η/[2(Dℓ)²]，仍充分。固定D≥2为prime power、ℓ=polylog n时，Theorem2.3先把s压到所需polylog逆幂，再Lemma4.4/4.7；从未以固定常数ordinary error直接免费得到多对数列表。

## 从列表接口到SetCover仍需的步骤

此平方损失桥只支付Corollary4.8的列表可靠性转换。完整core还依赖已证明PCP/重复，degree reduction，合适参数的partition system（D取依赖内部误差的充分大常数），SetCover集合构造Sa,σ及Claim4.10计数。若假设小cover C，令sa为a标签集数、sb=Σa∈N(b)sa，则Σb sb=dA|C|。均值比阈值D ln|U|(1−η)小一段，所以好右点比例实际至少η/(1−η)>η（内部取0<η<1/2），不是仅用相等边界与≤η硬碰。对sb≤ℓ的好右点，其每个邻居sa≤ℓ，故截断每左点至多ℓ标签时保留全部有关见证；高sa邻居不可能出现于这种好右点。partition contrapositive再给列表agreement，矛盾。

最后取|U|约|B|^{1/η}，lnN约(1+η)ln|U|，把内部η按最终α重新选小（如η<α/3并留渐近余量），才得到最终(1−α)lnN。整数阈值用floor/ceil及足够大n吸收常数误差；不把实数ℓ字面称为列表基数。平方损失单独没有完成这些构造、复杂度或参数膨胀证明。

## 实际read-add后的端点核对

M-a324d647caf14545974f47d8cd0096c8当前v2，pin 7f840a47c36d154cdb7a5a6de0d28feea972a24156696bf738e926ca7fbeb5c7，本轮完整record实读；shared body与primary证据完整阅读沿round41证书复用，唯一source差异已实读核对。模型、逐点至多ℓ列表与同一投影图及∀列表agreement量词吻合Lemma4.7。已交一条accepted/unconditional局部贡献边，source仅此桥，target为本SetCover core；conditions固定普遍条件句的输入域，不是假定尚未证明的源存在性。

UM-LIST-AGREEMENT-DEGREE-BUDGET-v1 v1，pin 204c4c5b6a99aea65bf6dd8d0ba7c5845437a1f01719e1058ce7a897b07c892f，完整body和registered evidence精确section已读。ticket地板为L(D−1)/(2d+L(D−1))，全agreement整数阈值L≥ceil(2d/D)，同一私有符号映射的锐性仅指全agreement阈值；不称分数地板逐图锐。

因此，**仅在其完整共同子域**（简单(d,D)双正则、D≥2、B非空、每右点邻居投影像公共交非空、不同邻居agreement、逐点列表≤L）下，若每个列表的agreement比例≤η<1，便必要有

    d/L ≥ (D−1)(1−η)/(2η),   L < ceil(2d/D).

若再由ordinary agreement ε0经平方损失得到η=ε0L²，则必要ε0≥(D−1)/[L(2d+L(D−1))]；这是有全部附加假设的兼容性检查。固定D而L增长，会在此子域强制d至少线性随L；Corollary4.8只固定右度D，从未声称左度d也是常数，所以即使该附加域成立也没有冲突。

本次primary定义仅给一般有限投影π_e，Theorem2.3/Cor4.8所列接口没有证明NO输入每右点所有邻居像公共交非空，也不能凭同名“LabelCover”补简单性与不同邻居条件。完美YES完整性只在YES输入给共同标签，不能把该另一个输入的见证移给NO。故本包不把degreefloor强加core全部来源，也不造degree→core逻辑边；共同子域里的精确必要不等式留在这份review供后续实际源核对。没有需要继续发布的具体3B/3C问题。

## 一般LabelCover定义不能补common-image的精确原因

甚至简单双正则也不够：A={a1,a2}、B={b}，d=1,D=2；ΣA={0}、ΣB={0,1}，两条边分别把0投成0与1。每个左点唯一非空列表都不在b agreement，公共像交为空。这只说明一般投影图定义不蕴含共同像条件，不声称此两边图是Moshkovitz PCP输出，也不反驳附有共同像假设的度预算定理。YES存在完美满足赋值会在每个b给共同投影值，但NO实例不能从YES的另一个输入获得这个见证。

## 最终覆盖与交付边界

任务当前owner Boss6，fresh claim request21edbd06c9b143e0b868b1e29fcdde81；派工确认pushed remote ef0813035c68c654927c3e8314f9ccb24fc61347。历史claim53c206b59bbf4b70bd497bcedfe9bfa2/read-add66c9893775944572b2e1da7ae64f290e只保阅读追溯，不作当前请求。核心覆盖linked，由一条accepted/unconditional局部贡献边支持；完整Theorem1.2本来已经proved，本边不替代全部原证明。精确ID检索未发现同core/桥canonical关系可复用；degree现有context检查边不是本关系，不重复。任务没有声明overlap_comparisons，follow_up_tasks与closed_overlaps均为空。

本轮fresh窄续已完成唯一文字差异及当前记录/任务核对，边的body evidence SHA、endpoint pins和review binding已在仓库外重算，receipt与ledger同步当前pin/request。原accepted/unconditional局部贡献及所有未付步骤保持原范围；degree域缺口没有变成迁移边。Boss可串行安装、edge-bind --write、edge-check、checkpoint pushed后done。没有重跑PDF导出、旧程序、LP或大规模实验。

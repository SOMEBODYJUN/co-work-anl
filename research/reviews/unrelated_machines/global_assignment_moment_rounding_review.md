# 全局任务矩近平坦提取与全HS反例的独立攻击和整合审查

本记录区分原始证明审查、独立程序审计和本次canonical整合复核。没有外部同行评审；没有一般矩生成或大缺陷近似定理。主目标UM-TARGET-v1仍OPEN。

## 1. 被审对象与冻结指针

精确Claim为`UM-GLOBAL-MOMENT-NEARFLAT-EXTRACTION-v1`和`UM-GLOBAL-MOMENT-HS-GREEDY-GAP-v1`。

原始证明及实现配对：

- `nearflat_greedy_hs_v2_proof.md` SHA-256 `8b3b90534f98d618381d50edada9035edadc5d48b5afcd3afd21b1fe94803d99`。
- 主实现v2 SHA-256 `8689cf87672e859875c880143db95c4c7861fa9b2a24df99792c4e7cd8cbf440`；canonical `nearflat_moment_extraction.py`与其原字节相同，仅外部路径不同。
- 独立HS脚本 SHA-256 `01fe0eec81d789d685e2bf264ecb2ebc896153939b27f9f216f35d4e7f866927`。
- 独立脚本所用既有有理工具 SHA-256 `1dfcaee91aaa6886dae201f5b796decbab9e2b667bb96ff24285a6a00c118666`。
- 全HS二倍反例脚本 SHA-256 `9adc3f3a95346b944b1169990c9be64b64ab4993e5f2e4fa8b67a8c9421edcda`。

原始独立证明审查为scratch `near_flat_hs_independent_review.md`；它完整重构了压缩算子、前缀近幂等、HS不塌缩、逐端loss、所有机器负载、位复杂度及NP生成边界。全HS反例由另一研究者statement-first构造，在未读近平坦证明前定位；冻结结论改用Fraction而非预搜索浮点。此次整合研究者先读上述实际原稿与代码，再逐不等式复核，不将其冒充另一次盲审。

canonical正文被审冻结hash和复制文件hash同时记录于[包证书](../../../evidence/certificates/unrelated_machines/global_assignment_moment_freeze.json)。canonical正文后续若变动，应另记录所审hash，不能自动把本记录覆盖到任意新版本。

## 2. 独立重构的承重点

1. **零范数商上的乘法良定。** 对degree≤1的q，PSD及布尔理想给`||x_eq||²=L(q x_eq)`；q为零向量即使右侧为0。因此X_e良定，无需flat、真实分布或entrywise四阶非负。
2. **共同残差与交换子。** `D_e=B_e*B_e`及`[A_e,A_f]=B_f*B_e−B_e*B_f`来自同一M2，不从独立pair数据拼合。零常数state缺陷不能替代全空间δ；每个合法证书在v0上均为0。
3. **近幂等乘积不假设自伴。** K²重排时任意一对不同位置最多交换一次；collapse平方后总误差≤`(Σ√δ_e)²≤nδ`。`||K||(1−||K||)≤||K−K²||`对非正规K也成立，因为`||K²||≤||K||²`。
4. **HS最大选择不累计指数概率损失。** 分支HS平方和≥1/8，最大分支opnorm≥1/√(8dR)。配合NF排除近0的幂等分支，保持opnorm≥1−2nδ。δ=0单独处理，不能用`2a>a`来覆盖a=0。
5. **linear-loss而非sqrt-loss。** `I−A=(I−A)²+D`使selected loss≤`[Rγ²+δ_e]/h`，再用`1184/961<3`。`tr(K†D_eK)≤tr D_e`使用K为contraction和D_e正性。没有把ρ解释成调度分布。
6. **全机器同一分配。** 只丢弃非负未选端贡献；逐机由同一ρ得到`L_i≤T+3Σselected p_eδ_e`。更强(1+3δ)界明确要求已剪p_e≤T。未剪枝只能先得`T/(1−3δ)≤(1+η)T`。
7. **总位复杂度。** 只有有理逆、乘、迹和exact PSD，不用谱分解、随机试验或未实现oracle。K乘积长度≤n，不按1/δ循环，分母乘积位长线性随n累加，故总位复杂度闭合。
8. **生成器量词。** 假定总位多项式生成器只需YES承诺成功、NO可任意输出，仍可用验证和实际提取决定半单位3DM YES/NO。因此原T强近平坦生成不是普通未解决子步骤；P≠NP下不存在。

未发现上述证明仍成立的fatal objection。

## 3. 已处理的合同与实现风险

- **旧原型额外前提。** 早期工具校验prefix-count localizer，并逐个要求存储moment非负；本文NF证明不使用它们。主实现v2已独立写`validate_required`，仅检查normalized Boolean/one-hot、M1/M2 PSD和row-load localizer PSD。derived operator检查来自这些前提，不是额外输入假设。旧冻结输出保留原字节，没有为适配新合同改写旧证据。
- **独立运行的较强测试域。** 独立HS脚本仍导入更强工具validator；其测试输入都是真实分布，额外检查成立。因此此运行支持实现交叉核验，不声称覆盖所有只满足C2-load的伪矩。理论的较弱合同由独立证明及主validator承担。
- **稀有权并不自动给小全空间缺陷。** 原子若新增V1方向，其小权可能被Gram归一化抵消。主fixture使用V1 rank不变3、M2 rank从3增至4的四角结构；独立fixture先以6个affinely independent支持张满V1，再给其余2个支持稀有权，rank为6/8。
- **冻结路径与源码hash。** 所复制主源和独立源均与JSON的source hash匹配。全HS旧JSON没有源码hash字段，因此另以包证书登记其代码与结果双hash；不虚称旧JSON原已含hash。
- **数据接口与造矩原子分离。** fixtures使用真实调度造矩，核心`greedy_hs`不接收原子。实际四阶矩已保存于examples，不将已知原分布当提取oracle。
- **零目标API范围。** n=0由核心API直接返回空分配；T=0核心仍先检查NF，可拒绝大δ零矩。原模型T0直接选零端是外层预处理范围，不能把该数学预处理说成v2已实现对所有零矩无条件返回调度。
- **未剪枝精细界。** v2接受未剪枝输入，其一般(1+η)界证明有效；canonical更精细(1+3δ)界只登记剪枝合同，避免将p_e≤T遗漏。

## 4. 本次真实重跑与有限范围

从canonical包的新路径运行，没有修改原冻结证据：

```bash
python3 tests/audits/unrelated_machines/nearflat_moment_extraction.py --output /tmp/nearflat_main_new.json
python3 tests/audits/unrelated_machines/near_flat_hs_independent_audit.py --output /tmp/nearflat_independent_new.json
python3 tests/audits/unrelated_machines/hs_effect_greedy_exact_m3.py > /tmp/full_hs_new.json
```

实际重跑输出保存在当次scratch，包证书登记重跑结果hash及与冻结JSON的比较。`/tmp`仅表示复现者应选择的新输出位置，不能覆盖已冻结结果。

- **主6例：** 1个flat；3个正时间非flat小δ；1个T0非flat小δ；1个大δ拒绝。含η1/2、1/10、零私人任务和大有理分母。逐prefix近幂等、逐selected loss和实际负载全部精确通过。主重跑JSON与冻结JSON完全相等。
- **独立21主例＋3边界：** 2个真正nonflat通过NF；19个普通大δ真矩不满足NF但仍实际运行；空任务、T0零私人任务、T0零effect端均输出合法零负载。其生成seed为20261016，随机一般例为3机4任务两端、时间{1/4,1/2,3/4,1}，完整枚举每例16个分配。19次无超T只说明该有限域，没有升级大δ贪心保证。
- **全HS精确反例：** 枚举全部210真实最优调度，exact构造17维基；验证每任务效果和I、每row负载算子为I；δ=66；首两处平局和后7处严格差值；实际输出负载(1,2,0)。重跑JSON与冻结JSON完全相等。
- **数字常数：** 以Fraction核`(37/32)/(31/32)^2=1184/961<3`，`1+3/64=67/64<3/2`及两者差`29/64`。没有用浮点舍入决定正负。

## 5. 未覆盖与准确价值判断

没有证明一般输入可生成适用证书，没有运行通用SDP求解器，没有对全部合法伪矩做穷尽测试，也没有主目标的统一ε。全HS反例只约束指定big-first规则；任务顺序、rank1初始化、其他效果更新及容量增广证书不在该反例的否定范围。

公屏252另报告针对rank1-state规则的真实二倍实例；本稿冻结时该独立资产尚未推送，本稿未借用其尚未重构的证据。它应在任何rank1一般保证研究前核查。当前两Claim均未主张rank1一般保证，故不受该报告的fatal攻击；本稿m3实例上的rank1成功也不能反驳该报告。

平坦部分属于经典机制。本稿新增可回收内容是定量全空间缺陷到确定性有理HS提取的具体接口，以及无NF时同一规则的实际二倍反例。其全球新颖性和独立论文价值仍待检索与外部专家判断。它是经过精确核验的条件性工具和方法边界，不能据此声称已跨过一般2近似壁垒。

## 6. 入库空白规范化与冻结指纹的精确关系

checkpoint的git diff --cached --check识别正文第13、16、18行的空白行含两个尾空格；本次仅将这三行改为单换行，数学文字及全部公式未变。现行正文SHA256为`c49e7d8dd13757f16ce6bd451c32999966739bed9be5c40d0bade4fce63cb1f0`。在现行正文这三行的换行前各恢复两个ASCII空格，逐字节得到包证书所记录的冻结正文SHA256 `5ec060ea153b2044de1c45395e7eec9db8dbc59a0769f38a86d5ff70dbd538b3`，root已实际反算核对。原包证书和三份冻结运行JSON保持原字节，不能把其中旧源hash说成现行规范化字节。

本节之前的本审查字节（保留其原末尾换行）SHA256为`ad9af3b95c68d1f5702ee928e62ec29ce9d0430d2c2f122e9afd30af44a4c352`，即包证书所记的原审查源；本节只是入库规范化与可恢复性说明，不升级独立审查或数学状态。

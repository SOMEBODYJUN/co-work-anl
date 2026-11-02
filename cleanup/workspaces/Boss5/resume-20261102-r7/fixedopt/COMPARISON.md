# A-fixedopt 十源与成熟正文的实读比较

本稿是 Boss5 内部比较者的知情阅读记录。只读结果仓库，不运行 `work.py`、Git 写入或数学程序，不修改共享正文。父清洗者负责逐源完整阅读、字节核对、最终 receipts 和推送；本稿不代替这些工作，也不预记 done。

仓库根：`/workspace/scratch/576451d28005/co-work-anl-boss5`。来源组：`/workspace/scratch/576451d28005/boss5-round7/A-fixedopt`。十份来源已有可继续使用的正式承接；本次找到一项需最小补充到已有程序正文的异常控制流边界，不需新造数学对象。这个判断来自下列正文、证明和原程序的实际阅读，不是采用证据 README 的完成声明。

## 实际阅读范围

下列十二篇正式文件均全文读取。路径都相对于仓库根。

| 正式路径 | 本次具体核对 |
| --- | --- |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | 单位客户均分、全部有序历史、重复/空主题、完整纯 SPE 量词，计数压缩与给定策略的区别 |
| `archives/customer-attraction/state/反例/固定最优遗漏私有化的完整可信性分离--反例.md` | 36客户构造、原43节点策略、指定全Y改造、全部新SPE的BI排除、有利全X量词边界 |
| `archives/customer-attraction/state/候选/存在最优遗漏私有化与有限关联下降--候选.md` | E-path/count/cover/defect 精确层级，OPT/旧叶收益保持，严格 incidence 下降与别名处理 |
| `archives/customer-attraction/state/程序/指定最优私有化的有序历史独立审计--程序.md` | 258项比较、259历史状态、旧48路径、新六Y排列、输入与写报告副作用合同 |
| `archives/customer-attraction/state/程序/可信全菜单与遗漏私有化的双攻击合同--程序.md` | C26锥的两个交替LP和20起点记录；P0的300提案、33原终局、任意兴趣owner与计数保留 |
| `archives/customer-attraction/state/审查/可信惩罚入口的逐人全菜单与遗漏私有化量词--审查.md` | 保当前槽核与删槽核的区别；后来六人银行反例及私有化的量词边界 |
| `archives/customer-attraction/state/定理/实际遗漏私有席位谱与锐界--定理.md` | 真实触块次数残余引理、实际每位置零触及、前m大席位求和、条件锐界及整数匹配族 |
| `archives/customer-attraction/state/反例/三人聚合末位保底--反例.md` | 同一36客户底层、216叶分类、原完整策略及原结论并非half反例 |
| `archives/customer-attraction/state/反例/银行完整根列的两查询最小分离--反例.md` | 全列两查询下界、精确Mfull匹配、m2/m3边界和恰六人数值 |
| `archives/customer-attraction/state/资源/净遗漏预算与最优前缀付款的历史接口--资源.md` | R65私有化尚未成立的历史接口，真实离轨后继变化，未将“尚无变换”误写成一般不可能 |
| `archives/customer-attraction/state/障碍/实际遗漏客户删除与可信根门槛的无界敏感性--障碍.md` | 五人五主题全参数切分、六前缀删除切口、单名客户无界门槛影响及其适用边界 |
| `archives/customer-attraction/state/审查/全部实际后缀包络的单位展开独审与两报告绑定--审查.md` | 后续all-owner有限诊断的历史地位；未补造已删除程序/输出或转授E-*量词 |

另全文读取两个证据包的 `README.md`：

- `archives/customer-attraction/tools/evidence/boss5-credible-primary/README.md`
- `archives/customer-attraction/tools/evidence/fixed-optimal-ordered-audit-primary/README.md`

原来源方面，本比较者全文读取了 `existential_privatization_obligation.md` 与 `fixed_optimum_privatization_counterexample.md` 两稿，以实际旧文对照成熟正文；并在父方发现异常控制流后独立全文读取 `full_menu_cone_attack.py` 4725B原程序核对。其他七源的逐行代码/报告阅读由父清洗者承担，本稿不声称自己逐行读取了那七源。对《实际遗漏客户减半的三人非单调可实现性》只读到部分输出，不将它计为全文阅读或本次结论的必要依赖。

## 十源精确映射和独有内容去向

两冻结提交是 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；完整 source refs 由组内 `sources.json` 保留。下表的源路径前缀统一为 `research/workspaces/customer-attraction/R-f81c243529cf49a0a454fba6708cf80f/`。不是把两个冻结版本当作两项数学发现。

| 源ID | 前缀后的原路径 | 已有正式承接 | 独有内容与区别 |
| --- | --- | --- | --- |
| `4974e352431c73b4e37a` | `branch_transport/audit_fixed_opt_privatization.py` | `state/程序/指定最优私有化的有序历史独立审计--程序.md` | 后续独立单位展开，完整有序历史缓存；不导入发现者或规范solver。独有实现身份和恢复旧路径的运行合同已保留 |
| `ee6a1c03f2219b5b4d85` | `branch_transport/audit_fixed_opt_privatization_report.json` | 同上；另供固定最优反例页比较 | 旧48可实现有序路径、新六Y排列、全部根分支与Y0末位表、有利全X仍保原有序z。独立PASS不倒填原自审的历史状态 |
| `57ebc3f6b881caee5b04` | `credible_attack/audit_fixed_optimum_privatization.py` | `state/反例/固定最优遗漏私有化的完整可信性分离--反例.md` | 发现者自含Fraction构造、原完整策略自审及全部新SPE可实现叶递推；与后续独审区分 |
| `c3cb151a34bd6c3969ff` | `credible_attack/existential_privatization_obligation.md` | `state/候选/存在最优遗漏私有化与有限关联下降--候选.md` | 四层存在C候选、条件有限下降、逐单位owner、别名映射和真正反例义务均保留 |
| `b743682de73fdaae3396` | `credible_attack/fixed_optimum_privatization_audit.json` | 固定最优反例页 | 原自审的精确输出及“独审待定”的历史时态；未与后续独审报告合并成同一执行事件 |
| `d0ead8d8ee65341e2289` | `credible_attack/fixed_optimum_privatization_counterexample.md` | 固定最优反例页 | 固定全Y最优C会迫使所有新SPE福利36，否定固定C保福利；底层36客户例复用而非新发现 |
| `0f986c2cee2fe0d124ed` | `credible_attack/full_menu_cone_attack.py` | `state/程序/可信全菜单与遗漏私有化的双攻击合同--程序.md` | 固定另一份34客户完整策略、63非空兴趣质量锥、258行SPE约束、交替优化查询和质量；未穷尽策略或证明全锥上界。新核权重LP失败后未初始化/跨起点旧weights的异常边界，应最小补充到此已有正文 |
| `f0f9a4156d755de4da13` | `credible_attack/full_menu_discovery.json` | 同上 | 20起点的末轮gap、一个最佳trace及完整p/w；浮点有限阴性记录，不是精确无分离证书 |
| `573e119ed5246e43a291` | `credible_attack/privatization_attack.py` | 同上 | 三人五主题随机单位输入；owner允许任意原兴趣，精确检查原计数能否在某新完整SPE实现；不检验E-defect精确量词 |
| `51eb1fa5fa710be8e509` | `credible_attack/privatization_discovery.json` | 同上 | seed、300提案、33原终局的有限阴性；没有逐提案/owner账本，成熟正文没有补造 |

上表 `state/...` 路径均以 `archives/customer-attraction/` 为根。三份核心承接的稳定ID分别为：

- `customer-attraction/fixed-optimal-omission-privatization-complete-credibility-separation`
- `customer-attraction/existential-optimal-omission-privatization-finite-incidence-descent`
- `customer-attraction/credible-full-menu-and-omission-privatization-two-attack-contracts`

后续独审资源ID为 `customer-attraction/fixed-optimal-privatization-ordered-history-independent-audit`。它不是第四个不同底层游戏。

## 数学检查与已吸收纠错

原36客户例取三人六主题。全X与全Y均覆盖36客户，原完整SPE实际路径为 `(X0,Y0,Y1)`，收益 `(10,12,12)`，福利34。仅遗漏 `{X1,Y2}` 与 `{X2,Y2}` 两客户。固定全Y最优C后二者owner只能是Y2；旧叶收益不变，离轨末回复和惩罚者意愿却改变。集合值BI以每个孩子可实现的当前收益最小值取最大门槛，必要性由所有未选分支仍须为子SPE，充分性由各离轨子树独立选择达到最小值的完整子SPE。这个递推穷尽叶，而非限制同负载历史共用策略。

成熟正文已经修复原稿一处容易误读的措辞：X0根收益上界10只量化其 **子SPE续局**。任意非均衡叶 `(X0,X1,X2)` 给根12，故不能把它写成任意两后继主题的上界。成熟反例页及独审程序页均显式保留此区别。

新全Y私有化的根门槛12排除全部X根，全部新可实现叶是三个Y的六种排列、福利36。改用真正最优全X、两遗漏客户分别归X1/X2，则存在新完整SPE仍实现原有序路径。由此否定的是 **任意预先固定最优C** 的保福利合同；不存在“本例反驳存在最优C”或“本例反驳六人half”的推论。34与36都严格满足三人half。

存在C候选要求对每个实例及每份原完整SPE，存在某个真正最优C、每个单位客户的owner及某份新完整SPE。E-path⇒E-count⇒E-cover⇒E-defect；最弱仅要求新福利不增。逐主题只缩小且C覆盖保持，给OPT精确不变；修改客户原本均未被实际路径覆盖，给同一旧叶的收益不变。二者不能推出任何策略的激励不变。

E-defect若普遍成立，确可重复：最优遗漏如已有全局singleton兴趣则停止；否则至少一名被修改遗漏客户失去一条兴趣，有限非负整数incidence严格下降。停止时其唯一主题必为极大全局私有主题，可调用私有遗漏锐界；OPT保持、福利不增，传回初始实例得一般锐 `OPT_m≤(2−1/m)W`。这个推导逻辑有效，承重前提E-defect仍未证。逐单位选择、同覆盖标签、空遗漏、零福利与m1均未被偷换。

P0与E-defect交叉地强弱不同：P0允许更宽的任意原兴趣owner，却要求更强的原计数可实现；E-defect限制owner来自可选最优C，却仅要求某新SPE福利不增。300提案、33原终局的阴性不认证E-defect，也不认证一般P0。

C26使用保留原当前槽的完整m槽真实菜单核，额外1为静态插入查询。其三人固定策略锥的有限阴性已由成熟正文正确保为历史实验。后来完整银行列给恰六人 `u1=6/5`、两查询对全部30列至少 `17/12`、精确Mfull=`53/30`；因此C26当前为假。该六人银行实际W12、OPT16，仍不是half反例。不能把C26或固定C的失败迁移为E-defect失败。

### 权重LP失败后的原实现边界

父清洗者先指出这一独有实现细节，本比较者随后全文读原程序独立确认。`weights` 只在权重LP成功后由 `sol.x[:-1]` 赋值，每个新起点没有重置；失败分支只记一项 `weight_lp_status` 后跳出内层轮次循环，接着仍执行 `weights.tolist()`。因此首起点第一轮失败会产生 `UnboundLocalError`；后续起点第一轮失败可能取到上一起点在函数作用域留下的 `weights`；若本起点此前已成功，则保本起点最近成功的一份质量。查询LP失败另有 `assert ps.success`，会直接中止。

失败起点最后trace项没有 `best_p_gap`，`best`排序给其−1e9、对应 `gaps`记录为null；这条异常边界不等于冻结最佳点已经污染。成熟正文所保冻结20个gap都为数值，最佳点有六轮成功trace，故无证据指向其经历了该失败路径。本次不触发失败来新增运行事件，也不倒填原未保存的每轮LP原始状态。正确处置是补足程序合同及其错误处理限制，保留冻结成功记录的有限观察身份。

## 后续状态检索和删除障碍的边界

本次在全仓 `archives` 中检索固定OPT/最优私有化、R-f81路径及后续词项，再针对 customer-attraction 正式state和six-providers正式state检索 `E-path/E-count/E-cover/E-defect`、`existential`、`私有化` 和纠错/修正词。检索结果所指核心正文及上述相关正文已按表阅读；未找到后来证明或反驳存在最优E-*候选的正式结果。这是本次检索与实读范围内的状态判断，不声称穷尽所有未清洗来源。

《实际遗漏客户删除与可信根门槛的无界敏感性》的稳定ID为 `customer-attraction/omitted-client-deletion-and-unbounded-credible-root-sensitivity`。五人五主题固定35个covered客户，E-private参数t使目标计数 `(2,1,0,0,2)` 可实现当且仅当t≥3/4；在t1删唯一E-private客户到t0后，允许重选全部策略仍不能保目标。根可信门槛从7升到33/4。整数化q=4s+1时只删一个实际单位客户，门槛差 `(5/4)q` 无界。其六个第二次F前缀切口完整排除所有目标顺序，而不仅排除原策略。

该删除操作改变客户总数和OPT，不是将遗漏兴趣缩到最优C内owner且保持OPT的变换；结论是保目标删除接口和统一绝对Lipschitz门槛界失败。它支持“旧叶收益不变不足以保可信性”的机制联系，不反驳E-defect，也不提供六人half反例。

后来《全部实际后缀包络的单位展开独审与两报告绑定》记载过all-owner有限诊断：无反例、无正定理；原冗余代码和输出已按当时父方要求删除。该正式审查明确没有补猜其参数或日志，也没有转授E-*的最优C与福利量词。本比较不把这句历史收尾当成新有限扫描证据。

## 关系判断和工作边界

这些关系可供第三阶段使用，但本稿不宣称建立完成三级超图：

- 36客户聚合例→固定最优私有化反例：同一构造与原完整策略复用；新结论只在指定改造后的可信叶集合。
- 原自审与后续有序独审→固定C反例：两个不同实现/历史事件的精确有限支撑；不是外部同行评审。
- 固定C反例→存在C候选：量词障碍和必要边界；全X的成功恰阻断将其移作存在C反例。
- E-defect及私有遗漏锐界→一般锐福利界：多前提条件推导；前提E-defect未成立。
- 全菜单锥→C26：有限寻找分离的观察；完整银行SPE→C26：真实反驳。两种关系不能混用。
- 删除敏感性→私有化讨论：机制提示和不可迁移边界；操作不保持OPT、目标又只保计数，所以不是E-defect反例。

本比较者的新数学程序运行、BI枚举、LP、随机扫描、原审计重放均为 **0次**。工具执行限于只读正文/检索和写本比较稿；未调用规范solver或导入带顶层副作用的旧程序。没有新独立盲审、外审或新颖性声明。父方的静态SHA/字节/链接核验须以父方自身记录为准。

自查：上表十源ID逐一对照组内 `sources.json`；十二正式路径和两README路径均在当前仓库存在；核心稳定ID按正文frontmatter核对。本文区分三人与六人、固定C与存在C、给定策略与可实现叶、原路径/计数/覆盖/福利、有限阴性与真反例，并明确正文复用、唯一程序合同补充及未新增正式对象的理由。

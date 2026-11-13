# 12核心Cartesian端点定向刷新

## 变更及阅读界限

本轮沿Boss6、任务 `boss6-cartesian-peer-refresh-repair-ec71fbe2d8764a14`，读取其任务原文、当前22个登记端点、被替代任务及收据、11条旧关系，并按实际承重部分复核成熟证明。Git、队列、绑定及发布由Root串行操作。

新旧任务22项input pins仅一项不同：`customer-attraction/cartesian-efficient-factors-welfare-counterexample` 从 `7c81389f0d5158b6073c91f940a64e429a95d8c4a120ba358f24e096bfe39734` 变为 `7ff89d8baec9d48c8ed5084a878e5dbbc5aaf6549fe061845deb7952d4996d94`。其body原始字节SHA仍是 `4a107a28ae3d2dd8aa8d67a1f6e72359936003a1ee36002916b7e9d7a25091b6`。浅历史没有给旧登记全文，本说明不臆测历史文字差异；按现行v2逐项审其准确模型、参数和证明，确认旧福利checks的数学仍正确、端点绑定需刷新。其余21端点未变。

旧收据成熟实读和独立核验继续作为历史工作复用。本轮没有把任务中扩大到约1.59M估计tokens的全部62证据文件重新全量执行或逐行重读。直接重读当前福利反例、全体玩家PU定理、有限Cartesian审计，任意背景/单背景回路、固定图二倍证书和Big6反例的承重解析部分；并行审读旧其余5边与各承重正文，核当前证据字节。程序本身、巨大原JSON、旧LP/BI/全树输出均保其历史运行身份。

## 福利反例：独立动作空间仍容许耦合后继

完整目录是三行与两色的六标签Cartesian积，单位客户块大小为a、q，整数a≥1、q≥a。末位选未用行；两色均已出现时末位自己选任一色都得q/2，但可根据过去经济行决定分享谁的颜色。这一合法历史依赖平局改变已行动玩家支付，不能因终局收益逐坐标相加或分量福利固定就认定每份联合SPE投影都是分量SPE。

第二人遵从同行异色，收益a/2+q；真实换到异行（无论是否换色）后由同一完整策略续完，收益a+q/2，差(q−a)/2≥0。同行同色差q/2。根任何六动作都得(a+q)/2。末位各坐标真实最佳且完整配对均合法，所以全部43有序决策历史的规则构成完整纯SPE。实际三标签0,1,2代表(0,0),(0,1),(1,0)，只覆盖两行两色；W=2a+2q，OPT=3a+2q，损失a>0。它只给联合最差福利≤这份W，不声称该策略是最坏或全部联合SPE已枚举。

本轮小算术独立从单位块份额重建每次真实偏离的完整后继，将所有258项差写成A·a+B·(q−a)。43节点的A、B均非负；记录见同目录 `independent-cartesian-coefficient-check.json`。这穷尽一个有限策略的符号IC而不抽样参数；任意参数结论仍有上述解析理由。旧审计七参数的两分量全集、216联合终局OPT和匹配v3仍作为有限原回归；本轮未重跑它们。

行分量中，第二人选新行得a而重复得a/2，末位总选剩余未用行，故每份分量SPE覆盖3a。色分量前两人同色时末位严格换色，异色则已全覆盖，故每份分量SPE福利2q。失败的是这两个分量最差SPE福利的自动组合，不是静态OPT、静态收益或安全值的可加。

## PU充分定理及有限证据

PU要求每分量每个有序子历史的所有完整SPE给全部m位玩家相同收益向量，包含已经行动者。归纳到某联合行动孩子，当前玩家已在其分量前缀行动；正是该过去玩家量词令孩子收益F_j(a_j)不受其它坐标行动及耦合选择影响。完整Cartesian动作允许单改坐标，当前最优性才推出各坐标最优；各有序子树独立拼接实现投影。反向独立乘积SPE不需PU。于是终局集合相等、再以不交客户福利求最小才得福利可加。

本福利反例的色分量在异色末节点，两名过去玩家向量为(q/2,q)或(q,q/2)，故不满足PU，二者无矛盾。旧80候选中的47个PU通过项只核根终局集合投影，普遍全子历史等式由解析归纳承担。两条旧Cartesian checks保持context，不升格逻辑边或所有策略分解，不外推有限证据为全称定理。本包没有已确认而未处理的共同价格补偿比较；原未指定的大量deferred候选不冒作已读前提。

## 其余成熟关系逐条处置

| 旧文件 | 保留作用及实际数学理由 |
| --- | --- |
| hidden-credit-to-single-background.json | whole。h=t e_c时V=tU_c，以同一客户把C_b=(r+s)U_b(q0)+V_b(q0)，消去隐藏信用与过滤差得三补偿系数。ζ符号、r=s不除零及r=2s保持。 |
| hidden-credit-zero-background-fixed-policy.json | step。h=0,r=2,s=1给I24=I34=0，只消去固定034对124支付的−I24+I34；三真IC、五非负sharp和坐标支付仍各自承重，不宣称一般half。 |
| two-background-seven-slot-rank-boundary.json | context。两个独立背景的七槽行列式−1/155520只否固定七槽非零齐次恒等式。按z分层、增T_b、增查询或不等式仍可用，不否任意背景夹逼。 |
| individual-seat-counterexample-to-big-block-witness.json | whole，维持原conditional关系。所有历史跟随大块得6/(a+r)≥1，偏小块得1/(b_j+1)≤1，根1<非法单席6但合法第六席恰1。两人路线的未来0须计入k=2；不是half反例，也不反所有路线修补。 |
| complete-outcome-recursion-to-omitted-client-threshold.json | whole。真实孩子全集min-max门槛与有序子树拼接给充分必要，弱序分区的129代表覆盖完整参数域。k=4s+1使删一客跨3/4，门槛增5k/4；不是只抽129点外推。 |
| convex-five-root-payment-fixed-projection.json | whole，ALL两输入不拆。五行真实IC/地板与凸共同匹配分离联合使严格负八态上包络连放宽拆分也不可能。固定64质量、实际会员、AE/second边缘不可取消，不推所有松弛点失败。 |
| exact-ab-cuts-to-fixed-query-graph-extensions.json | step。两条精确非负整数权分别排priced33及独立旧697的13支持，保其完整隐藏直方图域。每原子6336列；33/13支持分别209088/82368。raw28、整个1118/3088系统及六个受限词浮点报告仍不由本边解决。 |
| fixed-two-tail-tax-to-same-load-prefix.json | whole。同目录同负载的任一真两人SPE给尾税上界，控制查询后原策略实际尾对；与当前真IC联合后在c=0,1,2端点取最小得到全λ≥0式。无需让不同有序前缀选同一尾策略，旧437四折点只限固定点。 |
| off-support-slot-budget-to-actual-cap.json | step。整数倒数支撑线给E N_out≥6/25，排纯actual支持背景。删位值3、全目录cap≤5/2另有证书；T-only取等混合A查询为5，不是全部查询共同最优性。 |
| cartesian-audit-finite-payoff-unique-check.json | context，原字节复用。全m维PU筛选与47根投影检查准确，不自动证明所有子博弈普遍归纳。 |
| cartesian-audit-finite-welfare-check.json | context，同路径定向更新审读与当前绑定；七冻结样本有限检查保原范围。 |

三人I的遗漏量2→1→0为可实现→不可实现→恢复，五人参数族是另一域、单删客户无界门槛敏感性；无相互推导或同域被否目标，保原isolated coverage。七槽满秩亦只保context。12核心原有9 linked、3 isolated-after-review分类按收据实际值承接，不因目录或共享定义造hub。

## 固定前提、证据和开放义务

全部11条关系保premises_mode=all；每条原whole_result或contribution的作用范围保持。没有把回路身份单独当完整动态付款、没有把客户滤波IC符号免费保留、没有把有限证书当普遍half或统一菜单实现。

11项旧资产的原SHA全部匹配；28项唯一edge证据均在本地且SHA准确，包括参数分区 `48501a61ba3c7a3e3641a0bdff0d9e8d35e20f4f5da7178148106ab2ce28e0f6`。本轮唯一原路径改写为福利checks（任务明确授权），10条原字节保留。Root完成原生edge-bind后需将该一项最终SHA写入收据assets。两个原in-packet overlap已由对应whole/step关系解决，closed_overlaps明列；无待发布后续任务。

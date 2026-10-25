# 精确身份与状态

## HALF5-ORIGINAL

每个原 CAG-MODEL 的有限单位客户、非空有限共同目录、恰五名提供者及每个完整
有序历史依赖纯 SPE 都满足 OPT5<=2W。允许空主题、重复、零客户及任意历史平局。
**OPEN**。本轮没有目标反例或二倍证明。

## SHARED-MAX-HINGE5-v1

- 域/量词：同一原五人 SPE 的任意第三位有序历史，过去负载 p∈{0,1,2}，当前位置规定终局利润 v；两份任意五合法主题菜单的会员次数 d,j∈{0,...,5}；每个 t∈[0,35/2]。
- 结论：`40v-((35-2t)/5)Σ j/(p+3)-Σd/(p+1)+Σ2(d-t(p+1))_+/[(p+1)(p+3)]>=0`。
- 依赖：旧有背景 BNS 取剩余3、总人数5；同一个背景加权最大主题的目录 cap；非负组合及逐客户正部上界。
- 证据：自足解析推导；certificate、maxroot、父方内部独立核对；父方3024状态系数审计通过。完整参数族由13断点蕴含；不靠浮点网格外推。
- 限制：没有证明这些行联合实际收益可支付 OPT5/2；精确分离对象只是必要条件松弛。外审、新颖性未认证。
- 正文：root/shared_maximum_hinge_review.md；certificate/max_indexed_coupling.md 及精确分离证据；maxroot/weighted_hinge_independent_review.md。

## ACTUAL-UNION-WALLET5-v1

同域任意完整 SPE、任意合法 C，`4W-5u1-4|C|+|A1|>=0`；C最大大小K时有
`4W>=5u1+3K`。四个实际后位的真实分母保底 IC 权重为5/4,19/9,11/3,4，
64会员状态余项全非负。父方独立标准库核验通过。是旧 IC 的显示组合，非新
约束锥或福利界；没有外审/新颖性认证。

## TRUE-HQR-TABLE5-v1

- 域：原五人模型每份完整历史纯SPE、每个真实第三位历史；p为其客户过去负载，u为该当前优化者真实规定收益，M是原目录任意裸最大主题；两份任意五合法主题菜单会员数d,j。
- 结论：`17040u+1085|M|-2679Σj/(p+3)-ΣF(p,d)>=0`，F为正文3×6精确有理表。
- 依赖：该历史强制背景weighted最大H后的原σ真Q,R；原currentIC、H最大性、真末位IC、裸大小cap、已证两人税，七行非负组合后取隐藏位最大。
- 证据：作者144状态完整证书；父方不导入作者实现、从七原行独立重建全部144态及完整F表通过。任意第三源的范围是父方直接逐行推论，证明不需prefix包含M。
- 限制：没有封顶祖先变动利润；未证这些行足以支付2W。外审、新颖性未认证。正文certificate/trueH_seven_rows.md；父方root/trueH_seven_rows_review.md。

## WEIGHTED-H-COVERAGE-RESET5-v1

- 域：同模型任意真实第三位历史h，source真三尾A,B,E；同背景w=1/(p+3)最大合法H，强制H沿同σ真尾H,Q,R。
- 定义：K=w(H)，V_H为H强制者最终利润，eta=V_H-K；U_source,U_H均为包括完整过去覆盖的并集。
- 结论：`0<=eta<=u-K` 且 `|U_H minus U_source|<=24eta`，故相同两叶净福利升幅也<=24eta。
- 依赖：旧BNS精细强制H分支缺席账，source真末位比较H、H分支末位比较source E、同一H最大性及整数覆盖。当前IC只用于最后eta<=u-K投影；未遗漏旧玩家退款。
- 证据：自足解析证明与显式非负共同账户；父方独立核source kernel并强化eta，tree席另完整独立审查及展开账户。作者192态恒等式审计通过。外审、新颖性未认证。
- 限制：多个互斥source的eta尚无共同支付。若显式HQR系统已含全部承重原行，本关系不扩大其锥；非HALF5、非已失败的任意固定前缀reset归纳。
- 正文：direct/weighted_maximum_coverage_transfer.md；tree/coverage_reset_independent_review.md。

## SELECTED-TAIL-CREDIT5-v1

同域任意真实前三背景 q、实际末二 D,E。令 Gamma 为全局两槽调和势最大值减
实际两槽势；T 遍历可作为全局最大势对第一主题的合法主题，原真实末回 Q_T
仍达最大势；delta*=min_T u4(T,Q_T)，epsilon*=u4-delta*。
有 `delta*>=v5`，`0<=Gamma<=K=Gamma+epsilon*<=tax(D\\E)<=u4/2`。
`u1+u2+u3+K>=3v5` 为仍 OPEN 的充分条件，若成立可推出 half。
作者和 direct 席独立解析重构；六客户两主题完整 SPE 严格展示 K>Gamma。
没有将该充分桥提升为已证。

## TERMINAL-SHARE5-FAILURE

存在五人10单位客户、5主题完整 SPE，实际收益 `(3/2,3/2,3/2,2,7/2)`，
W=OPT5=10，故 `2W<6u5`。完整781历史策略、3124非自比较；父方另以10单位
客户独立回放3905含自比较通过。一般C2早已FALSE，此处只给明确五人证据并纠正
旧稿OPEN标签，非首次一般反例，非HALF5反例。正文 tree/terminal_share_and_padding.md。

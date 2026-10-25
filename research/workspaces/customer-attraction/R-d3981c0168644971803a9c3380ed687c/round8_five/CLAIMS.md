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

# Singleton 当前定向替代的 3D 审读

审读身份：Boss5 / 474257b8。结论：**RETAIN，无需小修**。当前已 done 的新边准确组合两份既有局部构造，完整支付同一登记目标；不需新数学任务。

本轮接续仓库中 round14-followups-3d-474257b8 的成熟具体审读。三份当时完整读取的数学源 SHA 均未变化。本轮完整读新任务、新收据、新边；定向重看当前三对象、singleton 证明段、包络§8和支持势证明段，复核旧资产身份与 pin。没有把这些接续核对声称为新的三源全文独立重读或额外独立证明。

## 当前正式身份与冻结值

- task：`round15-exact-edge-corrections-repair-74e19652d0cf7131`；当前 owner Boss1、state done，supersedes `boss5-474257b8-singleton-3b-602e0414fba69244`。
- task 文件 SHA256：`3222e611c83926d7d98148da32743ca260da9d7bc821ab564bfc64ff1c66aca7`。
- receipt 文件：`map/receipts/round15-exact-edge-corrections-repair-74e19652d0cf7131.json`。
- receipt SHA256：`91580e5d11c73cbe1030258c0954e5217f001f65322fbd06bbf9c7313744e878`。
- receipt canonical pin：`b72c49312a1972986306528abd5dc5032d238cea05b2a3a907ef5acc9fd3bb19`。
- edge：`singleton-ring-defect-envelope-and-support-give-minimum-threshold`；accepted / implies / ALL / unconditional / whole_result。
- edge 文件：`map/edges/round15-exact-edge-corrections-repair-74e19652d0cf7131/singleton-ring-defect-envelope-and-support-give-minimum-threshold.json`。
- edge SHA256：`0b5330ed7b04c09fbed03fc79be6d4ed7d7683c8847d7602e6ca8fc9c161741e`。
- edge canonical pin：`2cfee7888416677cca25d3afbeaee6916455c385d291229dc668dfa5d611e4e1`。
- edge review_digest：`aafafa36e3e27a256561bd2a94a4d87ce9c7ef345b950453c63dd183b873d46e`。

| endpoint | 当前 object pin |
| --- | --- |
| `WC-R1-RESOURCE-SUPPORT` | `f3251dcce0ad8790ada62d0e325c4c6f79efe3a9be7f5b8da0db2c4be09b27d0` |
| `WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1` | `fd14a44994955fb5ff9f4e2318b4b847ee18d1011a527b3e93e6ea77ec225162` |
| `weighted-congestion/singleton-cohort-ring-defect-graph-equilibrium` | `8ecd54dc4822bd40aec9d69056abba72674e218ad85adb0d2ba55622d7cfe0af` |

## 数学整条结论已付清

完整目标是在每个合法奇 m≥3、整数 d≥2、正实权重、位置内副本同费、非负系数次数≤d且允许零费用的真实单成员双动作环中，存在整域 min{2,T_d}-PNE，并另有 2m 单冲突商态之一的 T_d-PNE。成本不乘自身权，偏离重算自身真实新负载。

奇 m 的奇偶约束排除零冲突。固定一个冲突位置后，其余位关系确定状态至全局翻位，同费副本保证互补两态等成本，得到 2m 个商顶点。非邻接玩家翻位把两项 solo 变 shared，非负非减费用排除严格改善。相邻两人移动缺陷向左右；一条无向边两方向是同一玩家两种真实成本的互逆。因此 α≥1 时不能同时严格改善，零成本也成立。若所有池内状态都有严格出边，2m 条边必全被使用且同向。正向恰给 n_i=1 的两项 strict 测试，不能仅从一般两测试失败直接跳到存在均衡。

从 f_d(R)=[R(1+R)^d+1]/[(1+R)^d+R^(d+1)] 有 f_d(1)=1 且 f′_d(1)=(2^d−d−1)/(2^d+1)>0（d≥2），故 T_d>1。包络的正分母合同因此适用于 α=T_d，排除全环 strict 测试；没有严格 T_d 改善恰是目标的弱 T_d 稳定，端点已经包括。

零 F_i 使 A_i→B_i 的 solo-to-shared 比较不能严格改善；零 G_i 使下一项 B_i→A_(i+1) 不能严格改善。假想全 strict 循环中的形状于是非零，幅度可取一，包络的正分母可用。纯常数不能通过相应 strict 测试，混合常数由非负凸组合覆盖；不除成本，不出现 0/0。

反向取旧 i=−j mod m，并设 H′_j=L_i、L′_j=H_i、u′_j=v_i、v′_j=u_i。保留动作位，A′_j^b=A_i^b，B′_j^b=B_(i−1)^(1−b)，F′_j=F_i，G′_j=G_(i−1)。新 hub 的 incoming 与新 light 的 outgoing 恰是旧玩家原资源，故权重、资源使用、真实负载和偏离成本逐项保持。新正向 A′_j→B′_j→A′_(j+1) 恰对应旧逆向 A_i→B_(i−1)→A_(i−1)。这实际资源同构支付反取向，未只做形式的反序。

每个 A_i^b 的潜在用户只有 H_i,L_i，每个 B_i^b 只有 L_i,H_(i+1)。全纯态总成本最小点由 ΔΨ≤2C_i(new)−C_i(old)−C_common 得真实 2-PNE。该见证来自全域：T_d≤2 时取池内 T_d-PNE；2<T_d 时取全域 2-PNE，同时保留另一池内 T_d-PNE。两见证可以不同。没有推出池内 2-PNE、singleton 锐性或一般多成员结论。

## 两旧资产与 receipt

新收据中的三个核心均以当前 object pin linked 到这一条 whole ALL 边。独立 receipt 与任务嵌入 receipt 完全一致；endpoint、evidence、review digest、asset SHA 和两个唯一 section 逐项匹配。两旧资产全部且仅有以下 replaced，指向同一个新边。旧直接证据的并集与新边三项直接证据恰相同；原数学适用域和证明机制没有遗失。

| 旧资产 | SHA256 | 去向 |
| --- | --- | --- |
| `map/edges/boss5-474257b8-singleton-3b-602e0414fba69244/singleton-ring-defect-envelope-gives-single-conflict-pool-threshold.json` | `07656e65e721ba5622cb456ef3aee84ba5d95bb12b1d57ea60486b0d2d825e18` | replaced → 新 whole 边 |
| `map/edges/boss5-474257b8-singleton-3b-602e0414fba69244/singleton-ring-resource-support-gives-global-factor-two.json` | `bd8c9b9d9dd20ccc6efc0556988c489902f82171d90e79539d09895f6e907343` | replaced → 新 whole 边 |

本轮 20 项针对性身份、字节与绑定核验全通过。当前所读 `map/integration.json` 仍有旧任务及两旧边，尚无新任务/新边；这属于根接下来串行 assemble 要完成的投影状态，不是数学失败。接入新 done receipt 后，应由正式 supersession 移除两条旧 canonical 边。

## 可追加到 archive_reviews 的文字

Boss5/474257b8 接续既有 round14 singleton 审读，定向核当前已 done 的 round15-exact-edge-corrections-repair-74e19652d0cf7131。三份成熟数学源字节未变；本轮复用原完整比较，补核新 whole 边、receipt、真实反向资源同构、T_d>1、零费/弱端点及全域支持二势。ALL{WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1,WC-R1-RESOURCE-SUPPORT} 已推出目标完整合取：每个合法单成员同费非负多项式奇环均有整域 min{2,T_d}-PNE，同时有 2m 单冲突商态之一的 T_d-PNE。T_d≤2 可取池内见证，2<T_d 时全域 2-PNE 可是另一个状态。两旧 partial 资产在新 receipt 逐项 replaced 到同一 whole 资产，旧证据并集完整保留；retain accepted/unconditional/whole，不需要再做数学修订。

## 可追加到 cross_archive_review 的文字

本次 singleton 接续是 weighted-congestion 档内联合证明的统一投影，不新增跨档迁移。全域支持二的总成本势与单冲突包络分别支付完整目标的不同子句，不能拆为两条各自 whole 的单源支持，也不计为新独立证明；不推出 singleton 锐阈值、池内 2-PNE 或一般多成员群组结论。

未执行 Git、网络、队列命令或仓库写入，未运行原有限图审计，未新增任务或代理。JSON 保留全部精确输入引用、检查项、旧资产去向和作用边界。冻结摘要见同目录 SHA256SUMS。

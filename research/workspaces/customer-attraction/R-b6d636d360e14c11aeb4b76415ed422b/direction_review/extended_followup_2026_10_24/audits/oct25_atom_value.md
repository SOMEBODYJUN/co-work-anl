# seq310 原子回撤：一般价值、去重及失败 cut 的准确变化

2026-10-25，Boss3 内部价值审查。对象仍为任意有限单位客户、任意有限非空共同目录、任意人数及每份完整有序历史纯 SPE，含空主题、重复主题、全零客户与任意历史依赖平局。Q-CAG-HALF 仍 **OPEN**。本页不发送外部消息、不 commit、不读凭据，不新跑固定规模搜索；解析重构与来源核对不提升为外审或全球新颖性认证。

**结论：新稿不是单纯把旧流换成更多标签。真正放松的是“同一 owner 的全部初始 R 边必须等比例回撤”；固定流上的可行修复集合因此扩大，并给出精确分散返还。这个增量是一般线性修复工具，不是新的 SPE 总资金。相对旧 owner 比例类，它只能改善特定非均匀价格 cut，不改善全 1 cut、任何二值价格 cut，亦不改善按角色单调的价格 cut。现有真实 SPE 例没有展示严格优势或修好一个旧失败 cut；严格分离例只是合法三角 source/cap 数据。应保留工具和精确诊断，不继续以拆相同标签、扫价格或复核无分散旧例作为一般主线。**

## 1. 本次实际来源与数学层级

新稿读取的是父方提供的 `/workspace/scratch/10c0bc6cd6b0/c8_retraction_visit.json` 的 `text`，路由元数据为：

- actor：`R-c8ca54e5f2854c2c93bf83abc2f24f5c`；commit：`b22021bbfb77e3340bf1b497bc0a5269bfefbfbc`。
- 原路径：`research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/common_capacity/atom_retraction_and_dispersion_rebate.md`。
- snapshot SHA256：`9e242a9c874a1311b8f7ade28490b51ac450fd2bdc8ba3c23b0414c6bb250b4a`；text SHA256：`d14b56fd312203f9fc298b9a8c76ab7cfc467aa4e3f32740b8359dfc70aca48b`。

没有把新 actor 与旧 3bc actor 合并。旧来源及本轮直接读取的共同接口为：

- [旧 owner 比例回撤](../../../../R-3bc48d936f044f12b0fa743482ff5eb0/flow/origin_retraction_shared_capacity.md)及其 [application audit](../../../../R-3bc48d936f044f12b0fa743482ff5eb0/optimal_gap/origin_retraction_application_audit.md)、[三角贪心盲审](../../../../R-3bc48d936f044f12b0fa743482ff5eb0/optimal_gap/triangular_retraction_blind_audit.md)。
- round8 [共同付款 LP](../../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/linear_joint_payment_certificate.md)、[common-edge 价格势](../../../../R-cd789330fc7141299ac491bbb3ffa420/round8/residual/common_edge_price_potential.md)及[独立审查](../../../../R-cd789330fc7141299ac491bbb3ffa420/round8/independent/linear_joint_payment_review.md)。
- Boss3 [共同钱包旧审查](../../continued_exchange_2026_10_24/audits/wallet_review.md)、[价值尺度复核](parent_value_review.md)和[方向名单](directions_roster.md)。

旧共同证书已允许非最大 current、逐初始边不同金额、逐客户 common 边选择，并已经用有限凸分离刻画共同 cap。按 source 或初始边拆出合法同质子流也是其既有密度证明的方法。新稿不能另认领这些基础事实；新增处在于固定这份流后，允许各初始边独立回撤，并算出相对 owner 比例限制的精确差。

## 2. 不同的三件事：分解、自由度与新资金

固定同一个合法 seed flow，令 `A_l=d_l+H_l+J_l`，`cap_l=2u_l`。每条初始 R 边记为 atom a，质量 b_a，owner 为 i(a)。在合流处按进入质量比例分裂原输出，得 terminal current K_al；置 `t_al=K_al/b_a`，正 atom 满足

\[
t_{al}\ge0,\qquad t_{al}=0\ (l\le i(a)),\qquad \sum_l t_{al}=1.
\]

只有标签拆分、却继续要求同 owner 的 `y_a/b_a` 相同，所得 cost 集合与旧 owner 回撤完全相同。新稿实际取消了这一等比例限制。独立选择 `0≤y_a≤b_a` 并统一缩放该 atom 的全部后代，给

\[
F'_l=A_l+\sum_a b_at_{al}
+\sum_{a:i(a)=l}y_a-\sum_at_{al}y_a.\tag{AR}
\]

每条 atom 的输入、mandatory 输出、common 输出和 current 同比缩放，合并后仍满足原局部合同；初始边只减小，减少的量在同一 `(owner,x)` current 保留。因而此项是真实的固定-flow可行集变换，不是凭终端分布任意捏造退还。全额逐角色追踪 `Σ_aK_al` 是必要合同；只验证总量相同会漏掉固定 current 的价格成本。

总质量仍为 `Σ_lF'_l=|O|`，I、H、J 固定不变。新增 current 可能使 `d'_i>u_i`；这与旧 owner 扩展一样，进入的是放松 INIT 的证明证书类，须从同一个 `2u_i` cap 支付。它没有多调用一次 IC，没有给每条 atom 一个新钱包。

若某份回撤后仍有 `d'_i≤u_i`，它本来就是原共同 LP 的另一可行 INIT/R-FLOW 选择；此时新增的是构造/选择方法，并未扩大原 LP 类。超过该界时，扩大的是放松 INIT 的扩展类，其充分性来自库存守恒与最终共同 cap。二者都不能误报为一条新的原树激励不等式。

## 3. 一个旧失败价格究竟改善多少

给任意 `λ≥0`，定义 `q_a=Σ_lt_alλ_l` 及 `r_l=2u_l−A_l`。atom 修复可行当且仅当所有 price 都满足

\[
\sum_ab_a\min(\lambda_{i(a)},q_a)\le\sum_l\lambda_lr_l.\tag{AP}
\]

这是有限盒的线性最小化/凸分离，不新增 SPE 信息。固定 owner i，令 `b_i=Σ_(i(a)=i)b_a`，`q̄_i=Σb_aq_a/b_i`，并定义

\[
D_i=\sum_{i(a)=i}b_a(\lambda_i-q_a)_+,\qquad
E_i=\sum_{i(a)=i}b_a(q_a-\lambda_i)_+.
\]

旧 owner-price 需求与新需求的差恰为

\[
b_i\min(\lambda_i,\bar q_i)
-\sum_{i(a)=i}b_a\min(\lambda_i,q_a)
=\min(D_i,E_i).\tag{REBATE}
\]

因此，若旧 cut 的严格违反量为 ε，则相同 price 在新类中的违反量精确为

\[
\varepsilon_{\rm atom}=\varepsilon-\sum_i\min(D_i,E_i).
\]

只有同一 owner 的正质量 atom 下游价格同时严格位于 owner 价两侧，才有严格返还。返还至少为 ε 只消掉这一条失败 price；其他 prices 仍可能分离，所以不能据一个旧 cut 过关宣称 repair 成功。反之，同 owner 所有 t 行相同，或该 price 下所有 q_a 在 λ_i 同一侧时，这条 cut 完全不变。

### 两个无需扫描的准确零增益范围

以下都比较同一固定原流、同一 K/t 上的旧 owner 类与新 atom 类；不是说回撤本身相对未经修复的 F 不能降低某些集合的成本。

**二值价格。** 任取 `0≤α≤β`，若每个角色价格都在 `{α,β}`，则每个 q_a 都在 `[α,β]`。当 λ_i=α 时 D_i=0；当 λ_i=β 时 E_i=0。故所有 owner 的返还都为0，旧、新 price 左边完全相同。这包含全部 0/1 集合 cut 和全 1 cut，不限于后缀。

**按角色单调的价格。** 严格 future 支持还给：若 λ 随角色不降，则所有 q_a≥λ_i，D_i=0；若不升，则所有 q_a≤λ_i，E_i=0。所以这两类任意多价位 price 同样没有改进。严格优势只能出现在存在合适中间 owner 价的非单调价格上；新稿抽象例的 `(1/2,1,0)` 正是这种情形。

特别取后缀 `S_k={k,…,m}` 的 0/1 price，(AP)变成固定 I/R 证书的必要条件

\[
\sum_{l\ge k}(A_l+b_l)\le2\sum_{l\ge k}u_l,
\quad b_l=\sum_{i(a)=l}b_a.\tag{SUFFIX}
\]

后缀内 owner 的所有 R 质量最终仍在该后缀；更早 owner 可以全撤回前面。atom 细化与旧 owner 回撤对这个 cut 无差别。这里 A 含固定 J，不能直接照搬旧 full-SAFE 的 `r+H` 后缀数值；但“二值 cut 不变”的判断在本合同内是无条件解析事实。若既有失败证书属于这些零返还范围，继续拆 atom 无法改动它，应换 seed、I分配、路由、T 或引入新的真实关系。

## 4. 全 1 未付款的含义：精确限制，不能扩大成无价值

λ恒为1时，所有正 atom 有 q_a=1，返还全部为0，(AP)成为

\[
\sum_ab_a\le\sum_l(2u_l-A_l)
\quad\Longleftrightarrow\quad |O|\le2W.
\]

所以 atom 细化不会产生总资金，也不能单独承担一般 HALF 的资金证明。这个事实在 round8 原 LP、common-edge 价格DP及旧 owner 回撤里已经明确，不能把同一未付总账换成新 price 名称计为福利进展。

但它也不意味着局部分配工具没有价值，或全部非均匀 cut 都是多余的：即使总量足够，固定 owner 比例类仍可因局部共同 cap 失败，atom 类有时能修复。新稿§5抽象数据恰证明这种严格包含。若未来另有一般机制支付总量/限制价格，独立回撤可以作为其分配组件，减少不必要的同 owner 围栏；它不需要自己独立证明完整half才值得保存。

准确区分应为：**一般解析修复工具已得到；原 SPE 强迫所有 atom cuts 成立尚未得到；新无条件福利上界未得到。** 不得把后两项未闭合写成工具为假或无价值，也不得把第一项称为总资金已推进。

## 5. 严格优势例的来源：目前只有抽象分离

新稿§5给 `u=(1,1,1)`、`A=(3/2,2,1)`，owner1两条质量1/2、分别终结角色2与3的 atom。旧比例类失败，选择性撤回第一条成功；`λ=(1/2,1,0)` 的原违反1/4恰由返还1/4消除。该例清楚标明**未声称来自原 SPE、INIT 或原目录**。它证明两个线性修复类严格不同，不能称真实博弈上的严格优势。

来源核对未找到另一份真实严格优势见证：

- 新稿§7的52客户完整 SPE有1554条含自身全历史 IC；两条正 R 初始边 owner 不同，且都只终结末位。因此每 owner 的 t 行没有分散，所有 λ 下 REBATE 恒为0。它核对全额追踪、缩放和守恒，不核严格优势。
- 旧 `origin_retraction_exact_audit.json` 的另一348客户、258条IC例没有R源；52客户例是 `K_03=K_13=1/8`，原成本已经满足cap。五人 all-big、全主题、零客户及所述顺序平局边界亦没有提供严格分散例。
- round8共同证书和独立审查给的是充分接口与密度合法性，不给上述真实严格分离。

因此目前没有已保存证据说明“一个已知真实 SPE 失败 cut 已被新细化消除”。这不是说严格优势不可能来自 SPE。没有必要为补展示而另开固定规模搜索；若自然出现既有失败 seed，可直接使用其精确 price 和 t 评估 REBATE，或给一个全输入结构关系解释为何这种返还恰好足够。

## 6. 同一一般机制代入 m=5

atom owner最多为4，终端只在其后角色。五人没有额外新原理：需对所有 `λ∈R_+^5` 证明(AP)，或构造同一组 `y_a` 使五个实际 cap 同时成立。

已证无条件层是：任意合法 seed 都可作精确 atom 分解/缩放，AP与固定类可行性等价；第一实际角色没有 incoming R，`A_1≤2u_1`。其余角色容量尚非自动成立。新选择比旧 owner比例类自由，但仍没有证明任意五人共同目录、每个完整 SPE存在成功 seed/回撤。

尤其 `λ=(1,1,1,1,1)` 仍正是未付 `OPT_5≤2W`；全部五人二值及单调价格也没有分散返还。因而本轮**不能无条件推出 five half，也没有新的无条件五人常数**。这个压力判断没有否定一般候选，没有要求五人先成功才准研究；它只指出未来的真正承重项必须来自何处。继续一般推导可保留该组件，但不转成五人专用调系数、加行或规模扫描。

## 7. 保留与停止的具体边界

| 工作 | 价值判断与下一义务 |
| --- | --- |
| 固定合法流的独立初始边回撤、AP精确cut及REBATE | 保留为一般条件工具；它消除了真实的等比例限制。独立审查可核数学合同，但不能代填一般可行性。 |
| 对一个已有失败price计算精确返还 | 有直接判别价值：能说明这个失败是否仍有效。应同时报告seed、T、J、route与逐角色全额追踪，不混不同方案的有利项。 |
| 用新真实 off-history IC控制剩余prices，或与别的总资金机制连接 | 值得继续的一般义务；需点名新增原树关系、实际支付来源及一次使用的共同预算。可以绕开AP，不是强制接口。 |
| 改选T、INIT、I-PAY或合法路由 | 若有一般选择原理，可形成真实新机制；仅再写一个存在式/LP不算已付款。固定拆分的失败也不分离这些更大选择类。 |
| 把一个atom按相同比例拆成更多标签 | 停止作为改进任务。同owner且t相同的行可合并，任何cut和修复集合都不变。 |
| 继续对52客户无分散例扫价格，或扩同类合同检查数量 | 停止作为一般主线。这里REBATE对所有price已经解析为0；更多有限价格不能提供优势或一般付款。 |
| 继续证明密度≤1、总质量守恒、单context whole-IC，再改名为共同cap | 已有来源清楚，归并即可；这些关系没有增加同角色跨历史的资金。 |

“拆相同标签无增益”不能扩大成禁止一切更细合法流。若改变拆分或路由后真正产生不同终端分布，必须重新证明各子流仍满足mandatory等式、common区间及总库存；这已经是另一个可行集/选择机制。特别不能直接按末端路径任意删枝，因为只撤一条mandatory子枝通常破坏 `z=h/c_A`。此类真改变应按其新增数学内容判断，不按标签数判断。

上述是内部价值与去重结论，不是开工审批、单次判别配额或对远程作者状态的宣称；本页没有请求其停止一切相关一般研究。

# 零需求定向替代的 3D 数学整合意见 · 474257b8

本意见只提供可追加的实质 3D 范围与结果，不是新的 3A receipt，不修改共享图或登记。当前实读任务为 `boss5-474257b8-zero-demand-repair-f062dc9eaaaef22f`，`state: done`、`owner: Boss1`，明确替代 `round9-source-repair-repair-d0ac122f3ce74353`。旧 0195 任务已是历史，不应再被重新替代。本次没有发现新的实质数学错误。

## 当前版本与待办处置

当前收据精确处置旧 15 资产：13 retained、2 replaced，没有遗漏或无去向资产。17 个核心中，15 个覆盖条目逐字段沿用；只更新给定见证原入口与真实源有限重放两个核心的比较说明。28 个输入 pin 中恰有这两个核心与只读 joint-slot 定理三个变更，其余 25 个不变。全部当前输入 pin、15 资产字节 SHA、每边端点 pin、证据 SHA 均与实际文件/登记一致。旧收据与新收据内所有 retained 资产 SHA 一致。

**可关闭的 D0 待办**是“原处分支限定尚待修正”以及“等待 d0ac 的定向替代交付”：当前源已正确分支，新替代已 done、旧资产去向完整。**仍需 root 最终接入的动作**是把这个 done 的新 semantic receipt pin 接到实际 assemble。此 worker 读到的 `map/integration.json` 仍包含旧 d0ac pin，没有新任务 pin，registry canonical 尚未接入新两边；这是本次只读快照，不能写成已经整合或作为否定 root 后续 assemble 的状态。

integration 的 task receipt pin 是紧凑、键排序 JSON 的语义 hash；它与 receipt 文件原始字节 SHA 不同。旧 integration pin 与旧实际 receipt 的语义 hash 正确相等，没有旧 receipt 失配。

第九源《门槛覆盖》原处分支修正本轮也已核，但它所属的 `unrelated-machines-3a-3a-b10995ada0ae22bc` 在所读本地快照仍是 available、owner=null。本轮 17 核心替代不替它完成独立 3A 覆盖；这项任务不能随 D0 交付待办一起关闭。

## 正需求归一与零需求旁路的完整理由

在失真组合同中，H 与 Z 不交，私有组唯一 home、组间不交、整组共同资格 E_h。每件 home 重量 w_j、sink 实际时间 q_hzj 满足

\[
\frac{b_{hz}}\kappa w_j\le q_{hzj}\le b_{hz}w_j,
\quad W_h\le T,
\quad w_j\le\delta T,
\quad \tfrac12\le r<1-\delta.
\]

令 d_h=(W_h−rT)_+、c_hz=b_hz d_h。若真实 T 调度在 h 放了宏 β>T/2，则该 home 至多一宏，私有留量≤T−β<T/2。实际迁出的 **home 体积** e_h 满足 e_h>W_h−T/2。只有 d_h>0 时才有

\[
e_h>W_h-T/2\ge W_h-rT=d_h>0.
\]

所以仅正需求分支定义 y_hz=e_hz/e_h，并由下包络逐组逐 sink 得到

\[
c_{hz}y_{hz}
=b_{hz}d_h\frac{e_{hz}}{e_h}
\le b_{hz}e_{hz}
\le\kappa\!\sum_{j\in J_h:\sigma(j)=z}q_{hzj}.
\]

先在每个真实源态用该态宏归属构造 a，并用同态出口构造 y，再用相同权重平均。于是 Σ_z y_hz=x_h=Σ_b a_bh，逐 sink 分数成本≤κT；不能把两个独立平均的证书拼接。

若 d_h=0，则 W_h≤rT。该被占 home 的单位占用流直接给本 home 私有零成本旁路；即使原真实调度曾把部分该组任务送走，也不必模仿该出口，不计算 e_hz/e_h，不要求 e_h>0。未占宏 home 的 x、y 都为零。旁路是证书中的私有出口，不是实际机器，也不删除任务。恢复时该零需求组所有私有任务留 home，负载≤T+W_h≤(1+r)T。

空私有组给 d_h=e_h=0，已经足以说明不能把严格出口链或除法扩到零分支。W_h<T/2 时 W_h−T/2<0=d_h，更直接否定未限定的第二个比较。本次当前源与新检查边均已补对分支，冻结原证明 §2 也一直明确正/零分支。

## 两条替换语境边的实际用途

`supplied-distortion-implementation` 仍是 accepted **implements/context**。规范入口先验证全部原任务与真实资格、包络、Σ_h a_bh=1、x_h≤1、Σ_z y_hz=x_h 和每 sink 的 κT 预算。它的成功方向只要求正宏流所走真实端 p_hb≤T；宏下界>T/2只为“真实 T 调度必给必要 LP”服务，不能倒写为该验证器成功的必要条件。

按 c_hz 非增切单位槽，只有严格正区间交长连边。一个宏→home-in→home-out→sink 槽的网络同时选择宏、home 和接收槽，home 中间容量1、槽容量1。给定 a/y/交长提供同一满分数流，整数容量流给覆盖全部宏的整数解。不能先选宏匹配再拼另一份出口证书。

实际前缀停止于 home 私有余量≤(r+δ)T；若真撤离，末件≤δT给总出口<d_h。若没有撤离，出口0≤d_h。共同资格与上包络保证实际 sink 成本≤c_hz；第2及以后槽收费给前一完整槽，首槽多付至多一个最大成本。因此全部原任务实际输出满足

\[
L_h\le(1+r+\delta)T,
\qquad L_z\le[\kappa+\bar B(1-r)]T.
\]

这是一份合法给定证书的实现。拒绝一个坏证书只否该输入/见证；程序没有寻找普通精确 LP，不据任意证书失败判 OPT>T，也没有未知 OPT 端到端软件。

`true-source-distortion-check` 仍是 accepted **checks/context**。它记录实际源调度→同态 a/y→平均→另一套正交槽构造→同一宏/home/slot 打包→真实前缀和逐件回算的有限证据。独立脚本不导入 flow 或规范舍入，而用指数回溯打包 oracle；这支持固定实际输入的独立核查，不能承担一般位多项式算法。其 `verify` 明确先执行零需求私有 dummy 分支，再进入正需求严格出口断言。

本次只读了代码，没有新运行。16 固定证书与软件审查程序的5有效/10拒绝输入可按旧冻结证据保留。规范 main 另有5个直接边界；软件审查导入被测 core，不是第二套独立恢复 oracle。1248随机矩阵、1192421原分配、1087个T可行矩阵、3720真实源调度属于冻结独立生成器的历史段，不能写成本轮重跑，也不能把16份固定证书扩成对任意LP伪见证的穷尽。

确定性二home例中，每源态每组实际向两 sink 送2枚和1枚 quarter，归一为2/3和1/3；两组总 token 质量4/3与2/3。d=2/5、b=5/4给虚拟成本1/2，而恢复首件实际成本3/10。非整数末槽与真实 q 成本因此清楚分开；该有限算术并不替代一般槽收费证明。

## 门槛覆盖的同型更正及不能互换的恢复

当前第九源完整定理要求共同 E_h、**等端** w_j、宏>T/2，取 d_h=(W_h−τT)_+，τ≥1/2。d>0时 FPTAS 保存原覆盖约束，用同一个实际子集 X_h、e_h=w(X_h) 满足 d_h≤e_h≤(1+η)e_h*。真实 T 调度给迁出 r_h>d_h>0，故

\[
e_h\le(1+\eta)e_h^*\le(1+\eta)r_h,
\quad e_h\frac{r_{hz}}{r_h}\le(1+\eta)r_{hz}.
\]

d=0取 X_h=∅及私有旁路。共同整数槽流选定接收端后，必须把 LP 计费的**同一个 X_h**全部送过去；sink实际成本恰 e_h。home界1+τ、sink界(1+η)(2−τ+δ)共同给 R。它的精确覆盖 DP 是 poly(input,1/η)，不是 poly(log(1/η))。

这不能改为失真组的固定前缀：失真合同在 home 多保留δT，以保证迁出≤d；门槛覆盖把≥d的实际子集计入LP。第九源现有无界家族中旧固定前缀给 sink负载r，而真实OPT=1，已排除免费替换。该反例和修复本次全文核读，未重跑。

未知OPT搜索也只对 d_h(t)>0 的被占home使用 W_h−τt=d_h(t)>0及真实出口归一；零分支旁路。t≥OPT时一侧全接受，低于OPT可非单调。整数二分只保low拒绝、high接受及low<K*，因此终点high≤K*。该数学搜索不等同于现有给定a/y软件外层；本轮没有把门槛覆盖改成失真组的单调LP谓词。

## 13 份保留资产的范围保持

下表按旧 d0ac receipt、旧已审 primary 的精确引用和当前边全文进行有界复用。全部字节/端点/证据一致，且不依赖此次改版的三个对象。此 worker 没有重新全文审计这些13条边涉及的全部旧 primary、附件或17核心文献；原有比较理由和非本轮改变的证明继续用。全SHA与原证据定位在配套JSON的 `reviewed_assets`。

| 保留边 | 此次确认的数学范围 |
|---|---|
| `config-independent-retention` | 局部贡献：给定等式CONFIG(T)证书，独立逐机抽样并去重，实际峰≤T、期望保留≥(1−1/e)n；完整DGR比例另需大边匹配、小边前缀及证书算法。 |
| `half-choice-to-promise` | 完整条件关系：P≠NP及总确定性位多项式/统一可截断见证搜索合同下，排除固定δ<1/2的(Aδ)及所述逐机加性max预算搜索；不排除NO实例上的实际低于2调度。 |
| `karp-to-half-choice` | 完整迁移：显式perfect 3DM到half-unit唯一small端判定，r≥q与2r≤2q支付同一匹配；严格δ<1/2不可移到端点。 |
| `literal-proof-history-ownership` | 语境检查：同一异权literal-pool的clause-only、all-original-job消去/扩展及连续槽证明；不同证明不自动有同输出集合，保full-budget原任务。 |
| `markov-minimum-size` | 语境检查：真实D、固定树、冻结树任务及逐正概率态合同中，≤4机正面与5机坏态合成最小机器数边界；不能换成一般调度不存在。 |
| `private-tree-demand-to-graph-case` | 局部贡献：图边作k=2,h=1状态，给value与signed demand具体输出；反向minorant分离/Independent Set、包络及扩展LP后果另证。 |
| `query-count-uses-fixed-coloring` | 语境引用：固定两实际见证、同一主动染色及机器唯一色给坏query到重源机注入与同query低费；不是未知见证生成。 |
| `query-owner-filter-history` | 语境引用：保守G_owner⊆G_actual且可能严格，零端v1严格式修复与v3历史分开；筛掉owner不能判不存在合格调度。 |
| `quota-orientation-to-grid-frontier` | 完整ALL特化：固定Hall与真实树方向等价给行列网格精确前沿；最强Hall在全选集及重选最小ab依赖该对称结构，s=K=4给5/8。 |
| `tree-full-threshold-to-unit-test` | 局部贡献：全阈值恒等给C_(k−1)≥W−1和该层DP；删其余阈值及O(|V|)W/F/Z表示仍用额外色类及两向投影证明。 |
| `tree-valuation-global-xos` | 完整ALL：估值/实际最优子树与uniform全域minorant联合，给w(S)≥f(S)/G(k,h)、全域w≤f及锐性；不是调度近似比。 |
| `two-size-replay-ownership` | 语境检查：全资格同机整比双尺寸，原子批次边界的中性换形及tiny削平；macro最大ceil(k/m)、tiny由M+1/M−1至M/M、OPT=δM。有限计数/标签程序不替代一般证明。 |
| `vw-maxmin-to-degree-two-menu` | 完整迁移：显式度二indexed菜单，bonus保OPT、平均加性值与VW后端共同给完整实际调度及2−1/(2K)保证；固定K才统一离2，非一般UM或half搜索后端。 |

其中 `config-independent-retention`、`tree-full-threshold-to-unit-test`、`private-tree-demand-to-graph-case` 保原 contribution/remaining。局部一步已成立，不把整目标的独立其它步骤改称“新open”，也不把局部贡献升级为 whole。context 资产不令核心自动变 linked；本轮两个有限核心保 isolated-after-review 是准确处置。

## 与本轮 1766 的接口区别

本次只读1766当前三边的类型、条件、整句/贡献和范围字段，并复用已有 `integration-um-current-wave` 对其 primary 的审读结论，不声称本worker又完成其全部证明审计。

真实pin核的全q²请求OPT=2−1/q与单标签q请求OPT=1是两个不同任务集合的实际完整值，属于whole特化；F2每固定共同函数的quota也是受额外一致性限制的whole。Q_D双桥边只贡献显式CONFIG(1)、最高有限CONFIG阈值1及row/item度，actual菜单/SC值1/D与flat UM值2−1/D依赖正文另有整数上下界和值桥，不能由CONFIG可行直接推出。

本零需求修复处理的是给定或由真实源导出的共同a/y及其恢复，不提供困难源请求编译、每份低峰普通UM调度到同一f的物理一致性、或全实际输出的NO解码。capacity、LP、slot名称相同不构成模型映射。本轮没有新建这些无凭据比较边，也不把有限检查与近二实际值拼成hardness。

## 可直接追加的 archive_review

**comparison_scope：** 实读Boss1已done的零需求定向替代任务及当前收据，逐项处置d0ac的15份资产；重核失真组给定证书实现、真实源有限检查、共同a/y、正需求出口归一、零需求私有旁路及完整原任务回填；另全文核门槛覆盖同见证定理的两个同型分支。13保留资产按旧已审primary定位、当前边的精确条件/whole或contribution/语境作用、未变端点和证据SHA逐项复用；不重做17核心的全套文献审计。对1766只复核当前三边的整句/局部贡献/域接口，并以既有本轮整合笔记定位CONFIG与实际值的区别。

**outcome：** 正需求被占home才有e_h>W_h−T/2≥W_h−rT=d_h>0并以真实出口作分母，下包络按sink支付κT；零需求不归一，单位占用质量走本home私有零成本旁路，实际恢复保留全部私有任务在home。同一源态的a/y同权平均保守恒，成本c=b d有序槽在同一整数流同时选宏/home/接收槽；失真前缀由home的δT余量支付，得到原home与sink界。两条替换边仍分别为implements/context与checks/context，后者只有固定实际源输入的独立有限oracle，未升级为通用LP或未知OPT实现。13保留边和15个未变核心覆盖完整沿用；新收据只改两个有限核心覆盖及三个输入pin，未产生新算法、一般UM保证或困难性桥。

**unresolved_add：**

- 给定证书被拒仅否该输入证书；没有通用精确LP后端、未知OPT端到端软件或由任意软件失败判OPT>T的实现保证。
- 一般矩阵到唯一home/不交组/共同资格/统一上下包络/W和小任务承诺的保真共同表示仍未给出；失真组参数改善仅属于显式结构类。
- 门槛覆盖第九源的原处分支修正已核，但其独立b109任务在本次本地快照仍available/owner=null，不能由本轮17核心的替代交付代为关闭。
- 1766仍欠真实困难源的请求编译、普通矩阵内每份低峰完整调度的共同函数一致性及全实际输出NO解码；CONFIG/LP/slot同名不支付这些桥。

旧“等待 d0ac 定向替换”及本轮正/零分支勘误可按上述完成情况移除；不能用这份有界增量删掉全档其它真实未决事项或一般 `cross-batch review pending`，也不能把本意见的局部实读声称为全UM档审完。

## 精确版本与实际读取

| 版本引用 | 实际值 |
|---|---|
| task原始字节SHA256 | `5321603fdaa6f2c0dbe79939e289cef4ef675e2d696e66e79702b53923298faf` |
| 新receipt原始字节SHA256 | `51c944e291e03433f4f9e6b1c915a9fd920c88de2ea94aefdb2ce47fecb77c1b` |
| 新receipt semantic pin | `1b4af6b33df4a9c817f479a5f392c9047b2a364ae19806c1abba8e709cfbfadb` |
| 旧d0ac receipt原始字节SHA256 | `1b488b9d6b2b1dddb9dc5f2d414dfec5410f53072072800b8a6aa26742aba824` |
| 旧d0ac receipt semantic pin | `8ca6d302f7869af4a17e6f718f08e454ab613bb1b35a42c222cad750002864a3` |
| 所读registry原始字节SHA256 | `57a449f72d012171f1139584bcfe280d779b0b3b586c079e06c925125bcf6ba4` |
| 所读integration原始字节SHA256 | `ba2a29cf180508496b373daa02397897cc973459fd2d59efdf1e9b5b33bdc984` |

三个改版输入当前为joint-slot v3、真实源重放v2、给定见证原入口v2；其pin分别见JSON `changed_input_pins`。门槛覆盖当前v2，pin `fb6ae47daf4d59f95268a72db48cd295c608a39564a9a42d0ddac1db569cb473`。

两替换资产与13保留资产的精确SHA：

| 资产 | 处置 | 当前原始字节SHA256 |
|---|---|---|
| `config-independent-retention` | retained | `27eaae446e23c2b34332a7431aba4b3b57813252eabc3ca99894d6c1af7b16fe` |
| `half-choice-to-promise` | retained | `95919610311cb5f6d47d94e0f926e43ef22ecd2bd716a6de9ecfb686b3d1c689` |
| `karp-to-half-choice` | retained | `6881dac8ea7270a72c256d8bbfccb2fd4cd2be2fc1a25cad1797c7063cb0dca3` |
| `literal-proof-history-ownership` | retained | `77c15f4ccc66b05ff7421daf65abbd59ba7d94d3a4bd115773103f3632a969f4` |
| `markov-minimum-size` | retained | `bb9c336796a7cf630b7467681e39e7864119141700b18ba9d4f9b2537f0c7327` |
| `private-tree-demand-to-graph-case` | retained | `8585c4410aec1115bb95dc96de81659ad733c8a110a581dc0e653c762b11f390` |
| `query-count-uses-fixed-coloring` | retained | `871d43386d7b2f091f75f26fff7319f143f609de44e435dec81e5bcb78bc7b28` |
| `query-owner-filter-history` | retained | `6992375c90528421a996c41fdc7e6a921eb81dfdc98fc9f23cbf2ed5d878e50f` |
| `quota-orientation-to-grid-frontier` | retained | `56a9458f8343ff728692f108a80d407879439d59440d4e58a9fdae81585ae6e7` |
| `supplied-distortion-implementation` | replaced | `5fe42ff927052a2ab182d040863e034924f08e6d31bdcb48cb4b1fbcac6e2b97` |
| `tree-full-threshold-to-unit-test` | retained | `069de243c10762003b0b297df4c496a46cdb6aa9095d2a5a1deb841d3aaf35d4` |
| `tree-valuation-global-xos` | retained | `09fdb0d0026e1fcaefc7ee4fe49c2818ba446c77d3ed47e6906feff857c7090e` |
| `true-source-distortion-check` | replaced | `5753c74a431912bad15556a90ef66620d862bb393a956ec075745eb2b147e31f` |
| `two-size-replay-ownership` | retained | `8f46fadda978f5f2718fc7d64a5aa76e90024faf40d2b94525e1d41d24265493` |
| `vw-maxmin-to-degree-two-menu` | retained | `cecb8016b0d993516865cf3572e194942bb0f87c6adfef3b1856e4b6e57454f9` |

本次实际读取的主要数学来源：

- `AGENTS.md`：全文，工作约束；SHA256 `a24b90db5ceabf26f4db3b831a4d63d121133ecc35b283ed5dd334c77cb38c92`。
- `research/IMPLEMENTATION.md`：全文，接口与定向替代规则；SHA256 `28bdc88dd144cad15c2081b2f00a3d1a7023792a0dde04c37831944d49e56632`。
- `prompts/03-map-worker.md`：全文；SHA256 `6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2`。
- `archives/unrelated-machines/state/资源/失真组给定见证舍入与有效无效证书原入口--资源.md`：全文；SHA256 `3a1eaf8b5a1625d2111851c971576d9bf0d989addf69374f08012997cc147394`。
- `archives/unrelated-machines/state/计算/失真组实际源调度与联合槽独立程序复跑--计算.md`：全文；SHA256 `3ff4fc9e22775b542dd600a8b01787c3f8d6fb180b4ea550f8564ec278f56a78`。
- `archives/unrelated-machines/state/审查/失真组联合槽舍入与固定汇点占位双源审查--审查.md`：全文；本轮承重为第一部分完整§1–3，其余只保模型分工；SHA256 `7a3644e31616ec18cd434ab73163ea073cf7ba11dca8cdaac2c9ea406c961b29`。
- `archives/unrelated-machines/state/算法/门槛覆盖的同见证联合槽恢复--算法.md`：全文，尤其必要LP及未知OPT上侧全接受两处；SHA256 `2ba9c9b10faf1aa7931c82ffdb278a301a148632f2de96a540c4d773de80d9f0`。
- `archives/unrelated-machines/tools/evidence/um-following-palette-and-distortion-primary/comparison/research/current/unrelated_machines/distorted_group_joint_slot_rounding.md`：全文§1–9，完整冻结原证明；SHA256 `de39d3d70e4a1d5835eaecf196d0a0bcff51006f6d7eb4006354344b737f5deb`。
- `archives/unrelated-machines/tools/evidence/um-following-palette-and-distortion-primary/original/tests/audits/unrelated_machines/distorted_group_joint_slot.py`：全文，只读未运行；SHA256 `6235657b39bddf8845e7d1308465e2167971258179551bcb4383fa3126d6a368`。
- `archives/unrelated-machines/tools/evidence/um-following-palette-and-distortion-primary/original/tests/audits/unrelated_machines/distorted_group_software_review.py`：全文，只读未运行；SHA256 `a0af40d2cd6679ba1beafb1400f8a5eb39050df897fca3300e84e82b06f31a68`。
- `archives/unrelated-machines/tools/evidence/um-following-actual-code-primary/original/tests/audits/unrelated_machines/distorted_group_independent.py`：全文，只读未运行；SHA256 `5ee207d75e09db05cacebcc5c9d560a9bbce6bd897556488a5d7aad84f09029c`。
- `research/workspaces/map-v2/Boss5/errata-math-474257b8-final-review.md`：§5末段及§6–9；早期§1–4仅标题线索，未声称本轮重审；SHA256 `46134d0d8420d1223ef4f84bc0436dd54c497bc390557819a66df319d84b5a4a`。
- `research/workspaces/map-v2/Boss5/zero-demand-application-474257b8.json`：全文，原处应用记录；SHA256 `5c65b991c3ba6cf6a763638667b2250e2475ceb7948c00f4708608dd1db4eb07`。
- `research/workspaces/map-v2/Boss5/integration-updates-474257b8.json`：全文，定位旧待办；SHA256 `5cf16ee1f1f3079243f5ef92e4f09f3002f57a168da16dc99a9319e1ca0a64c9`。
- `research/workspaces/map-v2/Boss5/integration-um-current-wave-474257b8.md`：全文，1766比较为既有审读的复用边界，不倒填为本worker重读其所有primary；SHA256 `79e0057c321ed6fbd2b644bdd3a82a685c80d0af03c2a7ca19c32696928082bd`。

另实读本轮15条边全文、当前/旧收据的覆盖和资产处置、当前registry的四个受核对象完整记录；其余输入仅作精确pin核对。current integration仅读相关task pins、canonical是否含新路径及UM archive_review。未从旧注记继承不存在的本轮实读：`integration-resource-474257b8.md`是resource-activation整合资料，本轮仅浏览定位，未作为本失真组证明依据；errata早期§1–4仅检索标题，本轮不重审Bamas/outer/长链数学。Flow依赖、16份fixture JSON和历史随机报告未在本轮逐项重读或运行。未使用Git、网络、队列写入、registry/源/边/receipt改动。

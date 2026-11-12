# RET v3源版本的定向比较与修复

身份沿用Boss1；任务为 `boss1-wave12-ret-source-repair-1559410bdf704b13`，实际状态为claimed/Boss1，定义pin为 `711c01b839c5e9f6c62677f218630852dad6f4ddc2436f032731a4a6f19540da`。本稿只替换原有 `retained-comparison-pool-controls-static-private-block-loss`，保持其稳定edge_id、accepted、unconditional和contribution作用。唯一supersedes是有效done holder `boss5-eta-status-round55-repair-6cda1bce3d48b546`；14fd及原00c291只作历史来源。

本轮新核33份当前对象合同及全部input pins，实读有效round55 receipt全部21核心覆盖与19条prior边的完整数学语义。原任务500K规划预算、93 reading_refs及93有序passes均保留。实际新读14个完整声明段，79个未变段按现行合同、相关边作用及精确endpoint/evidence pins继承成熟证据；逐pass见 `readledger.json`。没有新执行原科学程序、LP、SPE求解器、完整策略重放或旧诊断扫描；下文解析推导直接使用新读的数学正文。

## 固定根比较池的静态贡献保真

固定达到OPT_m的m槽合法比较元组，槽标签可以重复，并集为O。实际前缀并集为C_t。均匀排列比较**索引**，删除前t槽，令J为保留的m−t槽。每份保留元组都是F_(m−t)(C_t)的合法补全，故

\[
F_{m-t}(C_t)\ge\mathbb E\left|C_t\cup\bigcup_{j\in J}T_j\right|.
\]

对于x∈O，其比较覆盖槽数d_x≥1；全部d_x个槽在前t次被删去的概率为 `binom(t,d_x)/binom(m,d_x)`。O内已被C_t覆盖者不会损失，O外的每个actual新增客户贡献一次负退款。因此同一客户集合计数给

\[
L_t=|O|-\mathbb E\left|C_t\cup\bigcup_{j\in J}T_j\right|
=\sum_{x\in O\setminus C_t}\frac{\binom t{d_x}}{\binom m{d_x}}
-|C_t\setminus O|.
\]

由于|O|=OPT_m，静态缺额

\[
\mathcal S_t:=\operatorname{OPT}_m-F_{m-t}(C_t)\le L_t.
\]

t=0二者为0；t=m没有保留槽且F_0(C_m)=W，故

\[
\mathcal S_m=L_m=\operatorname{OPT}_m-W.
\]

这一步没有使用任何收益最优性。重复标签保留不同索引，d_x是槽重数；同覆盖异标签亦合法。空主题、零客户及没有新增覆盖的前缀不引起除零。保O外退款是原half净差的必要部分，不能改成gross遗漏。

## 当前最优池重启给同一静态ε

在一个当前节点，过去并集P、余r、规定动作S。选达到F_r(P)的r槽元组T，写

\[
O_h=P\cup\bigcup_jT_j,\quad
D_j=T_j\setminus\left(P\cup\bigcup_{k\ne j}T_k\right),\quad
e=|S\setminus O_h|.
\]

此D_j仅相对于该元组，且避开过去覆盖。移除j并放入同一个S后的覆盖恰为

\[
F_r(P)+e-|D_j\setminus S|.
\]

余r−1槽是H=F_(r−1)(P∪S)的一份合法补全。令δ=F_r(P)−H，则

\[
\varepsilon_j=H-[F_r(P)+e-|D_j\setminus S|]\ge0,
\qquad
\operatorname{lost}_j-\operatorname{new}=|D_j\setminus S|-e=\delta+\varepsilon_j.
\]

均匀删除一个索引时，局部期望L_1=δ+(1/r)Σ_jε_j。这里的O_h包括原P，退款e绑定同一S和同一原比较并集；重复槽可使D_j为空但恒等式仍成立。这个局部重启池与固定根池O是两种不同选择，不能在中途悄悄换池而保留一条随机链。

完整私有块账本还须使用同一真实强制T_j分支上的

\[
|D_j|=d_j-d_j^{out}+L_j^{capture},\qquad
\Gamma_j=u-d_j\ge0.
\]

于是δ−u等于该同枝捕获份额减块外当前份额、已救私有客户、e、ε和Γ。这里的捕获量L_j^{capture}不是RET的L_t。随机保留的静态计算不把不同真实子树的捕获利润转成一份actual钱包。

## 旧全前缀付款已经失败的准确范围

新读CA-PREFIX正文的全部客户构造和所有有序历史解析证明。每个n≥4取x=n−2，普通叶L_j（j<n）有x个只喜欢L_j的客户、1个喜欢A/L_j的客户和x个喜欢B/L_j的客户；特殊叶L_n有x个只喜欢L_n的客户、x个喜欢B/L_n的客户和n−1个喜欢A/B/L_n的客户。全部叶两两不交。

完整策略是：root选A；非空非末位历史若全为B则选A，否则选B；末位取真实最佳回复，平局优先B、A、L_1、…、L_n。正文的末位五类、非末位四类分析覆盖全部有序历史，不能将其缩成仅actual叶或冻结偏离后继。n4证书说明另保259个字面节点和两个不同补全枚举的成熟责任；本轮没有重跑这两实现。

实际路径为AB^(n−1)，其

\[
u_1=n-1/n,\quad
u_i=n-1/n-1/(n-1)\ (i\ge2),\quad
W=n^2-2,
\quad\operatorname{OPT}_n=2n^2-2n-2.
\]

每叶有x>0名只能由自己覆盖的客户。n叶已覆盖全部客户，所以任何最优n槽支持必须包含每个叶，且恰各一次；最优元组只差排列。故任意最优元组下全部客户d_x=1，不能通过“存在一份较好的最优比较元组”救回付款。

第一步C_1=A⊂O，|A|=2(n−1)，因而

\[
L_1=\frac{|O\setminus A|}{n}=2(n-2),\quad
P_1=n-1/n,\quad
L_1-P_1=n-4+1/n>0.
\]

同时正文给F_(n−1)(A)=2(n−1)²，故静态𝒮_1=L_1。n4就是L_1=4>15/4=P_1，差1/4。

对i≥2，C_i=A∪B，已覆盖W=n²−2名客户。未覆盖恰为每叶x名私有客户；剩n−i槽最多补n−i个叶，每叶恰新增x名，可达到。所以

\[
F_{n-i}(C_i)=W+(n-i)x,
\qquad
\mathcal S_i=ix=L_i=i(n-2).
\]

真实累计收益

\[
P_i=i(n-1/n)-(i-1)/(n-1)
\]

满足

\[
P_i-L_i=i(2-1/n)-(i-1)/(n-1)>0\quad(i\ge2,n\ge4).
\]

因此此族在首步击破两种全前缀付款，而其后各前缀付款成立，且终点余量为2W−OPT_n=2(n−1)>0。这不能反驳终点half、SWAP/RET恒等式、旧逐人D或所有非局部信用。𝒮≤L的一般关系仍保真；本族恰在每步取等。即使另有严格L>𝒮的数值例，单个数值差也不足以证明两个全前缀命题的逻辑严格分离，本包没有作这类主张。

本次没有发现新反例：有效round55 receipt的RET coverage已经写出本族L_1>u_1。源正文旧open状态漏接了既有反例；现在RET v3的SWAP/RET代数不变，全前缀加强已反驳。直接refutes另由同批指定sibling处理，本边不把包外M-dfcc加入端点，不新增对象或gap节点。

## 保留的终端条件路线

`private-block-common-payment-condition-to-half` 的全部端点、证据及字节未变。它的共同前提是开放B?与已证同枝私有块账本。对B?给出的同一组兼容选择，TOTAL为

\[
\operatorname{OPT}-2W
=\sum_i[L_{ij}^{capture}-d_{ij}^{out}-|D_j\cap S_i|-e_i]
-\sum_i(\varepsilon_{ij}+\Gamma_{ij})\le0.
\]

此条件推导完整，relation_mode保持conditional；B?允许早期欠账与后期抵消，不能因RET的所有前缀已付清被反驳而误删这条充分路线。它仍缺不同真实子树对同一actual容量的一次共同付款。源重新分组的θ/ε及两种η不得叠加消费。

## 19项有效prior资产逐项处置

下表的“保留”都指原路径、原SHA原字节；全部18项当前仍canonical，端点和证据pin逐项吻合。旧RET桥在本轮Root assemble后因改版输入成为stale而暂时退出canonical，仍是有效prior receipt要求明确处置的资产；本包在reserved新路径替代它。

| 原edge_id | 处置 | 核对后保留的数学作用和边界 |
| --- | --- | --- |
| private-block-common-payment-condition-to-half | retained | B?+同枝TOTAL条件性充分推出half，B?未付；与全前缀RET付款不同。 |
| retained-comparison-pool-controls-static-private-block-loss | replaced | 原稳定edge_id在本包新路径更新RET v3引用；只给𝒮≤L、终点等号与局部ε贡献。 |
| regular-layers-pay-singleton-block-price | retained | 完整块置换和严格实际单占给REG/LAYER；有限mask不是任意人数独立证明。 |
| regular-symmetric-slice-reduces-fixed-policy-price-rows | retained | REG切片可用p+1同向查询；全部有序Γ和逐行上证书仍须保。 |
| two-role-tax-kernel-in-kept-early-branch | retained | 指定保持早期动作的同一真实枝三IC消对称核，不能无条件冻结未来。 |
| single-terminal-exchange-to-all-cross-coverage | retained | 同一最优元组的全早期角色×查询合同给β_k；仅局部配对不够。 |
| waterfill-credibility-distinguishes-fixed-masses-and-uniform-child | retained | context范围比较，三客户自由阈值、53客户固定高尾与P孩子统一缩尾量词分开。 |
| thirty-one-clients-refute-existential-safety-budget | retained | 31客户真完整SPE的唯一安全最优面费用32>31，精确否存在SSR。 |
| restricted-safety-dual-prices-thirty-one-client-gap | retained | 同一静态矩阵独立原/对偶证书给111/8<14，经验低费不等安全最优。 |
| ordered-safe-blocks-build-linked-three-query-projection | retained | 先合十一原行及两回复身份后联合极小；不能逐块先min。 |
| negative-prefix-family-forces-first-credit-factor-two | retained | 同一完整解析族使每个预先固定α<2在足够n失败；终点为正。 |
| universal-price-vertices-give-fixed-policy-contract | retained | 普适V_p加固定有序σ线性Γ给有限合同及零福利上证书规则。 |
| all-big-policy-instantiates-seven-maxima-seat-obstruction | retained | 增一小题保全部历史恒大策略，否定恰六人七极大的特定无条件seat行。 |
| all-big-calibrates-bare-theme-root-row | retained | 任意m恒大族R_1=OPT−(m−1)K/m的等号校准，不给普遍裸K保证。 |
| hall-cancellation-source-fee-exact-remainder | retained | 同一次实际取消、同一源查询分母的三项POOL与D=0边界；incoming仍独立。 |
| local-potential-reset-sums-all-actual-rows | retained | 同p与原σ的局部POT/RESET沿actual求和；较早位置signed债未付。 |
| bank-controller-defeats-bare-k-for-every-m-at-least-three | retained | 既有完整银行控制器逐m≥3否裸K，m3即可；不是m≥4菜单Jensen阈值。 |
| one-follower-decorrelation-pays-two-player-bare-k | retained | 恰一末回复、最优两索引iid给m2裸K普遍成立，重复最优槽保重数。 |
| optimal-tail-static-menu-penalty-enters-any-action-ledger | retained | 保round55现行ETA边；静态λ控制后仍有重新强制B的真实C_A−C_B，不能复活14fd旧边。 |

21个core在receipt各自写出本轮比较、新读/继承证据、结论和剩余义务；私有B?、privateledger、CA-PREFIX、RET另按新读实质重写。保留边的完整字节、端点和证据审计见 `prior-assets-audit.json`，不是用计数代替数学判断。

本definition没有formal follow-up对象对，故top-level `closed_overlaps=[]`、`follow_up_tasks=[]`。原00c291四项历史closure作为有效prior supersession的 `retained_closed_overlaps` 与来源追溯保存，不把它们伪装成本新定义提出的新比较义务。

## 交付与绑定边界

只在worker隔离目录写出mirror；共享clone无写入、Git、native mutation、凭据读取或spawn。Root复制到reserved路径后串行执行edge-bind/check，更新新边最终字节SHA再提交receipt。worker稿故意不制造review_digest。输入freeze保33个指定对象pin，完整93 refs/71文件的真实SHA均已核；全registry观测SHA仅用于取证，不要求追随无关对象的后续变化。

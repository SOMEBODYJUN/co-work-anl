# 全树双重重置与终局换位：未闭合的共同付款记录

2026-10-24。**探索 checkpoint；没有新增一般福利界，也没有证明 cap1/cap2。** 采用原 CAG-MODEL：单位客户、单位玩家、任意有限非空共同目录、全部有序历史纯 SPE。以下等式只定位真实未付项，不以表示本身充当推进。

## 1. 目标和已经存在的接口

固定完整历史纯 SPE \(\sigma\)，实际叶 \(Z=(S_1,\ldots,S_m)\)，实际覆盖 \(C\)、收益 \(u_i\)。取一个最优比较联合 \(O\)，令

\[
I=O\cap C,\qquad G=C\setminus O,\qquad R=O\setminus C.
\]

真正目标仍是

\[
|R|\le |I|+2|G|,
\]

而不是已被旧完整例反驳的 \(|R|\le W\)。

`R-cd789330fc7141299ac491bbb3ffa420/round5/credible/all_fresh_submarkov_elimination.md` 已把正 future 广播送到真实 prescribed contexts，past 正项只送 actual 角色券。`round6/credible/safe_coupon_netting.md` 已给同 context SAFE/CLIP 和同角色 pooling；`round6/relay/global_role_coupon_hitting.md` 已给全部 context 的角色集合 HIT。这些都没有给不同来源合计的 actual 钱包上界，本轮不重复认领。

## 2. 四叶双重重置实际给出的方向

取任意合法历史 \(g\) 长 \(i-1\)，记 \(a=\sigma_i(g)\)。四个真实 completion 为

\[
B=\operatorname{finish}_\sigma(g,a),\quad
A=\operatorname{finish}_\sigma(Z_{<i},a),\quad
E=\operatorname{finish}_\sigma(g,S_i),\quad
Z=\operatorname{finish}_\sigma(Z_{<i},S_i).
\]

令

\[
v=u_i(B),\quad D=u_i(A),\quad w=u_i(E),\quad u=u_i(Z).
\]

两条**不同历史**的真实 IC 给

\[
e=u-D\ge0,\qquad \ell=v-w\ge0.
\]

因此

\[
(v-D)-(w-u)=e+\ell\ge0.\tag{SQ}
\]

这是整行收益比较，不是按客户重权的 IC。所有后继均沿同一原 \(\sigma\) 真实改变。\(E\) 不得换成冻结 \(B\) 的后继，也不能因 \(a=S_j\) 将其与另一有序历史的规定叶识别。

本轮尝试用 \(\ell\) 控制同 actual 角色多份 \(\beta\) 的总量，但 (SQ) 本身仅以 \(v\ge w\) 限制 off-history 规定利润的**下侧**，不能给付款所需的 \(v\) 上界。现有图分母使用 \(v\)，所以较大 \(v\) 可以降低同一输入的 \(\beta\)；但还没有一条允许对所有不同 \(g\) 共同求和并由同一 \(u_i\) 支付的关系。不能直接删去 \(e+\ell\) 后声称两种前缀重置去相关。

## 3. BG-NEW 是旧候选，本轮没有重新产生证据

本轮独立写到过任意合法背景 \(b\)、余 \(r\) 人下的候选

\[
M_r(b)\le D_b(c)+U_b(c).
\]

root 指出这正是 `R-324fbf8f72b041578583b51189f13d1a/global_mechanism.md` §2–3 的 **BG-NEW**；读原稿后确认。其 \(r=1\) 基例、背景旧利润的解释和朴素删除一个比较主题的私有块缺口都已有，不认领新候选或新基例。

具体地，在实际当前行动 \(A\) 后使用 \(r-1\) 人归纳，删除一个比较主题 \(T_q\) 留下

\[
T_q\setminus\left(B\cup A\cup\bigcup_{j\ne q}T_j\right).
\]

不能把最小这样的私有块直接交给当前最终利润支付。root 提醒旧 71 客户例以及 root-tax 的实际前缀 \(h=(A)\) 已否定所需局部断言。任意背景 extra-one 前两人 floor 的解析分离 `R-cd789.../round5/menu/pair_attack.md` 也不能作为 BG-NEW 的反例：它的背景已覆盖全部客户，BG-NEW 的左侧新增覆盖为零。

本轮为该候选刚写的旧证书诊断在运行前删除；没有扩充同类阴性证据。BG-NEW 仍 OPEN，仍须跨步共享信用。

## 4. 终局 token 换位只给无损运输，不给共同容量

对任意合法完整有序终局 \(V\)，交换角色 \(j,k\) 的主题，得到 \(V^{jk}\)。终局客户负载逐客户不变，所以

\[
u_j(V)=u_k(V^{jk}),\quad
u_k(V)=u_j(V^{jk}),\quad
u_\ell(V)=u_\ell(V^{jk})\quad(\ell\notin\{j,k\}).
\]

这允许把一个利润 token 连同其主题搬到另一角色；**没有声称**交换后的终局或其路径是 SPE。把 token 放在末位后确可调用该有序末位前缀上的原真实 IC，但改变末位行动同时改变所有 incumbent token 的分母。

具体在固定其他角色负载 \(b_x\) 下，末位由 \(A\) 改为 \(T\)。定义

\[
L=\sum_{x\in T\setminus A:\,b_x>0}\frac1{b_x+1},\qquad
H=\sum_{x\in A\setminus T:\,b_x>0}\frac1{b_x+1},
\]

以及覆盖变化

\[
\Delta W=|\{x\in T\setminus A:b_x=0\}|-
|\{x\in A\setminus T:b_x=0\}|.
\]

逐客户给当前利润变化 \(\Delta u=\Delta W+L-H\)，旧角色总利润变化 \(H-L\)。单个 incumbent 的正损失逐客户不超过其修改前份额的一半。这是已有 `research/current/customer_attraction/terminal_reply_transport.md` §1、§5 的同一损耗机制，不另认领为新付款。

同时 token 方案的未付项是：连续换位并沿真实 IC 树上行时，很多互斥终局中的旧 token 都可能把这份“修改前一半”重新作为库存。局部半损失不能相加后称为同一 actual 客户/角色只付一次。换位还可能把相对原 \(\sigma\) 的最后偏离位置推到更晚；不能默认 token 仍对应交换前 IC 树的旧 actor。tree-dual 分支已明确提醒这一点。

没有构造一个同时运输全部最优 token、保留其余 token 损耗且最终每个 actual 角色容量至多 \(2u_i\) 的流；单 token 的等值搬运也不蕴含这样的流存在。

## 5. 本轮准确交接

没有提交成熟新关系供独立复核；没有新的完整 SPE 反例、有限搜索或数值正证据。四叶比较没有支付 actual 共同容量；BG-NEW 已去重；终局换位未闭合同一库存的损耗预算。上述三项均保持探索身份，不能提高一般主目标、BG-NEW 或 role-cap2 的状态。

若继续，承重结果必须是一项真正跨全部来源的支付，例如将同一批最优源的净终端金额 \(A_i\) 同时控制为 \(A_i\le2u_i\)，或直接控制 \(|R|\le|I|+2|G|\)。不能先假设该共同容量，再由守恒把它重写为结论。

## 6. 后续弱安全值付款尝试：仍无一般常数结论

root 随后要求改攻更弱但仍全输入的实际付款。对任意合法旧负载 \(b\)、余 \(r\ge1\) 人，定义原静态安全值

\[
v_r(b)=\max_p\min_{Y\in\mathcal S^{r-1}}
\mathbb E_{T\sim p}\sum_{x\in T}\frac1{b_x+1+c_x(Y)}.
\]

这里静态 \(Y\) 不能观察查询 \(T\)。所攻候选为当前真实收益 \(u\ge v_r(b)/2\)，或 \(r\ge2\) 时真实首两人和 \(u_1+u_2\ge v_r(b)\)。两者目前均未获证明；没有认领为一般弱常数福利界。

### 6.1 最小坏人数只有合法输入，没有自动闭合

若半值候选失败，取最小坏剩余人数，置 \(v=v_r(b)>0\)、实际 root 收益 \(u<v/2\)。每个真实更深历史增加的固定负载 \(d\) 可填入原静态竞争槽，故其剩余安全值 \(v_s(b+d)\ge v\)。最小性于是给全部更深 prescribed 角色收益至少 \(v/2>u\)。

这一步保留全部离轨历史，但**仍不足以完成付款**。root 提醒的旧伪菜单机制是：很大的全二元子集目录，根 \(\{a,b\}\)，尾部各选 \(a\) 或 \(b\) 加不同私有客户。可让根仅约 \(4/r\)，尾部各约 \(1+2/r\ge v/2\)，而 \(v\) 约为2；尾部可改选两个 fresh 客户获2，因此这不是 SPE。它准确表明，不能再只用“所有尾在阈值以上”的 stationary/整叶条件替代其真实 IC。本轮没有把它做成另一份新有限证据。

实际试用全部 IC 的第一条接法，是将 root 各查询枝的真实尾菜单合并为一个不观察查询的静态分布，以证明其菜单值至多 \(2u\)。每个单独 root 查询利润的确不超过 \(u\)，但把不同查询枝的后继独立于查询后，新增的去相关债尚未获付。这里没有用“对角都不超过 \(u\)”推出自由菜单值界。

### 6.2 首两人换位未支付高阈值孩子

另一接法试图从实际首对 \((A,B)\) 交换为 \((B,A)\)，把同负载尾子 SPE 移植后交换二人的终局利润。移植尾子局本身合法，但第二节点的未受祖先承诺限制的可信阈值 \(\mu_B\) 可能高于交换后第二人的利润，阻止该首对实现。此处正是已有 `round6/global/credible_adjacent_transposition.md` 的阈值障碍，不是当前两人钱包的新收入。

尤其，存在一个可实现 swap 叶不表示原 \(\sigma\) 的 root 可以偏离并自行选中它；原策略在该孩子可能指定另一份可信续局。不能从“交换后首对总和相同”或“某个孩子第二人很高”推出原实际首两人和已获支付。

### 6.3 末位 envelope 的局部 factor2 不能迭代

还尝试先消去真实末位：末位最佳回复确实最大化固定前缀上的 Rosenthal 势增加量。将这个最大值吸收到一个前缀 envelope 后，一个 incumbent 的末位回复切换可按单单位分母变化给局部 factor2 比较。但消去下一位时，其原真实 continuation 是 SPE，**不自动最大化这个 envelope**。因此不能逐层复用同一最大化论证，不能把一个末位的 factor2 宣称为任意 \(r\) 的半安全值 floor。此点只作为本轮证明尝试的准确断口保存，不新增局部常数定理。

root 曾提供统一缩尾税额的一个可能全路径接口，随后立即纠正：\(d_A\le u\) 只控制 root 强制 \(A\) 后原规定尾的那条叶，内部离轨 prescribed 叶的 root 利润可能更大。因此本稿不使用“整个 root 孩子的 max-path-regret 都不超过 root 钱包”的断言；它受已有 ancestor-promises-and-reset 边界阻止。

本轮后续没有生成新数值样本，亦未证明更弱的全人数常数付款。所缺仍是一个实质使用全部后继 IC 的共同去相关或跨步预算，不能仅以候选的命名或上述合法归约代替它。

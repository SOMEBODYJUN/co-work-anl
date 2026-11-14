# 第三阶段数学比较报告：M-b1b4276f0ec747ed8c347bda65c9e0af

## 任务与读取范围

主任务为 `customer-attraction-3a-3a-11c0fae95913e6f4`，核心对象为
`M-b1b4276f0ec747ed8c347bda65c9e0af`，registration pin 为
`8022368eb10c10d6e8989de8ec4702b581017b911828dc64bb96bdb1a251f0f5`。
任务声明的 CAG-MODEL（`customer-attraction/common-catalog-full-history-model`）和
`M-e394b173b9b1419588c6c380da4bd326` 都已完整读取。45 个 reading refs 均逐字节读取并与声明 SHA256 核对，全部通过；JSON 全部解析，代码和 Markdown 全文扫描，7,973,103 字节的
`complete624_actual4_R00_v1_matrix.json.gz` 已解压读取（44,009,386 字节），未把二进制证据当成未读。

任务原先把 M-b 与 M-e 标作 3B follow-up。仓库中已经存在并通过绑定的
`boss2-six-cross-shared-pair-to-query-hierarchy` accepted 边，故本报告复用该边，不再制造重复边。

## 共同模型、量词和可见域

CAG-MODEL 的对象是有限单位客户集 (N)、有限非空**标签**目录
(mathcal S) 及任意覆盖映射 (operatorname{cov}:mathcal S	o2^N)；不同标签可以同覆盖，空标签和零客户均保留。(m) 名单位权提供者按固定顺序各选一次，观察全部先前有序行动，允许重复行动。终局客户价值在覆盖者之间均分：
[
c_x(s)=#{i:xin S_i},qquad
u_i(s)=sum_{xin S_i}1/c_x(s),qquad
W(s)=left|igcup_i S_i
ight|,qquad
mathrm{OPT}_m=max_{Tinmathcal S^m}left|igcup_iT_i
ight|.
]
完整纯 SPE 的量词是对每个玩家 (i)、每个合法有序历史 (hinmathcal S^{i-1})、每个合法替代标签 (Tinmathcal S)，沿**同一完整策略在偏离历史后的真实后继**比较实际收益与偏离收益。不能冻结在轨后继，不能把不同有序历史按负载合并成同一个策略节点。本定义本身不证明六人半覆盖目标 (2Wgemathrm{OPT}_6)。

M-b 固定实际六位 (A_1,ldots,A_6) 和完整策略，固定 actual 第四人真实源历史；强制该源选择 (T=R) 后，真实末对为 (B,C)，再回到同一源历史强制同一真实 (C) 后，真实末对为 (J,V)。每个客户的隐藏会员为
(h=(b,c,j,v)in{0,1}^4)，其中同一 (c) 同时出现在第一枝末题和第二次源动作。记
[
p=sum_{j=1}^3a_j,quad ell=sum_{j=1}^5a_j,quad
z_1=p+t+b+c,quad z_2=p+c+j+v,quad
eta_1=p+t,quadeta_2=p+c.
]
0/0 份额定义为 0；所有其它分母按该历史负载取值。源两条 IC 使用同一源收益预算，合并时按总源权支付一次，不能把两个互斥后继各记一份 actual 收益。容量 (K) 对共同目录主题作统一上界。

固定第一类非对角轨道 (e=(i,j)), (i
e j)，并使用 17 个合法查询
[
Q_0,ldots,Q_{16}=(A_1,ldots,A_6,T_i,B_i,C_i,T_j,B_j,C_j,R_e,Z_e,
overline T_L,overline B_L,overline C_L),
]
其中 (L={1,ldots,6}setminus{i,j})，横线只是对合法纯主题的均匀查询记号，不是目录中的分数主题。共同可见型至少保留 actual 六位、六个旧三位词的 hist、R/Z 四态；也可压到
[
v=(p,ell,t,q_0,ldots,q_{16},mu_{TB},mu_{TC},mu_{BC}),
]
其中 (mu) 是剩余四索引的同索引二阶矩。严格性只在 actual 第四源、强制 (R)、第一类非对角轨道和这个固定 17 菜单上证明；不是所有源、历史、目录或完整六人游戏的结论。

## M-b 的完整 whole_result

令 (mathcal P_{76,l}) 是只固定查询 (Q_l) 时，34 条基础行加两枝六主题全部强 PAIR 的共同可见投影；该投影允许每个 (l) 使用各自隐藏提升。令 (mathcal P_{332}) 要求 17 个查询共用一份隐藏 (h=(b,c,j,v))，保留所有不含 (Q) 的 60 行，并对每个 (Q) 加 16 条含 (Q) 的 last/safe/PAIR/对角 PAIR 行。令 (mathcal P_{616}) 在同一提升上再加入两个旧查询的精确 same/off 联合索引 PAIR，共 284 条新增行。令 (mathcal P_{624}) 再加入原真实 (R)、(Z) 末节点对同一宏 (B/C/J/V) 的八条零预算反查行。

在共同细化的 actual-linked 域上，M-b 给出完整严格链
[
oxed{mathcal P_{624}subsetneqmathcal P_{616}
subsetneqmathcal P_{332}
subsetneqigcap_{l=0}^{16}mathcal P_{76,l}.}
]

两道包含先由同一隐藏提升的删行/投影得到：

* 删除 616 的 284 条跨查询行得到 (mathcal P_{616}subseteqmathcal P_{332})。
* 332 的共同提升固定任意一个 (Q_l) 并删去其它查询行，得到 (mathcal P_{332}subseteqigcap_lmathcal P_{76,l})。
* 新增的 (mu) 坐标只做可见型细化；旧提升按质量比例细分，保持全部质量和预算，不是把 17 份提升错误拼成一份策略。

第三道包含的域要单独记账：M-b 第 8 节定义 (mathcal D_{17})，在原固定 16-hist 之外加入确定型
[
a(H_*)=(0,0,0,1,0,1),qquad
(T_i,B_i,C_i)(H_*)=(1,1,1)quad(i=1,ldots,6),
]
并允许合法 R/Z 四态。原 5744 与 5775 见证以 (H_*) 质量 0 嵌入；624<616 的新见证使用 (H_*) 正质量。因此不能把第三道严格性写成原 16-hist 限制域内已经成立。

M-b 还证明了有限提升与**全部非负投影行**等价。对固定可见质量 (m_v)，隐藏提升空间是各型 16 态单纯形的有限直积；任意非负行权 (lambda) 的投影为
[
Pi_lambda=B_lambda-sum_vm_vmin_h
sum_alphalambda_alpha E_alpha(v,h).
]
紧凸分离给出
[
left[
oralllambdage0, Pi_lambdage0
ight]
Longleftrightarrow
left[exists	ext{ 一份共同隐藏提升同时满足全部原始行}
ight].
]
该等价包括源总权为 0 的面，不能只归一化源权而遗漏这些投影面；它仍只是局部形式质量提升，不是完整 SPE 策略充分性定理。

## 三道严格性见证和精确证据

### 1. (mathcal P_{332}subsetneqigcap_lmathcal P_{76,l})：5744

输入 `master_cuts/dynamic_5744_exact.json`，SHA
`17fc8c5f5cbb9464747802fc2a3ca8ed3c37aa6472b981c804b9c3806d2ebfa0`。
同一 actual 可见分布有 17 份独立有理隐藏提升；每份质量等式和 76 行全部精确通过，共核 1292 条预算，Main 独审 `main_verify_single_lifts_5744.json` 为 PASS。于是该点属于 (igcap_lmathcal P_{76,l})，且不是只通过 17 条手选权。

同一点上的 23 权共同行来自
`joint_common_denominator_5744.json`（SHA
`fcb9be905ab4282ab3ff90293ef47f196ab08e86f45e106d883d3944a655d3ab`）：
源权 (322,178)（总 500），actual 末价 (B,C,J,V) 权 (17,5,60,61)，容量 (V) 权 19，及各项 last/PAIR 权。其外部预算为
(500u_4+143u_6+19K)，在 4,849 个语义列上精确负：
[
-
rac{22186387251781301735192854216376511216449071620762450982858755328462613921054790415003309372693818702527979545134208653206957776497}
{141490782907623432045711252283612392613342535455539765478218119558168295908981803578521315220010122670297703327094277443274432555184}
approx-0.0003136089403967234.
]
`main_verify_portfolio_500.json` 为 PASS，故不是 LP 浮点 gap。该负行排除共同 332 提升，而 17 份单 Q 提升仍分别存在。

### 2. (mathcal P_{616}subsetneqmathcal P_{332})：5775

输入 `master_cuts/dynamic_5775_exact.json`，SHA
`81983304076358d591cbdac2e6bf7a4b697fc2854aad40918e8cf8cf2d99dd02`。该点有 56 个正可见型；`recover_332_lift_5775_v1.py` 恢复 79 个非零有理隐藏原子，全部 332 行和质量等式精确可行，Main `main_verify_332_lift_5775.json` 为 PASS，最小旧行余量为 0。

12 权新跨查询行的源权为 267,146（总 413），末价权 (49,45,28,42)，容量 V 权 14，last/PAIR 权按正文第 5 节；其新增核心是第一枝真末对 (B,C) 对旧主题 (T_i,B_j) 的强 PAIR。共同预算
[
413u_4+164u_6+14K
]
在同一点上精确为负，归一值约
(-0.0006503689544503674)（精确负分数见
`exact_332_lift_cross_strictness_5775_v1.json`，SHA
`39655d2eeb9f807053614ff17d830246199804dbca266b9784e116e8f8d09385`）。
`main_verify_cross_pairs_5775.json` 和 `main_verify_332_lift_5775.json` 均 PASS；因此不是把 5744 的旧负值移植到 5775。

该 12 权还满足逐客户对称差恒等式：
[
P^pi_{lm}
=	frac12(P_l^{diag}+P_m^{diag})
+
rac{(q_l+q_m)/2-
ho_{lm}}
{(eta+1)(eta+2)}.
]
在 actual 第四源的第一枝，(eta_1=p+t) 可见，故附加项独立于隐藏位并穿过同一 min。192 种 actual 合法参数型和 3,072 个逐隐藏恒等式已由
`cross_query_disagreement_identity_5775_v1.json` 与 Main 审计精确核验。这个恒等式解释新增信用来源，但仅凭非负信用仍不能排除其被其它 332 行推出；79 原子共同提升才完成严格分离。

### 3. (mathcal P_{624}subsetneqmathcal P_{616})：5799 + (H_*) padding

`reverse_terminal_5799_one_v1.json` 绑定 5799 基点（SHA
`63edbafd53493a20ec64ced5f09a694ead3f894bfb6419cde425de0b3a1710c1`）。
该点本来违反 616，不能直接拿新增 624 正权宣告严格性。先恢复一份 616 提升，其自由源付款比实际 (u_4) 多
[
delta=

rac{2465201632061400404249536195487906900932734809402071846465468132650811843841}
{1025894098230233788911678187335946670200853177785791271108828445442492646323610560}
>0.
]
加入 (H_*) 正质量 (6delta)，取 R=Z=1、宏隐藏 ((b,c,j,v)=(1,1,1,1))。补齐后有 57 个可见型、77 个隐藏原子，实际 (u_4,u_6,K) 同源更新；全部 616 行和 17 个 actual 末价/容量约束精确可行，最小余量 0。新增 624 反向 Z→V 权行的精确余量为
[
-
rac{148845568998121138356228513900153618711355035474766353741403675003844902443555714733}
{115156612526343742805335876528460013730045769206455070181965993000919799549825285360000000}<0.
]
`main_verify_reverse_terminal_strictness_v1.json` 为 PASS，核 616 行、质量、actual 关联和新增负分数。此证明只在 (mathcal D_{17})（允许 (H_*)）上给 624<616，不能升级为原固定 16-hist 域严格性，也不能声称 5799 主图本身完整可行或构成完整 SPE。

### 4. 624 原始矩阵的有限闭合证据

`complete624_actual4_R00_v1_contract.md` 和其映射/矩阵证明：在原 11,418×7,639 ZZ 基底上加入 4,992 个隐藏列、312 条边缘等式（正反双行）和 624 条预算，得到 12,666×12,631 矩阵。每个 (H,g,r,z) 的隐藏质量使用同一 16 态 (h)，索引重数 (M_{Hg}/30) 只乘一次；零质量组与零 R/Z 边缘仍保留。映射 SHA 为
`24a601ebc1e2f7dc5e175bca453a5ab05433e046dfc7c2a782e830849817d109`，矩阵 SHA 为
`556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a`。
`main_verify_complete624_v1.json` 为 PASS：3,115,008 个新系数、1,920 个字面查询检查、所有零质量域保留、原行列前缀不变。该证据证明固定结构的有限表示和行列语义，不证明其优化最优值、全目录闭包或 SPE 充分性。

## 对 M-e 的比较、边和处置

M-e 的一般结论是在任意有限实例、任意完整有序历史纯 SPE、任意合法共同标签菜单下，先固定同源第一枝真实 C，再把两枝强 PAIR 和 34 条预算在同一隐藏 ((b,c,j,v,s,s')) 上合账后取 min；它给出一般合法性和源总权一次支付。M-b 把这套 34+双 PAIR 合同具体化到 k=3、17 个查询和 76/332/616/624 的固定投影层级，并另给三组 actual-linked 严格见证。因而 M-e 是 M-b 的共同前提贡献，M-b 是该一般合同的固定菜单/固定轨道强化，二者不是等价对象，也不能把 M-e 单独当成 M-b 的严格性证据。

可复用的既有边（不新增）：

```json
{
  "edge_id": "boss2-six-cross-shared-pair-to-query-hierarchy",
  "kind": "implies",
  "status": "accepted",
  "premises_mode": "all",
  "relation_mode": "unconditional",
  "source_ids": ["M-e394b173b9b1419588c6c380da4bd326"],
  "target_ids": ["M-b1b4276f0ec747ed8c347bda65c9e0af"],
  "conditions": "完整有序历史纯SPE、有限共同标签目录；同一源两枝共享C；17查询为固定合法主题或合法纯主题的归一平均；same/off耦合对全部客户共同固定；严格见证限actual4/R/第一非对角轨道和同一细化可见域。",
  "evidence": [
    {"path":"archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md","sha256":"7547538073d8edf42f2430c5ed0d4139c2129fdaa8817ea0dbcba591552328e5"},
    {"path":"archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md","sha256":"6553bdd54417ea5cd1bc2d66480f39086e274ba1779bcab43cefb14fcb71f8e0"}
  ]
}
```

该边的 whole_result 是 34 行/双 PAIR 合法性、共同隐藏投影和
(mathcal P_{616}subseteqmathcal P_{332}subseteqcap_lmathcal P_{76,l}) 的一般推导；其 contribution/remaining 已准确写明：两道严格性依赖 5744/5775 有理见证，624 严格性另依赖原末节点行和 H* padding，不由一般 PAIR 恒等式单独推出。现有
`boss2-six-cross-complete624-projection-pays-lift`（source M-b → target M-ddceaa3d53064498b3e833a32e1f3b6f）继续复用 624 固定结构闭合，不把 624 局部提升升级为全局 SPE。

因此任务中标注的 M-b/M-e follow-up 可以写入
`closed_overlaps`：二者数学接口已由上述 accepted canonical edge 解决，继续发布 3B 任务会重复同一比较。没有新的独立 source/target edge 需要生成；不要把共享 CAG-MODEL 定义造为 hub 边。

## contribution / remaining 的严格账目

**本任务的 contribution（已完整支付）：**

1. 在 CAG-MODEL 的完整历史量词下，精确定义 76、332、616、624 四个投影族及其同一隐藏状态、same/off 二阶矩、源只付一次的预算语义。
2. 证明三道包含的非严格方向，并用不同 actual-linked 有理点分别完成两道原 16-hist 严格性和一道 D17 严格性。
3. 证明固定 624 行族上“全部非负投影权行”与一份共同有限隐藏提升的双向等价，包括源权为 0 的投影面。
4. 给出完整有限矩阵表示、索引重数、零质量保留和独立系数/恒等式审计。

**whole_result（本对象实际得到的完整结论）：**

在上述固定 actual4/R/第一非对角/17 菜单和相应共同细化域内，
[
mathcal P_{624}subsetneqmathcal P_{616}
subsetneqmathcal P_{332}
subsetneqigcap_lmathcal P_{76,l},
]
其中第三道严格性采用含 (H_*) 的 (mathcal D_{17})，前两道严格性可在原 16-hist 见证中成立；624 固定结构还具有全部非负投影权与一份共同有限提升的精确等价。

**remaining（明确未付义务）：**

1. 隐藏提升是局部客户类型质量，不是一个在全部有序历史上同时定义行动的完整纯策略；没有 SPE 充分性。
2. 没有证明任意目录、任意客户型域、任意源/历史/菜单的全局 624 闭包；固定 16/17 hist 和第一非对角轨道不能覆盖全域。
3. 没有给出六人目标 (2Wgemathrm{OPT}_6) 的全局共同付款证书，也没有构造 (W<mathrm{OPT}_6/2) 的完整 SPE 反例；5744/5775 的必要 LP 点不能当成反例。
4. 若研究问题坚持原固定 16-hist 域的 624<616 严格性，仍需另找一份不使用 (H_*) 的 16-hist 见证；当前报告明确不把 D17 见证迁移回 16-hist。
5. 完整 624 矩阵的精确最优值/原始对偶证书未由这 45 refs 本身宣告；可复用 canonical 结构边，但数值优化和 global half 仍需主任务/后续对象承担。

## 建议收据覆盖

```json
{
  "coverage": {
    "M-b1b4276f0ec747ed8c347bda65c9e0af": {
      "state": "linked",
      "object_pin": "8022368eb10c10d6e8989de8ec4702b581017b911828dc64bb96bdb1a251f0f5",
      "comparison_scope": "完整45 refs、CAG-MODEL、M-e及三道严格见证；同一actual4/R/第一非对角/17菜单；原16-hist与D17域分别记账",
      "reason": "复用 accepted canonical edge boss2-six-cross-shared-pair-to-query-hierarchy；M-e/M-b follow-up 已解决，无新边。",
      "edge_ids": [
        "boss2-six-cross-shared-pair-to-query-hierarchy",
        "boss2-six-cross-complete624-projection-pays-lift"
      ]
    }
  },
  "assets": [],
  "closed_overlaps": [
    {
      "core_id": "M-b1b4276f0ec747ed8c347bda65c9e0af",
      "peer_id": "M-e394b173b9b1419588c6c380da4bd326",
      "reason": "M-e 的34+双PAIR一般合法性和共同隐藏合账已由 accepted edge boss2-six-cross-shared-pair-to-query-hierarchy 接到 M-b；M-b 的固定17菜单层级和三组严格见证已独立完成，本次无剩余3B比较。"
    }
  ]
}
```

## 证据引用索引

核心正文与模型：

- `archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md`，SHA `6553bdd54417ea5cd1bc2d66480f39086e274ba1779bcab43cefb14fcb71f8e0`。
- `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`，SHA `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`。
- `archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md`，SHA `7547538073d8edf42f2430c5ed0d4139c2129fdaa8817ea0dbcba591552328e5`。
- `research/workspaces/six-boss2-20261111-cross/joint_requery/formal_query_projection_hierarchy_v1.md`，SHA `c1e5a8b8b06eb2ac70b64a44ea8e4a7d9625c9811cbdf5eb73e139da8d54a366`。
- `research/workspaces/six-boss2-20261111-cross/joint_requery/portfolio_comparison/formal_portfolio_strictness.md`，SHA `372b2dea7f7fe94ebd3514b044310c1b1aa73b0fd04ae0f43bd08cfc3561a0c5`。
- `research/workspaces/six-boss2-20261111-cross/joint_requery/formal_reverse_terminal_strictness_v1.md`，SHA `52a39a7babe4ae92fc18e808ca56877cac0fb15f5f06f069adc0001aa64381a5`。
- `research/workspaces/six-boss2-20261111-cross/joint_requery/complete624_actual4_R00_v1_contract.md`，SHA `84d2ba9d8da85879ab5f4847652f48f510a8566df445c99058ff9552d874ba39`。

计算/审计来源：

- 5744 输入 `dynamic_5744_exact.json` SHA `17fc8c5f5cbb9464747802fc2a3ca8ed3c37aa6472b981c804b9c3806d2ebfa0`；17 份单 Q 提升 SHA `329b5bca4ad9fdfa3e59b8fb0fcaeca396eceac950edc2d8c1c8ca8f67eca793`；500 权行 SHA `fcb9be905ab4282ab3ff90293ef47f196ab08e86f45e106d883d3944a655d3ab`。
- 5775 输入 SHA `81983304076358d591cbdac2e6bf7a4b697fc2854aad40918e8cf8cf2d99dd02`；332 提升/严格负行 SHA `39655d2eeb9f807053614ff17d830246199804dbca266b9784e116e8f8d09385`；跨查询包 SHA `bf9714af7e01fff4cddd33ead2ce41c014943ead5679e1b75a5160e9f9257759`；恒等式 SHA `4527dce663e0f6bc6441497f5fd03253de39051b0602ea4eaac5e7bb0987a490`。
- 5799 strictness separator SHA `3b39262c153be351853f2625809da5679e634648d895c233b554868f1bd0077c`；padding SHA `a06786cd8a5176754544d614034eeec78efc6a733f8ad0552f5ce760b48a14ce`。
- 624 矩阵 SHA `556c3cac51e87a699d1f3a9c427f556836932b6fc2399fa330f375c6efd8231a`；mapping SHA `24a601ebc1e2f7dc5e175bca453a5ab05433e046dfc7c2a782e830849817d109`。

未执行任何 Git commit/push，未修改共享 registry、canonical edge 或队列元数据。

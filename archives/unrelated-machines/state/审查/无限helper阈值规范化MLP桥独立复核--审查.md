# ∞ helper 对规范化 M-LP 的独立实质审查

本报告为 Boss6 已 claimed 的 `boss6-inf-chain-transfer-3b-ea6be0c00b1186cf` 提供辅助独立审读，不构成另一个主覆盖包。仅只读 clone `/workspace/scratch/62622ba39554/co-work-anl-boss6`；没有修改 Git、队列、`work.py`、登记身份，也没有重跑旧程序、求解器或枚举。新桥身份 `M-b86375379821448d857231e8c38d8f46` 由父 Boss 已分配，本报告不生成身份。

**最终结论（已核修订版）。** 2026-11-11 又完整实读修订稿 `/workspace/scratch/62622ba39554/staging-inf-chain-transfer-3b/mlp-interface-complete-proof.md`，实算 SHA `08fbaf632f6b5172e0a31b34708837633ee39c2a9c37023a38a5cb1ebdd75a52`。该数学版本可接受，以下所述旧错误已由该版纠正。新稿 §2 的同一 `D∞` 输出、同一 M 和同一 λ 的 M-LP 可行性双向保持，及 §5 的 `I_T/J_T` 精确值，均经本报告直接按 (4)–(8) 独立重构，通过。有限 H 的准确合同为：正向保证仅需 `M≤λH`，反向对所有 `M>0` 成立；高于 λH 的分数 helper 仍可能可行。4 副本有限链的 cap 值 `4/3`、旧 4 玩家 private/shared=100 例的 cap 值 `125` 均正确。原 CONFIG/整数精确值、人数重计以及新族 `Θ(N^(1/6))` 也通过。

**旧稿的两项已纠正接口。** 初读稿 `mlp-interface-complete-proof.md` 的 SHA 为 `85db14eb1ffb6aa0d42158eeb8714ef3f624dd851821de9036444d2b4af68ed0`。该稿 §3.1 的“R 不减任何估值”为假；§3.2 对 λ=1 cap 模型无条件声称原值 CONFIG(M/2) 转换也为假。第一项可逐配置修复，第二项必须实质撤回并加上小端条件；不能以引用原论文 Theorem 2.3 代替检查。主桥 §2 与这两处接口独立，不依赖该转换，因此保持定理本身没有被反例否定。本报告下文给出完整替代证明与精确反例。

## 1. 定义、证据与本次实际阅读范围

实际实读了 clone 根 `AGENTS.md`、`research/IMPLEMENTATION.md`、`prompts/03-map-worker.md`，本 3B task 定义及其五个 core 的当时完整 registry 记录：

- `M-080d9b22ae87408f9a673a898c7a6dc3` v3：finite unit-helper actual/CONFIG。
- `M-16209762a32e42e48ec20b76381b5e9d` v1：D∞ 的 actual/CONFIG 全正阈值保持。
- `M-7bc9eab74ecd475db7df33c3f4b75e61` v1：T-block 交域精确 CONFIG/整数族。
- `M-a9534c70ffa74fca9a91cd270468de3f` v3：原 Theorem 2.4 固定阈值整数降度。
- `M-b126c4b3ff29400589f7f38abdca4d85` v3：原 InfDegreeTwo 存在性 gap。

父 Boss 随后告知第一项已刷新 v4，pin 为 `5041d21ea4cc71de0cf1e759aade84c0cc09a86d8539510dc3683242679ff85c`；仅共享 evidence 的 P_gate 安排段变动，unit-helper 主正文及模型/statement/量词不变。此次 v4 delta 来自父 Boss 的精确实读报告，本独立报告不冒称扩审 P_gate。本文的数学只调用未变的 unit-helper §4，并已直接重证所需路径论证。

直接核对原 PDF：

- `archives/unrelated-machines/tools/evidence/retired-literature-pcsp-20261031/maxmin.pdf`，实算 SHA `7f7b21ff08b37e8489e9f60527e9aa9458dc5cf4cd6cc6804869665c24d51f7f`。
- 同目录 `maxmin.txt`，实算 SHA `5ce6cb935436e7c7cd7ea6157e618d754dc01afd9e657fca17a99dfbd5c3e846`。
- 用 `pdftotext -f 6 -l 8 -layout` 直接从该 PDF 导出并实读印刷页 6–8；另视觉查看已渲染的第 7 页，核 Definition 2.2 式 (4)–(8)、Theorem 2.3 及证明首步。另直接导出实读印刷页 12–13，核 §4 的 revaluation 条件及 InfDegreeTwo 脚注。没有声称通读整篇 49 页。

同时全文实读 `无限helper全阈值降度与三度二无限度配置间隙--定理.md`（SHA `9d56eff7715d695c85f6e45707b899633faef71dd1388c86bea1ac4fc721dbca`）、`规范化平菜单的CONFIG与正支撑LP双向保持--定理.md`（SHA `8bfbaa80b98546b6d1320e9760bb9491165e26a6cef1b6cd35eb86116c822f66`，实际使用 §4），以及主 worker 上述 staging 稿全部 §1–7。

另全文实读 `/workspace/scratch/62622ba39554/staging-cap-mlp-boundary/review.md`，实算 SHA `e5a5ce699585185b304799e0db30debf8e1d5f9d46b79f70f5977707ec512978`，并独立核其反例的全部四区间、D∞ 后计数及 big/small 边界。其 registry 搜索范围为该 worker 的报告，本独立报告不把这部分搜索冒作自己重新执行。

按原页 6–7，给 `M>0, λ≥1`，先逐玩家—物品端定义

\[
\widehat p_{ij}=R_{M,\lambda}(p_{ij})=
\begin{cases}M,&p_{ij}\ge M/\lambda,\\p_{ij},&p_{ij}<M/\lambda.\end{cases}
\]

然后 M-LP 为列容量 `Σ_i x_ij≤1`、行条件 `Σ_big x_ij+z_i≥1`、small 价值 `Σ_small p̂_ij x_ij≥Mz_i`、逐 small 端 `x_ij≤z_i`，以及非负性。没有行总 x=1 或 z=1 的普遍约束。所有 zero 端可先令 x=0：只降低列容量和 small 上界左端，其他行不变。此步必要，因为正向“重命名旧坐标”指的是清理后的正估值坐标。

## 2. D∞ 直接双向桥：全部约束的独立证明

固定一个输入 I；只按其正 owner 图构造一次 D∞(I)，不依赖 M 或 λ。对每件总正度 d>3 的旧物品 j，正 owner 为互异玩家 i₁,…,i_d，建副本 c₁,…,c_d。旧玩家 i_r 仅在自己的 c_r 保旧值；helper h_k 仅在 c_k,c_{k+1} 取 ∞，其余均零。低度物品保留。

R 保持正支撑；每个旧端在自己的副本上具有相同分类和相同 small 系数。每个新增 helper 的两个正端都被规范化为 M，是 big；其余端全为零 small。这是变量映射的基础，不是由 CONFIG 保持自动推得。

### 2.1 正向

给去零后的旧可行 `(x,z)`，固定一条链，令 q_r=x_{i_r,j}，Q=Σq_r≤1。取

\[
w_1=q_1+1-Q,\quad w_r=q_r\;(r>1),\quad W_k=\sum_{r\le k}w_r.
\]

于是 w≥q≥0，Σw=1，0≤W_k≤1。旧正端置 `y_{i_r,c_r}=q_r`，旧 z 保留；其余旧玩家在不属于自己的副本上的 zero 坐标设零。对 h_k 置

\[
z_{h_k}=0,\qquad y_{h_k,c_k}=1-W_k,\qquad y_{h_k,c_{k+1}}=W_k.
\]

每个 helper 的 big 质量恰为 1，故 (5) 成立；其 small 估值/坐标均零，(6) 为 0≥0、(7) 为 0≤0。副本 c_r 的 helper 使用恰为 1−w_r：两端分别为 1−W₁、W_{d−1}，内部为 W_{r−1}+1−W_r。加原 owner 的 q_r 后总使用 `q_r+1−w_r≤1`，全部列容量成立。每位旧玩家的正 big/small 坐标及 small 系数只是重命名，故 (5)–(7) 逐项保持，非负性保持。不同链无共同 helper，全部链同时执行即可。

### 2.2 反向

给输出可行 `(y,z)`，先去零。helper 没有任何正 small 系数，(6) 给 `0≥Mz_h`；M>0、z_h≥0 强制 z_h=0。(5) 于是给每位 helper 两个相邻 big 坐标之和≥1。对一条链的 d 个列容量求和，helper 总使用至少 d−1，所以旧 owner 在其专属副本上的总使用≤d−(d−1)=1。

令旧 `x_{i_r,j}=y_{i_r,c_r}`，低度物品原样保留，旧 z 保留，旧 zero 端设零。上式就是恢复后的旧列容量；所有旧行的正系数和分类逐项不变，因此恢复 (5)–(8)。不需要把 helper 的质量强制截成恰一，至少一已足够；也没有假设可行边际来自联合整数配置。

故对同一输出、每个有限 M>0 和有限 λ≥1：

\[
\mathcal M_\lambda(I,M)\text{ feasible}
\iff \mathcal M_\lambda(D_\infty(I),M)\text{ feasible}.
\]

λ 必须在所比较的两侧相同；固定 λ 后可行正参数集合相等，不能据此宣称该集合一定为前缀。最高值可在 `[0,+∞]` 中按 `sup(空正可行集)=0` 约定处理零端点。M=0 不属于证明；空物品输入对 M>0 时每行同时要求 z=0 和 z≥1，所以两侧都不可行。

### 2.3 计数、编码与度

设 S=Σ_{d_j>3}(d_j−1)，则 `n′=n+S,m′=m+S,E′=E+2S`，因为旧正端只改标签，每位 helper 增加两条正端。S≤E，所以显式输出大小多项式；稠密编码也至多多项式膨胀。

每个 helper 至多增两个非零 x；旧 z 保留，新增 z 为 0。给定总有理证书位长 L，部分和分母可取相关分母乘积，其位长不超过它们位长之和 O(L)，分子也只有多项式位长；所有残量/部分和均在 [0,1]，共 O(S) 个。故证书转换为多项式位长和时间。这是给定有理证书的转换；任意实 M、λ 的可行性等价为数学陈述，若另声称构造其 LP 系数/分类的比特算法，查询 M、λ 本身应给可运算编码，例如二进制有理数。该说明不缩小已证的实数量词。

内部副本总正度≤3，端点≤2。若旧每物品 ∞ 度≤2，可把至多两个旧 ∞ owner 放两端；内部仅两个 helper ∞ 端，端点至多一个 helper 加一个旧 ∞，故新每物品 ∞ 度≤2。旧玩家 ∞ 度本来若≤2则保持，新增 helper 度二；一般情况下不能额外声称玩家 ∞ 度≤2。λ 重估可能把有限旧端变 big，所以原 ∞ 度界不自动等于所有查询的 big 度界。

## 3. CONFIG 接口的两项修正及安全存在性引理

### 3.1 CONFIG(M) 正向可行，但 R 不是点态不减

`p>M` 时 R(p)=M<p，∞ 同样降为 M，故旧稿“重估不减任何估值”必须删除。正确的逐配置论证：原配置若含某个 `p≥M/λ` 的端，重估后该端恰为 M，可只保留此 singleton；若不含这样的端，全部端值不变，仍达到 M。得到规范化配置，物品边际只下降。

令 z_i 为标准化后所有 small 配置的总质量，x 为其与 big singleton 的物品边际。big 质量=1−z_i，每个 small 配置值≥M，每个 small 物品边际≤small 总质量 z_i，故全部 (4)–(8) 成立。λ=1 时原 CONFIG(M) 与 capped CONFIG(M) 的有效性还双向相同；λ>1 不能取消重估层。

### 3.2 λ=1 cap 不能无条件给原值 CONFIG(M/2)

独立核了 4 玩家反例：3 件 shared 对每人值 3/4；每人一件仅自己有值的 private，值 7/16。在 M=1、λ=1 下均为 small。每人 shared 的 x 各 1/4、自己的 private x=1、z=1。每 shared 列和=1；每 private 列和=1；每行价值为 `3·(3/4)·(1/4)+7/16=1`，逐 small 上界成立。因此 cap M-LP(1) 可行。原 CONFIG(1/2) 的每份配置必须有 shared；4 位玩家需要至少4的 shared 总边际，却只有3件，故不可行。

更一般 n≥4，令 v=(n−1)/n、a=(2n−1)/n²，n−1 件 shared 值v，各有一件 private 值a。raw OPT=raw ConfigOPT=a，cap 可行集合精确为 `(0,a]∪(v,1]`：

- `M≤a`：private 是 big，取私有 singleton。
- `a<M≤v`：shared big、private small；由 `Mz≤a x_private≤a z` 得 z=0，n 行各需至少一 shared，n−1容量矛盾。特别 M=v 仍不可行。
- `v<M≤1`：全部 small，取 shared 各1/n、private1、z1；每行价值 `(n−1)v/n+a=1`。
- `M>1`：全部 small、各 z≥1，而全实例总可用加权价值≤`(n−1)v+na=n`，小值总要求≥Mn>n，矛盾。

因此最高 cap 参数为1，`1/a=n²/(2n−1)=Θ(n)`，n=4 已大于2。uniform 单位值的近2例只表明一个下界，不能被用作所有 cap 实例的二倍上界。

原 PDF 页7确实把 Theorem 2.3 无附加条件写为 M-LP→CONFIG(M/2)，且前文没有显式 λ≥2 下界。证明首步把值≥M/2的端重估为M，减少 z 并截 small x；该首步不能在本例的 λ1 模型中保持其所称可行性：shared 质量和3/4，z从1降至1/4，private x截为1/4，小值仅7/64<1/4，直接违反(6)。因此不能把原 statement 的文字当成本报告显式 λ1 域的可用定理。此处的准确反驳范围是所展开的方程/量词接口，不推断论文其他结果一并错误。

### 3.3 安全 small 引理的独立证明（存在性，不声明显式多项式分解）

固定一个已经规范化的估值矩阵：big 值 M，small 非负值≤p_max<M。给其 M-LP 可行解。先可把所有 z 压至≤1：若 z>1，则每个 x≤1 由列容量成立，故改 z=1 仍保 (5)–(7)。每行 big 质量若超过1−z，可只下减 big 坐标使总和恰为1−z，列容量只降。

对 z>0 的一行，令 small 的 u_j=x_j/z∈[0,1]，有 Σp_j u_j≥M。逐坐标下减到 u′≤u 且 Σp_j u′_j=M（例如统一缩放）。考虑紧多面体

\[
P=\{t\in[0,1]^m:\sum_jp_jt_j=M\}.
\]

任何顶点至多一个坐标严格在(0,1)：若有两个正系数分数坐标，可沿保持加权和的方向作正负微扰；若某零系数坐标分数，则可独自微扰。都会与极点矛盾。将 u′ 有限凸分解成顶点；对各顶点，丢掉其至多一个分数坐标，留下0/1配置。其价值至少 M−p_max，且逐坐标边际只下降。

把这些配置的凸组合乘 z；补上总质量1−z的 big singleton。得到每玩家总质量1、每配置值≥M−p_max、每物品边际≤原x，因此 CONFIG(规范化实例,M−p_max) 可行。z=0时只需big singleton；没有 small 正端而z>0则(6)已不可能，所以无遗漏。

若额外 `p_max≤M/2`，这才给规范化实例上的 CONFIG(M/2)。R_{M,λ} 且 λ≥2 自动使正 small 值<M/λ≤M/2。此时回到原实例，含规范化 big 的配置至少有原值 M/λ 的一端，不含 big 的配置值不变，安全得到原 CONFIG(M/λ)。更一般已付的直接安全量为 `min{M−p_max,M/λ}`。没有条件时不得把 M−p_max 换成 M/2。本报告只使用紧多面体有限凸分解的存在性；不借此冒称已有多项式显式证书分解算法。

## 4. finite H 的完整边界及精确算例

对同一副本图，将 helper 两正端改成有限 H>0。

当 M≤λH，helper 被规范化为 big，§2 的正向和反向公式逐字成立，故这段 M-LP 可行性等价。M=λH 属 big 端点，应包含。

反向事实上对所有 M>0 成立。若 M>λH，helper 两端均为 small，由(5)得 z_h≥1，由(6)得 `H(y_left+y_right)≥Mz_h≥M`，故该 helper 消耗总质量至少M/H>λ≥1。每条链 d−1 helper 仍消耗至少d−1，扣除 d 个副本容量后，原 owner 总质量≤1。旧行分类/系数仍不变，投影给原解。因此不能把 finite-H 反向误限到低区间。

上区间可能仍有新解，但需要 `(d−1)M/H≤d`，即 `M≤dH/(d−1)`。这与 integer/CONFIG 在 s>H 时每 helper 至少需要两件实际副本的计数障碍不同。

对 d=4,H=1,λ=1,M=4/3，令三个 helper z=1，两端依次 `(1,1/3),(2/3,2/3),(1/3,1)`。四列使用依次为 `1,1/3+2/3,2/3+1/3,1`，均为1；每行small值4/3，逐x≤z。四位旧 owner 各有私有100物品且共享旧物品值100，令旧玩家只取私有big、z=0。得到完整输出可行解。若 M>1，helpers无big、z≥1，总使用≥3M≤4，故最高cap值恰4/3。raw integer与CONFIG在1可行，在s>1需要三名helper各占两件副本，6>4，故二者均恰1。

原4人实例的raw OPT与ConfigOPT均100：各取private达100；阈值>100则每份配置必须含唯一shared，四行质量与一件容量矛盾。原cap值恰125：M≤100取private big；100<M≤125取private x1、shared x1/4、z1，每行值125≥M；M>125时全部small、各z≥1，所有列总价值≤5·100，给4M≤500，矛盾。旧cap值不是100。

作为全部λ边界的附加核算，此固定100/1输入的旧规范化M-LP最高参数为 `max{125,100λ}`，finite-helper输出为 `max{4/3,λ}`：各自分类断点分别为100λ与λ，低区间都可由big匹配实现，高区间由上述加权总容量界和证书给精确上界/下界。本附加算式不必另造节点。

## 5. I_T/J_T 的精确值和人数指数

取T≥4。T个block，各有root a_r与T位b_{r,k}；root对其T件u值1，b_k对自己的u值∞、对本block全部T件w值1；另T−1件B_r给相邻root值∞。

### 5.1 cap最高阈值T

在M=T,λ=1处，令各root和b的z=1/T；root每个u的x=1/T，b自己的big u的x=1−1/T、每个w的x=1/T。B_r左/右root的x为(T−r)/T、r/T。任一root的B总质量=(T−1)/T（端点同样成立）；任一b的big u质量同样=(T−1)/T；各行small价值为1=Tz，全部small x=z。所有u、w、B列容量恰1，故完整可行。每条w链均匀hole q=w=1/T，helper big两端x为(T−k)/T、k/T，z=0，给J_T同目标证书。

若M>T，root的T个单位端全small，(6)、(7)给 `Mz_a≤Σ_kx_{a,u_k}≤Tz_a`，故z_a=0。全部T位root各需B big质量≥1，总需求≥T，但B只有T−1件，矛盾。原与D∞后cap最高参数都恰T。

### 5.2 固定任意λ：精确max(T,λ)

若M≤λ，全部单位正端都big；每block可令root取u₁、b₁取w₁、其余b取自己的u，得到一对一正边匹配，故z0证书可行。M=λ属于本情况。

若M>λ，unit端全small，∞端全big；当M≤T，上述T目标的证书仍满足small值1≥M/T，其他约束不变。若M>T，则root的同一不等式强制z=0并引出B容量矛盾。合并正参数精确为 `(0,max{T,λ}]`，故两族最高参数为max{T,λ}。这里每个I_T/J_T都使用同一个固定λ比较；没有随n换λ。对固定常数λ、T≥λ时恰T；λ>T时的提高来自重估，不能改称原ConfigOPT提高。

### 5.3 raw CONFIG、整数和规模

原CONFIG(T)证书：root以1/T取全u，其余质量按上述B singleton分配；b以1−1/T取自己的u singleton，以1/T取全w。各行质量1、各列边际1。若s>T，全部root合法配置必须含B，T对T−1容量矛盾，故raw ConfigOPT=T。

整数上界：某root没有B，若其取s件u、最小值V，则s≥V；这s位失u的b只能从T件w得到各自V，故sV≤T，V²≤T。有限最小值为整数，得OPT≤floor√T。令q=floor√T；每个root取q件u，失u的q位b各取q件互不相交w（q²≤T），其余b取自己的∞u，达q，故整数OPT=q。D∞已证raw保持，所以J_T两值仍精确T和q。

只降T²件w，每件度T，S=T²(T−1)。故原n=T²+T，原m=2T²+T−1；新N=T³+T，新m=T³+T²+T−1。正端计数还可核为原E=T³+2T²+2T−2、新E′=3T³+2T−2。各概率分母T、各有限值1，证书与输入按T显式多项式，不是poly(log T)。T³≤N≤2T³、√T/2≤q≤√T，故T/q=Θ(√T)=Θ(N^(1/6))；不能沿用原n指数1/4。输出每物品总正度≤3，每物品及每玩家∞度≤2，但root总正度T+外部邻接数、b总正度T+1，不是玩家总度三。

## 6. uniform 单位例及 cap反族经D∞的交叉核验

n位玩家、2n−1件所有人值1物品，cap最高参数精确2−1/n。M≤1用匹配；M>1时全部small、各z≥1，总容量给nM≤2n−1；等号由所有x=1/n、z=1达到。原CONFIG最高参数1，因为s>1每配置至少两件，需至少2n总边际但只有2n−1。原整数值也1。本例正确，但它不证明普遍gap≤2。一般λ下其最高参数为max{λ,2−1/n}。

共享—private反族经D∞后，S=(n−1)²，新N=n²−n+1，m′=n²，E′=n²+2(n−1)²=3n²−4n+2。raw actual/CONFIG桥保留值a；新M-LP桥保留同λ1下精确集合 `(0,a]∪(v,1]`。因此新物品DegreeThree∩InfDegreeTwo中亦有最高cap/rawOPT比n²/(2n−1)=Θ(√N)，且非前缀。此输入有限值是a、v而非原{0,1,∞}简化族；不能与I_T/J_T的CONFIG本身gap混同。n=4给N13、m′16、E′34，与报告数值一致。此核验只补确认已有反族报告，不提出另一个主覆盖任务。

## 7. 最终审查处置

可以接受为已证明：D∞直接保持每个同M、同λ的规范化M-LP可行性；给定证书的显式多项式转换；finite H的低区间双向与全M反向；I_T/J_T的max(T,λ)及T≥λ时精确T；精确整数/CONFIG和新人数指数；两类明确反例。

初读85db…稿不可整体原样交付；修订08fb…稿已纠正上述§3.1与§3.2，并补齐finite-H全参数反向、same-M/same-λ、非前缀sup与J_T度界的指称。安全small切片引理足以给限定存在性接口，不需要为主桥完成原论文整篇审查，也不必冒称原算法已核通过。本审查的全部数学结论不以未完成的登记/发布操作作额外数学前提。


## 8. 修订 SHA 08fb… 的完整复核及最终 disposition

收到主worker冻结版本后，再次实算其 SHA 为 `08fbaf632f6b5172e0a31b34708837633ee39c2a9c37023a38a5cb1ebdd75a52`，全文实际读取而非仅比较摘要。核实如下：

1. §2 直接桥保留全部原约束证明，明确两侧同一个M与同一个λ，并显式说明按不同人数重新选择λ不能自动使用该桥；空正可行集最高值约定0，无前缀假设。
2. §3.1 已逐配置证明达M有效性，不再声称点态不减。
3. §3.2 已公开首步promotion在n4反例中的7/64<1/4失败，撤回一般λ1原值M/2接口；完整给small切片顶点分解，仅声明存在性。其版本不先压z≤1，而是把质量`z+Σ_big x≥1`的配置集合按行归一，边际只降；这是正确的替代办法，即使原z>1也成立。pmax<M保证所得阈值正；有限凸分解中的零系数坐标也不产生遗漏。
4. §3.3 完整保留精确cap反族四区间及端点M=a可行/M=v不可行；Θ(n)与D∞后的Θ(√N)使用不同人数基准。反族正式对象身份由父Boss给定为`M-b6605b3864cb41e399d926496739f12d`，无新增ID请求。
5. §4 finite-H反向覆盖所有M、正向M≤λH；旧125/新4/3均不变且正确。
6. §5 I_T/J_T精确max(T,λ)正确，物品总度三已明确只称降度后J_T，玩家总正度不作三界。§6–7的证据与工作流措辞不作为数学步骤。

**最终 disposition：修订08fb…版本中§2主桥及§3–5所述限定接口、反例和精确族全部通过此独立数学审查；没有遗留数学缺步。** 正式化可把staging审查路径换为已发布的同数学内容证据路径，并删除工作流待登记文字；这些文字迁移不需要重新证明，也不允许重新引入已撤回的无条件M/2接口。本报告是辅助审读，既不替代主任务覆盖收据，也不建立第二个主覆盖任务。

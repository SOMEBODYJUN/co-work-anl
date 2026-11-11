# 根近饱和取等障碍、真实第五源加强及最优面审计

Boss1；RUN `six-boss1-20261111`；独立审计席 `early_shared_x_source_audit`。
写入仅限本页及 `root_near_equality_audit/`；两个此前已冻结的审计包均未改动。

## 1. 结论

**全部通过。** 在原六人完整有序历史纯 SPE 模型中，令 u 为实际第一位收益，K 为全目录最大覆盖大小，\(\mathcal O\) 为任意六个合法标签的覆盖并，\(O=|\mathcal O|\)。

第一，旧根近饱和预算

\[
H=150u-\frac{139}{6}K-O\ge0
\]

取等且 O>0 时，必有

\[
\boxed{K\ge\frac{23}{63}O.}
\tag{EQ}
\]

第二，Main 的定量加强成立于全部原模型实例：

\[
\boxed{N_{\rm root}:=10980u-1658K-87O\ge0.}
\tag{NEW}
\]

关键的逐客户控制 \(\delta+(12/5)\tau\ge0\) 已给解析分型证明，并独立核对全部 128 个有序布尔型。包括最初需要检查的 \(p=0,y_5=0,n>0\) 情形：该处 \(\delta\) 确实可以为负，但合并后的余项严格为正。

第三，两个新的全 257 列有符号恒等式以及更新对偶均独立重放通过。整个旧 217 行系统的归一化最优面被 (NEW) 排除，不只排除一个原始点。更新对偶给出原模型的另一个有效普遍下界

\[
\boxed{
W\ge
\frac{366720231019228542915}{860670652474859546101}\,operatorname{OPT}_6
}
\tag{LB}
\]

其系数约为 \(0.42608659882235334\)，严格大于旧证书的系数。本页不宣称这是新增约束后的精确最优值、SPE 锐界或最佳已知下界；没有匹配原始点，也没有调用优化器。

## 2. 原模型与唯一真实根分支

采用 [共同目录完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)。目录有限非空且所有玩家共同使用，客户单位权重，完整策略在全部有序历史上为纯 SPE；空覆盖、标签别名、重复行动和弱平局均允许。

取一个真正达到 K 的合法标签 C。只在根强制 C，之后沿同一份原策略的真实后继完成：

\[
(C,B_2,B_3,B_4,B_5,Z).
\]

记该分支根、第五、末位收益为 v、s、w。对每客户设

\[
p=1_C,\quad y_j=1_{B_j}\ (2\le j\le5),\quad z=1_Z,\quad
n=y_2+y_3+y_4+y_5,\quad c=p+n+z.
\]

三份真实收益分别为 \(p/c,y_5/c,z/c\) 的客户求和。c=0 时三个零分子份额均定义为零。

六个合法查询为 \(Q_1,\ldots,Q_6\)，其覆盖并位为 o、真实重数为 \(d=\sum_k1_{Q_k}\)。所以 \(d\ge o\)，\(d\in\{0,\ldots,6\}\)。令 \(\theta=o/6\)。本证明不用 \(\mathcal O\) 作为目录行动，也不删除并外客户。

本分支上的非负预算是

\[
I=u-v\ge0,\qquad D_j=K-|B_j|\ge0\quad(2\le j\le5),\qquad D_Z=K-|Z|\ge0.
\]

在真实末节点的六条合法查询 IC 取平均，再用 d≥o，给

\[
B=w-\sum_c\frac{o_c}{6(1+p_c+n_c)}\ge0.
\tag{B}
\]

新增的真实第五源位于**有序历史** \((C,B_2,B_3,B_4)\)。第五位真改一个合法查询 Q 后，必须沿该偏离自己的真实末回复继续；每名 Q 客户的总负载至多为 \(p+y_2+y_3+y_4+2\)。所以六条 SAFE 平均再减弱到并集，给

\[
G=s-\sum_c\frac{o_c}{6(p_c+n_c-y_{5c}+2)}\ge0.
\tag{G}
\]

根 C 即使不是原策略的最优根动作，这些后继节点仍受完整 SPE 量词约束。(G) 没有冻结本分支的末标签 Z。

## 3. 原转移余项的完整分型

从原 [根主题刚性 owner](../../../archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md) 的逐客户转移式，在 m=6 定义

\[
\begin{aligned}
\tau(p,n,z;\theta)
={}&\frac{n-4p}{2}+(z-p)+24\left(\frac pc-\frac p6\right)\\
&-\left[\frac\theta{1+5p}-\frac\theta{1+p+n}+\frac{z-p}{c}\right].
\end{aligned}
\tag{T}
\]

这里的 \((z-p)/c\) 是两份零分子约定后的份额差。直接整理给四个精确表达式：

| p | z | \(\tau(p,n,z;\theta)\) |
|---:|---:|---|
| 0 | 0 | \(n/2-\theta n/(n+1)\) |
| 0 | 1 | \(n/2+(1-\theta)n/(n+1)\) |
| 1 | 0 | \((4-n)(9-n)/[2(n+1)]+\theta(4-n)/[6(n+2)]\) |
| 1 | 1 | \((4-n)(6-n)/[2(n+2)]+\theta(4-n)/[6(n+2)]\) |

对整数 \(0\le n\le4\)、\(0\le\theta\le1\) 均非负。p=0,z=0 的最小值出现在 \(\theta=1\)，为 \(n(n-1)/[2(n+1)]\)；其余三行的各项已经非负。这保留了 p=0 的边界，也明确保留 p=1 时正查询分子增加的余项，没有把它丢掉后误判等号。

当 \(\theta=o/6\in\{0,1/6\}\) 时，四行进一步给出

\[
\boxed{\tau=0\quad\Longleftrightarrow\quad n=4p.}
\tag{T0}
\]

对 p=0,n≥1，有更定量的统一界

\[
\tau\ge\frac{5n}{12}.
\tag{T+}
\]

注意真实六查询平均 \(\theta=d/6\) 允许 \(\theta=1\)，那时 p=0,n=1,z=0 也可能使 \(\tau=0\)。取等证明必须先处理 d−o 的正松弛，不能直接对任意六查询平均套用 (T0)。

## 4. H 的两种精确非负分解

先使用真实重数 \(d\)。令

\[
B_d=w-\sum_c\frac{d_c}{6(1+p_c+n_c)}\ge0.
\]

把转移式按真实六查询平均，再对客户求和，可得

\[
\begin{aligned}
H={}&150I+3\sum_{j=2}^{5}D_j+6D_Z+6B_d
+6\sum_c\tau(p_c,n_c,z_c;d_c/6)\\
&+\sum_c(d_c-o_c)\left(1-\frac56p_c\right)
+\frac56|C\setminus\mathcal O|.
\end{aligned}
\tag{HD}
\]

每一项非负，其中菜单重数差的系数是 1 或 1/6，始终严格为正。

使用已经减弱的 \(\theta=o/6\) 时，同一代数又给更方便的分解

\[
\boxed{
H=150I+3\sum_{j=2}^{5}D_j+6D_Z+6B
+6\sum_c\tau(p_c,n_c,z_c;o_c/6)
+\frac56|C\setminus\mathcal O|.
}
\tag{HU}
\]

两式完全一致：B 包含真实平均 BR 与正重数差，\(\tau\) 对查询分子仿射。它们都只是同一真实根 C 分支上的恒等式，不引入额外假设。

与 [旧最大主题根近饱和 owner](../../../archives/customer-attraction/state/推论/最大主题根近饱和的覆盖阈值--推论.md) 对照，K 必须是 C 的真实大小及全目录大小上界；不能把某个可见标签的大小或加权最大 X 的大小代入替代 K。

## 5. H=0 的覆盖结构和 23/63 门槛

假设 H=0、O>0。由 (HD) 的每份非负松弛分别为零，得到：

- \(I=0\)，故 u=v。
- \(|B_2|=\cdots=|B_5|=|Z|=K\)。
- \(C\subseteq\mathcal O\)。
- 每个客户 d=o，即六查询的覆盖两两不交。空覆盖重复标签仍可存在。
- \(B_d=0\)，真实末位平均查询 IC 取等。
- 每个实际客户的转移余项为零。

现在 \(\theta=d/6=o/6\)，所以 (T0) 可合法应用，强制 n=4p。于是四个中间标签均与 C **覆盖相同**：

\[
\operatorname{cov}(B_2)=\operatorname{cov}(B_3)
=\operatorname{cov}(B_4)=\operatorname{cov}(B_5)=\operatorname{cov}(C).
\]

这不强制它们的标签身份相同。真实第五源依然是原有序历史 \((C,B_2,B_3,B_4)\)，不能未经证明改成另一个字面历史 \((C,C,C,C)\) 并沿它选择续局。

令 \(J=|C\cap Z|\)。由于前五个行动都覆盖 C、末标签大小为 K，实际分支收益为

\[
u=v=\frac{K-J}{5}+\frac J6
=\frac K5-\frac J{30},\qquad
w=K-\frac56J.
\]

末位前的五个覆盖均为 C；利用 d=o、\(C\subseteq\mathcal O\) 和平均 BR 取等，

\[
w=\frac{O-K}{6}+\frac K{36}
=\frac O6-\frac{5K}{36}.
\]

因此

\[
J=\frac{41K-6O}{30},\qquad
u=\frac{139K+6O}{900}.
\tag{UV}
\]

在真实第五源，前四个覆盖均为 C，而且第五位与根在最终分支上覆盖相同，故 s=v=u。将 (G) 在这个结构上展开，得到

\[
u\ge\frac{O-K}{12}+\frac K{36}
=\frac{3O-2K}{36}.
\]

与 (UV) 比较即得

\[
\frac{139K+6O}{900}-\frac{3O-2K}{36}
=\frac{63K-23O}{300}\ge0,
\]

证明 (EQ)。这一步使用第五位偏离后的真实末回复所给的 SAFE，而不是假定它可以得到冻结 Z 后的静态收益。

## 6. 定量余项：包含原先可疑的负 δ 类型

令

\[
T=u-\frac O{12}+\frac K{18},\qquad
\delta=\frac{p-y_5}{c}+\frac{o}{6(p+n-y_5+2)}-\frac o{12}+\frac p{18}.
\]

从真实根和第五位的均分份额逐项相消，有

\[
T=I+G+\sum_c\delta_c.
\tag{TG}
\]

需要控制的是 \(\rho=\delta+(12/5)\tau\)，其中 \(\tau\) 使用 \(\theta=o/6\)。以下分类覆盖全部 128 个 \((p,y_2,y_3,y_4,y_5,z,o)\) 有序布尔型。

### p=1

若 y5=0，则 n≤3。o=0 时 \(\delta=1/c+1/18>0\)；o=1 时

\[
\delta=\frac1c+\frac1{6(n+3)}-\frac1{36}\ge\frac1c>0.
\]

若 y5=1，则 1≤n≤4，且

\[
\delta=\frac1{18}-\frac{on}{12(n+2)}
\ge\frac{4-n}{36(n+2)}\ge0.
\]

两种情形都由 \(\tau\ge0\) 得 \(\rho\ge0\)。

### p=0、y5=0

此时精确地

\[
\delta=-\frac{on}{12(n+2)}.
\]

所以 o=1,n>0 时 δ 的确为负，不能忽略。n=0 时 \(\delta=\tau=0\)。n≥1 时由 (T+)：

\[
\rho\ge -\frac{n}{12(n+2)}+n>0.
\]

因此这一类型不否定所需的定量控制。

### p=0、y5=1

此时 n≥1，且

\[
\delta=-\frac1{n+z}-\frac{o(n-1)}{12(n+1)}
\ge-\frac1n-\frac{n-1}{12(n+1)}.
\]

再用 (T+) 得

\[
\rho\ge n-\frac1n-\frac{n-1}{12(n+1)}
=(n-1)\left[\frac{n+1}{n}-\frac1{12(n+1)}\right]\ge0.
\]

故 \(\rho\ge0\) 在完整域成立。类型

\[
(p,y_2,y_3,y_4,y_5,z,o)=(0,0,0,0,1,0,1)
\]

满足 \(\delta=-1,\tau=5/12\)，所以任何对全部这些布尔型成立的单余项控制 \(\delta+\lambda\tau\ge0\) 必须有 \(\lambda\ge12/5\)。这只认证该指定逐点比较的系数，不认证整个预算锥或 SPE 锐性。

## 7. 定量加强的完整付款及与旧界比较

将 (TG) 与 \((2/5)\times(HU)\) 相加，精确得到

\[
\begin{aligned}
T+\frac25H
={}&61I+G+\frac65\sum_{j=2}^5D_j+\frac{12}{5}D_Z
+\frac{12}{5}B\\
&+\frac13|C\setminus\mathcal O|+\sum_c\rho_c\ge0.
\end{aligned}
\tag{PAY}
\]

全部钱包属于同一真实根 C 分支或同一个全目录大小界。乘以 180 后恰为 (NEW)，没有额外未知标签或跨分支收益。

新旧 u 下界之差为

\[
\frac{1658K+87O}{10980}-\frac{139K+6O}{900}
=\frac{23O-63K}{18300}.
\]

所以新界在 \(K<23O/63\) 时严格较强，取等门槛与第 5 节一致。整个证明无须除以 O 或 K，零客户、全空目录和空查询菜单均合法。相同覆盖标签不被合并，所有查询始终使用原有序历史下的真实后继。

## 8. 当前精确点的排除

只从已认证的 `universal_union_wallet_lp/exact_certificate.json` 抽取 u、K、O，没有重算旧 LP 或重放旧点的全部约束。其 SHA 为
`ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85`。

\[
u=\frac{4717495469031803264}{142891298915142483961},\qquad
K=\frac{24376964954228547006}{142891298915142483961},\qquad O=1.
\]

精确计算为

\[
H=0,\qquad
\frac{23}{63}-K
=\frac{1750751082931878669725}{9002151831653976489543}>0.
\]

若该点可来自完整 SPE，第 5 节的真实第五源必需收入超过现有 u 的量为

\[
\frac{3O-2K}{36}-u
=\frac{70030043317275146789}{1714695586981709807532}>0.
\]

新整数行在该点的准确值是

\[
\boxed{
N_{\rm root}=
-\frac{1050450649759127201835}{142891298915142483961}<0.
}
\tag{PNEG}
\]

这已排除该点的完整 SPE 实现。下一节的独立恒等式审计将排除范围进一步扩至整个旧最优面。

## 9. 整个旧最优面的全列排除

旧普遍钱包证书已在 [universal_union_wallet_audit.md](universal_union_wallet_audit.md) 冻结审计。它在全部 257 个坐标上给

\[
W=\alpha_0 O+\sum_{R\in\mathcal R}\lambda_RR+\sum_jr_jz_j,
\quad
\alpha_0=\frac{243427385229576983115}{571565195660569935844},
\tag{OLD}
\]

其中 \(\mathcal R\) 是 13 个正权预算，全部 \(\lambda_R>0\)，239 个客户列 \(r_j>0\)，另 17 个客户列及 K 列余项为零。这里 z 的最后一坐标代表 K。

对旧系统任意归一化最优点，O=1 且 W=\(\alpha_0\)。因为 (OLD) 的所有 slack 非负，其 13 个预算必须全部取等，239 个正余项坐标必须全部为零。

Main 新提供两个有符号全列恒等式。本审计从原份额重新构造这 13 个预算的全部 \(13\times257=3341\) 个系数，逐一核对：

\[
K=k_0O+\sum_R\beta_R^{K}R+\sum_je_j^{K}z_j,
\qquad k_0=\frac{24376964954228547006}{142891298915142483961},
\tag{FK}
\]

\[
N_{\rm root}=c_0O+\sum_R\beta_RR+\sum_je_jz_j,
\qquad c_0=-\frac{1050450649759127201835}{142891298915142483961}.
\tag{FN}
\]

两个 e 向量均只支撑于上述 239 个旧正余项列；它们在另外 18 列上严格为零。\(\beta\)、e 可以有符号，因为这一步只在已证取等的最优面上消项，并未把有符号组合冒充普遍非负预算。

于是旧最优面每一点都满足 \(K=k_0\)、\(N_{\rm root}=c_0<0\)。这证明 **整个旧最优面** 都不满足新普遍必要行，不依赖代表点的选择，也不依赖最优面的维数计算。两份恒等式的全部系数与审计来源记录在 [face_audit_result.json](root_near_equality_audit/face_audit_result.json)。

## 10. 更新对偶的符号与新普遍下界

取

\[
\gamma=\frac{89213252833200687}{3442682609899438184404}>0.
\]

由 (OLD) 减去 \(\gamma\) 倍 (FN) 再将新预算移回右侧，得到全变量恒等式

\[
W=\alpha_1O+\sum_R\lambda'_RR+\gamma N_{\rm root}+\sum_jr'_jz_j,
\tag{NEWDUAL}
\]

其中

\[
\lambda'_R=\lambda_R-\gamma\beta_R,\quad
r'_j=r_j-\gamma e_j,\quad
\alpha_1=\alpha_0-\gamma c_0
=\frac{366720231019228542915}{860670652474859546101}.
\]

本审计独立逐项确认所有 \(\lambda'_R\ge0\)、所有 \(r'_j\ge0\)，全部 257 列的 (NEWDUAL) 精确相等。旧 ROOT_NEAR 权恰变为零；其余 12 个旧预算和新根行的权均为正。列余项仍是 239 个正、18 个零。

因此 (NEWDUAL) 是一个普遍有效的非负证书，而不仅是最优面上的有符号关系。取六查询为一个真正最优菜单，即得到 (LB)。严格增量是

\[
\alpha_1-\alpha_0
=\frac{93714119405760957396261886509309660645}
{491929389881103486752961144885848530344244}>0.
\]

这里没有求解新增约束后的 LP，没有新的匹配原始点，故不声明 \(\alpha_1\) 的最优性。已有 \(\alpha_0\) 下界依然有效；被排除的是旧必要系统达到该下界的全部抽象点。

## 11. 独立核验、精确范围与冻结

[check_exact.py](root_near_equality_audit/check_exact.py) 只用标准库 Fraction，不导入或运行 Main 的脚本，也不调用优化器。它有两个明确检查入口：

- 默认入口：128 个完整有序布尔型的 \(\tau,\delta,\rho\)，140 个真实六查询重数类型，以及 1304 个正式仿射恒等式。\(\rho\) 共 7 个零、121 个正，最小正值为 1/18；\(\max(-\delta/\tau)=12/5\) 的唯一极值型已保存。
- `--face` 入口：独立重建 13 个旧预算共 3341 系数；核对旧对偶的零列支持，(FK)、(FN) 各 257 列，以及更新对偶的全部 257 列与全部乘子符号。

结果分别为 `PASS_ROOT_NEAR_EQUALITY_AND_QUANTITATIVE_FIFTH_SOURCE_AUDIT` 和 `PASS_WHOLE_OLD_OPTIMAL_FACE_AND_CONSTRUCTIVE_NEW_UNIVERSAL_DUAL`。完整分数、全部 128 余项、点排除量、两份有符号恒等式和新对偶的所有列余项存于 [audit_result.json](root_near_equality_audit/audit_result.json) 与 [face_audit_result.json](root_near_equality_audit/face_audit_result.json)。

本页同时核对了 Main 的 [根近饱和加强证明](main_root_near_strengthening.md) 与 `main_universal_wallet_face.json`，没有发现需修正的数学来源或精确符号。所有本轮来源 SHA 和最终工件 SHA 记录在 [freeze_manifest.json](root_near_equality_audit/freeze_manifest.json)。旧 `universal_union_wallet_audit/` 及 `early_shared_x_source_audit/` 均未修改。

本明确义务完成并冻结；没有重新优化、扩展任意预算锥或声称一般 half 已闭合。

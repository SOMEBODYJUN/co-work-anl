# 分叉双人侧资源强迫割均衡：独立重构与边界攻击

## 审查对象、冻结版本与结论

审查 Claim：`WC-DIRECTED-FANOUT-FORCING-CUT-v1`，中文名称“分叉双人侧资源反馈在统一轻玩家强迫下的割均衡”。本审查只覆盖该 Claim 的精确私有双人侧资源拓扑及逐 light 的弱统一强迫假设 (UF)。没有审定 WC-TARGET 的全类匹配上界，也没有外部同行评审或全球新颖性认证。

审查者在收到作者正文之前，先从两类玩家的真实资源策略独立重构：侧资源正部容量、每源共享主资源预算、有限二染色割，以及自环处理。此阶段只读 MODEL 与既有奇环包络材料；没有先读本次作者证明，也没有参与其程序实现。随后读取并逐式攻击冻结稿，而非以赞同票替代推导。

冻结对象：

- 初始候选正文 SHA256：`e3d74b38a280c65339804ae12ab762517e6263d2dac4dd44951eca9b7f45cd66`。
- 规范正文 `research/current/weighted_congestion/directed_fanout_forcing_cut.md` 的审查 SHA256：`99d9de56cc1d99ff1fed7882332660fa51f04a24b5cbce481ce4218887b7052e`。
- 两版的“第一节：所需标量不等式”至“第四节：真实偏离成本”逐字节相同。规范版补充 Claim 元字段、状态、规范路径与二次、三次样本的参数前提，未改变量词、假设或数学结论。

**结论：所述范围内证明闭合，未发现仍成立的 fatal objection。** 下文给出独立重构和针对性攻击。非对称动作副本、多人共用同一侧资源、多主源 light、(UF) 失败的真实游戏均不在结论中；这些限制不能被删除后继续沿用本 Claim。

## 一、先验重构的核心义务

记 source 为 $o(\ell)$，target 为 $t(j)$，light 权为 $w_\ell$。先把所有 light 固定成与 source hub 反位。Hub $v$ 的主资源当前负载为 $u_v$，偏离后为 $u_v+W_v$，故其主资源成本差恰为

\[
-M_v=F_v(u_v)-\alpha F_v(u_v+W_v).
\]

侧索引 $j$ 的真实成本差，当 source 与 target hubs 同位时为

\[
Q_j=G_j(u_t+w_\ell)-\alpha G_j(u_t),
\]

异位时为

\[
-P'_j=G_j(u_t)-\alpha G_j(u_t+w_\ell).
\]

这些差可能有不同符号。不能直接把 $Q_j$ 当作非负割权。独立重构使用

\[
\lambda_j=u_t\max\{Q_j,0\}.
\]

所需瓶颈因而分成三项：

1. 标量包络须给 $\lambda_j\le w_\ell P_j$，其中 $P_j=\alpha G_j(u_t+w_\ell)-G_j(w_\ell)$。
2. 每个 source 的全部侧资源须共用预算 $\sum_{j:o(\ell(j))=v}\lambda_j\le u_vM_v$，不能对同一 light 的每个出侧重复领取完整主资源预算。
3. 须找到一种 hub 二染色，使入侧的带符号容量不超过该 source 的出预算；自环在单方翻位时不是普通割边。

上述瓶颈均由正文给出的同一标量包络、按 light 权重求和及非负加权割解决；与先验重构一致。

## 二、标量包络与参数端点

对 $0<R\le1$，二项式系数逐项至少为一，故 $(1+R)^k\ge\sum_{r=0}^kR^r$。将其代回 $f_k$ 的正分母，得到 $f_k(R)\le1$。这涵盖 $k=0$、$R=1$ 的等号。对 $R>1$，通分后的分子确为

\[
R(R-1)\left[(1+R)^k\sum_{r=0}^kR^r-R^k\right]\ge0.
\]

所以所有 $0\le k\le d$ 都受 $T_d$ 控制，常数项没有被忽略。两条标量不等式 (S)、(M) 分别使用 $R=u/w$、$R=W/u$，方向均正确；非负线性相加允许多项式各项的实际费用差为负，无需先对各项差假设正号。

无需外部定理即可确认 $T_d$ 有限并且 $T_d>1$：$f_2(R)>1$ 对 $R>1$ 成立；而 $f_d(R)\le d$ 可直接比较多项式

\[
d[(1+R)^d+R^{d+1}]-[R(1+R)^d+1].
\]

其常数项与最高次项系数均为 $d-1\ge0$，对 $1\le j\le d$ 的系数为

\[
d\binom dj-\binom d{j-1}
=\binom dj\frac{(d+1)(d-j)}{d-j+1}\ge0.
\]

因此规范程序使用的 $\alpha=d$ 确满足包络前提。二次样本使用 $\alpha=6/5$ 时，独立重算给

\[
6\operatorname{den}(f_2)-5\operatorname{num}(f_2)
=R^3-4R^2+7R+1
=R(R-2)^2+3R+1>0.
\]

规范正文新增的 $x=R-1$ 表示

\[
x(x-\tfrac12)^2+\tfrac74x+5
\]

与同一多项式完全相等，对 $x>0$ 为正。故 $T_2\le6/5$ 的样本前提成立，不依赖浮点优化。三次样本的补充式也独立展开为 $3\operatorname{den}(f_3)-\operatorname{num}(f_3)=2R^4+6R^2+8R+2>0$，与一般的系数证明一致。

关键端点 $\alpha=T_d$ 全程只需弱不等式；不需 $T_d$ 的极大点取得或某个严格包络间隙。费用商从未出现，故零费用不会造成 $0/0$。

## 三、共享主资源、负差与权预算攻击

因费用非负单调、$\alpha\ge1$，有 $P_j,P'_j\ge0$。由 (S) 得 $u_tQ_j\le w_\ell P_j$，右端非负，故取正部后仍成立。这是 (B1)；取正部并非额外假设。又

\[
P'_j-Q_j=(\alpha-1)[G_j(u_t+w_\ell)+G_j(u_t)]\ge0,
\]

结合 $P'_j\ge0$，得 (B2)。因此同位侧的真实差乘 hub 权不超过 $+\lambda_j$，异位侧的真实差不超过 $-\lambda_j$，无论 $Q_j$ 正负皆成立。

(UF) 改写之后必须先把每名 light 的全部 $P_j$ 求和，再乘该 light 的 $w_\ell$。随后同 source 求和，用

\[
\sum_{\ell:o(\ell)=v}w_\ell F_v(u_v+w_\ell)
\le W_vF_v(u_v+W_v)
\]

才能使用 (M)。正文确实如此，未把共享主资源重复记账；不同 light 异权、不同侧费用、任意出度和重复端点均未改变此式。

若 $W_v=0$，所有相应 light 和出侧索引不存在，左侧为空和；(M) 退化为 $0\le u_v(\alpha-1)F_v(u_v)$。零主费用、零侧费用和非零常数项同样受非负展开覆盖，无需把它们删除。

## 四、有向边、自环与真实偏离攻击

割目标对方向不敏感，但有向记账保留 source 和 target。对任意 hub，单点翻位局部最小性先给

\[
I^{\rm nonloop}_v\le-O^{\rm nonloop}_v
\le\sum_{j:\text{非自环出}v}\lambda_j,
\]

其中 $I,O$ 是按同位取正、异位取负的容量和。自环的割能量是常数，不得把它计入单点翻位差。将其容量和同时加到上述最后一项两边，恰好得到正文的 (CUT)。每个自环在入和与出和中各记一次，没有额外因子；同端点的多条资源索引逐条相加，双向边也无重复计数错误。

自环的真实 hub 偏离须单独核对：light 动作在 hub 单方偏离时固定，因此当前侧负载为 $u_v+w_\ell$，翻位后为 $u_v$，虽然两端的图顶点是同一 hub。故正文把自环计入同位 $Q_j$ 项正确；不能在这里让 light 随 hub 同时换位。

全反位状态的 light 主资源当前负载恰为 $W_v$，翻位后恰为 $u_v+w_\ell$；其他 light 不随其改变。侧资源只可能有 light 自身和其唯一 target hub，当前费用逐项至多 $G_j(u_t+w_\ell)$，偏离费用逐项至少 $G_j(w_\ell)$。由 (UF) 得更强的 $\alpha C_\ell(s)\le C_\ell(\text{偏离})$，于是所需弱 $\alpha$-PNE 条件成立。

Hub 当前 main 无任何 light；翻位后进入所有本 source light，故 $-M_v$ 精确。把上述侧差、(CUT)、(B3) 顺次代回，得到 $u_vD_v\le0$。$u_v>0$ 允许除去 hub 权；每人仅有另一个二进制动作，保留原动作由 $\alpha\ge1$ 自动满足。一般实权、实系数只使用有限和与精确不等式，证明不依赖有理化或有限搜索。

## 五、实现审计与证据层次

审查先完成上述独立重构，随后才阅读作者程序，故代码审计属于 informed code audit。临时代码 SHA256 为 `b5a58703a583f5a54ea3f6405f60034e16c7b0ec375d74040b7e4432dd70fe40`，其实际资源构造逐玩家重算负载，逐人单方翻位，且把推导中的精确 hub 差与资源定义得到的差直接比较。该检查未复用推导差作为真实费用来源。

规范配套入口为：

- `tests/audits/weighted_congestion/verify_directed_fanout_forcing_cut.py`；
- `evidence/runs/weighted_congestion/directed_fanout_forcing_cut_audit.json`。

规范代码审查 SHA256：`29d34284468c28fc728036040e43cb77dacffcd9d542431f79eada6c42abfbd9`；冻结 JSON SHA256：`0cd5da3ffd0b160f4f0b2c7478147b1073efdca9de720244b89728f3a4cc9f43`。审查者运行：

```bash
python3 tests/audits/weighted_congestion/verify_directed_fanout_forcing_cut.py --output /workspace/scratch/08522dd1290d/directed_fanout_final_review_audit.json
```

重新运行的 JSON 与规范冻结 JSON 逐结构一致。十九组实际资源样本共枚举三千五百三十二个全部纯状态，核查了每个单点局部最小割对应的 PNE，覆盖正负侧差、自环、空 light 集、常数费用、零费用、非零费用弱 (UF) 等号，以及二次与三次非负混合费用。输入权重、系数、拓扑、seed 和生成方式均保存于冻结输出，精确计算使用 `fractions.Fraction`。

规范程序还保存了独立的 (CUT) 组合枚举：全部三顶点有向图（含自环），九个有序端点对的容量分别取零、一、二，共一万九千六百八十三图；五万四千四百八十六个单点局部最小割均通过 (CUT)。该整数程序不引用资源费用，补足了正文“任意局部最小点”与实际资源样本的实现对应。临时的额外标量数值只用于寻找反驳，未另列为长期证据。所有有限枚举只核验公式和实现；一般实参数结论由前四节的证明承担。

## 六、状态与尚未解决的问题

Proof completion：上述精确范围闭合。Independent internal review：先重构再攻击，未发现 fatal objection。External review：未记录。Implementation：配套精确资源枚举核验，最终代码版本见其证据合同。Novelty：不作外部优先权判断。

本 Claim 说明：统一强迫预算下，增加同一 light 的私有双人侧资源出度，并不能越过奇环包络产生全状态非存在；全部出侧共同消耗同一主资源预算。它不说明任意真实非存在实例都满足 (UF)，不说明整个拓扑的存在门槛等于 $T_d$，也不处理全类 O(d/ln d) 上界。最关键未解义务仍是去掉该强迫前提或改变承重拓扑后，能否给出全类证明或严格反例族。

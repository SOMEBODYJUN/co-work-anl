# Wave17：private 分组不变性的独立 3D 数学审查

审查身份：Boss2；只读 clone：`/workspace/scratch/e8cf4ce833a5/co-work-anl-boss2`。本稿是 Root 指定的独立 3D 数学复核与定向表身份比较，不是 3A/3B 任务认领、primary 覆盖收据或已发布超边。父任务所称“尚未认领 primary”的状态在本轮没有查询队列；本轮工作不改变它。

## 结论与准确作用范围

候选一般桥成立。固定玩家数、完整标签集及 big/private 身份后，只改变 private 标签所属等质量独立块的 partition，**全部完整有序历史上的纯 SPE 策略函数集合完全相同**。这里保留每个原标签、每个离轨历史，以及在同覆盖标签间任意依赖历史的平局选择，不进行标签商化，也不只比较可实现终局集合。

每份共同 SPE 的根标签路径相同，根福利也相同：无 private 时为 \(mq\)，出现一次 private 时为 \((m+1)q\)。当 \(q>0\)、\(m\ge2\) 时根路径至多出现一次 private。若 private 分组数为 \(g\)，静态最优覆盖为

\[
\operatorname{OPT}_m=mq+q\min\{m-1,g\}.
\]

这准确解释四端点所用 G8/G7 客户表：它们有相同的 SPE 函数集合，但最优覆盖分别为 8 和 7。原保存表经只读结构比较还显示：`results[0]` 与 `results[1]` 是同一张表，`results[2]` 与 `results[3]` 是另一张表；四张表并非全相同。两张不同表仅在历史 `(1,2,3)` 的规定动作不同，分别为 4 和 3。

一般桥不包含保存策略的原逐历史 IC 证书认证，也不包含两个 7/5 固定锥的 14 非零对偶认证。本轮没有重新执行这些认证，没有重跑 SPE 搜索或 LP。它也不适用于把某个原 private 标签改成 big 的 G10/G9 变换。

## 实读入口、合同与字节绑定

本轮实读了 clone 根 `AGENTS.md`、`prompts/03-map-worker.md`，以及 `research/IMPLEMENTATION.md` 第三阶段与定向替代规则。遵循“精确端点、整条结论与局部贡献分开、不为连通造边”的要求。本轮没有运行 Git、`work.py`、native、队列、edge/receipt/global/source 写入；唯一新文件是 clone 外本稿。

按指定接口执行 `tools/research_runtime.py` 的 `load(root, verify=False)`，定向取出下列两份完整对象合同，未进行全库数学检索。对合同列出的 body/evidence 另调用 `ref_bytes` 校验现存字节 SHA；这项字节核对不冒称读懂或重新验证每份附件的所有数学。

| 对象 | 版本与 registration pin | 本轮所用合同范围 |
|---|---|---|
| `M-c38f48fb4739493382960e39269f6cde` | v1；`d97957549cdf679439ed37603ddbd0399929331c9248ee910b23d840e6c902f0` | 两个根计数各两份完整 2801 节点策略；G8/G7 客户点；W5、OPT8/7；另有原 7/5 对偶证据 |
| `M-26829807ff6941a0b613be909e155889` | v1；`15b8cf3c7be4a054dc21e9b83733bddefd2322c424bf8a312b8e5282f3e20069` | 原保存 330 计数状态策略展开到 2801 有序历史；big 标签为 0/1/3/4，private 为 2/5/6；W5、OPT8 |

实读数学正文与定义如下，路径均相对于只读 clone：

| 路径 | SHA256 |
|---|---|
| `archives/customer-attraction/state/计算/R-3b942共享遗漏循环完整锥攻击--计算.md` | `c130c9c079de3c47c8a8139662d7109ad70de3daa3a8d1ff2d6f5078a033f964` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/state/计算/首人弱覆盖门槛的固定策略探针与计数游走--计算.md` | `5ce7e14fd38088dfbcafe9d5d058b04f554d17d15079acd5ba32cb278ee53aa0` |

四端点主冻结附件为

`research/registration/evidence/register-lead-recovered-evidence-01/shared_cycle_cone_attack.json.gz`

原压缩字节 35543B，SHA256：`dda4102d0991074c232d1f0da80fac75fa1fd7af2eb570eea7c64fb9a48b3de8`。

其余合同绑定也核对一致：`audit_finite_cag.py` 为 `0a92ab7f0f3a6b3005e502a7ac0ecb0e563b27155a36dd97e4356188096350ef`；`audit_finite_cag.json` 为 `9bcff83a958a76d162bf3b63727250aad992fdaa04f8583531cd94dd34d86031`；M-268 的 `frozen-first-floor-exact-audit.json` 为 `716d2b9f2114f8533ec77268f1f11605b4af72b9afec7349d848826df3426dd0`。本轮没有执行这些审计程序。

## 一般桥：精确模型与命题

设 \(m\ge2\)，共同有限标签集 \(A=B\sqcup P\)，其中 \(B\ne\varnothing\)，允许 \(P=\varnothing\)。固定 \(q>0\)。每个 \(b\in B\) 恰覆盖同一个质量为 \(mq\) 的客户块 \(C_B\)。给定 \(P\) 的任意 partition \(\mathcal Q\)，每个组 \(Q\in\mathcal Q\) 对应质量恰为 \(q\) 的块 \(C_Q\)，且

\[
C_B\cap C_Q=\varnothing,
\qquad C_Q\cap C_{Q'}=\varnothing\quad(Q\ne Q'),
\qquad\operatorname{cov}(p)=C_Q\quad(p\in Q).
\]

没有额外跨块客户，也没有覆盖上述多个块的标签。所有玩家按固定次序各行动一次，观察完整有序历史，终局均分客户价值。每个玩家所有动作都允许重复，标签虽可同覆盖但始终可区分。

在原“有限不同单位客户”模型，非空 private 块要求 \(q\) 为正整数；若原来给的是有理质量，可先清分母作同倍整数克隆，全部收益及福利同倍缩放，SPE 判据不变。任意实数质量的说法属于质量模型；不能把不可有限克隆的实数块直接称为有限单位客户实例。\(P=\varnothing\) 时只需 \(mq\) 能由单位客户实现。

对两个 partition \(\mathcal Q,\mathcal Q'\)，完整纯策略空间是同一空间

\[
\Sigma=\prod_{i=1}^m A^{A^{i-1}},
\]

因为玩家顺序和全部动作标签均未改变。命题是作为这个共同空间的子集，

\[
\operatorname{SPE}(\mathcal Q)=\operatorname{SPE}(\mathcal Q').
\]

这个等号不要求任意非均衡策略的收益函数相同，也不要求两个 partition 的全部 IC 线性行相同。

## 证明一：任何含 private 的历史强制后续 big

取任意决策历史 \(h\in A^{i-1}\)，令

\[
\pi(h)=\#\{j<i:h_j\in P\}.
\]

\(\pi\) 是先前 private **行动次数**，不是 distinct private 标签数，更不是 private 组数。假设 \(\pi\ge1\)。当前玩家选任意 \(b\in B\)，不论这个行动后所给策略如何按历史变化，终局 big 使用者总数 \(n_B\) 满足

\[
1\le n_B\le m-\pi,
\qquad u_i\ge\frac{mq}{m-\pi}>q.
\]

当前玩家改选任意 \(p\in P\)，不论之后选择何种续局，其块只含质量 \(q\)，故收益至多 \(q\)。若与已有 private 共组，实际收益还可能低于 \(q\)，但该上界已经足够。

这些界针对**当前行动与其各自真实后继联合产生的终局**，不冻结 prescribed 后继；即使不同 big 标签触发不同续局，下界仍逐标签成立。因此在任一含 private 的决策历史，任意 big 都严格优于任意 private。每份完整纯 SPE 必须满足

\[
\tag{A}\forall h\text{ with }|h|<m,\ \pi(h)\ge1:\quad \sigma_{|h|+1}(h)\in B.
\]

这同时覆盖全部离轨历史，包括前缀中已经有多个 private、private 在同组重复、异标签同覆盖，以及原根路径根本不会经过的历史。无需假设这些历史先前的行动理性。

反过来，若完整策略满足 (A)，从任何这样的历史开始，不论当前强制哪个动作，之后所有决策历史仍含 private，故后继全选 big。当前若选 big，所得收益正好为 \(mq/(m-\pi)\)，与 big 标签无关。当前若选 private，所得收益至多 \(q\)。所以 (A) 已足以保证所有含 private 历史上的完整 IC；这里只允许 big 之间任意平局。

## 证明二：全 big 历史上的每个真实菜单值均与分组无关

固定任意满足 (A) 的完整策略函数 \(\sigma\)，不预先假设它在某个 partition 下是 SPE。取全 big 历史 \(h\in B^{i-1}\)。对任意当前强制动作 \(a\in A\)，记

\[
V_\sigma(h,a)=u_i\bigl(\alpha((h,a),\sigma_{i+1},\ldots,\sigma_m)\bigr).
\]

若 \(a=p\in P\)，此前没有 private，而选 \(p\) 后已有 private，(A) 强制全部后继 big。因此当前玩家是该 private 块的唯一使用者：

\[
\tag{1}V_\sigma(h,p)=q\qquad(p\in P).
\]

若 \(a=b\in B\)，沿 \(\sigma\) 的真实后继，在第一次 private 出现之后全选 big，因此其后续 private 次数

\[
\delta_\sigma(h,b)\in\{0,1\}.
\]

这个 \(\delta\) 由同一策略函数在具体标签历史上的取值决定。它可以随 \(b\) 改变，不能以“所有 big 同覆盖”为理由把它们的续局强行合并。但两游戏的标签树和同一 \(\sigma\) 一样，故每个 \(\delta_\sigma(h,b)\) 在两个 partition 间相同。当前玩家的终局收益为

\[
\tag{2}V_\sigma(h,b)=\frac{mq}{m-\delta_\sigma(h,b)}\in\left\{q,\frac{mq}{m-1}\right\}.
\]

(1) 与 (2) 给出了按**原动作标签逐项索引**的全部当前菜单。所有值均独立于 private partition。特别地：

- 若某个 big 真实后继出现一次 private，则最大菜单值为 \(mq/(m-1)>q\)，当前必须选具有这种后继的 big 标签。
- 若所有 big 真实后继均全 big，则全部 big 和全部 private 菜单值均为 \(q\)，允许任意标签、任意历史依赖的弱平局选择。

由此得到完整而可直接复用的充要判据：

\[
\boxed{\sigma\text{ 是 SPE}\iff\text{(A) 成立，且每个 }h\in B^{<m}\text{ 上 prescribed 动作最大化 (1)—(2)。}}
\]

必要性来自第一部分和每个决策历史的真实偏离 IC；充分性来自第一部分对全部含 private 历史的 IC，以及第二部分对全部全 big 历史的 IC。两类历史穷尽完整决策树，双方都保留弱不等式。

这个判据的两侧没有任何 private 组成员关系。因此它对 \(\mathcal Q\) 和 \(\mathcal Q'\) 逐个 \(\sigma\) 相同，证明两个 SPE 集合相等。该证明也给出反向迁移，既不重新选平局器，也不换成只具有相同 outcome 的另一策略。

注意：这不是要求联合多玩家偏离的强均衡判据。原模型每个玩家仅在自己的层行动一次，上述逐历史单方最佳回复正是完整纯 SPE 条件。

## 根路径、福利与 OPT

固定同一确定性完整策略时，根有序标签路径相同是标签树相同直接给出的事实；对共同 SPE 另有更强结构：第一次 private 后后继全 big，所以根 private 总次数只可能是 0 或 1。

若为 0，\(m\) 条行动都覆盖同一个 big 块，福利 \(mq\)。若为 1，由 \(m\ge2\) 仍至少有一个 big 使用者；所覆盖块正好为一个 big 块和一个 private 块，福利 \((m+1)q\)。不会因为别的未使用 private 标签与该标签共组而改变福利。

当 \(P\ne\varnothing\) 时两个福利值均可实现：任意全树 prescribed big 的策略给 \(mq\)；另取根 prescribed 一个 private、其余所有历史 prescribed big，根 private 与任何 big 偏离的收益均为 \(q\)，给 \((m+1)q\)。这是存在性说明，不是要求原保存策略出现 private。

静态最优方面，至少选一个 big 时，其余至多 \(m-1\) 槽能新覆盖 \(\min(m-1,g)\) 个 private 组，达到

\[
mq+q\min(m-1,g).
\]

不选 big 的任意 \(m\) 槽至多覆盖 \(q\min(m,g)\le mq\)，不会更优。目录允许重复，槽不足时可重复补齐。因此所报 OPT 公式既是上界又可实现。

作为这一个明确块族的推论，所有 SPE 有

\[
\frac{\operatorname{OPT}_m}{W}\le\frac{m+\min(m-1,g)}m\le 2-\frac1m<2.
\]

这只排除本块族的 half 反例；固定原策略锥中还有其它客户类型、质量比例或共享结构时，不在此推论的域中。故不能由它推出原共享循环整个客户锥安全。

## 边界与失效条件

| 条件 | 核验结果 |
|---|---|
| \(m=2\) | 证明原样成立；含一个先前 private 时 big 至少给 \(2q>q\)；OPT 为 \(2q+q\min(1,g)\)；两种可能福利为 \(2q,3q\) |
| \(P=\varnothing\) | 只有空 partition、\(g=0\)；全部动作属于同覆盖 big，任意完整策略都是 SPE，W=OPT=\(mq\) |
| \(P\ne\varnothing\) | 至少一组；组内可含任意多个不同标签，证明不要求 private 标签覆盖互异 |
| \(q=0\) | 必须另支：所有块都零质量，所有完整策略均为 SPE，分组不变性仍成立；W=OPT=0；“后继强制 big/至多一次 private”不成立，效率比不能记作 0/0 |
| 重复、弱平局、同覆盖异标签 | 全部保留；特别是同覆盖 big 的后继可因标签不同而不同，已由 \(\delta_\sigma(h,b)\) 逐项处理 |
| 任意离轨历史 | 第一部分使用任意历史的 private 次数，未用根可达性，也未假设前缀本身为最佳回复 |
| 空 big 类 | 不在命题内且确有失效：两玩家、两个 private 标签，分成两组时第二玩家应避开前标签，合为一组时两标签可平局，SPE 集合会改变 |
| 修改 private/big 身份 | 不在命题内；同标签树不够，还须固定两类身份及覆盖尺度 |

最后一项可用小例明确区分：\(m=2\)，原 big 标签 \(b\) 覆盖 \(2q\)，private 标签 \(p\) 覆盖独立 \(q\)。在历史 \((p)\)，再选 \(p\) 至多得 \(q/2\)，选 \(b\) 得 \(2q\)，不能规定 \(p\)。若把同一标签 \(p\) 改成也覆盖 big 块，则所有动作都覆盖同一块，原历史上也可规定 \(p\)。这证明“private 变 big”的变换一般不保策略集合，不能借本桥为 G10/G9 作迁移。

## 四端点：原冻结定位、客户掩码与策略函数身份

以下下标严格采用原 gzip 解压 JSON 的零基 `results[i]`，不按根计数或组合另行重排。每条完整策略位于 `results[i].strategy`，其两个键恰为 `terminal_counts` 与 `actions`；动作数组每条恰含 `history`、`action`。`history` 是长度 0—4 的有序整数标签数组，`action` 为 0—6 中一个整数。共同玩家数 5、标签数 7。

| i | 原根计数字段及 `strategy.terminal_counts` | 原 portfolio | `integer_clones` 非零项（mask:单位重数） | 保存根路径 |
|---:|---|---|---|---|
| 0 | `(0,1,1,1,2,0,0)` | `(0,1,2,5,6)` | `1:1, 30:5, 32:1, 64:1` | `(1,2,3,4,4)` |
| 1 | `(0,1,1,1,2,0,0)` | `(1,2,3,5,6)` | `30:5, 32:1, 65:1` | `(1,2,3,4,4)` |
| 2 | `(0,1,1,2,1,0,0)` | `(0,1,2,5,6)` | `1:1, 30:5, 32:1, 64:1` | `(1,2,3,3,4)` |
| 3 | `(0,1,1,2,1,0,0)` | `(1,2,3,5,6)` | `30:5, 32:1, 65:1` | `(1,2,3,3,4)` |

掩码 30 的位集为 \(\{1,2,3,4\}\)，因此这四标签为 big；private 标签固定 \(P=\{0,5,6\}\)。G8 即 i=0/2，private partition 为 \(\{\{0\},\{5\},\{6\}\}\)，\(g=3\)；G7 即 i=1/3，掩码 65 位集为 \(\{0,6\}\)，partition 为 \(\{\{0,6\},\{5\}\}\)，\(g=2\)。所以 \(m=5,q=1\)，big 块 5 单位，OPT 分别 8、7。

本轮的只读结构比较覆盖了四条 `strategy.actions` 的**全部记录**，没有只读根路径或计数压缩摘要。检查包括：每表有 2801 条、无重复历史；key 集精确等于 \(\bigcup_{d=0}^4\{0,\ldots,6\}^d\)；各深度数 1/7/49/343/2401；每条 history/action 的类型、范围与键名正确。随后按有序历史逐项比较规定动作，另核 `terminal_counts`。这属于完整表身份与形状比较，不是逐历史收益/IC 重新认证。

为避免把重排或格式误当数学差异，固定如下规范化：历史按 `(长度, 字典序)` 排列，构造 `[{"history":list(h),"action":sigma(h)}, ...]`；对 JSON 使用 `sort_keys=True,separators=(',',':')`，UTF-8 编码后取 SHA256。原四个 `actions` 数组本来就是这个顺序，所以本轮原数组规范化哈希与排序后的规范化哈希相同。哈希只作可复核定位；等同性是实际逐项比较得出的。

| i | 规范化 `actions` SHA256 | 规范化整个 `strategy` SHA256 |
|---:|---|---|
| 0、1 | `0f87843050a3c47ac6a35334603a459c7688c8c1ac8e2e05ba003ce8fbef873c` | `ace085f3b04d1480aeac3bff785f95f452c046f665d3a42c762984931e7d427e` |
| 2、3 | `cf5e8b80aa7693fd329df9557580e5e4a5b3e18a861bb66a977e72f84bbfcbc6` | `621110580d2774846f87e48434d1dc3ff5626c8e87b052729d7aac7a339c7686` |

实际比较结果：i=0 与 i=1 的整个 `strategy` 字段逐项相同；i=2 与 i=3 同样相同。两个不同根计数组的动作函数只有一处差异：

\[
\sigma^{(0)}(1,2,3)=\sigma^{(1)}(1,2,3)=4,
\qquad
\sigma^{(2)}(1,2,3)=\sigma^{(3)}(1,2,3)=3.
\]

其余 2800 处规定动作相同，但 `terminal_counts` 也随这处根可达差异改变，故不能说四个完整 `strategy` 全同。第一张表 prescribed 标签计数为 `{1:88,2:109,3:970,4:1634}`；第二张为 `{1:88,2:109,3:971,4:1633}`，全部规定动作在 big 类。这为有限端点提供结构解释；本轮并未重新计算 4×16806 条真偏离 IC，也未重新构造任何对偶行编号。

一般桥加上述表身份比较允许精确说：每一对 G8/G7 保存的是同一完整策略函数，同一根路径且 W=5，但只因 private partition 合并，静态 OPT 从 8 变为 7。这不是说 8/5 与 7/5 的原 LP 最优性可互相迁移；目标覆盖、允许客户变量和固定锥的对偶问题均须按各自合同处理。

## M-268 的 0↔2 共轭：输入相同，保存策略不相同

原冻结 JSON 的精确定位为

`archives/customer-attraction/tools/evidence/background-terminal-first-floor-primary/original/research/workspaces/customer-attraction/R-e6796fb9db2a4ae9994cee93ac9bd152/background/first_floor_best_5_7.json`

37938B，SHA256：`e8ef2e9f90a844b2fe7249886dff78efca84f8830f58048dfe509992b64e237b`。本轮读取此 original 原件，不使用新游走或重跑产物替代给定策略。

原对象的非零 mask 是 `4:1,27:5,32:1,64:1`，big 为 \(\{0,1,3,4\}\)，private 为 \(\{2,5,6\}\)。令 \(\tau\) 交换标签 0 与 2，其余标签不变。正确的保存策略运输必须同时重命名输入历史和输出动作：

\[
\sigma_i^\tau(h_1,\ldots,h_{i-1})
=\tau\bigl(\sigma_i(\tau^{-1}(h_1),\ldots,\tau^{-1}(h_{i-1}))\bigr).
\]

原策略以 330 条计数状态 `acts` 定义，故读取新历史时先按 \(\tau^{-1}\) 改名再计数、查询原 `acts`，最后把原动作按 \(\tau\) 改名。只改客户 mask 或只改 prescribed 输出而不改历史参数，均不是这个给定策略的共轭。

共轭后的非零客户 mask 恰为 `1:1,30:5,32:1,64:1`，即 G8 输入；它确实保全“原给定策略的显式重命名像”这一身份。但它**不等于**四端点中已有的任一保存策略：

| 比较项 | M-268 的共轭策略 | 四端点 i=0/1 | 四端点 i=2/3 |
|---|---|---|---|
| 根动作 | 3 | 1 | 1 |
| 根路径 | `(3,3,3,1,1)` | `(1,2,3,4,4)` | `(1,2,3,3,4)` |
| 与共轭策略不同的有序历史数 | 0 | 1830 | 1829 |
| 全树规定动作可取标签 | `{1,2,3}` | `{1,2,3,4}` | `{1,2,3,4}` |

上述差异数是把原 330 计数状态表在同一 2801 有序历史域逐项展开后作结构比较，未计算 IC 收益。共轭展开表按上一节规范的 `actions` SHA256 为 `06ef199745eeba44e38c46db9cfb49db6f0508756672331b4226421e160904fa`。

因此可以把 M-268 的给定策略通过显式共轭送到 G8，再通过本桥保留同一函数送到 G7；这得到的是**另一个给定策略的准确运输结果**，不能把它偷换成 M-c38 已保存的两张表。更不能从“它们在同一客户输入下都是 SPE”得出两个有限对象的整条陈述等价。M-c38 还包含四保存记录及两个指定对偶的内容，M-268 则固定原 330 状态表；整条合同不同。

## 后续可复用交付与 primary 边界

一般桥已完成完整证明，不需要再做大规模 SPE/LP 试算来判断其真假。值得后续正式接续的是一个窄端点问题：在现有精确对象中，分别明确“相同客户输入”“显式标签共轭的给定策略”“不同 private partition 下同一策略”三种关系，并把所得 SPE/根福利运输记为实际的局部数学贡献。原 primary 也可直接用本稿解释其两对保存表为什么 W 相同而 OPT 不同。

若 Root 认为该定向比较应正式派工，建议使用同档对象间的具名比较问题，核查当时实际队列与 endpoint pins 后安排，避免与原 primary 重复认领。该正式交付至少应保留：上述两个对象 ID、共轭公式、M-268 共轭后与 M-c38 保存表不相同的根动作证据、以及“只运输 SPE/福利，未运输指定 LP 对偶”的边界。不应把这种局部结果写作两对象的 whole-result 等价。

单个 M-c38 对象内部的 G8/G7 两对记录不必人为建立同对象到自身的边；其解释可留在对象正文、实际 comparison_scope 或已有边的贡献说明中。一般桥是否有独立对象价值由 Root 按后续复用需要决定，不能仅因本次证明出现而自动 new-node。

本审查既不认领原 primary，也不交付它的正式 coverage/receipt；没有把表身份比较写成 IC 重新认证，没有把结构桥写成原 7/5 对偶证明。现有原合同的真值仍由其原正文与冻结证据承载，Root 可在随后串行整合时引用本稿的已证明桥及精确结构事实。

## 补充定位：可选有限 checks/context 的原全称目标

按 Root 的追加指示，另外只读定位了四端点来源实际提及的原一般目标，未猜测同名对象。用同一 `load(root, verify=False)` 精确取 `objects['Q-CAG-HALF']`，读完整合同，并对其 body 用 `ref_bytes` 校验文件 SHA、读取所指 section：

| 字段 | 精确当前值 |
|---|---|
| object_id | `Q-CAG-HALF` |
| version | 2 |
| registration_pin | `dccd5277f7b0c1bb4dcac17287010f1d012bb40c6244c51f24808c1519a4b5ea` |
| title | 任意人数共同目录完整历史纯SPE的半覆盖问题 |
| truth_status | open |
| body.path | `archives/customer-attraction/state/问题/任意人数完整均衡半覆盖--问题.md` |
| body.sha256 | `bc5add8e880e83c3ed799f457607103532aa9120018c862ae3ac869f2ed34d15` |
| body.section | `完整量词和目标` |

完整核心量词为：对每个整数 \(m\ge1\)、每个有限不同单位客户与有限非空带标签共同目录实例、每份在全部有序历史定义的完整纯 SPE \(\sigma\)，是否均有 \(2W(\sigma)\ge\operatorname{OPT}_m\)。保留空主题、重复、同覆盖异标签、离轨历史、零客户与任意弱平局；OPT 允许重复主题。原正文明确此稳定 ID 保持任意 \(m\) 的原题身份，五人定理已闭合，恰六人全量词问题另列独立目标。

四个保存端点最多可成为这一原全称命题的四个给定实例的有限 `checks`/context；此类边不证明该全称问题，也不由其近二比值反驳该问题。本补充只给 Root 可选 target 的精确定位，不替 primary 决定是否出边；primary 即使最终实读后零边，也可依其正式任务范围完成覆盖。没有为这些实例另造主题 hub 或同对象自边。

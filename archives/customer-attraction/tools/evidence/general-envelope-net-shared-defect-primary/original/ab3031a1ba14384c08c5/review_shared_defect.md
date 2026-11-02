# 共享遗漏缺陷推论与解析架构的独立审查

**范围与等级。** 本次逐式阅读同目录 `architecture_audit.md`，回到旧来源 `research/workspaces/customer-attraction/R-324fbf8f72b041578583b51189f13d1a/dynamic_budget.md` §2 式 (2.5)，并重读 canonical `research/current/customer_attraction/uncovered_private_seat_spectrum.md` §§1–3 的阈值归纳与完整谱预算。以下是解析内部复核；未运行新扫描，未认证外部审查或新颖性，不改变一般/六人 OPEN 状态。

## 1. 最优主题扩成极大主题：合法且不改变比较并集

固定最优至多 `n` 主题并集 `O`。有限目录中每个主题有一个包含它的合法 inclusion-maximal coverage。逐题选择这些容器后，仍只使用至多 `n` 个合法主题；新并集 `O'` 包含 `O`，但由 `OPT_n` 定义 `|O'|≤|O|`。有限集合包含及等基数给 `O'=O`。

此操作仅在比较元组内进行，原完整策略、实际行动及其收益分母都没有变化。它不是把早期真实动作升级成容器，故不涉及 SPE 是否在这种替换后仍成立的问题。

## 2. 旧谱预算逐步重构

令实际覆盖 `C0`，`W=|C0|`。全部目录极大全局私有块为 `P_j`，令 `Q_j=P_j\C0`、`a_j=|Q_j|`、`v_j=|B_j\Q_j|`。这是全目录 maximal incidence 恰为 `{j}` 的私有性，不能换成“在所挑最优主题中只出现一次”。

把最优并集写作 `O=∪_{j∈J}B_j`，`|J|≤n`。定义

\[
 I=|O\cap C0|,\quad
 D_p=|(O\setminus C0)\cap\cup_jP_j|,\quad
 D_s=|(O\setminus C0)\setminus\cup_jP_j|.
\]

全局私有客户属于 `O` 当且仅当其唯一的极大主题在 `J` 中，所以 `Σ_{j∈J}a_j=D_p`。并且

\[
 \bigcup_{j\in J}(B_j\setminus Q_j)
 = O\setminus\bigcup_{j\in J}Q_j,
\]

其大小为 `I+D_s`；故 `Σ_{j∈J}v_j≥I+D_s`，重复计算共享客户只会加强此上界。

canonical 谱包含每个第一席位 `a_j+v_j/n`。前 `n` 大项之和 `Λ` 至少为 `J` 中至多 `n` 个第一席位之和；不足 `n` 项时使用其余非负席位补齐。原完整 SPE 的实际总收益给 `W≥Λ`。于是

\[
 \boxed{W\ge\Lambda\ge D_p+(I+D_s)/n.}
 \tag{1}
\]

空块、目录仅一个极大主题和零客户均无除零问题。谱归纳所用的 `Q_j` 在所有离轨历史保持固定，实际路径不触及 `Q_j`，因此没有把不同分支的遗漏集合混为一谈。

## 3. 缺陷上界通过；还可保留实际额外覆盖

令 `η=1−1/n`。由 `OPT_n=I+D_p+D_s` 和式 (1)，

\[
 \operatorname{OPT}_n\le W+\eta(I+D_s)
 \le (2-1/n)W+\eta D_s.
 \tag{2}
\]

与父方正文相同，其精确非负账是

\[
 (2-1/n)W+\eta D_s-\operatorname{OPT}_n
 =\underbrace{W-D_p-(I+D_s)/n}_{S\ge0}
 +\eta\underbrace{(W-I)}_{E\ge0}.
 \tag{3}
\]

所以 `n≥2` 时，`D_s≤W/(n−1)` 足够 half；真正严格反例对每个最优并集均必须 `D_s>W/(n−1)`。该断言是旧预算的直接代数推论，审查通过。

还可以在式 (2) 第一步保留 `E=|C0\O|=W−I`，得到更精细的同一推论：

\[
 \boxed{\operatorname{OPT}_n\le(2-1/n)W
 +(1-1/n)(D_s-E).}
 \tag{4}
\]

此时精确余量就是 `S`，并有

\[
 n(2W-\operatorname{OPT}_n)
 =nS+W-(n-1)(D_s-E).
 \tag{5}
\]

因此 `D_s−E≤W/(n−1)` 已足够 half；真正严格反例对每个最优 `O` 必须

\[
 \boxed{D_s-E>W/(n-1).}
 \tag{6}
\]

六人时即 `D_s>E+W/5`。保留 `E` 与原任务的净差口径一致，并不将遗漏总量当作目标。式 (4)–(6) 仍只是原混合席位预算的显式推论，没有新增能控制共享遗漏的 SPE 行，也没有证明这个必要条件不可能满足。`n=1` 由 `OPT_1=W` 单独处理，不使用 `(n−1)` 分母。

## 4. 同时审过的架构边界

* 独立逐型重构了 `architecture_audit.md` §3 的三列 Farkas 障碍：early-only/o=0 给 `τλ_i≤2`，penultimate-only/o=0 给 `τρ≤2`，omitted/o=1 给 `1≤Σ λ_i/(n−i+1)+ρ`，合为必要条件 `τ≤2H_n−1`。这仅排除所写完整独立 literal 域的 prefix-only+R 模板。若另取 `C=U` 主动删除 `o=0` 列，该见证不适用；若加入末位安全行、actual-B 查询或其他真实行，也不能沿用此停界。
* 本次回到既有 9/2 正文 `research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_6/fractional_cover_pair_half.md` 第一节“当前较强版本：9/2，七条真行”，核对 `R_τ` 中 `A` 是实际倒二行动，bonus 是 `o a 1_{p=0}/4`；不是末位新增覆盖，不依赖 maximality。该正文给的同源 `S/Z/V` 消元对任意非负整数背景 `p` 和任意 `τ≥1` 适用，父方一般人数的恢复没有引入新分母。
* 关于用户 `f_j(p+e_k,r−1)≥f_j(p,r)` 的错误及合法修正，完整解析另见同目录 `private_recurrence_audit.md`：同路由 private 损失精确为 `w_{ {j} }/[(p_j+1)(p_j+2)]`；不能把其补偿势免费计为福利。

审查没有把非负总行的每客户系数当作非负，也没有把 Farkas 加权列当作真实 SPE。到此没有发现上述已明确范围内的致命异议；尚缺的是对式 (6) 中净共享缺陷的普适共同付款。

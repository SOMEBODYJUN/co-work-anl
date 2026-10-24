# 一般节点福利 relay 的背景纠错与严格完整 SPE 证书

2026-10-24。一般共同目录、任意人数、完整有序历史纯 SPE。以下纠正现有 `R-1740705e79f14baba6326b951a52152f/representation/cross_branch_welfare_relay_identity.md` 的 R1；不改变 Q-CAG-HALF 的 OPEN 身份，不作为一般 half 正面突破。

## 1. 漏项

节点 h 长 i−1。强制当前选 T、以后沿原完整策略得到 z(T)。定义

\[
B(T)=\sum_{j<i}u_j(z(T)),\qquad
d(T)=u_i(z(T)),\qquad
V(T)=\sum_{j>i}u_j(z(T)).
\]

即使过去的动作固定，其最终利润 B(T) 仍随真实后继变化。完整福利恒等式是 W(z(T))=B(T)+d(T)+V(T)，不是 d(T)+V(T)。写规定主题 A*，原 SPE 给 g(T)=d(A*)−d(T)≥0，故精确地

\[
\boxed{W(z(T))-W(z(A^*))
=B(T)-B(A^*)+V(T)-V(A^*)-g(T).}\tag{C1}
\]

合法中继不等式因此是

\[
\boxed{\Delta W\le\Delta B+\Delta V.}\tag{C2}
\]

根节点 B=0 时恢复旧 R1。一般节点也可改用 active 总利润 P(T)=d(T)+V(T)，精确得到 ΔP=ΔV−g，故 ΔP≤ΔV；P 一般不是完整福利。

原调和势式 R2 仍合法：对每个终局令 Φ=Σ_xH_c，则 d(T)=Φ(z(T))−Φ(z(T)_{−i})。因此 ΔΦ≤ΔΦ_{−i}。其中 Φ_{−i} 包含过去与未来的全部其他玩家，不可只解释成后继势。

## 2. 四客户、两主题、全部非平凡 IC 严格

m=2，单位客户 {1,2,3,4}，共同目录

\[
A=\{1,2,3\},\qquad C=\{4\}.
\]

完整策略：根选 A，末位在两个可能前缀 (A)、(C) 后均选 A。全部非平凡 SPE 比较如下：

| 有序历史 | 规定当前收益 | 唯一另一行动的真实收益 |
| --- | ---: | ---: |
| 空历史 | 3/2（终局 AA） | 1（强制 C 后终局 CA） |
| (A) | 3/2（AA） | 1（AC） |
| (C) | 3（CA） | 1/2（CC） |

所以这是一份完整严格纯 SPE，不依赖任何平局。实际终局 AA 覆盖 W=3。在一般节点 h=(A) 强制末位改选 C，终局 AC 覆盖 W=4，且两枝均无后继，V(T)=V(A*)=0。因此旧 R1 会给 1≤0，严格错误。

本节点过去玩家利润从 AA 中的 3/2 变为 AC 中的 3，当前收益从 3/2 变为 1。C1 给 1=3/2−1/2，完全吻合。原目标仍满足：W=3，OPT_2=4。

## 3. 固定背景的客户分解

令过去负载 b，过去覆盖 U={x:b_x>0}；强制分支的全部 active 负载 k(T)。记 fresh 覆盖

\[
F(T)=|\{x\notin U:k_x(T)>0\}|,
\quad G(T)=\sum_{x\in U}\frac{k_x(T)}{b_x+k_x(T)}.
\]

则 W=|U|+F，B=|U|−G，P=F+G，因而 C1 也等价于

\[
\boxed{\Delta F=\Delta V-\Delta G-g.}\tag{C3}
\]

背景的 active 股权变化 ΔG 是一般节点缺少的精确项；其符号不固定。沿不同节点把它删掉或免费计入原实际路径，会再次产生跨枝漏洞。

## 4. 需要纠正的导航/Claim（本分支未原位修改）

以下检索位置当时仍把旧式称一般节点合法关系：

- 原个人区正文 `representation/cross_branch_welfare_relay_identity.md`，定义后 W=d+V 及 R1。
- 原个人区 `README.md:12,15`。
- `research/customer_attraction/CLAIMS.md:63` 的 `CA-CROSS-BRANCH-RELAY-v1`。
- `research/customer_attraction/RESEARCH_STATE.md:104,108`。
- `research/current/customer_attraction/README.md:13` 只提供“节点级”导航，修正文后可保留链接，但应避免继续暗示福利式仅含 tail。

root 统一通知与修订；本分支只保存审查与可重放证书。

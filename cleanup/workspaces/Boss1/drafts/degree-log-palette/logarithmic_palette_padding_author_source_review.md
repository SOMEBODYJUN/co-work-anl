---
id: "unrelated-machines/private-padding-log-source-a18"
kind: "review"
type_tag: "审查"
title: "私有填充对数调色板作者草稿的版本核对"
status: "integrated-into-private-padding-log-equivalence"
summary: "完整读取 a18 作者草稿；其数学内容与现有私有填充对数调色板等价对象相同，保留作者版本与有限审计边界，不新建第二个定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/logarithmic_palette_padding_author_draft.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/logarithmic_palette_padding_author_draft.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/model_and_classical_barriers.md#8"
---

# 私有填充对数调色板作者草稿：版本核对与归并

## 来源身份和实读范围

冻结源 ID 为 `a18ca503081e65e1a99f`，路径为
`history/source/notes/unrelated_machines/logarithmic_palette_padding_author_draft.md`；两份定位是
`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交
`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。inventory blob 为
`96402d03c73e2febd83bfd114caecece8a14c088`，文件大小 9155 bytes，SHA-256 为
`75aa7722c3839f8404bdf1f2377dd9dd4b3d262a50aa2cc05b9e33fd6814082a`。

正文七节全部读取，并与现有正式对象
[私有填充的对数字母表调度等价--等价.md](../../../../archives/unrelated-machines/state/等价/私有填充的对数字母表调度等价--等价.md)、三种正规形审查和保存的 canonical 模型 §8 逐段比较。作者草稿是该 §8 的早期编号/措辞版本：它用式 (1)–(9) 和普通二级标题，canonical §8 改用 (8.1)–(8.9)，并在最后补入证据链接及“scoped proof”措辞。没有数学量词或结论差异；应把它作为作者版本 provenance 合并到现有对象，而不是创建重复等价定理。

## 主张和精确量词

固定 (N\ge2)，(H=\operatorname{bitlength}(N))，对 (j\ge2)、(2^j\le H) 置
(b_j=1+1/(8j))、(R_{N,j}=\lfloor H/2^j\rfloor)，定义
[
\mathcal A_N=\{1,N^2\}\cup
\bigcup_{j\ge2,2^j\le H}\{\lceil b_j^r\rceil:0\le r\le R_{N,j}\},
]
去重后 (|\mathcal A_N|=O(\log N))。`D_log` 是所有显式 (m'\times N) 正整数有限矩阵，(m'\ge1)，每项在该同一调色板中。UM-TARGET-v1 有统一小于 2 的改善，当且仅当 `D_log` 有确定性多项式位算法带统一改善。定量地，对固定 (k\ge2)，若 `D_log` 后端 (B) 的比率为 \(\alpha=2-1/k\)，则构造全模型比率小于 (2-1/(2k)) 的算法；多项式次数可依固定 (k) 变化，不声称把二进制 (k) 当输入的统一多项式。

## Padding、阈值网格和全目标矩阵

对原矩阵 (P)，(n=0) 直接空调度；每个任务有零边时直接输出 OPT=0。否则
(0<L=\max_j\min_i p_{ij}\le O=OPT(P)\le U=\sum_j\min_i p_{ij}\le nL)。取
(ell) 为 (2^\ell\ge8kn) 的最小非负整数，令
(E=2^k8k\ell)、(N=2^E)、(H=E+1)、(d=N-n)。加入 (d) 个私有 dummy 任务和 (d) 台私有机器，目标矩阵为 ((m+d)\times N)。第 (k) 个网格覆盖 (8kn)，固定 (k) 下 (N) 是原输入规模的固定次数多项式。

对 (T=L b^t) 网格直到首个不小于 (U) 的候选，令 (s=8kn)。若 (p_{ij}\le T)，取
(z=sp_{ij}/T)，最小 (r\ge0) 使 (b_k^r\ge\max(1,z))，并置 (q_{ij}=\lceil b_k^r\rceil)；其余原边及原任务到 dummy 机为哨兵 (N^2)。每个 dummy 任务自己的机器成本 1，其他所有机器成本 (N^2)。故所有目标矩阵项在同一 (mathcal A_N)。精确地 (z\le q(z)\le b_kz+1)，包括 (z=0,1) 和 (p=T)。算法运行假定 backend (B)，检查完整输出和哨兵边；拒绝坏候选不等于证明 (OPT(P)>T)，保留候选后去除 dummy 块并按原矩阵精确计算峰值。

## 解码证明和比率

取第一个 (T\ge O)，则 (O\le T\le b_kO)，原最优赋值及 dummy 私有赋值给出
[
OPT(Q(T))\le b_k(s/T)O+n\le(8k+2)n.
]
所有每个峰值至多 \(\alpha OPT(Q(T))\) 的完整输出都排除哨兵，因为
(alpha OPT(Q(T))<2(8k+2)n<N^2) 且 (N\ge16kn)。因此 backend 的实际输出也必须把每个 dummy 放回私有机、每个原任务留在原保留边。

对每个保留边 (p_{ij}\le Tq_{ij}/s)，使用上式的强第一项而非粗界：
[
C_P(B(Q(T)))\le (T/s)\alpha OPT(Q(T))
\le\alpha[b_kO+T/(8k)]\le\alpha b_k^2O
< (2-1/(2k))O.
]
反向蕴含只是把全模型算法限制到 `D_log`；因此这是统一改善的存在性等价，而非给出一个具体 backend 或 hardness。

## 复杂度、审计和缺口

固定 (k) 时 (E=O_k(\log(n+1)))，目标全矩阵和所有 dummy 交叉边必须显式写出，每项位长 (O_k(\log(n+1)))，阈值网格也只有 (O_k(\log(n+1))) 项；ceil、比较、回译均按总编码长度多项式，不按分母倒数循环。不能把 padding 后的天文 (N=2^E) 误读为小整数 (E)。

作者草稿附带的 `audit_logarithmic_palette_padding.py` 只做完整压缩分类：任一 dummy 非私有或原任务去 dummy 机的负载至少 (N^2)，低峰 dummy 必须唯一私有，剩余状态由原 active 分配决定。它不物化天文矩阵，也不运行未知 backend。源中记录的精确边界包括 (n=0)、(m=1)、(n=1)、OPT=0、∞ 边、522-bit 分母；同一 §7 audit 的 `--max-n 128 --large-bits 64 --seed 20261019` 复跑与冻结字段一致，旧默认 (n=16..4096) 网格没有由该作者草稿复跑。该有限审计不能替代一般证明或把 rejected candidate 当作 OPT>T 证书。

## 与既有对象和范围的关系

现有对象已经保存同一数学链：单一只依实际 (N) 的 (O(\log N)) 调色板、固定 (k) 的显式 padding、全矩阵哨兵排除、强式回译和“未知 backend/UM-TARGET 正反面仍开放”的边界。作者草稿的独有 provenance 是早期式号、源自作者的 audit 运行说明和“未检查仓库 Git 状态/发布状态”的角色限制；这些应作为源版本和证据 manifest 保留，不改变对象真值或完成度。

建议处置为 `integrated`，目标为
`archives/unrelated-machines/state/等价/私有填充的对数字母表调度等价--等价.md`，并在该对象 `source_refs` 与 `archives/unrelated-machines/state/审查/三种正规形的分节冻结与独立核验--审查.md` 的 log-padding 小节加入本源 commit/path/SHA。没有新一般算法、NP 困难性、同任务数 (O(\log N)) 结论、外审或全球新颖性认证；六人 SPE 目标保持独立。

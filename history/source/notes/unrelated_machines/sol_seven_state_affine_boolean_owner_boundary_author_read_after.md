# 七态 affine Boolean / owner 分类：作者 Proof 实读后记录

2026-10-18。此为 read-after，不是第二份盲审。此前 Exact-first 独立记录 `/workspace/scratch/038d9dcc4cac/sol_seven_state_affine_boolean_owner_boundary_exact_first_review.md` 的 SHA256 为 `d3201aba5c072a5a48accffd80347820eb6dead90cf22a30d3ff6799784787d0`，保留原字节。

本次按 root 在实际读完该记录后释放的路由，实际全文读作者 Proof `/workspace/scratch/038d9dcc4cac/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md`，SHA256 `b887d569b134bebe1a99172d2332d670e60088705e41764db24d775d2da97259`，header 与 §1–9 全部 138 行 / 8086 bytes，工具完整返回 2045 tokens、无截断。没有打开 identity 新 AND 候选的 Exact/Proof/策略，也未索取其机制。另在旧记录冻结后、这份 Proof 获释前，实际读过 global 的不相关 product-shadow first-witness 作者 learning v2；该阅读不回填进旧分类独立记录。

结论：PASS/no fatal，作者 Proof 确证已读 Exact 的全部新分类、M3 Gram-extension、同行 owner 与背景 scope；不扩为算法、hardness 或新颖性认证。

作者 §2–4 的函数证明与我的独立重构数学路线相同：先由 C=0/1 排掉混合，再用 h-subset 交换得到系数差属于 −1/0/1；h=1 单独处理；h≥2 的两水平宽度迫单高或单低，单低由全一向量值 d/h−1≥3 排除。h=d/4 与最小 d=4,s=2 均已覆盖。作者另给域外 h=d/2 的反例 H/h−Y_i；在 d≥4、h≥2 时确非 literal 且在 0,h,d 三 slice 上 Boolean，未冒本域反例。

Gram 段使用一种不同但等价、较短的闭合：D=X−f 为 M3 null vector，乘 X^r−f^r 的 telescoping 第二因子（次数 r−1≤3）直接给 Lhat f^r=Lhat X^r，r=1,2,3,4。原 Boolean 四次 identities 于是给 E_P[(f²−f)²]=0。我的独立证明则先证 D(X+f−1) 的 Gram 范数零，再与 X²−X 的 null 关系相减。两者都只需 M3 所提供的次数≤3 正交，不假定新增端点有真实联合 law，不给 M2 免费升阶。

作者 §6–7 的 pair 支持与 owner 证明完整：不同 primitive bits 的四种模式在 Ω0 上均有正质量；两个非零 literal/constant 仅互补对可以 pair 零。因此 A_w 最多两个正 owners，常数一只能独占；A 之外 endpoints 与零一阶资格数均不受结论限制。CONFIG(B<2) 的 unit-pair 零是必要条件，没有把它写成充分调度条件。

§8 的逐背景前提与 N-job 跨背景例子均核通。条件化并未免费继承 M3/full support；每枚新增 job 的 w/private 端点之和逐样本为一，w load=C，其余 private rows≤1。所有 N 个 w 端点积分后 first=(1/10+p)/N>0 而 pairs 点态零；固定 β 只有一个正 owner。这个例子只反驳无条件物理 degree≤2 的越界解释，不能充作 actual near-two NO。

作者 §9 的有限代数 scope 与 Exact 一致。没有发现需修正文或改先行记录的错误；没有软件运行或 repo/Git/Work 修改。

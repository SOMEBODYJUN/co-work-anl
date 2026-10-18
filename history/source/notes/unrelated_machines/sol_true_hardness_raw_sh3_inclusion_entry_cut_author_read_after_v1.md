# 包含图 raw SH3 入口切：作者证明实际读后对照

日期：2026-10-18。审者：sol_true_hardness（6.1sol max）。仅 scratch；保留 Exact-first 原字节。

## 1. 实际顺序和读取范围

独立 Exact-first 记录是 `sol_true_hardness_raw_sh3_inclusion_entry_cut_exact_first_attack.md`，181 行 / 11095 bytes，SHA256 `00c51ccf3cc89270d0b1f6b9aa328bf91272fd555a8b605683c6c6495e0ef8a2`。parent 明确通知已实际全文读后，才释放作者 Proof。

本轮实际全文读取作者 `sol_raw_sh3_inclusion_entry_cut_author_proof_v1.md` 的引言和 §1–7，核得 SHA256 `d418c68c558b7c3de5e47ecaacf0b20b085061b44b1f2afc3b77d1b11fa3513a`。
对应 Exact 的 SHA256 是 `0b8815af7ded08ed5fd85efdf06c10691b683aa54c66ed1caa4b61377b77c41d`。

没有读取作者 audit/code/output、所提 general-DAG 新合并正文或 global 后续推导。本记录也没有实读 Bamas 原文来认证作者 §7 的文献对应或论文原定理；只审这里自足的原 job 数学合同。没有新运行或软件代签。

## 2. §1 的次数支付合法

作者从同机两个不同 unit endpoints 的 CONFIG 二阶零矩出发，令 n=RR'。Boolean 约化给 L(n²)=L(n)=0，因此 M3 零范数列 n 与全部 deg<=3 多项式正交。这一步正确。

作者进一步将零值提升到 deg-4 multiplier，也没有免费使用条件非负性：对任意 linear l，nl 的次数<=3，且 L((nl)²)=L(n l²)=0；最后等号因为 n 的零列已与 deg-2 的 l² 正交。因此 nl 也是 M3 零列，与任意 deg<=3 的 q 正交。将任意四次单项式拆为 lq，便得 L(nw)=0（deg w<=4）。最大总次数是六，所有 Boolean 等式乘子处于合同内。

据此，一条 unit 行的全部 incoming 之和 C_v、任意子族之和，以及它们的补量，确实在后续总次数<=6 的使用范围内表现为幂等投影。对**总共至多三个**这样的 linear factors / 原 endpoint / complement，P 的次数<=3；L(P²-P)=0 与 M3 给 L(P)>=0。不能解释成“三个投影以外还可任意追加别的因子”，但作者实际 §2 只用总共二或三个，合法。

Exact-first 中较窄的 unit-capacity lemma 只需 pair-null 的 deg<=2 multiplier；作者的较强表述有上述额外提升，二者不冲突。

## 3. §2–3 的 flux 与独立稿差别

我独立稿取 F_SW 为该固定 U_S 的原 f-entry 子族，alpha_W=L(A F_SW)，beta_WR=L(A F_SW X_WR)。作者取 C_W 为 B_W **所有** incoming f entries，b_W=L(A C_W)，y_WR=L(A C_W X_WR)。这是另一组合法、稍粗的入口质量，不是漏保原 job 身份。

作者 (2.4) 用 F_SW⊆C_W，加上每个额外项 L(A x)>=0，得到 sum_(W⊃S)b_W>=delta d1 p。其他祖先或 inactive rows 的外送可以增加 b_W，不会破坏下界。随后每个 W⊃S 的 bad terminal 数仍恰为 M，和究竟哪枚 f 触发该 B 无关。

B 的 load localizer 使用原 polynomial A R_j（deg 2）；原式最高次数五，Boolean 约化和同 B-unit pair-null 给作者 (2.3)。这不是假设一个新的“条件后可行点”。三投影 positivity 给 0<=y<=b；也可逐原 endpoint 按我独立稿的平方证明。

作者 (2.5) 使用 p=A x(1-C_W)（deg 3）的 M3 平方；L(p²-p)=L(Ax(C_W²-C_W))=0，给 y 的 parent-bound。对同一个物理 Z_R 的全部原 e endpoints 累加，再以 A(1-C_ZR) 的非负平方给 sum_W y_WR<=p。这共同容量包括所有 W，不给同祖先或同 terminal 重复预算。

作者 §3 在 delta d2>=M 分支乘入口下界，等号情形左端为零；在 <M 分支单独用非正左端，符号处理正确。H 与 M 两个组合计数同 Exact-first 重构。实际调度解释也计入了不同原 f/e jobs、同 B/同 Z 的 unit 独占，以及额外 inactive exports 只能占容量。

## 4. §4–6 的完整 jobs、有限界、floor 和 bit

作者完整 CONFIG(1) 分布与独立稿相同：U 的 singleton selector/all-home-f；B 的各 singleton incoming-f/all-home-e；Z 的各 singleton incoming-e/empty。所有原 endpoints 的 marginal 求和恰一，a_B=Kd1/(NC)<=1，terminal 总质量 d1d2/N<=C/N<=1。selector unit 下界给 CONFIG optimum 恰一。实际一条 f/e 链加其余全 home 的完整峰为 max(1,2-1/d1,2-1/d2)，这里只是上界。

四个 finite binomial bounds 与独立稿重构相同。作者精确 floor 表述 e1=Ks1/C、e2=s2/K，(6.1) 在 delta d2-M>=0 时也合法：d1>=1 的承诺保证 e1<=1，因此将 d1 下界与该非负项相乘、再代入 d2 下界，方向保持。充分大 q 时 e1<=1/2、e2<=1/4、s2M/(delta K)<=1/4，右侧至少 delta²/(4q^(a+b))，支付了 floors；比我独立稿使用的 1/8 常数更强，均足够。

各 binomial/H/M 只有 O(m) bits；这次与 ancestry 稿曾有的 O(ell log n) 问题不同：此处 m<=N 已由显式物理机器数支付，d1/d2 的全部原 jobs 也确实列出。作者没有要求构造 huge family matrix 来运行其 binomial arithmetic，也没有声称 exact SDP feasibility 位多项式。作者软件与小完整矩阵示例本记录未读未跑。

## 5. 保留的边界与冻结意见

Exact-first 指出的 rational T / real delta 定义域澄清仍保留，作者此版未单独写出有理 T' 单调解释；该澄清可以修复，不影响本证明核心。parent 已明确同意后续 canonical 显记，不能在本记录里冒称已读未来 canonical。

作者 §7 关于 source paper 的 assignment-LP、shadow 和 rho 只有作者引用/读取报告，不升级为本审者已核文献结论。本合同只切该明确包含族的 ordinary-job raw SH3；既不是 hierarchy integrality gap，也不反驳别的编码的论文定理、不提供一般算法或 near-2 计算困难性。外接 source 必须另付正 unit-entry mass 和全部原 jobs。

**冻结结论：实际读后未发现新的核心 fatal 或 free conditioning。** 作者全 incoming flux 与我的固定-S flux 证明都成立；两份独立记录保持原状，数学与作者软件/外部文献认证分开。

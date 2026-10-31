# Token-label lift：实际作者读后 v1

2026-10-18，sol_true_hardness（6.1sol max）。root 实际全文读过独立 Exact-first 之后释放作者 Proof；本次实际完整读取该 Proof 的导言与全部 §1–6。

实际文件与 SHA256：

* Exact：`sol_token_label_lift_exact_v1.md`，`5a953ed6365e2be029ef31d3ee0184447d626971ad8af7369ee5190eac69a86d`（此前独立阶段已全文读）。
* 作者 Proof：`sol_token_label_lift_author_proof_v1.md`，`88904ae073464b199a928516af9918422f684c606ff5efe67e075ba2e70a06a8`（本次实际全文读）。
* 保持冻结的独立稿：`sol_true_hardness_token_label_lift_exact_first_attack.md`，`091585c4b21b13eb8487435d094fa6b0d8905655c88a7232faa4a39d32d1b9d0`。

结论：Exact 的 (A)–(D) 无新增 fatal，作者证明与独立重构相容。下列对照明确区分实际相同的数学、两种不同的 PSD/no-extension 证法和 Proof 的额外说明。未读取作者 audit/code，未重跑作者程序；此次未新增数值运行。

## 1. 一般 M1 与 home 混合

作者 §1–2 的 category counts `n0=k−rA,nw=Xw` 将独立稿的 home/head contrast 块写成 weighted category Laplacian：

`k diag(L n)−L(nnᵀ)`。

其 home/head 权为 `L(n0Xw)=hL(Xw)≥0`，head/head 权为 `L(XwXv)≥0`。这正等于独立稿的

`[[hrL(A),−h pᵀ], [−h p,k diag(p)−M]]`。

两个写法都只在 contrast 向量中使用，平均项保留与所有其它 groups/context 的共同 aggregate 相关；没有独立化这些相关。k=1 单独线性代换，r=0/k 和 inactive-home 项的系数无冲突。两稿都没有把真实 injection kernel 的随机解释免费应用到 pseudoexpectation 后声称 M2 PSD。

§2 最后的 native-row 配置说明明确另需 incoming-activity 与 destination pair-zero 等 native identities。它不是 Exact 抽象 group 方程单独的结论。其所描述 row law 若使用这些额外关系，incoming端 e 与 home 的 mixed 矩须满足 `L'(e t_a)=(h/k)L'(e)`；由 e≤A 及 lift 的 `t_a=1−rA/k` 一阶 replacement 得到。此读后不将该条件说明升级为任意 aggregate 模型的原生 row-lifting 定理、显式小支持列举或配置 oracle。

## 2. aggregate M2：作者较大 Schur 与独立的精确 pair-basis Schur

作者 §3 没用独立稿的 45 维 pure-X pair basis，而是将 q0(X) 扩大成 210 个 four-subsets 上的任意函数。其 220 维 block 的 Schur 是

`delta(M_beta−delta Dlarge)`，`Dlarge=210 Bᵀ W² B`。

这是合法的充分正性证明：actual degree-two polynomial evaluations 是这个较大空间的线性子空间。作者所列 Dlarge 三类 eigenvalues 经本次独立手算核为

`5271/100`、`105/2`、`5313/1600`。

例如 Dlarge 的 diag、同半 offdiag、跨半 offdiag 分别为 `5271/400,15771/1600,21/1000`，直接相加减即得上述谱。delta=1/100 时 M_beta−delta Dlarge 的三个 eigenvalues 是

`10729/10000`、`59/40`、`2687/160000`，全正。

独立稿的 E=CᵀA⁻¹C 是仅允许 pure-X degree-two 子空间时的精确 Schur 费用，谱为 `4932/125,15,453/1000`，较作者的 Dlarge 小；二者不是数值不一致。作者扩大空间要求更强，仍满足正性。完整 67 Gram 的 rank55 亦与独立稿的 12 个 null relations及55维正定 quotient 一致。作者报告 audit 直接消元的事实本次未代签；独立稿自己的 Fraction 消元已冻结。

## 3. formal kernel 负平方与所有 extension 不存在

作者 §4 的 `2/[4·3] L[Y(4ΣXi−S²)]` 与独立稿展开是同一表达式，精确值 −1/150。Q 的度数二，平方只到四。

所有 extension 不存在的作者证明使用 S4 平均；独立稿用任意 extension 的 Gram 差。作者平均保留一热方程、head full row laws、PSD 和全部 aggregate 矩。对 i≠j，原 same-token 不同heads 的 null 排除重复 token 项；token对称性再将12个异标签项均分，因此 `Lhat(Yx_1i x_2j)=L(YXiXj)/12`。对同head的异 token 项，原 head row 二阶零加 M2/Boolean 使其 quadratic monomial null，乘 Y 后仍零。故平均 extension 中 Q 的负平方确实被 aggregate 矩强迫，不只是强迫一个随意 kernel。

独立稿的必要 block 证明不需平均，两法同样排除任何保持整个给定 aggregate point 的原 token M2 extension。两者均没有声称同一个普通输入上所有其它 aggregate points 都不可延拓。

## 4. Proof 额外 ordinary context 与多 context 口径

§5 的示例有13台机器、6枚 jobs、48个 finite ends：g一个端，4枚 f各11端，y三个端。root 的 f homes 总1/2加 y home1/2，合1；target1时 g 已占1，五枚其它 jobs全离开root。一份完整调度是四 f 去四个互异 z、y去y0，负荷1，且g给 OPT≥1，所以 OPT=1。该例的 no-extension 仅针对给出的 erased aggregate point；作者已明确它不是 native integrality gap。此处只是解析核矩阵计数与完整调度，没有新运行，也没有把 identity-erased rows 冒充 original-job CONFIG/M2 可行点。

§6 式 (8) 的同一 Boolean Y 必要 PSD block 无歧义，与 Exact (D) 完全相同。

§6 式 (9) 提到 distinct linear contexts Z,Z' 时，准确有效对象是以 `(head i,context Z)` 为索引的**整体** conditional-contrast Gram；所显示式子给其 Z,Z' cross-block。不能把任意固定 Z≠Z' 的 i×j 交叉矩阵单独称为 PSD，例如 Z'=−Z 将同-context正块取负。原式 (9) 没有单独写 PSD 符号，我按这个整体 Gram 含义理解；后续若引用须显式保留整体索引，避免把 cross-block 误写成独立 PSD 条件。这不影响 Exact 的 (A)–(D)。

## 5. 运行与冻结来源

自己的独立代码及输出完整路径、hash 为：

* `/workspace/scratch/038d9dcc4cac/sol_true_hardness_token_label_lift_exact_first_audit.py`，`01de46cee0e87f0cd19edb2b6bc2cab25501ee106c8d9100c5a631f6dc651497`。
* `/workspace/scratch/038d9dcc4cac/sol_true_hardness_token_label_lift_exact_first_audit_output.json`，`b3496538d7bf399ea6000838919dca9cfe855c3c3064eb3f2ba3870c053c068a`。

仅标准库，无本地互 import；本读后未读或重放作者 code。数学 read-after 不替代 root 实际全文代码审读与独立新目录重放。原 Exact-first 及 audit 字节保持不改，没有 repo/Work/Git/凭据操作。

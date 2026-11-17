# 价格边范围补判：完整标签域的条件转移与集合域的价格存在性必须拆分

任务：`customer-attraction-3a-3a-ca44cde7e1f709dd`。内部检查：`CAG-WALLET-KERNEL-CHECK`。本补充仅重判 `cag-ca44-universal-price-and-root-wallet-transfer`，不修改既有 `review.md`、`reading-ledger.json`、原 staging 边、共享 clone 或 registry。

**结论：应按 Root 所提方向拆分。原 ALL 边的公式推导正确，但其整体条件与结论不能覆盖 M-c53 v2 的全部模型域和“任意给定有效 λ”量词，因此不应继续标为该目标的 whole_result。**

此前独立 review 把“在真实集合子模型、HALF(n) 下得到完整转移公式”评价为这条 ALL 边支付目标 whole，范围判定不够严格。这一评价在本补充中撤回。公式本身没有被推翻；更正的是源到既有目标的全域/全量词覆盖判定。

## 1. 对照的现行原句

重新完整读取了现行 registry 中以下三个端点及原 staging 价格边：

| 对象 | 精确承重范围 |
| --- | --- |
| `M-c53fb7d0b92a42f9932d5d637d6a97ba` v2 | model 为有限非空共同**标签**目录；quantifiers 为“任意原 m 人 SPE 及真实根主题 T；任意满足 UP 合同的同一人数统一 λ”。目标是条件转移，不要求另证 λ 存在。 |
| `customer-attraction/one-root-wallet-for-terminal-BR-normalization-and-true-price-transfer` v1 | 全标签域、每一完整纯 SPE、所有合法根主题、任意删后末位 BR；给 `0≤ℓ_T≤P_T` 及一次实际根预算。 |
| `customer-attraction/universal-signed-credible-defect-price-equivalence` v2 | quantifiers 明确限有限共同**真实集合**目录；HALF(n) 当且仅当存在只依 n 的非负统一实价，证明依赖可唯一读回坐标的 Cartesian 目录。 |
| 原 ALL staging 边 | conditions 先全局限制覆盖映射单射、真实集合目录，再给开放 HALF(n) 或“显式给定任一满足 UP 的 λ”；scope 也明确只是真实集合子模型。whole_result 后句虽写“更一般给定任一满足 UP 的 λ，同样转移直接成立”，没有解除上述全局域限制。 |

原目标正文以及价格等价正文、作者原稿和完整独审已经在先前独立窄审中全文读取，详见原 reading ledger。本轮不把这次端点重读写成又一次全文源读取，也不新增科学计算。

## 2. 形式量词揭示两个不同命题

令 \(\mathcal L_m\) 为全部 m 人有限标签目录实例；令 \(\mathcal S_m\subsetneq\mathcal L_m\) 为覆盖映射单射的真实集合目录子域。令

\[
\operatorname{UP}_{\mathcal D}(n,\lambda)
:\Longleftrightarrow
\lambda\ge0\ \text{且}\quad
\forall G\in\mathcal D_n\ \forall z\text{（末位 BR 目标）},\quad
2W_G(z)-OPT_n(G)+\lambda\cdot g_G(z)\ge0.
\]

再令 \(\operatorname{TR}(G,\sigma,T,B;\lambda)\) 表示目标的完整身份及不等式：

\[
F_\lambda(q_T^+)-F_\lambda(q_T)
=2\ell_T+\sum_{j<n}(2-\lambda_j)\Delta_j,
\]
\[
OPT_n\le2W(q_T)+\sum_{j<n}\lambda_jg_j(T)+2P_T+\Omega_\lambda(T).
\]

M-c53 v2 的完整条件命题应按下式判读：对每个 \(n=m-1\ge2\)，

\[
\boxed{
\forall\lambda\in\mathbb R_+^{n-1},\quad
\operatorname{UP}_{\mathcal L}(n,\lambda)
\Longrightarrow
\forall G\in\mathcal L_m\ \forall\sigma\ \forall T\ \forall B_T\in BR_0(H_T),
\ \operatorname{TR}(G,\sigma,T,B_T;\lambda).
}
\tag{T-L}
\]

这里只要求对每个给定、确实满足 UP 的 λ 证明转移。即使尚未知道是否存在全标签域的 UP 价格，条件定理仍可以通过固定任意这样的 λ 来证明。证明条件定理无需把价存在性当成开放输入。

统一价等价源给出的则是

\[
\operatorname{HALF}_{\mathcal S}(n)
\Longrightarrow
\exists\lambda\in\mathbb R_+^{n-1},\quad
\operatorname{UP}_{\mathcal S}(n,\lambda),\qquad
\sum_j\lambda_j\le2n-1.
\tag{E-S}
\]

与根钱包和转移代数共同使用后，得到

\[
\boxed{
\operatorname{HALF}_{\mathcal S}(n)
\Longrightarrow
\exists\lambda\bigg[
\operatorname{UP}_{\mathcal S}(n,\lambda),\ \sum_j\lambda_j\le2n-1,
\ \forall G\in\mathcal S_m\ \forall\sigma,T,B_T,
\operatorname{TR}(G,\sigma,T,B_T;\lambda)
\bigg].
}
\tag{C-S}
\]

这是有用的集合子域存在性供给与转移结论，但它不是 (T-L)：

- **模型域不同。** \(\mathcal S_m\) 中的所有实例不等于 \(\mathcal L_m\) 中的所有实例。不能靠 CAG-MODEL 的共同名称或覆盖收益只依计数，就免费商掉同覆盖异标签和历史依赖续局。
- **价格量词不同。** 在 HALF 前提下供给某个 λ，不等于证明目标对任意给定有效 λ 的整个条件定理。存在性供给中的 λ 也只确证 UP\(_\mathcal S\)，没有确证其为目标完整 UP\(_\mathcal L\) 合同的见证。
- **额外 HALF 前提不同。** (T-L) 的前提是给定的 λ 满足 UP；目标没有要求另有 HALF\(_\mathcal S\)，也没有要求 λ 由等价源的分离构造产生。

即使原边的“或者显式给定 λ”在集合域内被理解为覆盖该域所有有效 λ，它也至多补出集合域版本的任意 λ 转移，仍未覆盖全标签域。(C-S) 的存在性分支尤其不能自行支付 (T-L)。

## 3. 钱包单源加显式 UP 可以证明目标整个域

固定任意 \(G\in\mathcal L_m\)、原完整纯 SPE σ、真实根标签 T、同一人数任意 \(\lambda\ge0\)，并假设目标的 UP 合同。所有标签及其精确有序历史保留，不作覆盖合并。

原策略在 T 后的真实叶是 \((T,H_T,A_T)\)。删去根提供者、保留原客户及共同标签目录，定义 \(q_T=(H_T,A_T)\)；固定 H_T 取任意删后末位 BR \(B_T\)，得 \(q_T^+=(H_T,B_T)\)。同覆盖异标签可以产生不同 H_T，这里对每个真实标签 T 分别处理，不将这些叶合并。

原根钱包源的两次末位 BR 论证在该完整标签域中给

\[
0\le\ell_T=f_0(B_T)-f_0(A_T)\le P_T.
\tag{W}
\]

q 与 q⁺ 在每个 \(j<n\) 的精确有序前缀完全相同，删后 n 人实例、标签目录和客户也相同，因此真正完整孩子 SPE 的集合以及相应 min-max 门槛 \(M_j\) 原样不变。这里无需标签覆盖单射；也不要求将原 σ 先变成删后完整 SPE，因为 UP 本来量化任意末位 BR profile。

令 \(\Delta_j=u_j(q^+)-u_j(q)\)，利用 \(W=\sum_i u_i\)，直接得到

\[
F_\lambda(q^+)-F_\lambda(q)
=2\ell_T+\sum_{j<n}(2-\lambda_j)\Delta_j
=2\ell_T+\Omega_\lambda(T).
\tag{I}
\]

由显式给定的 UP，q⁺ 是其适用目标，所以 \(F_\lambda(q^+)\ge0\)。结合 (I)、(W)，便得目标全部不等式。每个步骤均对任意给定有效 λ、任意原标签实例及任意真实根标签成立。这正好证明 (T-L)。不需要 HALF(n)，不需要真实集合目录单射，也不需要 \(\sum\lambda\le2n-1\) 或 λ 为有理数/全 2。

统一价等价源没有参与这段给定 UP 后的代数推导。其数学作用是给价存在性；不能因此将它列为证明 (T-L) 的必要 ALL 前提，并称两来源“不能拆成各自足够”。准确说法应是：**钱包源加目标原有的显式 UP 合同足以得到完整条件转移；等价源另给集合子域内的条件价存在性。** 钱包源本身仍不声称存在 UP 价格。

## 4. 建议拆分后的两条关系

以下是供 fresh worker 参考的语义规格，不是新增登记或已绑定的边。

### A. 根钱包单源 → M-c53 v2：完整条件 whole

**source：** `customer-attraction/one-root-wallet-for-terminal-BR-normalization-and-true-price-transfer`。

**target：** `M-c53fb7d0b92a42f9932d5d637d6a97ba` v2。

**conditions：** 原完整标签模型；\(n=m-1\ge2\)；给定任意同一人数 \(\lambda\in\mathbb R_+^{n-1}\)，满足目标精确 UP 合同；固定删根后的 H_T，仅将末位 A_T 改成任意 B_T∈BR₀(H_T)。不添加集合域或 HALF 限制。

**whole_result 的建议内容：** 对全部原有限标签实例、每份完整纯 SPE、每个真实根标签和任意删后末位 BR，以及每个给定满足 UP 的统一 λ，完整成立 (I) 与目标 OPT_n 不等式。若引用任意根分布的一次预算，准确保持 \(2E_pP_T\le u_1\)，不将其扩为更早修复付款。

**证明输入：** 钱包源给 ℓ≤P；同一前缀保持真正 M 不变及利润守恒给身份；显式 UP 只在 q⁺ 使用。三者在全标签域成立，故支付目标全部模型域及全部条件量词。

### B. ALL{统一价等价，根钱包} → M-c53 v2：集合子域的价存在性贡献

**conditions：** 覆盖映射单射的真实集合目录子模型；\(n=m-1\ge2\)；开放输入 HALF\(_\mathcal S\)(n)。删除原边中混在此处的“或者任意给定 UP λ”分支，避免再次混合两种任务。

**contribution.result 的建议内容：** HALF\(_\mathcal S\)(n) 经等价源供给只依 n 的某个统一实非负价 λ，满足 UP\(_\mathcal S\)，可取总价≤2n−1；同一 λ 对全部原集合实例、原完整纯 SPE、真实根主题及任意删后末位 BR，满足目标的两条转移公式。其数学内容是 (C-S)。这应称为“目标转移公式的集合子域版本及该子域的价格供给”，而不是已经实例化完整标签域的 UP 合同。

**contribution.remaining 的建议内容：** 该存在性分支没有证明标签别名模型中的 UP\(_\mathcal L\) 价存在性；其集合域 witness 未被证明满足 UP\(_\mathcal L\)。它也不承担目标对任意给定 UP\(_\mathcal L\) λ 的全标签条件转移；后者已由关系 A 的完整证明单独支付。这里保留的是 B 关系自身的范围不足，不是宣称整个数学任务还缺这项代数证明。

不应为使 B 继续保持 whole 而缩写、改版或重注册 M-c53，使目标反过来迁就当前源边的窄域。既有目标的宽模型与任意给定 λ 量词本来就有正确完整证明；应让 A 承接 whole，让 B 准确保留有用贡献。

## 5. 为什么不能原样保留 ALL whole

纯命题逻辑中，给一份真正覆盖全标签、任意给定 UP λ 的证明，再把无用的价格等价命题额外加进前提，仍能推出目标。但这不能补救当前边：当前整体条件仍限制集合域，而且 explanation 将“两源不可拆”作为理由，未陈述全标签 generic-λ 分支。

若彻底改写原边，使其一支显式为完整 (T-L)，另一支为 (C-S)，从纯逻辑上可把完整目标归给含冗余前提的 ALL。然而那只是把根钱包单源 whole 藏进一个额外价格源不参与的分支，掩盖源作用与量词差异。按“whole 必须支付目标整个域/量词、只创建有解释的有用关系”的要求，拆分 A/B 最准确。

因此最终判定是：**原 ALL 在其声明子域内的数学推导成立，但按现行 M-c53 v2 完整目标应降为 contribution；根钱包单源加显式 UP 合同可获得全域完整条件 whole。** 该判定取代前一独立 review 对这条价格 ALL 的 whole 范围评价，其它 COMMON/PUSH/QUERY 结论不受影响。

## 6. 本补充读取与执行账

本轮完整重读：现行 registry 的上述三条完整对象记录，以及原 staging 的 `universal-price-and-root-wallet-transfer.json`。已使用的原根钱包正文、价格等价正文、作者统一价格稿及独审全文，在先前 ledger 中均有全文实读记录；本轮未再次宣称逐文重读。未读取新的 PDF、凭据或历史数值向量，未运行科学脚本、LP、SPE 枚举、Git、work/registry/bind，也未修改旧两审查文件。唯一新增交付是本补充。

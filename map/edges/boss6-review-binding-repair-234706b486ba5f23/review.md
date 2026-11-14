# 共同真实回复的严格投影层级复核

## 原批资产与复核范围

本批替代任务 customer-attraction-3a-3a-11c0fae95913e6f4 对核心对象 M-b1b4276f0ec747ed8c347bda65c9e0af 的交付。核心为登记版本 2，pin 为 8022368eb10c10d6e8989de8ec4702b581017b911828dc64bb96bdb1a251f0f5。原任务账本为旧路径 review.md 记录的 SHA-256 是 0665b5c598714e8ecc99edf663d57cb68f2e6ba1165f55456bc93550a3486ff3。该路径现行 SHA-256 为 6583ee42f8cac888a3f42529a6ee6180c729858f79a7a3d314bb2af2b88f823a，和仓库旧路径的独立收据一致。Boss6 在 cdce4e66b 已保全此差异。本页替换账本中过期的审查资产。另两项资产的当前字节与原账本一致，沿用原数学边和 SHA-256。[原任务账本](../../../research/operations/map-v2/tasks/customer-attraction-3a-3a-11c0fae95913e6f4.json) · [旧路径收据](../../receipts/customer-attraction-3a-3a-11c0fae95913e6f4.json) · [Boss6 失配清单](../../../research/workspaces/map-v2/Boss6/current-run/runtime-recovery/stale-review-bindings/discovery.json)

旧任务 45 项和修复任务 212 项声明的证据引用，文件均存在且逐字节 SHA-256 匹配。本轮数学复核读取共同模型、核心引理、同源强 PAIR 的承重推导、有限计算对象的 624 部分、三组严格性证明、证书与独立核验。212 项的其余附证用于只读端点的身份核对。[修复任务定义](../../../research/operations/map-v2/tasks/boss6-review-binding-repair-234706b486ba5f23.json)

## 真实历史和共享提升

对任意有限单位客户、有限非空共同标签目录和完整有序历史纯 SPE，逐一量化每位提供者、其所有合法有序历史及每个合法偏离标签。每次比较都沿同一完整策略的真实后继。弱平局、重复选择、同覆盖异标签、空覆盖和零客户均保留。固定 actual 路径 \(A_1,\ldots,A_6\) 的第四源及第一类非对角轨道 \(e=(i,j)\)。原真实末节点为 \(R_{ij}=\sigma_6(A_1,A_2,A_3,T_i,B_j)\) 和 \(Z_{ij}=\sigma_6(A_1,A_2,A_3,A_4,R_{ij})\)。在 actual 第四源强制 \(T=R_{ij}\)，读真末对 \(B,C\)。回到同一有序源强制这个 \(C\)，读真末对 \(J,V\)。对每位客户使用一组 \(h=(b,c,j,v)\in\{0,1\}^4\)，两处 \(C\) 共享同一 \(c\)。\(p=\sum_{a=1}^3 1_{A_a}\)、\(\ell=\sum_{a=1}^5 1_{A_a}\)，两枝末对背景为 \(p+t,p+c\)。源两条 IC 的预算都是同一个 actual \(u_4\)，合权时只按其源权总和支付。\(u_4,u_6\) 由同一份 actual 六位可见质量给出，\(K\) 上界所用主题的容量。[完整历史模型](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md) · [核心引理，第 1–3 节](../../../archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md)

17 个查询为 \(A_1,\ldots,A_6,T_i,B_i,C_i,T_j,B_j,C_j,R_e,Z_e,\overline T_L,\overline B_L,\overline C_L\)，\(L=\{1,\ldots,6\}\setminus\{i,j\}\)。后三项是在合法纯主题上均匀查询。强 PAIR 来自真倒二偏离、偏离后真末回复对固定查询的 IC、原真末回复对该偏离后继的 IC，再加非负交叠余量。查询对平均时成本中的 \(xy\) 使用 \(\mathbb E[xy]\)，联合索引分布对全部客户共同固定。同索引自配对用 \(\mathbb E[x]\)。对剩余菜单两个不同族，same 为同索引二阶矩 \(\mu_{fg}\)，off 为 \((4\bar q_f\bar q_g-\mu_{fg})/3\)。可见型细化后，旧提升按同一粗型下的条件质量比例细分，各型质量和旧预算保持。查询对 PAIR 与其两个对角 PAIR 平均的差为 \(\tfrac12\mathbb E[(x-y)^2]/[(\beta+1)(\beta+2)]\)，在第一枝背景 \(\beta=p+t\) 可见时，该差可直接提出共同 min。[同源双末对，第 1–4 节](../../../archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md) · [核心引理，第 2、3、6 节](../../../archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md)

| 投影 | 对固定可见质量所要求的隐藏提升 |
| --- | --- |
| \(\bigcap_{l=0}^{16}\mathcal P_{76,l}\) | 对每个 \(Q_l\) 分别存在一份提升，各满足该查询的 34 基础行和两枝 42 条强 PAIR。 |
| \(\mathcal P_{332}\) | 存在一份提升同时满足 60 条查询无关行及每个 \(Q_l\) 的 16 条新增行。 |
| \(\mathcal P_{616}\) | 同一份提升再满足两枝共 284 条旧查询对 PAIR 行。 |
| \(\mathcal P_{624}\) | 同一份提升再满足原 \(R,Z\) 末位节点各对四个宏主题的零预算 IC。查询代价用各自原背景 \(p+t_i+b_j\) 和 \(p+a_4+r\)，这里 \(r\) 是客户的 \(R\) 会员。 |

624 和 616 逐级删行得前两个非严格包含。332 的一份共同提升限制到每个 \(Q_l\) 就给出交集所需的 17 份 76 提升。固定质量 \(m_v\) 后，隐藏提升域为各型 16 态质量单纯形的有限积，其成本像加非负正交锥为闭凸上集。若预算不属于此集，存在非负法向严格分离，分离下界按各型独立取 \(\sum_v m_v\min_h\sum_\alpha\lambda_\alpha E_\alpha(v,h)\)。故一份共同提升存在，当且仅当对所有 \(\lambda\ge0\) 加权预算均不小于该下界，其中允许源权总和为零。[核心引理，第 8–9 节](../../../archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md)

## 三道严格包含的有理见证

三份点均比较 actual 第四源、强制 \(R\)、第一类非对角轨道和同一 17 菜单。共同细化域 \(\mathcal D_{17}\) 在原 16 个直方图型上添加下文 \(H_*\)，允许合法 \(R/Z\) 四态，保实际收益与可见质量的关联。

| 严格包含 | 大集可行性证书 | 小集分隔证书 | 见证支撑 |
| --- | --- | --- | --- |
| \(\mathcal P_{332}\subsetneq\bigcap_l\mathcal P_{76,l}\) | 5744 点有 17 份非负有理提升，均保持同一实际收益与可见质量。\(17\cdot76=1292\) 条预算最小余量为零。 | 23 个整数权对同一隐藏提升合账，预算 \(500u_4+143u_6+19K\)。完整 4,849 坐标重建后，按源权归一余量约 \(-0.0003136089403967234\)。 | 原 16-hist，\(H_*\) 质量为零。 |
| \(\mathcal P_{616}\subsetneq\mathcal P_{332}\) | 5775 点的一份共同提升在 56 个正可见型上有 79 个非零有理隐藏原子，匹配质量并通过全部 332 行，最小余量为零。 | 12 个整数权给预算 \(413u_4+164u_6+14K\)，唯一新增行是第一枝 \(\mathrm{PAIR}(T_i,B_j)\)，权 48。按源权归一余量约 \(-0.0006503689544503674\)。逐型差额公式另核 192 组 min 和 3,072 个逐隐藏恒等式。 | 原 16-hist，\(H_*\) 质量为零。 |
| \(\mathcal P_{624}\subsetneq\mathcal P_{616}\) | 5799 加 \(H_*\) 后有 57 个正可见型和 77 个非零有理隐藏原子，满足 616 条预算、质量等式、actual 收益关联及全部 17 查询的 actual 末价与容量，最小余量为零。 | 16 个整数权给预算 \(10^7u_4+3862317u_6+331490K\)，唯一新增方向是原 \(Z\) 查询宏 \(V\)，权 54,741。补齐后的同点精确归一余量约 \(-0.0000012925490402391834\)。 | \(\mathcal D_{17}\)，\(H_*\) 质量严格为正。 |

5744 分数见 Main 报告的 integer_scale_slack，归一值须再除以 500。5775 的归一分数见 new_negative_slack，并与跨查询 4,849 列独立重建的同一行完全相符。原 5799 点已违反 616。先在暂时放宽至 \(u_4+\delta\) 的源预算下恢复完整 616 提升，再补质量 \(6\delta\) 的确定型 \(H_*\)，其 actual 六位为 \((0,0,0,1,0,1)\)，六个旧词皆为 \(111\)，\(R=Z=1\)，宏隐藏四位全为 1。新实际 \(u_4,u_6\) 各增加 \(3\delta\)，\(K\) 增加 \(6\delta\)。两源成本各增加 \(2\delta\)，各付清原缺额 \(\delta\)，其他预算足额。新分隔方向在 \(H_*\) 上的归一单位余量为 \(1/6\)，故新点总余量为原 5799 分隔余量加 \(\delta\)，精确为

\[
-\frac{148845568998121138356228513900153618711355035474766353741403675003844902443555714733}
{115156612526343742805335876528460013730045769206455070181965993000919799549825285360000000}<0.
\]

五份冻结验证器已只读重放，除运行秒数外，输出与各自保存报告一致。三份有理点给出同一 \(\mathcal D_{17}\) 上
\[
\mathcal P_{624}\subsetneq\mathcal P_{616}\subsetneq\mathcal P_{332}
\subsetneq\bigcap_{l=0}^{16}\mathcal P_{76,l}.
\]
原 16-hist 上 \(\mathcal P_{624}\subsetneq\mathcal P_{616}\) 仍待独立见证。[5744 逐查询报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_single_lifts_5744.json) · [5744 500 权报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_portfolio_500.json) · [5775 共同提升报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_332_lift_5775.json) · [5775 跨查询报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_cross_pairs_5775.json) · [5799 补齐报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_reverse_terminal_strictness_v1.json)

## 两条关系与剩余义务

- boss2-six-cross-shared-pair-to-query-hierarchy 的源 M-e 提供两枝 34 预算及强 PAIR 的合法性和共享 \(C\) 的先合账再取 min。目标 M-b 用其支付 76/332/616 行、两个非严格包含及共同可见细化。原 3B 比较已由该贡献边与目标三道独立见证闭合。Boss6 保存的 parent_math_check.py 本轮只读重放与报告逐字节一致，核对三 IC 恒等式、含原倒二主题的 PAIR 冗余及对称差。其 13 原子和 \(-90896/19269\) 负余量承担 M-e 自己的旧 34 行分隔。三道层级严格性由上节各自的证书支付。[原贡献边](../customer-attraction-boss2-six-cross-20261111/boss2-six-cross-shared-pair-to-query-hierarchy.json) · [Boss6 算术报告](../../../research/workspaces/map-v2/Boss6/current-run/runtime-recovery/stale-review-bindings/parent-math-check.json)
- boss2-six-cross-complete624-projection-pays-lift 把 M-b 的共同提升语义接入 M-ddce 的固定 16-hist 有限必要矩阵。78 个词对组的四个旧 \(R/Z\) 状态各接 16 态，共加 4,992 个非负列。312 条质量等式写成正反 624 行，再加 624 条原预算，使 \(11418\times7639\) ZZ 基底变成 \(12666\times12631\)。保留原行列前缀、零质量型、零源权面，原归一和目标在新列为零，索引重数只乘一次。有限表示核验已只读重放，3,115,008 个系数、1,920 个字面查询和 247 个零 \(R/Z\) 边缘均通过，除运行秒数外与冻结报告一致。该有限优化的 \(W\approx0.49265618211149476\) 由计算对象另附的 929 正原始列及 516 正对偶项认证，\(O=1\)、\(1-2W>0\)。该矩阵限原 16-hist，补齐型 \(H_*\) 用于上节的扩域分隔。[原贡献边](../customer-attraction-boss2-six-cross-20261111/boss2-six-cross-complete624-projection-pays-lift.json) · [有限表示合同](../../../research/workspaces/six-boss2-20261111-cross/joint_requery/complete624_actual4_R00_v1_contract.md) · [有限表示报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_complete624_v1.json) · [有限最优性报告](../../../research/workspaces/six-boss2-20261111-cross/main_verify_complete624_opt_v2.json)

研究前沿仍包括其他源、其他 \(R/Z\) 结构及不同旧组的共同客户会员，整份共同目录在全部有序历史上的策略一致性，以及六人全域 \(2W\ge\mathrm{OPT}_6\) 的共同付款或完整反例。当前有理见证只证明所列局部投影的强弱。指定十二标签的全 SPE 排除及其局部新题付款缺口由 M-ddce 的独立正文承担。[有限计算与固定目录结果](../../../archives/customer-attraction/subarchives/six-providers/state/计算/同源跨枝增强必要图的精确最优值与半界缺口--计算.md)

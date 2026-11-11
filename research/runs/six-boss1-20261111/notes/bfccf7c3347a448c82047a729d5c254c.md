# 共同 max-B 必要行增广：完整 20911 × 20585 系统

状态：**working；装配与独立精确结构审计 PASS，准备交 Main 唯一 Actions 发现。** 本目录只研究原固定 16hist 必要 LP 增加一条普遍合法 max-B 行后的最优值，尚未得到新精确最优。原六人共同有限非空目录、单位客户、全部有序历史纯 SPE 的 `2W ≥ OPT6` 义务仍 **OPEN**。

## 1. 冻结输入及新增行

已实读 `full624_augmented_lp/recovery_report.md`、`terminal_response_cycles/max_b_lift.py`、`max_b_certify.py`、`max_b_audit.py` 及其证书/独立报告；也实读原 owner `customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints` 的完整正文，包括共同目录 F 的 RC 证明及 β 的合法端点。Main 已另从 hist 描述符和通用 κ 公式独立复核本行。

旧父引理在固定 actual 前四的真实两人子局，以全目录最大潜力主题 X 取得同一个 `F=B_X`。它保证 `u5 ≥ U(Q,X)` 对全部合法查询 Q，以及 `B_Q+B_R−J_QR ≤ u5+B_X` 对全部合法主题对；结合实际末位查询 X 和 `|X|≤K` 可以把同一 X 的客户会员位消去。这里复用旧父引理，未把 max-B 机制认作新定理。

| 冻结资产 | SHA256 |
|---|---|
| 旧完整矩阵 `full624_augmented_lp/recovery/exact_matrix.json.gz` | `96388092e21621f157b4428ce99f98b93afa99ed3a0c12c72b1d6475c26fba30` |
| 旧精确点 `full624_augmented_lp/recovery/augmented_lp_exact.json` | `cb45ee6f8df153764c91bd77d0543527cc44719ff7cc43646ffce06a7921a932` |
| 旧对偶 `full624_augmented_lp/recovery/exact_dual_certificate.json` | `22381bc9844aa5452b45a5bd8ef4a6148808388455b80666b49475df0f7377b3` |
| 新 cut `terminal_response_cycles/max_b_exact_certificate.json` | `f6189600d6ccccdbd9fcbc4ae4af9e768c9382af8de1ae41d6e6a7ee7662f664` |

新行取证书字段 `sparse_original4849_row_K_normalized`，以 `row·x ≥ 0` 追加为从零起算的第 **20910** 行。K 系数为 1，恰有 17 个非零系数，分别位于 K 及全部 16 个 hist；剩余 15736 列系数均为 0。`maxb_cut_mapping.json` 逐项保存原描述符、系数、旧权和旧点贡献。没有把该点的行值变成任何常数 RHS。

独立重建使用每个 hist 的 actual 六位、前四覆盖数 `p`，以及六个菜单词中的 `dB,dC,dBC`。令 `D=(p+1)(p+2)`，`u=a5/(p+a5+a6)`、`v=a6/(p+a5+a6)`，分子为零的收益按零解释；定义

\[
\kappa=\frac{12a_6+24a_5+6d_C-(p+2)(p+9)}{D}.
\]

该 hist 的行系数为

\[
64u+24v-\frac{12a_6}{p+1}
-\frac{8d_B+26d_C}{3(p+1)}
+\frac{8d_{BC}}{3D}+\max(0,\kappa).
\]

这从同一个 X 的四种合法钱包与容量预算非负组合取得，并用逐客户 `max(0,κ)−κ·1_X ≥ 0` 消元。证书的十条非负 LP 行与五条非负新变量项是该组合在所选 16hist 上的显式实现。构造本增广不依赖旧点权重，故是通用必要行。

## 2. 完整装配及独立核验

`assemble.py` 直接读取冻结旧完整矩阵，只追加上述一行。全部旧 **20910** 行、名称、**20585** 个列描述符、目标与归一向量逐项相同；旧浮点 CSR 数据、列索引、行指针、行缩放前缀亦逐数组相等。完整非零元数由 3208797 增至 **3208814**。

所有 10744 旧辅助列、4992 共享624隐藏列、312 个共享边缘块、原 16hist 全保留。旧点的六个零 hist 为列 `1,59,366,449,524,574`，这些 hist 及其全部隐藏态均未删去。312 对正反边缘行也逐项保留。

`verify_certificates.py --structure-only` 不导入装配、恢复、max-B lift 或数值库。它独立检查全部矩阵域、完整旧行列不变、由 hist 重建新行、3360 个完整 Boolean/菜单计数组合的投影恒等式，重新核旧点全部20910行，以及旧点的7954个规范 max 和2790个规范 min。全部 PASS。

| 新资产 | SHA256 |
|---|---|
| `maxb_augmented_lp/exact_matrix.json.gz` | `b2ef1da774412ac42a951931914afcd31fd917ef261fd28d2e7b5072ed125682` |
| `maxb_augmented_lp/floating_problem.npz` | `c4cb94bb1587392f1d6587eefbc1ee092ad4ca348c756a199aa15caa4263f1c9` |

完整输入 SHA 清单在 `inputs_manifest.json`，结构报告在 `assembly_verification.json` 和 `structure_and_lower_verification.json`。所有文件均在本新目录内写入，旧冻结资产未改。

## 3. 目前精确可证的结论

旧完整对偶在新增行取权 0，其20585个残差逐项保持不变且非负。因此增广系统仍有精确下界

`W9 = 18544018235046858814466929845378235903447304630529981018163179757013933898399 / 37610930738552016886760210756472139042422876797320439967207958074168853634165`，约 `0.49304863960834766`。

旧点对新行的值为

`−4426145324455836398818752701603934797071201573118130939132148836781341509474 / 37610930738552016886760210756472139042422876797320439967207958074168853634165`，约 `−0.11768241938025059`。

因此旧 cb45 点不可行，但**尚未证明整个旧 W9 最优面被排除**。需要新系统的匹配有理原始/对偶，或其他完整精确证据，才能声称最优值提高。也未从这个有限必要 LP 得出全历史 SPE 的可实现性或反例。

## 4. 唯一 Actions 发现与后续恢复合同

`actions_solve.py` 为自包含 runner，只依赖标准库、NumPy、SciPy；默认只核输入，必须实际 Actions 标志才允许 `--execute`。Main 建请求和 push，本代理不操作 Git、RUN、registry 或凭据。

计划为一次 `highs-ds`、solver 上限1800秒、job40分钟，完整求解20911×20585系统。输入文件由 `runtime_inputs_manifest.json` 和 `actions_request.json` 逐一绑定；默认输入核验还把浮点 CSR 的每个系数和缩放与精确矩阵重算匹配。失败不自动重跑。

每次实际运行保完整 x、行/归一/上下界 marginals 及 residuals、未缩放行乘子、重算的行余量与对偶残差、数组存在性、solver 状态、输入 SHA、实际执行源码、stdout/stderr、退出码和失败记录。若 solver 无解向量，仍保正确维度的 NaN 数组和明确状态，不伪造原始证书。

数值数组返回后，复制到本目录独立 recovery 子目录，使用已复制并改为本地依赖的 `recover.py`。先按实际数值目标判断是否需要 sameW 活动面恢复；自由 W 恢复只用于不匹配或确有记录的 sameW 失败。每次失败均保方程、支持、traceback，不把活动面失败当整个最优面不可达。恢复过程不调用优化器。

最终必须以全部20911行、20585列、归一、目标、原始/对偶非负、互补性和全部10744规范辅助量的独立精确核验为结论门槛。若不能恢复，保实际输入/输出和当前精确下界，不冒称数值最优就是精确最优。本数学义务仍在工作中。

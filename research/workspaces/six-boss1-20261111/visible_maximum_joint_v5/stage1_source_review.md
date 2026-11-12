# STAGE1_SOURCE_REVIEW_ONLY

Boss1；RUN `six-boss1-20261111`；实现席 `visible_joint_v5_prepare`。本页记录已读的准确来源及 v5 准备接口。**第一阶段只准备代码和既知来源合同，优化器调用为 0；未生成或冻结 `exact_input.json`。最终总行数尚未确定。**

## 1. 原模型及本次承接边界

已实读[共同目录完整历史模型](../../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)，SHA256 为 `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`。模型是有限单位客户、有限非空共同**标签**目录、恰六人和任意给定完整有序历史纯 SPE；保留空覆盖、重复行动、同覆盖不同标签以及所有弱平局。原目标是所有该类 SPE 满足 `2W >= OPT6`。

源 IC 必须使用原实际源收益和相应强制标签后的真实续局收益。内部 SAFE 必须使用同一真实分支中该内部源的真实前缀及偏离后的真实后继。查询并 O 仅是六个真实合法查询的覆盖并，不能视作一个合成合法行动。有限客户逐个相加后得到的非负实数原子矩阵只提供必要条件；锥点没有 SPE 充分性含义。

Main 已说明 v4 的 1586 行完整输入恰被消费过一次；旧冻结文件中的 `UNRELEASED_INPUT` 是当时的准备记录，不解释成今天可以重求旧系统。v5 代码无求解入口，不读取任何 primal/dual/候选点文件，不绑定旧参数值或支持。

## 2. 已实读来源和固定身份

| 来源 | 本阶段读取内容 | SHA256 |
| --- | --- | --- |
| `visible_maximum_joint_v4/exact_input.json` | 全 1586 raw 行及完整矩阵元数据 | `fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839` |
| `visible_maximum_joint_v4/freeze_manifest.json` | 原准备身份和逐件工件记录 | `21da98ff5b72702363824200e25320fc7d510633be48d91de6e2eea5e708c337` |
| `visible_maximum_joint_v4/source_review.md` | 原模型量词、真实预算、尺度与等式边界 | `2143637bac4d41adf5fcbd0da375647742f0b8b3ccc1714565169d14705b2a1d` |
| `visible_maximum_joint_v4/check_literal.py` | 实际完整准备检查实现；旧包没有名为 `check_preparation.py` 的文件 | `28eb83fb133251b44598c64b882363a7cbb81ad382d619ac9273866a0967ba59` |
| `all_source_ordered_menu_cells/proof.md` | 完整连续来源、活跃 cell、有限生成与全索引量词 | `d5be7d17de3b3dd16ffd68b61a812127c94dd74e6e36ea9c9d8f80a639ca36d4` |
| `all_source_ordered_menu_cells/exact_family.json` | 全 181 行 | `f1bca409d9927f9721764a327f1fcd52a18c38f0968d9c240fa20288aa95eac3` |
| `all_source_ordered_menu_cells/freeze_manifest.json` | 最终冻结身份 | `313e3fe07138c1ecf0b42bd8fbafa4e4f334f583141f0a950eeb71bb09ad6430` |
| `source2_cap_coupled_internal_safe/proof.md` | 真付款、完整非乘积域和 C 自由等式符号 | `d7d2db3a6bfd84667e13fa82a335c2c1e8face2b07d7736c8277482c71f86eb9` |
| `source2_cap_coupled_internal_safe/exact_family.json` | 全 28 行 | `b5c950664a21da750245cb7115dc3a60721feb494ce7cf1e32771d5aeeba2906` |
| `source2_cap_coupled_internal_safe/freeze_manifest.json` | 最终冻结身份 | `a744e986913415ac964c6fc12dafa51a86f1982983b2a6fcd0507091bfaafd28` |
| `source2_minimal_cap_safe/proof.md` | Main 新授权读取的已冻 C-only 完整来源；最终 Main 审查待付 | `e0686cf9db0ab9611eea9852a2e56141e24d9011d124ec2a881a10c8dc5f48d6` |
| `source2_minimal_cap_safe/exact_family.json` | 全 28 行，未提升为已释放追加 | `dfdadf4dec0cc1b135cb015fc60ba92f2208a8678a02835003213faefdc3161f` |
| `source2_minimal_cap_safe/freeze_manifest.json` | 最终冻结身份，读取由 Main 单独授权 | `d63c117b0adf2353f70ffaf7d959dd91e8c4ee378838f7e5f4af6e99c86861ec` |

另已读 v4 `build_input.py`、`literal_check_result.json`、数值尺度、原列路由与行目录，以及 `main_visible_c_v4_preflight.py/.json` 的实际接口。原两族的坐标合同、完整源行、尺度及 Main 全来源检查记录，以及新授权只读的 frozen source2 minimal 文件，分别绑定到 `preparation_contract.json` 的 35 个直接批准文件 SHA。Main 已完成 ordered/coupled 两族的完整几何、真实付款和全列复核；source2 minimal 的 Main 最终复核仍待付。本阶段不重跑来源项目程序。

`main_cap_coupled_complete_check.json` 同时含来源复核和已知面的诊断字段。准备程序只绑定该记录的文件身份，不解析或利用任何面值来选择来源行；两族完整行数由最终来源及任务指定，始终为 181 与 28。传递来源链通过精确最终 manifest/source-pin 文件绑定，未打开其指向的任何候选或求解结果文件。

## 3. 原 1586 的字面继承合同

完整坐标仍为所有 `(a1,a2,a3,a4,a5,a6,x,o,c)` 的 512 个型和独立 K 列 512；513 列全部非负。目标为原实际覆盖 W，保留两条自由等式 `sum(o*z)=1` 与 `sum(c*z)-K=0`。原等式的稀疏字典与系数字符串、原目标字典、非负列集合、原列顺序均逐字继承。

1586 行的系数字典并非全都存满 513 项：既有稀疏省略零，也有显式零。生成器深复制原字典，不密化、不稀疏化、不约分重写字符串。原 `rhs=-1` 行有 30 条；零行 `SAFE_6_6` 位于 raw 索引 45，原空系数字典保留。旧冻结检查报告的全部重复行也随 1586 原行整体继承，重复统计仅供诊断。

旧 `numerical_scaling.json` 的 1586 个正尺度**字符串**逐项保留，原 raw 顺序不变。新行统一使用数值正除数 25，精确矩阵本身不作数值除法；实际源 IC 权可随参数变化，不替换该数值除数。

## 4. Ordered 的 181 行：完整 cell 顶点，原 K 付款

181 个合并参数点按来源原顺序分为 `119,40,16,6`，对应实际源 i=1,2,3,4。旧参数域经最大值活跃区域划为 14 个闭 cell，共 369 个顶点—cell 关联，所有交界平局保留。行系数在每个 cell 内仿射，故完整 cell 顶点非负等价于指定连续族非负。原 67 点不能凭旧顶点凸平均替代新增 114 点；本次 181 行一条不少，包括全部 119 个根源行。

设 `n=6-i`、`c_i=(n+1)/2`、`a=25+sum(theta)-s`，并令

\[
L=\max\!\left(0,\max_j\left\{\theta_j+\sum_{h>j}\frac{\theta_h}{5(7-h)(8-h)}-\frac25\right\}\right).
\]

精确行是

\[
a u_i+c_iK-\sum_x o_xG_i(p_x)\ge0,
\]

\[
G_i(p)=\frac16\left[c_i+\frac{24}{p+n+1}+\frac1{p+1}
-\frac{s}{\min(p+n+1,5)}+\sum_j\frac{\theta_j}{p+7-j}\right]
-\mathbf1_{p=0}\frac56L.
\]

同一六个真实查询作外层六平均，每个外索引内部仅排除该**索引**后作五平均；覆盖别名与重复标签不被排除。K 列仍为原 `c_i`，本族不使用 C 大小等式。末 BR 原均值权 1，数值除数 25。阶段一独立代码从上述公式重建 181×513 个系数及原尺度，完整几何和真隐藏态付款仍引用 Main 已冻结复核。

## 5. Coupled 的 28 行：先支付新增帽，再用一次 C 等式

该族只强制真正达到全目录最大裸大小 K 的合法标签 C；它是固定基底内部 SAFE 与中间帽联动的完整 11 面、28 顶点非乘积域。所有顶点按源文件原顺序保留，不以任何面值筛选。

设 `theta*= (12425/31104,175/432,5/12)`，`theta_j=theta*_j+e_j`；`Gamma_3=e_3+e_4/72+e_5/36`，`Gamma_4=e_4+e_5/36`，`Gamma_5=e_5`。真实 K 帽付款是

\[
H_K=5/2+\Gamma_3+\Gamma_4+\Gamma_5,
\qquad a=25+\sum_j\theta_j-s.
\]

源文件已用自由等式 `E_C=|C|-K`，乘子 `H_K-s/5`，得到原存储行

\[
a u_2+\frac{s}{5}K-24\sum_x\frac{c_x}{p_x+5}
-\sum_x\frac{o_x}{6(p_x+4c_x+1)}
-\sum_{j=3}^5\theta_j\sum_x\frac{o_x}{6[p_x+(j-2)c_x+7-j]}\ge0.
\]

因此存储 K 列为 `s/5`。准备器直接复制它，不再加减一次等式；独立检查器把源的“真帽成本 + 有符号自由等式”身份在全部 28×513 列核对。这个身份不删除任何已有行，也不把一般合法 T 的大小当成 K。

## 6. 新授权读取的 source2 minimal：28 条 C-only，Main 最终审查待付

已实读此已冻包完整 `proof.md`，其域为 `tau_j>=0`、`0<=s<=9` 加每个 j 的两帽

\[
\frac45\tau_j+\sum_{h>j}\frac{\tau_h}{6(7-h)(8-h)}\le\frac{43}{60},
\qquad
\frac34\tau_j+\sum_{h>j}\frac{\tau_h}{6(7-h)(8-h)}+\frac{s}{20}\le\frac{67}{60}.
\]

它以坐标最小帽

\[
\beta_j=\frac1{12}+\tau_j+\sum_{h>j}\frac{\tau_h}{6(7-h)(8-h)}
\]

支付真实中间帽。原实际源 IC 权 `a=25+sum(tau)-s`，真 K 付款 `H=1+sum(beta)`；C-only 存储行使用 `mu=H-s/5` 的自由等式，最终 K 仍为 `s/5`。独立公式路由对所有 28×513 列及这个有符号等式身份核验。

自由等式乘子不能加非负限制：`tau=0,s=9` 给 `H=5/4,mu=-11/20`，其源 IC 权为 16、所有实际预算付款仍非负。准备器保留此端点和负乘子字符串，既不删行，也不对已完成的 C 等式再消元。该族保持真正最大 C 的限定，不被改名为通用 T 族。

此 28 行的准确冻结身份已绑定，但 Main 的最终复核记录尚未交付；它只列于 `reviewable_frozen_pending_sources`。没有生成 1823 行中间输入，已核定追加前缀小计仍只记 1795。

## 7. 实际 JSON 格式与待付来源

| 包 | 行列表字段 | 计数字段 | 坐标读取 | 第一阶段范围 |
| --- | --- | --- | --- | --- |
| `visible_maximum_joint_v4` | `raw_rows` | `raw_inequality_count=1586` | 输入原字段 | raw 0–1585 |
| `all_source_ordered_menu_cells` | `rows` | `raw_row_count=181` | 顶层与 `coordinate_contract.json` | raw 1586–1766 |
| `source2_cap_coupled_internal_safe` | `rows` | `raw_rows=28`，此字段是整数 | 顶层不含 bit_order，完整合同在 `coordinate_contract.json` | raw 1767–1794 |
| `source2_minimal_cap_safe` | `rows` | `raw_rows=28`，此字段是整数 | `coordinate_contract.json` | Main 最终审查/追加顺序未付，未分配 |
| `all_source_minimal_cap_safe` | **待读最终来源后确认** | **待 Main** | **待 Main** | 未分配 |
| 适应帽 ordered-menu 候选族 | **最终包名及是否纳入待 Main** | **待 Main** | **待 Main** | 未分配 |

1795 仅是已核定前缀小计；不是 v5 最终总行数。`source2_minimal_cap_safe` 只有在 Main 给出其准确最终身份并明确允许后才被读取。`all_source_minimal_cap_safe` 与适应帽 ordered-menu 族的活跃目录均未读取、列举、复制或导入；`pending_sources.json` 分别记录每族的权限、身份与待付状态。

Main 已明确一般 minimal 族将含五个实际源，其中源 2 的通用八标签族为 224 行；它在 C 等式使用前直接支付自身 K 帽成本，不能改称 C-only。这仅确定来源范围，尚未确定该完整包总数和行序。本席也不据此估计总行数。

下一阶段仍须由 Main 给出所有纳入族的准确最终 manifest、完整源行文件、证明、坐标文件及各 SHA；完整 raw 行数；源文件原行序及其哈希；完整来源复核记录及哈希；最终追加顺序；完整最终总行数。第三个 q=1/5 适应帽 ordered-menu 族需由 Main 显式决定纳入或不纳入，并给出最终包名；不能由本席猜选。所有纳入族须实读准确最终证明并核其真实预算/坐标路由，再更新本页；没有这些输入不生成完整矩阵。一般 T 行仍保自身原 K 成本，`H=t/min(D,5)` 不能无条件改为 `|T|/5` 或 K/5。若来源已经完成 C 等式路由，则不再消第二次。

## 8. 可执行接口与权限

`check_preparation.py --stage1` 仅检查已批准冻结包，分别输出“已完成 Main 源复核”和“允许阅读但 Main 最终复核待付”的检查记录，产出 `stage1_known_source_check.json`；不写合并矩阵。`build_input.py` 首先检查独立的 `final_release.json`，没有 Main 完整来源释放就直接退出。已提供的 `final_release.template.json` 不是释放文件，也不能通过生成门。其 `pending_source_decisions` 必须逐族明确决定，不固定为恰好两个追加族。

最终释放接口明确区分 `assembly_authorized`、`optimizer_authorized`、`freeze_authorized`；本席后续最多按 Main 指令开启完整组装，其余两项在准备代码中必须为 false。生成器只复制字典并记录来源，独立 `check_preparation.py --assembled` 不导入生成器或来源程序，逐全列核验字面原序、全部 metadata、旧尺度、目标、两等式与零/重复行保留。新的 minimal 真预算公式适配必须等最终来源阅读后补齐或明确由 Main 的最终源证明记录承担，不能提前声称本阶段已做。

本阶段只写本目录及相邻 v5 说明，不改 Git、RUN、登记或旧冻结工件。没有求解、行筛选、支持限制、固定 K、SPE 实现或新的全域最优值声明；half 仍 OPEN。

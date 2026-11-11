# 四个actual源的同分支第五源SAFE族：符号准备完成

Boss1；RUN `six-boss1-20261111`。状态 **PREPARED_NO_OPTIMIZER**。本包证明并冻结 **36条完整513列必要候选行**，0次优化器调用，未将任何行接入LP，未读取或绑定1003后续结果。

## 普遍必要式与真实来源

有限单位客户、有限非空共同标签目录、恰六人完整有序历史纯SPE；允许空覆盖、同覆盖别名、重复行动、全部弱平局。取actual源i=1,…,4，n=6−i，客户实际前缀负载p∈0,…,i−1，D=p+n+1，ci=(n+1)/2，θ=5/12。T为任意合法强制标签，t为其会员；O为任意六合法可重复查询的覆盖并，o为会员，不必OPT，也不作为行动。

定义

\[
m_i(p,t,o)=c_it+\frac{24t}{D}
+\frac{o}{6(p+1+nt)}
+\frac5{12}\left[
\frac{o}{6(p+(5-i)t+2)}-\frac{t}{\min(D,5)}
\right].
\]

则通用真实付款为

\[
\boxed{R_i(T)=25u_i+c_iK-\sum_xm_i(p_x,t_x,o_x)\ge0.}
\]

它来自actual源对T的IC权25、同分支每个中间尾大小帽权1/2、末尾大小帽权1、同一真实末节点六查询BR均值权1，并加入同一分支内部真实第五源的六查询SAFE均值权5/12。强制T不获得新的source-i最优性；内部第五源自身是该真实历史的最优行动者。

令前第五源尾会员和r、第五/第六位y,z，k=p+n。解析最小值证明为：t=0时每加一个r会员严格增加成本至少175/432，再逐四个(y,z)端点得到非负闭式；t=1时全部非末尾会员都严格降低成本，末位加入差恰为

\[
\frac{k^2-25+5/12}{k(k+1)}.
\]

k≤4取末位1，k=5取末位0，所以第五源份额必须用1/min(D,5)。若错误地用1/D，八个完整反证态的余项均为−1/72。固定仿射公式的θ段准确至5/12，p=0,t=0,o=1且仅第五尾覆盖的态在超出后立即给负余项；这不是对全部真实预算权的最优性声明。

## 36候选、四条弱行与C2准确等价

每个i取T=A1,…,A6,X,C,outerOmean，共36行；全部512型 `(a1,…,a6,x,o,c)` 和独立K512列保留。纯T行直接取公式，均值角色则先对同六个真实外索引求平均。若m0=m_i(p,0,o)、m1=m_i(p,1,o)，准确外平均为m0+d(m1−m0)/6，因m1−m0>0才弱化为m0+o(m1−m0)/6。20类型最小差为2333/432。内外都用同一六标签列表，包括对角与重复标签，没有独立性或分割假设。

36原行都保25ui付款尺度，数值正除数记录为25。以下比较已逐513列核验：

- 四条outerOmean行被已有P25双mean **30异索引**行逐客户支配。十个(i,p)准确正差见proof及比较JSON；这些行保留在请求的候选包内，不自动建议加入未来LP。
- 令EC=Σcz−K=0，四个纯C行均可通过自由等式R_i(C)+ciEC消去ci(K−|C|)。
- Main已证NS5整数行与本族C2恰有 **NS5=12R_2(C)+29EC**。二者在C等式上等价，不是独立加强。
- 其余纯T行只声明合法真实付款来源和指定点诊断，不声称已证明逐条严格新增或锥独立。

## 全域字面核验

第二套标准库Fraction程序没有导入builder，先从每条真实IC/CAP/BR/SAFE的客户列重新求完整隐藏态最小值，再以这些枚举最小值独立重建36行。其身份是内部独立实现，未冒称外部盲审。

| 核查 | 数量与结果 |
|---|---|
| 全有序隐藏态及最低值 | 416态、40类，全部PASS |
| 新候选矩阵 | 36×513=18468项，全部PASS |
| 内层真实六索引会员/尾状态 | 13312态，全部PASS |
| 同六列表外索引与内层尾状态 | 39936态，全部PASS |
| 外平均与正斜率 | 640平均、20斜率，全部PASS |
| 四个C等式消元 | 2052列项，全部PASS |
| Main NS5尺度及自由等式身份 | 513列，全部PASS |
| 全族与旧P25比较 | 18468列项，全部PASS |
| 冻结1002点 | 513非负列、1002旧行、2等式全部PASS |

## 冻结1002点上的两条准确违反

只绑定旧1002输入SHA `b0610bb00298a4ee953423a8066dab050cb9d515fd6d5dde41f5117116f2ba33` 与证书SHA `8dd66c5c1cd3d729d262b64d6874ca9c7090952f0100c97d5ccc5397c6465347`。

36新行中只有两条负，其余34非负：

| 行，原25ui尺度 | 准确slack | 约值 |
|---|---|---:|
| i2，T=C | −15981204499895866953854050884598865236619 / 1037123521286961071765261538670269631165152 | −0.01540916214 |
| i2，T=A4 | −24476170389995617182629345358265365736487 / 10500875653030480851623273079036480015547164 | −0.002330869463 |

C2准确值是Main NS5整数行值的1/12。A4给另一条合法查询的旧点诊断，没有证明其在加入NS5后的独立性。该点只是冻结必要投影点；本包不构造SPE、不求最优值、不做点补全。原half仍OPEN。

## 文件入口与冻结绑定

- [proof.md](all_source_nested_safe_family/proof.md)：完整真实付款、解析最小值、同六列表外平均及精确比较。
- [exact_family.json](all_source_nested_safe_family/exact_family.json)：36条完整513列未缩放符号行。
- [row_catalog.json](all_source_nested_safe_family/row_catalog.json)：四条弱外mean、C2等价及所有来源描述。
- [hidden_state_checks.json](all_source_nested_safe_family/hidden_state_checks.json) 与 [minimum_table.json](all_source_nested_safe_family/minimum_table.json)：全部416态、40类及全部达到态。
- [old_P25_comparisons.json](all_source_nested_safe_family/old_P25_comparisons.json)、[C_equality_comparisons.json](all_source_nested_safe_family/C_equality_comparisons.json)：全部比较列。
- [frozen_1002_point_diagnostics.json](all_source_nested_safe_family/frozen_1002_point_diagnostics.json)：36条准确slack与旧点来源绑定。
- [check_literal.py](all_source_nested_safe_family/check_literal.py)、[literal_check_result.json](all_source_nested_safe_family/literal_check_result.json)：不导入builder的第二实现与完整结果。
- [freeze_manifest.json](all_source_nested_safe_family/freeze_manifest.json)：所有产物SHA及只读源绑定。

| 核心文件 | SHA256 |
|---|---|
| exact_family.json | `340267bbe7148107a685eb260ffc24029de1a93f77f4a4fd3f201cc109e5aa8b` |
| proof.md | `80a6ce05d8fc236298ff2e6b9fe0cc47073b5cbd7afbb155b560cce1ec95e212` |
| check_literal.py | `966c26b472c29a97faf445658bf543c2ae0835d0b21325186a3961cd04415965` |

全部8份直接来源在构建与检查前后保持相同SHA。写入仅限本新目录与同名摘要，未操作旧包、Git、RUN、registry或凭据，未将36候选中的任何行自动接入后续优化。

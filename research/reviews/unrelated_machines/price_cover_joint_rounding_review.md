# 任意汇点价格覆盖与共同占位算法的独立审查

被审正文：[arbitrary_sink_private_group_price_cover_rounding.md](../../current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md)。最终全文 SHA256：`6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580`。此审查只覆盖三个精确 ID，不关闭一般 `UM-TARGET-v1` 或其反面。

## 实际顺序与证据层级

1. `hardness_decoder` 先只看精确列预算/平行扩张 Claim，自行重构紧集链与单侧残差计数；`independent_selection` 已收到 boss 的计数提示，其重构和精确代码核验不冒称全盲。前者独立稿在看作者证明及查旧文献之前冻结，SHA `f26dcb5dd22e5a35ce2366f625bf79dd9119f916523ea12a0168ae0fc63d5424`，原字节保存在 [statement-first 重构](../../../history/source/notes/unrelated_machines/upper_column_budget_base_statement_first_reconstruction.md)。它证明一般基秩 r 的接口；canonical 另要求存在覆盖全部宏任务的满秩匹配，不能由空模式类自动推出。
2. `global_relaxation` 先只看原结构算法陈述（当时为更松的加性2D界），自行重构价格覆盖与 MW；之后收到 boss 的 +B 计数提示，再核其细节，故不把 +B 这一步记为全盲重构。`menu_generation` 构造极小覆盖与价格 oracle，MW桥由boss提出后共同攻击。上述讨论发生在读作者完整冻结稿之前；后续实际全文审查另列。内部角色不是独立 Work 身份，不自行提交。
3. 四位实际完整读取作者冻结首稿 `07e65d4798eece8159ba9c4cbad6631bf3b2c221013eba97c48e1c3cdd3c7d1f`，都指出同一个空模式满秩漏洞；不能以多数赞同抵消该异议。首稿的“Q_h 可空且原 G 覆盖 B ⇒ 模式基大小 |B|”错误：一宏一 home 一边、Q_h 空时模式拟阵秩零，不能恢复该宏。
4. 修复后显式要求非空模式类的 home 集 H_Q 仍覆盖 B。结构算法的共同匹配频率自动给该条件。第二稿 `9fa1bb886e50b9393873366116fe6e58c120ad5e1617eac2d36c3849477c849f` 已实际全文重读；之后仅把精度措辞改为“不声称对 eta 的二进制编码长度为多项式”。最终完整 143 行又由两位实际 hash→cat 全文→攻击，未改旧报告冒新 SHA。
5. 最终实际读后原件：[全链审查](../../../history/source/notes/unrelated_machines/arbitrary_sink_price_cover_final_full_read_review.md)，SHA `d45f00c0e7684bae520ae61ed53213cf20e91a24c18e7eed0972753f8b1a9a63`；[平行基与全链复核](../../../history/source/notes/unrelated_machines/arbitrary_sink_price_cover_parallel_base_final_read_review.md)，SHA `a87e2b22d197734a64a49714b086a99719378058cbd67f0239bcf96e76a50aca`。它们都实际绑定本页顶部的最终正文 SHA。boss9 另亲自核对全部推导、代码及实际重跑。

## 承重检查及处理结果

| 义务 | 实际核查 | 结论/限制 |
| --- | --- | --- |
| 对象和满秩 | 非空模式类 H_Q 全宏匹配；每 home 至多一 occupied copy | 首稿异议已关闭；不允许直接复制邻接丢 home 容量 |
| 单侧舍入 | 紧秩格极大链每块质量正整数；sum(1−x)≤d≤保留行数；逐行 residual≤B | +B；不是双侧或任意成本保持 |
| 实际匹配 | 固定 copy 只固定 home 被占；宏流可重排；最后重新全局匹配 | 不冻结旧宏身份 |
| 顶点/位长 | x 投影 lex 顶点；下一轮释放临时分数 lex 等式；仅永久固定0/1 | 未调用免费配置或整数 oracle |
| 覆盖与零值 | 真 home 覆盖不舍入；正成本猜测 DP；零成本先取、再删冗余 | 出口量≤rho(1−tau+delta)T；任意逐件资格 |
| 价格/MW | epsilon=gamma=eta/4、N=ceil(16RK/eta²)、R≤max(1,|H|) | 均值≤(1+eta)T；权重/价格精确有理 |
| 所有任务和机器 | 同一实际模式回溯；empty 全回 home；私有组不交；宏集合独立 | 每件恰一次，所有 sink 同时受界 |
| 未知 OPT | 当前查询不检查宏>T/2；OPT 处单宏见证适用于每个 T≥OPT | one-sided FAIL 和非单调接受整数二分成立 |
| 边界 | T0 先零边；空任务/组/宏/sink，单端、零时间、大分母 | 纯数学分支齐全；有限覆盖范围见下 |

## 可复现有限核验与实现界限

- [列预算审计](../../../tests/audits/unrelated_machines/upper_column_budget_base_audit.py)及[顶点核心](../../../tests/audits/unrelated_machines/occupation_vertex_audit_core.py)：root 实际重新运行 187 例，283 次面检查、380 个整数基选择、96 条删行；27 例原预算无整数基，均满足加性 B。独立排列匹配、紧秩全部子集、永久零支持、秩一渐近锐性及丢 home 容量的负控制均有实际检查。[冻结结果](../../../evidence/runs/unrelated_machines/upper_column_budget_base_audit.json)保 seed、源码及核心 SHA。指数顶点枚举不是多项式实现。
- [独立价格覆盖/MW 审计](../../../tests/audits/unrelated_machines/arbitrary_sink_price_cover_mw_audit.py)不导入已有覆盖程序；root 从规范路径在新输出目录实际重跑。112 静态矩阵、64 个 T 可行静态例、371 静态价格；合计 104920 份完整原矩阵分配、1876 次 oracle、4016 次覆盖子集对照。触发真近似成本 97/96、近紧 B、任意逐件资格、零价格、宏占位切换及一次真实 priced FAIL。四组完整 N 分别 64、512、384、512 轮；三 sink 小 eta 只跑32轮前缀，未冒称完整 N。三个 T0 分支独立检查。[输入](../../../examples/unrelated_machines/arbitrary_sink_price_cover_mw_cases.json)和[冻结结果](../../../evidence/runs/unrelated_machines/arbitrary_sink_price_cover_mw_audit.json)含精确参数、seed、源 SHA、未检查范围。
- 结果生成只写显式新目录并拒绝覆盖；默认 stdout。root 的生成输出名与归档名不同，原字节/fixture SHA 精确相同。有限审计分别核菜单/MW和舍入，不代表生产级完整有理 LP 后端；软件实现轴仍为 none。

源码与冻结原件不为通过检查而改写。一般证明由正文承担，有限计算只用作 checks。未知 OPT 搜索另在实际审查中用非单调谓词精确枚举，不拿这些谓词实验替代一般不变式证明。

## 来源与剩余义务

boss9 实际打开 2019v2 原始 arXiv PDF，Theorem2 印2/PDF3 给 upper-only multiplicities 的 Delta−1；该工具经共同分母直接涵盖 +B，应记标准已知工具。另核 2026v1 §5 的双侧加权背景。独立审查者没有全部重读这些外文，不把作者来源核查倒记为所有人的认证。覆盖 DP、最小成本匹配、MW 都是标准工具，组合结构的新颖性/独立论文价值未认证；没有外部 peer review。

最终 standing 实质 objection：无。主目标及一般反面仍 OPEN。唯一 home、W_h、出口 rho 包络及 delta 余量没有从一般输入生成；正面结果可用于排除输出始终满足这些结构承诺、且 YES/NO 绝对阈值超出本近似系数的候选归约，不能称作一般近二困难性或一般次二算法。


## 提交前代码字节复核

checkpoint 的 cached whitespace 检查发现有限顶点核心 EOF 多一个 LF。只移除这一字节；不关闭或弱化检查，不改原冻结记录。当前核心追加一个 LF 后的 SHA 可精确恢复原 `8c5464edfd9990c98ee7bc4901544f108e31ae1c89fe5411119f6899bf93beba`；数学函数全部字节未变。root 按现有规范路径重新运行187例，[新冻结结果](../../../evidence/runs/unrelated_machines/upper_column_budget_base_clean_source_audit.json)保当前核心 SHA，与旧报告除该依赖hash外所有数值、源码hash和断言字段完全一致。两份实际读后源保原字节，不冒称已读新hash；本段是root实际差异和重跑复核。最终数学正文SHA仍为本页顶部6c23677a。

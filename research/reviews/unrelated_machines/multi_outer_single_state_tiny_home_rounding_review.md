# 多outer、单state、极小home权重：实际算法审查

2026-10-18，boss11。正式身份 UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1。最终正文175行/17086bytes，SHA256 84d6031655ac43d9c5726ed2cac6f5241e709743232290e604d767602613778a。只覆盖原k⁴-tiny域，不混后续k²/vector/高阶偶矩learning。

## 独立性及实际阅读链

作者先冻Exact38c85f…与Proof ce05c7…分开；NSW只读32行Exact，先独立重构205行c06379…，未读作者算法/程序。该独立路线用floored-simplex强凸势、可计算有理投影subgradient、fixedstates allocation LP去掉至多k个split items，和作者MW+平方势方案不同。root实际全文读Exact与该205行记录后才释放作者Proof；root也实际全文读作者193行Proof。

NSW实际完整读193行Proof，冻146行567b9e…读后，逐核作者MW/逐i variance及shared-state请求后端，root实际全文读该记录。不能以不同独立算法的正确性代替对作者方案的核查。root亲自参与过公共分母与最终不能丢请求币的讨论，因此root不算另一方向盲审。

作者新175行自足稿8138cf…由root实际全文读；最后只规范正式ID/status/链接和root已实际重跑的有限软件，成84d603…；数学算法不变。最终实际读范围以所存final record为准，root实际全文读该记录后再登记成熟。NSW后续另写variance/moment工具的作者合作不归入本ID、不回写旧独立记录。

## 完整数学合同

k任意输入正整数，所有positive homes互异、每home own-unit helper，outer各只有一个state，wmax<=1/(4096k⁴)，共享B arbitrary normalized fallback。输入只有Q，不给LP/OPT/actualallocation/oracle。全文保全部indexedstates和原selectors/incidence jobs，zero和inactive payload最后回原private。

OPT=2−V完整双向给出。显式ordinary rational common-SA1 LP必要于V>=15/16，不可行给actualOPT>17/16，baseline全jobsC2比<32/17<1.9；feasible不是被当整数可行。own singleton整化仅需同一SA1二阶点，得到全部helpers共享packing cap1及各outer ε benchmark，没有各outer复制容量。

独立helper states+条件请求，CDF weighted oracle >=1125/2048；floored rational MW N1024k轮，逐outer均值>=757/1792>2/5。所有轮的g共用固定底层概率分母，N轮分母位长线性累加；λ改变order不改变probability，避免位复杂度循环。

每resource独立混合orders，whole-helper替换含自身所属outer影响，<=16k w_j；逐i Efron–Stein+全k求和给总variance<=129/4096<1/25。精确平方势只需单/双资源winner events，shared helper必须同一state；state内请求coins才独立。CE全固定后保实际请求winner，不能重新把未请求chosen clauses加进max。所有q=.1回填及每个原job执行，实际C<=1.9；OPT>=1给同一ratio。

全部rational LP/排序/one-two-resource枚举及CE为固定总位多项式，次数不随k增长；无tiny概率倒数循环、隐式profile枚举或exact SDP finder。有限归一化与原jobs构造没有替换模型。限定near2源排除只在全部输出typed域且YESactualOPT1、NO>=2−γ、fixed0<γ<.1，并明确P≠NP；不排一般source。

## 有限软件：root实际读跑，非全算法实现

root实际完整读195行自足程序（SHA460679…），在全新scratch目录运行其原CLI，stdout与作者JSON逐字同e7433d…。规范路径保原字节，完整actual argv/cwd/真实范围在root scope。数学审者未读跑代码，不替root签执行。

两固定小例各3helpers、2outers、2states/helper、2resources、2rules，统一request rate。公式单/双资源moments与完整2048/2916outcomes精确枚举相等，各11步state→coin→rule CE势不增，最终moments等actual requesting-winner values。最终势565057/26873856和8248921/150994944；第二例outer值0，因为它不满足本定理tiny/均值前提，不据此冒算法实验。

只这个Fraction后端审计，无seed；没有建/解Rε、没有MW实现、没有tiny实例、没有ordinary全jobs输出。算法是完整数学规格而非端到端软件，有限data只checks后端。一般正确性来自证明和独立攻击，不以样本代替全称量词。

## 价值与未解决义务

标准CDF/welfare、MW、Efron–Stein、conditional expectation和normalized值桥不认领新颖性。可复用组合是同一全局point→全部outer均值→所有outer同时平方势→真实请求winner的确定性生成，保持任意共享fallback及可变k。主页单outer13/8不能直接当多outer结果。本限定profile仍依赖tiny和单state，真正multistate/大系数共享选择未闭合；一般UM及反面OPEN。外审、全球新颖性和独立成文价值未认证，精确范围无standing fatal。

## 保真来源

| 来源 | Container SHA256 | Original SHA256 | 包装 |
| --- | --- | --- | --- |
| history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_exact_v1.md | 38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a | 38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a | original bytes |
| history/source/notes/unrelated_machines/sol_general_repair_multiouter_single_state_tiny_home_19_10_author_proof_v1.md | ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332 | ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332 | original bytes |
| history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md | c063799d1cfa38db6f05cd14f47bc728136dd6766856e4956f9cbe5570a2549a | c063799d1cfa38db6f05cd14f47bc728136dd6766856e4956f9cbe5570a2549a | original bytes |
| history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_author_read_after.md | 567b9e1153ecfb15b2ff14013a14e52df73a5acefe7585fe2e5652fdfb7483d0 | 567b9e1153ecfb15b2ff14013a14e52df73a5acefe7585fe2e5652fdfb7483d0 | original bytes |
| history/source/notes/unrelated_machines/sol_multi_outer_tiny_home_final_canonical_actual_read.md | 299a27d33a68522b78ee70e8779752df6961b90b0dd5a7c8b4ef8396cadb2d90 | 299a27d33a68522b78ee70e8779752df6961b90b0dd5a7c8b4ef8396cadb2d90 | original bytes |

代码：tests/audits/unrelated_machines/multi_outer_request_winner_pair_backend.py。冻结证据：evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json, evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_root_replay_scope.json。

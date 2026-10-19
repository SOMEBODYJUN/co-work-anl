# 固定d整行一致性仍gap2：新增§13的实际审查

2026-10-18，boss11。正式身份 UM-DILUTED-SHARED-TERMINAL-ROW-DEGREE-GAP-v1。当前440行SHA256 fb705e62ae3344a24c95ca962d4fa2cfd83dbc57422eb59fd6285713e29a121b；前245行/19100bytes SHA256 7128241668e8f7b5abe014775f9d0d3b4f59a5bfecbb2f1aef8e357272bb01b4原字节不变。本审查只升级新195行，不代替旧v1的全245行实读记录。

## 精确次序、角色与真实实读

作者literal与identity共同讨论subset插值，二者不互计独立审。先冻Exact e23ae4…及另冻Proof7fb8ae…；general仅看Exact，在熟悉rawK2但未看新旧literal Proof/code的背景下独立重构4294c1…；root实际全文读该7节记录后才释放Proof。general实际全文读作者Proof另冻c3ac3d…，root实际全文读Exact、Proof及这两条不同证明记录。

作者standalone§13 21ab76…全195行由root实际全文读；root保留旧245行前缀，仅规范status/review routing/真实软件范围，组合成fb705e…。root实际全文读组合后的新§13。general实际完整读246–440新195行，旧前缀只hash不追认旧审；final v1先透明指出root完成时态的CLI应由其实际兑现。root随后确实运行规范代码到全新scratch文件，结果byte-identical，再回报事实；general另冻final v2 d4dcc1…，仍未打开code/JSON/root scope，不冒独立软件执行。root实际全文读final v1和v2，两原件均保留，不回写中间审查。

## 数学覆盖

每固定d>=2、k>=d，s=d−1,D=max(4,d)，新M含120Lk4与4kZAmax；不是旧v1同一M的状态升级。原矩全部jobs/所有finite端明确，dense ∞矩阵规模也为固定d多项式。实际OPT上下界仍由完整调度r²<=k与attaining assignment给出，组件数不影响逻辑。

所有具体subset containment identity由有限差分或审者生成函数证明，含s=k−1边界。unit+home mixed≤d与purehome d次完整匹配；purehome corrections在所有阶抵消。foreground baseline aδC0all不是额外叠在旧H边际上；背景负质量吸收恰由显式M−1>=4kZAmax同时支付，所有配置合法且总质量1。不是只有signed moment相等。

old-half Qold的任意截距/所有e系数square下界给||c||²/(60Lk4)；H负项≤2||c||²；其余全部组件的conditional variance乘正slack均值。M−1>=120Lk4保证所有global affine localizers，而不仅fixed row principal frame。审者另给独立Var_Qold路线，未把作者proof反标成先行所知。

指定moment table只到D，所有原quotient等式完整到D、globalM2与全row≤d分别付款。自然law有all-degree PSD不表示更高q负载localizers成立。原degree3跨行selector×incoming条件始终为负。下一mixed d+1 witness若d+1>D，仅是指定finite-law自然延伸，不能宣称degree-D restriction没有其他延伸。Joint Boolean CONFIG links/canonicalC2/S3及hardness均不在范围。

fixed d下Z<=d k^(d−1)、M多项式、O(E^D)表和subset CONFIG list可detbitpoly生成，partial injection/permutation的不可容纳事件先判零。d若binary输入则没有统一多项式指数承诺。标准CONFIG-first slot2上界与缩放逼近2给supremum2，不求出各实例精确relaxation阈值。

## 实际有限软件

root实际完整读新的122行独立作者trade程序，原字节SHA acee8c…复制规范路径。规范CLI --output指定全新scratch文件，四例passed，JSON与作者原输出逐字相同416d76…。argv/cwd、真实返回与范围在root replay scope。用Fraction及整数共同分母，无seed。

仅(d,k)=(2,2),(3,3),(4,4),(4,7)，全≤d squarefree row monomials分别11/42/163/1471，全行矩相等、配置质量非负/合法/总1、purehome完整边际及自然下一阶witness均核。没有实际展开globalM2/localizers、没有general-d证书生成器，也没有把旧50dim审计升级。全部无穷参数与allcontexts由解析证明承担。审者没有打开程序，不替root签执行；无外审/新颖性认证。

## 来源与准确价值

新可复用增量是把rare-H全局支配与显式低home subset背景结合，通过逐subset有限差分trade在任意固定整行阶数维持实际gap2。有限差分/标准slot工具不认领新颖性；不把局部阶数增加误称完整SoS或原主目标反证。主目标及一般反面仍OPEN。当前精确范围无standing fatal。

| 来源 | Container SHA256 | Original SHA256 | 包装 |
| --- | --- | --- | --- |
| history/source/notes/unrelated_machines/sol_diluted_shared_terminal_row_degree_d_exact_only.md | e23ae495b4a997f081e0de06323e5dd9563c98d3828b78804ddc7670b16c9f6a | e23ae495b4a997f081e0de06323e5dd9563c98d3828b78804ddc7670b16c9f6a | original bytes |
| history/source/notes/unrelated_machines/sol_diluted_shared_terminal_row_degree_d_author_proof.md | 7fb8ae7e6635853417963a5ff379406cbc3a0abf347a73015ebc79c1a207c407 | 7fb8ae7e6635853417963a5ff379406cbc3a0abf347a73015ebc79c1a207c407 | original bytes |
| history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_exact_first_reconstruction_v1.md | 4294c156fa6feb502b6c3e90bec6c0bd8fb9e8e5ecc4008c2cf9b71838cf3447 | 4294c156fa6feb502b6c3e90bec6c0bd8fb9e8e5ecc4008c2cf9b71838cf3447 | original bytes |
| history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_author_read_after_v1.md | c3ac3d56ef9ae27b1b4041adf7b8bb91b78c63b303f7fc27d3a70757672081d6 | c3ac3d56ef9ae27b1b4041adf7b8bb91b78c63b303f7fc27d3a70757672081d6 | original bytes |
| history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_final_section13_post_read_v1.md | a2807db48cff732c57147cb0b54db28111dc543738750cacc9b6e00f742b1b3b | a2807db48cff732c57147cb0b54db28111dc543738750cacc9b6e00f742b1b3b | original bytes |
| history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_final_section13_post_read_v2.md | d4dcc198d7e8777d54fe0c74657998fb943f6fa235f2f5bc8e5aeb4641050c28 | d4dcc198d7e8777d54fe0c74657998fb943f6fa235f2f5bc8e5aeb4641050c28 | original bytes |

代码：tests/audits/unrelated_machines/diluted_shared_terminal_row_degree_trade_audit.py。冻结证据：evidence/runs/unrelated_machines/diluted_row_degree_trade_four_cases_audit.json, evidence/runs/unrelated_machines/diluted_row_degree_trade_root_replay_scope.json。


代码行数校正：原审查误写140行，实际原字节代码为122行；SHA、完整实读及一次规范CLI的记录不变。

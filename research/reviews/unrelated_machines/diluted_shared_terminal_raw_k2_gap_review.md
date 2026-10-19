# 稀释共享终端 raw K2 真实锐 gap：实际审查及软件范围

2026-10-18，boss11。正式身份 UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1；该次冻结最终正文245行/19100bytes，SHA256 7128241668e8f7b5abe014775f9d0d3b4f59a5bfecbb2f1aef8e357272bb01b4。该系统的一般 gap 上确界为2，不是一般UM的计算困难性。

## 独立重构、作者证明及最终文本

作者先分别冻86行Exact25888ec…和135行Proof2e926c…；identity只读Exact，在已有K2/CONFIG背景下独立重构257行622caf…，先冻，未读作者Proof/code。root实际全文读该257行记录、Exact全部§1–5后，才释放Proof；root也实际全文读135行作者Proof。identity实际全文读作者Proof，另冻122行f960b9…；root实际全文读该记录。独立Var_Q路线与作者系数范数路线不同，两者均核通明确M=1+60Lk4，未用维数固定连续性或未知小常数。

作者中文草稿5865dba…全部12节由root实际全文读，再只规范状态、独立review routing、完整dense矩阵编码和k2有限核范围，成最终712824…；root实际全文读该245行终稿。最终独立审查对象及实际读范围、hash以所存final record为准，root实际全文读该record后才登记完成。较强固定d探索、SH3后续learning均未混入本Claim或当前证明。

## 逐项数学结论与边界

全部M(1+L+k)台机器、1+Mk(1+L)原jobs、全部有限端均明确；真实OPT=2−floor(sqrt(k))/k由r²<=k和完整可达schedule双向给出，覆盖h的每个目的组件。矩法则是真实完整assignment law，但含负载2的samples；不能把M2 positivity当成所有sample负载合法。

每B五类合法CFG与全部first/pair逐项吻合，差质量非负由M−1>=4k²和4k(k−1)保证。U/terminals逐点load<=1。Q square domination对任意截距及任意e-head系数成立；H negative bound为−2||c||²；conditional selector后其它全部组件的variance只乘正slack均值。由此所有全局affine contexts同时付清，无机器数因子漏项。

Certificate生成只查询<=4原端的partial injection/permutation，完整表大小固定poly；实际P若dense还输出所有infinity，总mn亦poly。没有按指数support枚举，没有一般exact SDP/CONFIG finder。slot matching给每个raw可行T的OPT<=2T；infimum下界2及family比值极限2正确，ratio只对正OPT讨论。OPT0/空任务的主目标不被本限域gap声明替换。

此v1不匹配same-row triple：F(R_jY_lY_l')=a/L>0而legalCFG为0。F(A_i C_B slack_B)=a(k/L)(T0−2)<0，故更强两事件条件、joint Boolean CONFIG-M2及canonical export gates未被排除。本点的失败不证明所有更强证书失败；实际near2 gap不是源问题的YES/NO reduction。UM-TARGET-v1及一般反面保持OPEN。

## 实际有限软件核验

root实际完整读代码，SHA4da7af…原字节复制到规范路径。先用原代码在新scratch目录--output重放，再用规范代码在第二全新目录同CLI重放；两次输出均与作者原JSON逐字一致SHA0b2b750…，完整argv/cwd在root replay scope。所有运算是Fraction，没有随机seed。

这个程序只在k2、L8、M7681时直接枚举121个component states，核一台B的全first/pair，以及constant+selector-regime+16f-head+32e-head的50×50 affine Gram精确LDL；逐项LDL重构、50个严格正pivots。它不展开84,491台机器/138,259个jobs的全局矩阵，不检测所有跨组件contexts，不是general-k证书生成器。k2比值恰1，不以它数值认证近二；任意k和global contexts由解析证明承担。独立数学审者未读跑软件，不替root签执行。

## 最接近既有资产与价值分开登记

已有UM-WEAK-H2-CONFIG-MOMENT-GAP-v1只共享CONFIG first；旧资源星在加入同机pair后被UM-STRONG-H2-ROW-PAIR-STAR-EXACT-v1精确识别。当前不同共享终端族同时通过全部同机pair、真实全局M2和全部affine physical localizers而实际OPT趋2，因此确实改变这个更强合同的已知边界。旧strong matching-law obstruction的actualOPT1不被追认为整数gap。

标准slot2上界、均匀injection计数、matching integrality不是新成果。新的可复用数学是这份具体普通原矩阵上的rare-H/background-Q定量支配，以及跨任意数量components的完整conditional-variance支付。全球文献新颖性与独立论文价值未认证；定向primary检索不等于穷尽不存在先例。没有外审记录，无general调度软件。

## 保真来源

| 来源 | Container SHA256 | Original SHA256 | 包装 |
| --- | --- | --- | --- |
| history/source/notes/unrelated_machines/sol_diluted_shared_terminal_raw_k2_exact_only.md | 25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b | 25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b | original bytes |
| history/source/notes/unrelated_machines/sol_diluted_shared_terminal_raw_k2_author_proof.md | 2e926c6471c68843602f78c101874198e0ad2808b8db12d737cc8a04f27ad948 | 2e926c6471c68843602f78c101874198e0ad2808b8db12d737cc8a04f27ad948 | original bytes |
| history/source/notes/unrelated_machines/sol_identity_coupling_diluted_shared_terminal_raw_k2_exact_reconstruction.md | 622cafcc002d4b507ae8905cf2b4d2cc0cc16f538b33974f51695bd9fb58cb0f | 622cafcc002d4b507ae8905cf2b4d2cc0cc16f538b33974f51695bd9fb58cb0f | original bytes |
| history/source/notes/unrelated_machines/sol_identity_coupling_diluted_shared_terminal_raw_k2_author_proof_read_after.md | f960b9f1cf8751aa82396c286929a950e3fa1ef563ea3b2deee5a4eff1f5e4b9 | f960b9f1cf8751aa82396c286929a950e3fa1ef563ea3b2deee5a4eff1f5e4b9 | original bytes |
| history/source/notes/unrelated_machines/sol_identity_coupling_diluted_shared_terminal_raw_k2_final_actual_read.md.gz | 372fbef7e8313285a5b10ebb44ff40af4a8782916fe9ca3bf4e9cd91dcb7909f | 1ffa72b0838dac59855ddf39a90b4da540329b3f973cf67c5b7a031fc8011836 | lossless gzip |

代码：tests/audits/unrelated_machines/diluted_shared_terminal_raw_k2_finite_audit.py。冻结运行：evidence/runs/unrelated_machines/diluted_shared_terminal_raw_k2_local_frame_audit.json, evidence/runs/unrelated_machines/diluted_shared_terminal_raw_k2_root_replay_scope.json。


## 后续追加的审查范围

当前440行正文SHA fb705e62ae3344a24c95ca962d4fa2cfd83dbc57422eb59fd6285713e29a121b；本次原245行/19100bytes前缀712824…逐字不变。新增§13的固定d整行一致性gap由[另一审查](diluted_shared_terminal_row_degree_gap_review.md)覆盖；本旧v1审查不追认已审新M/T/D或新软件。

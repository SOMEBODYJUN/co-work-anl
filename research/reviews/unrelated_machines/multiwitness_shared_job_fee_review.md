# 多见证互斥查询、实际费用与共同容量的审查

2026-10-18，boss11。只新增canonical§6，完整文件SHA256 `bf942037e600967fa86b76c2b1f0db41673a2bae71411e1afb6527d6f332c709`。旧§1–5前缀保留。新身份UM-MULTIWITNESS-SHARED-JOB-FEE-CAPACITY-v2不是旧双见证结论的扩大版。

作者先冻结v1 Exact；独立审者先重构所有pattern OPT/闭阈值fee，并发现非空子集推论漏K非空，K=empty会给0<0。该fatal及原v1字节保留；作者另冻v2 Exact与Proof，明确empty费0且严格和式仅非空K。审者再实际全文读v2 Exact/Proof、最终canonical完整§1–6，核两合同不冲突；root实际读新Exact/Proof/规范§6及全部实际审查，并独立核完整原矩阵和所有阈值分支。

每singlequery有自己的strict见证，但全部unit汇流时不存在共同全开strict见证。阈值二收费与旧双见证三半分离不冲突；至多一枚可在strict共同激活且在beta>=3/2都必收费的容量结论阻止免费fanout。此构件OPT1、显式可解，不是NP源gap。

规范代码SHA `0697e1b9da8a26c4ba1e7808e272ffa720a52e7ea09b975c962a101adaae64c6`，原资格完整分配mask/Fraction是独立主oracle，再比数学公式。root实际113cases/287104完整分配/3004patterns/19832闭阈值核验通过。另一独立实现359cases/135712分配/4660patternOPT/23908阈值另冻，不混成同一批。源码审者实际全读并拒既存output，未假称也重跑root批。

重放命令：`python3 tests/audits/unrelated_machines/multiwitness_shared_job_fee.py --output <新的scratch路径>`。两端资格、empty、beta=B/c+B、sum界等号、c1与tiny a均在明确有限cases内；有限结果不代一般证明。

限定证明及实际攻击无standing fatal；外审、新颖性、实际source decoder和通用fanout均未取得。与旧多输出预载星的对象/量词区分见正文，不把三个接口混为一谈。主UM正反面仍OPEN。

## 保真来源

| 保真来源 | SHA256 |
| --- | --- |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_exact_v1_with_empty_gap.md | 018a57a9dc367a7287fbaa1806b93f81bf76582978dbdf0e3236b9664b726ad1 |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_exact_v2.md | b3b3f2d98a6b81d5ee525bcdfa0fb26d1021994db58419f11f4862b321e6a607 |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_author_proof_v2.md | 0a7cf2b347cb8cf1627faafd0ac8da03ad565905c58d07c486e5b868a6ff56be |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_exact_first_review.md | 182c1c6318b24f2cd88247cfff50c9d8465946de41e4ffbea2714429d52b35b1 |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_proof_read_after_review.md | a106c640f48154a7dfaebf418fc43ba9c44380e432e47da49002b7f0962157d7 |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_final_section_review.md | a657ddaa05ff7dbd5cb0b9778256cd6ef4e68dd2b798dff0662894f2028fd950 |
| history/source/notes/unrelated_machines/multiwitness_shared_job_fee_code_review.md | d216022cbb61cd0222d470b3f2085e70d6bf1d3c6f005d391a33102646302585 |

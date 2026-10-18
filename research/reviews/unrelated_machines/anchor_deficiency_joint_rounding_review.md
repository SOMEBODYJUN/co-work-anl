# 锚点缺额联合舍入的独立重构与冻结攻击

范围：UM-ANCHOR-DEFICIENCY-JOINT-ROUNDING-v1、UM-ANCHOR-DEFICIENCY-PROMISE-APPROX-v1。限定结构/承诺类，非一般 UM 完成。

## 实际被审对象

- 正文 `research/current/unrelated_machines/anchor_deficiency_joint_rounding.md`，SHA256 `dd2e88af7ef222d0eecfd8ed0b1ac3c10f6da8ca41ae7c5f4ca46333c91ea779`。
- 给定LP见证审计 `tests/audits/unrelated_machines/anchor_deficiency_joint_rounding_audit.py`，SHA256 `dbf9fcafd36a9b86d10bdda5f372d543188006ddeaf6c372b38b285252f3204a`。
- 冻结结果 `evidence/runs/unrelated_machines/anchor_deficiency_witness_audit.json`。

## 已发生的独立数学工作

内部研究者 anchor_selection 先重构饱和匹配、可变占位、最小Hall blocker，并给出一次LP+阈值匹配+tiny ST。独立研究者 global_repair 在未读其稿时只收到完整精确声明，独立推出低q总删机质量<1、Hall、全机负载与有理LP双证书。其后实际读最终正文；读前/读后hash均为上列正文hash。两者均按用户指定 GPT-6.1-sol ultra 推进，boss亲自核公式与实现，不按赞同票升级。

冻结全文攻击覆盖：strict < cutoff与d=0、任意多分量及tiny跨分量、一份联合x只做一次ST、α<1/2用途、β0/零任务、域外OUT-OF-CLASS；弱OPT witness仅约束所用边、成功分支无需anchor下界、仅上截接受性单调、删边保全部顶点的缺额求和、原分母积Q的网格/二分次数/有理位长、承诺域FAIL含义。

最初几何网格方案被更强的仅上截整数二分取代；最终攻击实际审了更强版本，没有将旧版审查冒充新版。§11给定D的最小blocker推广也已核，未假定求最大cocircuit的免费oracle。

## 结论与实测范围

没有仍成立的fatal objection。普遍结论依据自足推导；root Fraction仅核三个给定联合LP见证（跨分量/异质饱和/严格删机且300位分母）、锐cutoff等号及零/空边界。未实现一般LP后端、没有运行整个unknownOPT求解器，也没有将有限tests当一般证明。标准Hall/LP/ST机制不认证新颖性；外审未记录。

# 承重证据与精确数值摘要

本 support 只列本轮实际读取、可复核的承重事实；程序输出与数学量词分开。

## 固定非 PNE 见证

输入 `archives/customer-attraction/tools/evidence/nonpne-fixed-policy-primary/original/nonpne_best.json`（SHA `a4a5d9f5b8045915bef2339e2205975e3a4a8d8592d31c5e00dd7d491cfbe0b1`）的 18 个类型重数总和为 1,992,009，`players=5`、`topics=7`、`terminal_counts=[2,0,0,0,1,0,2]`、实际叶为 `00466`、`nonpne_deviation=[4,0]`。

独立固定点审计 `fixed-witness-audit.json`（SHA `ffe6d60b59a9d28a87511573bc250adb87f4f5beeb9e60160a550454d27cc70a`）报告：

- 2,801 个有序历史；19,607 项含自身比较；16,806 项非自身比较；16,558 严格正，248 平局，最小非自身 slack `0`；
- 实际收益 `(251678,251678,248928,248858,248858)`，`W=1250000`，`OPT=1992009`，`exact_ratio=1992009/1250000`，`half_margin=507991`；
- 静态冻结偏离 `4→0` 的 old/new payoff 为 `248928/250178`，gain `1250=W/1000`；真实续局叶 `[0,0,0,6,5]` 中偏离者 payoff 仍 `248928`；
- `passed=true`，且本次审计未导入作者包、未运行 solver、LP、BI 或随机搜索。

`exact-ic-data.json`（SHA `0df2e8bb296f9ae0df554ba2d7df1cfdbd0abfb5a4f6963048dfd7274e3af21b`）以 scale 60 的整数收益保存 276 个去重 payload，并按深度索引全部 2,801 个历史；它不是只保存最小 slack 的摘要。

## 程序合同与有限探针边界

程序正文 SHA `20066b9c2ef8ec6f3e78412fd2a2d1835a858b2d98e7470a46cc6c60f8e1ca3d`，入口 SHA `89e5b85efeb795c551d73c8a4d5c341583f43a1af8df18ea5314665f900aaba6`，实际 Engine SHA `766ae31b8049acb3483ae1a0939a3a7030b62236bcff8a74bb6ab36c8177c6d6`。Engine 用浮点 `R(k)` 提案、有限 `J` 的 LP、活跃行有理恢复，再由完整策略 verifier 做固定点检查；它没有枚举所有 σ、所有 J 或所有非极小可信续局。

原 run SHA `a0f93e5637e0c5dffaf04e95e69fcf948186ab920624924489028a1fa8842c4d` 的参数为 steps 1500、m 5、p 7、seed 2026102107、g 1000；记录 16 个去重锥、21 个候选端点，1484 个 step 的 `root_nonpne=0`。`record-analysis.json` 的 SHA 未作为输入 pin，它只是可逆视图；“有限探针、未保存其余15完整见证”以原正文合同为准。

## 静态平滑桥

资源正文 SHA `6c820d65b20837733a798635da97272e2e6c65ec4d8c65b166fec9b2d0f06f4a` 的完整静态层是
\[
W(a)+\sum_i u_i(O_i,a_{-i})\ge OPT_m,
\]
再由静态 PNE 的冻结 IC 给 `OPT_m≤2W(a)`。其三人真实续局表给 `A={a}, B={a,b}, C={b,c}`、实际 `CAC`、静态中间偏离收益 `4/3`、真实 `CBB` 偏离收益 `5/6`；因此 SPE 真实 IC 不能支付冻结 SM 项。其额外预算只推出 `OPT≤3W` 级粗界，未闭合 half。

## 关联代码契约

模型实现 `model.py` SHA `ac28fc1a3837954ab9b8fc658701f53aecf0a1da059e316158aab7565dc5f6a8` 保留标签别名、空覆盖、单位客户重数和 Fraction 收益；`exact.py` SHA `a4c76d77fd6c8d18ac668ce2070a65f927d9dca6bbe3cdd36f467d1598b4a892` 的 `R(k)` 递推是全集语义但本轮没有作为程序探针的运行后端；`certificate.py` SHA `a269b532260b537e67879eba609ef23e046e8f7303458ecf11271c4673aecc45` 逐有序历史计算给定策略的真实子树 IC。

Deferred 正文 `CA-STRATEGY-CONE`（SHA `ae4bcfd424eca8d4e3d79965f72182c0b2c8eefb72e74b44c2521b519f7aad39`）支持固定 σ 的 Γ 锥解释，`CA-EXACT-PURE-SPE-ALL`（SHA `667d6f319b1f325bd32538f6b0e5a8e95c1942e2ec97cbc76d7cbaef06b36954`）支持全集递推；两者的全称量词不由本有限运行支付。Deferred 固定见证正文 SHA `addbe8021888b92a6822628afaeef7e2e6b751c8b35e31721e16bf178263389c` 与本固定审计数值一致，但该对象仍只是有限端点。

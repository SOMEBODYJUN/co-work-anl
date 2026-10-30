# 单正小端级联的完整查询立方体：实际审查与证据

Claim：`UM-SINGLE-HOME-CASCADE-QUERY-SEPARATION-v2`。日期2026-10-18，boss11/root负责最终核对与Git，内部agents未登记独立Work身份。

独立审查者先仅从Exact重构直接机器弧图证明，之后读v2冻结Exact与作者的单位匹配增广路证明，两条路线均闭合。root亲读并核所有原job分割、同home多query、跨查询home、无根圈、Z零端、全子集与δ(S)及费用。最终canonical又经独立组合审查；该时刻软件pending，冻结记录如实保留。

其后root审读实际代码并运行14机器14任务的完整例子，按输入显式列出的8种查询模式逐机Fraction核验。非query支持费分别34/7/17，总58≤σ1对应费100；无根fee环42被丢弃。峰依次1、19/16、9/8、1、17/16、9/8、9/8、1。给定S={q1,q3}接口也实际运行，完整原分配峰9/8。代码拒绝覆盖已有输出；root只创建一次新的冻结运行。

没有standing fatal。结论是这个严格normal form的全部模式族；一般双见证新定理只保单query，不据其冒称这里的全子集输出。两个strict见证是输入，不能当一般UM最优求解。

Canonical：[现行正文](../../current/unrelated_machines/single_home_cascade_query_separation.md)。证明完成、内部审查完成；外审/新颖性未认证；主目标正反面未升级。

## 冻结读取对象

下表SHA针对实际原字节，读取顺序/独立性详见相应记录；入main不是数学升级。

| 文件 | SHA256 |
|---|---|
| `history/source/notes/unrelated_machines/home_cascade_query_v1_exact.md` | `92bf02bfeb64b4a7518efd54bdfbb7713b7938211d715b269a84e7bbf6455e41` |
| `history/source/notes/unrelated_machines/home_cascade_query_v1_proof.md` | `ba7f99b8b2ebd3909eaf7b5a778707e2444959e2230184716dceb261c31c79b9` |
| `history/source/notes/unrelated_machines/home_cascade_query_cube_v2_exact.md` | `975f43d6c5708a3c37f1fb4675ddc1c108856d3306f6186e376d6e2981d879d3` |
| `history/source/notes/unrelated_machines/home_cascade_query_cube_v2_author_proof.md` | `bd3b1a40f5f260406bd7611d0a4b0e323589ee4a6154129133d66402ff06e9ae` |
| `history/source/notes/unrelated_machines/home_cascade_query_cube_v2_independent_review.md` | `af8b3989464f8a384e12c3fbb06b23d847aa193f622cae518fb6f98f778326ce` |
| `history/source/notes/unrelated_machines/home_cascade_query_cube_v2_final_composition.md` | `fb31107fd874d672daf884f4acee31c51111e339a93ea024b36335299fe669c8` |

## root实际复现

```sh
python3 tests/audits/unrelated_machines/single_home_cascade_query_separation.py --input examples/unrelated_machines/home_cascade_query_patterns.json --output <不存在的新输出路径>
```

本次实际新输出：`evidence/runs/unrelated_machines/single_home_cascade_query_patterns_v2.json`，内含实际命令、输入/代码SHA、Python版本、完整原任务分配、全机负荷及有限范围。审计代码SHA：`c52eb5be01a64e7d13f1e80a7ad1cb5711ed187f0a8ad1000269847d004d59cd`。

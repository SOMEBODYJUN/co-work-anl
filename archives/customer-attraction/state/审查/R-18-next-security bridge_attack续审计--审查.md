# R-18 next_security bridge_attack 续审计

## 来源与实际执行

本页处置七源：`677b5324b53f63f8cd9f`（menu_cone_search.py）、`423203c961a00083c5af`（menu_test.py）、`cfaa71f29b5816a3f457`（distinct-34query MILP 输出）、`952532985a9ea2df7d3a`（distinct-uniform MILP 输出）、`c20b147f166ad055a93b`（repeated-uniform MILP 输出）、`b10e4b71128db5d92d16`（search.py）和 `76999021c12a81468d52`（security_milp.py）。原文字节和运行记录在 `archives/customer-attraction/tools/evidence/R-18-next-security-bridge-attack-continuation-20261031/`。源 SHA-256 依次为 `cf86004d524b809a4f8bc1d7d72a3d75836d10698592a6db4ace1b577b148dc0`、`f4578212aff7ca05b1572f1a0a8be4b7aafe6a9cea7d6cf899763622575793d3`、`dd0c0b9de10557e2848cda9bc2d36bb4165251147e2a6787468e733ba78bf5a5`、`5893f666003e0272c9f0e29d9bebf7cb826209f956976e5e4bd8ff1f7292817a`、`0f34a7d92a713d6c3c26e191618c3a80fa5bbe28ebb04f78e495c4c00b43131d`、`8032fd6816cca78da286bd22d3308b74b7ec61610a62f57f5533083a31765cc6`、`7bd7f177bb129ccfee9cab5a77d8ef24d6a90162cc67fc979ba48bbfa64294ba`。

## 数学对象与边界

`menu_cone_search.py` 在 Oracle 的完整计数层上生成一个固定 Markov policy cone，但 `wopt` 只把实际路径的 first-deviation 菜单放入 LP；源码自己声明“not full BR”。实际以 k=7,m=5、seed185、1 iteration 回放，得到 `BEST ... gap=-0.0`、`DONE 1 -0.0`。这是 on-path menu 的有限零结果，不是全历史 security 结论。

`menu_test.py` 把冻结完整策略映射到已提供的 examples/certificates，构造实际路径的所有一次偏离菜单并求共同菜单 cap。当前可用的两个输入实际得到：`root_tax_failure` 的 `W=38`、菜单大小3、`m cap/W=0.9473684210526315`；`individual_security_failure` 的 `W=32`、菜单大小5、`m cap/W=0.9270833333333334`。它们都低于1，只能说明这两个固定策略的 menu cap，不覆盖其它 CAG SPE。

三个 MILP JSON 都是 `k=6,m=3,path` 的固定查询输出，变量580、约束4459，目标浮点均约 `1/3`：distinct-34query 和 distinct-uniform status=1、55秒 time limit，dual bounds 分别约 `0.393610` 与 `0.363636`；repeated-uniform status=0、dual bound等于 objective。三者都显式写 `bound_is_not_a_proof=true`，不能把浮点根界或 time-limit 输出当作安全证书。

`search.py` 是 count-cached SPE outcome-set + static minimax 的随机发现器；实际 k=6,m=3、2 iterations、seed0 退出码0，输出 `DONE ... best=0.0`，无候选。`security_milp.py` 是完整历史 MILP discovery；实际 k=6、路径012、均匀 query、2秒限时退出码0但 HiGHS status=1，floating objective `1/3`、dual bound约 `0.435606`，并明确 bound 非证书。

## 处置

这些源共同增加的是“固定 first-deviation 菜单、随机 discovery 和有限 MILP 的真实运行边界”：没有正 gap 的 exact full-BR 反例，没有完整跨策略 safety 证书，也没有 Q-CAG-HALF 反例。保留 source 输出的 time-limit、依赖路径和 on-path 限制；第三阶段可把菜单 cap<1 与浮点候选作为诊断，不能升级为一般定理。

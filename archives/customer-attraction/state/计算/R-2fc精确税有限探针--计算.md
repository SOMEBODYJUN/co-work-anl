---
id: customer-attraction/r2fc-exact-tax-finite-probe
type_tag: 计算
kind: computation
title: R-2fc 实际分数负载税桥的有限完整SPE锥探针
status: finite-probe-retained
truth_status: finite-no-hit; auxiliary-bridge-unproved
scope: 固定 p=6、m=4/5 的随机有限完整纯SPE证书与其全有序历史偏离锥；不覆盖所有实例或全部纯SPE
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_root/exact_tax_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_root/exact_tax_scan_m4p6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/round3_root/exact_tax_scan_m5p6.json
evidence_packet: ../../tools/evidence/R-2fc-round3-root-20261031/
related_objects:
  - ../反例/五客户无拥挤SPE负载桥障碍--反例.md
  - ../反例/三人碰撞自由族福利障碍--反例.md
  - ../障碍/九客户二层占用探针的精确障碍--障碍.md
---

# 对象和量词

探针测试一个比普通占用函数更强的实际分数预算接口。对完整有序历史纯 SPE 的终局客户负载 (c_x)，令

\[
\alpha=(m-1)/m,\qquad g(T)=\sum_{x\in T}\frac1{1+\alpha c_x},\qquad G=\sum_{c_x>0}\frac1{1+\alpha c_x},
\]

候选桥为 (m\max_T g(T)\le W+G)，其中 (W) 是实际覆盖客户数，(T) 是一个查询主题。源程序的量词是：从随机非空掩码客户权重生成一个有限共同目录实例，调用 `ExactSPESolver` 选一个完整策略结局，再随机选择证书中的动作/续局平局；固定该证书后，对所有长度小于 (m) 的有序历史和所有非规定动作建立 IC 差行，最后在这些行定义的浮点锥上解 LP。

正 LP 候选才进入有理逼近、整数缩放和 `verify_certificate` 的精确源模型验证；若没有正候选，程序只写有限扫描报告。代码遇到 LP `status==3` 会报错，说明它不把意外无界当作无反例证据。

# 三个冻结源的读数

`exact_tax_scan_m4p6.json` 固定 (m=4,p=6,mathrm{seed}=2026102171)，含 40 个 trial；每个 trial 记录一个 outcome 和 1295 行非自身偏离，`status=finite_probe_only`，最佳目标值为 (-1/4)。`exact_tax_scan_m5p6.json` 固定 (m=5,p=6,mathrm{seed}=2026102172)，含 50 个 trial；每 trial 有 7775 行偏离，trial 35 保留两个完整 SPE outcome，其余 trial 一个，最佳值为 (-1/5)。冻结 m=4 报告只跑了 40 次，不能按代码默认 50 次复述。

历史数来自

\[
\sum_{k=0}^{m-1}p^k,
\]

所以 m=4 时 (259) 个有序历史乘 (p-1=5) 个非自身动作为 1295；m=5 时 (1555\times5=7775)。这两个报告均未生成 `exact_tax_failure_*.json`，意味着在其固定随机证书集合上没有进入正候选的精确重构分支。

我在独立副本中对原程序做了 `py_compile`，并用同一依赖下运行 m=4 两 trial、m=5 一 trial smoke；两次均退出 0、stderr 为空，输出首 trial 仍为 `best=-0.25` 与 `best=-0.2`，没有失败 JSON。证据包保存了完整 stdout/stderr、源指纹、重放与验证结果。

# 可确立的用途与缺口

这批源保留了一个清晰的“发现—精确核验”接口：未来若 LP 找到正值，程序会把有理客户权重、完整策略和逐历史证书写出并重新调用验证器；当前有限 no-hit 只能说明上述两组固定参数、随机种子和所选完整策略锥中未找到违反点。它不证明候选桥，更不证明六人或任意人数 (2W\ge OPT)，也不构成低福利完整 SPE 反例。

此前五客户、碰撞自由族和九客户二层占用障碍都说明若干更简单的负载/势桥会失败，但本探针改变了权重函数和搜索对象；这些对象之间只能建立“辅助路线的相邻检验”关系，不能把有限 no-hit 当作成功闭合。空主题、重复、零客户、离轨历史和任意平局均不因该随机实验被删除。

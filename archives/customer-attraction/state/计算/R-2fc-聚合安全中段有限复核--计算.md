---
id: customer-attraction/r-2fc-aggregate-security-mid-limited-replay
kind: computation
type_tag: 计算
title: R-2fc 聚合安全中段入口有限复核
status: replayed-source-entry; finite-floating-only; enlarged-model-not-CAG
truth_status: reproducible execution metadata; no exact theorem or CAG certificate
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_potential_probe.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/individual_groups_n3k6.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-2fc8878b4bdd4328bbc1bcf1df8ca831/aggregate_security/dr_n5k3.json
evidence_packet: ../../tools/evidence/R-2fc-aggregate-security-mid-20261031/
---

# 入口与有限运行

`dr_potential_probe.py` 的 raw 源字节已逐一读取；保存的 evidence 副本 SHA-256 为 `fa9b84b296ae2c80eb126b9e7ed06bcea2a3011e887816402c8b6bcc1a75015f`，与 inventory 一致。入口在扩大 DR marginal-potential 模型上构造 numpy/scipy `linprog`，把 `Phi(q)-Phi(q-e_a)` 当作 utility；其模块说明明确写出这不是 customer-attraction input class。

为保持检查有限且可复核，运行了三条命令并保存完整 stdout/stderr：

1. `--k 3 --n 3 --trials 1 --seed 22101 --no-dr`：退出 `0`；stdout `{"completed": 1, "best": 0.0}`；stderr 为空；输出 status 仍为 enlarged/floating/not CAG。
2. `--k 3 --n 5 --trials 1 --seed 22103`：退出 `0`；stdout `{"completed": 1, "best": 0.0}`；stderr 为空。它对应 `dr_n5k3.json` 的参数族，但把 500 trials 限为 1 以进行快速复核。
3. `--k 6 --n 3 --trials 1 --seed 22112 --policy groups --first 1`：退出 `0`；stdout 先报告两个有限 objective（`-0.0025252525252525263` 和 `-0.002645502645502644`），最后报告 `{"completed": 1, "best": -0.002645502645502644}`；stderr 为空。该结果与 `individual_groups_n3k6.json` 的 objective、root `[0,3,4]`、query 近似四等分 witness 一致。

证据包的 `run/commands.txt`、`run/*stdout.txt`、`run/*stderr.txt`、JSON 输出和完整脚本保留了实际命令、退出码、标准输出、标准错误与结果字段。没有运行更大试验，也没有用 LP 的近零结果替代有理证书。

# 复核失败机制与比较

八项 `clean show` 均先实际调用，但当前 clone 是 promisor checkout，缺失 blob 触发对 `https://github.com/SOMEBODYJUN/co-work-anl.git/` 的 fetch；browser-proxy 端口 `8889` 不可连接，因此每项退出 `1` 且无输出文件。raw 浏览器读取随后成功，故“clean show 失败”与“正文已实际读取”分别记录，不把 inventory 元数据冒充源正文。

旧十源资源、尾部六源计算对象和精确障碍对象均被读取并用于比较。中段八源的新增内容只有五人随机诊断、首位个体预算、plateau/monotone policy 参数行以及源码入口的有限复核；没有新的整数势、静态原/对偶安全值、support 不变总收益或客户类型。已有 `P=161,v=56` 障碍仍明确标为 enlarged-model/not-CAG，故这些浮点行不能推出或否定六人 half。

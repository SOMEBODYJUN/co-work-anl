---
source_id: 9a2fcf936eefd8d2c1db
source_path: examples/unrelated_machines/nearflat_moment_inputs.json
source_sha256: f5b35bc248500d8986f7fb9b58e427c0c6cc9194ec6a9a879789eaa5f78f4b3f
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/近平坦HS矩提取与负接口有限审计--审查.md
---

# 近平坦矩输入夹具的语义清洗

## 来源身份与合同

这是一个 3,510,935 字节的 JSON 输入夹具，不是调度证明、求解器输出或通用矩提取器。冻结源版本来自 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，内容 SHA-256 为 `f5b35bc248500d8986f7fb9b58e427c0c6cc9194ec6a9a879789eaa5f78f4b3f`。

顶层合同明确是 `C2-load only`：输入只承诺 degree-four Boolean/one-hot moments、二阶矩 `M2` PSD 和 degree-one row-load localizers PSD；没有 prefix-count 或逐元素 fourth-moment positivity 要求。`jobs` 把有限机器标签映射到非负有理处理时间字符串，缺省端点表示无穷；`variables[e]=(machine,job)`，矩的 monomial 使用 edge index。`generating_distribution` 只作来源证明，后续 greedy/HS 消费的核心字段是 jobs、T、variables、moments 和 eta。

## 六个夹具的完整结构

逐项解析得到 6 个 case，所有 generating-distribution 权重和均为 1；每个 moment monomial 唯一、按次数/字典序排列，常数矩为 1，所有值是有理数字。六项的结构如下：

| case | jobs | variables | moments | (T) | (eta) | distribution atoms | degree counts |
|---|---:|---:|---:|---|---|---:|---|
| `three_point_flat_eta_half` | 10 | 20 | 4521 | 1 | 1/2 | 3 | 1+20+180+960+3360 |
| `rare_fourth_eta_half` | 10 | 20 | 4521 | 1 | 1/2 | 4 | 1+20+180+960+3360 |
| `rare_fourth_eta_tenth_zero_job` | 11 | 21 | 5682 | 1 | 1/10 | 4 | 1+21+200+1140+4320 |
| `rare_fourth_large_denominators` | 10 | 20 | 4521 | 超大有理数 | 1/10 | 4 | 1+20+180+960+3360 |
| `all_zero_T` | 4 | 8 | 81 | 0 | 1/10 | 4 | 1+8+24+32+16 |
| `uniform_nonflat_rejected` | 10 | 20 | 4521 | 1 | 1/10 | 4 | 1+20+180+960+3360 |

六个夹具的 moments 都由各自的 generating distribution 逐 monomial 精确重算得到，全部无差异。该检查确认输入内部自洽；它不证明下游 HS 充分条件，也不证明任意 unrelated-machines 实例可生成相同 moments。

## 与既有 near-flat HS 审计的关系

现有 `nearflat_moment_extraction_audit.json` 的六个 case 与本输入逐项同名；jobs 和 fixture distribution 全部字节级字段一致。下游审计的五个 certified actual schedule 与一个 `uniform_nonflat_rejected` 分支因此有明确输入来源：前五项是给定矩夹具上的 exact Schur/PSD 与实际调度证书，最后一项只是 trace defect 超过充分阈值，不能解释为不可行性证明。

本输入本身不带下游的 `result`、rank、trace defect 或 `certificate_rejected` 字段；这些结论只能引用对应审计输出。相同地，`generating_distribution` 是 provenance，不应被误读为一个从任意输入自动恢复支持的算法。

## 处置和边界

建议将源标为 `integrated`，复制到 `archives/unrelated-machines/tools/evidence/nearflat-hs-interface-20261030/`，并把源引用及哈希补入既有《近平坦 HS 矩提取与负接口有限审计》。它的独有贡献是六项下游审计的完整 moments/jobs/variables/distribution 输入合同；不新建第二个 near-flat 对象。

它不提供通用 near-flat 分布生成器、moment-to-support 解码、SDP/LP 真实性验证器或任意输入的调度近似比。不得把 finite pass/rejection、输入夹具自洽性或六组参数外推成一般定理，更不能与 customer-attraction 六人 half 模型混合。

验证命令和本地证据：

```sh
python3 tools/cleanup.py --repo . show 9a2fcf936eefd8d2c1db --out cleanup/workspaces/Boss5/nearflat_moment_inputs.json
sha256sum cleanup/workspaces/Boss5/nearflat_moment_inputs.json
```

本次另外用 `Fraction` 逐项重算六个 case 的 moments，检查 4521/5682/81 个 monomial 的全部值，并核对下游审计的 jobs 与 fixture distribution；没有运行未提供的通用求解器。

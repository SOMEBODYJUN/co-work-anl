---
source_id: 336b9d755a7d2cddea33
source_path: examples/unrelated_machines/private_tree_branching_valuation_examples.json
source_sha256: f63823f65df9c45d23df6340a658c5e3bbccb92a32ab02484e774f3bd8659d78
status: ready-for-parent-review
recommended_disposition: integrated
recommended_target: archives/unrelated-machines/state/审查/私有树估值与签名价格有限审查--审查.md
---

# 私有树分叉估值输入夹具的语义清洗

## 来源与范围

该 JSON 在 legacy-cleanup 与 main 两个冻结提交中相同，大小 13,582 字节，源 SHA-256 为 `f63823f65df9c45d23df6340a658c5e3bbccb92a32ab02484e774f3bd8659d78`。顶层 schema 为 `private_tree_branching_valuation_inputs_v1`，声明七个实际输入；完整输出、树证书和计数由冻结的 `private_tree_branching_valuation_audit.json` 承载，本输入文件没有复制这些输出。

源声明的三个对象是：`UM-PRIVATE-TREE-Q-VALUATION-v1`、`UM-TREE-Q-XOS-ENVELOPE-v1` 和 `UM-TREE-Q-MINORANT-LP-v1`。因此它是既有树估值对象的输入合同和有限边界夹具，不是新定理、通用 LP 求解器或新的 unrelated-machines 全局结论。

## 七个输入及实际内容

前三个 `shared-states-signed-prices-0/1/2/3` 都是 (k=2,h=2)、7 个资源、2 个共享状态的 signed-price 输入。其价格依次为全零；六个价格为 2 且最后一项为 (-1/3)；
\[
(-2/3,1/3,0,4/3,-1/3,1,-2/3);
\]
以及六个极小正价和一个同尺度负价。它们覆盖全零基线、明显负资源信用、混合正负价格与接近零的符号边界。价格在输入中是有理字符串，不能把这些向量当作统一优化输出。

`unary-deep-negative-unused-resource` 是 (k=1,h=30) 的深 unary 树，3 个资源、2 个状态，专门保留“负价资源未被候选子树使用”的边界。`non-XOS-three-ary-height-two` 是三叉深度二的具体输入，用于既有 non-XOS 证书；它不证明所有树估值都非 XOS。`compact-LP-data-and-feasible-uniform-support` 是 (k=3,h=2)、9 资源的紧凑 LP 数据及一个可行 uniform support；源对象明确不等于通用 LP 最优化。七项共同说明输入层确实覆盖了 signed prices、负资源、non-XOS 与 compact-LP 边界。

## 与既有审查和证据的关系

既有 `私有树估值与签名价格有限审查--审查.md` 已读取相同树估值审计输出，记录 800 个显式叶子子集、901 个实际树证书、7 个包络实例、21 个查询、8 个 compact LP certificate、408 次次可加 pair、52 次 full-subset separation 比较、24 个 signed-price 向量、1 个 unary deep boundary、1 个 non-XOS certificate 和 9/11 个 reject 分支。该审查还明确 `generic_LP_optimization_implemented=false`、负价和 non-XOS 不能升级成一般结构定理。

本输入的独有贡献是把上述七类输入的树、状态、资源、价格和 LP 字段完整保全，并给冻结 audit 一个可追溯的源版本/哈希身份。应在既有审查和 `private-tree-valuation` evidence manifest 中补入本源路径与 SHA；不新建第二个估值对象，也不把输入夹具误读为 audit 输出。

## 处置与边界

建议 `integrated` 到既有私有树估值与签名价格审查，并复制至对应 `tools/evidence` 输入目录。后续若重放，只能引用冻结 audit 的实际输出；本输入本身不能证明树递推、XOS envelope、minorant LP 或任意 (k,h) 的全称结论。多状态共享资源、generic LP、任意 sink law 和全局调度耦合仍按既有定理与审查中的开放缺口处理，不与 customer-attraction 六人 half 模型混合。

读取命令：

```sh
python3 tools/cleanup.py --repo . show 336b9d755a7d2cddea33 --out cleanup/workspaces/Boss5/private_tree_branching_valuation_examples.json
sha256sum cleanup/workspaces/Boss5/private_tree_branching_valuation_examples.json
```

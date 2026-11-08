# Boss7 首轮范围比较与处置建议

本目录是 `Boss7` 对三个仍由 `Boss2` 持有包的只读复核与候选草稿。没有修改官方任务 JSON、`research/registry.json`、正式 batch/receipt，也没有执行 claim/done/checkpoint/push。

## 0002（customer-attraction）

- 任务冻结 41 份材料；本地 `Boss2/0002/partial-batch.json` 只有 19 个候选对象、14 个材料记录，不是可发布批次。
- Boss2 `handoff.md` 明确：连续实读的是零基 0–12、20、34、36 加共享定义；其余材料没有全文实读。零基 34 的三条既有付款主对象、零基 36 的两个既有反例应走 attachment/定向接证，不应冒为新对象。
- 本复核逐字节核了 41/41 冻结 SHA；候选映射 13 份，其他 28 份显式 `deferred`。19 个候选 ID 当前均不在 canonical registry；其中 `CA-AGGREGATE-LAST-FLOOR-NO` 与 `B10-IID-SUPPORT-AVERAGE-NO-v1` 的 handoff 明示需与 0001-5-evidence、0056、0069 以及另一执行线去重后才能接收。
- 0002 候选中的“全尾真实查询行”正文自承：ROW 恒等式已证，但 `RETURN` 与 `MIN-ROW` 仍 open；负去相关反例不能倒填为 half/ROW 反例。`r=2` 倒二行已证，早期行仍有符号返还缺口。

## 0094（positive-kernels 等多档案混合批）

- 任务冻结 51 份材料，跨 fair-allocation、local-potential-games、matching-faces、matroid-structures、positive-kernels、resource-activation、robust-optimization、unrelated-machines。
- `Boss2/0094/pk-fragment.json` 与 `build_pk_fragment.py` 只声明完整实读零基 23–29 的七份 positive-kernels 正文/审查；其余 44 份没有在该 fragment 中形成去向。
- 本复核逐字节核了 51/51 SHA；fragment 的 8 个对象（4 个 PK 已证/定义对象及 4 个 open/representation 对象）全部已有 canonical object ID，应作为 attachment/owner route，不能复制主记录。所有未读材料保留 `deferred`，不因同一档案名而推导数学身份。

## 0102（unrelated-machines）

- 任务冻结 42 份材料。`Boss2/0102/root-fragment.json` 有 8 个对象且 `materials=[]`，其 reading note 明说 M0–18 为 root read、M19–41 只部分/定向；`resume-review/closed-cycle-correction.json` 对闭环弱局部障碍补了一个修订对象和单任务逃逸阈值对象。
- 本复核逐字节核了 42/42 SHA；候选草稿合并 root 与 correction 后保留 9 个对象，所有未映射材料显式 `deferred-or-partial`。修订对象替换 root 中同 ID 的过强“必须新 tiny”表述：正确量词是必须激活一个原未激活的完整环；`UM-CLOSED-CYCLE-SINGLE-JOB-ESCAPE-THRESHOLD-v1` 需与 0105/0081 已有路由先去重。
- independent-review.md 明确 M2 私有汇点、M17 高阶尾概率、M4 闭环、M29 LS 锥双极号、M30 固定 K2 公式和 M40 整比双尺寸均有定向纠错；不能把 root fragment 当完整交付。

## 生成文件

- `audit.json`：每个冻结材料的 path、frozen SHA、实际 SHA、字节数、行数、标题/章节索引、候选映射、阅读状态和未决原因；每个候选对象的 body/evidence path+SHA+section 审计。
- `candidate-0002-batch.json`、`candidate-0094-batch.json`、`candidate-0102-batch.json`：仅工作区草稿，均 `schema: 2` 且 `edge_files: []`。
- 对应 `candidate-*-receipt.json`：明确 `local-candidate-incomplete-not-pushed`、资产 SHA、审读范围、延迟材料和不得发布限制。

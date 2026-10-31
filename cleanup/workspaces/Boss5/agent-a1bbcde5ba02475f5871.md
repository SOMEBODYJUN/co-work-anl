---
source_id: a1bbcde5ba02475f5871
source_path: history/research_operations/customer_attraction_transition/original/research/weighted_congestion_frontier/prompts/PRO_ATTACK.md
source_sha256: 1b215a8df0645dbf7487b5e371810c9f5f1173fa592b163be52c236e47939eaa
source_blob: 184346cbe5884beb514fe679ae1a56b0345bfdcf
source_size: 2108
source_commits:
  - 68fad804ec5946cb296f77dc5b336308a66abf12
  - aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c
proposed_disposition: integrated
proposed_target: archives/weighted-congestion/state/资料/接题来源映射与文献导入的版本边界--资料.md
---

# 实际读取

通过 `python3 work.py clean show a1bbcde5ba02475f5871` 完整读取 2108 字节冻结 Markdown，并用 `clean list --owner self --full` 核对 blob、大小、SHA-256 和两个冻结提交。两提交内容相同，SHA 为 `1b215a8df0645dbf7487b5e371810c9f5f1173fa592b163be52c236e47939eaa`。

文件标题为“Pro数学任务：一般不相关并行机的统一常数突破”。它先把材料身份固定为 `UM-TARGET-v1`、存档 `unrelated-machines`，随后要求对一般 (R\|C_{\max}) 输入研究统一 \((2−ε) 目标：二进制非负有理处理时间或不可用边、每项完整不可拆分分配、机器/任务数可增长、允许空任务与 `OPT=0`，需输出实际分配并在总编码位长多项式时间内保证 \((2−ε) 近似\)。文件明确该目标仍 OPEN。

正文还规定：经典槽舍入和配置 LP gap=2 只是前人基线，不能从松弛 gap 直接推出一般算法或一般困难性；固定机器、受限指派、固定槽/见证、估值和准多项式结果必须保持各自范围；若转向困难性，必须写明复杂度假设和全量词；有限实验和赞同不代替证明；候选要注明失败边界并扣除已有定理后说明新增。

# 与现有材料比较

- 当前 `archives/unrelated-machines/README.md`、定义/问题对象和 `archives/unrelated-machines/state/资料/不相关机研究入口与文献状态--资料.md` 承接同一 UM-TARGET-v1 的精确输入、实际调度输出、统一 ε 和 OPEN 边界；本源是迁移时点的 Pro 任务合同，不是新的算法或反例。
- `archives/weighted-congestion/state/资料/接题来源映射与文献导入的版本边界--资料.md` 已保存旧 Pro brief 的 S0–S20 映射，并明确三种身份不可混淆：旧 brief、审查绑定的旧 task hash，以及当前结果分支同路径 443 字节兼容入口。本源 2108 字节、SHA `1b215a8d…` 是迁移目录的另一冻结版本；它不等于当前 443 字节 stub，也不等于审查记录中 `76b12f43…` 的旧完整 task hash。
- `archives/weighted-congestion/tools/evidence/pro-material-reviews/` 已保存旧 task 的字节/版本审查和当前 443 字节兼容文件，但没有本源这份 2108 字节过渡版；因此本源有真实 provenance 增量，应保留原件与 manifest，不能简单标 `duplicate`。
- 现有 `archives/weighted-congestion/state/资料/历史角色提示词三件套--资料.md` 只覆盖 CLEANER、EXTRACTOR、MODELS 三份角色/模型配置；本源是 Pro 的实际任务文本，提供完整量词与“证明/反例/候选/有限证据分层”合同，不能并入三件套而丢掉独立 source identity。

# 数学身份和不应外推的范围

该源含有完整问题合同和经典基线提醒，但没有算法、完整证明、真实整数 gap、代码输出、证书或外部文献核验。因此不由本源推出：

- 一般 (R\|C_{\max}) 的统一 \((2−ε) 算法不存在或存在；
- `P ≠ NP`、近二困难性、配置 LP gap 以外的全类下界；
- weighted-congestion、customer-attraction 六人 SPE 半覆盖或任何设施模型结论；
- 旧提示中的“目标仍 OPEN”在迁移后当前状态仍自动成立，或当前结果分支已经执行其研究指令。

它可作为历史任务入口和范围合同，提醒读者把实际调度、总位复杂度、复杂度假设、有限实验和证明区分开；数学真值必须回到当前 UM canonical state/review/evidence 对象。

# 处置与去向

建议 `integrated`：将 source refs、大小、SHA、历史两个提交和上述版本差异补入 `archives/weighted-congestion/state/资料/接题来源映射与文献导入的版本边界--资料.md`，原 2108 字节复制到独立 evidence manifest。不要将其写入定理/问题对象或第三阶段 `derives` 边；可建立“历史任务入口 → 当前 UM 入口/旧 Pro 版本审查”的资料关系。

当前迁移包的 `PRO_ATTACK.md` 443 字节兼容 stub、审查绑定的 76b12… 旧 task 和本源 2108 字节过渡任务必须保持三个稳定身份。后续若取得缺失的旧完整 task/ZIP，只能新增证据并保留本源事实，不能悄改本次实读范围。

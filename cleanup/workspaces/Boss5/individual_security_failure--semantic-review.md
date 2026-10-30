# `examples/customer_attraction/individual_security_failure.json` 语义清洗稿

## 来源身份

- 来源 ID: `46b1b3c7907ee8c886ce`
- 冻结 SHA-256: `bc5202502faa778fae402da4d74a4da8971ffa30bd712423147555b6e15a437a`
- 源路径：`examples/customer_attraction/individual_security_failure.json`
- 两个冻结版本：`68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）与 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）；内容哈希相同。
- 文件类型：JSON 输入夹具，不是证明脚本或独立结论报告。

## 实际读取和模型内容

JSON 给出 3 名顺序玩家、6 个主题 `X0,X1,X2,Y0,Y1,Y2`，以及 13 类客户兴趣集合和重数。总客户数为 34。将主题依次编码为 0 到 5，13 个掩码/重数为

\[
(4,1),(27,4),(29,3),(30,3),(31,2),(32,1),
(43,3),(45,3),(46,3),(51,3),(53,3),(54,3),(59,2).
\]

其中 4 与 32 是主题 2、5 的私有客户，主题 0、2、5 的并集覆盖全部 34 名客户。因此同一夹具支持 \(\operatorname{OPT}_3=34\)，但夹具本身不定义策略、收益、SPE 或静态查询分布；这些内容由另存的完整证书和审计程序解释。

## 与已完成数学对象的对应

该 JSON 是三人 34 客户逐人混合安全值反例的原始输入。现有对象已用相同客户重数、同一六主题策略和全部有序历史完成以下语义工作：

- 根选 0；首主题在 X 组时第二人选 3，否则选 0；末位在第二行动所属组选择尚未出现的最小组内主题。
- 该策略覆盖 43 个有序历史、258 个指定/偏离比较，实际路径为 \((0,3,4)\)，收益为 \((29/3,67/6,67/6)\)，福利 \(W=32\)。
- 静态安全值为 \(v_3=2411/246\)，根玩家收益为 \(u_1=29/3\)，故 \(u_1-v_3=-11/82\)。这否定“每位完整 SPE 玩家均有 \(u_i\ge v_n\)”的逐人桥。
- 同一实例仍满足 \(W-3v_3=213/82>0\) 与 \(2W-\operatorname{OPT}_3=30>0\)；后继补偿使总预算 \(W-\sum_i C_i=60/41>0\)。因此它不是聚合安全值桥或六人 half 目标的反例。

上述数值和全历史结论来自已冻结的 `evidence/certificates/customer_attraction/individual_security_failure.json`、`tests/audits/customer_attraction_individual_security.py` 及其 replay 输出；本次没有把 JSON 输入本身误读为独立重放。

## 与 360 客户候选和 34 客户正式对象的关系

JSON 是 34 客户最终夹具，不是后续 360 客户候选的输入。360 客户源改变同一形式策略的重数，用于历史搜索；它的安全值与福利边界另有独立证据。34 客户输入已经有完整反例正文和单位客户 Fraction 审计，因而不应新建第二个“34 客户反例”对象。该源的独有贡献是可复现的紧凑客户输入及其源版本/哈希身份。

## 处置决定

**建议 `integrated`，而非 `duplicate`。** 将来源 SHA 和两个 `source:` 引用补入：

1. `archives/customer-attraction/state/反例/三人逐人混合安全值--反例.md`（反例对象的原始输入）；
2. `archives/customer-attraction/state/计算/后继安全值与完整树精确审计--计算.md`（审计输入清单）；
3. `archives/customer-attraction/tools/evidence/continuation-security/source-manifest.json` 已经保存该路径与哈希，可作为证据入口。

不把 JSON 单独升级为定理，不宣称客户输入最小，不宣称它反驳聚合安全值、完整福利桥或六人 half。

## 验证边界

读取命令：

```sh
python3 tools/cleanup.py --repo . show 46b1b3c7907ee8c886ce --out cleanup/workspaces/Boss5/individual_security_failure.json
sha256sum cleanup/workspaces/Boss5/individual_security_failure.json
```

数学复现命令（已在既有证据对象记录并可从仓库根运行）：

```sh
python archives/customer-attraction/tools/evidence/continuation-security/tests/audits/customer_attraction_individual_security.py
```

该复现使用已保全的策略/证书资源，验证全历史与精确安全值；本 JSON 只是输入夹具，不能单独支撑上述数值。

# 来源迁移、分支清单与解释账本的原件和实际读取

4主源全部字段/条目/可见正文已实读，680解释通过187精确文字组去重保全，未额外done引用数学。原件不改。

| ID | 原路径 | bytes | SHA-256 |
| --- | --- | ---: | --- |
| `48efc2103c109f9bffd3` | [research/path_migration.json](original/research/path_migration.json) | 7217 | `2dbcc3539d2e1e1f007babe7fad281a4ed2c444fa19f86c48de7cc6cb5cf53c8` |
| `014668282ad7a97a0116` | [research/branch_cleanup.json](original/research/branch_cleanup.json) | 123785 | `f56832c364f40eb70b011c44157bdc5e881d68e21d80fe21593cec03ea9af449` |
| `5f719b81313dfcf26cb5` | [research/source_crosswalk.json](original/research/source_crosswalk.json) | 395476 | `f6017cabf428a34e8e79ebe5e15fd5c04f5d81ad9b64ff29ffd7bba7c680ca02` |
| `60a01a03bbce857246d8` | [research/source_crosswalk.md](original/research/source_crosswalk.md) | 457647 | `fc234ebf594f13473662266557a31835c00f916d7adfedf8a314050c0dce6f68` |

[source-manifest.json](source-manifest.json)含两完整冻结commit；[reading-scope.json](reading-scope.json)给606实读块范围及原件/相关/未读下游层次。

## 新有限检查与完整保留

- [inspect_ledger.py](inspect_ledger.py)：独立新代码，只读本包字节/冻结inventory，不执行旧模块、不用Git/网络。
- [ledger-structural-audit.json](ledger-structural-audit.json)：整个457647字节MD完全相等、680/187保留、530显式SHA和141归档预期元数据比对、路径引用。
- [json-field-census.json](json-field-census.json)：全部3主JSON的递归字段/标量/源SHA/digest。
- [normalized-records.json](normalized-records.json)：680记录全部原字段与187精确解释，组号不是数学身份。
- [execution-record.json](execution-record.json)：唯一新本地结构check和数学校正读取的范围。
- [write_resources.py](write_resources.py)：完整三资源表格与解释的作者辅助源码；不修改原件。

## 实际取消的额外补核

[cancelled-byte-binding-attempt.json](cancelled-byte-binding-attempt.json)保非TTY只读Gitcat-file补核exit130、stdout空/无结果和promisor/blob:none观察。是否补入过对象无法由现有输出判断；没有141bytePASS、没有认证或重试。原执行脚本在[preliminary-read-only/check_archived_blob_bindings.py](preliminary-read-only/check_archived_blob_bindings.py)，按失败原件保留，**不可当作已通过或直接重跑**；未来任何必要Git读取须显式GIT_NO_LAZY_FETCH=1并报告缺对象。主源4字节/语义完整与这个取消补核分开。

## 相关比较

[comparison-manifest.json](comparison-manifest.json)列12份实际版本和读取scope。两个当前正式iid反例全文读，N031旧弱桥文字只保历史并给当前明确纠正；旧4研究tip正祖先证据只复用、不重跑，shallow返回1不作缺历史结论。没有当前远端删除/secret重审/底层141数学或全部外部论文认证。

所有作者provenance/已证/独立措辞保留原时点，不成为当前权限、软件/外审/新颖性认证。原680Markdown全字节重构是表示绑定，不能替代这些数学证明。

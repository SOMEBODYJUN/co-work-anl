# Boss4 对称源10源本地交付

本批10份冻结来源均完成全文语义审查、相关比较、原字节保全与适当精确重放。全部新增文件仅在本地；未做Git写入、sync、claim、done或checkpoint。Boss统一处理保存与勾选。远端推送审批边界仍由Boss处理，不能把本文件或receipt称为已推送/已done。

## 正式正文

| 文件 | 稳定ID | 承担内容 |
| --- | --- | --- |
| `archives/weighted-congestion/state/定理/对称两列拓扑的单项式两攻击归约--定理.md` | `weighted-congestion/symmetric-two-column-source-reduction` | v3完整实域证明：非空稳定区间、左右分支、右N=1转换、弦替换/常数删除/单项式选择、sup比较、全部边界及版本纠正 |
| `archives/weighted-congestion/state/定理/三十二次两攻击源包络上界--定理.md` | `weighted-congestion/source-degree32-upper-envelope` | 全部n/k/实w/β≥0的89/50源包络上界，解析消元、有限域约化、完整Bernstein/叶覆盖证书及边界 |
| `archives/weighted-congestion/state/计算/对称两列与三十二次源证书的精确核验--计算.md` | `weighted-congestion/symmetric-source-exact-audits` | 三程序/三报告/完整证书的实际证据、范围、独立审查与真实报告差异 |

逐源记录为 `cleanup/workspaces/Boss4/symmetric-receipts.json`，共10项，均为integrated，targets仅指上表自足正文。数学正文与证据先按Boss流程保存后，才能由Boss统一done；我没有操作勾选。

## 证据与复现

全部新增资源在 `archives/weighted-congestion/tools/evidence/symmetric-source/`：

- `original/<完整原path>`：10份原件，不改字节。`provenance.json`保存10源ID、hash、blob和两个完整来源commit/path；逐文件SHA全部吻合。
- `replay_suite.py`：仅负责身份核对、隔离复制、执行及报告对照；不改数学程序，不写原件。
- `replay/`：三份原程序的执行副本、源证书副本、stdout、stderr及两套状态程序的结果；三次stderr均为空。
- `replay-comparison.json`：本机Python 3.12.14、各次命令、返回码、实际耗时、逐共享字段相等性及证书5个细分条目完整叶路径。

在仓库根复现：

```sh
python3 archives/weighted-congestion/tools/evidence/symmetric-source/replay_suite.py
```

本次三程序均返回0；作者套件约48秒，独立审查约5秒，源32约1.6秒。前两份结果与冻结JSON逐字段完全相同。源32的结论、1760多项式、1768叶、最大深度2、算术字段全部相同；耗时与历史1888ms不同，并明确记录。旧报告额外的日期、Python全文、旧工作室命令、PROOF.md hash及当时仓库map检查计数没有冒称本轮验证。

重要计数解释：作者套件144个输入、4948状态、28992不同翻位、720输入/倍率检查、17高倍率归约，触发非零平移计数为0；独立套件实际269个游戏输入×5倍率=原报告的1345 `games`，20400状态是按倍率重复计数，12次无PNE组合中10左2右，并有显式非零平移。两套都是有限输入实现检查。只有源32在解析约化后对每个实闭区间的完整符号证书承担全实域结论。

## 相关比较与关系判断

已全文比较两主证明、独立审查、3程序/3报告/全证书；另读crossover/separation与main_check的独立直接叶变换，读后续linear_degree_allstate_lower_bound完整一般构造和全状态覆盖，并比较正式闭端点、资源支持势对象。未替这些相关来源的owner登记完成。

新增对象的关系已在正文作了有条件解释：一般两列归约与源32上界联合给对称拓扑32次存在界；该存在界与crossover负责的非对称16态9/5无均衡例联合给分离。两主定理的稳定路径/ID已提前直接通知crossover，其对象路径为 `archives/weighted-congestion/state/定理/十四资源非对称例与对称两列拓扑的三十二次分离--定理.md`。未重复保存或登记其程序和16态证书，也没有阶段二直接改共享图。

旧全类OPEN语句已明确按后续每个d≥2^20的全状态d/10下界纠正；当前对象不承担该巨大构造的重新清洗，不以改善环替代全状态非存在。

## 局限与核对

未认证外部同行评审、全球新颖性或最优常数；拓扑归约只覆盖相同轻权和对称费用，不升级为全类上界，存在性归约不称单实例最佳倍率相等。源32证书不自动推广到其他次数。历史源证书的hash支持原件身份，不替代逐系数检查。

已本地校验3正文的Markdown本地链接全部存在，10个receipt ID唯一且所有targets存在并指正式state正文；完整证据重放通过。未访问或输出凭据，未改任何共享README或其他人的正文。无尚缺必需附件或未处理源项。

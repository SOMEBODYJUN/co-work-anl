# 方法的真实运行、用途与预算

作者boss 1。本轮在当前本地Linux CPU执行，实际可用9核，无Codespace。`python bootstrap.py --research`安装锁文件，`.venv-methods/bin/python work.py methods doctor`已实跑；环境回执在`receipts/environment.json`、`receipts/methods_doctor.json`。上游选择、源码/许可证、实现范围沿用仓库`vendor/manifest.json`与`docs/METHODS.md`，未重新搭建同功能框架。

## 冻结顺序与执行

先登记本地6核小时预算，在仓库统一入口执行`compute plan/run`，先跑已接好的JST历史预警和银行会计，再部署中国活动面板及真实银行实验。输入清单分别为`models/compute-initial.json`、`models/compute-china-activity.json`、`tasks/bank_research/compute_jobs.json`。实际结果在`compute/outputs/`，每个条目在`compute/ledger.json`保存input/code/environment/output SHA256、版本、运行秒数和完成状态。历史测试已见后不重切为新的未见测试。独立审计随后发现35个未知标签和3个全特征缺失训练行，修复准备脚本并另建 `models/compute-audited-history.json` 实跑，旧输入输出保留。

| 实际任务 | 输入性质 | 回答的问题 | 本轮权限 |
|---|---|---|---|
| historical-warning-v1（原版保留） | JST R6真实18国历史 | 固定训练/校准/测试和阈值后能否预警历史系统性银行事件 | HGB拒绝主用途；logit保留比较，拒绝中国事件概率 |
| historical-warning-audit-v2 | 同JST原始文件，剔除35未知标签及3全特征缺失后的1703行 | 保持原模型和切分的审计纠错重估 | 已见测试，不作新验证；校准HGB拒用，logit比较 |
| historical-warning-portable-v3 | 同纠错版逐字节相同的原始数据与1703行面板 | 修复相对输出目录落成绝对CSV路径后的可移植性重放 | 模型、切分与阈值完全相同，全部数值复现；不是新增经济验证 |
| bank-accounting-check | 明示合成会计例 | 准备、信用损失、流动性融资、折价出售是否勾稽 | 仅工程验证，不是中国损失测算 |
| mixed-frequency-interface | 明示合成混频例 | DFM新闻分解是否勾稽 | 仅接口验证 |
| china-bridge-long | 43季129月真实观测回溯面板 | PMI桥接对单季GDP同比能否超过滞后一季基线 | 有平均改善但不稳健，拒绝精确预测 |
| china-bridge-single-vintage | 23季69月同GDP发布版本 | 长样本结果对拼接版本是否稳健 | MAE明确更差，否定稳健改善 |
| china-nowcast-diagnostic | 真面板、末端季度留出、旧/新PMI信息集 | 同一输入的活动更新和news归因 | 算术通过；单次GDP误差约−0.98个百分点，不采用点预测 |
| china-bank-icbc-h1 / q3 | 两期工行集团真实报表 | 既有资产净额上新增信用费用如何侵蚀权益 | 条件损失会计；监管判定另做CET1桥接 |
| china-bank-lanzhou-h1 / q3 | 两期兰州集团真实报表 | 同一自身信用费用量尺及RWA敏感性 | 条件压力，不是出现频率和全国抽样估计 |

补充真实核算没有混入模型数量证明：地产财政`recompute.py`重算公布水平、同城指数与财政差额；银行`bank_accounts.py`以披露CET1单独桥接；`models/household_observations.py`计算调查均值的比值及官方年历总回报复利；历史代理在冻结JST上独立计算峰后路径。这些是透明的描述核算，不声称识别因果系数。

## 实际成绩与拒绝

详细原版成绩在`models/model_decisions.md`及`model_results.md`；当前纠错成绩以`historical_model_correction.md`为准。预警最终13个合格危机事件，预注册校准后logit检出3漏10，HGB检出0漏13。独立复核同时指出未校准HGB检出8漏5、Brier0.15595、AUC0.7393；校准期只有9个事件，校准后排序翻转必须披露，不将拒用推广到整个算法。独立重估证实不是正负类列误取，旧校准斜率−0.196335、新−0.262958。纠错后logit校准检出3/13、Brier0.170316；HGB raw检出7/13、Brier0.156506，校准后1/13、Brier0.185399、误报43/148；基准0.175914。已看最终测试后不能改选raw并当新独立验证。活动同版样本桥接MAE0.643对基线0.345，足以拒绝本轮GDP点预测用途。没有把分数归一化成概率，没有将多个模型平均成“中国危机概率”。

银行原生适配器的`capital_ratio`为账面权益/RWA，不是监管CET1。因此保留原输出，并在专题使用披露CET1、固定监管调整差额、显式RWA条件。工行9月未单列的摊余成本准备不由四舍五入覆盖率逆推；6月精确准备和9月净额情景分开。可用性降级比改写输入更可信。

## 预算与恢复

首批三任务、第二批中国活动三任务、第三批四个银行任务及第四批历史纠错作业的CLI会话均已结束。前四批的分配核数×运行时长累计约0.0233核小时；追加可移植性复演约0.00580核小时后，12条运行记录合计约0.0291核小时；它是这些命令的保守计费估计，不含依赖安装、检索、代理推理、图形审计与空闲进程，不能称整项研究只耗此CPU量或账户余额。实际峰值、包版本和作业指纹以回执为准。复算任务按相同指纹可跳过已完成结果；独立复核须另留实际重放记录，不能把跳过说成重新估计。

新目录应从保存提交克隆、安装同一锁定依赖、恢复同一actor/run_id，并重放核心方法；验证数值与输入/代码版本，不要求运行时刻相同。当前没有需要停止的远程实例。本地长任务结束后不留无限循环、轮询或承诺会话外继续运行。

## 新目录发现的路径缺陷与修复

独立新clone发现历史纠错版experiment.json写死原工作树的绝对CSV路径，最初该项重跑虽读到相同字节，却不满足完全从新clone读取。原输入、原输出及这一失败记录保留。准备程序改为先解析绝对路径，再生成仓库相对引用；新目录 `models/jst_portable_20261127` 经同一原始文件重新准备，面板与原始DTA逐字节一致。`models/compute-portable-history.json` 实际执行第12条记录 `historical-warning-portable-v3`；与纠错版除执行时刻和两模型耗时三项外，全部输出字段严格相等。输入核验和结果差异保存在 `receipts/portable_input_repair.json`、`receipts/portable_experiment_replay.json`。这只是同一次研究实验的可移植复演，不把作业条数当作独立样本量；经济用途与拒用裁决保持原样。

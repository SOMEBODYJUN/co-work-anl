# GitHub / 研究方法使用手册（按任务选择，不盲目拉仓库）
检索于2026-11-27。下面对可见README、目录、文档或发布记录做了核对；没有逐个运行仓库或验证预测性能。采用成熟基线优先，必要时才扩展。所有代码只是研究工具，不把外部预测当结论。

## M1：历史危机定义、样本与基准率（必用）
Global Macro Database: https://github.com/KMueller-Lab/Global-Macro-Database
版本：https://github.com/KMueller-Lab/Global-Macro-Database/releases
本次查到2026_09版，commit 1dbe128，167个数据来源，更新Laeven–Valencia银行危机日期并加入主权违约数据。
具体用法：优先使用公开数据下载或Python包global_macro_data；README示例`from global_macro_data import gmd; df=gmd(version="2026_06",country=["USA","CHN"],variables=["rGDP","CPI"])`。实际执行前查新版本支持情况和变量字典；锁定版本及国家。提取中国、日本、韩国、美国及其他可比经济体的年GDP、物价、投资、信用/债务、汇率与危机年份。不要将年度GMD当最新月度中国数据。使用IMF银行危机数据定义事件，不以A股跌幅代替银行危机。
IMF 2026版： https://www.imf.org/en/publications/wp/issues/2026/05/14/systemic-banking-crises-database-1970-2025-576036
输出：可比历史面板、事件定义、起止、累计产出损失、政策干预；将金融危机与长期停滞分别标注。
验收：每列单位与实际/名义口径清晰；时间边界不使用未来数据；不能把未发生银行危机的长期停滞样本删掉。

## M2：中国月度数据与发布时点（必用）
AKShare https://github.com/akfamily/akshare ，接口文档 https://akshare.akfamily.xyz/
用于定位宏观中国、市场和金融序列，不是统计权威。根据实际安装版本查 macro_china 系列接口是否存在；只取对应指标，不运行交易脚本。央行/统计局等原表优先。输入统一为`indicator,observation_period,release_date,vintage,value,unit,source_url`。累计值、同比、环比、存量和流量分别保留。历史可比口径与当前修订明确记录。
输出：月/季度时间序列及新数据增量表。缺测用NA，不能以零填充，不把日内九股缓存当宏观样本。验收：单位、发布时间、公布期匹配；聚合到月频遵守指标类型。

## M3：经济活动即时预测与“新闻到底改变了什么”（核心）
首选稳定实现：statsmodels https://github.com/statsmodels/statsmodels
技术文档 https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.dynamic_factor_mq.DynamicFactorMQ.html
源代码定位 https://github.com/statsmodels/statsmodels/blob/main/docs/source/statespace.rst
纽约联储参考 https://github.com/FRBNY-TimeSeriesAnalysis/Nowcasting
读取`example_DFM.m`,`example_Nowcast.m`,`functions/`及说明文档，理解混频、数据缺失和新发布数据归因。
2026近期实现： https://github.com/SermetPekin/nowcasting-dfm
阅读`04_nowcast_update.py`,`04b_nowcast_update_core_api.py`,`05_daily_report.py`,`06_fredmd_integration.py`及README。公开示例`dfm_sp.Options, get_with_options, run, sp_update_nowcast`；美国样例不直接用于中国。
具体应用：建立中国月度PMI、工业增加值、社零、投资、地产、信用、物价、出口等与季度实际GDP的混频面板。先做简单桥接回归或AR基线；若样本和版本可用，再使用`DynamicFactorMQ`的月度和季度输入、`fit()`、`get_forecast()`与结果对象`news()`。比较上次与本次数据发布对同一目标期预测的改变量，拆解数据修订和新增观测。模型可观测性不足时使用透明的区间和经验桥接，不伪造拟合。
输出：当前经济活动、3/6/12月风险增量及“本条新闻使哪一项判断变了多少/方向是什么”。Nowcast是当期活动，不是十年危机概率。
验收：扩展窗口伪实时测试；只使用当时已发布数据；记录MAE、误报和模型失败。短样本不要强行训练深网。

## M4：银行危机预警（必做基线，机器学习有条件）
Bank of England WP848复现 https://github.com/bank-of-england/MachineLearningCrisisPrediction
具体读取`experiments/`（交叉验证与预测）、`data/`（JST Macrohistory v3）、`analysis/`、`results/baseline/`（示例预测和解释结果）、`scripts/`及README。该项目是17国1870–2016年的研究代码，依赖旧Python/R，**不是现成中国预测服务**。只学习变量变换、信贷增长/收益率曲线、基准模型比较、非线性和SHAP解释。另查BIS：
https://data.bis.org/topics/CREDIT_GAPS
https://www.bis.org/publications/qr-201803/early-warning-indicators-banking-crises-expanding-family
https://www.bis.org/publications/working-paper-1235-aggregate-debt-servicing-and-limit-private-credit
用信用/GDP缺口、家庭/企业偿债率DSR、房价偏离、信贷增速、利差等指标。历史危机前的过热信号与已经进入去杠杆后的收缩信号分开。单边趋势滤波，不使用双边未来值。若做logistic/hazard，按时间与国家留出，报告Brier、PR-AUC、召回率、假警报；不要把随机交叉验证成绩当中国适用性。
输出：预警表、危机事件概率的证据强度与校准范围。中国样本不足时，国外模型只作外部参照，概率使用明确的主观区间而不是假称精确训练结果。
安全：不开未经检查的pickle，不运行旧安装脚本；检查许可与依赖。代码能在隔离环境运行才运行。

## M5：中国债务存量—流量模型（必用，自己构造）
不靠某个万能GitHub。使用财政/央行/银行报表、IMF 2026地方财政研究与2025金融系统评估。明确房地产开发商、地方政府/LGFV、居民、银行、中央政府、企业的资产负债关系。
债务递推：期末债务=期初债务+新增融资−本金偿还±重估/核销。利息、债务置换、再融资与财政转移分别列账；置换不能当债务自动消失。
银行压力：分风险暴露EAD、违约概率PD、损失率LGD，估计信用损失区间；把拨备、当期收益、资本及再融资缓冲逐层抵减；数据不足保留区间。地方财政：净土地资源=毛土地收入−土地取得/相关支出（按可得口径），并计算转移支付、债务利息与刚性支出；不得直接把土地收入降幅等同财政支出降幅。
输出：风险损失由哪个部门承担、政策需要的资源、对家庭收入与住房价格的传导区间。

## M6：研究辩论工作流（不是自动交易）
TradingAgents https://github.com/TauricResearch/TradingAgents
本次README显示2026-10发布v0.7.1，修正信息时点与收盘结算等问题。学习其独立分析、正反研究、风险审核、最终裁决的工作流；不照搬股票交易信号、自动下单或多数投票。原ZIP本来也借鉴该项目，但没有捆绑上游代码。
每条重大新闻的结构化记录：事实→数据口径→与先前预期差异→影响部门→政策实际可执行性→新证据对主情景的增量→是否改变家庭行动。反方需提出证据和必要量级；审计员核实同样的举证标准。只有真实可用工具才创建独立Subagent；无工具则透明降级，不假称并行。

## M7：贷款、现金流和优化（计算器必用）
https://github.com/numpy/numpy-financial ：用`pmt`,`ipmt`,`ppmt`作为等额本息测试对照，注意现金流符号。计算器自己以元和月逐期记账，浮动利率/提前还款另写逻辑。
https://github.com/scipy/scipy ，文档 https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html ：对于线性化且有整数决策的超大组合可研究`milp`。不要强行把非线性房屋处置、随机出售时点与提前还贷写成错误的线性优化。
默认方案：用Python和JavaScript分别实现透明的有限枚举、约束过滤及Pareto排序；100–500个策略规模不需要强化学习或遗传算法。按用户真实房产数量生成组合，使用月度现金流引擎，计算各情景最大资金缺口、最低现金、实际终值及后悔值，先约束后排序。复杂情况再扩展混合整数规划。
此前发现的参考候选（不要求使用；本轮未逐一重验或运行）：
https://github.com/mbk-dev/okama-planner
https://github.com/gthgomez/MonteCarlo-Ledger
https://github.com/murraystokely/mortgagemath
https://github.com/dcajasn/Riskfolio-Lib
分别只研究家庭现金流场景、收入延迟、贷款计算测试和金融资产风险计算；Riskfolio不适合直接优化不可分割的房产/车贷。不得上传私人资产到仓库或API。

## M8：最终中文写作清洗（必用）
https://github.com/jiji262/humanizer-chinese/blob/main/SKILL.md
本轮实际核对SKILL.md：采用其嵌入模式，内部改写和终审，用户只看最终文本。压缩机械小标题、重复对举、段尾复读、空洞升华、教科书腔、模糊套话；保持研究报告语域。禁止捏造具体细节、第一人称经历或来源。文字编辑不能改变数字、日期、概率、模型参数、实质判断或删去真正影响决策的限制。
备选参考： https://github.com/larashero3-dotcom/lieflat-less-ai-tone （前轮候选，未重新核对全文）。
不要求安装Skill：若运行环境不能安装，就读取规则并作为终稿编辑指令。

## 更新与取舍规则
仅搜索能改善上述任务的更新仓库，优先官方研究复现、有论文、有数据/测试的实现。记录检索日、具体文件/API、commit/tag、采用/未采用及原因。没有依赖环境就用简洁可复现的本地实现；不能编造已运行代码。不要为了显示研究复杂而拉取几十个仓库。原包Qlib/TradingAgents提示词不提供经过验证的训练权重，不能称作已校准模型。

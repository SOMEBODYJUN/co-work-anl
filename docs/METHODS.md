# 统一方法接口与已运行记录

所有方法使用同一个入口，输出 `cncrisis-method-result.v1` JSON。Pro 克隆本仓库后直接调用；依赖通过 PyPI 安装，不再克隆第三方仓库。

```bash
python bootstrap.py
.venv-methods/bin/python crisis.py methods doctor
.venv-methods/bin/python crisis.py methods list
.venv-methods/bin/python crisis.py methods run --name loan --output work/loan.json
.venv-methods/bin/python crisis.py methods run --name bridge --output work/bridge.json
.venv-methods/bin/python crisis.py methods run --name nowcast --output work/nowcast.json
.venv-methods/bin/python crisis.py methods run --name stock-flow --output work/accounting.json
.venv-methods/bin/python crisis.py methods run --name akshare --output work/gdp-replay.json
.venv-methods/bin/python -m unittest tests.test_methods -v
```

`bootstrap.py` 创建独立环境，优先按 `requirements-methods-lock.txt` 安装完整传递依赖，不继承系统包。`requirements-methods.txt` 固定六个主要包版本；完整锁文件已在不继承系统包的 Python 3.12 Linux 新环境实际安装。迁移系统时先运行 doctor，按实际操作系统的对应 wheel 安装依赖。标准库研究台不要求这些包，运行数值方法时才安装。

| 方法 | 本次实际连接和执行 | 研究使用方式 |
|---|---|---|
| numpy-financial 1.0.0 | 原始 `_financial.py` 和 BSD 许可已入库，贷款逐月本金/利息与 `pmt/ipmt/ppmt` 逐期核对 | 验证家庭计算器贷款；不是宏观预测 |
| statsmodels 0.15.0 | `DynamicFactorMQ.fit()`、同参数 `apply()`、`get_forecast()`、`news()` 均运行；源文件和 BSD 许可入库 | 传入有真实发布版本的中国月/季面板，计算同目标期的新观测增量 |
| NumPy 桥接基线 | 32 个季度的固定合成样本，前12季初训，20季扩展窗口检验，比较上一季基线 | 先有基线，再判断复杂模型是否值得保留 |
| 存量流量 | 债务/现金会计恒等式实算；再融资不抹债、负现金列缺口、超额还债拒绝 | 参数来自财政与报表，追踪损失由哪个部门承担 |
| AKShare 1.20.70 | `macro_china_gdp()` 真实端点成功，取得83行；对应 `macro_china.py`、MIT许可、原CSV、取数收据、SHA和离线复播已保存 | 寻找时序后追原始统计发布；该表是年内累计季度GDP，须按相应口径处理 |
| FRBNY Nowcasting | 固定commit的两份MATLAB入口与 `update_nowcast.m` 及许可入库；本次没有运行MATLAB | 学习混频、数据版本、新观测分解；数值执行使用statsmodels适配器 |
| TradingAgents | 固定commit的宏观展望、情景分析、论点复审提示词及Apache-2.0许可入库 | Pro与真实agent读取后执行独立论证、挑战、裁决；CLI没有调用外部LLM |
| humanizer-chinese | 固定commit的完整中文编辑规则和MIT许可入库 | 独立编辑者在事实冻结后改写，再复核数字与判断 |
| Global Macro Database | 当前数据库许可原文已保存；提供调用者CSV读入适配器；未复制数据库 | 符合上游条件时自行取得面板后读入，或使用许可适合的官方历史资料 |
| BoE WP848 | 代码GPL-3.0-or-later许可已核对保存；JST数据另有CC BY-NC-SA许可；未执行其旧Python/R训练流程 | 借鉴按时间/国家留出验证及预警变量；不把国外旧模型称中国概率模型 |

实际版本、文件、commit、下载链接与SHA见 `vendor/manifest.json`。使用目录中的原始许可；本仓库自身许可不替代上游许可。`tools/vendor_methods.py` 只下载已锁定许可和方法文件，不执行上游代码。

两个已执行适配器的精确源码快照分别在 `vendor/statsmodels/dynamic_factor_mq.py` 和 `vendor/AKShare/macro_china.py`，各自目录同时保存对应发行包的原始许可。它们用于本仓库研读和追溯；运行时加载锁定发行包，使编译扩展和传递依赖由发行包保持一致。

## 输入与输出

每个运行接口都支持 `--input 文件.json --output 结果.json`。未给输入时，贷款、会计、桥接与混频使用明确标记的合成工程样例，AKShare使用实际取数缓存；合成样例不会进入正式经济证据。

贷款输入示例：

```json
{"principal":1000000,"annual_rate":0.03,"months":240,"input_kind":"synthetic_test"}
```

利率用年率小数，输出金额单位元、时间单位月。这里执行标准合同还款，不是完整的家庭方案枚举器。提前还款、卖房到账、失业与负资产处置由正式家庭引擎实现后，用这些对照接口核验。

会计输入示例：

```json
{"opening_debt":100,"new_financing":20,"principal_repaid":10,"writeoff":2,"revaluation":0,"opening_cash":15,"cash_receipts":20,"cash_payments":18,"unit":"亿元","input_kind":"synthetic_test"}
```

这只是债务和现金恒等式；现金收支由调用者按同一部门范围完整列账，不从债务净变化猜测现金。它不创建加权风险分、危机概率或损失率。

月季面板格式见 `tests/fixtures/methods/synthetic_panel.json`：月度期索引、按指标列出的月度数组、季度期索引、季度GDP数组和 `input_kind`。正式研究把每个发布时点的数据另存一份；指标单位、转换、统计期、发布日期和修订版本存在证据表，不用事后修订表伪装当时已知。

默认混频演练拿掉最新季度目标和最后一期月度发布，拟合旧版本；用同一参数接上新月度观测，比较同一GDP目标期的估计。`news_impact` 必须和新旧预测差勾稽。EM收敛按statsmodels原有似然增量停止规则判定并记录迭代数、容差和警告。该工程样例检验接口与时间边界，正式模型仍须在真实中国发布版本上做扩展窗口评价。

AKShare默认离线重放；实时取数输入如下：

```json
{"mode":"live","output_csv":"work/inputs/gdp-cumulative.csv"}
```

`macro_china_gdp` 返回累计季度表，没有逐历史发布日字段。因此缓存不得冒充伪实时历史数据库；单季量、可比价与季调转换另行按统计原表处理。

GMD面板适配器要求调用者提供已经取得使用权的CSV：

```json
{"csv":"work/inputs/historical-panel.csv","country_column":"country","countries":["CHN","JPN","KOR","USA"]}
```

GMD仓库当前数据库条款限制使用主体与重分发；Python包的代码许可不能替代数据库许可。本工作台没有打包它的数据库，也未运行GMD中国历史校准。BoE代码GPL与JST数据非商业许可分别记录，不混写成一个许可。

## 已保存的演练证据

`tests/fixtures/methods/akshare_live_receipt.json` 记录真实取数日期、函数、行数、头尾记录与原CSV指纹。`results/` 保存实际计算JSON，`synthetic_panel.json` 保存固定输入，`tests/test_methods.py` 实际调用这些路径验证。

离线复跑贷款、会计、桥接、混频和缓存读入都不需要网络，不调用模型API。`research-contract`、`editorial-contract`、`frbny-reference`、`boe-reference` 返回准确的方法文件与执行范围，由Pro/agent负责思想分析、主判断与写作；“文件可读”与“上游完整程序已执行”在状态中分开记录。

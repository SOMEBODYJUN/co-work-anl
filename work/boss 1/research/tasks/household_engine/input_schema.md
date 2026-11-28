# 输入契约与程序接口

计量币种为人民币，时间从第 1 月到第 120 月。JSON 的利率、折价、空置与收费比例采用小数；页面标有“%”的家庭输入框会换算。情景表按所标小数或倍数直接编辑。家庭金额可为一个数或形如 {"low":10000,"base":15000,"high":22000} 的区间。rangeCase 选择 low、base、high；两个端点之间没有填中心值时，选择 base 会报错。低端一律取低值，所以同时降低收入和成本，并不天然意味着“最坏情景”。

## 顶层与分组

独立家庭文件使用 schema = household-cny.v1。离线页面导出 {"schema":"household-offline.bundle.v1","household":{...},"scenarios":[...]}。单独导入家庭文件会沿用当前页面情景。完整默认结构可查看 engine.js 中 blank()、templates 和随包 synthetic_household.json。空白家庭只有零个条目、现金与最低生活 null，试算必须显式填写两者，零是有效输入。系统不会保存浏览器本地状态。

| 顶层字段 | 含义 |
|---|---|
| dataKind | household 或 synthetic_example。后者通过显式载入按钮或导入已标记示例产生，编辑后保持标志，CSV 也带标志 |
| cash、cashAnnual | 期初可用现金、有效现金年回报。每月按 (1+r)^(1/12)−1 对期初现金计息 |
| minimumLiving、reserveMonths | 基础生活支出的下限、现金储备目标月数。必要现金需求取基础开支与下限较高者，加教育、医疗、养老、保险，再计入当期突发费用。储备以当期常规必要开支乘月数，突发支出按实际发生月单次纳入 |
| cutFraction、maxSaleWait | 允许削减的可选支出上限比例、从挂牌到成交可接受的最长月数 |
| preference、rangeCase | cash、wealth、debt、regret；区间低端、中心、高端 |
| citySources | 用户可录入或离线导入 [{id,city,period,source,scope}]。每套房可单独指定 city 和 sourceId；家庭工程包不推测城市行情 |

所有资产、债务、收入和支出的 id 在全部清单内唯一。支持无任何房屋、车辆、收入、证券或贷款的家庭。名称用于显示。字符串 id 避免空格和特殊标点，允许汉字、大小写字母、数字、点、短划线、下划线，首字符使用汉字、字母或数字。每组最多 100 条。录入中的交易、提前还款许可与相关费用可以留空。空值表示未确认，免手续费或立即到账须明确填 0，最早第一个月可办填 1。合同的普通月度还款仍可独立计算。其他模板设定如整月步长显示在输入项中；新增具有经济意义的本金、市值、工资及必要的持有成本需填写。金额显示可切换元 / 万元，存储始终为元。

| 清单 | 输入字段及真实用途 |
|---|---|
| incomes | kind 为 wage、bonus、business、other；monthly 是每次实际税后到账或经营净回款，from/to/every 为首月、末月与间隔，annualGrowth 为该笔收入的年变化。stability 记录说明。stressJob 允许全体失业事件施加于本收入。jobStart、jobMonths、jobPayFraction、recoveryMonths、returnFraction 定义该来源独立中断、过渡和复工后水平。奖金可每 12 月到一次。 |
| expenses | kind 为 necessary、education、medical、elder、insurance、discretionary、emergency；monthly、from/to/every、annualGrowth、inflationLinked 允许分段、单次或不规则年度费用。只有 discretionary 随预算动作削减。 |
| financial | kind 为 deposit、instant、stock、fund、bond、gold、other；value、annualReturn（有效年总回报）、concentration、fee、settle 为当前市值、集中比例、成本率、到账间隔。unlock 为最早交易月、maturity 为到期月（0 表示无），restriction 为 unknown/free/restricted/pledged，purpose 记录用途。交易费用、到账时长、解锁条件及用途未知时保留持仓。pledged 必须关联贷款。全额处置时，仍有余额的每一笔质押贷款须明确允许同步解押，并确认结清条件、费用和所需补差。部分解除质押未另设合同，分批与补储卖出仅在关联贷款结清后执行。杠杆本金在 loans 中单列。定存到期受限制时继续分账；普通证券总回报含分红。 |
| properties | city/type/use 分别记录各自城市、类型和 occupied/let/idle。value 为账面估值，saleValue 为保守成交总价，两个数可各自给区间。saleLag/lock/canSell、rent/vacancy、leaseLag/discountRent/discountLeaseLag、carry/saleFee/closingFee 分别处理交易、出租、经常管理/物业/税费及交割费用。自住房出售须 replacementAllowed 并填 replacementMonthly；替代费用从交割月开始。 |
| vehicles | value、saleValue、annualDepreciation、carry、saleLag、lock、canSell、saleFee、closingFee。necessary 标记必要通勤生产车辆，出售须有 replacementAllowed 与 replacementMonthly。车辆关联贷款及结清费用在 loans 录入。 |
| loans | kind 可为 mortgage、car、consumer、card、business、family、margin、guarantee、other。collateral 引用任一金融或实物资产 ID，空字符串表示无抵押。principal、annualRate、months、method 是余额、名义合同年率、剩余期数和 annuity/principal/bullet 三类合同，固定月供 payment 可以在 annuity 指定（最后一期清余本）。rateType、resetFirst、resetEvery 限定浮息重定价。canPrepay、prepayFrom、prepayMin、prepayFee、settlementFee、allowRecast、allowShorten 限定预付；transferWithLien 为 null 表示解押安排未确认；false 意味着实物出售交割前必须筹足该笔全部解押资金，质押证券须先另行结清。预付须确认许可、时间及费率；全部结清还须确认固定结清费，部分预付另须确认合同方式和最低额。monthlyFee 为合同每期费用。guarantee 的 start 是已设定的代偿触发月，超出 120 月时本期不入账。 |
 
## 贷款的预付与提前解押条款

普通合同还款仅需原本金、利率、剩余期数与还款法。可选的提前偿还另按下表逐项判断。准确支持旧 JSON 中数值形式的 prepayMax，以及 allowFull 的布尔值。未支持的贷款业务字段会报错，补充文字可放 notes 或 metadata。旧输入缺少新合同字段时可继续算原合同；请按实际合同填写额外许可再评估相关动作。

| 字段 | 含义 |
|---|---|
| canPrepay、allowFull、allowRecast、allowShorten | 分别确认一般自愿预付、提前全部清偿、部分预付降月供、部分预付缩期限。可填 true/false/null。一般许可不等于允许全清。部分预付若金额恰好结清剩余本金，同样须明确允许全清。 |
| prepayFrom、prepayMin、prepayFee、settlementFee | 最早可预付的贷款期数（从 1 开始）、最低部分预付额、预付比例费用、提前全清固定费。页面金额以选定的元或万元显示，JSON 金额以元表示。 |
| prepayMax | 每笔额外本金的最高额，有限的人民币数值，0 表示当前不能预付；无上限必须显式填字符串 unlimited（界面可输入“不限”）。空或缺失代表未知。 |
| prepayPeriodMax | 合同一个限额期间内累计额外本金最高额。数值、unlimited、null 三种语义同上。两类限额需分别确认。 |
| prepayPeriodMonths、prepayPeriodRemaining、prepayPeriodUsed | 有限期间额度才使用。完整周期月数、从第一模拟贷款月起当前周期还剩几个月（含该月），以及模拟开始前本期已经用掉的元数。若剩余 2 个月、周期 3 个月，前两个月共用期初余额，第 3 月和第 6 月各开新期。缺资料时正常还款继续，相关预付不进入可行集。 |
| salePayoffRule | unknown 表示待确认；same_terms 让抵押物提前出售结清适用普通全清许可和剩余额度；forbidden 禁止借出售提前解押；sale_exception 是已经确认、独立于自愿预付限额的出售清偿例外。没有明示例外时，不能推断可以借卖资产绕过上限。 |
| salePayoffFrom、salePayoffFee、saleSettlementFee、salePayoffFeeBase | sale_exception 所需的独立起始期数、出售提前结清比例费率、固定费。有效正费率下，资产交割需明确计费本金是 balance（该笔全部待清余额）或 extra（只取超过当月合同应还之本金）；这是 feeBase 的两种取值。 |
| saleMaturityReleaseFee | 原定本金已经全额到期，同时出售资产时另列的行政解押成本。in_asset_cost 表示解押已含在该资产申报的成交费用中；数字是尚未包含的额外费用，0 表示明确无附加费；null 表示交易费用范围待确认。没有资产交易时，该项不计入普通按期还本。 |
| transferWithLien | 指能否在成交时用成交款同步解除这一抵押/质押；与“允许提前全清、限额、例外”分开。房地产、车辆和质押证券的共同交割核算都执行对应条款。 |

每次预付的可用额度为单次上限和本期尚余限额之较低者。只在预付实际清算时占用额度；同一笔贷款可在不同月份预付，每月只接受一个显式自愿预付动作。合同定期应还的本金不占用提前额度。提前卖资产的清偿只把超过本月合同应还的本金计入提前额度，交割时仍须付清全部待还本金、利息和费用，各只扣一次。到了合同原定清偿月份，普通本息仍须支付，已有全额合同应还本金的出售清算不受未来或自愿提前还款许可限制。

## 情景数据

scenarios.json 顶层是数组。单项包含 id、name、role、description、paths。role = recovery 标记“恢复机会成本”的参照路径。build.py 也能读取有 scenarios 数组的报告封装。每条路径参数包括 key、mode、value、unit、start、duration、range 两端、sourceId、editable、assumption、target。目标必填；缺失或空串不能代表通配。来源类别可为 observed、historical、research_estimate、stress_test。随包的 design-continuity、design-severe、design-recovery 是试验设计来源 ID，所有参数为 stress_test。range 约束已填 value。当前默认路径中的单点范围是明确的试验设值，页面更改该设值时同步移动单点，也可编辑两端。

| 参数组 | 施加规则 |
|---|---|
| wageFactor、businessFactor、otherIncomeFactor、rentFactor、reemploymentFactor | level，单位“倍”，在起点与持续月内有效。工资和奖金同类，经营回款独立 |
| unemploymentMonths、recoveryMonths | 前者 event，单位“月”，只在 start 发生一次，其 value 是实际中断月数。后者 level，事件开始时读取的恢复时长。具体 target 可给任一收入增加中断事件；与通用或家庭事件重叠时使用较低的当月收入水平，避免重复削减 |
| propertyShock、financialShock、concentrationHaircut | shock，单位“比例”，duration=1，分别为一次估值变动和按集中比例的附加折价，实际资产保留新的水平 |
| propertyAnnual、inflationAnnual | annual，单位“年率小数”，有效年率按月复利 |
| loanRateDelta、cashRateDelta、securityAnnual | annual，单位“年率差”。浮息仅在约定重定价月读取合同年率差，固定贷款保持原率；金融资产年总回报按合同/持仓基线加差值 |
| vacancyAdd、saleHaircut、saleDelay | level，单位分别“比例差”、“比例”、“月”。空置夹在 0 至 1，额外成交时间在挂牌月锁定，价格折让在交割月读取 |
 
target="*" 是可跨户使用的通用路径，即使当前家庭没有对应资产也可保留。具体目标须是当前家庭中实际读取该参数的唯一 ID。工资/奖金、经营收入、其他收入各自匹配收入类别；失业和复工可指向任一收入来源；房价、租金、空置只可指向房产；成交等待/折价可指向房或车；证券冲击、总回报、集中折价只可指向 stock/fund/bond/gold/other 类市价资产；贷款利差只可指向浮息合同。通胀与现金利率差仅接受 *。导入、编辑和试算时都会复核绑定；删除、改名、改类别导致旧 ID 失效时，需先更正情景。普通参数同月同 target 同 key 重叠拒绝；具体 ID 优先于通用层。每项事件/冲击只施加一次。默认 financialShock 与 securityAnnual 的共同冲击针对证券等市价资产；定存和随时可用余额保持各自输入年回报。城市资料和特殊收益可用具体资产 ID 细分。三条人工路径分别递推，无情景权重字段。

## 函数接口

Node 使用 require("./engine.js")，浏览器中为 HouseholdEngine。所有输入均为 JavaScript 对象。

| 接口 | 返回 |
|---|---|
| blank()、templates、baseStrategy() | 空白家庭、可增删条目的字段模板、不行动基准 |
| validateHousehold(input)、validateScenario(scenario,rangeCase,household)、prepare(household,scenarios) | 校验并转换区间、引用、单位与参数路径；缺失关键金额会抛出中文错误。prepare 的结果含 h、scenarios |
| enumerate(prepared.h,limit) | 100 至 500 的上限内生成不同策略及 coverage。只有一个组合时只返回一个 |
| simulate(household,scenario,strategy) | 单策略详情，含 summary、逐月 rows、实际 events、byLoan、propertyFlows。失败月之后 rows 停止 |
| assess(household,scenarios,limit=500) | 所有方案 results、各情景 outcomes、coverage、commonCount、best、winners、shortlist。各结果的 trajectory 标识本次运行的经济轨迹，coverage.distinctMonthlyTrajectories 与 distinctFeasibleMonthlyTrajectories 分别统计所有与共同可行的轨迹 |
| inspect(study,strategyId,scenarioId)、rank(results,objective) | 重放一项的逐月明细、按单目标排序。无合格集时 winners 的正常比较留空，leastGap 返回已跑候选中待补资金最小的一项 |
| reverse(household,scenario,strategy,{incomeId,propertyId,loanId,financialId}) | 已测试的工资/中断/出售延迟/房价/租金/联合冲击的边界与重入标志、租售反事实、可预付上限及卖股/还贷相对现金耗尽变化 |
| path(key,value,start,duration,target,sourceId) | 生成完整的人工情景参数行，便于研究参数接口集成 |

策略对象形如 {"id":"custom","actions":[{"kind":"list","asset":"flat","month":6}]}。list 可加 trigger:"reserve"、buffer；rent 使用 discount；liquidate 使用 all、stages 或 reserve 的 mode；prepay 带 loan、month 和 full/recast/shorten，部分预付另带 amount；cut 带 fraction 与可选的 trigger/buffer。触发条件读取当月期初现金或已知到期和可用资金。已知挂牌时滞只用于合同办结日期，不让决策预见未来房价。


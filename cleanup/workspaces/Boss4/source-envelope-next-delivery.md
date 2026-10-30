# source-envelope-next交付

已完整读取正式claim批次中的12源版本，全部原件SHA-256与冻结inventory一致。claim由Boss执行并收到pushed，提交为 `312c5851e9e6e7256584ab8d3e3c1da2df0dd966`。本子代理未执行claim/done/sync/commit/push；以下成果已写入共享工作树，等待Boss集中checkpoint确认pushed后再done。

## 交付路径

- `archives/weighted-congestion/state/定理/两攻击源参数包络的全域对数上限--定理.md`
- `archives/weighted-congestion/state/定理/两攻击源参数包络的锐渐近--定理.md`
- `archives/weighted-congestion/state/审查/两攻击源包络的审查与诊断范围--审查.md`
- `archives/weighted-congestion/tools/evidence/source-envelope/`（12冻结原件、3全文比较依赖、来源清单、全仓相关检索、重跑驱动、三份实际输入程序/完整输出/stdout/stderr/逐字段比较）
- `cleanup/workspaces/Boss4/source-envelope-next-receipts.json`（12条逐源实质记录，targets只指正式正文）
- 本文件。

## 数学对象与保全范围

显式ceiling保留每个整数d,n,k及任意合法实w,beta上的联合必要条件、标量分域、R≥e²时的8常数和ln d≥16时的sqrt128常数；锐渐近保留2/sqrt(e)首项常数、合法floor/ceil参数与全中间极限、任意近sup序列定位和sup不达量词。完整源游戏、全部状态指定偏离、精确完整minimax与源两商证书的区别均写明。

另一份candidate主稿作为额外比较依赖全文读取，独有的完整状态成本表、有效S/32有限保证、y坐标人数限制、三域一致标量引理完整保留，不把它的来源版本顺带登记done。source_ceiling中的旧 `current/lower_family/sharp_envelope.md` 不在冻结清单，明确记为旧别名，没有虚构取回；当前候选真实路径是 `research/questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md`。

三份审查分别保留：先独立重构ceiling且当时程序尚未交付、较后完整sharp逐稿攻击和全状态进口重建、candidate源事实/初步新颖性审计。旧pending与外审/优先权未认证分开。已完整读MODEL及较后linear_degree_allstate_lower_bound.md：对每个整数d≥2^20的全状态d/10下界更新旧OPEN，不让源包络或奇环障碍冒充全类上界。

## 实际复现与自检

在仓库根运行 `python3 archives/weighted-congestion/tools/evidence/source-envelope/replay_suite.py`；三份冻结程序未改写，在独立目录并行完整运行，Python 3.12.14，均退出0。所有新JSON与对应冻结报告逐字段零差异。

- ceiling：484个Fraction输入、16个R>1、4个beta=0边界；7个大次数Decimal行和5994个标量点。一般log不等式由解析证明承担。
- sharp logs：6个整数次数行在两种精度下floor/ceil稳定；4个n=N连续代理独立标记。Decimal没有严格区间误差，双精度稳定不认证真实对数取整。
- candidate：720游戏、10800字面状态、46080单人翻位的Fraction检查；9个巨大次数Decimal行另行解释。巨大样本不枚举指数状态空间。

已做：12原件hash、3比较依赖hash、12回执ID唯一与目标存在、3篇YAML必需字段/稳定ID、所有相对文件链接存在、无行末空白、重跑逐字段零差异。没有对整个仓库运行共享图构建或改他人正文/README。

## 关系判断供Boss接续

1. 显式ceiling与锐渐近研究相同合法源sup，前者给有限明确常数，后者给首项等价；保留两种不同上界推导。
2. 有限Fraction资源枚举实现源全状态接口；Decimal与连续代理仅诊断，不画成一般定理证明边。
3. 已有完整对称两列归约与锐渐近联合才产生该特定拓扑的锐渐近；源sup本身不是每实例完整minimax，也不是全类阈值。
4. 固定32次源整数符号证书、非对称十四资源分离、奇环较粗源ceiling和后续全状态线性下界都是已比较的不同范围对象；新正文给出共同域和为何不能替换。

第三阶段再按这些解释建立图；本批未改共享图，不因同名引用造边。所有源均可按12条receipt integrated，但应以Boss真实checkpoint pushed作为done前提。

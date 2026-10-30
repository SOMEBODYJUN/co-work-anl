# Boss5 续局CCE与均匀组合归纳批次交接

本次分两批实质清洗，共9源。首批3源的回执是 `receipts.json`，Boss已另行串行保存/登记；接续6源的回执是 `receipts-benchmarks.json`，本报告只交付本地成果待Boss保存。子代理未执行Git写、checkpoint、done、claim、sync或公屏send，未读取或输出凭据。

## 首批3源及修改清单

- `6e26300f60355e62637f` → `archives/customer-attraction/state/障碍/均匀组合背景归纳的尾部余量--障碍.md`；完整独立证据目录 `archives/customer-attraction/tools/evidence/uniform-portfolio-induction/`。
- `45dfb652f8f558701583`、`2e9cd770fef4e67ed7b5` → `archives/customer-attraction/state/计算/静态CCE福利分离的初次策略锥证据--计算.md`；完整独立证据目录 `archives/customer-attraction/tools/evidence/continuation-cce-initial/`。十三客户README中已完成正文通过正常链接比较，不再完成旧源。

归纳源独有内容：精确写出背景候选和LOCAL、尾部差恒等式；任意m≥3的完整SPE全选大主题族在根UP恰等，LOCAL差恰为负尾差−(m−2)(m+1)/2。另从定义发现原稿未限n的字面BG-UP在唯一非空主题、r≥2、n=1时已经失败；n=m≥r的归纳范围仍未证，根UP和half没有被这个局部失败反驳。

初次策略锥独有内容：归一化W1、CCE下界3011/2950；清分母31575后有43426名不同单位客户，W31575、OPT42100、CCE下界3802893/118。没有原始达到分布，不称初次锐最低值。另完整保存四相同覆盖标签策略的两轮零差，只是固定策略有限未分离。

首批已实际核3回执所有targets存在、4份新Markdown本地链接、4冻结原件SHA，以及两个标准库独立审计的完整输出重放相同；任意m障碍来自正文符号证明，不由m3至20有限核对外推。

## 接续6源及修改清单

六源分别为 `4543a51671f34d050558`、`7872a6fd5466b83fe15d`、`606d17e49bb1ab70b650`、`fd6f7bb77a02640b255c`、`807d5ce448721b833219`、`b9106edbe4088e387d29`。

新增正文：`archives/customer-attraction/state/计算/静态CCE原始对偶基准与缩小记录--计算.md`。

新增独立证据目录：`archives/customer-attraction/tools/evidence/continuation-cce-benchmarks/`，含README、source-manifest、原相对树source内六主源与六运行依赖、comparison内前批初次JSON、两份完整原程序重放、环境版本、新标准库audit和完整独立输出。共13冻结原件；运行依赖和前批已完成源不被这六源批再次勾选。未修改首批对象或其他代理正文。

独有数学及比较结果：

1. 16客户PNE例最低CCE72669/5132<15，472客户iid起始例最低CCE20980/59<358；给出匹配原始/对偶，避免把PNE/iid来源例误当全部CCE分离。
2. 零客户、单人、空/重复覆盖三个有限边界全部认证；说明软件重复标签与数学集合目录的区别。
3. 70客户中间例完整31动作，155比较、W51、各收益17、OPT68、CCE下界3070/59；完整保存不同客户向量，未因有十三客户例而删掉。
4. 13客户缩小JSON保留旧乘子下界8621/944，有别于后续137/15和锐2785/297；独立重构constraint_scales=[6,2832]，不把HiGHS最优状态当全局规模最小性。
5. small_benchmark给另一15点有序CCE达到分布，与旧正式18点分布同锐值而非逐行重复，全部15项个体约束认证。
6. 原probe和cone_attack全文逐函数理解、按原字节复跑；两程序分别是固定有限基准LP及固定完整策略固定对偶的客户锥发现工具，不是普遍桥证明。

最终核验实际通过：6回执所有targets存在；13原件字节数及SHA一致；新正文和README全部本地链接有效；独立标准库audit在最终包路径完整重跑与输出逐结构相同；原probe和cone_attack在最终包路径真实重跑，与保存完整输出分别相同，且这两输出已分别与冻结benchmark_regression和alternating_cone_result全部结构一致。

新增独立实现不导入作者/规范模型或求解器，逐有序终局核静态列、逐玩家核CCE约束、逐有序历史核70/13及两起始策略，并用完整有序历史集合值递推核五基准及十三客户最低SPE。不是新增外部审查。

## 实读比较与阶段三关系材料

全文读取AGENTS、cleanup/README、OBJECTS、tools/README和全部9主源；第一批比较已清洗共同目录定义、两人平均偏离定理、匹配障碍、静态安全值锐例、CCE反例/核验资源、十三客户独审，并读取冻结global/README、resume_uniform/README和两份independent_attack/README。第二批额外全文读两程序、四份规范包运行依赖、两个起始输入、已清洗PNE正文/核验资源和iid桥对象，逐字段比较新旧十三客户原始分布。

正文已解释关系证据：四合法末位比较给两人基步；精确尾差恒等式与完整锐族反驳LOCAL；全策略和客户证SPE；非负CCE约束与全部对偶列证下界；匹配分布与下界证最低值；同策略不同重数连接发现与缩小来源链；不同最优分布是同一LP不同原始点；有限负面搜索不能成为普遍定理。未导入旧图，也未为了连通强造超边。

保留所有承重域、量词、非零背景利润/根覆盖区别、失败机制和接续用途。恰六人half仍需对每份完整有序历史纯SPE证明2W≥OPT6；本批没有六人反例或该全称证明。规模最小性、新颖性、外部同行审查均未认证。

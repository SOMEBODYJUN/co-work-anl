---
id: "unrelated-machines/actual-kronecker-full-matrix-two-certificates-audit"
kind: "computation"
type_tag: "计算"
title: "完整Kronecker矩阵与双平方证书核验"
status: "finite-exact-audit-replayed"
summary: "原样保留8机10任务种子的完整平方输入、两份不同实际调度及规范程序；一次重放核1024份原分配、400条平方有限边和四次幂实际调度，报告字节一致。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/actual_kronecker_product.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/actual_kronecker_product.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:examples/unrelated_machines/actual_kronecker_square_input.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:examples/unrelated_machines/actual_kronecker_square_input.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/unrelated_machines/actual_kronecker_square_assignment.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/certificates/unrelated_machines/actual_kronecker_square_assignment.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/actual_kronecker_product_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/actual_kronecker_product_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/private_graft_and_resource_repetition.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/actual_kronecker_product_review.md"
---

# 完整Kronecker矩阵与双平方证书核验

本对象保留[完整矩阵Kronecker偶次幂坍缩](../反例/完整矩阵Kronecker偶次幂坍缩--反例.md)的实际输入、两份完整平方调度、最终规范审计程序和冻结输出。基实例为固定的 8 台机器、10 件任务，其 OPT=3/2；平方完整保留 64 台机器、100 件任务和 400 条有限边，两份不同调度均使全部机器负载为 1。规范程序另检查统一初态加十五件同时改派，以及由此平方调度相乘形成的四次幂实际调度。

本轮全文读取五份原文件，保留其原字节及相对依赖目录，使用 Python 3.12.14 完整重放一次。新报告与原 1301 字节报告逐字节一致。本轮没有重新运行寻找证书的优化器；原证书中的 HiGHS 状态与目标值只是冻结的搜索元数据。可核证据是每件实际任务的合法端、精确费用和逐机负载重算。所有偶次幂、任意输入的未剪枝 assignment LP 可乘性仍依赖数学证明，不能由有限运行推出。

## 原资源、身份及目录合同

五份原资源保存在 tools/evidence/private-tree/actual-kronecker 下，目录层级与冻结仓库相同。程序以自身路径的 parents[3] 作为依赖根；把程序单独移动到平面目录会改变其输入定位，不能照原命令使用。

| 来源 ID | 原样保存文件 | 字节 |
|---|---|---:|
| 6433e6d79f7a8744650f | [tests/audits/unrelated_machines/actual_kronecker_product.py](../../../../tools/evidence/private-tree/actual-kronecker/tests/audits/unrelated_machines/actual_kronecker_product.py) | 7505 |
| 0249a542652111825a60 | [examples/unrelated_machines/actual_kronecker_square_input.json](../../../../tools/evidence/private-tree/actual-kronecker/examples/unrelated_machines/actual_kronecker_square_input.json) | 23074 |
| 2f3a8f4273e30dabbb4b | [evidence/certificates/unrelated_machines/actual_kronecker_square_assignment.json](../../../../tools/evidence/private-tree/actual-kronecker/evidence/certificates/unrelated_machines/actual_kronecker_square_assignment.json) | 1610 |
| 83712161b220eb1a4b39 | [evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json](../../../../tools/evidence/private-tree/actual-kronecker/evidence/certificates/unrelated_machines/actual_kronecker_square_independent_assignment.json) | 46398 |
| 34b9ea1a3015bd668efd | [evidence/runs/unrelated_machines/actual_kronecker_product_audit.json](../../../../tools/evidence/private-tree/actual-kronecker/evidence/runs/unrelated_machines/actual_kronecker_product_audit.json) | 1301 |

本轮另保存[完整重放报告](../../../../tools/evidence/private-tree/actual-kronecker/replay_report.json)、[stdout 摘要](../../../../tools/evidence/private-tree/actual-kronecker/replay_stdout.json)和[重放比对记录](../../../../tools/evidence/private-tree/actual-kronecker/replay_verification.json)。最后一项包括完整 hash、命令、解释器、字节比较、证书差异和有限运行范围。

从仓库根运行，输出必须选择尚不存在的路径，例如：

~~~bash
python3 tools/evidence/private-tree/actual-kronecker/tests/audits/unrelated_machines/actual_kronecker_product.py \
  --output cleanup/workspaces/Boss3/private-tree/kronecker-new-run.json
~~~

程序只使用 Fraction、itertools、pathlib、collections、argparse、hashlib、json、platform 等标准库，无优化器和其他仓库代码依赖。--output 必填，父目录可由程序创建，已有输出会被拒绝，最后以独占创建模式写完整报告。stdout 则有意去掉 sha256 和 limitations 两字段，不能把它当作完整报告。本轮保存了两种输出。检查使用 assert，需普通 python3 执行。

## 完整矩阵的约定及输入内容

种子机器的固定顺序是

\[
M=(S_{00},S_{01},S_{10},S_{11},R_{00},R_{01},R_{10},R_{11}),
\]

任务顺序为 \(A_0,A_1\) 及按 \((g,l,a)\in\{0,1\}^3\) 字典序排列的八件 \(B_{gla}\)。A_g 在 S_g0、S_g1 上均耗时 1；B_gla 在 S_gl 上耗时 1/2、在 \(R_{a,l\oplus ga}\) 上耗时 1，其余端不可用。每件原任务恰有两个有限端，共 20 条有限边。

平方机器 \((i,h)\) 编号为 \(8i+h\)，平方任务 \((j,k)\) 按 j 优先的字典序，行号为 \(10j+k\)。边当且仅当两个原坐标都可用，费用为 \(p_{ij}p_{hk}\)。输入完整保存 64 个机器对、100 个任务对，以及按任务行排列的有限端列表，每行四个不同端，未列端不可用。mixed 任务 A×B、B×A 全部包括在内。

程序自行遍历 100×64 个候选端，由种子公式重建 400 条有限边，再逐行比较输入，故没有把证书提供的稀疏边列表直接当成矩阵定义。最终代码要求总行数 100，每行恰有四个端 ID，ID 严格为 int、介于 0 至 63 且互不重复；随后把字符串费用转为 Fraction，核对应字典完全相同。机器与任务标签列表也必须等于固定字典序列表。

| 平方有限时间 | 边数 | 由种子端类别得到的数量 |
|---|---:|---|
| 1 | 144 | 12 条原单位端的两两乘积 |
| 1/2 | 192 | 12 条单位端与 8 条半单位端的两种次序 |
| 1/4 | 64 | 8 条半单位端的两两乘积 |

这提供固定完整输入的准确检查合同，不是任意 UM 矩阵的通用输入验证器。顶层 object 描述文字不参与数学核验；不影响资格和负载的附加元数据，也不由该程序统一认证。

## 两种完整调度证书

### 数值编号证书

第一份文件给出长度 100 的 assignment 数组，第 z 项直接是任务行 z 的平方机器编号；loads 为 64 个字符串“1”。规范验证要求数组长度正好 100，每个编号严格为 int 且在 0,…,63 中。对每个实际任务，程序把编号拆成两个机器坐标，检查两个原端都可用，然后以 Fraction 累加处理时间乘积，最后要求全部 64 行精确等于 1。

文件同时保留旧搜索的 status=0、HiGHS “Optimal” 消息、objective=0.0、bound=0.0，以及 machines/jobs/finite/exact_witness_peak 等元数据。该 objective 是原搜索模型留下的字段，不能据其数值零把调度 makespan 读成零。规范程序没有重跑 HiGHS，也不依赖其最优性声明；完整实际调度给上界 1，任意 A×A 任务在合法端时间都为 1 给下界 1。

### 显式标签证书

第二份文件保存种子机器标签及任务标签，把数学 A 改名为 f、B 改名为 e，坐标顺序不变。100 条 assignment 记录各包含完整任务对、完整机器对和有理数字符串 p；64 条 loads 各含完整机器对及负载“1”，另有 max_load=“1”和三个尺寸摘要。

程序先核种子标签数组，逐任务行核记录中的 task pair 确为该行预期的两个任务，把机器标签映射回 M 中的编号，再核 p 恰为原费用乘积。它还核整个 64 行 loads 表等于固定机器对顺序的一表，随后使用同一 verify_square 对所有真实负载重新计算。文件的 max_load 和尺寸摘要不是独立最优性证明，执行核验的核心是完整记录及重算结果。

两份证书都实际存有 100 项任务到机器映射，不是仅存 load 表。本轮把显式标签翻译成同一数值序号后，确认两份证书在 **29 个任务行**的目的地不同，具体行号记录在 replay_verification.json。两份见证不同并不自动证明其发现过程完全独立；旧研究者先按精确对象重构、后读作者证明的顺序由冻结审查记载，本轮重放不改写该历史。

## 规范程序的有限核验链

### 种子精确最优值：完整 1024 份分配

seed_options 由种子公式生成，10 件任务各有两个有限端。程序完整遍历 \(2^{10}=1024\) 份指派，没有分支剪枝或对称商；每份逐机计算负载并取最小峰值，得到 3/2。报告中的 seed_assignments_enumerated 写为常数 1024，但实际循环的选择空间确为上述笛卡尔积，随后另断言每件任务恰有两个端。

这里 1024 指完整原实例调度数量，与其他审计中的 DFS 递归节点计数不同。这个固定种子的穷举不推广为一般实例的高效最优调度算法。

### 统一初态与十五件同时改派

原程序的 start(j,k) 覆盖全部 A×A、A×B、B×A、B×B 类别，恰为反例正文的全任务初态。它逐项累计初态负载，并检查只有四个 RR 位置偏离 1：编号对 (6,6)、(7,7) 为 2，(6,7)、(7,6) 为 0。CHANGES 恰列十五件原任务的新机器对；程序确认实际有十五项改变，再对最终完整 100 项分配检查可用端与每行负载为 1。

这是一次同时替换的最终证书检查，不保证按任意顺序逐项移动时中间负载也不超过 1。该结构调度与两份存储证书分别接受检查，没有把“stored_certificates_checked=2”解释为所有已检查调度一共只有两份。本轮未把这份运行中生成的结构调度再序列化为第三份新证书；此前的[独立结构核验结果](../../../../tools/evidence/private-tree/structural_witness_check.json)已保存该公式对应的完整 100 项分配。

### 四次幂：完整实际任务调度，不是全边枚举

把刚构造的平方调度与自身相乘：遍历全部 \(100^2=10000\) 个任务对，对每个四坐标任务确定唯一的四坐标目的地，按四个种子费用相乘并累加。程序确认出现全部 \(64^2=4096\) 台四次幂机器且每台负载为 1。

这确实检查全部四次幂实际任务，但没有建立其全部 \(20^4=160000\) 条有限边，也没有枚举所有四次幂调度或求解其整数优化问题。每个实际目的地的合法性来自已逐项检查的平方调度及坐标积定义。四次幂可行上界 1 结合全 A 元组的单位时间下界，便可精确得到此实例的 OPT=1，无须最优解搜索。

所有 \(2k\) 次幂的命题仍由负载乘积分解和单位任务下界证明：本程序只实际展开 k=1、2，未对无穷多 k 作计算核验，也未研究奇次幂最优值。

### 种子未剪枝 assignment LP 的原初与对偶

规范代码检查两个确切种子见证。原初把每件任务的质量各半分到两个合法端，算得八台机器分数负载全部为 1。对偶给四台 S 机器各权 1/6、四台 R 机器各权 1/12，权和为 1，并计算

\[
\sum_j\min_{i:p_{ij}<\infty}y_i p_{ij}=1.
\]

两者一起证明这个种子的未剪枝 assignment LP 值为 1。代码检查的 primal 和 dual 都明确存在，不能沿用初版“只算 dual 却称 primal_dual”的旧缺陷描述来否定最终版本。

程序没有实现一般 LP 求解器，也没有对任意两矩阵计算 \(F(P\otimes Q)\)。任意合法非负有理矩阵（含零、空任务、不可用端）的乘法恒等式，来自反例正文的原初/对偶乘积证明。这一定义不按候选阈值删除长边，不等于剪枝 LST 或 CONFIG；本固定输入也没有测试一般定理的全部零边界。

## 冻结报告逐字段范围与重放

| 报告字段 | 精确含义 |
|---|---|
| seed_assignments_enumerated=1024；seed_optimum=3/2 | 固定 8×10 种子的全部原分配及其最优峰值 |
| square_machines=64；square_jobs=100；square_finite_edges=400 | 平方全输入尺寸，所有有限端已从原公式重建核对 |
| stored_certificates_checked=2 | 两份存储文件各含完整调度，均精确通过且分配不相同 |
| simultaneous_changes=15；all_square_loads=1 | 另行重建的公式初态加十五件同时改派使平方逐行负载为 1 |
| fourth_power_jobs_checked=10000；fourth_power_machines_checked=4096 | 完整四次幂实际调度中的任务与被覆盖机器数 |
| all_fourth_power_loads=1 | 上述调度每台机器的精确负载，未进行全图最优解搜索 |
| seed_unpruned_lp_primal_dual_value=1 | 只回算种子的一组具体原初及对偶见证 |
| sha256 | 最终程序、完整平方输入、两份证书各自原字节的 hash |
| limitations | 有限证书与一般偶次幂证明有别；无一般 LP 求解、困难性归约、奇次幂或一般种子行为结论 |

本轮完整报告与冻结报告 SHA256 同为 84fe6d1acb3554ef8ac85ceceb442c270347f8f84b1f5f308da5cb1b5c5afdc9。下表把 report 内四份依赖及报告自身的原字节标识明确保留；复制未改路径内部含义或文件内容。

| 文件 | SHA256 |
|---|---|
| actual_kronecker_product.py | 8e95e8c4b00654b2e85efbd37e294837796755ce189e7e933e5200752abebbb3 |
| actual_kronecker_square_input.json | e1ddd488baaae57191ca64136100ae21d8bfe45e0e5215396d13010cd69d2d1c |
| actual_kronecker_square_assignment.json | e9549591650682d90bb5918be55a3e74c8f7df4694cec4f50b54b09ddfe70f21 |
| actual_kronecker_square_independent_assignment.json | cc62a3c385008150e411590240c78ef8c6f6b182d7625552fc1523220ad0e9a3 |
| actual_kronecker_product_audit.json | 84fe6d1acb3554ef8ac85ceceb442c270347f8f84b1f5f308da5cb1b5c5afdc9 |

## 审查关系、已知拒绝边界与接续

本轮按文件名全仓检索，并比较已读数学正文§7、专门审查和现反例对象；五份本批来源逐源理解后再保存及重放。最终 v3 的严格端 ID、100 行、每行四个不同端，是既有审查修复的结果。旧版负索引别名、额外记录、遗漏 primal 及 v2 同端重复序列化的问题，须按冻结版本分别记述，不能把本轮最终版本通过倒写成旧版本已正确。

本批没有实际重跑错误变异，也尚未全文清洗 v2/v3 两份独立变异报告。它们是接续核验拒绝边界的直接相关来源，不包含在本批五源完成范围；目前已有正文对其历史结论的记载不等于这两份报告已被本轮逐项审读。

计算对象的复用方式是取得完整输入、两种完整实际调度及确定性 Fraction 检查器，直接核全部资格与负载。它证明固定完整矩阵平方会把实际 3/2 种子变为单位可行，配合解析论证得到所有偶次幂坍缩；不否定源专用困难图像、不证明一切张量都失败，也不产生一般 UM 近似算法。下一步若研究保 NO 的源专用乘积，仍须对全部实际低负载调度建立源解码，不能只保 assignment LP 的乘法值。

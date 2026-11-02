# 显式共同R/Z原子与固定边缘根扩张

八primary共984127B，双冻结提交同字节。完整原件和来源/blob/SHA保存在`original/`、`source-manifest.json`。三份正式正文位于`../../../state/`：

- `计算/六人共同回复的二十七原子必要系统障碍--计算.md`：完整16hist、27会员原子、K/O/W、1143/3889/1905关系及后来固定点排除。
- `计算/固定实际边缘的最大根图四十原子扩张--计算.md`：336行全部定义、40个根原子、八类边缘与163条件乘积证明。
- `程序/共同回复联合列的恢复与两级复核--程序.md`：发现/恢复/原verify的真实合同、依赖和各次执行边界。

## 两次新增计算，既有ZZ充分复用

`old3889-replay/`保存仅一次继承`attractive_nested.verify`调用。输入为原聚合1905列，SHA50a864…；执行时使用真实原相对布局和25件实际读取的依赖，work.py只作惰性找根标记，未执行任何协作控制器。调用检查全部描述符、非负/O1/W、3889行及普通行交叠系数正号。耗时约332.86秒、exit0/stderr0，3889=1083raw+2806bound，2329零/1560正。`all-old-slacks.json`的全部1905值和3889行名/slack直接从**该次调用已经计算的frame**保存，不第二次build，不含ZZ重算或LP。

`root40-definition-check/`保存新标准库只对40保存rootbits按336行原定义计算的13440系数，全部精确整数×60。336行43零/293正；按八actual/d边缘耦合得到163正乘积原子，27/40两侧全部边缘精确恢复。工具进程约0.620秒、exit0/stderr0，脚本内部约0.509秒。完整系数、全部336slack与163原子均在`all336-and-glue.json`。此程序不导入NumPy、root发现器或原verify，没有生成/报价全8192赋值矩阵，没有优化或完整SPE求解。

新增原joint_atoms/verify_joint_atoms主入口0、原root入口/原root.verify0、发现/恢复LP0、定价0。旧库回代是继承同一数学实现，新根检查是指定点的定义实现，均不冒全型最优性或新外审。

B本轮同SHA1905聚合与60ZZ已正式发表在`optimal-support-and-zz-audits-boss3`。其原独审只执行前105行，核117612字面项/同数分母恒等式、194隐式00、5612有序/对角RR上界、1905质量和60完整值（24零36正，18空轨道），未运行其旧库段。A已实读其完整事件与60值并逐字段对原主报告，没有再跑这117612项。复用路由及SHA在`full-field-review.json`。

## 数据与依赖

`full-field-review.json`保存全部16候选hist的域/组数/正质量统计、全部27压缩位串/质量、1905列种类及正列分类、新旧结果对照和正式B事件路由。一次内部字段检查初版曾错误用defaultdict访问后长度判正hist数，随即改为数正质量项；它未执行任何科学入口、未影响原数据或两次成功计算，最终字段报告通过。

`dependency-manifest.json`给本次旧verify真正读取的25个依赖，保留其原SHA和现有仓库去向；`dependencies-original/`保存这些实际原字节。`related/`另保两个仅关联、未代done的根定义源root_shared_prices.py和discover.py。它们使336的164原根行、两复制路径、低位优先bits及60缩放有原文依据。原root_shared_prices在import时会动态构造8192赋值并依赖mixed_pair；本包新40列检查不借stub声称那条原入口运行。

准备runtime时曾复制现有完整45件依赖包；只有25件实际被旧verify打开，其余20件不计本次读过/验证过来源，也未再次持久复制。45是布局准备数量，25是运行读取闭包；聚合schema另作为八primary之一记录。

## 从本包重新准备旧回代环境

`prepare_old_runtime.py`仅从包内`dependencies-original/`复制上述25件真实原依赖，再从`original/`复制已绑定SHA的主源schema，按原路径建立新runtime；逐件核SHA，不依赖本次scratch目录、被省略的20件文件或任何stub模块。它只另外写一份comment-only `work.py`供原源码找根，以及准备清单，既不导入旧数学模块也不调用验证函数。目标runtime必须尚不存在，避免覆盖。

在本证据目录执行以下命令即可。第一条只准备环境；第二条才会新增一次明确的数学回代，可能需要数分钟，应为新事件另存输出。

```sh
python3 -I -B prepare_old_runtime.py --runtime /tmp/cag-joint-old3889-new
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I -B replay_old_schema_only.py --runtime /tmp/cag-joint-old3889-new --output /tmp/cag-joint-old3889-new-slacks.json
```

需要Python3及NumPy/SciPy（原依赖会导入这些库，本回代不调用优化器）。本轮对准备脚本只作语法/文件路由检查，没有借添加说明再运行旧数学核。新根定点代码仅需Python标准库，可用`check_saved_root_atoms.py --output-dir`指定另一个尚不存在的目录；本轮也没有为此新增第二次根核验。

八primary与旧/新报告分开，历史源没有覆盖。所有数据都是必要条件点；虽共同会员可实现，后来三人源v1（有全目录K条件）和无K中间十三行都已排原27点完整延拓。root乘积保旧边缘，不能消掉这些负值。根与R/Z交叉IC未加入，当前六人half不由本包证明或反驳。

`source-dispositions.json`为八源逐件语义处置草案；`relationship-assessment.json`给实际关系与不能跨越的量词。正式Git/claim/checkpoint/done由根Boss串行办理，A未执行这些写端点。阶段三图未自动生成。

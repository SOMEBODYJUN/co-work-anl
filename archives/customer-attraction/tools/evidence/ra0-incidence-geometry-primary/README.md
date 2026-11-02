# Ra0 incidence_geometry 十六主源与两个固定输入的新补证

本包实际主源为同一 `R-a0bb57fa24044a8794bc7991918a19c6/incidence_geometry/` 下五程序、十一 JSON，共 **26868B**。父方 claim 已 pushed 为 `dc0f4ae783ff979b76c377fbdad1f89e7e523378`；这只是认领，不冒正文已发布或 done。全部主源在导出后全文读，原字节保在 `original/<source-ID>/<basename>`，每项双冻结 commit/path、blob、size/SHA 及导出元数据分别见 [source-manifest.json](source-manifest.json) 与 `export-metadata/`。没有改写旧 JSON 或 noisy 数值。

## 正式正文

- [二关联目录的精确终局探针与内部子题边界](../../../state/程序/二关联目录的精确终局探针与内部子题边界--程序.md)：六源，基础300/20000/root5000保存记录、完整生成与停止规则、内部3000例的基础/全标签域及静态缩减证明。
- [二关联完整策略锥与后继保底松弛的有限合同](../../../state/程序/二关联完整策略锥与后继保底松弛的有限合同--程序.md)：十源，真实后继IC锥、四浮点计数/模式缺口、k4/k5松弛全菜单与C5版本。
- [二关联保存点的两份常值三人策略](../../../state/计算/二关联保存点的两份常值三人策略--计算.md)：本次对两不同保存输入补精确全集、全策略、全部IC、theta/OPT；保原随机事件和当前补证身份。

[related-material.json](related-material.json) 绑定实际全文读的九个正式相关对象及 SHA，含当前七环逐人反例、旧五环非SPE障碍、规范全集算法、另个Rffea原探针以及R92静态子题缩减。旧已充分C5/C7审核没有重复；[relations.json](relations.json) 给阶段三关系和逐条承重证据。[all-report-read-ledger.json](all-report-read-ledger.json) 是十一 JSON 的结构读域索引；它不代替完整原件或数学判断。

## 原程序可运行闭包与历史版本缺口

[reused-dependencies.json](reused-dependencies.json) 指向已保存的四个规范模块共25475B及精确SHA，实际完整读过。四个原脚本用自身 `parents[5]` 加入根路径，须恢复原目录布局和根 `customer_attraction` 包；本证据按ID散置的原件本身不等于可直接运行原布局。floor MILP 无此包依赖。规范原精确代码只需标准库；cone另需NumPy/SciPy linprog/HiGHS，floor另需NumPy/SciPy milp/HiGHS，历史版本未冻结。

原代码入口接受的参数和副作用已在正文逐项解释。基础随机输出可省为stdout；有输出路径时所有探针都 `open('x')`，不覆盖已有文件、不创建缺失父目录。C5只打印JSON。没有冻结原命令、stdout、环境和各样本轨迹，不能假称一份默认CLI就是旧实际命令。尤其旧基础300/20000报告缺当前代码的根字段，旧前三锥报告缺当前代码的mode字段，不能字节复产或补历史目标。

## 本次唯一数学执行事件

原随机 main、原锥/松弛 main、LP、MILP、旧C5/C7重放、新随机输入，当前均 **0**。本次只执行 [fixed_saved_inputs_audit.py](fixed_saved_inputs_audit.py) **一次**，输入是三旧报告中两个不同 `worst_ratio.instance`。为了避免导入不明环境，将已核同SHA的四规范模块复制到clone外隔离目录，再显式传 `--package-root`。实际参数、cwd、开始/结束UTC、Python版本、脚本/stdout SHA和退出状态保 [execution-boundary.json](execution-boundary.json)，完整stdout/stderr分别是 [fixed-audit.stdout.txt](fixed-audit.stdout.txt)、[fixed-audit.stderr.txt](fixed-audit.stderr.txt)。stderr为零字节，exit0。

完整新输出 [fixed-saved-inputs-report.json](fixed-saved-inputs-report.json) 包含全部输入、全部根终局、精确最差福利/OPT、theta与全部最小背景、两张31/43行完整动作表及核验计数。A为71客户/五题/三人，常3策略，唯一根终局3³，W51/OPT69，theta及根最低17；B为88客户/六题/三人，常5策略，根终局5³或4·5²，最小W50/OPT81，theta及根最低50/3。339个非self比较中336严格/3平局；含self共413，没有IC违反。报告和动作表全部阅读，新输出不是原报告遗失策略的历史恢复声明。

如需独立复核本次保存点，可从项目根执行下面的**新固定审核**；`NEW_OUTPUT.json` 必须不存在。此为可执行说明，不是额外运行记录：

```sh
python archives/customer-attraction/tools/evidence/ra0-incidence-geometry-primary/fixed_saved_inputs_audit.py \
  --package-root archives/customer-attraction/tools/evidence/strategy-cones/original \
  --source-dir archives/customer-attraction/tools/evidence/ra0-incidence-geometry-primary/original \
  --output NEW_OUTPUT.json
```

新审核只有两固定输入，不运行原随机发现。若改变规范模块或输入，应重新核SHA并另存事件，不沿用本次exit0。

## 数学边界

两个新证点均W=3theta、half余量正，不反half。k5浮点松弛解析恢复为2/3加权重标C5，坏分支末位可严格偏离，故只是保底接口障碍；k4微负质量与近零epsilon不是精确阳性。1800个锥报告计数/2152800累计行是旧保存历史，三份缺mode，不是本次成功精确对偶。内部子题的全标签关联可到四，不能叫全目录rank2。

一般全标签rank2逐人theta已被另个七环完整SPE否定；这十六源没有闭合二关联聚合门槛、任意人数half或当前六人目标。清洗回执保存每源实际读域、比较和独有处置，发布/done由父方另行串行办理。

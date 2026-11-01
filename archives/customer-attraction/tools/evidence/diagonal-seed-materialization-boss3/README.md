# 对角R/Z十八主题单位实例：原件、物化事件与指定尾障碍

三primary共92407B，完整原件在`original/`；所有252/288兴趣类型及其正整数复制数均保留。指纹和完整冻结定位见[source-manifest.json](source-manifest.json)。正式对象：[对角末回复十八主题单位客户实例](../../../state/构造/对角末回复十八主题单位客户实例--构造.md)。

## 实际执行与精确输入

[input-manifest.json](input-manifest.json)绑定旧5108 combined（816453B、d1aeba…）和旧10344 pair（158498B、090586…），不是5277。原writer仅需这两文件与标准库。本次放到独立空目录执行一次：[执行记录](replay/execution.json)、[stdout](replay/stdout.jsonl)、[空stderr](replay/stderr.txt)，exit0，约.073秒。Rdiag/Zdiag两个新JSON分别与冻结原件逐字节相等；没有覆盖原件。

新生成的[Rdiag meta](replay/seed18_Rdiag_meta.json)、[Zdiag meta](replay/seed18_Zdiag_meta.json)保完整别名、尺度、两输入SHA及路径。它们是本次输出，不假装等于未提供的历史meta原件。两游戏均18个不同非空覆盖列，映射恒等；全部单位客户恰属于一个T，所以OPT6精确等N。N分别为1355844795595364297990920717351092816000、22671100841923417905691033278899642291933621798808000，两个actual覆盖/N同为原低于half的w，但没有SPE继承。

## 当前指定前缀末两人精确审计

[audit_instances_and_actual_tail.py](audit_instances_and_actual_tail.py)逐条核完整unit-type输入，然后只固定actual前四主题、枚举每例18×18=324个有序终局，保每个第五行动后全部末位BR及第五利润区间。一次运行exit0、约.209秒，完整[输出](replay/instance-and-actual-tail-audit.json)、[stdout](replay/tail-audit.stdout.json)、[执行记录](replay/tail-audit.execution.json)保原结果；不导入原图、物化器或SPE库，未运行六人root BI或LP。

两例actual末位A6是BR，原尾却不能由任一尾SPE实现：第五位改A6后，Rdiag的所有末BR是T1…T6，Zdiag是Zdiag1…6；对这些回复均严格增益。全部有理收益/BR/324终局在输出中；[归一展示](replay/normalized-tail-witness.json)由已审计收益直接整理，无新博弈求解。原字段profile_is_game_SPE是简写，准确含义是给定有序actual路径不能属于任何完整历史SPE；不将一个行动列表称完整策略。

## 历史报告与复用边界

本批另完整关联读5199B Rdiag前缀报告与两1111B根BI/控制器报告，原件在`related/`，完整定位见[related-reports-manifest.json](related-reports-manifest.json)，不额外primary/done。两root报告的exact_input_root_outcome_count=1、worst_ratio=1与另外三次float cone试验分开；本批没有重跑历史root BI、早期depth0…3保底或那些float试验。当前Rdiag末两层的u5、最大可信floor、u6与旧前缀报告精确相等，见[历史对照](replay/historical-comparison.json)。

[comparison-manifest.json](comparison-manifest.json)记实际全文对象与前批读取复用；[relation-review.json](relation-review.json)分开数据投影、单位化/别名、字节重放、OPT识别、局部SPE补全反驳与历史报告。共同客户会员和终局收益保持不等于完整策略继承；阶段三图未改。

## 重现

从仓库根，可先只恢复三份不可变输入到新的绝对目录，再自行执行原writer；前一步不运行数学：

```sh
python3 archives/customer-attraction/tools/evidence/diagonal-seed-materialization-boss3/materialize_runtime.py /absolute/new-seed-runtime
python3 /absolute/new-seed-runtime/materialize_diagonal_seeds.py
```

原writer直接覆盖同目录两seed与两meta，因此不要对`original/`运行。若想重跑本次局部审计，应另建完整证据副本并删掉其旧结果文件，保持原seed/meta；审计器以独占创建写结果。原输入和所有输出均应核SHA，不能把别的5108/10344/5277点替换而沿用本报告。

本包只认证两份合法六人单位客户输入、字节生成和指定低覆盖路径失败；不是六人half反例、通用最优性证明、完整根SPE验证或新颖性/外审。三份逐源receipt由Boss3在正文推送后串行登记。

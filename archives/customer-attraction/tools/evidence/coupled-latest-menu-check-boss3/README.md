# R5 5277行联合点与普通新Y末价

四primary共846028B，全部完整原件在`original/`；原始向量包括2033列及所有零质量/嵌套描述符。双冻结定位、blob、大小、SHA见[source-manifest.json](source-manifest.json)。本批正式对象：[实际末主题联合主图的局部切面与末价停界](../../../state/计算/实际末主题联合主图的局部切面与末价停界--计算.md)。

原点SHA `303291e7ec19437d226bb8d33d3e689beaf54f52103fde53a12e28f1058f806a`；不是R2 5259或后来的5494/5664/5692点。新wrapper先设latest/local-v2，实际5198母行再加79条件B枝行，得5277/2033。18条local-v2由5nested、5requery、8portfolio组成，均为冻结有限行，不是无限全目录闭包。

## 本次两件成功执行

1. 原916B `check_B_menu_actual_last_price.py`执行一次：[执行记录](replay/checker.execution.json)、[stdout](replay/checker.stdout.txt)、[空stderr](replay/checker.stderr.txt)，exit0，约0.046秒。它只读原点及320B旧报告，核一条真actual末位价格的精确负值，打印输入SHA；不生成全图，不写文件。
2. [verify_latest_point.py](verify_latest_point.py)调用原builder一次，完整列序/序列化身份/长度与全部weight核对，全部5277个具名行有理回代：[执行记录](replay/matrix.execution.json)、[stdout](replay/matrix.stdout.txt)、[空stderr](replay/matrix.stderr.txt)，exit0，约37.194秒。它是同实现回代加接口核，不是第二套独立行实现。原master main/verify、float LP、完整SPE求解均0次，本批无失败尝试。

[完整summary](replay/latest/summary.json)记录230正列、2120零slack，O1、W约.48844904255403476；正列K1/hist11/joint98/overlap103/B态17。完整具名行和有理余量见[全部5277行](replay/latest/all-row-slacks.json)，完整16hist条件边缘见[hist边缘](replay/latest/histogram-marginals.json)，新增18行分别见[局部切面表](replay/local-eighteen-slacks.json)：五nested均正，五requery有2零，八portfolio有1零，其余正。

与5259全2033描述符、K、16hist质量、W均相同，但168隐藏质量改变（joint80、overlap70、B态18），正列242→230。普通Y菜单actual1…5和CAP正，actual6平均行负；其六倍精确为

`-37649034345157581458948354799628857270185177/275841129375927621860270205917097912705837888`。

这排除保该点质量/ell坐标的完整SPE补全，不能称原模型half反例。当前stdout与冻结320B报告schema不同，保各自身份，不伪报原字节相等。

## 依赖和复现

[runtime-file-checks.json](runtime-file-checks.json)核47份母依赖、前批5源和本批4源，共56可用冻结文件运行后逐SHA不变；不是动态加载trace。[materialize_runtime.py](materialize_runtime.py)只复制核同原字节，无程序执行、网络或凭据。

从仓库根、对尚不存在的目的目录可另建执行事件：

```sh
python3 archives/customer-attraction/tools/evidence/coupled-latest-menu-check-boss3/materialize_runtime.py /absolute/new-latest-runtime
python3 -B archives/customer-attraction/tools/evidence/coupled-latest-menu-check-boss3/verify_latest_point.py /absolute/new-latest-runtime latest /absolute/new-latest-output
python3 -B /absolute/new-latest-runtime/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_5/check_B_menu_actual_last_price.py
```

须开启assert；builder顶层需要NumPy/SciPy，检查价格的916B原码只用标准库。原wrapper的无verify发现模式会覆盖源码目录exact/status，不应对`original/`运行它；上述命令未调用发现模式。

## 相关纠错和关系

[comparison-manifest.json](comparison-manifest.json)列实际全文比较的旧正式对象与18行源码/数据。额外关联3013B [pending五记录](related/coupled_pending_cuts.json)绑定相同点SHA，三portfolio/两query8、11 requery尚未共同重优；后两在对角i=j上查询同一个Ci=Cj，所以五记录至多四不同约束。父方持有其primary，独立数值核验由“同源再查询与容量报价的三份冻结切面包”承担，本批只读相关源，不额外done或重复运行五cut。

[relation-review.json](relation-review.json)分开来源/实现、cut模板转用、两个不同向量的比较、遗漏合法价反驳和后续pending。阶段三图未改。本包没有完整共同客户隐藏实现、全历史策略、精确LP最优或六人half结论。逐源receipt在`cleanup/workspaces/Boss3/receipts-20261101-coupled-latest.json`，由Boss3正文checkpoint pushed后串行done。

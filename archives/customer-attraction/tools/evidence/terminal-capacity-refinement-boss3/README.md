# 共同容量29切面与5112有理点的两源证据

正式对象：[共同容量与多查询投影的二十九切面精化点](../../../state/计算/共同容量与多查询投影的二十九切面精化点--计算.md)。本批只处置两份新冻结数据，复用前批已读且已完成的投影源码/基域，不替依赖再次done。

## 原件与真实差别

`source-manifest.json` 保两个冻结commit、原路径/blob、SHA/大小和持久位置。原件均不改写：

| 源ID | 原文件 | 字节 | SHA-256 |
|---|---|---:|---|
|504b5c22ca1331dc9ef5|terminal_capacity_refinement_cuts.json|11523|22230fad8e877ae37755803107941f37b79f49278479a84856e15b71eea0995b|
|2ac41f3470c74caa54b1|terminal_capacity_refinement_exact.json|819848|0bf850f2489986a56cc2847cfdae0a1f8d86fe1b069a425cad5d40fa253e91ee|

29条全部mu13、全部beta_last正、9条beta_middle正，15R/14Z，覆盖actual源2/3/4/5；23条单正查询、6条双正查询。完整参数及(A,B)预算在正式表逐条保留；其它mu全零。与前8条“全Z/单A6/beta0”不同，不能从同程序名推断相同参数特性。所有参数非负和匹配的真IC投影合法性已核，不把记录数29说成29条线性独立关系。

819848B点的全部12字段及1905列均实读，含所有零坐标。194正列为1K/10hist/87joint/96overlap；base5083+29=5112，原W严格低于half。源文件没有精确最优对偶、策略或全历史证书。

## 一次原容量核验

`run_original_once.py` 按现共享冻结依赖树与原repo相对路径，在clone外新目录物化输入。三份此前完成的源码/八cut以原字节放 `related/`，身份在 `related-inputs-manifest.json`；控制器work.py仅写根定位注释，不执行。真实argv为 `python3 -B <原层级>/refine_terminal_portfolio.py --capacity --verify`。

实际约38.936秒、exit0、stderr空，原stdout160B是字典repr而非JSON，精确记录5112行/base5083/cut29/min0/W。`runs/original-execution.json` 保UTC开始/argv/cwd/耗时及全部输入身份。52条物化角色记录对应49个唯一文件，三个同路径覆盖都是同SHA字节；它们是可用输入清单，不是加载追踪。输入前后全部不变。

本批原容量入口1次，默认5083入口0次，参数LP/发现循环/新策略搜索0次。`--capacity`本身只是预装前八行和切换输出前缀；通用finder原来就支持beta，不是这个旗标才启用容量变量。

## 独立完整记录及29行核验

`audit_point_and_cuts.py` 复用已读标准库结构审计，按新两源身份、29行及非零beta/双查询适配。全1905记录、194隐含00、2612交叠上界、O/W/六利润及54局部价/CAP通过。29个向量用实际索引对和字面2^n后继位构造，先合正mu再min，不用作者count-compressed psi；原纯函数仅作为对照通过AST提取，不执行顶层或发现器。

29×1905=55245坐标全等，包括实际中间/末位容量系数；mu13末补三零后的另55245坐标全等。当前29行6零23正，前8行当前全部严格正。完整29个参数/预算/余量、前8余量和旧点回代Fraction保在 `independent-audit.json`。

独立入口总2次。首次成功完成后，为把比较用4个静态输入也全部移出clone，按SHA复制到外部 `audit_inputs` 根，再用同脚本执行正式完全外部输入核验。两次完整报告和stdout逐字节相同；保 `runs/initial-independent-audit.json` / `initial-independent.stdout` 以及最终报告/stdout，`runs/independent-executions.json` 如实登记两次路由与同SHA。没有为第二次更换数学参数或重跑原5112入口。

最终所有独立输入及输出均在clone外，具体静态输入身份见 `independent-inputs-manifest.json`；原图运行及独立静态依赖分别路由，不依赖Git事务中目录暂存的可见性。

## 实现边界和旧点区别

当前151个overlap低于真实Fréchet下界，原LP只设非负与上界所以仍准确通过其必要行。完整短例列953/hist117、actual000000、H=(0,3,2,0,0,0,1,0)、两个完整group与两边缘均h/v0保正式正文和报告；全部151项也保留。它只否定原辅助量全作字面同客户交叠，不说所有点不可实现或六人half被反驳。

新点K、10个正hist质量、W均较5083改变，231权坐标不同；29条在旧5083全负，旧5075/5108各28负1正。三份旧点的完整非weight身份与精确值均在报告，不从前8点同K/hist的结论迁移到当前点，也不免费继承5180/5277/5692其它关系。

程序模式、完整基域及原局部引理详见前批[组合查询程序](../../../state/程序/共享末回复组合查询的发现与有限精化程序--程序.md)。本批补的是容量/双查询数据及5112实际核验，不重复宣称一套新机制、全图独立实现、精确最优或完整SPE。

## 后续主动复现

新原容量核验事件可调用本包 `run_original_once.py REPO NEW_RUNTIME`；新runtime必须不存在。它会写新的执行记录，不能冒充本包已保存事件。独立核验的四份静态比较输入可先用 `materialize_audit_inputs.py REPO NEW_AUDIT_INPUT_ROOT` 复制，再运行：

```sh
python3 -I -B audit_point_and_cuts.py --source original/2ac41f3470c74caa54b1/terminal_capacity_refinement_exact.json --output /absolute/new-audit.json --repo /absolute/new-audit-input-root
```

上述相对脚本/原件路径以本证据包为工作目录；静态物化工具只核指纹和复制，不执行数学。持久共享依赖及两个真实执行层次的路由见 `dependency-manifest.json`。正文解释必要行实现、有限点分离、共同预算与字面实现障碍，三级超图仍留第三阶段实际审边。

# 原13查询末回复独立局部审计的两源证据

正式对象：[十三查询末回复投影的原独立局部核验](../../../state/计算/十三查询末回复投影的原独立局部核验--计算.md)。本包只完成原审计代码和320B报告，人工MD及现作者代码是范围比较，不替它们再次done。

## 精确原件

`source-manifest.json` 保存双冻结提交/原路径/blob/SHA/大小/当前保留路径。原1913B代码SHA为 `5befae25d6c5f8905a9526d2b53f69ab1b425f3855b3695ab814864d1df8e759`，320B报告为 `feff3843da4004a73406fd3abcfec1a7a37926445808ae6618c65eacfc195b13`，均原字节保留在各source ID目录。

代码只有share函数，全部数值循环和写报告在顶层；没有main guard，import也运行。它不导入/读取/调用作者代码，不读任何输入文件。原JSON七字段精确为scope、28800恒等式、3360最小值、3价格模式、8查询位模式、K系数字符串及PASS；没有审计/作者SHA、版本、时间、行向量或全图输入。

## 唯一原脚本重放

`run_original_once.py` 把源码复制到一个新空clone外目录，直接 `python3 -I -B review_terminal_portfolio.py`，不复制原报告到将写目标。原320B报告保在原件目录，只作结果比较；它不是审计程序的执行输入。

实际约2.674秒、exit0、stderr空，生成 `review_terminal_portfolio.json` 和stdout均320B，逐字节同冻结原报告。`runs/generated-review.json`、`original.stdout`、`original.stderr` 和 `execution.json` 保存真实字节、argv/cwd/UTC时间、耗时及前后指纹。

本批原审计执行1次，新独立数学实现0、作者程序/row执行0、LP/原图执行0。相同历史代码重放不是再加一个独立审查者。报告没有历史源码绑定；当前新事件只绑定本次明确5bef…代码到feff…结果，不倒填历史。

## 实际域与静态比较

完整价/查询模式在正式正文保留：13位q、3组固定价格，包含一组全13mu正；q只有全0/全1/交替和5个one-hot共8模式，非全部8192模式。n1…5，p0…5−n，ell p…5共有70个数值对；每对乘2t/8q/3价格，得3360min，再乘2^n字面后继共28800恒等式。只有50对满足actual前缀ell≤p+n，且q未执行作者actual/旧词/self绑定；这些是代数局部测试，非SPE实例。u/last/K为固定有理占位数，只核等式/min相等，不核测试rhs项非负。

`audit_source_scope.py` 只读AST并作整数循环计数，不执行旧数学程序。它确认全部导入仅标准库、无读输入文件/作者导入、顶层执行，并比较当前作者psi返回式与原compressed表达式的AST完全相同。结果为 `scope-audit.json`。

对照作者冻结原件仅放 `related/terminal_portfolio_cuts.py`，SHA `46815b59bb97fad17d2aab75ab9a698fe3a3884bc41caac4196bf8e0251d5389`，来源f47已在前批完成；身份见 `comparison-manifest.json`。本批没有运行该作者文件。核心MIN表达式一致不能绑定旧历史被审整文件SHA，也不认证当前qvec16、ct/K或1905 row实现。

2493B历史人工MD确有13Q通用语义、ct归一、K收费一次和仿射读出的论证，正式对象准确保留，不将其删掉或归进28800程序检查。前8/29向量构造及5083/5112原入口又是另外事件，范围和次数分别链接正式对象，不合并为全历史SPE认证。

## 复现

从本包任意位置调用绝对脚本路径 `run_original_once.py NEW_EMPTY_RUNTIME` 可重做一条新事件；新目录必须不存在。直接import原冻结脚本会写其旁同名JSON，不宜作为纯读取方式。本轮只在独立目录运行，原件未被覆盖。`audit_source_scope.py` 是静态检查，不重新运行28800/3360循环。

完整数学身份、域、历史未绑定和当前复现关系在正式正文解释，三级超图留第三阶段逐边整理。

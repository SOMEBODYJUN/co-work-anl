# old_query_reply_cuts.py 精确网格程序证据

主源 `e061ba9e37672cdc056b`，4128B，SHA256 `1d2feaf16a20f6d64158b5a1887d63e5500d17489977ce604157af7c95f057d5`。[正文](../../../state/程序/旧查询回复的有限网格分离程序--程序.md)展开真实量词、八字段、9900计数、排序/去重/截断以及既有PAIR端点。[manifest](manifest.json)保冻结提交、原路径、字节和实际阅读范围。

- `original/old_query_reply_cuts.py` 未改字节；`related/` 保存直接数学核心和原八cut小表。
- 815347B输入复用 [all_reply_floors_exact.json](../all-reply-actual-floors-program/related/all_reply_floors_exact.json)，不重复归档；SHA `f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314`。
- [audit_old_query_grid.py](audit_old_query_grid.py)用独立六索引边枚举与隐藏二元位最小化重算整个有限网格；原groups/psi只作为比较目标，不调用discover/build或LP。
- [replay/grid-audit.json](replay/grid-audit.json)保360结构的全部网格最小点，以及9900值序列SHA；9880正、12零、8负。11000个局部字面投影与原快速ψ相等。独立八向量与72-PAIR的比较由配套数据对象负责，本脚本不重复。
- [rerun/execution.json](rerun/execution.json)原样记录本轮前段唯一一次原发现入口；本续接未重复运行。原算法也是全Fraction，没有浮点求解器。exit0、stderr空，输出 [report.json](rerun/report.json) 与冻结2130B表逐字节相同。
- [point-comparison.json](point-comparison.json)只比较原4963点与后来4971点的全部列描述符和权；同W但114权不同，不能互换输入。

自足重放默认只执行独立局部审计：

```sh
python3 -B run_local.py --out /path/to/new-grid-audit
```

脚本先核原码、核心、八cut和共享输入SHA，再在指定输出目录下准备临时冻结相对布局；用未执行的work.py作路径标记，namespace customer_attraction仅含原priced模块。它没有声称执行旧包初始化。结束后删除临时布局。显式加 `--mode original` 才重复作者discover入口；本续接未运行local或original模式；前段两套已完成核验和唯一原入口记录足够供核对。

当前只核有限输入的9900网格及相关局部公式，不认证4963/4971/5108全部约束、连续价格闭包、完整目录SPE或一般六人half。原输入的全部旧图可行性保持作者报告身份。

[自查](self-check.json)只记录本续接实际发生的JSON/源码哈希/相对链接和报告内部一致性核验，不伪装为再次9900扫描或整图重跑。原字节、唯一原运行stdout/stderr、完整独立360结构最小值及点比较均原样沿用；[manifest](manifest.json)分别标明继承证据与本续接动作。

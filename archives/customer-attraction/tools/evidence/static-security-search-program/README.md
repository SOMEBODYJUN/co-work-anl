# 静态安全值有限搜索程序证据

主源99f46e401eb918a3f747完整3195B正常clean show并原样保存于[original/search_security.py](original/search_security.py)，SHA4db23c4998abc729dafb08bf6535ec825231a7ba21a37690ca52e374b33cb842。[程序正文](../../../state/程序/静态安全值的有限搜索程序--程序.md)保模型、全部SPE结果集合递推、int16范围、真正静态整数安全LP、六项返回值、随机CLI和best身份。

[source-manifest.json](source-manifest.json)保两冻结提交、原字节和实际输入身份。原程序无本地导入；只需标准库、NumPy、SciPy。[related/random_best.json](related/random_best.json)是本轮真正加载的1179B保存输入，数据主源由配套代理处理；[related/fractional_cover_safety.md](related/fractional_cover_safety.md)是全文读过的4140B静态基准稿，仅related不额外done。[comparison-manifest.json](comparison-manifest.json)保七现行数学对象的语义比较和指纹。

[replay_saved_input.py](replay_saved_input.py)以非main名称导入未修改原源码，只执行一次Probe(5,7)和一次solve(saved_weights)：1整数BI、1静态安全LP、0随机main/RNG。[执行记录](replay/execution.json)与[进程捕获](replay/process-capture.json)记录初始化0.012306081秒、solve0.017826781秒，exit0、stderr空及源/输入前后SHA相同。未重生旧第238号提案或历史总轮数。

- [original-return.json](replay/original-return.json)：target五次T5、W29、数值v/ratio/query/target四字段同旧报告；792计数状态各单结果；scale60/int16系数≤60、int64收益≤1596与充分界2040。
- [outcome-sets.json](replay/outcome-sets.json)：完整792原计数状态结果集合，不是2801节点有序动作表。
- [terminal-payments.json](replay/terminal-payments.json)：原返回462终局缩放收益矩阵，未占用行动按原码为0。
- [stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)保包装调用原输出；原solve本身不打印。
- [execution-scope.json](execution-scope.json)列已执行及未执行，不把函数调用冒随机CLI或旧发现事件。

配套[精确数据对象](../../../state/计算/五人七主题静态安全值探针的精确取等点--计算.md)与[point-audit.json](../static-security-search-data/point-audit.json)独立展开单位客户，给v=29/5、W29、OPT34、精确比1以及全有序历史唯一SPE恒选T5的解析证明。它一次核210×7有理份额、462终局覆盖，未调用原BI/LP；程序包不重做。[共享指纹](shared-audit-binding.json)绑定这些证据。旧ratio0.9999999999999999不是反例。

从仓库根复现本保存点到一个新的不存在目录：

```sh
python3 -B archives/customer-attraction/tools/evidence/static-security-search-program/replay_saved_input.py --source archives/customer-attraction/tools/evidence/static-security-search-program/original/search_security.py --input archives/customer-attraction/tools/evidence/static-security-search-program/related/random_best.json --out-dir /tmp/static-security-new-saved-point
```

该命令不是随机历史重放；换数值环境可能改变最后几位浮点，精确点仍以有理证书为准。原CLI语法为`python search_security.py n k tries out`，本轮没有运行它。安全值是静态查询分布对不观察本次查询的整数背景，不是顺序SPE的总付款；有限输入上的精确BI也不穷尽所有客户实例。

[check_package.py](check_package.py)只核原字节、记录结构、共享指纹、JSON/Python语法、交付链接与回执，不执行BI/LP或独立数学审计；[artifact-manifest.json](artifact-manifest.json)和[self-check.json](self-check.json)保交付绑定及静态结果。

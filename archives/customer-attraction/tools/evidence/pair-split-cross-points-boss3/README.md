# 固定split/cross阈值上的两份配对可行点

正式对象：[拆分与跨源固定阈值的配对可行点](../../../state/计算/拆分与跨源固定阈值的配对可行点--计算.md)。

source-manifest.json给两primary完整来源和SHA，original保114803B pair_closure_exact与127211B pair_cross_exact。related-manifest给旧split/cross两个1905输入与当前pair/zz代码；这些related不额外done。runtime-dependency-manifest保存原50件可用冻结依赖的定位与补录合同，可用清单不冒加载跟踪。

两完整当前事件均在clone外独立进程，由verify_pair_mode.py调用未改原build各一次：

- split：7931行全部有理非负/min0，275保存变量全元数据绑定、22 R层/1903隐式交叠，37.81秒、exit0/stderr空。
- cross：显式cross+priced+optimum，9311行全部通过，302变量/24层/2102交叠，38.12秒、exit0/stderr空。
- 没有原main/CLI、linprog或求新点；没有重复旧split/cross原向量的全图，而是在重新分配Z后的新点重核旧3945/4927仿射行。
- 独立阈值/守恒读取恢复全部新1905坐标，R边缘保持，Z及旧RR改变。275/302不是客户数或主题数，隐式1903/2102不再存一份独立自由数组。
- 33/38个正有理原子同时给全部Z积分和所有同层ZZ最小交叠；不是逐对随意选有利交叠。索引平均后的目录主题大小均≤K且K确被主题达到，有限单位化存在性和SPE义务分别保留。
- 现点普通价格独立重算：7931实际末位查询旧B/C两负；9311保留四R早源负价，并出现两个C族对角Z早源负价。因此实际低覆盖路径不能是完整SPE，虽有限闭包和会员实现都成立。

replay/split与replay/cross各自保存：

- execution-record.json / stdout.txt / stderr.txt：两次当前事件的真实输出与版本；
- semantic-and-full-matrix-report.json：九顶层字段、全部数量、变量界、目录大小、所有价格及完整分区统计；
- all-row-slacks.json：全部7931/9311具名行的有理余量；
- common-cube-atom-recipe.json：共同R/Z会员的33/38原子配方；
- mapped-1905-weights.json：新Z及RR共同阈值重建的旧布局向量，明确不是原source文件或SPE。

replay/preserved-margins-and-history.json复用已保存旧14价和36地板审计，核本次值与固定边缘应有的不变量一致，不重跑旧审计。432B报告point SHA/7931/W/min确匹配，但历史source SHA210ae7...与现bf72...不同，代码版本缺口没有被当前通过消掉。

从仓库根复原独立运行树：

    python3 archives/customer-attraction/tools/evidence/pair-split-cross-points-boss3/materialize_runtime.py /absolute/new-runtime

之后需要时可以独立复核：

    python3 -B archives/customer-attraction/tools/evidence/pair-split-cross-points-boss3/verify_pair_mode.py split /absolute/new-runtime
    python3 -B archives/customer-attraction/tools/evidence/pair-split-cross-points-boss3/verify_pair_mode.py cross /absolute/new-runtime
    python3 -B archives/customer-attraction/tools/evidence/pair-split-cross-points-boss3/compare_preserved_margins.py /absolute/repository-root

每种模式另开进程，不能在一次Python导入缓存里改argv后复用模块。原verify依赖NumPy/SciPy，assert须开启；它没有完整元数据绑定而本包增强核补齐。materializer只复制SHA核过的冻结文件和注释性work.py标记，不执行Git、网络或研究入口。run_mode_once.py是本次事件组织脚本，拒绝覆盖已存事件记录；直接复核会更新本包当前replay报告，不改original。

有限图可行、共同客户会员实现、指定路径SPE、精确LP最优和全输入六人half分别保留。没有用master156主题的尾部结论代替这两输入各自的报价否定，也没有把当前代码冒作432B的历史来源版本。

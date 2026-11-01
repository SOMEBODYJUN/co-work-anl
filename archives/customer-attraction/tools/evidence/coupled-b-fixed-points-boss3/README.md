# 实际末主题单枝/三枝：完整固定向量与当前精确核验

五个primary原文共1859305字节。原路径、双冻结提交、blob、size/SHA及原字节位置见[source-manifest.json](source-manifest.json)。单枝844597字节点复用既有同字节证据，其余四原件在`original/`；没有截断列向量、丢掉零坐标或改写历史header。

正式正文：

- [实际末主题单枝与三枝条件联合的精确点](../../../state/计算/实际末主题单枝与三枝条件联合的精确点--计算.md)：完整新增行、列身份、两个有理点的全部行回代、普通Y漏价与5259→5494→5664→5692版本边界。
- [共同最大主题会员的真实分支证书线性程序](../../../state/程序/共同最大主题会员的真实分支证书线性程序--程序.md)：4213字节max_branch_lp完整语义，包括coupled没有调用的充分证书solve和自定义参数守卫。

## 两份成功的当前精确回代

[verify_fixed_point.py](verify_fixed_point.py)只调用冻结作者`build()`，不调用float LP或原main。逐列检查JSON序列化身份与顺序、全部长度、每个有理质量、O/W/gap及正列数；逐行保存全部具名有理slack。它是原矩阵同实现回代加接口/漏价核，不是独立矩阵生成器或完整SPE检查。

| 点 | 行/列 | 正列 | 零slack | W近似 | 结论 |
|---|---:|---:|---:|---:|---|
| single | 5259/2033 | 242 | 2125 | .48844904255403476 | 全部保存行非负；source4新Y实际末价负 |
| families | 5494/2801 | 224 | 2391 | .48882270176796966 | 全部保存行非负；source4新Y的actual2/3/4/6价和CAP负 |

各16个旧hist的完整有理质量和逐枝条件边缘见[single边缘](replay/single/histogram-marginals.json)、[families边缘](replay/families/histogram-marginals.json)；全部行名/有理slack见[single全行](replay/single/all-row-slacks.json)、[families全行](replay/families/all-row-slacks.json)；原字段、K、各kind正列、全部新Y七价见[single摘要](replay/single/summary.json)、[families摘要](replay/families/summary.json)。原向量所有列仍由各primary JSON完整保留。

真正成功事件是[single执行](replay/single.execution.json)及[families执行](replay/families.execution.json)，exit0、stderr空，分别33.439秒和34.259秒。它们各调用一次原row builder，无原main/verify入口、float LP或SPE求解。最初两份clone内输出尝试因目录被同步暂收起而无法保存；随后两次外部构建停在Python tuple/list的过严身份比较。所有失败另保[尝试总账](replay/attempt-ledger.json)、[未收集输出说明](replay/failed-output-capture.json)与`replay/failed-type-comparison/`原日志/当时核验器，不把失败改为PASS。最终核验器仅按原JSON writer规范化nested tuple为array，未改原源码、系数或任何坐标。

## 完整依赖路由与重现

本次从已有`combined-branch-master-program`复用47冻结文件，再按本批五原件覆盖到隔离原路径；[runtime-file-checks.json](runtime-file-checks.json)核52文件运行后原字节不变。这是可用文件检查，不是假装52文件全被动态加载的trace。相邻可选root_lines在本次runtime不存在，但coupled只调用不引用ROOT_LINES的branch_rows，base_rows/solve均未运行。

若要建立另一份独立执行事件，可在仓库根运行，目的路径必须尚不存在：

```sh
python3 archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/materialize_runtime.py /absolute/new-coupled-runtime
python3 -B archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/verify_fixed_point.py /absolute/new-coupled-runtime single /absolute/new-single-output
python3 -B archives/customer-attraction/tools/evidence/coupled-b-fixed-points-boss3/verify_fixed_point.py /absolute/new-coupled-runtime families /absolute/new-families-output
```

材料化程序只核SHA并复制原字节，根`work.py`只有定位注释、从未执行，不需要凭据。运行需[environment.json](environment.json)所记Python/NumPy/SciPy，assert必须启用。复现不是自动授权扩大支持、调价、重优或把代码main覆盖到原件目录。

## 数学身份与比较

[comparison-manifest.json](comparison-manifest.json)区分本批实际全文读过的18份相关正文/源码/原JSON，与仅按已有清单保全的其它执行依赖；旁读不额外claim/done。关联A的5664→5692验证与C的7客户参数反例分别归属其正式对象，不冒成本批额外运行。[relation-review.json](relation-review.json)解释来源、实现、有限检查、点补全反驳、共同K与投影包含；阶段三图未改。

默认真实行只在被强制者早于最后两名真优化者时按M/Z证明使用。max_branch_lp接受的更广Python参数没有自动补前提；六人根线也不能移到其它n。两个W<1/2都是固定16旧hist的有限必要系统点，非精确最优、共同客户全隐藏实现、完整SPE或真实half反例。五份逐源receipt由Boss3在本包checkpoint pushed之后串行登记。

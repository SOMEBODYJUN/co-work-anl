---
id: "weighted-congestion/curvature-step-exact-finite-audits"
kind: "computation"
type_tag: "计算"
title: "曲率与阶跃DAG的精确有限核验"
status: "reproduced"
summary: "保留8份不改字节的原精确审计、6份冻结记录、完整实际复跑及逐字段差异；全部复跑成功且冻结记录完全一致。"
review_status: "source and input inspected; actual rerun; finite evidence only"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/polynomial_curvature/verify.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/polynomial_curvature/extension_verify.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/polynomial_curvature/verify_dag_low_leakage.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/polynomial_curvature/independent_dag_low_leakage.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/step_dag/verify.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/step_dag/independent_audit.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/step_dag/verify_polynomial_extremal_all_in.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/weighted_congestion/step_dag/independent_polynomial_all_in.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/polynomial_curvature/results.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/polynomial_curvature/dag_low_leakage.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/polynomial_curvature/dag_low_leakage_independent.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/step_dag/verification.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/step_dag/polynomial_extremal_all_in.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/weighted_congestion/step_dag/polynomial_extremal_all_in_independent.json"
---

# 曲率与阶跃DAG的精确有限核验

这是有限精确计算资源对象，不是一般数学定理。数学证明分别见
[三点包络](../定理/非负多项式三载荷精确包络--定理.md)、[前缀过冲](../障碍/前缀阶跃平台的三载荷过冲--障碍.md)、[阶跃路径门槛](../定理/阶跃依赖DAG的路径精确门槛--定理.md)、[端点预算](../定理/有向无环端点低泄漏的精确次数预算--定理.md)与[极值幅度全入均衡](../定理/阶跃极值幅度的多项式全入均衡--定理.md)。
所有下述计数保留自己的输入域，不能把多个不同程序的案例相加成更强一般结论。

## 原件、运行合同与实际结果

证据根为 [`tools/evidence/curvature-step`](../../tools/evidence/curvature-step/)。
其中 [source-manifest.json](../../tools/evidence/curvature-step/source-manifest.json)保存23源的精确commit/path、blob和SHA256；本轮读取每份原始字节并验证SHA256与清单一致。
`original/tests/audits/weighted_congestion/`下是8份原程序，`original/evidence/runs/weighted_congestion/`下是6份冻结JSON，均不改字节。
不用旧统一replay入口或未保存的环境依赖；原程序只需Python标准库。

从任意目录运行保存的 [replay.py](../../tools/evidence/curvature-step/replay.py)：

```sh
python3 archives/weighted-congestion/tools/evidence/curvature-step/replay.py
```

该命令从仓库根执行；若当前不是仓库根，改用replay.py绝对路径即可。
它通过自身路径定位原件，以最多4个子进程运行全部8份程序。
两份作者程序原main会写同目录结果，包装器改为`runpy.run_path(...)["run"]()`后序列化返回值，避免覆盖原件；数学函数和源码字节未改。
其余程序直接运行默认stdout合同。
结果完整保存到`rerun/*.stdout.json`、`*.stderr.txt`和[replay-summary.json](../../tools/evidence/curvature-step/rerun/replay-summary.json)。
差异函数递归比较6份冻结JSON的全部字典、列表与标量，另两份没有清单内独立冻结JSON，保留实际输出而不伪称有逐文件冻结比较。

本轮在Python3.12.14全部8项退出码0，所有stderr为空；6份冻结记录的差异数组全部为空，连Python版本字段也相同。
独立全入的1533737字节记录被完整解析，逐案例核查权、图边、h、系数、两个策略、全入位串、缺口矩、所有偏离before/after/bound字段；复跑后210案例及1470偏离的每个实际标量均与冻结记录相同。
没有手工逐个重算其中所有大分数；其复核强度是完整结构阅读、生成算法实读及重新精确生成逐字段相等。
有限审计没有枚举任意实输入或巨大一般游戏的全部状态。

## 八份程序的语义与覆盖

| 程序标签 | 实际输入、核验机制 | 本轮真实输出 |
|---|---|---|
| curvature | literal前缀资源集合构造；整数/Fraction检查几何、三负载、次数界 | 38几何、114载荷、728非零`{0,1,2}^6`向量；4368个多项式不等式及4368个次数界；9常数/零值检查 |
| envelope | 固定`r=11/12,s=5/4`；n=0..5、theta∈{0,1/4,1/2,3/4,1}；枚举`{0,1,2}^5`归一化权 | 78仿射网格小于式、30极小多项式、2335可行多项式比较；m=2粗指数反例精确成立 |
| leakage-author | 1..5顶点全部forward-labelled DAG；z∈{101/100,11/10,3/2,2}；d∈{1,2,5,20}；反拓扑权递推、slack传播 | 1099图、4396 graph-z、17584次数端点、13188 slack、29490多项式、26376 q比较、3严格边界、4二次数域端点 |
| leakage-independent | 实际DFS枚举路径；不同z网格增加21/20、5/4，d∈{1,2,5}；64次Fraction夹逼q | 1099图、19782单项式次数案例；2225可行graph-z；2206有边严格q上界；1424非负多项式；8个Q(phi)等号端点 |
| step-author | 0..4顶点全部forward DAG，加5/7/9点空图、链、完整图；逐资源真实费用及全部偏离 | 76枚举小图；12824平衡状态、81256偏离、380 greedy状态；较大样本不计入graphs字段 |
| step-independent | 整数缩放dyadic负载；独立resource coefficient masks；小图全振幅+固定种子200207466较大随机图 | 103图、5918实际载荷状态、2954振幅实例、105050振幅状态；515平衡实例、154树、3精确整数端点、2拒绝等号fixture |
| all-in-author | 搜索1099小图筛integer q；加q=3/4/5空图；d∈{1,2,5,10,20}；dyadic/均匀权与单项式/常数/混合费用 | 59选中图、2715真实游戏、17490实际偏离；缺口矩、真实费用、Jensen链、列交换均检查 |
| all-in-independent | 5组明确图权；q=2/3/4、d∈{0,1,2,4,16,32}；7费用形状，seed=524170；不导入作者代码 | 210完整游戏、1470实际偏离；包含接近总权1与多个incoming的图；每项输入及费用记录完整 |

`forward-labelled DAG`指按某个拓扑顺序编号后枚举所有可能前向弧子集，并非无标号图各一次。
低泄漏独立程序的有理预算恰等号计数为0，不代表弱端点不存在；它另用8次精确Q(phi)测试该边界。
全入独立degree0是费用常数的额外边界核验，不扩大主定理的$d\ge1$严格Jensen结论。
两份含固定随机种子的程序仍是确定的有限输入，不能升级概率保证或任意参数证明。

## 实现差别和防止误读

作者和独立step审计的动作位编码不同：作者轻玩家位1使自身资源与根同列，独立程序位0使之同列。二者各自reduced公式与literal策略一致，是动作名互换，不是模型冲突。
低泄漏作者用起点路径动态规划，独立代码用DFS，正文的幅度递推则用终点路径；路径总数相同但权重递推方向不得互换。
全入作者检验路径数缺口矩，独立代码检验双重和缺口矩；都重建真实玩家策略，并未直接假定阶跃简化费用在多项式中成立。
本轮未发现数值或记录差异，不据此声称新颖性、外审通过、一般博弈均衡或全状态无均衡。

## 与审查及后续来源的关系

审查报告中给出的独立性过程是历史来源声明，清洗者没有把复跑包装成新的盲审。
本轮内部子代理另完整清洗原曲率review，见[独立审查对象](../审查/三载荷包络的独立审查范围--审查.md)。其新375个graph-r有限化简表检查保存于`independent-cleanup/`，含75图、5490个固定根列light状态、27020个比及750个全入/全出因子检查；它没有literal资源负载，作为本轮额外内部旁证，不冒充历史冻结源，也不计入上表8份原审计。其量词核对还修正了有理振幅不使任意原实权自动有理的措辞。
原证明的数学内容、审查的额外论证以及旧OPEN与较后线性下界的区别见[审查范围](../审查/曲率与阶跃结论的审查范围--审查.md)。

# R-18 counterexample-search 五源比较记录

## 来源与精确统计

| ID | 文件 | 大小 / SHA-256 | 处置 | 核心结果 |
|---|---|---:|---|---|
| `1938b7a2ae2dbbc7882d` | projection_m5p15_best.json | 6,588,793 B / `77ce18781c299fe55b0b718803c78ff7474362d26272307ddbc8889639946bf6` | retained | 46 类型、15 主题、5 人；54241 histories、759374 deviations；exact OPT/W≈1.35035 |
| `7cec56f8cc250e8eec92` | projection_m5p15_run.json | 4108 B / `6784bb680722b298adb781282e9ff5a53378c0dee7c0030d009d54d696b70dd2` | retained | 4 steps/8 portfolio records；types 52–54、DAG 3876、rows 41532–43989；best≈1.35035 |
| `7a8e772e2723d5707669` | projection_symmetric_m5p15_best.json | 6,596,755 B / `62cfe417d7d5803336fc633975d671b4fb52453598b1467b1ede735d508f80c5` | retained | 155 类型、15 主题、5 人；54241/759374；W=OPT、ratio=1 |
| `ad317e98c20865e766fe` | projection_symmetric_m5p15_run.json | 1218 B / `b17c2fd1a519032c80c2b54996a1aeac4850803bd47199ed42b14d215d211181` | retained | symmetric run 两 records；types155、DAG10154、rows109656；best=1 |
| `83b29244c281cae6b652` | symmetric_projection_audit.py | 2876 B / `765332d082cc21070889df50426f69e23d87d8bf29165ffedf9f5582b13fbaec` | integrated | Fraction/ExactSPESolver audit：ABCD feasible，ABC 不可行，9 个严格 profitable deviations |

## 非对称投影候选

大 JSON 的 exact ratio 为

\[
\frac{48363883710042491181514168}{35815737353498434201706253}
\approx1.3503528695415332,
\]

实例重算 W=71631474706996868403412506、OPT=96727767420084982363028336。它低于 2，因此不是 `2W<OPT` 反例。运行摘要明确 limitation 是 finite sparse-support/randomly aligned projections，replies not preserved；完整策略验证字段只认证该保存实例，不认证 indexed relaxation 的一般迁移。

## 对称投影与 exact prefix obstruction

对称 best JSON 的 155 类型端点 W=OPT，ratio=1。它本身没有福利 gap，但 `symmetric_projection_audit.py` 进一步固定 desired ABCDE path，构造实际 15-topic instance，以 ExactSPESolver 从最深 prefix 向上检查：

- prefix ABCD：desired continuation SPE feasible，actual=threshold，11 outcomes；
- prefix ABC：desired continuation SPE infeasible，actual payoff−threshold = `-4262528025340808635153148385102788890849920`；
- V、W、X、Y、T1–T5 九个 deviation 在每个 SPE reply 下都有正 gain。

这是指定 projection/path 的 exact obstruction，不能排除其他 root path 或一般实例。它与非对称 ratio=1.35 候选一起说明：投影得到的福利 gap 目标和完整均衡实现义务是两个独立门槛。

## 与既有对象去重

- `R18五人十五主题投影有限候选--计算` 已保存同一非对称 m5p15 一步 exact candidate；本批大 JSON 增量是完整 instance/strategy 字节、54241/759374 verification counts 及对称分支。
- 五人 indexed bound / harmonic obstruction 是 projection 的输入依赖，不是本批新证明；symmetric audit 只把固定 desired path 的不可实现性在实际 catalog 上 exact 化。
- 现有 full-tree MILP/credible cone 对象区分 fixed cone exact certificate 与 universal quantifier；本批沿用这一边界，没有把 exact candidate ratio 或 prefix obstruction 升格为全目录反例。
- R-18 gap-floor/sparse probes 与本批不同：前者比较 `(OPT-W)/min_pay` 门槛，本批直接计算固定策略 candidate `OPT/W` 与 designated-path SPE feasibility。

## 结论边界

五源只支持：

1. 一次非对称 15-topic projection 的 exact candidate，ratio≈1.35035<2；
2. 对称 15-topic projection 的 exact non-gap endpoint，ratio=1；
3. 对称 desired ABCDE path 在 prefix ABC 的 exact SPE obstruction；
4. 有限 run 的 types/DAG/rows/portfolio 统计及 limitation。

它们没有证明一般 projection 不可能性、Q-CAG-HALF 反例、所有 15-topic 实例的 gap、算法/hardness 或 unrelated-machines 结论。

# 直接共居SAT编译的三半锐界：冻结陈述

ID: UM-DIRECT-COHABITING-SAT-COMPILER-SHARP-THREE-HALVES-v1。
对象是weighted_direct_cohabiting_query_return_all_formula_failure_exact_v1.md所明示完整普通P，但固定全部真实x_i=y_i=1/2、dummy x1，3/4<rho<1。源为有限CNF每clause至少2occ、重复允许、每变量显式padding环长至少3。空公式返回一idle机零job。矩阵：q_i仅Mi:rho/Mi+:1/Ci:x_i；b_i仅pin(i):rho/Ci:1；u_c仅真实i属于c的Ci:1/2；其余∞。所有原jobs须执行。

Exact：所有非空域内公式，SAT则真实OPT=1，UNSAT则真实OPT=3/2；任意完整峰<3/2调度可detbitpoly解码SAT。空Φ单列OPT0。要求给全部原jobs调度与任意完整调度lower，不把strict1NP-hardness或固定3/2锐界冒充near2目标反证。

固定rho4/5和Φ=(x∨x)∧(¬x∨¬x)、occ顺序正正负负，无dummy，是8machine10job、24finite条目的明确sharp UNSAT例。代码或穷举仅为有限checks，不能代一般证明。

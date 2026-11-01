# 冻结指派24实际JSON输入的全字段阅读视图
纯JSON结构变换；未计算收益/IC/最优或运行原程序。动作向量按最后历史标签0..k−1索引，可恢复每个完整有序键；原字段和非策略数据完整保留。

## fractional_actual_load_failure
example路径 examples/customer_attraction/fractional_actual_load_failure.json
example完整JSON={"topics":["A","B","Q","D"],"customers":[{"topics":[0],"multiplicity":3},{"topics":[2],"multiplicity":1},{"topics":[0,3],"multiplicity":1},{"topics":[1,2,3],"multiplicity":12}],"players":4}
certificate路径 evidence/certificates/customer_attraction/fractional_actual_load_failure.json
strategy其余字段={"terminal_counts":[1,3,0,0]}
root动作=1
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [2, 1, 2, 2]
depth 2
prefix=(0,) -> [2, 2, 2, 2]
prefix=(1,) -> [2, 1, 2, 2]
prefix=(2,) -> [2, 3, 3, 2]
prefix=(3,) -> [2, 2, 2, 2]
depth 3
prefix=(0, 0) -> [2, 2, 2, 2]
prefix=(0, 1) -> [2, 2, 3, 2]
prefix=(0, 2) -> [2, 3, 3, 2]
prefix=(0, 3) -> [2, 2, 2, 2]
prefix=(1, 0) -> [2, 2, 3, 2]
prefix=(1, 1) -> [2, 0, 3, 2]
prefix=(1, 2) -> [3, 3, 3, 3]
prefix=(1, 3) -> [2, 2, 3, 2]
prefix=(2, 0) -> [2, 3, 3, 2]
prefix=(2, 1) -> [3, 3, 3, 3]
prefix=(2, 2) -> [3, 3, 3, 3]
prefix=(2, 3) -> [2, 3, 3, 2]
prefix=(3, 0) -> [2, 2, 2, 2]
prefix=(3, 1) -> [2, 2, 3, 2]
prefix=(3, 2) -> [2, 3, 3, 2]
prefix=(3, 3) -> [2, 2, 2, 2]

## worst_cce_welfare_failure
example路径 examples/customer_attraction/worst_cce_welfare_failure.json
example完整JSON={"topics":["0","1","2","3","4"],"customers":[{"topics":[1],"multiplicity":2},{"topics":[2],"multiplicity":1},{"topics":[3],"multiplicity":1},{"topics":[0,1,2,3],"multiplicity":2},{"topics":[4],"multiplicity":4},{"topics":[0,2,3,4],"multiplicity":3}],"players":3}
certificate路径 evidence/certificates/customer_attraction/worst_cce_welfare_failure.json
strategy其余字段={"claim_id":"CA-WORST-CCE-WELFARE-NO","scope":"Complete full-history pure SPE and static CCE primal/dual finite certificate; not a half-coverage counterexample.","terminal_counts":[1,0,0,0,2],"terminal_path":[0,4,4],"terminal_payoffs":["3","3","3"],"terminal_welfare":9,"opt":12,"simple_cce_dual":{"lambda":["0","1/5","1/5","1/5","2/5"],"lower":"137/15"},"optimal_cce_dual":{"lambda":["0","38/99","1/11","1/11","28/99"],"lower":"2785/297"},"optimal_cce_primal":{"interpretation":"For each profile uniformly randomize over its distinct ordered permutations.","count_support":[{"profile":[0,0,4],"probability":"67/1188"},{"profile":[0,1,4],"probability":"20/297"},{"profile":[0,4,4],"probability":"251/396"},{"profile":[2,2,4],"probability":"4/33"},{"profile":[3,3,4],"probability":"4/33"}]},"static_security_cap":{"background":[0,4],"query_values":["2","3","3","3","3"]}}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [4, 4, 4, 4, 0]
depth 2
prefix=(0,) -> [4, 4, 4, 4, 4]
prefix=(1,) -> [4, 4, 4, 4, 2]
prefix=(2,) -> [4, 4, 4, 4, 3]
prefix=(3,) -> [4, 4, 4, 4, 2]
prefix=(4,) -> [4, 2, 3, 2, 2]

## portfolio_matching_failure
example路径 examples/customer_attraction/portfolio_matching_failure.json
example完整JSON={"topics":["A","B","T","D","E"],"customers":[{"topics":[0],"multiplicity":15},{"topics":[1],"multiplicity":15},{"topics":[0,2],"multiplicity":6},{"topics":[1,2],"multiplicity":5},{"topics":[0,1,2],"multiplicity":1},{"topics":[3],"multiplicity":16},{"topics":[2,3],"multiplicity":6},{"topics":[4],"multiplicity":14},{"topics":[2,4],"multiplicity":6},{"topics":[1,2,4],"multiplicity":2}],"players":2}
certificate路径 evidence/certificates/customer_attraction/portfolio_matching_failure.json
strategy其余字段={"terminal_counts":[1,0,0,0,1]}
root动作=4
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [1, 2, 1, 2, 0]

## prefix_balance_failure
example路径 examples/customer_attraction/prefix_balance_failure.json
example完整JSON={"topics":["L0","A","B","L1","L2","L3"],"customers":[{"topics":[0],"multiplicity":2},{"topics":[0,1],"multiplicity":1},{"topics":[0,2],"multiplicity":2},{"topics":[3],"multiplicity":2},{"topics":[1,3],"multiplicity":1},{"topics":[2,3],"multiplicity":2},{"topics":[4],"multiplicity":2},{"topics":[1,4],"multiplicity":1},{"topics":[2,4],"multiplicity":2},{"topics":[5],"multiplicity":2},{"topics":[2,5],"multiplicity":2},{"topics":[1,2,5],"multiplicity":3}],"players":4}
certificate路径 evidence/certificates/customer_attraction/prefix_balance_failure.json
strategy其余字段={"terminal_counts":[0,1,3,0,0,0]}
root动作=1
动作原数组次序=[[],[0],[0,0],[0,0,0],[0,0,1],[0,0,2],[0,0,3],[0,0,4],[0,0,5],[0,1],[0,1,0],[0,1,1],[0,1,2],[0,1,3],[0,1,4],[0,1,5],[0,2],[0,2,0],[0,2,1],[0,2,2],[0,2,3],[0,2,4],[0,2,5],[0,3],[0,3,0],[0,3,1],[0,3,2],[0,3,3],[0,3,4],[0,3,5],[0,4],[0,4,0],[0,4,1],[0,4,2],[0,4,3],[0,4,4],[0,4,5],[0,5],[0,5,0],[0,5,1],[0,5,2],[0,5,3],[0,5,4],[0,5,5],[1],[1,0],[1,0,0],[1,0,1],[1,0,2],[1,0,3],[1,0,4],[1,0,5],[1,1],[1,1,0],[1,1,1],[1,1,2],[1,1,3],[1,1,4],[1,1,5],[1,2],[1,2,0],[1,2,1],[1,2,2],[1,2,3],[1,2,4],[1,2,5],[1,3],[1,3,0],[1,3,1],[1,3,2],[1,3,3],[1,3,4],[1,3,5],[1,4],[1,4,0],[1,4,1],[1,4,2],[1,4,3],[1,4,4],[1,4,5],[1,5],[1,5,0],[1,5,1],[1,5,2],[1,5,3],[1,5,4],[1,5,5],[2],[2,0],[2,0,0],[2,0,1],[2,0,2],[2,0,3],[2,0,4],[2,0,5],[2,1],[2,1,0],[2,1,1],[2,1,2],[2,1,3],[2,1,4],[2,1,5],[2,2],[2,2,0],[2,2,1],[2,2,2],[2,2,3],[2,2,4],[2,2,5],[2,3],[2,3,0],[2,3,1],[2,3,2],[2,3,3],[2,3,4],[2,3,5],[2,4],[2,4,0],[2,4,1],[2,4,2],[2,4,3],[2,4,4],[2,4,5],[2,5],[2,5,0],[2,5,1],[2,5,2],[2,5,3],[2,5,4],[2,5,5],[3],[3,0],[3,0,0],[3,0,1],[3,0,2],[3,0,3],[3,0,4],[3,0,5],[3,1],[3,1,0],[3,1,1],[3,1,2],[3,1,3],[3,1,4],[3,1,5],[3,2],[3,2,0],[3,2,1],[3,2,2],[3,2,3],[3,2,4],[3,2,5],[3,3],[3,3,0],[3,3,1],[3,3,2],[3,3,3],[3,3,4],[3,3,5],[3,4],[3,4,0],[3,4,1],[3,4,2],[3,4,3],[3,4,4],[3,4,5],[3,5],[3,5,0],[3,5,1],[3,5,2],[3,5,3],[3,5,4],[3,5,5],[4],[4,0],[4,0,0],[4,0,1],[4,0,2],[4,0,3],[4,0,4],[4,0,5],[4,1],[4,1,0],[4,1,1],[4,1,2],[4,1,3],[4,1,4],[4,1,5],[4,2],[4,2,0],[4,2,1],[4,2,2],[4,2,3],[4,2,4],[4,2,5],[4,3],[4,3,0],[4,3,1],[4,3,2],[4,3,3],[4,3,4],[4,3,5],[4,4],[4,4,0],[4,4,1],[4,4,2],[4,4,3],[4,4,4],[4,4,5],[4,5],[4,5,0],[4,5,1],[4,5,2],[4,5,3],[4,5,4],[4,5,5],[5],[5,0],[5,0,0],[5,0,1],[5,0,2],[5,0,3],[5,0,4],[5,0,5],[5,1],[5,1,0],[5,1,1],[5,1,2],[5,1,3],[5,1,4],[5,1,5],[5,2],[5,2,0],[5,2,1],[5,2,2],[5,2,3],[5,2,4],[5,2,5],[5,3],[5,3,0],[5,3,1],[5,3,2],[5,3,3],[5,3,4],[5,3,5],[5,4],[5,4,0],[5,4,1],[5,4,2],[5,4,3],[5,4,4],[5,4,5],[5,5],[5,5,0],[5,5,1],[5,5,2],[5,5,3],[5,5,4],[5,5,5]]
depth 1
prefix=() -> [2, 2, 1, 2, 2, 2]
depth 2
prefix=(0,) -> [2, 2, 2, 2, 2, 2]
prefix=(1,) -> [2, 2, 2, 2, 2, 2]
prefix=(2,) -> [2, 2, 1, 2, 2, 2]
prefix=(3,) -> [2, 2, 2, 2, 2, 2]
prefix=(4,) -> [2, 2, 2, 2, 2, 2]
prefix=(5,) -> [2, 2, 2, 2, 2, 2]
depth 3
prefix=(0, 0) -> [2, 2, 2, 2, 2, 2]
prefix=(0, 1) -> [2, 2, 2, 2, 2, 2]
prefix=(0, 2) -> [2, 2, 3, 2, 2, 2]
prefix=(0, 3) -> [2, 2, 2, 2, 2, 2]
prefix=(0, 4) -> [2, 2, 2, 2, 2, 2]
prefix=(0, 5) -> [2, 2, 2, 2, 2, 2]
prefix=(1, 0) -> [2, 2, 2, 2, 2, 2]
prefix=(1, 1) -> [2, 2, 2, 2, 2, 2]
prefix=(1, 2) -> [2, 2, 2, 2, 2, 2]
prefix=(1, 3) -> [2, 2, 2, 2, 2, 2]
prefix=(1, 4) -> [2, 2, 2, 2, 2, 2]
prefix=(1, 5) -> [2, 2, 2, 2, 2, 2]
prefix=(2, 0) -> [2, 2, 3, 2, 2, 2]
prefix=(2, 1) -> [2, 2, 2, 2, 2, 2]
prefix=(2, 2) -> [3, 2, 1, 0, 0, 1]
prefix=(2, 3) -> [2, 2, 0, 2, 2, 2]
prefix=(2, 4) -> [2, 2, 0, 2, 2, 2]
prefix=(2, 5) -> [2, 2, 1, 2, 2, 2]
prefix=(3, 0) -> [2, 2, 2, 2, 2, 2]
prefix=(3, 1) -> [2, 2, 2, 2, 2, 2]
prefix=(3, 2) -> [2, 2, 0, 2, 2, 2]
prefix=(3, 3) -> [2, 2, 2, 2, 2, 2]
prefix=(3, 4) -> [2, 2, 2, 2, 2, 2]
prefix=(3, 5) -> [2, 2, 2, 2, 2, 2]
prefix=(4, 0) -> [2, 2, 2, 2, 2, 2]
prefix=(4, 1) -> [2, 2, 2, 2, 2, 2]
prefix=(4, 2) -> [2, 2, 0, 2, 2, 2]
prefix=(4, 3) -> [2, 2, 2, 2, 2, 2]
prefix=(4, 4) -> [2, 2, 2, 2, 2, 2]
prefix=(4, 5) -> [2, 2, 2, 2, 2, 2]
prefix=(5, 0) -> [2, 2, 2, 2, 2, 2]
prefix=(5, 1) -> [2, 2, 2, 2, 2, 2]
prefix=(5, 2) -> [2, 2, 1, 2, 2, 2]
prefix=(5, 3) -> [2, 2, 2, 2, 2, 2]
prefix=(5, 4) -> [2, 2, 2, 2, 2, 2]
prefix=(5, 5) -> [2, 2, 2, 2, 2, 2]

## coverage_opportunity_failure
example路径 examples/customer_attraction/coverage_opportunity_failure.json
example完整JSON={"topics":["A","B","T","D","E"],"players":3,"customers":[{"topics":[0],"multiplicity":2},{"topics":[1],"multiplicity":2},{"topics":[2],"multiplicity":1},{"topics":[2,3],"multiplicity":1},{"topics":[2,4],"multiplicity":1},{"topics":[0,3,4],"multiplicity":3},{"topics":[1,3,4],"multiplicity":1}]}
certificate路径 evidence/certificates/customer_attraction/coverage_opportunity_failure.json
strategy其余字段={"terminal_counts":[2,1,0,0,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [0, 0, 0, 0, 0]
depth 2
prefix=(0,) -> [1, 3, 3, 4, 3]
prefix=(1,) -> [3, 0, 0, 0, 0]
prefix=(2,) -> [3, 0, 0, 0, 0]
prefix=(3,) -> [4, 0, 0, 0, 0]
prefix=(4,) -> [3, 0, 0, 0, 0]

## collision_free_occupancy
example路径 examples/customer_attraction/collision_free_occupancy.json
example完整JSON={"topics":["A","B","C","D"],"customers":[{"topics":[0],"multiplicity":1},{"topics":[0,1,2],"multiplicity":2},{"topics":[1,3],"multiplicity":1},{"topics":[3],"multiplicity":1}],"players":2}
certificate路径 evidence/certificates/customer_attraction/collision_free_occupancy.json
strategy其余字段={"terminal_counts":[0,0,1,1]}
root动作=2
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [1, 0, 3, 0]

## eight_cce_welfare_gap
example路径 examples/customer_attraction/eight_cce_welfare_gap.json
example完整JSON={"topics":["T0","T1","T2","T3"],"customers":[{"topics":[0,2,3],"multiplicity":2},{"topics":[1],"multiplicity":4},{"topics":[2],"multiplicity":1},{"topics":[3],"multiplicity":1}],"players":3}
certificate路径 evidence/certificates/customer_attraction/eight_cce_welfare_gap.json
strategy其余字段={"terminal_counts":[1,2,0,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [1, 1, 1, 1]
depth 2
prefix=(0,) -> [1, 1, 1, 1]
prefix=(1,) -> [1, 2, 3, 2]
prefix=(2,) -> [1, 3, 1, 1]
prefix=(3,) -> [1, 2, 1, 1]

## worst_pne_welfare_failure
example路径 examples/customer_attraction/worst_pne_welfare_failure.json
example完整JSON={"topics":["0","1","2","3"],"customers":[{"topics":[1],"multiplicity":1},{"topics":[0,1],"multiplicity":2},{"topics":[0,1,2],"multiplicity":2},{"topics":[1,3],"multiplicity":3},{"topics":[2,3],"multiplicity":3},{"topics":[0,2,3],"multiplicity":5}],"players":3}
certificate路径 evidence/certificates/customer_attraction/worst_pne_welfare_failure.json
strategy其余字段={"terminal_counts":[1,0,0,2]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [3, 2, 1, 0]
depth 2
prefix=(0,) -> [3, 3, 3, 3]
prefix=(1,) -> [3, 3, 3, 3]
prefix=(2,) -> [3, 3, 1, 1]
prefix=(3,) -> [3, 2, 1, 1]

## residual_counterexample
example路径 examples/customer_attraction/residual_counterexample.json
example完整JSON={"topics":["A","B","T","D","E"],"players":2,"customers":[{"topics":[1],"multiplicity":3},{"topics":[2],"multiplicity":3},{"topics":[0,3],"multiplicity":2},{"topics":[0,4],"multiplicity":2},{"topics":[1,3,4],"multiplicity":2},{"topics":[2,3,4],"multiplicity":2}]}
certificate路径 evidence/certificates/customer_attraction/residual_counterexample.json
strategy其余字段={"terminal_counts":[1,1,0,0,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [1, 3, 3, 4, 3]

## aggregate_theta_failure
example路径 examples/customer_attraction/aggregate_theta_failure.json
example完整JSON={"topics":["X0","X1","X2","Y0","Y1","Y2"],"customers":[{"topics":[0,3],"multiplicity":1},{"topics":[0,4],"multiplicity":1},{"topics":[0,5],"multiplicity":1},{"topics":[1,3],"multiplicity":1},{"topics":[1,4],"multiplicity":1},{"topics":[1,5],"multiplicity":1},{"topics":[2,3],"multiplicity":1},{"topics":[2,4],"multiplicity":1},{"topics":[2,5],"multiplicity":1},{"topics":[0,1,3,4],"multiplicity":3},{"topics":[0,1,3,5],"multiplicity":3},{"topics":[0,1,4,5],"multiplicity":3},{"topics":[0,2,3,4],"multiplicity":3},{"topics":[0,2,3,5],"multiplicity":3},{"topics":[0,2,4,5],"multiplicity":3},{"topics":[1,2,3,4],"multiplicity":3},{"topics":[1,2,3,5],"multiplicity":3},{"topics":[1,2,4,5],"multiplicity":3}],"players":3}
certificate路径 evidence/certificates/customer_attraction/aggregate_theta_failure.json
certificate其余顶层={"claim":"CA-AGGREGATE-LAST-FLOOR-NO","scope":"complete pure SPE counterexample to W >= n theta_n; not to half coverage","root_history":[0,3,4],"root_payoffs":["10","12","12"],"welfare":34,"optimum":36,"theta":"12"}
strategy其余字段={"terminal_counts":[1,0,0,1,1,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [3, 3, 3, 0, 0, 0]
depth 2
prefix=(0,) -> [1, 2, 1, 4, 3, 3]
prefix=(1,) -> [2, 0, 0, 4, 3, 3]
prefix=(2,) -> [1, 0, 0, 4, 3, 3]
prefix=(3,) -> [1, 0, 0, 4, 5, 4]
prefix=(4,) -> [1, 0, 0, 5, 3, 3]
prefix=(5,) -> [1, 0, 0, 4, 3, 3]

## individual_security_failure
example路径 examples/customer_attraction/individual_security_failure.json
example完整JSON={"players":3,"topics":["X0","X1","X2","Y0","Y1","Y2"],"customers":[{"topics":[2],"multiplicity":1},{"topics":[0,1,3,4],"multiplicity":4},{"topics":[0,2,3,4],"multiplicity":3},{"topics":[1,2,3,4],"multiplicity":3},{"topics":[0,1,2,3,4],"multiplicity":2},{"topics":[5],"multiplicity":1},{"topics":[0,1,3,5],"multiplicity":3},{"topics":[0,2,3,5],"multiplicity":3},{"topics":[1,2,3,5],"multiplicity":3},{"topics":[0,1,4,5],"multiplicity":3},{"topics":[0,2,4,5],"multiplicity":3},{"topics":[1,2,4,5],"multiplicity":3},{"topics":[0,1,3,4,5],"multiplicity":2}]}
certificate路径 evidence/certificates/customer_attraction/individual_security_failure.json
certificate其余顶层={"security":{"primary":["5/41","5/41","21/82","5/41","5/41","21/82"],"dual":[{"rivals":[0,1],"probability":"23/82"},{"rivals":[0,2],"probability":"9/82"},{"rivals":[1,2],"probability":"9/82"},{"rivals":[3,4],"probability":"23/82"},{"rivals":[3,5],"probability":"9/82"},{"rivals":[4,5],"probability":"9/82"}],"value":"2411/246"},"scope":"Full-history individual mixed-security failure; not an aggregate BR or half-coverage counterexample."}
strategy其余字段={"terminal_counts":[1,0,0,1,1,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [3, 3, 3, 0, 0, 0]
depth 2
prefix=(0,) -> [1, 2, 1, 4, 3, 3]
prefix=(1,) -> [2, 0, 0, 4, 3, 3]
prefix=(2,) -> [1, 0, 0, 4, 3, 3]
prefix=(3,) -> [1, 0, 0, 4, 5, 4]
prefix=(4,) -> [1, 0, 0, 5, 3, 3]
prefix=(5,) -> [1, 0, 0, 4, 3, 3]

## high_insertion_2cycle_348_exact
原路径 research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json
instance={"topics":["X0","X1","X2","Y0","Y1","Y2"],"customers":[{"topics":[1],"multiplicity":42},{"topics":[2],"multiplicity":38},{"topics":[0,3],"multiplicity":24},{"topics":[1,3],"multiplicity":12},{"topics":[2,3],"multiplicity":16},{"topics":[0,2,3],"multiplicity":3},{"topics":[4],"multiplicity":42},{"topics":[0,4],"multiplicity":12},{"topics":[0,1,4],"multiplicity":9},{"topics":[1,3,4],"multiplicity":9},{"topics":[0,2,3,4],"multiplicity":24},{"topics":[5],"multiplicity":38},{"topics":[0,5],"multiplicity":16},{"topics":[0,3,5],"multiplicity":3},{"topics":[0,1,3,5],"multiplicity":24},{"topics":[0,2,3,5],"multiplicity":12},{"topics":[1,2,3,5],"multiplicity":12},{"topics":[0,2,4,5],"multiplicity":12}],"players":3}
其余packet字段={"kind":"HIGH-INSERTION-2-CYCLE-NOT-MENU-COUNTEREXAMPLE","forced_paths":[[0,3,4],[1,3,4],[2,3,4],[3,0,1],[4,0,1],[5,0,1]],"root_payoffs":["147/2","147/2","147/2","147/2","147/2","147/2"],"potential":["304","304","304","304","304","304"],"K":[["47","68","67","51","221/4","329/6"],["68","169/4","143/2","41","185/4","89/2"],["67","143/2","130/3","69","159/2","159/2"],["51","221/4","329/6","47","68","67"],["41","185/4","89/2","68","169/4","143/2"],["69","159/2","159/2","67","143/2","130/3"]],"cycle":[2,5],"cycle_entry":["159/2","159/2"],"root_u":"147/2","verification":{"valid":true,"histories":43,"deviations":215}}
strategy其余字段={"terminal_counts":[1,0,0,1,1,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [3, 3, 3, 0, 0, 0]
depth 2
prefix=(0,) -> [1, 2, 1, 4, 3, 3]
prefix=(1,) -> [2, 0, 0, 4, 3, 3]
prefix=(2,) -> [1, 0, 0, 4, 3, 3]
prefix=(3,) -> [1, 0, 0, 4, 5, 4]
prefix=(4,) -> [1, 0, 0, 5, 3, 3]
prefix=(5,) -> [1, 0, 0, 4, 3, 3]

## terminal_pushforward_34_D_lt_C_exact
原路径 research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json
instance={"topics":["X0","X1","X2","Y0","Y1","Y2","Empty"],"customers":[{"topics":[2],"multiplicity":1},{"topics":[0,1,3,4],"multiplicity":4},{"topics":[0,2,3,4],"multiplicity":3},{"topics":[1,2,3,4],"multiplicity":3},{"topics":[0,1,2,3,4],"multiplicity":2},{"topics":[5],"multiplicity":1},{"topics":[0,1,3,5],"multiplicity":3},{"topics":[0,2,3,5],"multiplicity":3},{"topics":[1,2,3,5],"multiplicity":3},{"topics":[0,1,4,5],"multiplicity":3},{"topics":[0,2,4,5],"multiplicity":3},{"topics":[1,2,4,5],"multiplicity":3},{"topics":[0,1,3,4,5],"multiplicity":2}],"players":3}
其余packet字段={"kind":"EXACT-D-LT-C-NOT-C-LT-U","source_instance":"examples/customer_attraction/individual_security_failure.json","query_probability":["0","0","1/10","0","0","0","9/10"],"forced_root_paths":[[0,3,4],[1,3,4],[2,3,4],[3,0,1],[4,0,1],[5,0,1],[6,0,1]],"forced_root_payoffs":["29/3","29/3","29/3","29/3","29/3","29/3","0"],"entry_X2_after_empty":"32/3","entry_X2_after_X2":"13/2","D":"29/30","C":"41/40","D_minus_C":"-7/120","u_minus_C":"1037/120","verification":{"valid":true,"histories":57,"deviations":342}}
strategy其余字段={"terminal_counts":[1,0,0,1,1,0,0]}
root动作=0
动作原数组次序=按深度及字典序
depth 1
prefix=() -> [3, 3, 3, 0, 0, 0, 0]
depth 2
prefix=(0,) -> [1, 2, 1, 4, 3, 3, 1]
prefix=(1,) -> [2, 0, 0, 4, 3, 3, 0]
prefix=(2,) -> [1, 0, 0, 4, 3, 3, 0]
prefix=(3,) -> [1, 0, 0, 4, 5, 4, 4]
prefix=(4,) -> [1, 0, 0, 5, 3, 3, 3]
prefix=(5,) -> [1, 0, 0, 4, 3, 3, 3]
prefix=(6,) -> [1, 0, 0, 4, 3, 3, 0]

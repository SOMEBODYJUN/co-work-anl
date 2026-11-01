# 原十三目标与37最优元组全部字段
按原JSON字段展示，不计算收益/匹配；原文件完整保留。

## fractional_actual_load_failure
{"name":"fractional_actual_load_failure","players":4,"topic_count":4,"unit_customers":17,"actual":[1,1,1,0],"actual_payoffs":["4","4","4","4"],"W":16,"OPT":17,"full_history_nodes":85,"SPE_comparisons_with_self":340,"compared_multisets":35,"optimal_multiset_count":10,"cost_identity_checks":110,"least_optimal_tuple_K":"10","greatest_optimal_tuple_K":"16","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/fractional_actual_load_failure.json":"fba8f2ed045b903d639d666e4b43333ac8e5671cce89d7c69d013c81ca587f72","evidence/certificates/customer_attraction/fractional_actual_load_failure.json":"34713413620599b34cecb1a2bb7b0adebc177cea5167ea3d995e30617fc7a0a3"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 0, 0, 2]|10|[0, 0, 0, 2]|49/4|4|True|
|[0, 0, 1, 2]|12|[0, 0, 1, 2]|27/2|12|True|
|[0, 0, 2, 2]|13|[0, 0, 2, 2]|29/2|6|True|
|[0, 0, 2, 3]|25/2|[0, 0, 3, 2]|113/8|12|True|
|[0, 1, 1, 2]|14|[0, 1, 1, 2]|59/4|12|True|
|[0, 1, 2, 2]|15|[0, 1, 2, 2]|63/4|12|True|
|[0, 1, 2, 3]|29/2|[0, 1, 3, 2]|123/8|24|True|
|[0, 2, 2, 2]|16|[0, 2, 2, 2]|67/4|4|True|
|[0, 2, 2, 3]|31/2|[0, 2, 3, 2]|131/8|12|True|
|[0, 2, 3, 3]|15|[0, 3, 3, 2]|16|12|True|

## worst_cce_welfare_failure
{"name":"worst_cce_welfare_failure","players":3,"topic_count":5,"unit_customers":13,"actual":[0,4,4],"actual_payoffs":["3","3","3"],"W":9,"OPT":12,"full_history_nodes":31,"SPE_comparisons_with_self":155,"compared_multisets":35,"optimal_multiset_count":2,"cost_identity_checks":12,"least_optimal_tuple_K":"25/3","greatest_optimal_tuple_K":"25/3","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/worst_cce_welfare_failure.json":"720df3be13bdf5a3fc0d27bf5cfa7c52ef1deb62b6d55341490b198cb81383b2","evidence/certificates/customer_attraction/worst_cce_welfare_failure.json":"210c5cfd6fb3ab8dc13fe76068e6f45132b09e94942bfb39e03aa33ef4bf9c04"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[1, 2, 4]|25/3|[4, 1, 2]|85/9|6|True|
|[1, 3, 4]|25/3|[4, 1, 3]|85/9|6|True|

## portfolio_matching_failure
{"name":"portfolio_matching_failure","players":2,"topic_count":5,"unit_customers":86,"actual":[4,0],"actual_payoffs":["22","22"],"W":44,"OPT":45,"full_history_nodes":6,"SPE_comparisons_with_self":30,"compared_multisets":15,"optimal_multiset_count":1,"cost_identity_checks":2,"least_optimal_tuple_K":"44","greatest_optimal_tuple_K":"44","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/portfolio_matching_failure.json":"58edce2c369b680adac39d604cf24db79699df2d3b106e2ba7dff8c09ba2cfeb","evidence/certificates/customer_attraction/portfolio_matching_failure.json":"b3cf75ce0764531e3ef751c01802c99cb1b4f5ce4a3f6943df241498e53299ae"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[1, 3]|44|[3, 1]|177/4|2|True|

## prefix_balance_failure
{"name":"prefix_balance_failure","players":4,"topic_count":6,"unit_customers":22,"actual":[1,2,2,2],"actual_payoffs":["15/4","41/12","41/12","41/12"],"W":14,"OPT":22,"full_history_nodes":259,"SPE_comparisons_with_self":1554,"compared_multisets":126,"optimal_multiset_count":1,"cost_identity_checks":24,"least_optimal_tuple_K":"51/4","greatest_optimal_tuple_K":"51/4","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/prefix_balance_failure.json":"d5ceea3f067337f3b1dcf764cd223baa9a1479085532b9b84b41a6351f71a47c","evidence/certificates/customer_attraction/prefix_balance_failure.json":"98ce95bea081809990012a2eef7e644100f3bbde9d20b1e2a409743c70f0c27e"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 3, 4, 5]|51/4|[5, 0, 3, 4]|105/8|24|True|

## coverage_opportunity_failure
{"name":"coverage_opportunity_failure","players":3,"topic_count":5,"unit_customers":11,"actual":[0,0,1],"actual_payoffs":["5/2","5/2","3"],"W":8,"OPT":11,"full_history_nodes":31,"SPE_comparisons_with_self":155,"compared_multisets":35,"optimal_multiset_count":1,"cost_identity_checks":6,"least_optimal_tuple_K":"37/6","greatest_optimal_tuple_K":"37/6","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/coverage_opportunity_failure.json":"27cfbde57d3e8d4d05f420c55f8851c94fd5e142d96ff09c0bacaf7de42e6e17","evidence/certificates/customer_attraction/coverage_opportunity_failure.json":"f714a87c6448b0ddcc070d325bd81bedd4ca7f4689893e344f77214fc1668256"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 1, 2]|37/6|[1, 2, 0]|65/9|6|True|

## collision_free_occupancy
{"name":"collision_free_occupancy","players":2,"topic_count":4,"unit_customers":5,"actual":[2,3],"actual_payoffs":["2","2"],"W":4,"OPT":5,"full_history_nodes":5,"SPE_comparisons_with_self":20,"compared_multisets":10,"optimal_multiset_count":1,"cost_identity_checks":2,"least_optimal_tuple_K":"3","greatest_optimal_tuple_K":"3","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/collision_free_occupancy.json":"82ff7c34fd60823a8bbd2cb7da8e6000424038abcb76558bdaa3b31fd06ef137","evidence/certificates/customer_attraction/collision_free_occupancy.json":"30cc860b6a72effe67d231dc52ef2f992e30ec57d0d4417142848b727ed13f34"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 3]|3|[3, 0]|4|2|True|

## eight_cce_welfare_gap
{"name":"eight_cce_welfare_gap","players":3,"topic_count":4,"unit_customers":8,"actual":[0,1,1],"actual_payoffs":["2","2","2"],"W":6,"OPT":8,"full_history_nodes":21,"SPE_comparisons_with_self":84,"compared_multisets":20,"optimal_multiset_count":1,"cost_identity_checks":6,"least_optimal_tuple_K":"16/3","greatest_optimal_tuple_K":"16/3","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/eight_cce_welfare_gap.json":"e5ca31a0e87cd6ae7f8489bb5d600cc729bd0a1c0a50298e59c185b1032dfa26","evidence/certificates/customer_attraction/eight_cce_welfare_gap.json":"4e5d00a6859049809f687f11409735550cf55f83a5019d51a493493972b5645d"},"unique_optimal_cost_matrix":[["4/3","3","3"],["2","2","2"],["2","2","2"]],"nonoptimal_repeated_222_cost":"7"}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[1, 2, 3]|16/3|[1, 2, 3]|58/9|6|True|

## worst_pne_welfare_failure
{"name":"worst_pne_welfare_failure","players":3,"topic_count":4,"unit_customers":16,"actual":[0,3,3],"actual_payoffs":["17/3","14/3","14/3"],"W":15,"OPT":16,"full_history_nodes":21,"SPE_comparisons_with_self":84,"compared_multisets":20,"optimal_multiset_count":7,"cost_identity_checks":30,"least_optimal_tuple_K":"71/6","greatest_optimal_tuple_K":"41/3","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/worst_pne_welfare_failure.json":"0571643d1d96313be3500096fb89603c9ca42cb81e550121578e66aaa05cdc13","evidence/certificates/customer_attraction/worst_pne_welfare_failure.json":"eaca04a84c7f5447e4821e1df8a1e9a216086963b8e0cc3608d49a3b88cdb7ef"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 1, 2]|77/6|[2, 0, 1]|41/3|6|True|
|[0, 1, 3]|71/6|[3, 0, 1]|41/3|6|True|
|[1, 1, 2]|41/3|[2, 1, 1]|43/3|3|True|
|[1, 1, 3]|38/3|[3, 1, 1]|43/3|3|True|
|[1, 2, 2]|40/3|[2, 1, 2]|41/3|3|True|
|[1, 2, 3]|37/3|[3, 1, 2]|41/3|6|True|
|[1, 3, 3]|77/6|[3, 1, 3]|41/3|3|True|

## residual_counterexample
{"name":"residual_counterexample","players":2,"topic_count":5,"unit_customers":14,"actual":[0,1],"actual_payoffs":["4","5"],"W":9,"OPT":10,"full_history_nodes":6,"SPE_comparisons_with_self":30,"compared_multisets":15,"optimal_multiset_count":1,"cost_identity_checks":2,"least_optimal_tuple_K":"15/2","greatest_optimal_tuple_K":"15/2","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/residual_counterexample.json":"1bd04e4638c5cd855ddb2592db6c572dffecfed17cd0eacbb4b2188975b4337d","evidence/certificates/customer_attraction/residual_counterexample.json":"dfed2c8b278c3aae3d7ab69920557e83f78ebc746e00ba98fc289a1d388dc325"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[1, 2]|15/2|[1, 2]|35/4|2|True|

## aggregate_theta_failure
{"name":"aggregate_theta_failure","players":3,"topic_count":6,"unit_customers":36,"actual":[0,3,4],"actual_payoffs":["10","12","12"],"W":34,"OPT":36,"full_history_nodes":43,"SPE_comparisons_with_self":258,"compared_multisets":56,"optimal_multiset_count":2,"cost_identity_checks":12,"least_optimal_tuple_K":"86/3","greatest_optimal_tuple_K":"91/3","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/aggregate_theta_failure.json":"be0e1a54d3a7ddfeba327c03ce1975932e8fd1018926147b9c555fe6af180aaf","evidence/certificates/customer_attraction/aggregate_theta_failure.json":"cf08edab0813de8eccee8d5466d15b40bd42c980da9b0b68c925f4ae80991010"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 1, 2]|91/3|[1, 0, 2]|284/9|6|True|
|[3, 4, 5]|86/3|[5, 4, 3]|284/9|6|True|

## individual_security_failure
{"name":"individual_security_failure","players":3,"topic_count":6,"unit_customers":34,"actual":[0,3,4],"actual_payoffs":["29/3","67/6","67/6"],"W":32,"OPT":34,"full_history_nodes":43,"SPE_comparisons_with_self":258,"compared_multisets":56,"optimal_multiset_count":4,"cost_identity_checks":24,"least_optimal_tuple_K":"59/2","greatest_optimal_tuple_K":"32","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"examples/customer_attraction/individual_security_failure.json":"bc5202502faa778fae402da4d74a4da8971ffa30bd712423147555b6e15a437a","evidence/certificates/customer_attraction/individual_security_failure.json":"d5c8fc3abe3acf7b4b61b776a957a13e49dfe276df517ee9ba4a47093a2792ab"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 2, 5]|59/2|[2, 0, 5]|92/3|6|True|
|[1, 2, 5]|32|[1, 2, 5]|97/3|6|True|
|[2, 3, 5]|59/2|[2, 5, 3]|94/3|6|True|
|[2, 4, 5]|59/2|[2, 4, 5]|94/3|6|True|

## high_insertion_2cycle_348_exact
{"name":"high_insertion_2cycle_348_exact","players":3,"topic_count":6,"unit_customers":348,"actual":[0,3,4],"actual_payoffs":["147/2","171/2","71"],"W":230,"OPT":270,"full_history_nodes":43,"SPE_comparisons_with_self":258,"compared_multisets":56,"optimal_multiset_count":2,"cost_identity_checks":12,"least_optimal_tuple_K":"189","greatest_optimal_tuple_K":"226","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/high_insertion_2cycle_348_exact.json":"d60b843f01893bf24f11141342918760a9c3f25b44e43e1ddf8e4aefe09303d9"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[1, 2, 5]|226|[1, 5, 2]|698/3|6|True|
|[2, 4, 5]|189|[2, 4, 5]|632/3|6|True|

## terminal_pushforward_34_D_lt_C_exact
{"name":"terminal_pushforward_34_D_lt_C_exact","players":3,"topic_count":7,"unit_customers":34,"actual":[0,3,4],"actual_payoffs":["29/3","67/6","67/6"],"W":32,"OPT":34,"full_history_nodes":57,"SPE_comparisons_with_self":399,"compared_multisets":84,"optimal_multiset_count":4,"cost_identity_checks":24,"least_optimal_tuple_K":"59/2","greatest_optimal_tuple_K":"32","FOMA_EXISTS_on_this_target":true,"FOMA_ALL_on_this_target":true,"source_sha256":{"research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json":"14f8b29548715323a8ee6eac0fabc3efb7e8ea0537fb34cd866c66ed131c855d"}}

|T|minimum_cost|best_assignment|uniform_cost|assignment_count|K_le_W|
|---|---:|---|---:|---:|---|
|[0, 2, 5]|59/2|[2, 0, 5]|92/3|6|True|
|[1, 2, 5]|32|[1, 2, 5]|97/3|6|True|
|[2, 3, 5]|59/2|[2, 5, 3]|94/3|6|True|
|[2, 4, 5]|59/2|[2, 4, 5]|94/3|6|True|

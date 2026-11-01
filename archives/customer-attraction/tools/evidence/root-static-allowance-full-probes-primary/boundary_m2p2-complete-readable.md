# boundary_m2p2.json 完整可读视图

meta={"scope":"Finite complete-history SPE cone discovery; SA remains open unless an exact counterexample is stored","parameters":{"players":2,"topics":2,"steps":6,"seconds":15.0,"seed":202610218,"output":"research/workspaces/customer-attraction/R-ffea274483aa4105a317300038fe04ce/root_static_allowance/boundary_m2p2.json"},"formula_checks":90,"cones":4,"elapsed_seconds":0.019545911000022897,"best":{"instance":{"topics":["T0","T1"],"customers":[{"topics":[0],"multiplicity":1}],"players":2},"query_topic":0,"D_T":"1","W":1,"OPT":1,"D_over_W":"1","SA_gap":"1/2","verified_histories":3,"verified_nonself_deviations":3,"discovery":{"seed":827638671,"mode":"random","root_menus":1,"retained":6,"target":0,"seed_welfare":13},"strategy_terminal_counts":[2,0]}}

policy_d字符串：字符序号j从0开始，对应j的固定d位k进制历史；d0为空历史，k=parameters.topics。
policy_d0=0
policy_d1=00

records固定schema：成功记录 [step,topic,D_over_W,rows,true]；失败记录 [step,topic,false]。原顺序和所有字段无损；纯格式转换，不核数学。
[1,0,"1",2,true]
[1,1,"1",2,true]
[2,0,"1",3,true]
[2,1,"1",3,true]
[3,0,"1",2,true]
[3,1,"1",2,true]
[4,0,"1",3,true]
[4,1,"1",3,true]

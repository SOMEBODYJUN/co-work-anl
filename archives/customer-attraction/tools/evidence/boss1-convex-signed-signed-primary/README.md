# 严格种子退出锥与真删首独审：六原件证据

正式正文为[六原件程序合同](../../../state/程序/严格种子退出锥与真删首独立审计的六原件合同--程序.md)。六主源总288963B，九份依赖与全部主源由冻结来源逐件定位；本目录保原字节，不改相邻原JSON。两冻结提交为`68fad804ec5946cb296f77dc5b336308a66abf12`与`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，本批对应内容相同。逐件blob、路径、size、SHA256和复制来源见[source-manifest.json](source-manifest.json)。

## 六主源

|源ID|文件|字节|SHA256|
|---|---|---:|---|
|3843917d11c266b489f4|[attack_designated_seeds.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/attack_designated_seeds.py)|3220|`b770c61806e41ac2846137803c4c941538976586b4a96356e3d43360305758e3`|
|f643101b3da8aecb9e25|[designated_seed_attack.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/designated_seed_attack.json)|10221|`e99c5ca16adfb5a15b4ec63df3c98bc3d01899dda1fa445ccdf677e8205be7bc`|
|dbde2c6423efa51e6c1c|[independent_floor_deletion_review.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/independent_floor_deletion_review.json)|257750|`679bbce5a4a36284514b5a0efd107692c7cfb07b0a9041b8991ef1015bc48cb5`|
|97bf7e572715010250c7|[independent_floor_deletion_review.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/independent_floor_deletion_review.py)|8957|`866a9df9355ee0f0f1e0f7cc5ce604f940f177c6eac5c532a22fddb2ce5ec008`|
|f2b793206c777d25fde2|[one_cone_seed_attack.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/one_cone_seed_attack.json)|1724|`c05b0afe51623b4b61644614d85883e2e7d43ae111f65de8791f69fbd6e101da`|
|c55f23cf6e3b2e6e4b37|[one_cone_seed_attack.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/one_cone_seed_attack.py)|7091|`3c08e062b138f8d5ae9e33060cd7ec74a1481f1ff50df7fa7d81d4542374130f`|

## 实际输入与依赖路由

|原路径|作用|本地保全|
|---|---|---|
|`customer_attraction/__init__.py`|规范package导出与导入闭包|[__init__.py](dependency/customer_attraction/__init__.py)|
|`customer_attraction/model.py`|有限单位客户/共同目录利润与最优覆盖|[model.py](dependency/customer_attraction/model.py)|
|`customer_attraction/exact.py`|全部可实现SPE终局集合及真门槛|[exact.py](dependency/customer_attraction/exact.py)|
|`customer_attraction/certificate.py`|exact模块导入所需证书类型；本批未调用verifier|[certificate.py](dependency/customer_attraction/certificate.py)|
|`examples/customer_attraction/root_tax_failure.json`|61客户原四人输入，五人仅代换players|[root_tax_failure.json](dependency/examples/customer_attraction/root_tax_failure.json)|
|`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/credible/true_reset_floor_counterexample.json`|31单位客户/原85动作完整策略的准确输入|[true_reset_floor_counterexample.json](dependency/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/credible/true_reset_floor_counterexample.json)|
|`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/independent_floor_deletion_review.md`|原内部独审的读序和数学合同|[independent_floor_deletion_review.md](dependency/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/independent_floor_deletion_review.md)|
|`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/README.md`|原探索/后来指定独审的时序与边界|[README.md](dependency/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/README.md)|
|`research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/signed_seed_screen.md`|已整理的一般净遗漏筛选|[signed_seed_screen.md](dependency/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/signed/signed_seed_screen.md)|

## 仅一次新的保存记录核

已全文读[check_saved_records.py](check_saved_records.py)后运行一次。实际argv、cwd、实现SHA、exit0、耗时及stdout/stderr字节数见[实际调用](record-check/actual-invocation.json)；[完整stdout](record-check/stdout.json)通过。该程序只解析保存数据、逐SHA核15主源/依赖、精确重算12个给定叶的利润/覆盖与预算、核锥正点七个重数和/预算、核85动作域、两audit值同一、每audit340保存行、21行floor结构和5/3差。

它没有导入或执行任何原入口或规范模型/solver，没有BI、真实策略重放、LP、769约束重建、M重算或argmin认证。保存comparison的IC_gap只作字段/非负最小值核，并未重新计算这些gap；有理正点也未用来证明锥最优值。新增数学入口/原入口/规范导入/BI/策略重放/LP均0。

## 已有充分定义核验复用

31客户输入SHA为`2b8fc76f799bee83b5e8588f94f7c8dfa6f91a634ffe624ede820cc909af541c`。已全文比较既有[KC补核代码](../random-retention-common-pool-and-reset-primary/supplement/check_original_31_policy_and_true_three_floor.py)、[修正成功summary](../random-retention-common-pool-and-reset-primary/supplement/corrected-replay/summary.json)、[真实调用](../random-retention-common-pool-and-reset-primary/supplement/actual-invocation-corrected.json)，复用原340IC与真三人85状态/21决策/84强制孩子的成功证据，不重复。旧补核有一次错误加强“末位重置后就是根SPE”的失败，改正断言后同输入成功；完整历史留原目录。该KC过程未重构原四人第二策略，也未做四人全341状态BI，不能代替本signed原程序的构造流程身份。

## 原程序运行合同

`attack_designated_seeds.py`与`one_cone_seed_attack.py`按原目录的`parents[6]`找原项目根，且会覆盖相邻JSON；独审程序按相邻credible子目录找输入，随后也写相邻JSON。这里保全路径将primary与dependency分开，不能将直接在本目录运行原脚本称为原树复跑。若以后确有新的验证需要，应先在临时区按manifest的原路径组装原项目根，把四个规范模块、root-tax输入、credible准确输入和三入口置回原路径，在该副本记录真实调用；需要SciPy/NumPy的仅one-cone LP。不要覆盖冻结原件。

## 数学关系判断

本程序实现/有限检查的是既有真实M、signed修复和删后门槛合同。三指定输入阴性不支付一般MP，固定退出锥的正可行点/无精确对偶不构成全锥下界，31例只反驳含未经末位BR重置目标的删首助手。与SCREEN为调用前筛选关系；与共同后继池后继为不同真实退出上界构造，未由本批证据推出普遍付款。正式正文逐项解释这些关系，未新造超边或把同名signed-harmonic并成同对象。

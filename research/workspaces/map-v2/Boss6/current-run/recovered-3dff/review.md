# 3dff 运行恢复后的定向数学复核

任务：`boss2-wave22-um-repair-3dff15adda4a5b83`，替代已完成的 `unrelated-machines-3a-3a-7670a89f413f26a6`。本轮沿用 Boss6；本地任务为 claimed/owner Boss6，派工时 Boss 已另核远端归属。本 worker 未执行 Git、同步、队列或共享 registry/coverage/integration 写入。

交付收据为 `map/receipts/boss2-wave22-um-repair-3dff15adda4a5b83.json`，SHA-256 `8a49f65c67426d03817582d965f8d549b7e05f3409452a8d7ca757692b316115`。21 个核心的覆盖为 11 linked、10 isolated-after-review；9 个已发布 canonical 资产全部以原路径、原 SHA retained，没有新增/替换/退休边。

## 精确版本差异

本轮实读根 AGENTS、worker 提示词、IMPLEMENTATION、完整当前任务、旧任务及其完整收据、runtime recovery handoff，以及当前全部 30 个输入对象登记。逐个按原生 canonical JSON pin 算法核对，当前 30 个 pin 全部匹配任务；旧任务到修复任务仅 `unrelated-machines/arbitrary-sink-price-cover-final-audit` 一项 input pin 变化。

该对象当前 v3 pin 为 `b84d7dcde4025297f642cc2800ea45a71bb8b442546881884e84441985d40d6f`。从当前记录只作以下反向操作可重建 v2：version 改为 2，去掉 objections 最后的 Boss3 订正说明，将第一条 evidence 的 SHA 从 `1465810d1c9ae66592a579089d33e154a0ab587ac4abc6738d53026cb3b4cb26` 恢复为 errata manifest 给出的 `3a3edde0a48bb34fbb0dccda407d271b43ee322156ecaab6205cb251b75cf026`。所得 canonical pin 精确命中旧任务 `dde0ea37fdd1584dfe632900cb12aa353a12e818ccc9598911930b44014a93e8`。因此旧/新登记的差异精确限于 version、objections 和这一项审查源的字节绑定；model、statement、quantifiers、assumptions、scope、truth_status、body 和其它证据均相同。

旧审查页字节本轮未取得，不声称逐字 before/after diff。`research/workspaces/map-v2/Boss3/source-errata-20261113.json` 明确记录了该页 old/current SHA；上述 pin 反算独立核对其对登记记录的影响。

本轮全文读了以下当前三份审查：

- `任意汇点私有组价格覆盖最终正文内部审计--审查.md`；
- `任意汇点价格覆盖最终冻结读后审查--审查.md`；
- `任意汇点价格覆盖与共同占位联合舍入最终审查--审查.md`。

并全文读取最终原证明 `archives/unrelated-machines/tools/evidence/um-next-four-audit-primary/comparison/research/current/unrelated_machines/arbitrary_sink_private_group_price_cover_rounding.md` §1–9，其 SHA 精确为各审查绑定的 `6c23677ab25afb0db3f0c6ced6b1fb16bb8993a541c875d6b3ee2dfaf3d6e580`。未变成熟数学按旧任务交付复用；本轮没有假称重新全文审查其余所有历史正文、重新执行旧有限证书或继承丢失草稿的运行结果。

## 未知 OPT 合同的承重检查

令 O 为真实 OPT。未知 OPT 版本的静态输入仍是唯一 home、不交私有任务组、逐件合法 sink 资格、宏只在 homes、统一上界 `p_zj≤rho*a_j`。结构承诺在真实 O 处为 `W_h≤O`、`a_j≤delta*O`、每条有限宏边 `>O/2`。

原证明 §7 的程序只取消“宏边 > 当前 T/2”这一检查。它仍剪掉宏边 `p_hb>T`，仍检查 `W_h≤T` 与 `a_j≤delta*T`，随后运行同一 cover/共同宏匹配/MW/基舍入。审查中“不检查结构 promise”不应扩读为取消这两项显式当前 T 上界；它表示算法不验证涉及未知 O 的原承诺。

对 T≥O，原最优调度在每个 home 至多放一宏，因为两个宏各 >O/2 会超过 O。该调度所用宏时间 ≤O≤T，故不会被剪；其 occupied home 的私有留量 `<O/2≤tau*T`。真实承诺同时推出 `W_h≤T`、`a_j≤delta*T`。因此**同一份**原最优调度提供共同 macro/home/出口见证，不能把各 home 的独立选择拼接冒充它。

对该见证的出口删冗余得到真实 minimal cover；empty home 私有任务全部回 home。对每个共同价格向量，该共同见证的总价格成本 ≤T，覆盖 FPTAS 和最小成本宏匹配给 ≤(1+epsilon)T，故在 T≥O 时不会 FAIL。MW 积累的每轮真实共同匹配，平均后提供同一平行扩张基的显式分数点；非空模式 home 仍能覆盖全部宏，home 容量一也完整保留。

任意成功查询的恢复只需要实际被选宏 ≤T、保留的 W/a 上界和真实 cover 的列预算。它给 home 负载 ≤(1+tau)T、sink 负载 ≤(1+eta+b0)T，因此仍为 alpha*T；没有重新使用当前 T 的宏下界。低于 O 可以成功，也可以非单调接受。分母网格的“失败下端严格低于 O、成功上端保存真实调度”不变量足以在终止时给 alpha*O。

结构承诺不可一般验证，当前结果也没有从一般 UM 矩阵生成 home/组/宏/sink/统一余量的算法。复杂度为 poly(L,1/eta)，没有生产级有理 LP 后端。这项复核不支付一般可靠阈值接口的全输入前提，`UM-TARGET-v1` 仍 open；一般物理复制/低峰 decoder 的开放义务也保持。

## 9 资产为何保原字节

本轮逐条实读边 JSON 的全部解释、条件及结果范围。所有边都不以唯一改版 review 为端点，也不引用发生变化的审查页；它们的当前 endpoint pins、evidence bytes/标题和 review digest 均通过新的原生 edge-check。

额外实读范围如下，均为本轮读取而非继承声称：

- Li 资源 §2–3、BGW §5，核小槽扩张、中心匹配、前槽收费及尚未给出的分布式并发桥；
- 包络资源“单行定义及可提取性”、半密度原程序审查“半片、一次共同匹配与真实森林”，核全部原任务的同一次匹配；
- Karp §1、§2、§3.4、§5.1、§5.4，核历史语言、三点路径、incidence 转置与 base(r+1) 无进位编码；源端其余已发布 NP 完全性证明继续复用；
- cactus 主审查的精确块算法和任意给定围长间隙族两节，核 b=1 的实际可解性仅是局部贡献，配置阈值仍为可行上界；
- 共同流正文 §3、§5–6 与版本审查 §3，核两 actual 半半流替换 r 份平均的桥、整数件数容量及两套任意 S 的完整原任务回填；
- 一般问题的阈值/剩余缺口、可靠阈值接口节、双树正文的排除范围，核一般目标条件边与 CONFIG 动机边不同。

8 条逻辑边中，4 条为 whole、4 条为 step；另 1 条是 context。所有 step 的 remaining 和唯一条件 whole 的未付接口继续保留，没有因结构检查通过而提升数学状态。

## 旧 overlap 的保全

旧任务的 Kronecker follow-up 已作出数学处置；本轮实读同一正文 §7.1–7.4 再核：一般未剪枝 assignment LP 值 F 精确可乘；特定 actual seed 却从 OPT=3/2 在完整平方降至 1，并由十五件同时交换给全任务证书。F=1 不保证一般实际积分；一个 actual 特例也不推出任意矩阵的 LP 恒等式。这是相容的不同量词结果，未解决奇幂或受限 hard image 的保 NO 问题。

此处保存在 Kronecker coverage 和本笔记；当前修复定义没有 overlap_comparisons，故新收据的 closed_overlaps=[]，不复制旧对象对造成 unknown-closure。旧两个 in-packet 比较的实质结论继续保留于对应 coverage，不另制造后续任务。

## 本轮实际核验

`recover_and_check.py` 创建新收据并保存 `validation.json`；所有检查实际在本轮执行：

- 30 个当前 input pins；89 个去重精确引用绑定、60 份引用文件的完整字节与所用唯一标题；
- 9 次 `python work.py research edge-check`，另以原生 `_map_receipt_coverage`、`_supersession`、`validate_map_follow_ups` 核收据，确认 retained 与旧资产数组逐项完全相同；
- Fraction 精确算术核 68 组平衡参数与反代、300 组 MW 不等式及余量恒等式；
- 对最优网格点 1..10、上端至 12，穷举所有低阈值接受图样，共 8,164 例，核原证明与一般条件边两种二分写法；
- 自建两专用 home、两 unit 宏、每组两件 1/4 私有任务且无 sink 的小例。真实峰固定 3/2；rho=1、delta=1/2、eta=1/4 给 tau=7/8、alpha=15/8。在 T=1、3/2、2、3 时保留检查及成功解码均成立；T≥2 时当前宏下界不成立，表明取消该检查确有作用。T=1/2 宏剪枝失败仍正确低于 OPT；另核 W 超界和 delta=0 的直接乘法守卫。

这些是结构与有限 sanity 核验，不替代上述一般证明，也不是旧 upper-column、price/MW、Kronecker 或其它历史有限审计的新运行。旧任务、旧收据、9 边、主正文及共享文件均未改。交付冻结给 Boss 保存后处理；本 worker 不提交队列 done。

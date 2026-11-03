# 均匀全槽池九原件与有限执行证据

正式说明：[均匀全槽池的精确尾审计与三类有限攻击合同](../../../state/程序/均匀全槽池的精确尾审计与三类有限攻击合同--程序.md)。完整主源九件61727B均读，四程序/五JSON全部正文及数据结构保全，输入依赖十二JSON及四规范模块亦按原SHA保存。

本目录沿用中断前已经充分完成的一次标准库Fraction核验：`verified/event.json`、`verified/stdout.json`与空`verified/stderr.txt`；恢复未重跑原四main、原/新均衡求解、LP、SLSQP或该独立核验。新`self-check.json`只记源字节、平坦frontmatter、链接和处置结构检查。

原始来源统一冻结于legacy-cleanup `68fad804ec5946cb296f77dc5b336308a66abf12`与main `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；两源同路径同字节。完整source refs/大小/blob/依赖角色在`source-manifest.json`。

|主源ID|文件|字节|SHA-256|
|---|---|---:|---|
|23bd57f56c76a81d23cf|[attack_pooled_full_cone.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/attack_pooled_full_cone.py)|3446|0068832e18c3771bacebcd7377e2574e06a9213d62e8d2f80c213eedb081c97d|
|a622427fde1ef2070006|[attack_shared_cone.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/attack_shared_cone.py)|7164|f865e32a0ef63a234d8cfc390586d0834f7c503e8972486b7481f4001fda7221|
|51ade31b3d6f6521a619|[audit_terminal_pool.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/audit_terminal_pool.json)|3021|bc2eb6b476c16fa8b628528374cfd8e7976ff216372aa12c9725b4dfbcb154c4|
|bd80ac5bfeacbae563a1|[audit_terminal_pool.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/audit_terminal_pool.py)|3674|ad0d400ad7bb1ba0b1892808293b4df5b27e144748acf5c171e948bd4e7f03a5|
|9884979cd5b09099b910|[pooled_full_cone_attack.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/pooled_full_cone_attack.json)|29816|1b07b0581d079afa474ba869881aa9545f685d66561d6c01dbc880ab6911eefa|
|f60884bf6affcdd2e21d|[pooled_full_probe.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/pooled_full_probe.json)|2667|e051f7bd3916382e0b4c16e7d1139067dc0c8591bde5a32f6895f8283192ba14|
|1d27993cac177644180d|[pooled_full_probe.py](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/pooled_full_probe.py)|3143|3dec241d1dedd6f2021425aab486fd185223ddfcad7157739d69294da52ad3de|
|b8676cbcecc4f65b51c8|[shared_cone_best.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/shared_cone_best.json)|2426|742e6f727a134f031fb2ca167297b7688d447db67041aae6cc475e53dba16d4a|
|7a301393b149d47a8c70|[shared_cone_run.json](original/research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/round6_general/convex/shared_cone_run.json)|6370|5d0ef155cec4eb37ffc7404004cc567e8a83a6b38a5a8b074d3ea3d0010a5a4f|

## 所有原报告的独有内容

- `audit_terminal_pool.json`：六记录、每记录15字段；全部有理IC、cross BR、两插入税、共同Jensen、early、bank和W−mF不裁剪。
- `pooled_full_probe.json`：六条完整p、float F/gap、W与原全历史核验计数。此p最优性未精确认证。
- `pooled_full_cone_attack.json`：24条m/k/actual/ratio，每条完整p/2^k−1质量/iteration/ic_min/normalization；没有阴性政策全树，不能只用报告重放它们。
- `shared_cone_run.json`：30个trial摘要各是该trial三p中的最好一个，并非90个保存认证；默认参数20与保存30的范围分别保留。
- `shared_cone_best.json`：trial0完整21行policy、15质量、4p、12q；只有该保存角点作指定有理恢复及精确全IC，未认证其它29政策。

## 输入与实际事件

六游戏及同名证书严格按清单角色保存。root_tax为游戏SHA `864eca4cc1d5df2d039704eb444863405298e6fc6746efb18c49035a801a7ce6`、证书SHA `59fd58d85a3c3b989837467eb3523286d1f5ee529b0f119cd4d263bef6984111`，61单位客户、实际AAAF/0005、W38。规范Verifier按全部有序历史读给定策略，未调用outcome-set solver；exact模块只因包初始化被导入。

既存独立事件argv指向`verify_pool_records.py`，Python3.12.14、exit0、wall0.12339618599980895秒、script SHA `1e335c53a13e82093ddc950cebad1787199b9f782c853a88209d3a3e6638a6e2`。六记录合710完整历史/3338非自身偏离；均完整record字典相等。另保存角点21历史/63非自身，恢复mask1=1/3、mask14=1后重核全部IC；全部12删槽列两正型负载恒(0,2)，任意p/q值1/3、W1。不是把原binary浮点当有理等号，也不把K−等号用于K+ PF。

`event.json`的original_main/canonical_solver/canonical_verifier/lp/floating_optimizer calls全部0；独立标准库核验没有导入原程序或规范包。原源码/旁报告不被该事件变成新运行。

## 全仓实际比较与关系

- `archives/customer-attraction/state/引理/均匀全槽池的末两行与共同Jensen储备--引理.md`
- `archives/customer-attraction/state/引理/均匀位置完整菜单的极小极大与标签产品可加性--引理.md`
- `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`
- `archives/customer-attraction/state/计算/共享菜单固定查询与全局鞍点的双精确证书--计算.md`
- `archives/customer-attraction/state/审查/共享凸负载的静态信用与真实末位误差--审查.md`
- `archives/customer-attraction/state/资源/第十一轮共享负载的凸信用与共同付款停界--资源.md`

成熟末两行引理沿用；新程序页实现其有限精确检查并分清SHARED K−、PF K+与指定q_i=p。均匀菜单/逐行最小是邻近而不同的域；双精确证书提供真正query活跃/KKT的对照；round11审查确认旧混合/早期金额尚未付。本资源没有导向普遍PF、SHARED、六人half的证明边。

## 三个须保留的停止点

1. `saddle`实际均匀赋权数值近活跃query，注释LP stationarity不对应实际代码。
2. `minimize_query`非success但行和误差小仍可继续，未产精确全局KKT；float cut值不自带全局下界。
3. PF阳性有理接纳未显式核wf≥0。冻结24条均false，无阳性输出，此缺口须在未来编译时补核。

逐源receipt与发布路径清单由Boss1父方串行提交；本worker没有commit/push/sync/claim/done或通信外发。

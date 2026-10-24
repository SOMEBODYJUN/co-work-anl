# incoming off-history 账的独立核对

2026-10-23。对象为 `../credible/incoming_slack_transport.md` 本轮稿。逐式检查已通过下述范围；没有核新实例，不把此账认作 K_in 总付款。此审查读取作者陈述和证明后独立重构，不称盲审。

设 A 为 actual-prefix查询a的完整真实叶，B为自然 incoming 的原父历史 g 后规定a的真实叶，W为同一g偏离原实际主题S_i后的真实叶。原SPE在g给 ell=u_i(B)-u_i(W)>=0。actual slack精确为

    u_i(Z)-u_i(A)
       =[u_i(Z)-u_i(W)]+[u_i(B)-u_i(A)]-ell。

因为 S_i subset C，前一差只在 C；后一差按 a intersect C 与 a outside C 分开，正是作者 OFF-IC，符号及全部正分母正确。它不是只含 tracked incoming 客户的等式。

对 fresh x，actual前缀覆盖0，off-history背景b>=0。以未来 coverer U、V记两叶，1/c_B-1/c_A=[|U\V|-|V\U|-b]/(c_A c_B)正确。若 x 是从更早父查询转来的 tracked客户，则父当前主题覆盖x且保留在g，故b>=1。新增 recipient j in U\V严格未来，贡献1/(c_A c_B)<=u_j(A;x)/2。

乘整体系数theta后，对每个recipient的tracked贡献H_j<=theta v_j(A)/2。A中j的历史是真实原历史，之后确实沿sigma，因此可购买其完整IC；正方向仅为(H_j/v_j)d_j(query)<=H_j。不能反向用便宜query价支付H_j，也不能直接把v_j(A)换成actual u_j。

补充一个安全合并范围：若多个父g进入**同一**actual查询s=(i,a)，A完全相同。按父来源拆theta_g、各自tracked集合后，对同一recipient可相加为

    sum_g H_(j,g)<=[sum_g theta_g]v_j(A)/2。

它仍是一份同A whole-IC系数；跨不同s/A的共同付款没有因此解决。credible 收到该补充后独立核对同意。

剩余三类支出与作者范围一致：C内跨叶迁移、非tracked的新R广播、真正新outside，外加负ell必须同账保留。owner-return不自动具有sigma(g)=a的自然见证。没有发现IC域或支撑错误。

与 relay 共用priority世界仅有一条尚未付款的标签：tracked x若在某actual查询终止，该叶全部未来coverers均低于U_owner；FRESH正recipient位于这些未来角色中，也获同一低阈值标签。该事实不证明其整体系数可共同结算，未升级为收缩或half。

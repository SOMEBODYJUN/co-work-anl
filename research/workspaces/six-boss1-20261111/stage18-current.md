# Stage18：1586行精确全域界、整面排除及两套完整新参数族

## 恢复入口和原题

Boss1；RUN `six-boss1-20261111`；结果分支 `rebuild/research-v2`；父档 `customer-attraction`、子档 `six-providers`。实际研究 clone 为 `/workspace/scratch/b0fef5ec503f/co-work-anl-boss1`，全部推导和计算在 `research/workspaces/six-boss1-20261111/`，RUN事件在 `research/runs/six-boss1-20261111/`。原题仍是任意有限单位客户、有限非空共同标签目录及每份完整有序历史纯SPE的 `2W>=OPT6`，或满足全部离轨弱最优性约束的精确反例。空主题、重复动作、覆盖别名、零客户和全部弱平局均保留。

写此说明时最后确认数学推送为 `4328330998fcd54659ff38060243bb450720a785`；正式图十四条关系已接回并推至 `3d2b34b8e72754f31e13e9e2c15c8f89fe090e32`。本阶段新的pushed身份以实际 `checkpoints/stage18.json` 回执为准。只把确认pushed的内容当作远端可恢复；活跃新目录单独列于末节。

恢复先运行 `python research/workspaces/six-boss1-20261111/restore_frozen_text.py`，将所有 portable_frozen_text* 清单中的原始冻结字节准确还原；再 `python work.py research resume six-boss1-20261111`。冻结TSV中的末尾空字段保留于无损gzip，没有修改原数学输入、清单或SHA。不要重跑任何已消费LP，也不要为了重放而调用有写入的发现程序。

## 已核的1586行普遍界

`visible_maximum_joint_v4/` 保全部1586原行、513非负列和两等式，输入SHA `fbd3b0cb65736b5c41b64dd630b442e9647b701e446c36819e3f726c620ac839`。上游1050保持未求解；本输入经Main明确释放后在 `visible_maximum_joint_v4_solve/` **恰调用一次** highs-ds，65迭代，后续精确恢复和面分析均0优化。

\[
\alpha_{1586}=\frac{208101173892952666162424962783956947305005629564084333}
{471722007522064528882747177426615554317607603285651548}
\approx0.4411521416736506.
\]

完整原尺度非负对偶证明 `W>=alpha1586 OPT6`。证书SHA `6049aba7ddb134159f95adea1f3bc6470bdfcb902a111e702e52b9b6f3cec34b`；最终manifest `cf4f29d6ed36d09de746314b49b3ec6c7269c207fbb3cda6a54c19285f4e195f`；proof `74c44f77ac0f6986c1cae020f5b60432968867bf2343233197612a67f3bef0f7`。Main亲读完整证明，另核全部1586原行/513列/两自由等式及互补，记录于 `main_visible_c_v4_certificate_check.py/json` 与 `main_visible_c_v4_proof_review.json`。

全部零对偶列有20个，正行/等式秩13，准确全最优面为七参数并保全部1586不等式。实际正C行1018、1433共同在同一真实历史(A1,C)取等：完整弱零态先保留后取交集，中间R3/R4/R5覆盖恰C且收益都是K/5。真正内部SAFE分别要求K/5>=N3,N4,N5，而全脸三个差均严格固定负；Main独立核全部15个泛函的7695列有符号身份。因此整个必要锥最优面无完整SPE实现。此非达到结论不自行给出统一新epsilon，更不证明half。

## 已核的181行连续菜单完整有限化

`all_source_ordered_joint_menu/` 证明外层强制Q_k、内层对同一六菜单中的五索引l!=k平均，保准确重数d和各真实续局。连续域内d=1唯一最弱，客户系数具有 `L=max(0,ell_j)` 的分片仿射损失。旧67参数顶点只给合法样本，不能直接生成整个连续族。

`all_source_ordered_menu_cells/` 切成14个活跃区域，完整181参数顶点（源1/2/3/4分别119/40/16/6），包含67原顶点及114新交界点。每区域内行仿射，因此181行准确生成指定连续族；不是所有SPE钱包的最优性声明。family SHA `f1bca409d9927f9721764a327f1fcd52a18c38f0968d9c240fa20288aa95eac3`，manifest `313e3fe07138c1ecf0b42bd8fbafa4e4f334f583141f0a950eeb71bb09ad6430`。

Main亲读两包证明并独立重建32448个边界组合、全部14区域/181顶点/369关联、92853系数与114个严格Jensen差。全部PASS在 `main_ordered_cells_check.py/json`。最初Main检查程序的整数除法误生浮点已明确修正为逐元素Fraction，失败记录保留；没有修改冻结来源或矩阵。181包原样保119根行，任何冗余另由完整正付款证明。

## 已核的28行联动域与26条整面分离

`source2_cap_coupled_internal_safe/` 同时给源IC、内部SAFE和中间大小帽增权。固定theta*下的参数(e3,e4,e5,s)完整域有11个真面、28顶点；关键新增面为

\[
\tfrac34e_j+\sum_{l>j}\frac{e_l}{6(7-l)(8-l)}+s/20
\le7/10+\theta_j^*/4.
\]

原“e域乘[0,9]”猜测被真实态余项−1/192否定；保留全部12个失败候选状态。新family SHA `b5c950664a21da750245cb7115dc3a60721feb494ce7cf1e32771d5aeeba2906`、manifest `a744e986913415ac964c6fc12dafa51a86f1982983b2a6fcd0507091bfaafd28`。Main再重建全部11面/330交点/28顶点、3584真实余项、224准确min及14364列。28行中的26条在完整1586最优面上固定严格为负，另两条是已紧基底端点；见 `main_cap_coupled_complete_check.py/json`。

Main自己推导的六个单坐标端点、失败product原程序和完整768态保在 `main_cap_coupled_safe_seed/`。新行先由非负真预算支付，再写成旧基底行加sum e_j(u2−Nj)，不能把各u2−Nj擅自当作普遍非负。

## 当前实际下一义务与写入范围

- `/root/early_shared_x_source_audit`：`source2_minimal_cap_safe/`。新任意tau>=0，改中间帽为beta_j=1/12+tau_j+sum_later tau_l/[6(7-l)(8-l)]，完整域与C-only行；0优化、不读新点。28点旧包已停写。
- `/root/visible_maximum_joint_solve`：`all_source_minimal_cap_safe/`。推广同一直接付款到源1/3/4/5，保H=t/min(D,5)，先核真参数域和枚举规模；0新优化、不读1586点。1586求解包已冻结停写。
- `/root/visible_maximum_joint`：`ordered181_on_1586_diagnostic/`。Main已明确释放准确1586点/面作只读诊断；核全181准确面表达及119根的ROOT270正支付。0优化、不改冻结181。
- Main：回流独有连续付款引理和新的全域精确界到正式正文/登记；亲核下一更一般帽族，组成新的完整全类型输入后才明确释放新的一次求解。原734固定C模板保持UNBOUND，已排除的1586全脸不花phase-I。

本阶段checkpoint排除以上三个仍活跃目录及其相邻笔记，只推已闭合实际产物、Main推导和RUN。任何 `work.py sync` 前必须先协调停写；不能再让include-untracked的stash与子席写入竞态。checkpoint只串行选择闭合路径，不stash/reset/清理活跃工作。

旧23676×21021固定16hist云任务仍唯一为 run43096304349（请求C-six-boss1-common-x-joint-23676-01）；本轮仅查询原请求并保存 `cloud23676-check12.stdout.json`，没有重发、取消或绕过本地Actions守卫。其结果若尚未取回，单列为待取云端产物，不计入已核全类型界。

half原题仍OPEN。继续从真实分支的内部偏离付款推导，不以新的必要锥低点冒充完整SPE，不在checkpoint后结束研究。

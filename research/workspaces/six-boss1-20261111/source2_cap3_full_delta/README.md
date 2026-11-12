# Boss1：完整δ区间的第三帽减量

RUN `six-boss1-20261111`；实际 agentID `/root/source2_cap3_tradeoff`。本阶段隔离于本目录，原cap3冻包及REPO均只读。

## 结论

一般合法T的h差公式、C-only全域冗余身份、ordered的两类p的G公式都覆盖整个 `0≤δ≤5977/6912, 0≤h≤B(δ)`，原样成立。所有正重数整域严格有 `f1<f2<⋯<f6`，相邻差至少8567/82944；没有最弱菜单重数转换。

旧 `m0=min(零尾,1000)` 的简式在ordered四个大q条件必须增加1100候选：p0的q=3/5、4/5、1，及p1的q=1。准确修正为 `m0=min(Z,J,J+E)`，E由真实成本相减给出。新损失不改变上述h差，因为1000、1100都有r3=1。s=9、δ=0的原损失187/27648仍保留。

## 文件

- [proof.md](proof.md)：完整解析证明、真实预算、全部条件修正、有限生成与结论边界。
- [exact_envelopes_2d.json](exact_envelopes_2d.json)：96条件、1536真实成本平面；每个尾的完整闭弱域；150个cell、369条边、225顶点及全部弱态。
- [independent_weak_regions.json](independent_weak_regions.json)：独立边界线对枚举重建，含167个二维域、44个一维域、9个孤立点。
- [all_cell_corner_certificates.json](all_cell_corner_certificates.json)：全部205824个cell角点逐尾差证书。
- [formula_audit.json](formula_audit.json)：各旧公式的整域真伪、四个大q准确失败见证和修正式。
- [multiplicity_cell_certificates.json](multiplicity_cell_certificates.json)：全部重数对在每个cell上的准确比较。
- [row_recipe.json](row_recipe.json)：完整513列坐标约定、真实IC/K/freeEC和行构造配方；未物化矩阵。
- [four_corner_interpolation_checks.json](four_corner_interpolation_checks.json)：四角凸组合的全部局部系数身份。
- [literal_checker_output.json](literal_checker_output.json)：独立检查PASS及完整计数。
- [boundary_catalog.md](boundary_catalog.md)：紧凑边界目录。

若未来按全物理条件复形物化，保全部来源和接口时为585条端点行；本阶段仅交付配方及有限顶点，不生成这些矩阵。C-only全二维子族已由旧δ底边15条端点行加非负客户质量支付，可以关闭。

独立检查从真实个人份额重建全部成本，使用172989个边界线对、74880个公共角点逐尾重算、205824个cell角点尾差及全部菜单索引路由。优化器调用为0，LP点/最优面读取为0，旧包修改为0。执行失败记录为空，数学失效见证完整保留。

复现见proof末节。全部新增文本只以一个换行结束，无行末空格或tab。完成后冻结并停止写入，交由Main接入同RUN。

# Degree-two group bounded-menu：canonical 最终 read-after v2

审查者：general_query_response_review。2026-10-18。

审查对象：`co-work-anl-boss11/research/current/unrelated_machines/degree_two_group_bounded_menu_joint_rounding.md`。

审查版本 SHA-256：`41ceb9e9bdbe2fe81705d2c4f8b64c23983beba2f9767ec97ad36db4eba97e18`。

读取顺序：先只读新 Exact 及获准 primary §5.1，独立重构、渲染查看 PDF10–11 并冻结独立记录；之后首次读作者 Proof，另冻 read-after；本轮才实际通读整个 canonical。未修改 repo、Work、Git 或此前冻结字节。

**最终结论：canonical v2 通过，无 fatal。完整输入、真实 OPT 分析、published 接口和原 jobs 恢复与已冻结 Exact/Proof 一致。**

## 完整组合核对

1. **结构域准确。** 显式非空 groups 与非空 indexed menus；每 resource 跨全部 states 至多两不同 groups；state 私有机独有、private row sum≤1；selector 外无其它 jobs 或 side constraints。每 incidence 的两原端恰为本 state 私有机及单位 resource 机。资源 tag 与私有机 tag 不交；结构标签是输入而非免费识别能力。empty states、重复 indices 和 zero private jobs保留。
2. **完整实际输出。** 所有原 selector 和 incidence jobs 各赋值一次，只用原合法端。allocation 后每组只选一个 state，未选 state jobs 全部停回各自私有机；没有隐含丢弃其它 state jobs。资源 sets 跨组不交及单 state 内无 multiplicity 给 resource 机至多一枚 unit。
3. **归一化恒等式。** normalized 私有 row sum=1 时，allocation→schedule 负载是2−选中 clause 质量，未选 state机1，故OPT≤2−V。反向只在最优C<2使用 resource unit独占，并可无损收回未选 state jobs。OPT=2 的独立分支用V>0会产生<2调度而矛盾，未把独占错误延伸至2。selectors使OPT≥1、全私有基线使OPT≤2。
4. **平均层次与 coupling。** 每group一辅助 agent，`f/K≤f/K_g≤v≤f`；同组多 state 重复出现同一 resource 不增加 auxiliary agent 数。A≥V/K，外部 degree-two additive 后端输出全部groups共同满足的 allocation；最后再扫描每组菜单选一个真实 state。没有先锁定 heavy matching、拆散 states 或后补 diffuse choices。
5. **外部来源逐条件符合。** 唯一 imported approximation 为实际读过的VW2010v1 §5.1 Theorem12。items 是 resources，positive-value agents 至多两groups，两端异值允许，degree1 bonus允许、zero edges可删。primary hash与实际原PDF吻合；没有导入其 makespan LP-gap。canonical明确是结构推论，不把已发表 additive 近似冒称新算法。
6. **阈值后端不能当精确feasibility。** §5正确说明：失败只证明 additive OPT<T，成功仅给效用≥T/2。用失败单向证书维护二分上界并保存成功输出即可得到factor2，无需接受谓词单调。独立核查：清分母后整数OPT=A，最后 upper=lower+1且A<upper给A≤lower，保存的效用≥lower/2≥A/2；A=0以空allocation处理。canonical未声称重构technical-report的精确二次实现。
7. **relative-OPT 与 ratio。** normalized输出≤2−V/(2K)，配合V=2−OPT给式(1)第一项；差值 `(2−1/K)(OPT−1)≥0` 给ratio。算法不输入OPT、V、原最优σ、YES witness或state分布。绝对阈值只用于OPT=1，不对任意输入冒称C≤2−1/(2K)。
8. **Bonus精确保OPT。** 每欠量 indexed state只增一枚独有resource及job，bonus私有时间1−W。原调度C≥1可把所有states的bonuses各自export至新机，C不增；augmented删除bonuses也不增。实际OPT双向相等，K不变、degree条件不变。运行normalized算法后删去的只有新增bonus，原jobs不删。
9. **位复杂度。** 所有 states/resources/incidences显式，无succinct展开。row sums、averages、bonus及common-denominator缩放的编码长度poly；不按分母数值复制资源或jobs。二分依赖数值位长而非数值；state argmax与实际全部原job输出均poly。K可随输入增长而算法仍poly，仅固定K给统一constant改善。
10. **Promise与cube。** 检查实际输出正确决定strict-unit YES versus OPT>R promise；中间实例不作承诺。tagged cube在明确injective incidence indices下跨组数≤min(d,Q)，Q=2可用；K≤7给27/14。旧uniform/DGR结果仅作较窄域对照，未被引入本新证明；本次没有重新认证这些旧比较定理。
11. **2SAT准确。** unit selector使所选 state所有正权 jobs必须export，zero可留根；因此strict-unit可行等价于跨组选中正supports不交。canonical明确只对跨组冲突state pairs加2CNF，single-state组固定即可；此边界不需要degree2，也不提供更大makespan精确OPT算法。
12. **软件与范围。** 本页只称软件状态另行登记，未声称generic backend或联合算法已完成实现。审查未运行新生产软件或以有限例子替代全量词证明。resource外端必须exact1、group-degree≤2、private machines独有及无其它约束等均是实质前提；degree3、任意外端时间、一般UM或全局新颖性均未认证。

已逐字节扫描该canonical：除正常LF外没有ASCII控制字节，公式未出现反斜线转义污染。本轮未发现需要修正的公式或范围措辞。

**冻结批准：上述hash的canonical数学与组合通过；旧raw/v1及本审查此前冻结来源均保持原字节。**

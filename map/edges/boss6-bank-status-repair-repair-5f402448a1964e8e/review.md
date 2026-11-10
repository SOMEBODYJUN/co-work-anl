# Boss6 round48：root-only threshold 精确替换审读

当前任务 `boss6-bank-status-repair-repair-5f402448a1964e8e`，owner Boss6，request `775ec5aed9dc47e8bbdf18f58fa2d151`，definition pin `a198f64bd27f8ba03da221536866df30257281e8d7a2ff70cb6fb16c83f5039a`。本包只 supersede 当前有效的 `round18-ca-representation-repair-repair-29b87721a16fc7a3`；更早227包保持已被替代，不复活。新正式关系为 `cag-r48-bank-controller-instantiates-root-only-threshold-crossing`，accepted / unconditional / whole_result。

## 当前输入与精确继承

实际任务是19 core、8 read；27个登记pin全部与当前registry一致。与有效旧receipt相比，仅bank read输入从v2/finite升为v3/proved：`5793c5af5870d521dab05af319ab471892e8ac837820b65dbb796c1879aaca0c` → `0130f938c010a5a8b941ea5d24f6932c1075fdf5778124bbbf57cc62184b3be4`。approved delta逐字段比较仅version、truth_status变化，body、statement、model、量词、evidence等全部相同。19 core的pin全未变。当前target是R79 v2/proved，精确陈述是下述指定银行控制器的根唯一低，而非整份资源中其它话题。

旧receipt的16个资产逐字SHA及canonical归属均核对；仅旧root-only路径被替换，15个未受影响canonical资产保原path与原SHA，不复制文件。新receipt的18个未受影响coverage条目与旧receipt逐字段完全相等；唯一受影响的R79条目只更新edge ID、source v3/proved状态及本次已证无条件说明，保留原数学结论和量词。

## 独立实读与控制器解析复核

本轮完整实读bank正文206行、R79资源133行、模型129行、source/target/model完整登记记录、原canonical边、有效旧receipt及其全部coverage/沿革。Root独立窄审计review与audit JSON、approved delta作为已有审计依据审读并核对本次源改版。其余18核心与相关数学承接旧包成熟审读，不机械重读context_plan所估396982 tokens；15个保留边只作当前绑定、证据/文件SHA核验，不将该核验表述为本轮重新实读所有旧承重证明。

经济单客与两客户银行全乘积给每个主题收益1/n_a+2/n_b。BASE在任意根实际行动后以该行动重锚，因而根全部偏离仍处在同一预先定义的σ中。BASE中间位规定收益2+1/(m−1)>2；非规定新银行进入以该已发生银行为固定目标的PUNISH，末位恰多分一次银行，使偏离者收益≤2；旧银行分支亦≤2并进EXIT。BASE末位每银行已有一人，取未用经济可得2，是真实联合BR。

PUNISH进入时过去银行全异、目标已在过去；剩r人时恰r−1个未用银行。非末位选fresh两坐标，此后fresh银行不再被目标规则复制，收益3；末位取未用经济及任一已有一次的银行，最佳值2。目标固定不随后来的fresh行动移动。任何银行重复永久进EXIT；已有重复使深度t未用银行至少m−t个，经济亦够，所有再次偏离后合法性不变量仍保持。EXIT规定收益3，达到主题裸上界。逐节点收益/全部真实联合偏离证明覆盖同一σ的每个有序历史，而非normal path或冻结偏离续局。

根任意主题的真实续局均给经济m−1人共享、银行两人共享，u₁=1+1/(m−1)=m/(m−1)。实际覆盖两个经济客户与全部银行客户，W=2m；m个主题可覆盖全部3m−2客户，因此OPT=3m−2。这些公式均由原解析全参数证明承担，本轮没有运行旧全树或solver。

## 完整目标与无条件性

固定原总m与原OPT，令t=(3m−2)/(2m−1)。有3/2−t=1/[2(2m−1)]>0，且

`t−u₁=(m²−4m+2)/[(2m−1)(m−1)]=[2+m(m−4)]/[(2m−1)(m−1)]>0`，每个整数m≥4。

因此根全部行动值低于t；proper BASE非末2+1/(m−1)、末2，PUNISH非末3、末2，EXIT3，都≥2>t。m=4例4/3<10/7<2。新whole_result明确包含目录、完整SPE、W/OPT、固定门槛、全部proper规定收益及根唯一低，覆盖当前R79 v2全部陈述。源当前proved，没有其它开放前提；m≥4及指定σ是已证适用域，原仅因finite保留的conditional理由已失效。

量词不扩大为任一proper子局其它SPE的最低leader值，不涉及该资源中静态匹配、有限锥报告、动态incoming预算、其它模型或一般half。source自由分数逐人严格失败、聚合与half的原边界全继承，不增任何结论。

## Supersession、结案及执行边界

本次直接替代旧有效round18 receipt，16资产逐项明确15 retained、1 replaced；新edge路径是唯一replacement。此前227→round18的资产沿革仍由未改旧receipt精确引用保存，不作新的supersession目标。旧receipt没有顶层follow_up_tasks/closed_overlaps，任务本轮也没有deferred overlap；旧supersession中的三项retained_closed_overlaps逐字承接在本轮对round18的supersession note中，作为历史结案而非本轮新结案。无新增follow-up。

`binding-preview.json` 仅以当前对象及证据执行只读 `edge_bindings`；绑定值只写入staging edge，clone零写入。Root安装后按正常native edge-bind/check/checkpoint/done流程发布。全27 pin、全部16旧资产SHA、15保留边当前绑定和原证据SHA已核。manifest的新文件与retained canonical分列；manifest不hash自身或receipt，receipt可hashmanifest，无循环。

本轮科学程序运行0；无旧LP、BI/SPE solver、全树IC、有限扫描、成熟科学证书或原CLI重跑。Python均-B。没有Git、队列、clone写入、凭据或Library访问。仅做正文数学审读、JSON解析、SHA/pin/证据标题与只读binding元数据核验，保存本指定staging镜像产物。

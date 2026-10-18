# 归一化XOS规模锐界：canonical §4–6 最终实际 read-after v2

审查者：general_query_response_review。2026-10-18。

对象：`co-work-anl-boss11/research/current/unrelated_machines/normalized_weighted_menu_santa_value_and_size.md`。

最终全文SHA-256：`ce1c320ecd4d3833030307e4b4e3f4959ecd187281187c5914e80bddae8d13c5`。

**认证范围仅为§4–6的 `UM-NORMALIZED-XOS-THRESHOLD-MENU-SIZE-OBSTRUCTION-v2`。** 本轮实际全文读了组合上下文，但不认证§1–3的SC值桥；它是另一ID及另一独立审查任务。整文件hash只是精确标识本次读取的字节，不能把范围扩张到前一Claim。

顺序：先只据规模v2 Exact独立重构并冻结；随后首次读规模v2作者Proof并另冻read-after；本轮才实际读canonical，反馈一处非fatal精度措辞后又重新读修后全文。原Exact、Proof、独立及作者读后四份记录均保持原字节；审查者未改repo/Git/Work。

**最终结论：上述版本的§4–6有效，无standing fatal；与冻结规模Exact/Proof一致。**

## 精确核对

1. Domain仍是固定有理η∈(0,1)、t≥1、同U有2t项、非负有理finite explicit max，每clause全U总量恰1；允许零系数和重复indexed clauses。Unit量词是全部t-subsets，low量词是全部≤d-subsets，未缩成只看reachable bundles。
2. `d=floor(ηt)`、`k=max(1,ceil(d/η))`正确，保证0≤d<t及1≤k≤t。d0不错误用k0，t1原生给k1与K_min2；d≥1时support最小k的推导先排support≤d，再用top-d平均值，不假定uniform或单项≤1/t。
3. Finite max及norm1/nonnegative使unit T包含某clause整个正support。每clause任选k正项均匀化可不增K，保所有unit及low≤d/k≤η；只保两个阈值，不声称整个f逐集合不增。
4. `K_min=Θ(2t,t,k)`两向证明完整。Family方向明示为每个t集包含一个指定k集，不误用反向covering design。最小值有限、可满足；Θ不被当作poly可计算的oracle。
5. 每k-set覆盖t-sets恰C(2t−k,t−k)，计数比值下界正确；重叠及duplicate不帮助。Canonical没有把该比值说成一般参数皆可达到。
6. d0时singletons hitting全部t-sets等价complement≤t−1，精确t+1可达到。ηt为正整数时k=t，每T自身必须列入，精确中央二项式可达到。固定约分η分母的任意正倍数t满足该正整数条件；low使用≤允许d/t=η等号。
7. `t−k=floor({ηt}/η)≤ceil(1/η)−1`在d≥1时正确；余数<1处理了1/η整数边界。覆盖分母≤(2t)^c、中央项≥4^t/(2t+1)给式(6)，固定η才使c为常数。
8. 一玩家2t个1/t资源的显式长度O(t log(t+1))，输出至少K个indexed supports。固定η时超多项式输出成立；没有声称2^{Ω(source总位长)}、η变化时同一个固定c，或能poly求Θ/输出指数菜单。
9. §5附带的冗余全零clause删除只适用于外部表示额外添的零clause，其余非零部分仍满足norm1；零clause不改变非负max或unit覆盖。该说明没有将本ID扩大成任意subnormalized非零clauses域。
10. §6只否定同U逐玩家explicit norm1并保所有unit/tiny subsets的shortcut。辅助资源/玩家、全局耦合、仅可达分配保真、unit completeness损失、未归一化clauses及另证的implicit表示均明确排除于否定范围；与允许bonus资源的保OPT normalization不矛盾。
11. 对§3源义务的引用只说明一种接口不能直接使用，不因此证明整个SC值桥、SC hardness、UM近二NO或全局归约不可能。本规模证明不依赖SC值桥数值恒等式，也没有外部hardness、软件或有限实验前提。

## 本轮精度修正与实际字节确认

首次稿在整数锐端点中称uniform clause“任意d项和d/t=η”。若把U中support外零项也计入，这个逐clause恒等式不够准确；正确的是至多d项质量≤d/t，support内d项可以达到。

root已只将该短语改为“它们的均匀权clause在任意至多d项上的和至多d/t=η，取support内d项达到，故确实满足”。最终全文实际重读，改后恰为正确的≤条件及达到解释。将新短语回替旧短语可精确恢复首次canonical SHA-256 `42450690b6dc42cf8a40371071a890aa14e272ef6295c7853c4f1b9bb7fdfcad`，确认未夹带其它修改。冻结Exact/Proof不变，这不构成新的数学对象。

最终全文除正常LF外无ASCII控制字节。Pending导航/审查登记由root另处理，不影响本记录仅限数学§4–6的结论。

**最终冻结批准：所列hash的canonical §4–6规模v2通过；不扩张至§1–3、软件实现、外审或全球新颖性。**

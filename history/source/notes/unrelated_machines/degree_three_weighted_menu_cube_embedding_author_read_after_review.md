# 三组加权菜单嵌入零权立方体：作者 Proof 实际 read-after

审查者：general_query_response_review。2026-10-18。

读取顺序：先只据Exact独立推导并冻结审查，root实际读取后才授权本轮首次读取作者Proof；本文件单独记录实际read-after，不修改旧独立记录。尚未读取canonical最终稿。未读取其它agent论证，未修改repo/Work/Git。

冻结对象SHA-256：

- Exact：`b7cd715acf14005fdda54865a23d6d31a956b6f20a7cb19f211189cc154e76ef`
- 独立Exact-only审查：`b0cc7db624d4543d268df4bf2b7225686124e363d90c32ca98a0aafa6f6b54b4`
- 作者Proof：`2cd17f28206f45dcd29cb9407c98b06628d124e0ca4dc9944f9835d582c74fff`

**明确结论：作者Proof通过，无fatal；与先行独立重构一致。**

## 实际核对

1. **Slice和active格。** 组在某变量的incidence index为i时，state label也取i，slice为a_i=i。a*=(1,2,3)确实在每一个这样的slice内。Source degree≤3保证每变量的groups可取互异indices，原incidence的active格绝不缺失。
2. **全原job单射与资格。** 保留g/s/u原标识，原incidence对应其state、x_u的active-cell job，原p包括0直接复制。其仅有原private和active resource两个有限端，所有其它∞资格也保持。Missing原incidence对应的是新增aux job，不能与原zero job混淆；Proof明确区分。
3. **重复labelvector异cost。** 所有旧states仍各有private机和同一原selector的独立选项，所有states的incidence jobs都存在。Target允许state-indexed costs，因此相同labelvector不会把这些states合并。Proof没有暗用labelvector唯一决定cost或job身份的更窄模型。
4. **任意schedule扩展。** 每原job保原端，其余所有aux jobs放本state private零端；selected与unselected states一视同仁。原machine loads完全不变，aux资源idle，makespan恰原值。不要求源schedule最优或C<2，也不只处理全export见证。
5. **任意schedule投影。** Target可以把aux零private jobs导出到unit资源，Proof仍删除这些aux jobs后逐原job逆映。原jobs没有非active资源资格，所以不会有逆映失败。删jobs及aux机器只降负载；原unused active资源机是原machine像，应保留。完整原job每枚恰一次，原zero jobs不删。
6. **实际OPT与所有makespan阈值。** 双向schedule映射直接给实际OPT相等，含OPT=2；没有任何资源在C=2必须独占的错误假设。已成立的源实际makespan promise可转移，但不自动供应源promise、allocation hardness或额外收费/任务计数合同。
7. **Interaction exact。** 源有共同u则target共同active格；源无共同u则变量tag及dummy tags不交。两向都用完整U_g，包括零权membership；故group graph及M是精确相同，不是仅正supports图。每target格的groups至多其cube的三个incident groups，dummy至多1，unused cube可0；M不受固定Q=d=3限制。
8. **Strict-unit positive support。** Selector吃满所选private1，正jobs必须export、zero jobs可以留private。两个实例均有“选态正supports跨组不交 iff actual C≤1”的完整原job证明。Target positive support正是源positive support的active格像；全slice几何相交不产生额外正support约束。
9. **退化与计数。** q_g=0给仅该组dummy、U为空也可；unused源resources保完整27格及原active机。State private mass恰原W，K_g/S/selector数保留，resource数27(|U|+e)，incidence数9ΣK_g max(1,q_g)。每原job恰一个像，其余为零，不按有理数值复制。
10. **位复杂度。** max(1,q_g)≤max(1,|U|)，故补齐至全部group-union variables仍poly；没有3^{q_g}全局展开。Dense矩阵乘积及sparse对象数均poly，times仅原值复制或0/1/∞，tags/labels/maps为poly编码。扩展/投影也只扫描这些显式对象。
11. **Composition边界。** Proof只条件调用已命名bounded-interaction v2 positive theorem并代Delta=3、保同一M。本轮未重新审查该外部定理本身；embedding结构上没有新的调用障碍。任意M、固定K≥3的source gap未由此完成。
12. **Zero不可擅改positive。** Proof明确没有给all-positive perturbation。给aux cells正小质量会让selected state新增强制unit exports，破坏原严格unit可行性；相同labelvector且state-dependent cost的许可也不能悄悄撤销。没有不当global novelty、一般UM算法或hardness升级。

未发现Proof相对冻结Exact的范围漂移或需要修正的数学差异。此前独立审查字节重验不变。

**冻结判断：Exact与作者Proof有效；等待canonical实际全文read-after。**

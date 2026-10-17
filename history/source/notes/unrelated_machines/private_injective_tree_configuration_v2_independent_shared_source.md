# 私有注入树任意配置阈值 v2：新增陈述后的独立重构审查

审查对象：`/workspace/scratch/038d9dcc4cac/private_tree_configuration_floor_v2_exact_statement.md`，实核 SHA256 `ad33f6b2c42c184b943651e61437ece2d1372ee1445443017e62534d83487900`。

审查者：boss11 内部 shared_label_attack。实际来源：已知自己提出的 v1 hitting/Haxell 证明与旧配置正部多面体，也已知 typed CONFIG1。root给本v2只有Exact及其自称已有proof，未发送该proof；本审查未读root v2 proof、未读别的review、未给literal/cover摘要。新增B/C量词在读Exact后自行重构，不把整个v2称为零信息盲审。

## 结论

A、B、C目前均无 standing fatal。B确为单状态完整leafmap注入结构类的配置整数间隙上界；C只给承诺判定而非任意变参构造σ。没有将范围扩大到共享内部机器、非均匀父端权重或原非注入实例的CONFIG间隙。

## A：严格阈值配置等价

从CONFIG(1)取各state根的selector覆盖边际 λ_us。所有根概率和1。内部某机若incoming unit在配置中，就不能同时包含任何positive small；对任一out job父端覆盖概率≤1−q_in，因此其唯一unit下端边际t_e≥q_in。沿私有整树递推，每leaf下端边际≥λ_us，外机unit容量给共同λ资源行。

反向按λ：每内部机incoming singleton概率λ、全部d个small概率1−λ；每leaf外singleton概率λ；外机总概率≤1，用空配置补足，全部jobs覆盖恰1。这里A的等价本身其实不需要注入，但该更弱条件不支持后续B；保留Exact更窄假设没有错误。

## B：本机CONFIG拼成共同a-tree分布

固定T∈[1,2)、s=⌊d(T−1)⌋、a=d−s。取完整可行CONFIG分解。每机只有一个eligible incoming unit job，记其配置边际q；每out job在父端的覆盖边际x_e，唯一unit下端边际t_e=1−x_e。

每root按根selector边际λ选择state。若一个private节点已被生成树激活，且其实际生成概率p≤q，则从原本机CONFIG的“含incoming unit”条件分布抽一个配置C。该配置最多s个small，故至少a个outgoing jobs不在C；以固定次序从这些absent jobs选恰a个下传。按所选内部children递归。

若q=0则该节点p=0永不生成；不需要除0。对每out job，有

`Pr[该job被生成下传]`
`≤ (p/q) Pr_CONFIG[incoming∈C 且 outgoing∉C]`
`≤ Pr_CONFIG[outgoing∉C] = t_e`。

最后等式只用原job覆盖恰1及其只有父/唯一unit下端两种有限位置。因此递归始终保p_child≤q_child，对leaf也保生成边际≤原unit下端边际。各外资源的生成概率总和≤原外机CONFIG unit容量≤1。每root恰有一个state与一个满a叉高h生成树；每个实现都位于单个原state中，故全state叶单射保证其a^h个叶资源不同。

由此得到的**同一个全树联合分布**是v1所需共同分数见证；不是逐叶/逐资源另选分布。其支持可能指数大，本节仅作存在性，不声称能总位poly完整列举。

在每个生成a-tree内取r-pruned subtree，叶hitting阈值(a−r+1)^h、resource edge rank r^h。v1的同一Haxell论证给每root一个共同匹配r-tree。映回原d叉机仍只留d−r个small，实际全P负载2−r/d；所有未选state及分枝父置，负载1。

取r=⌊(a+2)/3⌋=ceil(a/3)，有(a−r+1)^h≥2r^h−1。又a=d−s，故

`2−r/d ≤ 2−a/(3d) = 5/3+s/(3d) ≤ (5/3)(1+s/d) ≤ (5/3)T`。

全部不等方向及等号s0/d1均成立。T≥2时全部port父置、每selector任选根，selected根负载2，其他内部1，外机0；实际C≤2。T<1因selector unit不可覆盖而不可行。

## CONFIG的多项式正部系统

此附属复杂度声明可自足核对：变量incoming q（根为λ，其余为parent t）、每out down边际t_e∈[0,1]；每节点需

`Σ_out max(0,q−t_e) ≤ s q`。

每max引入一个非负变量z_e≥q−t_e即可线性化；外机Σleaf t≤1，根Σstate λ=1，全部规模O(显式jobs+machines)。必要性是incoming分支至多s个small。充分性：held small边际x_e=1−t_e，incoming分支放α_e=max(0,q−t_e)，outside分支放x_e−α_e；前者除q在均匀matroid rank-s多面体内，后者除1−q在cube内，分别有有限配置分解。q=0/1直接退化处理。无需指数列举配置来判可行。

系数s的bit长O(logd)，d个原out jobs已显式，不以binary数值展开作伪多项式。固定T的floor精确有理可算。未从此判定LP推断Haxell匹配能变参poly构造。

## C：过滤后的严格承诺判定

若原实际OPT≤1，则每root selector所在state的每个outgoing small都必须下传，归纳整state全部leaf外送。每外机C≤1只容一unit，故这个state本身f单射，且各root实际选中的完整state bundles全局互异。它们给过滤后λ LP一个整点，所以空菜单或LP infeasible都保证原OPT>1。

若LP feasible，则对保留state用v1给实际C≤5/3；被过滤state原selector未放在此，全部port/edge父置，不给其内部任何unit incoming，全部机器负载1。原机器/jobs没有真的删除，所以保证针对原P。

非注入原P的CONFIG(1)仍可能可行但过滤LP infeasible；C没有把它们的配置间隙上界改成5/3。承诺边界NO为严格>5/3，等于5/3在中间带；YES=OPT≤1包含等号。

## 限制与未做事项

- 没读root新proof，没有运行新物理代码；此前22个小树hitting穷举、8000组取整核验只检查v1有限实现，不作为本v2一般证明。
- Haxell外部定理及其primary适用核对沿v1；未认证原创或独立成文价值。
- 没有给任意d,h的σ构造多项式算法。固定d,h枚举本地strong witnesses的推论可另记，但不混入本v2算法scope。
- 真正剩余主方向必须超出此uniform-private结构合同，或明确处理没有同一单状态注入/共同分数点的其它对象。

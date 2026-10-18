# 仿射线逐tuple/globaldummy：最终 canonical 范围实读审查 v1

审查者：rank_deficiency_fee，2026-10-18。完整实际读取正式current及修正后字节，另冻本记录；未修改repo、Work、Git或任何原冻结文件。

## 1. 精确读取对象与修正链

正式ID：`UM-AFFINE-LINE-TUPLE-GROUP-GLOBAL-DUMMY-ESCAPE-v1`。

实际全文读取canonical：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/affine_line_tuple_groups_global_dummy_compilation_escape.md`。

第一次实际全文读取的draft wholeSHA：

`22c9377c33b1167827d3d89636d91820de94808fe9ded724273f6768bb162f36`。

当时发现§5 dense条目公式在机器数与jobs数之间误写逗号，已报root。Root改为显式 `\cdot` 后，本审查者**重新实际全文读取**，最终wholeSHA：

`edc0c8437260085bfcb408099f724306531a88b360d27811b0a8e70762fc2c65`。

以新文件字节仅将唯一的

    [n(d+1)+vR^2+d]\cdot n(D+d+1).

逆替换为原逗号版本并在内存回算，SHA恰恢复draft的22c9377c…2f36，确认只有这一处排版变化。没有在scratch重写旧canonical或修改原statement/Proof。**本次最终认证绑定修正后的edc0c843…c2c65字节。**

## 2. 原始路由与证据边界

先行独立Exact-first输入是root的完整消息陈述和旧current前27行source定义，正式statement当时尚未创建；不倒称其先读正式文件。独立记录已先冻结：

* `affine_line_tuple_groups_global_dummy_rank_exact_first_review_v1.md`，SHA `e8eed1514605e6f39a277172efd4a3e4b9bbed4e139810a292e7d3d04d6c0a14`。

Root实际读后才正式冻结statement/作者Proof，随后本审查者才全文读取并另冻作者读后：

* `affine_line_tuple_groups_global_dummy_statement_v1.md`，SHA `bfaea112b1c005cd64a32233170cf3ffb27db9cd41cdb2e150f29a8002f567b6`。
* `affine_line_tuple_groups_global_dummy_proof_v1.md`，SHA `9f1b98b2446cdeb4eb5877328ab0fdf9d07314bc8aec6017de08c489f988a804`。
* `affine_line_tuple_groups_global_dummy_rank_author_read_after_v1.md`，SHA `e830e7e47eb94e9d0e83bd1b9c429be1dbb5a2e58ae05d355a44e0d2189e9ccc`。

上述原件hash已重新核对、未变。本次只认证本canonical的自足实际编译合同及范围，不另行重审外部论文完整困难性证明或全球新颖性。

## 3. 最终完整数学核查

**完整域和P。** PrimeR≥2、k≥1、每relation含k个不同变量、variable-degree≤R、incidence注入、变量资源tag分离；allowed表可空。n数tuples，m₀数非空relations，1≤q≤m₀，d=n−q，D=kR。Tuple分别作独立group，menu为一个原D-set及d个globaldummy singleton；同一dummy由全部groups共享。每state独立private，selector1，incidence private1/D或1/resource1，其余∞；全部未选state jobs均存在，无预载。域内n≥1，每原job有finite端、机器数正，state质量严格1。

**不求源解的半保留finder。** 只选q个不同非空relations、每表第一tuple；剩余d个groups与d个dummy双射。不要求源赋值/packing/OPT见证。任意选中子族F中r_x≤R且intercepts不同，lines不重合、两两交≤1，故union≥r_xR−C(r_x,2)≥r_x(R+1)/2。按tag求和得每个Hall子族|N(F)|≥k(R+1)|F|/2≥ceil(kR/2)|F|。OddD、空F和r_x=0均有效。整数matching/flow给每组b=ceil(D/2)枚共同不交真实资源；没有对全部tuple groups滥用degree，也没有只核全体union。

**全部原jobs共同actual输出。** Selected原state只外送b件，其余D−b件留private；selecteddummy外送唯一job；其它所有states的全部incidences留各自private。Selected原private负载2−b/D，selecteddummy private仅selector1，unselectedprivate质量1，全部真实资源至多一unit。每原job恰一次、各机在同一分配中同时受控，得到≤2−ceil(kR/2)/(kR)≤3/2。

**Unit双向覆盖任意实际调度。** Fullset packing≥q可选这q个原states、其余dummy双射，selected全导出、unselected全private，给完整unit。反向任意actual≤1中selector已占private1，selected state每件private时间正故全部导出；资源unit使selecteddummy至多d、selectedreal至少q，提取其完整原sets不交。Unselected exports只多占资源，不破坏提取；未先假设正规调度。Selector也给OPT≥1。Unit等价没有变成≤3/2算法的unit判定承诺。

**q=n及空表。** q=n时d0且m₀=n、每非空表一tuple，所有groups选real，原Hall/actual/unit论证不依赖dummy存在、无除零。空relations不生成groups，不改变注入；m₀仅作本域与选择计数，不把原source归一化分母从|G|改成m₀，不把near-perfect YES变perfect YES。m₀0或q>m₀域外，完整归约若需要须另证合法分支。

**Counts与位多项式。** Private n(d+1)，resource vR²+d，jobs n(D+d+1)，finite n(2D+3d+1)；dense已修为明确乘积 `[n(d+1)+vR²+d]·n(D+d+1)`。原时间1/D位长O(logD)，选择/line枚举/qD边flow/dummy双射/全部原job输出均按完整显式总编码位长多项式，qb≤qD≤nD。没有枚举源assignments或Hall子族，没有按分母数值额外展开；不称succinct poly(logR)生成vR²资源，固定sourcek,R才直接为其source-polynomial。

## 4. 与旧D的关系和最终结论

旧constraint-as-group分析当时明确不排tuple另成groups的不同compiler，因为不能自动在全部tuples上保degree/line不重合。本新页针对明确d=n−q全局dummy数量及q≤m₀的选择规则，独立恢复了需要的q个relation子族，关闭的是这一具体编译；与旧D的历史范围并不矛盾。

认证**不**扩成所有tuple-group、所有globaldummy、任意dummy数量、非uniform权、不同source阈值或真实sharedguard机制的失败定理。外部整set困难性不能替代partial soundness，本文也未证明fullset packing易解。没有near2主反面、一般UM算法、新软件/有限实验或新matching理论结论。

在最终wholeSHA `edc0c8437260085bfcb408099f724306531a88b360d27811b0a8e70762fc2c65`下，canonical全文与正式statement/Proof及先行独立重构一致，发现的dense排版错误已修，未发现standing fatal objection。正式认证本明示compiler的完整actual半保留及unit双向合同；UM-TARGET-v1仍OPEN。

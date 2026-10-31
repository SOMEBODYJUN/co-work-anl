# LST affine-line uniform compiler：Proof 实际 read-after 审查

对象：`lst2025_affine_line_source_uniform_menu_compilation_proof_v1.md`。

Proof SHA-256：`e9ca11c2975bc8509681619857e772bb0086a489dc9c56a8cb9b1833a08c1e3b`，已实际全文读取并核验。

对应 Exact SHA-256：`a1334a82f1acf7fd9562c2d44e6620b84b5a1acd37993ce3c7131b81a8e56472`。

先前 Exact-only 记录 `lst2025_affine_line_uniform_compilation_independent_review.md` 的 SHA-256 仍为 `3576492af3ca5e319a888cca805897a850472ad3dca00cc80d1e647bddff6ffd`，本次复核确认未改原字节。读取次序确为先独立推导与 primary 核读，再冻结 Exact-only，最后经 root 授权实际读取作者 Proof。另存本记录，不覆盖旧记录。

**判定：作者 Proof 通过，无 standing fatal。** 认证范围仅为 constraint-as-group、allowed-tuple-as-state、所有菜单非空、uniform private weights 的冻结 compiler。不能将其 3/2 上界套到 tuple-as-group 加 dummy 的另一种 compiler。

## 1. §1–2：任意 local tuples 与全部 Hall 子集

Proof 一开始固定任意完整 local state 选择，又固定任意 group 子族 F，不利用全局一致 assignment。r_x 按当前子族中包含 x 的 indexed constraints 数计，满足 r_x≤R；既不按 states 数计，也不把 constraint 内重复变量当多次 incidence。

不同 constraints 的 j_x(g) 注入确保同一变量的 selected lines 不重合：同 slope 则 intercept 不同而平行不交，异 slope 则 prime field 中唯一交点。故 pairwise overlap≤1。Proof 没有只证明异 slope，也没有漏同 slope 时的 identical-line 风险。

二阶容斥的方向正确，多线 concurrent 不破坏它：r_x 条 R 点线给 union≥r_xR-binomial(r_x,2)≥r_x(R+1)/2。变量 tags 允许跨 x 直接求和；每 group 恰 k 个不同变量给 Σ_x r_x=k|F|。再用

    ceil(kR/2)≤kR/2+1/2≤k(R+1)/2

得到**所有** F 的 |N(F)|≥ceil(kR/2)|F|。空 F、r_x=0、k=1、R=2、kR odd 的 ceiling 都覆盖。没有用全 pool 总量冒充局部 Hall。

Proof 使用 capacitated Hall / integer maxflow 正当。等价地，把每 group 展开 b=ceil(kR/2) 个相同邻域 clones，任意 clone 子集所触 groups 为 F，邻域≥b|F|≥clone 数，普通 Hall 即覆盖全部 clones。合并后每 B_g 恰 b 个真实资源且跨组不交。group→resource capacity 1 与 resource→sink capacity 1 相容，没有 fractional owner 或强制 per-line/product 份额。

## 2. §3：全部原 jobs 的 actual schedule

每 selector 放固定 selected state，只有该 state 的 B_g incidences 导出；**所有**其它原 incidence 都留自己 private，包括每个未选 indexed state。各原 job 恰执行一次并保原资格。

resource 负载≤1，未选 private=1，选中 private=1+(kR-b)/(kR)≤3/2。选中负载≥1，故控制全部机器。G 非空给 OPT≥1，因此 absolute bound 同时给此结构类的 ratio≤3/2。

Proof 没有把 partial resource allocation 当成完整 schedule，也没有把 full original matrix 缩成 selected-state jobs。逐机串行即可输出精确有理起止时刻，不需要其它调度假设。

## 3. §4：真正 perfect witness 与 primary YES 的区别

若另给全满足的 CSP assignment，同变量各 selected lines slope 相同、incidence intercept 不同，故平行不交；不同变量 tags 也分离，因此全 selected sets 不交，可全部导出而 OPT=1。

Proof 明确把此 perfect witness 与 primary 仅 val≥1-ε 的 YES promise 区分，没有把 near-perfect 免费强化为 perfect。unconditional 3/2 也不依赖 YES，故 full-set matching soundness 不能直接成为当前 partial compiler 的 near-two NO。

NP⊄BPP 的 complexity 限制保持，没有换成较弱的 P≠NP。此前本审查实际核读的是 arXiv v1 在线 primary PDF；root 后来另行下载/亲读的本地 raw PDF 属于 root 的实际操作，本记录不冒称本审查下载或核过该本地 raw 文件。

## 4. §5：空关系和不同 grouping 不被混淆

A_g=∅ 时保留 selector 会无 eligible state，Proof 正确声明该输入在合同外。删除 constraints、增加 dummy 或其它 recoding 必须另证 source/target 合同，没有在这里静默补空菜单。

Proof 新明确指出：若每 allowed tuple 自成一个 group，再加全局 dummy choices，则同一原 constraint/incidence index 可贡献多个 selected lines；同变量的 tuple-group 数可超过 R，相同 slope/intercept 还可能形成完全相同的 lines。当前 r_x≤R 与 pairwise overlap≤1 不能直接沿用。因此**不排除或认证**该不同 compiler，不能给它引用这里的 3/2。

同样不覆盖非 uniform 权、变量 tag 合并、额外 jobs、一致性 gadgets 或所有 source-to-UM reductions。这个范围收口正确，并未否定原 k-dimensional matching hardness。

## 5. §6：显式位复杂度与来源角色

R,k 的数值展开已计入真实 resources 和 incidence jobs。L=kRa、m selectors、a private machines、vR² resources，以及全部 finite entries/原 jobs 都在 Exact 中明确。给定 explicit tuple tables 与 j_x，line 枚举、selected group-resource flow 与全部 job identifiers 输出均按该显式总位长多项式。

b≤kR，若以 clones 实现，其总量 mb≤mkR≤kRa=L，因为非空菜单给 a≥m；若用 capacities 则无需 clone。没有更大隐藏数值复制，也没有偷称 polynomial in log R 的 succinct 编译。先前 Exact-only 的 counts 及 bit bounds 未被 Proof 改换。

primary 只提供实际 full-set source、affine-line/degree 参数与 stated hardness；容斥、ceiling、Hall 和全部 job 回填是既有基础事实的应用。Proof 未包装成新主定理或一般 UM 改善/困难性。

## 6. 冻结结论与下一步范围

**Proof read-after 通过，旧独立记录原字节保持。** 未实施软件或有限枚举，未修改 repo、Work 或 Git。尚未读取 root canonical；未来组合若增加 source/direct-dummy compiler、其它 grouping 或其它数值结论，需按其实际文本另审，不能凭本记录自动认证。

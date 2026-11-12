# MinRep 泛域条件边的独立 3D 数学审查

结论：可采用当前 canonical 边 `um-129516aa-minrep-source-and-sparsification-pay-conditional-parameter-repair`，保持 `accepted / transfers / ALL / conditional / whole_result`。目标整条是“原显示参数行的缺口，以及在同一已实现正规源上的完整条件修复”，不是对任意预定 R 的无条件联合源存在性。本轮独立重算后没有发现需要正式 repair 的数学缺步。可清本报告指定的三个对象及这一条边的当前 pending；其余 pending 和 archive 整体 pending 不由本报告清除。本报告是 3D 采用依据，不是新 3A 包、收据或 done。

## 精确审查对象和现行绑定

只读 clone：`/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1`。首次记录 HEAD 为 `178626ed726b767033d61e2dedf6573a6634d288`；2026-11-12 17:46:49 UTC 末次对象/边/收据复验时 HEAD 已因父 Boss 工作推进为 `f81f40e9a4cdf633bd388403ca4d8325f2e454c4`，下表三端点和本边字节未变。

| 角色 | 对象 | 版本 | 当前 registration_pin |
|---|---|---:|---|
| MZ 源 | `M-9a7614916cf04cee8915aefce74b502a` | 4 | `12f2b0b849e6a0e259a911875357e454172c3f94fd8c1ceea54deb6526c25b84` |
| 保 N 稀疏化 | `M-8c360a7779154480879e38c65d1f827e` | 1 | `3dd4454f24e6ace08f116048d88ada39f73596fb57ae251b1d7b61568079281d` |
| 参数审查目标 | `M-fb633f3a6f1448fbbd63bfc7c3806c40` | 1 | `fdb940f4d9c1ac5bffffa7b4e6b2317975a6ace432efab15cb0b8dc480350364` |

现行边路径 `map/edges/boss5-mz-visual-repair-3c1fe8fa00844a15/source-and-sparsification-conditional-repair.json`；文件 SHA256 为 `a2bbdc8edaedb3c5c1c1ae1cdf595b796af41ba709ac9692ec2f520c41676605`，规范 JSON semantic pin 为 `09a5812accc8c96b9eafcea7bb9e535df3a976a078f473441fc070892e71b619`。它仍列于 registry.edge_files，integration 的本边 pin 与现行 semantic pin 一致。

现行任务 `boss5-mz-visual-repair-3c1fe8fa00844a15` 是 done、owner Boss5，当前任务文件 SHA256 `7c6927e7883975fcb05dafdd0f8a82d668658ae27c5f433177df72c103f86d29`。独立 receipt 文件 SHA256 `1adb68925dc316f0def048e6c293bdf7951febbd95f460cc2ee422a9eb395a81`，semantic pin `64e4ba979e642e81b7710c0aa95ea67009eef2c0d98f7f0d80a4a9d5f8fd96c8`；与任务嵌入 receipt 完全相同。三条当前 asset 字节均匹配本 receipt，所有端点 body/evidence 实际 SHA 仍 current。逐文件结果见 `current-bindings.json`；未运行全仓哈希或全仓科学程序。

## 实际读取与复用范围

实际读 AGENTS.md、prompts/03-map-worker.md、IMPLEMENTATION 第三阶段和定向替代规则；用 `research_runtime.load(..., verify=False)` 取得结构，只对本范围引用核实际字节。完整读取三端点登记陈述、量词、域、假设、objections 和 refs；两份中文正文承重实读为 MinRep 页的模型、§3–4.5 全部稀疏化证明和 §7.2，以及“四对一与字母表”页的 MZ §3。未将正文声称的历史 PDF 全读算成本次新读。

完整读取现行 3c1f task/receipt/edge，及被其替代的 a850 task definition、旧 receipt、旧条件边、当前原路径 review 全文。当前 reading-ledger 的 current_reading/current_corrections/independent_math_checks/limits 已读；historical_reading 仅作旧引用和阅读范围追溯，不声称逐项重新执行其旧阅读。旧条件边 SHA `53eaa72900ff29f21594683ae5e3083bed58fe245284560ecfb66d0f28ccf37e` 的全部有效数学保在现行边；旧 review/ledger 的同路径替换有现行 receipt 明确 disposition。

为区分联合存在性和泛域条件接口，完整读 e7d9 task 的定义与 done/owner、其独立 receipt、当前 canonical 三输入 ALL 边，以及 `map/edges/boss2-mz-joint-source-3b-7d327f911a777dc3/joint-source-proof.md` 全文（SHA `59c4ade2f67ca482de8fb89e95c9fb5b2ad46469fb5a95c33edce1a42ba191fa`）。本次不把该三输入证明偷偷并入被审两输入边，也不以此重审它所复用的全部内层 primary 或整数度桥。

本次从冻结原件重新抽取并实际读 MZ 印 2、3、18、59、60、61 页，Manurangsi 印 4、5、6 页；新渲染并逐图看 MZ 印 18、60、61 页。MZ 原件 SHA `13b8eb55f86cfe28ac8b283fe83612889b335e14b7a87d64d479451693c7dff4`；Manurangsi 原件 SHA `259edd7e850da816ddb5c318287a7a3a525ccc8963f07918787156384d7153d8`。所需 primary 正文已在 clone，未额外 web 搜索。复用已准确固定的 MZ 主定理/Lemma6.1 内层及其外部 Rao 重复定理接口，不重证 106 页论文。未核 FMW primary、Alon expander 算法、连通性具体费用模型、simple 源版本或 UM/SPE compiler；这些都不是本边完整条件句的未付证明步骤。

## 原显示行、完整条件和源量词

MZ 印 60 页 Lemma7.12 的 YES 结论确为 `(1+εd)N`；印 61 页取 `δ=1/g` 和 `γ₀=R^{-(1-η)}=2^-11 g^-2` 后，直接写 `MinRep≤2N`。固定 `0<η<1` 时，这个特定关系给

\[
R=(2^{11}g^2)^{1/(1-\eta)},\quad
d_0=10^6\,2\ln(2R)/\sqrt{\gamma_0}=\Theta(g\ln g),\quad
\delta d_0=\Theta(\ln g).
\]

因此所引引理只提供 `(1+Θ(ln g))N` 上界；这一上界不蕴含显示的 `2N`。此诊断限原参数关系，不能对任意独立 R 都声称 d 是 Θ(g ln g)。它是证明行的缺口，不是 MinRep 最优成本的反例，更不否定 PCP 主定理或 Theorem7.13 的真值。印 60 页 NO 前提是严格 `val<γ`，印 61 页源承诺却为 `val≤γ₀`，所以同阈值直接代入还缺严格性。

MZ Definition1.1 的 alphabet 参数是左右大小之和；Theorem1.3 是先固定 ε、τ，再取充分大 R。故不能仅据该显示定理，在任一事先预定 R 上事后把误差任改为 `1/d(R,Γ)`。现行边正确要求：g、整数 alphabet size R 先固定并独立于 SAT 输入规模；YES/NO gap、正规性与共同字母表必须由同一联合选择实现。小 R 的条件若无 NO 实例，是条件分支为空，不是源存在性已被证明。

被审边的两个 source 以 ALL 使用：MZ 提供实际 source/原应用行和双正规接口，稀疏化提供有意义域的完整随机合同。源联合存在性为显式条件；该条件下的关系证明已经完整，所以 accepted/conditional 正确，无须降为 proposed，也无需将其数学条件标成 needs-decision。

## 正规化、字母表、N 与约束身份

对已经实现所需联合 gap 的正度 `(d₁,d₂)`-biregular 多重约束源，设原记录数 M。每个左点作 d₁ 份、右点作 d₂ 份；每条原 constraint-ID 放到其端点全部 copy pairs，沿用其自身投影。两侧点数分别 `|A|d₁=M` 和 `|B|d₂=M`，故新 N=2M；每个新点记录度 `d₁d₂`，每条原记录复制同倍数 `d₁d₂`。

原赋值复制给新图，给新 val≥旧 val。反向固定任意新赋值，独立均匀抽每个原点的一份 clone 标签；每条旧边的期望满足率恰是其 copy pairs 上的满足比例。所有原 ID 复制倍数相同，期望总满足比例等于新赋值比例，故旧 val≥新 val。二向合得精确保值。这是显式多项式构造（最多 O(M³) 条记录），没有为每次复制另添概率或加法误差。它不声称 MinRep 成本按原 N 保持；后续稀疏化只以正规化后的 N 为基准。

共同字母表取带类型不交并 `Σ=Σ_L⊔Σ_R`，大小 Q=R。合法左标签照原投影；错型左标签先缩回固定合法左标签 l₀。所有像仍是合法右类型；错型右标签换回任一合法 r₀ 不会丢失原已满足边，错型左标签缩回 l₀ 不改变投影输出。原合法赋值仍可用，所以 val 精确保留且投影为全函数。没有要求投影满射或等原像数。

以上和下述证明都按 constraint-ID 计度、采样、覆盖；同端点同投影、同端点不同投影都不去重。重数不改变列表族只由 `V×Σ` 决定的计数。

## 保 N 稀疏化的独立复核

以 γ 表示通用阈值，`0<γ<1`，正度 regular 输入有两侧各 n 点、N=2n、Dn 条记录，预算 `Δ=10^6·2ln(2Q)/√γ>10000`。

当 `D≤Δ` 直出原图。近完美单标签先付 N，对每条未满足记录至多补两个标签，成本 `≤N+2εDn≤(1+εΔ)N`；NO 的原图便宜列表覆盖率界已直接排全覆盖。此分支不做提升度数的 blowup，所以保持此输入 N。

当 `D>Δ`，每条 ID 以 `p=10^-4Δ/D` 独立采样。只按中间度 `>Δ` 标记一次并删其全部关联记录，孤点保留；因此每个 seed 的最大度界确定成立。条件于一条记录已被选中，任一端点中间度期望 `<1+pD`，高度概率 `<1/Δ+pD/Δ<0.0002`。对两端作 union bound，删边总数 Z 满足

\[
\mathbb EZ\le0.0004pDn,\qquad
\Pr[Z>0.1pDn]\le0.004<0.01.
\]

此处尺度必须是 pDn，旧印 pΔn 不能沿用；平行记录独立采样下条件期望仍为 `1+p(D-1)`。

若 `val<γ`、`cost(ψ)≤a=0.06N/√γ`，以 `L=0.3/√γ` 切 heavy/light。heavy 点严格少于 `0.4n`，故触及记录严格少于 `0.4Dn`。若 ψ 覆盖至少 `0.5Dn`，就有严格多于 `0.1Dn` 条 light-covered 记录；各点独立从非空列表取标签，任一见证对被取中概率至少 `1/L²=γ/0.09>10γ`。期望满足记录严格多于 γDn，矛盾。因此每份便宜列表在原图留严格超过一半记录未覆盖。列表空时不可能见证覆盖边，不影响论证。

固定列表的未覆盖采样数 Y 有均值 `μ>0.5x`，`x=pDn`。取 `s=ln(2.5)` 的二项 MGF 得

\[
\Pr[Y<0.2x]\le
\exp[-(0.3-0.2\ln2.5)x]
\le\exp[-10^{-5}\Delta n]
=(2Q)^{-10N/\sqrt\gamma},
\]

因为 `0.3-0.2ln2.5≈0.11674185>0.1`。这独立支付所需最终指数，不依赖原印缺半因子的普通 Chernoff 中间式。

令 t=floor(a)。全投影非空源有 `val≥1/Q`，所以 NO 下 `Q>1/γ`，从而 `a<NQ`。成本恰 t 的列表族有 `binom(NQ,t)` 份；t≥1 时用 `(eNQ/u)^u` 单调性及
`0.06ln(eQ√γ/0.06)≤0.5ln(2Q)`，给计数至多 `(2Q)^(0.5N/√γ)`；t=0 仅一份全空列表。上述计数与固定列表 MGF 作 union bound，以 `>0.99` 概率同时留下每份成本 t 列表至少 `0.2pDn` 条未覆盖中间记录。与同一个 `Z≤0.1pDn` 事件联合，以 `≥0.98` 概率最终每份此类列表仍留正数未覆盖记录。更小列表可补到成本 t，覆盖单调；成本为整数故这正是排除全部 cost≤a 列表。于是 NO 好事件针对输出后任意自适应 cheap list 同时成立，并保证好 NO 输出非空。

YES 固定一份满足率≥1−ε的单标签 φ。未满足记录采样数期望 `≤εpDn=0.00005εΔN`。先付 N，再每条存留未满足记录补至多两个标签；Markov 以失败概率至多 0.0001 保成本 `≤(1+εΔ)N`。这证明所需≥0.9。近完美源不能升级成每 seed 的完美 singleton 源；只有原本 perfect-complete 输入在纯删边时保同一 singleton。

## Γ、严格 gap、概率和预算

在同一个已正规源上，取

\[
\gamma_0=2^{-11}g^{-2},\quad
\Gamma=5\gamma_0/4=5/(8192g^2),\quad
d=10^6\,2\ln(2R)/\sqrt\Gamma,\quad 0<\delta\le1/d.
\]

g>1 给 `0<Γ<1`；`val_NO≤γ₀<Γ` 严格满足稀疏化前提。代 `Q=R, ε=δ, γ=Γ, Δ=d`，YES 以≥0.9 成本 `≤(1+δd)N≤2N`，NO 以≥0.9 同时排全部成本 `≤0.06N/√Γ` 列表。又

\[
\left(\frac{0.03}{g\sqrt\Gamma}\right)^2
=0.03^2\,8192/5=1.47456>1,
\]

所以 NO 成本严格 `>0.06N/√Γ>2gN`。两项概率各对相应固定 promise 输入成立；不是在同一实例同时要求 YES、NO，更不是把每份列表单独的高概率误合成统一事件。每 seed 度界独立于这两个随机成功事件。随机归约限定保留。

原实阈值 d 的合同与整数预算实现必须区分。若取整数预算 Δ̂≥d，实际采样和 trimming 用 Δ̂，并重新在同一源上取 `δ≤1/Δ̂`（或保守 `≤1/(2Δ̂)`）；沿用仅 `δ≤1/d` 不足以自动给 `(1+δΔ̂)N≤2N`。可先算 d 的固定可编码上界再上取整使 `d≤Δ̂≤d+2`，故渐近阶不变。现行泛域边没有把此整数输出界误写成精确≤d；e7d9 的特定构造明确只声称每 seed≤Δ̂。

若同一参数族另有 `R=O(g^(2+ε′))`，则 `d=O(g ln g)`。逐项代入得到

\[
d^3R=O(g^{5+\varepsilon'}\ln^3g),\quad
d^4=O(g^4\ln^4g).
\]

对充分大 g，第二个上界可吸收到前一个上界；保留 Theorem7.11 自身输入合同后，只可直接得到 rooted k 的粗界 `O(g^(5+ε′)ln³g)`。原印同 ε′ 下只留 ln g 不由这些上界推出。若预留较小指数以吸收对数，是另一次参数安排，不是同指数直接算术。本报告不补外部费用模型。

## v4 实际改版与 e7d9 的不同域

读取现行 `source-correction.json`，旧中文 body SHA 为 `6d5be138de6825a1208776cbb485316c5b0e9d197870e32ab7c1d8ca5cf2f746`，现为 `d0273adacbf4ccbb9d6cd954cdfd44dddb5f8a8e969067107f63c77bdaaf4b78`。结合旧条件边的完整文字、当前段落和本次新渲染印18页，可确认这次实际数学 delta 是撤回“重复次数倒置”的抽取误诊；原 PDF 确写正确商数 `k/ceil(q^r/β)`。没有把旧完整 body 的不可见历史字节冒称本次逐字 diff。

保留的事件勘误是正确的：原句“Ui=Vi 或 Ui≠Vi 且 advice 全零”概率为 `1−β+βq^-r`；改成后半“并非全零”才是 `1−βq^-r`，其补事件是可暴露坐标。一般 `m=ceil(q^r/β)` 不整除 k 时，令 `t=floor(k/m)`，忽略末尾独立坐标给 `val(G^k)≤val((G^m)^t)`；`k≥2m` 时 `t≥βk/(4q^r)`，外层指数保持。在 e7d9 的实际 q=2 清分母格点上，`k=2^A, β=2^-B, m=2^(r+B)`，充分大 ℓ 保 `A−B−r=(2c/3)ℓ−r` 非负整数，故实际 m|k。此处不是该构造新的缺步，也不增加对源完备误差的依赖。对本泛域条件边而言，联合源本已是输入条件，更不需要额外用此段承诺源存在。

e7d9 当前已 done、owner Boss5；其 canonical 边 `boss5-mz-joint-source-and-sparsification-close-minrep-parameters` 文件 SHA `c3e4dbcb1b4427dd1ef133f463da66d78c5c16a1cbcc9de7cb07f9f319406f56`。其三个 ALL 输入另含整数度舍入桥，对任意固定 ε′、充分大固定 g 构造特定 Q(g)，按 q/ℓ/Q/预算先定再取 η、支付删除/舍入误差，闭合同一正规源。此成熟联合源不应继续称为“尚未有人证明”或挂新同题 follow-up。

但这个存在性只覆盖充分大 g 的特定 Q(g) 及其整数预算，不覆盖现行两输入边对任意固定 g>1、R≥2 的所有已实现源。因此保留泛域 conditional whole 有独立准确用途，不能把三输入 unconditional 边拆掉正规化输入后当成同一条关系，也不能据特定构造退休泛域条件定理。当前 receipt 的旧 follow-up 已落实为 e7d9 done；无需新 follow-up 或抢 owner。

## 可以清除与必须保留的 pending

本次可采用的精确 delta 为三个当前对象 `M-9a7614916cf04cee8915aefce74b502a`、`M-8c360a7779154480879e38c65d1f827e`、`M-fb633f3a6f1448fbbd63bfc7c3806c40`，以及当前 canonical 的 `um-129516aa-minrep-source-and-sparsification-pay-conditional-parameter-repair`。所清理由是上面逐项数学与 exact current bindings，非 native PASS；对象采用只指各自准确合同及本次比较范围，不为别的 incident 边补审信用。

保留其余所有 pending object/edge，以及 `archives/unrelated-machines` archive 整体 pending。本报告不独立清 `PCP-EXACT-PROJECTION-PERFECT-COMPLETE-BIREGULAR-ROUNDING-v1`，不清 FMW 共享 body 下其它对象或其新超图边，也不清其它 BLMRS、MMO、AFS 等并发变化。e7d9 已存在的成熟 done 范围可按原有效审读采用，本报告只是完整读它来判域，不以这次窄核冒充其全部原始证据的新独立复证。

泛域中“源须已在同一选择实现”的数学条件继续保留；任意预定 R 的存在性未被本边声称，因而既不是本边推导缺步，也不是身份 needs-decision。近完美与 perfect、单位成本与任意权重、全覆盖与 partial-MinRep、记录图与 simple 图、原 N 与正规化 N 的边界全部继续保留。无新 repair 请求；若未来需外部 expander/常数中间度或具体连通性费用合同，应按实际新问题另定位承接，不能作为本边待清工作的虚设阻碍。

末次复验：本报告所审三端点 registration pins、全部实际 body/evidence SHA、边物理 SHA/semantic pin、done 任务及 receipt 与资产 SHA 全 current；本边仍 canonical。完整可机读结果与当时未清 pending 原表均写在 `current-bindings.json`。整个审查没有 Git 写、队列、sync/checkpoint、source/registry/edge/receipt 修改或科学程序重跑。

交付前再次复验（2026-11-12T17:49:26.634470+00:00，HEAD `013e6e5f6574b9ee1afb2f8f2ce3b8a7329f4967`）：上述全部已读文件字节、三端点、canonical 及 done 状态仍一致，逐项结果全部通过；父 Boss 同期其它写入不在本审查采用范围。

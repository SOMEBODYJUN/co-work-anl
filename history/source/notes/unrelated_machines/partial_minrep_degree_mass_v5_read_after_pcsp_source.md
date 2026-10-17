# 度数质量复制正规化 v5：作者冻结证明读后攻击

审查者 pcsp_occurrence。实际完整读取作者 `degree_mass_copy_regularization_v5_root_frozen_proof.md`，读前、读后 SHA256 均为 `e2e60ca49cb6fcaf14a865a83c1d537d3213eb01a8d60c1e1f6baa1054b86c29`；绑定 v5 Exact `86dcd98daaa2cc479260e444f47f4e9eb3d8ae56936b220f0a1d18e82863d693`。本稿是读后攻击，不称盲审。

本人的先前真正 Exact-first 一般重构：v4 非空子域稿 SHA `36950255eaf5df611e01440082a13fec02a353841d408a876741e982f14fbe63`；收到 parent 转述另一审查者的 formal 空字母表 objection 后，v5 修复域核对稿 SHA `cb9baf54a78c86ffb2fb344934f4f23a1583a90725436b51dc7523048d398f11`。全部旧冻结文件原字节保留，不将他人的 formal objection 或作者 proof 冒作本人的先验独立发现。

结论：在 v5 精确非空 typed 对象域内，逐段与本人独立重构一致，无 standing fatal。以下列出本次实际读后的核验，而非只引用旧结论。

## 1. 模板、质量和 arbitrary copy lists

作者§1每侧Σ_v t_v=zM₀、N′=2zM₀、M′=dzM₀=dN′/2正确。输入 degree 可以不界、两侧原点数可以不同；每个 copy 每层1边的性质不依赖原 degree。same type/layer bucket 长度固定 z，与异长 fiber 不冲突。

§2承重归一化正确：随机均匀原 edge 的一侧 endpoint-copy 分布，在该侧每个 copy 的概率为 d_v/M₀·1/(d_vz)=1/(M₀z)=2/N′。这里是“每侧”概率，不应再错误地对全部 copies 的2/N′求和；作者接下来的 union 计算实际等价于 heavy 命中≤2h/N′≤2g/H，常数正确。

每原点独立抽 copy再抽 typed label 是实际旧单标签赋值，val≤γ可用。非空修复在空list任取合法label处确被使用。light-covered pair 满足概率≥H^(−2)，所以平均 p_e≤τ/2+16τ/1000<τ。未要求原点lists预算，也未把不相同的copylists无损合并。每 type 重复 dz次使均值μ=dzΣp_e<τM′。

## 2. 异长 permutations、typed 计数和统一 tail

§3逐 permutation 的点态 e^j 密度界对任意长度 t_v 都同样成立；不同对象长度不相同不影响总2k slots的乘积界。参照模型中模板边使用不交 slots，事件独立，factorial moments 与 Chernoff 逐行有效。μ=0和实数阈值已分别覆盖。

各 copy 的真实 labels 按其侧的显式 alphabet计数，bit positions数≤QN′，所以 K≤exp(gN′λ)。这里不会把左右不同 labels识别为同一符号，也不新增标签。≥250gN′λ的负指数抵掉全部 copy lists计数，得到的是同时性，不是固定lists保证。

## 3. 不同 fiber 的 cycle 条件与 repair

§4必须在最后一步闭合到起始原 v时用1/(t_v−G)，作者做到了。simple prefix与相邻layer不同保证最后当前copy及初始copy的该层边均未揭；已揭slots对template mate封闭保证新mate fresh。若原mate vertex不同则闭合概率0，否则 fresh image在至少t_v−G个未用编号中uniform。没有默认不同原纤维同样大，也没有假设最后原type均匀。

按原v求和t_v/(t_v−G)≤2N₀，因此 B₀=40N₀S确实控制cycle FAIL，不需扩大到40N′S。这与本人独立稿完全相符；长度2为不同层的parallel pair，已被计数。

§5同bucket f的禁点计数只依赖输出degree d，不依赖原degree。z的余量、四端不同、不新生短cycles、≤B₀次终止及每份listscovered增量≤2B₀均正确。M′=zm*≥8B₀/ρ将 repair 统一误差压至ρM′/4。保持type正是保fiber/surjectivity的原因，未使用“反向全函数”错误。

## 4. capped sampling、位复杂度和 source corollary

K₀=dΣ_v(t_v−1)>0，真实draw数、独立bit blocks与条件成功后的exact uniform分布正确。sampling FAIL≤.0005，cycleFAIL≤.05，NO同时性再扣<.001，保守.8结论成立。不是对所有非FAIL输出保证NO。

Qγ域支付数值g、1/ρ、d；N₀≤2M₀，t_v≤M₀z及固定G使显式规模、最坏时间、随机位硬界均多项式。typed alphabets与投影表显式列举，所以Q计入输入长度。原PCP无需constant-degree、biregular或两侧等大，由度数质量正规化直接接任意显式非空game。

§6同步label clone正确，但须明确它是显式source alphabet语义：新labels是原labels与实际tag s的pairs，π'_e(α,s)=(π_e(α),s)完整读取并输出tag。每个不同(α,s)都是独立计费的列表符号；所有后续Q、λ、d均按这个新输入重算。不能把s当作隐藏 routealias、忽略其列表成本或声称π看不见它。

value保持的两向证明正确：丢tag将每条新满足边投影为旧满足边，给val_new≤val_old；旧最优赋值统一取同一个tag给反向≥。每右(β,s)恰有原k_fiber个前像，equalfibers与surjectivity保持。无需为此先把typed alphabets retract到同一集合；那样的普通padding会改变fiber数，本稿未犯此错。主变换本身不新增labels；若选择本预处理，那就是另一个明确给出的新source实例。

固定g、ρ、G时fixed-error PCP alphabet虽可以很大但仍为常数，clone数及degree d亦为常数；这不推出一般4to1 PCP有Q=poly(g)。作者末句保留这一区分。第5项作为条件应用不需要本变换重新证明PCP。本人曾实际读取新ECCC primary Theorem1.6的陈述，此次未重新审原文证明，不能冒作该外部定理认证。

## 5. 与旧版本的状态边界

v4字面域曾允许空字母表而val不良定，不能追认其全域通过；v5明确两侧非空才是本次接受对象。旧稿仅对非空域的推导保留。此 formal修复由parent转述另一审查者指出，作者proof也明确登记。

无生产软件实现、无有限实验、无全球新颖性或UMcompiler认证。source随机归约给NP⊄BPP下的条件困难性用途，不升为仅P≠NP下确定性hardness；UM-TARGET-v1正反面均保持OPEN。最终：v5作者冻结proof读后攻击无 standing fatal。

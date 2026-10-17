# 度数质量复制正规化 v5：非空域修复后的 Exact-first 回执

内部审查者 pcsp_occurrence。实际完整读取 v5 Exact，读前/后 SHA256 为 `86dcd98daaa2cc479260e444f47f4e9eb3d8ae56936b220f0a1d18e82863d693`；实际 diff v4/v5，差异只有 Claim ID、修复说明、显式要求两侧 alphabet 非空。算法、参数、输出、概率与位复杂度合同未改。

此前只据 v4 Exact 独立重构的稿已先冻结，SHA256 `36950255eaf5df611e01440082a13fec02a353841d408a876741e982f14fbe63`。收到 parent 新消息前，该稿的结论明确限于通常非空投影游戏域，§8也写了非空的规范化建议；但其“非致命建议”措辞不能取代对 v4 字面对象域的正式否定。parent 随后转述：另一审查者抓到 v4 正式对象域缺口，允许空 Σ_A 会使 val 不良定，并已另冻 v5 修复。这里把该正式 objection 和修复来源如实记给 parent 所转述的另一审查者，不冒称该 formal objection 是我本次独立发现。

正确状态：v4 的字面完整域不获接受；旧稿仅证明其非空子域。原稿保字节。v5 显式修复后的全部对象域正好落入旧稿实际推导范围，故下列一般数学均无 standing fatal：

1. copies 总质量 N′=2M₀z、每侧 M₀z，输出 exact d-regular；任意原 degree 和两侧点数不平衡均允许。
2. 任意 cheap copy lists 的 heavy 端质量以 d_v/t_v=1/z 抵消，得到平均 p_e<τ；不同 copies 可完全不同，不假定原 cheap-list 预算。
3. 变长 permutations 仍逐对象有 e^j 点态界；factorial moments 给全部 lists 同时 tail。typed alphabet 的总 bit positions≤QN′，不需要混成共同域。
4. cycle 闭合概率用每个起始 v 的1/(t_v−G)；求和Σ_v t_v/(t_v−G)≤2N₀，所以 EX≤2N₀S，B₀ 合法。后续 same-type/layer repair 不生短环，任意 lists covered 统一增量≤2B₀。
5. K₀=dΣ_v(t_v−1)>0，bounded sampling 条件成功后精确 uniform；FAIL 和总位复杂度满足合同。固定 G、Qγ 域均不可删除。
6. 同步 label clone (α,s)→(π(α),s) 精确保 value、surjectivity、exact k fibers。clone 后 λ/d须按新 Q 重算；固定参数 PCP 与统一显式变换的位复杂度不能混写。一般 fixed-error 4-to1 PCP 未自动得到 Q=poly(g)，只有另给该量化条件时才有 d=Oρ(g)。

到本回执冻结为止，未读 v4/v5 的作者 proof，未读取或互传其他审查者的证明；仅收到 parent 转述的空字母表 formal objection。旧 v3 技术先验已在较早稿披露。无代码、无有限实验、无新颖性认证、无 UM compiler。接受对象为 v5 修复后的 Exact；UM-TARGET-v1 保持 OPEN。现可给作者冻结 proof 作读后攻击。

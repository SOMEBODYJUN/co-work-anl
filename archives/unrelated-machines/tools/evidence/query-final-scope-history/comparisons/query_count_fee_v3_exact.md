# 一般双见证中合格查询的数量与费用：冻结Exact v3

ID: UM-TWO-WITNESS-QUERY-COUNT-FEE-v3。
v1内部候选的η=0“严格超过d”错误由独立审查指出；本v2单列零质量情形，不改其原审查记录。

Domain/Quantifiers: UM-TWO-WITNESS-QUERY-SEPARATION-v2相同的任意一般P、两个实际σ0σ1≤有理T，但这里要求T>0。非空Q⊆D，d=|Q|。β∈[3/2,2)有理，c=β−1。采用该v2正文的固定I>T/2阈值染色算法所得同一族Aq、τq，任意非负改派权w，W=ΣD\Q w。令LQ_i=Σ_{q∈Q:σ0q=i}p_iq，Rβ=#{i:LQ_i>cT}。

Exact Statement: 可det bitpoly识别至少d−Rβ个query的集合G，所有q∈G有Cmax(τq)≤βT。若Rβ<d，则G非空且某q∈G费用≤W/(d−Rβ)。此为已有同族输出的筛选，不重新染色或假设新的全局调度。

Further uniform-individual bound: 若每个query的初态单件处理时间p_sigma0q,q≤ηT，其中有理0≤η<c，则：
(1) η=0时Rβ=0，全部d个query合格，至少一fee≤W/d；不声称“严格多于d”。
(2) 0<η<c时，严格多于(1−η/c)d个query合格（整数至少floor((1−η/c)d)+1），至少一fee≤W/[(1−η/c)d]。
(3) η>0时另令s=floor(c/η)+1≥2，则Rβ≤floor(d/s)，合格数至少d−floor(d/s)，至少一fee≤W/[d−floor(d/s)]。特别至少ceil(d/2)个合格。所有式子允许W=0，不把fee的≤改成不当严格<。

Fee consequence: 若每个合法单query模式在峰≤βT都被某物理编译合同要求非query改派费≥F>0，则W≥(d−Rβ)F；(3)域内进一步W≥[d−floor(d/s)]F。因此单件tiny查询即使同机聚合接近T，也不能免费共享一次激活费；对应费仅σ0→σ1改派/新增unit费，背景费、退款、其它收费另计。

No claim: 不给一般UM算法或近二困难性，不需要也不计算未知σ，两个T实际见证是输入。仅筛选singletons，非全子集cube。没有global novelty认证。


v3新增结论（由typed独立审查者先提出）: 不加统一η假设，令H=#{q∈Q:p_sigma0(q),q>(β−1)T}，S=d−H。则同族中至少ceil(S/2)个query合格，故W≥ceil(S/2)F。若F>0且全改变的对应费用W≤κF（给有理κ≥0），则H≥d−2floorκ。特别W≤F时至少d−2枚query初态时间严格大于(β−1)T；β=2−ε时几乎全部读取必须初态>(1−ε)T。这是改派费合同的必要条件，不是全局UM困难性，允许结论平凡或单query不可行；不额外声称充分性。

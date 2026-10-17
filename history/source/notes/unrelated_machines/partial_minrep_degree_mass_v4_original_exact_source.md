# 度数比例复制的任意投影源正规化：精确陈述，无证明

读取目的：只给独立审查者精确对象和合同，不给作者证明。Candidate ID `UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v4`。root 已自推证明，不把 root 称为盲审；尚未 canonical，不升级 UM-TARGET。

## Objects / Domain / Quantifiers

固定整数 G≥2。输入任意非空有限无权 bipartite multigraph Π=(A,B,E)，M₀=|E|≥1，删除孤点后 N₀=|A|+|B|；不要求两侧等大小、不要求正规或最大度有常数界。每条边 e=(a,b) 给显式全投影 π_e:Σ_A→Σ_B，两个字母表明确列举、Q=max(|Σ_A|,|Σ_B|)≥2；不要求共同域，不加新labels。平行边逐type计。val是单标签赋值满足的原边比例。各点列表可空，cost为全部列表大小之和。

给binary整数g≥2、binary有理0<ρ≤1，令

ℓ=floorlog₂g，λ=1+ceillog₂Q，τ=ρ/(100g²)，γ=ρ³/(10⁹g⁸)，d=ceil(1000gλ/(ρℓ))。

显式域要求 Qγ≥1。G固定；不声称binary G变参时统一poly。

S=Σ_{j=2}^G d^j，B₀=40N₀S，U=Σ_{j=0}^{G+1}d^j，m*=dM₀，

z=ceil max{2G+1, G B₀+4U+1, 8B₀/(ρm*)}。

每个原非孤点v建立 t_v=deg_Π(v)·z 个copies和同数slots，将slots按其incident original edge types分成每组z个；每type两端组slotwise配对，形成全部左右slots上的perfect matching模板。独立建d层；每个原v每层独立抽uniform[t_v] permutation将slots重命名至v的copies。每edge保留original type及layer，任一(type,layer) bucket总为z条matching边。

令N′=Σ_v t_v=2M₀z、M′=dM₀z=dN′/2。实际Fisher–Yates integer draws数K₀=dΣ_v(t_v−1)>0。每uniform integer draw以range的ceil-log₂公平位拒绝采样，至多R=ceil log₂(2000K₀)次；任一耗尽返回FAIL。计初始union长度2..G simple cycles（parallel两边算2cycle，单边往返不计）；若X>B₀返回FAIL。否则每次选短cycle边e=(a,b)，在同(originaltype,layer) bucket找f=(c,d)不在任何短cycle且两端均距e任一端>G，换ab,cd为ad,cb。按显式顶点/edge-type字典序确定选择规则。

## Exact Conclusions

1. 每次需要的f必存在，修复≤B₀次终止，不产生新长度≤G cycles。每个seed返回FAIL或显式simple、balanced、exact dregular、girth>G的投影游戏，保留各type的原投影表。因此原每边任何equal-fiber/surjective属性原样保持；不混写成强连通全函数反向投影。
2. 若val(Π)=1，每个非FAIL输出由原标签复制得到全满足；若val(Π)≤γ，至少0.8概率返回非FAIL输出，且对**所有**cost≤gN′的copy列表，同时covered<ρM′。同一原点copies可用不同列表，原点预算不要求按deg加权；输出预算就是全部真实copies的总大小。
3. 所有域内输入FAIL概率<0.1。FAIL是flag，不是假的girth源；归约caller可按YES处理。没有宣称每个非FAIL都是NO好事件。
4. 对固定G，最坏运行时间、输出规模和硬随机位数关于全部显式输入及binaryg,ρ总位长多项式；Qγ域用于数值复杂度。原degrees可以随输入增长，t_v与菜单无关，本定理不构造UM矩阵。
5. 若有任意固定误差perfect-complete常数字母表exact k-to1（固定k）投影PCP，取误差≤γ并接此变换，即得常数字母表、simple、balanced、constant exact degree及固定高girth的随机source family，同时保exact k fibers。可同步复制字母表标签作(α,s)→(π_e(α),s)以进入Qγ≥1合法域，value不变且k fibers不变。此项不要求原PCP constant degree、biregular或两侧等大小。若输入alphabet Q=poly_ρ(g)，则d=O_ρ(g)；一般fixed-errorPCP未声称该定量alphabet界。

## Scope / Assumptions / Status

这是随机源正规化，确定性promise判别器只导出NP⊆BPP；不伪称P≠NP足够，也不是UM困难性。新4-to1 primary theorem可作为第5项的Paper Fact，须另核原文，不能给本陈述内部概率证明投票替代。未写代码/未跑有限实验/未认证新颖性；冻结后先独立重构再读proof。

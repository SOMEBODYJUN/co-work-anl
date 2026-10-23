# 精确命题身份（个人区）

## ROOT-ONLY-REPAIR-3-v1

- Objects/domain/quantifiers：每个原CAG-MODEL实例、每个m>=2、每个完整纯计划tau，其在每个正深度子局已为SPE；根A不必最优。全部有序历史、重复/空主题、任意历史平局保留。
- Definition：u为实际根收益，d_B为按原tau完整后继的真实根偏离收益，Delta=max_B d_B−u>=0。给定有理s>=Delta且s>0。
- Conclusion：存在同m单位提供者、合法新共同Cartesian目录的完整纯SPE，旧坐标实际路径不变；W_new=W_old+(m+1)s、OPT_new=OPT_old+(2m−1)s、gap_new=gap_old−3s。有理账面数共同整数缩放成单位客户。Delta=0时旧计划已经SPE，无需修复。
- Dependencies：分支后独立Cartesian收益可加，H/L_X/L_Y/leaf-BI完整续局，最优组合可按位置同时配对。
- Evidence/status：自足一般证明及作者Fraction联合全树核验；independent/insurer_blind_review.md独立盲重构与定义级回放未发现致命异议。内部解析可靠，未外审/未认证新颖性；非Q-CAG-HALF解答。
- Related：compiler/padded_insurer_{statement,repair}.md、audit_padded_insurer.py/.json、independent/insurer_blind_*。

## ROBUST-ROOT-ONLY-3-EQUIV-v1

原Q-CAG-HALF（对所有共同目录，固定任意m>=2）等价于：每个上述root-only计划均满足OPT_old<=2W_old+3Delta。正向对Delta>0应用ROOT-ONLY-REPAIR-3-v1、取s=Delta并清分母；Delta=0直接用原命题。反向在完整SPE取Delta=0。该等价不证明任一边；当前状态OPEN等价重述，不冒充新half机制。

## 其他待独立审查对象

compiler/disjoint_insurer_three_sharp.md（准确架构三系数锐下界）、shared_omission/credible_degree_two_negative_flux.md（真实完整SPE无条件驻留负flux）各以正文量词为准，审查未完成时保持作者结果身份。

## DISJOINT-INSURER-DILUTION-3-v1

- Domain：每个m>=2，所有合法主题共同含K，去K后不同极大花瓣两两不交，任意内部子主题；固定同一根A，任意两份完整后继SPE。
- Definition/conclusion：高/低首人收益差delta>0，高分支福利W_H，同保险OPT_m=O，则2W_H−O>=|K|+3delta；每个m都有达到3delta的空核例。任意fixed-root后继分支另有2W−O>=0，允许任意多独立此类坐标异号求和得到修复成本>=3Delta。
- Status：作者一般证明、independent/insurer_three_sharp_review.md独立内部解析攻击及Fraction复核通过；不含根可遗漏的极大共同核，不含根以下跨坐标耦合。无外审/新颖性认证。

## DEG2-CREDIBLE-NEG-FLUX-v1

- Domain：q>=2、m=q+1、2q极大主题，两等组；每条跨组边b>=1单位客户、同组边整数0<=a<=b单位客户；完整全历史纯SPE。
- Conclusion/evidence：存在正文明确SPE，根L=theta=qb/2+(q−1)a、各后继H=(q−1/2)b+(q−1)a/2、均匀驻留根尾差−(q−1)(b−a)/2，W=OPT。a>0,q>=3时另有最优比较集共享遗漏D=G=a*binom(q−1,2)>0。
- Status：full_depth/degree_two_review.md独立解析审查通过；已修正1–1平局取最近动作组，代码原本正确。仅否定无条件根尾平均支付，根不严格低于theta。无外审/新颖性认证。

## STATIC-CROWDING-DOMINATION-v1

任意incidence、任意合法背景、r=q+1个剩余者和同一完整SPE的真实强制极大根菜单。h_x=max_{i∈I_x}K_i(x)。若q个整数合法静态槽p使c_p(x)>=h_x，则theta_r(b)<=max_i d_i<=u。degree2为顶点多重覆盖。root独立通分和单位客户核对通过（parent/static_crowding_review.md）。普遍存在这样的p已经被K5三人真实SPE需求C5、覆盖成本3>q2否定；一般half/degree2 theta仍OPEN。

## POPULATION-DELETION-ALL-v1

每个m>=2取偶t>=4、d>=1、整数0<epsilon<t/2，L=d+(m+1)t/2+epsilon；m个不交L块Ai及从各块取t并含d私有的T。全部m人完整SPE实际各Ai一次，W=OPT=mL，联合U；每个1<=s<m全部SPE均根T后fresh不同块，故全部覆盖U外私有。任意历史/重复均保留。security/population_review.md独立内部解析审查通过。新增是统一全人数/全部较少人数/原均衡最优范围，不认领首次否定固定人数联合删除。

## SECURITY-OPT-REAL-TAIL-GAP-v1

每个m>=2，复用旧两core稀有叶静态实例，存在指定安全最优均匀叶p*，对每份完整SPE及每个强制根a，其m−1真实尾列B(a)满足F_p*(B(a))>=v_m+m/[4(m+1)]。同族每个真实历史下当前及未来SPE行动者收益>=v_m，OPT_m=3m²。independent/strict_tail_review.md独立内部审查通过。存在指定p*不扩大为任意p*；尾列不含根，未否定Mfull或聚合安全值。无外审/新颖性认证。

## 仍开放/仅观察

B2两步安全债务非负仍OPEN；有限诊断及固定p,Q策略锥未命中不作一般证据。祖先cap reset递推是精确集合值BI的带条件重述，不能自动形成福利机制。所有Finite JSON范围见各正文，均非计算证明原half。

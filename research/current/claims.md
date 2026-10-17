# 现行命题登记：前提、结论、依赖与状态

## 2026-10-09 独立顺序客户吸引模型

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| CA-EXACT-PURE-SPE-ALL | 有限共同主题目录、单位权提供者依次观察完整历史、单位客户均分；整数重数代表单位 clones，全部历史依赖纯 SPE。 | 集合值逆归纳精确返回每个 prefix 的全部可实现终局计数，并为每个终局重构完整有序历史策略；不涵盖混合行为 SPE，不声称位多项式。 | [完整必要/充分归纳](customer_attraction/exact_solver.md)、独立完整策略枚举及规范实现；外审未记录。 |
| CA-SPE-NON-PNE | 同一 CAG-MODEL；存在两人四客户共同目录或另一个三人三客户实例。 | 完整纯 SPE 的终局可有盈利的静态单方行动偏离。反驳 SPE→PNE 桥梁；不反驳半覆盖。 | [两人证书与导入边界](customer_attraction/literature.md)、[三人证书](customer_attraction/continuation_lemmas.md)；直接证明及独立精确审计，外审未记录。 |
| CA-HISTORY-TIES | 同一 CAG-MODEL；三人、两个不交 unit singleton 主题。 | 存在完整纯 SPE 在同计数历史 AB/BA 选不同回复，且收益 (1/2,1,1/2)；两个收益次序单调方向都不普遍成立。 | [完整策略与逐节点证明](customer_attraction/continuation_lemmas.md)；直接证明及独立精确审计，外审未记录。 |
| CA-RESIDUAL-NO | 同一 CAG-MODEL；两人、五共同主题、十四名单位客户。 | 完整纯 SPE 收益 (4,5)、W=9、OPT=10，最大未覆盖主题大小 5；逐人 u_i≥M(C) 和聚合 W≥mM(C) 均错误；2W≥OPT 未被否定。 | [完整收益表、失败机制和证书](customer_attraction/continuation_lemmas.md)；独立展开客户审计及规范 verifier 均通过，外审未记录。 |
| CA-TWO-REMAINING-TAX | CAG-MODEL 的任意合法固定有序前缀，恰两位剩余单位提供者，任意完整历史依赖纯 SPE 和任意两个比较主题。 | R_b(T,S)≤R_b(A,B)+Σ_{x∈A}1/((b_x+1)(b_x+2))；只算剩余两人收益，非零背景时不等于完整覆盖。b=0重构文献3/2；首步桥和一般背景总税已否定；一般根总税亦由CA-ROOT-TAX-NO否定。 | [非负恒等式完整证明和条件性归纳](customer_attraction/two_remaining_tax.md)，独立逐客户精确审计；不声称新颖或外审。 |
| CA-PORTFOLIO-MATCHING-NO | CAG-MODEL 的两人、五共同主题、86名单位客户实例；唯一最优两主题支持。 | 完整 SPE W=44、OPT=45、最优遗漏42；真实偏离收益矩阵 ((19,19),(22,22)) 两种匹配均为41；不存在另一个最优组合修复。只否定匹配收费，不否定半覆盖。 | [完整策略、唯一最优性及矩阵](customer_attraction/portfolio_matching_counterexample.md)，独立定义级审计与规范核验；外审未记录。 |

| CA-THREE-UPPER-142-81 | CAG-MODEL，恰三名单位提供者、任意共同有限目录和全部完整历史依赖纯 SPE。 | OPT_3≤(142/81)W；零覆盖亦成立；不声称锐性或四人以上上界。 | [三个合法 slack 与非负恒等式](customer_attraction/three_player_bound.md)，独立逐段重构与 Fraction 审计；完整内部证明，外审/新颖性未认证。 |
| CA-TAX-BRIDGE-NO | CAG-MODEL，空背景、三人、四主题、十五名单位客户。 | 完整 SPE BBB，W=9、OPT=15；F3=15>u1+tau(B)+F2(B)=29/2。只否定首步机会成本桥；本例根总税恰等号。 | [弱占优完整策略及全部最优分类](customer_attraction/tax_bridge_counterexample.md)，独立全历史真实偏离核验；外审未记录。 |
| CA-GENERAL-TAX-NO | CAG-MODEL 的合法非零背景、四剩余人；反例位于完整七人根 SPE 的实际到达前缀 AAA。 | A7/B1/C1不交；实际剩余利润4、总税3/4，F4=24/5，差1/20。一般背景总税为假；不否定空背景总税或根半覆盖。 | [九客户反例、无限族及同主题根边界](customer_attraction/general_tax_counterexample.md)，独立完整子树与根树精确审计；外审未记录。 |
| CA-STRATEGY-CONE | 固定m≥1、p≥1共同主题标签，允许相同覆盖；任意单位客户整数类型重数与完整有序历史策略。 | 每策略SPE重数是有理锥；W=1截面紧，固定(m,p)最坏比例由有理极点缩放成整数客户达到；精确对偶可认证固定锥。 | [完整证明与Farkas符号](customer_attraction/strategy_cone.md)，小规模全策略接口回归；有限多锥攻击不证明主目标。 |

| CA-COVERAGE-OPPORTUNITY-NO | CAG-MODEL，三人、五共同主题、十一单位客户的完整纯 SPE，实际路径AAB。 | 在轨第二步δ=F2(A)−F1(A)=3>u2=5/2；逐层覆盖机会支付为假。Σδ=OPT−W仍为恒等式，全局余额及半覆盖未被否定。 | [完整31历史策略、收益表与望远镜余额](customer_attraction/coverage_opportunity_counterexample.md)，独立155真实行动比较精确审计；外审未记录。 |
| CA-PREFIX-BALANCE-NO | CAG-MODEL，每个整数n≥4存在n+2共同主题、2n²−2n−2单位客户及完整有序历史纯SPE；F为含原覆盖的最优总覆盖补全。 | 实际路径AB^(n−1)，u1=n−1/n、W=n²−2、OPT=2n²−2n−2、F_(n−1)(A)=OPT−2(n−2)，B1=4−n−1/n<0；每个固定实数α<2均存在该族实例使αu1+F_(n−1)(A)<OPT。根税和半覆盖余额严格为正。 | [全历史/Jensen完整解析证明](customer_attraction/prefix_balance_family.md)、[22客户四人完整策略证书](customer_attraction/prefix_balance_counterexample.md)，两路独立代数审查及互不导入精确审计；有限n4…8不替代普遍证明，外审未记录。 |

| CA-FOUR-UPPER-1499-750 | CAG-MODEL，恰四名单位提供者、任意有限共同目录、每个完整历史依赖纯 SPE。 | OPT_4≤(1499/750)W；零覆盖亦成立，保留所有平局、重复及空主题；未证锐性，五人以上仍开放。 | [真实根偏离续局与完整非负恒等式](customer_attraction/four_player_bound.md)，独立逐段审查及两份 Fraction 审计；完整内部证明，外审/新颖性未认证。 |
| CA-LAST-NODE-OPT-TAX | CAG-MODEL，任意人数m≥1；任意终局，只要求末位在实际前缀后最佳回复。 | OPT_m≤m u_m+τ_0(c_{<m})。末位收益≤平均则根税成立；税反例必须末位超过平均；非充分条件，不解决一般目标。 | [税页§6的直接逐客户证明](customer_attraction/two_remaining_tax.md)；内部复核，外审未记录。 |
| CA-THREE-SHARP-5-3 | CAG-MODEL，恰三名单位提供者、任意有限共同目录，每个完整历史依赖纯 SPE。 | OPT_3≤(5/3)W；三个互不交主题的完整SPE下界达到，三人最坏比例恰5/3；该锐界定理仅给三人范围。 | [真实L_i/Q/R回复、八类合法slack及完整非负恒等式](customer_attraction/three_player_sharp.md)；两路独立审查、Fraction全2048membership/160角点及完整下界审计；外审、新颖性未认证。 |

| CA-DISJOINT-MAXIMA-2M1 | CAG-MODEL，任意m≥1；删除共同核心K后，不同包含极大花瓣两两不交，内部子花瓣允许交叠。 | 每个完整历史纯SPE在每个历史选极大花瓣；OPT_m≤C+(2−1/m)(W−C)，锐。包含laminar目录；一般交叠极大目录不涵盖。 | [自足singleton重构、真实扩张续局及结构化简](customer_attraction/disjoint_maxima_bound.md)，独立内部审查和完整策略精确枚举；外审/新颖性未认证。 |
| CA-UNIFORM-PORTFOLIO-TWO | CAG-MODEL任意合法固定背景，恰两剩余玩家，每个完整历史纯SPE，任意比较T,S及其真实回复Q,R。 | 2R_d(T,S)≤R_d(A,B)+V1T+V1S+V2T+V2S；允许全部平局。任意人数的平均偏离界仍是未证义务。 | [四合法末节点slack、非负多项式及符号背景恒等式](customer_attraction/global_new_uniform_portfolio_two.md)，独立重构与Fraction审计；外审未记录。 |
| CA-FIVE-LIFT-ROWS-NO | 五人两条根偏离路径的明确460行必要条件松弛，非负有理13主题membership和辅助O，W=1。 | 23mask精确可行点有O>2W，故这些行不能单独证明O≤2W；O不是真实OPT，未给完整策略，不是主猜想反例。 | [完整变量、460行及证书边界](customer_attraction/five_player_lift_obstruction.md)，独立逐行重构与精确审计；外审未记录。 |
| CA-CREDIBLE-CONTINUATIONS | 固定CAG整数单位客户实例、可实现目标终局和完整有序历史；固定人数/标签数的策略锥。 | 可信孩子菜单覆盖全部完整SPE；均匀模式有限全支持。联合MILP只生成候选，M=m有严格证明；两项所选锥比例8/5、7/5不涵盖全部策略。 | [递归菜单及联合候选接口](customer_attraction/credible_continuations.md)，两棵781节点完整策略、整数原始及精确最优对偶审计，12路径接口回归；外审未记录。 |

| CA-LAST-TWO-FLOOR | CAG-MODEL，任意完整有序历史，恰两人剩余；任意非负整数背景。 | 两人实际收益各≥局部θ(P)，且最大化 f_p 的主题对所有真实末位最佳回应均保证该值；合法长度n−2背景时≥全局θ_n。 | [完整配对势差证明](customer_attraction/last_two_floor.md)，独立定义级全策略及恒等式审计；外审/新颖性未认证。 |
| CA-ALL-N-WELFARE-4N | CAG-MODEL，任意n≥2和每个完整历史纯SPE，单位均分、共同有限非空目录。 | W≥4(n−1)OPT_n/[n(2n−1)]；三人8/15、四人3/7均弱于现行结论；不解决五人以上半覆盖，不声称锐性。 | [末两人保底与K/n的完整合并](customer_attraction/last_two_floor.md)，精确内部审计；外审未记录。 |
| CA-LAST-FLOOR-ALL-PLAYERS-NO | CAG-MODEL，四人、十二主题、正整数类型重数代表不同单位客户，给定完整纯SPE。 | θ=6135346>u1=6135345；否定所有玩家u_i≥θ的辅助断言。W=24541476、OPT4=24541532，未反驳主目标。 | [上传工具比较、保存策略与定义级独立审计](customer_attraction/uploaded_tool_audit.md)，全部1885有序历史及完整偏离验证；外审未记录。 |

| CA-MOBIUS-BOOLEAN | p≥1、任意有理Boolean子集势F且F(∅)=0；有符号客户类型仅为辅助代数。 | 双Möbius反演唯一实现F的harmonic势；重复计数扩张因而被唯一固定。非负反演加正整数清分母恰为单位客户实现条件；不编译任意匿名收益表。 | [完整唯一性、整数边界及count约束](customer_attraction/mobius_compiler.md)，两路独立内部审查与精确审计；全球优先权未认证。 |
| CA-MOBIUS-FULL-HISTORY-EMBED | 上行子集边际收益游戏，p≥n≥1；清分母所得整数x，K=4Σ|x|+1。 | 正整数类型x+K给合法共同目录unit CAG；每个完整SPE在所有含重复的历史都选未用标签；合法无重复历史的SPE限制、根终局和有序路径精确对应。 | [fresh/old严格优势与全历史扩展证明](customer_attraction/mobius_compiler.md)，独立量词攻击和完整策略投影审计；不保福利比。 |
| CA-MOBIUS-BIAS-BARRIER | 上行安全大偏置编译器，M=Σ|x|、C=2^p−2^(p−n)。 | 根SPE和OPT各用n个不同标签；2W−OPT≥KC−3M>0，n≥5甚至OPT/W<125/123。因此安全编译器自身不能反驳半覆盖；小偏置另需完整策略核验。 | [统一覆盖偏置及严格代数边界](customer_attraction/mobius_compiler.md)，独立内部审查；不限制一般目录主目标。 |
| CA-THREE-REMAINING-PROFIT-5-3 | CAG-MODEL，任意合法固定有序背景，恰三人剩余，任意完整历史依赖纯SPE。 | F3(b)≤(5/3)R_b(实际后三人)，作为全部背景的统一常数锐；R_b为剩余总利润，非背景总覆盖。另有末三人精确组合接口及OPT_m≤(5m/9)V+Σb/(b+1)。 | [真实Li/Q/R'回复、非负二次系数完整恒等式](customer_attraction/three_remaining_profit_bound.md)，独立从2048原membership重构与两份精确审计；未证五人根半覆盖。 |
| CA-FOUR-REMAINING-PROFIT-1499-750 | CAG-MODEL，任意合法固定有序背景，恰四人剩余，任意完整历史依赖纯SPE。 | F4(b)≤(1499/750)R_b(实际后四人)，包含全部平局、重复和空主题；不声称锐性。R_b为剩余总利润，另有末四人精确组合接口及OPT_m≤(1499m/3000)V4+Σb/(b+1)。 | [真实D/Q/R/S节点、背景聚合校正和128类非负三次系数完整恒等式](customer_attraction/four_remaining_profit_bound.md)，两份互不导入的精确审计与独立正文审读；未证五人根半覆盖。 |

主目标 [Q-CAG-HALF](../questions/customer_attraction_half_coverage.md) 仍开放。
本分支的客户固定均分，不使用原设施模型的客户 NE 或因子 2 存在性。


| CA-SUNFLOWER-MAXIMA-2M1 | CAG-MODEL，任意n≥1；不同极大覆盖为C加两两不交私有花瓣，全部内部子主题与完整历史平局任意。 | OPT_n≤|C|+(2−1/n)(W−|C|)，锐；包含任意至多两个不同极大主题目录。不声称终局PNE或每步极大。 | [superset席位归纳与精确席位计数](customer_attraction/sunflower_maxima_bound.md)，独立内部重构及精确审计；外审/新颖性未认证。 |
| CA-MAXIMA-SUPERSET-SEATS | CAG-MODEL任意目录、n≥1；全历史SPE；每主题归属一个包含它的极大主题。 | f_j(k)=w_j/k+v_j/n第n大席位ν给每人u_i≥ν、W≥nν；任意前缀的剩余席位条件给逐人保底。任意共享union预算未闭合。 | [§8通用接口](customer_attraction/sunflower_maxima_bound.md)，独立内部证明核查；不解决一般半覆盖。 |
| CA-SUNFLOWER-PRIVATE-GAP | 同sunflower类，每非极大主题在某个极大扩张中遗漏私有花瓣客户；唯一极大主题无需额外条件。 | 每个完整SPE在每个历史只选极大主题，根花瓣计数为singleton PNE；福利定理无需此条件。 | [§6完整真实续局扩张](customer_attraction/sunflower_maxima_bound.md)，独立审查；省略条件有非极大且非PNE完整SPE。 |


| CA-LAMINAR-INCIDENCE-THETA | CAG-MODEL，任意n≥1；客户在不同极大覆盖主题间的关联索引集合组成laminar家族；任意内部子主题、全部有序历史纯SPE。 | 每个合法前缀中所有剩余玩家最终收益各≥全局θ_n；不要求主题目录自身laminar或终局PNE。 | [真实最大交叠保护及全历史归纳](customer_attraction/laminar_incidence_bound.md)，独立重构与精确审计；外审/新颖性未认证。 |
| CA-LAMINAR-INCIDENCE-MAXIMA-2M1 | 同上结构类；c为所有极大覆盖的共同核心大小，内部主题可遗漏核心。 | OPT_n≤c+(2−1/n)(W−c)，常数锐，严格扩展sunflower极大目录；一般交叠目录不涵盖。 | [逐客户预算及锐性证明](customer_attraction/laminar_incidence_bound.md)，独立内部审查与完整历史核验。 |
| CA-AGGREGATE-LAST-FLOOR-NO | CAG-MODEL，每个n≥3均存在有限共同目录单位客户实例与完整纯SPE。 | W=nθ_n−1的无限构造；36客户三人六主题实例W=34、θ=12、OPT=36。否定聚合W≥nθ，未反驳半覆盖。 | [紧凑完整策略、重复前缀预算与Möbius族](customer_attraction/aggregate_theta_counterexample.md)，独立直接单位客户重放及精确审计。 |
| CA-OBLIVIOUS-MIXED-SECURITY-2N1 | CAG-MODEL任意n≥1；当前人随机主题，其余n−1竞争主题可联合固定但不观察抽样实现。 | v_n≥OPT_n/(2n−1)，每个n均锐；逐人u_i≥v_n现由CA-INDIVIDUAL-SECURITY-NO否定；聚合W≥nv_n仍开放。 | [有限minimax、Jensen与共同目录预算](customer_attraction/oblivious_security.md)，独立审查与精确原始/对偶证书。 |
| CA-ROOT-TAX-ORDER-COUNTS-NO | CAG-MODEL，每个n≥4；同一静态PNE且完整SPE可达终局计数。 | 可信SPE顺序W+τ−OPT=1，某非SPE重排OPT−W−τ=(n−1)(n−3)/n>0；只排除仅看计数的根税证明。 | [§7无限族与完整策略](customer_attraction/two_remaining_tax.md)，独立重构、n=4全树及47个参数精确核验。 |
| CA-THREE-MAXIMA-HALF | CAG-MODEL，至多三个不同包含极大覆盖，任意内部子主题，任意n≥1、全部有序历史纯SPE；c为极大共同核心。 | n≥2时OPT_n≤U≤c+2(W−c)；n=1或唯一极大主题时最优。允许交叉关联，与不限极大主题数的laminar类不可比较；不声称福利常数锐。 | [全历史superset席位与共享union预算](customer_attraction/three_maxima_bound.md)，两路精确审计及独立证明重构；外审/新颖性未认证。 |
| CA-FIVE-UPPER-221-100 | CAG-MODEL，恰五位单位玩家、任意有限共同目录、零根背景、每个完整有序历史纯SPE，允许空/重复主题。 | OPT_5≤[24236714656727/10967499015623]W≤(221/100)W；精确系数仍大于2。 | [两条真实中途偏离及21-slack恒等式](customer_attraction/five_player_bound.md)，1024客户型余项与独立O系数经两份互不导入Fraction程序核对；不声称锐性、背景版或六人以上。 |
| CA-DYNAMIC-MAXIMA-FLOOR | CAG-MODEL，n≥1、s≥2不同极大覆盖、全部合法有序前缀、每个完整历史纯SPE，任意内部子主题。 | 当前收益≥c/n+(U−c)/D_t，D_t=max(t+s(n−t)/2,n+s−1)；W≥c+Γ_(n,s)(U−c)。四极大且n≥3给U≤2W−c；一般s的系数不保证半覆盖。 | [动态路由客户预算及同路由后继包含支配](customer_attraction/dynamic_maxima_bound.md)，独立重构、两份精确菜单/全历史审计；外审与锐性未认证。 |
| CA-DYNAMIC-MAXIMA-MIXED | 同一模型/量词；P为全局私有总质量，V为非core共享质量；A_t、B_t及其suffix minima按完整稿§5定义。 | 每位收益≥c/n+P·underlineA_t+V·underlineB_t；W≥c+PΣunderlineA_t+VΣunderlineB_t；允许漏core、无私有及多父路由。 | [私有/共享分离与单调包络](customer_attraction/dynamic_maxima_bound.md)，同一加权预算同时支付两质量；不将分别最大值相加；独立审查通过。 |
| CA-FIVE-MAXIMA-HALF | CAG-MODEL，至多五个不同包含极大覆盖，任意n≥1、任意内部子主题、全部完整历史纯SPE。 | OPT_n≤2W；n≥5时OPT_n=U≤2W−c；n=5进一步W≥c+5P/9+(67027/125400)V。n≤4用已知一般界，n≥6用Jensen；不把小人数OPT替换为U。 | [完整动态/混合预算与五极大整合](customer_attraction/dynamic_maxima_bound.md)，独立重构和精确复验；本条保持五极大范围；六极大由新joint定理覆盖，至少七极大的一般目标及锐性/新颖性仍开放。 |
| CA-SIX-MAXIMA-HALF | CAG-MODEL，至多六个不同包含极大覆盖，私有/共享关联、内部子主题任意，任意n≥1、全部完整有序历史纯SPE；空/重复行动和任意历史平局保留。 | OPT_n≤2W；n≥5还U≤2W，n≥6有OPT_n=U。n5用52完整路由的整数/10000客户级dual，n6…8同一path-free小分数dual；不普遍声称U≤2W−c。 | [完整真实会员预算证明](customer_attraction/six_maxima_joint_bound.md)，20080+14112列Fraction余项、396压缩恒等式、两份独立审计及数学重构通过；剩余一般目标需至少七极大且n≥5，外审/新颖性/锐性未认证。 |
| CA-SIX-MAXIMA-NO-PRIVATE-HALF | CAG-MODEL，至多六个不同包含极大覆盖；非core客户均至少属于两个极大主题；任意内部子主题、任意n≥1、全部有序历史纯SPE。 | OPT_n≤2W；n≥5还OPT_n=U≤2W−c。共享动态F(p,r)逐历史单调，n=5/6由67份显式整数/12路径系数证书闭合，n≥7用解析和式，n≤4用一般界；不推广至有全局私有客户的六极大类。 | [完整证明](customer_attraction/six_maxima_no_private.md)，3752项Fraction系数恒等式及独立全续局/有序证书审计及独立完整内部重构；外审、新颖性及常数锐性未认证。 |
| CA-SIX-MAXIMA-NINE-PLUS-HALF | CAG-MODEL，至多六个不同包含极大覆盖，任意私有/共享关联、任意内部子主题；n≥9、全部完整有序历史纯SPE。 | OPT_n=U≤2W−c；固定六极大私有包络和≥1/2，共享系数和≥665881/1330560>1/2。本推论保持n≥9的更强core界；新CA-SIX-MAXIMA-HALF已补齐n5…8的普通半覆盖，不将机制障碍称SPE反例。 | [动态混合接口的解析推论](customer_attraction/six_maxima_no_private.md#5-nine-or-more-providers-unrestricted-six-maxima)，精确系数/端点复验及独立完整内部审查；外审、新颖性及锐性未认证。 |
| CA-FIVE-INDEXED-UPPER | CAG-MODEL，恰五位单位玩家、有限共同目录、零根背景、全部完整有序历史纯SPE；空/重复主题和索引、历史依赖平局均允许。 | OPT_5≤[145473820534756099649387160645076613709/70560308704423797361284609157664425493]W≈2.06169478572W；437行真实索引续局、57个非负有理乘子、6144个全范围条件余项闭合；常数仍>2。 | [完整逐节点与直方图证明](customer_attraction/five_player_indexed_bound.md)，两份互不导入的标准库精确审计及独立数学重构；不声称半覆盖、背景版、六人以上或原游戏锐性，外审未记录。 |
| CA-FIVE-INDEXED-ROWS-NO | 上一条§1–3明确437行必要条件松弛、非负类型重数、W=1；O为五个比较主题并集变量。 | 64原子的精确有理可行点有O=beta>2，与57乘子dual匹配，beta为该松弛精确最优值；该模板不能单独推出O≤2W。 | [完整变量与精确障碍](customer_attraction/five_player_indexed_obstruction.md)，437行逐一核验和两份全范围dual审计；没有完整SPE，不声称真实OPT或猜想反例。 |
| CA-FIVE-REPLY-UPPER | CAG-MODEL，恰五位单位玩家、任意共同有限目录、零根背景、全部完整历史纯SPE、空/重复主题。 | OPT_5≤[493266145873827/234749688354196]W≈2.10124302755W；改善旧约2.209867，仍严格大于2。 | [三个真实最优回复菜单与24-slack恒等式](customer_attraction/five_player_reply_bound.md)，两份独立Fraction程序核49152角、157零余项及逐节点审查；不声称半覆盖、背景版或锐性。 |
| CA-ONE-FOLLOWER-DECORRELATION | CAG-MODEL，任意合法固定背景、恰两人剩余、每个完整SPE、任意主题概率p。 | 真实适应性查询均值减独立同分布回复均值，恰等于真实末位BR slacks均值≥0；实际菜单对偶值≤当前收益。 | [一后继普遍恒等式](customer_attraction/continuation_security_barriers.md)，独立逐式审查；多后继量词不能平移。 |
| CA-ADAPTIVE-DECORRELATION-NO | CAG-MODEL，已有四人十二主题、正单位客户、完整1885节点策略。 | 两个真实根偏离在各半分布下，适应性均值减独立回复均值=−11/4；否定普遍去相关。 | [完整策略重放及四项矩阵](customer_attraction/continuation_security_barriers.md)，22620精确比较及独立矩阵重构；未否定v_n收益桥或原目标。 |
| CA-ACTUAL-ROOT-TAIL-MENU-NO | CAG-MODEL，三人六主题36单位客户、给定全部43节点策略。 | 自由混合所有真实根后继组合的minimax值z1=11>u1=v3=10；stationary回复核仍cap11。 | [两列矩阵、所有概率界与完整SPE](customer_attraction/continuation_security_barriers.md)，258精确比较、完整静态安全值原始/对偶；不是原猜想反例。 |
| CA-CREDIBLE-MENU-SECURITY-NO-ALL-N | CAG-MODEL，每个n≥3；两组Boolean势经K=4Σabs(x)+1正编译；完整历史SPE。 | 每n都有z1=u1+1/2；扩大为2n个纯组尾组合却给合法静态dual cap≤u1，故失败只在真实菜单量词。 | [完整fresh策略、M2全历史嵌入、双向菜单值](customer_attraction/continuation_security_barriers.md)，独立普遍审查及n3…6算术回归；不以有限回归代替存在证明。 |

| CA-MOBIUS-SECURITY-BIAS-BARRIER | p≥n≥2，合法整数类型r_B=x_B+K、M=Σabs(x_B)，任意n个不同主题终局；不要求均衡。 | 每位u_i−v_n≥K·2^(p−n)(2^n−n−1)/(np)−M。标准M2偏置K=4M+1给所有完整根SPE逐人差≥1/4、聚合差≥n/4，故不能反驳真正安全值桥；小偏置未被排除。 | [均匀不同主题背景对偶及系数差证明](customer_attraction/compiler_security_barrier.md)，独立内部审查、28公式族/1757逐人精确检查；不解决一般目录桥。 |
| CA-OPTIMAL-LAST-QUERY-SUM-NO | CAG-MODEL，四人七主题1651单位客户，全部400节点完整纯SPE，实际路径E,G,A,C。 | W=1559、唯一最优四主题BCDF覆盖1562；实际末背景E,G,A对每个最优元组的查询和1560>W。否定存在最优组合查询总额≤W的充分桥；静态安全dual cap4889/14<每人收益。 | [明确整数输入、完整策略及唯一OPT证明](customer_attraction/optimal_last_query_counterexample.md)，两份独立Fraction审计2800比较/210终局；未否定根税、安全值桥或半覆盖。 |


| CA-ROOT-TAX-NO | CAG-MODEL，四人、六共同主题、61不同单位客户；实际空背景根路径的完整有序历史纯SPE。 | 路径AAAF，收益(9,9,9,11)、W38、OPT4=61、前n−1步根税45/2，OPT−W−tau=1/2>0。否定根总税全称充分桥；v4=9且W−4v4=2，不反驳安全值桥或半覆盖。 | [完整客户表、策略和逐节点比较](customer_attraction/root_tax_counterexample.md)，259历史/1295非自身偏离、两份独立Fraction审计；外审未记录。 |
| CA-AGGREGATE-DECORRELATION-NO | CAG-MODEL，四人六主题89单位客户的完整259历史SPE，p在标签1,2各半。 | 总kappa=sum(D_i−C_i)=−1/48，后三位均0；激励松弛和43/12，补偿预算57/16>0。W85、OPT89、v4=508643/26546，不是BR或GB反例；既有36例也已否定总kappa。 | [准确预算与89客户证书](customer_attraction/global_security_budget_boundaries.md)，1554完整比较和216静态竞争元组的匹配原始/对偶经两路独立核验。 |
| CA-ONPATH-DECOUPLED-BUDGET-NO | 既有三人六主题36单位客户完整SPE，p在未用X2,Y2各半。 | 实际(10,12,12)、所有e_i=0，kappa=(−1,1/2,0)，W−sum C_i=−1/2。因此包含激励松弛的全p预算GB为假；p静态安全值25/3<v3=10，W−3v3=4，不排除最优p版本或BR。 | [三真实查询矩阵及完整证明](customer_attraction/global_security_budget_boundaries.md)，258动作比较、原输入/策略一致性及静态安全值双路独立审计。 |
| CA-SECURITY-CONE-DUAL | 固定人数、标签数、全部有序历史形式策略sigma和有理混合p；固定完整SPE客户锥，允许相同覆盖标签；不同覆盖合同需策略已有合法实现。 | 全锥W≥n min_B beta_B(p)·w等价于存在不受限静态Q、非负全部节点乘子lambda和余项r，c−n sum Q beta=Gamma^T lambda+r。普遍证书存在等价于BR；有理正LP见证可缩放成真正反例。 | [minimax/Farkas完整推导及目录合同](customer_attraction/security_cone_duality.md)，独立数学审查；是既有策略锥的标准安全值扩展，未证明普遍证书存在或BR，外审未记录。 |

| CA-INDIVIDUAL-SECURITY-NO | CAG-MODEL，三人六个两两不同覆盖、34单位客户、全部43有序历史的指定纯SPE。 | u1=29/3<v3=2411/246，严格差11/82；安全最优p唯一。W32、OPT34，聚合安全桥与原目标均成立；三是此辅助失败的最小人数，不声称主题/客户最小。 | [完整策略、精确原始/对偶及可逆性证明](customer_attraction/individual_security_counterexample.md)，两路互不导入全树/静态审计；外审未记录。 |
| CA-IID-SECURITY-BENCHMARK | 任意共同有限非空目录、n≥1、非负客户类型质量；整数质量为不同单位客户。 | 期望harmonic势的最大者恰为静态对称混合Nash；其期望覆盖Z_n唯一且nv_n≤Z_n≤OPT_n≤U。W≥Z_n是更强开放桥，不是逐人保证。 | [凹性、单纯形条件及静态对偶完整证明](customer_attraction/iid_security_and_flow_barriers.md)，独立数学重构；外审/新颖性未认证。 |
| CA-FULL-TREE-AVERAGING-NO | 指定原36客户三人形式策略、六主题uniform q、全部非空兴趣类型。 | 任意非负按深度或43节点权重，在每节点先按q平均全部偏离，再加静态Nash乘子与非负余项，都不能支付c−ψ(q)。两项精确分离向量不满足完整SPE；未否定未压缩证书或任何主猜想。 | [流恒等式及六/十五类型分离证明](customer_attraction/iid_security_and_flow_barriers.md)，两路定义级精确审查；范围仅该非负线性模板。 |
| CA-SELECTED-SECURITY-CONES | 保存的36/61/89来源三棵完整形式策略，任意非负类型重数使其成为完整SPE；五个固定游戏各指定一个安全最优p。 | 三个整个锥都有W≥nv_n，两棵四人锥逐人亦成立；另外五游戏的全部完整SPE的给定最优p预算均严格正。分别为全锥恒等式与有限全策略枚举，不是任意策略定理。 | [共同Q支付及独立菜单拼接证明](customer_attraction/selected_security_cones.md)，4914客户系数恒等式、全部有序菜单/达到策略精确核对。 |
| CA-TAIL-FOUR-ALL-N | CAG-MODEL，任意n≥4、共同有限非空目录、每个完整历史纯SPE。 | OPT_n≤(n/2−1/750)W；无目录结构限制、系数仍随n增长，不解决常数二。一般k公式要求任意合法背景β_k≤k/2。 | [比较索引计数、真实K/n预算及完整消元](customer_attraction/tail_profit_lift.md)，依赖任意背景末四人利润定理；独立数学审查通过，外审未记录。 |
| CA-SEVEN-MAXIMA-N7-PLUS | CAG-MODEL，恰七不同极大覆盖、任意内部子主题、任意n≥7、每个完整历史纯SPE。 | U=OPT_n≤2W。来源证明完整且独立审查通过，现行页仅依赖和资产概述；恰七极大n5/n6仍缺16/44轨道，不宣布任意n完成。 | [来源证明checkpoint及独立审查](customer_attraction/seven_maxima_checkpoint.md)，24384 literal列、988压缩列及n≥13解析case已审；现行全文重构未作，外审未记录。 |

| CA-RANDOM-PREFIX-EXCHANGE-NO | CAG-MODEL，三人三不交主题，五单位客户及完整13历史SPE；随机最优比较索引排列的前两行动被强制。 | 最新强制成员期望4/3<前两总收益一半3/2，差1/6；唯一最优支持ABC。末位相同负载最优收益仍相等；不反驳uniform接口或半覆盖。 | [完整策略及六分支直接证明](customer_attraction/random_position_exchange_boundary.md)，39比较精确审计；外审未记录。 |

## 2026-10-10：全局安全债务与构造式真实分支转移

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| CA-SECURITY-CHAIN-INTERFACE | CAG-MODEL，任意n≥1、任意完整历史纯SPE；背景安全值始终是静态查询比较。 | 沿实际路径V_i=v_(n−i+1)(b_i)非降、V_n=u_n；Σ_(i<n)[u_i−V_i+(n−i)(V_(i+1)−V_i)]=W−nV_1。全局弱目标W≥(n−1/2)V_1足以半覆盖，但仍开放。 | [背景列嵌入及强/弱望远镜完整证明](customer_attraction/security_chain_and_local_boundary.md)，独立数学审查和两路精确复算；恒等式不是债务下界。 |
| CA-LOCAL-SECURITY-INDUCTION-NO | 三人六主题113不同单位客户、指定完整43历史SPE；背景是实际首主题0。 | u=(95/3,110/3,110/3)、W105、OPT113；u1+2V2−3V1<0及u1+1.5V2−2.5V1<0，简单界分别−1/20、−17/120。后一个局部非负条件反而更强；全局两安全桥仍成立。 | [19类型、全部真实策略及小分数夹逼](customer_attraction/security_chain_and_local_boundary.md)，两个匹配静态鞍点、全部258比较和单位展开独立核验；不声称最小客户数。 |
| CA-STATIONARY-PAIR-TRANSPORT | 任意n≥2、固定长度n−2有序前缀P、任意完整形式策略；全部兴趣类型。 | 末回复图循环C给Q均匀于P+a，有逐类型u_pen−E_Qf(t)=E_C[Γ_(P,a)+Γ_(Pa,t)]，公开非负λ且零余项。该配对模板非负余项当且仅当π平稳；收益强度不超过既知末两人保底。 | [循环望远镜与精确divergence](customer_attraction/stationary_pair_transport.md)，独立代数重构及全类型审计；一般多后继gluing未解。 |
| CA-PRESCRIBED-STATIC-KERNELS-NO | 指定三人22客户六不同主题SPE与三人7客户四标签SPE，前者根回复成员平稳Q、后者实际终局频率iid Q。 | 前者唯一核cap6>W/3=17/3；后者查询77/27>W/(3−1/2)=14/5。两规定Q构造失败，均未否定不受限Q的安全桥、所有实际节点菜单或半覆盖。 | [完整历史与两项严格分数差](customer_attraction/stationary_pair_transport.md)，两路独立Fraction复验；7客户例允许同覆盖标签。 |
| CA-TERMINAL-REPLY-DUAL-LIFT | 任意完整形式策略、n≥2；同主题计数末层代表规范化并保留实际根前缀；给定非负逐偏离形式证书。 | 末行拆成两条原Γ非负行；早期转移E=Σκδ。若r+E≥0可显式提升原Γ证书；非代表守恒是充分非必要条件。转移图按偏离次数为DAG；亏损/增加只分别有半/全旧收益预算。 | [全部行变换与构造式提升](customer_attraction/terminal_reply_transport.md)，独立完整数学审查、两路273列恒等式；仍未构造普遍λ,r+E预算。 |
| CA-TERMINAL-TIE-QUOTIENT-LIFT | CAG-MODEL，任意n≥2、完整形式策略、同计数保根末回复规范化；给定非负规范化证书。 | 若r+E属于非负类型锥加相反真实末行空间H，可用符号系数正负分拆显式提升；严格扩大r+E逐类型非负条件，尚未构造普遍输入乘子。 | [商空间完整构造](customer_attraction/terminal_tie_quotient.md)，两路定义级精确核验及自然2c−o成功证书；不假定规范化策略仍为SPE。 |
| CA-TERMINAL-TIE-LOCAL-QUADRATIC | 固定末主题计数q、原末回复集及真实可达incumbent净流；全部兴趣类型。 | 同q误差属于自身相反末行空间，等价于含p=0外部约束的O(m²)Boolean一次/二次系数式；逐q消去仅是全局充分条件，非均匀四边和跨q支付均可有效。 | [局部精确判别](customer_attraction/terminal_tie_quotient.md)，全类型审计；不声称全局必要或一般λ存在。 |
| CA-TERMINAL-TIE-FIXED-LIFT-NO | 三单位客户、三主题、三人完整历史SPE；自然比较元组A,B,C。 | 非负规范化2c−o证书可在保留早期乘子后留下s·w=−3/2；追加任意非负真实行均不能修复。同实例另选早期乘子即可商空间提升。 | [完整策略、逐类型两证书及精确分离](customer_attraction/terminal_tie_lift_obstruction.md)，root和两路Fraction复验；不是半覆盖或安全桥反例。 |
| CA-DYNAMIC-IID-DEBT-INTERFACE | 任意固定非负整数背景、剩r≥1人、共同非空目录，全部完整有序状态。 | 剩余harmonic iid势凹，KKT刻画对称NE并确定唯一剩余利润Z；总覆盖=前缀租金+Z。实际路径Σ(Z_h−Z_child−u_h)=Z_n−W；净债≤Z_n/(2n)足以半覆盖，仍开放。 | [背景微分、租金恒等式与全局接口](customer_attraction/dynamic_iid_debt_boundary.md)，独立数学重构；有背景Z不是覆盖。 |
| CA-WEAK-LOCAL-IID-DRIFT-NO | 五人七不同主题60单位客户、全部2801历史完整SPE；前缀PP位于实际路径。 | u=(12,12,10,12,12)、W58、OPT60；PP剩余Z3=97/3，PP0的Z2=21。第三人10<(9/10)(34/3)=51/5，弱逐步漂移亏1/5。全局弱桥仍成立。 | [原始类型与两个全查询KKT](customer_attraction/dynamic_iid_debt_boundary.md)，两路19607比较、纯iid/类型二项式独立复验；只否定局部命题。 |
| CA-NEW-POLICY-CONE-SECURITY | 保存的21棵新的指定完整形式策略（五人七/八主题及六人八主题），各自全部合法非负客户重数锥。 | 每锥有与w,p无关的共同静态Q及全部纯查询非负Γ证书，故整个锥W≥nv_n。不是任意策略或一个完整目录类定理；部分规则可能只有退化可行性。 | [共同Q的逐查询恒等式及压缩证书](customer_attraction/policy_security_checkpoints.md)，独立全有序Γ重建；据此停止沿这些树重复调权。 |
| CA-FIVE-INDIVIDUAL-SECURITY-NO | 五人十个两两不同极大主题、86单位客户、指定11111历史完整SPE。 | 实际(4,5,6,7,8)，u=(81/5,86/5,86/5,86/5,86/5)，v5=2262/139，根亏51/695；W85、OPT86。不否定聚合安全桥或主半覆盖。 | [完整可信菜单来源及静态鞍点](customer_attraction/policy_security_checkpoints.md)，111110动作比较、全部静态竞争计数与极大主题条件独立Fraction检查。 |

## 2026-10-09 EPTAS 预研与近带精确补全

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| SC-TWO-NEAR-BAND-REP | 固定两设施子局、非负有理独占背景、正逐名共同权、给定 H>0；轻权≤H，重权>H，每名重客户指定纯第一/纯第二/真正混合。 | 位多项式判定/输出符合重支持且 abs(Δ)≤H 的某个原实例精确 NE；不实现预定精确差值，不解原全 k 盒问题。 | [完整分支证明](shared/near_band_completion.md)，两路独立内部重构与精确攻击；prototype audits，不是规范通用实现；外审未记录。 |

算法义务 `Q-SC-ALPHA-EPTAS`：原共同目录双设施实例最优倍率的
`f(1/ε)poly(L)` 精确续局近似构造。已有少数重支持谱与近带補全的全局 C² 候选，
尚未登记完整 EPTAS 定理或一般位复杂度交付。见
[候选和下一任务](../questions/shared_alpha_eptas.md)、
[团队辩驳](../../history/source/notes/publication/facility_eptas_direction_debate_2026-10-09.md)。此义务不是已证明 Claim。

## 2026-10-09 四共同地点无 FPTAS

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| SC-FOUR-NO-FPTAS | 两设施、恰四共同地点、正二进制整数原子权、强制服务、实际负载成本、完整精确独立混合客户 NE 续局；优化域允许实概率，算法输出为显式有理概率。 | PARTITION 源 n=2max{t,2}，YES α*=13/10，NO 任意布局/续局 α*≥13/10+1/(100n²)；P≠NP 下无加性或乘性 FPTAS。不排除 PTAS/强 NP 难/一般任意盒 NE 搜索。 | [完整证明](shared/four_site_no_fptas.md)、[独立审查](../reviews/facility/four_site_no_fptas.md)；完整内部证明和两套定义级精确审计；外审未记录，新颖性未认证。 |

本结论对实例最优倍率近似，不改变一般盒内任意 NE 搜索的开放状态。

## 2026-10-08 complement search interfaces

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| SC-K-COMPLEMENT-GREEDY-REDUCTION | Co-singleton affine source: integer speeds q>=1, nonnegative rational backgrounds, individual positive rational weights, nonempty allowed sets; target is actual canonical greedy MF-MODEL with explicit k=1+sum(q). | Original multiplicities, gamma=1, every legal assignment in the full box and strict H; all deviations, source pure NE versus target station-pure independent-uniform NE, weighted potentials and specified dynamics correspond. Usual source-bit polynomial search reduction for q in {1,2}; arbitrary binary q is output-sensitive. No equilibrium oracle or hardness. | [Full reconstruction and bit bounds](multi_facility/complement_search_reduction.md); composite internal algebraic/definition-level review and canonical implementation, no external review. |
| SC-K-BOX-BOUNDED-COMPLEMENT | Ordered abstract q, c in [0,1], individual w in (0,1), nonempty A and home=min A. Compatible inverse source additionally has those weight/home constraints and initial q_t M-1<=Y_t(h)<=q_t M. | Y_t=q_t M-X_t preserves every original deviation and converts full-box output into exact load bands without expanding q. Arbitrary unbounded NE does not suffice; bands are output requirements, not hard capacities. Representation only, not a selector. | [Forward/inverse domains and strict band counterexample](multi_facility/complement_search_reduction.md); complete internal reconstruction, implemented import, no external review or general search-time theorem. |

The new source-to-greedy embedding and general bounded-complement representation do not change the feasibility or time status of `SC-K-RQ-MIXED-BOX`. The previous direct speed substitution remains false; the new interface uses strategy complements and an affine reversal of loads.

## 2026-10-07 greedy full-box existence and finite construction

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| SC-K-EQUAL-LIGHT-FLOW-BOX | Ordered positive binary-integer site multiplicities, rational c in [0,1], individually labeled customers with a common 0<delta<1, nonempty allowed sets and home=min allowed site. No restriction on incidence graph or binary multiplicity size. | Every unconstrained global Psi minimizer satisfies the full box, all original exact NE inequalities and H. A unit-capacity convex-cost flow constructs one in input-bit-polynomial time without expanding q. Lower-box constraints in the older selector are redundant. | [Self-contained paths, flow and bit bounds](multi_facility/equal_light_flow.md); independently internally reviewed, canonical on-path implementation and exact audits, no external review. |
| SC-K-EQUAL-LIGHT-FLOW-2 | Explicit rational MF-MODEL at its canonical greedy occupancy; all remaining multi-option customers below gamma have one common weight; frozen and single-option weights unrestricted. | The new selector and BOX-TO-2 yield the same-class polynomial mathematical factor-two continuation. This is not a new MF input class beyond UNIFORM-LIGHT-FLOW-2. Canonical on-path code is polynomial; connected off-path/default code remains finite pure improvement. | [Versioned construction and old/new optimum identity](multi_facility/equal_light_flow.md); mathematical proof complete, software partial for the polynomial contract, no external review. |
| SC-K-GREEDY-BOX-EXISTS | Every legal normalized abstract input: positive integer `q`, `0<w_i<1`, `c_t in [0,1]`, nonempty `A_i`, and `h_i in A_i` with `q_h_i >= q_t` for every allowed `t`; rational encoding for bit bounds. The forward greedy interface covers every common-catalog greedy occupancy with heavy and singleton-option customers frozen. | Arbitrary strict improvement from a box-and-`(H)` batch state followed by the prescribed return repair terminates in full-box exact customer NE plus `(H)`; at most `S-1` microsteps, `S=prod_i card(A_i)`, and polynomial space without a trace. No general polynomial total-time bound. | [Full reconstruction](multi_facility/greedy_box_global_progress.md); user-pasted proof source, independent internal review, finite exact implementation checks, no external review. |
| SC-K-GREEDY-BOX-FINITE-2 | Explicit positive binary rational common-catalog MF-MODEL input and labeled facilities; zero reach handled separately. | Finite exact full factor-two continuation at the canonical greedy occupancy, by GREEDY-BOX-EXISTS and BOX-TO-2. The connected executable uses finite cap-preserving pure best responses off path and is not an implementation of the polynomial imported scheduler. | [Proof and implementation boundary](multi_facility/greedy_box_global_progress.md); finite canonical constructor, independent internal review, no external review. |
| SC-K-BOX-STRUCTURED-POLY-2 | Same rational model, with either fixed individual light-incidence treewidth and two-sided degree, or fixed site-primal treewidth and per-site distinct incident light-weight count. | Existing exact DP always finds a full-box NE by GREEDY-BOX-EXISTS; BOX-TO-2 gives a bit-polynomial complete factor-two continuation. No two-option/depth-two restriction; older IDs retain their original hypotheses. | [Versioned corollary](multi_facility/greedy_box_global_progress.md), [incidence case](multi_facility/bounded_incidence_box.md), [local-weight case](multi_facility/local_weight_box_dp.md); complete internal proof, no canonical DP/imported-scheduler implementation or external review. |

The new potential interleaves threshold-clipped site-load vectors and home-return counts. It does not rehabilitate the old untruncated boxed lexmax or customer-potential selectors. General boxed feasibility is now settled; `SC-K-RQ-MIXED-BOX` retains only its unrestricted bit-polynomial algorithm obligation.

## 2026-10-04 deviator-specific frozen-overload continuation

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| MF-FROZEN-OVERLOAD-POLY | Fixed MF-MODEL layout and supplied feasible pure seed; ordinary loads at most `B>=0`, stationary frozen loads above `B`, every frozen external client load bounded at all alternatives by residual pure forced-client floors or other frozen loads. | Bit-polynomial full pure NE with the ordinary mover at most `B`; no successful seed-search guarantee. | [Exact proof and cap-41 separation](multi_facility/frozen_overload_completion.md); multiple internal reviews, finite audit, unimplemented imported scheduler, no external review. |
| SC-K-FROZEN-OVERLOAD-2 | Any supplied rational exact independent-mixed on-path NE plus successful frozen-overload certificates at `B=2a_f` for every actual labeled deviation. | Bit-polynomial complete factor-two continuation; no greedy or deletion-bin premise, no all-input on-path/certificate generator. | MF-FROZEN-OVERLOAD-POLY, compatible labeled continuations and published polynomial default; [full scope](multi_facility/frozen_overload_completion.md), internal review only. |

`MF-FROZEN-OVERLOAD-POLY` accepts a supplied pure deviation seed with ordinary loads at most `B` and stationary frozen loads above `B`, if every frozen client's external load is bounded by the residual pure forced-client floors at all ordinary alternatives and by other frozen loads. Published identical-link Nashification plus reinsertion yields a full pure NE with the mover at most `B` in bit-polynomial time. `SC-K-FROZEN-OVERLOAD-2` combines successful `B=2a_f` certificates for every actual labeled deviation with any supplied rational exact on-path NE and a polynomial default. [Exact identities and limitations](multi_facility/claims.md#mf-frozen-overload-poly-and-sc-k-frozen-overload-2----safe-stationary-overloads), [complete proof](multi_facility/frozen_overload_completion.md), [finite audit](../../tests/audits/kfac_frozen_overload.py). Independently internally reviewed conditional theorems; no all-input certificate generator, canonical scheduler implementation or external review.

## New arbitrary-k conditional construction and fixed-occupancy selector boundaries (2026-10-04)

| ID | Exact scope | Result and boundary | Current proof / audit |
| --- | --- | --- | --- |
| SC-K-ADAPTIVE-RESET | Greedy `gamma>0`, supplied explicitly rational independent-mixed on-path exact NE, every payoff at least `gamma`, and certified original-pool deletion bins at cap twice the source-site minimum payoff (or a supplied floor between `gamma` and that minimum). | Bit-polynomial complete exact factor-two continuation for the supplied occupancy; does not find arbitrary on-path NE or deletion bins. | [All-deviation proof](multi_facility/adaptive_reset_floor.md), internal reverse review; imported scheduling algorithm unimplemented, no external review. |
| SC-K-FORCED-FLOOR | Every **pure** exact on-path NE; forced-client weights at each occupied site and the explicit `eta` formula. | Every facility at that site earns at least `eta`; no mixed-NE assertion. | [Atomic best-response proof](multi_facility/adaptive_reset_floor.md), internal review, no external review. |
| SC-K-ADAPTIVE-DOUBLE-LPT-2 | First original-pool `q_s`-bin LPT has minimum `gamma`; second `(q_s-1)`-bin LPT has maximum `2 max(gamma,eta_s)` for each multisite source. | Input-bit-polynomial complete exact factor two conditional constructor; strict triangle passes while old `2 gamma` deletion packing is impossible. | [Full proof and example](multi_facility/adaptive_reset_floor.md), [finite audit](../../tests/audits/kfac_adaptive_reset.py); imported scheduler not locally implemented or externally reviewed. |
| SC-K-DEPTH-THREE-BOX-POTENTIAL-NO | One strict positive-integer greedy tree, directed depth three, one light atom per edge. | Unique boxed potential minimizer is not customer NE; a boxed NE exists. Specific selector obstruction only. | [Exhaustive analytic proof](multi_facility/depth_three_box_boundary.md), [Fraction audit](../../tests/audits/kfac_depth_three_box.py); no external review. |
| SC-K-BOX-LEXMAX-NO | One strict positive-integer greedy light path with heterogeneous paired edge weights. | Unique boxed lexmax load vector is not customer NE; a boxed NE exists. Specific selector obstruction only. | [Analytic classification](multi_facility/boxed_lexmax_boundary.md), [Fraction audit](../../tests/audits/kfac_box_lexmax.py); no external review. |


先读[规范模型](model.md)。逐命题的[五轴状态登记](../review_status.json)分别记录来源证明、现行 Markdown 重写、内部审读、外部评审与软件实现，并由图生成器检查其与命题节点的状态一致性。共同目录的完整主稿与现行全分支重写经过多轮内部审读；实例证书仅核查该实例。原稿和程序追溯见[资产索引](../assets.json)；逻辑合取和反例边见[超图](../graph.json)。

| ID | 作用域与量词 | 结论 | 必需依赖与状态 |
| --- | --- | --- | --- |
| SC-PHI-E | 任意非空相同目录、正实权重、模型 (NE)，存在完整延续选择 | 存在因子 \(\phi=(1+\sqrt5)/2\) 的纯选址近似 SPE | 依赖共同目录菜单覆盖、全目录环论证、局部强弦。来源稿：[完整主稿](../../history/source/manuscripts/shared_phi/main.tex)已成文；现行重写：[G1–G3、L1–L2 全分支](shared/README.md)已写出；内部审读：已记录多轮逐式审读；外部评审：尚未进行。 |
| SC-PHI-A | SC-PHI-E 且显式正二进制有理输入 | 构造该证书；主稿给出 \(O(|S|^2(n+1)^4)\) 次有理运算与多项式位长 | 依赖 SC-PHI-E、固定菜单与精确比较。来源稿：构造与位复杂度已成文；现行重写：[局部强弦](shared/local_chord_full.md)和[算法](shared/algorithm.md)已写出；实现：已有构造器；内部审读：已记录；外部评审：尚未进行。 |
| SC-PHI-SHARP | 同一共同目录**正有理数**实例类 | 最优普遍阈值（上确界）恰为 \(\phi\) | 必须联合 SC-PHI-E 与同类下界。来源稿：已发表六地点构造；现行重写：[共同目录六地点下界](shared/sharp_phi_lower.md)重算全部布局、明确修正源图的一项权重，并给统一正有理扰动半径；内部审读：当前证明与有限整数例已作精确核对，仍可接受进一步反例审查；外部评审：本仓库修正版未获评审。 |
| SC-DIAG-NORMAL | 两设施同一非空有限目录、正实权、模型 (NE)、逐布局独立选择完整精确延续；零 reach 允许 | 实例最优倍率等于同址对半候选 $\min_t\max(1,2H(t)/R_t)$ 与异址真实 NE 候选的最小值；存在最优证书在**每个**同址布局对半 | 依赖坐标极小值判别、标签反射、对半同址 NE；失效的异址对半惩罚改选同址候选。[全文](shared/instance_complexity_barriers.md)；本轮独立审读，外部评审未进行。 |
| SC-OFFDIAG-FPT | SC-DIAG-NORMAL 且显式覆盖、正二进制有理权；$\kappa_{\ne}=\max_{s\ne t}|C_s\cap C_t|$，单地点取零 | $O(|S|^2[n+\kappa_{\ne}3^{\kappa_{\ne}}])$ 次有理运算求**实例最优**有理倍率及完整精确 NE 证书，位长多项式；异址交叠至多 1 时多项式 | 依赖同址正规形与异址支持区间枚举；[证明](shared/instance_complexity_barriers.md)、[规范实现](../../facility_spe/exact/shared_offdiag.py)、[独立对照](../../tests/test_shared_offdiag.py)。内部证明与有限代码验收分开；外部评审未进行。 |
| SC-TWO-SITE-EXACT | 共同目录至多两个地点，任意正实权与交叠人数，完整精确客户续局 | 存在因子 1 的纯选址 SPE | 异址取任一纯 NE、标签反射、同址对半；三个可选布局分支逐项证。[结构边界](shared/instance_complexity_barriers.md)；本轮内部审读、外部未审。 |
| SC-EQUAL-REACH-EXACT | 共同目录所有地点 reach 相等，任意正实权与交叠人数 | 存在因子 1 的纯选址 SPE | 所有异址共有客户对半混合 NE，选重叠总重最小的地点对。[结构边界](shared/instance_complexity_barriers.md)；本轮内部审读、外部未审。 |
| SC-TWO-REACH-SPARSE | 共同目录每对不同地点最多一共有客户且 reach 至多两种；正实权与完整精确延续 | 存在因子 1 的纯选址 SPE | 高高、高潮低、低低三支异址威胁比较，必要时用 SC-DIAG-NORMAL 改选同址。[结构边界](shared/instance_complexity_barriers.md)；新内部证明，外部未审。 |
| SC-TWO-REACH-MULTI-NO | 共同目录恰三地点、五名正整数权客户、reach 为 $(20,20,16)$；AB 有两名共有客户 | 全部精确 NE 下实例最优因子 $\alpha^*=14/13>1$ | [全异址谱及同址正规形](shared/instance_complexity_barriers.md)；严格攻击删除 SC-TWO-REACH-SPARSE 的交叠条件，不攻击原命题。内部复算，外部未审。 |
| SC-THREE-DEC1-HARD | 共同目录恰三地点、显式正整数客户权、每个带标签布局独立选精确独立混合 NE；判定 $\alpha^*\le1$ | 弱 NP 完全；整数总重参数存在伪多项式算法 | `LOCAL-HARD` 的二次有界子集和源 + AB 双等重、AC 单客户及 BC 硬群，逐项排除三个同址与三个异址。[全证明](shared/three_site_exact_hardness.md)；三条内部独立审查，外部未审。 |
| SC-THREE-DECa-HARD | **对每个事先固定的有理 $1<a<(1+\sqrt3)/2$**，同一三地点共同目录、正整数客户权、完整精确混合 NE 存在量词 | 判定 $\alpha^*\le a$ 弱 NP 完全；不声称把 $a$ 作为输入时统一多项式，**恰三地点**端点和其上未分类 | `LOCAL-HARD` + $R_B>R_A>R_C$、AB/AC 各一共有客户、BC 硬群的完整 YES/NO 守卫；固定余量与正权预算、NP 证书、伪多项式上界。[全证明](shared/three_site_exact_hardness.md)；独立代数攻击和有限算术仅辅助，外部/优先权未核。 |
| SC-FIVE-DECa-HARD | **对每个事先固定的有理 $1<a<\phi$**，两设施同一恰五地点目录、显式正整数权客户，存在逐布局独立精确混合 NE 的完整续局 | 判定 $\alpha^*\le a$ 弱 NP 完全；归约 YES 为 $\alpha^*=a$，NO 为 $\alpha^*>a$。不声称五地点最少、强 NP 困难或固定常数间隙 | 三态 SUBSET SUM 局部源 + 严格强制桥宏客户的双向 NE 引理 + 五地点正私有预算与所有 25 带标签布局守卫 + NP 证书及伪多项式 DP。[全证明](shared/five_site_exact_hardness.md)、[独立内部数学及价值审查](../reviews/facility/five_site_fixed_factor_hardness.md)；有限精确回归与普遍证明分开，外部审查和文献新颖性未核。 |
| SC-GRANULAR-APPROX | 两设施共同非空目录、正实原子权、异址共有客户最大单体权 $\theta<R_{\max}=\max_s w(C_s)$；同址对半、异址可任取精确独立混合 NE | 存在完整规则与纯选址布局，倍率至多 $(R_{\max}+\theta)/(R_{\max}-\theta)$；$R_{\max}=0$ 时精确 | 已知可拆分客户对照的两设施字典序势 + (NE) 每异址坐标误差 $\le\theta/2$。[证明](shared/atomic_granularity.md)；定量界内部两路审读，外部/精确文献优先权未核。 |
| LOCAL-ATOM-WARDROP-k | 任意固定 $k\ge2$ 家设施布局、任意客户可达关系、正实原子权与精确独立混合客户 NE；同一布局上的 Wardrop 可拆分流；$\theta$ 为多设施可达客户最大单体权 | 对**任意**上述两种 NE，逐设施负载误差 $\le(k-1)\theta/2$，链族对每个 $k$ 取等号；**无全 $k$ SPE 结论** | 运输矩阵的净流出与误差排序间隙证明、相邻边单位客户链。[逐式证明](local_and_exact/atomic_wardrop_gap.md)；内部独立审读，已有广义 atomic–Wardrop 文献，精确常数新颖性未核。 |
| SC-SPARSE-3 | 共同目录至多三地点、每对**不同**地点至多一共有客户，正实权上界及正有理权同类下界 | 最优普遍倍率上确界为 $\sqrt2$ | 固定纯异址与重客户同址菜单的三地点矛盾；三客户匹配族排除所有布局/续局。[尖锐分类](shared/small_sparse_catalogs.md)；独立内部审读与精确有限样本，外部未审。 |
| SC-SPARSE-4 | 同上但至多四地点；正实权上界、正有理权同类下界 | 最优普遍倍率上确界为 $\sqrt[3]4$ | 四地点威胁递推得到 $B>rD>r^2C/2>r^3B/4=B$，五客户正有理参数族排除全部十种无序布局。[尖锐分类](shared/small_sparse_catalogs.md)；两路独立内部审读，外部未审。 |
| SC-SPARSE-5 | 同上但至多五地点 | 最优普遍倍率上确界为 $\phi$ | 上界来自 SC-PHI-E；下界只把既有六地点家族的选址目录限制至前五地点、保留六个客户，复用仍合法的十个异址与五个同址排除。[尖锐分类](shared/small_sparse_catalogs.md)、[原下界](shared/sharp_phi_lower.md)；内部审读与实例核对，外部未审。 |
| LOCAL-CHORD-IFF / POLY | 一个固定局部布局，\(U\ge V>\phi U/2\)、公共重 \(C<V/\phi\) 及双配额 | 最大原子二分判别；满足时多项式构造配额 NE | 来源稿：主稿附录已成文；现行重写：[局部强弦全文](shared/local_chord_full.md)覆盖交换、修复、退化端点及位复杂度；内部审读：已记录逐式审读；外部评审：尚未进行。 |
| HC-2-UP | 任意两非空目录（可异构）、正有理权重；纯客户延续 | 四个受保护种子/布局、全目录威胁给出因子 2 | 合法双色弦与任意环两类矛盾；已实现、内部候选。[证明](heterogeneous/README.md) |
| HC-2-LOW | 对每个 \(\alpha<2\)，足够大的正整数族；两边各两地点、可不相交 | 某异构实例最优因子超过 \(\alpha\)，局部严格唯一纯 NE | 六顶点族逐布局收益矩阵；内部候选。[下界](heterogeneous/README.md) |
| HC-2-SHARP | 全体异构目录模型 | 普遍最优因子等于 2 | HC-2-UP **且** HC-2-LOW；不能把该下界移用到相同目录 |
| HC-RHO | **同时**每个合法地点对至多一名公共客户，且至少一侧目录至多两地点 | 普遍尖锐因子 \(\rho=2\cos(\pi/7)\)；上界使用纯延续 | 依赖单交叠严格 2×2 分类、平局、全目录最佳列提升与严格下界族。来源稿：有受限类完整推导；现行重写：[逐分支证明](heterogeneous/restricted_rho.md)明确覆盖零收益、缺失交叠、身份与退化情况；内部审读：已逐式核对本轮重写，仍接受独立反例审查；外部评审：尚未进行。两侧目录均任意大的范围另由 SPARSE-RHO-ALL 闭合。 |
| SPARSE-LONG-CYCLE | **对每个**整数 $n\ge2$，两目录各 $n$ 地点，正整数客户重、每合法跨对最多一公共客户、每格唯一客户 NE；两方真实全目录坐标极小收益的严格最佳回应 | 存在上述实例，其唯一交替回应环经过全部 $2n$ 个带标签行动，任何非空回应封闭核心包含所有行动；**不**推出超过 $\rho$ 的倍率下界 | [显式可实现构造与逐式证明](heterogeneous/sparse_long_cycles.md)；依赖规范模型和 CORE-LIFT 中全目录威胁定义，不依赖 HC-RHO。一般 $n$ 代数已核，$n=2,\ldots,30$ 精确算术交叉复算；外部评审和文献新颖性未核。 |
| SPARSE-HIGH-ACYCLIC | 两目录任意有限非空、每跨对至多一共有客户、任意实 `r≥1`、按带标签 `(reach,priority)` 较小行动接收平局客户的完整纯 NE 规则；**该规则无任何 `r` 稳定布局** | 该规则的全目录最佳回应图中，高行动 `R_s≥M₁/r` 或 `R_t≥M₂/r` 的每条出边按全序严格下降且共有客户满足逐边重量下界；故每个任意长环至少含一低于本方阈值的行动 | [新直接证明与两处假设攻击](heterogeneous/sparse_high_reach_barrier.md)；由局部单客户 NE、全目录最佳回应和有限图推出；无环长度界。精确独立审查 [脚本](../../tests/audits/sparse_high_reach.py)、[记录](../../evidence/runs/2026-10-01/sparse_high_reach.json)；内部逐式审查，未经外部评审。 |
| SPARSE-BALANCED-R | 同上输入、任意实 `r≥1`，**同时**每个 `s∈U₁` 满足 `R_s≥M₁/r`，每个 `t∈U₂` 满足 `R_t≥M₂/r` | 存在纯布局和完整纯客户 NE 续局构成因子 `r` 近似 SPE；特别取 `r=ρ` 给双方任意长 reach 平衡稀疏子类的 `ρ` 上界 | 依赖 SPARSE-HIGH-ACYCLIC 与有限出度一图必有环；[证明](heterogeneous/sparse_high_reach_barrier.md)。一侧平衡不足：原 HC-RHO 下界整数输入在 `r=9/5` 有唯一 NE、最优倍率 `80193772/44504187>r`，但列目录全部高 reach。 |
| SPARSE-RHO-ALL | 任意两非空有限带标签目录、正实权原子客户、每合法跨对至多一共有客户；每格可独立选精确独立混合客户 NE；目录可交、同址且允许零 reach | **任意预先固定**的 `(reach,priority)` 纯客户 NE 全续局规则下存在 `ρ` 近似纯选址 SPE；结合 HC-RHO 的正整数 2×2 严格唯一 NE 下界族，整个 Q-SPARSE 类最小普遍因子恰为 `ρ` | [新全称证明](heterogeneous/sparse_unbounded_rho.md)：依赖规范单客户 NE、SPARSE-HIGH-ACYCLIC、首个高→低边界的身份同一性与 `q(ρ)=0`；下界沿用 HC-RHO，不依赖短目录提升。两条独立推导及多路线敌意审查未发现 fatal；精确有限攻击仅作辅助。来源主稿此前未含此全类证明，外部同行评审/文献新颖性均未核。 |
| SPARSE-BAD-LONG | 对每个固定实数 `3/2<r<ρ` 和每个整数 `n≥1`，存在两边各 `n+1` 个行动、正有理权、每跨对最多一公共客户且每格唯一 NE 的输入 | 全布局均严格违反 `r` 稳定，真实全目录严格唯一最佳回应构成遍历全部 `2(n+1)` 行动的唯一环；即使高行锚客户身份只有一种，也无统一大小的精确回应闭核心 | [显式 7/4 族、一般开参数与逐格证明](heterogeneous/sparse_bad_long_cycles.md)；[精确复现](../../tests/audits/sparse_bad_long_cycles.py)和[冻结记录](../../evidence/runs/2026-10-01/sparse_bad_long_cycles.json)仅算术审查，普遍 `n,r` 依赖证明。仅反驳 `r<ρ` 的坏倍率短核心推广；不与 SPARSE-RHO-ALL 冲突。外部审查/新颖性未核。 |
| SPARSE-BAD-LONG-ALL | **新版本**：对每个固定实数 `1≤r<ρ`、每个 `n≥1`，同类正有理 `(n+1)×(n+1)` 输入；并不声称每个 `A_i` 在较小 `r` 下都属于高区 | 全布局没有 `r` 稳定格，唯一精确 NE 与唯一严格全目录回应环遍历所有行动；高行只借同一客户 `x` 交叠。旧 SPARSE-BAD-LONG 为其严格子命题 | [开参数显式余量、`r=1` 单独转移与有理化证明](heterogeneous/sparse_bad_long_cycles.md)；基于旧构造的五类布局、严格回应与同一身份。新范围靠全称代数，不由冻结的 `7/4` 样本推断；本轮独立审读和逐式复算未见 fatal，外部评审/新颖性未核。 |
| CORE-LIFT | 两领导者有限行动、非负收益；各布局延续可独立选择，两个坐标极小值达到 | 全行动最小收益回应环可缩成保留**全局威胁**的平衡核心，并将核心选择提升回全部行动 | 存在性归约而非自动高效算法；若求真正极小值困难，计算收益并不免费。[直接推导](heterogeneous/core_lift_and_monotone.md) |
| HC-MONOTONE | 异构**纯**延续构造和严格下界族；每名客户两设施使用相同的严格递增实际负载成本，仍强制服务 | 原纯最优反应及严格占优链保留，因子 2 和受限 \(\rho\) 的纯结论可条件迁移 | 不推出任意独立混合 NE 集保持不变；全局候选状态沿用原定理。[范围与推导](heterogeneous/core_lift_and_monotone.md) |
| CERT-SOUND | 一个有效输入、指定在轨 NE、每个实际设施偏离各有精确 NE | 若全部收益不等式成立，可填充其余布局为该实例的 \(\alpha\)-SPE | [模型 §3](model.md)的直接判别。共享 [独立检查器](../../facility_spe/cli/verify_phi.py)定义级重算客户条件成本、偏离及所有默认布局；实例检查仍不证明普遍定理或实例最优。 |
| EXACT-KAPPA | 两设施线性负载模型；\(\kappa=\max_{s\in U_1,t\in U_2}|C_s\cap C_t|\) | 枚举三态支持区间求该实例全混合 NE 延续下的最优因子 | 完整局部支持表示；对 \(\kappa\) 指数，已实现、证明内部候选。[方法](local_and_exact/exact_algorithms_and_extensions.md) |
| MITM-EXACT | 任意局部正有理输入；可接受对公共客户数指数的时间与空间 | 局部极值、再用于全局实例最优 | 中途相遇枚举/单谷目标；研究实现，指数最坏界 |
| DP-W / LOCAL-HARD | 固定局部布局，公共权重为正整数，总重 \(W\)；困难性用二进制编码 | \(O(n^2W+n\log n)\) 的伪多项式谱 DP；局部最小收益弱 NP 困难 | 二者相容；不推出 SC-PHI-A 或 HC-2-UP 的困难性 |
| FPT-D | 局部输入有 \(d\) 种显式有理权重 | 固定维整数规划归约给出参数化局部方法 | 内部推导、**尚无实现** |
| QUAD-EQ / QUAD-PHI | 恰好两设施、强制服务，每客户两设施使用同一严格递增二次函数 | 局部客户均衡约束与线性模型等价；共享 \(\phi\) 迁移仍**条件于 SC-PHI-E** | 代数恒等式为直接推导；一般凸成本不获同一结论 |
| POLY-CONT | 两领导者收益非负，每布局可独立选延续，收益集合显式多项式个有理多面体 | 坐标优化可求第一阶段最优因子；给出客户策略还需有效实现过程 | 内部推导、**尚无实现** |

| SC-K-2-E | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | For every k>=2 and every positive-weight common-catalog instance, some labeled layout and complete exact independent-mixed continuation have factor <=2; on-path site-uniform and every off-path NE pure. No polynomial-time or sharpness claim. | [Full proof](multi_facility/uniform_two.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| SC-K-LEX-BUDGET | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | Every global lexmax site-uniform feasible profile is an exact client NE; every deviator has positive on-path load when maximum reach is positive, with all four transfer inequalities including singleton-source clients. | [Full proof](multi_facility/uniform_two.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| MF-PACK-2 | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | For all a>0 and h>=1, weights totaling <=(h+1)a fit h bins of load <=2a except isolated singleton weights >2a, by pair merging. | [Full proof](multi_facility/uniform_two.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| MF-PURE-CAP | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | At any fixed layout, isolated atoms heavier than B and ordinary loads <=B form a strict-improvement invariant; a pure exact NE exists in that invariant, for every B>0. | [Full proof](multi_facility/uniform_two.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| MF-CONT-COMPLETE | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | Exact on-path NE plus one exact NE at each actual deviation extend to a single complete rule; distinct coordinate deviations are distinct labeled layouts and all default subgames have pure NE. | [Full proof](multi_facility/uniform_two.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| SC-K-SYMMETRIC-MENU-OBSTRUCTION | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | For each q>=3, the three-site weights q^2,1,q-1/4 yield a lexmax on-path witness with symmetric-menu ratio q^2/(q-1/4)>q after B->T, but alpha*=1 in the full model. | [Full proof](multi_facility/symmetric_menu_obstruction.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| SC-K-LEXMAX-BARRIER | See exact domain and quantifiers in [branch claim identity](multi_facility/claims.md). | For every k>=2,h>=2, the explicit k-site family has unique lexmax occupancy up to labels with optimal factor 2h/(h+1) under all on/off-path NE choices, but full-instance alpha*=1 at another layout. | [Full proof](multi_facility/lexmax_boundary.md); complete new internal proof; independent reverse/code attack; no external review or priority certification. |
| MF-PURE-CAP-POLY | Given an explicit rational fixed-layout pure assignment with all loads above B consisting of one atom of weight above B and all other loads at most B. | Bit-polynomial exact pure NE with the heavy atoms fixed and all ordinary loads still at most B. This conditionally completes the off-path part of SC-K-2-E. | [Full import and proof](multi_facility/polytime_frontier.md): STOC 2004 restricted identical-link Nashification after removing heavy facilities; internal reverse check, no new software or external review. |
| SC-K-LEXMAX-STRONG-HARD | Integer positive weights, arbitrary explicit k=site count, equal site reaches; threshold on minimum load of global site-uniform lexmax. | The exact selection-oracle threshold is strongly NP-complete by 3-PARTITION. The reduction instances themselves admit a polynomially obtainable exact SPE; no hardness for finding a factor-two witness follows. | [Complete reduction and boundary](multi_facility/polytime_frontier.md); internal independent check, external review and novelty not recorded. |
| SC-K-LOCAL-PLS | Explicit binary rational common-catalog arbitrary-k input; legal site-uniform profiles, one-customer site transfers and canonical one-facility moves. | Any local lex maximum has exact on-path customer NE and all four transfer budgets; factorial-scaled radix objective places this sufficient-state search in PLS. No polynomial convergence or PLS-hardness is claimed. | [Neighborhood, bit objective and proof](multi_facility/polytime_frontier.md); internal reverse review, external review not recorded. |
| SC-K-GREEDY-BUDGET | Arbitrary explicit common-catalog k and positive rational weights, maximum reach positive; feasible site-uniform state without on-path NE requirement. | The new-coverage / occupancy-division greedy procedure produces positive loads and all four transfer budgets in polynomial time. Its chosen layout need not admit an on-path customer NE retaining those budgets; no factor-two algorithm follows. | [Full last-insertion proof and four-customer interface counterexample](multi_facility/polytime_frontier.md); internally reviewed, no software or external review. |
| SC-K-GREEDY-MAX-MULT | Same greedy *initial* site assignment, any positive weights and arbitrary k. | Every served client is initially assigned to a covered occupied site of maximum final facility multiplicity, by comparing site opening weights and the later site's final insertion score. The property need not persist after customer repair and does not solve factor two. | [Exact time-order proof](multi_facility/polytime_frontier.md); direct internal check, no external review. |
| SC-K-GREEDY-UNOPENED-2 | Same common-catalog model and fixed greedy occupancy; every prefix of strict site-level customer improvement from the greedy assignment, including a terminal exact site-uniform NE. | All loads remain at least the last insertion score gamma, and any unopened target has N_r<=gamma. For a singleton source, the newly covered plus surviving source customers that target covers weigh at most 2a. This repairs only the empty-target deviator cap, not occupied-site packing or polynomial NE search. | [Exact proof and remaining obligations](multi_facility/polytime_frontier.md); internal algebraic cross-check, no external review or implementation. |
| SC-K-EQUAL-MULT-GREEDY-2 | Arbitrary explicit common-catalog k whose greedy output has the same occupied-site multiplicity q>=2 everywhere. | Bit-polynomial 2-SPE construction: site-level identical-machine Nashification preserves q gamma <= W_t <= (q+1) gamma and yields an exact mixed on-path NE; all source sites survive, so the old occupied/unoccupied budgets and polynomial off-path cap repair apply. Conditional on the greedily recognizable subclass, not all instances. | [Full proof and primary theorem import](multi_facility/polytime_frontier.md); independent internal inverse review; no implementation or external review. |
| SC-K-DISTINCT-GREEDY-3 / SC-K-DISTINCT-GREEDY-2 | Arbitrary explicit common-catalog k whose greedy output occupies k different sites. | Old factor-three proof remains true but is superseded on this exact output class: first maximum-reach R site keeps an R/2 candidate score, so range-preserving identical-link Nashification gives every on-path facility at least R/2; **any** off-path NE gives a deviator at most R. Bit-polynomial factor-two complete continuation. | [Both proofs and scope](multi_facility/polytime_frontier.md); independent internal reverse check, no implementation or external review. |
| SC-K-COMPONENT-MULT-GREEDY-2 | Greedy occupied-site customer-overlap graph has constant q within each component; q=1 components must be singletons. Positive rational common-catalog arbitrary k. | Original bit-polynomial 2-bound remains true. Its singleton restriction is now **removed by the newer range-certificate theorem**, which uses a different pooled-source budget; do not silently change this old claim's assumptions. | [Original componentwise proof](multi_facility/polytime_frontier.md); independent internal inverse review, no implementation or external review. |
| SC-K-RANGE-GREEDY-2 / SC-K-LIGHT-COMPONENT-GREEDY-2 / SC-K-GREEDY-HEAVY-OVERLAP-2 | Final greedy multiplicity groups q with initial per-facility extrema alpha_q,beta_q; every initial customer i passes beta_q_i-w_i/q_i<=alpha_q_v for its cross-q occupied alternatives. Light-overlap constant-q and all cross-q weight>=gamma are sufficient special cases. | Groupwise restricted identical-machine Nashification and a pooled singleton-site bound give a **bit-polynomial factor-two full exact continuation**, including multi-site q=1 components and some light cross-q clients. The cross-q range condition is checked from greedy output and need not hold for all inputs. | [Statement, all-source proof and strict example](multi_facility/polytime_frontier.md); internal inverse review, no implementation or external review. |
| SC-K-GREEDY-STATIC-PACK-NO | One explicit positive-integer common-catalog instance, five sites and eight facilities, greedy tie order A,E,B,C,D; reachable exact site-uniform customer NE. | A B facility has a=41/2; after its departure B survives, but frozen site E has two clients 20+24=44>2a=41 and no isolated macro. Thus original per-site cap packing does not follow from arbitrary greedy-layout NE repair. It does not rule out cross-site reassignment or factor two. | [Instance, strict moves and all NE checks](multi_facility/polytime_frontier.md); exact independent arithmetic, no external review. |
| SC-K-GREEDY-CAP-INFEASIBLE | Six sites, eight facilities, ten positive-integer customers; greedy tie order A,E,B,C,D,G, a reachable exact site-uniform NE and B-to-G deviation. | For a=41/2, every feasible pure off-path assignment places a shared 24 with a forced private 20 on one of B,E,G, making a non-macro load 44>2a. Global MF-PURE-CAP-POLY initialization is impossible for that deviation, even with cross-site reassignment; an explicit exact NE has deviator load 20. This is a method obstruction only. | [Full integer instance, proof and off-path NE](multi_facility/polytime_frontier.md); independently recomputed exact arithmetic, no external review. |
| SC-K-GREEDY-REPAIR-ORDER-NO / SC-K-GREEDY-HEAVIEST-NO | Two explicit six-site, eight-facility, ten-positive-integer-client inputs, with a specified strict improvement path or the uniquely heaviest-improving path from greedy. | Both end at exact customer NEs where B→G gets 176 in **every** mixed NE: ratios 32/15 and 88/43. A different one-step reachable NE at the same respective greedy layout preserves the four transfer budgets. Only the proposed arbitrary/maximum-weight repair rules fail, not the greedily selected occupancy itself. | [Full exact proof](multi_facility/polytime_frontier.md), two JSON inputs and independent Fraction audits; no external review. |
| SC-K-TWO-SITE-COMPONENT-GREEDY-2 | Greedy occupied-site overlap components have either constant facility multiplicity or at most two sites, which may have unequal multiplicities; positive rational common-catalog input and explicit arbitrary k. | A descending-weight, one-pass strict high-q-to-low-q repair yields exact on-path NE and preserves the greedy load box on unequal pairs; constant-q components use restricted identical-link Nashification. Orphan-aware packing and capped completion give an input-bit-polynomial factor-two full exact continuation. Mixed components with at least three sites remain outside the theorem. | [All-source proof and range-condition separation](multi_facility/polytime_frontier.md); internal reconstruction, no external review or canonical implementation. |
| SC-K-ALL-OR-ONE-COMPONENT-GREEDY-2 | Greedy occupied-site overlap components each have constant q or every client has exactly one occupied option or all sites of its component. Positive rational common-catalog input, explicit arbitrary k; arbitrary component sizes and mixed q in the latter case. | Descending-weight assignment of all-site common clients to a current minimum normalized load yields an exact site-uniform NE, preserves the greedy final load box, and uses the private reserve of every singleton non-first site to prove occupied-target orphan budgets. Existing capped off-path completion yields a bit-polynomial full exact factor-two rule. It includes the two-site theorem's output class and a strict three-site q=(3,2,1) example outside RANGE. | [Full list-assignment, load-box and all-source proof](multi_facility/polytime_frontier.md); independent internal reverse audit, no external review or canonical implementation. |
| SC-K-NESTED-ANCHOR-GREEDY-2 | Each greedy overlap component has constant q or its first-opened H covers every multi-option customer and their occupied option sets form an inclusion chain **expanding in nonincreasing weight order**; explicit rational common-catalog arbitrary k. | Restricted minimum-normalized-load list assignment preserves all site load boxes and gives exact client NE by the last-assigned-customer inequality. A singleton source retains a private reserve for all orphan budgets; polynomial capped completion yields a full exact factor-two continuation. Strictly includes ALL-OR-ONE and a three-site partial-overlap instance outside RANGE. Reversing two option sets breaks the unrestricted list rule, not the layout. | [Exact conditional proof and method boundary](multi_facility/polytime_frontier.md), [integer data](../../examples/multi_facility/greedy_nested_anchor.json), [Fraction audit](../../tests/audits/kfac_nested_anchor.py); independent internal inverse check, no external review or canonical implementation. |
| SC-K-GREEDY-SINGLETON-RESET | Any greedy layout with gamma>0; a q=1 source facility has arbitrary on-path expected payoff a>=gamma, even if the on-path client profile is independently mixed. | Reset the **off-path** old customers to greedy's original assignment; first singleton opening bounds each surviving q=1 customer pool by 2gamma, higher-q original sites survive and are packable, and greedy (8) caps an unopened deviator at W_u^0<=2gamma. Polynomial capped Nashification gives a pure exact deviation NE with deviator at most 2gamma<=2a. It does not select an on-path NE. | [All-target constructive proof](multi_facility/polytime_frontier.md); independent internal inverse review, no external review or canonical implementation. |
| SC-K-GREEDY-BOX-TO-2 | Greedy occupancy, positive gamma, and an **explicit** site-pure/uniform exact on-path client NE with every occupied total in [q_t gamma,(q_t+1)gamma]. | All q>=2 sources use the box for stationary packing; all q=1 sources use SINGLETON-RESET. This gives a bit-polynomial full exact factor-two continuation without singleton private reserve or a specified repair path. Universal feasibility is now SC-K-GREEDY-BOX-EXISTS; general input-bit-polynomial selection remains open. | [Complete conditional interface](multi_facility/polytime_frontier.md); internal inverse review, no external review. |
| SC-K-UNIFORM-LIGHT-FLOW-2 | Greedy layout on arbitrary explicit rational common-catalog k; all customers with at least two occupied options and weight **below gamma** have one common weight delta<gamma. All other weights, incidence and multiplicities are unrestricted. | Integral convex-cost flow with per-site lower bound q_t gamma minimizes the exact client potential; a reverse path in the original-to-final equal-unit transport proves every upper bound (q_t+1)gamma. Heavy clients are already at NE; BOX-TO-2 gives a bit-polynomial full exact factor-two continuation including q=1 without private reserves. A strict three-site H--M--L instance is outside RANGE, ALL-OR-ONE and NESTED-ANCHOR. | [Network, reverse-path proof and limitations](multi_facility/polytime_frontier.md), [integer input](../../examples/multi_facility/greedy_uniform_light_flow.json), [Fraction audit](../../tests/audits/kfac_uniform_light_flow.py); independent internal inverse attack, no external review or canonical implementation. |
| SC-K-STAR-LIGHT-GREEDY-2 | 贪心轻客户交叠分量各自同重数，或为中心先开的星形且每名轻多选项客户恰选中心和一叶；任意正有理权、显式 $k$；跨分量重客户任意 | 各叶权重递减队列、可改善叶的最低当前负载优先，每名轻客户至多处理一次；产出盒内精确客户 NE 和位长多项式完整 2 倍续局 | 依赖 SC-K-GREEDY-MAX-MULT、同重数机器均衡修复和 SC-K-GREEDY-BOX-TO-2；[完整证明](multi_facility/polytime_frontier.md)、[分离旧条件类的整数输入](../../examples/multi_facility/greedy_star_edges.json)、[精确算术审查](../../tests/audits/kfac_star_edges.py)；内部独立逆审，外部未审，规范算法软件未实现。 |
| SC-K-TWO-LIGHT-LOWER-POTENTIAL-NO | 正整数共同目录族：七设施、四占站、仅两名不同轻权多选项客户；参数 $n\ge45$ 为 5 倍数 | 贪心初态是盒内精确 NE；施加全部下盒后的全局客户势最小值唯一越过 L 上盒一单位，只排除这一选均衡规则 | 依赖 MF-MODEL、SC-K-GREEDY-BUDGET、势恒等式；[四态解析证明](multi_facility/polytime_frontier.md)、[整数输入](../../examples/multi_facility/greedy_two_light_potential.json)、[精确审查](../../tests/audits/kfac_two_light_potential.py)；内部复核、外部未审；未否定盒内 NE 或全输入 2 倍构造。 |
| SC-K-DESCENT-ONLY-TRAP-NO | One six-client, three-site, six-facility positive-integer input with strict greedy trace and q=(3,2,1); from its greedy assignment allow strict customer transfers only to weakly lower-multiplicity occupied sites. | The unique maximal downward path ends at weights (64,46,27), where a weight-2 client strictly wants the upward return L→M, 25>23. One return yields exact NE (64,48,25). Thus downward-only repair and the pair-scan no-return argument do not extend to this partial-overlap three-site chain; no factor-two layout failure follows. | [Full forced-move arithmetic](multi_facility/polytime_frontier.md), integer JSON and independent exact branch audit; no external review. |
| SC-K-GREEDY-FIXED-LEXMAX-NO | The first six-site repair-order instance, its fixed greedy occupancy, and lexmax **only over site-pure/uniform customer assignments**. | The unique maximizer even of minimum per-facility load is the bad exact on-path NE with B→G forced payoff ratio 32/15 in every mixed off-path NE; another exact on-path NE at the same layout has factor two. This limits a fixed-layout customer-selection rule, not global layout lexmax or all independent-mixed on-path profiles. | [Exact uniqueness proof](multi_facility/polytime_frontier.md), 16-state independent Fraction audit; no external review. |
| SC-K-GREEDY-FIXED-POTENTIAL-NO | A second six-site, eight-facility positive-integer input at its greedy occupancy; global minimization of the exact weighted improvement potential **over all site-pure/uniform customer assignments**. | There are exactly two on-path customer NEs; their exact potential values are 86264 (good, all budgets) and 86200 (bad). Every global minimum is an NE, so the bad one is uniquely chosen and its B→G deviation forces ratio 215/107>2 in every exact independent-mixed off-path NE. This is a fixed-layout selection obstruction, not failure of the greedy layout. | [Potential identity, complete two-NE proof](multi_facility/polytime_frontier.md), integer JSON and independent 16-assignment Fraction audit; no external review. |

| SC-K-RESET-PACK-INTERFACE | 贪心布局任意精确独立混合在轨 NE、每设施收益至少 $\gamma$；原始每个 $q_u\ge2$ 客户池可显式装成 $q_u-1$ 个不超 $2\gamma$ 的普通箱或独立宏箱 | 偏离后重置初始贪心客户池，原站删席箱及其他站原预算接入多项式纯 NE 修复；完整精确 2 倍续局位长多项式 | [全偏离证明](multi_facility/polytime_frontier.md)；内部两路逆审；外部未审、规范软件未实现。 |
| SC-K-DOUBLE-LPT-GREEDY-2 | 对原始贪心客户池分别运行 $q_t$ 箱、$q_t-1$ 箱确定性 LPT；首轮每箱至少 $\gamma$，删席轮每箱至多 $2\gamma$；任意交叠与异权 | 首轮输入同速受限机器多项式 Nashification 保留最小设施收益，RESET-PACK 完成全部偏离；输入位长多项式 2 倍算法，所选在轨 NE 可以越站点上盒 | [证明及三角分离例](multi_facility/polytime_frontier.md)、[精确审查](../../tests/audits/kfac_double_lpt.py)；内部独立逆审、外审及规范实现未完成。 |
| SC-K-PATH-EDGE-LIGHT-GREEDY-2 | 轻客户交叠分量或同重数，或按贪心开启顺序成为有向路径；每人恰有边的两个选项，每条边内同权但跨边可异权；重客户任意 | 每名轻客户最多一次向后开站严格改派，盒保持且同边客户永不返；终局精确 NE 加 BOX-TO-2 得位长多项式完整 2 倍续局 | [证明与 P4 例](multi_facility/polytime_frontier.md)、[精确审查](../../tests/audits/kfac_path_edges.py)；内部独立逆审、外审及规范实现未完成。 |
| SC-K-BOX-NE-FPT-TYPES / SC-K-FROZEN-LIGHT-FPT | 固定贪心占站数 $m$ 与多选项客户不同权数 $d$；或冻结重客户、每个轻分量站数 $c$ 和权数 $d$ 有界 | 类型计数和支持二元变量给站纯/站内均匀**盒 NE**的完整固定布局 FPT 判定；冻结重客户的分量版 FPT 选择器保持原作用域；普遍贪心盒可行性现由 SC-K-GREEDY-BOX-EXISTS 独立提供 | [整数规划及量词](multi_facility/type_compression.md)；Lenstra 原定理为外部导入；内部逆审、外部未审，未实现规范求解器。 |
| SC-K-CATALOG-WEIGHT-XP-2 | 共同地点总数 $p$ 与输入不同权数 $d$ 固定；任意显式 $k$ 与客户数 | 类型计数组合穷举全部占据向量及站纯状态并选精确全局 lexmax；借既有证明输出完整 2 倍证书，运行时 $N^{f(p,d)}$，对固定 $p,d$ 位多项式，**不声称联合 FPT** | [证明及边界](multi_facility/type_compression.md)；内部逆审，外审及规范实现未完成。 |

| SC-K-THREE-SITE-CHAIN-BOX-EXISTS | 贪心轻客户分量恰为先开顺序 $H\to M\to L$ 三站链；每名轻客户选 HM 或 ML，每条边内部客户允许任意异重；重客户冻结 | 在全部贪心上下盒内最小化精确客户势的**每个**全局最小点都是精确 NE，故有盒 NE 和存在性的完整 2 倍续局；没有证明求全盒势最小点的位多项式算法 | [整批上游退回交换证明](multi_facility/three_site_chain_box.md)；内部独立逆审，外审及软件未完成。 |

| SC-K-CONVERGING-PATH-BOX-2 | 贪心轻交叠分量为四站汇聚路径 D--B--A--C，三条边各恰一名轻客户，初始站 D/B/C，重数 $q_D\ge q_B\ge q_A=q_C$，A 原负载恰下盒 | 首轮 Z 判断后分 T 先动或 X 先动，至多七次严格改派都保持完整盒，终局精确 NE；与 BOX-TO-2 组合得位长多项式完整 2 倍续局。只覆盖指定三客结构 | [全分支证明](multi_facility/converging_path_box.md)、[精确有限态审查](../../tests/audits/kfac_converging_path.py)；内部逆审，外审/规范实现未完成。 |

| SC-K-HEIGHT-TWO-BOX-EXISTS | 贪心轻客户均恰有两个占站选项，按站点首开先后定向后的图中每条有向路径至多两条边；任意分叉、汇合及各边任意异轻权 | 完整贪心盒内的**每个**客户势全局最小点都是真正客户 NE；从而存在盒 NE 与完整 2 倍续局。整批退回上游来源池的 first-crossing 交换给出严格降势；**未证明位长多项式求最小点** | [全证明](multi_facility/height_two_box.md)；两路独立内部逆审，外审、优先权和规范实现未完成。 |
| SC-K-INCIDENCE-BOX-DP | 显式正有理共同目录输入、贪心正 reach；冻结权至少 `gamma` 与单占站选项客户；剩余轻客户—已占站**逐名**二部图的树宽 `tau` 和两侧最大度 `d` 均固定 | 精确判定并构造站纯/站内均匀全盒客户 NE，位长多项式；不可行时只否定这个固定客户的盒内选择器 | [约束、分解与位复杂度](multi_facility/bounded_incidence_box.md)；Bodlaender 固定树宽算法为导入，内部逆审，无外审或规范软件。 |
| SC-K-HEIGHT-TWO-INCIDENCE-2 | 上一行全部条件；另每名轻客户恰有两个已占选项，首开定向后的最长有向路径至多两边 | 浅层存在性、关联 DP 与盒内离轨接口合取，位长多项式构造因子 2 布局及**完整精确客户 NE 续局**；不声称全输入算法 | [组合证明](multi_facility/bounded_incidence_box.md)和[浅层存在性](multi_facility/height_two_box.md)；两路内部逆审，无外审与规范实现。 |

| SC-K-CONVERGING-PATH-4MOVE-2 | 贪心轻分量 D--B--A--C 每边恰一轻客户，初始站 D/B/C，开启方向 D→B→A←C；重数按边非增，但 A 无需紧下盒、A/C 重数可不同 | 固定次序检查 Z、T、X、可能新改善的 T、可能返程的 Z，**至多四次**严格改派保持盒并完成 NE；BOX-TO-2 得位长多项式完整 2 倍续局，严格扩大旧七步小类 | [全分支证明](multi_facility/converging_four_moves.md)、[广范围精确有限审查](../../tests/audits/kfac_converging_four_moves.py)；内部逆审，外审/规范实现未完成。 |
| SC-K-LOCAL-WEIGHT-BOX-DP | 正有理共同目录输入及固定贪心占据；冻结单选项与权重至少 `gamma` 的客户；轻客户的地点 primal 图树宽 `tau`、每站不同轻权种类数 `d` 固定 | 站点最终权重计数及部分计数的树分解 DP 位长多项式精确判定、构造站纯/站内均匀盒内客户 NE；与浅层存在性和 BOX-TO-2 合用得交集类完整 2 倍续局；否结果只限定冻结客户的站纯盒 | [完整约束及证明](multi_facility/local_weight_box_dp.md)；内部复核，外审、优先权核查及规范实现未完成。 |
| SC-K-INWARD-STAR-2 | 正有理共同目录贪心布局；轻客户分量是每名客户连接先开叶和后开中心的星形，异权和叶数不受限，重客户冻结 | 按叶内降权队列和动态最大键每客处理一次，保持完整盒与所有客户最佳反应；BOX-TO-2 位长多项式给完整精确 2 倍续局 | [证明及无界中心权种族](multi_facility/inward_star_box.md)；内部复核，外审、优先权核查及规范实现未完成。 |
| SC-K-BOX-POTENTIAL-STRONG-HARD | 正整数共同目录输入；贪心全站各一设施、全部可动轻客户覆盖所有占站，且其所有分配自动满足完整盒 | 精确求全盒客户势全局最小值的阈值判定强 NP 完全；同一归约族仍有易求精确设施均衡，不能推出寻找盒内 NE 或完整 2 倍证书困难 | [3-PARTITION 归约及严格范围](multi_facility/polytime_frontier.md#sc-k-box-potential-strong-hard-exact-boxed-potential-optimization)；内部代数复核，外审未完成。 |

## SC-K-RQ-MIXED-BOX -- mixed-multiplicity selector obligation

**Objects/domain:** a greedy common-catalog occupancy with explicit positive rational weights, occupied-site multiplicities `q_t`, and a candidate load box `q_t gamma <= W_t <= (q_t+1) gamma`.

**Exact obligation:** construct, in input-bit-polynomial time, a site-pure/within-site-uniform customer assignment satisfying `(W_t-w_i)/q_t <= W_v/q_v` for every assigned customer `i:t` and every covered occupied alternative `v`, or replace the box interface by a different factor-two certificate. Equal `q_t` is exactly the restricted-identical-link subproblem.

**Current status (2026-10-07):** SC-K-GREEDY-BOX-EXISTS supplies universal feasibility and a finite exact constructor; SC-K-BOX-STRUCTURED-POLY-2 closes the two bounded-structure DP classes. General input-bit-polynomial total time remains open.

**Boundary/evidence:** the restricted-related-link inequality `W_t/s_t <= (W_v+w_i)/s_v` is not equivalent when multiplicities differ; `q_t=1,q_v=2,w_i=2,W_t=5,W_v=6` is an exact mismatch. [Boundary note](multi_facility/restricted_related_link_boundary.md) and [audit](../../tests/audits/restricted_related_formula.py). This is an open obligation and literature boundary, not a hardness theorem.



## 加权拥塞：精确范围与分开登记的审查

| ID | 结论入口 | 当前状态 | 条件与证明 |
| --- | --- | --- | --- |
| OC-INTERFACE-v1 | Odd-ring full-state and positive coefficient certificate | complete current proof, independently reconstructed and exactly audited; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| OC-AMPLIFIER-LIMIT-v1 | Linear reset gives an infinite d/log d lower bound | complete current proof, independently reconstructed and exactly audited; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| OC-AMPLIFIER-ENVELOPE-v1 | Explicit E_d is excluded at its endpoint | complete current proof, independently reconstructed and exactly audited; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| OC-LIGHT-FORCING-EXACT-v1 | A failed hub edge gives a real approximate equilibrium | complete current proof, independently reconstructed and exactly audited; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| OC-INTERFACE-BARRIER-v1 | Sharp leading order inside the forcing certificate | complete current proof, independently reconstructed and exactly audited; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R1-INTEGER-TRIAD | Integer quadratic triad has exact pure factor 286/267 | complete proof and exact replay; independent frozen review not recorded; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R1-RESOURCE-SUPPORT | Bounded resource user support gives r-PNE | complete proof and exact replay; independent frozen review not recorded; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R1-SOURCE-D2-ENVELOPE | Source equation (3) at d=2 has ceiling 19/18 | complete self-contained proof, internally reconstructed and exactly checked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R2-DENSITY-MOMENT | Sharp finite sparse power-moment inequality v1 | complete general proof, independently internally checked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R2-WEIGHT-DENSITY | Resource-local weight-density PNE existence v1 | complete general proof, independently internally checked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R2-RESOURCE-POWER-BRIDGE | Sparse power / ordered resource bridge | complete stated-scope proof, independently internally reconstructed and exactly checked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R2-POWER-PATH-OBSTRUCTION | Fixed sublinear power multiplier path obstruction | complete stated-scope proof, independently internally reconstructed and exactly checked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R2-AFFINE-TWO-TYPE | Sharp affine two-type marginal certificate | complete stated-scope proof, independently internally reconstructed and exactly checked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| R3-SOURCE-SHARP-ASYMPTOTIC-v1 | Sharp source-envelope asymptotic | complete current proofs, independently internally attacked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-FULL-TOPOLOGY-REDUCTION-v3 | Full symmetric topology reduction | complete current proofs, independently internally attacked; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-SOURCE32-178-v1 | Source d=32 full-parameter upper bound | complete exact statements with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WCF-R3-CROSS32-AUDIT-v1 | Four-player degree-32 strict 9/5 obstruction | complete exact statements with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WCF-R3-FIXED-DEGREE-FAIL-v1 | Fixed crossover coefficients do not preserve 9/5 | complete exact statements with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-CROSS32-TOPOLOGY-SEPARATION-v1 | Crossover exceeds the entire symmetric degree-32 topology | complete exact statements with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-DENSE-SHARE-v1 | Shapley share ordering and local weight envelope | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-DENSE-LOCAL-v1 | Resource-local R-PNE through Shapley potential | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-DENSE-POT-SHARP-v1 | Sharpness of the specified R Shapley selector | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-BAND-CURL-v1 | Separate band normalization violates ordinary potential integrability | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-BAND-LINEAR-v1 | Linear selected-potential loss across dense singleton bands | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WCF-R3-SCALED-ORIGINAL-v1 | Original crossover shrinking-weight constant family | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WCF-R3-SCALED-RETUNED-v2 | Retuned constant family and stronger uniform starting index | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WCF-R3-SCALED-TEMPLATE-v1 | Cubic feasibility boundary of the prescribed witnesses | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-POTENTIAL-DENSITY-PADDING-v1 | Potential-density padding preserves the entire existence question | complete stated-scope proofs with independent internal reconstruction; unrefereed | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-ODD-RING-CERTIFICATE-v1 | Odd-ring all-state and rational-coefficient certificate | complete general proofs with independent internal reconstruction; unrefereed; global priority unverified | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-ODD-RING-ENVELOPE-v1 | Exact degree-dependent odd-ring certificate envelope | complete general proofs with independent internal reconstruction; unrefereed; global priority unverified | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-ODD-RING-LOWER-v1 | Full-model growing lower bound with leading constant one | complete general proofs with independent internal reconstruction; unrefereed; global priority unverified | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-ODD-RING-POLYNOMIAL-ENVELOPE-v1 | Mixed polynomial shapes preserve the exact ring-test envelope | complete stated-scope proof with independent internal attack; unrefereed; global priority unverified | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |
| WC-R3-ODD-RING-SINGLETON-UPPER-v1 | Singleton cohorts admit a stable defect state | complete restricted existence proof with internal reconstruction; unrefereed; priority unverified | [精确身份](../weighted_congestion_frontier/CLAIMS.md)；[现行内容](weighted_congestion/README.md) |

| WC-ENVELOPE-CEILING | Source two-attack finite ceiling | complete restricted proof; internally reviewed; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](weighted_congestion/source_ceiling/README.md) |
| WC-R1-LF-SHARP | R1 source-envelope sharp candidate | complete account; stated extension review pending; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](../questions/weighted_congestion/source_envelope_candidate/sharp_envelope.md) |
| WC-R1-PREFIX-SMOOTHING | Nonnegative-polynomial prefix curvature obstruction | complete restricted proof; internally reviewed; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](weighted_congestion/polynomial_curvature/three_load_curvature_bound.md) |
| WC-R1-THREELOAD-ENVELOPE | Exact three-load polynomial tradeoff | complete account; stated extension review pending; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](weighted_congestion/polynomial_curvature/three_point_polynomial_envelope.md) |
| WC-R1-HET-ENDPOINT-REDUCTION | Heterogeneous endpoint certificate reduction | complete restricted proof; internally reviewed; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](weighted_congestion/heterogeneous_endpoint/endpoint_reduction.md) |
| WC-R1-DAG-STEP | Exact auxiliary step-DAG threshold | complete restricted proof; internally reviewed; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](weighted_congestion/step_dag/step_dependency_threshold.md) |
| WC-R1-MULTICOLUMN-2 | Balanced multicolumn escape | complete restricted proof; internally reviewed; unrefereed | [完整身份](../weighted_congestion_frontier/CLAIMS.md)；[正文](weighted_congestion/multicolumn/complement_column_escape.md) |

| WC-R1-MULTIPLIER-BARRIER | 任意玩家乘子的有限多尺度边际夹逼障碍 v1 | complete stated-scope proof with independent reconstruction and exact finite audit; unrefereed | [完整现行证明](weighted_congestion/separable_ordinal_obstruction.md)、[独立攻击](../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md)；全类目标仍开放 |

| WC-R1-GAME-SPECIFIC-SEPARABLE-ORDINAL-BARRIER | 依完整游戏选择的资源可分严格序势障碍 v1 | complete stated-scope proof with independent reconstruction and exact finite audit; unrefereed | [完整现行证明](weighted_congestion/separable_ordinal_obstruction.md)、[独立攻击](../reviews/weighted_congestion/ordinal_potentials/game_specific_independent_attack.md)；全类目标仍开放 |

| WC-ACTION-SIGNATURE-COMPRESSION-v1 | 有限动作的资源签名压缩 | complete general proof; independently reconstructed and exactly audited; unrefereed | [精确模板与证明](weighted_congestion/template_certificates/finite_action_duality.md)、[独立攻击](../reviews/weighted_congestion/template_certificates/finite_action_duality_review.md)；固定权重/动作数，任意资源数，无全类倍率。 |
| WC-ALLSTATE-SELECTOR-ALTERNATIVE-v1 | 全状态择证的精确线性替代 | complete general proof; independently reconstructed and exactly audited; unrefereed | 同上；全状态selector逐一取dual，非单环或单selector的全类推断。 |
| WC-GAME-SPECIFIC-MINIMIZER-EQUIVALENCE-v1 | 依游戏最小点选择与近似纯均衡存在等价 | complete elementary proof; independently checked and exactly audited; unrefereed | [一般等价证明](weighted_congestion/separable_ordinal_obstruction.md)第四节及[范围审查](../reviews/weighted_congestion/ordinal_potentials/minimizer_scope_review.md)；不提供新的α(d)。 |


## 高次费用与最小个体份额

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| WC-HIGH-DEGREE-SHARE-v1 | 任意MODEL有限游戏；按每资源真实最低正次数、潜在权份额定义λ_e，零/常数/无人资源取1。 | 每单方势局部min为max λ_e^−1-PNE；纯d次非存在须有严格小份额；固定正权向量、最低次数增长的保证对全部有限拓扑一致趋1。不是全类匹配界。 | [完整正文](weighted_congestion/high_degree_share.md)、[冻结独立攻击](../reviews/weighted_congestion/high_degree_share_review.md)，完整内部证明，未外审/未认证新颖性。 |

## 严格反例的整数规范形与普遍阈值端点

| ID | 精确范围与结论 | 状态与权威正文 |
| --- | --- | --- |
| WC-INTEGER-MONOMIAL-COUNTEREXAMPLE-v1 | 每个固定d≥0、实α≥1，全MODEL无α-PNE反例存在，当且仅当正整数权、单位x^k资源、非空策略反例存在；不保资源数或精确β。 | complete direct proof; independently reconstructed and exactly audited; unrefereed；[完整身份与证明](weighted_congestion/template_certificates/integer_counterexample_normal_form.md)、[独立攻击](../reviews/weighted_congestion/template_certificates/integer_counterexample_normal_form_review.md)。 |
| WC-UNIVERSAL-THRESHOLD-ENDPOINT-v1 | 单实例可行倍率[β(G),∞)，全类为[a_*(d),∞)，a_*等于规范形β的上确界；不声称一个游戏取得全类sup。 | 同上；没有统一C,d0，全类目标仍OPEN。 |


## 有序尾部冻结与 DAG 端点次数预算

| ID | 精确范围和结论 | 证明、审查与限制 |
| --- | --- | --- |
| WC-ORDERED-COHORT-FREEZING-v1 | 任意MODEL游戏、d≥0和玩家有序非空划分，资源组潜在用户最小/最大权a,b与后组潜在总权L定义A=max_(e,j)(b/a)(1+L/a)^d（无潜在用户取1）。依次固定先组背景，最小化按(1+L/a)^d/a缩放的活动组Shapley势并冻结，任取阶段全局最小均得到A-PNE。若组内比≤R且L≤εa，给R(1+ε)^d；不控制全类最佳划分参数。 | [完整正文](weighted_congestion/weight_bands/ordered_tail_freezing.md), [独立审查](../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md)；只证此实例参数界，无全类Cd/ln d；不要求同一势对全部改善边下降。 |
| WC-ORDERED-TAIL-PARAMETER-LIMIT-v1 | 任意d≥1,H≥1,K≥1，单资源一名权H玩家及K名单位权玩家、费用x^d、人人可选空策略或该资源。全部有序非空划分的最小A恰为min{H,(1+K/H)^d}。K=ceil(H²)时恰H，固定d仍可无界；游戏有全空精确PNE。 | [完整正文](weighted_congestion/weight_bands/ordered_tail_freezing.md), [独立审查](../reviews/weighted_congestion/weight_bands/ordered_tail_freezing_review.md)；只否定对该潜在尾部A参数的统一控制，不否定冻结程序可能有更精细分析，也不是均衡非存在。 |
| WC-DAG-LOW-LEAKAGE-DEGREE-BUDGET-v1 | 任意非空有限simple DAG、d≥1及ε∈(0,1)，令z=ε^(-1/d),P_k为k顶点有向路径数,S_D(z)=ΣP_kz^(k−1)。存在根权1、正轻权W<1及outsum<w_v、非零非负degree≤d费用通过p0(W)≤εp0(1)和pv(1+outsum)≤εpv(1+w_v)，当且仅当z(z−1)S_D(z)≤1。全部可行权有正文slack表示；饱和时权唯一。原辅助step阈值q满足q(q−1)≤1/[z(z−1)]≤d/ln(1/ε)，固定ε的√d量级在检测系统内可达。 | [完整正文](weighted_congestion/polynomial_curvature/dag_low_leakage_budget.md), [独立审查](../reviews/weighted_congestion/polynomial_curvature/dag_low_leakage_budget_review.md)；iff仅是指定端点检测系统；未控制高平台过冲或真实全状态偏离，不给实际多项式博弈的β上界。 |

## 择证循环边界与有向分叉强迫割均衡

| ID | 精确范围与结论 | 证明与状态 |
| --- | --- | --- |
| WC-SELECTOR-UNIT-SPEED-STATIONARY-BARRIER-v1 | 单位速度平稳择证的无界损失；For every finite real alpha>=1 and d>=1, some finite positive rational weight two-action template and full selector have no unit-speed stationary dual, already witnessed by an affine column; this is no nonexistence result. | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/stationary_selector_obstruction.md)、[独立审查](../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md)。 |
| WC-AFFINE-SELECTOR-CYCLE-DUAL-v1 | 任意仿射择证的循环权重对偶；For every finite positive-weight action template and tagged selector, every selected cycle gives an affine dual by lambda_s proportional to the selected mover weight; self-loops are allowed and all affine columns sum to zero at alpha=1. | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/stationary_selector_obstruction.md)、[独立审查](../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md)。 |
| WC-RECURRENT-SUPPORT-FIP-EQUIVALENCE-v1 | 循环支撑择证与全模板有限改善性等价；For fixed finite weights, action counts, degree, real alpha>=1 and any fixed nonempty signature-column subcone, every selector admits a dual supported on its recurrent states iff every nonnegative-coefficient game on that template has no strict alpha-improvement cycle; this is stronger than mere PNE existence. | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/stationary_selector_obstruction.md)、[独立审查](../reviews/weighted_congestion/template_certificates/stationary_selector_obstruction_review.md)。 |
| WC-DIRECTED-FANOUT-FORCING-CUT-v1 | 分叉双人侧反馈的统一强迫割均衡；For d>=2 and alpha>=T_d, every finite unique-source light/multihead-private-pair-side topology satisfying the weak uniform aligned-light forcing inequalities admits an all-anti alpha-PNE selected by any local minimum of the stated weighted cut; no unrestricted existence claim. | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/directed_fanout_forcing_cut.md)、[独立审查](../reviews/weighted_congestion/directed_fanout_forcing_cut_review.md)。 |


## 阶跃DAG极值幅度的真实多项式状态

| ID | 精确范围与结论 | 状态与限制 |
| --- | --- | --- |
| WC-DAG-EXTREMAL-AMPLITUDE-ALL-IN-v1 | 任意非空有限simple DAG，root权1、正轻权W<1且outsum<w_v、原双列binary策略；两列相同非零非负degree≤d费用，d≥1。令q=q_D>1、h_v=(1+Σ_in h_u)/q且Σh=q−1，存在A>0使p0(1)=A、pv(1+w_v)=A h_v。真实全入状态是max{1+1/q,B_d(q)}-PNE，B_d(q)=q/[1+(q−1)(1+1/[q(q−1)])^(−d)]；d≥16时统一为4√(d/ln d)-PNE。不要求低漏/高平台保真，但必须保留极值幅度条件。 | [正文](weighted_congestion/step_dag/polynomial_extremal_all_in.md)、[冻结独立攻击](../reviews/weighted_congestion/step_dag/polynomial_extremal_all_in_review.md)；仅限所写DAG策略及极值幅度；任意幅度/全类策略尚无归约，不是本题一般肯定证明，也不是非存在下界。 |

## 两权类别的平方根次数存在界

| ID | 精确范围与结论 | 状态与读取入口 |
| --- | --- | --- |
| WC-TWO-WEIGHT-ORDER-BLEND-v1 | 对每个d≥2及MODEL有限游戏，若所有玩家权重属于固定{a,b}、a≥b>0，则双排序混合势的每个单方局部最小点为A_d=(1+√(4d−3))/2-PNE，任意严格A_d改善终止；各类人数、权比、拓扑和系数任意。d≤1或仅一权时有精确PNE。不是任意权重全类上界。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[完整正文](weighted_congestion/weight_bands/two_weight_order_blend.md)、[独立攻击](../reviews/weighted_congestion/weight_types/two_weight_order_blend_review.md)。 |

## 循环窗口复制实现近线性倍率的真实改善环

| ID | 精确范围与结论 | 正文与实际状态 |
| --- | --- | --- |
| WC-CYCLIC-CLONE-IMPROVEMENT-CYCLES-v1 | 对每个d≥2、每个1≤α<ρ_d=sup_t>0[(d+1)(1+t)^d+t^(d+1)]/[d+(1+t)^(d+1)]，存在正有理权、全部资源费用x^d、人人策略族2^E的有限MODEL游戏，真实偏离图含严格α改善环，同时全空是精确PNE。ρ_d/d→1，故任何全局实值函数（含非可分）不能在该游戏全部严格α改善边下降。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/cyclic_clone_improvement_cycles.md)、[审查](../reviews/weighted_congestion/ordinal_potentials/cyclic_clone_improvement_cycles_review.md)；Only all-improvement termination and global strict ordinal potentials are obstructed; no PNE-nonexistence, chosen-step or minimizer-selection obstruction. |

## 共同幂混合全局最小点的线性障碍

| ID | 精确范围与结论 | 正文与实际状态 |
| --- | --- | --- |
| WC-COMMON-POWER-MIXTURE-MINIMIZER-OBSTRUCTION-v1 | 对每个d≥32，存在四玩家四资源、正有理权/系数、纯d次费用且有精确PNE的有限游戏，使任意非零非负Borel测度μ（全部状态目标有限）给出的Pμ(s)=Σ_e a_e∫_(p>0)x_e(s)^p dμ(p)每个全局最小点都非α-PNE，对全部1≤α<d/16成立；μ可依完整游戏。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/common_power_mixture_obstruction.md)、[审查](../reviews/weighted_congestion/ordinal_potentials/common_power_mixture_review.md)；Does not cover per-resource normalization, elimination of fixed-background players followed by a new coefficient rule, arbitrary separable objectives, nonseparable objectives or PNE nonexistence. |

## 有限可动权类别与窄权簇

| ID | 精确范围和结论 | 正文与状态 |
| --- | --- | --- |
| WC-WEIGHT-CLASS-TRIANGULAR-POTENTIAL-v1 | 对每个d≥2,k≥1，全MODEL中全球正权值至多k种的每个游戏有A_(d,k)-PNE，其中A∈[1,d)唯一满足A=Σ_(j=0)^(k−1)((d−1)/A)^j。三角排序混合势的每个单方局部min均是该均衡，全部严格A改善终止；任意人数、权比、费用/策略均覆盖。A≤B=(d−1)/(d^(1/k)−1)，固定k时A∼d^(1−1/k)，k≤ln d/lnln d且d≥16给2d/ln d。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[重构攻击](../reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md)、[informed攻击](../reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md)。 |
| WC-WEIGHT-CLASS-FIXED-BACKGROUND-v1 | 对每个d≥2,k≥1，全MODEL中只有可动玩家（策略族非单元素）的权值至多k种时，即使任意固定玩家的权种类无限制，仍有A_(d,k)-PNE。c_e(B_e+x)展开仍非负系数并逐状态保持可动者成本；无可动玩家时唯一状态精确。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[重构攻击](../reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md)、[informed攻击](../reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md)。 |
| WC-WEIGHT-CLASS-CLUSTER-ROUNDING-v1 | 对每个d≥2,k≥1,R≥1，若每个可动玩家有固定标签τ使v_τ≤w_i≤Rv_τ，其中k个代表权为正，则全MODEL原游戏有R^d A_(d,k)-PNE；固定玩家无需取整且权不受限。代表可重复/缺席；R=exp(1/d)时损失e，结合类别门槛给2e d/ln d的该明确子类界。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[重构攻击](../reviews/weighted_congestion/weight_types/finite_weight_classes_reconstruction_review.md)、[informed攻击](../reviews/weighted_congestion/weight_types/finite_weight_classes_informed_review.md)。 |

## 双轮环的全状态锁定编译

| ID | 精确范围和结论 | 正文与状态 |
| --- | --- | --- |
| WC-ANCHORED-POLYNOMIAL-CYCLE-LOCK-v1 | 每个n≥3、degree≤p、两动作MODEL游戏的严格α≥1双同序2n环，可保持玩家/权重/旧资源，增加2L个正单项式资源编译为无αPNE游戏。q≤max(p,D)，D=ceil[ln(4α²BL/η)/ln(1/δ)]，B为全状态成本界、η为环余量，L=C(n−1,2)，δ为锚定三元缺员负载比。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[完整证明](weighted_congestion/anchored_cycle_lock.md)、[独立重构攻击](../reviews/weighted_congestion/ordinal_potentials/anchored_cycle_lock_review.md)。D依实例且输出只保留两个动作；无全类次数预算。 |

## 三次双轮环的锚定时钟次数保持障碍

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-ANCHORED-DEGREE-THREE-LOCK-OBSTRUCTION-v1 | 显式四玩家有理三次基体G，权(1,1/2,1/4,1/8)、α=21/20，有严格双同序环及0101/1010精确PNE。任意λ>0，对λG只加anchor0的T012,T013,T023互补010/101同费pair，每T独立任意degree≤3非负多项式（可零/省略），若0000玩家0及1100玩家2的总αmargin均≥0，则0101/1010全部四个翻位margin均<0，故仍αPNE。 | complete fixed-architecture proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/anchored_clock_degree_barrier.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/anchored_clock_degree_barrier_review.md)。只限明示基体、anchor、phase、同pair两侧同费及degree≤3；不排常数倍degree、其他anchor、两侧异费、辅助玩家或其他拓扑。 |

## 去包含支配与必选背景的空交反链核心规范形

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-ANTICHAIN-CORE-NORMAL-FORM-v1 | 任意d≥0 MODEL游戏有不依α的有限core变换：或给显式exactPNE，或得到同次数界、原玩家非空子集/原权的H，人人≥2非空两两不可包含且交集空的策略；固定lift将每个实α≥1的任意H αPNE提升原游戏。同一固定d、实α处，全类无αPNE反例存在等价于该core策略结构的正整数权/单位单项式x^j(j≤d)反例存在。 | complete direct proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/integer_counterexample_normal_form.md)、[独立审查](../reviews/weighted_congestion/template_certificates/antichain_core_normal_form_review.md)。提升单向、不保人数/资源数、不保最佳因子或逐状态反投影；没有无限规范模板的规模截止或全类C,d0。旧整数v1身份/保人数义务不改。 |

## 统一低泄漏锚定时钟预算的普适次数障碍

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-UNIFORM-CLOCK-BUDGET-BARRIER-v1 | 任意n≥3、整数p≥0的MODEL两动作严格α≥1双同序环、任意锚点，B为全状态原成本有限上界、η为环最小严格差、L=C(n−1,2)、δ=max锚定三元(1−minw/Σw)。若任意整数D≥1满足δ^D≤η/(4α²BL)，则全局权比R>α、D>(R+1)ln(4α²BL/η)>2(α+1)ln(2α)，且每个实q≥D均有αlnq/q<α/(α+1)<1；包括实际输出最高次数。只封闭该统一充分预算的目标否定证书，非实际最小锁定次数下界或全类PNE存在结论。 | complete budget-obstruction proof; independently reconstructed and exactly audited; unrefereed；[一般证明](weighted_congestion/uniform_clock_budget_barrier.md)、[独立重构攻击](../reviews/weighted_congestion/ordinal_potentials/uniform_clock_budget_barrier_review.md)。 |

## 循环窗口前沿的扭转平移与精确相位商

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-CLONE-FRONT-PHASE-QUOTIENT-v1 | 任意m≥2,N≥1正类权、每类至少参与一test的循环窗口两动作lift（保留零系数资源），同test全部index及pair两侧同费；共同index平移并wrap翻bit逐成本/偏离协变。合法class prefix/suffix由x∈(Z2N)^m编码，对角T使x各加1，商恰(2N)^(m−1)，单clone留front动作恰±1（N1两邻居重合）。有显式2N长forward成本表及backward r+1交换式。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/class_front_phase_quotient.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/class_fronts_review.md)。count是互异MODEL动作状态；单测试子项可缺席类，但不能把空/空标签当两策略。class0商动作改变所有相对相位，须保mover标签。不是对全front出口或PNE的断言。 |

## 类内时钟的前沿出口障碍与不同步反例

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-CLASS-INTERNAL-CLOCK-FRONT-OBSTRUCTION-v1 | 任意α≥1，同权类内递增锚定010/101同费三元时钟在每条合法front边的own old=new=c(2w)，clock margin≤0。显式12player/N4/degree8/α21/20有理窗口lift有strict24步环，但phase(0,4,0)六端点margin<−9/50；512front恰8稳定，仍有内部clone margin>1/5。故strict环不自动给每个类front改善端点，任意此类clock不新增front内改善。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/class_front_phase_quotient.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/class_fronts_review.md)。局部lemma要两端均非full触发；front使用递增锚定三元，不涵盖任意乱序wrap。实例非αPNE，有离front出口；不排所有类内compiler或其他同步机制。 |

## 有限次局部成本空间与全成本资源压缩

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-DEGREE-LOCAL-COST-COMPRESSION-v1 | 固定n≥1,m_i≥1,d≥0与正实权，D=Σ_i m_i Σ_(T⊆N\i,|T|≤d)∏_(j∈T)(m_j−1)。全部玩家cost tables位于维D局部张量空间；任意游戏可用≤D正系数单项式签名类型及≤Σm_i零费私有动作marker保所有state/deviation成本和动作标签，core可保持。binary时D=2nΣ_(r≤min(d,n−1))C(n−1,r)，一般D=O_d((Σm_i)^(d+1))。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)。不保原资源身份、单位系数或算法效率；零成本可用0正资源但markers保MODEL合法。所有人数/动作数无界，维界不是全类规模截止。 |

## 全状态择证的低阶矩极锥与小支撑接口

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-SELECTOR-LOCAL-MOMENT-INTERFACE-v1 | 固定任意完整selector h及实α≥1，其概率dual等价conv{Ψ_h(s)}∩K^-非空；Ψ只含所选动作边和≤d对手动作的signed discounted矩，K为全部允许资源cost vectors锥。若dual存在，有≤D+1状态支撑dual。binary指定单mover翻位支撑且α1时，dual存在等价两方向≤d上下文矩匹配/无degree≤d严格多项式分离；α>1仅primitive非负tests乘性夹逼。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)。不能删selector-support marginal-polytope条件、改成任意局部一致矩或强求feature=0；不要求stationary/recurrent，未保证每selector可行或单mover证书。 |

## 完全暂态奇偶支撑的择证对偶

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-TRANSIENT-PARITY-SELECTOR-DUAL-v1 | 每个d≥0、每个d+3维正实权向量，都有binary无self-loop且唯一2cycle的selector，及全部支撑在暂态state的概率λ，对全部signature的degree0..d列在α1恰零、对所有α≥1非正；限制core proper signatures仍成立。flag0偶active states均匀分布，active维d+2使cost active-degree≤d+1严格低于维数。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)。仅证明transient dual可行；唯一2cycle自身也有dual，不证明暂态必要/更优，不给任意selector或全类存在。 |

## 锚定双轮时钟的有向差分、线性预算与逐次数锐效率

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1 | 任意n≥3、α≥1、正权两动作MODEL基体的严格双同序环，任意逐三元非负多项式同费010/101锚定pair：两半合法margin同为g_i，非法firstopp i的真实clock margin恰g_i+Σ_{j later同anchor}Δ_ij，Δ≥0。γ_i为两半base margin之min、B覆盖全部base成本时，γ_i+g_i>0及每i<j的g_i+Δ_ij>αB给全状态无αPNE的n+L条充分线性约束。保环必要Σg=−(α−1)ΣS、(α−1)ΣS<Γ；degree≤D的Δ/S锐界为逐0..D单项式max，一般不取最高次；κ逐状态列界另给保原αPNE的全玩家充分条件。明示四玩家三次基体有43次实际证书，原uniform预算选值91。 | complete stated-scope interface proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/anchored_clock_actual_margins.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/actual_clock_margins_review.md)。约束仅充分、总预算仅必要；κ稳定条件非必要，保firstopp失败不等于PNE；不保证给定D可行或B可多项式时间计算。43不称最优，91只是统一充分预算选值。没有一般次数效率或全类结论。 |

## 同权主玩家共享侧资源的统一强迫截断势均衡

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-SHARED-SIDE-TRUNCATED-ROSENTHAL-v1 | 对每个d≥2、有限同权u>0 hubs/任意正异权lights，每light唯一source、每side唯一light并允许任意hub子集H_j及空集/含source、两动作副本同费非负degree≤d；若α≥A_d=[1−(d−1)d^(−d/(d−1))]^(−1)，且逐light弱UF为F_v(u+w)+ΣG_j(w)≥α[F_v(W_v)+ΣG_j(w+|H_j|u)]，则所写截断Rosenthal势任hub单翻位局部最小点配全anti lights给αPNE。A_d≤2d/ln d对全部d≥2，常数仅限该子类。 | complete structural proof; independent bottleneck reconstruction and frozen attack; exactly audited; unrefereed；[正文](weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/shared_side_truncated_potential_review.md)。共同hub权、每side唯一light、每light唯一source、动作副本同费与UF最坏负载均承重。不覆盖异权hub、多source side或UF失败且直接AS+B未满足的全类情形；子类C2,d0=2不代替唯一题。 |

## 同权主玩家共享侧资源的直接侧势预算均衡

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-SHARED-SIDE-BUDGET-POTENTIAL-v1 | 相同unique-light/shared-hub/unique-source拓扑，任意d≥0、实α≥1；H_j(m)=Σ_{r≤m}[G_j(w+ru)−αG_j(ru)]_+、M_v=αF_v(u+W_v)−F_v(u)。若逐light AS为F_v(W_v)+ΣG_j(w+|H_j|u)≤α[F_v(u+w)+ΣG_j(w)]，逐source Σ_jH_j(|H_j|)≤M_v，则同一有限势每个单hub局部最小点配全anti是αPNE。无需UF或α≥A_d。 | complete conditional proof; independently attacked after abstraction; exactly audited; unrefereed；[正文](weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/shared_side_truncated_potential_review.md)。AS与源预算是充分假设，不证明所有该拓扑游戏都满足；仍限同权hub、unique-light/unique-source和同费副本。此ID扩大degree/alpha域并改变假设，未静默改UF-v1；后置抽象攻击不冒充初次未读稿全证明重构。 |

## 潜在可动用户共占高度的三角排序势

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-WEIGHT-INTERACTION-HEIGHT-POTENTIAL-v1 | 对任意d≥2 MODEL游戏，先吸收singleton固定玩家背景；非空可动玩家图置i→j当wi>wj且二者各有策略使用同一资源，k为DAG最长路径顶点数。则有A_(d,k)-PNE及全部严格A改善下降的身份子集资源可加势。A仍为A=Σ_{j<k}((d−1)/A)^j在[1,d)唯一根；全局不同权值数任意大，无可动者精确PNE。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[原稿新增第11–13节](weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[独立攻击](../reviews/weighted_congestion/weight_types/interaction_height_review.md)。潜在共占height是同一个全局玩家图参数，不能换成逐资源种类数或单点用户数；k无全类统一界。原有限权类ID中的k不变，本新ID单独扩大输入类。 |

## 严格改善闭合词中的实际共占长权链

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-REALIZED-INTERACTION-CHAIN-CYCLE-v1 | 对任意d≥2、实α≥1 MODEL游戏的非空有限严格α改善闭合真实单方词，令M为至少移动一次玩家；其余按沿词不变策略吸收背景。在M上按wi>wj及某端点状态实际同资源置弧，height为k，则α<A_(d,k)。所以任正整数K≥1、α≥A_(d,K)的这种闭词必含至少K+1顶点降权实际共占链，各边可来自不同状态/资源。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[原稿新增第11–13节](weighted_congestion/weight_bands/finite_weight_class_potentials.md)、[独立攻击](../reviews/weighted_congestion/weight_types/interaction_height_review.md)。只为给定严格改善闭词的必要链，不构造近d环，不证明无PNE；未访问状态不用相容，不把整链断言为同一状态共占。动态换秩改变势，尚无SCC出口或瞬态dual。 |

## 异权仿射全签名成本射线的刚性

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-AFFINE-FULL-SIGNATURE-RIGIDITY-v1 | 每个n≥2及不全相等正实权w、binary标签，V_i(s)=s_iΣ_jw_js_j的任何同玩家/权/标签完整成本保真有限非负系数多项式资源表示，在忽略零费/无人用资源后只能为全n玩家仅动作1使用、费用a_e x且Σa_e=1。任意提高有限degree仍不能把全部正资源潜在用户支持降到<n；V为有限表示锥K_fin的极射线。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文§9–10](weighted_congestion/template_certificates/selector_local_moments.md)、[独立重构与攻击](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)。只限完整成本保真、固定玩家/权/标签和有限表示锥，不声称闭包/暴露射线；等权存在≤2用户高次资源表示。原V有全0精确PNE，不限制改权/加玩家/仅保均衡或单向lift，也不反驳≤D资源数量压缩，未解全类题。 |

## 奇环缺陷择证的无界跨玩家补偿与锐支撑门槛

| ID | 精确范围与结论 | 当前状态、证据与限制 |
| --- | --- | --- |
| WC-SELECTOR-UNBOUNDED-MOVER-SUPPORT-v1 | 每个奇n≥3、d≥1、共同正权及任意binary缺陷择证（每态翻转一条相等邻边左端点），完整/proper签名degree0..d均有显式2n周期均匀dual。每个1≤α<2^d的任意dual须对全部n名移动者及其两方向给正质量；令r=(2^d−α)/(α2^d−1)，每方向≥r^(n−1)/[(1+α)Σ_(j<n)r^j]，最小状态支撑恰2n；α1各方向1/(2n)。min-index择证在α≥2^d有单mover二点dual，最小支撑恰2。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文§12–13](weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/selector_mover_support_review.md)。只限制统一有界移动者/状态支撑的dual构造；原族等权、有完整α1 dual，不是无PNE例，不排依n/动作数/D的支撑界或无界多玩家拼接；端点二点只限min-index择证。 |




## 原全三元统一时钟的低泄漏预算非必要证书

| ID | 精确范围与结论 | 状态及正文 |
| --- | --- | --- |
| WC-ANCHORED-FULL-UNIFORM-BUDGET-ESCAPE-v1 | 明示四玩家三次基体、权(1,1/2,1/4,1/8)、α=21/20；保留全部T012/T013/T023原010/101同费pair与统一M=2αB，只将次数取80，所得游戏全部16态有指定严格α出口且保留八条环边，但δ^80>η/(4α²BL)；满足(U)的最小整数为91。只证明(U)在原全三元统一幅度架构中也非必要，不称80最优或一般增长族。 | complete finite certificate; independently reconstructed and exactly audited; unrefereed；[正文第4节](weighted_congestion/anchored_clock_degree_barrier.md)、[审查](../reviews/weighted_congestion/ordinal_potentials/anchored_clock_degree_barrier_review.md) |


## 跨源反馈与归约/编译器的准确边界

| ID | 精确陈述 | 状态、证据与限制 |
| --- | --- | --- |
| WC-MULTISOURCE-SHARED-SIDE-ROSENTHAL-v1 | 任意d≥2、实α≥1+√d，同权hub u、唯一main source的正权lights，side允许任意hub子集及跨source任意light子集，两副本同费非负degree≤d。令T_j为side全light权、m_j为hub数、W_v为source总light权；若每light满足F_v(u+w_l)+Σ_(j:l∈L_j)G_j(w_l)≥α[F_v(W_v)+Σ_(j:l∈L_j)G_j(T_j+m_ju)]，则真实hub Rosenthal势任单hub局部最小点配全anti为α-PNE。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/multisource_shared_side_review.md)。同权hub、二元对称副本、唯一main source及UFmulti承重；不覆盖异权hub或UF失败，不改变全类OPEN。旧两个Claim身份保持。 |
| WC-APPROXIMATE-SUPPORT-DISTORTION-v1 | 每个m≥1、ε>0，原binary成本V_i=s_i(s_0+εΣ_(l=1)^m s_l)。任意相同玩家/标签的有限MODEL表示允许改正权及任意有限degree；若全部正资源潜在支持≤r≥1且所有玩家/状态V≤Ĉ≤βV，则β≥max{1,m(1+ε)/[(r−1)(1+mε)+mε]}。对称A夹逼给A²同必要界。固定有限r、β选择m和正有理ε即不可表示，原费用仅degree1。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/selector_local_moments.md)、[独立审查](../reviews/weighted_congestion/template_certificates/approximate_support_review.md)。完整逐状态成本、保零及无辅助玩家承重；原例有全0精确PNE。仅限制此近似表示归约，不排辅助玩家、均衡lift或全类存在，不声称固定参数sharp。 |
| WC-CLASS-INTERNAL-CLOCK-COMPILER-OBSTRUCTION-v1 | 显式12玩家/64资源degree8循环窗口binary游戏有24步strict21/20双同序环，但phase(0,0,1)是全部玩家严格exactPNE。任意有限fresh同类递增三元010/101互补pair，pair两侧同一非负非减费用，任何degree/幅度叠加均保留该严格exactPNE。因此仅追加这些clock不能对所有该倍率strict sweep输入保证全状态无PNE。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/class_front_phase_quotient.md)、[独立审查](../reviews/weighted_congestion/ordinal_potentials/class_internal_clock_compiler_review.md)。只排所写追加compiler；不排跨类、其他arity/phase、不等费pair、辅助玩家或更高倍率专用输入类。旧端点反例仍非PNE，不改其ID；本新fixture是真exactPNE。 |

## 正占用核的独立结构接口

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| PK-INTERACTION-RANK-FACE-v1 | 每个n≥1、正实质量w、整数r≥0及C∈K_fin：C的active秩≤r iff每个有限非负表示的所有正项min{k,|S|−1}≤r；r≤n−2时恰为顶背景(r+1)阶差分和L的零暴露面，r≥n−1为全锥。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](positive_kernels/occupancy_rank_faces.md)、[独立审查](../reviews/positive_kernels/rank_face_review.md)。不覆盖负混合或零/负质量；低阶大支持线性项仍允许，不能推出全小用户支持。 |
| PK-SHARP-FORBIDDEN-MASS-v1 | 每个n≥2、正实w、0≤r≤n−2，q=r+1；γ=min_|S|≥q+1 q!(|S|−q)e_q(w_S)/(|S|W_S^q)>0。任有限非负表示删除min{k,|S|−1}>r项得合法低秩C_low，bad全激活质量≤L_q(C)/γ，逐坐标0≤C−C_low≤L_q(C)/γ。γ是全部bad单核L/B精确最小且k=q达到；任意低秩绝对ε近似给n binom(n−1,q)2^q ε/γ界。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](positive_kernels/occupancy_rank_faces.md)、[独立审查](../reviews/positive_kernels/rank_face_review.md)。锐性只指单核L/B预算比；不称最终距离界最优、不恢复未知表示；q≥2时常数非跨正质量统一。 |
| PK-OCCUPANCY-CONE-CLOSURE-v1 | 每个n≥1、正实w：cl K_fin=cone({K_(S,k)}∪{U_S})，U_(S,i)=1_(i∈S)prod_(j∈S)s_j且cone仍有限和。n≥2原锥非闭；每r≥0有cl K_fin∩V_r=cl(K_fin∩V_r)，r≤n−2亦等于cl K_fin∩ker L_(r+1)。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文](positive_kernels/occupancy_rank_faces.md)、[独立审查](../reviews/positive_kernels/rank_face_review.md)。闭包新增对象不能冒充原有限表示；底背景差分无稳定gap，不能用其零面替代顶背景；没有均衡桥。 |

## 锚定保环时钟不可消去真实环余量依赖

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-ANCHORED-MARGIN-DEPENDENCE-OBSTRUCTION-v1 | 对每个整数D≥0，存在固定4玩家、权(1,1/2,1/4,1/8)、α=21/20、16正三次资源、两非空空交反链动作的有理MODEL基体G_D，原八边同序环全strictα；任意添加anchor0、全部允许T012/013/023、010/101同pair同费、degree≤D非负多项式时钟，只要保全部八环边strictα，就仍保0101/1010的所有翻位margin<−K_min/2<0。因此不存在仅依p,n,w,α而不依余量/实例细节的通用有限保环次数界。 | complete fixed-architecture all-cap obstruction; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/anchored_clock_actual_margins.md), [独立审查](../reviews/weighted_congestion/ordinal_potentials/actual_clock_margins_review.md)。只限制必须保原环的明示同费三元架构；不排特选健康余量增长输入、换支持/phase/两侧异费/aux或不保环。α=1不在新Claim范围。系数幅度保持有界，不声称幅度必须发散或任何全类结论。 |



## 完整空交反链签名锥中暂态择证质量的必要性

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-FULL-CORE-TRANSIENT-MASS-NECESSITY-v1 | 任d≥0、α≥1及n玩家positive-weight binary proper-resource degree≤d游戏的严格α简单环Q，补至n′=max(n,d+2)再加flag，在完整非空proper signature×0..d锥上有selector H，唯一recurrent为嵌入Q；同一完全暂态概率dual对全部β≥1可行。在给定α任何dual暂态质量≥η/(η+M)>0，且完整锥无共同PNE、任意点质量皆非dual。cyclic-clone的两互补动作给每d≥2、1≤α<ρ_d的实例。 | complete interface corollary; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/template_certificates/selector_local_moments.md), [独立审查](../reviews/weighted_congestion/template_certificates/selector_local_moments_review.md)。旧parity暂态可行及删列锥必要性在完整proper锥的同时化推论，非任意selector统一法；singleton列依状态变化，¬∃s∀a不能交换为∃a∀s。不构造全类非存在族，不给C,d0。零向量不叫概率dual。 |

## 跨源共享侧资源的强迫与目标倍率分离

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v1 | 任意整数d≥2、实τ>1和α≥1满足(τ−1)(α−1)≥d；同权hub u>0、正权light各唯一main source，二元同费主/侧副本，side任意hub及跨source多light用户子集，全部费用非负系数degree≤d。记W_v为源light总权、T_j为side全部light总权、m_j为hub数。若每light l满足F_v(u+w_l)+Σ_(j:l∈L_j)G_j(w_l)≥τ[F_v(W_v)+Σ_(j:l∈L_j)G_j(T_j+m_ju)]，则第8.2节真实hub Rosenthal势E任单hub局部最小点配全anti lights为α-PNE。τ与α无需大小排序；d≥16取τ=1+ln d给α=1+d/ln d≤2d/ln d。 | complete conditional proof; independently reconstructed and exactly audited; unrefereed；[正文第九节](weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/multisource_force_tradeoff_review.md)。同权hub、唯一main source、二元同费副本及所写UFτ均承重；不包含τ=1、不提供任意实例满足强迫条件的表示或稳定light选择，不覆盖异权hub或一般策略。旧三个Claim不变，WC-TARGET保持OPEN；未外审或认证新颖性。 |

| WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v2 | 第9.1节同权hub、唯一main-source、任意跨source多light/shared-hub的二元同费副本模型，费用非负系数degree≤d，任意整数d≥2、实τ>1及α≥1，保持UFτ但只需α(τ−1)≥d；同一真实hub Rosenthal势E每个单hub局部最小点配全anti为α-PNE。τ≥d+1时给精确PNE；d≥16且τ=1+ln d时给(d/ln d)-PNE。全部实正权/实非负系数、有限拓扑、零常数费用和空集合边界均量化。 | complete conditional proof; independently reconstructed and exactly audited; unrefereed；[正文9.8—9.12](weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/multisource_force_increment_review.md)。v2严格扩大v1充分条件域，旧版本不改；不称倍率条件必要或最优。同权hub/唯一main source/二元同费副本/UFτ承重；不含τ=1或一般游戏的强迫表示与light稳定选择，WC-TARGET保持OPEN；未外审、新颖性未认证。 |

## 局部异权主玩家共享侧资源的排序势均衡

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-HETEROGENEOUS-HUB-SORTED-SIDE-v1 | 任意d≥2、正实异权hub a_v和正权lights的唯一source二元同费主/侧副本模型，side含任意H_j及跨source L_j。令非空H_j的A_j=min_H a，R=max({1}∪{a_v/A_j:v∈H_j})，K=max({1}∪{a_o(l)/A_j:l∈L_j,H_j≠∅})，U_j=Σ_H a、T_j=Σ_Lw、W_v=Σ_sourcew。若α≥R、(α−1)²≥Kd，且每light满足F_v(a_v+w_l)+Σ_jG_j(w_l)≥α[F_v(W_v)+Σ_jG_j(T_j+U_j)]，则降序前缀侧势任单hub局部最小点配全anti为α-PNE。全局hub比R0时max{R0,1+√(R0d)}充分；R=K=1恢复1+√d。 | complete structural proof; independently reconstructed and exactly audited; unrefereed；[正文第十节](weighted_congestion/shared_side_truncated_potential.md)、[独立重构与最终攻击](../reviews/weighted_congestion/heterogeneous_hub_sorted_side_review.md)。R,K及UFhet仍承重；允许全局任意多权类和无界跨度但不消去局部比。单副本排序边际R因子在线性资源上渐近锐，该实例有exactPNE，故只限制逐副本夹逼；无全类C,d0或非存在结论。 |


| WC-MULTISOURCE-FORCING-TARGET-TRADEOFF-v3 | 第9.1节同权hub、唯一main source、任意跨source多light/shared-hub的二元同费副本模型，全部费用非负系数degree≤d，任意整数d≥2、实τ≥1及α≥1，满足原UFτ和ατ≥d时，同一真实hub Rosenthal势E每个单hub局部最小点配全anti为α-PNE。含τ1、零/常数费用、空集合及全部实正权/实非负系数。τ≥d可取α1；d≥16取τ=ln d给α=d/ln d。 | complete conditional proof; independently reconstructed and exactly audited; unrefereed；[原稿9.14—9.16](weighted_congestion/shared_side_truncated_potential.md)、[独立重构与冻结攻击](../reviews/weighted_congestion/multisource_force_increment_review.md)。同权hub、唯一main source、二元同费副本和原UFτ承重；不提供一般游戏的强迫表示、弱强迫下的统一选态或异权hub桥。v1/v2精确身份和原冻结证据保留。ατ≥d仅充分；独立sharp边界只限α1，WC-TARGET仍OPEN，未外审/新颖性未认证。 |
| WC-SHARED-SIDE-EXACT-FORCING-THRESHOLD-v1 | 对每个整数d≥2，在v3完全相同的同权hub/唯一source/二元同费副本结构类中，τ≥d的每个UFτ游戏均有精确PNE；对每个实1≤τ<d，显式2玩家4资源游戏严格满足UFτ却全部4态均有严格改善出口。因此该条件结构类保证精确PNE的统一强迫参数边界恰d并在端点取得。仅α1，不称α>1乘积边界必要，不是全类渐近非存在。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[原稿9.17](weighted_congestion/shared_side_truncated_potential.md)、[独立审查](../reviews/weighted_congestion/multisource_force_increment_review.md)。两边完整一般证明；仅exact forcing子类阈值，无全类否定。 |


## 异权乘积预算与潜在使用森林

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-HETEROGENEOUS-HUB-SORTED-SIDE-v2 | 任意d≥2、任意有限第十节异权hub/唯一source light/二元同费主侧副本拓扑，正实权和非负degree≤d费用；沿用A_j、R、K。对全部实τ≥1、α≥1，若每light满足F_v(a_v+w_l)+ΣG_j(w_l)≥τ[F_v(W_v)+ΣG_j(T_j+U_j)]，且α≥R、ατ≥Kd，则原E_het每个单hub局部最小点配全anti为真实α-PNE。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/shared_side_truncated_potential.md)。仍依R/K及UFτ；不是全类界。旧v1量词、正文和冻结证据保持；乘积域只称充分。 |
| WC-SORTED-SIDE-GLOBAL-MINIMUM-R-BARRIER-v1 | 每个实R>1、1≤α<R、整数d≥2与τ≥1，存在无线light、main零、单side G=x的合法游戏，侧内比R、K=1、UFτ真空；E_het全部全局最小点都是严格单翻位局部最小点且非α-PNE。取n>αR/(R−α)，n重RA与n轻A分离，重gain=nR/(R+n)；ΔE=a(n−x−y)^2+(a−A)y(n−y)使全局min恰两个分离态。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/shared_side_truncated_potential.md)。只限制旧降序E的局部或全局最小化，连global-min间择优也无效；原游戏有exactPNE，不是全类非存在或其他势障碍。 |
| WC-INCIDENCE-FOREST-EXACT-v1 | 每个有限正实权玩家、有限资源子集策略（可含空）且任意逐点有限非负非减资源费用的游戏，若玩家—资源潜在使用二部图为森林，则存在exactPNE；允许必用资源、任意策略耦合、不连续费用、零与常数。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/incidence_forest_private_reduction.md)。仅森林，不声称全部改善终止；无任意有环核心的规模或全类倍率界，单环已有明确反例。 |
| WC-ONE-PLAYER-TREE-PRIVATE-LIFT-v1 | 任意上述费用类游戏，非空保留玩家N0和资源E0，删除玩家不潜在使用E0；非E0附属二部图为森林且每分量至多接触一个保留玩家。各根边换非负私有常数资源，保留策略单射与玩家权，存在不依α的固定lift将reduced任实α≥1 PNE提升原；非负degree≤d多项式时保同次数上限d≥0。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/incidence_forest_private_reduction.md)。单向lift；不允许同一附属分量接触多个核心玩家或以核心资源为根，不保证最优倍率或原均衡反投影。 |
| WC-INCIDENCE-UNICYCLE-COUNTEREXAMPLE-v1 | 明示权(1,2)二玩家四资源游戏，e=x²、f=(9/2)x、私人p=4、q=71/4，策略分别{e,p}/{f}及{e,f}/{q}。潜在使用图连通且圈秩1，四态均有strict改善，最佳纯状态因子恰72/71并由00取端点。 | complete stated-scope proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/incidence_forest_private_reduction.md)。固定degree2、固定二玩家的exact存在反例，不是随次数增长下界或最坏单环阈值最优性。 |

## 同权类前沿到全状态的条件编译

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-CLASS-FRONT-ALLSTATE-COMPILER-v1 | 任意p≥0、α≥1的MODEL两动作游戏，玩家分为有序同权类，跨类权任意。𝔉为各类至多一次相邻bit变化的product-front。若每个𝔉态有保𝔉严格α出口，令B=max全状态玩家成本、η=min前沿最大保前沿margin>0、L=max类C(n_a−1,2)。L0时原游戏已无αPNE；L≥1时仅加2Σ_a C(n_a−1,2)个同类固定首位010/101时钟，费用M[x/(3w_a)]^D、M=2αB，任D≥1满足(2/3)^D≤η/(4α²BL)，即全部状态有margin≥η/2的strictα出口，输出次数≤max(p,D)。保前沿边clock margin恰−(α−1)r_iM(2/3)^D，故可改用(2/3)^D≤1/(4αL)及(α−1)LM(2/3)^D≤η/2；α1第二式自动成立，D不依η。 | complete conditional proof; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/class_front_phase_quotient.md#条件编译接口全部同权类前沿出口到全状态非存在)、[独立重构及冻结攻击](../reviews/weighted_congestion/ordinal_potentials/class_front_allstate_compiler_review.md)。条件要求全部product-front出口，单sweep环不够；没有增长输入族或B/η统一控制，D无独立跨类权比损失不表示参数与权谱无关。固定九玩家degree8证书仅前提非空与实现回归，不称新倍率/最优性或WC-TARGET完成。 |

## 固定主玩家的无强迫轻响应重构

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-FIXED-HUB-LIGHT-THRESHOLD-RESPONSE-v1 | 任意非负degree≤d多项式、d≥0、异权hub/light、唯一source且每side仅一light的二元同费副本模型，无UF。固定任意hub向量后，light子游戏由逐source二次阈值势（F常数时线性势）保留全部成本边的严格/平局符号，PNE恰势局部min且全部strict light改善终止。从全aligned按非降阈值删除，给每名light至多一次strict移动的exact响应。存在/FIP为Milchtaich1996已知两策略结果的直接应用；显式势和删除过程作自足重构接口，不主张新颖。 | complete reconstruction of a known existence/FIP corollary; independently reconstructed and exactly audited; unrefereed；[正文](weighted_congestion/fixed_hub_light_threshold_response.md)。仅固定hub/unique-light；多light共享side可用旧三玩家例反驳exact响应。重选light后hub成本稳定不能替代冻结light的真实偏离，尚无跨hub响应兼容预算，不给全类C,d0或位多项式算法。 |

## 一般群组奇环的精确实际阈值

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| WC-ODD-RING-GENERAL-COHORT-ACTUAL-UPPER-v2 | 每个d≥2、奇m≥3、n_i≥1、正实hub权u_i与群内共同light权v_i，任意同费动作副本及群内同费side、非负系数degree≤d多项式F_i/G_i（含零）的一般cohort奇环均有T_d-PNE；不要求UF。T_d=max_(R>1)[R(1+R)^d+1]/[(1+R)^d+R^(d+1)]。结合既有每α<T_d严格反例，该拓扑的普遍存在阈值恰T_d；T_d<d/ln d，故仅本拓扑C=1,d0=2。 | complete general-cohort topology threshold proof; independently reconstructed and exactly audited; unrefereed；[正文第10节](weighted_congestion/odd_ring/cohort_lower_bound_and_envelope.md)、[独立重构与攻击](../reviews/weighted_congestion/odd_ring_parameters/general_cohort_actual_upper_review.md)。群内同权、每light私有双人side、同费动作副本及单奇环关联承重；不是MODEL全类上界。不声称某个有限实例取得拓扑sup，不改变旧证书/下界/单成员Claim。未入规范层的v1只给max{2,T_d}，本v2单列增强。 |

## 加权拥塞：线性次数的全状态下界与本题否定

| ID | Exact scope | Result and boundary | Proof and status |
| --- | --- | --- | --- |
| WC-HEALTHY-LINEAR-SWEEP-v1 | 每个整数p≥20，α=p/10、Q=p^4、m−1=ceil(log_2(p²))、N=p^(4m−5)的显式两动作循环窗口基体有strictα双同序环；真实最小环margin恰H/2，H=2^p−α；全部基体状态全部玩家成本≤B*=mQ^(m−1)2^p，ln(B*/(H/2))=O((lnp)^2)。 | 仅基体的环和全状态成本上界；本条不声称无均衡。 | [自足正文](weighted_congestion/linear_degree_allstate_lower_bound.md)、独立重构/攻击及原有精确审计见正文第10节，[审查补节](../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另给整数次数证明与完整多类核验；完整一般证明，内部已审，外审/新颖性未认证。 |
| WC-HEALTHY-FRONT-COVERAGE-v1 | 每个整数p≥20，同一基体的每个product-of-class-front状态都有保持前沿的合法单clone偏离，真实α=p/10 margin≥η0=H/4。前沿指每类按0,...,N−1线性顺序至多一次相邻位变化。 | η0是统一下界，非真实min-max精确值；仅本显式族，不把任意strict sweep当全前沿覆盖。 | [自足正文](weighted_congestion/linear_degree_allstate_lower_bound.md)、独立重构/攻击及原有精确审计见正文第10节，[审查补节](../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另给整数次数证明与完整多类核验；[自足主稿](weighted_congestion/linear_threshold_article.tex)与[成稿核查](../reviews/weighted_congestion/linear_threshold_article_review.md)另供连续阅读；完整一般证明，内部已审，外审/新颖性未认证。 |
| WC-LINEAR-DEGREE-ALLSTATE-NONEXISTENCE-v1 | 每个整数p≥2^20，存在本文显式有限MODEL游戏G_p，权重均正有理，资源费用均正有理系数乘x^p，每名玩家恰两个非空不交资源子集动作；每个纯状态都有合法单人偏离满足C_i(s)−(p/10)C_i(t_i,s_−i)≥H/8>0。 | 全状态非存在证明；允许巨大人数、资源数、权比和系数，不作输入规模/复杂度或最优常数承诺。 | [自足正文](weighted_congestion/linear_degree_allstate_lower_bound.md)、独立重构/攻击及原有精确审计见正文第10节，[审查补节](../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另给整数次数证明与完整多类核验；[自足主稿](weighted_congestion/linear_threshold_article.tex)与[成稿核查](../reviews/weighted_congestion/linear_threshold_article_review.md)另供连续阅读；完整一般证明，内部已审，外审/新颖性未认证。 |
| WC-MATCHING-LOG-UPPER-NEGATIVE-v1 | 对每个实C≥1与整数d0≥2，存在整数d≥d0和有限MODEL游戏，使每个纯状态s都有合法偏离C_i(s)>(Cd/ln d)C_i(t_i,s_−i)。选整数k≥max{20,ceil(20C),ceil(log_2d0)}、d=2^k即可。 | 严格否定本题全类存在命题；不改变WC-TARGET v1原长期目标身份，不声称精确a*(d)。 | [自足正文](weighted_congestion/linear_degree_allstate_lower_bound.md)、独立重构/攻击及原有精确审计见正文第10节，[审查补节](../reviews/weighted_congestion/ordinal_potentials/linear_degree_allstate_review.md#补充复核整数次数预算与完整多类拼装)另给整数次数证明与完整多类核验；[自足主稿](weighted_congestion/linear_threshold_article.tex)与[成稿核查](../reviews/weighted_congestion/linear_threshold_article_review.md)另供连续阅读；完整一般证明，内部已审，外审/新颖性未认证。 |

## 不相关并行机：新主目标与已知地基重构

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-TARGET-v1 | ∃统一ε∈(0,1)，∃确定性位多项式算法，∀合法非负有理/不可用边输入（m,n可变），输出全部任务的合法分配且C_max≤(2−ε)OPT；零最优值亦覆盖。 | OPEN，无新算法；精确身份见[本题账本](../unrelated_machines/CLAIMS.md)。 |
| UM-ST-ROUND-v1 | ∀P,T≥0及剪枝LST有理可行x，可确定性位多项式舍入为每机器L_i≤分数负载+支撑最大值≤2T。 | 已知结果的[自足重构](unrelated_machines/model_and_classical_barriers.md)与[独立攻击](../reviews/unrelated_machines/classical_foundation_review.md)；只实现给定x接口，非新贡献。 |
| UM-CONF-GAP-v1 | 配置LP在正最优值实例上sup OPT/T_CONF=2，即使每任务至多两台可用机。 | [重索引两树证明](unrelated_machines/model_and_classical_barriers.md)；原高度疑点显式处理；只限相对该LP值的合同，不证明主目标为假。 |
| UM-LONG-PATH-GAP-v1 | 对每个整数g≥3，正最优值、恰两可用机器/任务、简单机器图围长≥g子类上sup OPT/T_CONF=2。 | [长链阈值保真证明](unrelated_machines/long_path_coalition_gap.md)、[冻结独立攻击](../reviews/unrelated_machines/long_path_coalition_review.md)；非算法困难性，全球新颖性未认证。 |
| UM-COALITION-PROJECTION-GAP-v1 | 对每个整数r≥1、g≥3，上述子类精确定义CC_r的sup gap=2；各coalition仅共享完整单机配置分布，不要求多机overlap一致。 | [正文定义和森林耦合](unrelated_machines/long_path_coalition_gap.md)；完整三机交叠相容性在本树宽2族精确；主目标OPEN，独立内部已审、未外审。 |

## 不相关并行机：大边残余与共享容量方法边界

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-HEAVY-MATCH-FILTER-v1 | ∀合法P,T≥0，精确GHMR在总位多项式内保留所有T可行调度的使用边；拒绝⇒OPT>T，接受不蕴含可行。 | [完整安全性及复杂度](unrelated_machines/heavy_matching_residual_and_escape.md)、内部独立冻结审查；无近似保证/全球新颖性认证。 |
| UM-SIMPLE-SUPPORT-GAP-v1 | 每k≥4路径终端两树：每任务恰2选、每机器对至多1任务、OPT=2−1/k、配置T₀=1+1/k可行；此子类sup gap=2。 | 同正文§4，已内部独立审查；已知障碍支撑简化，不是算法困难性。 |
| UM-ESCAPE-MATCH-GAP-v1 | 每k≥4，共享z成本1/2逃逸族OPT=2−1/k，配置T₀可行且GHMR首轮零删边；∀固定ε>0能击穿相对T的(2−ε)合同。 | 同正文§5，核心/星2选、占位3选；不排除联合强化或OPT相对算法。 |

## 不相关并行机：成束相容与计数闭包

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-BUNDLE-MOMENT-v1 | For every k>=4 the canonical VW two-tree instance has strengthened configuration threshold exactly 2-1/k after adding the aggregate second-moment complement equation for each terminal bundle. | [自足正文](unrelated_machines/bundle_coupling_subdivision_barrier.md)、[冻结攻击](../reviews/unrelated_machines/bundle_subdivision_review.md)；一般主目标仍OPEN，新颖性未认证。 |
| UM-CARDINALITY-CLOSURE-v1 | For all legal P and rational T>=0 the synchronous forced-residual cardinality filter preserves every T-feasible schedule and terminates in deterministic bit-polynomial time. Its monotone integer-scaled bisection gives a lower bound B<=OPT; acceptance is not feasibility. | [自足正文](unrelated_machines/bundle_coupling_subdivision_barrier.md)、[冻结攻击](../reviews/unrelated_machines/bundle_subdivision_review.md)；一般主目标仍OPEN，新颖性未认证。 |
| UM-PAIR-SUBDIVISION-GAP-v1 | The pair-configuration LP, with common singleton machine marginals and exact complementarity for every degree-two job internal to each pair, has supremum gap 2 even on simple bipartite machine graphs. The stated cardinality filter makes no deletion on the subdivided VW certificates. | [自足正文](unrelated_machines/bundle_coupling_subdivision_barrier.md)、[冻结攻击](../reviews/unrelated_machines/bundle_subdivision_review.md)；一般主目标仍OPEN，新颖性未认证。 |

## 不相关并行机：共同匹配补全与条件块容量

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-JOINT-SMALL-ROUND-v1 | ∀P,T≥0,δ≥0及给定(Aδ)有理H,x，位多项式输出保持H的合法调度，全部L_i≤(3/2+δ)T。 | [自足接口](unrelated_machines/joint_matching_completion_and_block_cuts.md)；ST直接推论，未给选择H算法。 |
| UM-JOINT-CHOICE-NP-v1 | 每固定有理δ∈[0,1/3)，(Aδ)存在性判定NP完全，即使T1、N空、每任务唯一small、时间{1/3,1}；不含δ1/3。 | 同正文§3；导入Karp3DM及完整新归约，精确接口障碍，不是UM近似困难性。 |
| UM-ESCAPE-BLOCK-CUT-v1 | 每k≥4、1≤B≤θ，末簇Z_g≥(r_B−1)Y_v有效；随B重算的块强化在共享z族的阈值恰θ=2−1/k。 | 同正文§4；对整个强化解的计数证明，尚无一般分离/舍入。 |

## 不相关并行机：生成树再耦合的固定补全边界

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-TREE-MARKOV-COMPLETION-NO-v1 | 指定五机实例T=OPT=1，真实全局分布的生成树pair Markov再耦合有概率1/4产生冻结树任务后最优补全2的态；只否定每个支持态都可补<2T的合同。 | [正文](unrelated_machines/tree_markov_completion.md)、[独立审查](../reviews/unrelated_machines/tree_markov_completion_review.md)；一步迁移即可修复，不排聪明择态/换树；同合同至多四机连通树总可补T。 |

## 不相关并行机：可恢复星消去与容量身份

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-MINIMAL-STAR-CONTRACTION-v1 | For every legal P,T>=0 after pruning p>T, if a machine full neighborhood F has S>T and S-p_va<=T for every a, its replacement by one job with outside min times preserves T-feasibility. Every reduced schedule B lifts in deterministic bit-polynomial time to max(B,T); <=m repeated contractions retain the same bound. | [自足正文](unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结攻击](../reviews/unrelated_machines/minimal_star_capacity_review.md)；非主目标突破。 |
| UM-CAPACITY-ONE-PAIR-GAP-v1 | Over positive-OPT UM inputs the general pair-configuration LP GPC2 has supremum gap 2, even after iterating the specified residual-cardinality filter and minimal-star contraction. Explicit two-value family has m=k²+3k-1,n=2k²+k,T=1,OPT=2-1/k, all pair witnesses, and neither preprocessing rule triggers for k>=3. | [自足正文](unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结攻击](../reviews/unrelated_machines/minimal_star_capacity_review.md)；非主目标突破。 |
| UM-STAR-Q-JOB-COMPRESSION-NO-v1 | For every integer q>=2, there is a (q+1)-job star with T=1 for which no q ordinary replacement jobs on the same external machines, with arbitrary nonnegative/infinite times and no extra identity constraints, preserve feasibility for every specified A/B residual capacity profile. | [自足正文](unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结攻击](../reviews/unrelated_machines/minimal_star_capacity_review.md)；非主目标突破。 |


## 条件证书与终端容量稀释

| ID | 精确增量与限制 | 正文/审查 |
| --- | --- | --- |
| UM-HEAVY-ALTERNATIVE-FILTER-v1 | 重备选源权部分匹配的安全位多项式删边；不额外覆盖全局必经大任务。 | [正文](unrelated_machines/diluted_sink_probe_gap.md)、[冻结审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)；外审/新颖性未认证。 |
| UM-DILUTED-SINK-PROBE-GAP-v1 | 配置可行＋全部逐边强制LST可行＋星匹配固定点仍sup gap2；阻塞任务多端，不是OPT相对否定。 | [正文](unrelated_machines/diluted_sink_probe_gap.md)、[冻结审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)；外审/新颖性未认证。 |
| UM-BIG-CARDINALITY-PROBE-v1 | 条件LST内加入大任务基数的安全位多项式探针；只证明对未加逃逸边的稀释族准确识别OPT。 | [正文](unrelated_machines/diluted_sink_probe_gap.md)、[冻结审查](../reviews/unrelated_machines/diluted_sink_probe_review.md)；外审/新颖性未认证。 |


| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-DILUTED-ESCAPE-PROBE-GAP-v1 | 配置可行＋所有边独立强制LST＋现行GHMR＋局部星匹配合用仍sup gap2；稀释底座加共享1/2小端，OPT=2−1/k。 | [正文§11](unrelated_machines/diluted_sink_probe_gap.md)、[冻结独立攻击](../reviews/unrelated_machines/diluted_sink_probe_review.md)；不含条件配置/条件基数；主目标OPEN。 |

## 半单位共同见证的全窗口边界

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-JOINT-HALF-CHOICE-NP-v1 | ∀固定有理δ∈[0,1/2)，T=1、唯一small端、有限时间仅{1/2,1}时(Aδ)存在性NP完全，且该整个子类上(Aδ)存在⇔OPT≤1。 | [完整证明](unrelated_machines/joint_matching_completion_and_block_cuts.md)§3a、[独立攻击](../reviews/unrelated_machines/half_unit_joint_choice_review.md)；内部已审，外审/新颖性未认证。 |
| UM-JOINT-HALF-PROMISE-NO-v1 | 假设P≠NP，∀固定有理δ∈[0,1/2)，不存在总确定性位多项式算法，对所有OPT≤T的合法输入保证输出(Aδ)见证；即使只要求T1、唯一small、时间{1/2,1}子类亦不可能。域外可任意输出。 | [完整证明](unrelated_machines/joint_matching_completion_and_block_cuts.md)§3a、[独立攻击](../reviews/unrelated_machines/half_unit_joint_choice_review.md)；内部已审，外审/新颖性未认证。 |

## 全局单行基数匹配与紧凑共享逃逸

| ID | 精确范围与结论 | 正文/审查 |
| --- | --- | --- |
| UM-GLOBAL-ROW-COUNT-FILTER-v1 | For every legal P and rational T>=0, the synchronous global single-row exact-load/count-capacity filter of section 1 preserves every T-feasible schedule edge and terminates in deterministic bit-polynomial time. With fixed globally valid row bounds/caps, the global query is equivalent in strength to all corresponding resource-subpool queries. Acceptance is not feasibility. | [自足正文](unrelated_machines/row_count_escape_gap.md)、[冻结审查](../reviews/unrelated_machines/row_count_escape_review.md)；主目标OPEN，外审/新颖性未认证。 |
| UM-COMPACT-COUNT-ESCAPE-GAP-v1 | For every integer k>=2, the section 2 family with N=2k² blocks, N-2k global unit slots and common Y escape cost 1/k has OPT=2-1/k and GPC2(1) certificates. No minimal-star/cardinality rule starts; all global row-count forced-edge queries pass in the first round. Every machine configuration at T=1 extends to a complete assignment obeying other machines initial row-min count caps. The conjunction contract has supremum gap 2 on positive-OPT inputs; it does not include conditional LST/configuration LP. | [自足正文](unrelated_machines/row_count_escape_gap.md)、[冻结审查](../reviews/unrelated_machines/row_count_escape_review.md)；主目标OPEN，外审/新颖性未认证。 |

## 直接联合舍入的受限类正面衔接

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-ROW-SPREAD-TWO-ROUND-v1 | ∀合法非负有理UM输入，删除有零端任务后，若每个非空机器行的有限正时间均在某[γ_i,2γ_i]内（各γ_i>0可不同），则存在确定性位多项式算法输出全部原任务合法调度，C_max≤3OPT/2；含空任务/OPT0。 | [完整构造](unrelated_machines/joint_slot_prefix_rounding.md)、[独立审查](../reviews/unrelated_machines/joint_slot_prefix_review.md)；已知机制直接推论，非一般目标突破，新颖性未认证。 |

## 稀疏深树的独立条件配置边界

| ID | Exact Statement及范围 | 正文与审查 |
| --- | --- | --- |
| UM-SPARSE-CONDITIONED-CONFIG-GAP-v1 | 每k≥3的显式三选族OPT=2−1/k，T=1+1/k下每条有限边各有强制为1的完整配置点；独立单边配置删边/基数LST均零删除，sup相对证书阈值间隙2。不同查询不需共同基点或交叠一致性，不含星消元预处理。 | [自足稿](unrelated_machines/sparse_conditioned_configuration_gap.md)、[独立审查](../reviews/unrelated_machines/sparse_conditioned_configuration_review.md)；不排主目标。 |

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-COMPACT-MULTIROW-EXTENSION-v1 | For each k>=2 compact family, every U with card(U intersect V)<=N-2k, every v in U and every T=1 configuration C of v has an explicit complete assignment with v exactly C, true load<=1 on all U, and initial row-min count caps on every machine. This universal center budget is sharp: some U with N-2k+1 centers plus z and pin z=empty has no such assignment. Different queries share no joint witness; no general solver is claimed. | [正文§6](unrelated_machines/row_count_escape_gap.md)、[追加冻结攻击](../reviews/unrelated_machines/row_count_escape_review.md)；主目标OPEN，外审/新颖性未认证。 |



## 完整单机配置的独立全LP延伸

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-MACHINE-CONFIG-PROBE-GAP-v1 | ∀k≥2，既有紧凑族在T1对每机器每个合法C分别有y_iC=1完整配置LP点，OPT=2−1/k，故该合同sup gap2。∀i∀C∃各自y，不含共同base/条件混合恒等式；(MP)非整数可行必要条件，安全规则仅删失败配置，本族无首次删除。 | [正文§7](unrelated_machines/row_count_escape_gap.md)、[独立审查](../reviews/unrelated_machines/machine_config_probe_review.md)；全部分类/位长/来源见正文与专题CLAIMS，双路有限证据不代一般证明；外审/新颖性未认证，主目标OPEN。 |

## 真实最优凸包与固定槽输出空间

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1 | ∀m≥2，m台identical机器/n=m²正有理任务有OPT1及m个显式最优调度均匀边际x=1/m；任意逐机ties的固定有序槽图，每个覆盖匹配值均为2m/(m+1)→2。修复另见下项。 | [自足正文](unrelated_machines/optimal_convex_fixed_slot_gap.md)、[冻结独立审查](../reviews/unrelated_machines/optimal_convex_slot_review.md)；不排换x/换槽/repair或主目标，不声称新颖性。 |
| UM-OPTIMAL-CONVEX-SLOT-REPAIR-v1 | 对固定槽反例族的任意覆盖matching调度，恰m−1任务跨槽迁移即可达到OPT1，且该Hamming修改数最优；扫描与重分配为O(n+m)组合操作。 | 同正文§4及增补审查；只针对显式族，不是一般repair算法。 |

## 不相关并行机：循环批量修复与分流合流

| ID | 精确范围与结论 | 正文与限制 |
| --- | --- | --- |
| UM-ROBUST-CYCLIC-BATCH-OPT-v1 | For every fixed rational eta in (0,1), all legal P,T>0 and pruned actual schedules sigma with Cmax<=2T admit deterministic bit-polynomial coordinatewise nonincreasing optimization to a state with no machine-simple arbitrary-bundle cycle reducing every participating load by eta*T. At most floor(4m/eta) successful rounds. Variable-eta complexity is polynomial in 1/eta, not log(1/eta). | [自足正文](unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)；[冻结审查](../reviews/unrelated_machines/cyclic_batch_fork_review.md)；主目标OPEN、新颖性未认证。 |
| UM-BATCH-SUPPORT-REPAIR-NO-v1 | For every integer k>=1 the section5 three-machine family has OPT=1, a pruned schedule of loads (2,2,2), minimum sorted-lex improvement support k+1, and minimum maximum per-machine outgoing count k. Thus neither constant support nor constant outgoing budget guarantees monotone improvement. | [自足正文](unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)；[冻结审查](../reviews/unrelated_machines/cyclic_batch_fork_review.md)；主目标OPEN、新颖性未认证。 |
| UM-FORK-MINCOST-ROUND-REPAIR-NO-v1 | For every integer k>=2 the sections6-7 padded fork has T=OPT=1 and explicit feasible rational assignment x; every minimum-processing-cost ordered-slot matching induces the same actual schedule sigma of makespan 2-1/k. No nontrivial makespan-nonincreasing reassignment from sigma can have at most one outgoing destination per source machine, even with arbitrary bundle size and arbitrarily many machines. | [自足正文](unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)；[冻结审查](../reviews/unrelated_machines/cyclic_batch_fork_review.md)；主目标OPEN、新颖性未认证。 |

## 有向需求树与真实调度的直接桥梁

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-DAG-DEGREE-TOKEN-IDENTITY-v1 | ∀显式根简单DAG及正文二进制需求，q=min(k,d)个tokens＋filler构造的真实调度OPT=2−截断需求树最优比例；任意C<2调度可解码比例≥2−C，反向也位多项式可构造。 | [自足正文](unrelated_machines/rooted_dag_degree_token_bridge.md)、[冻结独立审查](../reviews/unrelated_machines/rooted_dag_token_bridge_review.md)；已知机制直接重构，无SA/困难性转移。 |
| UM-TARGET-IMPLIES-DAG-DEGREE-v1 | 若UM-TARGET-v1有统一ε，则同一个调度算法在≤1+|E|个正确缩放输入上给所有上述DAG的真实根树，b(H)≥εb*，总确定性位多项式。 | 同正文§5；条件必要能力，不是新近似算法或新颖性认证。 |

## 逐坐标循环修复与真实最优凸包的衔接

| ID | 精确范围与结论 | 正文与限制 |
| --- | --- | --- |
| UM-COORDINATE-REPAIR-ST-GAP-v1 | ∀m≥2、∀有理η∈(0,1)，boss7真最优凸包槽族的任意matching输出接鲁棒循环优化仍0轮，值2m/(m+1)→2。相同机器任意逐坐标非增序列都保持每台负载。 | [正文§9](unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)、追加冻结审查；守恒＋既有族的直接推论，不是新族，不排低机上升的makespan改善。 |

## 不相关机：固定最优边际的舍入断点与森林批量恢复

| ID | Exact scope and result | Boundary and evidence |
| --- | --- | --- |
| UM-OPT-HULL-ROW-DISCREPANCY-GAP-v1 | ∀固定实常数a,b≥1，取所有OPT(P)>0的UM-MODEL-v1输入和有理x∈conv(最优整数调度)。ell_i=Σ_{j:p_ij<∞}p_ij x_ij，s_i=max_{x_ij>0}p_ij（空0），R_ab={合法σ:∀i L_i≤a ell_i+b s_i}。R_ab总非空，且sup_{P,x} min_{σ∈R_ab} C_max(σ)/OPT(P)=2。另∀固定整数b0≥0，每机任务数≤ceil(Σx_ij)+b0的合法集也非空且sup最佳比2。 | 本族直接可最优求解；换x/集中迁移不受排除。不是配置gap、算法困难性或主目标否定。 [正文](unrelated_machines/optimal_hull_marginal_rounding_barrier.md)，内部独立审查/有限精确核验；未外审/新颖性未核。 |
| UM-OPT-HULL-PAIR-NC-GAP-v1 | ∀整数k≥2,r≥k，在私有sink族的OPT1和固定最优平均x上，∀保持全部x边际的合法随机Σ，若每对同sink不同small的联合概率≤1/r²，则E C_max≥2−1/k−(k−1)/(2r)。∀ε∈(0,1)，q=ceil(εk)≥2时P(C_max≤2−ε)≤min(1,k(k−1)/(r q(q−1)))。r≥max(k,binom(k,2))时期望下界和每个q的非截断尾上界均分别精确达到。 | 真实最优平均的组内small为正相关，不属NC类。保持正相关、重选点/选好态和一般随机算法未被排除。 [正文](unrelated_machines/optimal_hull_marginal_rounding_barrier.md)，内部独立审查/有限精确核验；未外审/新颖性未核。 |
| UM-FOREST-BOUNDARY-AUGMENT-v1 | ∀给定单边界森林gadget(V,r,K)、有理T≥0和0<η≤1，存在确定性poly(总位长,1/η)算法，返回FAIL（蕴含内部≤T无解）或实际τ,b≥0，根负载b、内部负载≤(1+η)T；对每个内部≤T的原分配ρ均b≤L_r(ρ)。用单端根任务b替换，保全局T可行性正向，任意约化调度B恢复≤max(B,(1+η)T)。同T,η每次删至少一机器的≤m次嵌套消元保持同界。 | 成功不等于原T精确可行，根b可>T。单边界承重，多边界不能逐坐标min；已有bounded-treewidth FPTAS是背景，未认证接口新颖性。 [正文](unrelated_machines/forest_boundary_contraction.md)，内部独立审查/有限精确核验；未外审/新颖性未核。 |

## 容量接口与最小总处理量初始化的锐边界

| ID | Exact scope and result | Account and status |
| --- | --- | --- |
| UM-KNAPSACK-MATROID-ENVELOPE-v1 | For all integers k,p>=1, on one weight-1 item and k weight-1/k items, the minimum over all p same-ground-set matroids whose common independent sets contain every weight<=1 subset of the maximum common-independent-set weight equals max(1,2-p/k), and is attained by partition matroids. A uniform bound 2-epsilon requires p>=ceil(epsilon*k) on this family. | [原任务地集上多拟阵容量外包的精确损失](unrelated_machines/minimal_star_contraction_and_capacity_gap.md)；独立冻结审查通过；标准工具直接扩展，主目标OPEN，外审/新颖性未认证。 |
| UM-MIN-WORK-FACE-SUPPORT-GAP-v1 | For every m>=2 the positive finite m-machine home-penalty family has OPT=m+1/m and T_LST=m. At T=OPT every minimum-total-processing-time assignment-LP point has the same support and every supported integer assignment has makespan 2m-1; the face contains an explicit vertex of the original LP. Exact nonincreasing total-work schedules have the same bad value. With integer q>=0 small off-home moves allowed, the exact optimum is max(2m-1-min(q,m-1),m+1/m). | [最小总处理量整个最优面的支撑损失](unrelated_machines/optimal_convex_fixed_slot_gap.md)；独立冻结审查通过；标准工具直接扩展，主目标OPEN，外审/新颖性未认证。 |

### 大小任务共同迁移的新增限域身份

| ID | Exact Statement | 范围、状态与入口 |
| --- | --- | --- |
| UM-FROZEN-MACRO-TINY-REOPT-GAP-v1 | ∀整数r≥1，k=r(r+1)，存在所述受限指派P_r、r²个真实最优调度平均点x及真实ST槽输出σ，OPT=1、Cmax(σ)=2−1/r；固定全部宏任务位置后，允许全部微任务任意使用其所有有限边联合重优化，精确最优为2r/(r+1)。∀固定δ,ε∈(0,1)，可选r使微任务1/k≤δ且该值>(2−ε)OPT。 | 只排固定宏任务的后处理合同；重选宏任务或换x/匹配、一般算法均不受排除。 [正文](unrelated_machines/optimal_hull_marginal_rounding_barrier.md)；独立内部已审，未外审。 |
| UM-MACRO-MIGRATION-FRONTIER-v1 | ∀整数r≥1、0≤d≤r−1，k=r(r+1)、s=r−d，从指定σ改至多d个宏任务最终机器、微任务全自由时，精确最优F_r(d)=ceil(2sk/(s+1))/k。∀实α∈[1,2)，M=floor(kα)，达到Cmax≤α的最少宏任务改数恰max(0,r−floor(M/(2k−M)))。允许≥r−1次改动时OPT=1。 | 固定改善必改r−O(1/ε)个宏任务，但不排一次改变线性数量宏任务的位多项式算法。 [正文](unrelated_machines/optimal_hull_marginal_rounding_barrier.md)；独立内部已审，未外审。 |
| UM-DEPTH-TWO-HALF-v1 | ∀显式层状简单DAG D:{r}→U→W，r/U需求为正二进制整数、W需求0，存在确定性总位多项式算法输出真实根树H，b(H)≥b*/2；对原token/filler桥梁P(D,k)，实际输出调度Cmax≤2−b*/2≤3OPT/2。根为零需求终端的情形由原桥梁精确处理。 | 标准贪心收费的局部构造；深层资源共享和一般R∥Cmax均未解决，新颖性未认证。 [正文](unrelated_machines/rooted_dag_degree_token_bridge.md)；独立内部已审，未外审。 |

## 不相关机：双边界相关菜单与单目的地路径修复

| ID | Exact scope and result | Boundary and evidence |
| --- | --- | --- |
| UM-FOREST-TWO-BOUNDARY-MENU-v1 | ∀给定双边界a≠b的森林任务gadget、二进制有理T≥0及0<η≤1，存在确定性poly(总位长,1/η)算法输出多项式大小的实际分配菜单；每项内部及b负载≤(1+η)T。∀原分配ρ，若内部≤T且L_b(ρ)≤T（a不限容），则∃同一菜单项τ使L_a(τ)≤L_a(ρ)、L_b(τ)≤(1+η)L_b(ρ)，因此严格保b=0。 | 给定结构的可恢复接口；同批任务/内部不交挂件可共享存活边界，前向乘性贡献求和不按件数累计，选好项后逆恢复max(B,(1+η)T)。不包括结构寻找、普通job替换、一般核心共同选择或免费串行嵌套。 [正文](unrelated_machines/forest_boundary_contraction.md)。独立内审及有限精确核验，未外审/未认证新颖性。 |
| UM-ONE-DESTINATION-SLOT-REPAIR-v1 | ∀m≥2及UM-OPTIMAL-CONVEX-ST-SLOT-GAP-v1的任一槽输出σ，若每原来源机器全部迁出原任务至多去一个外部目的地，则达到OPT1的最小Hamming为m(m−1)/2；强制big搬走时最小为m(m+1)/2。big不动的达到构造可按路径逐批执行，第t批后C_t=(2m−t)/(m+1)，每整批严格降1/(m+1)，t=1,…,m−1。 | 仅此显式族的正面修复与精确修改数；接收机可增载。原不限制目的地的m−1最优迁移Claim不改变。没有一般配置初始化的首次进展或统一近似结论。 [正文](unrelated_machines/optimal_convex_fixed_slot_gap.md)。独立内审及有限精确核验，未外审/未认证新颖性。 |



## 星收缩的配置接口与预处理组合边界

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-STAR-CONFIG-TRANSFER-v1 | 全邻域极小星满足逐外机配置互斥时，配置可行性双向保持，全部独立单边条件证书向前保持；单点前向仅需外部占用Q≥1。每步全球最多分裂一列，复杂度计入给定证书。 | [星正文§8](unrelated_machines/minimal_star_contraction_and_capacity_gap.md)、[冻结攻击](../reviews/unrelated_machines/star_configuration_transfer_review.md)；缺条件及逆向probe均有反例；未外审/未核新颖性。 |
| UM-CONTRACTED-SPARSE-CONFIG-GAP-v1 | 每k≥3稀疏深树沿指定合法次序收两端后，无极小星、全部最终边条件CONFIG可行，OPT=2−1/k，T=1+1/k；组合接受合同sup2。 | [稀疏正文末节](unrelated_machines/sparse_conditioned_configuration_gap.md)；双路全最终边有限核验与一般证明分开，不排共同base或主目标。 |

## 单共享汇点的宏任务共同选择

| ID | Exact Statement | 范围、状态与入口 |
| --- | --- | --- |
| UM-SHARED-SINK-JOINT-MACRO-v1 | ∀给定H∪{z}、仅homes可用且每有限边>T/2的宏任务、各任务仅在唯一指定home与公共z的非空子集可用的私有组、二进制有理T≥0及0<η≤1，有确定性poly(总位长,1/η)算法返回FAIL或实际调度，所有home≤T、z≤(1+η)T；OPT≤T时必成功，故FAIL蕴含OPT>T。私有任务无需尺寸上界，宏任务图任意。 | 仅单共享sink与唯一home的给定结构，宏任务每有限边严格>T/2承重；成功不判定T精确可行，不含一般多sink/多home转换或统一ε。标准覆盖背包+匹配的组合接口，未认证新颖性。 [自足证明](unrelated_machines/shared_sink_joint_macro_assignment.md)、[冻结审查](../reviews/unrelated_machines/shared_sink_joint_review.md)。独立内部核验，未外审。 |

## 对称共同条件矩的运输与重新耦合

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-SYMMETRIC-JOB-AGGREGATION-v1 | For every nonempty bounded one-hot rational P, symmetric normalized certificate (x,Y), and given deterministic jobwise aggregation/deletion R with at least one retained job, mapped old true columns in their scaled P-prime imply (Rx,RYR^T) is a same-layer certificate. With no retained jobs check the zero-dimensional base separately. Given data and explicit P-prime can be checked in bit-polynomial time; finding R is not solved. | [正文](unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)、[冻结审查](../reviews/unrelated_machines/symmetric_moment_reset_review.md)；限范围完整证明/双路精确审计，外审与新颖性未认证，主目标OPEN。 |
| UM-SINGLE-MACHINE-MOMENT-RESET-THRESHOLD-v1 | For each q>=2, m=2q machines and n=2q^2 identical jobs p=1/q,T=OPT=1, the uniform balanced true-optimum moment matrix needs exactly 2q absorbed jobs for some deterministic single-machine fallback pushforward to satisfy residual true/false capacities. Every c<2q and every fallback fail. At c=q balanced groups, the same first moment Rx has a rebuilt true residual T-distribution, in deterministic bit-polynomial time. | [正文](unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)、[冻结审查](../reviews/unrelated_machines/symmetric_moment_reset_review.md)；限范围完整证明/双路精确审计，外审与新颖性未认证，主目标OPEN。 |

## 共同拥塞流、支撑选择和单位走廊的准确身份

| ID | Exact Statement | 范围与入口 |
| --- | --- | --- |
| UM-DAG-CONGESTION-FLOW-v1 | ∀显式根简单DAG及二进制非负需求（零需求仅原终端），∀整数K≥1及含根支撑W上的正文共同K证书，可确定性总位多项式用一次整数流输出真实根树b≥1/(2K−1)。固定W,K的证书可行性与一整数流饱和等价；可行性对K单调，可位多项式求最小可行K或报告该W无证书。∀K≥2存在本合同证书族且真实b*=1/(2K−1)。全支撑最优κ*在b*>0时满足(1+1/b*)/2≤κ*≤ceil(1/b*)；给评分β>0的实际树及K≥1/β可构造其支撑证书。 | W、K明确输入，允许不可达组件、正需求死点、任意根、极大二进制需求；K为整数。输出可用E[W]的零f边。给定W的不可行不意味着无好树。没有一般支撑搜索、统一常数K或一般调度算法。 [自足正文](unrelated_machines/rooted_dag_congestion_flow.md)、[冻结审查](../reviews/unrelated_machines/rooted_dag_congestion_review.md)。独立内审及精确有限核验，未外审/未认证新颖性。 |
| UM-DAG-ACTIVATION-CORRIDOR-GAP-v1 | ∀整数q≥2，正文四段DAG有1+q(q+3)点、2q²+2q边，根/走廊需求1、q个分叉点需求q、末端需求0。加强激活LP a_r=1、非根a_v=Σ_u x_uv≤1、Σ_w x_vw≥k_va_v、0≤x_vw≤a_v精确有理可行，但真实根树最优b*=1/q。 | 仅上述激活边际LP的统一正常数充分性反例；未满足或否定共同K强证书，未导入SA或调度困难性，未认证全球新颖性。 [自足正文](unrelated_machines/rooted_dag_congestion_flow.md)、[冻结审查](../reviews/unrelated_machines/rooted_dag_congestion_review.md)。独立内审及精确有限核验，未外审/未认证新颖性。 |

## 独立均匀选择的正面条件矩运输

| ID | 精确范围与结论 | 正文与状态 |
| --- | --- | --- |
| UM-INDEPENDENT-UNIFORM-MOMENT-RESET-v1 | For every q>=2 with m=2q,n=2q^2,p=1/q, the fixed uniform balanced optimal-distribution matrix under independent uniform rerouting of old deleted-machine choices satisfies residual P0(1) true/false capacities iff absorbed integer job count c>=q+2. Other old choices stay fixed; no conditioning on absorbed labels. Exact moments are deterministically bit-polynomial computable; transported states may still have load2. q=1 separately has threshold1. | [正文§9](unrelated_machines/symmetric_moment_reset_and_single_machine_threshold.md)、追加冻结审查和双路真实矩核验；非调度算法，m=2q不可省，主目标OPEN。 |

跨路线[补充审查](../reviews/unrelated_machines/joint_capacity_route_feasibility_review.md)仅核所列UM接口和拼接义务，未更改上述Claim量词、状态或新增主目标算法。

## 固定数量共享汇点的共同占位与实际调度

| ID | Exact Statement | 范围、状态与入口 |
| --- | --- | --- |
| UM-OCCUPATION-MODE-SIDE-CONSTRAINT-v1 | ∀有宏全覆盖匹配的有限宏/home二分图、每home有限非空带0/1占位标签的模式库、整数K≥0，P={每home模式和1、占位边际属于宏可匹配home基凸包}加任意K个线性侧不等式后，每个模式投影顶点至多2K个home有多于一个正模式。正支持内可用整数下界匹配和实际模式恢复，仅改变这些home；不承诺侧预算保持。 | K可随输入增长；一般结论只给2K支撑界。模式只依占位bit，不能依具体macro身份/残余容量；所有额外耦合约束须计入侧约束rank。 [正文](unrelated_machines/fixed_sink_occupation_rounding.md)、[冻结审查](../reviews/unrelated_machines/fixed_sink_occupation_review.md)。限域完整证明，未外审/未认证新颖性。 |
| UM-FIXED-SINK-PRIVATE-GROUP-THREE-HALVES-v1 | ∀固定整数K≥1，∃确定性A_K，∀给定H∪Z(|Z|=K)、仅H可用且每有限边>T/2的宏任务B、不交私有组J_h（每件仅{h}∪Z的非空子集可用）、二进制有理T≥0，A_K按输入总位长多项式返回可靠FAIL或实际调度Cmax≤3T/2；OPT≤T必成功。私有尺寸任意，有限p>T先剪枝。多项式次数依K。 | 给定T的one-sided资源增广；成功不判定T精确可行。固定K与唯一home分组承重，不提供一般实例分区/分组提取，不含K增长的统一多项式保证。 [正文](unrelated_machines/fixed_sink_occupation_rounding.md)、[冻结审查](../reviews/unrelated_machines/fixed_sink_occupation_review.md)。限域完整证明，未外审/未认证新颖性。 |
| UM-FIXED-SINK-MACRO-PROMISE-APPROX-v1 | ∀固定整数K≥1，∃确定性位多项式算法，∀同给定H/Z/B/私有组但无T的合法实例，若每条有限宏任务时间严格>OPT(P)/2（B可空），则输出实际调度Cmax≤3OPT(P)/2。零最优值精确零输出；算法不验证含OPT的promise，不要求给OPT或好调度。次数依K。 | 含OPT的大宏任务promise与结构分区为额外假设；不是一般UM-TARGET-v1。通过共同分母整数网格及可靠FAIL/任意成功负载界二分，不假定接受集合单调。 [正文](unrelated_machines/fixed_sink_occupation_rounding.md)、[冻结审查](../reviews/unrelated_machines/fixed_sink_occupation_review.md)。限域完整证明，未外审/未认证新颖性。 |

## 真实最优凸包初始化的长链修复边界

| ID | 精确范围与结论 | 正文与限制 |
| --- | --- | --- |
| UM-OPT-HULL-LONG-CHAIN-LOCAL-GAP-v1 | ∀k≥3,d≥1，两个真实OPT1调度平均点的全部mincost ST输出σ都有Cmax=2−1/k；严格lex改善的最小任务支持d+1、最小新旧端点参与机数d+2同时达到，每源仅迁一件。 | [循环正文§10](unrelated_machines/cyclic_batch_repair_and_fork_obstruction.md)、[冻结审查](../reviews/unrelated_machines/optimal_hull_long_chain_review.md)。中性Cmax链尾预修明确可行，未排一般算法，未外审/未核新颖性。 |

## 守恒扩区与非单位分叉参数的独立身份

| ID | Exact Statement | 范围与证据 |
| --- | --- | --- |
| UM-DAG-TRANSIT-CONGESTION-v1 | ∀上述合法D,k,r,K，新共同证书可总位多项式提取真实树b≥1/(2K−1)，每个K由单边k_r=2K−1族精确达到；固定W/K证书与一次整数流饱和等价，K可行单调且最小K位多项式可求。令h_K=#{k≥2K}，枚举这些高点子集、免费补入全L/Z，在2^{h_K}poly(总位长)判定某W证书并输出W/f/树。旧k≥K合同同W/K证书可拓扑裁流转新，反向不总成立。 | 新合同另立身份，不更改UM-DAG-CONGESTION-FLOW-v1。指数因子2^{h_K}仍在，未证明一般好支撑可多项式搜索，未给统一常数K或一般UM算法。 [正文](unrelated_machines/rooted_dag_congestion_flow.md)§7–10、[冻结审查](../reviews/unrelated_machines/rooted_dag_congestion_review.md)。内部独立核对，未外审/未认证新颖性。 |
| UM-DAG-NONUNIT-PARAMETER-EXACT-v1 | ∀上述合法D,k,r，令h=#{v:k_v≥2}和总二进制位长B_in；有确定性2^h poly(B_in)算法输出实际根树H，精确达到b(H)=b*。含b*=0、根终端、巨大二进制需求；不按k数值枚举。 | h是输入参数，任意h时2^h不是多项式。此为根树对象的精确FPT算法，不承诺一般调度近似，不免费从任意处理时间矩阵取得需求树结构。 [正文](unrelated_machines/rooted_dag_congestion_flow.md)§7–10、[冻结审查](../reviews/unrelated_machines/rooted_dag_congestion_review.md)。内部独立核对，未外审/未认证新颖性。 |


## 宏任务真实退出与完整profile接收池

| ID | Exact Statement | 范围与证据 |
| --- | --- | --- |
| UM-SHARED-SINK-MACRO-EXIT-v1 | ∀显式给定H∪{z}及宏B/唯一home私有组、非负二进制有理T≥0与0<η≤1；macro可在home或z使用，所有有限home宏时间>T/2。存在确定性poly(总位长,1/η)算法FAIL或输出home≤T、z≤(1+η)T的实际调度；OPT≤T必成功。宏数可超过home数，OPT0保持0。 | 仅单sink、唯一home与给定macro划分；不限制macro sink大小，不提供一般多sink容量恢复或一般输入划分。 [正文§8–10](unrelated_machines/shared_sink_joint_macro_assignment.md)、[独立审查](../reviews/unrelated_machines/private_group_exit_pool_review.md)。 |
| UM-BOUNDED-PROFILE-EXIT-POOL-v1 | ∀显式给定H∪Z(Z非空)、同样macro/唯一home私有组、T≥0、0<η≤1、ρ≥1、β≥0、a_z>0及c_j≥0；每任务在Z全可用或全不可用，前者逐z满足a_z c_j≤p_zj≤ρa_z c_j及p_zj≤βT。存在确定性poly(总位长,1/η)算法FAIL或实际调度，home≤T、各pool≤[ρ(1+η)+β]T；OPT≤T必成功，OPT0保持0。 | sink数不固定，但完整资格、给定共同profile上下包络、各pool边≤βT及唯一home承重；不输出一般矩阵分解，非一般统一ε。 [正文§8–10](unrelated_machines/shared_sink_joint_macro_assignment.md)、[独立审查](../reviews/unrelated_machines/private_group_exit_pool_review.md)。 |

## 有限覆盖的精确配置实现与反向困难性边界

| ID | Exact Statement | 范围与审查 |
| --- | --- | --- |
| UM-CONFIG-FINITE-COVER-v1 | ∀合法UM实例P，∀有限置换incidence覆盖Q，T_CONF(Q)=T_CONF(P)且T_CONF(P)≤OPT(Q)≤OPT(P)。∀整数g≥1，min_{有限cover Q,incidence girth>g}OPT(Q)=T_CONF(P)，最小值取得；不加g时可取q≤r^(r/2)，r≤m+n为配置等式系统rank。给定有理配置证书可输出敏感地精确实现为某cover的真实调度。 | 仅原机器/任务等q复制及逐incidence置换、保原时间的覆盖；高围长存在性不保证小尺寸或随机概率。未排精选接线/扩张条件/其他归约，未证明UM-TARGET-v1反面；不提供相对原输入的位多项式配置求解或覆盖输出。 [自足正文](unrelated_machines/configuration_finite_cover_obstruction.md)、[冻结攻击](../reviews/unrelated_machines/configuration_finite_cover_review.md)。独立内审/有限精确核验，未外审/未认证新颖性。 |

## 共同资格私有组的无界接收机联合流

| ID | Exact Statement | 范围与证据 |
| --- | --- | --- |
| UM-HALL-GROUP-JOINT-FLOW-v1 | ∀显式H∪Z、宏B/私有组J_h、整数q≥2、有理T≥0和δ≥0且qδ<2；macro仅homes且所有finite p>T/2；j∈J_h恰在h及同组共同E_h⊆Z可用且时间同为w_j≥0，(1/2+1/q)T≤W_h≤T、w_j≤δT。确定性总位poly返回FAIL或完整实际σ，Cmax≤q(2+δ)/(q+1)T；OPT≤T必成功。含T0、空Z/E及二进制q输入，实际机器至少一。 | 给定分组、同组共同资格、私有任务等端体积及组负载下界承重；q增长时改善趋零，不是一般UM统一ε。 [正文](unrelated_machines/hall_group_joint_flow.md)、[冻结审查](../reviews/unrelated_machines/hall_group_joint_flow_review.md)。 |
| UM-HALL-GROUP-PROMISE-APPROX-v1 | ∀同拓扑及q≥2,δ≥0,qδ<2，不给OPT；promise在真实OPT处所有finite macro p>OPT/2、(1/2+1/q)OPT≤W_h≤OPT、w_j≤δOPT。存在统一确定性总位poly算法输出完整实际σ，Cmax≤q(2+δ)/(q+1)OPT，OPT0含在内。q/δ可输入；固定q/δ时为该承诺类统一低于2。 | 不判定关于OPT的结构承诺；不提供一般矩阵分解，同组共同资格/等端体积和组负载范围保留；可变q时无统一正ε。 [正文](unrelated_machines/hall_group_joint_flow.md)、[冻结审查](../reviews/unrelated_machines/hall_group_joint_flow_review.md)。 |

## 真实最优矩的固定阶压缩向量贪心

| ID | Exact Statement | 范围与入口 |
| --- | --- | --- |
| UM-TRUE-MOMENT-VECTOR-GREEDY-LINEAR-GAP-v1 | 每固定r≥1、每素数q>4r+2，q台机器/q+1任务的显式实例有真实最优源D，OPT=4r+2；固定V_r压缩乘法向量范数贪心在任何任务顺序上都严格把q个普通任务送0，输出比q/(4r+2)=(n−1)/(4r+2)。一般真实T源下该规则合法且≤nT；固定r故最坏量级线性。 | 固定D/V_r/A_e并逐任务最大化‖A_eψ‖²；源矩真实，选择严格。不是任何层级gap。固定r矩输入位多项式，不提供最优源oracle。[自足正文](unrelated_machines/truncated_multiplication_vector_greedy_barrier.md)、[冻结审查](../reviews/unrelated_machines/truncated_vector_greedy_review.md)；内部审查/有限核验，未外审/未认证新颖性。 |

## 逻辑使用规则

- 所有“上界”都量化到每个满足输入条件的实例；有限运行不是其证明。“下界”要求明确属于同一个实例类，且量词是对每个更小因子存在反例。
- EXACT-KAPPA、MITM-EXACT 返回特定实例的最优因子；SC-PHI-A、HC-2-UP 返回符合普遍上界的一个因子。不能从一个短的达到证书推断它已达到实例最优。
- 保留历史稿中的推导供追溯，但以[现行分支](README.md)的命题条件为准。修改条件时新建 ID 或明确版本，不覆写旧 ID 的含义。

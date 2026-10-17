# 每机至多两条非单位正时间资格：精确三半近似合同（仅陈述）

ID `UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`。root已据hardness_route的阈值合同自行提出全类算法及下界；作者不是盲审。本文件不含证明。旧threshold v1来源不倒改，不升级一般UM目标。

输入是完整普通UM：m≥1，n≥0，finite p_ij为binary非负有理，其余∞，每job至少一条finite边；另给binary有理b>0，所有finite p_ij≤b。对每个machine i，其全部job资格中满足0<p_ij<b的不同job数至多2。时间恰b的unit资格数量无限制；一个job可有任意多个small端与unit端，不假设每job只有一个small或资格≤3，不限制共享/环或机器时间行和。时间0资格不限数。复杂度按完整P和b的总编码长度，输出全部原job的一个finite端。

精确结论：

1. 存在确定性总位多项式算法，对上述所有输入输出具体合法σ，Cmax(σ)≤(3/2)OPT(P)。OPT=0、所有/部分job有zero端、n0、单机、没有实际b端和binary极端尺度均覆盖。不依赖randomexpectation、估值或固定机器数。
2. 对每个给定binary有理0≤T<b，存在确定性位多项式精确可行性判定，OPT≤T当且仅当返回完整C≤T的真实σ；失败可证OPT>T。可按显式输入位长多项式求出最优值在[0,b)内是否存在，并在存在时输出exactOPT调度。
3. 对每个给定有理T=b+a，0≤a<b，存在确定性总位多项式程序，若OPT≤T则输出完整C≤3b/2+a≤(3/2)T调度；否则允许返回FAIL，但任意FAIL均保证OPT>T。此项程序成功时也满足该负载界，不用YES witness，不隐含调用OPT oracle。并非声称若OPT>T程序一定FAIL。
4. 因子3/2在复杂性意义下sharp：对每个固定ρ<3/2，本结构类不存在保证ρ的确定性位多项式近似算法，除非P=NP。困难性已在b=1、所有finite时间仅1/2或1、每job最多两种时间（端数仍可多）、无zero资格的更窄子类成立。给出从显式非空perfect3DM的确定性位多项式归约，YES OPT≤1、NO OPT≥3/2，且所有机器仍至多两条positive small资格。退化无可用triple的源可用合法常量NO实例处理。

这是结构类的实际算法与匹配复杂性下界，不是一般UM统一离二算法，也不证明一般UM反面。证明/构造、bit复杂度及外部标准3DM源须独立核；代码实现、有限运行、新颖性与独立论文价值未认证。若日后扩到三条small行或其它times另立版本。

# 逐源解析自查

五主源均为Markdown。此次自查为逐式解析和证据范围核对，数学程序调用0；不以无关有限扫描代替一般论证。

1. **HYB合法性。** Q只作分析基线；将未替槽扩到完整T后仍恰m合法槽。丢失集合要求owner在J且所有J内coverer缺席，不能用仅整叶R替代all-J库存。概率丢失p(1−p)^k中的owner不在coverer集合，否则客户不会丢失。
2. **HHYB端点。** 除p的p=0是可去端点；外部cJ=0为H0=0，owner缺失cJ=0积分为1。没有把IC按p或客户重权。
3. **A割。** b(J)=ΣcJ/c≤外部覆盖；M(J)每客户恰给1出割，已覆盖用全部J外真实份额、未覆盖用终点。源割为b(Jc)+capacity(J,Jc)，方向与净流出一致。
4. **B割。** kHc/c≤Hk来自递减前缀均值；missing-owner客户出割(1+l)/(1+k+l)与所需1/(1+k)之差为kl/[(1+k+l)(1+k)]≥0。终点包含已被非owner覆盖客户；不能把它说成真实遗漏。
5. **B锚定。** Qi⊆Bi使outside_i=0、owner全部不在E，source/自有出边/终点全0，非负流守恒迫使入流0。此论证不自动适用未改普通A图。普通A锚定排除A客户需另建O\A残余图；完整OPT前缀才保障活跃角色真实IC左端。
6. **资金强度。** B调和源可大于普通利润，两个不交最优singleton、两个玩家重复第三singleton时3/4>1/2。A/B客户容量不相加；任意合法B不等于原IC规定叶；逆角色运输不等严格未来流。
7. **ACT/NET/source。** actual A只用I边与R终点；gamma+out−in=g，in≤I给gamma+out≤u。固定delta_i≤g_i在全部角色割同时预送，eta=I+gamma总和W；source二分证明共用此eta而非u加eta。后续incoming仍未付。
8. **捕获守恒。** R客户actual过去零负载，c=1+future；每输入current及全部future份额和1，角色严格增。重置原actual前缀而非继续旧叶；正A保证D>0，A/D仅付总吸收，不逐客户支配输入。
9. **根regret。** tau所有正深度SPE而根可任意；D1≤u1+Delta，其余D≤u。根唯一初始主题无incoming给L1≤1。B=Σ(L−1)u必须signed。END依次给B−g−(3−L1)Delta和更粗B−g−2Delta，方向未反。
10. **精确税余额。** E=Σw(u−D)≥−L1Delta，E'=E+L1Delta≥0；逐项代入得|O|−2W−3Delta=B−g−E'−(3−L1)Delta。其它surplus已消同一slack时不能再留E'信用。比较T非最优时不将|O|叫OPT。
11. **旧强桥。** 71客户k=3完整SPE的唯一最优R36>W35，但G33、净缺口3；所以全源所有L≤1被阻断，不是half反例。已全文比较现有全参数反例及其输入版本说明，未新造/复跑此例。
12. **自由接纳。** 不同客户/来源的query分配只改A，最后每query唯一w=A/D；未接纳质量仍须守恒或有停止预算。无共享cap的Bellman可统一固定所有(i,x) argmin；H=V−1的分母是1+|F|，每项真实原税非负。自由起点不是角色容量一matching，也不继承唯一初始主题根cap。
13. **I^-激活。** owner∉actual J是独立性的关键；每coverer信用(1/c)∫[1−(1−p)^c]dp=1/(c+1)，query库存∫(1−p)^c dp=1/(c+1)，合计1。actual信用是error，kappa_i^-是1/[c(c+1)]的边际，二者不混。
14. **MARG事件。** 当前在J时A=0；source owner事件给1/(L+1)，nonowner事件含owner/i active、J∪F inactive，积分1/[(L+1)(L+2)]。L≥b+|F|保留真实背景，正负角色集合不交；没有暴露J-none后偷用独立性。nonowner reset使原owner处在actual过去且仍未覆盖，才能用对应ell。
15. **共享付款。** R/I先合A后只取一个w，A≤ell≤D给每state≤1而不控制row和。I-query增加同一kappa源，所以预算W+kappa减kappa才得half，不把停止信用或新增目标当额外福利。
16. **U与取消。** 单U实现相同单客户边际但可有不同跨客户相关；R源每world存在，允许world依赖Hall-A取消。此时只能保A≤ell，不能乘E rho。Hall-B I-query条件删除必须U前固定lambda，否则E[(lambda/kappa)1query]不必等于E lambda。两种G不叠加。
17. **有限与先验。** A/B历史报告9/14/852、11474割及两图各852只作已冻结有限输出；自由κ报告9类13叶、portfolio W41及非1价格，不混上批W44单证书。两报告本批只读。owner审查非盲、激活陈述后重构、free主稿当时待审、无外审各保真实身份。
18. **现行模型。** SAFE净列P、含税采购p、full-O坐标2u ROLE、自然recipient以及自由query的源/分母/钱包不互换。五人later theorem保有效，六人和一般root-only目标均不因这些局部组件闭合。

上述18项解析检查通过。独立文件检查程序只核原件字节、报告结构、receipt目标和链接，不调用任何原数学程序或求解器；结果另存artifact-check.json。

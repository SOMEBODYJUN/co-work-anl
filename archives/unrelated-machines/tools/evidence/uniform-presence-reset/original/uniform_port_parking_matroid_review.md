# 统一端口、余横截间隙与实际调度推论的独立攻击

两个合同必须分别读：[现行正文](../../current/unrelated_machines/uniform_port_parking_matroid_gap_and_actual_approximation.md)。UM-COTRANSVERSAL-UNIFORM-CONFIG-SHARP-GAP-v1给边际/LP gap，UM-UNIFORM-PORT-PARKING-PAPER-APPROX-v1给相对真实OPT的published算法推论；后者没有把坏LP证书变成常数保留。

## 显式gap的陈述先行重构

root先向一名未读其他审稿的独立者只给m=D+1精确对象及三个matroid结论/完整UM结论。对方独立发现真实Hall邻集仅m个所选A及D个B，严格少于每人2份的2m需求，及每人1份的达到匹配。冻结盲稿SHA256 `23e45ec0fba539aa2206c114de7e65c20c046f31f4ffea597be8e957a0a513b8`。另一名审查者另核该m=D+1修正与完整P/LP证明、纯右列失效，稿SHA256 `bc1991b00dabfe7e0f1f6a3de9fcf2d61d0fc78356e38548f52811e05d2f8845`。较早m=D版本只给2/D，不拿其审查冒同一个对象的审查。

root亲自重构全部计数与每机全负载：每C独立需提供完整aux matching；y∈P(M)需实际D项独立凸分解，不只看总rank；任意低C原σ使每所选parent至少送2ports才触发同一个Hall证据。所有未选states、mandatory任务、selector及外机都已计入。每C单独能停车不等于所有chosen C能同时停车；总rank不能代替这些任务的真实邻接集。

## 实际算法桥的先陈述后证明

精确算法陈述SHA256 `933e587e31b4364b0fb83b66bd95db4bdafcfc0dcf3adaac7e35d85b031d1288`先交另一名审查者。对方先实读BLMRS v1 Theorem4/Definition7/§4/Lemma22并独立重构，冻结SHA256 `3b5c2f2a9f717235bccbfe69da54d6c32969bfc9852e0d404b8cf775df8936d1`；之后才读拟议桥梁证明SHA256 `8087dc6554bcc920edc859e56f29003b8d6f6ec7465b382e37a54d59bde5496f`，读后稿SHA256 `454a96240f32622aa147b5bdf85b296d1e3318bafc787a6f63945cacd6846b7c`。接口分别无standing fatal。

- P_f的ground是variant players，f(X)=r_M(∪C_p)是整数次模；不是把items-ground global matroid误作同一source model。
- Rado lifting：整数计数可由eligible-pairs parallel extension与partition matroid intersection恢复实际资源。每resource只用一次，输出的是实际I_p，不只rank值。
- 大资源每u有R_u−1份，虽然可多份给同一variant，仍有至少一个variant未收到；取该variant并丢其它cheap分配保持独立。反向可给其它每variant一份，故SC最优精确Dβ*。
- 两值intrinsic values只有1与D，source与player无关，Definition7允许integer polymatroid；独立allocation可扩到base不减效用。D1及单label组均合法。
- Vacancy dual需aux unit可匹配；Baux≥2先做精确bmatching分支，不偷假设所有输入都有C1 parking。U空只有aux，完全空输出0/dummy。
- C<2使外部unit jobs共同占用互斥，活跃parent负载2−t/D；OPT=2−β*双向及β0边界成立。比例(2−β/α)/(2−β)在[0,1]递增，最大2−1/α。
- D和labels/ports全部显式，matching rank值≤|R|，固定η调用，所有后处理确定性位poly。没有把D_u不等时按player缩放的非polymatroid当同一资源。

root亲读原PDF相关定理与定义，逐式核桥梁。此结果扣除published Theorem4及标准matroid工具后只是准确应用；未宣称新通用近似定理或重证原local-search全文。

## 实现证据与限度

[精确家族代码](../../../tests/audits/unrelated_machines/cotransversal_uniform_configuration_gap.py) SHA256 `b23a7852f058c005a1e412dd6443cbbd15509e066ccf4706fb3a2e807ec82f92`；[冻结输出](../../../evidence/runs/unrelated_machines/cotransversal_uniform_configuration_gap_audit.json) SHA256 `e266450a58cc43111e0be2d21bcae11d65d3cef78eb665225cb5e2e096945169`。root全文读代码并完整复跑，JSON所有字段相同。

D3/D4分别63/124 machines、76/165原jobs、135/284显式配置，均逐项Fraction核每行和每job覆盖恰1；12/20个单C完整停车匹配、3/4个边际原子匹配。利用各u状态排列对称性，把任意state选择归到a0，完整枚举81/7776个两port/人模式，核实际Hall邻域至多7/9而任务数8/10；不称穷举所有完整UM调度。实际原σ全job回算给5/3、7/4。

只有显式gap家族与证书生成器已实现。相对OPT算法依赖的BLMRS/matroid程序未在本仓集成，未声称有生产实现或新的实际运行。所有限定证明/内部审查、实现、外审、新颖性分开。一般UM-TARGET-v1正反面不由此升级；真实hardness仍须退出这个统一D合同或增加另一种可验证机制。

最终gap整合审查实际核正文SHA256 `f617f2cf3fcfc8e02174046bcd695322cac732869c4d5cf19beab4249bcf8970`；发现括注曾可误读为每parent一selector，已明确改“每parent D枚ports；每u一枚selector可选其D个parents”，共同合同与原证明一直采用每u一个selector。审查者实际读改句后确认，未冒审另由cover核过的published算法。

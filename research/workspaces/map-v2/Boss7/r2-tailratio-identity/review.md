# r2-tailratio-identity 精确复核与最小接续

结论：两条被审边的数学都有效，均应继续保留为 `contribution`；问题是一个未核到canonical资产的“已发布一般边”断言。最低改动是只替换可信r4联合锐性边中的发布身份文字，并以同一已列正文(T)作直接证据。scalar高域根下界边完全不改，沿原SHA继承。不存在重写通用数学、修改端点登记或处理Boss5归属的需要。

本次只在指定staging写报告与草稿；没有Git、队列或clone写入，没有重跑任何科学实验。父Boss给出的恢复HEAD为 `1431d23cd6acf489255177974720ed1ff6cf0847`。本报告的实际字节锚见 `pin-summary.json`，不是对该HEAD以外远端最新状态的推断。

## 发布身份：当前具体核到什么

精确声称的ID为 `cag-7046-stationary-envelope-pays-full-tail-ratio`。当前树中的 `map/edges` 及 `research/registry.json.edge_files` 没有此edge的canonical资产；其任务预留目录 `map/edges/customer-attraction-3a-3a-7046ca9f679c3332` 也不存在。精确ID只见于r4边explanation、该包收据comparison_scope、done任务内嵌收据和派生coverage等叙述；没有可核的path/SHA、endpoint_pins、whole_result及review_digest，故不能把它当作已发布图证据。

相关任务 `customer-attraction-3a-3a-7046ca9f679c3332` 当前本地为 `Boss5 / claimed`，request为 `2ddce2ac1e6442a9bb585cc8a8ef5fdc`，任务文件SHA为 `3215796c92d85401ee301c3932f4b56e84b0d4712c1ffac45f1244ad827669c9`。父Boss已说明此前远端仍claimed、通知Boss5后尚无回复。本worker不推断其进程是否活跃，不建议抢占。若Boss5正在交付，所需精确接续是请其给该一般比例边的最终edge_id、路径、SHA、实际source/target及whole_result；核准后再接回3D，而不是替他生成重复的一般比例边。

受影响的原包 `ca-four-rook-regimes-recovery-3a-b5f11187db89543b` 当前仍为Boss5有效done，没有当前本地done替代者。它的全部输入pin与现registry一致，三个资产实际字节均吻合原收据SHA并已列入canonical。只是发布身份文字需定向修复，不是数学失效或输入过时。

## 一般WS到比例：(T)本身已完整支付

实读《驻留根菜单的最优标量包络与尾收益界》全文，特别是“模型、路由与逐客户量”“最优逐客户包络及点态证明”“对真实尾收益的条件推论”。原文(T)前的原句准确限定：“如果所分析的全部真实根分支中，根收益均不超过u、每个后继收益均至少t≥0”。这里是同一策略的全部真实强制根菜单；不能给每个根另挑一份续局，也不能把尾部在轨动作冻结后重用。

令n=r−1，q=floor(n²/4)，M_r=r+q=floor((r+1)²/4)。驻留与包含归属给S_x=E(M_i−K_i)≥0。原文逐客户(E)由I=0时K/(b+K)≤K/(b+1)、I=1时q≥K(n−K)逐点成立，因此直接得到聚合(G)：P≤M_rD。背景可在代数上为非负实数，真实原游戏的过去负载仍是整数；K的整数性不能删除。

全部根枝根收益≤u给D≤u；每枝r−1个真实后继均≥t给(r−1)t≤P−D。故

\[
(r-1)t\le P-D\le(M_r-1)D\le(M_r-1)u,
\qquad
u\ge\frac{r-1}{M_r-1}t.
\]

这就是原文(T)，r≥2时M_r−1>0。完整SPE的根IC可提供u为当前实际收益的统一根上界，统一尾下界仍须另证。该推导完全不需要另一个已发布edge文件；直接引用当前边已经列入evidence的正文(T)就够了。它证明一般r的**条件比例**，不证明一般r、背景和目录都存在真实完整SPE锐例，也不把系数提高成1。

## r4、18客户、同一完整纯SPE：联合锐性逐项成立

实读四人车图定理全文及锐菜单构造全文。取R=4、C=3、三行两列共六标签；客户总数3·4+2·3=18。定理的三人同列完整策略适用域是R≥C/3，含弱端点。其关键IC比较为R+C/3与R/2+C/2之差R/2−C/6≥0。在(4,3)处此差为3/2；其它前二历史的第三位按规则达R+C/2的上界，末位在每个历史选最低负载行列，第二位各替代行动的真实续局也已在该策略规则中付清。因此这是对全部有序离轨历史定义的一份完整纯SPE。

每个强制根(i,j)之后依次是另两行的同列标签，最后为根行另一列标签。四人收益均为(3,5,5,5)。全部六根使用同一策略，强制根收益都为3；每个根枝的每个真实尾都为5。六个根菜单恰构成三正则连通无向车图，均匀π=1/6是唯一驻留。真实尾使用完整归属主题，故K=M，逐客户S_x=0。

对任一行客户，属于根的概率1/3，内外根K均为1，所以D_x=(1/3)/2=1/6、P_x=1、S_x=3·(1/3)−1=0。对任一列客户，属于根的概率1/2，内部K=2、外部K=1，所以D_x=(1/2)/3=1/6、P_x=1、S_x=3·(1/2)−3/2=0。n=3时内部K=1或2都给K(3−K)=2=floor(9/4)，外部K=1也使点态不等式取等。故每名客户P_x=6D_x，总D=3、P=18，P/D=6。

取实际统一界u=3、t=5，得到

\[
3t=15=P-D=(M_4-1)D=(M_4-1)u,
\qquad u/t=3/5.
\]

所以WS的r4,b0倍数6和M-bed的r4,b0比例3/5分别不可改善，且由同一真正完整SPE共同见证。这里没有将“否定两式的合取”冒作分别反驳两个目标：任意把6减小都会被P/D=6否定；任意把3/5增大都会被u/t=3/5否定。

范围严格只到r=4、b=0的真实SPE锐性。构造正文对r≥5的原精确网格给末位严格偏离，因此不能从该菜单扩成所有人数的SPE锐性。W=OPT4=18，也不支付低福利反例或一般θ/v/t首位保证。

## scalar高域根下界边：原字节可保留

scalar边并没有声称一般7046边已发布，也不需要(T)来证明其结论；它直接用(G)的P≤6D。原解释独立证明六个强制根都全覆盖：若最终行为(3,1,0)，前三人必同一行，第三人原收益至多R/3+C/2；改空行及此前低负载列后，末位仍有另一空行严格优选，第三位保证R+C/2，矛盾。两列也由末位最低负载规则覆盖。因此每枝P=3R+2C，根IC给D≤u，故u≥(3R+2C)/6=R/2+C/3。

该推导对全部R,C>0成立，精确支付R≥C/3（含弱端点）域L公式的下界。低域的R/2+C/2仍差C/6，达界策略及三种静态门槛也另需证明。原contribution.result/remaining已准确写出这些范围，所以本次对此边应作零文本diff并保留 `acd64a7ec9ddbf1ee55bd54dac8168fafd0187d934247767b3271ef62436210d`。

## 最小定向repair与完整继承

`draftdiff.json`逐字段给before/after，`draftdiff.patch`提供易读统一差异；它们只是用于新repair文件的语义草稿，不能直接覆盖旧done资产。必要修改只有：

1. 新copy的可信r4边explanation中，将“已有cag-7046…”换成当前已列正文(T)的直接条件推导；review_note中将“已发布whole_result边直接复用”换成“直接使用正文(T)”；contribution.remaining明确一般条件比例有独立正文证明，r4专例只付r4,b0锐性。
2. 新收据comparison_scope不再声称完整比较未核到的7046资产，改写为完整核对同一正文(T)；reason补明其一般条件链与r4锐性的量词区别。保留原核心、输入pin、三条accepted边ID及原其它比较结论。
3. 旧scalar边和旧exact-regime边按canonical原路径、原SHA保留；只给修订的credible边配置新repair写入路径和最终新SHA。新边语义文字定稿后由Boss复核、edge-bind --write及edge-check，再计算新资产SHA。
4. 新task正常supersedes原有效done包；新收据supersession中旧credible标replaced、指向新路径，旧其它两边标retained并在assets保原SHA。新包done后assemble更新coverage/registry/integration，从新收据消掉派生coverage中的旧发布说法，不人工改历史任务或旧done收据。

机器可读完整继承计划见 `inherit-assets-plan.json`。其中 `<directed-repair-task-id>` 只是新任务ID占位，须由Boss正常发布repair后替换；该计划不是可直接done的回执。旧exact-regime边本次仅检查资产、endpoint及登记绑定的一致性，不借此扩称重新审读了其所有旧计算证明。

全部端点、三资产文件SHA、收据文件SHA/语义pin、当前registry快照SHA及Boss5 claimed任务字节锚均见 `pin-summary.json`。此处没有新增一般WS→ratio边，也没有请求或更改Boss5任务归属。

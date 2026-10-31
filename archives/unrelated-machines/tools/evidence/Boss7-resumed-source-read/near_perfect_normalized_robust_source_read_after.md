# 近完美源作者证明读后与最终规范正文交叉核查

日期：2026-10-18。读者：near_two_reduction（boss11 内部研究 subagent）。本次按root明确顺序实际全文读取两个文件，均只读；未改共同repo、未做git写入、未spawn。

## 1. 顺序、版本和审查身份

1. 本轮之前，只读源 Exact 并独立重构后冻结了 `near_perfect_normalized_robust_exact_first_attack.md`，SHA256 `283d29ac050a0757dcd8dd76c4fd2d68ba472f1dc70bc5a0212c19966326d779`。该记录明确未读作者Proof。
2. 本轮随后实际读完整作者 Proof：`/workspace/scratch/038d9dcc4cac/negative_hardness_work/current_hardness_sources/near_perfect_normalized_robust_gap_author_proof.md`，实际SHA256 `23513dbfd03ec6595b61880045b95a87cc465957f1b2bfc63d5fbd1748f29007`。
3. 再实际全文读root最终canonical：`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11-negative/research/current/unrelated_machines/normalized_gated_menu_welfare_and_robust_source_boundary.md`，从标题至§6全部段落、表格与公式(1)–(13)，实际SHA256 `3c0919735dbc90793fe99336e24f3b15d37b09bb8e7e9e138c71437e08acff01`，与root指定版本相同。

本人是前期general welfare-LP/gated v2的共同作者，已知其作者Proof；因此本记录只记**作者Proof读后与最终正文交叉核查**，不记为该canonical全文的独立review或blind全研究。近完美源的Exact-first独立重构身份仅按原冻结记录保留。本次不冒记独立代码审查；代码是本人所写，root另交独立reviewer。

## 2. 近完美作者 Proof 的实际读后结果

全文与本人先冻结重构吻合，无需改变Exact-first结论：

* 任意allocation的attaining-state积分点给W*≤L；norm1与x≤z给L≤n；x0说明福利LP始终可行。
* 一般福利共同前提用state后conditional x/z claims，z0分支清楚；资源tail概率和≤1只用于初始舍入；标准已知DNS机制没有被作者认领原创。
* YES的整数unit组数k≥(1−η)n直接给L≥阈值，不需取得该witness。
* NO_≥用h=#{r≥δ}<γn，NO_>用h=#{r>δ}<γn；各自低端分别<δ和≤δ，但均有W≤h+(n−h)δ<[γ+(1−γ)δ]n。strict来自h<γn与δ<1，对非整γn仍成立。
* 若LP越界，则L>0且W>(5/8)L≥(5/8)(1−η)n≥右侧阈值。等号(E)安全；decider只解LP，不必运行舍入finder。
* 三重等号η1/40、δ=γ3/8左右均39/64。作者Proof没有错加strict slack或整除前提。
* 参数输入只影响有理目标阈值比较，没有按参数倒数数值枚举；随机归约后果留待其真实成功合同，没有假造源hardness。

没有发现作者Proof相对Exact的新standing fatal。其一般福利细节是明确共同前提与另稿重构，不把本页短概述误记成重新独立完整验证了福利算法。

## 3. 最终canonical逐节交叉核查

### §1 对象与全部原jobs

核全部norm1 indexed states、distinct资源、zero/unused/重复state及缺项不生成job的合同。四类机器互异，pin/connector/selector/incidence端点完整。计数1+n+S+m、1+2n+I、1+3n+S+2I正确；未选states和零incidence仍执行。W*、β*只作有限最优值，不冒充oracle。

### §2 值恒等及两个方向

见证上界中根负载2−|H|/n、gate恰1、选根2−quality、未选private1、resource≤1同时成立。β0基线全部connectors在根、selector在gate，不删除任何job。任意C<2调度解码H由真实connector位置决定，selector受unit冲突离开gate；每resource全局unit独占给不交原bundles。C≥2另用β*≥0，未越界调用独占。故OPT=2−β*、根pin给OPT≥1正确；没有保原flat最优值的误称。

### §3 福利LP、标准舍入及精确去随机化

z与x行、原allocation嵌入、S+I_+变量数、L≤n全部吻合。初始tail事件概率为Σ_s x，不是Σ_s z或p*x。每资源只给最大系数提议者，实际质量由原state读取。

公式(7)使用原正权重levels，先逐state、后逐coin；z0不除，θ0/1只走可能支。canonical明确写出“条件化后ΣQ可能>1，只有初始(6)用Σq≤1”，正确堵住一个潜在误用。后续只需精确条件期望，不能继续套初始容量概率界。概率计算及分母位长按原有理输入因子的多项式次幂界定，没有重复平方或按数值网格循环。

### §4 whole-class 13/8

真实r排序有理扫描；若h/n>b且r_(h)>b则违反候选最大性，故W≤n(2b−b²)。最优balanced见证给W*≥n(β*)²。福利LP与完整job桥联合得到C≤1+sqrt(1−5β²/8)。平方差(209β²−468β+260)/64在[0,1]递减，最小1/64；D≥5/8，两边非负，13/8相对真实OPT成立。sqrt仅分析，算法不输入OPT。domain含pin所以不需伪造OPT0分支，也未缩小一般UM目标。

### §5 高低互补与近完美源

公式(11)正确保留high≥δ对应low<δ，high>δ对应low≤δ；γ_hi与旧低组比例确需互补。这里撤回旧§F解释而保留原低组定理/旧冻结字节的界限准确。

完整YES的support-LP判别需norm1使unit attaining support全进本bundle，正文准确。L=n后的count严格大于f(δ)n同时适用于两种高端，δ0/≥NO退化已注明。近完美YES另用福利LP与目标阈值，未误以support-LP可行作判据。

近完美NO正文用了较弱的非严格上界W≤[γ+(1−γ)δ]n，虽然作者Proof可得strict；这不损害E等号，因为舍入W>5L/8仍严格反超。NO_>低组可等δ，正文仍正确。η、δ、γ全部作为binary参数，3/8、1/40角点与非整count覆盖正确。未假设存在某hard source reduction。

### §6 边界与状态

完整gated类13/8限制b>(13/8)a的绝对YES/NO归约；原flat两unit组共享一resource负控给OPT2对gateOPT3/2，确实阻止normalform误称。共享内部机、多层、不归一、implicit和非all-allocationNO没有被本定理排除。主UM正反面仍OPEN、未把固定gap当所有ε反证。

Evidence指向实际审查记录而未把作者交叉核查当独立代码审；本记录不认证其链接中的其它尚未亲读材料。外审、新颖性与通用精确LP生产实现仍未升级。

## 4. 当前结果及未作事项

**本轮读后未发现standing fatal或需修改的数学陈述。** 无repo修改请求；无需重冻canonical正文。最终canonical版本与指定SHA完全匹配。

这不是一次新的独立canonical全文review，不回填为独立code审查；没有新增运行，也没有扩大原有限实验域。root仍需按实际独立reviewer记录管理全文/代码状态。若canonical后续改变，当前读后结论只覆盖上述hash，不自动延伸。

---
id: customer-attraction/weak-iid-star-author-representative-history-audit-and-rational-bracket
kind: program
type_tag: 程序
title: 弱iid星族的作者代表历史审计与有理夹逼
status: full-original-code-and-report-retained-no-new-execution
truth_status: known-analytic-counterexample-with-finite-author-audit-and-reported-exact-bracket
review_level: current-informed-full-source-and-mathematical-domain-review
scope: 固定30名单位玩家、100花瓣、40920代表历史及5行动；有理端点与窄根夹逼；不枚举102进制全树
summary: 保存作者4711B程序和2303B报告，证明逐偏离重数归约的适用范围，分开204600含self比较、原精确Fraction夹逼及float显示；不转移为新运行或一般half反例。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_iid/verify_weak_iid_star.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_iid/weak_iid_star_exact.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_iid/verify_weak_iid_star.py
related_source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_iid/weak_iid_star_counterexample.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_security/verify_star_family.py
---

# 弱iid星族的作者代表历史审计与有理夹逼

4711B原程序全部六个具名函数（含main）及内部lambda，2303B原报告全部23个根字段、30项路径、30项收益、全部大分数及四个浮点数均全文读过。size、SHA256和Git blob同冻结inventory逐项相等，两个来源提交同字节。原件及正常show回执见[证据目录](../../tools/evidence/weak-iid-author-native-audit-primary/README.md)。本轮0原程序导入、0原入口、0新数学checker；不把原报告的`exact_assertions_passed`当当前进程执行证明。

这补齐的是[既有星族定理](../定理/星核花瓣目录的匹配静态安全值--定理.md)中7121B作者稿对应的原代码及报告。它与[5445B内部复核程序](星核花瓣族的Fraction审计域与原报告--程序.md)是两个自含实现：前者在固定n30压缩偏离类，后者完整枚举四个小树并检查245组静态参数。两者同族、同n30弱iid端点，不增加一份新反族或外审。

## 固定输入、合法收益与完整策略

取30名单位权玩家、160名互异单位客户。两客户组成核H，58名客户组成互不交的B块，另有100名花瓣私客c_j。共同非空集合目录为A=H、B、C_j=H∪{c_j}，共102个互异主题。玩家顺序观察全部有序历史各选一次，允许重复；客户在最终覆盖者间均分。[完整历史模型](../定义/共同目录完整历史模型--定义.md)中的离轨前缀、并列最优及真实续局全部保留。

代码常量`N=30,K=100,PRIVATE_B=58`，标签A0、B1、C₁2、C₂3、C₃4、…、C₁₀₀101。设合法终局B出现b次、非B共ℓ次、当前所选花瓣C_j出现q_j次，`payoff`返回

$$u_B=58/b,\qquad u_A=2/\ell,\qquad u_{C_j}=2/\ell+1/q_j.$$

只在own实际出现在terminal时读取这些式子，分母才正。程序辅助函数不校验任意畸形标签、超长前缀或own不在终局的外部调用，不将它宣称为通用博弈输入验证器。

`action`在根选A；其它非末位节点选B；末位全B前缀选C₁，恰一项非B且为C₁时选C₂，恰一项非B且为其它C时选C₁，其余选B。这正是最小不同花瓣控制器，要求至少两朵花；本代码只审固定K100。`continuation`从传入的真实前缀反复调用同一action补满30项。比较替代行动a时调用`continuation(h+[a])`，没有冻结原轨后继。

实际根叶是AB²⁹，每人2、W60。最优覆盖是B加29朵不同C，故OPT=58+2+29=89；不选B最多2+30，选B后至多剩29朵不同C。这既不是把160客户总量当OPT，也不是声明所有SPE的福利都60。真实half余量2W−OPT=31>0。

## 40920代表历史和204600次比较的真实域

`audit_representatives`遍历depth d=0,…,29、非B总次数ℓ=0,…,d、A次数a=0,…,ℓ、C₁旧次数q=0,…,ℓ−a，取唯一代表

$$h=B^{d-\ell}A^aC_1^qC_2^{\ell-a-q}.$$

每个h计算指定行动真实完成的收益，再与A/B/C₁/C₂/C₃五个合法替代标签比较。所有计算是Fraction，逐项assert差≥0，并累计最小差。固定深度的代表数为

$$\sum_{\ell=0}^d\sum_{a=0}^{\ell}(\ell-a+1)=\binom{d+3}{3}.$$

因此总数Σ_(d=0)^29 binom(d+3,3)=binom(33,4)=40920，五项比较共204600，正合报告。每份指定行动都在这五标签中，所以含40920项self比较，非self为163680。最小差字符串“0”包含必然的self零差；真实非self平局也存在，不能从此数声称全体偏离严格。

这不是102进制全树的节点枚举，也不假定一般SPE只能依赖计数。压缩的正确理由是**逐个所查偏离的收益保留**，而不是整张策略对所有花瓣置换等变。固定C₁/C₂选择确实破坏任意花瓣重命名的整树等变性。

任意合法历史先按下列四类处理。对于ℓ≥2的非末位节点，未来末位必选B，无论当前再选A、B还是C；当前指定B的收益仅依ℓ，所查C_j的收益仅依它自己的旧重数q_j。当前本身是末位时没有后继，直接按相同ℓ及所查q_j计算即时收益，也适用这一重数归约。为这一个偏离，可以把C_j映到代表C₁，将其余C总质量合并为C₂，A次数原样保留；遍历q=0,…,ℓ−a涵盖所有可能q_j，保留基准和该偏离收益。其它C之间原本有多少种不同重数不影响这一项比较；五个标签并不声称在每个任意原历史都列出了全部花瓣重数。

ℓ0/1要另查，因为末位可能改选花瓣：全B、唯一A、唯一C的真实完成只区别“复制旧瓣/另选不同瓣”。代码含唯一C₁、唯一C₂以及替代C₁/C₂/C₃，覆盖这种相同/不同关系。选出的另一瓣究竟是哪一标签虽可不同，当前人的核负载和私有负载相同。过去位置排列不影响这些完成收益。K100且历史长度≤29，存在未出现花瓣；代表中的fresh C₃合法。此归约没有把当前偏离后的末位选择沿用原分支。

完整可信性还可不依赖运行而逐类直接证明。非末位情形包括根，根在第一行允许选A：

| 过去非B类 | 选B后真实收益 | 改A或C后真实收益 |
|---|---:|---|
| ℓ0 | 末位补C，B29次，得2 | A使末位B，得2；C使末位补另一C，也得2 |
| ℓ1且唯一A | 末位B，B29次，得2 | A得1，任意C得2 |
| ℓ1且唯一C_j | 末位补另一C，B28次，得58/28>2 | A得1，同C_j得3/2，另一C得2 |
| ℓ≥2 | 末位B，B共30−ℓ次，得58/(30−ℓ)>2 | A得2/(ℓ+1)，C_j得2/(ℓ+1)+1/(q_j+1)≤5/3 |

末位ℓ0时A2、B58/30、任意C3，指定C₁最佳；ℓ1唯一A时B和C均2、A1，指定B最佳；ℓ1唯一C时B和另一C均2、复制旧C为3/2、A1，指定不同C最佳；ℓ≥2时B>2，其它至多5/3。每个合法终局分母均正。由全部有序历史的一步偏离原理，这份完整纯策略是SPE。报告204600项与此解析覆盖相容，完整量词由上述分类承担，不靠原status扩展。

## 真正势最大iid分布、有限端点及夹逼的数学对象

这不是静态minimax值v。令S_x为覆盖客户x的标签集，q(S_x)=Σ_(T∋x)q_T；n个iid主题期望覆盖

$$Z_{30}(q)=\sum_x[1-(1-q(S_x))^{30}].$$

指定q*是谐和凹势F(q)=Σ_x E H_Bin(30,q(S_x))的全局最大者。其导数使用

$$g(t)=\frac1{30}\sum_{j=0}^{29}(1-t)^j,$$

代码的`g`直接求这30项，t0/1也无除零。把A正质量移给任一C使私客势严格增加，故q*_A0；B及各C私客使该面严格凹、花瓣对称迫使q_B=1−s、q_C=s/100。纯查询收益是

$$B(s)=58g(1-s),\quad C(s)=g(s/100)+2g(s),\quad A(s)=2g(s)<C(s).$$

B严格增、C严格减，两端异号，唯一内根s*满足B(s*)=C(s*)=λ；凹KKT给真正q*。单位客户预算及iid玩家对称给Z₃₀(q*)=30λ，故弱支付桥要求W≥(59/2)λ。这些优化事实在[匹配静态安全值定理](../定理/星核花瓣目录的匹配静态安全值--定理.md)完整证明，原程序没有另实现通用势优化器。

main先取s₀1/20，精确算B₀、C₀。原代码的严格断言链为

$$C_0>24457/12000>116/57>B_0>120/59,$$

其中B₀=(116/57)(1−20⁻³⁰)，g(1/2000)≥3971/4000，2g(1/20)>392/375，24457/12000−116/57=683/228000。依据分别为Bernoulli逐项界、5·19¹⁰<3·20¹⁰以及20³⁰>1711。于是s*>s₀、λ>120/59，严格否定W60≥(59/2)λ；不使用求根显示。更有正下界(59/2)λ−60>2/57−3422/(57·20³⁰)>0。与原5445B复核程序是同一有限端点，不增加独立反例。

此作者代码另选两个精确有理数

$$L=50342/10^6=25171/500000,\quad R=50343/10^6,$$

令D(s)=B(s)−C(s)，以Fraction断言D(L)<0<D(R)，不是浮点二分。因D严格增，这两个符号比较一旦成立给L<s*<R；B递增进一步给B(L)<λ<B(R)，弱失败量被(59/2)B(L)−60与(59/2)B(R)−60严格夹住。原报告保存L/R及B(L)/B(R)的完整大整数分数，但没有保存D(L)/D(R)字面值、逐条断言日志或历史解释器事件。本页将其身份保持为原有限精确断言及原报告，不冒称本轮已重新计算这两个符号或执行过全部代表比较。若需独立重核，足以用上述有限30项有理多项式核两端，不需要导入任何LP、SPE枚举器或数值求根器。

报告的`lambda_bracket_decimal`为2.035820614719545、2.0358227584626167，`weak_gap_bracket_decimal`为0.056708134226567175、0.056771374647197184。四者都先以Fraction算精确端点，再用Python float转换；二进制舍入后的显示值本身未有向取整，严格区间应引用原Fraction端点，不能把这四个float自动用作严格上下界。源码虽在docstring说“Decimal/float is display only”，实际无Decimal导入或Decimal运算；这不同于5445B程序的70位Decimal/240步显示，不能互换执行域、精度或报告身份。

## 原报告所有字段与运行边界

23根字段可按内容完整对应如下；长分数原字节见[2303B原JSON](../../tools/evidence/weak-iid-author-native-audit-primary/source-root/research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/new_iid/weak_iid_star_exact.json)，不截断成浮点证据。

| 原字段 | 准确内容与范围 |
|---|---|
| status | `author_exact_audit_not_independent_review`，作者审计身份 |
| players/petals/topics/unit_customers | 30/100/102/160，固定实例 |
| path/utilities | A后29项B；30个字符串“2”，原列表全部保留 |
| W/OPT | 60/89，代码分别字面保存并核实际收益、OPT算式 |
| history_class_deviation_checks/minimum_incentive | 204600/字符串“0”，压缩且含self |
| s0/B_s0/C_s0 | 1/20及两个完整精确分数 |
| simple_C_lower/simple_C_lower_minus_116_57/weak_lambda_threshold | 24457/12000、683/228000、120/59 |
| s_star_bracket/lambda_bracket | 两有理s端点和两个精确B端点 |
| lambda_bracket_decimal/weak_gap_bracket_decimal | 上述四项float显示，无有向舍入 |
| exact_assertions_passed | 成功走到构造result时字面True；非历史逐断言事件 |
| Q_CAG_HALF | 原文`OPEN; this example has 2W=120>OPT=89`，不是当前全人数状态认证 |

程序只导入标准库Fraction、Path、json、sys；没有外部数据输入、solver、规范审计器、候选packet或随机探索。所有计算在main保护下，读源不触发执行。没有通用命令行参数解析：恰有一个额外argv时，以`Path(argv[1]).open("x")`独占新建输出文件，已存在会报错；其它参数个数（包括多于一个额外argv）都只向stdout打印，不据此修改N/K或拒绝参数。json.dumps用ensure_ascii=False、indent2并加一换行；文件分支不打印payload。输出编码走默认文本编码。没有硬编码覆盖同目录冻结JSON的行为。

IC/有理端点/夹逼均由assert承载；正常解释器启用assert时，失败会在构造成功result之前抛出。`python -O`会移除这些assert，但计数循环仍运行，最终字面True不能证明优化模式下检查过任何不等式。冻结报告没有argv、优化标志、退出码、解释器版本、stdio或源码SHA绑定；本轮不补造这些历史。原稿所称作者独立编写不等于另一研究员复核，更不等于外审；当前是读过相关证明后的知情源审查。

与旧m20/J100、每m≥41族的[原审计合同](../资源/花瓣弱iid原审计的策略映射与有理阈值合同--资源.md)相比，这里只是同一最小不同瓣控制器的n30有限实例，1540类/4738比较、循环规则小树和本40920类/204600比较不可合并为一次运行。真正安全值为v₃₀=6429/3215，已知这份σ满足W−30v₃₀=6/643>0；不能用iid失败否定真正安全桥。五人half另有证明，恰六人/一般全目录half未由本实例关闭。关系是既有定理的有限实现、同族证据差异和精确端点的显示分层，正式超图留第三阶段。

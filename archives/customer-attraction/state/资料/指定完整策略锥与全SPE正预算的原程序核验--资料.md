---
id: "customer-attraction/selected-cone-and-ordered-budget-auditor-contracts"
kind: "resource"
type_tag: "资料"
title: "指定完整策略锥与全SPE正预算的原程序核验"
status: "full-source-read-exact-scope-and-runtime-boundaries-preserved"
summary: "五固定游戏全有序SPE正GB及三固定形式策略全质量锥证书；输入/政策身份、CLI空输出接续和4914坐标不扩量词。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_selected_security_budgets.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/customer_attraction_selected_security_budgets.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/customer_attraction_selected_security_cones.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/customer_attraction_selected_security_cones.py"
---

# 指定完整策略锥与全SPE正预算的原程序核验

主源cb88477459c73d47fafe（selected_security_budgets.py，3890B/72行，SHAfa481f8e…）及c0b20181754a4455d3cb（selected_security_cones.py，3344B/65行，SHA49cb05ae…）全部全文实读；两冻结refs同字节。[源原件与定位](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/source-manifest.json)保持不改。所有真实JSON/政策/Q/字段已读，数值向量全部原字节保全、全结构解析并定义级Fraction核验；319884B锥包的每个数字不冒称人工逐字读，也不额外完成这些相关源。

## 五个固定游戏：有序完整SPE菜单的精确递归

有限共同目录，正人数单位提供者，单位客户整数重数，全部有序历史。utility(z,i)直接按覆盖者均分，query(a,B)用1+竞争负载，coverage(z)取覆盖客户重数。可重复主题、离轨历史及各自平局全部保留。程序不导入生成器/求解器，而以ordered tuple h为lru_cache键，完全不做计数状态压缩。

叶菜单M(z)={z}。给定h，各行动孩子菜单已归纳得到，设

$$L(h)=\max_b\min_{z\in M(hb)}u_{|h|+1}(z),\qquad M(h)=\bigcup_b\{z\in M(hb):u_{|h|+1}(z)\ge L(h)\}.$$

必要性来自任意离轨孩子的收益至少其菜单最小值；充分性是为每个未选行动独立选择达到最小值的合法孩子策略。孩子历史子树彼此不交，所以可拼成一份完整纯SPE。不同有序路径即使计数相同仍分别保留，菜单不是全部完整策略的计数，也不是只沿在轨最优。

固定根可实现路径z和位置i，自己选原z_i的孩子由该路径固定；改选b≠z_i可在M(z_<i,b)中任取令当前人收益≤u_i(z)的完整续局。设Cbranch(z,i)=Σ_a p_a f_(z删除i)(a)，则每个备选b分别最大化Cbranch，再乘p_b加总。不同实际位置的首次偏离子树按首次离轨位置分离，可同时独立拼接，故这给该z上最大Σ_iC_i，遍历全部z即给所有完整SPE的最大ΣC−W。

程序还从输入重建一棵完整达到策略，检查全部有序历史真实偏离，并核其ΣC−W确等上述最大值。静态p/Q通过所有m^(n−1)合法背景的floor=min_B E_p f与cap=max_a E_Q f相等来确认证据；真实输入Q背景/动作合法性另在本批全字段检查中明确核过，不把原程序未全面做的schema检查补称其源码已有。

## 全部五输入与结果：负violation恰是正GB

BASE固定repo/evidence/certificates/customer_attraction/selected_security_budgets，main无argparse，依次只读original36、individual34、individual360、root_tax_failure、global_decorrelation_failure五JSON并打印报告，不写文件。verify(path)是函数入口。精确逐件字节/SHA见[输入清单](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/dependency-manifest.json)。五游戏/全部动作表/全部p与Q和历史作者字段均实际读完。

| 固定游戏 | n/m/客户 | 完整有序路径数 | 规定策略含自身IC | 最小GB=W−ΣC | 静态v |
| --- | --- | ---: | ---: | ---: | ---: |
| original36 | 3/6/36 | 48 | 258 | 17/6 | 10 |
| individual34 | 3/6/34 | 40 | 258 | 60/41 | 2411/246 |
| individual360 | 3/6/360 | 23 | 258 | 55088965/3710088 | 93177/908 |
| root_tax_failure | 4/6/61 | 102 | 1554 | 3/2 | 9 |
| global_decorrelation_failure | 4/6/89 | 6 | 1554 | 70429743611/10570351740 | 508643/26546 |

五项严格正。源字段GB_violation_sumC_minus_W记录最大ΣC−W，恰为本表负值；failure等文件名不是GB失败证明。其量词为**每个固定客户游戏、一个指定精确安全最优p、所有完整纯SPE**。没有量化该游戏其他安全最优p，更不量化任意客户游戏/六人。现行符号纠错正文和gb-sign-correction已实际比较，维持正确方向；旧原件/旧处置均不覆盖。

规范34客户个体输入与预算达界输入game和security完全相同，43动作中有12个离轨差别；原政策与另一个达界政策各自保全，不能只凭同根叶/同GB替换。360固定游戏的预算达到策略根(0,4,3)，其全SPE最小GB=55088965/3710088；早期特定(0,3,4)策略的GB=65339377/3710088是另一个更大正值，不是数值矛盾。61客户预算策略根(0,0,0,4)，锥包则(0,0,0,5)；89客户预算根(5,0,0,2)，锥包根(2,5,0,0)。相关游戏、形式策略与顺序身份不能合并。

程序只依实际使用的game、security primary/dual、possible_ordered_SPE_paths、violation及strategy动作核上述项目；输入额外顶层players/topics、root_SPE_count_menus、W/outcome/utilities/sum_C和部分security value标签不都是单独assert目标。原始元数据全部保留，不能把PASS说成每个作者字段已被原码逐项认证。该审计不是一般坏JSON验证器：有些合法动作/背景类型约束在原码只假定，实际冻结输入已另查精确int/范围，不扩通用schema能力。

## 三棵固定形式策略：任意非负客户质量锥

另一程序只读selected_security_cones.json（源7a48fb9d35ad4f79eb56，319884B，SHA48eba055b3f439e21d95d7f96b7f179f2cd907337ca42d57ade7b0f931327a70），没有优化器或生成器。对每case固定n,m与全部有序历史策略σ，非空客户兴趣T遍历1至2^m−1。定义真实完成终局z_h、z_ha和

$$\Gamma_{h,a;T}=\frac{\mathbf{1}_{\sigma(h)\in T}}{\#_Tz_h}-\frac{\mathbf{1}_{a\in T}}{\#_Tz_{ha}},\qquad \mathcal K_\sigma=\{w\ge0:\Gamma w\ge0\}.$$

零分子为零；非零时分母正。每条Γ真实重算后按完全相等Fraction向量去重；不冻结续局、不用计数策略替代原σ。policy全历史/重复键和动作范围均核；本旧程序的范围比较不是后来21锥脚本的精确int断言，实际输入的int身份已另检查，二者版本不能混写。

逐证书目标d_i,T是实际玩家i的最终份额，aggregate目标是覆盖c_T/n；索引0从第一人开始。每个合法静态背景元组B长n−1、可重复，f_B(a)_T=1_(a∈T)/(1+#_TB)。证书提供一个全查询共用概率Q和按查询a分的非负乘子λ_a，程序要求λ行是重建的真实Γ行，并核所有类型余项

$$r_a=d-\mathbb E_Q f_B(a)-\Gamma^{\mathsf T}\lambda_a\ge0.$$

对任意w∈Kσ内积，d·w≥E_Q f_B(a)·w对全部查询成立。再对任意混合p平均，min_B E_p f_B(a)≤E_Q E_p f≤d·w，取max_p得逐人u_i≥v_n或聚合W≥n v_n。固定Q/λ适用于整个锥，不是单点浮点实验；有理/整数质量可清分母展开单位客户，空兴趣客户不贡献可补回。这里不是有权提供者或顺序混合策略。

| 固定σ/name | n/m | 根叶 | 目标证书 | 历史/Γ比较构造 | λ列表项 |
| --- | --- | --- | --- | --- | ---: |
| aggregate_theta_failure | 3/6 | 0,3,4 | 第二人、第三人、aggregate | 43/258 | 80 |
| root_tax_failure | 4/6 | 0,0,0,5 | 每位及aggregate | 259/1554 | 33 |
| global_decorrelation_failure | 4/6 | 2,5,0,0 | 每位及aggregate | 259/1554 | 38 |

共3棵树、561历史、3366含自身Γ构造，复用于13证书；每证书6×63=378坐标，合4914。报告重复列出各证书的树规模不能再当13棵新树；nonzero_Gamma_multipliers源码按列表条目计数151，不仅凭名字断言每项严格正或去重。minimum_residual在本旧程序从全部实际余项取min，而非新21锥版本的零初值；实际13项均0。

完整Q去向如下。原三人第二人Q=(0,4)、第三人Q=(0,3)均为纯背景；aggregate在01、02、03、04、05、34、35上的概率依次1982/6471、1442/6471、1/3、565/6471、5/719、55/2157、115/6471。四人root-tax前三位Q=(0,0,5)，末位Q=(0,0,0)，aggregate为后两背景按3/4、1/4混合。global-decorrelation四位分别Q=(0,0,5)、(0,0,2)、(0,2,5)、(0,2,5)，aggregate在(0,0,2)取1/4、(0,2,5)取3/4。全部Q/151λ真实行与系数保原件和[全字段结构](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/input-structure-and-readiness.json)。原三人第一位没有对应全锥逐人证书，恰与34客户沿同形式策略的逐人反例相容。

这些正锥结论量化任意**使该固定σ为SPE**的非负客户质量和全部查询混合，并不量化任意σ。五固定游戏全SPE正GB与三固定σ全客户锥是交叉的不同量词；不能把其中一个当另一个的证明，更不能并作任意六人half。

## CLI身份、异常与本次精确绑定

selected-cones以第一个sys.argv位置参数为JSON，否则用repo默认路径，直接__main__打印完整报告；没有--output解析或自动保存。字节/环境及真实输入先齐全后，本批budget原CLI运行一次exit0/1.119秒，完整报告与旧1825B JSON全部相同。

cone首条命令直接执行同文件为__main__、无位置参数，exit0/0.568秒，但保存stdout/stderr均空；原空捕获保留，**不称额外PASS**。源码guard内是print(json.dumps(verify(path)))，所以按入口语义应进入verify，既不是import-only，也不是只加载定义；首轮无函数trace，无法单独确认空输出原因或给它补造报告。仅为此真实异常做一次同__main__、显式同一输入路径、PIPE捕获接续，exit0/0.501秒得到6686B/4914坐标，与旧报告全部字段相同。

准确统计为2次cone CLI调用，按静态入口应有2次verify调用，但只有1份报告可核的主体完成；首轮主体执行属于源码入口推断，不独立算数学证据，也不加倍样本。第二条是显式参数的相同主入口重跑，不是新算法/独立实现。两条原始命令、输入/代码SHA、首空记录及接续报告见[运行身份审查](../../../../tools/evidence/independent-security-and-waterfill-audit-primary/run-status-assessment.json)。全部用-I/-B普通未优化解释器，assert有效；无Git、网络、账号、公屏或凭据操作。

旧6686B/1825B报告没有当时审计代码SHA绑定，本次给当前主源补真实绑定；不反向改写其历史身份，不覆盖旧页“当时clone无活动入口”的准确当时记录。已存在完整冻结源可读是现在事实，与旧缺入口历史并存。此批不执行发现生成器，不额外done相关12源，不作阶段三导图或六人目标完成声明。

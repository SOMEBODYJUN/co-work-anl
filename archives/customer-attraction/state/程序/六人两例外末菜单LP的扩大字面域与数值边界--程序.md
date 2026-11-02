---
id: customer-attraction/six-provider-two-exception-terminal-menu-LP-expanded-literal-domain
kind: program
type_tag: 程序
title: 六人两例外末菜单LP的扩大字面域与数值边界
status: complete-code-contract-and-related-scope-review; no-new-LP-run
truth_status: floating-template-diagnostic-only; omitted-geometric-constraints-preserved; no-r2-impossibility
review_level: 1536B主码全文及3049B已完成scope原稿全文；4032解析计数/行来源与后续平方阈值比较
scope: 固定m6/r_exc2、五非负乘子、扩大4032客户型域；不构造完整SPE或认证真实两例外结构不可证明
summary: 原代码从Fraction行转HiGHS可行性问题，只stdout无报告。字面域缺非例外组至多2覆盖及A内必两覆盖约束，故阴性只限扩大域同一权模板；scope另记的−1/19和−1/37不属于此代码保存输出，错误d/6已撤回。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ad571a29e6fa477aad8b112b20cb5b59/r2_local_lp.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-ad571a29e6fa477aad8b112b20cb5b59/r2_local_lp_scope.md
---

1536B主程序来源ID630738ed721ab4027b6a完整实读；必要比较原件为已完成的3049B scope（ID32b28134ff211503aec5），本次只作related阅读保存，不重复认领或done。主程序没有配套结果JSON，本批也没有执行LP。scope的浮点infeasible及临时脚本数值按源述身份保留，不冒本次运行或精确Farkas证书。

## 行对象和完整五变量问题

单位客户、共同标签目录、完整有序历史纯SPE，固定实际末两主题A、B。总m6，选择早期四人中的两个角色为E组，其余两人为N组；目标结构是N组每个完整主题都包含A，E组允许例外。对客户a=1_A、b=1_B，前四真实负载p、E组覆盖次数e，比较六元组与其真实末回复的会员次数d、ℓ及同索引交积h。记c=p+a+b，α=a/c、β=b/c，零分子项为0；w=1_{c>0}、o=1_{d>0}。

代码按原末菜单行定义

\[
S=6\alpha-d/(p+1)+h/[(p+1)(p+2)],
\quad Z=6\beta-\ell/(p+a+1),
\quad V=(d\ell-6h)/[(p+1)(p+2)].
\]

它们是同一真实倒二节点对六主题偏离、actual末位对真实回复、各查询末节点相互比较的总行客户贡献；非负性是在客户加总后，而非每客户逐点。程序只允许固定关系6tS+tV，使h的系数6−6恰消去。

另外三系数为

\[
H_E=e/c-2a/6,\quad H_N=(p-e)/c-2a/6,
\quad K=H_E+[2\beta-e/(p+a+1)]/5.
\]

H_E/H_N来自各选中早期角色真实改A后的|A|/6保底；K还加入actual末位改两个E角色主题的保底，以1/5配比组合。源[少量遗漏定理](../定理/倒二主题少量早期遗漏平方阈值--定理.md)给这些真实原节点行的准确作用；不冻结早期偏离后原尾。

目标是找同一组t,q,μ,η_E,η_N≥0，使所有枚举类型都有

\[
2w-o-t(6S+V)-qZ-\mu K-\eta_EH_E-\eta_NH_N\ge0.
\tag{1}
\]

代码用Fraction生成全部系数，再转float，调用SciPy/HiGHS的linprog：五变量、全零目标、A_ub乘子≤2w−o、每变量非负，没有等式或最大margin变量。成功会打印x，否则x:null，并始终打印states/status/message；不写结果文件、没有有理恢复/乘子或不可行证书。

## 4032域如何得到，以及缺了什么

字面枚举a,b∈{0,1}、p=0,…,4、e=0,…,2、d,ℓ,h=0,…,6，仅筛

\[
e\le p,\qquad \max(0,d+\ell-6)\le h\le\min(d,\ell).
\tag{2}
\]

六对二元比较/回复的四格计数共有binom(9,3)=84种(d,ℓ,h)；合法(p,e)按p为1、2、3、3、3种，总12。因此字面域4×12×84=4032，和原scope一致。这是完整给定笛卡尔放松，不是4032个真实游戏或SPE。

本次逐码比较特别确认，(2)不是上述真实分组结构的完整客户域。N组只有两人，所以任何客户都应满足p−e≤2；若a=1，N组两个主题包含A，还必须p−e=2。代码既没有这两条，也没有其它早期主题身份。比如a=1,p=e=0进入字面枚举，却不可能是“另两早期主题都包含A”的客户。即使a=0，p−e=3或4也超过N组人数。

若只补这两项几何条件、仍保其它同样粗计数，则a=0有9种(p,e)，a=1有3种；加b两值和84索引类型为(9+3)×2×84=2016型。这是解析域计数，不是本次跑了修正版LP，更没有断言这2016型都可共同实现完整SPE。原4032域的精确正乘子若存在，当然也足以覆盖较小真实域；但其不可行**不排除较小几何域上同一行族存在证书**。

因此scope末段“两例外情形不能由这些行重权直接闭合”的语句应限为：**在写出的扩大4032型域上，没有从所述浮点诊断得到同一非负权证书。** 没有补几何域、没有精确不可行证书时，不能升级成真实r2命题失败、所有这种行族在真实域都失败、或六人目标反例。这一范围收紧是本次阅读发现，不静默修改原scope。

## 被撤回的早期IC归一化及不同数值来源

相关scope明确撤回另一个临时脚本的pay−d/6。对六个比较主题分别用六人最终负载上界，未平均式是6·pay−d/6≥0；除6才是pay−d/36≥0。少这个平均因子会把比较客户预算放大六倍。例如一客户唯一主题、六人全选该题的完整SPE，pay=1/6，六比较索引都同题d=6，错误行为−5/6，正确行恰0。

本1536B码没有那个pay/d行，不能说它仍包含已撤回错误。scope还记录正确系数临时版本的最大最小余项−1/19、分开两个异常角色约−1/37；这些属于**另外的临时优化合同**，未随本主码提供向量或输出。当前代码只做五变量可行性，不能将这两个值当作其目标值或本次新算结果。

## 原入口、实际范围和可接续义务

程序没有main guard/CLI，import或--help会立刻枚举4032行并求LP，只有NumPy/SciPy外部依赖；不读实例/策略/旧JSON，不调用规范SPE solver。它保留Fraction行在rows中，但实际A/b均float；原scope的infeasible没有精确对偶，不能以“Fraction系数”称数值判定已精确认证。

本批原入口、LP、修正域重算、Farkas恢复、SPE搜索均0。只完整读公式与scope并作静态指纹/语法/字段检查；原码和related字节在[证据](../../tools/evidence/four-topic-exhaustive-and-maxima-scope-primary/README.md)。m6/r1有已证平方阈值，m6/r2不在m≥10的同定理范围；本诊断不改变此状态。后续若研究，应先明确真正结构域及合法总行，再求新证书或精确分离，不能用旧4032阴性替代这个前提核对。

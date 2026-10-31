---
id: customer-attraction/private-spectrum-and-real-terminal-menu-original-audit-replay
kind: computation
type_tag: 计算
title: 私有席位与真实末菜单原审计的精确复跑
status: 两原源码全文及四包依赖全文核；原CLI各一次成功；非新独立实现
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-324fbf8f72b041578583b51189f13d1a/seat_spectrum_audit.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-324fbf8f72b041578583b51189f13d1a/terminal_menu_audit.py
---

# 私有席位与真实末菜单原审计的精确复跑

本批两个主源5585/5916B全文，标准包`__init__.py`691B、`model.py`8640B、`exact.py`9943B、`certificate.py`6201B四相关依赖全文实读。两个源码此前local-only查无blob，后来在其实际认领后经正常`work.py clean show ID --out …`取得，逐size/SHA256/Git-blob身份核同冻结版本；这不是换凭据、绕过被拒取源或修改原文件。原报告1466B先前已作为主源处置，本批不重复done它。

## 私有谱脚本：独立重算什么、依赖什么

源码用三名命名客户的八个覆盖子集，枚举非空目录family=1…255；每个目录m1/2/3构造原单位客户游戏。最优覆盖由至多m题子集穷举，不借solver的OPT值。每条`ExactSPESolver.ordered_outcomes()`输出路径上，直接由命名客户集合重算终局负载/各玩家Fraction收益、包含极大主题、全局私有块P_j、固定实际遗漏Q_j及完整谱a_j/k+(|B_j|−a_j)/m。逐位置断言u_i≥第m−i+1大谱值、W≥前m谱和。若存在最优O使O\C⊆⋃P_j，另断言mOPT≤(2m−1)W。

所以它独立于原私有谱计算实现，却**依赖同仓全部SPE路径枚举器**，不是对枚举器的独立第二实现，也不是普遍定理证明。现在代码已实际读到，能够确认`private_missing_corollary_paths`确实只在上述exist-opt私有遗漏条件满足时增一；本次输出中该计数等于全部1599条路径，故此有限样本每条都满足该条件。此前[原JSON/身份账本](../资源/私有谱原有限报告与可信构造身份账本的边界--资源.md)未有源码时不补造过滤语义的做法保持真实历史。

源码另核m1/2/3/6的唯一空主题零客户边界。全大题锐例m1…6时，按每个非终端**计数前缀**核常数全大题策略的全部行动比较；因为此策略后续恒定，这些比较覆盖对应全部有序历史的等价类，不等于显式列出整个有序树。所得状态数1/3/10/35/126/462，比较数1/6/30/140/630/2772；全部锐例W=m、OPT=2m−1。

## 包依赖与全历史语义核对

`model.py`保正重数为不同同偏好单位客户、共同标签目录、空主题/相同覆盖不同标签/零客户，终局每位份额按同一负载均分，优化为有限子集穷举而非位多项式算法。审计的255目录覆盖唯一子集标签，不能由它单独声称测试了全部重复覆盖标签实例；一般重复域由数学证明处理。

`exact.py`缓存每计数状态的**全部**可达终局集合，以

\[
M(p)=\max_a\min_{q\in R(p+e_a)}U_a(q),\quad
R(p)=\bigcup_a\{q\in R(p+e_a):U_a(q)\ge M(p)\}
\]

求解。当前动作选择实现q的孩子，其他孩子分别取偏离者最坏的可信续局，使其充分；必要性来自所有孩子收益至少各自最小值。不同同计数有序历史可分别选择不同实现，不强制一份Markov策略。`ordered_outcomes`转移同时要求target孩子会员和U_a(target)≥M(p)，所以枚举所有可实现路径而非全部完整策略。代码的`certificate`可对子历史分别选择最小偏离收益续局；`certificate.py`的独立定义级树比较器不调用集合solver，但**本次席位脚本未调用该比较器**，不能把读其代码冒作又一次全树验证。全部有限纯策略域，不覆盖混合SPE或一般六人任意目录。

## 末菜单脚本的真实检查范围

5916B源码只用stdlib Fraction。`audit(m)`检查q2三类规定区的计数节点、沿规定策略的终局计数及真实偏离的无条件收益上界；进入补集的分支以现有A人数/C人数/单例大小给界。另核W/OPT/S/γ公式、末位全部主题比较的单例系数成本、所有actual位置安全分母成本。`audit_q(m,q)`另用参数化区域，核2≤q≤m−2的对应公式、逐单例成本、早期查询证书系数与余项代数。

它没有显式展开全部有序历史BI补集，未独立从代码证明一般非重叠粘合，也未检查任意输入或输出SPE证书。全参数结论仍由[真实末菜单解析正文](../障碍/真实末菜单的覆盖成本分离与早期责任转移--障碍.md)的最小补集根粘合、所有偏离界及锥分离证明承担。脚本中“independently parameterized”指同一原程序的另一参数化函数，不是本批第二独立实现或盲审。

## 两次实际执行与原输出比较

在外部证据树保原`research/workspaces/customer-attraction/R-324…/`深度及`customer_attraction/`包，满足席位脚本`parents[4]`导入约定。全部源代码原字节不改，Python3.12.14、断言开启；两原CLI各首次执行一次，均exit0/stderr0，没有旧成功重复或新独立数学实现。

|原入口|实际时间|输出及结论|
|---|---:|---|
|seat_spectrum_audit.py|0.287276725秒|1466B；765目录人数对、1599有序路径、3660位置比较、1599私有条件路径；全部零空和六锐例字段通过；与冻结原JSON**逐字节一致**|
|terminal_menu_audit.py|9.220882113秒|181B；q2 m4…200共78997规定计数节点；m4…40全部703对(m,q)共139194节点；exact_checks passed|

席位源码SHA251542fe83c90f4189f212fb59b821e97710929d565e71c9e1bd7c50e5e48e2c，报告SHAf357229195f9f1f6909466d93cec113eca9c9f415c9c68084d72891477531cc5。末菜单源码SHA5f69614d4b8bb5b77e7278150d904cc72e045ee7b808257e5745151ae1bb1b29，stdout SHA9805ab15a04cc2cce23de125870ae92df632fc1642c836c66b3e60f03fa084b6。完整命令/cwd/版本/哈希/耗时及原stdout/stderr在[证据目录](../../tools/evidence/root-private-spectrum-and-terminal-audit-replay/README.md)，终端输出数字与原MD报告相同；没有不存在的原JSON供逐字节比较。

复现从证据目录`source-root`运行原入口；席位可加`--output <新路径>`，末菜单直接打印原Python字典。不要覆盖run-001原件。依赖代码、固定输入、运行记录和数学scope一起保存后才可复用其PASS。

## 本次补齐和仍未覆盖的材料

这次把先前IN/IX“缺源码、只认原报告”的两个具体证据缺口补齐，未篡改先前预检记录或增加过去运行次数。原九人残差的20终局/25920路径来自另一组代码/报告，本两脚本并未检查它，不能拿1466B逐字节一致给它背书；其四份材料随后单列来源任务。一般六人half、原共享遗漏总钱包、逐人净机会缺口仍没有由这些有限回放完成。程序处置与数学开放状态分开。

后续JK另完成[九人双实现复核](九人尾端选择障碍的双实现精确复核--计算.md)，并非本页两个私有谱/末菜单脚本执行过九人输入。

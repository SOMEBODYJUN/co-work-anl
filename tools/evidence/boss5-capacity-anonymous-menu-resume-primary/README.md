# 固定流、匿名势与删槽菜单的逐源复核

本批16份冻结源逐份全文读，按source ID保存到`original/ID/原文件名`，逐项size和SHA256与[source-manifest.json](source-manifest.json)核同。没有改冻结代码，没有执行Git或work.py远端写。双冻结提交的同字节内容不当作独立发现或两次实验。

## 四组数学内容的准确去向

1. 五份common_capacity源的完整数学保在[atom独立回撤定理](../../../archives/customer-attraction/state/定理/初始客户边独立回撤与共同价格分散返还--定理.md)、[return账本](../../../archives/customer-attraction/state/引理/真实历史返回动作的精确账本与共同资金缺口--引理.md)和[原程序合同](../../../archives/customer-attraction/state/程序/初始客户边回撤原审计的精确合同与有限覆盖--程序.md)。固定同一合法流的初始边a有质量bₐ、owner和终端K；回撤yₐ缩放其全部后代，把同量留owner，F′=F+owner回撤−终端撤量。全非负价格cut充要，细粗价格需求差精确为Σmin(Dᵢ,Eᵢ)，但λ≡1仍恰要求原half总资金。抽象严格分离不是SPE；真实52客户例的两atom均末位终结且owner不同，未激活严格分散。真实return给v=u+P−N+e、e≥0；e是成本，Jensen只给收益下界，尚未闭合共同资金上界。
2. 6486B成对水库原稿已完整进入[全参数可信缺陷收费障碍](../../../archives/customer-attraction/state/障碍/成对主题水库路径的全参数可信缺陷收费--障碍.md)。它的精确k≥4、m=k+1目录与指定C₁,…,C_k,D路径，在短尾每份真正SPE都有收益≥8的新鲜成对选项；污染数及严格15/2、13/2上界保护强制者，线性多个δ≥6使旧差k−8无法支付。正式页另外保存后续更强好组下界；只排该路径/尺寸/异质修复合同，不排一般反例或所有编译器。
3. C22主稿与原程序/JSON三源分属[匿名势反例](../../../archives/customer-attraction/state/反例/匿名边际势的自由列亏损与凹化保持--反例.md)和新增[原始精确核验程序合同](../../../archives/customer-attraction/state/程序/二十二环匿名势反例的全历史精确核验--程序.md)。原例是三人匿名势、总效用25、均匀自由列和34，差9；它不是CAG。后续[一般基数凹化](../../../archives/customer-attraction/state/定理/有限层匿名边际势的基数凹化--定理.md)保持全部完整SPE和差9，使单调DR仍不足；该后续由另一组独立整理并已全文对读。原程序只核原例10→12的DR失败，不能把凹化结果倒填进去。
4. 七份fresh_menu_attack源保在[全历史精确包络算法](../../../archives/customer-attraction/state/算法/实际位置删槽菜单的全历史精确包络--算法.md)和[攻击/定义核验程序合同](../../../archives/customer-attraction/state/程序/自由删槽全历史攻击与定义级核验--程序.md)。E/F收全部可信终局，R保actual叶并筛当前IC，H优化actual顺序；首次离轨子树不交使局部菜单最大值可同时拼合。此为固定实例p的最大AFC gap精确表示，不给gap≤0。计数固定策略锥的连续浮点LP、完整历史oracle和定义级穷举是不同对象，旧m5/k5/80负面日志不提升为全称证据。

所有原客户目标仍保有限单位客户、有限非空共同目录、重复主题标签/重复行动、空主题、零客户和任意有序历史平局。现有数学模型页的集合目录写法与软件的标签接口历史区分不在本批改写；本批没有利用删去同覆盖标签来缩小当前六人目标。原稿称五人OPEN为旧时态，当前五人half已另证；上述固定修复族的所有cuts、一般CAG-AFC和六人W≥OPT₆/2均未由本批解决。

## 一次新执行与两份成熟证据复用

本批只新执行一次原`verify_anonymous_potential_boundary.py`，普通Python保assert，exit0、stderr空，约3.11秒。它检查507有序历史、11154项含自身比较、10648终局、253背景、66实际自由列和指定零IC跨势分解。新stdout与冻结615B JSON**解析后完全相同但字节不同**，因为原JSON紧凑而程序indent=2打印。精确事件、两个SHA和语义比较见[runs/anonymous-event.json](runs/anonymous-event.json)；[新stdout](runs/anonymous.stdout.json)和原件分别保全。这是原实现复跑，不是新独立实现。

atom原审计与七例菜单核验均已有成熟同SHA的成功重放。本轮读代码、既有事件及实际输出，重新对原报告核字节同，记录在[reused-runs.json](reused-runs.json)，**没有再执行这两个脚本**。atom旧重放覆盖1554IC/两atom/81真实价格及另64抽象价格；菜单旧重放七例完整策略数和SPE数、空零/同覆盖标签边界均对应冻结JSONL。旧数值筛查不重跑，未扩大种子、人数或规模。

对既有菜单程序页只增加一段调用边界：其数值外层`run`无条件`np.max(ic@w)`，k=1时ic为空会报错；精确`best`和原七例验证有效。修改前内容由唯一插入段的精确逆操作恢复留存于[before快照](comparison/delete-slot-program.before.md)，方法与前后SHA见[shared-page-change.json](shared-page-change.json)。没有改原冻结程序。

## 阅读、关系及处置记录

[comparison-manifest.json](comparison-manifest.json)列本批实际全文对读的正式对象与SHA。逐源阅读、比较、独有去向和16项receipt在`cleanup/workspaces/Boss5/resume-20261102/group_c/`；不是以字段齐全代替数学判断。

[relation-review.json](relation-review.json)记录人工区分：固定流输入和有条件回撤后果、return未付接口、匿名势的扩大类反驳、凹化不变性、oracle的精确表示及有限实现检查。没有复制旧图或把链接列表充成第三阶段超图。无外审、新颖性、最小规模或一般方法不可能性认证。

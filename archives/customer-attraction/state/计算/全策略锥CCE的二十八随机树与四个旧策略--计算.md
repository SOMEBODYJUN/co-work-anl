---
id: customer-attraction/full-policy-cce-twenty-eight-random-and-four-named-records
kind: computation
type_tag: 计算
title: 全策略锥CCE的二十八随机树与四个旧策略
status: complete-report-read; all-660-attempts-accounted; no-new-mathematical-run
summary: 四原报告218982B共32条660轮全部字段保全；best为真实重求CCE后的最大浮点值，未命中阈值非全锥上界；两旧命名输入共用同一43动作而warm-start和有限最佳不同。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_n3k4.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_n3k4.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_n4k5.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_n4k5.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_n5k7.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_n5k7.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_named.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-3b6b03db882e4de48cfa5b406f57ef8f/security_global/cone_cce_named.json
---

# 全策略锥CCE的二十八随机树与四个旧策略

四份JSON共218982B全部实读；通过共享message及重复tuple字典编码逐条显示全部32条case和660个attempt的每一字段，再验证[可逆全值视图](../../tools/evidence/full-policy-cce-source-contracts-primary/README.md)逐项解码等于原JSON。字节哈希另与父方本次clean show逐份核对，六份直接源共226470B皆与旧已发表原件相同。可逆视图是阅读排版，不是挑字段摘要或给浮点数补有理值。

[完整程序合同](../程序/完整策略锥与静态粗相关对偶的交替接口--程序.md)给模型、Γ、占用CCE、正确对偶及全兴趣型删除理由。四报告只覆盖n3/4/5，没有六人实验；每条随机case是一棵由特定整数种子构造的完整策略，再固定它在客户质量锥内交替搜索，不是完整SPE集合的穷举。

## 三份随机报告的全部case标量

共同根字段scope准确为“Finite numerical alternating full-policy cone / CCE-dual attack. No universal claim; all ordered histories retained.”，correct_dual为`(1-sum(lambda))*W+sum(lambda_a)*D_a`，seed均20261021。elapsed依次0.6647751331329346、1.1272833347320557、16.906734943389893秒，属于历史报告，不是本次运行时间。cone_LPs分别200、200、160。

下表保全部case的非attempt数值；n,k及H/P是每表明列的共同字段。root_counts是原整数种子上σ实际叶的完整k维计数；seed_actual_W、seed_CCE_value也在原种子上。best_CCE_ratio则是重新赋质量、W归一化为1后各轮重求静态CCE值的最大值，不能拿seed_CCE_value/seed_actual_W去等同该best。

### n=3、k=4

每条H=21个有序决策节点，P=20个静态占用列；每条attempt恰是start0…3、iteration0…4的全部20轮，全部status0和同一HiGHS Optimal消息。

|case|unique_gamma_rows|root_counts|seed_actual_W|seed_CCE_value|best_CCE_ratio|
|---|---:|---|---:|---:|---:|
|0|33|`[0,1,0,2]`|94|79.9075546719682|1.0|
|1|41|`[1,1,1,0]`|107|84.24424668050382|1.0|
|2|39|`[1,0,0,2]`|85|74.91807513055195|1.0|
|3|42|`[1,0,1,1]`|90|72.87231512548644|1.0|
|4|41|`[0,1,1,1]`|92|80.97807302446384|0.9777991090719325|
|5|42|`[1,1,1,0]`|126|101.36546306530903|1.0|
|6|39|`[2,0,0,1]`|124|112.1518539484857|1.0|
|7|39|`[0,0,1,2]`|93|85.48883285302594|1.0|
|8|41|`[1,1,0,1]`|108|93.66229565382848|1.0|
|9|35|`[1,0,2,0]`|60|52.18600228223661|1.0|

### n=4、k=5

每条H=156个有序决策节点，P=70个静态占用列；每条attempt恰是start0…3、iteration0…4的全部20轮，全部status0和同一HiGHS Optimal消息。

|case|unique_gamma_rows|root_counts|seed_actual_W|seed_CCE_value|best_CCE_ratio|
|---|---:|---|---:|---:|---:|
|0|193|`[1,0,0,1,2]`|124|116.2569071469611|1.0|
|1|190|`[0,1,1,2,0]`|168|153.14757482478174|1.000000000000001|
|2|174|`[2,0,0,2,0]`|128|123.79899036255163|1.0000000000000013|
|3|193|`[1,0,0,2,1]`|145|128.34751953769327|1.0|
|4|197|`[0,1,1,1,1]`|177|148.58489464925867|1.0|
|5|195|`[1,1,1,0,1]`|154|138.91172835990173|1.0|
|6|182|`[1,0,2,0,1]`|134|119.63543792746162|1.0|
|7|180|`[0,0,2,0,2]`|146|140.63888231195938|1.0|
|8|180|`[1,0,2,0,1]`|121|113.864886582366|1.0|
|9|199|`[1,0,1,0,2]`|166|148.7030803917872|1.0|

### n=5、k=7

每条H=2801个有序决策节点，P=462个静态占用列；每条attempt恰是start0…3、iteration0…4的全部20轮，全部status0和同一HiGHS Optimal消息。

|case|unique_gamma_rows|root_counts|seed_actual_W|seed_CCE_value|best_CCE_ratio|
|---|---:|---|---:|---:|---:|
|0|1683|`[1,1,0,0,1,0,2]`|194|171.42750627369463|1.0|
|1|1655|`[1,0,0,2,1,0,1]`|285|253.53152706385984|1.0|
|2|1639|`[1,0,1,0,0,1,2]`|228|205.43959382729605|1.0|
|3|1698|`[0,0,2,0,1,1,1]`|264|235.44545794688062|1.0|
|4|1600|`[0,3,0,2,0,0,0]`|245|235.58776872120475|1.0|
|5|1641|`[1,0,1,0,2,0,1]`|296|258.9008491924669|1.0|
|6|1676|`[2,0,1,2,0,0,0]`|276|257.38745806001685|1.0|
|7|1581|`[0,1,2,0,0,1,1]`|292|269.5928142369648|1.0|

随机每attempt含start、iteration、status、message、objective、gamma_min、normalization、dual_slack_min共8字段；没有每轮重新求得的CCE值、weights或lambda。随机best从−∞起，28条实际都更新到有限值，故本表的1不是另一个安全值程序的初始化哨兵。它仍不是“该策略锥的精确最优恰1”：交替有限、浮点误差未排除且没有全局上界证书。n3/k4的case4最佳约0.977799，同样不能认证该锥全局上界小于1。

n4/k5有best略大于1，最大1.0000000000000013，原值照存；均未越过源码候选门槛1+10⁻⁶。四报告没有witness或policy候选字段，不能把缺失值补成全零或从seed推定完整策略。

原参数缺失还有可直接核的实质影响：所给源码每个正兴趣型最多20名客户，因此若n5/k7的case5确由此版本生成，其seed_actual_W=296迫使至少ceil(296/20)=15个正兴趣型。源码默认types=10只允许总质量≤200，不能生成这条记录。故“照报告seed、其余types取默认”不是对该报告的正确复现；只能推出实际types至少15或存在未记录的代码差异，不能据此擅填某个具体types、argv或历史版本。

## 四个旧策略命名报告

根字段只有scope和cases，无seed、elapsed、cone_LPs或历史argv。scope为“Numerical exact-full-policy cone attack on existing obstruction strategies; not new instances.”；随机流20261022及5×5循环是代码事实，不是JSON运行字段。每条恰保存start0…4、iteration0…4全部25项且status0，共100个cone attempts。每项含start、iteration、status、message、dual_lower_bound、CCE_ratio、gamma_min、dual_slack_min共8字段，没有normalization。

|name|n/k|完整有序历史|gamma_rows|seed_W|seed_CCE_value|best_CCE_ratio|达到best的(start,iteration)|
|---|---|---:|---:|---:|---:|---:|---|
|individual_security_failure|3/6|43|185|32.0|30.8060826618144|0.9930552093412386|`[[0,4]]`|
|local_security_increment|3/6|43|185|105.0|101.55148343409614|0.991746047795715|`[[0,4]]`|
|global_decorrelation_failure|4/6|259|371|85.0|79.90226540676869|1.000000000000001|`[[2,0]]`|
|dynamic_iid_local|5/7|2801|1578|58.0|51.486486486486484|0.9976784818208771|`[[2,4]]`|

四个best均等于所存25个CCE_ratio的浮点最大值；固定旧乘子下界常严格更小，例如individual首轮下界0.9871558976507984、重求CCE值0.9916254701289593。不能只看dual_lower_bound替代实际比较值。

### 命名输入及完整动作的绑定

以下四原模型全部客户行实际读过。mask第a位对应topics列表第a标签，重数为不同单位客户。完整动作证书已有正式交付，本轮按冻结原字节复用，核历史键域、动作标签和实际路径，不重跑IC、BI、旧独审或静态优化。

|name|单位客户数|证书键|实际路径|重算seed_W|完整动作域|
|---|---:|---|---|---:|---|
|individual_security_failure|34|`strategy`|`[0,3,4]`|32|全部43有序历史、无重复键、动作合法|
|local_security_increment|113|`strategy`|`[0,3,4]`|105|全部43有序历史、无重复键、动作合法|
|global_decorrelation_failure|89|`strategy`|`[2,5,0,0]`|85|全部259有序历史、无重复键、动作合法|
|dynamic_iid_local|60|`certificate`|`[6,6,0,3,4]`|58|全部2801有序历史、无重复键、动作合法|

- `individual_security_failure`全部非零兴趣型：`{"4":1,"27":4,"29":3,"30":3,"31":2,"32":1,"43":3,"45":3,"46":3,"51":3,"53":3,"54":3,"59":2}`。
- `local_security_increment`全部非零兴趣型：`{"4":3,"13":1,"14":3,"20":2,"23":1,"27":15,"29":8,"30":8,"31":4,"32":3,"34":2,"43":8,"45":13,"46":7,"49":3,"51":7,"53":7,"54":10,"59":8}`。
- `global_decorrelation_failure`全部非零兴趣型：`{"5":16,"10":1,"11":11,"15":8,"22":1,"23":2,"24":2,"26":1,"33":1,"35":5,"40":4,"46":2,"52":1,"53":4,"54":14,"56":2,"61":10,"62":4}`。
- `dynamic_iid_local`全部非零兴趣型：`{"9":1,"10":1,"12":1,"17":1,"18":1,"20":1,"27":3,"29":3,"30":3,"33":1,"34":1,"36":1,"43":3,"45":3,"46":3,"51":3,"53":3,"54":3,"64":24}`。

前两个命名例的全部43个history/action原记录逐项相同；所以n,k固定，其Γ、c、静态占用几何及客户锥LP可行域完全相同。原客户、最初CCE乘子不同，且命名随机流跨case连续，有限交替可得到不同点。0.993055与0.991746不是两份不同完整策略锥的精确最优值，更不能证明同一锥有不同最优值；无需改动旧动作或数据。

前三证书的strategy键和第四certificate键是实际解码区别；两n3/k6静态占用各56列，n4/k6为126列，n5/k7为462列（依binom(n+k−1,k−1)算出，named JSON未另存）。四模型/证书及规范包原件的SHA、完整提交和原路径见[绑定清单](../../tools/evidence/full-policy-cce-source-contracts-primary/source-bindings.json)，这些依赖没有另行认领。

## 全部660轮的残差与缺口

下表取原attempt字段直接最小值；normalization列取最大绝对偏差，named未记录即不假填0。这些是作者浮点求解后输出，不是本轮重算的精确SPE/对偶残差。

|报告|全部attempt|最小gamma_min|最小dual_slack_min|最大normalization绝对偏差|
|---|---:|---:|---:|---:|
|cone_cce_n3k4.json|200|-4.85722573273506e-15|-6.661338147750939e-16|9.769962616701378e-15|
|cone_cce_n4k5.json|200|-1.1362438767648086e-16|-2.6645352591003757e-15|1.3322676295501878e-15|
|cone_cce_n5k7.json|160|-1.0408340855860843e-17|-8.881784197001252e-16|6.661338147750939e-16|
|cone_cce_named.json|100|-1.3121677355787398e-11|-1.6503243216448027e-11|未记录|

named最负gamma与dual slack来自local_security_increment的start1/iteration4，约−1.31×10⁻¹¹和−1.65×10⁻¹¹。HiGHS的Optimal不能把负残差变成精确非负；现无有理化新解、全部质量/乘子或逐行精确核验。程序也没有显式保存新λ的非负精确检查，历史库/求解器版本缺失。

随机三报告有560个cone LP记录、named100个。按这份代码与全成功记录，若报告确由该版本生成，则另有660个紧随的CCE重求及32个种子CCE初始化；这是条件性代码计数，不是JSON所存总调用数或新复现。原件缺完整argv/环境绑定。

本轮只做原字节、全值可逆、字段网格及旧输入历史域/实际路径核对：19个source bindings、32条case、660个attempt均通过。原CLI、原模块import、随机搜索、LP、BI及新数学证书审计均0次。旧障碍页的一次“独立smoke”是隔离调用同一作者实现，不是独立SPE或CCE数学实现；其四轮历史记录继续保留，本次未重跑，且不加进上述660轮主报告。

## 当前状态与阶段三关系

保为有限浮点计算及程序资源，不新建真反例、普遍定理或“该方法不可能”的障碍。未越阈值只说明本32条没有新候选，不给固定锥全局上界、强CCE桥或六人half证明。现有[三人八/十三客户强CCE反例](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)已实际否定全人数桥，与有限阴性没有矛盾；本页不覆盖其正式精确证据。

[逐边关系证据](../../tools/evidence/full-policy-cce-source-contracts-primary/relation-evidence.json)区分：重数锥提供Γ的必要充分合同，占用CCE表示提供静态LP，二者联合实现本程序；四报告有限检查程序；前两命名输入是同动作图的不同客户种子；正式反例反驳目标桥，不反驳忠实保存的实验记录。较弱同人数CCE、跨人数平均CCE、真正静态安全值及六人half的边界在程序页已明确。没有从字段检查到定理真值的推导边，本批不生成或复制旧图。

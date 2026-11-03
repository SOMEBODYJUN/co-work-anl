---
id: "customer-attraction/amount-cap1-family-400-node-certificate-and-review-reading-order"
kind: "program"
type_tag: "程序"
title: "金额cap1锐族的四百节点原证书与审查读序"
status: "complete-source-and-certificate-reading;historical-replay-not-repeated"
truth_status: "all-n-family-already-proved;frozen-n3-table-preserved-with-structural-checks"
review_level: "five-primary-full-reading;no-original-entry-or-new-IC-replay"
summary: "保3332B顶层生成器、36652B全部400动作与n3金额证书、两原审查实际范围；作者全n稿精确复用现锐cap2定理，不重复400/2800算术。"
cleanup_primary_ids: ["44ac5a996de190a8da48", "c98e8355f192f5614a31", "110a1ed1af682948ed17", "a4a99bb614912c545bd9", "877bcf0bef8f85435968"]
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/coupling/audit_amount_cap1_family.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/coupling/audit_amount_cap1_family.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/coupling/amount_cap1_family_n3.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/coupling/amount_cap1_family_n3.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/credible/review_amount_cap1_family.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/credible/review_amount_cap1_family.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/independent/amount_cap1_family_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-5a15745a45ba44adb7d26c0557faacb7/independent/amount_cap1_family_review.md"
---

# 金额cap1锐族的四百节点原证书与审查读序

## 五源及全n数学的精确去向

主源共54013B：作者全n稿6880B、定义级原代码3332B、n3冻结JSON36652B、credible审3622B、independent审3527B。五件全文实读；JSON全部字段和400条动作都读，不只提取summary。作者稿是此前正常show同SHA原件精确复用，另外四件为本批新正常取回，不能称五次新show。当前完整认领回执pushed/synced，和上一terminal-cap批的needs-attention回执分开保存。

作者稿完整数学已在[末层金额预算锐cap2定理](../定理/末层多孩子金额预算的锐两倍列容量--定理.md)自足保留：m=n+1、|X_j|2、|Y_j|2(n−1)，A_j=X_j∪Y_j、T_j=Y_j、D=∪X_j；全部有序历史fresh-A override与永久非fresh子树的逆向构造，根改D时用真实末位T_j被A_j严格支配补关键边；实际W=OPT=2n²，多末位孩子λ=(2n−1)/(n+1)、q1，列比2−3/(n+1)>1且趋2。它否定AMOUNT-CAP1并给全人数统一cap2系数的锐性，不反half、不证更深cut的cap2。本批作者稿按这份精确数学去向作duplicate，原字节和本页新增证书/审查范围都保留；不再造同内容第二个家族定理。

## 原3332B生成器的全部输入与执行顺序

代码SHA256为`c02a932d0905807a04bcd2e3d6fff72fcc0d95f6d2008164fcbd8e919b76c609`。仅标准库Fraction、product、Path、argparse、json，不import规范solver、项目Instance或作者其它模块。它**没有main guard**：顶层parse_args、建全树、核比较、计算列并写JSON，import也会执行。唯一命令行参数`--n`默认3且assert n≥3；m=n+1、k=2n+1。

脚本标签为A_j=0…n−1，D=n，T_j=n+1…2n，与数学稿的一起始块指标应区分。`likes`先放每j两份frozenset(j,n)，再放每j的2(n−1)份frozenset(j,n+1+j)。相同frozenset在列表中代表**不同单位客户**，不能去重成2n个客户。pay(z,i)只对行动z_i覆盖的客户求1/覆盖次数，故每个求和分母至少1。

build(h)先递归构造全部k个真实孩子，再算当前角色在各孩子中的Fraction收益。fresh判据是所有历史标签<n且无重复；fresh长度<n选最小未用A，fresh长度n选D，其余用`max((收益,−标签))`选择最大收益、平局最小标签。随后assert所选收益确为全部孩子最大，存sigma[h]与该规定续局completed[h]。它完整实现了现定理的逆向构造，未把非fresh节点重新变fresh，也没将所有平局规定为严格。

P=build(())后断言actual路径是0,…,n−1,n。另独立遍历所有长度0…m−1的有序历史，对每个action含自身再核IC；非末位用completed[h+(a,)]，末位直接用h+(a,)。这是一份实现内的第二遍比较，不是另一个独立实现。默认n3的400决策前缀为1+7+49+343，2800比较为400×7；build还会访问7⁴=2401个终局叶，不能把报告400说成包含终局叶的全部树节点。

其后对每个sender j生成同一末位cut强制T_j的孩子，逐单位客户算parent/child负载及标准q，断言(parent,child,q)=(2n−1,n+1,1)、λ·child=parent；总输出需严格大于末位收益且比值等于(2n−1)/(n+1)。实际覆盖全部likes后，welfare等于总客户2n²；代码把optimum设为welfare，依据的是全覆盖上界达到，不是另跑最优元组搜索。

最后把含完整actions的JSON写至**脚本同目录**`amount_cap1_family_n{n}.json`，stdout仅打印去掉actions的summary。没有独立输出路径参数；在原目录执行会写同名文件。本批未执行/import，不覆盖冻结证书，也没有新stdout/exit可声称。

## 冻结n3证书的全部标量和三请求

原JSON36652B，SHA256为`810885da8ca4e752ec2d81f30f7ade5194270e54b678b884e5260c4bb2b502c3`。根字段共16项，下表覆盖除requests/actions外全部14项。

| 字段 | 原值 |
|---|---|
| claim | AMOUNT-CAP1 false; no HALF counterexample |
| n / players / topics / unit_customers | 3 / 4 / 7 / 18 |
| ordered_nodes / IC_including_self | 400 / 2800 |
| actual_path | [0,1,2,3] |
| welfare / optimum | 18 / 18 |
| recipient / recipient_payoff | 4 / 3 |
| combined_positive_price / column_coefficient | 15/4 / 5/4 |

requests原记录中sender/cut是一开始计数，forced_topic沿脚本零起始标签：

| sender | cut | forced_topic | parent_payoff | child_payoff | claim_coefficient | positive_price |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 4 | 5 | 4 | 5/4 | 1 |
| 2 | 4 | 5 | 5 | 4 | 5/4 | 1 |
| 3 | 4 | 6 | 5 | 4 | 5/4 | 1 |

由此可读实际利润(5,5,5,3)，但原JSON没有单独的profits数组；该向量亦为independent审稿明确报告。每sender预算(5/4)·4=5满额，recipient正价3·5/4=15/4>3，实际仍全覆盖18。该有限数据只实现n3；全n结论由现定理解析证明承担。

## 完整400动作的无损表式

以下只是原JSON数据的重排，不重新求最佳回复。根动作0；一动作历史h=(a₀)的规定动作如下。两动作历史表的行a₀、列a₁给第三人动作；七个末层表各固定a₀，行a₁、列a₂给第四人动作。连同根，共1+7+49+7×49=400条，完整编码了原actions，不删非fresh/重复/T/D历史。

| a₀ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 第二人动作 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

两动作历史（此表行是a₀，列是a₁）：

| a₀ / a₁ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 1 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 4 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 5 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 6 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

末层表：固定a₀=0。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 1 | 2 | 2 | 3 | 2 | 2 | 2 | 2 |
| 2 | 1 | 3 | 1 | 1 | 1 | 1 | 1 |
| 3 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 4 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 5 | 2 | 2 | 1 | 2 | 2 | 2 | 3 |
| 6 | 1 | 2 | 1 | 1 | 1 | 3 | 1 |

末层表：固定a₀=1。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 2 | 2 | 3 | 2 | 2 | 2 | 2 |
| 1 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 2 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 4 | 2 | 2 | 0 | 2 | 2 | 2 | 3 |
| 5 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 6 | 2 | 0 | 0 | 0 | 3 | 0 | 0 |

末层表：固定a₀=2。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 1 | 3 | 1 | 1 | 1 | 1 | 1 |
| 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 4 | 1 | 0 | 1 | 1 | 1 | 3 | 1 |
| 5 | 1 | 0 | 0 | 0 | 3 | 0 | 0 |
| 6 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

末层表：固定a₀=3。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 1 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 4 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 5 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 6 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

末层表：固定a₀=4。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 1 | 2 | 2 | 0 | 2 | 2 | 2 | 3 |
| 2 | 1 | 0 | 1 | 1 | 1 | 3 | 1 |
| 3 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 4 | 1 | 2 | 1 | 1 | 1 | 2 | 1 |
| 5 | 2 | 2 | 3 | 2 | 2 | 2 | 3 |
| 6 | 1 | 3 | 1 | 1 | 1 | 3 | 1 |

末层表：固定a₀=5。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 2 | 2 | 1 | 2 | 2 | 2 | 3 |
| 1 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 3 | 0 | 0 |
| 3 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 4 | 2 | 2 | 3 | 2 | 2 | 2 | 3 |
| 5 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| 6 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |

末层表：固定a₀=6。

| a₁ / a₂ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---|---|---|---|---|---|---|
| 0 | 1 | 2 | 1 | 1 | 1 | 3 | 1 |
| 1 | 2 | 0 | 0 | 0 | 3 | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 3 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| 4 | 1 | 3 | 1 | 1 | 1 | 3 | 1 |
| 5 | 3 | 0 | 0 | 0 | 3 | 0 | 0 |
| 6 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |

本批结构核对这些动作的history键域恰为全部7进制长度0…3前缀、无重复键、动作均在0…6、报告排序为深度再字典序，并从四步规定链读到[0,1,2,3]。**这些是动作表结构检查，不是重新计算2800项SPE利润比较。** 完整表的历史执行认证按下面原审查记录保存；当前没有另生一次数学成功日志。

## 两原审查的实质重构与可说的先后

credible审3622B逐类型重构同一全n模型，解释非fresh缺陷永久保留使BI补全是封闭子树；复核fresh末位D与任一A都得n，所以D只是允许的最佳回复，不能写为严格。它分别核其它未用A、重复A、T、非根D及根D五类偏离，最后一类只用真实离轨末位理性，不冻结后继；再重算parent/child利润、q1、AMOUNT满额与列比。它特别指出forced T_j即使不是末位BR，仍是合法强制孩子，以及同cut多孩子和λ可大于1是承重条件。

该稿自标独立攻击审查、无实质异议，但没有陈述先收到何种statement/何时读作者正文的详细日志，也未声称运行原3332代码或读取全部36652B输出。这里保其解析重构身份，不补成严格盲审、独立程序或一次新运行。

independent审3527B明确称先独立重构一般证明、随后对照作者正文，全文确给完整fresh/非fresh策略、五类偏离、根D关键最后BR和金额计算。按该原稿明示保留这项“先重构后对稿”顺序；没有更细收题/先验输入日志，不再补强为完全未知命题的盲审。它还明确报告把作者n3原代码复制到自己的目录重跑，覆盖400前缀/2800含自身比较，得到(5,5,5,3)、18、预算满额及15/4>3。

这次历史运行是**同一个coupling实现的重放**，原稿自己也明确不称独立实现；为了避免冗余，重复脚本和JSON后来删除，复现入口指回当前coupling代码/输出。本批没有找回或重建一份“独立实现”副本，更没有凭这份MD制造原argv/环境/exit日志。一般独立数学重构与同实现有限复跑是不同证据，均准确保留。作者稿另称父方复跑逐字匹配；没有其原始运行日志，这仍按作者记录身份保，而不冒当前byte comparison。

## 与父方深层cap2筛查的输入接口差异

[父方原筛查合同](跨枝金额列容量原筛查的完整策略与输入过滤合同--程序.md)扫描旧ROOT/evidence/certificates/customer_attraction/*.json，要求strategy同时含actions和terminal_counts且有同basename的examples输入。当前family输出在coupling目录，且其16字段中**没有terminal_counts**。即使另备同basename例文件，这份原JSON也过不了该字段门槛，不能默认被那段glob筛查接受或据旧阴性报告声称已审了它。

family生成器把单位likes内嵌在代码；父方筛查从项目Instance/example读客户，两者没有自动格式适配器。本稿不擅自搬移、补字段或改报告去重跑旧全证书。cap1反族的n3列比5/4本身也不违反cap2；两个程序的不同目标/默认IO和数据格式应分别记录。

## 本批处置与当前限度

本批五源原件/SHA/blob/实际完整claim均核；作者6880B数学精确duplicate到现定理，原程序/冻结证书/两审稿四件retained，以本页完整保存原实现、全表、数字和实际审查边界。此前作者稿作为related时没有done，本次才转primary处置；此前normalshow同SHA复用的事实不改为一次新取源。

当前原入口0、import0、新数学实现0、payoff/IC重算0、LP或SPE搜索0。已有全n解析证明及原同实现复跑报告未出现需重跑400/2800的具体数学缺口，因此不机械再执行；结构核只读字段/键域/动作范围/实际索引链，不冒全IC复验。冻结JSON没有代码SHA、argv、环境或exit日志，本页不倒填这些字段，也未宣称当前原生成器再次逐字节复现36KB输出。

两个原审查均不审一般half或证明更深cut的cap2；本族W=OPT，不能将辅助合同的反例改名为目标反例。重复/空主题/任意平局的通用模型仍在现定理中保，家族只证明存在一份允许的完整SPE。无外审、新颖性或固定人数最优常数认证；数学一般性、有限实现数据和审查先验各按自己的实际证据保存。

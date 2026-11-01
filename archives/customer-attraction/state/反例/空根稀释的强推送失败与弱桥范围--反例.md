---
id: "customer-attraction/empty-root-dilution-strong-push-failure-and-weak-bridge-scope"
kind: "counterexample"
type_tag: "反例"
title: "空根稀释的强推送失败与弱桥范围"
status: "complete-57-history-analytic-extension-and-general-two-point-identity; not-half-failure"
summary: "保34客户加入空主题后的14新节点解析SPE论证、全部收益/真实分支与一般epsilon恒等式；固定强反例仍有u−C正松弛，旧搜索/缺失独审与已成功同SHA程序分开。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/README.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_D_lt_C.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_D_lt_C.md"
---

# 空根稀释的强推送失败与弱桥范围

## 原件、比较对象和准确命题

[3569B主稿](../../../../tools/evidence/weak-pushforward-and-static-prefix-primary/original/71bdd0dc3ec8f127e59b/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_D_lt_C.md)和[2590B路由](../../../../tools/evidence/weak-pushforward-and-static-prefix-primary/original/666061ceda2882cfd25d/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/README.md)全文实读。它补充原JSON之外的14个空历史解析延伸与一般小概率机制；不只复述D−C负值。原作者定义级核验、root独立核验是其历史证据身份，无外审/新颖性。本批未取得其3051B audit_integer_push_34.py和5246B同名报告，不能把现有另一个3119B独立程序冒作这两个原件。

三名单位提供者、34个不同单位客户、七个共同主题0,…,5,E6，E为空。固定完整SPE，强制根B~p后沿同σ得含全部三槽的Z(B)。真实根收益均值D(p)=E_Bu_1(Z(B))；额外第四位查询A~p独立，C(p)=E_(A,B)Σ_(x∈A)1/[1+c_x(Z(B))]。被否定的是每个完整SPE、每p均D≥C，不是每p实际最优u≥C。

## 数据与完整策略

前六主题为X0,X1,X2,Y0,Y1,Y2，客户mask及不同单位数为

| mask | 数量 | mask | 数量 |
| --- | ---: | --- | ---: |
| 4 | 1 | 27 | 4 |
| 29 | 3 | 30 | 3 |
| 31 | 2 | 32 | 1 |
| 43 | 3 | 45 | 3 |
| 46 | 3 | 51 | 3 |
| 53 | 3 | 54 | 3 |
| 59 | 2 | — | — |

基础六主题/34客户的[完整43节点SPE](../反例/三人逐人混合安全值--反例.md)已逐表证明。根0，第二人见首主题在X={0,1,2}取3，否则0；两非空历史(a,b)后末位取b所属组三标签最小未出现者。加入E后，首E的第二人取0；末位恰有一个非空a时用rho=(1,0,0,4,3,3)，双空取0。前述规则与[7992B全部57动作](../../../../tools/evidence/weak-pushforward-and-static-prefix-primary/related/f218c3c894b4635ecca2/research/workspaces/customer-attraction/R-d22a706a03c5499d941a6a97f94128a8/representation/terminal_pushforward_34_D_lt_C_exact.json)逐条一致，尤其(a,E)不能误用全局最小标签；EO结构绑定已准确保该区别。

## 新增空历史的解析SPE检查

令U(t,a)=|T_t|−|T_t∩T_a|/2，为一个非空旧主题a加一个空行动之后，末位选择t的真实收益。六主题大小(23,23,21,23,23,21)，普通标签指0,1,3,4，特殊指2,5；同组普通对交14、普通/特殊对交11，跨组普通对交17、普通/特殊交14、特殊/特殊交12；这些由上表直接求和。故一空历史的rho及两名理性尾部首位收益为

| 非空a（或E） | rho(a) | 最后位最大收益 | 尾部首位选a后自身收益 |
| --- | ---: | ---: | ---: |
| 0 | 1 | 16 | 16 |
| 1 | 0 | 16 | 16 |
| 2 | 0 | 35/2 | 31/2 |
| 3 | 4 | 16 | 16 |
| 4 | 3 | 16 | 16 |
| 5 | 3 | 35/2 | 31/2 |
| E | 0 | 23 | 0 |

最后一行对应双空、最大主题0大小23。表中一空收益只依赖那个非空a，所以同时覆盖(a,E)与(E,a)共12个末位历史，双空再一，共13。空根后的第二人面对七个行动的真实收益为(16,16,31/2,16,16,31/2,0)，规定0最优，新增的第14个节点亦最佳。

旧43节点仍由原SPE控制所有非空偏离；新偏离E给当前收益0，不会改善非负的规定收益。根六个非空行动仍各得29/3，空根自身0，因此根0最优。此解析合并覆盖完整57历史，不要求匿名化一般SPE或排除离轨平局。actual(0,3,4)，利润(29/3,67/6,67/6)，W32；E不新增覆盖，原OPT3=34不变。

## 两条完整真实分支的精确负差

p(2)=1/10,p(E)=9/10。空根分支(E,0,1)中根收益0；主题2根分支(2,3,4)中根29/3。独立查询2对这两个**完整三槽**的价分别32/3和13/2，因此

\[
D=\frac1{10}\frac{29}3=\frac{29}{30},\quad
C=\frac1{10}\frac9{10}\frac{32}3+\frac1{100}\frac{13}2=\frac{41}{40},
\quad D-C=-\frac7{120}.
\]

u=29/3，u−C=1037/120>0，实际顺序D<C<u；原JSON kind中的NOT-C-LT-U不作数学真值，字段绑定/纠正在[完整证书资料](../资料/完整根查询证书的字段与审计范围--资料.md)。此例不否定实际u封顶、平均负载分数背景、自由额外槽值或half；一般WP另有不同银行输入反例，见[合法前缀归约](../引理/合法前缀的静态额外槽预算与条件归约--引理.md)，不能互相错认。

## 任意空根稀释的精确机制

任一允许空主题的完整原策略，固定合法T，令p(E)=1−epsilon,p(T)=epsilon，0<epsilon≤1。空源自身收益0、空查询价0，记g_T(Z)=Σ_(x∈T)1/[1+c_x(Z)]，则只剩三项

\[
D-C=\varepsilon[d_T-g_T(Z(E))]
+\varepsilon^2[g_T(Z(E))-g_T(Z(T))].\tag{EMPTY}
\]

所以a=g_T(Z(E))−d_T>0时，T必非空。其原根自身覆盖T的客户，使d_T−g_T(Z(T))=Σ_(x∈T)1/[c_x(Z(T))(1+c_x(Z(T)))]严格正；故二次系数b=g_T(Z(E))−g_T(Z(T))=a+[d_T−g_T(Z(T))]>a>0。负差恰发生在0<epsilon<a/b<1。空根后的真实尾本身是完整SPE，但根空行动一般非最优，不能删掉u−D这笔真实激励松弛。

本输入a1,b25/6，根部多项式−epsilon+25epsilon²/6，选1/10给−7/120。与三个actual位置合计的强预算多项式−epsilon+12epsilon²是不同目标；后者旧审计在1/24给−1/48，同1/10却+1/50。不能把根差值冒作整体失败值，更不能把强ΣG≤ΣD换成弱ΣG≤W。

## 发现轨迹与证据可复用范围

README称先有381客户JSON，后据空主题机制缩到34；381只为发现轨迹，本批本地未取得，不重构成新已证实例。原始搜索的浮点候选不凭exact文件名自获认证。k2复制弱例曾因少分母+1撤销，不能与这个保完整三槽再加查询1的真强反例合并。

本34输入同SHA的[既有3119B单位审计](../审查/额外槽扫描的实际强桥目标与两份定义级核验--审查.md)已真实成功核57节点399含自身/342非自身，EG又一次固定根算术核本节D/C。EO完整读其代码/旧执行/所有字段，EX字节复用而不重跑；这不是恢复本稿引用的另外3051B原程序。正文的新增空节点表与EMPTY是固定数据/双抽样的解析说明，不新增CLI、solver或SPE扫描。

强式失败不使源的弱式假设自动失败；当前WP普遍状态由独立银行反族决定，而一般half不因两者失败被否定。源README的下一步路线与未正式入库身份仅作历史；本轮完成的是完整保全证明、量词、发现/审查/实际已交证据之分，没有外审或新颖性认证。

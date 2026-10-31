# protected-cycle 只读准备交接（未认领、未成稿）

下一5来源的claim真实失败：parent报告代理CONNECT 403、网络调用取消、未pushed、本地无认领记录。本agent未重试network，未读取这5份primary原文，未写其正式数学正文或semantic-receipt，更未claim/done。计划将来staging为r3-protected-cycle-exchange-history，但必须在恢复写端点并收到新的实际pushed/synced认领确认后再正式读取、核SHA、逐版本比较和成稿。本目录只是获准保留的只读准备记录。

## 已经实际读到的上下文

已完整重读近单位canonical29d4881762b3773ed35d，32780B，SHA17b9a0fd3169f7b49bfcd279f17d300c4b2b4cced02be69f1deb05939da97307，包含§1–9。一度合并多文件tool输出被截断，随后单独完整重读，不能把前次截断算全文。完整读过旧正式《近单位PCSP与单位presence胶合双源审查》；它的数学正文未展开§9 protected Ci+Rc共同证书，后续五history可自足补齐，不重做既有主源29的done。

上下文§9声明的物理矩阵：每occurrence两原机M_i/C_i，每clause真实原R_c；q_i可M_i:a/M_(i+):1/C_i:1，真实i另可R_c:1；b_i可C_i:1/pin(i):a；u_c只本clause真实C_i:1，无R资格。0<a<1，每clause至少2物理occurrence，重复保持不同索引，变量环padding>=3，dummy不属clause。Rc是**真实公共原机**，不是新direct-cohabiting B/C证明的virtual标签，u也是unit，不能混成x/y半权模型。

已读上下文的全局证书：真实theta_i=1/k_c<=1/2、dummy0；q两个M先half，从pin扣theta并给实际R_c theta，q不向C给fraction；b在pin/C为theta/(1-theta)，u向C theta。所有job行和及M/C/R列和1，整数matching选原有限端、非idle每机恰一原job且原time<=1。这里分数是分析证书，非分数执行；a>B/2仅可选nearunit设置，不是该构造必需。

上下文提供10机10job UNSAT例：(x∨x)∧(¬x∨¬x)，顺序正正负负；q1R+、q3R−、q2M3、q4M4，b1C1、b2M2、b3C3、b4M1，u+C2、u−C4。读出q索引1/3，而返回b索引2/4，说明新增Rc接线后旧同编号/环phase推断不可免费沿用。它是保存的实际证书，不是本轮运行或一般枚举。

上下文明确v1空公式零台机器的问题由v2加一idle机修复；**尚未读v1/v2五份原始稿，不能先断言实际版本差异只有这一项**。恢复后必须全文读、实际diff、保反对/改域记录，核非空与空式、所有原jobs/finite端/dense成本及真正审查先验；不得以本上下文替五primary全文或把当前已知数学称新blind。

## 待认领来源与再后续

下一5元数据见candidate-inventory-snapshot.json：fc99dd4d57172611cc3c v1Exact、38db10e207ec50b55f72 v1Proof、4c40cbb485a3f56c7d2b Exact-first、59fe9850e4c59f801c90 v2Exact、41481a485314ca0453a3 v2Proof。各primary文本尚未读，metadata不算语义receipt。随后28818a3d1bca95c1ff20、49cd6d82095834f4adcf、78e0e856c2e3b5547327为读后/§9canonical终读/root终审，也没有本轮全文读取。

## 已完成成果的真实保存状态

- 尾批3已完整交付r3-uniform-exchange-final-tail，15文件/69956B，source claim pushed cf736ed49e4f3a2fd8dae8d985bb7eca5403a7a6。Parent最新报告已拷入repo；本agent未收到该尾批body远端pushed确认，不将其称已远端保存。Parent正处理本地checkpoint/handoff。
- uniform v2五源16文件及前面8个checker维护overlay，parent报告H17 body已实际pushed（仅提供前缀4696aac…），H17数学done尚未登记。本agent不补写/重跑done。
- 独立维护目录r3-checker-root-mode-fix：只拷control/copy-files.json的8个overlay目标，control/patch-manifest.json保实际repo beforeSHA、旧delivery beforeSHA及afterSHA；旧4包原文件/清单未改。4新脚本各在实际repo及旧staging验一次，8次完整性执行全PASS、数学run0；parent确认维护随H17 body推送。

所有主要交付stage及精确清单均在boss4-next-cache原路径保持。当前停止network/新认领来源成稿，等待新会话获得允许的写端点及真实claim确认后续接。

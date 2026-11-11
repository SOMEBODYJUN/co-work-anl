# raw S3 v4 定向复核

本任务替代 `boss3-sourcefix-repair-3f12a56d6fbf6961`，负责19核心及6共享对象。25个当前registration pins全部与当前registry一致。与旧任务相比，唯一变化的端点是raw-S3从旧pin `58dad6…`到当前v4 `55a06a…`；reading_refs改变的是d38审查SHA `b7af1754…`→`afefdddd…`，主资料桥与作者完整合同/证明SHA未变。

## 实际阅读与继承边界

本轮读当前任务全文；旧任务逐字段对照，读取不同值、确认其他值精确相同；旧收据全文；当前registry内19核心和6共享对象的陈述、域、量词、假设、scope、objections及body/evidence定位；9条旧边完整解释和精确作用范围。当前原文实读：

- `archives/unrelated-machines/state/资料/rawS3到canonicalSA1同点提取--资料.md`，全文128行。
- `archives/unrelated-machines/state/审查/完整原端三次条件的作者合同与拉回证明--审查.md`，全文156行。
- `archives/unrelated-machines/state/审查/identity-coupling-raw-k2-sa3-final-sections--审查.md`，全文157行。
- `archives/unrelated-machines/state/问题/不相关机的统一整数输出与全调度解码--问题.md`，仅完整唯一章节“阈值接口与可靠失败”。
- `archives/unrelated-machines/state/定义/不相关机器与两个调度松弛--定义.md`及`archives/unrelated-machines/问题--问题.md`，全文。
- 旧资产`raw-s3-five-group-non-psd-witness.md`，全文33行，解析重核各类约束及有理负平方。

其余18个未改版核心的承重正文没有在本轮重新逐句展开，沿用原任务/收据成熟比较，各coverage明确标注继承。8条保留边的字节、端点/证据绑定和edge-check已核；SHA核对不冒充数学重读。未读或运行旧附件程序、原始作者evidence、未列文献PDF或远端数学程序。

## 已付清的Dirac与FAIL链

固定完整显式normalized-flat菜单Q，所有原selector/incidence/零端/重复indexed states/unused resources/未选payload均保留。任意有理1≤T<2的完整真实threshold-T调度σ，在原finite-endpoints给0/1赋值，定义degree≤4 functional为逐点求值Lσ。Boolean/cover恒等式及允许乘子逐点为零；box和physical slack非负；resource端每件耗时一，故T<2强迫每resource至多一原job，独立unit-cap1非负。每个允许raw-literal乘子包括空/重复/互补均非负，所以整个S3成立。σ不必是canonical调度，也不依赖另一给定K2或S3点。

因此精确S3 LP不可行推出OPT(P(Q))>T。LP有O((N+1)^4)个moment变量、O(R(N+1)^3)个不等式lift和固定多项式等式lift。Farkas严格矛盾归一化、等式系数拆成两非负量后，基本解的Cramer/Hadamard界给多项式位长有理证书，可逐项独立核验。此局部论证完整；源对象当前登记conditional，故新边按合同保持accepted/conditional，仅标contribution，绝不据此声称目标完整阈值接口。

## 同点pullback与可选PSD

给定完整S3的同一L，A_s=a_s、Z_e=a_sE_e。primitive/补的正literal展开每项≤2因子；box/gate及resource补项≤4因子；resource主项需独立cap1。quality使用精确恒等式

`q_s-a_s h_s=(a_s²-a_s)+Σ_e p_e a_s(D_e+E_e-1)`。

乘canonical primitive/补W后，Boolean乘子≤2次、cover乘子≤3次，physical slack乘子≤3 raw literals，最高总次数4。因此完整二阶plain-SA1及所有row lifts保持。只有同一个L另具raw M2，canonical affine pullback degree≤2才给M1。S3不自动PSD，也不给Boolean赋值、共同真实law或整数舍入。

从实际调度“另造Dirac点”的存在性不能升级手中另一指定K2点。d38十八机例有OPT=1，而指定点有−1/160的跨行三重矩与−c/160的quality lift；二者相容。要求全部global triples非负才排该证书，任意一个triple非负不足。

若已给满足canonical行的Boolean赋值，gate使未选state的Z全0。把Z=1原incidence外送、其余回private，selector去唯一A=1状态：所选private为2−ΣpZ≤T，未选private为1，resource≤1。该整数商的正反向说明不从普通矩表产生上述Boolean赋值。

## 五组非PSD附件

五组两态，每态一件系数1、资源全部不同。原端代换为selector b_i/1−b_i、incidence private端0/resource端1，degree4 moments μ=(1,1/2,1/6,0,0)。至多四个不同位的p正q负cylinder值为binom(4−p−q,2−p)/6≥0；重复可约化、互补为零。每条S3不等式乘允许乘子经代换都是此类≤4因子cylinder或零；等式恒零。canonical Z=A，gate/quality行零，resource/box为literal，因此plain-SA1保持。

Y=Σ_(i=1)^5 A_(i,1)有F(Y)=5/2、F(Y²)=35/6、F((Y−5/2)²)=−5/12。只排指定表的M1及共同真实law，同一raw点也不满足可选M2。原矩阵另有全部incidence送独立resource、任取selectors的峰1完整调度。附件数学正确，保原路径原SHA，不改原文或registry。

## 保留边及每个follow-up

8条旧边保留：共同尺寸价格→统一头部证书、共同槽→有界配置为局部contribution；双树k4→medium/tiny及克隆包络→共同cycle为完整无条件特化；dense backend→一般目标、packing A→部分调度、可靠阈值接口→一般目标、一般UM算法且压缩桥→DAG比例保证保持完整conditional结论。最后一条保ALL两个承重前提。

当前修复任务和直接前件修复任务均无新follow-up，follow_up_tasks为空。原始任务的两个follow-up已解决并继续保留：

1. 共同cycle/有界克隆包络：同一identity/shift见证逐原任务完成、unit下界及包络给t1=2−1/m、t2=1，完整特化边已解决该对。源相关精选接线的NO decoder不是该已解决比较的遗漏。
2. medium/tiny/一般双树：k4/h3给74机169任务、CONFIG(5/4)、OPT=7/4、min p=1/4，对每个0<α<1/5完成特化；不延至α=1/5或否定正面K损失定理。

不额外把上述旧closed_overlaps写作本任务新overlap，以免伪造当前任务未列的对象对。

## 未付范围与资产处置

新边只付受限域可靠FAIL；S3可行分支仍需全部原任务固定ρ<2实际输出或另一可靠失败测试，且全接口尚须一般UM/所有T≥0。它无需拒绝每个OPT>T阈值。统一UM算法、dense后端B、packing后端A仍开放；部分任务权2/3不等于全任务输出；CONFIG gap/局部坏态不成为一般复杂性反面。

旧10资产逐项处置：8条无关边原SHA保留；raw-S3旧边同edge_id以新路径重新绑定替换；五组附件原路径原SHA保留；加入本说明。无原正文/registry修改；无Git或队列写入。本地结构和绑定检查不替代数学。

# Universal wallet v3：221行精确最优与共同最大A6接口

Boss1；RUN `six-boss1-20261111`。状态：**只一次授权LP；精确原对偶、全部源系数和残差核验完成；停止扩跑。** v2及更早三包/摘要56文件保持原字节。

## 数学结论

完整保留v2的219原行及全部256客户型+真实K，只加ROOT_SIZE_FEEDBACK与ROOT_TRUE_TAIL，得到221原始行、209去重行、257非负变量。

精确最优为

\[
\boxed{\alpha_3=\frac{999866079286562265469481}{2318932167377271341801106}
=0.4311752164865684\ldots.}
\]

10正预算的精确非负对偶证明原完整模型 \(W\ge\alpha_3\operatorname{OPT}_6\)。11正原子加K给匹配精确点，故这是指定221行必要系统的精确最优，仍低于half。没有完整SPE实现或反例主张，也不认领优于已有最佳全域界。

正付款为SAFE2(A6)、SAFE3(A5)、SAFE6(Omean)、UP2/3、MX(Omean)、RC(Omean,Omean)、K−|A6|、TRUE_X_TAIL_CUT、ROOT_TRUE_TAIL。ROOT_SIZE_FEEDBACK的权为0且在展示点严格松弛；该行仍完整保留检查。

ROOT_TRUE_TAIL的K系数已在自由列核准：37375524862−25779840855=11595684007。数值发现使用已记录正行尺度，最终原对偶及全221行全部回到原始未缩放分数。其约5.7×10^−12的正对偶权没有被数值阈值误删。

## 下一接口的准确量词

因为K−|A6|和ROOT_TRUE_TAIL的对偶权严格正，**每个221行最优点**都有K=|A6|和根线取等。若它来自原SPE，可以令真实最大标签C=A6，并要求该同一根分支的十个正预算和128型余项同时取等。TRUE_X_TAIL_CUT亦有正权，故其同一X两尾六钱包也必须同时紧。

当前展示点还令实际末位对X的BR紧；但此BR对偶权为0，本轮未把该事实推广至整个最优面。新点的X覆盖约0.005987939176实际未覆盖客户，不能把X强行限制在实际覆盖中。

本轮只记录这些共同分支必要接口，不扩新LP、不添加行族、不声称新点已被排除。后续独立任务由Main另行指定。

## 复核

[完整证明、10项整数权和11原子表](universal_union_wallet_v3/proof.md)；[精确证书](universal_union_wallet_v3/exact_certificate.json)；[独立checker结果](universal_union_wallet_v3/checker_output.json)；[全部残差索引](universal_union_wallet_v3/residual_index.json)。

```sh
python research/workspaces/six-boss1-20261111/universal_union_wallet_v3/check_certificate.py
```

checker不导入builder或优化器，核56797个源系数、221原行、257对偶列以及两新根来源，全部PASS。v3输入SHA `d5808676b4a59bc9a63deece83e291887ead8847a7177c3afac4221523f30f55`；其余最终哈希见manifest。

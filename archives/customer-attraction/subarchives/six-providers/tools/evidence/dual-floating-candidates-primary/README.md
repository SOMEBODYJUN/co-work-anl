# 三份完整终局浮点候选的证据包

本包保存三个冻结源版本的 `clean show --out` 原始字节，均来自 `R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/dual/`：

- `crosscap_n4_k6.json`（source id `42fcde2d629e9616429f`，SHA-256 `dc10f818d0c93f5eec70ce994a0151832cd0e72676f4a9abff78e63250d7ddd1`）：n=4、k=6、policy=141、pair=(3,5)、gap≈1/49、W≈36/49，含259个完整有序历史动作和12个非零浮点客户质量。其动作表与已归档的四人245客户精确输入一致；本包只保留浮点发现运行的来源与状态，不把它当作精确证书。
- `full_dag_best.json`（source id `ca04f81c425731a26fe5`，SHA-256 `bbbb1c6ee94ade5d0a9ee9abe9a393d09d7b784c9e0d9b8789974d38323aeadd`）：在R-275填充六人九主题完整DAG的交替LP点，gap=-1/9、W=2/3、cap=5/54，p在主题1,2,3上各1/3，保留16个完整终局背景；不含新动作表或SPE重证。
- `full_push_n3_k6.json`（source id `e5dacc2068167555dfbd`，SHA-256 `a60c877b2b05401202600dcf08a75c9c4432591bbd5edcd3602195d645002ff9`）：n=3、k=6、policy=6、iteration=0，gap=-1/28、W=3/7、p为六主题均匀分布，43个有序历史动作和五个非零客户质量；是全p完整终局推送目标的一个有限浮点点。

三源的状态字段都明确为 `floating discovery only`。浮点 LP/SLSQP 输出、有限迭代和负 gap 不能推出一般 SPE、精确 dual、原模型反例或六人半覆盖结论。原冻结来源仍是唯一来源身份，本包不改写其字节。

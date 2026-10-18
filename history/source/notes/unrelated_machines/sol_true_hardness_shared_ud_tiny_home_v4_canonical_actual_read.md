# shared-UD tiny-home v4：最终新增正文 actual-read 记录

审者 `/root/sol_true_hardness`，2026-10-18。知情最终正文实读；不改旧 Exact-first、作者读后或 canonical。

## 实际文件及阅读范围

实际读取 repo 只读文件 `research/current/unrelated_machines/multi_outer_single_state_tiny_home_rounding.md` 的新增第176–382行，207行含空行，全部 §12–20 及末尾另一独立证明说明。整文件382行、41518bytes，实际 SHA256：

    9ddf2305f65389409b7f4955a58a72256c98113d52e782cf108588d6819bde99

前175行只取字节 hash，不重读、不升级旧v1审查：17086bytes，SHA256：

    84d6031655ac43d9c5726ed2cac6f5241e709743232290e604d767602613778a

新增176–382行共24432bytes，独立实际 SHA256：

    f72b025518869aa34b1c0f863e5ef6eec3e185355c81019870ff19c1b1a5f9bd

本次同时实际生成了相对已全文读作者v4b（`1e3710870c8fbef4d4235cf2f90fe2d8ec6ca84b99ec6cd234464cc9d260df44`）的完整文字差分。新数学算法、公式、常数及分支没有变更；变化为规范状态/保真链接/实际审查与软件范围、vacancy措辞、末尾149行独立证明链接。

## 数学与量词

新增正文仍是同一个输入变量k的v4量词：k1无tiny，k≥2要求ν≤1/(16384k²)，单state outers、互异homes、own-unit helpers、B-only任意fallback、固定ε=15/16 exact-threshold-UD额外叶。无叶全匹配仍走真实baseline；empty/no-fallback、rank0、零incidences及重复states未被删出域。

本次全文核对：k1 fixed-order submodular greedy，k≥2 profile primal势/任意optimal fractional stable coupling/新k²曲率/rational FW/actual soundFAIL/共同leaf prefix-flow/最终Good helper与全部原jobs恢复，均保持作者v4b中已逐项实际读后核过的算法。未见新fatal；无需用我的另一实际allocation局部算法替其补步骤。

vacancy新句明确“叶侧已饱和、原资源侧rank=叶数，不假定=|B|”，准确消除旧“满rank”的潜在歧义。OPT=2−V、baseline与成功19/10分支、固定γ<1/10时仅对此域的source-gap排除均保原范围；末句也明确没有源问题decoder，不能称为一般UM反证。

## 阅读顺序与软件边界

本文对本审者的顺序描述准确：三个Exact先行→149行独立actual-allocation冻结`69036ac6…`→root实际读后释放作者v4b→80行作者读后`4d2d398e…`→本次规范新增部分全文实际读。我的独立算法原稿不使用FW、optimal stable coupling或最后prefix-flow，这一差别在新末段正确保存。

关于NSW旧/新审票、root实际软件完整读及fresh重放，canonical将其与本审者分开归属；我没有打开这些审票或finite code/json/scope文件，不能代签。正文明确finite软件只核4/5资源的exchange lemma，没有运行FW/potential/profile搜索、tiny输入、prefix-flow、k1 greedy或全部UM jobs；没有声称端到端实现。未把旧v1软件身份升级，也未用finite样本删除tiny条件。

本记录仅为上述规范新增207行的实际全文数学/范围/元数据核对；未认证旧175行、未读链接内容、程序、primary、新颖性、固定k heavy新working或一般UM。旧两份记录原字节不变；主真实近2硬度目标仍OPEN。

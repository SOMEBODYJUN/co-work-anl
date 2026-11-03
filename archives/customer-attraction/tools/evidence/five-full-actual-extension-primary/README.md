# 显式实际第三位扩展：九主源原件与阅读范围

本包保九个主源3118172B；`source-manifest.json`逐件固定源ID、完整原路径、两冻结commit、Git blob、size、SHA256及canonical保存路径。双冻结定位为`68fad804ec5946cb296f77dc5b336308a66abf12`和`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，同内容只处置一次。九主源已逐件正常`clean show --out`，stdout、空stderr和原字节核对在`acquisition/`；该只读取得不代表正文已推送或来源已done。

|source ID|原文件名|字节数|SHA-256|
|---|---|---:|---|
|`e16b612c8f680b846fc4`|`full_actual_extension.py`|5738|`34ed7cff5840fd75c5e0a228cd09ce16a08791b6075f3276682612cc1fd929e0`|
|`9aefbd5eafbef218ffff`|`known_actual_extension_pricing.json`|106521|`3cbdedf47253e28fab8596779b71a48a45f3a7557653eda597bc0d8df6ae04f6`|
|`54c6e788dc2fd08c384d`|`full_actual_extension_diagnostic.json`|547|`641f3b84cb131deeff6fbf7ca12318d5a101faa696ccb199ac21bd0c622b6f72`|
|`b222d1ec47f55691fe81`|`price_known_actual_extension.py`|7056|`d1b00f989b6e88f1950f08994d820ca3f1a091486241bd4187f43b916b0f1cdb`|
|`f6523d32bc3b03e8cb47`|`full_actual_extension_known_v1_discovery.json`|693869|`38876257c4935129ba9d6178d82db796d9ebc9817b956242bdfd64de97f9985d`|
|`f4fbc575910925a48d8a`|`full_actual_extension_discovery.json`|609085|`e0ad3d3e7599ee73ff90116e7d07b93fae674d97e3dcffb693089c4b8173aa20`|
|`08bb85310be0133f9f10`|`exact_full_actual_extension_known_v1.json`|1688965|`8b28de8d89c76684bc95c3eb3f890e6f4ee4492cb152102281d125912e2a30e2`|
|`41a7c7c2f319b580be2a`|`full_actual_extension_diagnostic_v2.json`|547|`4a8e50bf9ea4ff19ec7ac65a6dc848eafb7591db9917a25c1869329a3dc9d131`|
|`698d8947f0ff0623e52a`|`reopt_full_actual_extension.py`|5844|`012a541af8530e643dac74854bb98402b9d9560fe6ff2d825105984e80e99c43`|

正式数学去向：

- [受限列与旧池定价程序](../../../state/程序/显式实际第三位扩展的受限列与旧池定价--程序.md)：共享actual-HQR的747行语义、A13删除理由、LP/稀疏分派/前12列核系数/去重及Fraction恢复完整合同。
- [7497行有理必要点](../../../state/计算/实际第三位七千四百九十七行的有理必要点--计算.md)：两个diagnostic版本、504→623列数据链、85显式与64投影全部质量和7497项已存余量、后继资格与原游戏不可实现性。

全文实读三主程序5738/5844/7056B，完整正常取得并实读三个必要依赖：actual13_payment_pricing.py 6741B、trueH_own_index_pricing.py 3246B、two_real_weighted_branches.py 7501B；它们仅作related，`related-manifest.json`绑定字节，不另造主源receipt。另读成熟exact_cross_primal及fraction_solve，原件路径/身份见`reused-existing-material.json`。未声称传递闭包每一旧模块均由本批重审，也不把代码阅读加为历史成功运行。

全部六个主JSON按完整结构读取并检查：两个diagnostic全部字段、两发现文件全部7497行名/504及623个类型和primal_float/69及74个正对偶、119个定价新列/残差/附带字段、64+85个长有理质量以及全部7497个已存slack字符串。`saved-data-review.json`给每份报告完整顶层字段和所有标量叶消费数。`check_saved_data.py`只用标准库，检查原字节/源blob、atom域、seed+incoming精确类型链、全部有理质量、两表示聚合、W/O和已存slack符号；没有调用原行引擎，故不授第二次7497行系数认证。

首次新数据checker误假定119定价atom全只有七类型字段，在第一个附带旧exact_mass的atom处停止；细读发现7项保旧质量，reopt.clean明确删除。修正checker以允许、验证并在同边界删除该惰性字段后通过。该失败是新checker字段假设，非原数学错误；`validation-history.json`保准确记录，没有掩盖失败。总新数据checker调用2次（第一次停止、第二次通过）；结果明确分别记录两次调用、一次停止和一次成功，未声称首次运行即通过。

原数学程序/LP/定价/BI/全树SPE/7497行系数重构均0次。历史定价7.529秒、有理恢复39.417秒和双历史12.628秒各归原报告，当前未重跑。现有五人half、父审63点P13及144态七行只沿成熟正文复用；没有把63点负值移给64点，亦未把后续新证明13条负行误称旧A13。同批direction-next的《旧点的新活跃行分离》已完整承接53行诊断，本组已读该正文并建立准确交接链接；暂存单独校验会从其同批tree解析该前向链接，父Boss合入后是正常档内链接。

`relations-for-phase-three.json`解释两个新对象与成熟模型、747行映射、旧P13、双历史诊断、五人half及旧6750行查询补全的关系；不伪造六人证明或一份新的正式全仓图。逐源语义收据/自查/交付清单见`cleanup/workspaces/Boss4/full-actual-extension-primary/`。所有写入仅暂存tree，最终发布和登记由父Boss串行处理。

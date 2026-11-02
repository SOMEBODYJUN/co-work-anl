# 六标签首对的早期非均匀共同Q坐标证书

两份主来源是2175B `verify_group3_certificate.py`（`edfc78da9b8e2c3fdf88`）和4158B `group3_pair_exact_certificate.json`（`525c328a0f132e5096c9`），共6333B。唯一运行文件依赖4550B `group3_within_Q.json`（`83bf679b31715d121cdc`）只作必要关联输入，不在本批done。三份原字节均正常`clean show`导出，完整冻结commit/path/blob/size/SHA和角色见`source-manifest.json`。

三名提供者、六共同标签、零背景的固定反组完整形式策略有实际叶034。原程序从浮点输入恢复共同静态背景Q(01)=7/12、Q(02)=5/12，以及按六查询分组的5/5/13/5/5/5共38条非负有理IC乘子；逐6×63=378类型坐标核首对收益减两倍共同查询收益的余项非负。报告保存38条乘子和摘要，77项非零、最小0；不保存完整378余项数组。它证明凡满足该固定策略全部SPE行的非负客户质量，均有u1+u2≥2v3(0)；不是具体客户样本或任意策略证明。

原浮点输入全部字段已读，含两个背景概率、38个λ和微负`min_remainder=-5.329070518200751e-15`。HiGHS的成功状态不承担精确证明；代码对Q/λ执行`Fraction(value).limit_denominator(120)`后重新核归一、非负和378余项。t/k/status/message/seconds/scope和原浮点余项字段均不参与该原核验计算。

未发现该原入口同SHA的既有充分成功事件，本次只为这组具体坐标做一次原CLI执行。新空目录只放未改原PY和唯一输入，期待证书在执行前不存在；使用隔离Python并保留assert。`runs/original-entry-001/`保真实stdout、stderr、自动生成的完整report和execution事件。exit0、stderr空，约0.075358秒；新4158B报告与冻结主源全JSON及字节相同，SHA为`13e7155aedc408fcbc9e708306dc84d2672d936be9c99296310e023b81c0f0f4`，源码和输入前后SHA不变。

复验时将`original/verify_group3_certificate.py`与`original/group3_within_Q.json`复制到另一个新空目录，执行`python3 -I <副本路径>/verify_group3_certificate.py`，再与保存的完整原证书比较。原脚本无main guard、无参数解析，import亦执行，并会覆盖脚本同目录的同名证书；不要在保存冻结报告的`original/`中运行。stdout省略38条lambda，完整数据是自动生成的JSON。

此后没有再调用原入口，没有LP、搜索或新独立数学checker。当前任意逐客户非负背景的等权Q/单位Γ证明已经在[正式审查](../../../state/审查/反组六标签全背景首对支付的原多项式核验--审查.md)自足保存，原1134多项式审计的成功记录本次直接复用。它与本零背景非均匀Q有不同坐标，不能把378和1134合成同一程序或把这38乘子自动推广至任意背景。此包不新建重复定理，不认证一般成对安全桥、恰六人half、最小性、外部审稿或全球新颖性。

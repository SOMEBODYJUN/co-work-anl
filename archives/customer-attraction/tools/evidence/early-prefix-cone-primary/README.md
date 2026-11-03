# 早期前缀完整锥与十二客户标量点的证据

四个Boss2主源由`python3 work.py clean show ID --out …`正常导出，未手工读凭据，未改源分支。四文件935501B原字节在`original/`，逐源size、SHA-256、blob及两个冻结提交见[source-manifest.json](source-manifest.json)。相关依赖不是本批新增主源，不额外done。

正式数学为[固定锥效率界](../../../state/计算/早期前缀恒题与末位切换策略的五人精确锥界--计算.md)及[五人标量桥障碍](../../../state/障碍/早期前缀五人末位标量桥的十二客户障碍--障碍.md)。两py全文阅读；两JSON按全部字段、全部动作、所有127重数、21目标及全部稀疏乘子完整解析核验，不以摘要代读。

`earlyA_efficiency.py`调用原`StrategyCone.optimize`及`exact_export`；前者的`certified`只保证精确原始点，后者仅最优对偶通过时输出乘子。本JSON全部21目标均有最优对偶。`earlyA_scalar.py`只恢复精确原始点，没有标量最优对偶。两个生成器的实际历史argv/时间/环境未保存，本次不倒填。

已实读复用依赖：`../strategy-cones/original/tests/audits/customer_attraction_strategy_lp.py`中收益行、全历史键集、真实终局构造、有理行排序去重、原始恢复、整数克隆与直接核验；同目录`cone_attack_credible_variants.py`中`exact_export`和`verify`。已有正式[实现证据合同](../../../state/计算/固定策略锥精确证书与重放--计算.md)的旧350/348及两可信锥重放不重跑，不冒称这21点原已在那一批验证。

新`check_early_prefix.py`只用标准库，从收益定义重建整个策略，按完整有理行排序以解释原对偶行号；逐点显式保全部有序历史。准确检查结果在[fixed-input-check.json](fixed-input-check.json)：2801节点、19607含self比较/点、1302不同非零IC行；21份效率原始/最优对偶及1份标量点通过，22点431354比较。固定策略最大OPT/W9/5。标量整数点W=OPT12、D8/5、gap12/5、归一化1/5，没有保存标量最优对偶。

唯一新数学运行：在结果clone根运行`python3 archives/customer-attraction/tools/evidence/early-prefix-cone-primary/check_early_prefix.py`，exit0。未运行原生成器、LP、随机采样或旧成熟证据。此为读过源后的独立定义级实现；不是盲审、外部同行审查或原main重放。新核验自身按源SHA固定，不会改写`original/`。

同覆盖标签的处理已在正文说明：效率达到点0/5/6同覆盖，商为五个不同主题；标量点5/6同覆盖，商为六个不同主题。新JSON的`distinct_label_coverages`按非零类型支持核集合身份；原7标签完整动作表保留，无损商的IC论证在正文，不将7标签称7个不同集合。

当前只写本组独立新增文件，未改共享入口、未Git、未公屏、未claim/done。父Boss串行checkpoint后再按逐源receipt草稿处置；本地文件存在不是已推送声明。

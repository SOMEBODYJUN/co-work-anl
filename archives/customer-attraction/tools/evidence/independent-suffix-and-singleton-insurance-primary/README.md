# 独立suffix递推与单点资源保险诊断的原件

正式对象：[双副本全续局递推与单点资源保险诊断](../../../state/程序/双副本全续局递推与单点资源保险诊断--程序.md)。本目录保存三件主来源共6589B；两份程序功能不同，不能合计成同一个诊断样本域。

[source-manifest](source-manifest.json)逐件绑定冻结commit/path/blob/size/SHA256及原样保留路径。三件全文实读，原字节未改；[semantic-units](semantic-units.json)逐项交代所有语义单元的正文去向。

|源ID|字节|内容与合同|
|---|---:|---|
|1d6c3bb347980f614e11|2352|[coupled_suffix_frontier.py](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/coupled_suffix_frontier.py)：三人不交资源块、精确凸包、逐根低菜单M_cv与高3d−2W目标、唯一离散网格，两行Python repr stdout，无报告文件|
|499bf4a4c4a19b9560e0|3692|[review_product_transfer.py](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/review_product_transfer.py)：十单位客户和91节点策略重放、819含自身IC、不依赖policy的强制BB全可信suffix集合递推、四点LP解析数值核验，无main guard|
|4460c37d26ffeb1317f0|545|[review_product_transfer_exact.json](original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/independent_attack/review_product_transfer_exact.json)：完整12字段有限报告，无OPT/逐IC账本字段|

## 唯一依赖与已成熟证据复用

独立review入口唯一读取[作者原完整策略证书](../source-reset-two-original-audits/original/research/workspaces/customer-attraction/R-868a6ab8c81345f28335d75046b756b0/dynamic_matching/product_transfer_certificate.json)，SHA256为`9c47a8ae640baa0aa5d47a0f1e1a3ac0c9551c368c6913df7872ebb9d43d8fea`。本次全文读取四顶层和全部91条policy及十客户，依赖身份见[dependency-binding](dependency-binding.json)；证书不在本三源的主来源处置内。

同一证书及4/16/11末位BR/FILTER的[成熟source_reset原审计](../source-reset-two-original-audits/README.md)已交付完整固定重放。本次直接复用其字节和事件，没有再次运行该入口。新读的独立review实现另从强制BB递推全部有序suffix叶，算法与既有过滤实现不同；同一游戏仍只是一个十客户见证，不是新发现或新盲审。

## 当前执行事件与冻结输出分开

仅把未改`review_product_transfer.py`和上述证书复制到clone外隔离目录，保持`independent_attack`与`dynamic_matching`相邻。用Python3.12.14的`-I -B`原入口恰执行一次，断言未被`-O`关闭，退出0、stderr为空。

- [新生成报告](current-replay/review-product-transfer-generated.json)545B。
- [新stdout](current-replay/review-product-transfer-stdout.json)545B，是同一完整报告。
- [新stderr](current-replay/review-product-transfer-stderr.txt)0B。
- 三者的身份、真实argv/cwd/开始结束时间、源代码与输入SHA均见[execution](current-replay/execution.json)。新文件和stdout逐字节等于冻结报告，未覆盖原件。

所得91节点/819含自身比较与原policy完整一致，actual `CC,AA,BB`收益`4,3,3`、W10；根强制BB的最低可信L为5/2，单组件L为3/2、凸化值5/4。程序没有计算OPT或一般m舍入；W=OPT10由已知输入的全覆盖直接给出。没有half或SM反例。

`coupled_suffix_frontier.py`本次原入口0次、solve0次；没有另作数值网格或扩样。原MD仅报告未产生见证，未给stdout、完成计数或best值，本目录不捏造那些数据。正文保全其实际网格k=3/4/5、非降weights1..14且max≤3min+5、精确菜单和gain目标，以及M_cv不能直接冒有限产品真根floor的边界。阴性报告不作普遍保险3倍停界或六人half结论。

## 比较、关系与交付检查

[comparison-bindings](comparison-bindings.json)绑定实际全文比较的15份现存材料，包括全m转移、恰两尾FILTER、原独审scope、有效保险幅度、同质停界、原证书和成熟source_reset源码/完整报告/执行事件。先前MD批“未读代码/未跑”的声明保为准确历史，本次才增加这三件实读和一个原入口事件。

[relation-review](relation-review.json)逐条区分有限检查、不同实现比较、条件方法实现、阅读范围扩展和未得一般结果；不是阶段三正式超图。[source-dispositions](source-dispositions.json)是逐源完整处置草稿，正文及证据需由父Boss串行审核、checkpoint核远端后才可done；本目录不声称本地文件已推送。

[publication-check.py](publication-check.py)只核源字节、12字段、输出等同性、依赖/比较SHA、处置目标和链接，不运行原入口或证明数学。[publication-check.json](publication-check.json)记录本次结构检查；不能用它代替阅读/数学判断。将本目录连同正式对象放入结果树后，可用`python3 publication-check.py --repo <结果仓库根>`复查；只读。

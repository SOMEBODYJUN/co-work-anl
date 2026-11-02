# 指定最优私有化的有序历史独立审计

本包承接`R-f81c243529cf49a0a454fba6708cf80f/branch_transport/`两源，8638B标准库独立脚本和4271B完整冻结报告。完整冻结提交、原路径、源ID、blob、SHA256、大小及副本位置见[source-manifest.json](source-manifest.json)。两冻结来源同字节。原件不改；相同字节此前已作为[boss5可信攻击证据包](../boss5-credible-primary/README.md)的related比较材料保存，但没有包含在那一批八源清单。本次补足这两份来源的程序资源身份与逐源处置。

正式对象为[指定最优私有化的有序历史独立审计](../../../state/程序/指定最优私有化的有序历史独立审计--程序.md)，对应已有[固定最优私有化反例](../../../state/反例/固定最优遗漏私有化的完整可信性分离--反例.md)。后者原已全文比较这两源；本次不重复其数学对象，也不修改原反例正文。

原脚本逐重数展开36个单位客户，以完整有序历史为缓存键，精确穷尽旧、新与有利改造的全部SPE可实现叶；不导入发现者程序或规范求解器。原报告保存旧43决策节点258项含自身比较、48可实现有序路径/最低W34，新43决策节点/259总状态、六个Y排列/全部W36、六根分支及Y0末位六行表，并核全X最优比较仍保原有序z。完整数据保在原报告，不以摘要替代。

模型及量词保持：固定全Y最优比较后owner唯一，全部新SPE福利升至36，因此反固定C的W不增合同。存在一个有利全X最优比较的合同没有被反驳；E-defect仍未证。实例是三人、不是六人half反例。单位重数、全部有序历史、离轨平局及允许重选子树均承重。

原输入复用此前完整保存的[36客户JSON](../boss5-credible-primary/related/examples/customer_attraction/aggregate_theta_failure.json)，哈希及具体依赖路径列[dependency.json](dependency.json)。原程序寻找祖先首个`AGENTS.md`作为根，再读`examples/customer_attraction/aggregate_theta_failure.json`；证据副本所在目录不恢复这个旧根布局。复现应另建隔离临时目录、恢复输入路径和根标识、复制原脚本再执行。脚本将报告写到自身目录，不应在冻结副本位置覆盖原报告。

本轮逐个`work.py clean show`读取全部两源并与旧related副本逐字节比较，完整阅读原自审、反例、存在最优稿、模型、规范BI及输入。执行仅限SHA/大小、JSON和链接静态核查，数学审计、BI、LP和随机搜索的新运行次数均为0；沿用已保存精确报告，不创造新的独立运行或外审身份。来源和当前程序资源的关系见[relation-review.json](relation-review.json)；正式超图留第三阶段。

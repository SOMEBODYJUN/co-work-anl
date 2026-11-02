# 等单独收益两人子类与子集枢轴原审计

本目录保存R-75的child README及两个原程序的完整冻结字节、两次真实原入口运行和逐源比较，不保留临时下载工作树。实际导出/执行发生在clone外run-iid，程序无改动、assert开启；全部三个文件的字节数和SHA256已与cleanup/inventory.jsonl核对，两个冻结来源定位均保在[source-manifest.json](source-manifest.json)。

## 数学正文和本次增量

- [等单独收益两人首位引理](../../../state/引理/等单独收益目录的两人首位与任意iid人数比较--引理.md)：原README独有的全主题等f假设、全局最小交叠证明、任意n≥2与任意q的iid删除耦合、一人边界。它不是两个不等f程序输入的有限外推。
- [组合计数与逐客户程序合同](../../../state/程序/子集枢轴两人族的组合计数与逐客户有理审计--程序.md)：逐函数/断言、八组输入、真实输出和量词边界。
- [既有hub无限族](../../../state/反例/支持外枢轴修复与静态查询平均的两人分离族--反例.md)：一般区间、完整两人历史及262客户θ₂桥反例已正确自足保全，本批复用。旧正文称本批未读/执行原脚本是此前批次的历史说明；本次真正增加的执行另存于此。

## 文件、输入和运行

- [原README](original/README.md)、[原check_family](original/check_family.py)、[原check_hub](original/check_hub.py)原样保存。
- [真实事件](replay/execution.json)记录Python版本、argv/cwd、开始结束时间、exit、源与stdout指纹。两个原入口各1次，均exit0、stderr空；新增数学实现0、LP/BI/SPE solver0、随机0。
- [family stdout](replay/check_family.py.stdout.txt)含8行：262客户单例及偶m8…20的七个整数复制族；[hub stdout](replay/check_hub.py.stdout.txt)只含262客户单例。

family用组合计数代表完整两人历史的三种行动类别，不显式展开最大4249388个客户，也不穷举所有完整SPE。hub逐262个客户核全部辅助三人iid查询和静态theta2，只显式核H后的完整最佳回复集合及其根保证；其它首动作后的完整策略证明复用已有解析数学。

原脚本单独使用Python标准库，直接运行对应.py即可；必须保持assert开启。本次没有读取发现LP、求解七客户银行的完整策略程序或展开其它人数的所有历史。一般参数族靠已存解析证明，等f子类靠新引理的普遍论证，六人half不由本运行作结。

## 实读比较、后续纠错和关系判断

[comparison-manifest.json](comparison-manifest.json)列实际全文阅读的正式对象/必要原稿及当时指纹。另全文clean show循环PNE源3d55722d798eb4bff9df，只为核README导航不混静态PNE与完整两人SPE；该相关源不在本三项done中，也未在本目录复跑其程序。

全仓精确检索等单独收益、h_min、三个child路径和原程序名后，已有hub对象涵盖反族数学，尚缺README的等f普遍正面子类及两原程序真实实现。原README的全r extra-slot OPEN属于2026-10-23状态，现在按七客户三人/较大银行完整SPE纠正；不能把银行反驳倒归hub输入，或从等f子类推广到不等f。

[relation-review.json](relation-review.json)记录本批实际关系判断：等f引理使用既有两人f/h身份而增加全目录等f条件；两程序实现/有限核查既有hub族；后续银行反例只提供一般EI的范围边界。未导入旧图或为连通造边，正式第三阶段图由整体协议处理。

逐源回执位于cleanup/workspaces/Boss6/continue-20261102/iid-receipts.json；本目录不执行claim/done/checkpoint或Git写操作。

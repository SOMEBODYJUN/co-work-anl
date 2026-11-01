# 六人不交覆盖的两份搜索记录

[自足数学正文](../../../state/计算/六人不交覆盖搜索点的随机记录与锐界实例--计算.md)保存两主源全部字段、低位mask编码、两种不同覆盖商、精确十进制尺度、58客户点的全部SPE福利43、11客户锐例6/11，以及原浮点记录/新完整策略/精确证书的分层。

主源原件：[lp_best.json](original/lp_best.json)1423B、[random_best.json](original/random_best.json)1217B。原数组都含mask0共128项；原LP三项负零完整保留。完整冻结提交、blob、SHA和已读依赖在[source-manifest.json](source-manifest.json)。

新增独立数学入口只有一次：[audit_points.py](audit_points.py)展开两点58/11名单位客户，独立按均分定义计算924个终局，并对同一新捕获完整策略的19,608个历史逐点核137,256项IC。0原helper、0BI、0LP、0随机样本；外层约1.212秒、exit0。该脚本从原LP字面小数统一除公共单位a得到整数11点；不把二进制float直接喂Fraction双参数，也不默认为原数值输出就是归一化精确点。

|证据|含义|
|---|---|
|[point-audit.json](point-audit.json)|原字段、输入指纹、精确恢复尺度、两点覆盖商、完整IC余量分布与静态PNE全集|
|[exact-details.json.gz](exact-details.json.gz)|两点各924完整终局表，以及每个历史的动作、真实终局、60倍整数收益和七项IC余量|
|[lp-integer-point.json](lp-integer-point.json)|新精确整数化点，保全部128权与精确统一倍率|
|[execution.json](execution.json)、[stdout.txt](stdout.txt)、[stderr.txt](stderr.txt)|真实一次独立运行记录，不是旧作者执行|
|[review-record.json](review-record.json)|全仓比较和共享证据绑定；明确当前读取与未重复执行范围|
|[check_package.py](check_package.py)、[self-check.json](self-check.json)|静态语法、来源指纹、全部数据结构与实链接检查，不重算数学|

共享唯一原入口由[固定策略LP程序](../../../state/程序/六人七主题固定完整策略的福利比线性规划程序--程序.md)保存：一次带只读profile的原main含1 solve及7 LP，原1423B输出逐字重现。它新保留[完整σ](../r70-strategy-lp-program/replay/complete-strategy.json)，本包两点核验绑定其SHA；该文件不在两原数据里。

另一次共享[精确键/七对偶核](../r70-strategy-lp-program/exact-cone-audit.json)不重复本包点IC：它重建3048×127系数和889个对偶余项，给同一σ全部非负重数锥的6/11下界。本包11点取等，二者合起来认证这个固定锥的最小值；不外推全部完整策略。其它五omit分支只保存3/5精确下界，不声称已恢复它们各自的原始最优点。

正常接续读取现有报告即可，不为封包重跑。若因新修改需要重新检查，必须用新的输出目录，并保留新的事件；调用合同为：

    python -B audit_points.py --random original/random_best.json --lp original/lp_best.json --strategy ../r70-strategy-lp-program/replay/complete-strategy.json --output-dir NEW_DIRECTORY

原数学事件使用仓外绝对路径，execution保其原argv；正式目录复制是字节相同的保全，不伪装为又一次执行。检查脚本拒绝覆盖已有point-audit.json。已有不交锐例和覆盖商原测试均未在本包重复运行。

# 0123两步联合搜索主源的精确诊断

自足对象见[全兴趣四异标签停点与去除超时](../../../state/计算/全兴趣两步联合搜索的四异标签停点与去除超时--计算.md)。本包新增核验两个0123主源；旧joint-pair-policy-cone包把它们列为related且数学执行数为零，该旧事件身份不改。

|主源ID|复用原件|字节|SHA-256|
|---|---|---:|---|
|9a9073c94bd99b05119e|[joint_0123_all.json](../joint-pair-policy-cone/related/joint_0123_all.json)|34920|e4678d8d37f3c5a65462c97742d50c7ef897e86b63c3c0005bae693a292bcce4|
|243d456afe321b1c9d05|[joint_0123_all_strip.json](../joint-pair-policy-cone/related/joint_0123_all_strip.json)|843|4a97efdb5e1e553c8181cbf707210affedb32c1cc0113042f08bff519a7a709e|

两件均核对Boss7本轮另行clean show导出与inventory的SHA/blob及两个冻结提交定位，原件全文读，原拼写不改、不重复复制。实际数学和源身份在[source-manifest.json](source-manifest.json)。[原主程序](../joint-pair-policy-cone/original/pair_joint.py)及三件实际导入依赖也全文读，复用原字节；未运行其中任何函数。

[audit_0123.py](audit_0123.py)是本次新写的标准库定义级核，不导原程序、不建MILP、不优化、不修改质量/分布。实际只运行一次，记录在[execution.json](execution.json)，stdout/stderr原样保存。两种输入解释各1554条真实有序IC全部零，0负质量；所有静态背景纯收益恒为λ/4，原p/Q精确和非1，形式D为微正，合法分布下PAIR为零。普通点违反当前Σw=1与w63=0搜索约束；这不等于它不是非负质量标签游戏SPE。strip仅时间限制、未保存候选。

[exact-audit.json](exact/exact-audit.json)保全部字段名、原质量token、完整strip、两解释分数及模型维数；[完整账](exact/full-history-ledger.json.gz)含所有3108条比较及两套根/尾静态收益。压缩SHA为07c70ff447e7a44bdc1e6a9d30bed134a833a5ca3aa2119a8ee4f8a061449935，解压SHA为b1ae0547a35c1ffa5982b9bcb64f6dee0ab36df63503bded350b4c3947fffe12。

内部独立只读复核另有两次短脚本，[原命令与stdout](independent-review.json)保真实执行身份和记录缺失，不冒充完整主核、原MILP或历史重放。全批事件数是一主核加两短复核，均0LP/MILP，0012成熟数学核验不重跑。静态交付自查见[self_check.py](self_check.py)及[self-check.json](self-check.json)，不再计算IC或背景。

没有原argv、当时源码版本及完整控制变量；当前源码的全兴趣零界与普通表有近1冲突，不能将猜测的旧版本写成历史事实。四人有限计数策略记录不解决PAIR或六人half。需要未来另开核验时，给`audit_0123.py`指定新的不存在输出目录并保新的事件；本批不要求重跑已保存检查。

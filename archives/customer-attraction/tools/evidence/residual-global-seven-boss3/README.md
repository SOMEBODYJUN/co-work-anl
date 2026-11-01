# R642残余七源：原发现、完整策略、精确证书与随机合同

正式正文：

- [两级线性探针与根门槛随机检查](../../../state/程序/残余组合的两级线性探针与根门槛随机检查--程序.md)：七源逐接口、完整／必要行、正规化及未运行随机脚本。
- [27客户原版本与精确复核](../../../state/计算/二十七客户残余发现点的原完整回复与精确复核--计算.md)：原报告字节绑定、19客松弛点不可补全、9乘子64格及父方对称闭式、一般二人残余上界。

## 原件及相关依赖

`original/`保存七主源8182B，`source-manifest.json`给ID、size/SHA256/Git blob及双冻结来源commit。原两JSON不改格式、浮点或无末LF的原行为。

`dependency/`是已审规范包四文件同SHA副本，只用于两个随机脚本的API／原目录依赖保全，本批没有导入或运行；`dependency-manifest.json`不额外primary/done。实际执行的三数值源没有规范包依赖。`related-context-manifest.json`保完整相关正文、原2941B主稿及旧批已读定理的比较身份。

## 本轮三个原入口，未扩大搜索

`replay_residual_sources.py`为实际执行过的包装器，全部source输入／runtime／输出都在clone外：

1. 原`audit_residual_obstruction.py` CLI一次，0.031秒，exit0，生成326B与冻结JSON逐字节一致。原stdout是排序紧凑格式，不拿它冒同一pretty字节。
2. 原`residual_two_full.py` CLI一次，2.484秒，216次LP调用，生成1423B与冻结JSON逐字节一致。只固定rA=B、rT=Q、rS=R的216图，无新增回复搜索或精确全图最优对偶。
3. 原`residual_two_lp.py`在`runpy`下顶层执行一次，0.693秒、仅1个LP。读取同一次的结果对象，随后Fraction验证原始点、22必要行、归一化、9λ和全部64对偶余项，精确最优9/10。没有再调用solver；原源码本身不作这套后核。原partial没有冻结报告可匹配，本轮stdout和`partial-lp-exact-postcheck.json`是新证据。

总217次原LP，两个随机脚本0导入／0执行，不为1000和5000预算追加阴性。三个原入口各自stdout/stderr、新生成两JSON、包装器stdout/stderr全保，所有stderr为空。版本Python3.12.14、NumPy2.3.5、SciPy1.17.0。

`source-replay-events.json`保存包装器原产生的事件；`replay-events.json`另以明确aggregation字段追加下述独立父方事件，未假称由原包装器同时生成。报告的原历史运行命令／环境仍缺，当前byteexact复现不倒填旧event。

## 父方本轮独立精确复核

`parent-review/`三文件由父方提供，逐字节复制，另附origin/SHA manifest：标准库脚本、完整64格结果、实际event。它读取本次原证书SHA后从定义另建22行，不导probe、LP或BI；一次0.00856秒核原9乘子系数、T/S与Q/R交换平均及10乘子解析闭式，全一致。这里没有再次执行它，也没有把当前父审冒原历史审查或外审。

原证书给W−9R/10非负；父方对称闭式只需a及n=t+s、e=q+r便自足证明。由于所有真实二人SPE能从同一完整策略抽A,B,T,S,Q,R，全部必要行都真，64位独立cube的非负性覆盖别名／重复的相关子集，因此得一般9R2(C)≤10W。9/10只是22必要系统的最优：19客等号点根改B/Q/R后所有末位BR都提高根收益，不能作真实SPE锐性或更小残余反例。

`self-check.json`仅核最后交付的指纹、原报告byteexact、receipt和链接、父方certificate/script/result SHA绑定，不调用新的数学程序。

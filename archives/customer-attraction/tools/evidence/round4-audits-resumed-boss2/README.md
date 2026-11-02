# 五人557行原双证书审计恢复

正文：[原审计恢复与认证范围](../../../state/审查/五人五百五十七行双证书的原审计恢复与认证范围--审查.md)。

本包完整处置五个冻结主源：`full_pricing_audit.py/json`、`audit_full_primal.py/json`、`audit_optimum557_primal.json`。原字节在 `original/`，完整来源ID、两个冻结提交、路径、大小及SHA-256见 [source-manifest.json](source-manifest.json)。根程序正常 `clean show` 导出后逐份核同，没有改写原程序或报告。

## 两次实际运行

1. 原独立 `full_pricing_audit.py` 一次：51正整数乘子，三族完整直方图和旧菜单四角，6144条件全部非负，84零条件；输出与冻结报告仅 `seconds` 不同。
2. 原父审 `audit_full_primal.py --source exact_optimum_primal_overlap1.json` 一次：67原子、437复用定义行加120字面新增行，557个精确总slack与证书逐值相等，78零行；822字节输出与冻结报告逐字节相同。

完整stdout/stderr和JSON在 [replay/](replay/)，[execution.json](replay/execution.json)保实际argv、返回码、两种耗时范围、输出哈希与字段差异。[input-bindings.json](replay/input-bindings.json)列六个准确运行文件。空stderr是真实零字节文件。

旧60点已有成功557行核验，本批仅全读原报告并核对其输入指纹及公共数学字段，见 [mature-60-reuse.json](mature-60-reuse.json)；不重跑旧60、旧437完整CLI、发现LP、列生成或SPE搜索。

## 必要依赖与复现

原51乘子和67点位于相邻 `round4-pricing-resumed-boss2/original/`；旧437评价器复用 `five-player-indexed/tests/audits/customer_attraction_five_indexed.py`。项目根定位只检查原 `customer_attraction/__init__.py` 是否存在，复用 `catalog-boundaries-original-boss3/dependencies/customer_attraction/__init__.py` 的准确691字节，不导入模型包。

在仓库根使用Python及NumPy运行：

```sh
python archives/customer-attraction/tools/evidence/round4-audits-resumed-boss2/replay_recovered_audits.py --output /tmp/recovered-557-audits-new-run
```

输出目录必须尚不存在。启动器只把上述准确原件复制到新临时树以恢复相对路径，按顺序执行两个原入口；不访问网络、不修改冻结数据、不在原件目录覆盖报告。源程序里的父审会AST加载旧评价器的定义前缀，不执行旧证书的模块顶层循环。

双证书确定的是指定557行非负质量松弛的精确最优值约2.04215549。数学上的真实SPE必要性由原行推导及正式正文承担；有理松弛点没有被认证为完整共同目录SPE，六人半覆盖未因此解决。

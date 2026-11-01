# 末覆盖包含与残余原审计恢复

四主来源的原字节在original/<source-id>/；[source-manifest.json](source-manifest.json)保存双冻结定位、blob、SHA和大小。两个原MD已由旧批次主处置，本次全文比较后同字节保于related-notes，并在[related-context-manifest.json](related-context-manifest.json)标明只作关联材料。cascade源码关联全文读取，但不在本批主来源done中。

正文为[末覆盖重数与残余判据的原审计恢复](../../../state/计算/末覆盖重数与残余判据的原审计恢复--计算.md)。全参数证明、末节点包含极大性、原两参数松弛与后来gamma增量分开；原JSON有限PASS不代替这些证明。

## 实际运行

本次两个未经修改的原入口各一次，1.871049667秒和1.609925316秒，exit0、stderr0，stdout与802B/146B原JSON全部字节一致。[replay/events.json](replay/events.json)包含具体时间、版本和SHA，stdout/stderr及解析副本同目录保全。没有随机攻击、LP/MIP或第三次BI。报告11375案例不含内层t循环乘数；37820含g>k代数输入；两报告的174来自相同六游戏，不能相加为348条不同路径。

四个canonical模块来自既有全文实读的冻结同SHA材料。cascade的完整原件与[dependency-manifest.json](dependency-manifest.json)内runtime_path组成可重建运行树。报告自身没有原历史时间、环境或源码SHA，本次事件不倒填历史。

## 再现方法

安装可用的Python、NumPy、SciPy后，以本目录为当前目录，指定两个尚不存在的路径：

```sh
python replay_original_audits.py --evidence . --runtime /absolute/new-runtime --output /absolute/new-output
```

包装器核原件/依赖SHA，重建parents[5]及同目录import要求，执行两个原入口并保存实际日志；任一失败或字节差异即停止，不自动重试或改写原件。残余脚本没有main guard，直接import也会执行，故不要为“只读检查”导入它。

[reading-review.json](reading-review.json)仅是静态源循环计数和旧报告逐字段比较，含六个seed的精确客户类型、由全gap覆盖证明的OPT以及从已复现ratio解析得到的最小覆盖；它未额外调用solver。提供六条seed不是追加六次发现实验。

# R105独立静态指派JSON全字段核验

本目录保留源 `ec52aba43557844bf416` 的完整247215字节原JSON及一个新标准库核验器。数学合同、量词和历史身份边界见[计算对象](../../../state/计算/静态最优指派独立JSON的全字段精确核验--计算.md)。原审计程序和说明由同批其他对象处理，不在本目录重复保存。

- `original/independent_assignment_audit.json`：冻结原件，未改；包含全部216覆盖、258真实激励行、18静态收益及36指派。
- `verify_frozen_json.py`：新写的定义级核验，不导入/执行原审计；逐名客户Fraction和压缩六倍整数双路核216终局，反向构造全部43历史完成叶，再重建并递归比较全部源JSON。
- `verification-report.json`：新核验结果和全部统计；历史自述仅保全，不能计算认证作者的阅读过程。
- `source-manifest.json`：冻结定位、SHA及现有完整依赖路径；依赖不再复制或重复done。
- `run-manifest.json`：本次检查的真实命令、Python、退出、时长及输出指纹。

从结果仓库根：

```bash
python archives/customer-attraction/tools/evidence/r105-json/verify_frozen_json.py --report archives/customer-attraction/tools/evidence/r105-json/verification-report.json
```

这只覆写可再生的小核验报告，不写原JSON、输入或政策。原程序的历史旧绝对路径不被访问；实际输入复用相邻 `dynamic-exchange/original/` 的两份同SHA原件。脚本所有实质检查用显式异常，而非依赖可被`-O`关闭的assert。

# 五份贪心输入与原快速入口

正式资源合同见[五份贪心输入与轻量全盒回归的精确合同](../../../archives/facility-games/subarchives/common-many/state/计算/五份贪心输入与轻量全盒回归的精确合同--计算.md)。

`original/`保存本批五个JSON、原`tests/test_greedy_box_global.py`及八个已保存的真实执行依赖。14原文件共48762字节；[source-manifest.json](source-manifest.json)给六主源/依赖角色、完整双冻结提交来源、ID、长度、SHA。依赖不另认领、不重复done。

[replay.py](replay.py)在新目录复制原相对树，先核指纹，按地点原序做五输入的定义级贪心重放，并对等权local-NE输入枚举全部四赋值/全原跨站动作/无约束Ψ，随后以runpy执行原快速入口真实`__main__`一次，取它已有的report变量保存。它没有二次调用run、没有修改原字节、不需Git/网络；普通Python运行，不用`-O`。

```sh
python3 tools/evidence/multi-facility-example-assets/replay.py --run-dir /absolute/new-run-directory
```

已成功一次，勿为保存再次运行。`replay/`保实际命令、外部cwd/env、Python3.12.14、耗时、返回码、源码和输出SHA，完整quick report、一行原PASS stdout、空stderr、五输入及local四赋值定义检查。`source/`外部运行副本可由original精确重建，不重复保存第三份。

本次快速入口random_cases=12，450证书、1476实际偏离、4301布局求值(默认2523)，最大倍率1701/1000；与旧默认90例审计重叠，不能累加当独立覆盖。原source audit包含CLI子进程，临时输出落外部运行目录并自动清理。生产代码和assert均保留。

原cap/potential/repair审计、等权流5242例审计和默认90例全局审计均未重跑。仅五输入的规范贪心重放及local四赋值是本次新定义级检查；不是对其余三个反例重新穷举。全部数学责任与后续用途见正式正文。

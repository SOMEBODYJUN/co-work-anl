# R-18 任意对称势菜单候选探针

源 ID：`1877de0b5a329805604d`，冻结文件为 `next_representation/probe_potential_menu.py`，SHA-256 `14abbae1d6e806b696935c08c0d5feb958b5d833aa847dc3fac774dee64f4664`。

脚本在任意整数势函数 `Phi`（大小 `m-1` 与 `m` 的状态分别赋值）上递归重建完整历史，保留每个节点的 SPE 不等式；线性规划只寻找可能优于均值的菜单混合，候选查询再逐菜单精确核验。模型明确不是共同目录 CAG。

复跑：

```sh
python3 probe_potential_menu.py --players 3 --topics 3 --trials 200 --seed 18311 --report-every 50
python3 probe_potential_menu.py --players 3 --topics 3 --trials 1000 --seed 18311 --report-every 200
```

两次均 `found: false`；1000 次的菜单规模摘要为 2、2、3、3、3。该结果是固定参数、固定随机种子的有限探针，不能推出任意势函数或 CAG 的菜单半界。

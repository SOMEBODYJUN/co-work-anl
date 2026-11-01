# R4最大单例阈值测试器的原字节重放

本目录属于源 `5649214767cb58dd540f` 的程序审查证据。正式合同见[审查对象](../../../state/审查/R4最大单例阈值测试器--审查.md)。它只复现既有三人六主题36单位客户输入的阈值分离；不包含新目录搜索、完整策略生成、独立阈值实现或一般half结论。

- `original/`：按原层级保留的八份冻结文件，全部通过 `work.py clean show ID --out PATH` 取得，未修改。四个规范Python包文件是完整导入依赖；README和旧JSON仅供比较。
- `manifest.json`：每份文件的源ID、冻结提交及路径、大小、SHA-256。
- `run/stdout.json`：未改原入口的真实4156字节输出，与旧JSON逐字节相同；(M(0)=10<M(e_0)=12)，终局集合大小20和4。
- `run/stderr.txt`：真实空stderr。
- `run/event.json`：实际命令、Python版本、退出码、时长、输出哈希及比较结果。

从结果仓库根目录重放：

```sh
python3 archives/customer-attraction/tools/evidence/R4-singleton-threshold-test/original/research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/representation/test_maximum_singleton_threshold.py
```

保持 `original/` 内的完整层级；原脚本用 `parents[5]` 定位包及输入。它只调用规范 `ExactSPESolver`；第一次分离立即返回。本例在空背景首个主题即返回，故未继续外层背景扫描。输出为终局计数集合和阈值数据，不是完整有序历史动作表证书。

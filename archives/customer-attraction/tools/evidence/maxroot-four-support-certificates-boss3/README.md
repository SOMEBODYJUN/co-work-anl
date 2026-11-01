# 最大根双复制四支持线的四份冻结来源

正式对象：[六人最大根双复制四条支持线的精确核验](../../../state/计算/六人最大根双复制四条支持线的精确核验--计算.md)。

`original/` 的 `root_copy_lp.py`、`export_root_lines.py`、`root_lines_certificate_v2.json`、`verify_root_lines.py` 全部原字节保留；两个冻结提交、源ID、字节数、blob与SHA-256在 `source-manifest.json`。

`original-verifier-replay.json` 是本轮执行原标准库验证器恰一次的真实stdout；`execution.json` 记录入口指纹、Python版本、运行次数、退出码及范围。`original-verifier-stderr.txt` 为空。四条各8192类型的最小残差0、零数2，与原精确输入报告逐字段一致。没有执行浮点发现或导出器，也没有新增独立验证实现。

从仓库根验证：

```sh
python3 archives/customer-attraction/tools/evidence/maxroot-four-support-certificates-boss3/original/verify_root_lines.py
```

仅需Python标准库，且不修改原证书。原发现器和导出器需NumPy/SciPy；导出器会重新求浮点LP，不是已有有理证书的必要验证依赖。四支持参数不是r/K假设，三个负C不能截断，普遍必要界不等于六人half。

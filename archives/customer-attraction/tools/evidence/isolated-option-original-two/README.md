# 孤立未用主题：两主来源与一次原实现重放

数学正文为[孤立未用主题的完整终局探针与万例记录](../../../state/计算/孤立未用主题的完整终局探针与万例记录--计算.md)。本目录保存两份冻结原件、五份实际比较材料、来源清单和一次重放。

- `original/isolated_option_probe.py`：4140B原代码，SHA见manifest；不修改。
- `original/isolated_option_unit_seed1301.json`：300B原报告，保原耗时。
- `comparison/`：四份正式正文及R84根README，均为相关实读，未在本批额外认领或done。
- `replay-once/`：唯一一次新原程序执行的报告、stdout、stderr、环境及逐字段比较。八确定字段同，耗时独立保存。
- `replay_original.py`：仅包装执行与原件SHA/确定字段检查，不含第二套SPE算法。

要重放，使用一个尚不存在的输出目录，例如从本证据目录运行：

```bash
python3 replay_original.py --out replay-new
```

此入口拒绝覆盖已有目录。只执行seed1301/unit/10000的冻结范围；没有weighted运行、扩样、外部服务或第三方包。原输入指纹不包含终局证书；完整算法和有限统计的证据强度见正文。上述原实现成功不能当作独立外审。

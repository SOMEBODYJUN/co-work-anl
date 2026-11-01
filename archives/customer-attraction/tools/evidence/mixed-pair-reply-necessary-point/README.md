# 混合强PAIR必要图点证据

[正式计算对象](../../../state/计算/混合强配对回复图的有理可行点--计算.md)保存全部量词、12字段与1905列合同、5043行身份、实际有限验证及后继分离。[原JSON](original/all_reply_mixed_pair_exact.json)为816556B、SHA256 `83b469f45e6017c024d1f87c614c5b1e968be94bb171ed27bb913c7119843613`，此前仓库没有同源副本，本包只保一份。

`audit_mixed_point.py`逐项解析全部元数据和列，以Fraction重新核状态/容量/地板/O/W，复用前批已认证的直接有序边数学函数，把72行代到本点。所有非weight描述符已与前批两个认证输入完整比较相同，故没有重复137160系数对照或160型恒等式。它另复用连续cut的独立数学积分器，在本点新求64+32条保存cut的全部余量，不运行发现LP。结果在[point-audit.json](point-audit.json)：72行0负4零，64与32条后继cut全负；198个Fréchet下界失败只反驳原辅助坐标的字面交叠解释，不反驳5043必要图可行性。

从仓库根可重现新点局部检查，另选输出路径：

```bash
python3 -B archives/customer-attraction/tools/evidence/mixed-pair-reply-necessary-point/audit_mixed_point.py \
  --repo "$PWD" \
  --point archives/customer-attraction/tools/evidence/mixed-pair-reply-necessary-point/original/all_reply_mixed_pair_exact.json \
  --out /tmp/mixed-point-audit.json
```

`replay_original_once.py`创建一个必须全新的隔离目录，按共享manifest核并准备37份冻结文件，再加入当前点及只找根不执行的work.py marker。仅调用未改原 `all_reply_actual_floors.py --priced --optimum --old-query-cuts --mixed-pair --verify` 一次。真实[执行事件](rerun/execution.json)、[38份准备输入](rerun/runtime-inputs.json)、[stdout](rerun/stdout.txt)和[空stderr](rerun/stderr.txt)完整保存；5043行全部精确通过，退出0，全部准备文件SHA不变。没有优化或写回原点。

如确需在新环境复现原事件，可指定**不存在的**runtime和out目录：

```bash
python3 -B archives/customer-attraction/tools/evidence/mixed-pair-reply-necessary-point/replay_original_once.py \
  --repo "$PWD" \
  --point archives/customer-attraction/tools/evidence/mixed-pair-reply-necessary-point/original/all_reply_mixed_pair_exact.json \
  --runtime /tmp/mixed-point-fresh-runtime \
  --out /tmp/mixed-point-fresh-run
```

原CLI需要共享原依赖中的NumPy/SciPy可导入，但这里不进入优化分支。当前记录使用Python3.12.14；审计器只需标准库。原全图事件、当前点的独立数学检查、前批系数认证分别计数，不互相冒名。没有完整SPE、全域half、精确最优性或历史发现迭代认证。

[manifest.json](manifest.json)列源、代码与比较资产指纹；[self-check.json](self-check.json)保存实际clone的格式、链接、receipt targets、原件及运行证据一致性检查。

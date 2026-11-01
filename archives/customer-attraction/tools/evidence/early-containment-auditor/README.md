# 双包含系数审计器的原件与复跑

完整数学及实现合同见[程序对象](../../../state/程序/两早期主题包含倒二主题的系数审计器--程序.md)，配套数据另见[报告对象](../../../state/计算/两早期包含条件的有限系数审计--计算.md)。当前状态`local-prepared`，待Boss串行推送；本包不做Git或清洗状态写入。

`original/audit_containment.py`按源3118字节保存，另四份原MD是已全文读的必要比较材料。它们各自的源ID、原路径、冻结提交和SHA见[manifest](manifest.json)。相关来源不在本代码receipt中重复处置。

从仓库根执行：

```sh
python3 archives/customer-attraction/tools/evidence/early-containment-auditor/replay_original.py
python3 archives/customer-attraction/tools/evidence/early-containment-auditor/build_manifest_and_check.py
```

复跑器以`python -I`及独立cwd执行未改原件，忽略Python环境优化设置并启用源代码断言。原件仅输出stdout、不写文件；包装器保stdout、空stderr和最终运行元数据。开发包装时普通解释器及最终隔离模式各运行一次，stdout相同；保留的最终[405字节输出](rerun/original_stdout.json)逐字节等于冻结JSON。

这是原程序的1960约化型、3360含可行交叠型和六人常数复算，不是游戏、策略或LP搜索。全局真实SPE行的语义由原证明和正式程序对象解释；局部行系数可以为负。配套报告另有独立原始会员重构，本包不重复该实现或冒领为源程序原有字段。

交付检查见[self-check](self-check.json)，实读与关系比较见[comparison](comparison.json)，最终命令和范围见[metadata](rerun/metadata.json)。

# 真实 SPE 搜索与完整历史证人

当前目标仍Q-CAG-HALF，一般命题未解决。这里的主要本轮资产是：

- `outcome_witness_dag.md`：不限制计数Markov的终局证人DAG等价性、MILP线性扩展及严格适用范围。
- `outcome_dag_milp.py`：数值候选生成，展开完整有序历史并经有理策略锥重优化、独立Fraction逐偏离核验；数值MILP上界不认证。
- `fractional_weak_m4_instance.json`、`fractional_weak_m4_certificate.json`：四人四主题17单位客户实例及85节点完整SPE。实际B,B,B,A，W16，OPT17；弱分数实际负载桥失败，非half反例。独立审查由主代理保存。
- `audit_outcome_dag.py`、`outcome_dag_audit.json`：57个正福利固定输入目标的oracle回归、31个成功证人精确核验、旧非Markov例和30组规模计数公式核对。
- `dag_search_summary.json`：本轮实际有限探索与运行边界，包含环境版本及脚本哈希。m5p7完整DAG主目标攻击在约63秒仅返回比例1的平凡合法点；不得从超时或有限样本推数学结论。保留精确残余项的新充分桥在此轮几种小根负载上没有被反驳，仍开放。

本轮有限交叉检查和DAG生成的数值记录不是一般定理证据。命题身份、严格证明与有限计算分别写明。后继继续攻击一般half以及保留精确残余项的新充分桥。

复现：

```sh
python <本目录>/audit_outcome_dag.py
python <本目录>/outcome_dag_milp.py --root 1,4,0,0,0,0,0 --portfolio 2,3,4,5,6 --seconds 50 --output <新的JSON文件>
python <本目录>/outcome_dag_milp.py --root 1,2,0,0 --query 2 --budget --seconds 20 --output <新的JSON文件>
```

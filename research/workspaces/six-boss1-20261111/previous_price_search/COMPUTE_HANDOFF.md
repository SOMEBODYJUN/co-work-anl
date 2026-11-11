# 三个固定折扣的直接 OPT6 报价计算

主代理从仓库根目录执行以下请求。代理只准备输入与 manifest，没有创建请求或启动云任务。

```sh
python work.py compute request six-boss1-previous-price-19621-theta14 --manifest research/workspaces/six-boss1-20261111/previous_price_search/computations.json --request-id C-six-boss1-prev-price-19621-t14-01 --timeout-minutes 15
python work.py compute request six-boss1-previous-price-19621-theta12 --manifest research/workspaces/six-boss1-20261111/previous_price_search/computations.json --request-id C-six-boss1-prev-price-19621-t12-01 --timeout-minutes 15
python work.py compute request six-boss1-previous-price-19621-theta34 --manifest research/workspaces/six-boss1-20261111/previous_price_search/computations.json --request-id C-six-boss1-prev-price-19621-t34-01 --timeout-minutes 15
```

每项 30 案：来源 actual1…actual5，种子 A1…A6。依赖固定为 NumPy 2.3.5、SciPy 1.17.0；现有 Actions 工作流使用 Python 3.12。单项算法超时 600 秒，job 预算 15 分钟；小试每案发现不足 1.2 秒，只有负行才需批量展开完整 448 型，通常总计数分钟内。输出分别为 `actions_theta14/`、`actions_theta12/`、`actions_theta34/`，没有共享写路径。

请求实际绑定四个文件：发现脚本、独立复核器、精确点、精确矩阵。精确点与矩阵 SHA 分别为：

```text
d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f
6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9
```

本地严格只执行两个优化案例，均已通过独立复核：

| 来源 | 当前种子 | 折扣 | 返回权精确 slack（近似） | 全 14 权锥精确下界（近似） | 独立完整 Boolean 赋值数 |
|---|---|---|---:|---:|---:|
| actual2 | A6 | 1/4 | 0.00292674754628205 | 0.00292674754628198 | 262,144 |
| actual5 | A1 | 1/2 | 0.0216872827462983 | 0 | 32,768 |

第五源的两个 middle 参数完全无效，归一化优化时固定为零。对应有效 12 权锥有严格正下界；包含无效参数的完整 14 权锥精确下界是零。两种范围在结果中分开记录。

验收文件：每项的 `summary.json`、`manifest.json`、全部逐案结果以及 `independent_audit.json`。应确认请求 30 案全部成功、独立审计通过，负行若存在已核完 16 策略、448 型、完整 Boolean 域、4,849 原列和 10,744 个辅助零系数。若 `occupation_certificate.nonseparation_certified` 为假，即使返回权非负也不能宣布该权锥无分离；精确下界值和正负状态必须一起读取。

任务返回后只对这 90 个固定来源/种子/折扣合同作结论；不扩展到未采样折扣、其它固定菜单、跨源嵌套、一般 SPE 或 six-player half。

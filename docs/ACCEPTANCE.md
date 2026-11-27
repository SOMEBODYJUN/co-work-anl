# 已完成的工程验收

本次交付：首轮Pro完整流程、后续agent增量流程、统一CLI、选定工具与原始许可、研究输入、提示词和可复现测试。正式经济裁决与完整120月家庭方案计算器由首轮流程产出。

## 实际跑过的链路

| 项目 | 实际操作与结果 | 记录 |
|---|---|---|
| 当前材料接入 | 47条证据保存为47条观测，按18个来源项、10个来源家族分组；保留原状态和所属期 | `tests/live/seed-workspace/` |
| 采集和发现 | GitHub公共搜索、Crossref论文发现、BIS原文采集实际成功；原始来源访问回执单独保留 | `tests/live/` |
| 检索复用 | 已有查询直接复用；改变统计期或过期后重新搜索；同一范围的其他查询先呈现给研究者 | `tests/test_audit.py`、`tests/test_engine.py` |
| 首轮执行 | 实际按统一CLI完成20阶段，保存输入、联合前提、计算、报告和工程HTML，复核后发布 | `tests/run_end_to_end.py` |
| 增量执行 | 新输入触发旧判断与机制失效，分别提交机制/结论提案，独立审查后合并，重算、改稿、重新发布 | 同上 |
| 两次独立clone | 首轮提交后新clone恢复；增量提交后再clone恢复，均读取clone内代码与保存输入离线重放 | `tests/live/end_to_end.json` |
| 具体改判 | 明确标为合成的家庭收入由8000改为9000，现金缺口由第7月变为第13月；参数、正文、结果同步更改 | 同上 |
| 错误拦截 | 拒审撤销旧通过；审后改文件、未审apply、未回应旧理由的反转、旧原文篡改、空阶段产物均被拦住 | `tests/test_audit.py`、`docs/INDEPENDENT_REVIEW.md` |
| 贷款核验 | 本金、利息逐期对照真实numpy-financial源码；零利率、1期、长期贷款实际执行 | `tests/fixtures/methods/results/loan.json` |
| 混频模型 | statsmodels拟合、同参数更新、预测、news实际执行；固定合成两版本的预测差与增量勾稽误差约1.73e-16 | `tests/fixtures/methods/results/nowcast.json` |
| 时序取数 | AKShare宏观端点实际取回83行，并保存原CSV、函数、时点和SHA；离线重放相同 | `tests/fixtures/methods/` |
| 部门会计与基线 | 再融资不抹去债务；负现金列缺口；扩展窗口桥接基线实际运行 | 方法结果与测试 |
| 干净依赖环境 | `python bootstrap.py --environment .venv-clean` 安装完整锁，不继承系统包；`pip check`通过 | `requirements-methods-lock.txt` |

最终统一回归：34项通过。完整首轮/增量/恢复演练实际执行63条CLI，复算一致；测试次数用于定位回归，实际演练是工作流验收依据。

## 复跑

```sh
python bootstrap.py
.venv-methods/bin/python -m unittest discover -s tests -v
.venv-methods/bin/python tests/run_end_to_end.py --output /选择的输出路径/end_to_end.json
.venv-methods/bin/python tests/run_engine_demo.py --out /选择的新空目录
```

工程演练全部明确标记合成。宏观原始输入和实际接口取数单独保存。选定工具的执行用途、借用代码/提示词和精确版本逐项见 `docs/METHODS.md`；观点研究与经济裁决由Pro及研究agent执行。

## 交付状态

本地Git检查点、完整源码ZIP及可直接clone的Git bundle已准备。公开推送被自动审批拦下，待用户明确允许将本包中的程序、提示词、上传资料和测试记录发布到公开目标 `SOMEBODYJUN/co-work-anl` 的 `work/cn-crisis` 分支。仓库外凭据不进入交付物。

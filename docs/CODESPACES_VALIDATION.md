# Codespaces账户机型与远端建模实测

执行日：2026-11-26（America/Los_Angeles）。本次使用已授权的仓库外凭据调用GitHub REST，并真实创建、连接、停止和调整一个专用测试Codespace。以下结果来自远端Codespaces执行，不是本地容器限核模拟。

## 实际可选机型

本账户对 `SOMEBODYJUN/co-work-anl`、`work/cn-crisis` 的机器查询返回HTTP 200，只返回：

| API机型名 | CPU | 内存 | 磁盘 | 实际执行 |
|---|---:|---:|---:|---|
| basicLinux32gb | 2核 | 8GB | 32GB | 成功创建、SSH连接、安装及运行 |
| standardLinux32gb | 4核 | 16GB | 32GB | 停机后调整成功，重新连接及运行 |

机型响应见 `tests/live/codespaces-machine-availability.json`。没有返回8/16/32核或GPU，本次不声称这些配置可在此账户使用。机型可选和创建成功不证明学生认证状态或剩余免费余额；本次没有读取账单余额。

## 真正执行的工作

两种机型均安装Python 3.12方法环境并运行贷款、部门会计、扩展窗口桥接、DynamicFactorMQ更新及news归因、83行真实GDP缓存重放。随后训练正则化logit与直方图梯度提升分类器。

训练负载是固定随机种子的30000行、24特征合成数据：18000行训练，6000行单独拟合校准器，最后6000行留作测试。计算预测分数、Brier、log loss和average precision。它验证训练、预测和评估接口与机器容量；不含中国事件标签，不构成中国危机模型训练或科学验收。

| 观测 | 2核远端 | 4核远端 |
|---|---:|---:|
| 进程实际可见CPU | 2 | 4 |
| 系统可见总内存 | 约7.76GiB | 约15.62GiB |
| 本次完整进程峰值RSS | 约199MiB | 约199MiB |
| 两类训练与单独校准 | 完成 | 完成 |
| 混频信息更新勾稽 | 通过 | 通过 |

原始数值见 `tests/live/codespaces-2core.json` 与 `codespaces-4core.json`。单次计时包含冷启动、导入和线程差异，不用于宣称4核必然比2核快多少；峰值内存仅属于本次负载，不是最大可处理数据规模。校准后的Brier在此夹具中没有改善，也不能因执行过校准就宣布概率有效。

## 实际发现并修复的启动问题

默认Codespaces镜像中的 `python` 为3.14.2，而系统另有3.12.3。直接用系统3.12创建虚拟环境失败，因为缺少ensurepip；失败还留下了没有pip的半成品环境。

`bootstrap.py`现在检查环境中的pip，可用宿主pip的 `--python` 功能补齐这个环境，再按锁文件安装。该修复已经在上述真实失败的2核实例重跑成功，4核保留环境后也成功运行。实现参照[pip官方说明](https://pip.pypa.io/en/stable/topics/python-option/)。仓库新增Python 3.12容器配置，使新工作区固定同一Python系列；重建状态在最终执行记录中另列。

可复现入口：

```sh
python bootstrap.py --benchmark
.venv-methods/bin/python tools/benchmark_runtime.py \
  --rows 30000 --features 24 --threads 2 \
  --output work/runtime-benchmark.json
```

## 学生权益与选型

[GitHub学生官方说明](https://docs.github.com/en/education/about-github-education/github-education-for-students/about-github-education-for-students)规定，认证学生个人账户享有每月180核小时，存储额度等同Pro；[计费说明](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)列出Pro的20GB-month。180核小时理论上对应2核90小时或4核45小时；其他实例的使用共同消耗额度。存储是按时间计量的用量，不是把32GB机器磁盘缩为20GB。

当前结果支持先用2核/8GB建设真实面板、简单基线、表格机器学习和部门压力测试。需要多实验并行或更大内存时再选已验证的4核/16GB。现阶段不需要额外机器学习平台；长时间批处理、大规模文本模型或GPU训练出现明确负载时再配置外部计算。观点与原文的学习继续由研究者执行，扩容CPU不代替该工作。

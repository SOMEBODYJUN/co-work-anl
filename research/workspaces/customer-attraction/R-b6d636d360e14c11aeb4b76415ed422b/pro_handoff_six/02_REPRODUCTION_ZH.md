# 可选复现说明

解压后，在包含本文件的 `Q-CAG-HALF-6/` 目录运行。核验不是开始研究的前置步骤。

```sh
python verify_manifest.py
python run_checks.py
```

环境：Python 3.10+、NumPy、SciPy（完整依赖列于 `requirements.txt`）。五人核验需要 NumPy；七客户反例和后缀包络只需标准库；最新六人必要条件核验会导入旧行生成器的 NumPy/SciPy。运行入口不调用 LP 优化器、不访问网络、不使用凭据。

`run_checks.py` 将包内 `source/` 复制到临时目录，逐项运行以下入口，避免改动冻结源文件：

1. 五人完整局部组件核验；
2. 五人完整主证书核验；
3. 七客户零 regret 正 reset 的独立完整历史构造与 IC 核验；
4. 六人全部后缀势包络及实际盈利偏离核验；
5. 六人 27 原子共同回复见证及指定旧行系统核验；
6. 同一见证的 336 族最大根图扩张核验。

可以用 `python run_checks.py --only half5-local zero-reset` 只运行指定项；可选名为 `half5-local`、`half5-main`、`zero-reset`、`suffix-envelope`、`joint-atoms`、`root-extension`。`--output 路径.json` 保存本次报告。

所有判号按原程序的 Fraction 或整数计算；部分旧根图生成阶段使用 NumPy 构表再作有界整数缩放，保留原有实现与审查范围。新启动器只负责复现，不是第二份独立数学实现。退出码为零表示该项程序完成其明确检查，不把必要条件可行见证提升为 SPE，也不提升六人状态。

源树根部的 `source/work.py` 仅是供旧程序定位目录的无功能占位文件，没有仓库恢复、认证、网络或通信功能。

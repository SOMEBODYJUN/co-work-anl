# 共享负载发现四源的原件与当前复现

正式对象：[共享负载旧实例与保险协方差压力](../../../state/计算/共享负载旧实例与保险协方差压力--计算.md)。这里保留四份primary全字节，另存三份related输入/报告；related没有额外办理done。完整冻结提交、源ID、sha256和当前捕获路径见`source-manifest.json`。

`original/`的四文件来自逐项`work.py clean show ID --out`，读取与导出分开完成，没有改原件。`related/old36-input.json`为18客户类型的36单位客户输入，`old36-strategy.json`含全部43节点，`insurance-covariance-exact.json`为后续精确报告。primary四源同路径在两冻结提交字节相同；manifest保完整双来源定位。

## 独立有理检查

`python3 verify.py`仅用标准库，输出`verification.json`。

- 旧36：完整43有序节点×6行动=258条IC；18真实删槽列；冻结q单纯形；所有原F/C/D/I/余额精确再算。正支持KKT残差严格正，故冻结有理q不是极小点；原程序只打印它、没有assert KKT。原IC_sum硬编码0在本输入已独立证实。
- 保险：11坐标按1/2重数压16个单位客户；180实际前缀真实列与IC；指定有理q、L、固定uniform30精确KKT、所有F/C/D/I/余额及锚负载下界。完整六人有序树未枚举，SPE依正式对象所引解析控制器定理。对浮点冻结q重建L/F/C/D/I的最大误差约1.09e-14，不称精确浮点证书。

## 两原程序的实际执行

`python3 run_original.py old36`与`python3 run_original.py insurance`分别将原字节复制至临时冻结布局，旧36同时置入两个原依赖；执行完收集输出、删除临时树。原件不在运行目录。事件记录在`runs/{old36,insurance}/event.json`，stdout/stderr及生成JSON在同目录。

Python3.12.14、NumPy2.3.5、SciPy1.17.0下两次exit0、stderr空。两份生成发现JSON与各自primary冻结文件逐字节相同；`reproduction-comparison.json`保逐SHA结果。保险probe额外写的精确报告与related后续精确报告所有共有字段相同，后者多`by_role`；不宣称这两个报告字节相同。原程序依NumPy/SciPy；`verify.py`不依赖二者。

本批没有重放后续saddle producer或独审程序；后续全部最优查询量词来自所读正式对象和related数学稿，不冒作本次程序枚举。未做新扫描、外审或一般付款证明。独立检查和原程序执行各承担不同证据角色。

## 路径与协作范围

只新增本独占证据目录、正式对象及`cleanup/workspaces/Boss5/receipts-shared-covariance.json`。Git/claim/done/checkpoint由父Boss串行办理；本worker不执行这些写操作，不读凭据。receipt四源分别写独有内容与后续区别，不替相关来源额外done。

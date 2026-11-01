# 固定完整策略的终局税探针

主源 `17182ac367b77ce669e6` 是1887B `tax_probe.py`，SHA256 `8f72ad4dc8464ef17883bce8f273faefe55152dd31b35aeee136c8bcf3579e21`。本包完整保原件、一次原main和一次新增独立有理接口核；[自足程序正文](../../../state/程序/完整策略客户锥的终局税探针--程序.md)给全部域、真实分支、平局、归一化、输出局限及固定锥证书证明。

## 文件身份

|文件|角色|
|---|---|
|[original/tax_probe.py](original/tax_probe.py)|两冻结提交同字节原件，n4/k6；无参数解析，导入时构造259动作，main才优化。|
|[related/research_README.md](related/research_README.md)|全文读的2588B工作区背景，保研究身份，不代该源完成登记。|
|[run_original_once.py](run_original_once.py)|未改原main的透明runpy与只读profile观察器；没有第二次调用optimize。|
|[replay/execution.json](replay/execution.json)|真实命令、环境、函数/LP次数、6.952439421秒、exit0、源前后指纹。|
|[replay/capture.json.gz](replay/capture.json.gz)|原输入和259动作、1554×63有理矩阵、共用浮点约束、15个目标/原始解/dual边际、main的整数恢复；解压3482470B。|
|[replay/stdout.txt](replay/stdout.txt)、[stderr.txt](replay/stderr.txt)|原stdout114B、stderr0B；打印value是OPT比较覆盖减W减全税的方向。|
|[audit_source_contract.py](audit_source_contract.py)|独立标准库实现；无原helper/规范/SciPy导入、无LP；从有序真实续局重建系数并验有理原始/对偶。|
|[exact-audit.json](exact-audit.json)|97902个Γ系数、945个目标系数相等；15份精确原始/对偶及七客户点的实际量。|
|[execution-scope.json](execution-scope.json)|原入口、新独立核、旧61客户身份复用和调用者不同首样本的范围。|
|[manifest.json](manifest.json)、[self-check.json](self-check.json)|来源和比较指纹、交付路径与最终静态检查。|

原main实际命令为：

```text
python -B /workspace/scratch/c0ab78c47566/round15-tax-work/run_original_once.py
```

记录器运行的未改副本在 `/workspace/scratch/c0ab78c47566/round15-tax-work/runtime/tax_probe.py`，main1次、optimize1次、terminal216次、15LP全success。原代码不写JSON；本包捕获与事件是透明记录器新增的证据，未冒历史stdout。原source前后SHA相同。

新增独立核实际命令为：

```text
python -B /workspace/scratch/c0ab78c47566/round15-tax-work/audit_source_contract.py
```

首次PASS约0.834645325秒。脚本拒绝覆盖已有exact-audit，未来重做请复制所需输入到新目录；本轮未第二次执行。15个新有理原始点逐条核23310个IC；main七客户整数点另核1554个IC与15个静态比较。没有重复旧61客户全树认证。

## 精确新增结果及边界

本源归一化为**客户总质量1**，不是W1。15个固定比较的精确最优值分布为1/35×3、3/32×9、91/1030×3。每份都保存非负λ、等式乘子ν及非负坐标余项s，满足 `cost=ν·1+Γᵀλ+s`，并有可行原始点达到ν。因此仅对本页固定的259动作sigma，有 `W+τ−OPT₄≥总质量/35`。全部精确对偶在新审计中认证，不凭float success或原minGamma打印推断。

原main选出的七客户点为掩码2、4、8各1、49有4；W4、τ16/5、OPT₄7，余量1/5，总质量归一余量1/35，W归一余量1/20。它达到本锥的总质量界，仍是正余量，不是终局税或half反例。大块加私有单例属于已有锐性族，本包新增的是具体σ接口和全部15锥对偶。

默认seed恰同[61客户根税例](../../../state/反例/四人实际根总税--反例.md)，前三位恒A/末位最高标签破平局也相同。旧seed的SPE身份直接复用；它只反驳前三步税，全部终局税余量为41/10。不能把这个旧失败搬到全终局税。

[worst_tax首样本事件](../full-terminal-tax-sampled-policy-program/first-sample/execution.json)另对不同抽样σ调用optimize15次，随后在第二轮开始前停止；不是本源又跑一次，也不是80轮完成。本页精确对偶不为那个不同σ给下界。完整客户锥及终局税一般候选的比较见正文，阶段三关系由父方处理。

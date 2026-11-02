# Ra0 静态安全最优费用：七原件和31客户精确反例

Boss2本批只完成七来源，总17506B；claim pushed `501efec6deb1caa9ead12c7f8853bd532731359a`。两程序全部、五JSON全部字段/所有dense weights/query/Q/masks均完整实读；原字节、SHA与双冻结定位在[source-manifest.json](source-manifest.json)。未修改上批stage或现有SSR/BNS正文，root另统一维护旧候选/范围页的当前状态链接。

## 交付与独有内容

| 来源 | 文件 | 语义去向 |
|---|---|---|
| 3418236fa2060792e977 | static_regret_cone.json | 千轮固定完整σ锥的原有限报告；mask63单客户零点 |
| cc7a3a7e744f868515de | static_regret_cone_probe.py | 全43历史258Γ、保持静态p/Q鞍点的质量LP、再择最优面费用 |
| 4706541d2bfb28bf2669 | static_regret_k6n2.json | 31客户阳性；新增完整两人σ与精确全P*分离证书 |
| 97b589023b3d1fb20f38 | static_regret_k6n3.json | 1998非零样本/12客户保存点的数值零边界 |
| af94ad17223d1b5adbac | static_regret_k7n4.json | 1000非零样本/89总客户、W80保存点 |
| 84884ff7b056daca191b | static_regret_k8n5.json | 400非零样本/133总客户、W120保存点，补旧缺件样本数 |
| 651bb0c8a53932de03d2 | static_regret_probe.py | LCM整数集合续局、精确可实现计数集合与浮点安全/近似面费用筛查 |

[report-read-summary.json](report-read-summary.json)无损映射每份原报告所有非质量字段，另列完整稀疏质量；原稠密数组含负零仍保原JSON。[dependency-manifest.json](dependency-manifest.json)说明原程序没有本地数学依赖，两程序有main guard、需要NumPy/SciPy，原环境/命令未存。新固定核只用标准库和n2原JSON。

## 一次真正执行及准确范围

[check-thirty-one-client-point.py](check-thirty-one-client-point.py)只读固定n2输入，不导入发现器。实际执行恰1次exit0；[事件](thirty-one-fixed-execution.json)保命令、耗时、代码/输入/stdout SHA，[stdout](thirty-one-fixed-check.stdout.json)保全部42比较与6×6静态收益、3完整两人SPE和2终局计数、原始/对偶匹配、唯一最优面及R−W。

原两个main、所有随机扫描、原NumPy/SciPy优化、41核验器均0次。其他三个整数保存点未新跑集合BI/LP/完整策略恢复，千轮锥也没有新扫描或精确全锥dual；不得把原samples/elapsed当本次事件。

固定31点有真实有序路径(5,3)，完整σ根5、首标签0…5后的末位(2,2,0,0,2,3)。实际收益16/15，W=OPT2=31。静态p*=Q*各半0/2匹配v2=14；对偶严格排除另外四查询，再由背景0/2迫p*唯一。R=(32,43/2,32,26,3,55/2)，所以min整个P*R=32>W31。该例**精确否定一般EXISTS-SSR**，却满足强聚合安全和half。

复核命令（成功后本批未再次执行）：

```sh
python /absolute/path/check-thirty-one-client-point.py
```

脚本按自身保存目录定位原JSON，只向stdout输出，核验输出应另存新文件，不覆盖冻结证据。

## 比较与关系

10项全文比较绑定见[comparison-bindings](comparison-bindings.json)：SSR候选与旧scope、实际路径固定鞍点资源、完整策略锥对偶、两种旧regret/全p反例、41原JSON及隔离资源、PB两预算推论、保险边缘引理。绑定SHA是实际读时版本；这些相关对象不是运行依赖，旧SSR页后续附加当前31状态时不能倒称本批当时已读新字节。

41输入是三人五主题actual044，原scope只反ALL、保EXISTS；31是两人六主题，P*唯一，量词和客户谱不同。PB两菜单用真实强制r槽/v_(r+1)/首对α+β，SSR用冻结实际叶m−1槽/全体W；本31背景SSR否定只用b0包含，不借PB。静态正遗憾max正部、真实分支ΣCi、extra-one、强安全/half也分别保域。

[relation-evidence.json](relation-evidence.json)给5条人工解释的实现/固定证书/反驳/状态补闭/共享策略不同预算关系与明确不造的边。旧资源当时缺件声明保留；当前一般SSR由新独立反例更新，原恒等式和条件推论仍正确。没有新颖性、外审或客户/主题最小性声明。

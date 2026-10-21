# Boss9 一般全局证明分支

主目标 Q-CAG-HALF 仍 OPEN。此目录研究任意共同目录、任意人数、全部完整有序历史纯 SPE 的一般半覆盖；未获得一般证明或合法主目标反例。个人草稿由 root 汇总，不自行提交/推送。

## 当前材料

- `exclusive_credit_obstruction.md`：任意背景可恰望远镜到全局 entrant 信用的逐人“首行动最终独占税”递推，以及其四主题四人16单位客户完整 SPE 障碍。根收益13/4、零独占信用、最大插入价37/10，严格差−9/20；W=OPT=16。作者定义级核验通过，待另一研究员独立攻击，不是全局 entrant 信用反例。
- `exclusive_credit_four_instance.json`、`exclusive_credit_four_certificate.json`：最终输入及85有序历史完整策略；`exclusive_credit_independent_audit.py` 直接展开单位客户检查340项含自身比较，不导入规范模型/oracle；`exclusive_credit_audit.json` 为实际输出。
- `exclusive_credit_probe.py`、`exclusive_credit_witness.json`：原始37客户六标签发现源，已由最终16客户四真实主题替代。保存探索，不主张最小性。
- `entrant_cone_probe.py`：复用R-d7f.../exact_credit_probe.py完整策略锥发现代码，将背景系数改为α=1。`entrant_cone_probe_m4p5.json`、`entrant_cone_probe_m5p7.json` 分别为50轮250LP、20轮140LP有限筛选输出；未找到正目标，绝不构成桥成立的证明。
- `entrant_probe.py`：浮点集合值BI只作快速发现，潜在反例必须规范exact重核；1000随机实例未找到正点，不承担普遍结论。
- `potential_probe/`：嵌套研究员的独立势/完全单调核探索，以及对 tree_coupling 的支持守恒模板9/4障碍的独立定义级审查。审查未调用发现者checker，精确重建图、稀释、守恒及客户身份失败；准确为抽象模板障碍，非CAG或half反例。

## 尚未闭合的精确义务

全局候选（早先Boss8已提出，不是本轮新命题）

`m max_T Σ_{x∈T}1/(1+c_x) <= W+Σ_{c_x>0}1/(1+c_x)`

仍开放，若成立则逐客户代数给 `OPT <= mM+W−G <=2W`。本轮否定的只是不能将G信用按当前玩家的最终独占客户逐人分摊的加强。不应重新尝试相同局部递推；需要跨玩家/分支补偿或改换全局表示。

当前继续研究完整SPE与离散凹势/完全单调均分核之间的全局近似VI；普通势函数已存在更早障碍，不能把静态PNE/CCE、Φ≥OPT或每期非负重新引入。

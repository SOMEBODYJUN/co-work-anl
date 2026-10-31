# R-171 区间租金有限审计（2026-10-31）

原始冻结源 `83e61bcee68d546ff8c9` 是 `audit_path_interval_rent.py`，SHA256 为 `32aacda40fc7fe2820593ae6f20b4e346f6faf8edd5886dfd44c161823a4ea46`。脚本只用 Python 标准库 `Fraction`、穷举和固定随机种子；没有均衡求解器，也没有声称 Q-CAG-HALF。`replay/audit_path_interval_rent.out.json` 是本次直接运行输出。

运行通过 147456 个单区间、51384 个小型全宽度组合、4094 个加权路径和 2000 个固定种子随机样本。输出同时保留了被拒的二次秩改进（bits=1010，实际成本 1/4 而错误界为 1/6）和非连续槽族：小例 `100111` 的成本 11/36，错误区间界 3/10，差额 1/180；一般 q 族成本为 `H_q/((rho+1)(rho+2))`，`W=Gamma=1`，故 q 增长时不受连续区间界控制。

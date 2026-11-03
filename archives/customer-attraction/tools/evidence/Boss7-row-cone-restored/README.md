# 根税固定完整策略的ROW对偶恢复

四个primary：row_attack.md、row_attack.py、row_attack.json及同目录README（本处credible_README.md）。两个related：root_tax_failure.json和customer_attraction_strategy_lp.py。原件按冻结字节保留；manifest.json给完整路径、提交、size/SHA与primary/related身份。related不在本批另记done。

父Boss7完整读取正文/源码；JSON完整解码所有252案例，逐元组、位置、状态、原始标志、目标值及412乘子解释。新verify_row_duals.py不导入原程序、NumPy/SciPy或模型：从259个有序节点重建1295偏离、310个非零不同Γ行及全部126最优比较行，核252份对偶/15876残差；另以mask49单客户直接认证同锥最大值−1/4。verification.json是实际运行输出。

原报告不保存逐案例原始客户向量，因此只独立认证其全部上界及总体最大值，未认证252个逐案原始最优点。详细数学和互异目录边界见[正式正文](../../../state/计算/根税完整策略锥的同节点最优菜单精确余量--计算.md)。

复现：在任意目录以Python3运行本目录verify_row_duals.py，输出verification.json。无网络、求解器、随机扫描或外部依赖。

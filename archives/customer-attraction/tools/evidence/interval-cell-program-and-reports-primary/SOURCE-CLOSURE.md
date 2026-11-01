# 原源码闭包与执行边界

interval_cell_attack.py以自身parents[5]定位original根，正常动态导入同original根下R-ffea.../credible_counterexample/cone_search.py。两者都按research/workspaces/customer-attraction/...完整路径保留，因此原本地导入目标具备。主程序继承Search.__init__的mask/LCM/计数树/pay/obj及seeds；不调用依赖探索solve/cone/opt/main。依赖无额外本地源码import，只含标准库、NumPy、SciPy。

当前不导入或调用任何原探索入口。若未来经新数学疑点确有必要，必须从原路径运行并单独记命令、源码hash、环境、stdout及精确重放，不能把存放在这里叫作已运行。Python/NumPy/SciPy/HiGHS版本未冻结；现有JSON没有seed/命令记录，m5与当前队列存在静态不对应，故不承诺当前环境重现历史报告。

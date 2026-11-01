# 背景菜单有限证书程序证据

主源 `d46bde33a0a22e62434e` 全文2429B已正常 clean show，原字节、39乘子/384行构造、理论合同及全部文件分支进入[自足程序对象](../../../state/程序/背景菜单的有限证书程序--程序.md)。[source-manifest.json](source-manifest.json)记录两冻结提交、blob、SHA和无本地运行依赖/无输入文件事实。

- [original/background_menu_certificate.py](original/background_menu_certificate.py)为未修改原件；[run_original.py](run_original.py)只把它复制到新的隔离目录并执行一次，拒绝已有输出目录。
- [replay/execution.json](replay/execution.json)是本轮唯一原main事件：一次39变量384行LP，0.872866510秒exit0，精确Fraction断言通过、stderr空；脚本前后SHA相同。
- [replay/background_menu_certificate.json](replay/background_menu_certificate.json)和[stdout](replay/stdout.txt)均186B，完全等于配套冻结证书，SHA db25a2460aa58d9a8438f7aea0e20445c12264f717c587cafdd9974338d58689；[stderr](replay/stderr.txt)为空。原数据主源另由配套数据页处理，未重复认领。
- [comparison-manifest.json](comparison-manifest.json)保存现有数学对象实读比较；[execution-scope.json](execution-scope.json)列实际执行及未执行，特别没有第二次原入口、相邻探索或六人SPE运行。
- [配套数据对象](../../../state/计算/背景菜单的有限证书--计算.md)和[独立有理审计](../background-menu-certificate-data/exact-audit.json)负责从原始客户份额验证四项稀疏支撑、384精确行和符号余项；程序包直接复用，不重复其计算。

理论命题是合法H重复L≥1后恰剩两人的 P+Δ≥freshOPT₂；更一般“合法H恰等于旧覆盖并集”的条件推论由逐客户仿射证明给出。任意背景未必有该合法H，不能把本证书升级成已被52客户例反驳的一般GLOBAL或六人half。

从仓库根复现到一个新的目录：

```sh
python3 archives/customer-attraction/tools/evidence/background-menu-certificate-program/run_original.py --source archives/customer-attraction/tools/evidence/background-menu-certificate-program/original/background_menu_certificate.py --out-dir /tmp/background-menu-new-replay
```

该命令是可复现入口，不表示本轮又运行了一次。浮点求解器版本可能改变所发现的最优乘子；wrapper还检查本冻结输出SHA，若返回另一份合法证书会因字节不同拒绝把它冒认为旧证书。数学有效性必须另验非负乘子及精确余项；原main未给完整SPE存在或最优福利证明。

[check_package.py](check_package.py)只检查原字节、运行事件、所有本地链接、JSON/Python语法与回执目标，不调用原main或数学审计；[artifact-manifest.json](artifact-manifest.json)绑定交付文件，[self-check.json](self-check.json)保存本轮静态结果。

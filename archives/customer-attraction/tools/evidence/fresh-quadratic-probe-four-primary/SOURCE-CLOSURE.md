# 原入口复现闭包与缺失历史过程

原源码按research/workspaces/customer-attraction/R-5e9dedd2606746ff8afbbb73bf816e7a/new_representation完整相对路径存档，三个JSON仅冻结输出不是程序文件输入。程序无本地helper/实例依赖，标准库+numpy/scipy，output由CLI要求给定。原文件有main guard，导入不做样本/BI/LP但会导科学包，--help亦同；此批未import。

模型合法域1<=m<=p且samples>=1；source未验证这些前提。output只write_text覆盖、不自动建父目录，可能异常前保留旧报告。原报告缺source SHA/argv/lp_every/requestedsamples/环境/stdio/exit/所有points；已存source字节与数学合同可复现新探索，但不是原执行逐字节闭包。不为补日志重放旧阴性。

三报告所有11字段逐项保存。当前code正周期10/20/20条件与次数相容，不写回原件/冒实际argv；failure均null，最小sample差0，LP微负目标只是浮点记录。完整source size/SHA/blob/normal/owner核与数学证明不同，不把前者当普遍正确性测试。

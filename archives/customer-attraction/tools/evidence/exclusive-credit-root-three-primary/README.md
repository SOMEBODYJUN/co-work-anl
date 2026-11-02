# 首人独占信用反例的根独审三原件

三原件均由本次clean show导出并核冻结SHA。original/保持旧仓库布局，含三主源、两份有哈希输入和四个规范模块；规范代码及作者输入为已有已出版同SHA只读依赖，不额外done。

本次仅根独审原main一次：启用assert，exit0，stderr空，761B stdout与冻结JSON逐字节相同。该脚本调用预存的定义级verify_certificate，沿完整有序历史重算85节点、255真偏离，再独立展开单位客户重算根算术；未运行作者审计、发现器或ExactSPESolver搜索。

复验可在包目录执行 `python -B -I original/research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/audits/exclusive_credit_review.py`，只打印JSON；-B避免生成缓存。实际本次命令、依赖SHA、输入和策略SHA在execution.json。根独审依赖规范verifier，不把它称为完全自含第二SPE实现、盲审或外审。

数学见[原资源补录](../../../state/资源/四主题十六客户独占信用反例的完整策略与定义审计--资源.md)。局部式假、原点全局余额为正，六人half另题。

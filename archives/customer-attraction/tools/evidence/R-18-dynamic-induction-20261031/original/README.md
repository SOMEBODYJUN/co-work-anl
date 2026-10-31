# 动态归纳个人探索记录

研究者任务：任意背景剩余利润、可闭合归纳与非局部势。当前一般半覆盖仍 OPEN；本目录只保存探索与准确范围的边界。

## 已完成

- `profit_opportunity_boundary.md`：完整全历史 SPE 的经典大主题族否定新候选利润机会步；所需首位收益乘数随人数发散。包括精确闭式和独立 Fraction 审计。
- `profit_opportunity_audit.py`：不导入规范求解器，逐历史检查大主题族完整策略，穷举背景利润组合，输出新的审计记录。
- `background_step_instance.json` / `background_step_certificate.json`：另一五人12客户真实路径反例；规范求解器生成、独立 Fraction 审计复核121个有序历史。
- `step_profit_search.py`：探索脚本，有限搜索不是一般证明。

## 继续方向

利润机会量下降同时包括失去一个动作槽与背景租金变更，两项会在根步合并成发散缺口。单靠当前终局收益无法固定系数支付。寻找允许路径偿还的非局部势，不能把局部失败扩大成半覆盖反例。

# 实际位置删槽全历史菜单：七主源证据

七源共24581B均逐源clean show完整读取，original保未经修改字节；source-manifest.json核冻结size/SHA/blob及双来源。

正式对象：

- [删槽精确包络算法](../../../state/算法/实际位置删槽菜单的全历史精确包络--算法.md)：公共客户不变性、E/F/R/H与完整历史拼合，固定实例/p精确表示全部SPE最大gap。
- [攻击与定义级核验程序](../../../state/程序/自由删槽全历史攻击与定义级核验--程序.md)：两个搜索域、数值LP、整数/Fraction边界、七个完整策略穷举输入和历史记录的范围。

## 目录

- original/：全部七个冻结原件。
- source-manifest.json：每主源ID/完整commit/原路径/size/SHA256/blob。
- dependencies/ 与 dependency-manifest.json：唯一原verify入口需要的四规范模块，已全文读并对inventory同SHA。model提供最后的Fraction逐历史核；ExactSPESolver/certificate只被包初始化导入，未调用。
- comparison/ 与 comparison-manifest.json：实际全文比较的四份正式正文及父方四份后续来源快照；related不额外done。
- runs/event.json、verify.stdout.jsonl、verify.stderr.txt：2026-11-02一次未改原verify入口的真实运行，exit0，七例stdout与冻结851B JSONL逐字节一致，stderr为空。

没有执行attack/full_menu搜索，没有新增维度/种子，没有把旧中途版本的80输入筛查伪装为最终冻结源码重放；父方历史重跑与本轮运行分开。无一般AFC付款、六人half、原模型反例、外审或新颖性认证。重复覆盖主题只作较宽软件标签边界核验，不改原集合目录量词。

# 独立全局攻击工作台

本目录仅为未完成研究备份，不提升任何一般结论。目标保持一般共同目录、任意人数、任意完整历史纯 SPE 的 `2W>=OPT`。

已读根入口、模型、前沿与失败地图。独立思路：从同目录克隆偏离、背景利润与跨真实威胁分支的全局支付入手；逐人残余和逐期安全漂移不能使用。

`security_alternation.py`（探索代码）在固定完整策略锥内，交替优化真正静态安全查询分布和非负客户重数，用于寻找强聚合桥 `m v_m<=W` 的障碍。浮点只作候选，任何发现必须另做精确客户、全部历史和安全下界核验；有限未找到反例不证明桥。

外部原始文献检查：Brethouwer, *The quality of equilibria in generalized market sharing games* (2018), §7 shared-misery payoff guarantee 只直接适用于满足逐次伤害者收益不超过被伤害者新收益的类。一般 CAG 不满足；不能直接导入一般half。原文链接：https://essay.utwente.nl/fileshare/file/76986/Brethouwer_MA_EEMCS.pdf 。此处仅作来源定位，不作新定理。

下一步：检查真正强聚合安全预算，或找到一个跨背景有效的平均伤害/克隆交换引理。主目标和强桥均未解决。

## 本轮探索状态

- 强聚合安全交替LP：4主题3人70个完整锥、5主题4人35个完整锥，没有浮点越界候选；最优值可到 `m v/W=1`。这仅记录搜索范围。
- `uniform_interface_attack.py`：攻击 `global_new_uniform_portfolio_two.md` (6)，3人5主题100个完整锥与4人6主题45个完整锥没有越界候选；达到 `m OPT−ΣVij=(m−1)W` 的边界。这不证明开放接口。
- 父代理指出旧候选有限扫描信息价值低，已停止这条扩张，下一工作优先为可信反例同事新padding声明做不依赖其证明的独立重建。

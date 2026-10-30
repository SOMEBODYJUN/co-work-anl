# quadratic-triad四源交付

claim由Boss执行并pushed，提交 `5a784a3676b6a517d1cd69d43c7ebe00a0899281`。4原件均已完整读取、逐SHA256核验并原样保留。子代理未做Git、clean事务或共享图/他人正文修改，最终全部自查通过。

## 路径

- `archives/weighted-congestion/state/反例/三玩家六资源整数二次均衡阈值--反例.md`
- `archives/weighted-congestion/state/计算/三玩家整数二次例的完整阈值核验--计算.md`
- `archives/weighted-congestion/tools/evidence/integer-quadratic-triad/`
- `cleanup/workspaces/Boss4/quadratic-triad-receipts.json`
- 本文件。

## 实质结果

固定权(16,2,5)、六资源13x²/59x/2x²、每人两个非空不交动作，最佳纯均衡倍率恰286/267。全部8态、24个不同单人翻位由明确动作和资源负载重建，端点010/101有弱PNE，对全部1≤alpha<286/267无PNE。完整表、整数交叉积、正确商环和0/1/2/0/1/2六步literal环已自足保留。不是一般存在上界、无限增长族、文献最优或新颖性认证。

与旧separable-certificates的exact_fixtures第一例逐项核权、六资源全部系数及所有策略完全相同；旧53/50询问是同一游戏的较弱阈值，未算独立新发现。决策JSON只是这一既有例的具名资源格式转换。二次19/18源包络此前只核286/267差但未认证该游戏；本批取得真实例后可作25/1602严格有限比较，不将19/18升级为整个对称拓扑上界。

已全文比较既有clock编译代码：同mask/权/系数，INITIAL=010，alpha21/20。该代码本批不重跑不done，62次新增时钟预算仍由原计算对象负责。另一权(1,2,3)、阈值20896/20875的三hub侧资源游戏是不同对象。resource_cone独审旧路径在冻结inventory无匹配，没有伪称取得审查；原MILP支持选择记录只作为历史，不承担证明。全类旧OPEN用后续linear全文更新。

## 实际复现及自检

运行 `python3 archives/weighted-congestion/tools/evidence/integer-quadratic-triad/replay.py`，原验证器未改写隔离执行，Python3.12.14退出0，完整新报告与冻结JSON逐字段零差异；费用乘7、互补、零成本/空动作/常数/共同membership边界一并执行。

新增literal检查不导入作者实现，从决策JSON显式策略/资源系数独立计算；全部8态24翻位的当前/偏离费用、比、最大攻击者、精确阈值、弱端点、53/50各态严格余量和6条环边均通过。完整输入、原/新输出、stdout/stderr、源码hash与比较报告均保存。它是内部迁移交叉核验，不是新盲审或独立构造发现。

自查通过：4原件hash、4比较依赖hash、4回执ID唯一/targets存在、2正文YAML/稳定ID、全部相对文件链接、无行末空白、原报告差异为空、literal输出完整；正文展示010时玩家0的16/23负载到23/16负载及2002→1869已另以整数式复核。

关系判断已写入正文：同一旧53/50证书的精确化与格式迁移；真实完整有限表给固定反例；具体反例与源公式上界作联合有限比较；同一基体到时钟编译须另担新增次数/环外覆盖；潜在支持≤3给整个小支持子类3-PNE，不能据资源复制取得无界倍率。Boss可先checkpoint上述正文证据pushed，再用4条integrated回执done。

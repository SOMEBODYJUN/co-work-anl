# 三十二有理精化切面的数据核验

主源9ddb1502995eb9e435eb；[完整3252B原件](../continuous-old-query-cut-data/related/continuous_refinement_cuts.json)已由前批作为相关原件保存，本批正式清洗，继续共享。SHA aa696d0ebbb1e5b1ccc3b593c5f5a4bcac4cf411966dfd9499192d8170fb5c36。全文两字段与32八元组均保，不补造原表没有的slack/输入/轨迹。

[数学正文](../../../state/计算/连续旧查询的三十二切面精化表--计算.md)解释全部坐标、真实IC投影、与64表的21元组交集及不同阶段点身份。仓库根复现：

```sh
python3 -B archives/customer-attraction/tools/evidence/continuous-query-refinement-data/audit_refinement_cuts.py
```

[审计器](audit_refinement_cuts.py)调用前批已归档数学积分函数，不导入原发现器或求LP。当前退出0，[完整报告](four-stage-cut-audit.json)逐条保四阶段余量：4971点32负；5075点3零29正；5108点5零27正；换Zpair点3零29正。还核所有输入SHA、5075/5108列描述符相同、W相同但124权重不同。

5075点的[816661B原件](../continuous-query-refinement-program/related/continuous_refinement_exact.json)及一次原5075 verify事件共用代码包，不复制或重跑。原发现历史、连续族闭包、最优性、其它旧行在新Z处及完整SPE均不由本数据审计认证。

# R51父方路径与末尾审计器

正式对象：[R51路径末尾障碍审计器](../../../state/审查/R51路径末尾障碍审计器--审查.md)。主源ID `46a066e1314b35a10c1f`，4937字节原程序已全文读取，SHA256见manifest。相关原报告ID `5fbb919968e92b8c7ad2`，277934字节，仅作为完整输出比对与范围检查，不由本回执替它done。

源码只依赖Python标准库。`main`内置m2…15全部合法k、radius共560组，实际路径比较合计134400；指定五个r0参数的尾计数代表比较合计245478；m≤4十参数全有序树比较合计12694，其中415项负值都在早期保护带外；所有455个d≥2组另有明确远轨负见证。105个d1组W=OPT，解析上是完整SPE，只有其中六个m≤4组在本入口直接全树穷举。41个低于half的形式路径全有负见证，均非SPE。

不交整数块大小可展开为不同单位客户；实现没有逐客户展开。完整形式策略在每个有序历史定义，但只为所列域要求IC非负。完整尾部计数压缩只在进入无条件fresh-B规则后成立，不能压缩早期标签汉明保护带。三个比较域有重叠，不求虚假的互不重复总量。其他大参数保护球/全尾及一般无界比结论仍靠已归档解析证明。

原CLI会覆盖写**源码旁**的`path_tail_obstruction_audit.json`，stdout只打印两行摘要。本次将原码复制至`run/`再运行，没有在`original/`执行。正常assert开启，Python3.12.14，exit0、stderr0、约1.296秒；`run/event.json`记真实命令与指纹，完整新报告与冻结报告逐字节相同。原内存数据含tuple，而JSON序列化把它变list；这里精确比较序列化JSON字段和字节，不比较原内存容器类型。

可复现命令（从仓库根，先确保run只用于新生成证据）：

```sh
cp archives/customer-attraction/tools/evidence/R51-path-tail-obstruction-auditor/original/audit_path_tail_obstruction.py archives/customer-attraction/tools/evidence/R51-path-tail-obstruction-auditor/run/audit_path_tail_obstruction.py
python3 archives/customer-attraction/tools/evidence/R51-path-tail-obstruction-auditor/run/audit_path_tail_obstruction.py
```

第二条命令会在run中重写完整JSON；当前保存的一次真实执行由外层包装捕获stdout/stderr和事件，复跑不会自动更新这些日志。勿用`python -O`关闭assert。无随机发现、外部输入、LP、网络、规范求解器、原发现者代码或新盲审/外审。

已实读比较的正式对象包括共同目录完整历史模型、标签汉明删行障碍、双独立审查资源、[20组原独审程序](../../../state/审查/R51汉明尾部审计器--审查.md)、[20组报告](../../../state/计算/R51汉明尾部有限审计报告--计算.md)和[不交最大主题全效率定理](../../../state/定理/区间终局剪枝的上界比较与全效率目录类--定理.md)。程序560组与20组全有序保护域、发现方8组尾样本各有独立计数范围，不能混算。报告的字段独立核验见[同批计算对象](../../../state/计算/R51路径末尾障碍有限审计--计算.md)。

`manifest.json`保主源/相关源/当前事件与文件指纹；`relations.json`逐项说明模型、实现、删行、负行和后续全效率定理的关系。正式超图留第三阶段；本目录没有完整SPE半覆盖反例、完整Γ分离或六人全目录结论。

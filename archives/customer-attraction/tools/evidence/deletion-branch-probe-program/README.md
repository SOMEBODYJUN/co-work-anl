# 固定反组策略的终局删除查询探针

自足正文：[固定反组策略的终局删除查询探针](../../../state/程序/固定反组策略的终局删除查询探针--程序.md)。主源54ba59fc852a4f5ee5b9的[2574B原程序](original/deletion_36.py)按冻结字节保存；名称36不代表人数或客户输入。实际是n=3、k=6、固定43历史策略、root034，63质量变量加一个t，22次固定查询分布LP。

| 证据 | 准确身份 |
| --- | --- |
| [original/deletion_36.py](original/deletion_36.py) | 完整原源，保留动态exec、无main保护和候选输出路径错误 |
| [original-event/execution.json](original-event/execution.json) | 一次未改原入口：1.676442691秒、exit0、22个正常循环LP调用、六输入前后SHA相同 |
| [stdout.txt](original-event/stdout.txt)、[stderr.txt](original-event/stderr.txt) | 原stdout37B、stderr0B；best为−0.08333333333333315，未命中候选 |
| [run_original_once.py](run_original_once.py) | 本次实际使用的隔离包装器原样留存；保当时scratch路径和单次保护，不是又一次运行 |
| [inspect_contract.py](inspect_contract.py) | AST和保存执行事件的静态解释；不运行原代码、随机实例或优化 |
| [contract-audit.json](contract-audit.json) | 首次静态核输出：全部22个p、43/258/261/64结构、未使用ww、覆盖n、负结果和候选自覆盖诊断 |
| [source-manifest.json](source-manifest.json) | 主源、共享五依赖、原运行与相关数学对象的绑定 |
| [check_package.py](check_package.py)、[self-check.json](self-check.json) | 正式文件指纹、事件/合同、Markdown链接和回执的静态收尾 |

五依赖统一保在[相邻程序包](../deletion-security-probe-program/README.md)：tax_probe.py提供当前exec前缀及coef等名字，四个customer_attraction模块由正常导入加载。本轮已全文读这些源。tax的n4初始sigma会构造，但随后本源改成n3固定sig；tax main/optimize和ExactSPESolver均未调用。随机ww也没有进入LP。

数学对象是固定实际终局z的三删除背景：34、04、03。对每个预定p，t≤每个删除背景下的独立查询期望，优化W−(5/2)t，并保全部真实历史IC。这里删除支持小于真正静态安全值允许的全部两槽背景。现有[同策略共同Q证书](../../../state/定理/三人六标签固定分组策略的共同静态安全对偶--定理.md)在01、02、03上给v₃≤W/3，它与本三删除支持的有限浮点结果不是同一证书。

best负数不是精确−1/12下界，原程序没有保存最佳p、质量、t或逐LP状态，也没有保存精确对偶。候选分支若命中，错误的`replace('deletion_probe.py',...)`在本文件名不生效，会覆盖正在执行的deletion_36.py；本次未触发该分支。不能直接在正式原件旁重新运行。

当前独立工作仅有一次完整原入口和首次静态合同解释；没有重复22个LP、没有重核旧36客户游戏，也没有把配套随机n4程序的受控首迭代当作本源运行。原事件包装器保实际运行路径；接续若确需新运行，应使用新隔离目录、正确文件名和匹配冻结依赖，并保原源的完整备份及执行后输出，不能覆盖本次已保存事件。

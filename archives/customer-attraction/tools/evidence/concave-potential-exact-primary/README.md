# 单调凹势、格点DR与插入VI的五源证据

承载数学见[自足障碍页](../../../state/障碍/凹势可行变分不等式与DR曲率--障碍.md)。全部五件主源以`clean show ID`实际全文读；27579字节原件分别在`original/`。`source-manifest.json`保ID、size、SHA256、Git blob、两冻结来源完整commit:path，已对两别名实际取字节核同。原CLAIMS/root账本的related阅读没有代替本五件的primary处置。

|原件|源ID|字节|用途|
|---|---|---:|---|
|`concavity_DR_VI_obstruction.md`|1da1ba0e2f4fffe9b3ce|5097|十平面、全历史策略、VI违约及两类不可表示性|
|`audit_concave_potential.py`|bc73da21d4fef7f9b2b3|4827|标准库整数表、支持面、全有序历史的定义级审计|
|`concave_potential_exact_audit.json`|ec74ab253c80561a7b6f|2966|原完整有限报告，含13历史的全部收益比较|
|`concave_potential_probe.py`|cbaad1c4eb99b87358dc|4299|随机种子计数策略、浮点固定策略锥发现器|
|`concave_potential_candidate.json`|766df212542d765c3f6e|10390|35势值、35梯度、10计数策略和归一违约的原浮点见证|

正文保全势与福利的不同、全域凹性与有限DR域、真实后继IC、调和克隆和完全单调边界，以及发现器中几何种子不限制最终LP的细节。候选`actual`是计数(0,2,1)，精确报告`actual`是有序路径(1,2,1)。本例不是CAG半覆盖反例，未赋真正客户目录或OPT。

## 实际执行与输出

`replay/`是单独副本，原整数审计在其中实际执行一次（启用断言、退出0、stderr空），输出同冻结2966B报告逐字节相同。保`run.json`、完整stdout、stderr和所执行脚本；环境及两报告SHA见run记录。它不读浮点发现点、不调用第三方优化库。这是知情内部重放，不称另一人的盲审、外审或新颖性判断。

`inspect_saved_candidate.py`已实际执行一次：只用AST读取原脚本中的字面量表，不import原脚本；完整比较浮点35值/105梯度坐标/10策略点与F/44、G/44、整数策略；从十面公式另输出全部60个DR残差及35个势值。完整结果为`saved-candidate-comparison.json`。这是数据对应及表提取，不是重新求解LP；数值误差不承担反例有效性。

发现器、几何核探针及任何CAG求解器均未运行。原默认iterations100不足走到候选的零基iteration163；至少需164轮，但原argv与random-policy选项未记录。没有补造原命令、原stdout或不存在的对偶。两原程序均顶层执行；import原审计会覆写相邻输出，`-O`会移除assert，故未来重放应复制原脚本到新空目录并正常启用断言。例如：

```sh
mkdir /tmp/concave-vi-new-run
cp original/audit_concave_potential.py /tmp/concave-vi-new-run/
cd /tmp/concave-vi-new-run
python3 audit_concave_potential.py > stdout.txt 2> stderr.txt
```

这是假定当前工作目录为本证据包时的将来重放示例；本次实际argv/cwd以`replay/run.json`为准，不在`original/`覆写原报告。

## 相关比较与已出版覆盖

`comparison-manifest.json`记录全文读过的三份现有正式对象之哈希及已在本clone拥有的origin跟踪提交；实际从该提交读取并核同，未fetch、sync、修改或重复生成它们。既有根账本准确有结论摘要，但明确未主读代码/报告或执行，缺十面和完整表，所以本次增加自足对象与资源闭包有实质增量。独占信用真实客户点只反局部加强；13人缩放精确税反例分母不同，不能据它们判断此未缩放桥。

另外正常`clean show`并全文读两个related源，保原字节但不为其另办primary/done：

- `source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-fa8dd4ddea574a74a634ebc71e6f9ccb/global_proof/potential_probe/README.md`（a380f41c9134d6746137）：确认本五资产的来源层次和未给一般几何核结论。
- `source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/potential/potential_boundaries.md`（57d7ff8d279a686510a0）：完整比较真实客户高阶交叉差、M凹交换障碍、全策略改善环及各自量词；它不为混合增删分支给统一符号。

关系判断在数学正文末节：本对象反驳扩大模型(VI)，原程序实现有限证书，重放只支持这份见证；它补充根账本并与其它信用公式分版。阶段三尚未建超图，未将程序PASS当一般half推导。父Boss串行checkpoint pushed后才可记本五源完成。

# R4背景候选的来源与定义核验

主源ID `c912ce14f70eebc638f1`；6002字节原件由 `work.py clean show`完整读取并原样导出为[background_candidate_attack.original.md](background_candidate_attack.original.md)，SHA256为 `578ddcb2648b3096a224bb30c47271dfb2c28dd5bf4635e99b8cc92cda44b54d`。两冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12`和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`的该路径内容相同；原路径为 `research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/transport/background_candidate_attack.md`。

[正式障碍对象](../../../state/障碍/R4背景候选运输攻击--障碍.md)保留其全部语义单元并据后续52客户GLOBAL证书纠正BG的历史OPEN状态。没有更改冻结原件，也没有为同一52客户证书新增反例身份。

从仓库根运行：

```bash
python3 archives/customer-attraction/tools/evidence/R4-background-candidate-attack/check_contract.py
```

[check_contract.py](check_contract.py)只用Python标准库。14/11客户的兴趣表和完整策略由已完整实读的 `continuation_lemmas.md`及 `coverage_opportunity_counterexample.md`逐项转录；52客户输入及259节点策略复用[既有原件包](../global-actual-prefix/source-manifest.json)，程序按相对路径读取这两个确切文件并验证原SHA256，不写该包任何文件。完整有序策略检查不以计数匿名替代历史。

本次结果为[review.json](review.json)：296个有序决策历史，1739项含自身行动比较，全部非负；随后精确核对三例的DEFECT、PRIVATE-LOSS，以及52例所有最优元组与真实偏离分支。关键数值为 $(\delta,u,S,defect)=(1,4,5,-8),(3,5/2,3,-5/2),(9,8,0,1)$。52例最优元组仅 $(T,Q),(Q,T)$；两个真实分支均给SWITCH左12、右9。输出可确定重生，没有浮点或优化器。

本次是对既有有限完整策略及本源公式映射的内部定义核验；未重新运行旧八例686点诊断，不声称一般BG、根half、六人half或最小规模证明。来源比较及条件性解析证明在正式对象展开；本目录不为未处置的比较来源登记done。

# 真实末位与额外插入菜单的三种有限探针

四primary共5982B：last_menu_separation.json 470B、probe_last_menu.py 1862B、probe_pure_menu.py 1745B、probe_relay.py 1905B，双冻结提交同字节，原件及SHA保存在`original/`和`source-manifest.json`。

正式正文为`state/程序/真实末位与额外插入菜单的三种有限探针--程序.md`及`state/反例/十五客户五人全根分支的末位收益分离--反例.md`，相对于本包在`../../../state/`。本包补原JSON缺少的完整策略，保低末位利润列、纯完整列插入cap、混合Mfull及half四种不同量词。

## 两个分别记录的新事件

1. **原固定函数调用一次。** `probe_last_menu.solve(3,5,[[1,6],[2,3],[3,6]])`，原模块import1、solve1、main0、随机扫描0，约0.002350秒。返回u和三menu按原格式序列化，470B与冻结JSON逐字节相同。报告字段index26是原数据保留项，本轮没有重跑前26个随机样本或认证历史首命中。`original-fixture-call/event.json`保源/输入SHA、参数和cache统计，`returned-fixed-instance.json`是本轮函数返回值的序列化，不冒原main重放输出。`recorded-original-call-driver.py`保实际编排器和当时绝对路径。

2. **新独立构造与定义核验一次。** `build_and_verify_fifteen_customer.py`不导入原probe、canonical或LP。用显式r1真BR基础的带末位标签集合递推构造完整σ，再由另一段只看实际有序路径/策略表/15名客户的验证器检查全部121节点、363项真实IC。后者不调用构造的tagged集合、threshold或type_pay。222严格、141等号（含121自身、20非自身平局）；所有242真正偏离都非负。事件在`independent-complete-strategy/event.json`，完整策略、15个客户、所有规定/偏离路径和有理收益在`certificate-and-all-IC.json`。

第二次进程通过exec_command实际exit0，约0.019943秒。工具合并返回了程序打印的完整摘要；本次未分别重定向stdout/stderr，故不补造一份独立原stderr文件。`report-derived-printed-summary.json`明确是按真实完整报告字段再序列化的摘要。完整报告本身是该次程序直接写出的原产物，源SHA和输入SHA均在其中。

没有运行任一原main、1000/1400/1200随机扫描、pure_menu.solve、relay.solve或未提供报告的探针。新脚本的完整证明范围只是一份固定σ，未声称枚举该游戏全部SPE。

## 该有限证书究竟证了什么

实际σ根选0、路径00001，收益(27/10四次,21/5)，W=OPT5=15。三个强制根分支00001、10010、21000末位收益21/5、16/5、7/2，全部超过实际根27/10，最小差1/2。目录标签2为空，包含它的全部离轨节点仍被定义/核验。相同计数的不同历史可在真平局中选不同动作，证书没有强迫计数策略。

额外插入cap在三列分别5/2、5/2、27/10，全部≤根；所以这不是纯插入列或混合完整菜单价格反例。后来银行全根Mfull反族有自己的底层游戏和全列证书，不回填成这份旧短报告的内容。

原2616B工作区README只在导航源述二主题三人低末位列例；它的原件已在`inherited-claim-state-primary`保全。本冻结报告实际三标签五人十五客户。本包已全文比较原README，不把两者拼成一份同版本证书。

## 复验

新独立代码默认读取本包冻结JSON，默认输出目录为相邻`independent-complete-strategy/`；为保护当前真实事件，默认该目录已存在时会拒绝写入。要另作一次复验，应提供尚不存在的新目录，例如：

```sh
python3 build_and_verify_fifteen_customer.py --output-dir /tmp/cag-fifteen-new-verification
```

这条命令仅为以后复验说明，不是本轮第二次调用。原三源码均无CLI参数；调用其main会启动对应随机扫描并可能覆写相邻报告，应先保留原件，不能因已有证书就随意覆盖历史源。

`source-dispositions.json`为四源逐件真实语义处置，`relationship-assessment.json`保存已读相关对象、共同前提、目标差异和没有直接推导的比较。六人half不由这些有限探针关闭；本包不增加外审或新颖性认证，也没有自动建立图边。

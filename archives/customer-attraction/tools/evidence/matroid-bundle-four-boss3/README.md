# 三份固定GF2向量束best的模型与精确证据

正式正文：

- [全历史Shapley安全探针](../../../state/程序/二元线性秩向量束的全历史Shapley安全探针--程序.md)：扩大模型、signed核、全部SPE集合与静态LP的完整原合同。
- [三点客户实现及精确安全值](../../../state/计算/三份向量束秩记录的客户实现与精确安全值--计算.md)：一份真非coverage、两份9单位客户、三套匹配有理安全证书。

`original/`保存原4708B程序和三JSON，合7590B；`source-manifest.json`保四primary ID、size/SHA256/Git blob及两个冻结来源commit，原float、args和历史耗时不改。`related-context-manifest.json`保全域Shapley定理、原5197B稿及相关数学的实际比较，不重复primary/done。

## 唯一一次固定输入核验

实际命令：

```text
python audit_fixed_matroids.py > fixed-best-audit.stdout 2> fixed-best-audit.stderr
```

程序／全部输入／输出均在clone外stage。原程序以runpy安全加载定义，main guard使随机循环不执行；0原随机CLI、0随机向量生成。仅对三份已存bundle各建立一次原整数BI缓存，再用已填缓存构造三份新完整动作表，没有重复BI搜索。另有3个新的静态LP提案及Fraction原/对偶后核，非原evaluate或原3400-game批次重放。

检查器直接按玩家联盟Shapley子集式独立重算全部2184占用收益，并沿三新动作表真实完成每个偏离。320个C值、3244有序节点、22665含自身／19421非自身比较精确通过。静态背景完整数21/84/210；保存query恢复成有理概率后，在315背景精确检查下界，三个同次LP的对偶背景概率另给匹配上界。没有仅把float值舍成分数就称最优。

`fixed-best-exact-audit.json`保全部320个C值、唯一非零signed类型、原记录元数据、完整背景query保证、精确对偶支持和每纯查询上界。三个`*-new-full-strategy.json`保当前完整动作表，身份明确为对保存target的本轮重建，**原JSON没有actions字段**。stderr为空、一次exit0；内部审计计时0.255秒包含三个新证书写入、不含最终汇总序列化，也不含初始库导入。`run-event.json`保命令、cwd、程序及所有输出SHA、版本与计时边界，未捕获的进程起始UTC时间不事后填造。

## 三点实际结论

|点|coverage实现|精确v|W−mv|
|---|---|---:|---:|
|三人六标签|否，交集t125=−1|1|0|
|四人七标签|9单位客户、完全不交主题|15/16|1/4|
|五人七标签|9单位客户、题6子集题1|14/15|1/3|

三人原负浮点噪声未越原−1e−8闸门，没有exact_gap；不称失败。五人原10不同向量rank9仍可coverage，不能把“有线性相关”当客户不可实现。四／五人全函数的非负客户表已恢复，原扩大模型身份不抹其合法CAG特例。

一般全域单调次模Shapley定理已有独立解析证明；三有限点不证明普遍聚合或half。原历史games2000/1000/400和elapsed仍仅冻结报告字段，无原运行event、全输入轨迹或源码SHA，本轮不补造其成功或无反例。

`self-check.json`只做最终字节、receipt、链接及当前事件SHA绑定，不调用数学入口。

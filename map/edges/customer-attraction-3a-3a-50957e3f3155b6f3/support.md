# 支持证书（SOLVER-THREE-TAIL-OBSTRUCTION-FRESH）

## 读入与哈希

任务固定版本 `33a57e03700c9f5aacc5110d752aac295e9dff8c82037897a91849f7135cd11f`，核心 pin `bc6b2e584afa224224f68788b9589ec0ec7298ce37130773af2d1b9688f8d002`。本包完整读取以下五份声明输入：

- `archives/customer-attraction/state/反例/实际三人余局的全最优六查询去相关障碍--反例.md` — SHA256 `b069213a466d4e1bacf10fdf1b9deae881c19cbf79847a5f6210fe1b55d692ae`，10,033 bytes，105 lines；完整反例陈述、量词、固定88客户SPE、四个最优支撑及解析恒等式。
- `archives/customer-attraction/tools/evidence/six-optimal-query-decorrelation-primary/new-independent-audit/outputs/actual-banks.policy.json` — SHA256 `2ad53054ee597a52b58c86ee6ca2a6638b3c97a546d516f328688af5a7913563`，913,417 bytes；保存的完整实际策略库。
- `archives/customer-attraction/tools/evidence/six-optimal-query-decorrelation-primary/new-independent-audit/outputs/independent-audit.payload.json` — SHA256 `e5f0ca814437da3f5be0ca0b01dc3ae9e50ea27355c41bc3927ceeea4425f0b4`，19,343 bytes，931 lines；独立审计载荷。
- `archives/customer-attraction/tools/evidence/six-optimal-query-decorrelation-primary/new-independent-audit/independent_six_decorrelation.py` — SHA256 `5d596fd1b87bae2652e92b01223f5dbc0e8ecc55f97cfbc1f11c75b914d4f375`，9,201 bytes，115 lines；独立审计算法。
- `archives/customer-attraction/tools/evidence/six-optimal-query-decorrelation-primary/missing-original-audits-boundary.json` — SHA256 `dda021de9c02ef8fbde5a8f083a1999f89e3273ab77071240d33b146f3c3f338`，2,920 bytes，67 lines；原审计证据缺口。

## 有限证书核对

- 88 客户、9 主题、6 玩家；实际路径 `(6,7,8,0,3,4)`，实际三人余局 `h=(6,7,8)`。
- 保存策略库：66,430 个有序历史键；597,870 个含自身比较，531,440 个非自身偏离，477,287 个严格劣，54,153 个平局。
- `W=86`，`OPT6=88`；3,003 个六槽无序多重集穷举后恰有四个最优支撑。
- 四支撑的精确值为：`D=28/3`；前两行 `Q=683/72`, `Δ=-11/72`；后两行 `Q=85/9`, `Δ=-1/9`。
- 四行分解 `Δ=I+J+R` 分别为 `(5/36,0,-7/24)`, `(1/12,1/24,-5/18)`, `(11/36,0,-5/12)`, `(1/12,1/6,-13/36)`。每一行的 `R` 严格为负，故不能由 `I,J≥0` 推 `Δ≥0`。

## 第一支撑的直接算术

其 cross-tail 矩阵为

```
29/3  29/3  55/6  29/3  29/3  29/3
29/3  29/3  32/3  29/3  29/3  29/3
32/3  32/3  29/3  32/3  32/3  32/3
9     9     9     9     9     9
9     9     9     9     9     9
9     9     9     9     9     9
```

对角和 56 给 `D=56/6=28/3`；全和 `683/2` 给 `Q=(683/2)/36=683/72`。这两个除法也固定了 `Δ=-11/72`，无需浮点近似。

## 证书语义

以上是一个保存的完整策略和其全部有序历史偏离比较的有限证书。独立载荷和脚本是 definition-level reconstruction；缺失边界文件说明原始两主程序/报告不可得。本轮脚本额外执行只作为一致性检查，不改写任何声明输入，不能升级为原始审计的字节复现。

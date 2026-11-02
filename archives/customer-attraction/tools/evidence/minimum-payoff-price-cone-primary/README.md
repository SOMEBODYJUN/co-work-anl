# 完整历史策略锥价格攻击：原件、复现与验收范围

本目录保存四主源：8389B README、7461B攻击器、330960B最佳JSON、28938B运行JSON。`source-manifest.json`记录冻结完整路径、blob、SHA256、两来源commit及主源/比较依赖身份。`original/`是四主源的原字节；`source-root/`按真实导入路径保存未改的攻击器、11291B真实helper及四个规范模块。后者五项不是本批新增done。

所有主源均由`python work.py clean show ID --out ...`取得。最佳JSON的2801条actions逐项解析：有序域恰为所有0至4长度七进制串，无重复、缺项或非法动作；根6，其余2800动作全0。源码、全部顶层/嵌套记录字段、38条运行记录和152轮数值均实读。没有仅凭文件名、`canonical_full_history_verified`布尔字段或旧README验收。

正式数学对象：

- [完整历史策略锥的最低收益价格攻击](../../../state/资源/完整历史策略锥的最低收益价格攻击--资源.md)：原方法、固定策略充要IC、浮点提议和精确证书层次、最低价格角色未保持的限制、完整复现和一客户解析证书。
- [十三人包与不交复制块的精确定价](../../../state/计算/十三人包与不交复制块的截断覆盖精确定价--计算.md)：README独有两份匹配原/对偶、传递群定价曲线及固定价格不交加性。
- README的对称轨道证明及有限报告另由[轨道算法](../../../state/算法/对称不交卫星块的完整SPE结果轨道递推--算法.md)和[有限报告资源](../../../state/资源/对称卫星商程序与八九人有限报告的证据合同--资源.md)负责。各项运行与计数不互相代授PASS。

## 实际执行

从仓库根运行原CLI恰一次，命令如下；仅输出前缀与冻结不同，避免覆盖原件：

```bash
python archives/customer-attraction/tools/evidence/minimum-payoff-price-cone-primary/source-root/research/workspaces/customer-attraction/R-6e3a5707f1f94c1d86bcbc61b4db4345/counterexample_search/price_cone_attack.py --players 5 --topics 7 --steps 40 --rounds 4 --seed 2026102137 --output replay_price_m5p7
```

当时stdout/stderr保存为`replay-stdout.jsonl`、`replay-stderr.txt`；后者空。stdout含正常最终摘要，原CLI自报26.949秒。首次启动会话的进程退出码没有单独留存，不伪造exit-code回执。产物位于该攻击器相邻的`replay_price_m5p7_best.json`和`replay_price_m5p7_run.json`。当前运行环境Python3.12.14、NumPy2.3.5、SciPy1.17.0。

`replay-comparison.json`记录：除计时/output参数，38条原记录连同浮点token完全相等；best除output参数全字段相等。40请求中的18/22重复树跳过、38锥/152轮及最大4/5都重现。这是原实现复现，未宣称独立LP重实现；也未把有限成功升为普遍价格上界。

独立定义级审计命令：

```bash
python archives/customer-attraction/tools/evidence/minimum-payoff-price-cone-primary/audit_saved_price_attack.py
```

已实际运行成功，输出`audit.json`。规范Fraction verifier和另外写的逐单位树遍历都通过2801历史、16806非自身IC，最小差0；核叶60000、W=OPT1、五收益1/5及可行值4/5。脚本另完整消费152轮字段、检查38个hash唯一和根计数合法，精确检查13人两份packing以及复制块端点。它不调用浮点LP或集合求解器；也不新验13人自动机或复制族完整SPE。

## 限制及全仓比较

源码在每锥初始点选最低收益已用主题，随后LP不保持最低收益行，故一般轮次仅是某个已用主题价格的下界；单调性仍让任何超过W的精确点成为最低收益候选的反证。原152轮无此正点。该限制、有限提议没有精确上界、非best未保存完整端点，均在正文和逐源回执明确保留。

实际比较了删除质量对偶、d321最低收益固定菜单锥、R977强菜单固定查询锥、旧十三人完整策略对象、不交复制弱θ构造和34客户静态模块。三种归一/最低角色/查询族不同；36客户复制块也不与34客户模块混同。旧同名`R-18-cone-cycle-20261031/original/cone_walk.py`为Walker/ConeScout版本，不能替代冻结实际导入的Engine版本。全仓检索没有同SHA四主源的既有正式清洗交付，因此本次保完整原件并建立新对象。

当前没有外审/新颖性结论，未构造新的half反例或一般定理。第二阶段关系判断随两篇正文保留，第三阶段图不自动生成。临时语义回执在`cleanup/workspaces/Boss7/resume-current/price-cone/receipts.json`，这份文件本身不证明已经checkpoint、推送或done。

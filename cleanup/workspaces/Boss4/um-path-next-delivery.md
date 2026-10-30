# 给定目标路径与支撑释放批次交付

本批23源已完整读取、比较并写逐源真实语义回执。claim由Boss串行完成，pushed提交`312c5851e9e6e7256584ab8d3e3c1da2df0dd966`；本子代理未执行Git、claim、done或sync。正文和证据当前为待Boss checkpoint的本地新文件，不能在pushed前称已远端保存。

## 精确checkpoint清单

以下八份是新正式数学正文，全部相对链接已检查存在：

1. `archives/unrelated-machines/state/定理/剪枝首步与固定批量环能垒--定理.md`
2. `archives/unrelated-machines/state/定理/永久缓冲激活与安全解锁--定理.md`
3. `archives/unrelated-machines/state/反例/历史接收预算与源端优先级死锁--反例.md`
4. `archives/unrelated-machines/state/定理/保留坏环与实际最大件初态--定理.md`
5. `archives/unrelated-machines/state/定理/任务包共同入流剥离--定理.md`
6. `archives/unrelated-machines/state/障碍/固定正支撑释放的精确近二前沿--障碍.md`
7. `archives/unrelated-machines/state/障碍/单token共同资格与端点成本--障碍.md`
8. `archives/unrelated-machines/state/计算/给定目标重配置的精确审计与版本纠错--计算.md`

其余本批自有路径：

- `archives/unrelated-machines/tools/evidence/reconfiguration-paths/`（整个新目录）
- `cleanup/workspaces/Boss4/um-path-next-receipts.json`
- `cleanup/workspaces/Boss4/um-path-next-delivery.md`

未修改共享README、共享图、他人正式对象或原代码。八对象均有描述性稳定ID、原legacy_ids及完整commit/path来源；程序/报告不是代替数学对象的targets。原源保存在证据目录`original/`，23本批与13比较依赖标明角色，共36原件；manifest逐份hash校验通过。比较依赖不额外勾选。

## 当前数学状态与关键纠错

1. 后续bundle五阶段完整证明已闭合**给定τ、任意T剪枝初态**的全程`U=max(2T,C+T/2)`路径；旧held/activation/首步稿的多件激活OPEN只属历史。正文完整保源二侧包、阶段0核心出口、共同入流保护、逆删除顺序、补集释放、逐机profile及LPT证明，不由有限测试代替。
2. 首步不需τ，保DONE/MOVE/可靠单向NO，但MOVE无改进或收敛承诺；路径仍给定完整τ。C=T的锐性指另一个指定目标，B<C时初态不在状态图；固定批量和三机严格<2前驱合同分开。
3. actual-max局部promise给eligible，标准槽实际输出满足promise；锐例未证来自同一实际槽输出，保上界/下界范围区别。
4. 一次性原接收预算整数化失败，源量或源/目标比率评分均可真死锁；受限动作耗尽和全局无安全步分开。完整参数OPT、minimax及好路径保留。
5. 旧LST族真实OPT严格<1；新单位锚块族真实OPT=1，r块少于r条零质量边释放时精确峰2−1/m。程序只全枚举单块，多块预算公式由数学独立性证明。
6. 同源threshold程序的异资格/异端成本两反例和四精确代数式单独保存；没有把公式比值小于2当LP/FPTAS恢复器。
7. 已发布未知目标PARTITION及共同容量guard正文全文比较，目标搜索/一般次二算法仍独立未解。旁读threshold审查还有别的独有数学，本批不替其全部done。
8. 旧cycle-path-hs manifest把held报告内部proof hash误写成报告hash；新manifest据inventory/字节纠正，未改他人产物。旧有限审计缺完整证明的描述由本批新正文接续，不否定其有限证据价值。

## 实际验证

- 九本批原程序及两后续bundle原程序，原字节、本目录层级依赖，实际各运行一次：全部退出0、stderr空。
- 十一stdout JSON逐字段与冻结结果完全相同，没有筛掉Python字段或数值差异。真实命令/cwd/hash、stdout/stderr及差异JSON均保存；可复现入口`replay_audits.py`。
- 新增`matrix_certificate_replay.py`从两原矩阵及证书独立枚举，不导入历史构造：四机256分配OPT1、单件minimax47/20、全部原证书状态/h/死锁剩余步匹配；三机64分配OPT1、单件及≤2件minimax9/4、首次≤2变化峰9/4。仅为两个明确fixture的新补核。
- 八份新正文frontmatter解析、source_refs完整40位commit、稳定ID互异、全部本地链接存在；36原件hash、23回执targets及角色分母核验通过。两个新driver AST解析、复现入口help通过。仅清理本次运行在自有证据目录产生的`__pycache__`。

历史审查所记修前bundle漏阶段0未取得修前代码，本轮没有重演它；现行修后实际16弧回放通过。strict_sub2前驱两文件仅全文比较，没有把其历史审计计入本轮复跑。

## done入口与关系判断

Boss先将以上精确清单checkpoint到`rebuild/research-v2`，确认pushed后，再使用`cleanup/workspaces/Boss4/um-path-next-receipts.json`完成23来源登记。回执targets只指八份正式正文。

各正式页已解释关系角色：永久阈值→安全解锁/坏环/包屏蔽；源剪枝+包屏蔽→全剪枝路径；首步环族→全程锐性；actual-max及ST输出→eligible上界；静态/优先级反例→选序合同限制；未知目标障碍→不能删τ；LST前沿和token资格→不同终态合同边界。阶段三据这些精确共同条件建边，本轮未造共享图边，不把它们迁移到CAG或WC模型。
